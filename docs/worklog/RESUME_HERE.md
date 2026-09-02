# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

> **READ THIS FILE FIRST AFTER ANY INTERRUPTION.**

**Marker version:** 9  
**Last completed action file:** `docs/worklog/2026-09-02/0012-live-manifest-revisions-verified.md`  
**Logging protocol active:** YES

## Current repository checkpoints

### Device
- Repository: `derveror/device_red_hydrogenone`.
- Branch: `lineage-22.2-stock118-rework`.
- Cross-tree lock pins vendor `6fef3d7c6333602d7114aefa0284a03f5aadb454`.
- Fresh zero-collision cross-tree evidence is pinned to that vendor commit.
- Production local-manifest template: `docs/manifests/hydrogenone-lineage-22.2.xml`.
- Local-manifest regression test: `tests/test_local_manifest_contract.py`.
- Permanent production verification after manifest promotion passed both `verify` and `cross_tree`.

### Vendor
- Repository: `derveror/proprietary_vendor_red_hydrogenone`.
- Branch: `lineage-22.2-android15-contract`.
- Current GREEN head and device pin: `6fef3d7c6333602d7114aefa0284a03f5aadb454`.

## Canonical stock authority

- Build: `H1A1000.082ho.01.00.10r.118`.
- Android 9 / API 28; first API 27.
- Archive SHA-256: `7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`.
- Exact `.118` boot/kernel, product identity, vendor patch, DSDS/qcrild, fstab migration, camera topology/tuning and major Android 15 ownership contracts are pinned.

## Clean-checkout source acquisition status

All four production local-manifest refs have been verified live on GitHub:

1. device branch `lineage-22.2-stock118-rework` exists;
2. exact vendor SHA `6fef3d7c...` resolves;
3. `LineageOS/android_kernel_essential_msm8998` branch `lineage-22.2` exists (head observed `9c9099707ed19ff15321ed5e10b0659c19384d1b`);
4. `LineageOS/android_device_qcom_sepolicy_vndr` branch `lineage-22.2-legacy-um` exists (head observed `6d3b8e5a7baa5271c8823171bee35f0a528b328f`).

The custom RED vendor remains intentionally outside `lineage.dependencies`; the checked-in local manifest is its acquisition mechanism.

## Hard architecture constraints

- Target LineageOS 22.2 / Android 15 / API 35.
- Never create `device/red/msm8998-common`.
- Never create `vendor/red/msm8998-common` or another RED common vendor repository.
- Open/adapted config -> `device/red/hydrogenone`.
- Proprietary payload/generated proprietary modules -> `vendor/red/hydrogenone`.
- `.118` stock outranks donor assumptions.

## Immediate next action — DO THIS FIRST

Create and test a single workspace preflight/build-log script. It must run from a complete LineageOS 22.2 top, verify required paths and the exact vendor commit, source `build/envsetup.sh`, run `lunch lineage_hydrogenone-userdebug`, execute `m nothing`, and save a complete timestamped log plus concise environment/revision metadata. It must fail without mutating the source tree when prerequisites are absent.

## After preflight script GREEN

Use it on the user's complete LineageOS workspace. The first real `m nothing` output becomes the authoritative next debugging input; fix only errors emitted by that build, then advance through `bootimage`, `vendorimage`, `systemimage`, target-files and OTA gates.

## Recovery rule

After interruption, do **not** infer state from chat prose. Read this marker, then the last numbered action file, then verify both branch heads and any active workflows from GitHub before continuing.
