#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable, Iterator

COPY_DEST_RE = re.compile(
    r":\$\((TARGET_COPY_OUT_[A-Z0-9_]+)\)(?:/([^\s\\]+))?"
)
FOREACH_WILDCARD_RE = re.compile(
    r"\$\(\s*foreach\s+([A-Za-z_][A-Za-z0-9_]*),"
    r"\$\(\s*wildcard\s+\$\(LOCAL_PATH\)/([^)]+)\),",
    re.S,
)
BP_MODULE_START_RE = re.compile(r"(?m)^([A-Za-z_][A-Za-z0-9_]*)\s*\{")
BP_NAME_RE = re.compile(r'\bname\s*:\s*"([^"]+)"')
BP_SRCS_RE = re.compile(r"\bsrcs\s*:\s*\[(.*?)\]", re.S)
BP_STRING_RE = re.compile(r'"([^"]+)"')
SUPPORTED_VENDOR_PREBUILT_TYPES = {
    "cc_prebuilt_binary",
    "cc_prebuilt_library_shared",
}

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


def iter_blueprints(root: Path) -> Iterable[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("Android.bp") if path.is_file())


def normalize_destination(variable: str, relative: str | None) -> str:
    partition = PARTITION_NAMES.get(variable, variable.lower())
    return partition if not relative else f"{partition}/{relative.lstrip('/')}"


def _add_owner(owners: dict[str, list[str]], destination: str, owner: str) -> None:
    paths = owners.setdefault(destination, [])
    if owner not in paths:
        paths.append(owner)


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


def _find_matching_brace(text: str, open_index: int) -> int:
    """Return the index just after a Blueprint block's matching closing brace."""

    depth = 0
    in_string = False
    escaped = False
    line_comment = False
    block_comment = False
    i = open_index

    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""

        if line_comment:
            if ch == "\n":
                line_comment = False
            i += 1
            continue
        if block_comment:
            if ch == "*" and nxt == "/":
                block_comment = False
                i += 2
            else:
                i += 1
            continue
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            i += 1
            continue

        if ch == "/" and nxt == "/":
            line_comment = True
            i += 2
            continue
        if ch == "/" and nxt == "*":
            block_comment = True
            i += 2
            continue
        if ch == '"':
            in_string = True
            i += 1
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1

    raise ValueError("unterminated Android.bp module block")


def iter_blueprint_modules(text: str) -> Iterator[tuple[str, str]]:
    """Yield top-level Blueprint module type and block text."""

    cursor = 0
    while True:
        match = BP_MODULE_START_RE.search(text, cursor)
        if match is None:
            return
        open_index = text.find("{", match.start(), match.end())
        end = _find_matching_brace(text, open_index)
        yield match.group(1), text[match.start() : end]
        cursor = end


def scan_vendor_soong_install_outputs(root: Path) -> dict[str, list[str]]:
    """Infer outputs for generated RED proprietary ELF Soong modules.

    The vendor generator preserves the canonical stock path in each prebuilt
    src entry (proprietary/vendor/...). For the supported cc_prebuilt module
    types, that stock-relative path is the intended vendor install output.
    This avoids pretending to be a full Soong evaluator while still checking
    the exact generated contract used by this vendor tree.
    """

    outputs: dict[str, list[str]] = {}
    for path in iter_blueprints(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(root).as_posix()
        for module_type, block in iter_blueprint_modules(text):
            if module_type not in SUPPORTED_VENDOR_PREBUILT_TYPES:
                continue
            if not re.search(r"\b(?:soc_specific|vendor)\s*:\s*true\b", block):
                continue
            name_match = BP_NAME_RE.search(block)
            if name_match is None:
                continue
            module_name = name_match.group(1)
            owner = f"{module_name}@{rel}"
            for src_array in BP_SRCS_RE.finditer(block):
                for src in BP_STRING_RE.findall(src_array.group(1)):
                    if not src.startswith("proprietary/vendor/"):
                        continue
                    destination = src[len("proprietary/") :]
                    _add_owner(outputs, destination, owner)

    for owners in outputs.values():
        owners.sort()
    return dict(sorted(outputs.items()))


def build_report(device_root: Path, vendor_root: Path) -> dict[str, object]:
    device = scan_copy_destinations(device_root)
    vendor = scan_copy_destinations(vendor_root)
    vendor_soong = scan_vendor_soong_install_outputs(vendor_root)

    copy_collisions = sorted(set(device) & set(vendor))
    device_copy_vs_soong = sorted(set(device) & set(vendor_soong))
    vendor_copy_vs_soong = sorted(set(vendor) & set(vendor_soong))
    copy_vs_soong = sorted(set(device_copy_vs_soong) | set(vendor_copy_vs_soong))
    vendor_soong_output_collisions = sorted(
        destination
        for destination, owners in vendor_soong.items()
        if len(set(owners)) > 1
    )
    install_collisions = sorted(
        set(copy_collisions)
        | set(copy_vs_soong)
        | set(vendor_soong_output_collisions)
    )

    return {
        "schema_version": 3,
        "device_root": str(device_root),
        "vendor_root": str(vendor_root),
        "device_copy_destinations": device,
        "vendor_copy_destinations": vendor,
        "vendor_soong_install_outputs": vendor_soong,
        "copy_destination_collisions": copy_collisions,
        "device_copy_vs_vendor_soong_collisions": device_copy_vs_soong,
        "vendor_copy_vs_vendor_soong_collisions": vendor_copy_vs_soong,
        "copy_vs_vendor_soong_collisions": copy_vs_soong,
        "vendor_soong_output_collisions": vendor_soong_output_collisions,
        "install_destination_collisions": install_collisions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Detect device/vendor Make and generated Soong install-output collisions"
    )
    parser.add_argument("--device-root", type=Path, required=True)
    parser.add_argument("--vendor-root", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report(args.device_root, args.vendor_root)
    collisions = report["install_destination_collisions"]
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    elif collisions:
        print("cross-tree install-output collisions:")
        for destination in collisions:
            print(f"- {destination}")
    else:
        print("cross-tree install-output ownership: no collisions")
    return 1 if collisions else 0


if __name__ == "__main__":
    raise SystemExit(main())
