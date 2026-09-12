from __future__ import annotations

import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXACT_STOCK118_FILES = {
    "audio/audio_platform_info.xml": "614af67cfec5dc1ad38e70ad04b0e9e323b514c572e7291b8535e6023efbd186",
    "audio/mixer_paths_tasha.xml": "d17baa0cc2866a100cad237a7c057a8f0f2c24cb150be3f4b5bdf85200140fd2",
    "media/media_profiles_V1_0.xml": "a88313e1cccb57c7dd5c22fe11907e04e25425f0764d6b118788f423f4cd9721",
    "power/powerhint.xml": "2e8ad4504f16340763e7cdd22a0ed244f9824871601b550857a018be279e5209",
    "wifi/WCNSS_qcom_cfg.ini": "e80e07974d5d335c62b60e8742713c083d9a5b726fbab7a40bf457aa752c69ca",
    "keylayout/gpio-keys.kl": "ef1e59efc273cfe995c91633bc35fdae040318205e777305d7318618f417b4cd",
    # The source NXP HAL reads this active name. Its contents are the exact
    # RED .118 nqx.default configuration shipped as libnfc-nxp_default.conf.
    "configs/nfc/libnfc-nxp.conf": "af152b8705c3a8362fd10ad970ef2213d1f0c97129063c544f03e31d215c726d",
}

PUBLIC_LIBRARIES = (
    "libqti-perfd-client.so",
    "libadsprpc.so",
    "libcdsprpc.so",
    "libsdsprpc.so",
    "libfastcvopt.so",
    "liblistenjni.so",
    "liblistensoundmodel2.so",
    "libOpenCL.so",
    "libnpu.so",
)


class Stock118RuntimeConfigContractTest(unittest.TestCase):
    def test_exact_stock118_hardware_configs(self) -> None:
        failures = []
        for relative, expected_sha in EXACT_STOCK118_FILES.items():
            path = ROOT / relative
            if not path.is_file():
                failures.append(f"missing {relative}")
                continue
            actual_sha = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual_sha != expected_sha:
                failures.append(f"{relative}: {actual_sha} != {expected_sha}")
        self.assertEqual(failures, [], "stock .118 identity mismatch:\n" + "\n".join(failures))

    def test_stock118_public_library_contract(self) -> None:
        actual = tuple(
            line.strip()
            for line in (ROOT / "configs/public.libraries.txt").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )
        self.assertEqual(actual, PUBLIC_LIBRARIES)

    def test_android15_gnss_group_translation_is_preserved(self) -> None:
        text = (ROOT / "gps/izat.conf").read_text(encoding="utf-8")
        self.assertIn("qcom_diag", text)
        self.assertNotIn("oem_" + str(2901), text)


if __name__ == "__main__":
    unittest.main()
