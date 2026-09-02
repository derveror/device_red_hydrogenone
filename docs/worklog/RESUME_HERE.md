# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

> **READ THIS FILE FIRST AFTER ANY INTERRUPTION.**

**Marker version:** 10  
**Last completed action file:** `docs/worklog/2026-09-02/0013-m-nothing-preflight-tdd-green.md`  
**Logging protocol active:** YES

## Current repository checkpoints

### Device
- Repository: `derveror/device_red_hydrogenone`.
- Branch: `lineage-22.2-stock118-rework`.
- Cross-tree lock pins vendor `6fef3d7c6333602d7114aefa0284a03f5aadb454`.
- Fresh zero-collision cross-tree evidence is pinned to that vendor commit.
- Production local-manifest template: `docs/manifests/hydrogenone-lineage-22.2.xml`.
- Production preflight runner: `tools/build/run_m_nothing_preflight.sh`.
- Permanent production run `33687201146` after preflight promotion passed `verify=success` and `cross_tree=success`.

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

All four production local-manifest refs are live and tested by repository contract:

1. `device/red/hydrogenone` -> device branch `lineage-22.2-stock118-rework`;
2. `vendor/red/hydrogenone` -> exact vendor SHA `6fef3d7c...`;
3. `kernel/essential/msm8998` -> LineageOS branch `lineage-22.2`;
4. `device/qcom/sepolicy-legacy-um` -> LineageOS branch `lineage-22.2-legacy-um`.

## First real build gate

Use only:

```text
device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh
```

The script:

- refuses incomplete or dirty required checkouts;
- verifies exact vendor SHA from the cross-tree lock;
- has a `--validate-only` mode;
- records device/vendor/kernel/sepolicy revisions and host metadata;
- runs only `source build/envsetup.sh`, `lunch lineage_hydrogenone-userdebug`, and `m nothing`;
- preserves full output and exit status under `out/hydrogenone-build-logs/`.

## Hard architecture constraints

- Target LineageOS 22.2 / Android 15 / API 35.
- Never create `device/red/msm8998-common`.
- Never create `vendor/red/msm8998-common` or another RED common vendor repository.
- Open/adapted config -> `device/red/hydrogenone`.
- Proprietary payload/generated proprietary modules -> `vendor/red/hydrogenone`.
- `.118` stock outranks donor assumptions.

## Immediate next action — DO THIS FIRST

Replace the stale historical `BUILD_FIRST.md` instructions that still mention the old `.109` 4.4.78 kernel and `m bacon`. Make it a current pointer to the tested preflight script and canonical `.118` bring-up sequence. Record that documentation cleanup as the next action file.

## After documentation cleanup

Run the tested preflight on the user's complete LineageOS workspace:

1. `--validate-only` first;
2. then the real `m nothing` gate;
3. use the generated `.log`, `.meta.txt`, and `.status` files as the authoritative next debugging input.

Do not start `bootimage`, `vendorimage`, `systemimage`, target-files or OTA until `m nothing` is GREEN.

## Recovery rule

After interruption, do **not** infer state from chat prose. Read this marker, then the last numbered action file, then verify both branch heads and any active workflows from GitHub before continuing.
