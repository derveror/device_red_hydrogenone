# Action 0001 — Restore the RED `.118` SSD QSEE listener

## Observed failure

A durable normal-boot trace from the physical H1A1000 proved that the
source-built Linux `4.4.302+` kernel reached Android init. Init then remained
blocked on `wait_for_prop vendor.sys.listeners.registered true` while
`qseecomd` repeatedly exited with status 255.

## Root cause

RED `.118` `qseecomd` loads its mandatory RPMB and SSD listeners with `dlopen`,
so the normal `DT_NEEDED` dependency audit could not discover the SSD listener.
The built vendor image contained `librpmb.so` but omitted `libssd.so`. Stock
`.118` also mounts the dedicated `cmlog` partition at
`/mnt/vendor/persist/data` before starting `qseecomd`.

## Correction

- Retain exact stock `.118` `vendor/lib64/libssd.so` as a P0 blob:
  SHA-256 `9a6b9bee2d010fb6156f2931a6cbea72c0bbab26b565e49524fee10c93024c74`.
- Package `libssd` with its verified ELF providers and normal checkelf policy.
- Mount `/dev/block/bootdevice/by-name/cmlog` as ext4 at
  `/mnt/vendor/persist/data` during `on fs`, before `post-fs` starts `qseecomd`.
- Pin the resulting vendor commit in the device cross-tree contracts.

## Verification

- Device unit tests: 137 passed; full-tree contract passed.
- Vendor unit tests: 80 passed.
- Full LineageOS 22.2 build completed successfully.
- Packaged kernel identifies as Linux `4.4.302+`.
- Packed `vendor.img` copies of `libssd.so` and `qseecomd` match the source
  payload byte-for-byte; ext4 and OTA ZIP integrity checks pass.

Physical validation of this correction remains pending. The next step is to
sideload the rebuilt OTA from Lineage Recovery and perform one controlled normal
boot attempt.
