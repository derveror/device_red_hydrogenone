from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VENDOR_HIDL_CONTRACT = (
    ROOT / "docs" / "reference" / "vendor-hidl-runtime-contract.json"
)


def text_files() -> list[Path]:
    result: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        data = path.read_bytes()
        if b"\0" not in data:
            result.append(path)
    return result


class Stock118PurgeContractTest(unittest.TestCase):
    def test_obsolete_stock_identity_is_absent_from_current_tree(self) -> None:
        forbidden = (
            "." + str(100 + 9),
            "Android " + "8.1",
            ":8." + "1.0/",
            "O-" + "MR1",
            "4.4." + str(70 + 8),
            "H1A1000.010ho.01.01.01r." + str(100 + 9),
        )
        findings = []
        for path in text_files():
            text = path.read_text(encoding="utf-8", errors="ignore")
            for token in forbidden:
                if token in text:
                    findings.append(f"{path.relative_to(ROOT)}: {token}")
        self.assertEqual(
            findings,
            [],
            "obsolete stock identity remains:\n" + "\n".join(findings),
        )

    def test_obsolete_raw_reference_and_prebuilt_trees_are_absent(self) -> None:
        forbidden = (
            "prebuilt",
            "reference/stock_boot",
            "reference/stock_vendor",
            "reference/stock_system",
            "reference/dtbs/production",
        )
        present = [relative for relative in forbidden if (ROOT / relative).exists()]
        self.assertEqual(present, [], f"obsolete reference trees remain: {present}")

    def test_device_extraction_list_matches_pinned_vendor_selection(self) -> None:
        entries = [
            line.strip()
            for line in (ROOT / "proprietary-files.txt").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        # The complete FP3 radio generation includes QCRIL, QMI, netmgr and
        # DPM. The former unpinned RED copies of nine replaced QMI paths are
        # removed so every installed destination has exactly one source.
        destinations = [
            entry.split(";", 1)[0].split(":", 1)[0].lstrip("-").split("|", 1)[0]
            for entry in entries
        ]
        self.assertEqual(len(entries), 710)
        self.assertEqual(len(destinations), len(set(destinations)))

    def test_vendor_hidl_runtime_contract_is_pinned_to_red118(self) -> None:
        contract = json.loads(VENDOR_HIDL_CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(contract["schema_version"], 1)
        self.assertEqual(
            contract["vendor_commit"],
            "a6560ec388398760f3d45e7634ba23c89f4a2eb6",
        )
        self.assertEqual(contract["selected_file_count"], 460)
        self.assertTrue(contract["source_owned_hidl_base_pruned"])
        self.assertEqual(contract["selected_stock_hidl_base_blobs"], [])
        self.assertEqual(contract["hidlbase_shim_consumer_count"], 63)
        self.assertEqual(
            contract["imsdatadaemon_needed_replacement"],
            {"from": "libhwbinder.so", "to": "libhidlbase.so"},
        )

    def test_active_reference_lock_excludes_obsolete_hydrogen_archives(self) -> None:
        obsolete = (
            "device_red_hydrogenone-" + "fix-lineage-22.2-runtime-contract.zip",
            "device_red_hydrogenone-" + "main(1).zip",
        )
        active = (
            ROOT / "docs/reference/source-lock.json",
            ROOT / "docs/reference/archive-inventory.json",
            ROOT / "docs/reference/archive-comparisons.json",
            ROOT / "docs/reference/SUPPLIED_SOURCES.md",
            ROOT / "docs/reference/README.md",
        )
        findings = []
        for path in active:
            text = path.read_text(encoding="utf-8")
            findings.extend(
                f"{path.relative_to(ROOT)}: {name}"
                for name in obsolete
                if name in text
            )
        self.assertEqual(findings, [], "obsolete active archives remain:\n" + "\n".join(findings))
        self.assertFalse((ROOT / "docs/reference/full-artifacts.sha256").exists())

        lock = json.loads((ROOT / "docs/reference/source-lock.json").read_text(encoding="utf-8"))
        inventory = json.loads((ROOT / "docs/reference/archive-inventory.json").read_text(encoding="utf-8"))
        comparisons = json.loads((ROOT / "docs/reference/archive-comparisons.json").read_text(encoding="utf-8"))
        self.assertEqual(len(lock["reference_archives"]), 11)
        self.assertEqual(len(inventory), 11)
        self.assertEqual(len(comparisons), 5)
        self.assertEqual(
            lock["repository_authority"]["development_branch"],
            "118-lineage-22.2-kernel-302",
        )


if __name__ == "__main__":
    unittest.main()
