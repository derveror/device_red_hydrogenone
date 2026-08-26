# First LOS 22.2 build target

This is the intended first compile/boot experiment, not a claim that all HALs are already fixed.

## Source
Use LineageOS `lineage-22.2`.

Place this tree at:
`device/red/hydrogenone`

Extract the supplied stock blobs into:
`vendor/red/hydrogenone`

## Build target
```bash
source build/envsetup.sh
lunch lineage_hydrogenone-userdebug
m bacon
```

## First-flash philosophy
Keep RED's exact prebuilt 4.4.78 `Image.gz-dtb` for the first userspace bring-up.
Build new `system.img` and `vendor.img`; do not substitute a donor boot image or DTB.

The device is A/B.  Before destructive testing, preserve boot/vendor/system from both slots
and verify the current active slot.

## Expected first failures
1. old O-MR1 proprietary ELF linker dependencies
2. SELinux denials / service labels
3. legacy Qualcomm init services referring to removed Android 8 system binaries
4. camera/media ABI edges
5. radio/IMS Java/framework compatibility

Do not try to solve all five before the first boot log.  Fix the earliest fatal blocker shown
by kernel/init/linker logs, then iterate.
