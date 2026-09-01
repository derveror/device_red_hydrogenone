#!/usr/bin/env python3
from __future__ import annotations
import gzip, hashlib, struct, subprocess, sys, tempfile
from pathlib import Path

EXPECTED_KERNEL='6cf3a70ece8b32dcd6bccf9db1a22c1da29b9b37fe67cc0e4ec9b4f87fec2426'
BOOT_LIMIT=67108864

def align(n,a): return (n+a-1)//a*a

def fail(msg):
    print('BOOT IMAGE: FAIL')
    print(msg)
    raise SystemExit(1)

p=Path(sys.argv[1] if len(sys.argv)>1 else 'out/target/product/hydrogenone/boot.img')
b=p.read_bytes()
if b[:8]!=b'ANDROID!': fail('bad Android boot magic')
if len(b)>=BOOT_LIMIT: fail(f'image is not smaller than 64 MiB: {len(b)}')
vals=struct.unpack_from('<10I',b,8)
ks,ka,rs,ra,ss,sa,ta,ps,hv,osv=vals
if (ka,ra,ta,ps,hv)!=(0x8000,0x01000000,0x100,4096,0):
    fail(f'header mismatch: kernel={ka:#x} ramdisk={ra:#x} tags={ta:#x} page={ps} hv={hv}')
ko=ps; ro=ko+align(ks,ps)
k=b[ko:ko+ks]; r=b[ro:ro+rs]
kh=hashlib.sha256(k).hexdigest()
if kh!=EXPECTED_KERNEL: fail('stock kernel SHA mismatch: '+kh)
cmd=(b[64:576].split(b'\0',1)[0]+b[608:1632].split(b'\0',1)[0]).decode(errors='replace')
for token in ('androidboot.hardware=qcom','androidboot.configfs=true','androidboot.usbcontroller=a800000.dwc3','androidboot.boot_devices=soc/1da4000.ufshc'):
    if token not in cmd: fail('missing cmdline token: '+token)
try: raw=gzip.decompress(r)
except Exception as e: fail('ramdisk gzip error: '+str(e))
with tempfile.TemporaryDirectory() as td:
    root=Path(td)
    cp=subprocess.run(['cpio','-idmu','--quiet'],cwd=root,input=raw,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if cp.returncode: fail('cpio extraction failed: '+cp.stderr.decode(errors='replace'))
    required=[
        'system/bin/init','system/bin/recovery','system/bin/adbd',
        'init.recovery.qcom.rc','init.recovery.usb.rc',
        'fstab/recovery.fstab','system/etc/twrp.flags','system/etc/init/hw/init.rc'
    ]
    for f in required:
        if not (root/f).exists(): fail('missing ramdisk file: '+f)
    usb=(root/'init.recovery.usb.rc').read_text(errors='replace')
    for token in ('sys.usb.controller a800000.dwc3','sys.usb.configfs 1'):
        if token not in usb: fail('custom ConfigFS USB init incomplete: '+token)
    if '/sys/class/android_usb/android0' in usb:
        fail('legacy android_usb USB init is still installed')
print('BOOT IMAGE: PASS')
print('path:',p)
print('size:',len(b))
print('sha256:',hashlib.sha256(b).hexdigest())
print('kernel sha256:',kh)
print('ramdisk compressed:',rs)
print('cmdline:',cmd)
