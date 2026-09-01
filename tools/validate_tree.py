#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys
root=Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[1])
req=['AndroidProducts.mk','BoardConfig.mk','device.mk','twrp_hydrogenone.mk','prebuilt/Image.gz-dtb','recovery/root/fstab/recovery.fstab','recovery/root/fstab/twrp.flags','recovery/root/init.recovery.qcom.rc','recovery/root/ueventd.qcom.rc','recovery/root/system/usr/keylayout/gpio-keys.kl']
missing=[p for p in req if not (root/p).exists()]
if missing:
 print('TREE CONTRACT: FAIL'); print('\n'.join('missing: '+x for x in missing)); raise SystemExit(1)
k=root/'prebuilt/Image.gz-dtb'; sha=hashlib.sha256(k.read_bytes()).hexdigest()
expect='6cf3a70ece8b32dcd6bccf9db1a22c1da29b9b37fe67cc0e4ec9b4f87fec2426'
checks=[('kernel sha',sha==expect),('64MiB boot','BOARD_BOOTIMAGE_PARTITION_SIZE := 67108864' in (root/'BoardConfig.mk').read_text()),('recovery-as-boot','BOARD_USES_RECOVERY_AS_BOOT := true' in (root/'BoardConfig.mk').read_text()),('UFS path','soc/1da4000.ufshc' in (root/'recovery/root/init.recovery.qcom.rc').read_text())]
bad=[n for n,ok in checks if not ok]
if bad:
 print('TREE CONTRACT: FAIL'); print('\n'.join('failed: '+x for x in bad)); raise SystemExit(1)
print('TREE CONTRACT: PASS')
print('kernel SHA-256:',sha)
