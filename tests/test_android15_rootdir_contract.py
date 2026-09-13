from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "rootdir/etc/init/hw/init.target.rc"
QCOM = ROOT / "rootdir/etc/init/hw/init.qcom.rc"

SERVICE_RE = re.compile(r"(?m)^\s*service\s+(\S+)\s+(\S+)")
IMPORT_RE = re.compile(r"(?m)^\s*import\s+/vendor/etc/init/hw/(\S+)")

EXPECTED_SERVICES = {
    "vendor.per_mgr": "/vendor/bin/pm-service",
    "vendor.per_proxy": "/vendor/bin/pm-proxy",
    "vendor.rmt_storage": "/vendor/bin/rmt_storage",
    "vendor.qseecomd": "/vendor/bin/qseecomd",
    "spdaemon": "/vendor/bin/spdaemon",
    "vendor.thermal-engine": "/vendor/bin/thermal-engine",
    "vendor.adsprpcd": "/vendor/bin/adsprpcd",
    "vendor.energy-awareness": "/vendor/bin/energy-awareness",
    "vendor.imsqmidaemon": "/vendor/bin/imsqmidaemon",
    "vendor.imsdatadaemon": "/vendor/bin/imsdatadaemon",
    "vendor.pd_mapper": "/vendor/bin/pd-mapper",
    "vendor.ims_rtp_daemon": "/vendor/bin/ims_rtp_daemon",
    "vendor.imsrcsservice": "/vendor/bin/imsrcsd",
    "vendor.hvdcp_opti": "/vendor/bin/hvdcp_opti",
}

LEGACY_TOKENS = {
    "/dev/stune/": "schedtune cgroup paths were removed from modern Android task-profile ownership",
    "mount_all /vendor/etc/fstab.qcom --expand": "mounting belongs to init.qcom.rc first/late-stage fs_mgr flow",
    "restorecon_recursive /persist": "Treble vendor persist is /mnt/vendor/persist",
    "mkdir /persist/": "Treble vendor persist is /mnt/vendor/persist",
    " /persist/": "direct /persist paths are not part of the Android 15 control plane",
    "insmod /vendor/lib/modules/qca_cld3_wlan.ko": "manual WLAN loading is not used by current LineageOS MSM8998 rootdir",
    "/system/vendor/": "vendor executables must use the canonical /vendor mount path",
    "/vendor/bin/init.qti.qseecomd.sh": "script is absent from the selected RED .118 vendor contract",
}

REMOVED_STALE_SERVICES = {
    "rfs_access",
    "audiod",
    "ppd",
    "cnss_diag",
    "mdtpd",
    "qvrd",
    "keyserver",
}


def services(text: str) -> dict[str, str]:
    return {name: executable for name, executable in SERVICE_RE.findall(text)}


def reachable_services(entrypoint: Path) -> dict[str, str]:
    pending = [entrypoint]
    visited: set[Path] = set()
    discovered: dict[str, str] = {}

    while pending:
        current = pending.pop()
        if current in visited or not current.is_file():
            continue
        visited.add(current)
        text = current.read_text(encoding="utf-8")
        discovered.update(services(text))
        pending.extend(current.parent / filename for filename in IMPORT_RE.findall(text))

    return discovered


def reachable_rc_files(entrypoint: Path) -> list[Path]:
    pending = [entrypoint]
    visited: set[Path] = set()
    discovered: list[Path] = []

    while pending:
        current = pending.pop(0)
        if current in visited or not current.is_file():
            continue
        visited.add(current)
        discovered.append(current)
        text = current.read_text(encoding="utf-8")
        pending.extend(current.parent / filename for filename in IMPORT_RE.findall(text))

    return discovered


def action_blocks(text: str) -> list[tuple[str, list[str]]]:
    blocks: list[tuple[str, list[str]]] = []
    trigger: str | None = None
    commands: list[str] = []

    for line in text.splitlines():
        if line.startswith("on "):
            if trigger is not None:
                blocks.append((trigger, commands))
            trigger = line.removeprefix("on ").strip()
            commands = []
        elif trigger is not None and line and not line[0].isspace() and not line.startswith("#"):
            blocks.append((trigger, commands))
            trigger = None
            commands = []
        elif trigger is not None and line.strip() and not line.lstrip().startswith("#"):
            commands.append(line.strip())

    if trigger is not None:
        blocks.append((trigger, commands))

    return blocks


def qseecomd_ready_before_fbe(entrypoint: Path) -> bool:
    files = reachable_rc_files(entrypoint)
    blocks = {
        event: [
            commands
            for path in files
            for trigger, commands in action_blocks(path.read_text(encoding="utf-8"))
            if trigger == event
        ]
        for event in ("early-init", "init", "fs", "post-fs")
    }

    started = False
    listeners_ready = False
    for event in ("early-init", "init", "fs", "post-fs"):
        for commands in blocks[event]:
            for command in commands:
                if command == "start vendor.qseecomd":
                    started = True
                elif command == "wait_for_prop vendor.sys.listeners.registered true" and started:
                    listeners_ready = True

    return started and listeners_ready


class Android15RootdirContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.target = TARGET.read_text(encoding="utf-8")
        self.qcom = QCOM.read_text(encoding="utf-8")

    def test_target_declares_only_verified_red_daemons(self) -> None:
        self.assertEqual(services(self.target), EXPECTED_SERVICES)

    def test_secure_daemons_are_reachable_from_android_hardware_init(self) -> None:
        discovered = reachable_services(QCOM)
        self.assertEqual(discovered.get("vendor.qseecomd"), "/vendor/bin/qseecomd")
        self.assertEqual(discovered.get("spdaemon"), "/vendor/bin/spdaemon")

    def test_qseecomd_is_ready_before_android15_starts_keymaster(self) -> None:
        self.assertTrue(qseecomd_ready_before_fbe(QCOM))

    def test_red118_securefs_is_mounted_before_qseecomd(self) -> None:
        fs_commands = [
            command
            for trigger, commands in action_blocks(self.qcom)
            if trigger == "fs"
            for command in commands
        ]
        self.assertIn(
            "mkdir /mnt/vendor/persist/data 0700 system system",
            fs_commands,
        )
        self.assertIn(
            "mount ext4 /dev/block/bootdevice/by-name/cmlog "
            "/mnt/vendor/persist/data noatime nosuid nodev barrier=1",
            fs_commands,
        )

    def test_target_contains_no_android8_9_control_plane_paths(self) -> None:
        conflicts = [f"{token}: {reason}" for token, reason in LEGACY_TOKENS.items() if token in self.target]
        self.assertEqual(conflicts, [], "legacy rootdir constructs remain:\n" + "\n".join(conflicts))

    def test_stale_stock_services_are_not_reintroduced(self) -> None:
        names = set(services(self.target))
        conflicts = sorted(names & REMOVED_STALE_SERVICES)
        self.assertEqual(conflicts, [], f"stale stock services remain: {conflicts}")

    def test_mount_persist_and_fingerprint_are_owned_by_init_qcom(self) -> None:
        self.assertIn("mount_all /vendor/etc/fstab.qcom --early", self.qcom)
        self.assertIn("mount_all /vendor/etc/fstab.qcom --late", self.qcom)
        self.assertIn("/mnt/vendor/persist", self.qcom)
        self.assertIn("soc:fpc1020", self.qcom)
        self.assertNotIn("/sys/class/smartp/smartctrl/", self.qcom)

        self.assertNotIn("mount_all", self.target)
        self.assertNotIn("soc:fpc1020", self.target)
        self.assertNotIn("/sys/class/smartp/smartctrl/", self.target)

    def test_service_triggers_only_reference_defined_device_services(self) -> None:
        defined = set(services(self.target))
        referenced: set[str] = set()
        for command in re.finditer(r"(?m)^\s*(?:start|stop|restart)\s+(\S+)", self.target):
            referenced.add(command.group(1))
        unknown = sorted(referenced - defined)
        self.assertEqual(unknown, [], f"rootdir triggers reference undefined services: {unknown}")

    def test_required_modern_service_semantics_are_present(self) -> None:
        self.assertRegex(self.target, r"service vendor\.rmt_storage /vendor/bin/rmt_storage\n(?:.*\n)*?\s+shutdown critical")
        self.assertRegex(self.target, r"service vendor\.per_proxy /vendor/bin/pm-proxy\n(?:.*\n)*?\s+disabled")
        self.assertRegex(self.target, r"service vendor\.imsdatadaemon /vendor/bin/imsdatadaemon\n(?:.*\n)*?\s+disabled")
        self.assertRegex(self.target, r"service vendor\.ims_rtp_daemon /vendor/bin/ims_rtp_daemon\n(?:.*\n)*?\s+disabled")
        self.assertRegex(self.target, r"service vendor\.imsrcsservice /vendor/bin/imsrcsd\n(?:.*\n)*?\s+disabled")


if __name__ == "__main__":
    unittest.main()
