#!/usr/bin/env python3

import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


DEVICE_ROOT = Path(__file__).resolve().parents[1]
POLICY_DIR = DEVICE_ROOT / "boot" / "update_verifier"
POLICY_HEADER = POLICY_DIR / "legacy_avb1_verifier_policy.h"
POLICY_SOURCE = POLICY_DIR / "legacy_avb1_verifier_policy.cpp"


class LegacyAvb1VerifierPolicyTest(unittest.TestCase):
    def test_only_unlocked_red_avb1_logging_mode_skips_block_verification(self):
        if not POLICY_HEADER.is_file() or not POLICY_SOURCE.is_file():
            self.fail("legacy AVB1 verifier policy is not implemented")

        harness = textwrap.dedent(
            r"""
            #include <iostream>
            #include "legacy_avb1_verifier_policy.h"

            struct Case {
              const char* verified_boot_state;
              const char* verity_mode;
              const char* avb_version;
              const char* vbmeta_device_state;
              bool virtual_ab_enabled;
              bool expected;
            };

            int main() {
              const Case cases[] = {
                  {"orange", "logging", "", "", false, true},
                  {"green", "logging", "", "", false, false},
                  {"orange", "enforcing", "", "", false, false},
                  {"orange", "disabled", "", "", false, false},
                  {"orange", "eio", "", "", false, false},
                  {"orange", "logging", "1.2", "", false, false},
                  {"orange", "logging", "", "unlocked", false, false},
                  {"orange", "logging", "", "", true, false},
              };

              for (const auto& test : cases) {
                const bool actual = hydrogenone::ShouldSkipLegacyAvb1Verification(
                    test.verified_boot_state, test.verity_mode, test.avb_version,
                    test.vbmeta_device_state, test.virtual_ab_enabled);
                if (actual != test.expected) {
                  std::cerr << test.verified_boot_state << "/" << test.verity_mode
                            << "/" << test.avb_version << "/"
                            << test.vbmeta_device_state << "/"
                            << test.virtual_ab_enabled << ": expected "
                            << test.expected << ", got " << actual << "\n";
                  return 1;
                }
              }
              return 0;
            }
            """
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            harness_path = temp_path / "policy_test.cpp"
            binary_path = temp_path / "policy_test"
            harness_path.write_text(harness, encoding="utf-8")

            compile_result = subprocess.run(
                [
                    "g++",
                    "-std=c++17",
                    "-Wall",
                    "-Wextra",
                    "-Werror",
                    f"-I{POLICY_DIR}",
                    str(harness_path),
                    str(POLICY_SOURCE),
                    "-o",
                    str(binary_path),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(compile_result.returncode, 0, compile_result.stderr)

            run_result = subprocess.run(
                [str(binary_path)], capture_output=True, text=True
            )
            self.assertEqual(run_result.returncode, 0, run_result.stderr)


if __name__ == "__main__":
    unittest.main()
