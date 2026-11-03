# Interrupt- und Idle-Fortschritt, Revision 17

[English](README.md)

Das private `7.3.1-odroidu3-v17` erweitert die begrenzte RAM-Diagnose aus [v16](../7.3.1-a9-errata-v16/README.de.md). v16 bestand vier aufeinanderfolgende Warmstarts mit demselben Kernel; der fünfte scheiterte. Die letzten I²C-IRQ-Marker zeigen die Rückkehr des Handlers, belegen aber nicht den späteren Befehlszähler von CPU0. Die Errata-Optionen allein beheben den Hänger nicht.

Sieben Kanäle je CPU erscheinen in `odroid-u3-i2c-progress` und den begrenzten RCU-/Softlockup-Momentaufnahmen. Die bisherigen Kanäle 0–3 bleiben kompatibel. Kanal 4 trennt I²C-MMIO-/Abschlussmarker im Prozesskontext vom IRQ-Kanal 2. Kanal 5 erfasst den allgemeinen GIC-Pfad: 10 vor dem IAR-Lesen, 11 danach, 12 vor dem Dispatch, 13 danach, 14 bei ungültigem Interrupt und 15 bei Handler-Rückkehr. Kanal 6 erfasst Eintritt (1) und Rückkehr (2) des ARM-Idle-Pfades. Transferkanal 3 ergänzt Grenzen für Set-Master, Nachrichtenstart, Abschlusswarten, Wait-Idle und Aufräumen (10–19).

Ergänzt werden RAM-Schreibzugriffe um vorhandene Operationen. Die ursprünglichen MMIO-Zugriffe, IRQ-Bestätigungs-/EOI-Logik, Wartevorgänge und Idle-Aufrufe bleiben erhalten. Keine neuen Registerzugriffe, Timer, Sperren, CPU-übergreifenden Anfragen oder Hardware-Workarounds. Die drei Cortex-A9-Errata-Optionen und alle 101 Serverkriterien bleiben aktiviert; in der Konfiguration ändert sich nur der Versionssuffix. Der DTB ist bytegleich v16. Die Diagnose kann das Timing beeinflussen; die Marker sind Näherungen und keine atomare CPU-Momentaufnahme.

Der kumulative Patch lässt sich auf 13 ursprüngliche Quelldateien anwenden. Entfernt man ausschließlich die neuen Marker, erhält man den veränderten v16-Code exakt zurück. Quell-, Bau- und Paketprüfung bleiben von der Hardwareabnahme getrennt. Passende Debug-ELF-, Paket- und UART-Nachweise erhalten. Dieser Diagnosekandidat ändert nicht die Imagevorgabe und darf nicht als abgenommene Korrektur veröffentlicht werden.
