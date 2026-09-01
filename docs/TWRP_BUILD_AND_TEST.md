# TWRP build and hardware-test procedure

## Host verification

```bash
cd device/red/hydrogenone
bash tools/run_twrp_tests.sh
```

After building `boot.img`:

```bash
bash tools/run_twrp_tests.sh \
  "$ANDROID_BUILD_TOP/out/target/product/hydrogenone/boot.img"
```

Do not continue unless the tree and boot-image validators pass.

## Confirm bootloader and slots

```bash
adb reboot bootloader
fastboot devices
fastboot getvar unlocked
fastboot getvar current-slot
fastboot getvar slot-successful:a
fastboot getvar slot-successful:b
```

Normal and critical unlock must already be complete.

## Preferred temporary boot

```bash
fastboot boot "$ANDROID_BUILD_TOP/out/target/product/hydrogenone/boot.img"
```

Wait up to 90 seconds, then test:

```bash
adb wait-for-device
adb shell getprop ro.twrp.version
adb shell getprop ro.boot.slot_suffix
adb shell ls -l /dev/block/bootdevice/by-name
adb shell cat /etc/recovery.fstab
```

## Inactive-slot fallback

Use only when `fastboot boot` is rejected and a verified stock `.109` `boot.img` is ready for restoration. Example when the original current slot is `a`:

```bash
sha256sum stock-109-boot.img twrp-hydrogenone-boot.img
fastboot flash boot_b twrp-hydrogenone-boot.img
fastboot --set-active=b
fastboot reboot recovery
```

Do not overwrite `boot_a` in this example. Restore after a failed test:

```bash
fastboot flash boot_b stock-109-boot.img
fastboot --set-active=a
fastboot reboot
```

Reverse the slot letters when the original slot is `b`.

## Evidence to collect after ADB starts

```bash
mkdir -p hydrogenone-twrp-evidence
adb shell getprop > hydrogenone-twrp-evidence/getprop.txt
adb shell dmesg > hydrogenone-twrp-evidence/dmesg.txt
adb shell logcat -b all -d > hydrogenone-twrp-evidence/logcat-all.txt
adb shell cat /proc/cmdline > hydrogenone-twrp-evidence/cmdline.txt
adb shell cat /proc/version > hydrogenone-twrp-evidence/version.txt
adb shell ls -l /dev/block/bootdevice/by-name > hydrogenone-twrp-evidence/by-name.txt
adb shell cat /etc/recovery.fstab > hydrogenone-twrp-evidence/recovery.fstab.txt
adb pull /tmp/recovery.log hydrogenone-twrp-evidence/recovery.log
```

Record display, touch, buttons, ADB, MTP, current slot, partition mounts, microSD, USB OTG, Format Data and sideload separately.

## Encryption gate

A successful UI boot does not prove decryption. Test stock `.109` encrypted data, Format Data, Lineage credential-encrypted storage and a second TWRP unlock/mount as separate steps. Crypto failure does not invalidate UI, ADB, sideload or formatting; it identifies the next keymaster/QSEE integration task.
