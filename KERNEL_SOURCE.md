# RED Hydrogen One kernel source

The LineageOS 22.2 device build uses the RED-specific source kernel below.

| Field | Value |
|---|---|
| Workspace path | `kernel/red/msm8998` |
| Repository | `https://github.com/derveror/android_kernel_red_msm8998` |
| Branch | `lineage-22.2` |
| Pinned commit | `a70742ff9578d6aa0201f66a389659386c716f10` |
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

Earlier source-built 4.4.302 commit `f3819ee` booted Lineage Recovery and
LineageOS on a physical H1A1000. The current `a70742ff` commit restores the
ARM64 KASLR/MODVERSIONS kcrctab relocation contract after runtime rejection of
`wlan.ko`; it still requires a clean full LineageOS build and physical test.
The standalone GNU-binutils diagnostic build is not a production artifact.

TFA speaker runtime also requires packaging and testing `tfa98xx.cnt` and
`tfa98xx_a3d.cnt` from stock-authoritative vendor material.
