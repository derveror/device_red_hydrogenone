#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, sys, xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
if len(sys.argv) == 2 and not sys.argv[1].startswith('-'):
    ROOT = Path(sys.argv[1]).resolve()
elif len(sys.argv) > 1:
    raise SystemExit('usage: test_full_tree.py [device-tree-root]')
required_dirs = [
    'audio','configs','gps','keylayout','media','overlay','overlay-lineage',
    'power','configs/camera','configs/nfc','rootdir/etc/init/hw','seccomp','sepolicy/vendor','sepolicy/private',
    'sepolicy/public','wifi','prebuilt'
]
required_files = [
    'Android.bp','AndroidProducts.mk','BoardConfig.mk','device.mk','lineage_hydrogenone.mk',
    'extract-files.py','setup-makefiles.py','proprietary-files.txt',
    'rootdir/etc/fstab.qcom','rootdir/etc/init/hw/init.qcom.rc','rootdir/etc/init/hw/init.qcom.usb.rc','rootdir/etc/init.recovery.qcom.rc','rootdir/etc/ueventd.rc',
    'audio/audio_policy_configuration.xml','audio/audio_platform_info.xml','audio/default_volume_tables.xml','audio/mixer_paths_tasha.xml',
    'media/media_codecs.xml','media/media_profiles_V1_0.xml',
    'configs/msm_irqbalance.conf','configs/thermal-engine.conf','configs/public.libraries.txt',
    'configs/camera/camera_config.xml','configs/nfc/libnfc-nci.conf','configs/nfc/libnfc-nxp.conf',
    'gps/etc/gps.conf','gps/etc/flp.conf','gps/izat.conf','wifi/WCNSS_qcom_cfg.ini','wifi/wpa_supplicant_overlay.conf',
    'seccomp/mediacodec.policy','prebuilt/Image.gz-dtb','vendor.prop'
]
errors=[]

# Approved analysis contract for the stock .118 / Android 15 rework.
required_analysis_files = [
    'docs/superpowers/specs/2026-09-02-hydrogenone-lineage22.2-design.md',
    'docs/reference/SUPPLIED_SOURCES.md',
    'docs/reference/source-lock.json',
    'docs/reference/archive-inventory.json',
    'docs/reference/archive-comparisons.json',
    'docs/reference/full-artifacts.sha256',
    'docs/reference/README.md',
    'docs/stock/h1a1000-r118/README.md',
]
for analysis_file in required_analysis_files:
    if not (ROOT/analysis_file).is_file():
        errors.append('missing analysis contract file: '+analysis_file)

source_lock_path = ROOT/'docs/reference/source-lock.json'
if source_lock_path.is_file():
    try:
        source_lock = json.loads(source_lock_path.read_text(encoding='utf-8'))
        target = source_lock.get('target_platform', {})
        expected_target = {
            'lineage_branch': 'lineage-22.2',
            'android_release': '15',
            'android_api_level': 35,
        }
        if target != expected_target:
            errors.append('source-lock target_platform is not LineageOS 22.2 / Android 15 API 35')
    except Exception as e:
        errors.append(f'cannot validate source-lock target: {e}')

for forbidden_dir in ('device/red/msm8998-common', 'vendor/red/msm8998-common'):
    if (ROOT/forbidden_dir).exists():
        errors.append('forbidden RED common tree exists: '+forbidden_dir)

forbidden_common_paths = ('device/red/msm8998-common', 'vendor/red/msm8998-common')
build_inputs = set(ROOT.rglob('*.mk')) | set(ROOT.rglob('Android.bp'))
for relative in ('lineage.dependencies', 'extract-files.py', 'setup-makefiles.py'):
    candidate = ROOT/relative
    if candidate.is_file():
        build_inputs.add(candidate)
for candidate in sorted(build_inputs):
    relative = str(candidate.relative_to(ROOT))
    if relative.startswith(('docs/', 'tests/', 'tools/')):
        continue
    content = candidate.read_text(errors='ignore')
    for forbidden in forbidden_common_paths:
        if forbidden in content:
            errors.append(f'forbidden RED common-tree reference in {relative}: {forbidden}')
for d in required_dirs:
    if not (ROOT/d).is_dir(): errors.append('missing directory: '+d)
for f in required_files:
    if not (ROOT/f).is_file(): errors.append('missing file: '+f)
for x in ROOT.rglob('*.xml'):
    try: ET.parse(x)
    except ET.ParseError as e: errors.append(f'invalid XML {x.relative_to(ROOT)}: {e}')
for x in ROOT.rglob('*.json'):
    import json
    try: json.loads(x.read_text())
    except Exception as e: errors.append(f'invalid JSON {x.relative_to(ROOT)}: {e}')
# No donor device identity/runtime paths.
for x in ROOT.rglob('*'):
    if x.is_file() and x.suffix.lower() not in {'.dtb','.img','.so','.jar','.apk'} and x.stat().st_size < 2_000_000:
        relative = str(x.relative_to(ROOT))
        if relative.startswith(('docs/', 'reference/', 'tests/', 'tools/')):
            continue
        try: t=x.read_text(errors='ignore')
        except: continue
        if re.search(r'device/(essential/mata|oneplus/dumpling|nubia/nx563j)', t):
            errors.append(f'donor runtime path in {relative}')
        if re.search(r'(?i)(sidecar_essential|hal_sidecar|neko_device|sysfs_sidecar|essential_camera|hal_fingerprint_essential)', t):
            errors.append(f'donor-specific source in {relative}')


# First-stage fstab must use the real UFS path; /dev/block/bootdevice is a later compatibility symlink.
fstab=(ROOT/'rootdir/etc/fstab.qcom').read_text(errors='ignore') if (ROOT/'rootdir/etc/fstab.qcom').exists() else ''
for part in ('system','vendor','userdata','modem','bluetooth','dsp','persist'):
    expected=f'/dev/block/platform/soc/1da4000.ufshc/by-name/{part}'
    if expected not in fstab:
        errors.append('fstab does not use real UFS path for '+part)

# Full subsystem wiring: RED camera tuning and NXP NFC configs must be installed.
device=(ROOT/'device.mk').read_text(errors='ignore') if (ROOT/'device.mk').exists() else ''
for needle in (
    'configs/camera/camera_config.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/camera_config.xml',
    'configs/nfc/libnfc-nci.conf:$(TARGET_COPY_OUT_VENDOR)/etc/libnfc-nci.conf',
    'configs/nfc/libnfc-nxp.conf:$(TARGET_COPY_OUT_VENDOR)/etc/libnfc-nxp.conf',
    'android.hardware.nfc@1.2-service',
    'vendor_bt_firmware_mountpoint',
    'vendor_dsp_mountpoint',
    'vendor_firmware_mnt_mountpoint',
    'android.hardware.light-service.lineage',
):
    if needle not in device:
        errors.append('missing device.mk wiring: '+needle)

# A real LineageOS build requires the verified RED .118 vendor tree. Match
# maintained Lineage device trees and fail early if generated vendor makefiles
# are absent instead of silently configuring a source-only product.
board=(ROOT/'BoardConfig.mk').read_text(errors='ignore') if (ROOT/'BoardConfig.mk').exists() else ''
prod=(ROOT/'lineage_hydrogenone.mk').read_text(errors='ignore') if (ROOT/'lineage_hydrogenone.mk').exists() else ''
if not re.search(r'(?m)^\s*include\s+vendor/red/hydrogenone/BoardConfigVendor\.mk\s*$', board):
    errors.append('missing mandatory RED BoardConfigVendor include')
if re.search(r'(?m)^\s*-include\s+vendor/red/hydrogenone/BoardConfigVendor\.mk\s*$', board):
    errors.append('RED BoardConfigVendor must not be optional')
if '$(call inherit-product, vendor/red/hydrogenone/hydrogenone-vendor.mk)' not in prod:
    errors.append('missing mandatory RED vendor product inheritance')
if 'inherit-product-if-exists, vendor/red/hydrogenone/hydrogenone-vendor.mk' in prod:
    errors.append('RED vendor product inheritance must not be optional')

# MSM8998 generic policy is a real LineageOS dependency, pinned to its 22.2 legacy-um branch.
deps=json.loads((ROOT/'lineage.dependencies').read_text()) if (ROOT/'lineage.dependencies').exists() else []
want={'repository':'android_device_qcom_sepolicy_vndr','target_path':'device/qcom/sepolicy-legacy-um','branch':'lineage-22.2-legacy-um'}
if want not in deps:
    errors.append('missing pinned qcom legacy-um sepolicy dependency')
if 'include device/qcom/sepolicy-legacy-um/SEPolicy.mk' not in board:
    errors.append('missing qcom legacy-um sepolicy include')

# LineageOS 22.2 vendor/lineage/build/tasks/kernel.mk compares TARGET_KERNEL_VERSION
# for every Qualcomm device before it branches to the prebuilt-kernel path.  An
# empty version therefore aborts ckati with `kernel.mk:110: error: Argument missing.`
qcom_enabled = re.search(r'(?m)^\s*BOARD_USES_QCOM_HARDWARE\s*:?=\s*true\s*$', board)
prebuilt_enabled = re.search(r'(?m)^\s*TARGET_PREBUILT_KERNEL\s*:?=', board)
if qcom_enabled and prebuilt_enabled:
    km = re.search(r'(?m)^\s*TARGET_KERNEL_VERSION\s*:?=\s*([0-9]+\.[0-9]+)\s*$', board)
    if not km:
        errors.append('Qualcomm prebuilt kernel requires TARGET_KERNEL_VERSION for Lineage kernel.mk')
    else:
        # Validate the declared major.minor against the first gzip member.  The
        # stock Image.gz-dtb has appended DTBs, so zlib.unused_data is expected.
        import zlib
        kernel_path = ROOT/'prebuilt/Image.gz-dtb'
        if kernel_path.exists():
            try:
                image = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(kernel_path.read_bytes())
                vm = re.search(rb'Linux version ([0-9]+\.[0-9]+)\.', image)
                if vm and km.group(1) != vm.group(1).decode():
                    errors.append(
                        f'TARGET_KERNEL_VERSION {km.group(1)} does not match prebuilt kernel {vm.group(1).decode()}'
                    )
            except zlib.error as e:
                errors.append(f'cannot inspect prebuilt kernel version: {e}')

# A prebuilt boot kernel is not enough for vendorimage. Native Qualcomm modules
# consume generated_kernel_headers, whose LineageOS genrule runs `make -C
# $(TARGET_KERNEL_SOURCE) headers_install` unless a prebuilt header archive is
# configured. Keep the RED boot payload, but provide a maintained MSM8998 source
# tree solely for userspace UAPI header generation.
kernel_source_match = re.search(r'(?m)^\s*TARGET_KERNEL_SOURCE\s*:?=\s*(\S+)\s*$', board)
kernel_config_match = re.search(r'(?m)^\s*TARGET_KERNEL_CONFIG\s*:?=\s*(\S+)\s*$', board)
prebuilt_headers_match = re.search(r'(?m)^\s*TARGET_PREBUILT_KERNEL_HEADERS\s*:?=\s*(\S+)\s*$', board)
if prebuilt_enabled and not (kernel_source_match or prebuilt_headers_match):
    errors.append('prebuilt kernel lacks TARGET_KERNEL_SOURCE or TARGET_PREBUILT_KERNEL_HEADERS for generated kernel headers')
if kernel_source_match:
    if kernel_source_match.group(1) != 'kernel/essential/msm8998':
        errors.append('unexpected kernel header source: '+kernel_source_match.group(1))
    if not kernel_config_match or kernel_config_match.group(1) != 'lineageos_mata_defconfig':
        errors.append('kernel header source requires lineageos_mata_defconfig')
    if not re.search(r'(?m)^\s*TARGET_FORCE_PREBUILT_KERNEL\s*:?=\s*true\s*$', board):
        errors.append('kernel source must not replace the exact RED prebuilt boot kernel')
    kernel_dep={'repository':'android_kernel_essential_msm8998','target_path':'kernel/essential/msm8998'}
    if kernel_dep not in deps:
        errors.append('missing MSM8998 kernel-source dependency used for header generation')

# Exact bring-up kernel identity comes from the canonical RED .118 boot contract.
# Cross-check the boot contract against the independently generated stock inventory
# so changing the prebuilt and its expected hash together cannot silently weaken this audit.
boot_contract_path=ROOT/'docs/stock/h1a1000-r118/boot-image-contract.json'
stock_inventory_path=ROOT/'docs/stock/h1a1000-r118/inventory-summary.json'
try:
    boot_contract=json.loads(boot_contract_path.read_text(encoding='utf-8'))
    stock_inventory=json.loads(stock_inventory_path.read_text(encoding='utf-8'))
    contract_stock_sha=boot_contract.get('authority',{}).get('stock_archive_sha256')
    inventory_stock_sha=stock_inventory.get('canonical_archive',{}).get('sha256')
    if not contract_stock_sha or contract_stock_sha != inventory_stock_sha:
        errors.append('boot contract stock authority does not match canonical inventory')
    expected_kernel=boot_contract.get('kernel',{})
    expected_kernel_sha=expected_kernel.get('sha256')
    expected_kernel_size=expected_kernel.get('size')
    k=ROOT/'prebuilt/Image.gz-dtb'
    if k.exists():
        data=k.read_bytes()
        h=hashlib.sha256(data).hexdigest()
        if h != expected_kernel_sha:
            errors.append('stock kernel hash mismatch: '+h)
        if len(data) != expected_kernel_size:
            errors.append(f'stock kernel size mismatch: {len(data)} != {expected_kernel_size}')
except Exception as e:
    errors.append(f'cannot validate canonical RED .118 kernel contract: {e}')

# A file owned by device.mk must not also be extracted at the same vendor destination.
copy_dest_list=[
    'vendor/'+match.group(1)
    for match in re.finditer(r':\$\(TARGET_COPY_OUT_VENDOR\)/([^\s\\]+)', device)
]
copy_dests=set(copy_dest_list)
duplicate_copy_dests=sorted({x for x in copy_dest_list if copy_dest_list.count(x) > 1})
if duplicate_copy_dests:
    errors.append('duplicate PRODUCT_COPY_FILES destinations: '+', '.join(duplicate_copy_dests[:20]))
prop_sources=set()
for raw in (ROOT/'proprietary-files.txt').read_text(errors='ignore').splitlines():
    line=raw.strip()
    if not line or line.startswith('#'):
        continue
    body=line.split(';',1)[0]
    src=body.split(':',1)[0]
    prop_sources.add(src)
collisions=sorted(copy_dests & prop_sources)
if collisions:
    errors.append('device/vendor ownership collisions: '+', '.join(collisions[:20]))

# A Soong prebuilt_etc module and PRODUCT_COPY_FILES may not own the same output.
# Kati otherwise aborts with `overriding commands for target ... previously defined
# at out/soong/installs-<product>.mk`.  This caught the gps.conf/flp.conf R5 bug.
prebuilt_etc_outputs={}
for bp in ROOT.rglob('Android.bp'):
    text=bp.read_text(errors='ignore')
    for block in re.findall(r'\bprebuilt_etc\s*\{(.*?)\n\}', text, re.S):
        if re.search(r'(?m)^\s*installable\s*:\s*false\s*,?\s*$', block):
            continue
        if not re.search(r'(?m)^\s*vendor\s*:\s*true\s*,?\s*$', block):
            continue
        nm=re.search(r'(?m)^\s*name\s*:\s*"([^"]+)"\s*,?\s*$', block)
        if not nm:
            continue
        fn=re.search(r'(?m)^\s*filename\s*:\s*"([^"]+)"\s*,?\s*$', block)
        sd=re.search(r'(?m)^\s*sub_dir\s*:\s*"([^"]+)"\s*,?\s*$', block)
        filename=fn.group(1) if fn else nm.group(1)
        rel='/'.join(x for x in ('vendor/etc', sd.group(1) if sd else '', filename) if x)
        prebuilt_etc_outputs.setdefault(rel, []).append(str(bp.relative_to(ROOT)))
soong_copy_collisions=sorted(copy_dests & set(prebuilt_etc_outputs))
if soong_copy_collisions:
    errors.append('Soong prebuilt/PRODUCT_COPY_FILES collisions: '+', '.join(soong_copy_collisions[:20]))


# Build/boot contract checks discovered during the second audit.
board_text=(ROOT/'BoardConfig.mk').read_text(errors='ignore') if (ROOT/'BoardConfig.mk').exists() else ''
android_bp=(ROOT/'Android.bp').read_text(errors='ignore') if (ROOT/'Android.bp').exists() else ''
prop_packages=device

# androidboot.hardware=qcom means init imports init.qcom.rc, not init.hydrogenone.rc.
if 'androidboot.hardware=qcom' in board_text:
    if not (ROOT/'rootdir/etc/init/hw/init.qcom.rc').is_file():
        errors.append('androidboot.hardware=qcom but rootdir/etc/init/hw/init.qcom.rc is missing')
    if (ROOT/'rootdir/etc/init/hw/init.hydrogenone.rc').exists():
        errors.append('stale init.hydrogenone.rc will not be imported when ro.hardware=qcom')
main_init=ROOT/'rootdir/etc/init/hw/init.qcom.rc'
if main_init.exists() and 'import /vendor/etc/init/hw/init.qcom.usb.rc' not in main_init.read_text(errors='ignore'):
    errors.append('init.qcom.rc does not import init.qcom.usb.rc')

# Mata's qti vibrator provider lives in the hardware/google/pixel Soong namespace.
for ns in ('hardware/google/interfaces','hardware/google/pixel'):
    if ns not in device:
        errors.append('missing PRODUCT_SOONG_NAMESPACES entry: '+ns)
if 'hardware/google/pixel' not in android_bp:
    errors.append('device Soong namespace does not import hardware/google/pixel')

# Every XInclude used by the selected audio policy must be installed.
audio_policy=ROOT/'audio/audio_policy_configuration.xml'
if audio_policy.exists():
    import xml.etree.ElementTree as _ET
    ns={'xi':'http://www.w3.org/2001/XInclude'}
    ar=_ET.parse(audio_policy).getroot()
    for inc in ar.findall('.//xi:include',ns):
        href=inc.attrib.get('href','')
        if href and f'/etc/{href}' not in device:
            errors.append('audio policy XInclude is not installed: '+href)

# Device-owned init files must not be re-extracted into the future vendor tree.
for owned in ('vendor/etc/init/hw/init.qcom.rc','vendor/etc/init/hw/init.qcom.usb.rc'):
    if owned in prop_sources:
        errors.append('device-owned init path remains in proprietary-files.txt: '+owned)


# Source-only m nothing must not expose a module whose link dependencies are vendor blobs.
# libsynergy_loc_api needs libqmi_cci and libqmi_common_so from vendor/red/hydrogenone.
if (ROOT/'location/synergy_loc_api/Android.bp').exists():
    errors.append('active libsynergy_loc_api Android.bp requires vendor QMI modules during source-only m nothing')
if re.search(r'(?m)^\s*libsynergy_loc_api\s*\\?\s*$', device):
    errors.append('libsynergy_loc_api must not be in base PRODUCT_PACKAGES before vendor tree exists')
gps_conf=(ROOT/'gps/etc/gps.conf').read_text(errors='ignore') if (ROOT/'gps/etc/gps.conf').exists() else ''
active_gps_conf='\n'.join(line for line in gps_conf.splitlines() if not line.lstrip().startswith('#'))
if re.search(r'(?m)^\s*GNSS_DEPLOYMENT\s*=\s*1\s*$', active_gps_conf):
    errors.append('GNSS_DEPLOYMENT=1 selects SS5 but libsynergy_loc_api is inactive')

# The copied Qualcomm GNSS source stack uses the same selector as official mata.
if 'BOARD_VENDOR_QCOM_GPS_LOC_API_HARDWARE := default' not in board_text:
    errors.append('missing BOARD_VENDOR_QCOM_GPS_LOC_API_HARDWARE := default')

# Keep the stock RED configs at the source paths owned by the existing
# prebuilt_etc modules.  Stale root-level copies previously caused device.mk to
# install the same outputs a second time through PRODUCT_COPY_FILES.
for cfg in ('gps.conf','flp.conf','gnss_antenna_info.conf'):
    if not re.search(r'(?m)^\s*'+re.escape(cfg)+r'\s*\\?\s*$', device):
        errors.append('missing GNSS config PRODUCT_PACKAGES entry: '+cfg)
for stale in ('gps/gps.conf','gps/flp.conf'):
    if (ROOT/stale).exists():
        errors.append('stale root-level GNSS config: '+stale)

# first_api_level is generated from PRODUCT/BOARD_SHIPPING_API_LEVEL, not injected into vendor.prop.
vendor_prop=(ROOT/'vendor.prop').read_text(errors='ignore') if (ROOT/'vendor.prop').exists() else ''
if 'ro.product.first_api_level=' in vendor_prop:
    errors.append('ro.product.first_api_level must not be duplicated in vendor.prop')

# Legacy vendor recovery compatibility library follows official mata. Android
# 15 rejects ELF files installed through PRODUCT_COPY_FILES unless the device
# explicitly enables the same narrow compatibility exception used by mata.
recovery_vndksupport_copy = (
    'llndk-stub/libvndksupport.so:'
    '$(TARGET_COPY_OUT_RECOVERY)/root/system/lib64/libvndksupport.so'
)
if recovery_vndksupport_copy not in device:
    errors.append('missing recovery libvndksupport compatibility copy')
if (
    recovery_vndksupport_copy in device
    and 'BUILD_BROKEN_ELF_PREBUILT_PRODUCT_COPY_FILES := true' not in board_text
):
    errors.append(
        'recovery libvndksupport ELF copy requires '
        'BUILD_BROKEN_ELF_PREBUILT_PRODUCT_COPY_FILES := true'
    )


# Product registration must append rather than clobber other products/lunch choices.
products=(ROOT/'AndroidProducts.mk').read_text(errors='ignore') if (ROOT/'AndroidProducts.mk').exists() else ''
if 'PRODUCT_MAKEFILES +=' not in products:
    errors.append('AndroidProducts.mk must append PRODUCT_MAKEFILES with +=')
if 'COMMON_LUNCH_CHOICES +=' not in products:
    errors.append('AndroidProducts.mk must append COMMON_LUNCH_CHOICES with +=')

# Follow the maintained Lineage product inheritance order: common product, base telephony,
# optional proprietary product, then the device definition.
common_pos=prod.find('vendor/lineage/config/common_full_phone.mk')
device_pos=prod.find('device/red/hydrogenone/device.mk')
if common_pos < 0 or device_pos < 0 or common_pos > device_pos:
    errors.append('lineage_hydrogenone.mk inherits device before common_full_phone')


try:
    fingerprint_contract=json.loads((ROOT/'docs/stock/h1a1000-r118/boot-image-contract.json').read_text(encoding='utf-8'))
    expected_fingerprint=fingerprint_contract.get('build_properties',{}).get('ro.build.fingerprint')
    if not expected_fingerprint:
        errors.append('canonical RED .118 boot contract lacks stock fingerprint')
    elif f'BuildFingerprint={expected_fingerprint}' not in prod:
        errors.append('missing exact canonical RED .118 BuildFingerprint override')
except Exception as e:
    errors.append(f'cannot validate canonical RED .118 BuildFingerprint: {e}')


if 'rootdir/etc/init.recovery.qcom.rc:$(TARGET_COPY_OUT_RECOVERY)/root/init.recovery.qcom.rc' not in device:
    errors.append('missing recovery init wiring')

if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print('full-tree contract: PASS')
