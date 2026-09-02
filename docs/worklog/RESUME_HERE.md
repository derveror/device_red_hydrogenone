# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

> **READ THIS FILE FIRST AFTER ANY INTERRUPTION.**

**Marker version:** 11  
**Last completed action file:** `docs/worklog/2026-09-02/0015-build-first-updated-to-stock118-preflight.md`  
**Logging protocol active:** YES

## Current repository checkpoints

### Device
- Repository: `derveror/device_red_hydrogenone`.
- Branch: `lineage-22.2-stock118-rework`.
- Cross-tree lock pins vendor `6fef3d7c6333602d7114aefa0284a03f5aadb454`.
- Fresh zero-collision cross-tree evidence is pinned to that vendor commit.
- Production local-manifest template: `docs/manifests/hydrogenone-lineage-22.2.xml`.
- Production preflight runner: `tools/build/run_m_nothing_preflight.sh`.
- Preflight TDD GREEN and permanent production run `33687201146` passed `verify=success` and `cross_tree=success`.
- `BUILD_FIRST.md` now points only to the canonical `.118` + `m nothing` preflight path; old `.109`/4.4.78/`m bacon` guidance has been removed.

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

All four production local-manifest refs are live:

1. device branch `lineage-22.2-stock118-rework`;
2. exact vendor SHA `6fef3d7c...`;
3. LineageOS kernel branch `lineage-22.2`;
4. LineageOS sepolicy branch `lineage-22.2-legacy-um`.

The custom RED vendor is intentionally acquired through the checked-in local manifest, not `lineage.dependencies`.

## First real build gate

From a complete LineageOS 22.2 top:

```bash
bash device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh --validate-only
bash device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh
```

The second command internally performs only `envsetup`, `lunch lineage_hydrogenone-userdebug`, and `m nothing`, preserving complete logs under `out/hydrogenone-build-logs/`.

## Hard architecture constraints

- Target LineageOS 22.2 / Android 15 / API 35.
- Never create `device/red/msm8998-common`.
- Never create `vendor/red/msm8998-common` or another RED common vendor repository.
- Open/adapted config -> `device/red/hydrogenone`.
- Proprietary payload/generated proprietary modules -> `vendor/red/hydrogenone`.
- `.118` stock outranks donor assumptions.

## Immediate next action — DO THIS FIRST

Create clean-workspace bootstrap documentation next to the local manifest. It must provide a fresh-directory `repo init` + local-manifest installation + `repo sync` path without modifying the tested preflight script. Then statically verify the documented manifest source and commands.

## After bootstrap documentation

The remaining decisive gate is on the user's actual complete LineageOS workspace: run `--validate-only`, then `m nothing`. The generated `.log`, `.meta.txt`, and `.status` become the authoritative next debugging input. Do not advance to image targets until `m nothing` is GREEN.

## Recovery rule

After interruption, do **not** infer state from chat prose. Read this marker, then the last numbered action file, then verify both branch heads and any active workflows from GitHub before continuing.
