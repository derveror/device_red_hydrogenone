# Supplied source lock

This file records the exact inputs used for the RED Hydrogen One LineageOS 22.2 bring-up.

## Target

- LineageOS branch: `lineage-22.2`
- Android target: Android 15 / API 35
- Device: RED Hydrogen One H1A1000 (`hydrogenone`)
- SoC: Qualcomm MSM8998
- Repository topology: `device/red/hydrogenone`, `vendor/red/hydrogenone`, and a separate kernel tree. No RED MSM8998 common repository is permitted.

## Git safety boundary

- Historical baseline commit: `a9e9d30959f1844e3e5ef05cb1c51a05ac29b14e`
- Archival branch: `legacy-pre-stock118-rework`
- Development branch: `lineage-22.2-stock118-rework`

## Canonical stock source

```text
H1A1000.082ho.01.00.10r.118_userdebug_fastboot.rar
size:    1,850,671,123 bytes
SHA-256: 7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e
status:  all 8 parts verified; RAR test passed; 74 files extracted successfully
```

The older `[FileSell]` archive remains recorded as an encrypted alternate with SHA-256 `6fcc610fd86b9b9152f1fcc9d0ca24a4ecba340d8dfd3f011495e2b8fc4d9c6c`.

## Reference archives

| Archive | Embedded source commit | Files | SHA-256 |
|---|---|---:|---|
| `android_device_essential_mata-lineage-22.2.zip` | `76f0a9e6d6ede586c2bdb74f61af04832599ed38` | 383 | `efe76632c3e900cbc2887c21f379e3c5405290e936d406a9160b413b1b364b91` |
| `android_device_nubia_msm8998-common-lineage-22.2.zip` | `d1a3824cff196d85a9ccf04b17c5b2df3484d8bb` | 268 | `af16f85b66c5eca3cfd9a68321277866d53b8fcc6faaf7d544620afd7cd374d4` |
| `android_device_nubia_nx563j-lineage-22.2.zip` | `a0cc35e3839c7f26a0b297b0447165457f28cb8e` | 73 | `26f11d7e70c583ac54e32d36c0c81078007cec046ebdc8bbf8ad367fb64813c8` |
| `android_device_oneplus_dumpling-lineage-22.2.zip` | `673c6b5b76d5d4806759014efb2e9ec8704022da` | 27 | `d7a26294c5b3caa8fd60cb1ff18f2327104a2a16878719d0d47acb0275dbc3d0` |
| `android_device_oneplus_msm8998-common-lineage-22.2.zip` | `213a9c24ebcc555c67fde3af8c7c7951502b20cd` | 136 | `32b996a3478b2e2445e0be8578b229c438242986c1cec5fe12c2fb0c19080366` |
| `android_device_razer_cheryl-lineage-22.2.zip` | `e7990dd5b94c16574c45bd241a23f1abc76b9638` | 230 | `e32bdafc99050519d6af4a465a651e969b72620625f9462e4593002f67c4b023` |
| `device_red_hydrogenone-fix-lineage-22.2-runtime-contract.zip` | `a9e9d30959f1844e3e5ef05cb1c51a05ac29b14e` | 423 | `3e0c611ef94c1c4d703817d60f816aaf0c2e891d27b8f080e0d825617f2499e8` |
| `device_red_hydrogenone-main(1).zip` | `a9e9d30959f1844e3e5ef05cb1c51a05ac29b14e` | 423 | `cd7afbbba2c388abd48dbb6331d25d614d750e30c3e2a13e6708de3f09e99b0b` |
| `proprietary_vendor_essential_mata-lineage-22.2.zip` | `e9ecf8a856e5a1ed389c735643d92b4aa5c395f4` | 861 | `ae63d96f46e94a0c000a38c2fa0cf62d303e7c487bb28da3d2a3dc0828e192bc` |
| `proprietary_vendor_nubia_msm8998-common-lineage-22.2.zip` | `7e2744c4c7ce246b0acb9c81d68deca355e58a63` | 449 | `3c44f6894e25b6b3d33efdce9424ef85d33c37ff6d96a6d612dacbfa88047863` |
| `proprietary_vendor_oneplus_dumpling-lineage-22.2.zip` | `a19d15c9b8da744f8d537b1365e3f7e869239b0d` | 70 | `8e366b0d9b47b55eedfa572338eefe8cd189f36ded22e368efd17a86d9da5bb0` |
| `proprietary_vendor_oneplus_msm8998-common-lineage-22.2.zip` | `de920245bb19635422643ba46d4c6e03a6cd6668` | 736 | `2e805b08de0142b4a683e9bf7648e840b2a82aa091b49b9b8f8de0cb38415a64` |
| `proprietary_vendor_razer_cheryl-lineage-22.2.zip` | `a7725d8bf663838d755aaff953a16c58450e533d` | 731 | `57ddb1285d0d23536f48c123e822afbd56df395d0a48d8023bedac06d1909733` |

## Initial conclusions

- The existing Hydrogen One tree shares 299 relative paths with mata, 253 byte-identically. Donor-derived content remains historical input, not RED hardware truth.
- OnePlus and Nubia device-common trees share 59 relative paths but only eight byte-identically, proving that their common layers are manufacturer-family implementations rather than a universal MSM8998 template.
- Stock-versus-vendor comparison found real Qualcomm-common blobs, but only a minority of each donor list is byte-identical to RED `.118`.
- Donor common trees remain analysis inputs. Selected open configuration is flattened into `device/red/hydrogenone`; proprietary RED payload belongs in `vendor/red/hydrogenone`.
