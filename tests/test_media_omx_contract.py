from __future__ import annotations

import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MediaOmxDeviceContractTest(unittest.TestCase):
    def test_manifest_declares_source_owned_omx_1_0_default_instances(self) -> None:
        root = ET.parse(ROOT / "manifest.xml").getroot()
        matches = [
            hal
            for hal in root.findall("hal")
            if hal.findtext("name") == "android.hardware.media.omx"
        ]
        self.assertEqual(len(matches), 1)
        hal = matches[0]
        self.assertEqual(hal.attrib.get("format"), "hidl")
        self.assertEqual(hal.findtext("transport"), "hwbinder")
        self.assertEqual(hal.findtext("version"), "1.0")
        instances = {
            (iface.findtext("name"), iface.findtext("instance"))
            for iface in hal.findall("interface")
        }
        self.assertEqual(
            instances,
            {
                ("IOmx", "default"),
                ("IOmxStore", "default"),
            },
        )

    def test_device_packages_source_omx_service_and_keeps_codec_payload(self) -> None:
        text = (ROOT / "device.mk").read_text(encoding="utf-8")
        for module in (
            "android.hardware.media.omx@1.0-service",
            "libc2dcolorconvert",
            "libOmxCore",
            "libOmxVdec",
            "libOmxVenc",
            "libstagefrighthw",
        ):
            self.assertRegex(
                text,
                rf"(?m)^\s*{re.escape(module)}\s*\\?\s*$",
                module,
            )

        self.assertIn(
            "# OMX source frontend/service; proprietary codecs remain in vendor",
            text,
        )


if __name__ == "__main__":
    unittest.main()
