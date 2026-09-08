# RED kernel status and adaptation requirements

## Actual selected kernel

`prebuilt/Image.gz-dtb` is the canonical RED .118 Linux 4.4.153+ payload:

- size: 37015950 bytes;
- SHA-256: `584ed86bab46bf57c2cd6b6b48ac4026c5d24a70d57bcdd04472d39c5591064d`;
- stock boot header v1, 4096-byte pages, kernel address 0x8000;
- RED board DTBs remain attached.

Older .109 / 4.4.78 notes describe history, not the active payload.
`TARGET_FORCE_PREBUILT_KERNEL` means the Essential source project is used for
UAPI headers only. Neither changing its defconfig nor editing the saved
`prebuilt/stock_kernel.config` changes the booted prebuilt image.

## Confirmed Android 15 compatibility gap

The extracted .118 config has BPF_SYSCALL, BPF_JIT and CGROUP_PIDS disabled.
The LineageOS 22.2 network BPF loader requires BPF map operations, and its init
service requests reboot on failure. See `docs/BOOT_DIAGNOSTICS.md` for exact
source references and collection of the user's actual failure.

Do not assume userspace can first be fully brought up on this stock kernel.
The compatibility gap may prevent reaching that milestone. Disabling the OTA
VINTF kernel check or suppressing the reboot action would not supply missing
kernel interfaces or a working Android network stack.

## Adaptation direction

1. Identify the physical boot failure from the tested image and phone logs.
2. Use cheryl as the primary maintained MSM8998 integration/kernel comparison;
   use mata and other devices as secondary cross-checks.
3. Establish a RED-capable source kernel with the RED board DTS, panel/touch,
   fingerprint, storage, charging, audio and required drivers preserved.
4. Port the Android-required kernel functionality and backports, including
   BPF/cgroups; validate APIs against the actual LineageOS 22.2 userspace.
5. Rebuild kernel modules against the chosen kernel and check hardware in stages.

A donor kernel/DTB is not a ready RED image. Source availability and the RED
board/driver delta still need investigation; no working source-built RED kernel
is delivered by this userspace/init correction. RED/Leia/SmartPort support needs
separate hardware validation after basic boot.
