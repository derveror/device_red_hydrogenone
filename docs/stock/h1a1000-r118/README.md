# RED Hydrogen One H1A1000 `.118` stock evidence

This directory is the evidence root for rebuilding the RED Hydrogen One device and vendor trees for LineageOS 22.2 / Android 15.

## Authority

The canonical stock package is the unencrypted and fully verified archive:

```text
H1A1000.082ho.01.00.10r.118_userdebug_fastboot.rar
SHA-256: 7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e
```

All eight parts, the reconstructed RAR, the full archive test, and extraction passed. The older `[FileSell]` package is retained only as a byte-verified encrypted alternate.

## Directory map

- `ACQUISITION.md` — transport, reconstruction, archive-test, and extraction evidence.
- `ANALYSIS_STATUS.md` — verified stock findings and remaining work.
- `DONOR_STOCK_COMPARISON.md` — exact stock-versus-donor measurements and adoption rules.
- `inventory-summary.json` — machine-readable high-level stock contract.
- `archive-files.tsv` — all 74 regular files in the unencrypted fastboot package.
- `extracted-files.sha256` — SHA-256 manifest for those package files.
- `image-hashes.sha256` — primary image identities.
- `original.sha256` / `parts.sha256` — canonical archive reconstruction identities.
- `archive-entries.tsv` and `encrypted-alternate-*` — preserved provenance for the first encrypted package.
- `analysis-evidence.sha256` — identity of the full reproducible analysis bundle.

## Non-negotiable migration rule

Android 9 is the hardware and stock-runtime authority, not the target software architecture. LineageOS 22.2 targets Android 15/API 35. Old paths, HIDL declarations, properties, init services, SELinux policy, linker assumptions, and package contracts are retained only when an Android 15 consumer and validation method are documented.

No `device/red/msm8998-common` or `vendor/red/msm8998-common` repository may be created. Open configuration selected from donor common trees is flattened and adapted into `device/red/hydrogenone`; proprietary RED payload belongs in `vendor/red/hydrogenone`.

## Security boundary

Never commit raw `persist`, modem NV, userdata, IMEI/MEID material, DRM keys, Wi-Fi/Bluetooth identities, enrollment data, private certificates, or device-unique calibration. Generic firmware/configuration may enter the vendor tree only after path, consumer, redistribution, and Android 15 compatibility review.
