# U3 I2S/USB revision4

[Deutsch](README.de.md)

Release7.3.1-odroidu3-v4/package7.3.1-5 uses the unchanged signed Linux7.3.1 base and complete101-capability server profile. The full patch retains the five prior board changes and corrects optional VBUS acquisition, secondary I2S stream-specific DMA ownership/parentage and the missing MAX98090 capture route in the legacy U3 audio graph. No generic log suppression, fabricated power rail or removal of audio functionality.

The primary TX/RX channels were present on v3; its duplicate RX warning came from the unused secondary playback PCM. A real baseline capture attempt also exposed a missing backend route. Resource-logic host checks and ARM compilation precede separate native USB/playback/capture qualification. Keep the tested v3 packages and matching current-root backup as fallback. Source/configuration does not by itself accept hardware.
