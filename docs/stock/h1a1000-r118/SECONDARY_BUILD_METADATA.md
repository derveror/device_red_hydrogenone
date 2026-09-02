# RED Hydrogen One `.118` exact-build property evidence

**Evidence status:** secondary, pending comparison with the decrypted supplied archive.

## Provenance

The public `xdaGari/tadiphone-buildprop-archive` repository contains three property captures under:

```text
.other/red/hydrogenone/HydrogenONE-userdebug-9-PKQ1.190118.001-118-release-keys/
```

Pinned source commit:

```text
4f53547b326b17b140fb70e9f2aebd2344cc3af6
```

Captured source blobs:

| File | Git blob SHA |
|---|---|
| `system.system.build.prop` | `1f723ebfba74471d96ff416e8a67286495136786` |
| `system.system.product.build.prop` | `95ae909ca9297797f53ababe780def7fd3bb02d5` |
| `vendor.build.prop` | `e128605ea758112ad73dbc70c745547e86c85e33` |

These files match the exact `.118` build identity, but they are not accepted as substitutes for extracting and hashing the supplied stock images.

## Confirmed build identity from the secondary capture

| Property | Value |
|---|---|
| `ro.build.id` | `PKQ1.190118.001` |
| `ro.build.display.id` | `H1A1000.082ho.01.00.10r.118` |
| `ro.build.version.incremental` | `118` |
| `ro.build.version.release` | `9` |
| `ro.build.version.sdk` | `28` |
| `ro.build.version.security_patch` | `2019-04-05` |
| `ro.vendor.build.security_patch` | `2018-08-05` |
| `ro.build.date.utc` | `1560961030` |
| `ro.build.type` | `userdebug` |
| `ro.build.tags` | `release-keys` |
| `ro.build.flavor` | `HydrogenONE-userdebug` |
| `ro.build.fingerprint` | `RED/HydrogenONE/HydrogenONE:9/PKQ1.190118.001/118:userdebug/release-keys` |
| `ro.product.model` | `H1A1000` |
| `ro.product.brand` | `RED` |
| `ro.product.name` | `HydrogenONE` |
| `ro.product.device` | `HydrogenONE` |
| `ro.product.manufacturer` | `RED` |
| `ro.product.internaledition` | `H1A1000.082ho.01.00.10r.118_r20032_G58793.2_190620_0003` |
| `ro.product.board` | `msm8998` |
| `ro.board.platform` | `msm8998` |
| `ro.product.first_api_level` | `27` |
| `ro.build.system_root_image` | `true` |
| `ro.build.ab_update` | `true` |
| `ro.treble.enabled` | `true` |
| `ro.fota.platform` | `MSM8998_9.0` |
| `ro.fota.oem` | `cloudminds8998_9.0` |
| `ro.fota.version` | `H1A1000.082ho.01.00.10r.118_20190620-0019` |

## Hardware and vendor-contract clues requiring direct stock verification

The captured properties identify the following candidates for later dependency mapping:

- Qualcomm `msm8998`, arm64 primary ABI with 32-bit compatibility;
- Bluetooth SoC `cherokee`;
- NFC implementation `nqx.default`;
- Qualcomm RIL path `libril-qc-qmi-1.so` and DSDS radio configuration;
- audio offload/fluence properties and a 192-frame audio HAL period;
- camera auxiliary exposure, SAT, HAL post-processing, dual-FOV and UBWC controls;
- IMS/VoLTE/VT and IWLAN properties;
- FPC wake-up control, suggesting an FPC fingerprint stack;
- RED/CloudMinds camera platform version properties;
- `/proc/bt_mac` as the stock Bluetooth address source;
- FRP partition path `/dev/block/bootdevice/by-name/frp`.

None of these properties are copied verbatim into LineageOS 22.2 merely because they existed on Android 9. Every retained setting must have an Android 15 consumer, a correct property namespace, and evidence from the decrypted images or runtime capture.

## Android 15 adaptation boundary

The target remains LineageOS 22.2 / Android 15 / API 35. In particular:

- old `persist.*`, `vendor.*` and `ro.*` properties must be checked against Android 15 property-context and ownership rules;
- `/system/vendor/...` paths must be normalized to the actual Android 15 partition layout;
- Android 9 HIDL declarations and services require VINTF and service-instance verification;
- Android 9 SELinux binaries or compiled policy are never imported;
- the old first API level, VNDK contract and system-as-root layout inform compatibility decisions but do not dictate the new build structure.
