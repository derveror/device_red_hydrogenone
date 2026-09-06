# Physical bring-up baseline — RED Hydrogen One H1A1000

The first physical LineageOS 22.2 bring-up is defined against the canonical RED
Android 9 stock build `H1A1000.082ho.01.00.10r.118`.

## Required stock baseline

Before the first LineageOS boot/flash test, boot the phone on the complete RED
`.118` stock firmware and verify all of the following:

- fingerprint: `RED/HydrogenONE/HydrogenONE:9/PKQ1.190118.001/118:userdebug/release-keys`
- incremental: `118`
- Android release: `9`
- SDK: `28`

Use `tools/verify_stock118_device_baseline.py` to validate the observed values.

The Verizon `.109` build `H1A1000.010ho.01.01.01r.109` is Android 8.1 / SDK 27
and is not an accepted physical bring-up baseline for this tree.

## Why this is a hard gate

The checked-in transitional kernel is the exact RED `.118` kernel, the vendor
tree is derived from `.118`, and the verified `.118` stock boot image uses boot
header version 1. Android 8 and earlier use the legacy version-0 boot image
format, while Android 9 introduced versioned boot headers.

A `fastboot boot` rejection on a `.109` device therefore must not be "fixed" by
downgrading the production LineageOS boot image to header v0. The production
image remains aligned to the verified `.118` stock contract.

## Firmware boundary

LineageOS OTA packaging remains limited to `boot`, `system`, and `vendor`; it
does not carry RED bootloader/modem/trust-zone firmware. Establish the complete
`.118` stock firmware baseline separately with the verified RED fastboot
package before testing the LineageOS OTA.

Do not mix donor firmware, do not flash individual firmware partitions from
another device, and do not treat a `.109` userspace boot as proof that the
required `.118` firmware baseline is present.
