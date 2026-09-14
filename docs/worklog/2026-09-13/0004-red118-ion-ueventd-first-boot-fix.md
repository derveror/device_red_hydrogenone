# RED .118 ION ueventd first-boot fix

## Symptom

The OTA containing the physically verified RED `.118` QTI Keymaster stack
installed successfully, but normal boot remained at the RED logo. Durable
diagnostic traces v10 and v11 showed no kernel panic. `qseecomd` stayed ready,
the `cmlog` securefs partition mounted, `/data` mounted, and the Keymaster
service aborted repeatedly with `QSEECom_start_app failed`.

## Root cause proof

Diagnostic v11 instrumented only the QSEE application lookup boundary. Every
Keymaster attempt found the bootloader-preloaded 64-bit TrustZone application:

```
H1QSEE: query-result ... app=keymaster64 ret=0 app_id=65537
```

No ION or QSEE command ioctl followed. The userspace library immediately tried
the 32-bit `keymaster` fallback and then aborted. Recovery inspection showed
that, without the temporary permissions used by the earlier chroot harness,
`/dev/ion` was `0600 root:root`. The curated device `ueventd.rc` contained the
QSEECom rule but had accidentally omitted ION.

The original RED `.118` vendor image was converted read-only from sparse form
and its root `ueventd.rc` was read with `debugfs`. It specifies exactly:

```
/dev/ion                  0664   system     system
```

The same mode and ownership are present in the LineageOS 22.2 MSM8998 device
trees for Essential mata, Razer cheryl and OnePlus msm8998-common. This also
explains why the controlled Recovery chroot succeeded: the harness had first
applied the missing production mode manually.

## Permanent tree change

- Restore the exact RED `.118` `/dev/ion 0664 system system` ueventd rule.
- Add a regression contract that rejects removal or mutation of that rule.
- Do not change the QTI Keymaster blobs, service credentials, SELinux domain or
  Linux 4.4.302 ION/QSEE drivers; all of those paths already passed the
  controlled runtime test.

## Evidence

- v11 durable log:
  `logs/hydrogenone/diagnostic_boot_20260913/v11/normal_boot_kmsg_v11.log`,
  SHA-256
  `2352783eb9587e2eb1f06a09ce19d20a682f5028d5fc6ae2e48dd29aa1b06fec`.
- v11 captured region SHA-256:
  `8d720d7dc3a7404246c87f53cfe0bb0ff5b3c8f1a971739bb4e41ebc03acd9d7`.
- The diagnostic kernel changes remained in a detached temporary tree and are
  not production source.
- The full production `boot_b` backup was restored after the trace; slot `b`
  is active, bootable, and its retry count was reset to seven.

## Verification

- Regression suite: 141 tests PASS.
- Full-tree contract: PASS.
- Full `mka -j4 bacon`: PASS, including kernel 4.4.302, all four production
  DTBs, SELinux/neverallow, filesystem generation and VINTF compatibility.
- The staged vendor tree, target-files vendor tree and final sparse
  `vendor.img` each contain the exact RED `.118` ION rule.
- ZIP integrity: PASS.
- Production kernel contains no `H1BOOTLOG`, `H1QSEE` or other temporary
  diagnostic marker.
- OTA:
  `lineage-22.2-20260914-UNOFFICIAL-hydrogenone.zip`, SHA-256
  `483a69f65e0b6166460b9df9e33c04835e88a899227e88c8c3c86ef4e6212186`.
- Boot image: 32,403,456 bytes, SHA-256
  `414347e0fa484f7de18a35b1f5238b5abfbcca5a63b801c87715f0d381d42936`;
  it fits the 64 MiB boot partition.
- Vendor image SHA-256:
  `7bffe7595f17dc055de42a6d349ee02b326414175e161b344ffa9cee4b2b2e5c`.

The remaining gate is a physical install and normal-boot test. These build
results are not, by themselves, a claim that Android has completed boot.
