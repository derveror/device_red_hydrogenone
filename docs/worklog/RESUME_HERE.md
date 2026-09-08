# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

Marker version: 13. Updated: 2026-09-08.
Current action: `docs/worklog/2026-09-08/0001-boot-import-and-evidence.md`.

## Current state

- User reports complete LineageOS compilation succeeded, but phone does not boot.
- Device branch: `codex/lineage-22.2-bringup`.
- Vendor branch: `codex/lineage-22.2-bringup`.
- Vendor pin: `6d80047932b9ecade6ba34c4cff22a9206972cb6`.
- Device parent for the boot correction: `73ca80baf580f05f0670161128991c3d3a95ce2b`.
- Main reference by explicit user decision: cheryl device + vendor. Mata is secondary.
- Hardware/proprietary authority: RED H1A1000 .118, Android 9 / first API27.
- Target: LineageOS22.2 / Android15 / API35.
- Lunch: `lineage_hydrogenone-bp1a-userdebug`.

## Confirmed changes and open boot boundary

The missing init.target import is corrected and covered by an import-reachability
regression. All 14 service executables already exist in the pinned vendor.
The host collection tool is `tools/collect_boot_diagnostics.py`; it saves evidence
under `<source top>/logs/hydrogenone` without flashing or changing phone state.

The selected stock kernel lacks BPF_SYSCALL. LineageOS netbpfload requires that
interface and can trigger bpfloader-failed reboot. Kernel adaptation remains open.
The phone's exact failure stage is not proven; collect the existing failure and
image metadata using `docs/BOOT_DIAGNOSTICS.md`. Do not return to the obsolete
first-m-nothing gate from marker12: the user has now reported a successful build.

Keep device and vendor separate; do not introduce RED msm8998-common projects.
Do not substitute donor firmware/DTBs. Power HAL, Android IMS app and Widevine
are still incomplete; the init correction is not a claim those are implemented.
