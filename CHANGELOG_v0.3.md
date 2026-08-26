# v0.3

- Filled exact 4 GiB system and 1 GiB vendor partition sizes.
- Added vendor to A/B OTA partition set now that the port builds a vendor image.
- Confirmed stock `ld.config.txt` has non-isolated default namespaces for both system and vendor.
- Switched legacy-HIDL plan to LineageOS 22.2 `libhidlbase-v32.vendor`.
- Archived supplied O-MR1 32/64-bit HIDL libraries as ABI references only.
- Added supplied `/system/lib/modules` inventory, SHA-256 values and vermagic.
- Corrected v0.2's MSM VIDC module assumption: VIDC is built into the stock kernel.
- Confirmed QCE/QCEDEV are also built into the stock kernel; stale factory insmods are nonessential.
- Removed stock `vendor/etc/fstab.qcom` from proprietary list so the Android-15-adapted fstab wins.
- Added vendor copy of the adapted fstab and kept first-stage recovery copy.

## Additional corrections after stock system/module inspection
- Confirmed the supplied boot image itself is exactly 67,108,864 bytes (64 MiB), matching `BOARD_BOOTIMAGE_PARTITION_SIZE`.
- Confirmed system image capacity 4,294,967,296 bytes (4 GiB) and vendor image capacity 1,073,741,824 bytes (1 GiB).
- Stock `ld.config.txt` has `namespace.default.isolated=false` in both `[system]` and `[vendor]`. Do **not** ship this linker config on Android 15; keep it only as ABI reference.
- Replaced historical `/system/vendor/...` paths in a source-owned `init.target.rc` with `/vendor/...`.
- Removed four stale `msm-vidc*.ko` insmods: stock kernel config has VIDC built in and those modules are absent from the supplied stock module set.
- Kept WLAN module loading from `/vendor/lib/modules/qca_cld3_wlan.ko`.
- Disabled `qvrd` during initial bring-up because `/system/bin/qvrservice` was not present in the supplied vendor dump; restore only after locating/porting the stock system binary if actually needed.
- Switched custom-ROM `PRODUCT_DEVICE` to lowercase `hydrogenone` while preserving stock `ro.vendor.product.device=HydrogenONE` for proprietary compatibility.
- Added modern Lineage `setup-makefiles.py` wrapper for regenerating the proprietary vendor makefiles from `extract-files.py`.
