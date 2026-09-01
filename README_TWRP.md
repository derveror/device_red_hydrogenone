# TWRP 12.1 for RED Hydrogen One (H1A1000)

This branch provides a recovery-as-boot device tree for `device/red/hydrogenone`.

## Locked RED `.109` hardware contract

- MSM8998 / Snapdragon 835.
- Android boot header v0, 4096-byte pages.
- Kernel/base offsets: `0x00008000`, `0x01000000`, `0x00f00000`, `0x00000100`.
- Boot partition: 67,108,864 bytes.
- Exact RED `Image.gz-dtb` SHA-256: `6cf3a70ece8b32dcd6bccf9db1a22c1da29b9b37fe67cc0e4ec9b4f87fec2426`.
- All 60 appended Qualcomm/RED/CloudMinds DTBs.
- A/B recovery-as-boot. There is no standalone `recovery` partition.

No donor kernel or donor DTB is used.

## Build

```bash
mkdir -p ~/twrp-hydrogenone
cd ~/twrp-hydrogenone
repo init -u https://github.com/minimal-manifest-twrp/platform_manifest_twrp_aosp.git -b twrp-12.1
repo sync -c -j2 --force-sync --no-clone-bundle --no-tags

mkdir -p device/red
git clone -b twrp-12.1 https://github.com/derveror/device_red_hydrogenone.git device/red/hydrogenone

source build/envsetup.sh
lunch twrp_hydrogenone-eng
m bootimage -j2
```

Expected image:

```text
out/target/product/hydrogenone/boot.img
```

Run the validators before testing the phone:

```bash
cd device/red/hydrogenone
python3 tools/validate_tree.py .
python3 tools/validate_twrp_boot.py \
  "$ANDROID_BUILD_TOP/out/target/product/hydrogenone/boot.img"
```

## First boot

```bash
adb reboot bootloader
fastboot devices
fastboot boot out/target/product/hydrogenone/boot.img
```

Never use `fastboot flash recovery`: H1A1000 has no recovery partition. If temporary boot is rejected, test through the inactive boot slot only after preparing a verified stock `.109` boot image for restoration.

The first runtime gate is UI, touch, ADB, MTP, slot detection, Format Data and sideload. Crypto support is compiled in, but stock FDE/Lineage FBE decryption remains unproven until tested on a physical H1A1000.
