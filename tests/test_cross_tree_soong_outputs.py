from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "analysis" / "cross_tree_contract.py"


class CrossTreeSoongOutputTest(unittest.TestCase):
    def run_tool(
        self,
        device_mk: str,
        vendor_bp: str,
        vendor_mk: str = "",
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            device = base / "device"
            vendor = base / "vendor"
            device.mkdir()
            vendor.mkdir()
            (device / "device.mk").write_text(device_mk, encoding="utf-8")
            (vendor / "hydrogenone-vendor.mk").write_text(vendor_mk, encoding="utf-8")
            (vendor / "Android.bp").write_text(vendor_bp, encoding="utf-8")
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

    def test_reports_device_copy_vs_vendor_soong_output_collision(self) -> None:
        proc = self.run_tool(
            "PRODUCT_COPY_FILES += \\\n"
            "    $(LOCAL_PATH)/foo:$(TARGET_COPY_OUT_VENDOR)/bin/hw/vendor.foo\n",
            '''cc_prebuilt_binary {
    name: "vendor.foo",
    owner: "red",
    target: {
        android_arm64: {
            srcs: ["proprietary/vendor/bin/hw/vendor.foo"],
        },
    },
    compile_multilib: "64",
    relative_install_path: "hw",
    soc_specific: true,
}
''',
        )
        self.assertEqual(proc.returncode, 1, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(
            payload["copy_vs_vendor_soong_collisions"],
            ["vendor/bin/hw/vendor.foo"],
        )
        self.assertIn(
            "vendor/bin/hw/vendor.foo",
            payload["vendor_soong_install_outputs"],
        )

    def test_reports_duplicate_vendor_soong_install_output(self) -> None:
        proc = self.run_tool(
            "",
            '''cc_prebuilt_binary {
    name: "vendor.foo.primary",
    target: { android_arm64: { srcs: ["proprietary/vendor/bin/vendor.foo"], }, },
    soc_specific: true,
}
cc_prebuilt_binary {
    name: "vendor.foo.duplicate",
    target: { android_arm64: { srcs: ["proprietary/vendor/bin/vendor.foo"], }, },
    soc_specific: true,
}
''',
        )
        self.assertEqual(proc.returncode, 1, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(
            payload["vendor_soong_output_collisions"],
            ["vendor/bin/vendor.foo"],
        )
        self.assertEqual(
            sorted(payload["vendor_soong_install_outputs"]["vendor/bin/vendor.foo"]),
            ["vendor.foo.duplicate@Android.bp", "vendor.foo.primary@Android.bp"],
        )

    def test_distinct_vendor_soong_output_is_green(self) -> None:
        proc = self.run_tool(
            "PRODUCT_COPY_FILES += \\\n"
            "    $(LOCAL_PATH)/foo.conf:$(TARGET_COPY_OUT_VENDOR)/etc/foo.conf\n",
            '''cc_prebuilt_library_shared {
    name: "libvendorfoo",
    target: {
        android_arm: {
            srcs: ["proprietary/vendor/lib/hw/libvendorfoo.so"],
        },
        android_arm64: {
            srcs: ["proprietary/vendor/lib64/hw/libvendorfoo.so"],
        },
    },
    compile_multilib: "both",
    relative_install_path: "hw",
    soc_specific: true,
}
''',
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["copy_vs_vendor_soong_collisions"], [])
        self.assertEqual(payload["vendor_soong_output_collisions"], [])
        self.assertIn("vendor/lib/hw/libvendorfoo.so", payload["vendor_soong_install_outputs"])
        self.assertIn("vendor/lib64/hw/libvendorfoo.so", payload["vendor_soong_install_outputs"])


if __name__ == "__main__":
    unittest.main()
