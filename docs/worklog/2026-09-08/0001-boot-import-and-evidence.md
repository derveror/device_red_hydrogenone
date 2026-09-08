# Boot import correction and evidence collection — 2026-09-08

## Inputs and decision

The user reports full LineageOS compilation succeeded, but the ROM does not boot.
GitHub branch heads matched the audited archives exactly:

- device parent: 73ca80baf580f05f0670161128991c3d3a95ce2b;
- vendor: 6d80047932b9ecade6ba34c4cff22a9206972cb6.

The user selected cheryl device + vendor as primary reference; mata is secondary.
RED .118 remains hardware and proprietary authority.

## Correction and diagnostics

Restored init.qcom.rc's import of init.target.rc. Its 14 selected vendor binaries
exist; definitions were unreachable because Android init does not recursively
scan vendor/etc/init/hw. The added regression failed with all14 services missing,
then passed after the one-line import correction.

Added tools/collect_boot_diagnostics.py for existing boot.img/header/kernel hash,
installed init/fstab and readonly ADB/fastboot evidence. It archives logs under
<top>/logs/hydrogenone. Commands are bounded by timeouts; there is no flash,
erase, format, slot switch, reboot, adb root or log-clearing action. An independent
review found ambiguous mixed-transport device selection; the correction resolves
one serial across all observed transports/states before issuing phone commands,
with a failing-then-passing regression. No Critical/Important review findings remain.

Corrected the preflight default to lineage_hydrogenone-bp1a-userdebug. An executable
fixture rejected the old default and passed with bp1a, recording build status0.
Updated current donor, build, kernel, boot-failure and resume documentation.

## Verification

- Device unit suite:128 tests passed.
- Device standalone full-tree contract:PASS.
- Vendor unit suite:77 tests passed; existing readelf local-symbol warnings remain.
- Live cross-tree copy destinations match the pinned evidence exactly; zero collisions.
- git diff --check:clean.
- Host-only, boot-header/truncation, fastboot and device-selection regressions pass.

These are local static/tooling checks. No complete LineageOS build or physical boot
was performed in this environment. The vendor payload and pin remain unchanged.

## Remaining runtime boundary

The actual stock .118 kernel lacks BPF_SYSCALL. LineageOS22.2 NetBpfLoad requires
BPF map operations; netbpfload.35rc requests reboot,bpfloader-failed on failure.
That confirms a kernel/userspace gap, but the user's observed failure could be
at an earlier bootloader/mount/SELinux/encryption/APEX stage. Kernel adaptation is
not completed by this import fix. Power HAL, Android IMS app and Widevine also
remain separate integration work.

Next input: run the collector on the user's existing failed build/phone, attach
the exact printed archive and describe the visible boot stage/install method.
Do not infer a working ROM from the test counts above.
