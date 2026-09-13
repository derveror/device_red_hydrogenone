# Action 0002 — Restore the RED `.118` securefs mount permission

## Physical evidence

The OTA containing the SSD QSEE listener was sideloaded successfully to slot
`B`. A durable 100-second normal-boot trace proved that `qseecomd` now remains
running and publishes `vendor.sys.listeners.registered=true` in 39 ms. Android
init consequently advances through `late-fs` and into `post-fs-data`.

The same trace exposed the next deterministic blocker. Init's stock-derived
mount of `cmlog` at `/mnt/vendor/persist/data` failed with this enforcing
SELinux denial:

```text
avc: denied { mounton } comm="init" path="/mnt/vendor/persist/data"
scontext=u:r:init:s0 tcontext=u:object_r:persist_drm_file:s0 tclass=dir
```

Without that mount, `vendor.keymaster-3-0` exited with status 1 on every start,
and vold remained blocked in `cryptfs enablefilecrypto` waiting for Keystore.

## Root cause proof

- The physical `cmlog` filesystem contains RED `.118` securefs state under
  `keymaster64`, `widevine`, `tz` and `app_g`.
- Stock `.118` mounts that partition at `/persist/data` before starting
  `qseecomd`.
- Stock `.118` policy contains the exact permission
  `allow init persist_drm_file:dir mounton;`.
- The device policy omitted that single RED-specific permission.
- Both phone slots contain byte-exact `.118` `keymaster64.mbn`, `cmnlib.mbn`
  and `cmnlib64.mbn` prefixes.
- The packaged legacy keystore and QSEECom blobs are byte-identical to the
  working LineageOS 22.2 `mata` and `cheryl` MSM8998 blobs.

## Correction

Grant only `mounton` from `init` to the existing `persist_drm_file` directory
type. Keep the cmlog mount early in `on fs`, before qseecomd and Keymaster.
A regression test binds the init command and this policy permission together.

## Verification

- 137 device unit tests passed; full-tree contract passed.
- Android SELinux policy, neverallow checks and context tests passed.
- A complete LineageOS 22.2 OTA build passed.
- VINTF compatibility and OTA ZIP integrity passed.
- Output ZIP SHA-256:
  `6f0d377c91cf8d825f82a16560519750b0123b47ebe6dea684944dce8ebc463f`.
- Output boot SHA-256:
  `de425880b858568353a2c93cc2b9c91903402d55ed0975c49ab334169b354d03`.

## Physical validation result

The verified OTA was sideloaded from Lineage Recovery while slot `B` was
running. Update Engine wrote and verified `boot_a`, `system_a` and `vendor_a`,
reported `Update successfully applied`, and recovery finished with status 0.
The saved recovery log has SHA-256
`56f30165150452c31eb0fd6491b9eea30919e36532607cd6168d00e9a609a0bc`.

The subsequent normal-boot attempt did not complete. The physical device
remained on the RED logo for at least 150 seconds, exposed neither ADB nor
fastboot over USB, and did not automatically return to the bootloader during
that observation window. This is a different symptom from the earlier rapid
return to the bootloader, but it is not proof that the securefs/Keymaster gate
was passed. A new durable normal-boot trace is required before the next code
change. LineageOS boot is not claimed.
