# LineageOS 22.2 reference-ril Soong header fix

## Failure

A full `m bacon` for Hydrogen One reached `hardware/ril/reference-ril` and failed compiling `reference-ril.c` because `telephony/ril_cdma_sms.h` was not in the compiler include path.

## Root cause

LineageOS 22.2 inherits `libreference-ril` from the generic Android `base_vendor.mk`. The 2024 conversion of `libreference-ril` from Android.mk to Android.bp did not declare the existing `ril_headers` header library, so the Soong compile action lacks `hardware/ril/include`.

This is a platform-source build dependency defect, not a RED proprietary radio ABI defect. The RED `.118` runtime radio stack remains proprietary (`qcrild`/`rild` and Qualcomm radio libraries). MSM8998 references cheryl, mata and dumpling/msm8998-common likewise use Qualcomm proprietary radio payload rather than AOSP reference-ril as their modem implementation.

## Bring-up fix

Run from an initialized LineageOS build shell:

```bash
python3 device/red/hydrogenone/tools/apply_reference_ril_header_fix.py
```

The tool makes one idempotent change to `hardware/ril/reference-ril/Android.bp`:

```bp
header_libs: ["ril_headers"],
```

No RED vendor blobs or runtime radio ownership are changed.
