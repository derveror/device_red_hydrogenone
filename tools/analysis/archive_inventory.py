#!/usr/bin/env python3
"""Create deterministic metadata inventories for ZIP reference archives."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Sequence
from zipfile import BadZipFile, ZipFile, ZipInfo

_READ_CHUNK_SIZE = 1024 * 1024


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(_READ_CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_root(infos: list[ZipInfo]) -> str | None:
    parts = [PurePosixPath(info.filename).parts for info in infos]
    if not parts or any(len(item) < 2 for item in parts):
        return None
    roots = {item[0] for item in parts}
    return next(iter(roots)) if len(roots) == 1 else None


def inventory_zip(path: Path) -> dict[str, object]:
    path = Path(path)
    try:
        with ZipFile(path) as archive:
            infos = [info for info in archive.infolist() if not info.is_dir()]
            root = normalized_root(infos)
            files: list[dict[str, object]] = []
            for info in infos:
                relative = info.filename
                if root and relative.startswith(root + "/"):
                    relative = relative[len(root) + 1 :]
                files.append(
                    {
                        "path": relative,
                        "size_bytes": info.file_size,
                        "sha256": sha256_bytes(archive.read(info)),
                        "zip_mode": (info.external_attr >> 16) & 0xFFFF,
                    }
                )
            files.sort(key=lambda item: str(item["path"]))
            comment = archive.comment.decode("utf-8", "replace").strip()
    except (BadZipFile, OSError) as exc:
        raise ValueError(f"cannot inventory ZIP {path}: {exc}") from exc

    return {
        "archive": path.name,
        "archive_sha256": sha256_file(path),
        "archive_size_bytes": path.stat().st_size,
        "embedded_source_commit": comment or None,
        "root_directory": root,
        "file_count": len(files),
        "uncompressed_size_bytes": sum(int(item["size_bytes"]) for item in files),
        "files": files,
    }


def inventory_many(paths: Sequence[Path]) -> list[dict[str, object]]:
    return [inventory_zip(path) for path in sorted(paths, key=lambda value: value.name)]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inventory ZIP archives without extracting proprietary contents."
    )
    parser.add_argument("archives", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="omit per-file records while retaining archive-level counts and hashes",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    payload = inventory_many(args.archives)
    if args.summary_only:
        payload = [
            {key: value for key, value in record.items() if key != "files"}
            for record in payload
        ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
