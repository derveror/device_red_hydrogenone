from __future__ import annotations

import gzip
import hashlib
import io
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_twrp_boot.py"
PAGE = 4096


def align(value: int, alignment: int = PAGE) -> int:
    return (value + alignment - 1) // alignment * alignment


def cpio_newc(entries: dict[str, bytes]) -> bytes:
    out = bytearray()
    ino = 1
    for name, payload in entries.items():
        encoded_name = name.encode() + b"\0"
        fields = [ino, 0o100755, 0, 0, 1, 0, len(payload), 0, 0, 0, 0, len(encoded_name), 0]
        out += b"070701" + b"".join(f"{value:08x}".encode() for value in fields)
        out += encoded_name
        out += b"\0" * ((4 - len(out) % 4) % 4)
        out += payload
        out += b"\0" * ((4 - len(out) % 4) % 4)
        ino += 1
    trailer = b"TRAILER!!!\0"
    fields = [ino, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, len(trailer), 0]
    out += b"070701" + b"".join(f"{value:08x}".encode() for value in fields)
    out += trailer
    out += b"\0" * ((4 - len(out) % 4) % 4)
    return bytes(out)


def make_fdt() -> bytes:
    return struct.pack(">10I", 0xD00DFEED, 40, 40, 40, 40, 17, 16, 0, 0, 0)


def make_boot(path: Path, omit: str | None = None) -> tuple[str, int]:
    files = {
        "init": b"init",
        "system/bin/recovery": b"twrp",
        "system/bin/adbd": b"adbd",
        "etc/recovery.fstab": b"fstab",
        "system/etc/recovery.fstab": b"fstab",
        "fstab.qcom": b"fstab",
        "init.recovery.qcom.rc": b"rc",
        "ueventd.rc": b"ueventd",
    }
    if omit:
        files.pop(omit)
    kernel = b"synthetic-kernel" + make_fdt()
    stream = io.BytesIO()
    with gzip.GzipFile(fileobj=stream, mode="wb", mtime=0) as archive:
        archive.write(cpio_newc(files))
    ramdisk = stream.getvalue()
    kernel_sha = hashlib.sha256(kernel).hexdigest()

    header = bytearray(1632)
    header[:8] = b"ANDROID!"
    struct.pack_into("<10I", header, 8, len(kernel), 0x8000, len(ramdisk), 0x01000000, 0, 0x00F00000, 0x100, PAGE, 0, 0)
    cmdline = b"androidboot.hardware=qcom androidboot.usbcontroller=a800000.dwc3 androidboot.boot_devices=soc/1da4000.ufshc"
    header[64 : 64 + len(cmdline)] = cmdline
    image = bytearray(header)
    image += b"\0" * (PAGE - len(image))
    image += kernel
    image += b"\0" * (align(len(image)) - len(image))
    image += ramdisk
    image += b"\0" * (align(len(image)) - len(image))
    path.write_bytes(image)
    return kernel_sha, 1


class BootValidatorTests(unittest.TestCase):
    def run_validator(self, image: Path, kernel_sha: str, dtbs: int) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(image), "--expected-kernel-sha", kernel_sha, "--expected-dtb-count", str(dtbs)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_valid_boot_image_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "boot.img"
            kernel_sha, dtbs = make_boot(image)
            result = self.run_validator(image, kernel_sha, dtbs)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("BOOT IMAGE: PASS", result.stdout)

    def test_missing_recovery_fstab_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "boot.img"
            kernel_sha, dtbs = make_boot(image, "etc/recovery.fstab")
            result = self.run_validator(image, kernel_sha, dtbs)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("etc/recovery.fstab", result.stdout + result.stderr)

    def test_wrong_kernel_hash_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "boot.img"
            _, dtbs = make_boot(image)
            result = self.run_validator(image, "0" * 64, dtbs)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("kernel SHA-256", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
