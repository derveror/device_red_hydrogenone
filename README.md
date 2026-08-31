# RED Hydrogen One (`hydrogenone`) — LineageOS 22.2

Full source-side device configuration for the RED Hydrogen One H1A1000 (Snapdragon 835 / MSM8998).
The tree is intended for `device/red/hydrogenone`.

## Design

Hardware authority is the RED H1A1000 `.109` stock firmware. The maintained Essential PH-1
`mata` LineageOS 22.2 tree is used as the primary MSM8998/A-B/Treble architectural reference;
OnePlus 5/5T and Nubia Z17 are secondary references. Donor-specific hardware data is not used as
RED hardware configuration.

The first bring-up deliberately keeps the exact RED stock `Image.gz-dtb` so that RED/CloudMinds
board DTBs, panels, touch, fingerprint and SmartPort wiring are not replaced by donor hardware.

## Included source-side subsystems

- `audio/` — RED `.109` audio policy, Tasha mixer, sound-trigger and platform configuration.
- `configs/camera/` — RED `.109` camera module topology and all stock chromatix-selection XMLs.
- `configs/nfc/` — RED/NXP PN80T-family NFC configuration.
- `gps/`, `location/` — MSM8998 Qualcomm GNSS source stack with RED stock configs. The optional
  SS5 `libsynergy_loc_api` blueprint is inactive because RED `.109` does not select that backend and
  its QMI link libraries belong to the future vendor tree.
- `keylayout/` — power, volume and two-stage camera shutter layout.
- `media/` — RED stock media codec/profile configuration.
- `overlay/`, `overlay-lineage/`, `rro_overlays/` — Hydrogen One framework/Lineage/Wi-Fi overlays.
- `power/` — RED stock power hint configuration.
- `rootdir/` — Android 15-adapted fstab, init, USB and ueventd configuration.
- `seccomp/` — media seccomp policy from stock.
- `sepolicy/` — source SELinux policy adapted from maintained MSM8998 patterns and RED paths.
- `wifi/` — RED stock WCNSS and supplicant configuration.
- `prebuilt/` — exact stock 4.4.78 kernel payload and extracted kernel config.
- `tools/` — targeted Android 8.1 HIDL compatibility data used by `extract-files.py`.

A `bluetooth/impl` directory is intentionally **not** copied from mata: mata's implementation reads
Essential-specific Bluetooth address storage. RED uses the stock Qualcomm Cherokee provider; its
binary/provider closure belongs in the future `vendor/red/hydrogenone` tree. The same rule applies
to donor-only `devicesettings` and hardware-specific powerstats implementations.

## Vendor tree

Proprietary blobs are not bundled here. Future vendor output is wired at:

```text
vendor/red/hydrogenone
```

`BoardConfig.mk` conditionally includes `BoardConfigVendor.mk`, and the product conditionally
inherits `hydrogenone-vendor.mk`. `proprietary-files.txt` and `extract-files.py` are included for that next stage. Source-owned
configuration paths are removed from the proprietary inventory to avoid duplicate installs.

## Kernel / boot contract

The initial diagnostic kernel is the exact RED `.109` payload:

- Linux 4.4.78-perf+
- `Image.gz-dtb`
- SHA-256 `6cf3a70ece8b32dcd6bccf9db1a22c1da29b9b37fe67cc0e4ec9b4f87fec2426`
- boot header v0
- page size 4096
- boot partition 64 MiB
- system partition 4 GiB
- vendor partition 1 GiB

This old kernel is a bring-up choice, not a release-quality Android 15 kernel.

LineageOS native Qualcomm modules also require generated Linux UAPI headers during
`vendorimage`. Because RED did not publish a matching kernel source tree, the maintained
LineageOS `android_kernel_essential_msm8998` tree is downloaded at
`kernel/essential/msm8998` and used **only** for `headers_install`. The exact RED
`Image.gz-dtb` remains forced through `TARGET_FORCE_PREBUILT_KERNEL := true`; no Mata
kernel image or DTB is placed in the Hydrogen One boot image.

## Legacy ARM graphics ELF exceptions

The exact RED `.109` ARM32 graphics stack retains legacy ARM EABI
compiler-runtime references. The first real `vendorimage` failure exposed
`libgsl.so` (`__aeabi_ul2d`, `__aeabi_uldivmod`), and the next run exposed
`libEGL_adreno.so` (`__aeabi_ldivmod`). A complete `readelf --dyn-syms` audit
then identified the same narrowly defined non-memory `__aeabi_*` class in nine
ARM32 P0 blobs.

LineageOS 22.2 bionic still lists these compatibility exports across
`libc/arch-arm/bionic/libcrt_compat.c`, `libc/libc.map.txt`, and the ARM-only
`LIBC_DEPRECATED` block in `libm/libm.map.txt`. The Soong vendor prebuilt checker
nevertheless rejects the old Android 8.1 references. The proprietary list uses
file-scoped `DISABLE_CHECKELF` only for the audited ARM32 inputs; no ARM64 source
entry is flagged and no RED binary is modified or replaced by a Mata payload.

Because extract-utils combines each ABI pair into one Soong module, the generated
`check_elf_files: false` property is module-wide. The vendor regression test
compensates by pinning every ARM32 source hash and exact strong non-memory EABI
symbol set, while ensuring that the ARM64 proprietary-file entries remain
unflagged. This bypass only removes Soong's static check; physical-device linker
validation remains mandatory during bring-up.

## Legacy RED Vulkan private-symbol exception

The RED Android 8.1 `vendor/lib64/hw/vulkan.msm8998.so` additionally references
`android::AHardwareBuffer_to_ANativeWindowBuffer(const AHardwareBuffer*)`. In
LineageOS 22.2 the full `libnativewindow` still implements and exports this symbol
inside the `LIBNATIVEWINDOW_PLATFORM` version node, but the vendor-facing stub
used by `check_elf_file` intentionally omits platform-only C++ exports. This makes
the static checker fail even though the implementation remains in the platform
library.

The exact RED Vulkan blob is therefore given its own file-scoped
`DISABLE_CHECKELF`; it is not replaced by Mata's newer Android 29 Vulkan payload.
The blob hash and exact undefined symbol are pinned by the vendor regression test.
This remains a runtime hypothesis until the Vulkan SP-HAL loads successfully on
the physical H1A1000; a linker failure there will require a dedicated shim or a
carefully matched newer MSM8998 graphics stack rather than a broader bypass.

## Build target

Place this repository at `device/red/hydrogenone`, then from a LineageOS 22.2 checkout:

```bash
source build/envsetup.sh
breakfast hydrogenone
lunch lineage_hydrogenone-bp1a-userdebug
m nothing -j1
```

After `vendor/red/hydrogenone` is generated, continue with `vendorimage`, `bootimage`, `systemimage`
and `bacon`. A successful static build still does not prove device boot; physical H1A1000 logs are
required for runtime validation.

## Lineage dependencies

The tree pins `android_device_qcom_sepolicy_vndr` to `lineage-22.2-legacy-um` at
`device/qcom/sepolicy-legacy-um`. It also declares the same maintained MSM8998 kernel source
used by the official Mata tree at `kernel/essential/msm8998`, solely to generate UAPI headers
needed by source-built Qualcomm modules. The RED boot kernel remains the verified stock
prebuilt and is never replaced by the dependency.
