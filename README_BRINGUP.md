# RED Hydrogen One LineageOS 22.2 bring-up notes

The current device-tree branch is `118-lineage-22.2-kernel-302`. Hardware facts
come from RED build `H1A1000.082ho.01.00.10r.118`; donor MSM8998 trees provide
only LineageOS adaptation patterns.

## Hardware and partition contract

- RED Hydrogen One H1A1000, Qualcomm MSM8998;
- ARM64 with 32-bit secondary ABI;
- A/B update layout and recovery-as-boot;
- 64 MiB boot, 4 GiB system and 1 GiB vendor partitions;
- real UFS path `/dev/block/platform/soc/1da4000.ufshc`;
- Android 15 file-based encryption migration for userdata.

## Kernel contract

LineageOS builds `kernel/red/msm8998` with
`lineageos_hydrogenone_defconfig`. The tree is Linux 4.4.302 and contains only
the exact RED TM, TM CSP, SIM and JDI DTB targets. No kernel image stored in the
device repository is used by the build.

The canonical `.118` boot image remains immutable evidence for boot header v1,
page size, load addresses, command line, partition limit and stock DTB order.

SmartPort is excluded from both kernel and init scope. USB, USB-C charging,
Bluetooth, display/Leia, cameras, fingerprint and the normal phone power paths
remain required functionality.

## Vendor and HIDL contract

The pinned vendor commit is recorded in
`docs/reference/cross-tree-lock.json`. It contains 459 selected `.118` files.
The platform HIDL base libraries come from LineageOS source rather than RED
prebuilts.

Compatibility is limited to evidence-backed transformations:

- 63 retained `.118` interface consumers load `libhidlbase_shim`;
- `imsdatadaemon` resolves its ProcessState import through Android 15
  `libhidlbase`;
- the ARM32 face-processing blob clears exactly three obsolete symbol versions.

The extraction script reproduces those transformations when the vendor tree is
regenerated from stock.

## Runtime ownership

- Device tree: open configuration, rootdir, SELinux and source wrappers.
- Vendor tree: proprietary RED payload and generated proprietary modules.
- Kernel tree: RED source kernel, DTBs and modules.

The Android 15 rootdir starts the two `.118` DSDS qcrild instances and uses
first-stage fstab mounts. Device and vendor copy destinations are checked for
collisions.

## Build order

From a complete LineageOS 22.2 workspace, first run:

```bash
bash device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh --validate-only
bash device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh
```

After `m nothing` succeeds, build `bootimage`, `vendorimage`, `systemimage`,
target-files and OTA in that order. A passing repository audit is not a boot
claim; physical testing must retain a recoverable stock slot and collect kernel,
init, SELinux, linker and service logs.
