# Action 0005 — Audit clean-checkout dependency acquisition

**Target:** clean LineageOS 22.2 checkout leading to `lunch lineage_hydrogenone-userdebug` and `m nothing`.

## Device dependency file observed

Current `lineage.dependencies` contains only:

1. `LineageOS/android_device_qcom_sepolicy_vndr` -> `device/qcom/sepolicy-legacy-um`, branch `lineage-22.2-legacy-um`;
2. `LineageOS/android_kernel_essential_msm8998` -> `kernel/essential/msm8998`, branch currently implicit.

It does **not** contain the custom RED vendor repository.

## External branch verification

- `LineageOS/android_kernel_essential_msm8998` has branch `lineage-22.2`, observed head `9c9099707ed19ff15321ed5e10b0659c19384d1b`.
- `LineageOS/android_device_qcom_sepolicy_vndr` has branch `lineage-22.2-legacy-um`, observed head `6d3b8e5a7baa5271c8823171bee35f0a528b328f`.

## Critical roomservice finding

Current LineageOS 22.2 `vendor/lineage/build/tools/roomservice.py` constructs ordinary `lineage.dependencies` GitHub projects as:

```text
name="LineageOS/<repository>"
remote="github"
```

Therefore `derveror/proprietary_vendor_red_hydrogenone` **cannot** be represented as a normal `lineage.dependencies` entry: doing so would incorrectly resolve under the `LineageOS/` organization.

## Consequence

A reproducible clean checkout needs a checked-in local-manifest strategy for the custom device/vendor repositories. `lineage.dependencies` should remain for LineageOS-owned dependencies, with the kernel branch made explicit for determinism.

## Proposed next build-readiness change

Create and test a local-manifest template that pins:

- `derveror/device_red_hydrogenone` -> `device/red/hydrogenone` on `lineage-22.2-stock118-rework`;
- `derveror/proprietary_vendor_red_hydrogenone` -> `vendor/red/hydrogenone` at the exact cross-tree lock commit;
- LineageOS kernel and legacy sepolicy dependencies at their required branches.

Also make the kernel branch explicit in `lineage.dependencies` so roomservice and manual manifest flows agree.

## Status

Analysis only; no dependency file changed in this action.
