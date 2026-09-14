# RED .118 Radio and Camera Runtime Restore Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restore standard Wi-Fi, Bluetooth, camera, and flashlight contracts while preserving the confirmed LineageOS 22.2 boot path.

**Architecture:** Keep source and proprietary ownership separated across the existing kernel, device, and vendor branches.  Make the single proven kernel ABI correction, restore exact RED .118 runtime inputs, and enforce them with cross-tree tests before producing one full build.

**Tech Stack:** Linux 4.4 UAPI, Android product makefiles, extract-utils, Python `unittest`, Soong, LineageOS 22.2 build system.

**Spec:** `docs/superpowers/plans/2026-09-14-radio-camera-runtime-restore-design.md`

## Global Constraints

- Work only on kernel `lineage-22.2`, device `118-lineage-22.2-kernel-302`, and vendor `lineage-22.2-kernel-302`.
- Preserve the confirmed boot, display, touchscreen, DTB, recovery, and init path.
- Use only RED stock Android 9 build .118 proprietary inputs.
- Exclude SmartPort.
- Never flash or reboot the phone during implementation.
- Never commit diagnostic kernel instrumentation.

---

### Task 1: RED Camera Kernel ABI

**Files:**
- Create: `kernel/red/msm8998/tests/test_red118_camera_uapi.py`
- Modify: `kernel/red/msm8998/include/uapi/media/msm_camsensor_sdk.h`
- Modify: `kernel/red/msm8998/include/uapi/media/ais/msm_ais_sensor_sdk.h`

**Interfaces:**
- Consumes: RED .118 camera blob ABI evidence from the approved design.
- Produces: both camera UAPI variants with `MAX_POWER_CONFIG == 16`.

- [x] **Step 1: Write the failing ABI test**

```python
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
HEADERS = ("include/uapi/media/msm_camsensor_sdk.h",
           "include/uapi/media/ais/msm_ais_sensor_sdk.h")

class Red118CameraUapiTest(unittest.TestCase):
    def test_red118_power_array_capacity(self):
        for relative in HEADERS:
            text = (ROOT / relative).read_text()
            self.assertIn("#define MAX_POWER_CONFIG      16", text, relative)
```

- [x] **Step 2: Run the test and require failure on the current value 12**

```bash
python3 -m unittest tests.test_red118_camera_uapi -v
```

- [x] **Step 3: Change only both `MAX_POWER_CONFIG` definitions to 16**

```c
#define MAX_POWER_CONFIG      16
```

- [x] **Step 4: Run the new test and existing kernel contract tests**

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

- [x] **Step 5: Compile the Hydrogen One kernel and verify boot image budget**

```bash
mka bootimage
```

### Task 2: Bluetooth and Wi-Fi Runtime Contracts

**Files:**
- Create: `device/red/hydrogenone/tests/test_radio_runtime_restore_contract.py`
- Modify: `device/red/hydrogenone/Android.bp`
- Modify: `device/red/hydrogenone/device.mk`
- Modify: `device/red/hydrogenone/vendor.prop`

**Interfaces:**
- Consumes: source `libbt-vendor` and RED .118 persist MAC file.
- Produces: packaged Bluetooth vendor library, exact controller property, and stock Wi-Fi MAC link.

- [x] **Step 1: Write tests for the three missing contracts**

```python
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class RadioRuntimeRestoreTest(unittest.TestCase):
    def test_bluetooth_vendor_library_is_packaged(self):
        self.assertIn("libbt-vendor", (ROOT / "device.mk").read_text())

    def test_exact_cherokee_property_exists(self):
        self.assertIn("vendor.qcom.bluetooth.soc=cherokee",
                      (ROOT / "vendor.prop").read_text().splitlines())

    def test_stock118_wlan_mac_link_is_extracted(self):
        bp = (ROOT / "Android.bp").read_text()
        self.assertIn('installed_location: "firmware/wlan/qca_cld/wlan_mac.bin"', bp)
        self.assertIn('symlink_target: "/mnt/vendor/persist/wlan_mac.bin"', bp)
```

- [x] **Step 2: Run the new test and require all three assertions to fail**

```bash
python3 -m unittest tests.test_radio_runtime_restore_contract -v
```

- [x] **Step 3: Add the packages, property, and exact Soong symlink module**

```make
PRODUCT_PACKAGES += \
    libbt-vendor \
    wlan_mac_bin_symlink
```

```properties
vendor.qcom.bluetooth.soc=cherokee
```

```bp
install_symlink {
    name: "wlan_mac_bin_symlink",
    vendor: true,
    installed_location: "firmware/wlan/qca_cld/wlan_mac.bin",
    symlink_target: "/mnt/vendor/persist/wlan_mac.bin",
}
```

- [x] **Step 4: Run device tests and build radio modules**

```bash
python3 -m unittest discover -s device/red/hydrogenone/tests -p 'test_*.py' -v
mka libbt-vendor android.hardware.wifi-service vendorimage
```

### Task 3: Production Camera Proprietary Closure

**Files:**
- Create: `device/red/hydrogenone/tests/test_camera_runtime_closure.py`
- Modify: `device/red/hydrogenone/proprietary-files.txt`
- Regenerate: `vendor/red/hydrogenone/Android.bp`
- Regenerate: `vendor/red/hydrogenone/hydrogenone-vendor.mk`
- Add: selected files under `vendor/red/hydrogenone/proprietary/vendor/lib/`
- Add: `vendor/red/hydrogenone/proprietary/vendor/firmware/cpp_firmware_v1_12_0.fw`

**Interfaces:**
- Consumes: four production chromatix XML files, the captured runtime missing-library set, and `/tmp/red-stock118-vendor.EBES7N`.
- Produces: a vendor image containing every RED .118 production camera runtime input.

- [x] **Step 1: Write a closure test that parses all four XMLs**

```python
for node in ElementTree.parse(xml_path).getroot().iter():
    value = (node.text or "").strip()
    if value:
        expected.add(f"vendor/lib/libchromatix_{value}.so")
self.assertEqual(len(expected), 138)
self.assertTrue(expected.issubset(proprietary_entries))
```

The same test requires `libSonyIMX380PdafLibrary.so`, both LC898219XL
actuators, both M24C64S EEPROM modules, `libflash_pmic.so`, all 36 ISP modules
named by the captured log, the three stock-present image-processing modules,
the `libremosaic_daemon.so` dependency required by `libmmcamera_quadracfa.so`,
and `cpp_firmware_v1_12_0.fw`. Together with the 138 chromatix libraries this
is an exact 185-file production runtime closure.

- [x] **Step 2: Run the closure test and require it to report the absent set**

```bash
python3 -m unittest tests.test_camera_runtime_closure -v
```

- [x] **Step 3: Add the exact paths to `proprietary-files.txt` and extract from .118**

```bash
./extract-files.py /tmp/red-stock118-vendor.EBES7N
```

- [x] **Step 4: Re-run closure tests and verify all generated modules/files**

```bash
python3 -m unittest tests.test_camera_runtime_closure -v
python3 -m unittest discover -s ../vendor/red/hydrogenone/tests -p 'test_*.py' -v
```

- [x] **Step 5: Build camera provider and vendor image**

```bash
mka android.hardware.camera.provider@2.4-service vendorimage
```

### Task 4: Cross-tree Verification and Delivery Build

**Files:**
- Verify all files changed by Tasks 1-3.

**Interfaces:**
- Consumes: passing kernel, device, and vendor contracts.
- Produces: one current LineageOS 22.2 installation ZIP and matching boot image.

- [x] **Step 1: Run every device, vendor, and kernel Python contract test**

```bash
python3 -m unittest discover -s device/red/hydrogenone/tests -p 'test_*.py' -v
python3 -m unittest discover -s vendor/red/hydrogenone/tests -p 'test_*.py' -v
python3 -m unittest discover -s kernel/red/msm8998/tests -p 'test_*.py' -v
```

- [x] **Step 2: Build one cleanly timestamped full package**

```bash
mka bacon
```

- [x] **Step 3: Verify ZIP, boot image, vendor contents, SPL, hashes, and branch diffs**

```bash
unzip -l "$ZIP" | grep -E 'payload.bin|META-INF/com/android/metadata'
sha256sum "$ZIP" out/target/product/hydrogenone/boot.img
```

- [x] **Step 4: Commit and push each repository to its existing named branch**

```bash
git push origin lineage-22.2
git push origin 118-lineage-22.2-kernel-302
git push origin lineage-22.2-kernel-302
```

- [x] **Step 5: Stop before installation and provide artifact paths and manual recovery instructions**

No command in this task may reboot or flash the connected phone.
