# RED .118 CNSS daemon / WLFW handshake restoration

**Date:** 2026-09-16

**Device branch:** `118-lineage-22.2-kernel-302`

**Vendor branch:** `lineage-22.2-kernel-302`

**Kernel branch:** `lineage-22.2` (unchanged)

## Runtime failure boundary

The installed `bc1283e4` Linux 4.4.302 build accepts and loads the matching
external `wlan.ko`. The module reports driver version `5.1.1.77V`, but Android's
legacy Wi-Fi HAL initially sees no `wlan0`, times out waiting for driver ready
and reports `WifiNative Failure`.

ICNSS and the modem transport were alive: WLAN QMI registration, MSA info,
MSA-ready request/response, firmware capability discovery and QRTR/TFTP were
all observed. ICNSS did not receive the final MSA-ready indication, did not
send the configuration/mode requests and recorded no `FW_READY` event.

The four current production/PVT DTBs were decompiled and compared with the
corresponding RED `.118` stock DTBs. Their ICNSS node, regulators, IOMMU and
VADC wiring match. The active device is the TM CSP PVT variant. This ruled out
a DT selection or ICNSS-node regression at the observed failure boundary.

## Proven root cause

RED `.118` stock contains `/vendor/bin/cnss-daemon`, an AArch64 WLFW QMI client
that waits for MSA readiness, uploads the WLAN board data and calibration
report and completes firmware memory readiness. The previous Android 15 vendor
selection omitted it.

The exact stock binary was copied temporarily to the running device and started
with its stock arguments (`-n -l`) without disabling SELinux. It connected to
the WLFW service; approximately 2.7 seconds later ICNSS reported `WLAN FW is
ready`, the qcacld probe ran and both `wlan0` and `p2p0` appeared. This is the
direct runtime proof for the missing userspace handshake. `cnss_diag` remains
excluded because it is diagnostic-only and is not required for this path.

Exact restored payload:

- path: `vendor/bin/cnss-daemon`;
- size: 69,880 bytes;
- SHA-256: `ccb5244705d434f749f5836aa7db7cfebcc117ca5714a8f1168fc7608ece46a2`.

## Permanent implementation

- Selected and packaged the exact RED `.118` binary as a checked ELF prebuilt.
- Added the stock-equivalent `vendor.cnss-daemon` service to `init.qcom.rc` in
  class `late_start`, user `system`, groups `system inet net_admin wifi` and
  capability `NET_ADMIN`.
- Reused the existing Qualcomm legacy sepolicy `wcnss_service` domain and
  executable label; no permissive rule or new exception was added.
- Regenerated the vendor source lock, manifest and ELF audit. The tree now has
  664 selected files and 509/509 proprietary ELF modules checked, with zero
  checkelf exceptions.

Vendor commit: `ec16aa36d6a5173655c45636183193260da12c06`.

## Verification

- Device tests: 174 passed; complete-tree contract passed.
- Vendor tests: 99 passed.
- Kernel tests: 11 passed.
- Full `make bacon -j7` completed successfully.
- VINTF compatibility returned `compatible`.
- The built `vendor.img` was unsparsed and inspected: the installed daemon has
  mode 0755 and the exact stock SHA-256 above; its init service is present with
  the expected credentials.
- Final OTA:
  `lineage-22.2-20260916-UNOFFICIAL-hydrogenone.zip`, 851,071,144 bytes,
  SHA-256 `12a8cf73d60a47fe709e1ddd612ac46b3edced27c4e0376561217f3983e98ef3`.
- Boot image: 32,403,456 bytes,
  SHA-256 `01084bfa71d167d6e7ec0d70fa970d4092e48857d6eaded4050ec2fd8ad7ef52`.
- Kernel payload: 15,655,357 bytes, 1,121,859 bytes below 16 MiB,
  SHA-256 `9d066fb204fbce603692fcfb6e3512866da5a163e00dd3814ae2867d9768c150`.
- Android security patch level embedded in boot/OTA: `2026-09`.

The build and live one-shot daemon test prove the root cause and packaging
closure. Full Wi-Fi UI/association remains a physical runtime gate after the
new OTA is installed and booted. Bluetooth is a separate remaining runtime
issue. No flash or reboot was performed during this work.
