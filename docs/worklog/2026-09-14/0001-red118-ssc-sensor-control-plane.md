# RED .118 SSC sensor control-plane restoration

## Symptom

Normal boot reached the Lineage animation after the QSEE, QTI Keymaster and ION
corrections, but Android userspace restarted before completing boot. The kernel
remained alive, so another durable kernel and logcat capture was collected with
temporary v16 diagnostics isolated outside the production kernel tree.

## Root cause proof

Durable trace v16 shows `vendor.sensors-hal-1-0` failing once per second with
`Couldn't load sensors module` and `Could not find instance default`.
`system_server` blocks twice for 66 seconds in
`SystemSensorManager.nativeCreate`, reached through
`DeviceStateProviderImpl.setStateConditions`, and is then killed by the Android
software watchdog. The trace contains no kernel panic, GPU fault or hardware
watchdog reset.

Evidence files outside the repositories:

- `kernel_v16.log`, SHA-256
  `bbeeafca62b0c76c0ef43b1385b6d18f4ff6d5ff8e801e8c39b6c1ff75aa970d`;
- `logcat_v16.log`, SHA-256
  `ece3b4d3296433b7348fc2a65cced5152e292a36e0ddcee49a6fe57c348c391e`;
- `headers_v16.txt`, SHA-256
  `1fce57b11b6a6de866754af526f38ec76fa3409955877a6e75bb969d39b8edf8`.

## Permanent tree change

- Restore the exact stock `.118` arm/arm64 `sensors.ssc.so`,
  `libsensor_reg.so`, `libsns_low_lat_stream_stub.so` and `libsdsprpc.so`.
- Restore stock `.118` `hals.conf` and `sensor_def_qcomdev.conf`.
- Retain the Android 15 source-built Sensors HIDL service and implementation;
  do not import the obsolete stock wrapper.
- Boot SLPI, run the stock `sensors.qti` registry daemon through the stock helper
  script, and reproduce stock ownership for the complete persist sensor registry.
- Do not import `sensor_calibrate.so` without a retained consumer, or `sscrpcd`,
  which is absent from the stock `.118` vendor image.
- Keep all temporary v16 diagnostics outside production history.

The corresponding vendor payload is commit
`b9e652a35e9dd5b5bec3dfa349ca445f62b2b0ef` on
`lineage-22.2-kernel-302`.

## Verification

- All four multilib modules pass Android 15 `check_elf_file` for arm and arm64.
- Device unit tests: 146 PASS; vendor tests: 84 PASS.
- Device full-tree contract: PASS; live cross-tree copy collisions: none.
- Full `mka bacon`: PASS in 2:28:30. Final incremental `mka bacon`: PASS in
  6:03 after completing the stock registry-ownership contract.
- SELinux neverallow and VINTF checks: PASS.
- ZIP integrity: PASS.
- Production kernel: Linux `4.4.302+`; FPC, LM36923H, TFA9894 and CYTTSP5
  runtime artifact contracts PASS; exact DTB order is TM, TM CSP, SIM, JDI;
  SmartPort and v16 diagnostic markers are absent.
- OTA: `lineage-22.2-20260914-UNOFFICIAL-hydrogenone.zip`, 853,047,186 bytes,
  SHA-256 `f0b63723a732d16b2e2d6f4b7cb88a84080b7470e45d75f04d1fee83e6c1ecf2`.
- Boot image: 32,391,168 bytes, SHA-256
  `5103376dc9bcd01a9de65c2f4d4398130b14948fe16fabe72a4eef3a7063c5c4`;
  it fits the 64 MiB boot partition.
- Vendor image: 319,480,028 bytes, SHA-256
  `8f28010a5d99d5bf5df7e8a313650d9d7f8e913ad0b0b7ed0a579459c23928d2`;
  it fits the 1 GiB vendor partition.
- Full build log SHA-256:
  `58dd1006962f356c33997c8d8cff83218b86b385a018bc579aa9684833df94aa`.
- Final incremental build log SHA-256:
  `2e3f97d707c5c143e937c330b24aef986840d0204ef169c8b054ae0f164650d6`.

The remaining gate is a physical OTA install and normal-boot trace. Static and
build success do not by themselves prove a complete Android boot or any hardware
subsystem.
