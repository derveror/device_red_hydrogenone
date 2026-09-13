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

Physical validation of this policy correction is the next gate; successful
compilation is not recorded as proof of a successful Android boot.
