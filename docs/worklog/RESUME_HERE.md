# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

> **READ THIS FILE FIRST AFTER ANY INTERRUPTION.**

**Marker version:** 2  
**Last completed action file:** `docs/worklog/2026-09-02/0003-verify-current-vendor-head.md`  
**Logging protocol active:** YES

## Current repository checkpoints

### Device
- Repository: `derveror/device_red_hydrogenone`
- Branch: `lineage-22.2-stock118-rework`
- Last non-log project commit observed before enabling worklog: `4036ecea476c5561001310ec17451cb8bcb18adb`
- Logging commits after that do not change device runtime/build behavior.

### Vendor
- Repository: `derveror/proprietary_vendor_red_hydrogenone`
- Branch: `lineage-22.2-android15-contract`
- Current verified GREEN head: `6fef3d7c6333602d7114aefa0284a03f5aadb454`
- Previous device-pinned commit: `d30ac19025b348ca61535afaaecb23b95347b2f4`
- Comparison result: `6fef3d7c...` is exactly one commit ahead and changes only `.github/workflows/verify-vendor-contract.yml`; proprietary payload/config is unchanged.

## Canonical stock authority

- Build: `H1A1000.082ho.01.00.10r.118`
- Android: 9 / API 28; first API 27
- Archive SHA-256: `7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`
- Boot image contract, exact `.118` transitional kernel, product identity, vendor patch level, radio DSDS/qcrild startup, fstab migration and major Android 15 ownership contracts are pinned and statically tested.

## Hard architecture constraints

- Target: LineageOS 22.2 / Android 15 / API 35.
- Never create `device/red/msm8998-common`.
- Never create `vendor/red/msm8998-common` or a separate RED common vendor repository.
- Open/adapted configuration belongs under `device/red/hydrogenone`.
- Proprietary RED payload/generated proprietary modules belong under `vendor/red/hydrogenone` in `proprietary_vendor_red_hydrogenone`.
- `.118` RED stock outranks donor assumptions.
- Transitional exact `.118` prebuilt kernel is allowed for bring-up; final milestone remains a source-built RED-compatible kernel.

## Next planned action

1. Update `docs/reference/cross-tree-lock.json` to vendor commit `6fef3d7c6333602d7114aefa0284a03f5aadb454`.
2. Verify permanent device CI/cross-tree checks on the updated lock.
3. Continue clean-checkout build-readiness work leading to an actual LineageOS workspace `lunch lineage_hydrogenone-userdebug` and `m nothing`.

## Recovery rule

After an interruption, do **not** infer state from chat prose. Read this marker, then the last numbered action file, then verify both branch heads from GitHub before continuing.
