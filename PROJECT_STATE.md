# RED Hydrogen One LineageOS 22.2 project state

Last updated: 2026-09-03. This is the canonical long-lived state summary for the
paired device and vendor repositories. Detailed evidence remains under `docs/`.

## Selected baselines and branch audit

The device baseline is `lineage-22.2-stock118-rework` at `5fb932b`. It contains
the integrated `.118` stock contracts, Android 15 ownership split, camera/media,
radio, init/fstab, manifest, extraction, cross-tree and build-preflight work.
The active paired branch is `test/lineage-22.2-bringup`.

Device remote branches found were: `main`, `legacy-pre-stock118-rework`,
`fix/lineage-22.2-runtime-contract`, `lineage-22.2-stock118-rework`,
`build-preflight-tdd`, `camera-stock118-tdd`, `cross-tree-green-tdd`,
`cross-tree-schema3-integration`, `cross-tree-schema3-integration2`,
`cross-tree-soong-output-tdd`, `manifest-readiness-tdd`,
`media-profiles-stock118-tdd`, `radio-control-tdd`, `radio-evidence-tdd`,
`radio-prop-tdd`, `radio-runtime-tdd`, `radio-shell-tdd`,
`stock-config-audit-final`, `stock-config-audit-tdd`,
`stock118-build-contract-tdd`, `vendor-inheritance-final`,
`vendor-inheritance-tdd`, `tmp-apply-vendor-contract-20260902`,
`tmp-extract-utils-export`, `codex-auth-test`, and `twrp-12.1`.

The TDD/final/integration branches are historical topic branches whose verified
changes were integrated or superseded in the selected baseline; Git topology
may show divergence because the integration used rebases/cherry-picks. The
`tmp-*` branches are one-shot transport branches. `codex-auth-test` tests GitHub
authorization, and `twrp-12.1` is recovery work; neither is a bring-up base.
`main`, `legacy-pre-stock118-rework`, and the identically pointed runtime branch
are pre-`.118` legacy state and omit the later evidence-driven work.

Vendor branches found were `lineage-22.2` and
`lineage-22.2-android15-contract`. The latter at `6fef3d7` is selected because it
adds the Android 15 ELF, init, HAL/VINTF, daemon and source/proprietary ownership
contracts absent from `lineage-22.2`. The active paired branch adds documentation
only at `266c8f9`; proprietary payload content is unchanged.

## Evidence and recovered decisions

All tracked Markdown documents in both selected trees were inventoried. The
primary synthesis inputs are `README_BRINGUP.md`, `BUILD_FIRST.md`, the
changelogs and kernel/donor notes, the Android 15 manifest contract, every `.118`
stock report under `docs/stock/h1a1000-r118/`, the design/plan documents, the
numbered worklog and resume marker, plus the vendor README. Historical claims
were checked against tracked stock artifacts, generated JSON evidence, Git
history, and permanent tests rather than accepted as authoritative prose.

Confirmed authority and decisions:

* Stock authority is `H1A1000.082ho.01.00.10r.118` (Android 9, first API 27),
  archive SHA-256 `7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`.
* The target is LineageOS 22.2 / Android 15 / API 35. Open configuration belongs
  in the device tree; proprietary payload and generated modules belong in the
  vendor tree. No speculative RED `msm8998-common` tree is permitted.
* The exact `.118` 4.4.153+ prebuilt kernel is transitional and evidence-backed;
  a validated source-built kernel remains a later milestone.
* The device is A/B and the `.118` fstab, boot parameters, radio DSDS/qcrild
  behavior, camera topology/tuning, and proprietary HAL inventory outrank donor
  devices and the older `.109` bring-up.
* Source-owned GNSS/NFC and compatibility wrappers were removed from proprietary
  ownership where tests proved collisions. Vendor VINTF fragments and required
  P0 daemons were completed, and the generated device/vendor copy contract has
  zero ownership collisions.

Unconfirmed assumptions in older notes include full runtime viability of legacy
HIDL blobs on Android 15, completeness of hardware behavior inferred only from
static stock files, and suitability of donor-device values. None is treated as
proof of bootability.

## Current cross-tree contract

The chain is represented as device packages/configuration -> source or generated
vendor module -> VINTF/init declaration -> runtime service expectation. Static
contracts cover camera, audio/media, radio, fingerprint/sensors, graphics/DRM,
GNSS, Wi-Fi/Bluetooth, NFC, power/thermal, firmware, rootdir and partitions.
`docs/reference/cross-tree-lock.json` pins the exact paired vendor revision;
`docs/stock/h1a1000-r118/cross-tree-copy-contract.json` records the generated
zero-collision ownership result. The local manifest and CI use the same pin.

## Verified state and remaining gates

Repository tests validate stock hashes/inventory, extraction and generated-file
structure, references, make/Soong ownership, VINTF/init/fstab/radio/camera
contracts, duplicate copy destinations, ELF policy, source locks and the paired
vendor revision. These are static checks, not a successful Android build.

The next authoritative action is external: in a complete, clean LineageOS 22.2
workspace run `tools/build/run_m_nothing_preflight.sh --validate-only`, then the
same script without that flag. No complete Android source tree is present here.
After `m nothing`, advance separately through `bootimage`, `vendorimage`,
`systemimage`, target-files and OTA. Boot, SELinux, linker, radio, camera, audio,
sensors, display, DRM, thermal/power and slot/OTA behavior all require actual
build output and staged H1A1000 hardware testing.
