#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

STATIC_LOCAL_COPY_RE = re.compile(
    r"\$\(LOCAL_PATH\)/([^:\s\\]+):\$\((TARGET_COPY_OUT_[A-Z0-9_]+)\)(?:/([^\s\\]+))?"
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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_destination(variable: str, relative: str | None) -> str:
    partition = PARTITION_NAMES.get(variable, variable.lower())
    return partition if not relative else f"{partition}/{relative.lstrip('/')}"


def iter_makefiles(root: Path) -> Iterable[Path]:
    return sorted(path for path in root.rglob("*.mk") if path.is_file())


def _append_mapping(
    mappings: dict[tuple[str, str], dict[str, str]],
    source: str,
    destination: str,
    makefile: str,
) -> None:
    mappings[(source, destination)] = {
        "source": source,
        "destination": destination,
        "makefile": makefile,
    }


def _scan_foreach(
    root: Path,
    text: str,
    makefile: str,
    mappings: dict[tuple[str, str], dict[str, str]],
) -> None:
    for start in FOREACH_WILDCARD_RE.finditer(text):
        variable = start.group(1)
        glob_pattern = start.group(2).strip()
        window = text[start.end() : start.end() + 1000]
        eval_re = re.compile(
            r"\$\(\s*eval\s+PRODUCT_COPY_FILES\s*\+=\s*"
            + re.escape(f"$({variable})")
            + r":\$\((TARGET_COPY_OUT_[A-Z0-9_]+)\)/"
            + r"([^$\s\\]*?)"
            + r"\$\(\s*notdir\s+"
            + re.escape(f"$({variable})")
            + r"\s*\)"
        )
        target = eval_re.search(window)
        if target is None:
            continue
        partition = target.group(1)
        prefix = target.group(2)
        for source_path in sorted(root.glob(glob_pattern)):
            if not source_path.is_file():
                continue
            source = source_path.relative_to(root).as_posix()
            destination = normalize_destination(partition, f"{prefix}{source_path.name}")
            if destination.startswith("vendor/"):
                _append_mapping(mappings, source, destination, makefile)


def scan_local_vendor_copies(root: Path) -> list[dict[str, str]]:
    mappings: dict[tuple[str, str], dict[str, str]] = {}
    for makefile_path in iter_makefiles(root):
        text = makefile_path.read_text(encoding="utf-8", errors="replace")
        makefile = makefile_path.relative_to(root).as_posix()
        _scan_foreach(root, text, makefile, mappings)
        for match in STATIC_LOCAL_COPY_RE.finditer(text):
            source = match.group(1)
            if "$(" in source:
                continue
            destination = normalize_destination(match.group(2), match.group(3))
            if not destination.startswith("vendor/"):
                continue
            _append_mapping(mappings, source, destination, makefile)
    return sorted(mappings.values(), key=lambda row: (row["destination"], row["source"]))


def compare_mapping(device_root: Path, stock_vendor_root: Path, mapping: dict[str, str]) -> dict[str, Any]:
    source = mapping["source"]
    destination = mapping["destination"]
    device_path = device_root / source
    stock_relative = destination.removeprefix("vendor/")
    stock_path = stock_vendor_root / stock_relative

    row: dict[str, Any] = dict(mapping)
    row["stock_relative_path"] = stock_relative

    if not device_path.is_file():
        row.update(
            {
                "status": "missing_device_source",
                "device_size": None,
                "device_sha256": None,
                "stock_size": stock_path.stat().st_size if stock_path.is_file() else None,
                "stock_sha256": sha256_bytes(stock_path.read_bytes()) if stock_path.is_file() else None,
            }
        )
        return row

    device_data = device_path.read_bytes()
    row["device_size"] = len(device_data)
    row["device_sha256"] = sha256_bytes(device_data)

    if not stock_path.is_file():
        row.update({"status": "missing_in_stock", "stock_size": None, "stock_sha256": None})
        return row

    stock_data = stock_path.read_bytes()
    row["stock_size"] = len(stock_data)
    row["stock_sha256"] = sha256_bytes(stock_data)
    row["status"] = "identical" if device_data == stock_data else "different"
    return row


def build_report(device_root: Path, stock_vendor_root: Path) -> dict[str, Any]:
    rows = [compare_mapping(device_root, stock_vendor_root, mapping) for mapping in scan_local_vendor_copies(device_root)]
    counts = Counter(row["status"] for row in rows)
    summary = {
        "different": counts.get("different", 0),
        "identical": counts.get("identical", 0),
        "missing_device_source": counts.get("missing_device_source", 0),
        "missing_in_stock": counts.get("missing_in_stock", 0),
        "total": len(rows),
    }
    return {
        "schema_version": 1,
        "device_root": str(device_root),
        "stock_vendor_root": str(stock_vendor_root),
        "summary": summary,
        "rows": rows,
    }


def render_markdown(report: dict[str, Any]) -> str:
    s = report["summary"]
    lines = [
        "# Device-owned vendor config audit against RED .118",
        "",
        f"Local device → vendor mappings: **{s['total']}**.",
        f"Byte-identical to stock: **{s['identical']}**.",
        f"Different from stock: **{s['different']}**.",
        f"No stock counterpart: **{s['missing_in_stock']}**.",
        f"Missing device source: **{s['missing_device_source']}**.",
        "",
        "## Different from stock",
        "",
    ]
    different = [row for row in report["rows"] if row["status"] == "different"]
    for row in different:
        lines.append(
            f"- `{row['source']}` → `{row['destination']}` — device `{row['device_sha256']}`, stock `{row['stock_sha256']}`"
        )
    if not different:
        lines.append("- None.")
    lines.extend(["", "## Missing in stock", ""])
    missing = [row for row in report["rows"] if row["status"] == "missing_in_stock"]
    for row in missing:
        lines.append(f"- `{row['source']}` → `{row['destination']}`")
    if not missing:
        lines.append("- None.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare local device vendor-copy files with canonical stock vendor files")
    parser.add_argument("--device-root", type=Path, required=True)
    parser.add_argument("--stock-vendor-root", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--markdown", action="store_true")
    args = parser.parse_args()

    report = build_report(args.device_root, args.stock_vendor_root)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    elif args.markdown:
        print(render_markdown(report))
    else:
        print(json.dumps(report["summary"], sort_keys=True))
    return 1 if report["summary"]["missing_device_source"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
