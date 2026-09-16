# Hydrogen One radio compatibility for LineageOS 22.2

## Runtime diagnosis

The pre-fix runtime capture is stored at:

`/home/surface/los/logs/hydrogenone/radio-baseline-20260916-034802`

The RED 118 modem subsystem, QMI transport, both `qcrild` instances, and SIM
indications were alive. Android 15 rejected the published interfaces instead:

- `IRadio <1.4 is no longer supported.`
- `IRadioConfig <1.1 is no longer supported.`

The missing baseband, IMEI, and SIM UI were therefore a userspace radio-HAL
compatibility failure, not evidence of a missing NON-HLOS image or kernel modem
failure.

## Source decision

RED stock 118 remains authoritative for modem firmware and device-specific
configuration, but its Android 9 QCRIL only publishes IRadio 1.1/1.2. The
LineageOS 22.2 trees for Essential Mata, Razer Cheryl, OnePlus MSM8998-common,
and Nubia MSM8998-common all use the same newer Qualcomm QCRIL generation from
FP3 6.A.025.0 to publish IRadio 1.4/1.5.

Hydrogen One adopts the ABI-minimal portion of that proven stack: `qcrild`, the
QCRIL implementation, its new-only framework/data/interface providers, and the
Lineage radio-config compatibility shims. RED 118 modem firmware, QRTR name
service, TFTP/WLAN path, camera stack, and other device-specific daemons are not
replaced.

The QCRIL blob's RadioConfig dependencies are redirected to
`android.hardware.radio.c_shim@1.0-1.2`; the Lineage wrapper publishes
`android.hardware.radio.config@1.1` to Android 15. The vendor manifest publishes
IRadio 1.4 and the Lineage RadioConfig backend. Stock 118 DSDS and SIM power
properties are retained.

## Runtime acceptance gate

The change is build-time verified only until a new OTA is installed. Runtime
acceptance requires all of the following:

1. `gsm.version.baseband` is populated.
2. IMEI is visible to the framework.
3. The inserted SIM is detected.
4. `lshal` exposes `android.hardware.radio@1.4::IRadio/slot1` or newer and
   `android.hardware.radio.config@1.1::IRadioConfig/default`.
5. Logcat contains neither of the two unsupported-HAL errors above.
6. Wi-Fi, camera preview/capture, USB debugging, and normal boot remain intact.
