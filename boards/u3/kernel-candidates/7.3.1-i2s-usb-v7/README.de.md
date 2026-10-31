# U3-I2S/USB-Kandidat Revision 7

[English](README.md)

Kernel `7.3.1-odroidu3-v7` / Paket `7.3.1-8` behält die signierte 7.3.1-Basis, vollständige Serverkonfiguration und alle funktionalen USB-/DMA-/Aufnahme-/HDMI-Korrekturen von v6. Zurückgenommen wird nur die neu hinzugefügte Elternbeziehung des sekundären I2S-Softwaregeräts; `i2s.c` ist wieder bytegleich mit Upstream. Der DMA-Callback ermittelt das tatsächliche CPU-DAI-Gerät bereits ausdrücklich.

Damit wird eine mögliche Regression der Shutdown-/Runtime-PM-Reihenfolge geprüft: v3 bestand mehrere Warmstarts auch nach Audio; v4 und v6 zeigten Aussetzer. Die Elternbeziehung ist noch nicht als Ursache bewiesen. Wiederholte native Boot-/Audio-/USB-Abnahme vor Veröffentlichung erforderlich. Ursprüngliches Backup und v3-Pakete zur aktuellen Rootidentität behalten. Kein boot0- oder permanenter Kartenschreibzugriff.
