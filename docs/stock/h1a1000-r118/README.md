# RED Hydrogen One H1A1000 `.118` stock intake

This directory defines the evidence and integrity contract for the stock package used to rebuild the LineageOS 22.2 device and vendor trees.

## Expected source

```text
Archive: [FileSell]_H1A1000.082ho.01.00.10r.118_USERDEBUG_FASTBOOT.rar
Google Drive reported size: 1,851,974,911 bytes
Expected update label: H1A1000.082ho.01.00.10r.118
Claimed source Android version: Android 9
```

The Android version is not considered verified from the filename. It must later be confirmed from the extracted `build.prop`/property files, SDK level, build fingerprint, security patch, VNDK properties, boot header, and runtime capture.

The connected Google Drive download path rejects an individual file larger than 268,435,456 bytes. Split parts must therefore remain below this boundary. The project standard is 240 MiB per part.

## Creating uploadable parts

Run in the directory containing the original RAR:

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

Expected part names begin with:

```text
H1A1000_r118.rar.00.part
H1A1000_r118.rar.01.part
H1A1000_r118.rar.02.part
```

Upload every `.part` file, `parts.sha256`, and `original.sha256`. Do not recompress the parts or edit either manifest.

## Manifest format

`parts.sha256` uses the standard `sha256sum` format, one part per line:

```text
<64 lowercase hex characters><two spaces><filename>
```

The manifest order is the reconstruction order. Filenames must be basenames only; directory separators, `.` and `..` entries, duplicate names, malformed hashes, absent parts, and hash mismatches are rejected.

## Reconstruction

Read the final digest from `original.sha256`, then run:

```bash
python3 tools/analysis/reconstruct_stock.py \
  --parts-dir /path/to/H1A1000_r118_parts \
  --manifest /path/to/H1A1000_r118_parts/parts.sha256 \
  --output '/path/to/[FileSell]_H1A1000.082ho.01.00.10r.118_USERDEBUG_FASTBOOT.rar' \
  --expected-sha256 '<digest copied from original.sha256>'
```

The tool performs these operations in order:

1. validates manifest syntax and filenames;
2. validates every part SHA-256 without creating a partial output;
3. concatenates parts in manifest order into `<output>.partial`;
4. flushes and `fsync`s the partial file;
5. verifies the reconstructed RAR SHA-256;
6. atomically renames the verified partial file to the requested output path.

An existing output file is preserved. Replacing it requires the explicit `--replace` option.

## Required verification before extraction

The archive is not accepted as stock evidence until all commands below succeed:

```bash
stat --printf='%s  %n\n' \
  '[FileSell]_H1A1000.082ho.01.00.10r.118_USERDEBUG_FASTBOOT.rar'

sha256sum \
  '[FileSell]_H1A1000.082ho.01.00.10r.118_USERDEBUG_FASTBOOT.rar'

7z t \
  '[FileSell]_H1A1000.082ho.01.00.10r.118_USERDEBUG_FASTBOOT.rar'
```

The recorded size must equal `1,851,974,911` bytes. The SHA-256 must equal the digest in `original.sha256`. `7z t` must report no archive, CRC, or data errors.

After the RAR test succeeds, extraction is performed into a new empty directory. The original RAR and parts remain read-only evidence. The extracted package receives its own complete path/size/SHA-256 manifest before any image is mounted or modified.

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

## Entry gate for the stock extraction phase

The next plan, `docs/superpowers/plans/2026-09-02-hydrogenone-stock118-extraction.md`, is not created or executed until these facts exist:

- verified reconstructed archive SHA-256;
- exact archive size;
- successful `7z t` output;
- extracted package file manifest with SHA-256 values;
- confirmed Android release, SDK, fingerprint, build ID, security patch, and product identity from extracted files.
