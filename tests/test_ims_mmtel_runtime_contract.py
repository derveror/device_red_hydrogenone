from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def make_variable_tokens(text: str, variable: str) -> set[str]:
    values: set[str] = set()
    logical = ""
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        logical = f"{logical} {line}".strip()
        if logical.endswith("\\"):
            logical = logical[:-1].rstrip()
            continue
        match = re.match(rf"^{re.escape(variable)}\s*\+=\s*(.*)$", logical)
        if match:
            values.update(match.group(1).split())
        logical = ""
    return values


class ImsMmtelRuntimeContractTest(unittest.TestCase):
    def test_qti_ims_java_contract_is_packaged(self) -> None:
        packages = make_variable_tokens(
            (ROOT / "device.mk").read_text(encoding="utf-8"), "PRODUCT_PACKAGES"
        )
        self.assertTrue(
            {
                "ims-ext-common",
                "ims_ext_common.xml",
                "qti-telephony-hidl-wrapper",
                "qti_telephony_hidl_wrapper.xml",
                "qti-telephony-utils",
                "qti_telephony_utils.xml",
            }.issubset(packages)
        )

    def test_telephony_binds_the_qti_mmtel_service(self) -> None:
        overlay = (
            ROOT
            / "overlay/packages/services/Telephony/res/values/config.xml"
        ).read_text(encoding="utf-8")
        self.assertRegex(
            overlay,
            r'<string\s+name="config_ims_mmtel_package"[^>]*>'
            r'org\.codeaurora\.ims</string>',
        )

    def test_stock118_ims_feature_policy_is_preserved(self) -> None:
        properties = {
            line.strip()
            for line in (ROOT / "vendor.prop").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        self.assertTrue(
            {
                "persist.data.iwlan.ims.enable=1",
                "persist.dbg.volte_avail_ovr=1",
                "persist.dbg.vt_avail_ovr=1",
                "persist.dbg.wfc_avail_ovr=0",
                "persist.dbg.allow_ims_off=1",
            }.issubset(properties)
        )

        framework_overlay = (
            ROOT / "overlay/frameworks/base/core/res/res/values/config.xml"
        ).read_text(encoding="utf-8")
        self.assertRegex(
            framework_overlay,
            r'<bool\s+name="config_device_volte_available">true</bool>',
        )
        self.assertRegex(
            framework_overlay,
            r'<bool\s+name="config_device_vt_available">true</bool>',
        )
        self.assertRegex(
            framework_overlay,
            r'<bool\s+name="config_device_wfc_ims_available">false</bool>',
        )


if __name__ == "__main__":
    unittest.main()
