# Action 0012 — Verify every production local-manifest revision on live GitHub

**Manifest:** `docs/manifests/hydrogenone-lineage-22.2.xml`

## Verified projects

### Device

```text
repository: derveror/device_red_hydrogenone
revision: lineage-22.2-stock118-rework
```

Live branch exists. Head observed during this action:

```text
59d2fd5e22506bbb0bb072bcabd788f1cb17d1e5
```

### Vendor

```text
repository: derveror/proprietary_vendor_red_hydrogenone
revision: 6fef3d7c6333602d7114aefa0284a03f5aadb454
```

The exact commit resolves on GitHub and is the same commit pinned by `docs/reference/cross-tree-lock.json`.

### MSM8998 kernel source used for UAPI/header generation

```text
repository: LineageOS/android_kernel_essential_msm8998
revision: lineage-22.2
```

Live branch exists. Head observed:

```text
9c9099707ed19ff15321ed5e10b0659c19384d1b
```

### Qualcomm legacy-um sepolicy

```text
repository: LineageOS/android_device_qcom_sepolicy_vndr
revision: lineage-22.2-legacy-um
```

Live branch exists. Head observed:

```text
6d3b8e5a7baa5271c8823171bee35f0a528b328f
```

## Result

The production local-manifest template does not contain a dead repository or nonexistent branch/SHA. All four fetch targets are currently resolvable.

This verifies source acquisition metadata only; it does not replace an actual `repo sync` or Android build.

## Next action

Create and test a single workspace preflight/build-log script that, from a complete LineageOS 22.2 checkout, verifies the exact device/vendor revision contract, sources `build/envsetup.sh`, lunches `lineage_hydrogenone-userdebug`, runs `m nothing`, and preserves the complete terminal output for deterministic failure analysis.
