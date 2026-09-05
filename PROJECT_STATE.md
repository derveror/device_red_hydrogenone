# RED Hydrogen One LineageOS 22.2 project state

Last updated: 2026-09-04.

This is the canonical long-lived status summary for the paired repositories
`device/red/hydrogenone` and `vendor/red/hydrogenone`. Detailed stock evidence,
audit outputs and worklogs remain under `docs/`.

## Target and authority

- Device: RED Hydrogen One H1A1000 (`hydrogenone`), MSM8998.
- Target: LineageOS 22.2 / Android 15 / API 35.
- Primary hardware authority: RED stock `H1A1000.082ho.01.00.10r.118`, Android 9.
- Stock archive SHA-256: `7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`.
- Stock fingerprint: `RED/HydrogenONE/HydrogenONE:9/PKQ1.190118.001/118:userdebug/release-keys`.
- Reference devices (architecture/patterns only): Essential mata, OnePlus dumpling,
  Razer cheryl and ZTE nx563j. Hardware-specific donor values are not authority.

## Branch audit and selected bases

### Device repository

The `.118` integration line is `lineage-22.2-stock118-rework` (`5fb932b`).
Most older topic branches are TDD/audit/integration branches whose useful work is
already integrated or superseded. `radio-runtime-tdd` and
`vendor-inheritance-final` are strict ancestors of the `.118` line; several
other topic branches diverge because their changes were integrated by later
commits/rebases rather than by retaining the original topic head.

Excluded from bring-up base selection:

- `main`, `legacy-pre-stock118-rework`, `fix/lineage-22.2-runtime-contract`:
  pre-`.118` legacy state.
- `codex-auth-test`: GitHub authorization test only.
- `twrp-12.1`: TWRP/recovery task, not LineageOS system bring-up.
- `tmp-*`: one-shot transport/integration branches.
- `work` and `codex/fix-vndk-28-config`: attempt to filter VNDK 28 from
  `BoardConfig.mk` after product variables are already read-only; not suitable.
- `test/lineage-22.2-bringup`: useful documentation/pinning work, but its paired
  vendor head still requests VNDK 28.

Selected device base:
`codex/fix-vndk-version-assignment-errors` at
`f65a4262b2633fc6d0678be142aee6a57cdad5ae`.

Reason: it is based directly on the complete `.118` rework and removes the
remaining Android 15 product-discovery blocker: importing the generated vendor
BoardConfig that requests the unavailable VNDK 28 snapshot. It keeps mandatory
vendor product inheritance and the explicit recovery v32 compatibility library.

Active bring-up branch:
`codex/lineage-22.2-bringup`.

### Vendor repository

`lineage-22.2-android15-contract` is 55 commits ahead of the original
`lineage-22.2` vendor line and adds the Android 15 ELF, init, VINTF, source/blob
ownership, daemon-completion and validation contracts.

The later `test/lineage-22.2-bringup` moves
`PRODUCT_EXTRA_VNDK_VERSIONS += 28` from `BoardConfigVendor.mk` into product
configuration. That fixes the read-only-variable placement error but still asks
LineageOS 22.2 to package a VNDK v28 snapshot that is not available. It is not
used as the base.

Selected vendor base:
`lineage-22.2-android15-contract` at
`6fef3d7c6333602d7114aefa0284a03f5aadb454`.

Active bring-up branch:
`codex/lineage-22.2-bringup`.

The audit branch removes the obsolete VNDK-28 request while leaving the
proprietary payload byte-equivalent to the selected Android 15 base.

## Recovered project decisions

Confirmed from stock evidence, current code and permanent tests:

- The `.118` firmware, not `.109`, is authoritative for hardware behavior.
- The device is A/B and uses the `.118` boot/fstab/partition contract.
- The exact RED `.118` 4.4.153+ prebuilt kernel is a transitional bring-up
  payload. A validated source-built kernel remains a later milestone.
- Open/source-owned configuration and HAL wrappers belong in the device tree;
  proprietary payload/generated prebuilts belong in the vendor tree.
- No speculative RED `msm8998-common` tree is used.
- Source-owned GNSS/NFC and other wrappers must not coexist with conflicting
  stock prebuilts/services.
- VINTF ownership, init ownership and copy destinations are checked cross-tree.
- Reference devices provide Android 15/LineageOS adaptation patterns only; their
  panel, camera, radio, partition, property or HAL values are not copied without
  Hydrogen One evidence.

Not proven by static evidence:

- that every Android 9 proprietary HIDL/ELF will link and start under Android 15;
- that the device boots;
- SELinux runtime completeness;
- working camera/audio/radio/sensors/display/DRM/GPS/Wi-Fi/BT/NFC/power/thermal;
- slot switching/OTA behavior.

## Vendor payload state

The canonical Android 15 vendor selection contains 499 files. The generated
vendor `proprietary-files.txt`, `proprietary-manifest.json` and on-disk
`proprietary/` payload agree on 499 entries; the manifest hashes/sizes are the
provenance authority. `SOURCE_LOCK.json` records the same 499-file selection.
The current contract classification is P0=108, P1=374, P2 RED/Leia=17.

The device repository's historical `proprietary-files.txt` is only a 93-entry
bootstrap/P0-era subset and is **not** a reproducible description of the current
499-file vendor tree. Two entries in that subset (`vendor/lib64/libllvm-qgl.so`
and `vendor/lib64/libsmemlog.so`) are not present in the final Android 15 vendor
payload. Do not regenerate the production vendor tree from that device-side list
until it is rebuilt from the canonical `.118` manifest with extraction fixups
and pruning semantics preserved.

This mismatch is intentionally recorded as outstanding reproducibility debt;
blindly deleting entries or replacing the list with raw manifest paths would
lose checkelf/fixup/pruning semantics and is not an acceptable fix.

## Cross-tree status

Static contracts cover the chain:

`DEVICE CONFIG -> PACKAGE/HAL -> VENDOR/SOURCE IMPLEMENTATION -> VINTF/INIT -> RUNTIME EXPECTATION`.

Covered areas include camera, audio/media, radio, fingerprint/sensors,
graphics/DRM, GNSS, Wi-Fi/Bluetooth, NFC, power/thermal, firmware, rootdir,
partitions and copy-destination ownership.

Current generated copy-contract evidence is pinned to vendor `201149b...`
and device branch `codex/lineage-22.2-bringup`. The Android 15 vendor tree now
uses the Lineage source-owned `libnbaio_mono`; the obsolete RED Android 9
32/64-bit prebuilts were removed after they shadowed the source module and
broke `audio.r_submix.default`. Regenerate the evidence whenever payload or
generated package ownership changes.

## Confirmed issues found in this audit

1. Android 15 product discovery / VNDK:
   the selected vendor base requested VNDK 28 from `BoardConfigVendor.mk`.
   LineageOS 22.2 cannot package that snapshot. The selected device base stops
   importing that generated board file; the audit vendor branch removes the
   obsolete request and has a regression test forbidding it in both board and
   product vendor configuration.
2. Vendor README provenance counts were stale (`583 / 137 / 431 / 15`) and were
   corrected to the actual Android 15 contract (`499 / 108 / 374 / 17`).
3. Device extraction comments still described the old Android 8.1-era analysis;
   they now explicitly identify those HIDL groups as legacy helpers and `.118`
   as the authoritative current payload.
4. Device `proprietary-files.txt` is a non-canonical 93-entry legacy/bootstrap
   subset; see the reproducibility debt above.
5. Static scan finds `libhidlmemory.recovery` listed twice in `device.mk`.
   This is cleanup debt rather than a second implementation, but should be
   deduplicated before declaring makefile hygiene complete.
6. `device.mk` still contains a stale comment saying stock kernel 4.4.78; the
   `.118` boot contract is 4.4.153+. The `overlay/` path was rechecked and is a
   real (currently empty) directory, so it is not treated as a broken reference.
7. Python bytecode/cache files are tracked in historical tree snapshots. They
   should be removed and ignored; they are not build inputs.
8. The standalone `tests/test_full_tree.py` contract passes when invoked as its
   intended CLI, but naïve `unittest discover` imports it and exits on argument
   parsing. CI already excludes it from discovery and runs it separately.

## Validation performed

On a local copy reproducing the selected device-base VNDK change:

- 94/94 device unit-test modules pass;
- standalone `tests/test_full_tree.py <device-root>` reports
  `full-tree contract: PASS`.

On a local copy reproducing the audit vendor VNDK change and its regression test:

- `python3 -m unittest discover -s tests -v`: 25/25 pass.

Additional static checks:

- vendor proprietary manifest vs on-disk payload: 499/499 paths match and all
  recorded SHA-256/size checks match;
- generated vendor Android.bp module set and `PRODUCT_PACKAGES` selection are
  mutually consistent in the static parser;
- device explicit vendor proprietary references resolve against the vendor
  payload;
- existing stock build, fstab, init, VINTF, camera, radio and cross-tree
  contracts pass static validation on the selected snapshots.

A complete LineageOS 22.2 source checkout is not present in this execution
environment, so no claim of a successful `m nothing`, image build or boot is
made here.

## Next authoritative gates

1. In a clean full LineageOS 22.2 workspace, use the paired audit branches and
   run product discovery / `m nothing` first.
2. Fix only the first real build failure; do not pre-emptively replace HALs or
   hardware values with donor-device values.
3. Then build `bootimage`, `vendorimage`, `systemimage`, target-files and OTA.
4. Validate boot and collect kernel/logcat/dmesg/SELinux/linker/service evidence.
5. Bring up radio, display/graphics, audio, camera, sensors, GNSS, Wi-Fi/BT,
   fingerprint, DRM, power/thermal and OTA/slots as separately testable gates.
6. Regenerate a full canonical `.118` extraction list so device-side extraction
   can reproduce the 499-file Android 15 vendor payload without relying on the
   already-generated vendor repository.
