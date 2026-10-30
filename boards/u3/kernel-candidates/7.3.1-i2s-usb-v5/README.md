# U3 I2S/USB revision 5

[Deutsch](README.de.md)

Kernel `7.3.1-odroidu3-v5`, package `7.3.1-6`, retains the signed Linux 7.3.1 base and complete 101-capability server profile. The full local patch handles optional USB VBUS correctly, preserves real provider errors, requests secondary I2S DMA only for an attached stream and adds the missing capture backend. A separate Microphone widget connects MICBIAS and the actual IN12 preamp to the headset microphone endpoint; headphone playback remains separate.

The actual patched C resource logic and compiled capture graph are checked by `scripts/check-i2s-usb-resources.py --kernel-source BUILD`. ARM compilation and these checks do not replace native boot, USB, playback, capture and physical microphone acceptance. Revision 4 established the resource fixes but exposed the missing microphone source during native testing. V3 remains the tested fallback; boot0 is never changed by this package.

Native intermediate result: ADC, microphone bias and capture DAPM path are now on and produce samples. The full-duplex test exposed an unrelated false HDMI capture capability, corrected in [revision 6](../7.3.1-i2s-usb-v6/README.md). Revision 5 was not published.
