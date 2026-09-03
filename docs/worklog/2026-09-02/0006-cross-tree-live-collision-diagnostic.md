# Action 0006 — Diagnose live device/vendor copy-destination collisions

**Device repository:** `derveror/device_red_hydrogenone`  
**Device branch:** `lineage-22.2-stock118-rework`  
**Vendor repository:** `derveror/proprietary_vendor_red_hydrogenone`  
**Vendor revision checked:** `6fef3d7c6333602d7114aefa0284a03f5aadb454`

## Recovery-state verification

Before continuing, the branch heads were re-read from GitHub instead of inferred from chat:

- device head observed: `8c3e4cf66e562a12936661301cf0c2e9914521f1`;
- vendor head observed: `6fef3d7c6333602d7114aefa0284a03f5aadb454`.

The current device branch contains the new vendor pin in `cross-tree-lock.json`, the permanent CI checkout uses the same vendor commit, and the diagnostic one-shot workflow is still present.

## Exact live diagnostic

Workflow run `33685212091`, job `100430940661`, executed `tools/analysis/cross_tree_contract.py` against the current device tree and exact pinned vendor tree. The tool returned nonzero because the following install destinations are produced by both trees:

```text
vendor/bin/init.qcom.sensors.sh
vendor/bin/init.qti.ims.sh
vendor/etc/hbtp/qtc800h.bin
vendor/etc/hbtp/qtc800h_8998_660.bin
vendor/etc/hbtp/qtc800s_dsp.bin
vendor/etc/init/android.hardware.biometrics.fingerprint@2.1-service.rc
vendor/etc/init/android.hardware.bluetooth@1.0-service-qti.rc
vendor/etc/init/android.hardware.media.omx@1.0-service.rc
vendor/etc/init/com.qualcomm.qti.wifidisplayhal@1.0-service.rc
vendor/etc/init/hw/init.msm.usb.configfs.rc
vendor/etc/init/qcrild.rc
vendor/etc/init/rild.rc
vendor/etc/init/vendor.cm.hardware.thermal3d@1.0-service.cm.rc
vendor/etc/init/vendor.leia.hardware.leiadisp@1.0-service.rc
vendor/etc/init/vendor.qti.esepowermanager@1.0-service.rc
vendor/etc/init/vendor.rild.rc
vendor/etc/libnfc-mtp-NQ3XX.conf
vendor/etc/libnfc-mtp-NQ4XX.conf
vendor/etc/libnfc-mtp_default.conf
vendor/etc/libnfc-mtp_rf1.conf
vendor/etc/libnfc-mtp_rf2.conf
vendor/etc/libnfc-nci.conf
vendor/etc/libnfc-nci_NCI2_0.conf
vendor/etc/libnfc-nxp_default.conf
vendor/etc/libnfc-qrd-NQ3XX.conf
vendor/etc/libnfc-qrd-NQ4XX.conf
vendor/etc/libnfc-qrd_default.conf
vendor/etc/libnfc-qrd_rf1.conf
vendor/etc/libnfc-qrd_rf2.conf
vendor/etc/permissions/android.hardware.nfc.hcef.xml
vendor/etc/permissions/com.android.nfc_extras.xml
vendor/etc/thermal-engine-3d.conf
vendor/etc/thermal-engine.conf
vendor/firmware/a530_pfp.fw
vendor/firmware/a530_pm4.fw
vendor/firmware/a530_zap.b00
vendor/firmware/a530_zap.b01
vendor/firmware/a530_zap.b02
vendor/firmware/a530_zap.elf
vendor/firmware/a530_zap.mdt
vendor/firmware/a540_gpmu.fw2
vendor/firmware/a540_zap.b00
vendor/firmware/a540_zap.b01
vendor/firmware/a540_zap.b02
vendor/firmware/a540_zap.elf
vendor/firmware/a540_zap.mdt
vendor/firmware/leia_pfp_470.fw
vendor/firmware/leia_pm4_470.fw
```

## Interpretation

This is not caused by the `d30ac190 -> 6fef3d7c` vendor update: that update changes only vendor CI and leaves payload/config byte-identical. The collisions are therefore real ownership duplication between the current evolved device tree and the already-selected proprietary vendor payload.

The old `cross-tree-copy-contract.json` is stale and must not simply have its authority hash changed.

## Required fix strategy

Classify every collision by owner before deletion:

- proprietary RED/Leia/Qualcomm firmware and configuration should normally stay vendor-owned;
- source-owned Android 15 HAL/control-plane files should stay device-owned and be pruned from vendor if stock copies conflict;
- standard AOSP feature XML should be source-owned when equivalent;
- no blanket deletion is allowed.

## Next action

Inspect the exact device and vendor producers for each collision group, classify ownership, encode it in tests, then prune the losing side and regenerate the live cross-tree evidence to zero collisions.
