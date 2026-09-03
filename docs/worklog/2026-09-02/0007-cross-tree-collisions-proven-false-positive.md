# Action 0007 — Prove cross-tree collision list was a diagnostic false positive

**Diagnostic workflow run:** `33685648028`  
**Job:** `100432382834`  
**Device branch:** `lineage-22.2-stock118-rework`  
**Pinned vendor:** `6fef3d7c6333602d7114aefa0284a03f5aadb454`

## Investigation

The diagnostic workflow was enhanced to print both producer makefile lists for every reported destination collision.

For every one of the 49 previously reported destinations, the output had this shape:

```text
DEVICE=["vendor-tree/hydrogenone-vendor.mk"]
VENDOR=["hydrogenone-vendor.mk"]
```

Examples included qcrild RC, fingerprint/Bluetooth/OMX RC, NFC configs, thermal configs, HBTP firmware, Adreno firmware and Leia firmware. There were **zero** reported collisions whose device-side producer was an actual device makefile such as `device.mk`.

## Root cause

The one-shot workflow checked the vendor repository out at:

```text
<device repository root>/vendor-tree
```

It then invoked:

```text
cross_tree_contract.py --device-root . --vendor-root vendor-tree
```

`cross_tree_contract.py` intentionally scans all `*.mk` recursively under `device_root`. Because `vendor-tree` was nested inside `.`, the same vendor `hydrogenone-vendor.mk` was scanned once as part of the supposed device root and again as the vendor root.

Therefore all 49 collisions were the vendor tree colliding with **itself**.

## Conclusion

- The 49-item list from Actions 0004/0006 is **not evidence of runtime device/vendor ownership duplication**.
- No device or vendor payload/config file should be deleted because of that list.
- The production `cross_tree_contract.py` behavior is correct for its normal use where device and vendor roots are separate sibling directories.
- The permanent `verify-analysis.yml` cross-tree job already uses sibling paths `device-tree` and `vendor-tree`, so it does not have this nesting bug.
- The one-shot regeneration workflow must move the vendor checkout outside the device scan root before running the tool.

## Next action

Fix only `regenerate-cross-tree-evidence.yml` so the vendor checkout is moved to `$RUNNER_TEMP/vendor-tree`, rerun the live audit, regenerate the evidence for vendor `6fef3d7c...`, remove the one-shot workflow on success, and restore permanent CI to GREEN.
