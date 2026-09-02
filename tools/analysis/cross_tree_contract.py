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


def scan_copy_destinations(root: Path) -> dict[str, list[str]]:
    owners: dict[str, list[str]] = {}
    for path in iter_makefiles(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(root).as_posix()
        for match in COPY_DEST_RE.finditer(text):
            destination = normalize_destination(match.group(1), match.group(2))
            owners.setdefault(destination, []).append(rel)
    for paths in owners.values():
        paths.sort()
    return dict(sorted(owners.items()))


def build_report(device_root: Path, vendor_root: Path) -> dict[str, object]:
    device = scan_copy_destinations(device_root)
    vendor = scan_copy_destinations(vendor_root)
    collisions = sorted(set(device) & set(vendor))
    return {
        "schema_version": 1,
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
