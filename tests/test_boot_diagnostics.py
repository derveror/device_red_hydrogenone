from __future__ import annotations

import importlib.util
import json
import os
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/collect_boot_diagnostics.py"


class BootDiagnosticsTest(unittest.TestCase):
    def load_tool(self):
        self.assertTrue(SCRIPT.is_file(), "boot evidence collector is missing")
        spec = importlib.util.spec_from_file_location("boot_diagnostics", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_reads_header_and_kernel_from_actual_image(self):
        tool = self.load_tool()
        with tempfile.TemporaryDirectory() as directory:
            data = bytearray(8192)
            data[:8] = b"ANDROID!"
            struct.pack_into("<10I", data, 8, 4, 0x8000, 0, 0x1000000,
                             0, 0xf00000, 0x100, 4096, 1, 0)
            data[64:89] = b"androidboot.hardware=qcom\0"
            data[4096:4100] = b"test"
            path = Path(directory) / "boot.img"
            path.write_bytes(data)
            result = tool.inspect_boot(path)
            self.assertEqual(result["header_version"], 1)
            self.assertEqual(result["page_size"], 4096)
            self.assertEqual(result["kernel_size"], 4)
            self.assertEqual(result["kernel_address"], "0x00008000")
            self.assertEqual(result["cmdline"], "androidboot.hardware=qcom")
            self.assertEqual(result["kernel_sha256"],
                             "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08")

    def test_rejects_truncated_kernel_payload(self):
        tool = self.load_tool()
        with tempfile.TemporaryDirectory() as directory:
            data = bytearray(4096)
            data[:8] = b"ANDROID!"
            struct.pack_into("I", data, 8, 1024)
            struct.pack_into("II", data, 36, 4096, 1)
            path = Path(directory) / "boot.img"
            path.write_bytes(data)
            with self.assertRaisesRegex(ValueError, "truncated"):
                tool.inspect_boot(path)

    def test_host_only_collects_evidence_without_adb_or_fastboot(self):
        self.assertTrue(SCRIPT.is_file(), "boot evidence collector is missing")
        with tempfile.TemporaryDirectory() as directory:
            top = Path(directory)
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--top", str(top), "--host-only"],
                capture_output=True, text=True, timeout=15,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            bundles = list((top / "logs/hydrogenone").glob("boot-diagnostics-*.tar.gz"))
            self.assertEqual(len(bundles), 1)
            summary = json.loads(next((top / "logs/hydrogenone").glob("*/summary.json")).read_text())
            self.assertFalse(summary["device_queried"])
            self.assertIn("missing", summary["boot_image_error"])

    def test_fastboot_only_records_slot_and_reboot_evidence(self):
        self.assertTrue(SCRIPT.is_file(), "boot evidence collector is missing")
        with tempfile.TemporaryDirectory() as directory:
            top = Path(directory)
            bin_dir = top / "bin"
            bin_dir.mkdir()
            # Model only the unavailable USB boundary. Unexpected commands fail;
            # the collector still has to preserve their status and actual output.
            for name in ("adb", "fastboot"):
                fake = bin_dir / name
                fake.write_text("#!" + sys.executable + "\n" + '''
import sys
from pathlib import Path
name = Path(sys.argv[0]).name
args = sys.argv[1:]
if args == ['devices', '-l'] and name == 'adb':
    print('List of devices attached\\n')
elif args == ['devices'] and name == 'fastboot':
    print('test-serial\\tfastboot')
elif args[:2] == ['-s', 'test-serial'] and args[2:3] == ['getvar']:
    print('(bootloader) ' + args[3] + ': test-value', file=sys.stderr)
else:
    print('UNEXPECTED COMMAND: ' + repr(args), file=sys.stderr)
    sys.exit(90)
''')
                fake.chmod(0o755)
            env = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ.get("PATH", ""))
            env.pop("ANDROID_SERIAL", None)
            result = subprocess.run([sys.executable, str(SCRIPT), "--top", str(top)],
                                    env=env, capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            bundle_dir = next((top / "logs/hydrogenone").glob("*/summary.json")).parent
            logs = "\n".join(p.read_text() for p in bundle_dir.glob("*.txt"))
            self.assertIn("current-slot: test-value", logs)
            self.assertIn("reboot-reason: test-value", logs)
            self.assertNotIn("UNEXPECTED COMMAND", logs)

    def test_multiple_phones_across_transports_are_not_selected_implicitly(self):
        with tempfile.TemporaryDirectory() as directory:
            top = Path(directory)
            bin_dir = top / "bin"
            bin_dir.mkdir()
            for name in ("adb", "fastboot"):
                fake = bin_dir / name
                fake.write_text("#!" + sys.executable + "\n" + '''
import sys
from pathlib import Path
name = Path(sys.argv[0]).name
if sys.argv[1:] == ['devices', '-l'] and name == 'adb':
    print('List of devices attached\\nother-phone\\tdevice product:other')
elif sys.argv[1:] == ['devices'] and name == 'fastboot':
    print('red-phone\\tfastboot')
else:
    print('UNEXPECTED DEVICE QUERY', file=sys.stderr)
    sys.exit(90)
''')
                fake.chmod(0o755)
            env = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ.get("PATH", ""))
            env.pop("ANDROID_SERIAL", None)
            result = subprocess.run([sys.executable, str(SCRIPT), "--top", str(top)],
                                    env=env, capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary_file = next((top / "logs/hydrogenone").glob("*/summary.json"))
            self.assertFalse(json.loads(summary_file.read_text())["device_queried"])
            logs = "\n".join(p.read_text() for p in summary_file.parent.glob("*.txt"))
            self.assertNotIn("UNEXPECTED DEVICE QUERY", logs)


if __name__ == "__main__":
    unittest.main()
