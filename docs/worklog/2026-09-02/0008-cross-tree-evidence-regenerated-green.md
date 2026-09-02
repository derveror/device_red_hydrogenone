# Action 0008 — Regenerate cross-tree evidence with isolated vendor root

**Device repository:** `derveror/device_red_hydrogenone`  
**Device branch:** `lineage-22.2-stock118-rework`  
**Vendor revision:** `6fef3d7c6333602d7114aefa0284a03f5aadb454`

## Infrastructure fix

The one-shot workflow was changed so that after `actions/checkout` creates `vendor-tree`, it moves that checkout to:

```text
$RUNNER_TEMP/vendor-tree
```

before invoking `cross_tree_contract.py`.

This keeps the vendor repository outside the recursively scanned device root.

## Verification

Workflow run: `33685771854`  
Job: `100432790735`

All steps succeeded:

1. checkout device tree;
2. checkout exact pinned vendor tree;
3. move vendor outside device scan root;
4. regenerate evidence from isolated roots;
5. verify cross-tree lock/evidence unit tests;
6. commit regenerated evidence and self-remove the one-shot workflow.

The live collision list was empty and the cross-tree tests passed.

## Published result

GitHub Actions committed:

```text
e01f8d83fb20aa90abf1c790fbb0e9ea8871f892
```

Commit message:

```text
docs: regenerate cross-tree evidence for verified vendor head
```

The one-shot `regenerate-cross-tree-evidence.yml` was removed as intended.

## Conclusion

- The vendor pin `6fef3d7c...` is now represented by freshly generated zero-collision cross-tree evidence.
- The earlier 49-item collision list was entirely an artifact of the nested diagnostic checkout.
- No runtime/proprietary files were removed to obtain GREEN.

## Next action

Run/confirm the permanent device `verify-analysis.yml` workflow on commit `e01f8d83...`. If both `verify` and `cross_tree` jobs are GREEN, advance to clean-checkout local-manifest and dependency determinism work.
