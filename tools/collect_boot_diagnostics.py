#!/usr/bin/env python3
"""Collect existing build/USB evidence without flashing or changing phone state."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import shutil
import struct
import subprocess
import tarfile
from datetime import datetime, timezone
from pathlib import Path

DEVICE_ROOT = Path(__file__).resolve().parents[1]


def inspect_boot(path: Path) -> dict:
    data = path.read_bytes()
    if len(data) < 1632 or data[:8] != b"ANDROID!":
        raise ValueError("missing or truncated Android boot header")
    fields = struct.unpack_from("<10I", data, 8)
    kernel_size, kernel_addr, ramdisk_size, ramdisk_addr = fields[:4]
    second_size, second_addr, tags_addr, page, version, _ = fields[4:]
    result = {"file": str(path), "size": len(data),
              "sha256": hashlib.sha256(data).hexdigest(), "header_version": version}
    if version > 2:
        result["error"] = "expected legacy RED boot header 1; payload not parsed"
        return result
    if page < 2048 or page > 65536 or page & (page - 1):
        raise ValueError(f"invalid boot page size: {page}")
    ramdisk_offset = page + ((kernel_size + page - 1) // page) * page
    if not kernel_size or len(data) < page + kernel_size or len(data) < ramdisk_offset + ramdisk_size:
        raise ValueError("truncated boot kernel or ramdisk payload")
    kernel = data[page:page + kernel_size]
    cmdline = data[64:576].split(b"\0", 1)[0] + data[608:1632].split(b"\0", 1)[0]
    result.update(page_size=page, kernel_size=kernel_size,
                  kernel_address=f"0x{kernel_addr:08x}",
                  ramdisk_size=ramdisk_size, ramdisk_address=f"0x{ramdisk_addr:08x}",
                  second_size=second_size, second_address=f"0x{second_addr:08x}",
                  tags_address=f"0x{tags_addr:08x}",
                  kernel_sha256=hashlib.sha256(kernel).hexdigest(),
                  cmdline=cmdline.decode("utf-8", errors="replace"))
    return result


def capture(directory: Path, name: str, command: list[str], timeout: int = 10) -> tuple[int, str]:
    try:
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 timeout=timeout, check=False)
        code, output = process.returncode, process.stdout
    except subprocess.TimeoutExpired as error:
        code, output = 124, (error.stdout or b"") + b"\nCOMMAND TIMED OUT\n"
    except OSError as error:
        code, output = 127, str(error).encode()
    text = output.decode("utf-8", errors="replace")
    (directory / f"{name}.txt").write_text(
        f"$ {shlex.join(command)}\nexit_status={code}\n{text}", encoding="utf-8")
    return code, text


def select_serial(output: str, requested: str | None, states: set[str]) -> str | None:
    devices = [parts[0] for line in output.splitlines()
               if len(parts := line.split()) >= 2 and parts[1] in states]
    if requested:
        return requested if requested in devices else None
    return devices[0] if len(devices) == 1 else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top", type=Path, default=DEVICE_ROOT.parents[2])
    parser.add_argument("--output-root", type=Path, help="default: <top>/logs/hydrogenone")
    parser.add_argument("--boot-image", type=Path, help="default: built out/target/product/hydrogenone/boot.img")
    parser.add_argument("--serial", default=os.environ.get("ANDROID_SERIAL"))
    parser.add_argument("--host-only", action="store_true", help="do not query adb/fastboot")
    args = parser.parse_args()
    top = args.top.resolve()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    output_root = args.output_root or top / "logs/hydrogenone"
    directory = output_root.resolve() / f"boot-diagnostics-{stamp}"
    directory.mkdir(parents=True)
    summary = {"timestamp_utc": stamp, "top": str(top), "device_queried": False,
               "note": "Static and observed evidence; successful collection is not a successful boot."}

    for label, project in (("device", DEVICE_ROOT), ("vendor", top / "vendor/red/hydrogenone"),
                           ("kernel_headers", top / "kernel/essential/msm8998")):
        capture(directory, f"{label}-revision", ["git", "-C", str(project), "rev-parse", "HEAD"])
        capture(directory, f"{label}-status", ["git", "-C", str(project), "status", "--short"])
    for source, name in ((DEVICE_ROOT / "docs/reference/cross-tree-lock.json", "cross-tree-lock.json"),
                         (DEVICE_ROOT / "prebuilt/stock_kernel.config", "selected-kernel.config"),
                         (DEVICE_ROOT / "docs/stock/h1a1000-r118/boot-image-contract.json", "stock-boot-contract.json")):
        if source.is_file():
            shutil.copyfile(source, directory / name)

    product = top / "out/target/product/hydrogenone"
    boot = args.boot_image or product / "boot.img"
    try:
        summary["boot_image"] = inspect_boot(boot)
        contract_path = directory / "stock-boot-contract.json"
        if contract_path.is_file():
            expected = json.loads(contract_path.read_text())["kernel"]["sha256"]
            summary["built_kernel_matches_selected_stock"] = summary["boot_image"].get("kernel_sha256") == expected
    except (OSError, ValueError, KeyError) as error:
        summary["boot_image_error"] = f"missing or invalid boot image: {error}"

    for relative in ("vendor/etc/init/hw/init.qcom.rc", "vendor/etc/init/hw/init.target.rc",
                     "vendor/etc/fstab.qcom", "system/etc/init/bpfloader.rc",
                     "system/etc/init/netbpfload.rc", "system/build.prop", "vendor/build.prop",
                     "recovery/root/first_stage_ramdisk/fstab.qcom"):
        source = product / relative
        if source.is_file():
            dest = directory / "installed" / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, dest)

    if not args.host_only:
        capture(directory, "usb-devices", ["lsusb"])
        _, adb_output = capture(directory, "adb-devices", ["adb", "devices", "-l"])
        _, fastboot_output = capture(directory, "fastboot-devices", ["fastboot", "devices"])
        # Resolve one phone across both transports, including inaccessible ADB
        # states. Otherwise an unrelated authorized phone could hide a RED that
        # is offline, unauthorized, or waiting in fastboot.
        states = {"device", "recovery", "offline", "unauthorized", "sideload", "bootloader", "fastboot"}
        observed = {parts[0] for line in (adb_output + "\n" + fastboot_output).splitlines()
                    if len(parts := line.split()) >= 2 and parts[1] in states}
        chosen = args.serial or (next(iter(observed)) if len(observed) == 1 else None)
        adb_serial = select_serial(adb_output, chosen, {"device", "recovery"}) if chosen else None
        fastboot_serial = select_serial(fastboot_output, chosen, {"fastboot"}) if chosen else None
        if adb_serial:
            summary["device_queried"] = True
            summary["transport"] = "adb"
            adb = ["adb", "-s", adb_serial]
            commands = {
                "properties": ["shell", "getprop"],
                "kernel-version": ["shell", "uname", "-a"],
                "kernel-cmdline": ["shell", "cat", "/proc/cmdline"],
                "mounts": ["shell", "cat", "/proc/mounts"],
                "dmesg": ["shell", "dmesg"],
                "last-kmsg": ["shell", "cat", "/proc/last_kmsg"],
                "pstore": ["pull", "/sys/fs/pstore", str(directory / "pstore")],
                "recovery-log": ["pull", "/tmp/recovery.log", str(directory / "recovery.log")],
                "logcat": ["logcat", "-b", "all", "-d", "-v", "threadtime"],
            }
            for label, command in commands.items():
                capture(directory, label, adb + command)
        elif fastboot_serial:
            summary["device_queried"] = True
            summary["transport"] = "fastboot"
            for variable in ("product", "current-slot", "unlocked", "version-bootloader",
                             "version-baseband", "reboot-reason", "slot-successful:a",
                             "slot-successful:b", "slot-unbootable:a", "slot-unbootable:b"):
                capture(directory, "fastboot-" + variable.replace(":", "-"),
                        ["fastboot", "-s", fastboot_serial, "getvar", variable])
        else:
            summary["transport"] = "none or ambiguous; inspect devices logs; use --serial for multiple devices"

    (directory / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    archive = directory.with_name(directory.name + ".tar.gz")
    with tarfile.open(archive, "w:gz") as bundle:
        bundle.add(directory, arcname=directory.name)
    print(f"Evidence archive: {archive}")
    print("No flash, erase, format, reboot, slot change or adb-root command was issued.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
