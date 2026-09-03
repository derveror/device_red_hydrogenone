# RED Hydrogen One .118 boot image contract

Canonical stock SHA-256: `7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`

Boot image SHA-256: `8e120a2920f5d4eec65cb5929d31fe271738af85b218d5adb96035eb28806af6`
Header version: `1`; header size: `1648`; page size: `4096`.
Kernel: `37015950` bytes, SHA-256 `584ed86bab46bf57c2cd6b6b48ac4026c5d24a70d57bcdd04472d39c5591064d`.
Ramdisk: `9466573` bytes, SHA-256 `7be9e9c0eedcb38aa8829ccd94a8813b082d7760de93a56b9b35e7175a070767`.
Kernel addr: `0x00008000`; ramdisk addr: `0x01000000`; tags addr: `0x00000100`.
OS: `9.0.0`; patch: `2019-04`.

## Kernel command line

`console=ttyMSM0,115200,n8 androidboot.console=ttyMSM0 earlycon=msm_serial_dm,0xc1b0000 androidboot.hardware=qcom user_debug=31 msm_rtb.filter=0x37 ehci-hcd.park=3 lpm_levels.sleep_disabled=1 sched_enable_hmp=1 sched_enable_power_aware=1 service_locator.enable=1 swiotlb=2048 androidboot.configfs=true androidboot.usbcontroller=a800000.dwc3 firmware_class.path=/vendor/firmware_mnt/image loop.max_part=7 buildvariant=userdebug veritykeyid=id:7e4333f9bba00adfe0ede979e28ed1920492b40f`

## Linux version strings

- None found.

## Matching partition.xml records

- `{'tag': 'partition', 'attributes': {'label': 'system_a', 'size_in_kb': '4194304', 'type': '97D7B011-54DA-4835-B3C4-917AD6E73D74', 'bootable': 'false', 'readonly': 'false', 'filename': 'system.img', 'sparse': 'true'}, 'text': ''}`
- `{'tag': 'partition', 'attributes': {'label': 'vendor_a', 'size_in_kb': '1048576', 'type': '97D7B011-54DA-4835-B3C4-917AD6E73D74', 'bootable': 'false', 'readonly': 'false', 'filename': 'vendor.img', 'sparse': 'true'}, 'text': ''}`
- `{'tag': 'partition', 'attributes': {'label': 'userdata', 'size_in_kb': '12582912', 'type': '1B81E7E6-F50D-419B-A739-2AEEF8DA3335', 'bootable': 'false', 'readonly': 'false', 'filename': 'userdata.img', 'sparse': 'true'}, 'text': ''}`
- `{'tag': 'partition', 'attributes': {'label': 'boot_a', 'size_in_kb': '65536', 'type': '20117F86-E985-4357-B9EE-374BC1D8487D', 'bootable': 'false', 'readonly': 'false', 'filename': 'boot.img'}, 'text': ''}`
- `{'tag': 'partition', 'attributes': {'label': 'boot_b', 'size_in_kb': '65536', 'type': '77036CD4-03D5-42BB-8ED1-37E5A88BAA34', 'bootable': 'false', 'readonly': 'false', 'filename': 'boot.img'}, 'text': ''}`
