# Action 0011 — Clean-checkout local-manifest contract GREEN

**Production branch:** `lineage-22.2-stock118-rework`  
**Manifest commit:** `1c465a88b8d243b2bc16dbcdf0ee7a7214f8ddfa`  
**Regression-test commit:** `324564da28d06e4e5f6ad0785ee49219f14f8722`  
**Permanent verification run:** `33686679780`

## RED -> GREEN summary

The isolated `manifest-readiness-tdd` branch first proved RED for exactly the intended gaps:

- missing `docs/manifests/hydrogenone-lineage-22.2.xml`;
- attempted explicit kernel branch in `lineage.dependencies` conflicted with the older full-tree audit shape.

After inspecting LineageOS 22.2 `roomservice.py`, the dependency strategy was refined:

- the **local manifest** explicitly pins the kernel to `lineage-22.2` for deterministic clean checkout;
- `lineage.dependencies` keeps the kernel branch omitted, which is a supported roomservice contract because GitHub dependencies without a branch are resolved through `get_default_or_fallback_revision()`;
- the non-default sepolicy branch remains explicitly pinned to `lineage-22.2-legacy-um`;
- the custom RED vendor is not placed in `lineage.dependencies`, because roomservice would otherwise resolve it incorrectly as a `LineageOS/...` repository.

## Production manifest

`docs/manifests/hydrogenone-lineage-22.2.xml` contains exactly four projects:

1. `device/red/hydrogenone` -> `derveror/device_red_hydrogenone`, `lineage-22.2-stock118-rework`;
2. `vendor/red/hydrogenone` -> `derveror/proprietary_vendor_red_hydrogenone`, exact pinned commit `6fef3d7c6333602d7114aefa0284a03f5aadb454`;
3. `kernel/essential/msm8998` -> `LineageOS/android_kernel_essential_msm8998`, `lineage-22.2`;
4. `device/qcom/sepolicy-legacy-um` -> `LineageOS/android_device_qcom_sepolicy_vndr`, `lineage-22.2-legacy-um`.

It defines explicit `derveror` and `lineageos` GitHub remotes and contains no RED common-tree paths.

## Verification

Permanent production run `33686679780`:

- `verify`: **SUCCESS**;
- `cross_tree`: **SUCCESS**.

The verify job passed:

- all unittest modules including the new local-manifest contract;
- `test_full_tree.py`;
- canonical stock records;
- exact `.118` boot/kernel payload checks.

The cross-tree job passed against exact vendor commit `6fef3d7c...`.

## Result

The repository now contains a reproducible clean-checkout manifest template and a regression test ensuring its paths/revisions remain synchronized with the pinned vendor contract.

## Next action

Verify the four manifest repository/revision pairs against live GitHub refs, then prepare the minimal clean-workspace bootstrap/build-log capture path leading to the first real `lunch lineage_hydrogenone-userdebug` and `m nothing` on a complete LineageOS 22.2 workspace.
