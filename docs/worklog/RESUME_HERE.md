# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

> **READ THIS FILE FIRST AFTER ANY INTERRUPTION.**

**Marker version:** 8  
**Last completed action file:** `docs/worklog/2026-09-02/0011-clean-checkout-manifest-green.md`  
**Logging protocol active:** YES

## Current repository checkpoints

### Device
- Repository: `derveror/device_red_hydrogenone`.
- Branch: `lineage-22.2-stock118-rework`.
- Cross-tree lock pins vendor `6fef3d7c6333602d7114aefa0284a03f5aadb454`.
- Fresh zero-collision cross-tree evidence is pinned to that vendor commit.
- Permanent run `33686679780` after promoting the clean-checkout manifest contract passed `verify=success` and `cross_tree=success`.
- Production local-manifest template: `docs/manifests/hydrogenone-lineage-22.2.xml`.
- Local-manifest regression test: `tests/test_local_manifest_contract.py`.

### Vendor
- Repository: `derveror/proprietary_vendor_red_hydrogenone`.
- Branch: `lineage-22.2-android15-contract`.
- Current GREEN head and device pin: `6fef3d7c6333602d7114aefa0284a03f5aadb454`.

## Canonical stock authority

- Build: `H1A1000.082ho.01.00.10r.118`.
- Android 9 / API 28; first API 27.
- Archive SHA-256: `7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`.
- Exact `.118` boot/kernel, product identity, vendor patch, DSDS/qcrild, fstab migration, camera topology/tuning and major Android 15 ownership contracts are pinned.

## Clean-checkout manifest contract

The template pins:

1. `device/red/hydrogenone` -> `derveror/device_red_hydrogenone`, branch `lineage-22.2-stock118-rework`;
2. `vendor/red/hydrogenone` -> `derveror/proprietary_vendor_red_hydrogenone`, exact commit `6fef3d7c...`;
3. `kernel/essential/msm8998` -> `LineageOS/android_kernel_essential_msm8998`, branch `lineage-22.2`;
4. `device/qcom/sepolicy-legacy-um` -> `LineageOS/android_device_qcom_sepolicy_vndr`, branch `lineage-22.2-legacy-um`.

The custom RED vendor is intentionally not placed in `lineage.dependencies`; LineageOS roomservice would otherwise resolve it under the `LineageOS/` organization. The kernel dependency remains branch-less in `lineage.dependencies`, which is a supported roomservice contract: current LineageOS 22.2 `roomservice.py` resolves missing GitHub dependency branches via `get_default_or_fallback_revision()`. The local manifest provides the explicit deterministic kernel pin for clean checkout.

## Hard architecture constraints

- Target LineageOS 22.2 / Android 15 / API 35.
- Never create `device/red/msm8998-common`.
- Never create `vendor/red/msm8998-common` or another RED common vendor repository.
- Open/adapted config -> `device/red/hydrogenone`.
- Proprietary payload/generated proprietary modules -> `vendor/red/hydrogenone`.
- `.118` stock outranks donor assumptions.

## Immediate next action — DO THIS FIRST

Verify that all four repository/revision pairs from `docs/manifests/hydrogenone-lineage-22.2.xml` are live/reachable on GitHub, including the exact vendor SHA. Record the result as the next numbered worklog action.

## After live revision verification

1. Create a minimal clean-workspace bootstrap/build-log capture path.
2. Establish the exact commands for `repo init`, local-manifest installation and `repo sync`.
3. Move to the first real complete LineageOS 22.2 workspace gate: `source build/envsetup.sh`, `lunch lineage_hydrogenone-userdebug`, `m nothing`.
4. Fix only errors emitted by that actual build.

## Recovery rule

After interruption, do **not** infer state from chat prose. Read this marker, then the last numbered action file, then verify both branch heads and any active workflows from GitHub before continuing.
