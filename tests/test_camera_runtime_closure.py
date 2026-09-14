from __future__ import annotations

import unittest
import xml.etree.ElementTree as ElementTree
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANDROID_ROOT = ROOT.parents[2]
VENDOR_ROOT = ANDROID_ROOT / "vendor" / "red" / "hydrogenone"
PRODUCTION_XMLS = (
    "imx268_main_chromatix.xml",
    "imx268_sub_chromatix.xml",
    "imx380_main_chromatix.xml",
    "imx380_sub_chromatix.xml",
)
PRODUCTION_SUPPORT = {
    "vendor/lib/libSonyIMX380PdafLibrary.so",
    "vendor/lib/libactuator_lc898219xl_main.so",
    "vendor/lib/libactuator_lc898219xl_sub.so",
    "vendor/lib/libflash_pmic.so",
    "vendor/lib/libmmcamera_m24c64s_main_eeprom.so",
    "vendor/lib/libmmcamera_m24c64s_sub_eeprom.so",
    "vendor/lib/libmmcamera_paaf_lib.so",
    "vendor/lib/libmmcamera_ppeiscore.so",
    "vendor/lib/libmmcamera_quadracfa.so",
    "vendor/lib/libremosaic_daemon.so",
    "vendor/firmware/cpp_firmware_v1_12_0.fw",
}
RUNTIME_ISP_MODULES = {
    "libmmcamera_isp_bpc48.so",
    "libmmcamera_isp_cac47.so",
    "libmmcamera_isp_chroma_enhan40.so",
    "libmmcamera_isp_chroma_suppress40.so",
    "libmmcamera_isp_clamp_encoder40.so",
    "libmmcamera_isp_clamp_video40.so",
    "libmmcamera_isp_clamp_viewfinder40.so",
    "libmmcamera_isp_color_correct46.so",
    "libmmcamera_isp_color_xform_encoder46.so",
    "libmmcamera_isp_color_xform_video46.so",
    "libmmcamera_isp_color_xform_viewfinder46.so",
    "libmmcamera_isp_cs_stats46.so",
    "libmmcamera_isp_demosaic48.so",
    "libmmcamera_isp_demux48.so",
    "libmmcamera_isp_fovcrop_encoder46.so",
    "libmmcamera_isp_fovcrop_video46.so",
    "libmmcamera_isp_fovcrop_viewfinder46.so",
    "libmmcamera_isp_gamma44.so",
    "libmmcamera_isp_gic48.so",
    "libmmcamera_isp_gtm46.so",
    "libmmcamera_isp_hdr48.so",
    "libmmcamera_isp_hdr_be_stats46.so",
    "libmmcamera_isp_hdr_bhist_stats44.so",
    "libmmcamera_isp_ihist_stats46.so",
    "libmmcamera_isp_linearization40.so",
    "libmmcamera_isp_ltm47.so",
    "libmmcamera_isp_mce40.so",
    "libmmcamera_isp_mesh_rolloff44.so",
    "libmmcamera_isp_pdaf48.so",
    "libmmcamera_isp_pedestal_correct46.so",
    "libmmcamera_isp_rs_stats46.so",
    "libmmcamera_isp_scaler_encoder46.so",
    "libmmcamera_isp_scaler_video46.so",
    "libmmcamera_isp_scaler_viewfinder46.so",
    "libmmcamera_isp_sce40.so",
    "libmmcamera_isp_snr47.so",
}


def chromatix_paths() -> set[str]:
    paths: set[str] = set()
    for name in PRODUCTION_XMLS:
        root = ElementTree.parse(ROOT / "configs" / "camera" / name).getroot()
        for node in root.iter():
            value = (node.text or "").strip()
            if value:
                paths.add(f"vendor/lib/libchromatix_{value}.so")
    return paths


def proprietary_entries() -> set[str]:
    entries: set[str] = set()
    for raw_line in (ROOT / "proprietary-files.txt").read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        path = line.lstrip("-").split("|", 1)[0].split(";", 1)[0].split(":", 1)[0]
        entries.add(path)
    return entries


class CameraRuntimeClosureTest(unittest.TestCase):
    def test_production_xmls_select_138_stock_tuning_libraries(self) -> None:
        selected = chromatix_paths()
        self.assertEqual(len(selected), 138)
        missing = sorted(selected - proprietary_entries())
        self.assertEqual(missing, [], "missing production chromatix entries:\n" + "\n".join(missing))

    def test_runtime_support_and_isp_modules_are_listed(self) -> None:
        self.assertEqual(len(RUNTIME_ISP_MODULES), 36)
        required = PRODUCTION_SUPPORT | {
            f"vendor/lib/{name}" for name in RUNTIME_ISP_MODULES
        }
        missing = sorted(required - proprietary_entries())
        self.assertEqual(missing, [], "missing camera runtime entries:\n" + "\n".join(missing))

    def test_every_selected_file_exists_in_vendor_tree(self) -> None:
        required = chromatix_paths() | PRODUCTION_SUPPORT | {
            f"vendor/lib/{name}" for name in RUNTIME_ISP_MODULES
        }
        missing = sorted(
            path for path in required if not (VENDOR_ROOT / "proprietary" / path).is_file()
        )
        self.assertEqual(missing, [], "missing vendor camera files:\n" + "\n".join(missing))

    def test_extraction_replays_the_android15_vendor_contract(self) -> None:
        extraction = (ROOT / "extract-files.py").read_text(encoding="utf-8")
        self.assertIn("apply_android15_vendor_contract.py", extraction)
        self.assertIn("subprocess.run", extraction)
        self.assertIn("check=True", extraction)


if __name__ == "__main__":
    unittest.main()
