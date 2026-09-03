# Reference archive analysis

This directory locks and compares the exact device and vendor archives supplied for the RED Hydrogen One LineageOS 22.2 bring-up.

## Files

- `SUPPLIED_SOURCES.md` — human-readable source list, embedded commits, archive hashes, and initial conclusions.
- `source-lock.json` — machine-readable source contract.
- `archive-inventory.json` — compact deterministic archive-level summary for all 13 locked ZIP files.
- `archive-comparisons.json` — compact exact comparison counts for the selected donor pairs.
- `full-artifacts.sha256` — hashes and connected-Drive location of the full per-file reports.

The full reports contain every normalized archive path, file size, SHA-256, ZIP mode, and every comparison path classification. They are stored as `hydrogenone-reference-analysis-2026-09-02.tar.xz` in `/Google Drive/gpt/` and are pinned by SHA-256 in `full-artifacts.sha256`. The bundle contains metadata and hashes only; it does not contain proprietary file contents.

The authoritative design is `docs/superpowers/specs/2026-09-02-hydrogenone-lineage22.2-design.md`.

## Reproducing the inventory

Use an explicit input list. Do not use a broad `device_red_hydrogenone*.zip` glob: the working directory can contain generated or historical ZIP files that are not part of the locked evidence set. The source-lock validator intentionally rejects such an extra archive.

```bash
# Full path/hash inventory used for detailed analysis
python3 tools/analysis/archive_inventory.py \
  --output /tmp/archive-inventory.full.json \
  /mnt/data/android_device_essential_mata-lineage-22.2.zip \
  /mnt/data/android_device_nubia_msm8998-common-lineage-22.2.zip \
  /mnt/data/android_device_nubia_nx563j-lineage-22.2.zip \
  /mnt/data/android_device_oneplus_dumpling-lineage-22.2.zip \
  /mnt/data/android_device_oneplus_msm8998-common-lineage-22.2.zip \
  /mnt/data/android_device_razer_cheryl-lineage-22.2.zip \
  /mnt/data/device_red_hydrogenone-fix-lineage-22.2-runtime-contract.zip \
  '/mnt/data/device_red_hydrogenone-main(1).zip' \
  /mnt/data/proprietary_vendor_essential_mata-lineage-22.2.zip \
  /mnt/data/proprietary_vendor_nubia_msm8998-common-lineage-22.2.zip \
  /mnt/data/proprietary_vendor_oneplus_dumpling-lineage-22.2.zip \
  /mnt/data/proprietary_vendor_oneplus_msm8998-common-lineage-22.2.zip \
  /mnt/data/proprietary_vendor_razer_cheryl-lineage-22.2.zip

# Compact archive-level summary checked into GitHub
python3 tools/analysis/archive_inventory.py \
  --summary-only \
  --output docs/reference/archive-inventory.json \
  /mnt/data/android_device_essential_mata-lineage-22.2.zip \
  /mnt/data/android_device_nubia_msm8998-common-lineage-22.2.zip \
  /mnt/data/android_device_nubia_nx563j-lineage-22.2.zip \
  /mnt/data/android_device_oneplus_dumpling-lineage-22.2.zip \
  /mnt/data/android_device_oneplus_msm8998-common-lineage-22.2.zip \
  /mnt/data/android_device_razer_cheryl-lineage-22.2.zip \
  /mnt/data/device_red_hydrogenone-fix-lineage-22.2-runtime-contract.zip \
  '/mnt/data/device_red_hydrogenone-main(1).zip' \
  /mnt/data/proprietary_vendor_essential_mata-lineage-22.2.zip \
  /mnt/data/proprietary_vendor_nubia_msm8998-common-lineage-22.2.zip \
  /mnt/data/proprietary_vendor_oneplus_dumpling-lineage-22.2.zip \
  /mnt/data/proprietary_vendor_oneplus_msm8998-common-lineage-22.2.zip \
  /mnt/data/proprietary_vendor_razer_cheryl-lineage-22.2.zip

python3 tools/analysis/source_lock.py \
  --validate \
  --lock docs/reference/source-lock.json \
  --inventory docs/reference/archive-inventory.json
```

Expected validator result:

```text
source lock verified: 13 archives
```

The current inventory indexes 4,810 archive files with a combined uncompressed size of 1,303,453,109 bytes.

## Reproducing comparisons

```bash
# Full path-level comparison report
python3 tools/analysis/tree_compare.py \
  --inventory /tmp/archive-inventory.full.json \
  --pair 'device_red_hydrogenone-main(1).zip:device_red_hydrogenone-fix-lineage-22.2-runtime-contract.zip' \
  --pair 'device_red_hydrogenone-main(1).zip:android_device_essential_mata-lineage-22.2.zip' \
  --pair 'device_red_hydrogenone-main(1).zip:android_device_oneplus_msm8998-common-lineage-22.2.zip' \
  --pair 'device_red_hydrogenone-main(1).zip:android_device_nubia_msm8998-common-lineage-22.2.zip' \
  --pair 'android_device_oneplus_msm8998-common-lineage-22.2.zip:android_device_nubia_msm8998-common-lineage-22.2.zip' \
  --pair 'android_device_oneplus_dumpling-lineage-22.2.zip:android_device_oneplus_msm8998-common-lineage-22.2.zip' \
  --pair 'android_device_nubia_nx563j-lineage-22.2.zip:android_device_nubia_msm8998-common-lineage-22.2.zip' \
  --pair 'proprietary_vendor_oneplus_dumpling-lineage-22.2.zip:proprietary_vendor_oneplus_msm8998-common-lineage-22.2.zip' \
  --pair 'proprietary_vendor_oneplus_msm8998-common-lineage-22.2.zip:proprietary_vendor_nubia_msm8998-common-lineage-22.2.zip' \
  --output /tmp/archive-comparisons.full.json

# Compact count-only comparison summary checked into GitHub
python3 tools/analysis/tree_compare.py \
  --inventory /tmp/archive-inventory.full.json \
  --pair 'device_red_hydrogenone-main(1).zip:device_red_hydrogenone-fix-lineage-22.2-runtime-contract.zip' \
  --pair 'device_red_hydrogenone-main(1).zip:android_device_essential_mata-lineage-22.2.zip' \
  --pair 'device_red_hydrogenone-main(1).zip:android_device_oneplus_msm8998-common-lineage-22.2.zip' \
  --pair 'device_red_hydrogenone-main(1).zip:android_device_nubia_msm8998-common-lineage-22.2.zip' \
  --pair 'android_device_oneplus_msm8998-common-lineage-22.2.zip:android_device_nubia_msm8998-common-lineage-22.2.zip' \
  --pair 'android_device_oneplus_dumpling-lineage-22.2.zip:android_device_oneplus_msm8998-common-lineage-22.2.zip' \
  --pair 'android_device_nubia_nx563j-lineage-22.2.zip:android_device_nubia_msm8998-common-lineage-22.2.zip' \
  --pair 'proprietary_vendor_oneplus_dumpling-lineage-22.2.zip:proprietary_vendor_oneplus_msm8998-common-lineage-22.2.zip' \
  --pair 'proprietary_vendor_oneplus_msm8998-common-lineage-22.2.zip:proprietary_vendor_nubia_msm8998-common-lineage-22.2.zip' \
  --summary-only \
  --output docs/reference/archive-comparisons.json
```

Current headline results:

| Left | Right | Shared paths | Byte-identical | Different contents |
|---|---|---:|---:|---:|
| Hydrogen main | Hydrogen runtime-contract | 423 | 423 | 0 |
| Hydrogen main | Essential mata | 299 | 253 | 46 |
| Hydrogen main | OnePlus MSM8998 common | 50 | 3 | 47 |
| Hydrogen main | Nubia MSM8998 common | 139 | 22 | 117 |
| OnePlus MSM8998 common | Nubia MSM8998 common | 59 | 8 | 51 |
| OnePlus Dumpling | OnePlus MSM8998 common | 14 | 1 | 13 |
| Nubia NX563J | Nubia MSM8998 common | 21 | 1 | 20 |
| OnePlus Dumpling vendor | OnePlus MSM8998 common vendor | 3 | 1 | 2 |
| OnePlus MSM8998 common vendor | Nubia MSM8998 common vendor | 400 | 314 | 86 |

## Interpretation rules

A matching relative path is not evidence that the file is valid for Hydrogen One. It proves only that two repositories chose the same path.

A byte-identical open configuration file still requires RED stock or runtime confirmation when it encodes hardware paths, properties, services, partition names, permissions, thermal limits, audio routing, camera sensors, firmware names, or device nodes.

A byte-identical proprietary blob across donors is evidence of a shared Qualcomm binary lineage, not proof that the blob is compatible with RED. A donor blob is not adopted unless its hardware interface, kernel interface, firmware expectations, transitive ELF dependencies, init/VINTF contract, and runtime behavior match Hydrogen One.

The OnePlus and Nubia `msm8998-common` device trees are manufacturer-family layers, not a universal MSM8998 template. Their limited byte-identical overlap supports the project rule that no `device/red/msm8998-common` repository is created.

The larger overlap between OnePlus and Nubia vendor-common trees identifies candidates for Qualcomm-platform classification. Those files remain donor evidence only until they are matched against verified RED `.118` stock.

When an open donor common-tree file is accepted, its semantics are flattened into `device/red/hydrogenone` and all paths, namespaces, module names, and inheritance are rewritten for RED. Proprietary payload and generated proprietary module definitions belong in `vendor/red/hydrogenone`.

Generated inventories store metadata and hashes only. They never embed proprietary file contents or unique per-device data.
