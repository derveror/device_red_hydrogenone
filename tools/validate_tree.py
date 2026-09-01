#!/usr/bin/env python3
"""Validate the immutable RED Hydrogen One TWRP device-tree contract."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

EXPECTED_KERNEL_SHA = "6cf3a70ece8b32dcd6bccf9db1a22c1da29b9b37fe67cc0e4ec9b4f87fec2426"
REQUIRED_FILES = (
    "Android.bp",
    "AndroidProducts.mk",
    "BoardConfig.mk",
    "twrp_device.mk",
    "twrp_hydrogenone.mk",
    "prebuilt/Image.gz-dtb",
    "recovery/root/fstab.qcom",
    "recovery/root/etc/recovery.fstab",
    "recovery/root/system/etc/recovery.fstab",
    "recovery/root/init.recovery.qcom.rc",
    "recovery/root/ueventd.rc",
)
BOARD_CONTRACT = (
    "TARGET_BOARD_PLATFORM := msm8998",
    "TARGET_PREBUILT_KERNEL := $(DEVICE_PATH)/prebuilt/Image.gz-dtb",
    "BOARD_KERNEL_IMAGE_NAME := Image.gz-dtb",
    "BOARD_BOOT_HEADER_VERSION := 0",
    "BOARD_KERNEL_PAGESIZE := 4096",
    "BOARD_KERNEL_OFFSET := 0x00008000",
    "BOARD_RAMDISK_OFFSET := 0x01000000",
    "BOARD_SECOND_OFFSET := 0x00f00000",
    "BOARD_TAGS_OFFSET := 0x00000100",
    "BOARD_BOOTIMAGE_PARTITION_SIZE := 67108864",
    "BOARD_USES_RECOVERY_AS_BOOT := true",
    "TARGET_NO_RECOVERY := true",
    "TW_INCLUDE_REPACKTOOLS := true",
)
FORBIDDEN_DONORS = ("mata", "walleye", "taimen", "cheeseburger", "dumpling")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("tree", nargs="?", default=".")
    root = Path(parser.parse_args().tree).resolve()
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    board_path = root / "BoardConfig.mk"
    board = board_path.read_text(errors="replace") if board_path.is_file() else ""
    for expected in BOARD_CONTRACT:
        if expected not in board:
            errors.append(f"BoardConfig contract missing: {expected}")

    products = (root / "AndroidProducts.mk").read_text(errors="replace")
    if "twrp_hydrogenone-eng" not in products:
        errors.append("AndroidProducts.mk does not expose twrp_hydrogenone-eng")

    kernel = root / "prebuilt/Image.gz-dtb"
    if kernel.is_file():
        actual = sha256(kernel)
        if actual != EXPECTED_KERNEL_SHA:
            errors.append(f"kernel SHA-256 mismatch: expected {EXPECTED_KERNEL_SHA}, got {actual}")
        if kernel.stat().st_size < 20 * 1024 * 1024:
            errors.append("kernel is implausibly small; Git LFS probably did not download it")

    twrp_fstab_path = root / "recovery/root/system/etc/recovery.fstab"
    twrp_fstab = twrp_fstab_path.read_text(errors="replace") if twrp_fstab_path.is_file() else ""
    for mount in ("/boot", "/system_root", "/vendor", "/data", "/misc", "/persist"):
        line = next((line for line in twrp_fstab.splitlines() if line.split() and line.split()[0] == mount), "")
        if not line:
            errors.append(f"TWRP fstab missing mount: {mount}")
        elif mount in ("/boot", "/system_root", "/vendor") and "slotselect" not in line:
            errors.append(f"TWRP fstab mount lacks slotselect: {mount}")

    fs_mgr_path = root / "recovery/root/fstab.qcom"
    fs_mgr = fs_mgr_path.read_text(errors="replace") if fs_mgr_path.is_file() else ""
    if "/dev/block/platform/soc/1da4000.ufshc" not in fs_mgr:
        errors.append("fstab.qcom does not use the verified H1A1000 UFS path")
    if "first_stage_mount" not in fs_mgr:
        errors.append("fstab.qcom lacks first_stage_mount entries")

    critical_paths = (
        "AndroidProducts.mk",
        "BoardConfig.mk",
        "twrp_device.mk",
        "twrp_hydrogenone.mk",
        "recovery/root/fstab.qcom",
        "recovery/root/system/etc/recovery.fstab",
        "recovery/root/init.recovery.qcom.rc",
    )
    critical = "\n".join(
        (root / path).read_text(errors="replace")
        for path in critical_paths
        if (root / path).is_file()
    ).lower()
    for donor in FORBIDDEN_DONORS:
        if donor in critical:
            errors.append(f"donor identifier in critical configuration: {donor}")

    if errors:
        print("TREE CONTRACT: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("TREE CONTRACT: PASS")
    print(f"- kernel SHA-256: {EXPECTED_KERNEL_SHA}")
    print("- recovery-as-boot/A-B/UFS/fstab contract verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
