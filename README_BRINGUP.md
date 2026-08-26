# RED Hydrogen One H1A1000 - LineageOS 22.2 bring-up v0.3

This tree is a reverse-engineered scaffold based on the supplied stock H1A1000 firmware and
current LineageOS 22.2 MSM8998 devices.

## Confirmed from H1A1000 stock files
- product device `HydrogenONE`, model `H1A1000`
- Qualcomm MSM8998 / Snapdragon 835, ARM64 + 32-bit secondary ABI
- shipped Android 8.1 / API 27
- A/B OTA and system-as-root stock layout
- separate system/vendor partitions
- recovery-as-boot
- UFS controller `soc/1da4000.ufshc`
- stock kernel Linux 4.4.78-perf+, 4096-byte boot pages, `Image.gz-dtb`
- 60 appended DTBs; production PVT variants include TM, TM-CSP, SIM and JDI
- stock HIDL includes camera 2.4, graphics 2.0/2.1, Wi-Fi 1.0, radio 1.1,
  fingerprint 2.1, keymaster 3.0 and RED Leia display 1.0

## Important correction from v0.1: stock vendor is too old to be the final LOS 22.2 vendor
A full ELF scan of the supplied Android 8.1 vendor found:
- 272 vendor ELFs directly needing `libhidlbase.so`
- 267 needing old `libhidltransport.so`
- 172 needing old `libhwbinder.so`

That means keeping the Android 8.1 vendor *completely untouched* is useful only as a diagnostic
phase, not as the intended final Android 15 setup. Current Lineage MSM8998 ports use compatibility
libraries/blob fixups for this class of old HIDL binary.

The intended bring-up is therefore:
1. Keep RED kernel/DTBs initially.
2. Recreate vendor from the H1A1000 stock files.
3. Patch only old proprietary ELF ABI edges (initially HIDL base/transport/hwbinder).
4. Replace standard Qualcomm HAL services with current source-built Lineage/CAF versions subsystem
   by subsystem, while retaining RED-specific blobs/configs.
5. Once userspace is stable, port RED DTS/drivers into the maintained Lineage MSM8998 4.4.302 kernel.

## Donors
See `DONOR_MATRIX.md`. Primary layout donor is Essential PH-1 `mata`; OnePlus 5/5T and Pixel 2/2 XL
are secondary Qualcomm references.

## Stock kernel module trap
Stock vendor init unconditionally loads four `msm-vidc*.ko` modules from `/system/lib/modules`.
Replacing system without copying these stock modules breaks video with the prebuilt RED kernel.
See `reference/analysis/stock_kernel_module_requirements.txt`.

## v0.3 facts confirmed from newly supplied stock system files
- system partition: **4 GiB** (`4294967296`)
- vendor partition: **1 GiB** (`1073741824`)
- these capacities exactly match the maintained Essential PH-1 `mata` LOS 22.2 layout,
  strengthening `mata` as the primary architectural donor
- stock `/system/etc/ld.config.txt` has `namespace.default.isolated=false` for **both**
  framework and vendor process namespaces; the old vendor is not cross-version-clean
- stock 32-bit and 64-bit O-MR1 HIDL transport libraries were archived as ABI references
- stock `system/lib/modules` confirms WLAN/WiGig external modules, while MSM VIDC and QCE
  are built into the RED 4.4.78 kernel despite stale init `insmod` lines

## Next bring-up blocker
The tree is now dimensioned correctly and has a concrete legacy-HIDL strategy.  The next
real milestone is a **source-tree build** against LineageOS 22.2.  Build/linker errors will
tell us which remaining O-MR1 blobs need `libutils-v32`, `libbase`/`libcutils` shims, renamed
protobuf libraries, or subsystem replacement.  After the image boots far enough for ADB,
collect `dmesg`, `logcat -b all`, and `lshal` before replacing more HALs.

## v0.3 linker/partition confirmation
The stock O-MR1 linker configuration is deliberately **reference-only**. Both framework and vendor default namespaces were non-isolated, which allowed vendor processes to resolve libraries directly from `/system`. Android 15 cannot rely on that ABI leak. The LOS 22.2 tree therefore uses modern namespaces and patches old proprietary ELF dependencies toward Lineage compatibility libraries such as `libhidlbase-v32`.

Exact supplied image capacities:
- boot: 67,108,864 bytes (64 MiB)
- system: 4,294,967,296 bytes (4 GiB)
- vendor: 1,073,741,824 bytes (1 GiB)

The 4 GiB system + 1 GiB vendor layout exactly matches current LineageOS 22.2 `mata`, reinforcing Essential PH-1 as the primary A/B MSM8998 architecture donor. H1-specific kernel, DTB, display/touch/fingerprint/SmartPort pieces remain RED-derived.
