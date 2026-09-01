# First physical boot and diagnostics

The first generated image built without a device-specific USB init remained on
RED's splash and never enumerated ADB. Static inspection found that TWRP had
installed the legacy `/sys/class/android_usb/android0` USB script even though
the stock H1A1000 kernel enables ConfigFS and uses `a800000.dwc3`.

This revision adds `TW_EXCLUDE_DEFAULT_USB_INIT := true` and a device-specific
`init.recovery.usb.rc` that restores ConfigFS before the recovery `fs` trigger.

Build and validate:

```bash
export ALLOW_MISSING_DEPENDENCIES=true
source build/envsetup.sh
lunch twrp_hydrogenone-eng
m bootimage -j2
python3 device/red/hydrogenone/tools/validate_built_boot.py \
  out/target/product/hydrogenone/boot.img
```

Temporary test only:

```bash
fastboot boot out/target/product/hydrogenone/boot.img
```

Never run `fastboot flash recovery`; H1A1000 is recovery-as-boot.
