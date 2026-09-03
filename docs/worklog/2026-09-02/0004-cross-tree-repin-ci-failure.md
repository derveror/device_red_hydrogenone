# Action 0004 — Advance cross-tree lock to current vendor head; CI failure captured

**Device repository:** `derveror/device_red_hydrogenone`  
**Device branch:** `lineage-22.2-stock118-rework`  
**Vendor repository:** `derveror/proprietary_vendor_red_hydrogenone`

## Action

Updated `docs/reference/cross-tree-lock.json`:

- previous vendor commit: `d30ac19025b348ca61535afaaecb23b95347b2f4`;
- new vendor commit: `6fef3d7c6333602d7114aefa0284a03f5aadb454`.

Device commit that changed the lock: `5cc099b7fa65ab183476ed403351c82013084974`.

## Verification result

Permanent device workflow run `33684878692` failed.

Two jobs failed:

- `verify` — failure during `Run all unit-test modules`;
- `cross_tree` — failure during `Verify pinned cross-tree ownership contract`.

Earlier JSON/source-lock validation passed, so the failure is not malformed JSON or an unreadable lock file.

## Important conclusion

Although `6fef3d7c...` changes only the vendor CI workflow relative to `d30ac190...`, the device-side tests encode additional assumptions about the exact pinned vendor revision/contract. The lock must not be declared GREEN until the failing tests are inspected.

No force-push or blind rollback was performed.

## Next action

Read the exact logs for jobs `100429832398` (`verify`) and `100429832118` (`cross_tree`), identify the first concrete assertion failures, and fix or revert only based on that evidence.
