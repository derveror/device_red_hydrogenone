# ARM64 kcrctab fix — clean LineageOS build evidence

## Purpose

This record verifies the first complete LineageOS 22.2 artifact built with the
ARM64 KASLR/MODVERSIONS kcrctab relocation fix in kernel commit
`a70742ff9578d6aa0201f66a389659386c716f10`. The previous physical build used
kernel `f3819ee` and rejected `wlan.ko` at `module_layout`; this build replaces
that superseded artifact.

Compilation success is not a Wi-Fi runtime claim. The OTA recorded here has
not been installed on the physical phone.

## Locked source state

- device: branch `118-lineage-22.2-kernel-302`, commit
  `f557b1112910d7c08b1fa585dd3f4239ebe3b036` before this evidence commit;
- kernel: branch `lineage-22.2`, commit
  `a70742ff9578d6aa0201f66a389659386c716f10`;
- vendor: branch `lineage-22.2-kernel-302`, commit
  `f5192d041cb9bc914b5e438c1fc54c1aae7f8891`;
- stock firmware authority: `H1A1000.082ho.01.00.10r.118`.

The workspace completed a full `repo sync -c -j8 --fail-fast
--no-clone-bundle` before the build. The output tree was cleaned with
`m clean`. An initial invocation was stopped without cleaning its output so
that the continuation could explicitly use every logical processor:

```text
mka bacon -j$(nproc --all)
```

`nproc --all` returned `8`; Ninja ran `bacon -j 8`. The resumed invocation
completed successfully in `03:49:45` and produced
`lineage-22.2-20260915-UNOFFICIAL-hydrogenone.zip`.

Build log:

- path: `/home/surface/los/logs/mka_bacon_20260915_a707_clean.log`;
- bytes: `28,961,581`;
- SHA-256:
  `8c3e77e66ef9d4034fca21b5175d1d0e9680909f38aef5553a9e15ec521c26ba`.

## Kernel, module and DTB verification

- kernel release: `4.4.302+`;
- linker recorded in `.vmlinux.cmd`:
  `prebuilts/clang/host/linux-x86/clang-r536225/bin/ld.lld`;
- `.config` contains `CONFIG_MODULES=y`, `CONFIG_MODVERSIONS=y`,
  `CONFIG_RANDOMIZE_BASE=y` and `CONFIG_QCA_CLD_WLAN=m`;
- the kernel extracted from the generated `boot.img` is byte-identical to the
  current kernel output `arch/arm64/boot/Image.gz-dtb`;
- the packaged `vendor/lib/modules/wlan.ko` is byte-identical to an
  `llvm-strip --strip-debug` copy of the current KERNEL_OBJ module;
- source and packaged WLAN modules have identical 435-entry modversion lists,
  the same `4.4.302+ SMP preempt mod_unload modversions aarch64` vermagic, and
  `module_layout=0x13d71df1`, matching the current `Module.symvers`;
- `Image.gz-dtb` is byte-for-byte `Image.gz` followed by exactly TM, TM CSP,
  SIM and JDI, in that order, with no generic or fifth DTB;
- all four DTBs pass the sorted DTB to DTS to DTB to DTS round trip;
- all four retain `qcom,msm-id=<0x124 0x20001>`,
  `qcom,board-id=<0x8 0x0 0x1 0x0>`, `fih,hw-id=<0x4 0x4 0x0>` and display
  IDs TM `0x02`, TM CSP `0x0e`, SIM `0x7f`, JDI `0x64`;
- exact SmartPort markers remain absent.

The round trip emits 360 already-classified legacy DTC warning lines. It
introduces no new warning class or RED hardware-value mismatch.

## Boot, OTA and partition gates

- boot header version: `1`;
- page size: `4096`;
- OS version / patch in boot header: Android `15.0.0`, `2026-09`;
- recovery-as-boot is enabled; a separate `recovery.img` is therefore not
  expected;
- `boot.img` uses `32,403,456` of `67,108,864` bytes and leaves
  `34,705,408` bytes;
- sparse `system.img` expands to exactly the declared 4 GiB partition;
- sparse `vendor.img` expands to exactly the declared 1 GiB partition;
- VINTF target-files check: `COMPATIBLE`;
- OTA type: A/B; pre-device list: `hydrogenone,HydrogenONE,H1A1000`;
- OTA security patch: `2026-09-01`;
- SignApk signature structure is present and `unzip -t` reports no errors.

Post-build contracts also pass:

- device: 172 unit tests plus the standalone full-tree gate;
- vendor: 99 tests;
- kernel: 10 tests;
- `git diff --check` in all three RED trees.

The existing source-tree compatibility edit in
`hardware/ril/reference-ril/Android.bp` remains an intentional uncommitted
workspace patch and is not part of any RED repository commit.

## Generated artifacts

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| LineageOS A/B OTA ZIP | 851,026,784 | `3b54b9dfa3b16291a9b84cea390155f94b3b4b8b50ed3df1b40386addc49b4f1` |
| `boot.img` | 32,403,456 | `c67f079d1ece6a39a6d436d100a50d943e51a053f648892c3f1da265598a6132` |
| sparse `system.img` | 1,856,074,380 | `ff679863423e8f1a02969587380783149af525fc9b8206c60cb534db5cd4029e` |
| sparse `vendor.img` | 333,467,880 | `ed83894f4ddb10b51c65791d1e9f8609d6ca1d3ac4524603a32df6879f300f0b` |
| `.config` | 140,952 | `ec1b3502a9c4da9bbb46c1b55f2eb605fdda27152379bcf2abbd08d38e20fe4d` |
| `vmlinux` | 271,304,872 | `1a3c69008048b526de40003547413981d0553ac0addeb87c227a2fc2a146faa3` |
| `System.map` | 6,460,427 | `b4c724fac5a86caa76758cd0d60f4ce7b22e374cbdbbdfcb3f1f931ab554381c` |
| `Module.symvers` | 584,782 | `02893707963d6856cba191da909fa77a7c611d4bc139b83ffbbeaf564a4bd547` |
| `Image.gz` | 14,079,972 | `b33ffee53f08b3b233ba3b42d1a6bca6d5d4df55055081dbad5cb43b9769b11c` |
| `Image.gz-dtb` | 15,655,118 | `3f0c7db6402332deba25568bc0c75c1db05b396d685cdecea4586453f7e8edcf` |
| unstripped `wlan.ko` | 95,147,952 | `feff2626f56e1be6e9db412993f08fc7288c18f070c40b758e6d47549050edda` |
| packaged `wlan.ko` | 5,660,568 | `a8126f3fb6c58516a3263a63454f67068035c643682a8f26a630d933a8516c72` |

Artifact paths:

```text
/home/surface/los/out/target/product/hydrogenone/lineage-22.2-20260915-UNOFFICIAL-hydrogenone.zip
/home/surface/los/out/target/product/hydrogenone/boot.img
/home/surface/los/out/target/product/hydrogenone/system.img
/home/surface/los/out/target/product/hydrogenone/vendor.img
```

## Remaining physical gate

Only a controlled install and physical boot can establish whether the ARM64
kcrctab correction allows `wlan.ko` to load and whether the restored RED .118
modem/QRTR/TFTP path reaches ICNSS `FW_READY`. Wi-Fi and Bluetooth remain
unverified in this artifact. No flash or reboot operation was performed while
creating this record.
