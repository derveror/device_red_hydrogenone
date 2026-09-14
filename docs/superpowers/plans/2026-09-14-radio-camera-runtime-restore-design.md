# RED .118 Radio and Camera Runtime Restore Design

## Goal

Restore standard Wi-Fi, Bluetooth, camera, and flashlight operation on the
already booting LineageOS 22.2 system without changing the proven boot,
display, touchscreen, DTB, or recovery path.

## Evidence

- The source Bluetooth vendor library reads `vendor.qcom.bluetooth.soc`, but
  the device only declares legacy aliases and does not package
  `libbt-vendor`.
- RED stock .118 exposes
  `/vendor/firmware/wlan/qca_cld/wlan_mac.bin` as a link to
  `/mnt/vendor/persist/wlan_mac.bin`; the Lineage vendor image omits it.
- Camera logs show all four configured sensors fail with
  `invalid power_setting size_up = 0`.  The RED .118 32-bit camera blob uses
  the structure offset produced by `MAX_POWER_CONFIG == 16`; the kernel UAPI
  currently declares 12.
- The same logs list absent Sony PDAF, ISP, image-processing, and CPP firmware
  modules.  The four production chromatix XML files reference 138 stock .118
  libraries that are absent from the built vendor image.
- The stock `libmmcamera_quadracfa.so` has a direct ELF dependency on
  `libremosaic_daemon.so`; both must be retained as one runtime unit.  The
  resulting production camera closure contains exactly 185 stock .118 files.

## Design

Keep the kernel change limited to the two public camera UAPI headers.  Restore
the exact Bluetooth property/module contract in the device tree.  Restore the
stock Wi-Fi MAC link without synthesizing or overwriting a persist MAC.  Add
only the camera closure selected by the four production XML files plus modules
requested by the captured runtime log and known sensor support modules.

The proprietary files remain owned by `vendor/red/hydrogenone` and are
extracted from the exact RED .118 vendor image.  Dynamically requested files
that are absent even from stock .118 are treated as optional and are not
invented or imported from another device.

## Safety boundary

- Do not modify DTS, defconfig, DTB order, display, touchscreen, recovery,
  boot image layout, or init ordering.
- Do not add SmartPort support.
- Do not flash or reboot the phone.
- Do not claim runtime hardware success before a fresh image is installed and
  live logs are collected.
