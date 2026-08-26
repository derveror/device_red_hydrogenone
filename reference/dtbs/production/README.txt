Production-looking DTBs extracted from the stock H1A1000 Image.gz-dtb:

dtb_40.dtb - CloudMinds redphone TM PVT       (cm,display-id = 0x02)
dtb_49.dtb - CloudMinds redphone TM CSP PVT   (cm,display-id = 0x0e)
dtb_55.dtb - CloudMinds redphone SIM PVT      (cm,display-id = 0x7f)
dtb_58.dtb - CloudMinds redphone JDI PVT      (cm,display-id = 0x64)

Do not collapse these into a single DTB yet. JDI PVT differs substantially from TM PVT,
including touchscreen-related nodes; the stock kernel carries all variants and chooses at boot.
