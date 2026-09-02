# RED Hydrogen One H1A1000 `.118` stock intake

This directory defines the evidence and integrity contract for the stock package used to rebuild the LineageOS 22.2 device and vendor trees.

## Verified source identity

```text
Archive: [FileSell]_H1A1000.082ho.01.00.10r.118_USERDEBUG_FASTBOOT.rar
Size: 1,851,974,911 bytes
SHA-256: 6fcc610fd86b9b9152f1fcc9d0ca24a4ecba340d8dfd3f011495e2b8fc4d9c6c
Container: RAR5, one volume, non-solid
Visible entries: 79 total, 78 regular files
Encryption: all 78 regular files use RAR5 AES
```

The original archive was supplied as eight parts because the connected Google Drive path rejects an individual download larger than 268,435,456 bytes. All eight part hashes matched `parts.sha256`; concatenation produced the exact size and SHA-256 in `original.sha256`.

Detailed evidence:

- `ACQUISITION.md` — reconstruction and encryption report;
- `archive-entries.tsv` — every archive entry visible before decryption;
- `original.sha256` — canonical RAR digest;
- `parts.sha256` — all eight part digests;
- `SECONDARY_BUILD_METADATA.md` — exact-build public properties, retained as secondary evidence.

## Current gate

Archive headers are readable, but the file data is encrypted. The archive comment states that the password is supplied by the archive vendor as a sold/paid item. The project will not attempt password cracking or bypass that access control.

The stock extraction phase can continue from either of these legitimate inputs:

1. the correct archive password; or
2. the complete locally extracted `fastboot/` directory, accompanied by a `sha256sum` manifest.

Until one of those inputs exists, no claim is made about the bytes inside `boot.img`, `system.img`, `vendor.img`, `NON-HLOS.bin`, the partition XML files, or any other encrypted member.

## Exact-build metadata already established as secondary evidence

A public build-property archive contains files whose identity is exactly:

```text
H1A1000.082ho.01.00.10r.118
RED/HydrogenONE/HydrogenONE:9/PKQ1.190118.001/118:userdebug/release-keys
```

It reports Android 9, SDK 28, first API level 27, A/B updates, system-as-root, Treble, platform `msm8998`, system security patch `2019-04-05`, and vendor security patch `2018-08-05`.

Those facts may guide investigation, but they do not replace comparison with the decrypted files. See `SECONDARY_BUILD_METADATA.md` for the pinned source commit and blob hashes.

## Reproducible splitting procedure

The original parts were created using 240 MiB chunks:

```bash
mkdir -p H1A1000_r118_parts

split \
  -b 240M \
  -d \
  -a 2 \
  --additional-suffix=.part \
  '[FileSell]_H1A1000.082ho.01.00.10r.118_USERDEBUG_FASTBOOT.rar' \
  'H1A1000_r118_parts/H1A1000_r118.rar.'

(
  cd H1A1000_r118_parts
  sha256sum H1A1000_r118.rar.*.part > parts.sha256
)

sha256sum \
  '[FileSell]_H1A1000.082ho.01.00.10r.118_USERDEBUG_FASTBOOT.rar' \
  > original.sha256
```

The checked-in `tools/analysis/reconstruct_stock.py` validates manifest syntax, verifies every part before writing output, concatenates into a temporary file, verifies the final digest, and atomically installs the reconstructed archive.

## Extraction procedure after password availability

Use a new empty destination and never modify the evidence archive:

```bash
archive='[FileSell]_H1A1000.082ho.01.00.10r.118_USERDEBUG_FASTBOOT.rar'
out='stock-r118-extracted'

7zz t -p"$R118_ARCHIVE_PASSWORD" "$archive"
mkdir "$out"
7zz x -p"$R118_ARCHIVE_PASSWORD" -o"$out" -- "$archive"
find "$out" -type f -print0 | sort -z | xargs -0 sha256sum > extracted-files.sha256
```

The password must be provided through an environment variable or interactive prompt and must never be committed to Git.

## Security boundary

The stock package can contain device-specific partitions or files. Analysis output must never publish or commit:

- IMEI, MEID, serial, or modem NV data;
- Widevine/device DRM keys;
- fingerprint enrollment or unique calibration data;
- Wi-Fi or Bluetooth identities;
- user data;
- private certificates or tokens;
- raw `persist`, `modemst`, `fsg`, `frp`, or similar per-device backup contents.

Only generic firmware, configuration, executable metadata, hashes, dependency records, and explicitly reviewed redistributable vendor material may enter the project repositories.

## Entry gate for image analysis

Already satisfied:

- all eight part hashes verified;
- reconstructed size verified;
- reconstructed SHA-256 verified;
- RAR5 headers and complete entry inventory read successfully;
- Android release and build identity independently corroborated as secondary evidence.

Still required:

- legitimate password or locally extracted contents;
- successful full `7zz t` with the password;
- complete extracted-file SHA-256 manifest;
- direct comparison of extracted `build.prop` files with the secondary capture;
- image-format, partition, boot-header, VINTF, init, ELF, firmware, and SELinux analysis.
