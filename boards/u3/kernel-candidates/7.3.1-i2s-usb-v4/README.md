# U3 I2S/USB intermediate revision 4

[Deutsch](README.de.md)

Kernel `7.3.1-odroidu3-v4`, package `7.3.1-5`, uses signed Linux 7.3.1 and the unchanged 101-capability server configuration. Native eMMC testing removed the optional-VBUS dummy-regulator and duplicate I2S RX-channel warnings. USB Ethernet transferred 16 MiB each way with verified SHA256; headphone playback was accepted on both sides.

Adding the capture backend made ALSA capture open, but samples were all zero. DAPM inspection proved the legacy board represented the microphone as a headphone sink and connected IN1 while the selected microphone preamp consumes IN12; ADC/bias stayed off. This intermediate revision was not published. Continue with [revision 5](../7.3.1-i2s-usb-v5/README.md). Its exact source profile and test package are retained for traceability.
