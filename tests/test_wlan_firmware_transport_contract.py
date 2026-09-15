from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


DEVICE_ROOT = Path(__file__).resolve().parents[1]
ANDROID_ROOT = DEVICE_ROOT.parents[2]
VENDOR_ROOT = ANDROID_ROOT / "vendor/red/hydrogenone"

REQUIRED_PAYLOAD = {
    "vendor/bin/qrtr-ns": {
        "size": 68632,
        "sha256": "294d3d810af39d66db49469917e46fc0537e5122cf54c883344135bfd83bf7dd",
    },
    "vendor/bin/tftp_server": {
        "size": 136648,
        "sha256": "ecdfa1761175b257b2179eb51868d7ad41bc38fdc5dd054098d3612951a49d24",
    },
    "vendor/lib64/libqsocket.so": {
        "size": 68000,
        "sha256": "8f3cde8b60e41034e04d527d022a7f07d9c5ef710142db959045a412aeb37406",
    },
    "vendor/lib64/libqrtr.so": {
        "size": 68112,
        "sha256": "f2992d563abbe8ea4a9092b8c0a6fe04a9918b9ccdf1c336c0b3783a96645e88",
    },
}


def selected_paths() -> set[str]:
    result: set[str] = set()
    for raw in (DEVICE_ROOT / "proprietary-files.txt").read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        body = line.split(";", 1)[0]
        result.add(body.split(":", 1)[0].lstrip("-"))
    return result


def readelf(*args: str, path: Path) -> str:
    return subprocess.run(
        ["readelf", *args, str(path)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


class WlanFirmwareTransportContractTest(unittest.TestCase):
    def test_stock118_transport_payload_is_selected(self) -> None:
        self.assertEqual(
            sorted(set(REQUIRED_PAYLOAD) - selected_paths()),
            [],
            "RED .118 WLAN firmware transport paths are not selected",
        )

    def test_stock118_transport_payload_has_exact_identity(self) -> None:
        failures: list[str] = []
        for relative, expected in REQUIRED_PAYLOAD.items():
            path = VENDOR_ROOT / "proprietary" / relative
            if not path.is_file():
                failures.append(f"missing {relative}")
                continue
            data = path.read_bytes()
            if len(data) != expected["size"]:
                failures.append(f"{relative}: size {len(data)} != {expected['size']}")
            actual_sha = hashlib.sha256(data).hexdigest()
            if actual_sha != expected["sha256"]:
                failures.append(f"{relative}: sha256 {actual_sha} != {expected['sha256']}")
        self.assertEqual(
            failures,
            [],
            "RED .118 WLAN firmware transport identity mismatch:\n" + "\n".join(failures),
        )

    def test_vendor_manifest_pins_transport_payload_as_p0(self) -> None:
        manifest = json.loads(
            (VENDOR_ROOT / "proprietary-manifest.json").read_text(encoding="utf-8")
        )
        by_path = {entry["path"]: entry for entry in manifest["files"]}
        failures: list[str] = []
        for relative, expected in REQUIRED_PAYLOAD.items():
            wanted = {"tier": "P0", "path": relative, **expected}
            if by_path.get(relative) != wanted:
                failures.append(f"{relative}: {by_path.get(relative)} != {wanted}")
        self.assertEqual(
            failures,
            [],
            "RED .118 WLAN transport manifest mismatch:\n" + "\n".join(failures),
        )

    def test_tftp_server_is_aarch64_and_links_private_qrtr_transport(self) -> None:
        path = VENDOR_ROOT / "proprietary/vendor/bin/tftp_server"
        self.assertTrue(path.is_file(), f"missing RED .118 payload: {path}")
        if not path.is_file():
            return

        header = readelf("-h", path=path)
        self.assertRegex(header, r"(?m)^\s*Class:\s+ELF64$")
        self.assertRegex(header, r"(?m)^\s*Machine:\s+AArch64$")

        dynamic = readelf("-d", path=path)
        needed = set(re.findall(r"Shared library: \[([^]]+)]", dynamic))
        self.assertTrue({"libqsocket.so", "libqrtr.so"}.issubset(needed), needed)

    def test_qrtr_name_service_is_aarch64_and_links_private_qrtr_transport(self) -> None:
        path = VENDOR_ROOT / "proprietary/vendor/bin/qrtr-ns"
        self.assertTrue(path.is_file(), f"missing RED .118 payload: {path}")
        if not path.is_file():
            return

        header = readelf("-h", path=path)
        self.assertRegex(header, r"(?m)^\s*Class:\s+ELF64$")
        self.assertRegex(header, r"(?m)^\s*Machine:\s+AArch64$")

        dynamic = readelf("-d", path=path)
        needed = set(re.findall(r"Shared library: \[([^]]+)]", dynamic))
        self.assertIn("libqrtr.so", needed)

    def test_qrtr_name_service_precedes_tftp_with_stock118_credentials(self) -> None:
        init = (DEVICE_ROOT / "rootdir/etc/init/hw/init.qcom.rc").read_text(encoding="utf-8")
        qrtr_match = re.search(
            r"(?m)^service vendor\.qrtr-ns /vendor/bin/qrtr-ns -f\s*$"
            r"(?P<body>(?:\n(?:[ \t]+[^\n]*|[ \t]*))*)",
            init,
        )
        self.assertIsNotNone(qrtr_match, "vendor.qrtr-ns service is not declared")
        if qrtr_match is None:
            return

        directives = {
            line.strip()
            for line in qrtr_match.group("body").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        self.assertIn("class core", directives)
        self.assertIn("user vendor_qrtr", directives)
        self.assertIn("group vendor_qrtr", directives)
        self.assertIn("capabilities NET_BIND_SERVICE", directives)
        self.assertNotIn("disabled", directives)

        qrtr_offset = init.index("service vendor.qrtr-ns")
        tftp_offset = init.index("service vendor.tftp_server")
        self.assertLess(qrtr_offset, tftp_offset, "QRTR name service must precede TFTP")

    def test_unproven_qrtr_utilities_are_not_selected(self) -> None:
        self.assertTrue(
            {"vendor/bin/qrtr-cfg", "vendor/bin/qrtr-lookup"}.isdisjoint(selected_paths())
        )

    def test_tftp_service_starts_in_core_class_as_root(self) -> None:
        init = (DEVICE_ROOT / "rootdir/etc/init/hw/init.qcom.rc").read_text(encoding="utf-8")
        match = re.search(
            r"(?m)^service vendor\.tftp_server /vendor/bin/tftp_server\s*$"
            r"(?P<body>(?:\n(?:[ \t]+[^\n]*|[ \t]*))*)",
            init,
        )
        self.assertIsNotNone(match, "vendor.tftp_server service is not declared")
        if match is None:
            return

        directives = {
            line.strip()
            for line in match.group("body").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        self.assertIn("class core", directives)
        self.assertIn("user root", directives)
        self.assertNotIn("disabled", directives)


if __name__ == "__main__":
    unittest.main()
