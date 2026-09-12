# RED Hydrogen One kernel source

The LineageOS 22.2 device build uses the RED-specific source kernel below.

| Field | Value |
|---|---|
| Workspace path | `kernel/red/msm8998` |
| Repository | `https://github.com/derveror/android_kernel_red_msm8998` |
| Branch | `lineage-22.2` |
| Verified commit | `440e8eb4eea36404d340a2a4ad001cf013304447` |
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

Physical boot and hardware operation remain unverified. TFA speaker runtime
also requires packaging and testing `tfa98xx.cnt` and `tfa98xx_a3d.cnt` from
stock-authoritative vendor material.
