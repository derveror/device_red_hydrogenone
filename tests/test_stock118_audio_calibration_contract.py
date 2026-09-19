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
VENDOR_PAYLOAD = VENDOR_ROOT / "proprietary"

STOCK118_AUDIO_CALIBRATION = {
    "vendor/etc/audio_tuning_mixer.txt": (
        3712,
        "c09d6e8fdb0e367e132064a23bac781318be1313b7454712b43feae5e8f09f28",
    ),
    "vendor/etc/acdbdata/MTP/MTP_Bluetooth_cal.acdb": (
        72370,
        "0c46a904c6c262248a5e0ef7ccb4f8e5131b28232ec71e19a78850f71961260a",
    ),
    "vendor/etc/acdbdata/MTP/MTP_General_cal.acdb": (
        29433,
        "09631f20c7d55738b833b570b79a83a35d5bf86f46a7a787de92433d1868d31a",
    ),
    "vendor/etc/acdbdata/MTP/MTP_Global_cal.acdb": (
        9821,
        "8dd3d326ecd0ce07c8e5a818189033683e923948fe655a865b7e5de89a6a4bdd",
    ),
    "vendor/etc/acdbdata/MTP/MTP_Handset_cal.acdb": (
        282428,
        "a70ad69f8483139c1f468967eae30ea45590957a6e5af4e68212235c46eeeb67",
    ),
    "vendor/etc/acdbdata/MTP/MTP_Hdmi_cal.acdb": (
        7673,
        "114c3045e91a383dc27a9d85c332131b9229371310fd498de7664a4ccf5b6ed0",
    ),
    "vendor/etc/acdbdata/MTP/MTP_Headset_cal.acdb": (
        152517,
        "af9e08c497bff64be90d1ee47d197814e19a6bf0970b3d87a0038ac4047ee781",
    ),
    "vendor/etc/acdbdata/MTP/MTP_Speaker_cal.acdb": (
        353538,
        "3aa79fd5505166cbce6afda67b2d3d3a18090b95892b14ece29072831750ac9a",
    ),
    "vendor/etc/acdbdata/MTP/MTP_workspaceFile.qwsp": (
        6656,
        "17385208d13d3d70e8b2c5649a076f4243c7a580a14a830e21cacf6f1607521e",
    ),
    "vendor/lib/libacdb-fts.so": (
        19704,
        "9d5b7fc1618bf3f63fea4ef87799c3b8f9701b3472bfee01019287e1f98eb8ea",
    ),
    "vendor/lib/libacdbloader.so": (
        112336,
        "93f8bebc7c3b057745f7dddb7f073007c3f619ac0435cf35411bae344dc1a648",
    ),
    "vendor/lib/libacdbrtac.so": (
        32152,
        "390f0255b4f8aab3076de4aa266fa51b00c54f1d1722796bd8579150900610f9",
    ),
    "vendor/lib/libadiertac.so": (
        32056,
        "09af96612bac9a615cc08f7934ba09b0d00d24d13fb5e1ed4bf5017e45a15d51",
    ),
    "vendor/lib/libaudcal.so": (
        148636,
        "d035a7cfde4e2959d7aa58442f30bf1e9e75a10176caad36f462a2fc22289d0e",
    ),
    "vendor/lib64/libacdb-fts.so": (
        68224,
        "51730e0e9f9d7c9ad3261e894672350d3816975a4a83b7cab7524589a1cda082",
    ),
    "vendor/lib64/libacdbloader.so": (
        136248,
        "5ce12163b8e8ea2cd2e75babbdfd9fa398ec39c97b6656a9250a76d1a6b91eaf",
    ),
    "vendor/lib64/libacdbrtac.so": (
        68200,
        "f69f4d134e8759ba39bb07d0d0487319172f1f5e1e299588f42a56cf5b5356ed",
    ),
    "vendor/lib64/libadiertac.so": (
        68376,
        "c949030b2da1191aebb79a93e368fdc1a0d1d57eaaad681ada2214c04bc29a40",
    ),
    "vendor/lib64/libaudcal.so": (
        199640,
        "0e81c904a1c49fa829c82288048ecc597e161b229be17de615150ee2dac0a153",
    ),
}


def selected_paths(path: Path) -> set[str]:
    result: set[str] = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        result.add(line.split("|", 1)[0].split(";", 1)[0].split(":", 1)[0].lstrip("-"))
    return result


def readelf(*args: str, path: Path) -> str:
    return subprocess.run(
        ["readelf", *args, str(path)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


class Stock118AudioCalibrationContractTest(unittest.TestCase):
    def test_stock118_mtp_calibration_runtime_is_selected_and_present(self) -> None:
        required = set(STOCK118_AUDIO_CALIBRATION)
        for listing in (
            DEVICE_ROOT / "proprietary-files.txt",
            VENDOR_ROOT / "proprietary-files.txt",
        ):
            self.assertEqual(
                sorted(required - selected_paths(listing)),
                [],
                f"missing RED .118 audio calibration entries in {listing}",
            )

        missing = sorted(
            relative
            for relative in required
            if not (VENDOR_PAYLOAD / relative).is_file()
        )
        self.assertEqual(missing, [], "missing RED .118 audio calibration payload")

    def test_audio_calibration_payload_is_exact_stock118(self) -> None:
        failures: list[str] = []
        for relative, (expected_size, expected_sha256) in STOCK118_AUDIO_CALIBRATION.items():
            path = VENDOR_PAYLOAD / relative
            if not path.is_file():
                failures.append(f"missing {relative}")
                continue
            payload = path.read_bytes()
            if len(payload) != expected_size:
                failures.append(f"{relative}: size {len(payload)} != {expected_size}")
            actual_sha256 = hashlib.sha256(payload).hexdigest()
            if actual_sha256 != expected_sha256:
                failures.append(
                    f"{relative}: sha256 {actual_sha256} != {expected_sha256}"
                )
        self.assertEqual(failures, [], "RED .118 audio payload mismatch:\n" + "\n".join(failures))

    def test_vendor_manifest_pins_audio_calibration_as_p0(self) -> None:
        manifest = json.loads(
            (VENDOR_ROOT / "proprietary-manifest.json").read_text(encoding="utf-8")
        )
        by_path = {entry["path"]: entry for entry in manifest["files"]}
        failures: list[str] = []
        for relative, (size, sha256) in STOCK118_AUDIO_CALIBRATION.items():
            expected = {
                "tier": "P0",
                "path": relative,
                "size": size,
                "sha256": sha256,
            }
            if by_path.get(relative) != expected:
                failures.append(f"{relative}: {by_path.get(relative)} != {expected}")
        self.assertEqual(failures, [], "audio manifest mismatch:\n" + "\n".join(failures))

    def test_acdb_loader_exports_the_hal_runtime_contract(self) -> None:
        for arch in ("lib", "lib64"):
            loader = VENDOR_PAYLOAD / f"vendor/{arch}/libacdbloader.so"
            symbols = readelf("-Ws", path=loader)
            for symbol in (
                "acdb_loader_init_v3",
                "acdb_loader_send_audio_cal_v3",
                "acdb_loader_send_voice_cal",
            ):
                self.assertRegex(symbols, rf"\b{re.escape(symbol)}\b", f"{loader}: {symbol}")

            needed = set(
                re.findall(
                    r"Shared library: \[([^]]+)]",
                    readelf("-d", path=loader),
                )
            )
            self.assertTrue(
                {
                    "libacdb-fts.so",
                    "libacdbrtac.so",
                    "libadiertac.so",
                    "libaudcal.so",
                }.issubset(needed),
                f"{loader}: {needed}",
            )


if __name__ == "__main__":
    unittest.main()
