# RED Hydrogen One source-kernel status

## Active tree

The LineageOS 22.2 device configuration builds the RED-specific MSM8998 kernel
from source:

```text
repository: https://github.com/derveror/android_kernel_red_msm8998.git
branch: lineage-22.2
path: kernel/red/msm8998
commit: 39e74780ffb29d0b6ac30e9d68ae5b1195fe529e
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

## Remaining runtime gates

The kernel build result has not yet been boot-tested on a physical H1A1000.
The next gates are a complete LineageOS 22.2 workspace build, boot-image
packaging (including resolution of the recorded TFA `.cnt` packaging gap), and
staged device testing with serial/ADB, `dmesg`, `logcat` and service evidence.
