# RED Hydrogen One `.118` stock acquisition report

**Captured:** 2026-09-02

## Reconstruction verification

- Canonical archive: `[FileSell]_H1A1000.082ho.01.00.10r.118_USERDEBUG_FASTBOOT.rar`
- Reconstructed size: `1851974911` bytes
- SHA-256: `6fcc610fd86b9b9152f1fcc9d0ca24a4ecba340d8dfd3f011495e2b8fc4d9c6c`
- Split parts: `8/8` matched the supplied `parts.sha256` manifest.
- Reconstructed archive size and SHA-256 matched `original.sha256` exactly.
- Container: RAR5, one volume, non-solid, 79 blocks.
- Archive headers are readable; all 78 regular files are AES-encrypted.
- Extraction status: blocked by the archive password. No image payload has been trusted or analyzed as extracted stock yet.

## Archive contents visible without decryption

- Entries: `79` (`78` files, `1` directory).
- Declared uncompressed file size: `4635168668` bytes.
- Key payloads include `boot.img`, `ramdisk.img`, `system.img`, `vendor.img`, `NON-HLOS.bin`, Qualcomm firehose/GPT/rawprogram/patch files, and boot-chain images.

### Largest declared files

| Path | Declared size (bytes) | Encrypted |
|---|---:|:---:|
| `fastboot/system.img` | 3746394440 | yes |
| `fastboot/vendor.img` | 593264872 | yes |
| `fastboot/NON-HLOS.bin` | 109105152 | yes |
| `fastboot/boot.img` | 46495016 | yes |
| `fastboot/otafs_ufs_2gb.img` | 36364976 | yes |
| `fastboot/persist.img` | 33554432 | yes |
| `fastboot/mdtp.img` | 17808306 | yes |
| `fastboot/adspso.bin` | 16777216 | yes |
| `fastboot/splash.img` | 11075640 | yes |
| `fastboot/userdata.img` | 5756588 | yes |
| `fastboot/adb.exe` | 5462626 | yes |
| `fastboot/xbl.elf` | 2686892 | yes |
| `fastboot/tz.mbn` | 1912832 | yes |
| `fastboot/ramdisk.img` | 1905816 | yes |
| `fastboot/fastboot.exe` | 1339392 | yes |

## Encryption boundary

The RAR comment states that the password is supplied by the archive vendor as a sold/paid item. Public site-name and contact-string candidates were tested only to rule out a published generic password; 7-Zip reported `Wrong password`. No password cracking or access-control bypass is part of this project. The next accepted input is either the legitimate password or a locally extracted copy of the archive contents.

## Trust boundary

This report proves that the supplied split files reconstruct the expected byte-identical RAR. It does not prove the contents of any encrypted member. Build properties found independently in a public exact-build archive are recorded separately and remain secondary evidence until the RAR payload is decrypted and compared.

## Next verification after password availability

1. Test the complete archive with 7-Zip.
2. Extract into a clean directory without overwriting unrelated files.
3. Hash every extracted member and validate image formats.
4. Confirm Android release, SDK, fingerprint, security patches, partition metadata, boot header, VINTF, init, and proprietary payload directly from the extracted images.
