# RED Hydrogen One kernel source

The LineageOS 22.2 device build uses the RED-specific source kernel below.

| Field | Value |
|---|---|
| Workspace path | `kernel/red/msm8998` |
| Repository | `https://github.com/derveror/android_kernel_red_msm8998` |
| Branch | `lineage-22.2` |
| Pinned commit | `bc1283e4bf00425cf60f43d549f49ff26bf7474e` |
| Kernel version | Linux `4.4.302+` |
| Defconfig | `lineageos_hydrogenone_defconfig` |
| Image target | `Image.gz-dtb` |

`BoardConfig.mk` builds this tree directly. The local-manifest template pins
the verified commit, while `lineage.dependencies` records the branch and
workspace path.

The kernel build and static artifact gates pass for all four production/PVT
variants in exact order: TM, TM CSP, SIM and JDI. FPC1020, LM36923H, TFA9894
and JDI CYTTSP5 support is built in. The proprietary rear SmartPort is excluded;
ordinary USB-C, charging, Bluetooth and UFS remain in scope. Leia/display is
retained.

Source-built 4.4.302 commit `a70742ff` boots Lineage Recovery and LineageOS on
a physical H1A1000, but its module loader subtracts the KASLR delta from an
already-absolute LLD kcrctab CRC and rejects the matching `wlan.ko`. Current
commit `bc1283e4` accepts both raw LLD CRC entries and the standard relocated
ARM64 form. Its source tests, boot-image build, exact four-DTB order, module CRC
identity and boot-size gate pass; physical Wi-Fi validation remains required.
The complete A/B OTA also passes VINTF, ZIP/signature, partition and payload
checks.

TFA speaker runtime also requires packaging and testing `tfa98xx.cnt` and
`tfa98xx_a3d.cnt` from stock-authoritative vendor material.
