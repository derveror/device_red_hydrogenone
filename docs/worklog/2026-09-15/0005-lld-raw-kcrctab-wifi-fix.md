# LLD raw kcrctab Wi-Fi module fix

## Physical failure

The clean `a70742ff` LineageOS build boots Android on the physical H1A1000,
but Wi-Fi remains unavailable. The installed `/vendor/lib/modules/wlan.ko` is
byte-identical to the build output and the modem/QRTR/TFTP/ICNSS control plane
is online. Kernel dynamic debug records the decisive mismatch:

```text
Found checksum FFFFFFE183B71DF1 vs module 13D71DF1
wlan: disagrees about version of symbol module_layout
```

The KASLR slide is `0x1e90200000`. Subtracting it from the correct raw CRC
`0x13d71df1` produces the rejected value `0xffffffe183b71df1` exactly.

Captured evidence is stored under:

```text
/home/surface/los/logs/hydrogenone/wifi-a707-live-20260915/
```

## Linker and reference analysis

The production kernel is linked by Clang 19 LLD with
`--no-apply-dynamic-relocs`. Its `__kcrctab_module_layout` entry contains raw
little-endian value `0x13d71df1`; `.rela.dyn` has no relocation for that entry.
The packaged module also requires `module_layout=0x13d71df1`.

Stock RED Android 9 `.118` uses external `qca_cld3_wlan.ko`, so retaining a
loadable WLAN module matches the stock architecture. Every supplied maintained
MSM8998 reference checked for this bring-up instead uses
`CONFIG_QCA_CLD_WLAN=y`, avoiding this module-loader path. Building qcacld in
was already tested here, but crosses the H1A1000's observed 16 MiB kernel
payload window. The production fix therefore keeps `CONFIG_QCA_CLD_WLAN=m`.

## Kernel correction

Kernel commit `bc1283e4bf00425cf60f43d549f49ff26bf7474e` changes the version
check to accept either:

1. the exact raw CRC emitted by LLD; or
2. the standard ARM64 KASLR-adjusted CRC used when the linker emits a relocated
   kcrctab entry.

This preserves strict symbol-version matching and supports both observed link
representations. DTS, defconfig, DTB selection, Wi-Fi firmware, device
configuration and vendor payload are unchanged.

## Verification

- kernel contracts: 11/11 PASS;
- device contracts: 172/172 PASS plus full-tree PASS;
- vendor contracts: 99/99 PASS;
- VINTF: compatible;
- OTA ZIP/signature structure and compressed-data integrity: PASS;
- boot header v1, page size 4096, Android 15 / 2026-09: PASS;
- kernel payload: 15,655,357 bytes, below 16 MiB by 1,121,859 bytes;
- boot image: 32,403,456 of 67,108,864 bytes;
- exact appended DTB order TM, TM CSP, SIM, JDI: PASS;
- `wlan.ko` and vmlinux `module_layout`: both `0x13d71df1`;
- LLD relocation count for `__kcrctab_module_layout`: zero.

Generated production candidate:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `lineage-22.2-20260916-UNOFFICIAL-hydrogenone.zip` | 851,029,208 | `d3a582d50980d8d9e9eb1350f8f9ffb535a8d2f4b821209c3962e768de9581dc` |
| `boot.img` | 32,403,456 | `1234df9d5112e481a354177467bb513e41c16c7bddf3094677d6acee1a96d854` |
| kernel payload | 15,655,357 | `9d066fb204fbce603692fcfb6e3512866da5a163e00dd3814ae2867d9768c150` |
| packaged `wlan.ko` | 5,660,568 | `a8126f3fb6c58516a3263a63454f67068035c643682a8f26a630d933a8516c72` |

Compilation and artifact checks do not claim physical Wi-Fi success. The next
gate is a user-authorized recovery install followed by one captured Wi-Fi
enable attempt. No reboot, flash or sideload was performed during this fix.
