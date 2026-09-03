# RED Hydrogen One LineageOS 22.2 Bring-up Design

**Status:** Approved design baseline, updated 2026-09-02

**Target:** RED Hydrogen One H1A1000 (`hydrogenone`), Qualcomm MSM8998, LineageOS 22.2, Android 15 / API 35

**Existing baseline:** `derveror/device_red_hydrogenone` at commit `a9e9d30959f1844e3e5ef05cb1c51a05ac29b14e`

## 1. Goal

Create reproducible, reviewable, and bootable LineageOS 22.2 device and vendor trees for the RED Hydrogen One. The Android 9 stock firmware is the hardware authority, but no Android 9 build artifact, policy, manifest declaration, property, or filesystem layout is copied into Android 15 without compatibility analysis and an explicit reason.

The first milestone is a clean build and diagnosable first boot. The final milestone is a source-built kernel, enforcing SELinux, a complete vendor contract, stable A/B update behavior, and working mandatory hardware.

## 2. Non-negotiable constraints

1. Do not create `device/red/msm8998-common`.
2. Do not create a separate RED MSM8998 common vendor repository.
3. The final repository topology is:

   ```text
   device/red/hydrogenone
   vendor/red/hydrogenone
   kernel/red/msm8998   # final name may change only if the recovered source lineage requires a more accurate RED-specific name
   ```

4. Open device configuration adopted from donor common trees is flattened into `device/red/hydrogenone` and rewritten to use `DEVICE_PATH := device/red/hydrogenone`.
5. Proprietary payload and generated proprietary module declarations are stored in `vendor/red/hydrogenone`.
6. OnePlus, Nubia, Essential, and Razer files are references, not authoritative RED files.
7. The existing Hydrogen One tree is historical input. It may be rewritten from zero when stock evidence contradicts it or when its structure is inherited from another device without RED-specific proof.
8. No global compatibility bypass is accepted as a final solution. Any temporary bring-up exception must be narrow, documented, and removed or justified before the stable milestone.
9. Compiled Android 8/9 SELinux policy is never imported into the Android 15 source policy.
10. Unique device data from `persist`, modem NV, DRM key storage, calibration partitions, IMEI-related storage, Wi-Fi/Bluetooth identities, or user data is never committed.

## 3. Version-control safety

The original work remains preserved at commit `a9e9d30959f1844e3e5ef05cb1c51a05ac29b14e`.

Two branches define the safety boundary:

- `legacy-pre-stock118-rework`: immutable archival branch for the current tree.
- `lineage-22.2-stock118-rework`: all stock `.118` analysis, design, and reimplementation work.

The development branch must not be force-pushed. Each subsystem is committed independently so a regression can be bisected and reverted without discarding unrelated work.

## 4. Input sources and authority order

The supplied archives, embedded source commits, archive hashes, and sizes are recorded in `docs/reference/SUPPLIED_SOURCES.md` and `docs/reference/source-lock.json`.

Evidence is ranked in this order:

1. Verified RED `.118` stock images and their extracted metadata.
2. Runtime capture from a device booted on the matching `.118` firmware.
3. RED kernel binary, DTB/DTBO, ramdisk, partition table, firmware, and device nodes.
4. Current official LineageOS 22.2 source patterns and build-system contracts.
5. Donor device, common, vendor, and kernel trees at the exact supplied commits.
6. Existing Hydrogen One tree and older `.109` analysis.

A lower-ranked source cannot override contradictory higher-ranked RED evidence without a written decision record.

## 5. Stock acquisition and verification contract

The intended stock archive is:

```text
[FileSell]_H1A1000.082ho.01.00.10r.118_USERDEBUG_FASTBOOT.rar
```

Google Drive reports a size of `1,851,974,911` bytes. The current connector rejects a single download larger than `268,435,456` bytes, so the archive must be supplied in reconstructable parts below that limit. Reconstruction is accepted only when:

1. all part hashes match the supplied manifest;
2. concatenation produces one RAR file;
3. the reconstructed file SHA-256 is recorded;
4. the RAR test operation succeeds without errors;
5. extraction succeeds without skipped or renamed files.

The label “Android 9 stock” remains an input claim until confirmed from the extracted build properties. Verification records at least:

- `ro.build.version.release`;
- SDK level;
- build ID and incremental;
- build fingerprint and description;
- product device, name, model, brand, and manufacturer;
- build type and tags;
- platform and vendor security patch levels;
- kernel version and command line;
- Treble/VNDK properties;
- A/B and slot properties.

## 6. Reproducible stock inventory

Every object extracted from every stock filesystem receives one inventory row. The inventory schema contains:

- source archive and source image;
- partition;
- absolute path;
- object type;
- symlink target;
- size;
- SHA-256;
- mode, UID, GID, capabilities, and SELinux context when recoverable;
- file format and CPU architecture;
- ELF SONAME and build ID when applicable;
- classification;
- destination decision;
- evidence and rationale.

Required classifications are:

- built from AOSP/LineageOS source;
- required proprietary blob;
- firmware;
- device configuration;
- application/framework package;
- init/VINTF/SELinux contract input;
- obsolete or unused stock artifact;
- debug/test artifact;
- unique per-device data excluded from source control;
- unresolved, requiring a concrete follow-up probe.

The inventory is complete only when the object count independently calculated from mounted/extracted filesystems equals the number of indexed objects plus explicitly recorded exclusions.

## 7. Partition, boot, and update contract

The following values are measured from `.118`; values inherited only from `.109` are not final:

- GPT partition names, numbers, sizes, GUIDs, and slot suffixes;
- sparse versus raw image encoding;
- filesystem types and mount flags;
- boot image header version, page size, base, offsets, cmdline, ramdisk compression, and appended DTB layout;
- recovery-as-boot behavior;
- presence and role of `vbmeta`, `dtbo`, recovery, cache, metadata, vendor, and modem-related partitions;
- AVB descriptors, rollback indexes, and signing chain;
- A/B payload partition list and post-install requirements;
- encryption footer or metadata partition behavior.

`BoardConfig.mk`, fstab, recovery configuration, and OTA configuration are generated from this measured contract. Partition sizes are never copied from a donor.

## 8. Android 9 to Android 15 adaptation rules

### 8.1 Shipping level versus stock update level

The device shipping API level represents the Android version with which the device originally launched, not the version of the `.118` update. The current value `27` is retained only after launch history and stock properties are reconciled. Android 15 target API 35 does not change the historical shipping API.

### 8.2 Product partitions and install locations

Every stock `system`, `vendor`, `odm`, `product`, and `system_ext` object is reclassified for the Android 15 partition model. A stock path is not automatically its final destination. Privileged permissions, overlays, framework jars, native libraries, and init fragments must be installed where Android 15 namespace and partition rules expect them.

### 8.3 Properties

Legacy properties are checked against Android 15 property namespaces and contexts. Device-owned vendor properties use vendor namespaces. Read-only build identity properties are set through current product variables rather than copied as arbitrary runtime properties. Unknown or obsolete Qualcomm properties are omitted until a consumer is identified.

### 8.4 Init

Stock init files are parsed into a service and trigger graph. Each adopted service must have:

- an existing executable module or proprietary file;
- valid Android 15 init syntax;
- correct partition placement;
- user, group, capabilities, sockets, and seclabel derived from actual need;
- matching SELinux domain and transitions;
- a documented property or class trigger;
- a verified device-node or firmware dependency.

Services that cannot run on Android 15 are replaced with current source implementations where available, otherwise isolated for a documented shim or compatibility decision.

### 8.5 VINTF and HALs

Stock manifests are evidence of the Android 9 contract, not files to copy unchanged. The Android 15 device manifest contains only HAL versions and instances that are provided by the final source or vendor tree and observed in either stock runtime or the implemented service graph.

Each HAL entry maps to:

- service binary or source-built service;
- init rc entry;
- interface library;
- instance name;
- service/hwservice contexts;
- required framework compatibility matrix entry;
- runtime verification command.

Fake declarations, empty compatibility fragments used only to pass assembly, and declarations for missing binaries are prohibited.

### 8.6 ELF, VNDK, and linker namespaces

Every proprietary ELF is scanned for architecture, interpreter, SONAME, `DT_NEEDED`, symbol versions, RPATH/RUNPATH, undefined imports, and partition namespace. Android 9 blobs must not rely on implicit Android 9 linker behavior.

Compatibility actions are selected in this order:

1. use a maintained Android 15 source implementation;
2. use the RED `.118` blob unchanged when all dependencies resolve;
3. apply a local blob fixup with an exact reason;
4. add a small source-built shim exporting only the missing symbols;
5. replace a broken RED component with a known-compatible donor implementation only when the complete dependency and hardware contract matches.

`DISABLE_CHECKELF`, global broken-build flags, and broad namespace relaxations are not default fixes. Any remaining exception identifies the exact module and unresolved technical reason.

### 8.7 Applications and Java framework components

APK/JAR analysis records package name, certificate digest, UID, privileged permissions, uses-libraries, target/min SDK, native libraries, overlays, and framework dependencies. Android 9 privileged applications are excluded unless required for hardware and proven compatible. Missing uses-library declarations and obsolete private APIs are repaired explicitly rather than bypassed globally.

### 8.8 SELinux

Android 15 source policy is written from runtime behavior and source-service requirements. Policy development uses denials as evidence, but no blanket `allow` rule, global permissive domain, imported compiled policy, or neverallow bypass is accepted in the final tree.

The final build boots with SELinux enforcing. Diagnostic permissive operation, when required, exists only in a non-release bring-up configuration and is removed before the stable milestone.

## 9. Donor analysis and flattening model

The supplied donor sets are analyzed as complete families:

- Essential mata device and vendor;
- OnePlus Dumpling device, OnePlus MSM8998 common device, Dumpling vendor, and OnePlus MSM8998 common vendor;
- Nubia NX563J device, Nubia MSM8998 common device, and Nubia MSM8998 common vendor;
- Razer Cheryl device and vendor.

Their include graphs, `lineage.dependencies`, product inheritance, generated vendor makefiles, proprietary lists, VINTF, init, SELinux, kernel dependencies, and blob fixups are analyzed together.

Initial measurements already show:

- the two supplied Hydrogen One archives contain the same 423 relative files and all 423 files are byte-identical;
- the current Hydrogen One and mata device trees share 299 relative paths, of which 253 are byte-identical;
- OnePlus and Nubia MSM8998 common device trees share only 59 paths, with only 8 byte-identical files.

Therefore, “common” means common within a manufacturer family, not universally correct for MSM8998.

For each donor file, one of four decisions is recorded:

1. reject because it is manufacturer or hardware specific;
2. use only as a structural example;
3. adapt semantics into a new RED-specific file;
4. adopt unchanged because stock and runtime prove exact compatibility.

When a common-tree item is adopted, its path is flattened:

```text
device/oneplus/msm8998-common/<path>  -> device/red/hydrogenone/<appropriate path>
device/nubia/msm8998-common/<path>    -> device/red/hydrogenone/<appropriate path>
vendor/<donor>/msm8998-common/<blob>  -> vendor/red/hydrogenone/proprietary/<appropriate path>
```

References, module names, copy destinations, namespaces, and include paths are rewritten for Hydrogen One. Directory copying without subsystem review is prohibited.

## 10. Device-tree boundary

`device/red/hydrogenone` owns the build-time hardware description and open configuration:

```text
Android.bp
AndroidProducts.mk
BoardConfig.mk
device.mk
lineage_hydrogenone.mk
lineage.dependencies
config.fs
product.prop
system_ext.prop
vendor.prop
board-info.txt
rootdir/
recovery/
vintf/
sepolicy/
overlay/
overlay-lineage/
rro_overlays/
audio/
media/
gps/
wifi/
bluetooth/
thermal/
power/
keylayout/
seccomp/
extract-files.py
setup-makefiles.py
proprietary-files.txt
```

Only directories supported by RED hardware and the final build contract are created. The list describes ownership, not a requirement to create empty folders.

The extraction scripts and proprietary list remain in the device repository because they define how verified stock material generates the vendor repository. The generated blobs and generated vendor makefiles live in `vendor/red/hydrogenone`.

## 11. Vendor-tree boundary

`vendor/red/hydrogenone` contains only proprietary or generated vendor content:

```text
Android.bp
Android.mk
BoardConfigVendor.mk
hydrogenone-vendor.mk
proprietary/
```

Generated module definitions must preserve:

- source partition and destination partition;
- 32/64-bit architecture;
- symlinks;
- module suffixes used to avoid duplicate module names;
- init/VINTF fragments when those fragments are inseparable parts of a proprietary service;
- ELF checks and narrowly scoped blob fixups;
- firmware install locations and permissions.

The vendor tree is reproducible from the verified stock source. Re-running extraction from a clean vendor directory must produce the same expected file count and the same generated text files, apart from explicitly documented tool-version formatting changes.

No proprietary donor blob is used merely because it came from another MSM8998 device. Donor replacement requires matching hardware interface, kernel interface, firmware expectations, dependency graph, and runtime behavior.

## 12. Kernel strategy

The project uses two explicitly separated phases.

### 12.1 Diagnostic prebuilt phase

A verified RED stock kernel may be used temporarily to isolate Android userspace, ramdisk, partition, init, and vendor failures. The device tree must label this as diagnostic bring-up, and the stock kernel must come from the verified `.118` image rather than the older `.109` payload once `.118` is available.

### 12.2 Source-built final phase

The final tree builds a RED-compatible kernel from source. Work includes:

- identifying the closest released RED/Qualcomm source lineage;
- recovering the effective stock config;
- matching kernel version and required Android compatibility patches;
- restoring RED DTB/DTBO nodes and panel/touch/fingerprint/audio/haptics/SmartPort hardware descriptions;
- validating UFS, USB, WLAN, Bluetooth, modem, sensors, cameras, suspend, charging, thermal control, and ramoops;
- comparing generated image layout and command line with the verified stock boot contract.

The source-built kernel is first tested against stock userspace where practical, then against LineageOS. A successful build alone does not establish kernel compatibility.

## 13. Subsystem dependency model

For every subsystem, the project records a closed dependency chain:

```text
product package or proprietary module
-> installed file
-> init service or framework loader
-> VINTF instance where applicable
-> SELinux domain and contexts
-> shared libraries
-> properties
-> device nodes
-> firmware/calibration
-> kernel driver and DT node
-> runtime verification
```

Subsystems are reviewed independently:

- boot and storage;
- display/composer/gralloc/Vulkan;
- touch and input;
- audio and sound trigger;
- camera;
- media codec and codec2/OMX compatibility;
- Wi-Fi;
- Bluetooth;
- GNSS/location;
- radio, IMS, and data services;
- sensors;
- fingerprint;
- NFC;
- DRM/keymaster/gatekeeper;
- health/charging/battery;
- thermal and power;
- USB;
- RED/Leia 4-View and other RED-specific hardware.

## 14. Build gates

The tree is validated from a clean LineageOS 22.2 checkout. The build sequence is:

```bash
source build/envsetup.sh
lunch lineage_hydrogenone-bp1a-userdebug
m nothing
m bootimage
m vendorimage
m systemimage
m target-files-package
m otapackage
```

The exact lunch release token is taken from the active LineageOS 22.2 product configuration; if the branch uses another release token, `AndroidProducts.mk` is updated to the branch-supported value rather than retaining a stale token.

Each gate includes the following checks where applicable:

- Soong namespace resolution;
- duplicate modules;
- make inheritance and product package existence;
- generated vendor consistency;
- ELF dependency resolution;
- VINTF assembly and `checkvintf`;
- filesystem contexts and `checkfc`;
- SELinux compilation and neverallow checks;
- partition image sizes;
- AVB and boot image metadata;
- target-files and OTA payload contents;
- clean rebuild without manually retained files in `out`.

A build is not considered reproducible until it succeeds after deleting the Hydrogen One product output and generated vendor tree, then recreating vendor files through the documented extraction process.

## 15. Device bring-up gates

Bring-up proceeds in an order that maximizes diagnostics:

1. bootloader accepts the image and preserves a recoverable slot;
2. kernel reaches init and ramoops/pstore captures failures;
3. required partitions mount with expected labels and options;
4. SELinux policy loads;
5. `adbd` is reachable in the diagnostic build;
6. vendor services start without linker failures;
7. display and touch work;
8. zygote and system server start;
9. boot animation runs and `sys.boot_completed=1` is reached;
10. userdata encryption, reboot, and slot handling remain stable;
11. mandatory hardware is enabled subsystem by subsystem.

Every test build records its source commits, stock/vendor source hash, boot image hash, active slot, flash commands, result, `dmesg`, pstore, full logcat, properties, mounts, `lshal`, services, and relevant dumpsys output.

## 16. Hardware acceptance tiers

### Tier P0: safe and diagnosable boot

- boot and reboot;
- ADB;
- display;
- touch;
- userdata and encryption;
- USB data and charging;
- Wi-Fi;
- basic speaker and microphone path;
- stable suspend/resume sufficient for continued testing.

### Tier P1: usable phone

- SIM detection;
- cellular data;
- SMS;
- voice calls;
- IMS/VoLTE configuration where carrier provisioning permits it;
- proximity and call audio paths;
- Bluetooth;
- GNSS;
- sensors;
- fingerprint;
- front and rear cameras;
- video encode/decode;
- NFC;
- battery reporting and health;
- thermal control;
- A/B OTA and recovery/install flow.

Emergency-call configuration is inspected safely; a real emergency call is not used as a routine test.

### Tier P2: RED-specific features

- Leia/4-View display mode;
- associated RED display firmware and services;
- RED-specific media/framework components;
- haptics behavior beyond standard vibration;
- SmartPort and other proprietary accessories.

P2 does not block first boot, but every unavailable P2 component must have a dependency map explaining what is missing.

## 17. Commit and review structure

Commits follow evidence boundaries rather than file-count convenience. Expected commit classes are:

1. source lock and stock inventory tooling;
2. partition and boot contract;
3. clean product/board skeleton;
4. rootdir, fstab, and recovery;
5. generated vendor foundation;
6. graphics/display;
7. audio;
8. radio/data/IMS;
9. Wi-Fi/Bluetooth/GNSS;
10. camera/media;
11. sensors/fingerprint/NFC;
12. health/thermal/power/USB;
13. SELinux enforcing completion;
14. source-built kernel integration;
15. OTA and final documentation.

Each commit must state its evidence source and verification performed. Generated vendor commits identify the stock source hash and extraction command.

## 18. Completion criteria

The project is complete when all of the following are true:

- the `.118` source is reconstructed, hashed, and verified;
- every stock object is indexed and classified;
- every included proprietary file has a recorded origin and consumer;
- device and vendor repositories contain no separate MSM8998 common layer;
- the vendor repository is reproducibly generated;
- a clean LineageOS 22.2 checkout builds all required images;
- boot, vendor, VINTF, SELinux, and OTA contracts pass their checks;
- SELinux is enforcing;
- the final boot image uses a source-built RED-compatible kernel;
- P0 and P1 hardware tests pass or an explicitly scoped release decision documents a non-critical remaining item;
- P2 status is implemented or dependency-mapped without pretending unsupported RED features work;
- the legacy baseline remains recoverable from its archival branch.

## 19. Current known risks

- The `.118` archive is not yet available locally because of the Drive per-file limit; no `.118` file-level conclusion is accepted before reconstruction.
- The current tree is heavily derived from mata, so apparent completeness can hide wrong device-specific behavior.
- Android 9 proprietary services may require Android 15 linker, VINTF, init, and SELinux adaptation.
- RED-specific kernel source and DTS availability may be incomplete.
- Verizon radio/IMS behavior may require carrier-specific stock components and runtime evidence.
- Leia/4-View functionality may depend on closed framework and firmware components not needed for P0/P1.

These risks change execution order, not the final requirements.
