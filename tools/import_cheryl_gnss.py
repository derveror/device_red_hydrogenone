#!/usr/bin/env python3
"""Import the pinned cheryl LineageOS 22.2 Qualcomm GNSS ABI closure.

RED .118 remains the hardware/config/proprietary authority. This importer only
replaces the source implementation closure whose ABI must satisfy RED Pie-era
location blobs.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path

PINNED_CHERYL_COMMIT = "e7990dd5b94c16574c45bd241a23f1abc76b9638"
SOURCE_DIRS = ("core", "utils", "gnss", "location", "pla", "android")
STALE_GPS_PATHS = (
    "batching",
    "geofence",
    "Makefile.am",
    "configure.ac",
    "gps_vendor_board.mk",
    "gps_vendor_product.mk",
    "izat.patch",
    "loc-hal.pc.in",
)


def git_head(path: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def replace_between(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    return text[:start] + replacement + text[end:]


def update_device_mk(root: Path) -> None:
    path = root / "device.mk"
    text = path.read_text(encoding="utf-8")
    start = "# GNSS - Qualcomm MSM8998 source stack with RED .109 configuration"
    if start not in text:
        start = "# GNSS - Qualcomm MSM8998 legacy ABI source stack."
    block = """# GNSS - Qualcomm MSM8998 legacy ABI source stack.\n# Razer cheryl is the primary source-ABI donor here because its maintained\n# LineageOS 22.2 tree preserves the Pie-era Qualcomm LocApiBase ABI required\n# by RED .118 libloc_api_v02/libizat_core/liblbs_core while adapting the HAL\n# frontend to Android 15 build rules. RED stock remains configuration truth.\nPRODUCT_PACKAGES += \\\n    android.hardware.gnss@1.0-impl-qti \\\n    android.hardware.gnss@1.0-service-qti \\\n    libgnss \\\n    libgnsspps\n\n# RED GNSS configuration modules. gps.conf/flp.conf/antenna info stay owned by\n# the local prebuilt_etc definitions; RED-specific Izat/LOWI/SAP/XTWiFi files\n# are copied directly and are not replaced with Razer configuration.\nPRODUCT_PACKAGES += \\\n    flp.conf \\\n    gnss_antenna_info.conf \\\n    gps.conf\n\nPRODUCT_COPY_FILES += \\\n    $(LOCAL_PATH)/gps/izat.conf:$(TARGET_COPY_OUT_VENDOR)/etc/izat.conf \\\n    $(LOCAL_PATH)/gps/lowi.conf:$(TARGET_COPY_OUT_VENDOR)/etc/lowi.conf \\\n    $(LOCAL_PATH)/gps/sap.conf:$(TARGET_COPY_OUT_VENDOR)/etc/sap.conf \\\n    $(LOCAL_PATH)/gps/xtwifi.conf:$(TARGET_COPY_OUT_VENDOR)/etc/xtwifi.conf\n\n"""
    text = replace_between(text, start, "# Health", block)
    path.write_text(text, encoding="utf-8")


def update_manifest(root: Path) -> None:
    path = root / "manifest.xml"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r'\s*<hal format="hidl">\s*<name>android\.hardware\.gnss</name>.*?</hal>\s*',
        "\n",
        text,
        flags=re.S,
    )
    block = """    <hal format="hidl">\n        <name>android.hardware.gnss</name>\n        <transport>hwbinder</transport>\n        <version>1.0</version>\n        <interface>\n            <name>IGnss</name>\n            <instance>default</instance>\n        </interface>\n    </hal>\n"""
    needle = '    <hal format="hidl">\n        <name>android.hardware.graphics.allocator</name>'
    if needle not in text:
        raise SystemExit("graphics allocator manifest anchor not found")
    text = text.replace(needle, block + needle, 1)
    path.write_text(text, encoding="utf-8")


def update_manifest_test(root: Path) -> None:
    path = root / "tests/test_android15_manifest_contract.py"
    text = path.read_text(encoding="utf-8")
    if '"android.hardware.gnss@1.0::IGnss/default"' not in text:
        text = text.replace(
            '    "android.hardware.gatekeeper@1.0::IGatekeeper/default",\n',
            '    "android.hardware.gatekeeper@1.0::IGatekeeper/default",\n'
            '    "android.hardware.gnss@1.0::IGnss/default",\n',
        )
    text = re.sub(
        r'# The local QTI GNSS source service owns its own XML through vintf_fragments in\n'
        r'# gps/android/2\.1/Android\.bp, so duplicating GNSS here would create two owners\.\n'
        r'SELF_FRAGMENTED_SOURCE_HAL_NAMES = \{"android\.hardware\.gnss"\}\n',
        '# The cheryl-compatible QTI GNSS 1.0 source service has no VINTF fragment;\n'
        '# its IGnss/default instance is therefore owned by the device manifest above.\n'
        'SELF_FRAGMENTED_SOURCE_HAL_NAMES: set[str] = set()\n',
        text,
    )
    path.write_text(text, encoding="utf-8")


def update_donor_matrix(root: Path) -> None:
    path = root / "DONOR_MATRIX.md"
    text = path.read_text(encoding="utf-8")
    if "## Primary for GNSS/location ABI" in text:
        return
    section = """\n## Primary for GNSS/location ABI: Razer Phone (`cheryl`)\nUse `cheryl` before `mata` for the Qualcomm GNSS/location source ABI. The Razer\nPhone launched on Android 7.1.1 and its final official Android release was 9.0,\nwhich aligns with RED `.118` Android 9 vendor consumers. Its maintained\nLineageOS 22.2 tree deliberately preserves the legacy Qualcomm `LocApiBase` ABI\nwhile adapting the source stack to Android 15 build rules.\n\nFor Hydrogen One GNSS this means:\n- RED `.118` remains hardware/configuration/proprietary-blob truth;\n- `cheryl` is the first donor for `libgps.utils`, `libloc_core`,\n  `liblocation_api`, `libgnss`, and the QTI GNSS HIDL frontend;\n- `mata`, OnePlus msm8998 and Nubia remain cross-checks for Android 15 platform\n  contracts, ownership and generic msm8998 integration;\n- never copy Razer device identity, partitioning, kernel DTBs, or GPS configs.\n"""
    marker = "\n## Secondary: OnePlus 5/5T"
    if marker not in text:
        raise SystemExit("donor matrix insertion anchor not found")
    path.write_text(text.replace(marker, section + marker, 1), encoding="utf-8")


def update_manifest_doc(root: Path) -> None:
    path = root / "docs/ANDROID15_MANIFEST_CONTRACT.md"
    text = path.read_text(encoding="utf-8")
    if "- GNSS 1.0 / `IGnss/default`;" not in text:
        text = text.replace(
            "- gatekeeper 1.0 / `IGatekeeper/default`;\n",
            "- gatekeeper 1.0 / `IGatekeeper/default`;\n- GNSS 1.0 / `IGnss/default`;\n",
            1,
        )
    start = "The versions follow the actual LineageOS 22.2 packages selected by `device.mk`"
    vendor = "## Vendor-owned HALs"
    if start in text:
        a = text.index(start)
        b = text.index(vendor, a)
        replacement = """The versions follow the actual LineageOS 22.2 packages selected by `device.mk`. GNSS is the intentional exception to the newer `mata` frontend: Hydrogen One uses the maintained `cheryl` LineageOS 22.2 Qualcomm GPS closure because RED `.118` proprietary location consumers require the older Pie-era `LocApiBase` ABI.\n\n## GNSS source HAL ownership\n\nThe active source service is:\n\n```text\ngps/android/Android.bp\nandroid.hardware.gnss@1.0-service-qti\n```\n\nUnlike the removed 2.1 frontend, it has no private VINTF fragment, so `manifest.xml` owns `android.hardware.gnss@1.0::IGnss/default`. Vendor tests continue to forbid the retained Android 9 stock GNSS wrapper from registering the same default instance.\n\n"""
        text = text[:a] + replacement + text[b:]
    path.write_text(text, encoding="utf-8")


def prune_gps_etc(root: Path) -> None:
    path = root / "gps/etc/Android.bp"
    text = path.read_text(encoding="utf-8")
    blocks = []
    for match in re.finditer(r"prebuilt_etc\s*\{.*?\n\}", text, re.S):
        block = match.group(0)
        if any(f'name: "{name}"' in block for name in ("gps.conf", "flp.conf", "gnss_antenna_info.conf")):
            blocks.append(block.strip())
    if len(blocks) != 3:
        raise SystemExit(f"expected 3 RED GNSS config modules, found {len(blocks)}")
    path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
    seccomp = root / "gps/etc/seccomp_policy"
    if seccomp.exists():
        shutil.rmtree(seccomp)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--cheryl", type=Path, required=True)
    parser.add_argument("--allow-unpinned-donor", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    donor = args.cheryl.resolve()

    head = git_head(donor)
    if head and head != PINNED_CHERYL_COMMIT and not args.allow_unpinned_donor:
        raise SystemExit(f"cheryl donor must be {PINNED_CHERYL_COMMIT}, got {head}")

    donor_gps = donor / "gps"
    if not donor_gps.is_dir():
        raise SystemExit(f"missing donor GPS tree: {donor_gps}")

    gps = root / "gps"
    for name in SOURCE_DIRS:
        dst = gps / name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(donor_gps / name, dst)
    shutil.copy2(donor_gps / "Android.bp", gps / "Android.bp")

    for relative in STALE_GPS_PATHS:
        path = gps / relative
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()

    prune_gps_etc(root)
    update_device_mk(root)
    update_manifest(root)
    update_manifest_test(root)
    update_donor_matrix(root)
    update_manifest_doc(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
