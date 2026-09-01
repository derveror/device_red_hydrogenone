#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1])
required = [
    'AndroidProducts.mk',
    'BoardConfig.mk',
    'device.mk',
    'twrp_hydrogenone.mk',
    'prebuilt/Image.gz-dtb',
    'recovery/root/fstab/recovery.fstab',
    'recovery/root/fstab/twrp.flags',
    'recovery/root/init.recovery.qcom.rc',
    'recovery/root/init.recovery.usb.rc',
    'recovery/root/ueventd.qcom.rc',
    'recovery/root/system/usr/keylayout/gpio-keys.kl',
]
missing = [p for p in required if not (root / p).exists()]
if missing:
    print('TREE CONTRACT: FAIL')
    print('\n'.join('missing: ' + p for p in missing))
    raise SystemExit(1)

board = (root / 'BoardConfig.mk').read_text(errors='replace')
qcom = (root / 'recovery/root/init.recovery.qcom.rc').read_text(errors='replace')
usb = (root / 'recovery/root/init.recovery.usb.rc').read_text(errors='replace')
kernel = root / 'prebuilt/Image.gz-dtb'
sha = hashlib.sha256(kernel.read_bytes()).hexdigest()
expected = '6cf3a70ece8b32dcd6bccf9db1a22c1da29b9b37fe67cc0e4ec9b4f87fec2426'
checks = [
    ('kernel sha', sha == expected),
    ('64MiB boot', 'BOARD_BOOTIMAGE_PARTITION_SIZE := 67108864' in board),
    ('recovery-as-boot', 'BOARD_USES_RECOVERY_AS_BOOT := true' in board),
    ('UFS path', 'soc/1da4000.ufshc' in qcom),
    ('exclude legacy USB init', 'TW_EXCLUDE_DEFAULT_USB_INIT := true' in board),
    ('ConfigFS controller', 'sys.usb.controller a800000.dwc3' in usb),
    ('ConfigFS enabled', 'sys.usb.configfs 1' in usb),
    ('no legacy android_usb path', '/sys/class/android_usb/android0' not in usb),
]
bad = [name for name, ok in checks if not ok]
if bad:
    print('TREE CONTRACT: FAIL')
    print('\n'.join('failed: ' + name for name in bad))
    raise SystemExit(1)

print('TREE CONTRACT: PASS')
print('kernel SHA-256:', sha)
