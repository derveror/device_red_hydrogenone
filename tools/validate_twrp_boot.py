#!/usr/bin/env python3
"""Validate a built H1A1000 TWRP recovery-as-boot image."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import struct
import sys
from dataclasses import dataclass
from pathlib import Path

ANDROID_MAGIC = b"ANDROID!"
EXPECTED_KERNEL_SHA = "6cf3a70ece8b32dcd6bccf9db1a22c1da29b9b37fe67cc0e4ec9b4f87fec2426"
EXPECTED_DTB_COUNT = 60
MAX_BOOT_SIZE = 67_108_864
FDT_MAGIC = b"\xd0\x0d\xfe\xed"


def align(value: int, alignment: int) -> int:
    return (value + alignment - 1) // alignment * alignment


@dataclass(frozen=True)
class BootHeaderV0:
    kernel_size: int
    kernel_addr: int
    ramdisk_size: int
    ramdisk_addr: int
    second_size: int
    second_addr: int
    tags_addr: int
    page_size: int
    header_version: int
    os_version: int
    cmdline: str


def parse_header(data: bytes) -> BootHeaderV0:
    if len(data) < 1632:
        raise ValueError("image is smaller than an Android boot header v0")
    if data[:8] != ANDROID_MAGIC:
        raise ValueError("missing ANDROID! boot magic")
    fields = struct.unpack_from("<10I", data, 8)
    cmdline = (data[64:576] + data[608:1632]).split(b"\0", 1)[0].decode(errors="replace")
    return BootHeaderV0(*fields, cmdline)


def parse_newc(payload: bytes) -> set[str]:
    names: set[str] = set()
    offset = 0
    while offset + 110 <= len(payload):
        header = payload[offset : offset + 110]
        if header[:6] not in (b"070701", b"070702"):
            raise ValueError(f"unsupported CPIO record at offset {offset}: {header[:6]!r}")
        try:
            values = [int(header[6 + i * 8 : 14 + i * 8], 16) for i in range(13)]
        except ValueError as exc:
            raise ValueError(f"invalid CPIO header at offset {offset}") from exc
        file_size = values[6]
        name_size = values[11]
        offset += 110
        if name_size <= 0 or offset + name_size > len(payload):
            raise ValueError("invalid CPIO filename size")
        name = payload[offset : offset + name_size].rstrip(b"\0").decode(errors="replace").removeprefix("./")
        offset = align(offset + name_size, 4)
        if name == "TRAILER!!!":
            break
        names.add(name)
        if offset + file_size > len(payload):
            raise ValueError(f"CPIO payload for {name!r} exceeds ramdisk")
        offset = align(offset + file_size, 4)
    return names


def valid_fdt_count(kernel: bytes) -> int:
    count = 0
    start = 0
    while True:
        offset = kernel.find(FDT_MAGIC, start)
        if offset < 0:
            return count
        if offset + 8 <= len(kernel):
            total_size = struct.unpack_from(">I", kernel, offset + 4)[0]
            if 40 <= total_size <= len(kernel) - offset:
                count += 1
        start = offset + 4


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("--expected-kernel-sha", default=EXPECTED_KERNEL_SHA)
    parser.add_argument("--expected-dtb-count", type=int, default=EXPECTED_DTB_COUNT)
    parser.add_argument("--max-size", type=int, default=MAX_BOOT_SIZE)
    args = parser.parse_args()
    errors: list[str] = []

    try:
        data = args.image.read_bytes()
    except OSError as exc:
        print(f"BOOT IMAGE: FAIL\n- cannot read {args.image}: {exc}")
        return 1
    if len(data) > args.max_size:
        errors.append(f"image size {len(data)} exceeds boot partition {args.max_size}")

    try:
        header = parse_header(data)
    except ValueError as exc:
        print(f"BOOT IMAGE: FAIL\n- {exc}")
        return 1

    expected_header = {
        "kernel_addr": 0x00008000,
        "ramdisk_addr": 0x01000000,
        "second_addr": 0x00F00000,
        "tags_addr": 0x00000100,
        "page_size": 4096,
        "header_version": 0,
    }
    for field, expected in expected_header.items():
        actual = getattr(header, field)
        if actual != expected:
            errors.append(f"{field}: expected {expected:#x}, got {actual:#x}")

    kernel_offset = header.page_size
    ramdisk_offset = align(kernel_offset + header.kernel_size, header.page_size)
    kernel_end = kernel_offset + header.kernel_size
    ramdisk_end = ramdisk_offset + header.ramdisk_size
    if header.kernel_size <= 0 or header.ramdisk_size <= 0:
        errors.append("kernel or ramdisk is empty")
    if kernel_end > len(data) or ramdisk_end > len(data):
        errors.append("kernel/ramdisk range exceeds image size")
        kernel = b""
        ramdisk = b""
    else:
        kernel = data[kernel_offset:kernel_end]
        ramdisk = data[ramdisk_offset:ramdisk_end]

    if kernel:
        actual_sha = hashlib.sha256(kernel).hexdigest()
        if actual_sha != args.expected_kernel_sha:
            errors.append(f"kernel SHA-256: expected {args.expected_kernel_sha}, got {actual_sha}")
        actual_dtbs = valid_fdt_count(kernel)
        if actual_dtbs != args.expected_dtb_count:
            errors.append(f"appended FDT count: expected {args.expected_dtb_count}, got {actual_dtbs}")

    names: set[str] = set()
    if ramdisk:
        if not ramdisk.startswith(b"\x1f\x8b"):
            errors.append("ramdisk is not gzip-compressed")
        else:
            try:
                names = parse_newc(gzip.decompress(ramdisk))
            except (OSError, EOFError, ValueError) as exc:
                errors.append(f"cannot parse gzip/newc ramdisk: {exc}")

    mandatory = {
        "init",
        "etc/recovery.fstab",
        "system/etc/recovery.fstab",
        "fstab.qcom",
        "init.recovery.qcom.rc",
        "ueventd.rc",
    }
    for name in sorted(mandatory - names):
        errors.append(f"ramdisk missing: {name}")
    if not ({"system/bin/recovery", "sbin/recovery"} & names):
        errors.append("ramdisk missing recovery executable")
    if not ({"system/bin/adbd", "sbin/adbd"} & names):
        errors.append("ramdisk missing adbd")

    for token in (
        "androidboot.hardware=qcom",
        "androidboot.boot_devices=soc/1da4000.ufshc",
        "androidboot.usbcontroller=a800000.dwc3",
    ):
        if token not in header.cmdline:
            errors.append(f"cmdline missing: {token}")

    if errors:
        print("BOOT IMAGE: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("BOOT IMAGE: PASS")
    print(f"- image size: {len(data)} / {args.max_size}")
    print(f"- kernel SHA-256: {args.expected_kernel_sha}")
    print(f"- appended FDTs: {args.expected_dtb_count}")
    print(f"- ramdisk entries: {len(names)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
