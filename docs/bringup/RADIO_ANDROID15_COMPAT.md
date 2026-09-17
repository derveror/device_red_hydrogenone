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

## Physical test and QMI closure correction

The first compatibility candidate did publish IRadio 1.4 and RadioConfig 1.1,
so the original Android 15 framework rejection was corrected. Baseband, IMEI
and SIM nevertheless remained absent. The installed-device trace then showed
both `vendor.qcrild` instances crashing roughly every 100 seconds in
`QtiBusSocketTransport::clientLoop()` because `/dev/socket/qmux_radio` did not
exist.

A reversible live test created the stock-required QtiBus socket directory and
`/data/vendor/radio` with their exact owners, modes and SELinux labels. The
`ril_ipc` socket appeared and both daemons remained stable for more than 120
seconds. The permanent init contract additionally copies the packaged QCRIL
database, records its state flags, and handles
`ro.vendor.ril.mbn_copy_completed=1` as stock 118 does.

With QtiBus stable, QCRIL reported
`qmi_client_init_instance returned (-17) for DMS`. Qualcomm's QMI client enum
defines `-17` as a parameter error. The installed QCRIL was therefore using an
incompatible mix of the newer FP3 QCRIL and older RED QMI client/IDL libraries.
Mata, Cheryl, Nubia and OnePlus maintained MSM8998 trees all carry a
byte-identical FP3 QMI closure and the same version-10 QCRIL database. The
vendor tree now packages that complete generation rather than mixing ABIs.

The newer `libqmiservices.so` does not export the IMS-private service object
required by RED's retained 64-bit `lib-imsrcs-v2.so`. RED's stock
`lib-imsrcsbaseimpl.so` does export it, so extraction reproducibly adds that
specific provider as a dependency. Checkelf remains enabled; no undefined
symbol exemption is used.

## Runtime acceptance gate

The corrected closure is build-time verified only until a new OTA is installed. Runtime
acceptance requires all of the following:

1. `gsm.version.baseband` is populated.
2. IMEI is visible to the framework.
3. The inserted SIM is detected.
4. `lshal` exposes `android.hardware.radio@1.4::IRadio/slot1` or newer and
   `android.hardware.radio.config@1.1::IRadioConfig/default`.
5. Logcat contains neither of the two unsupported-HAL errors above.
6. Wi-Fi, camera preview/capture, USB debugging, and normal boot remain intact.
