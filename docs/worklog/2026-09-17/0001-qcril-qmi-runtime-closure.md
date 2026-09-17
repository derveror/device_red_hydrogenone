# QCRIL QMI runtime closure

## Physical failure

The first Android 15-compatible QCRIL candidate booted the system and published
IRadio 1.4 plus RadioConfig 1.1, but the phone still reported an unknown
baseband, no IMEI and no SIM. The device was already on the complete RED `.118`
firmware base, so the failure was investigated in userspace before changing the
kernel or firmware.

Both `vendor.qcrild` instances crashed roughly every 100 seconds in
`QtiBusSocketTransport::clientLoop()`. `/dev/socket/qmux_radio` was absent.
Creating the exact stock-required paths live was deliberately reversible:

- `/dev/socket/qmux_radio`, owner `radio:radio`, mode `2770`, context
  `qmuxd_socket`;
- `/data/vendor/radio`, owner `system:radio`, mode `0770`, context
  `vendor_radio_data_file`.

The `ril_ipc` socket appeared immediately and both QCRIL instances stayed alive
for more than 120 seconds. This isolated the first failure to the missing init
runtime contract.

## Second boundary

Once QtiBus was stable, QCRIL logged
`qmi_client_init_instance returned (-17) for DMS`. Qualcomm's QMI client enum
defines `-17` as `QMI_CLIENT_PARAM_ERR`. The new QCRIL binary was paired with
older RED QMI client and IDL libraries, which was an internally inconsistent
runtime generation.

The maintained Mata, Cheryl, Nubia and OnePlus MSM8998 vendor trees were
compared. All four carry byte-identical FP3 6.A.025.0 copies of the required
QMI closure and the same version-10 QCRIL database. That repeated reference
agreement was used only for Android 15 compatibility; RED `.118` remains the
authority for modem firmware and device-specific configuration.

## Implemented correction

Device init now creates the QtiBus socket and radio-data directories, initializes
the QCRIL database flags, copies the packaged database, and handles
`ro.vendor.ril.mbn_copy_completed=1` in the stock order.

The vendor tree now packages one coherent FP3 generation of:

- `libqmi.so`, `libqmi_cci.so`, `libqmi_client_helper.so`;
- `libqmi_client_qmux.so`, `libqmi_common_so.so`, `libqmi_encdec.so`;
- `libqmiservices.so`, `librilqmiservices.so`, `qcrild_librilutils.so`;
- `qcril.db` and upgrade scripts 0 through 10.

The newer `libqmiservices.so` lacks the IMS-private service object imported by
the retained RED 64-bit `lib-imsrcs-v2.so`. Stock
`lib-imsrcsbaseimpl.so` exports exactly that object. The extraction pipeline now
reproducibly adds this provider dependency to `lib-imsrcs-v2.so`; checkelf stays
enabled and no undefined-symbol exemption was introduced.

Vendor commit: `0c0351fcfc0a00edece8147403675d3575185e7f` on the existing
`lineage-22.2-kernel-302` branch.

## Verification

- 112 vendor unit tests: PASS.
- 179 device unit tests: PASS.
- Complete device-tree audit: PASS.
- Full `mka bacon -j7`: PASS.
- VINTF compatibility: PASS.
- Kernel remains `4.4.302+` with the exact four RED DTBs.
- Installed QMI hashes, database files, init directives and IMS provider edge
  match their contracts.

Build artifacts:

| Artifact | Size | SHA-256 |
| --- | ---: | --- |
| `lineage-22.2-20260917-UNOFFICIAL-hydrogenone.zip` | 858,334,655 | `6a78e95d96a3d0e1c9b8fd9cdb6fb78b49e89edb04d1c75f0dcb6b977a920224` |
| `boot.img` | 32,403,456 | `c89def7c5a2f8d7296966d9c56dcb38ce279b08928111eca2eccc36d54cecf90` |
| `vendor.img` | 369,557,736 | `137409e2129fe179c65ca847287231af0e36e028014aca47d7f3f416a4425773` |

The candidate has not been installed. Runtime baseband, IMEI, SIM, calls and
data remain physical acceptance gates. No radio success is claimed from the
build alone.
