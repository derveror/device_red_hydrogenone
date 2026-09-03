# RED Hydrogen One — clean LineageOS 22.2 workspace bootstrap

Use this procedure for a **fresh separate source directory**. It is intentionally not a repair/reset procedure for an existing workspace.

The canonical project manifest is:

```text
docs/manifests/hydrogenone-lineage-22.2.xml
```

It pins the RED vendor repository to the exact commit verified by the device cross-tree lock and explicitly selects the LineageOS MSM8998 kernel/sepolicy branches required by this bring-up.

## 1. Create a fresh source directory

Example:

```bash
mkdir -p "$HOME/los-hydrogenone"
cd "$HOME/los-hydrogenone"
```

Do not point this procedure at an existing workspace that contains uncommitted work.

## 2. Initialize LineageOS 22.2

```bash
repo init \
  -u https://github.com/LineageOS/android.git \
  -b lineage-22.2 \
  --git-lfs
```

## 3. Install the Hydrogen One local manifest

```bash
mkdir -p .repo/local_manifests

curl --fail --location --retry 3 \
  https://raw.githubusercontent.com/derveror/device_red_hydrogenone/lineage-22.2-stock118-rework/docs/manifests/hydrogenone-lineage-22.2.xml \
  --output .repo/local_manifests/hydrogenone.xml
```

Validate that the downloaded XML parses before syncing:

```bash
python3 - <<'PY'
import xml.etree.ElementTree as ET
ET.parse('.repo/local_manifests/hydrogenone.xml')
print('hydrogenone local manifest: OK')
PY
```

## 4. Sync the source tree

```bash
repo sync \
  -c \
  --no-clone-bundle \
  --no-tags \
  -j"$(nproc --all)"
```

This bootstrap intentionally does not use `--force-sync`; a fresh checkout should not need it.

If `repo sync` reports a real error, preserve that output rather than deleting projects or changing revisions blindly.

## 5. Validate the completed workspace

From the LineageOS top:

```bash
bash device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh --validate-only
```

The preflight requires all of these checkouts to exist and be clean:

```text
device/red/hydrogenone
vendor/red/hydrogenone
kernel/essential/msm8998
device/qcom/sepolicy-legacy-um
```

It also verifies that the vendor checkout is exactly the SHA in:

```text
device/red/hydrogenone/docs/reference/cross-tree-lock.json
```

## 6. Run the first real build gate

Only after `--validate-only` succeeds:

```bash
bash device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh
```

The script runs only:

```bash
source build/envsetup.sh
lunch lineage_hydrogenone-userdebug
m nothing
```

and writes:

```text
out/hydrogenone-build-logs/m-nothing-<timestamp>.log
out/hydrogenone-build-logs/m-nothing-<timestamp>.meta.txt
out/hydrogenone-build-logs/m-nothing-<timestamp>.status
```

Those files are the authoritative input for the next debugging iteration.

## Gate order after `m nothing`

Do not skip ahead. After `m nothing` is GREEN, proceed one target at a time:

```text
bootimage
vendorimage
systemimage
target-files-package
otapackage
```

Physical-device testing starts only after the relevant image/build gates pass and their outputs are checked against the canonical `.118` partition/boot contracts.
