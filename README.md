# TWRP device tree for RED Hydrogen One (H1A1000)

Target: TWRP 12.1, `bootimage` (A/B recovery-as-boot).

- Qualcomm MSM8998 / Snapdragon 835
- stock RED `.109` prebuilt `Image.gz-dtb`
- boot header v0, 4096-byte pages, 64 MiB boot partition
- system/vendor A/B slot selection
- recovery root fstab + TWRP flags
- RED physical key layout and ueventd rules

Build:

```bash
repo init -u https://github.com/minimal-manifest-twrp/platform_manifest_twrp_aosp.git -b twrp-12.1
repo sync -c -j2
source build/envsetup.sh
lunch twrp_hydrogenone-eng
m bootimage -j2
```

First test with `fastboot boot out/target/product/hydrogenone/boot.img`.
Do not use `fastboot flash recovery`: this device has no standalone recovery partition.

TWRP 12.1 upstream does not support legacy stock FDE decryption. The tree is aimed first at boot/UI/ADB/storage and modern ROM use; stock encrypted `/data` may require formatting or a legacy recovery/decryption path.
