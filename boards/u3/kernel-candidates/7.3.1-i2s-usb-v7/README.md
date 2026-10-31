# U3 I2S/USB revision 7 candidate

[Deutsch](README.de.md)

Kernel `7.3.1-odroidu3-v7` / package `7.3.1-8` retains the signed 7.3.1 base, complete server configuration and all functional v6 USB/DMA/capture/HDMI fixes. It removes only the newly introduced parent relationship of the software secondary I2S device; `i2s.c` is byte-identical to upstream again. The DMA callback already resolves the actual CPU-DAI device explicitly.

This tests a possible shutdown/runtime-PM ordering regression: v3 passed repeated warm starts, including after audio; v4 and v6 showed failures. The parent relationship is not yet established as their cause. Native repeated boot/audio/USB qualification is required before promotion. Keep the original current-root v3 backup and packages. No boot0 or permanent card setting is changed.

Native result: initial boot, 48 kHz digital full duplex, playback and USB Ethernet integrity passed. The first v7 self-restart returned with a GIC CPU-mask error; the second hung and required a power cycle. Thus reverting the parent relationship is insufficient. V7 is not qualified for release; preserve v3 and the verified backup. See [the investigation](../../../../docs/I2S-USB.md).
