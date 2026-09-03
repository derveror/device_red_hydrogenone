# Action 0003 — Verify current vendor head against pinned vendor commit

**Device repository:** `derveror/device_red_hydrogenone`  
**Vendor repository:** `derveror/proprietary_vendor_red_hydrogenone`  
**Vendor branch:** `lineage-22.2-android15-contract`

## Inputs

- Device cross-tree lock pinned vendor commit: `d30ac19025b348ca61535afaaecb23b95347b2f4`.
- Current vendor branch head: `6fef3d7c6333602d7114aefa0284a03f5aadb454`.

## Comparison

GitHub comparison `d30ac190... -> 6fef3d7c...`:

- status: direct `ahead` successor;
- commits ahead: `1`;
- payload/config changes: none;
- only changed path: `.github/workflows/verify-vendor-contract.yml`.

Therefore proprietary files, manifests, generated Soong modules and vendor makefiles are byte-identical between the pinned commit and current vendor head.

## Verification

GitHub Actions run for `6fef3d7c6333602d7114aefa0284a03f5aadb454`:

- workflow: `Verify Android 15 vendor contract`;
- conclusion: `success`.

## Result

`6fef3d7c...` is a compatible, GREEN verification-only successor of the device-pinned `d30ac190...` commit. It is safe to advance the device cross-tree lock to `6fef3d7c...` without changing proprietary payload behavior.

## Next action

Update `docs/reference/cross-tree-lock.json` in the device tree to vendor commit `6fef3d7c6333602d7114aefa0284a03f5aadb454`, then run the permanent device cross-tree verification.
