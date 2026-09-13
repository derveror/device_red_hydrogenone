# RED .118 QTI Keymaster runtime fix

## Symptom

After the securefs/cmlog mount policy correction, normal boot still remained at
the RED logo. Durable diagnostic boot v8 captured the final 256 KiB of kernel
log before returning to Recovery. The kernel did not panic: `qseecomd` stayed
running, `/data` mounted, and `vold` waited for
`android.system.keystore2.IKeystoreService/default` while
`vendor.keymaster-3-0` exited with status 1 once per second.

## Root cause proof

The installed LineageOS system and vendor partitions were mounted read-only in
Recovery and the production Keymaster service was run inside a complete system
chroot under `strace`. The generic MSM8998 implementation opened
`/dev/qseecom`, queried the secure app, then failed with `ENOENT` on
`/vendor/firmware_mnt/image/keymaster.mdt` and exited. Hydrogen One does not
ship file-based Keymaster firmware there: RED `.118` boots the secure app from
its dedicated A/B `keymaster` and `keymaster64` partitions.

The exact RED `.118` QTI service, QTI implementation and
`libkeymasterdeviceutils.so` were then tested in the same chroot without
modifying any phone partition. With a current LineageOS 22.2 source-built
64-bit `libion.so`, the QTI implementation opened `/dev/qseecom` and
`/dev/ion`, completed its TrustZone ioctls, registered
`android.hardware.keymaster@3.0::IKeymasterDevice/default`, and remained
running. A second test used the exact stock filename
`android.hardware.keymaster@3.0-impl-qti.so` with the generic `impl.so`
absent; HIDL discovered the QTI implementation and registered it successfully.

## Permanent tree change

- Stop selecting the generic LineageOS Keymaster 3.0 service and
  implementation from `device.mk`.
- Restore the exact RED `.118` QTI service, rc, implementation and
  `libkeymasterdeviceutils.so` in the proprietary vendor tree.
- Keep legacy HIDL runtime providers in the vendor build; do not duplicate
  them in the device tree.
- Build the required 64-bit `libion.so` from LineageOS 22.2 source.
- Retain the stock service credentials: user `system`, groups `system drmrpc`.
- Use the existing Qualcomm `hal_keymaster_qti` SELinux domain.

## Verification

- Device targeted tests: PASS.
- Vendor targeted and complete tests: PASS.
- Device full-tree contract: PASS.
- Full `mka bacon`: PASS, including prebuilt ELF checks, SELinux/neverallow,
  VINTF, the 4.4.302 kernel and all four RED production DTBs.
- Built vendor output contains only the QTI Keymaster service/implementation;
  the generic service, rc and `impl.so` are absent.
- The chroot runtime test was repeated with the exact stripped 64-bit
  `libion.so` from the completed vendor output; QTI Keymaster again registered
  `IKeymasterDevice/default` and remained running.
- OTA:
  `lineage-22.2-20260913-UNOFFICIAL-hydrogenone.zip`, SHA-256
  `fb4890863015e01bcf210d12c4ad4b5e1b5b0ff256be0937e8ff698bda2b2f65`.
- Boot image: 32,403,456 bytes, SHA-256
  `dd3020b018f2c32c1f264f1f4acbe89e4dd3607fed626d4dc02b196b13c6e50d`.

This is runtime proof of the corrected Keymaster path, not yet proof of a
complete Android boot. The next physical gate is to sideload this OTA and test
normal boot once.
