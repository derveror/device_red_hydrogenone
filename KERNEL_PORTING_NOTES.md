# RED Hydrogen One source-kernel status

## Active tree

The LineageOS 22.2 device configuration builds the RED-specific MSM8998 kernel
from source:

```text
repository: https://github.com/derveror/android_kernel_red_msm8998.git
branch: lineage-22.2
path: kernel/red/msm8998
commit: a70742ff9578d6aa0201f66a389659386c716f10
version: Linux 4.4.302+
defconfig: lineageos_hydrogenone_defconfig
output: arch/arm64/boot/Image.gz-dtb
```

`BoardConfig.mk`, the local manifest, workspace preflight and cross-tree lock
all point to this tree. No donor kernel image or donor DTB is selected.

## RED device scope

The DTS implementation layers four production/PVT variants over the maintained
QCOM MSM8998 base:

- TM
- TM CSP
- SIM
- JDI

It preserves the stock board/display IDs and relative appended-DTB order. RED
Leia/display remains in scope. SmartPort is deliberately excluded because it is
the proprietary rear accessory interface and is not required for the standard
USB, charging or Bluetooth paths.

## Completed static/build validation

- full kernel source compilation;
- exact four-entry DTB selection in the Hydrogen One defconfig;
- DTB compilation and reverse decompilation;
- appended `Image.gz-dtb` order validation;
- selected external-module build (10 modules);
- boot partition budget: 26,354,984 bytes used of 67,108,864 bytes.

Detailed evidence is stored in the kernel repository at
`docs/hydrogenone/runtime-driver-build-evidence.md`.

## Runtime status and remaining gates

Earlier 4.4.302 commit `f3819ee` booted Lineage Recovery and LineageOS on a
physical H1A1000. Runtime Wi-Fi diagnostics then proved that its removal of the
ARM64 KASLR/MODVERSIONS kcrctab relocation contract makes the kernel reject the
matching `wlan.ko` at `module_layout`.

Current commit `a70742ff` restores that upstream ARM64 contract. Its standalone
diagnostic build used GNU binutils and is not a production candidate. The next
gate is a clean complete LineageOS 22.2 build through the normal Clang
19/LLVM/LLD path, followed by exact kernel/module/DTB/boot-image verification
and staged physical testing with ADB, `dmesg`, `logcat` and service evidence.
