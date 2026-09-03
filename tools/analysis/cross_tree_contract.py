#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable

COPY_DEST_RE = re.compile(
    r":\$\((TARGET_COPY_OUT_[A-Z0-9_]+)\)(?:/([^\s\\]+))?"
)
FOREACH_WILDCARD_RE = re.compile(
    r"\$\(\s*foreach\s+([A-Za-z_][A-Za-z0-9_]*),"
    r"\$\(\s*wildcard\s+\$\(LOCAL_PATH\)/([^)]+)\),",
    re.S,
)

PARTITION_NAMES = {
    "TARGET_COPY_OUT_VENDOR": "vendor",
    "TARGET_COPY_OUT_SYSTEM": "system",
    "TARGET_COPY_OUT_PRODUCT": "product",
    "TARGET_COPY_OUT_SYSTEM_EXT": "system_ext",
    "TARGET_COPY_OUT_ODM": "odm",
    "TARGET_COPY_OUT_RECOVERY": "recovery",
}


def iter_makefiles(root: Path) -> Iterable[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*.mk") if path.is_file())


def normalize_destination(variable: str, relative: str | None) -> str:
    partition = PARTITION_NAMES.get(variable, variable.lower())
    return partition if not relative else f"{partition}/{relative.lstrip('/')}"


def _add_owner(owners: dict[str, list[str]], destination: str, makefile: str) -> None:
    paths = owners.setdefault(destination, [])
    if makefile not in paths:
        paths.append(makefile)


def _scan_foreach_wildcards(
    root: Path,
    text: str,
    makefile: str,
    owners: dict[str, list[str]],
) -> None:
    """Expand the simple foreach/wildcard/notdir copy pattern used by device.mk.

    This is intentionally not a GNU Make interpreter. It only recognizes the
    concrete pattern used by Android device trees to copy every file matching a
    LOCAL_PATH-relative glob into a fixed TARGET_COPY_OUT_* directory while
    retaining each source basename.
    """

    for start in FOREACH_WILDCARD_RE.finditer(text):
        variable = start.group(1)
        glob_pattern = start.group(2).strip()
        window = text[start.end() : start.end() + 1000]
        source_ref = re.escape(f"$({variable})")
        notdir_ref = rf"(?:{re.escape(f'$({variable})')}|{re.escape(f'${variable}')})"
        eval_re = re.compile(
            r"\$\(\s*eval\s+PRODUCT_COPY_FILES\s*\+=\s*"
            + source_ref
            + r":\$\((TARGET_COPY_OUT_[A-Z0-9_]+)\)/"
            + r"([^$\s\\]*?)"
            + r"\$\(\s*notdir\s+"
            + notdir_ref
            + r"\s*\)"
        )
        target = eval_re.search(window)
        if target is None:
            continue
        partition_variable = target.group(1)
        destination_prefix = target.group(2)
        for source in sorted(root.glob(glob_pattern)):
            if not source.is_file():
                continue
            destination = normalize_destination(
                partition_variable,
                f"{destination_prefix}{source.name}",
            )
            _add_owner(owners, destination, makefile)


def scan_copy_destinations(root: Path) -> dict[str, list[str]]:
    owners: dict[str, list[str]] = {}
    for path in iter_makefiles(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(root).as_posix()

        _scan_foreach_wildcards(root, text, rel, owners)

        for match in COPY_DEST_RE.finditer(text):
            relative = match.group(2)
            # A raw match that still contains Make expansion syntax is not a
            # concrete output path. Supported foreach forms are expanded above.
            if relative and "$(" in relative:
                continue
            destination = normalize_destination(match.group(1), relative)
            _add_owner(owners, destination, rel)

    for paths in owners.values():
        paths.sort()
    return dict(sorted(owners.items()))


def build_report(device_root: Path, vendor_root: Path) -> dict[str, object]:
    device = scan_copy_destinations(device_root)
    vendor = scan_copy_destinations(vendor_root)
    collisions = sorted(set(device) & set(vendor))
    return {
        "schema_version": 2,
        "device_root": str(device_root),
        "vendor_root": str(vendor_root),
        "device_copy_destinations": device,
        "vendor_copy_destinations": vendor,
        "copy_destination_collisions": collisions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Detect cross-tree PRODUCT_COPY_FILES destination ownership collisions"
    )
    parser.add_argument("--device-root", type=Path, required=True)
    parser.add_argument("--vendor-root", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report(args.device_root, args.vendor_root)
    collisions = report["copy_destination_collisions"]
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    elif collisions:
        print("cross-tree PRODUCT_COPY_FILES collisions:")
        for destination in collisions:
            print(f"- {destination}")
    else:
        print("cross-tree PRODUCT_COPY_FILES ownership: no collisions")
    return 1 if collisions else 0


if __name__ == "__main__":
    raise SystemExit(main())
