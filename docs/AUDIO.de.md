# Analoger U3-Ton

[English](AUDIO.md)

MAX98090-Kopfhörerausgabe auf 7.3.1-odroidu3-v1 geprüft:48 kHz,16 BitStereo, Links-/Rechtstöne als normaler `odroid`; beide Kanäle vom Nutzer ausdrücklich bestätigt. Die I2S-RX-DMA-Warnung(-19) verhinderte die Wiedergabe nicht. Mikrofon/Aufnahme sind durch diesen Ausgabetest nicht abgenommen.

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
