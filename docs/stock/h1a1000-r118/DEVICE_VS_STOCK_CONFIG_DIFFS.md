# RED .118 device config semantic differences

Different files: **17**.

## `audio/audio_effects.conf`

Destination: `vendor/etc/audio_effects.conf`.
XML semantically identical after whitespace normalization: `None`.
Changed lines: +0 / -7.

```diff
--- stock-.118/etc/audio_effects.conf
+++ device/audio/audio_effects.conf
@@ -32,9 +32,6 @@
   }
   loudness_enhancer {
     path /vendor/lib/soundfx/libldnhncr.so
-  }
-  dynamics_processing {
-    path /vendor/lib/soundfx/libdynproc.so
   }
   proxy {
     path /vendor/lib/soundfx/libeffectproxy.so
@@ -228,10 +225,6 @@
   loudness_enhancer {
     library loudness_enhancer
     uuid fa415329-2034-4bea-b5dc-5b381c8d1e2c
-  }
-  dynamics_processing {
-    library dynamics_processing
-    uuid e0e6539b-1781-7261-676f-6d7573696340
   }
   aec {
     library audio_pre_processing
```

## `audio/audio_platform_info.xml`

Destination: `vendor/etc/audio_platform_info.xml`.
XML semantically identical after whitespace normalization: `False`.
Changed lines: +2 / -378.

```diff
--- stock-.118/etc/audio_platform_info.xml
+++ device/audio/audio_platform_info.xml
@@ -1,5 +1,5 @@
 <?xml version="1.0" encoding="ISO-8859-1"?>
-<!-- Copyright (c) 2014, 2016-2018, The Linux Foundation. All rights reserved.   -->
+<!-- Copyright (c) 2014, 2016-2017, The Linux Foundation. All rights reserved.   -->
 <!--                                                                        -->
 <!-- Redistribution and use in source and binary forms, with or without     -->
 <!-- modification, are permitted provided that the following conditions are -->
@@ -37,11 +37,6 @@
         <device name="SND_DEVICE_OUT_VOICE_SPEAKER_2_PROTECTED_VBAT" acdb_id="150"/>
         <device name="SND_DEVICE_IN_CAPTURE_VI_FEEDBACK_MONO_1" acdb_id="151"/>
         <device name="SND_DEVICE_IN_CAPTURE_VI_FEEDBACK_MONO_2" acdb_id="152"/>
-        <device name="SND_DEVICE_IN_UNPROCESSED_MIC" acdb_id="143"/>
-        <device name="SND_DEVICE_IN_UNPROCESSED_STEREO_MIC" acdb_id="144"/>
-        <device name="SND_DEVICE_IN_UNPROCESSED_THREE_MIC" acdb_id="145"/>
-        <device name="SND_DEVICE_IN_UNPROCESSED_QUAD_MIC" acdb_id="146"/>
-        <device name="SND_DEVICE_IN_UNPROCESSED_HEADSET_MIC" acdb_id="147"/>
     </acdb_ids>
     <bit_width_configs>
         <device name="SND_DEVICE_OUT_SPEAKER" bit_width="24"/>
@@ -72,7 +67,7 @@
         <usecase name="USECASE_AUDIO_RECORD_AFE_PROXY" type="in" id="7"/>
         <usecase name="USECASE_AUDIO_RECORD_LOW_LATENCY" type="in" id="17" />
         <usecase name="USECASE_AUDIO_PLAYBACK_ULL" type="out" id="17" />
-        <usecase name="USECASE_AUDIO_PLAYBACK_SILENCE" type="out" id="27" />
+        <usecase name="USECASE_AUDIO_PLAYBACK_EXT_DISP_SILENCE" type="out" id="27" />
         <usecase name="USECASE_AUDIO_PLAYBACK_MMAP" type="out" id="33" />
         <usecase name="USECASE_AUDIO_RECORD_MMAP" type="in" id="33" />
     </pcm_ids>
@@ -121,376 +116,5 @@
         <device name="SND_DEVICE_OUT_SPEAKER_AND_BT_SCO" backend="speaker-and-bt-sco" interface="SLIMBUS_0_RX-and-SLIMBUS_7_RX"/>
         <device name="SND_DEVICE_OUT_SPEAKER_AND_BT_SCO_WB" backend="speaker-and-bt-sco-wb" interface="SLIMBUS_0_RX-and-SLIMBUS_7_RX"/>
     </backend_names>
-    <!-- below values are for ref purpose to OEM, doesn't contain actual hardware info on MTP -->
-    <microphone_characteristics>
-        <microphone valid_mask="31" device_id="builtin_mic_1" type="AUDIO_DEVICE_IN_BUILTIN_MIC" address="bottom" location="AUDIO_MICROPHONE_LOCATION_MAINBODY"
-            group="0" index_in_the_group="0" directionality="AUDIO_MICROPHONE_DIRECTIONALITY_OMNI" num_frequency_responses="93"
-            frequencies="100.00 106.00 112.00 118.00 125.00 132.00 140.00 150.00 160.00 170.00 180.00 190.00 200.00 212.00 224.00 236.00 250.00 265.00 280.00 300.00 315.00 335.00 355.00 375.00 400.00 425.00 450.00 475.00 500.00 530.00 560.00 600.00 630.00 670.00 710.00 750.00 800.00 850.00 900.00 950.00 1000.00 1060.00 1120.00 1180.00 1250.00 1320.00 1400.00 1500.00 1600.00 1700.00 1800.00 1900.00 2000.00 2120.00 2240.00 2360.00 2500.00 2650.00 2800.00 3000.00 3150.00 3350.00 3550.00 3750.00 4000.00 4250.00 4500.00 4750.00 5000.00 5300.00 5600.00 6000.00 6300.00 6700.00 7100.00 7500.00 8000.00 8500.00 9000.00 9500.00 10000.00 10600.00 11200.00 11800.00 12500.00 13200.00 14000.00 15000.00 16000.00 17000.00 18000.00 19000.00 20000.00"
-            responses="-0.78 -0.71 -0.64 -0.60 -0.55 -0.50 -0.47 -0.42 -0.39 -0.36 -0.34 -0.33 -0.32 -0.29 -0.28 -0.28 -0.27 -0.25 -0.25 -0.24 -0.23 -0.23 -0.22 -0.22 -0.19 -0.17 -0.15 -0.15 -0.14 -0.14 -0.12 -0.11 -0.10 -0.10 -0.08 -0.07 -0.07 -0.04 -0.03 -0.01 0.00 0.04 0.06 0.07 0.08 0.13 0.09 0.14 0.19 0.23 0.28 0.29 0.31 0.37 0.88 0.86 0.77 0.78 0.84 0.86 1.05 1.12 1.18 1.25 1.43 1.66 1.83 2.02 2.23 2.59 2.84 3.35 4.01 6.82 6.62 6.42 7.30 8.23 7.54 12.68 13.76 18.69 19.68 20.90 23.70 25.10 21.65 16.18 18.84 25.44 23.48 23.22 24.89"
-            sensitivity="-37.0" max_spl="132.5" min_spl="28.5" orientation="0.0 0.0 1.0" geometric_location="0.0269 0.0058 0.0079" />
-        <microphone valid_mask="31" device_id="builtin_mic_2" type="AUDIO_DEVICE_IN_BACK_MIC" address="back" location="AUDIO_MICROPHONE_LOCATION_MAINBODY"
-            group="0" index_in_the_group="1" directionality="AUDIO_MICROPHONE_DIRECTIONALITY_OMNI" num_frequency_responses="92"
-            frequencies="106.00 112.00 118.00 125.00 132.00 140.00 150.00 160.00 170.00 180.00 190.00 200.00 212.00 224.00 236.00 250.00 265.00 280.00 300.00 315.00 335.00 355.00 375.00 400.00 425.00 450.00 475.00 500.00 530.00 560.00 600.00 630.00 670.00 710.00 750.00 800.00 850.00 900.00 950.00 1000.00 1060.00 1120.00 1180.00 1250.00 1320.00 1400.00 1500.00 1600.00 1700.00 1800.00 1900.00 2000.00 2120.00 2240.00 2360.00 2500.00 2650.00 2800.00 3000.00 3150.00 3350.00 3550.00 3750.00 4000.00 4250.00 4500.00 4750.00 5000.00 5300.00 5600.00 6000.00 6300.00 6700.00 7100.00 7500.00 8000.00 8500.00 9000.00 9500.00 10000.00 10600.00 11200.00 11800.00 12500.00 13200.00 14000.00 15000.00 16000.00 17000.00 18000.00 19000.00 20000.00"
-            responses="-0.75 -0.74 -0.69 -0.65 -0.62 -0.61 -0.56 -0.53 -0.50 -0.47 -0.43 -0.40 -0.37 -0.36 -0.33 -0.30 -0.28 -0.25 -0.24 -0.24 -0.24 -0.25 -0.24 -0.12 -0.10 -0.08 -0.09 -0.07 -0.07 -0.06 -0.06 -0.06 -0.05 -0.04 -0.05 -0.04 -0.01 0.02 0.02 0.00 0.02 0.03 0.07 0.10 0.10 0.13 0.01 0.01 0.10 0.11 0.19 0.24 0.38 0.46 0.26 0.27 0.43 0.76 0.75 1.09 1.09 0.94 1.06 1.21 1.47 1.45 1.36 2.07 2.85 2.90 3.85 4.65 5.84 5.46 6.15 7.50 8.30 10.62 12.70 16.65 20.95 25.41 26.32 20.20 16.60 11.24 7.85 7.62 20.19 7.32 2.87 5.18"
-            sensitivity="-37.0" max_spl="132.5" min_spl="28.5" orientation="0.0 1.0 0.0" geometric_location="0.0546 0.1456 0.00415" />
-        <microphone valid_mask="31" device_id="builtin_mic_3" type="AUDIO_DEVICE_IN_BUILTIN_MIC" address="" location="AUDIO_MICROPHONE_LOCATION_MAINBODY"
-            group="0" index_in_the_group="2" directionality="AUDIO_MICROPHONE_DIRECTIONALITY_OMNI" num_frequency_responses="92"
-            frequencies="100.00 106.00 112.00 118.00 125.00 132.00 140.00 150.00 160.00 170.00 180.00 190.00 200.00 212.00 224.00 236.00 250.00 265.00 280.00 300.00 315.00 335.00 355.00 375.00 400.00 425.00 450.00 475.00 500.00 530.00 560.00 600.00 630.00 670.00 710.00 750.00 800.00 850.00 900.00 950.00 1000.00 1060.00 1120.00 1180.00 1250.00 1320.00 1400.00 1500.00 1600.00 1700.00 1800.00 1900.00 2000.00 2120.00 2240.00 2360.00 2500.00 2650.00 2800.00 3000.00 3150.00 3350.00 3550.00 3750.00 4000.00 4250.00 4500.00 4750.00 5000.00 5300.00 5600.00 6000.00 6300.00 6700.00 7100.00 7500.00 8000.00 8500.00 9000.00 9500.00 10000.00 10600.00 11200.00 11800.00 12500.00 13200.00 14000.00 15000.00 16000.00 17000.00 18000.00 19000.00"
-            responses="-9.24 -9.31 -9.39 -9.45 -9.46 -9.47 -9.50 -9.52 -9.51 -9.52 -9.51 -9.50 -9.49 -9.47 -9.48 -9.49 -9.48 -9.50 -9.51 -9.53 -9.55 -9.59 -9.63 -9.67 -9.58 -9.57 -9.65 -9.68 -9.71 -9.75 -9.79 -9.84 -9.87 -9.87 -9.90 -9.90 -9.91 -9.97 -10.01 -10.05 -9.85 -9.93 -9.94 -9.98 -10.04 -10.12 -10.28 -10.25 -10.01 -9.86 -9.81 -9.82 -9.61 -9.46 -8.27 -8.42 -8.98 -8.99 -8.82 -9.21 -8.92 -8.97 -9.30 -9.44 -9.52 -9.28 -9.09 -8.81 -7.02 -5.72 -5.30 -7.26 -8.39 -12.28 -8.23 -6.99 -5.52 -4.87 -3.82 -6.09 0.00 -2.15 -0.26 1.48 5.22 10.92 6.41 9.55 12.96 3.35 22.00 19.75"
-            sensitivity="-37.0" max_spl="132.5" min_spl="28.5" orientation="0.0 0.0 1.0" geometric_location="0.0274 0.14065 0.0079" />
-        <microphone valid_mask="31" device_id="builtin_mic_4" type="AUDIO_DEVICE_IN_BACK_MIC" address="" location="AUDIO_MICROPHONE_LOCATION_MAINBODY"
-            group="0" index_in_the_group="3" directionality="AUDIO_MICROPHONE_DIRECTIONALITY_OMNI" num_frequency_responses="92"
-            frequencies="106.00 112.00 118.00 125.00 132.00 140.00 150.00 160.00 170.00 180.00 190.00 200.00 212.00 224.00 236.00 250.00 265.00 280.00 300.00 315.00 335.00 355.00 375.00 400.00 425.00 450.00 475.00 500.00 530.00 560.00 600.00 630.00 670.00 710.00 750.00 800.00 850.00 900.00 950.00 1000.00 1060.00 1120.00 1180.00 1250.00 1320.00 1400.00 1500.00 1600.00 1700.00 1800.00 1900.00 2000.00 2120.00 2240.00 2360.00 2500.00 2650.00 2800.00 3000.00 3150.00 3350.00 3550.00 3750.00 4000.00 4250.00 4500.00 4750.00 5000.00 5300.00 5600.00 6000.00 6300.00 6700.00 7100.00 7500.00 8000.00 8500.00 9000.00 9500.00 10000.00 10600.00 11200.00 11800.00 12500.00 13200.00 14000.00 15000.00 16000.00 17000.00 18000.00 19000.00 20000.00"
-            responses="-0.75 -0.74 -0.69 -0.65 -0.62 -0.61 -0.56 -0.53 -0.50 -0.47 -0.43 -0.40 -0.37 -0.36 -0.33 -0.30 -0.28 -0.25 -0.24 -0.24 -0.24 -0.25 -0.24 -0.12 -0.10 -0.08 -0.09 -0.07 -0.07 -0.06 -0.06 -0.06 -0.05 -0.04 -0.05 -0.04 -0.01 0.02 0.02 0.00 0.02 0.03 0.07 0.10 0.10 0.13 0.01 0.01 0.10 0.11 0.19 0.24 0.38 0.46 0.26 0.27 0.43 0.76 0.75 1.09 1.09 0.94 1.06 1.21 1.47 1.45 1.36 2.07 2.85 2.90 3.85 4.65 5.84 5.46 6.15 7.50 8.30 10.62 12.70 16.65 20.95 25.41 26.32 20.20 16.60 11.24 7.85 7.62 20.19 7.32 2.87 5.18"
-            sensitivity="-37.0" max_spl="132.5" min_spl="28.5" orientation="0.0 1.0 0.0" geometric_location="0.0546 0.1456 0.00415" />
-    </microphone_characteristics>
-    <snd_devices>
-        <input_snd_device>
-            <input_snd_device_mic_mapping>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_HANDSET_MIC">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_HANDSET_MIC_AEC">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_HANDSET_MIC_NS">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_HANDSET_MIC_AEC_NS">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_HANDSET_DMIC">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_2"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_HANDSET_DMIC_AEC">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_2"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_HANDSET_DMIC_NS">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_2"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_HANDSET_DMIC_AEC_NS">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_2"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_SPEAKER_MIC">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_SPEAKER_MIC_AEC">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_SPEAKER_MIC_NS">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_SPEAKER_MIC_AEC_NS">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_SPEAKER_DMIC">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_2"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_SPEAKER_DMIC_AEC">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_2"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_SPEAKER_DMIC_NS">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_2"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_SPEAKER_DMIC_AEC_NS">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_2"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_VOICE_SPEAKER_MIC">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_CAMCORDER_MIC">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_VOICE_DMIC">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_2"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_VOICE_SPEAKER_DMIC">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_2"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_VOICE_SPEAKER_TMIC">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_2"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_3"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_VOICE_SPEAKER_QMIC">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_2"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_3"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_4"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_VOICE_REC_MIC">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_VOICE_REC_MIC_NS">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_VOICE_REC_DMIC_STEREO">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_2"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_VOICE_REC_DMIC_FLUENCE">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_2"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_AANC_HANDSET_MIC">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_2"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_3"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_QUAD_MIC">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_2"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_3"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_4"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_HANDSET_STEREO_DMIC">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_2"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_SPEAKER_STEREO_DMIC">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_2"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_VOICE_SPEAKER_DMIC_BROADSIDE">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_3"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
-                    <snd_dev in_snd_device="SND_DEVICE_IN_SPEAKER_DMIC_BROADSIDE">
-                        <mic_info mic_device_id="builtin_mic_1"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                        <mic_info mic_device_id="builtin_mic_3"
-                            channel_mapping="AUDIO_MICROPHONE_CHANNEL_MAPPING_PROCESSED"/>
-                    </snd_dev>
... diff truncated; total lines 407
```

## `audio/audio_policy_volumes.xml`

Destination: `vendor/etc/audio_policy_volumes.xml`.
XML semantically identical after whitespace normalization: `False`.
Changed lines: +7 / -33.

```diff
--- stock-.118/etc/audio_policy_volumes.xml
+++ device/audio/audio_policy_volumes.xml
@@ -43,8 +43,6 @@
     </volume>
     <volume stream="AUDIO_STREAM_VOICE_CALL" deviceCategory="DEVICE_CATEGORY_EXT_MEDIA"
                                              ref="DEFAULT_MEDIA_VOLUME_CURVE"/>
-    <volume stream="AUDIO_STREAM_VOICE_CALL" deviceCategory="DEVICE_CATEGORY_HEARING_AID"
-                                             ref="DEFAULT_HEARING_AID_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_SYSTEM" deviceCategory="DEVICE_CATEGORY_HEADSET">
         <point>1,-3000</point>
         <point>33,-2600</point>
@@ -57,8 +55,6 @@
                                          ref="DEFAULT_SYSTEM_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_SYSTEM" deviceCategory="DEVICE_CATEGORY_EXT_MEDIA"
                                          ref="DEFAULT_DEVICE_CATEGORY_EXT_MEDIA_VOLUME_CURVE"/>
-    <volume stream="AUDIO_STREAM_SYSTEM" deviceCategory="DEVICE_CATEGORY_HEARING_AID"
-                                         ref="DEFAULT_HEARING_AID_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_RING" deviceCategory="DEVICE_CATEGORY_HEADSET"
                                        ref="DEFAULT_DEVICE_CATEGORY_HEADSET_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_RING" deviceCategory="DEVICE_CATEGORY_SPEAKER">
@@ -71,8 +67,6 @@
                                        ref="DEFAULT_DEVICE_CATEGORY_EARPIECE_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_RING" deviceCategory="DEVICE_CATEGORY_EXT_MEDIA"
                                        ref="DEFAULT_DEVICE_CATEGORY_EXT_MEDIA_VOLUME_CURVE"/>
-    <volume stream="AUDIO_STREAM_RING" deviceCategory="DEVICE_CATEGORY_HEARING_AID"
-                                       ref="DEFAULT_HEARING_AID_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_MUSIC" deviceCategory="DEVICE_CATEGORY_HEADSET"
                                         ref="DEFAULT_MEDIA_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_MUSIC" deviceCategory="DEVICE_CATEGORY_SPEAKER">
@@ -92,10 +86,8 @@
                                         ref="DEFAULT_MEDIA_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_MUSIC" deviceCategory="DEVICE_CATEGORY_EXT_MEDIA"
                                         ref="DEFAULT_MEDIA_VOLUME_CURVE"/>
-    <volume stream="AUDIO_STREAM_MUSIC" deviceCategory="DEVICE_CATEGORY_HEARING_AID"
-                                        ref="DEFAULT_HEARING_AID_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_ALARM" deviceCategory="DEVICE_CATEGORY_HEADSET"
-                                        ref="DEFAULT_NON_MUTABLE_HEADSET_VOLUME_CURVE"/>
+                                        ref="DEFAULT_DEVICE_CATEGORY_HEADSET_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_ALARM" deviceCategory="DEVICE_CATEGORY_SPEAKER">
         <point>1,-4680</point>
         <point>42,-2070</point>
@@ -103,11 +95,9 @@
         <point>100,0</point>
     </volume>
     <volume stream="AUDIO_STREAM_ALARM" deviceCategory="DEVICE_CATEGORY_EARPIECE"
-                                        ref="DEFAULT_NON_MUTABLE_EARPIECE_VOLUME_CURVE"/>
+                                        ref="DEFAULT_DEVICE_CATEGORY_EARPIECE_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_ALARM" deviceCategory="DEVICE_CATEGORY_EXT_MEDIA"
-                                        ref="DEFAULT_NON_MUTABLE_EXT_VOLUME_CURVE"/>
-    <volume stream="AUDIO_STREAM_ALARM" deviceCategory="DEVICE_CATEGORY_HEARING_AID"
-                                        ref="DEFAULT_NON_MUTABLE_HEARING_AID_VOLUME_CURVE"/>
+                                        ref="DEFAULT_DEVICE_CATEGORY_EXT_MEDIA_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_NOTIFICATION" deviceCategory="DEVICE_CATEGORY_HEADSET"
                                                ref="DEFAULT_DEVICE_CATEGORY_HEADSET_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_NOTIFICATION" deviceCategory="DEVICE_CATEGORY_SPEAKER">
@@ -120,8 +110,6 @@
                                                ref="DEFAULT_DEVICE_CATEGORY_EARPIECE_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_NOTIFICATION" deviceCategory="DEVICE_CATEGORY_EXT_MEDIA"
                                                ref="DEFAULT_DEVICE_CATEGORY_EXT_MEDIA_VOLUME_CURVE"/>
-    <volume stream="AUDIO_STREAM_NOTIFICATION" deviceCategory="DEVICE_CATEGORY_HEARING_AID"
-                                               ref="DEFAULT_DEVICE_CATEGORY_HEADSET_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_BLUETOOTH_SCO" deviceCategory="DEVICE_CATEGORY_HEADSET">
         <point>0,-4200</point>
         <point>33,-2800</point>
@@ -142,8 +130,6 @@
     </volume>
     <volume stream="AUDIO_STREAM_BLUETOOTH_SCO" deviceCategory="DEVICE_CATEGORY_EXT_MEDIA"
                                                 ref="DEFAULT_MEDIA_VOLUME_CURVE"/>
-    <volume stream="AUDIO_STREAM_BLUETOOTH_SCO" deviceCategory="DEVICE_CATEGORY_HEARING_AID"
-                                                ref="DEFAULT_HEARING_AID_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_ENFORCED_AUDIBLE" deviceCategory="DEVICE_CATEGORY_HEADSET">
         <point>1,-3000</point>
         <point>33,-2600</point>
@@ -156,8 +142,6 @@
                                                    ref="DEFAULT_SYSTEM_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_ENFORCED_AUDIBLE" deviceCategory="DEVICE_CATEGORY_EXT_MEDIA"
                                                    ref="DEFAULT_DEVICE_CATEGORY_EXT_MEDIA_VOLUME_CURVE"/>
-    <volume stream="AUDIO_STREAM_ENFORCED_AUDIBLE" deviceCategory="DEVICE_CATEGORY_HEARING_AID"
-                                                   ref="DEFAULT_HEARING_AID_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_DTMF" deviceCategory="DEVICE_CATEGORY_HEADSET">
         <point>1,-3000</point>
         <point>33,-2600</point>
@@ -170,8 +154,6 @@
                                        ref="DEFAULT_SYSTEM_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_DTMF" deviceCategory="DEVICE_CATEGORY_EXT_MEDIA"
                                        ref="DEFAULT_DEVICE_CATEGORY_EXT_MEDIA_VOLUME_CURVE"/>
-    <volume stream="AUDIO_STREAM_DTMF" deviceCategory="DEVICE_CATEGORY_HEARING_AID"
-                                       ref="DEFAULT_HEARING_AID_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_TTS" deviceCategory="DEVICE_CATEGORY_HEADSET"
                                       ref="SILENT_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_TTS" deviceCategory="DEVICE_CATEGORY_SPEAKER"
@@ -180,18 +162,14 @@
                                       ref="SILENT_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_TTS" deviceCategory="DEVICE_CATEGORY_EXT_MEDIA"
                                       ref="SILENT_VOLUME_CURVE"/>
-    <volume stream="AUDIO_STREAM_TTS" deviceCategory="DEVICE_CATEGORY_HEARING_AID"
-                                      ref="SILENT_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_ACCESSIBILITY" deviceCategory="DEVICE_CATEGORY_HEADSET"
-                                                ref="DEFAULT_NON_MUTABLE_VOLUME_CURVE"/>
+                                                ref="DEFAULT_MEDIA_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_ACCESSIBILITY" deviceCategory="DEVICE_CATEGORY_SPEAKER"
-                                                ref="DEFAULT_NON_MUTABLE_SPEAKER_VOLUME_CURVE"/>
+                                                ref="DEFAULT_DEVICE_CATEGORY_SPEAKER_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_ACCESSIBILITY" deviceCategory="DEVICE_CATEGORY_EARPIECE"
-                                                ref="DEFAULT_NON_MUTABLE_VOLUME_CURVE"/>
+                                                ref="DEFAULT_MEDIA_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_ACCESSIBILITY" deviceCategory="DEVICE_CATEGORY_EXT_MEDIA"
-                                                ref="DEFAULT_NON_MUTABLE_VOLUME_CURVE"/>
-    <volume stream="AUDIO_STREAM_ACCESSIBILITY" deviceCategory="DEVICE_CATEGORY_HEARING_AID"
-                                                ref="DEFAULT_NON_MUTABLE_HEARING_AID_VOLUME_CURVE"/>
+                                                ref="DEFAULT_MEDIA_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_REROUTING" deviceCategory="DEVICE_CATEGORY_HEADSET"
                                             ref="FULL_SCALE_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_REROUTING" deviceCategory="DEVICE_CATEGORY_SPEAKER"
@@ -199,8 +177,6 @@
     <volume stream="AUDIO_STREAM_REROUTING" deviceCategory="DEVICE_CATEGORY_EARPIECE"
                                             ref="FULL_SCALE_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_REROUTING" deviceCategory="DEVICE_CATEGORY_EXT_MEDIA"
-                                            ref="FULL_SCALE_VOLUME_CURVE"/>
-    <volume stream="AUDIO_STREAM_REROUTING" deviceCategory="DEVICE_CATEGORY_HEARING_AID"
                                             ref="FULL_SCALE_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_PATCH" deviceCategory="DEVICE_CATEGORY_HEADSET"
                                         ref="FULL_SCALE_VOLUME_CURVE"/>
@@ -210,7 +186,5 @@
                                         ref="FULL_SCALE_VOLUME_CURVE"/>
     <volume stream="AUDIO_STREAM_PATCH" deviceCategory="DEVICE_CATEGORY_EXT_MEDIA"
                                         ref="FULL_SCALE_VOLUME_CURVE"/>
-    <volume stream="AUDIO_STREAM_PATCH" deviceCategory="DEVICE_CATEGORY_HEARING_AID"
-                                        ref="FULL_SCALE_VOLUME_CURVE"/>
 </volumes>

```

## `configs/camera/camera_config.xml`

Destination: `vendor/etc/camera/camera_config.xml`.
XML semantically identical after whitespace normalization: `False`.
Changed lines: +1 / -2.

```diff
--- stock-.118/etc/camera/camera_config.xml
+++ device/configs/camera/camera_config.xml
@@ -87,7 +87,6 @@
 -->

 <CameraConfigurationRoot>
-<!--
   <CameraModuleConfig>
     <CameraId>0</CameraId>
     <SensorName>s5k2l7sx</SensorName>
@@ -166,7 +165,7 @@
       <MinFocusDistance>0.1</MinFocusDistance>
     </LensInfo>
   </CameraModuleConfig>
--->
+
   <CameraModuleConfig>
     <CameraId>0</CameraId>
     <SensorName>imx380_main</SensorName>
@@ -254,7 +253,6 @@
       <MinFocusDistance>0.34</MinFocusDistance>
     </LensInfo>
   </CameraModuleConfig>
-
   <CameraModuleConfig>
     <CameraId>3</CameraId>
     <SensorName>imx268_main</SensorName>
```

## `configs/camera/imx268_main_chromatix.xml`

Destination: `vendor/etc/camera/imx268_main_chromatix.xml`.
XML semantically identical after whitespace normalization: `False`.
Changed lines: +2 / -2.

```diff
--- stock-.118/etc/camera/imx268_main_chromatix.xml
+++ device/configs/camera/imx268_main_chromatix.xml
@@ -114,7 +114,7 @@
       <A3Video>imx268_main_zsl_video_lc898122</A3Video>
     </ChromatixName>
     <!--wuyh0623@thundersoft.com begin-->
-    <ChromatixName sensor_resolution_index="0" special_mode_mask = "CM_3D_VIDEO_MODE">
+    <ChromatixName sensor_resolution_index="0" special_mode_mask = "ARC_3D_MODE">
       <ISPPreview>imx268_main_preview</ISPPreview>
       <ISPSnapshot>imx268_main_preview</ISPSnapshot>
       <ISPVideo>imx268_main_default_video</ISPVideo>
@@ -140,7 +140,7 @@
       <A3Video>imx268_main_zsl_video_lc898122</A3Video>
     </ChromatixName>
     <!--wuyh0623@thundersoft.com begin-->
-    <ChromatixName sensor_resolution_index="1" special_mode_mask = "CM_3D_VIDEO_MODE">
+    <ChromatixName sensor_resolution_index="1" special_mode_mask = "ARC_3D_MODE">
       <ISPPreview>imx268_main_preview</ISPPreview>
       <ISPSnapshot>imx268_main_preview</ISPSnapshot>
       <ISPVideo>imx268_main_default_video</ISPVideo>
```

## `configs/camera/imx268_sub_chromatix.xml`

Destination: `vendor/etc/camera/imx268_sub_chromatix.xml`.
XML semantically identical after whitespace normalization: `False`.
Changed lines: +2 / -2.

```diff
--- stock-.118/etc/camera/imx268_sub_chromatix.xml
+++ device/configs/camera/imx268_sub_chromatix.xml
@@ -114,7 +114,7 @@
       <A3Video>imx268_sub_zsl_video_lc898122</A3Video>
     </ChromatixName>
     <!--wuyh0623@thundersoft.com begin-->
-    <ChromatixName sensor_resolution_index="0" special_mode_mask = "CM_3D_VIDEO_MODE">
+    <ChromatixName sensor_resolution_index="0" special_mode_mask = "ARC_3D_MODE">
       <ISPPreview>imx268_sub_preview</ISPPreview>
       <ISPSnapshot>imx268_sub_preview</ISPSnapshot>
       <ISPVideo>imx268_sub_default_video</ISPVideo>
@@ -140,7 +140,7 @@
       <A3Video>imx268_sub_zsl_video_lc898122</A3Video>
     </ChromatixName>
     <!--wuyh0623@thundersoft.com begin-->
-    <ChromatixName sensor_resolution_index="1" special_mode_mask = "CM_3D_VIDEO_MODE">
+    <ChromatixName sensor_resolution_index="1" special_mode_mask = "ARC_3D_MODE">
       <ISPPreview>imx268_sub_preview</ISPPreview>
       <ISPSnapshot>imx268_sub_preview</ISPSnapshot>
       <ISPVideo>imx268_sub_default_video</ISPVideo>
```

## `configs/camera/imx380_main_chromatix.xml`

Destination: `vendor/etc/camera/imx380_main_chromatix.xml`.
XML semantically identical after whitespace normalization: `False`.
Changed lines: +1 / -24.

```diff
--- stock-.118/etc/camera/imx380_main_chromatix.xml
+++ device/configs/camera/imx380_main_chromatix.xml
@@ -128,31 +128,13 @@
       <A3Preview>imx380_main_4k_preview_lc898122</A3Preview>
       <A3Video>imx380_main_4k_video_lc898122</A3Video>
     </ChromatixName>
-    <!--4k for 3d video used when >1080p-->
-    <ChromatixName sensor_resolution_index="1" special_mode_mask = "CM_3D_VIDEO_MODE">
+    <ChromatixName sensor_resolution_index="1" special_mode_mask = "ARC_3D_MODE">
       <ISPPreview>imx380_main_preview</ISPPreview>
       <ISPSnapshot>imx380_main_preview</ISPSnapshot>
       <ISPVideo>imx380_main_default_video</ISPVideo>
       <CPPVideo>imx380_main_cpp_video</CPPVideo>
       <A3Preview>imx380_main_zsl_preview_lc898122_3dmode</A3Preview>
       <A3Video>imx380_main_zsl_video_lc898122</A3Video>
-    </ChromatixName>
-    <ChromatixName sensor_resolution_index="1" special_mode_mask = "CM_3D_SNAPSHOT_MODE">
-      <ISPPreview>imx380_main_preview</ISPPreview>
-      <ISPSnapshot>imx380_main_preview</ISPSnapshot>
-      <ISPVideo>imx380_main_default_video</ISPVideo>
-      <CPPSnapshot>imx380_main_cpp_4k_3d_snapshot</CPPSnapshot>
-      <CPPVideo>imx380_main_cpp_video</CPPVideo>
-      <A3Preview>imx380_main_4k_3d_snapshot_lc898122</A3Preview>
-      <A3Video>imx380_main_zsl_video_lc898122</A3Video>
-    </ChromatixName>
-    <ChromatixName sensor_resolution_index="1" special_mode_mask = "CM_PANORAMA_MODE">
-      <ISPPreview>imx380_main_preview</ISPPreview>
-      <ISPSnapshot>imx380_main_preview</ISPSnapshot>
-      <ISPVideo>imx380_main_default_video</ISPVideo>
-      <CPPVideo>imx380_main_cpp_video</CPPVideo>
-      <A3Preview>imx380_main_4k_panorama_lc898122</A3Preview>
-      <A3Video>imx380_main_4k_video_lc898122</A3Video>
     </ChromatixName>
     <ChromatixName sensor_resolution_index="2">
       <ISPPreview>imx380_main_qhd_hfr_60</ISPPreview>
@@ -190,7 +172,6 @@
       <A3Preview>imx380_main_480p_hfr_240_lc898122</A3Preview>
       <A3Video>imx380_main_480p_hfr_240_lc898122</A3Video>
     </ChromatixName>
-    <!--360p 30fps for 3d video chat-->
     <ChromatixName sensor_resolution_index="6">
       <ISPPreview>imx380_main_snapshot</ISPPreview>
       <ISPSnapshot>imx380_main_snapshot</ISPSnapshot>
@@ -199,18 +180,14 @@
       <A3Preview>imx380_main_360p_3d_video_lc898122</A3Preview>
       <A3Video>imx380_main_zsl_video_lc898122</A3Video>
     </ChromatixName>
-    <!--1080p 30fps for 3d video, used default-->
     <ChromatixName sensor_resolution_index="7">
       <ISPPreview>imx380_main_snapshot</ISPPreview>
       <ISPSnapshot>imx380_main_snapshot</ISPSnapshot>
       <ISPVideo>imx380_main_default_video</ISPVideo>
-      <CPPPreview>imx380_main_cpp_1080p_3d_video</CPPPreview>
-      <CPPSnapshot>imx380_main_cpp_1080p_3d_video</CPPSnapshot>
       <CPPVideo>imx380_main_cpp_video</CPPVideo>
       <A3Preview>imx380_main_1080p_3d_video_lc898122</A3Preview>
       <A3Video>imx380_main_zsl_video_lc898122</A3Video>
     </ChromatixName>
-    <!--720p 30fps for 3d video, no used-->
     <ChromatixName sensor_resolution_index="8">
       <ISPPreview>imx380_main_snapshot</ISPPreview>
       <ISPSnapshot>imx380_main_snapshot</ISPSnapshot>
```

## `configs/camera/imx380_sub_chromatix.xml`

Destination: `vendor/etc/camera/imx380_sub_chromatix.xml`.
XML semantically identical after whitespace normalization: `False`.
Changed lines: +1 / -20.

```diff
--- stock-.118/etc/camera/imx380_sub_chromatix.xml
+++ device/configs/camera/imx380_sub_chromatix.xml
@@ -128,30 +128,13 @@
       <A3Preview>imx380_sub_4k_preview_lc898122</A3Preview>
       <A3Video>imx380_sub_4k_video_lc898122</A3Video>
     </ChromatixName>
-    <ChromatixName sensor_resolution_index="1" special_mode_mask = "CM_3D_VIDEO_MODE">
+    <ChromatixName sensor_resolution_index="1" special_mode_mask = "ARC_3D_MODE">
       <ISPPreview>imx380_sub_preview</ISPPreview>
       <ISPSnapshot>imx380_sub_preview</ISPSnapshot>
       <ISPVideo>imx380_sub_default_video</ISPVideo>
       <CPPVideo>imx380_sub_cpp_video</CPPVideo>
       <A3Preview>imx380_sub_zsl_preview_lc898122_3dmode</A3Preview>
       <A3Video>imx380_sub_zsl_video_lc898122</A3Video>
-    </ChromatixName>
-    <ChromatixName sensor_resolution_index="1" special_mode_mask = "CM_3D_SNAPSHOT_MODE">
-      <ISPPreview>imx380_sub_preview</ISPPreview>
-      <ISPSnapshot>imx380_sub_preview</ISPSnapshot>
-      <ISPVideo>imx380_sub_default_video</ISPVideo>
-      <CPPSnapshot>imx380_sub_cpp_4k_3d_snapshot</CPPSnapshot>
-      <CPPVideo>imx380_sub_cpp_video</CPPVideo>
-      <A3Preview>imx380_sub_4k_3d_snapshot_lc898122</A3Preview>
-      <A3Video>imx380_sub_zsl_video_lc898122</A3Video>
-    </ChromatixName>
-    <ChromatixName sensor_resolution_index="1" special_mode_mask = "CM_PANORAMA_MODE">
-      <ISPPreview>imx380_sub_preview</ISPPreview>
-      <ISPSnapshot>imx380_sub_preview</ISPSnapshot>
-      <ISPVideo>imx380_sub_default_video</ISPVideo>
-      <CPPVideo>imx380_sub_cpp_video</CPPVideo>
-      <A3Preview>imx380_sub_4k_panorama_lc898122</A3Preview>
-      <A3Video>imx380_sub_4k_video_lc898122</A3Video>
     </ChromatixName>
     <ChromatixName sensor_resolution_index="2">
       <ISPPreview>imx380_sub_qhd_hfr_60</ISPPreview>
@@ -201,8 +184,6 @@
       <ISPPreview>imx380_sub_snapshot</ISPPreview>
       <ISPSnapshot>imx380_sub_snapshot</ISPSnapshot>
       <ISPVideo>imx380_sub_default_video</ISPVideo>
-      <CPPPreview>imx380_sub_cpp_1080p_3d_video</CPPPreview>
-      <CPPSnapshot>imx380_sub_cpp_1080p_3d_video</CPPSnapshot>
       <CPPVideo>imx380_sub_cpp_video</CPPVideo>
       <A3Preview>imx380_sub_1080p_3d_video_lc898122</A3Preview>
       <A3Video>imx380_sub_zsl_video_lc898122</A3Video>
```

## `audio/default_volume_tables.xml`

Destination: `vendor/etc/default_volume_tables.xml`.
XML semantically identical after whitespace normalization: `False`.
Changed lines: +0 / -59.

```diff
--- stock-.118/etc/default_volume_tables.xml
+++ device/audio/default_volume_tables.xml
@@ -67,63 +67,4 @@
         <point>60,-2100</point>
         <point>100,-1000</point>
     </reference>
-    <reference name="DEFAULT_HEARING_AID_VOLUME_CURVE">
-    <!-- Default Hearing Aid Volume Curve -->
-        <point>1,-12700</point>
-        <point>20,-8000</point>
-        <point>60,-4000</point>
-        <point>100,0</point>
-    </reference>
-    <!-- **************************************************************** -->
-    <!-- Non-mutable default volume curves:                               -->
-    <!--     * first point is always for index 0                          -->
-    <!--     * attenuation is small enough that stream can still be heard -->
-    <reference name="DEFAULT_NON_MUTABLE_VOLUME_CURVE">
-    <!-- Default non-mutable reference Volume Curve -->
-    <!--        based on DEFAULT_MEDIA_VOLUME_CURVE -->
-        <point>0,-5800</point>
-        <point>20,-4000</point>
-        <point>60,-1700</point>
-        <point>100,0</point>
-    </reference>
-    <reference name="DEFAULT_NON_MUTABLE_HEADSET_VOLUME_CURVE">
-    <!--Default non-mutable Volume Curve for headset -->
-    <!--    based on DEFAULT_DEVICE_CATEGORY_HEADSET_VOLUME_CURVE -->
-        <point>0,-4950</point>
-        <point>33,-3350</point>
-        <point>66,-1700</point>
-        <point>100,0</point>
-    </reference>
-    <reference name="DEFAULT_NON_MUTABLE_SPEAKER_VOLUME_CURVE">
-    <!-- Default non-mutable Speaker Volume Curve -->
-    <!--    based on DEFAULT_DEVICE_CATEGORY_SPEAKER_VOLUME_CURVE -->
-        <point>0,-5800</point>
-        <point>20,-4000</point>
-        <point>60,-1700</point>
-        <point>100,0</point>
-    </reference>
-    <reference name="DEFAULT_NON_MUTABLE_EARPIECE_VOLUME_CURVE">
-    <!--Default non-mutable Volume Curve -->
-    <!--    based on DEFAULT_DEVICE_CATEGORY_EARPIECE_VOLUME_CURVE -->
-        <point>0,-4950</point>
-        <point>33,-3350</point>
-        <point>66,-1700</point>
-        <point>100,0</point>
-    </reference>
-    <reference name="DEFAULT_NON_MUTABLE_EXT_VOLUME_CURVE">
-    <!-- Default non-mutable Ext Media System Volume Curve -->
-    <!--     based on DEFAULT_DEVICE_CATEGORY_EXT_MEDIA_VOLUME_CURVE -->
-        <point>0,-5800</point>
-        <point>20,-4000</point>
-        <point>60,-2100</point>
-        <point>100,-1000</point>
-    </reference>
-    <reference name="DEFAULT_NON_MUTABLE_HEARING_AID_VOLUME_CURVE">
-    <!-- Default non-mutable Hearing Aid Volume Curve -->
-    <!--     based on DEFAULT_HEARING_AID_VOLUME_CURVE -->
-        <point>0,-12700</point>
-        <point>20,-8000</point>
-        <point>60,-4000</point>
-        <point>100,0</point>
-    </reference>
 </volumes>
```

## `rootdir/etc/fstab.qcom`

Destination: `vendor/etc/fstab.qcom`.
XML semantically identical after whitespace normalization: `None`.
Changed lines: +14 / -19.

```diff
--- stock-.118/etc/fstab.qcom
+++ device/rootdir/etc/fstab.qcom
@@ -1,19 +1,14 @@
-# Android fstab file.
-# The filesystem that contains the filesystem checker binary (typically /system) cannot
-# specify MF_CHECK, and must come before any filesystems that do specify MF_CHECK
-
-#TODO: Add 'check' as fs_mgr_flags with data partition.
-# Currently we dont have e2fsck compiled. So fs check would failed.
-
-# A/B fstab.qcom variant
-#<src>                                   <mnt_point>             <type> <mnt_flags and options>                          <fs_mgr_flags>
-/dev/block/bootdevice/by-name/system     /                       ext4   ro,barrier=1,discard                             wait,slotselect,verify
-/dev/block/bootdevice/by-name/userdata   /data              ext4   noatime,nosuid,nodev,barrier=1,noauto_da_alloc,discard wait,check,forceencrypt=footer,quota,reservedsize=128M
-/devices/soc/c0a4900.sdhci/mmc_host*     /storage/sdcard1        vfat   nosuid,nodev                                     wait,voldmanaged=sdcard1:auto,encryptable=footer
-/dev/block/bootdevice/by-name/misc       /misc                   emmc   defaults                                         defaults
-/dev/block/bootdevice/by-name/modem      /vendor/firmware_mnt    vfat   ro,shortname=lower,uid=0,gid=1000,dmask=227,fmask=337,context=u:object_r:firmware_file:s0 wait,slotselect
-/dev/block/bootdevice/by-name/bluetooth  /vendor/bt_firmware     vfat   ro,shortname=lower,uid=1002,gid=3002,dmask=227,fmask=337,context=u:object_r:bt_firmware_file:s0 wait,slotselect
-/dev/block/bootdevice/by-name/dsp        /vendor/dsp             ext4   ro,nosuid,nodev,barrier=1                        wait,slotselect
-/dev/block/bootdevice/by-name/persist    /mnt/vendor/persist     ext4   noatime,nosuid,nodev,barrier=1                   wait
-/devices/*/xhci-hcd.0.auto/usb*          auto               auto   defaults                                         voldmanaged=usb:auto
-/devices/*/xhci-hcd.1.auto/usb*          auto               auto   defaults                                         voldmanaged=usb:auto
+# RED Hydrogen One H1A1000 - LineageOS 22.2
+# Stock FDE userdata must be formatted before first FBE boot.
+/dev/block/platform/soc/1da4000.ufshc/by-name/system     /system              ext4  ro,barrier=1,discard                                  wait,slotselect,first_stage_mount
+/dev/block/platform/soc/1da4000.ufshc/by-name/vendor     /vendor              ext4  ro,barrier=1,discard                                  wait,slotselect,first_stage_mount
+/dev/block/platform/soc/1da4000.ufshc/by-name/userdata   /data                ext4  noatime,nosuid,nodev,barrier=1,noauto_da_alloc,discard wait,check,latemount,formattable,fileencryption=ice,quota
+/dev/block/platform/soc/1da4000.ufshc/by-name/misc       /misc                emmc  defaults                                              defaults
+/dev/block/platform/soc/1da4000.ufshc/by-name/modem      /vendor/firmware_mnt vfat  ro,shortname=lower,uid=1000,gid=1000,dmask=227,fmask=337,context=u:object_r:firmware_file:s0 wait,slotselect
+/dev/block/platform/soc/1da4000.ufshc/by-name/bluetooth  /vendor/bt_firmware  vfat  ro,shortname=lower,uid=1002,gid=3002,dmask=227,fmask=337,context=u:object_r:bt_firmware_file:s0 wait,slotselect
+/dev/block/platform/soc/1da4000.ufshc/by-name/dsp        /vendor/dsp          ext4  ro,nosuid,nodev,barrier=1,context=u:object_r:adsprpcd_file:s0 wait,slotselect
+/dev/block/platform/soc/1da4000.ufshc/by-name/persist    /mnt/vendor/persist  ext4  noatime,nosuid,nodev,barrier=1                         wait
+/devices/soc/c0a4900.sdhci/mmc_host*     /storage/sdcard1     vfat  nosuid,nodev                                          wait,voldmanaged=sdcard1:auto
+/devices/*/xhci-hcd.0.auto/usb*          auto                 auto  defaults                                              voldmanaged=usb:auto
+/devices/*/xhci-hcd.1.auto/usb*          auto                 auto  defaults                                              voldmanaged=usb:auto
+/dev/block/zram0                         none                 swap  defaults                                              zramsize=2147483648
```

## `gps/izat.conf`

Destination: `vendor/etc/izat.conf`.
XML semantically identical after whitespace normalization: `None`.
Changed lines: +34 / -10.

```diff
--- stock-.118/etc/izat.conf
+++ device/gps/izat.conf
@@ -46,12 +46,16 @@
 NLP_COMBO_MODE_USES_QNP_WITH_NO_EULA_CONSENT = 1

 #########################################
-# NLP PACKAGE SETTINGS
-#########################################
-# OSNLP_PACKAGE has been deprecated and replaced
-# by system property ro.location.osnlp.package
-# REGION_OSNLP_PACKAGE has been deprecated and
-# replaced by system property ro.location.osnlp.region.package
+# NLP PACKAGE AND ACTION SETTINGS
+#########################################
+# OSNLP_PACKAGE/OSNLP_ACTION: name/action of default NLP package
+OSNLP_PACKAGE = com.google.android.gms
+OSNLP_ACTION = com.android.location.service.v3.NetworkLocationProvider
+# REGION_OSNLP_PACKAGE/REGION_OSNLP_ACTION:
+# These two values will be used as alternative
+# for particular region where default NLP is not functional.
+#REGION_OSNLP_PACKAGE = com.baidu.map.location
+#REGION_OSNLP_ACTION = com.android.location.service.v3.NetworkLocationProvider

 # Threshold period for ZPP triggers
 ZPP_TRIGGER_THRESHOLD=60000
@@ -182,8 +186,12 @@
 IZAT_FEATURE_MASK=0
 PLATFORMS=all
 BASEBAND=all
+LEAN_TARGETS=DISABLED
 HARDWARE_TYPE=automotive

+#Valyes for LEAN_TARGETS can be:
+#ENABLED  -> if this process is supposed to run on lean and mean targets
+#DISABLED -> if this process is to be disabled on lean and mean targets
 PROCESS_NAME=garden_app
 PROCESS_ARGUMENT=-l 0 -T 1
 PROCESS_STATE=ENABLED
@@ -192,6 +200,7 @@
 IZAT_FEATURE_MASK=0
 PLATFORMS=all
 BASEBAND=all
+LEAN_TARGETS=DISABLED
 HARDWARE_TYPE=automotive

 PROCESS_NAME=gpsone_daemon
@@ -202,16 +211,18 @@
 IZAT_FEATURE_MASK=0
 PLATFORMS=msm7630_fusion
 BASEBAND=svlte2a sglte sglte2
+LEAN_TARGETS=DISABLED
 HARDWARE_TYPE=all

 PROCESS_NAME=lowi-server
 PROCESS_ARGUMENT=
 PROCESS_STATE=ENABLED
-PROCESS_GROUPS=gps net_admin wifi inet oem_2901
+PROCESS_GROUPS=gps net_admin wifi inet qcom_diag
 PREMIUM_FEATURE=0
 IZAT_FEATURE_MASK=0xf303
 PLATFORMS=all
 BASEBAND=all
+LEAN_TARGETS=DISABLED
 HARDWARE_TYPE=all

 PROCESS_NAME=xtwifi-inet-agent
@@ -222,26 +233,29 @@
 IZAT_FEATURE_MASK=0xf0f
 PLATFORMS=all
 BASEBAND=all
+LEAN_TARGETS=DISABLED
 HARDWARE_TYPE=all

 PROCESS_NAME=xtwifi-client
 PROCESS_ARGUMENT=
 PROCESS_STATE=ENABLED
-PROCESS_GROUPS=wifi inet gps system oem_2904
+PROCESS_GROUPS=wifi inet gps system oem_2952
 PREMIUM_FEATURE=1
 IZAT_FEATURE_MASK=0xf0f
 PLATFORMS=all
 BASEBAND=all
+LEAN_TARGETS=DISABLED
 HARDWARE_TYPE=all

 PROCESS_NAME=slim_daemon
 PROCESS_ARGUMENT=
 PROCESS_STATE=ENABLED
-PROCESS_GROUPS=gps oem_2901 can
+PROCESS_GROUPS=gps qcom_diag can
 PREMIUM_FEATURE=1
 IZAT_FEATURE_MASK=0xf0
 PLATFORMS=all
 BASEBAND=all
+LEAN_TARGETS=DISABLED
 HARDWARE_TYPE=all

 PROCESS_NAME=xtra-daemon
@@ -252,4 +266,14 @@
 IZAT_FEATURE_MASK=0
 PLATFORMS=all
 BASEBAND=all
-HARDWARE_TYPE=all
+LEAN_TARGETS=DISABLED
+HARDWARE_TYPE=all
+
+##################################################
+# The name of process which launches XTRA client.
+# Default process name in software which launches
+# XTRA client is system-server. Uncomment the below
+# to set the desired process which will start the
+# XTRA client.
+##################################################
+# XC20_LAUNCH_PROCESS_NAME=garden_app
```

## `media/media_codecs_vendor_audio.xml`

Destination: `vendor/etc/media_codecs_vendor_audio.xml`.
XML semantically identical after whitespace normalization: `False`.
Changed lines: +0 / -72.

```diff
--- stock-.118/etc/media_codecs_vendor_audio.xml
+++ device/media/media_codecs_vendor_audio.xml
@@ -18,81 +18,9 @@
 -->
 <Included>
     <Decoders>
-        <MediaCodec name="OMX.google.mp3.decoder" type="audio/mpeg">
-            <Limit name="channel-count" max="2" />
-            <Limit name="sample-rate" ranges="8000,11025,12000,16000,22050,24000,32000,44100,48000" />
-            <Limit name="bitrate" range="8000-320000" />
-        </MediaCodec>
-        <MediaCodec name="OMX.google.amrnb.decoder" type="audio/3gpp">
-            <Limit name="channel-count" max="1" />
-            <Limit name="sample-rate" ranges="8000" />
-            <Limit name="bitrate" range="4750-12200" />
-        </MediaCodec>
-        <MediaCodec name="OMX.google.amrwb.decoder" type="audio/amr-wb">
-            <Limit name="channel-count" max="1" />
-            <Limit name="sample-rate" ranges="16000" />
-            <Limit name="bitrate" range="6600-23850" />
-        </MediaCodec>
-        <MediaCodec name="OMX.google.aac.decoder" type="audio/mp4a-latm">
-            <Limit name="channel-count" max="8" />
-            <Limit name="sample-rate" ranges="7350,8000,11025,12000,16000,22050,24000,32000,44100,48000" />
-            <Limit name="bitrate" range="8000-960000" />
-        </MediaCodec>
-        <MediaCodec name="OMX.google.g711.alaw.decoder" type="audio/g711-alaw">
-            <Limit name="channel-count" max="1" />
-            <Limit name="sample-rate" ranges="8000-48000" />
-            <Limit name="bitrate" range="64000" />
-        </MediaCodec>
-        <MediaCodec name="OMX.google.g711.mlaw.decoder" type="audio/g711-mlaw">
-            <Limit name="channel-count" max="1" />
-            <Limit name="sample-rate" ranges="8000-48000" />
-            <Limit name="bitrate" range="64000" />
-        </MediaCodec>
-        <MediaCodec name="OMX.google.vorbis.decoder" type="audio/vorbis">
-            <Limit name="channel-count" max="8" />
-            <Limit name="sample-rate" ranges="8000-96000" />
-            <Limit name="bitrate" range="32000-500000" />
-        </MediaCodec>
-        <MediaCodec name="OMX.google.opus.decoder" type="audio/opus">
-            <Limit name="channel-count" max="8" />
-            <Limit name="sample-rate" ranges="48000" />
-            <Limit name="bitrate" range="6000-510000" />
-        </MediaCodec>
-        <MediaCodec name="OMX.google.raw.decoder" type="audio/raw">
-            <Limit name="channel-count" max="8" />
-            <Limit name="sample-rate" ranges="8000-96000" />
-            <Limit name="bitrate" range="1-10000000" />
-        </MediaCodec>
         <!-- SimpleOMXComponet based software decoder-->
         <MediaCodec name="OMX.qti.audio.decoder.flac" type="audio/flac" >
             <Limit name="concurrent-instances" max="10" />
         </MediaCodec>
     </Decoders>
-    <Encoders>
-        <MediaCodec name="OMX.google.aac.encoder" type="audio/mp4a-latm">
-            <Limit name="channel-count" max="6" />
-            <Limit name="sample-rate" ranges="8000,11025,12000,16000,22050,24000,32000,44100,48000" />
-            <!-- also may support 64000, 88200  and 96000 Hz -->
-            <Limit name="bitrate" range="8000-960000" />
-        </MediaCodec>
-        <MediaCodec name="OMX.google.amrnb.encoder" type="audio/3gpp">
-            <Limit name="channel-count" max="1" />
-            <Limit name="sample-rate" ranges="8000" />
-            <Limit name="bitrate" range="4750-12200" />
-            <Feature name="bitrate-modes" value="CBR" />
-        </MediaCodec>
-        <MediaCodec name="OMX.google.amrwb.encoder" type="audio/amr-wb">
-            <Limit name="channel-count" max="1" />
-            <Limit name="sample-rate" ranges="16000" />
-            <Limit name="bitrate" range="6600-23850" />
-            <Feature name="bitrate-modes" value="CBR" />
-        </MediaCodec>
-        <MediaCodec name="OMX.google.flac.encoder" type="audio/flac">
-            <Limit name="channel-count" max="2" />
-            <Limit name="sample-rate" ranges="1-655350" />
-            <Limit name="bitrate" range="1-21000000" />
-            <Limit name="complexity" range="0-8"  default="5" />
-            <Feature name="bitrate-modes" value="CQ" />
-        </MediaCodec>
-    </Encoders>
 </Included>
```

## `media/media_profiles_V1_0.xml`

Destination: `vendor/etc/media_profiles_V1_0.xml`.
XML semantically identical after whitespace normalization: `False`.
Changed lines: +6 / -492.

```diff
--- stock-.118/etc/media_profiles_V1_0.xml
+++ device/media/media_profiles_V1_0.xml
@@ -25,7 +25,7 @@
 <!ATTLIST EncoderProfile quality (high|low) #REQUIRED>
 <!ATTLIST EncoderProfile fileFormat (mp4|3gp) #REQUIRED>
 <!ATTLIST EncoderProfile duration (30|60) #REQUIRED>
-<!ATTLIST EncoderProfile cameraId (0|1|2|3|4|5) #REQUIRED>
+<!ATTLIST EncoderProfile cameraId (0|1) #REQUIRED>
 <!ELEMENT Video EMPTY>
 <!ATTLIST Video codec (h264|h263|m4v) #REQUIRED>
 <!ATTLIST Video bitRate CDATA #REQUIRED>
@@ -90,7 +90,7 @@
     <CamcorderProfiles cameraId="0">

         <EncoderProfile quality="qvga" fileFormat="3gp" duration="60">
-            <Video codec="h264"
+            <Video codec="m4v"
                    bitRate="128000"
                    width="320"
                    height="240"
@@ -224,7 +224,7 @@
     <CamcorderProfiles cameraId="1">

         <EncoderProfile quality="qvga" fileFormat="3gp" duration="60">
-            <Video codec="h264"
+            <Video codec="m4v"
                    bitRate="128000"
                    width="320"
                    height="240"
@@ -330,492 +330,6 @@

     </CamcorderProfiles>

-    <CamcorderProfiles cameraId="2">
-
-        <EncoderProfile quality="qvga" fileFormat="3gp" duration="60">
-            <Video codec="h264"
-                   bitRate="128000"
-                   width="320"
-                   height="240"
-                   frameRate="15" />
-            <Audio codec="amrnb"
-                   bitRate="12200"
-                   sampleRate="8000"
-                   channels="1" />
-        </EncoderProfile>
-
-        <EncoderProfile quality="cif" fileFormat="mp4" duration="30">
-            <Video codec="h264"
-                   bitRate="1200000"
-                   width="352"
-                   height="288"
-                   frameRate="30" />
-            <Audio codec="aac"
-                   bitRate="96000"
-                   sampleRate="48000"
-                   channels="1" />
-        </EncoderProfile>
-
-        <EncoderProfile quality="480p" fileFormat="mp4" duration="30">
-            <Video codec="h264"
-                   bitRate="6000000"
-                   width="720"
-                   height="480"
-                   frameRate="30" />
-            <Audio codec="aac"
-                   bitRate="96000"
-                   sampleRate="48000"
-                   channels="1" />
-        </EncoderProfile>
-
-        <EncoderProfile quality="720p" fileFormat="mp4" duration="30">
-            <Video codec="h264"
-                   bitRate="12000000"
-                   width="1280"
-                   height="720"
-                   frameRate="30" />
-            <Audio codec="aac"
-                   bitRate="96000"
-                   sampleRate="48000"
-                   channels="1" />
-        </EncoderProfile>
-
-        <EncoderProfile quality="1080p" fileFormat="mp4" duration="30">
-            <Video codec="h264"
-                   bitRate="17000000"
-                   width="1920"
-                   height="1080"
-                   frameRate="30" />
-            <Audio codec="aac"
-                   bitRate="96000"
-                   sampleRate="48000"
-                   channels="1" />
-        </EncoderProfile>
-
-        <EncoderProfile quality="timelapseqcif" fileFormat="mp4" duration="30">
-            <Video codec="h264"
-                   bitRate="192000"
-                   width="176"
-                   height="144"
-                   frameRate="30" />
-            <!-- audio setting is ignored -->
-            <Audio codec="amrnb"
-                   bitRate="12200"
-                   sampleRate="8000"
-                   channels="1" />
-        </EncoderProfile>
-
-        <EncoderProfile quality="timelapsecif" fileFormat="mp4" duration="30">
-            <Video codec="h264"
-                   bitRate="1200000"
-                   width="352"
-                   height="288"
-                   frameRate="30" />
-            <!-- audio setting is ignored -->
-            <Audio codec="aac"
-                   bitRate="96000"
-                   sampleRate="48000"
-                   channels="1" />
-        </EncoderProfile>
-
-        <EncoderProfile quality="timelapse480p" fileFormat="mp4" duration="30">
-            <Video codec="h264"
-                   bitRate="6000000"
-                   width="720"
-                   height="480"
-                   frameRate="30" />
-            <!-- audio setting is ignored -->
-            <Audio codec="aac"
-                   bitRate="96000"
-                   sampleRate="48000"
-                   channels="1" />
-        </EncoderProfile>
-
-        <EncoderProfile quality="timelapse720p" fileFormat="mp4" duration="30">
-            <Video codec="h264"
-                   bitRate="12000000"
-                   width="1280"
-                   height="720"
-                   frameRate="30" />
-            <!-- audio setting is ignored -->
-            <Audio codec="aac"
-                   bitRate="96000"
-                   sampleRate="48000"
-                   channels="1" />
-        </EncoderProfile>
-
-        <EncoderProfile quality="timelapse1080p" fileFormat="mp4" duration="30">
-            <Video codec="h264"
-                   bitRate="17000000"
-                   width="1920"
-                   height="1080"
-                   frameRate="30" />
-            <!-- audio setting is ignored -->
-            <Audio codec="aac"
-                   bitRate="96000"
-                   sampleRate="48000"
-                   channels="1" />
-        </EncoderProfile>
-
-        <ImageEncoding quality="95" />
-        <ImageEncoding quality="80" />
-        <ImageEncoding quality="70" />
-        <ImageDecoding memCap="20000000" />
-
-    </CamcorderProfiles>
-
-    <CamcorderProfiles cameraId="3">
-
-        <EncoderProfile quality="qvga" fileFormat="3gp" duration="60">
-            <Video codec="h264"
-                   bitRate="128000"
-                   width="320"
-                   height="240"
-                   frameRate="15" />
-            <Audio codec="amrnb"
-                   bitRate="12200"
-                   sampleRate="8000"
-                   channels="1" />
-        </EncoderProfile>
-
-        <EncoderProfile quality="cif" fileFormat="mp4" duration="30">
-            <Video codec="h264"
-                   bitRate="1200000"
-                   width="352"
-                   height="288"
-                   frameRate="30" />
-            <Audio codec="aac"
-                   bitRate="96000"
-                   sampleRate="48000"
-                   channels="1" />
-        </EncoderProfile>
-
-        <EncoderProfile quality="480p" fileFormat="mp4" duration="30">
-            <Video codec="h264"
-                   bitRate="6000000"
-                   width="720"
-                   height="480"
-                   frameRate="30" />
-            <Audio codec="aac"
-                   bitRate="96000"
-                   sampleRate="48000"
-                   channels="1" />
-        </EncoderProfile>
-
-        <EncoderProfile quality="720p" fileFormat="mp4" duration="30">
-            <Video codec="h264"
-                   bitRate="12000000"
-                   width="1280"
-                   height="720"
-                   frameRate="30" />
-            <Audio codec="aac"
-                   bitRate="96000"
-                   sampleRate="48000"
-                   channels="1" />
-        </EncoderProfile>
-
-        <EncoderProfile quality="timelapseqcif" fileFormat="mp4" duration="30">
-            <Video codec="h264"
-                   bitRate="192000"
-                   width="176"
-                   height="144"
-                   frameRate="30" />
-            <!-- audio setting is ignored -->
-            <Audio codec="amrnb"
-                   bitRate="12200"
-                   sampleRate="8000"
-                   channels="1" />
-        </EncoderProfile>
-
-        <EncoderProfile quality="timelapsecif" fileFormat="mp4" duration="30">
-            <Video codec="h264"
-                   bitRate="1200000"
-                   width="352"
-                   height="288"
-                   frameRate="30" />
-            <!-- audio setting is ignored -->
-            <Audio codec="aac"
-                   bitRate="96000"
-                   sampleRate="48000"
... diff truncated; total lines 543
```

## `audio/mixer_paths_tasha.xml`

Destination: `vendor/etc/mixer_paths_tasha.xml`.
XML semantically identical after whitespace normalization: `False`.
Changed lines: +25 / -65.

```diff
--- stock-.118/etc/mixer_paths_tasha.xml
+++ device/audio/mixer_paths_tasha.xml
@@ -1,5 +1,5 @@
 <?xml version="1.0" encoding="ISO-8859-1"?>
-<!-- Copyright (c) 2015-2018, The Linux Foundation. All rights reserved.    -->
+<!-- Copyright (c) 2015-2017, The Linux Foundation. All rights reserved.    -->
 <!--                                                                        -->
 <!-- Redistribution and use in source and binary forms, with or without     -->
 <!-- modification, are permitted provided that the following conditions are -->
@@ -125,10 +125,6 @@
     <ctl name="MultiMedia1 Mixer SLIM_0_TX" value="0" />
     <ctl name="MultiMedia1 Mixer SLIM_4_TX" value="0" />
     <ctl name="MultiMedia1 Mixer SLIM_7_TX" value="0" />
-    <ctl name="HDMI RX Format" value="LPCM" />
-    <ctl name="HDMI_RX Bit Format" value="S16_LE" />
-    <ctl name="HDMI_RX SampleRate" value="KHZ_48" />
-    <ctl name="HDMI_RX Channels" value="Two" />
     <ctl name="HDMI Mixer MultiMedia1" value="0" />
     <ctl name="HDMI Mixer MultiMedia2" value="0" />
     <ctl name="HDMI Mixer MultiMedia3" value="0" />
@@ -143,10 +139,6 @@
     <ctl name="HDMI Mixer MultiMedia14" value="0" />
     <ctl name="HDMI Mixer MultiMedia15" value="0" />
     <ctl name="HDMI Mixer MultiMedia16" value="0" />
-    <ctl name="Display Port RX Format" value="LPCM" />
-    <ctl name="Display Port RX Bit Format" value="S16_LE" />
-    <ctl name="Display Port RX SampleRate" value="KHZ_48" />
-    <ctl name="Display Port RX Channels" value="Two" />
     <ctl name="DISPLAY_PORT Mixer MultiMedia1" value="0" />
     <ctl name="DISPLAY_PORT Mixer MultiMedia2" value="0" />
     <ctl name="DISPLAY_PORT Mixer MultiMedia3" value="0" />
@@ -575,6 +567,8 @@
     <ctl name="SLIMBUS_5_TX LSM Function" value="None" />
     <!-- listen end-->
     <!-- split a2dp -->
+    <ctl name="BT SampleRate" value="KHZ_8" />
+    <ctl name="AFE Input Channels" value="Zero" />
     <ctl name="SLIM7_RX ADM Channels" value="Zero" />
     <!-- split a2dp end-->

@@ -660,8 +654,7 @@
     </path>

     <path name="deep-buffer-playback bt-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="deep-buffer-playback bt-sco" />
     </path>

@@ -722,8 +715,7 @@
     </path>

     <path name="low-latency-playback bt-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="low-latency-playback bt-sco" />
     </path>

@@ -803,8 +795,7 @@
     </path>

     <path name="audio-ull-playback bt-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="audio-ull-playback bt-sco" />
     </path>

@@ -881,8 +872,7 @@
     </path>

     <path name="compress-offload-playback bt-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="compress-offload-playback bt-sco" />
     </path>

@@ -953,8 +943,7 @@
     </path>

     <path name="compress-offload-playback2 bt-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="compress-offload-playback2 bt-sco" />
     </path>

@@ -1025,8 +1014,7 @@
     </path>

     <path name="compress-offload-playback3 bt-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="compress-offload-playback3 bt-sco" />
     </path>

@@ -1097,8 +1085,7 @@
     </path>

     <path name="compress-offload-playback4 bt-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="compress-offload-playback4 bt-sco" />
     </path>

@@ -1170,8 +1157,7 @@
     </path>

     <path name="compress-offload-playback5 bt-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="compress-offload-playback5 bt-sco" />
     </path>

@@ -1242,8 +1228,7 @@
     </path>

     <path name="compress-offload-playback6 bt-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="compress-offload-playback6 bt-sco" />
     </path>

@@ -1314,8 +1299,7 @@
     </path>

     <path name="compress-offload-playback7 bt-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="compress-offload-playback7 bt-sco" />
     </path>

@@ -1386,8 +1370,7 @@
     </path>

     <path name="compress-offload-playback8 bt-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="compress-offload-playback8 bt-sco" />
     </path>

@@ -1458,8 +1441,7 @@
     </path>

     <path name="compress-offload-playback9 bt-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="compress-offload-playback9 bt-sco" />
     </path>

@@ -1526,8 +1508,7 @@
     </path>

     <path name="audio-record bt-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="audio-record bt-sco" />
     </path>

@@ -1544,8 +1525,7 @@
     </path>

     <path name="audio-record-compress bt-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="audio-record-compress bt-sco" />
     </path>

@@ -1562,8 +1542,7 @@
     </path>

     <path name="low-latency-record bt-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="low-latency-record bt-sco" />
     </path>

@@ -1730,8 +1709,7 @@
     </path>

    <path name="hfp-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="hfp-sco" />
    </path>

@@ -1762,8 +1740,7 @@
     </path>

     <path name="compress-voip-call bt-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="compress-voip-call bt-sco" />
     </path>

@@ -1813,8 +1790,7 @@
     </path>

     <path name="vowlan-call bt-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="vowlan-call bt-sco" />
     </path>

@@ -1864,8 +1840,7 @@
     </path>

     <path name="voicemmode1-call bt-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="voicemmode1-call bt-sco" />
     </path>

@@ -1915,8 +1890,7 @@
     </path>

     <path name="voicemmode2-call bt-sco-wb">
-        <ctl name="BT SampleRate RX" value="KHZ_16" />
-        <ctl name="BT SampleRate TX" value="KHZ_16" />
+        <ctl name="BT SampleRate" value="KHZ_16" />
         <path name="voicemmode2-call bt-sco" />
     </path>

... diff truncated; total lines 271
```

## `power/powerhint.xml`

Destination: `vendor/etc/powerhint.xml`.
XML semantically identical after whitespace normalization: `False`.
Changed lines: +1 / -1.

```diff
--- stock-.118/etc/powerhint.xml
+++ device/power/powerhint.xml
@@ -65,7 +65,7 @@
         <!-- L CPU - disable ignore_hispeed_notif -->
         <!-- B CPU - disable ignore_hispeed_notif -->
         <Config
-            Id="0x00001203" Enable="true" Timeout="0" Target="msm8998"
+            Id="0x00001203" Enable="true" Target="msm8998"
             Resources="0x41400000, 0x4, 0x41410000, 0x5F ,0x41414000, 0x326, 0x41420000, 0x5A, 0x41400100, 0x4, 0x41410100
             , 0x5F, 0x41414100, 0x22C, 0x41420100, 0x5A, 0x41810000 ,0x9C4, 0x41814000,
             0x32, 0x4180C000 ,0x0, 0x41820000, 0xA, 0x41438100, 0x0, 0x41438000, 0x0" />
```

## `configs/public.libraries.txt`

Destination: `vendor/etc/public.libraries.txt`.
XML semantically identical after whitespace normalization: `None`.
Changed lines: +2 / -4.

```diff
--- stock-.118/etc/public.libraries.txt
+++ device/configs/public.libraries.txt
@@ -2,8 +2,6 @@
 libadsprpc.so
 libcdsprpc.so
 libsdsprpc.so
-libfastcvopt.so
-liblistenjni.so
-liblistensoundmodel2.so
+libqvrservice_client.so
+libvraudio_client.so
 libOpenCL.so
-libnpu.so
```

## `configs/sec_config`

Destination: `vendor/etc/sec_config`.
XML semantically identical after whitespace normalization: `None`.
Changed lines: +257 / -265.

```diff
--- stock-.118/etc/sec_config
+++ device/configs/sec_config
@@ -1,8 +1,6 @@
 /* IPC Security Config */
 /* <GPS QMI Service ID - 16>:<GPS QMI Instance ID - all instances>:<Client Group ID> */
-16:4294967295:1000:1021:1026
-/* <QDMA QMI Service ID - 75>:<QDMA QMI Instance ID - all instances>:<Client Group ID> */
-75:4294967295:1000:1001:3006
+16:4294967295:1000:1021
 /* <LOWI QMI Service ID - 38>:<LOWI QMI Instance ID - all instances>:<Client Group ID> */
 56:4294967295:1021
 /* Allow SS CTL service to be used by system and net_raw processes */
@@ -14,270 +12,264 @@
 /* QMI-SLIM service permitted to gps and net_raw */
 55:4294967295:1021
 /* Allow Sensor services to be used by sensor process */
-256:4294967295:1000:1006:1013:1021:1047:3011
-257:4294967295:1000:1006:1013:1021:1047:3011
-258:4294967295:1000:1006:1013:1021:1047:3011
-259:4294967295:1000:1006:1013:1021:1047:3011
-260:4294967295:1000:1006:1013:1021:1047:3011
-261:4294967295:1000:1006:1013:1021:1047:3011
-262:4294967295:1000:1006:1013:1021:1047:3011
-263:4294967295:1000:1006:1013:1021:1047:3011
-264:4294967295:1000:1006:1013:1021:1047:3011
-265:4294967295:1000:1006:1013:1021:1047:3011
-266:4294967295:1000:1006:1013:1021:1047:3011
-267:4294967295:1000:1006:1013:1021:1047:3011
-268:4294967295:1000:1006:1013:1021:1047:3011
-269:4294967295:1000:1006:1013:1021:1047:3011
-270:4294967295:1000:1006:1013:1021:1047:3011
-271:4294967295:1000:1006:1013:1021:1047:3011
-272:4294967295:1000:1006:1013:1021:1047:3011
-273:4294967295:1000:1006:1013:1021:1047:3011
-274:4294967295:1000:1006:1013:1021:1047:3011
-275:4294967295:1000:1006:1013:1021:1047:3011
-276:4294967295:1000:1006:1013:1021:1047:3011
-277:4294967295:1000:1006:1013:1021:1047:3011
-278:4294967295:1000:1006:1013:1021:1047:3011
-279:4294967295:1000:1006:1013:1021:1047:3011
-280:4294967295:1000:1006:1013:1021:1047:3011
-281:4294967295:1000:1006:1013:1021:1047:3011
-282:4294967295:1000:1006:1013:1021:1047:3011
-283:4294967295:1000:1006:1013:1021:1047:3011
-284:4294967295:1000:1006:1013:1021:1047:3011
-285:4294967295:1000:1006:1013:1021:1047:3011
-286:4294967295:1000:1006:1013:1021:1047:3011
-287:4294967295:1000:1006:1013:1021:1047:3011
-288:4294967295:1000:1006:1013:1021:1047:3011
-289:4294967295:1000:1006:1013:1021:1047:3011
-290:4294967295:1000:1006:1013:1021:1047:3011
-291:4294967295:1000:1006:1013:1021:1047:3011
-292:4294967295:1000:1006:1013:1021:1047:3011
-293:4294967295:1000:1006:1013:1021:1047:3011
-294:4294967295:1000:1006:1013:1021:1047:3011
-295:4294967295:1000:1006:1013:1021:1047:3011
-296:4294967295:1000:1006:1013:1021:1047:3011
-297:4294967295:1000:1006:1013:1021:1047:3011
-298:4294967295:1000:1006:1013:1021:1047:3011
-299:4294967295:1000:1006:1013:1021:1047:3011
-300:4294967295:1000:1006:1013:1021:1047:3011
-301:4294967295:1000:1006:1013:1021:1047:3011
-302:4294967295:1000:1006:1013:1021:1047:3011
-303:4294967295:1000:1006:1013:1021:1047:3011
-304:4294967295:1000:1006:1013:1021:1047:3011
-305:4294967295:1000:1006:1013:1021:1047:3011
-306:4294967295:1000:1006:1013:1021:1047:3011
-307:4294967295:1000:1006:1013:1021:1047:3011
-308:4294967295:1000:1006:1013:1021:1047:3011
-309:4294967295:1000:1006:1013:1021:1047:3011
-310:4294967295:1000:1006:1013:1021:1047:3011
-311:4294967295:1000:1006:1013:1021:1047:3011
-312:4294967295:1000:1006:1013:1021:1047:3011
-313:4294967295:1000:1006:1013:1021:1047:3011
-314:4294967295:1000:1006:1013:1021:1047:3011
-315:4294967295:1000:1006:1013:1021:1047:3011
-316:4294967295:1000:1006:1013:1021:1047:3011
-317:4294967295:1000:1006:1013:1021:1047:3011
-318:4294967295:1000:1006:1013:1021:1047:3011
-319:4294967295:1000:1006:1013:1021:1047:3011
-320:4294967295:1000:1006:1013:1021:1047:3011
-321:4294967295:1000:1006:1013:1021:1047:3011
-322:4294967295:1000:1006:1013:1021:1047:3011
-323:4294967295:1000:1006:1013:1021:1047:3011
-324:4294967295:1000:1006:1013:1021:1047:3011
-325:4294967295:1000:1006:1013:1021:1047:3011
-326:4294967295:1000:1006:1013:1021:1047:3011
-327:4294967295:1000:1006:1013:1021:1047:3011
-328:4294967295:1000:1006:1013:1021:1047:3011
-329:4294967295:1000:1006:1013:1021:1047:3011
-330:4294967295:1000:1006:1013:1021:1047:3011
-331:4294967295:1000:1006:1013:1021:1047:3011
-332:4294967295:1000:1006:1013:1021:1047:3011
-333:4294967295:1000:1006:1013:1021:1047:3011
-334:4294967295:1000:1006:1013:1021:1047:3011
-335:4294967295:1000:1006:1013:1021:1047:3011
-336:4294967295:1000:1006:1013:1021:1047:3011
-337:4294967295:1000:1006:1013:1021:1047:3011
-338:4294967295:1000:1006:1013:1021:1047:3011
-339:4294967295:1000:1006:1013:1021:1047:3011
-340:4294967295:1000:1006:1013:1021:1047:3011
-341:4294967295:1000:1006:1013:1021:1047:3011
-342:4294967295:1000:1006:1013:1021:1047:3011
-343:4294967295:1000:1006:1013:1021:1047:3011
-344:4294967295:1000:1006:1013:1021:1047:3011
-345:4294967295:1000:1006:1013:1021:1047:3011
-346:4294967295:1000:1006:1013:1021:1047:3011
-347:4294967295:1000:1006:1013:1021:1047:3011
-348:4294967295:1000:1006:1013:1021:1047:3011
-349:4294967295:1000:1006:1013:1021:1047:3011
-350:4294967295:1000:1006:1013:1021:1047:3011
-351:4294967295:1000:1006:1013:1021:1047:3011
-352:4294967295:1000:1006:1013:1021:1047:3011
-353:4294967295:1000:1006:1013:1021:1047:3011
-354:4294967295:1000:1006:1013:1021:1047:3011
-355:4294967295:1000:1006:1013:1021:1047:3011
-356:4294967295:1000:1006:1013:1021:1047:3011
-357:4294967295:1000:1006:1013:1021:1047:3011
-358:4294967295:1000:1006:1013:1021:1047:3011
-359:4294967295:1000:1006:1013:1021:1047:3011
-360:4294967295:1000:1006:1013:1021:1047:3011
-361:4294967295:1000:1006:1013:1021:1047:3011
-362:4294967295:1000:1006:1013:1021:1047:3011
-363:4294967295:1000:1006:1013:1021:1047:3011
-364:4294967295:1000:1006:1013:1021:1047:3011
-365:4294967295:1000:1006:1013:1021:1047:3011
-366:4294967295:1000:1006:1013:1021:1047:3011
-367:4294967295:1000:1006:1013:1021:1047:3011
-368:4294967295:1000:1006:1013:1021:1047:3011
-369:4294967295:1000:1006:1013:1021:1047:3011
-370:4294967295:1000:1006:1013:1021:1047:3011
-371:4294967295:1000:1006:1013:1021:1047:3011
-372:4294967295:1000:1006:1013:1021:1047:3011
-373:4294967295:1000:1006:1013:1021:1047:3011
-374:4294967295:1000:1006:1013:1021:1047:3011
-375:4294967295:1000:1006:1013:1021:1047:3011
-376:4294967295:1000:1006:1013:1021:1047:3011
-377:4294967295:1000:1006:1013:1021:1047:3011
-378:4294967295:1000:1006:1013:1021:1047:3011
-379:4294967295:1000:1006:1013:1021:1047:3011
-380:4294967295:1000:1006:1013:1021:1047:3011
-381:4294967295:1000:1006:1013:1021:1047:3011
-382:4294967295:1000:1006:1013:1021:1047:3011
-383:4294967295:1000:1006:1013:1021:1047:3011
-384:4294967295:1000:1006:1013:1021:1047:3011
-385:4294967295:1000:1006:1013:1021:1047:3011
-386:4294967295:1000:1006:1013:1021:1047:3011
-387:4294967295:1000:1006:1013:1021:1047:3011
-388:4294967295:1000:1006:1013:1021:1047:3011
-389:4294967295:1000:1006:1013:1021:1047:3011
-390:4294967295:1000:1006:1013:1021:1047:3011
-391:4294967295:1000:1006:1013:1021:1047:3011
-392:4294967295:1000:1006:1013:1021:1047:3011
-393:4294967295:1000:1006:1013:1021:1047:3011
-394:4294967295:1000:1006:1013:1021:1047:3011
-395:4294967295:1000:1006:1013:1021:1047:3011
-396:4294967295:1000:1006:1013:1021:1047:3011
-397:4294967295:1000:1006:1013:1021:1047:3011
-398:4294967295:1000:1006:1013:1021:1047:3011
-399:4294967295:1000:1006:1013:1021:1047:3011
-400:4294967295:1000:1006:1013:1021:1047:3011
-401:4294967295:1000:1006:1013:1021:1047:3011
-402:4294967295:1000:1006:1013:1021:1047:3011
-403:4294967295:1000:1006:1013:1021:1047:3011
-404:4294967295:1000:1006:1013:1021:1047:3011
-405:4294967295:1000:1006:1013:1021:1047:3011
-406:4294967295:1000:1006:1013:1021:1047:3011
-407:4294967295:1000:1006:1013:1021:1047:3011
-408:4294967295:1000:1006:1013:1021:1047:3011
-409:4294967295:1000:1006:1013:1021:1047:3011
-410:4294967295:1000:1006:1013:1021:1047:3011
-411:4294967295:1000:1006:1013:1021:1047:3011
-412:4294967295:1000:1006:1013:1021:1047:3011
-413:4294967295:1000:1006:1013:1021:1047:3011
-414:4294967295:1000:1006:1013:1021:1047:3011
-415:4294967295:1000:1006:1013:1021:1047:3011
-416:4294967295:1000:1006:1013:1021:1047:3011
-417:4294967295:1000:1006:1013:1021:1047:3011
-418:4294967295:1000:1006:1013:1021:1047:3011
-419:4294967295:1000:1006:1013:1021:1047:3011
-420:4294967295:1000:1006:1013:1021:1047:3011
-421:4294967295:1000:1006:1013:1021:1047:3011
-422:4294967295:1000:1006:1013:1021:1047:3011
-423:4294967295:1000:1006:1013:1021:1047:3011
-424:4294967295:1000:1006:1013:1021:1047:3011
-425:4294967295:1000:1006:1013:1021:1047:3011
-426:4294967295:1000:1006:1013:1021:1047:3011
-427:4294967295:1000:1006:1013:1021:1047:3011
-428:4294967295:1000:1006:1013:1021:1047:3011
-429:4294967295:1000:1006:1013:1021:1047:3011
-430:4294967295:1000:1006:1013:1021:1047:3011
-431:4294967295:1000:1006:1013:1021:1047:3011
-432:4294967295:1000:1006:1013:1021:1047:3011
-433:4294967295:1000:1006:1013:1021:1047:3011
-434:4294967295:1000:1006:1013:1021:1047:3011
-435:4294967295:1000:1006:1013:1021:1047:3011
-436:4294967295:1000:1006:1013:1021:1047:3011
-437:4294967295:1000:1006:1013:1021:1047:3011
-438:4294967295:1000:1006:1013:1021:1047:3011
-439:4294967295:1000:1006:1013:1021:1047:3011
-440:4294967295:1000:1006:1013:1021:1047:3011
-441:4294967295:1000:1006:1013:1021:1047:3011
-442:4294967295:1000:1006:1013:1021:1047:3011
-443:4294967295:1000:1006:1013:1021:1047:3011
-444:4294967295:1000:1006:1013:1021:1047:3011
-445:4294967295:1000:1006:1013:1021:1047:3011
-446:4294967295:1000:1006:1013:1021:1047:3011
-447:4294967295:1000:1006:1013:1021:1047:3011
-448:4294967295:1000:1006:1013:1021:1047:3011
-449:4294967295:1000:1006:1013:1021:1047:3011
-450:4294967295:1000:1006:1013:1021:1047:3011
-451:4294967295:1000:1006:1013:1021:1047:3011
-452:4294967295:1000:1006:1013:1021:1047:3011
-453:4294967295:1000:1006:1013:1021:1047:3011
-454:4294967295:1000:1006:1013:1021:1047:3011
-455:4294967295:1000:1006:1013:1021:1047:3011
-456:4294967295:1000:1006:1013:1021:1047:3011
-457:4294967295:1000:1006:1013:1021:1047:3011
-458:4294967295:1000:1006:1013:1021:1047:3011
-459:4294967295:1000:1006:1013:1021:1047:3011
-460:4294967295:1000:1006:1013:1021:1047:3011
-461:4294967295:1000:1006:1013:1021:1047:3011
-462:4294967295:1000:1006:1013:1021:1047:3011
-463:4294967295:1000:1006:1013:1021:1047:3011
-464:4294967295:1000:1006:1013:1021:1047:3011
-465:4294967295:1000:1006:1013:1021:1047:3011
-466:4294967295:1000:1006:1013:1021:1047:3011
-467:4294967295:1000:1006:1013:1021:1047:3011
-468:4294967295:1000:1006:1013:1021:1047:3011
-469:4294967295:1000:1006:1013:1021:1047:3011
-470:4294967295:1000:1006:1013:1021:1047:3011
-471:4294967295:1000:1006:1013:1021:1047:3011
-472:4294967295:1000:1006:1013:1021:1047:3011
-473:4294967295:1000:1006:1013:1021:1047:3011
-474:4294967295:1000:1006:1013:1021:1047:3011
-475:4294967295:1000:1006:1013:1021:1047:3011
-476:4294967295:1000:1006:1013:1021:1047:3011
-477:4294967295:1000:1006:1013:1021:1047:3011
-478:4294967295:1000:1006:1013:1021:1047:3011
-479:4294967295:1000:1006:1013:1021:1047:3011
... diff truncated; total lines 539
```
