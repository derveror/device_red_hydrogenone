#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path

MODULE_NAME = 'name: "libreference-ril"'
MODULE_OPEN = "cc_library_shared {"
ANCHOR = '    static_libs: ["libbase"],\n'
HEADER = '    header_libs: ["ril_headers"],\n'


def _module_bounds(text: str) -> tuple[int, int]:
    name_pos = text.find(MODULE_NAME)
    if name_pos < 0:
        raise ValueError("expected libreference-ril module was not found")
    start = text.rfind(MODULE_OPEN, 0, name_pos)
    if start < 0:
        raise ValueError("expected libreference-ril cc_library_shared block was not found")
    end = text.find("\n}", name_pos)
    if end < 0:
        raise ValueError("expected libreference-ril module terminator was not found")
    return start, end + 2


def patch_android_bp(text: str) -> tuple[str, bool]:
    start, end = _module_bounds(text)
    block = text[start:end]

    if 'header_libs: ["ril_headers"]' in block:
        return text, False

    if block.count(ANCHOR) != 1:
        raise ValueError(
            "expected libreference-ril static_libs anchor was not found exactly once"
        )

    patched_block = block.replace(ANCHOR, ANCHOR + HEADER, 1)
    return text[:start] + patched_block + text[end:], True


def default_path() -> Path:
    top = os.environ.get("ANDROID_BUILD_TOP")
    if top:
        return Path(top) / "hardware/ril/reference-ril/Android.bp"
    return Path("hardware/ril/reference-ril/Android.bp")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Add the missing ril_headers dependency to LineageOS 22.2 "
            "hardware/ril reference-ril after its Soong conversion."
        )
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=None,
        help=(
            "Android.bp to patch (defaults to "
            "$ANDROID_BUILD_TOP/hardware/ril/reference-ril/Android.bp)"
        ),
    )
    args = parser.parse_args()

    path = args.file if args.file is not None else default_path()
    if not path.is_file():
        print(f"ERROR: file not found: {path}")
        return 2

    original = path.read_text(encoding="utf-8")
    try:
        patched, changed = patch_android_bp(original)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 3

    if changed:
        path.write_text(patched, encoding="utf-8")
        print(f"PATCHED: {path}")
    else:
        print(f"ALREADY_PATCHED: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
