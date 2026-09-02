# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

> **READ THIS FILE FIRST AFTER ANY INTERRUPTION.**

**Marker version:** 1  
**Last completed action file:** `docs/worklog/2026-09-02/0001-persistent-resume-protocol.md`  
**Logging protocol active:** YES

## Current repository checkpoints

### Device
- Repository: `derveror/device_red_hydrogenone`
- Branch: `lineage-22.2-stock118-rework`
- Last non-log project commit observed before enabling worklog: `4036ecea476c5561001310ec17451cb8bcb18adb`
- Meaning: camera topology/tuning restored from audit-pinned RED `.118` evidence on top of the prior GREEN `.118` build/boot/radio/fstab/vendor-lock work.

### Vendor
- Repository: `derveror/proprietary_vendor_red_hydrogenone`
- Branch: `lineage-22.2-android15-contract`
- Current branch head observed: `6fef3d7c6333602d7114aefa0284a03f5aadb454`
- Parent: `d30ac19025b348ca61535afaaecb23b95347b2f4`
- Device cross-tree lock last known to pin: `d30ac19025b348ca61535afaaecb23b95347b2f4`

## Canonical stock authority

- Build: `H1A1000.082ho.01.00.10r.118`
- Android: 9 / API 28; first API 27
- Archive SHA-256: `7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`
- Boot image contract, `.118` kernel, product identity, vendor patch level, radio DSDS/qcrild startup and major static Android 15 ownership contracts are already pinned in the device repository.

## Hard architecture constraints

- Target: LineageOS 22.2 / Android 15 / API 35.
- Never create `device/red/msm8998-common`.
- Never create `vendor/red/msm8998-common` or a separate RED common vendor repository.
- Open/adapted configuration belongs under `device/red/hydrogenone`.
- Proprietary RED payload/generated proprietary modules belong under `vendor/red/hydrogenone` in `proprietary_vendor_red_hydrogenone`.
- `.118` RED stock outranks donor assumptions.
- Transitional exact `.118` prebuilt kernel is allowed for bring-up; final milestone remains a source-built RED-compatible kernel.

## Next planned action

1. Compare vendor commit `d30ac190...` to current vendor head `6fef3d7c...`.
2. Verify whether `6fef3d7c...` changes payload/contract or is verification-only.
3. If it is a compatible successor, update the device cross-tree lock to the current GREEN vendor head and verify both repositories.
4. Continue the clean-checkout build-readiness gate leading to an actual LineageOS workspace `lunch` + `m nothing`.

## Recovery rule

After an interruption, do **not** infer state from chat prose. Read this marker, then the last numbered action file, then verify both branch heads from GitHub before continuing.
