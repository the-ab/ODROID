# Analoger U3-Ton

[English](AUDIO.md)

Der U3 verwendet den MAX98090-Codec. Frühere Kernel bestanden physische 48-kHz-/S16-Stereo-Kopfhörerprüfung mit beiden hörbar bestätigten Kanälen. Die aktuelle interne v32-Stereoschleife bestand; die frühere I2S-RX-DMA-Warnung ist korrigiert. Physische Sprachaufnahme und aktuelle v32-Hörprüfung bleiben getrennte Abnahmen.

Das SSH-Image benötigt keinen Desktop-Audioserver. ALSA-Werkzeuge bei Bedarf installieren:

```sh
sudo apt update
sudo apt install alsa-utils
aplay -l
amixer -c 0 sget Headphone
sudo alsactl --no-ucm -f /pfad/zu/vorher.state store 0
amixer -c 0 -- sset Headphone -20dB
```

`--` vor dem Befehl verhindert, dass ein negativer dB-Wert als Option gelesen wird. Mit einer leisen Datei über `aplay -D plughw:0,0 DATEI.wav` testen, nicht bei maximalem Pegel starten. Geprüft wurden `MIXHPLSEL Mux`/`MIXHPRSEL Mux` auf `DAC Only` und aktivierte linke/rechte Kopfhörerschalter. `odroid` ist bereits in der Audiogruppe. `alsactl --no-ucm` sichert/restauriert direkte Mixerregler ohne Board-UCM-Profil. Desktop-PipeWire/PulseAudio, Mikrofonrouting und andere Geräte bleiben eigene Prüfungen. Testeinstellungen anschließend zurückgestellt, funktionierenden Snapshot privat aufbewahrt.

Die [Plattformkorrekturen](I2S-USB.de.md) beschreiben richtungsspezifische DMA-Anforderungen und den Aufnahmegraphen. Interner Vollduplex bestätigt weder ein angeschlossenes Headset-Mikrofon noch dessen Verdrahtung oder den externen Analogeingang.
