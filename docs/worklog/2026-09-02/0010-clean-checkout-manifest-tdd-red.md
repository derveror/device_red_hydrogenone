# Action 0010 — Clean-checkout manifest/dependency contract TDD RED

**Isolated branch:** `manifest-readiness-tdd`  
**Permanent workflow reused:** `Verify stock intake and analysis tooling`  
**RED run:** `33686111572`  
**Verify job:** `100433903439`

## Test introduced

`tests/test_local_manifest_contract.py` defines the required clean-checkout contract:

- a well-formed `docs/manifests/hydrogenone-lineage-22.2.xml`;
- exact `device/red/hydrogenone` project from `derveror/device_red_hydrogenone`, revision `lineage-22.2-stock118-rework`;
- exact `vendor/red/hydrogenone` project from `derveror/proprietary_vendor_red_hydrogenone`, revision equal to the cross-tree lock commit;
- exact `kernel/essential/msm8998` project from `LineageOS/android_kernel_essential_msm8998`, revision `lineage-22.2`;
- exact `device/qcom/sepolicy-legacy-um` project from `LineageOS/android_device_qcom_sepolicy_vndr`, revision `lineage-22.2-legacy-um`;
- explicit GitHub remotes;
- no RED `msm8998-common` projects;
- explicit branch pins for the Lineage-owned kernel/sepolicy entries in `lineage.dependencies`;
- custom RED vendor must not be declared as a normal `lineage.dependencies` entry because Lineage roomservice would resolve it under the `LineageOS/` organization.

## RED verification

The existing full static suite ran. All previously established device/stock/radio/fstab/camera/vendor/cross-tree tests passed before the new manifest tests.

The new contract failed only for the expected missing implementation:

1. `docs/manifests/hydrogenone-lineage-22.2.xml` does not exist — expected RED;
2. `kernel/essential/msm8998` in `lineage.dependencies` has no explicit branch (`None` vs `lineage-22.2`) — expected RED.

The test proving that the custom vendor is **not** incorrectly present in `lineage.dependencies` was already GREEN.

## Conclusion

This is a clean TDD RED, not an infrastructure failure. The required implementation scope is narrow and known.

## Next action

Create the four-project local-manifest template and add the explicit `lineage-22.2` branch to the kernel dependency. Re-run the same full permanent verification suite on the isolated branch and require GREEN before promoting only the production files to `lineage-22.2-stock118-rework`.
