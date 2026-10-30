# U3 I2S/USB revision 6

[Deutsch](README.de.md)

Kernel `7.3.1-odroidu3-v6`, package `7.3.1-7`, retains the signed Linux 7.3.1 base and complete 101-capability server profile. The full local patch handles optional USB VBUS correctly, preserves real provider errors, requests secondary I2S DMA only for an attached stream and adds the missing capture backend. A separate Microphone widget connects MICBIAS and the actual IN12 preamp to the headset microphone endpoint; headphone playback remains separate.

The actual patched C resource logic and compiled capture graph are checked by `scripts/check-i2s-usb-resources.py --kernel-source BUILD`. ARM compilation and these checks do not replace native boot, USB, playback, capture and physical microphone acceptance. Revision 4 established the resource fixes but exposed the missing microphone source during native testing. V3 remains the tested fallback; boot0 is never changed by this package.

Exynos HDMI now advertises its actual playback-only capability, so a shared multi-codec backend cannot reserve a fictitious HDMI capture stream and block analog full duplex. Native qualification of this exact revision is still required.
