#!/usr/bin/env python3
"""Verify split stock parts and reconstruct the original archive atomically."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from pathlib import Path
from typing import Sequence

_READ_CHUNK_SIZE = 1024 * 1024
_SHA256_RE = re.compile(r"[0-9a-fA-F]{64}")


def _validate_sha256(value: str, label: str) -> str:
    if _SHA256_RE.fullmatch(value) is None:
        raise ValueError(f"invalid SHA-256 for {label}: {value}")
    return value.lower()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(_READ_CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_part_filename(filename: str) -> None:
    if (
        not filename
        or filename in {".", ".."}
        or "/" in filename
        or "\\" in filename
        or Path(filename).name != filename
    ):
        raise ValueError(f"unsafe part filename: {filename}")


def _read_manifest(manifest_path: Path) -> list[tuple[str, str]]:
    try:
        lines = manifest_path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise ValueError(f"cannot read part manifest {manifest_path}: {exc}") from exc
    if not lines:
        raise ValueError("part manifest is empty")

    entries: list[tuple[str, str]] = []
    seen: set[str] = set()
    for line_number, raw_line in enumerate(lines, start=1):
        digest, separator, filename = raw_line.partition("  ")
        if not separator or not digest or not filename:
            raise ValueError(
                f"invalid manifest line {line_number}: expected '<sha256>  <filename>'"
            )
        digest = _validate_sha256(digest, f"manifest line {line_number}")
        _validate_part_filename(filename)
        if filename in seen:
            raise ValueError(f"duplicate part: {filename}")
        seen.add(filename)
        entries.append((digest, filename))
    return entries


def reconstruct(
    parts_dir: Path,
    manifest_path: Path,
    output_path: Path,
    expected_sha256: str,
    *,
    replace: bool = False,
) -> None:
    parts_dir = Path(parts_dir)
    manifest_path = Path(manifest_path)
    output_path = Path(output_path)
    expected_sha256 = _validate_sha256(expected_sha256, "final archive")

    if output_path.exists() and not replace:
        raise FileExistsError(f"output already exists: {output_path}")

    entries = _read_manifest(manifest_path)
    verified_parts: list[Path] = []
    for expected, filename in entries:
        part = parts_dir / filename
        if not part.is_file():
            raise ValueError(f"missing part: {filename}")
        actual = _sha256_file(part)
        if actual != expected:
            raise ValueError(f"{filename}: expected {expected}, got {actual}")
        verified_parts.append(part)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    partial = output_path.with_name(output_path.name + ".partial")
    if partial.exists():
        raise FileExistsError(f"partial output already exists: {partial}")

    try:
        with partial.open("xb") as destination:
            for part in verified_parts:
                with part.open("rb") as source:
                    for chunk in iter(lambda: source.read(_READ_CHUNK_SIZE), b""):
                        destination.write(chunk)
            destination.flush()
            os.fsync(destination.fileno())

        actual_output_hash = _sha256_file(partial)
        if actual_output_hash != expected_sha256:
            raise ValueError(
                f"final archive: expected {expected_sha256}, got {actual_output_hash}"
            )
        partial.replace(output_path)
    except Exception:
        partial.unlink(missing_ok=True)
        raise

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verify split-file hashes and reconstruct a stock archive atomically."
    )
    parser.add_argument("--parts-dir", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--replace", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        reconstruct(
            args.parts_dir,
            args.manifest,
            args.output,
            args.expected_sha256,
            replace=args.replace,
        )
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"reconstructed and verified: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
