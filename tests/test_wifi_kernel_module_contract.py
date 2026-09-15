from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


DEVICE_ROOT = Path(__file__).resolve().parents[1]
ANDROID_ROOT = DEVICE_ROOT.parents[2]
KERNEL_DEFCONFIG = (
    ANDROID_ROOT
    / "kernel/red/msm8998/arch/arm64/configs/lineageos_hydrogenone_defconfig"
)


def evaluated_wifi_variables() -> dict[str, str]:
    makefile = """
include device/red/hydrogenone/BoardConfig.mk
.PHONY: print-wifi-module-contract
print-wifi-module-contract:
	@printf 'path=%s\\nname=%s\\narg=%s\\n' \\
		'$(WIFI_DRIVER_MODULE_PATH)' \\
		'$(WIFI_DRIVER_MODULE_NAME)' \\
		'$(WIFI_DRIVER_MODULE_ARG)'
"""
    result = subprocess.run(
        [
            "make",
            "--silent",
            "--no-print-directory",
            "-C",
            str(ANDROID_ROOT),
            "-f",
            "-",
            "print-wifi-module-contract",
        ],
        input=makefile,
        text=True,
        check=True,
        capture_output=True,
    )
    return dict(line.split("=", 1) for line in result.stdout.splitlines())


class WifiKernelModuleContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.variables = evaluated_wifi_variables()

    def test_wifi_driver_is_a_loadable_kernel_module(self) -> None:
        self.assertIn("CONFIG_QCA_CLD_WLAN=m", KERNEL_DEFCONFIG.read_text())

    def test_wifi_hal_loads_the_source_built_module_from_vendor(self) -> None:
        self.assertEqual(
            self.variables["path"],
            '"/vendor/lib/modules/wlan.ko"',
        )
        self.assertEqual(self.variables["name"], '"wlan"')
        self.assertEqual(self.variables["arg"], "")


if __name__ == "__main__":
    unittest.main()
