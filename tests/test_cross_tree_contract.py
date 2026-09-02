from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "analysis" / "cross_tree_contract.py"
DEVICE_MK = ROOT / "device.mk"

VENDOR_OWNED_RED118_CONFIGS = {
    "configs/nfc/libnfc-nci.conf": "$(TARGET_COPY_OUT_VENDOR)/etc/libnfc-nci.conf",
    "configs/thermal-engine.conf": "$(TARGET_COPY_OUT_VENDOR)/etc/thermal-engine.conf",
}


class CrossTreeContractTest(unittest.TestCase):
    def run_tool(self, device_mk: str, vendor_mk: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            device = base / "device"
            vendor = base / "vendor"
            device.mkdir()
            vendor.mkdir()
            (device / "device.mk").write_text(device_mk, encoding="utf-8")
            (vendor / "hydrogenone-vendor.mk").write_text(vendor_mk, encoding="utf-8")
            return subprocess.run(
                [
                    sys.executable,
                    str(TOOL),
                    "--device-root",
                    str(device),
                    "--vendor-root",
                    str(vendor),
                    "--json",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

    def test_reports_duplicate_vendor_copy_destination(self) -> None:
        proc = self.run_tool(
            "PRODUCT_COPY_FILES += \\\n    $(LOCAL_PATH)/configs/a.conf:$(TARGET_COPY_OUT_VENDOR)/etc/shared.conf\n",
            "PRODUCT_COPY_FILES += \\\n    vendor/red/hydrogenone/proprietary/vendor/etc/b.conf:$(TARGET_COPY_OUT_VENDOR)/etc/shared.conf\n",
        )
        self.assertEqual(proc.returncode, 1, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["copy_destination_collisions"], ["vendor/etc/shared.conf"])

    def test_distinct_destinations_are_green(self) -> None:
        proc = self.run_tool(
            "PRODUCT_COPY_FILES += \\\n    $(LOCAL_PATH)/configs/a.conf:$(TARGET_COPY_OUT_VENDOR)/etc/a.conf\n",
            "PRODUCT_COPY_FILES += \\\n    vendor/red/hydrogenone/proprietary/vendor/etc/b.conf:$(TARGET_COPY_OUT_VENDOR)/etc/b.conf\n",
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["copy_destination_collisions"], [])

    def test_normalizes_recovery_and_vendor_partitions_separately(self) -> None:
        proc = self.run_tool(
            "PRODUCT_COPY_FILES += \\\n    $(LOCAL_PATH)/fstab:$(TARGET_COPY_OUT_RECOVERY)/root/fstab.qcom\n",
            "PRODUCT_COPY_FILES += \\\n    vendor/red/hydrogenone/proprietary/vendor/etc/fstab.qcom:$(TARGET_COPY_OUT_VENDOR)/etc/fstab.qcom\n",
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["copy_destination_collisions"], [])

    def test_red118_vendor_owned_configs_are_not_active_device_copies(self) -> None:
        text = DEVICE_MK.read_text(encoding="utf-8")
        for source, destination in sorted(VENDOR_OWNED_RED118_CONFIGS.items()):
            self.assertNotIn(f"$(LOCAL_PATH)/{source}:{destination}", text, source)
            self.assertFalse((ROOT / source).exists(), source)


if __name__ == "__main__":
    unittest.main()
