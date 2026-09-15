# RED .118 QRTR name-service restoration

## Runtime evidence

The source-built `wlan.ko` registers with ICNSS, but the physical device shows
zero `SERVER_ARRIVE` and `FW_READY` events. The installed TFTP transport is
running and `wlanmdsp.mbn` is present, yet no firmware request occurs.

Stock `.118` startup provides the missing ordering evidence: it starts
`vendor.qrtr-ns` before `vendor.tftp_server`, then TFTP serves
`wlanmdsp.mbn`, and ICNSS reports its QMI server connection. Starting the same
binary late during a diagnostic session cannot replay the modem's boot-time
request and therefore is not considered a valid runtime fix test.

## Implemented contract

- retain the exact stock `.118` AArch64 `/vendor/bin/qrtr-ns`;
- pin its size `68,632` and SHA-256
  `294d3d810af39d66db49469917e46fc0537e5122cf54c883344135bfd83bf7dd`;
- start `vendor.qrtr-ns` in `class core` as `vendor_qrtr:vendor_qrtr` with
  `NET_BIND_SERVICE`, before the existing TFTP service;
- use the existing MSM8998 `qrtr` SELinux domain and `qrtr_exec` label;
- keep unproven `qrtr-cfg` and `qrtr-lookup` outside the product;
- replay the change automatically after vendor extraction/regeneration.

Vendor commit:
`f99b7f3f6c284ac418eda689a4f89e556fb33069`.

## Verification

- vendor tests: 96 passed;
- device tests: 168 passed; full-tree contract passed;
- all 508 proprietary ELF modules retain `check_elf_files`, with zero
  exceptions;
- full LineageOS 22.2 `bacon` build completed successfully;
- VINTF result: `compatible`;
- final `vendor.img` contains the exact binary as mode `0755` with SELinux
  label `u:object_r:qrtr_exec:s0`;
- `boot.img` is 32,403,456 bytes, leaving 34,705,408 bytes below the stock
  64 MiB partition limit;
- OTA SHA-256:
  `bcb028f8137fbd370354ac2e65fe172c9f017299a6efa343de247b25dc21f51f`.

The OTA has not yet been installed. Wi-Fi recovery remains a physical runtime
gate; build success alone is not reported as Wi-Fi success. Bluetooth remains
a separate bring-up item.
