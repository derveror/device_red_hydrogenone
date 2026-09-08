# LineageOS builds, but RED does not boot

Status on 2026-09-08: the user reports a successful build from device
`73ca80baf580f05f0670161128991c3d3a95ce2b` and vendor
`6d80047932b9ecade6ba34c4cff22a9206972cb6`, followed by a failed boot.
The exact installed artifacts and failure stage have not yet been observed here.

## Confirmed correction

`init.qcom.rc` now imports `init.target.rc`. All 14 service executables from
that file exist in the pinned vendor payload. The new regression traverses
the hardware init imports: it failed with all 14 services unreachable before
the import was added, then passed afterwards.

This repairs service registration, including qseecomd, DSP, thermal and IMS
daemons. It does not prove that the phone has reached second-stage init, or
that every daemon can start with the final SELinux policy and linker namespace.
The binary payload does not need replacement to repair this missing import.

## Kernel incompatibility requiring physical evidence

The checked-in boot payload is the RED .118 Linux 4.4.153+ kernel. Its extracted
configuration disables `CONFIG_BPF_SYSCALL`, `CONFIG_BPF_JIT` and `CONFIG_CGROUP_PIDS`.
The Essential kernel project currently supplies UAPI headers only.

LineageOS 22.2 [NetBpfLoad.cpp](https://github.com/LineageOS/android_packages_modules_Connectivity/blob/lineage-22.2/bpf/loader/NetBpfLoad.cpp)
creates and writes a BPF array map before finishing. Its
[Android 15 init service](https://github.com/LineageOS/android_packages_modules_Connectivity/blob/lineage-22.2/bpf/loader/netbpfload.35rc)
uses `reboot_on_failure reboot,bpfloader-failed`. Kernel version checks downgraded
to warnings by Lineage do not implement the missing BPF syscall.

Therefore the selected kernel cannot complete that normal BPF-loading path.
Look for `bpfloader-failed`, `netbpfload`, BPF map errors or `Function not implemented`
in reboot reasons, logcat and kernel logs. An earlier bootloader, mount, policy,
APEX or encryption failure may occur before this path is reached.

Do not mark the ROM bootable after the init fix. A maintained kernel needs RED
board/driver adaptation and the required Android kernel backports; editing the
saved config text cannot change the prebuilt binary. A donor boot image or DTB
does not provide that adaptation. Cheryl is the primary comparison; RED .118
remains hardware authority.

## Collect the existing failure first

Connect the phone in its currently accessible state and run on the build host:

```bash
cd /home/surface/los
python3 device/red/hydrogenone/tools/collect_boot_diagnostics.py
```

The command prints the exact archive path under:

```text
/home/surface/los/logs/hydrogenone/boot-diagnostics-<timestamp>.tar.gz
```

It records source revisions and dirty state, the actual built boot header/kernel
hash, installed init/fstab files, and whichever USB evidence is available:

- ADB: properties, cmdline, mounts, dmesg, logcat, last_kmsg, pstore and recovery log.
- Fastboot: named product/slot/firmware/reboot variables. Unsupported variables
  remain visible as command errors; they are not interpreted as a diagnosis.
- No accessible device: host/build evidence is still archived. Unauthorized,
  offline or multiple-device output is retained. With multiple phones use
  `--serial SERIAL`; without a selection no per-phone commands are issued.

No flash, erase, format, slot change, reboot, adb-root, log clearing or on-device
settings change is performed. Commands have timeouts. Some logs require access
that normal ADB lacks; permission errors are preserved instead of enabling root.
The .118 config has pstore and the RED last_kmsg feature, but readable retained
logs still depend on the running environment. Collect promptly if recovery is
already accessible. The tool does not put the phone into recovery itself.

If ADB appears only briefly, run the collector again while it is visible. A
snapshot with no USB access cannot recover an earlier kernel log by itself.
Host-only collection is available with `--host-only`. Use `--boot-image PATH`
when the tested image is not the default build output. No full images are put
in the archive. Checkout revisions are recorded at collection time and may
postdate existing build artifacts; report which ZIP/image was actually installed.

Along with the archive, describe the visible failure: fastboot rejects the
image, RED logo stays, repeated reboot, Lineage animation, or black screen.
Also state how it was installed and whether userdata was previously formatted
for this ROM. This gathers evidence; it is not an instruction to format data.

## Open integration work

Power HAL, Android IMS app integration and Widevine remain incomplete in this
pair. They are separate from the confirmed init import correction and the
missing kernel BPF interface. Firmware .118 and boot header v1 remain the
recorded project baseline; the collector helps compare it with the physical
device without changing either. A successful stock fingerprint check alone
does not attest every installed firmware partition.
