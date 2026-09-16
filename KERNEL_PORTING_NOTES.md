# RED Hydrogen One source-kernel status

## Active tree

The LineageOS 22.2 device configuration builds the RED-specific MSM8998 kernel
from source:

```text
repository: https://github.com/derveror/android_kernel_red_msm8998.git
branch: lineage-22.2
path: kernel/red/msm8998
commit: bc1283e4bf00425cf60f43d549f49ff26bf7474e
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
- current boot partition budget: 32,403,456 bytes used of 67,108,864 bytes;
- current kernel payload: 15,655,357 bytes, below the 16 MiB loader window.

Detailed evidence is stored in the kernel repository at
`docs/hydrogenone/runtime-driver-build-evidence.md`.

## Runtime status and remaining gates

Commit `a70742ff` boots Lineage Recovery and LineageOS on a physical H1A1000,
but live dynamic-debug evidence records kernel CRC
`0xffffffe183b71df1` versus module CRC `0x13d71df1`. The LLD-linked vmlinux
contains raw kcrctab value `0x13d71df1` and no dynamic relocation for that
entry; unconditional subtraction of the KASLR slide therefore corrupts it.

Current commit `bc1283e4` retains the upstream ARM64 relocation path for GNU
linker output and first accepts an exact raw CRC for LLD output. A normal
Clang 19/LLVM/LLD boot-image build passes exact kernel/module/DTB/size checks.
The complete A/B OTA passes VINTF, ZIP/signature, partition and payload checks.
The remaining gate is staged physical Wi-Fi testing with ADB, `dmesg`,
`logcat` and service evidence.
