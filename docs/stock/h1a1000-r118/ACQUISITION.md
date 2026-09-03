# RED Hydrogen One `.118` stock acquisition report

**Captured:** 2026-09-02  
**Status:** canonical archive reconstructed, tested, extracted, and inventoried

## Canonical source

```text
H1A1000.082ho.01.00.10r.118_userdebug_fastboot.rar
size:    1,850,671,123 bytes
SHA-256: 7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e
format:  RAR5, one volume, non-solid, unencrypted
```

All eight split parts matched `parts.sha256`. Concatenation produced the exact size and digest in `original.sha256`. A complete 7-Zip test returned `Everything is Ok`, and extraction returned the same result:

```text
Folders:    2
Files:      74
Size:       4,630,918,949 bytes
Compressed: 1,850,671,123 bytes
```

`archive-files.tsv` and `extracted-files.sha256` record every extracted fastboot-package file. The canonical package contains `boot.img`, `system.img`, `vendor.img`, `ramdisk.img`, modem/DSP/Bluetooth firmware, Qualcomm GPT/rawprogram/patch data, boot-chain images, flash scripts, and build metadata.

## Important image identities

| Image | Bytes | SHA-256 |
|---|---:|---|
| `boot.img` | 46,495,016 | `8e120a2920f5d4eec65cb5929d31fe271738af85b218d5adb96035eb28806af6` |
| `system.img` | 3,746,394,440 | `5cb9695ecae27ec092b9413a73a90a2178cb815d76b8f197cda5cadee292c1dc` |
| `vendor.img` | 593,264,872 | `8f564431ce915e1e7e5c51b0db48e6154fdc3785494fbee512734a7ae3002156` |
| `ramdisk.img` | 1,905,816 | `1cef7d02466e0f3658270a8574b18e48f67b25d5e603cf0e182f820e79bb527f` |
| `NON-HLOS.bin` | 109,105,152 | `07ce51680158521d6c51fd24291d9d6494594ec5f2ec82221fefc19841f387c5` |
| `BTFM.bin` | 421,888 | `8cf8b8816569e053ab4336dff6908ae5e93ed5051040600a41a764538ba5389e` |
| `adspso.bin` | 16,777,216 | `d0c8b604dd7081cf9e2d94dd5b57d99bca99141a207791fe36901f9886dd4467` |

`persist.img` and `userdata.img` were hashed and format-inspected, but their contents are not published or used as vendor material.

## Alternate encrypted package

A different package supplied earlier remains byte-verified but is not the canonical extracted source:

```text
[FileSell]_H1A1000.082ho.01.00.10r.118_USERDEBUG_FASTBOOT.rar
size:    1,851,974,911 bytes
SHA-256: 6fcc610fd86b9b9152f1fcc9d0ca24a4ecba340d8dfd3f011495e2b8fc4d9c6c
status:  RAR5 headers readable; 78 regular files encrypted
```

Its listing remains in `archive-entries.tsv`; its checksums are preserved under the `encrypted-alternate-*` filenames. The unencrypted archive supersedes it for analysis without erasing its provenance.

## Trust boundary

The canonical archive identity and extraction are now authoritative. This does **not** mean every Android 9 file belongs in LineageOS 22.2. Each file still requires classification as AOSP-built, proprietary blob, firmware, configuration, obsolete/debug material, or prohibited per-device data, followed by Android 15 compatibility analysis.
