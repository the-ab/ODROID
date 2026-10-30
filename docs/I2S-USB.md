# U3 I2S and USB investigation

[Deutsch](I2S-USB.de.md)

The pinned [revision 6 candidate](../boards/u3/kernel-candidates/7.3.1-i2s-usb-v6/README.md) uses Linux `7.3.1-odroidu3-v6` / DEB `7.3.1-7`. It has not been promoted to the public APT channel or image default. The published v3 packages and immutable 1.0.2 images remain unchanged.

The USB PHY binding makes `vbus-supply` optional, while the driver used mandatory regulator acquisition. The patch requests an optional supply, accepts only ENODEV as absence and propagates real errors/probe deferral. It adds no fake regulator and does not join the shared PHY to the independently switched OTG power rail. Native USB Ethernet, hub and HID enumeration work; a 16 MiB transfer in each direction on the USB Ethernet path had matching SHA256 and zero interface RX/TX errors. Six RX-drop counter increments occurred during that run; they are not presented as zero packet drops. No unused USB storage device or OTG host/device role is blanket-qualified.

The primary I2S TX and RX channels already existed. A software secondary playback PCM eagerly requested the primary RX channel again. The wrapper now requests only an attached stream using its actual CPU DAI DMA name, and the secondary device has its controller as parent. Primary/legacy paths remain; secondary functionality is not disabled to hide a warning. Native DMA debug state shows the primary TX/RX owners and no duplicate allocation.

Real capture testing revealed two additional legacy DT defects: a missing capture-backend route, and a microphone wired to a headphone sink/IN1 instead of a microphone source and the selected IN12 preamp. A distinct Mic Jack widget connects MICBIAS and IN12 to the capture graph. DAPM now powers the microphone bias, preamp, ADCs and I2S capture while recording.

The Exynos HDMI transmitter also advertised capture by default. On the shared multi-codec backend, that fictitious stream occupied hdmi-codec's single-stream reservation and rejected analog full duplex. `no_i2s_capture` now describes the actual transmitter capability. Native internal codec loopback at 48 kHz/S16 stereo returned the exact separate 400 Hz/600 Hz channels, over 99.9999% reference-tone energy and negligible cross-channel energy. Headphone playback on v6 was accepted on both sides. An unverified headset produced only a very small analog capture level; physical microphone speech acceptance remains open.

Resource checks execute the actual changed C wrapper/regulator branch with host API stubs, inspect the compiled DT capture graph and verify the HDMI capability. ARM compilation, the unchanged 101-capability server gate, 23 package/boot protection tests and source comparison are separate evidence. All 95,979 upstream regular files were compared: 95,970 unchanged, exactly nine documented modified files. The complete config differs from v3 only in LOCALVERSION.

A warm restart into v6 did not return, with a steady blue LED/black HDMI. The same unchanged payload subsequently booted after a power cycle with no journal errors, failed units or taint. The prior journal reached clean userspace shutdown; it does not identify the stage after logging stopped. Warm-start qualification is still open and blocks release promotion. This is not evidence for reflashing boot0, which remained byte-identical.

References: [optional regulator API](https://docs.kernel.org/driver-api/regulator.html), the exact upstream binding/driver files included in matching Linux sources, and the local full patches. These are local reviewed fixes, not claimed to be accepted upstream.

Follow-up: a second v6 warm restart also failed after one intervening successful warm restart. Two power cycles recovered the unchanged v6 payload. Hardware reset is already permanently enabled (`RST_N_FUNCTION=0x01`), pwrseq_emmc is bound and the active-low reset GPIO is correctly owned/high. No EXT_CSD settings were changed. A controlled comparison with the retained v3 kernel is prepared; the reset/early-boot cause remains unproved.
