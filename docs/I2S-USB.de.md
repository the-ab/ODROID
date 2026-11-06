# U3-Plattformkorrekturen

[English](I2S-USB.md)

Das ausgelieferte v32-Profil behält folgende geprüfte lokale Änderungen im kanonischen `boards/u3/patches/platform.patch`. Sie werden nicht als upstream akzeptierte Korrekturen dargestellt.

- Samsung I2S fordert nur die DMA-Richtungen der jeweiligen primären/sekundären Schnittstelle an. Der U3-Capture-Graph benennt den primären Endpunkt und erhält die Wiedergabe-/Aufnahmezuständigkeit.
- Der HDMI-DAI bietet nur Wiedergabe an. Optionale USB-VBUS-Regulatoren reichen echte Provider-/Defer-Fehler weiter und akzeptieren eine fehlende optionale Versorgung; USB-Reset und Leistungsgrenzen bleiben erhalten.
- MMC-Spannungsauswahl lehnt umgekehrte Bereiche ab und reicht fehlgeschlagene Abfragen unterstützter Spannungen vor der Regulator-API weiter. Dies korrigiert einen sekundären Fehlerpfad und belegt MMC nicht als Ursache des ursprünglichen Stillstands.
- Der nicht gebankte GIC-Zugriff wählt seine CPU-spezifische Registerbasis über den initialisierten RAM-Schlüsselzähler. Fehlversuche erfassten eine falsche ursprüngliche Basis-/Bereichsauswahl; gesunde Alias-/Fremd-CPU-Gegenproben wurden getrennt geprüft. Der genaue Textpatch-/Cachemechanismus bleibt unbewiesen. Keine spekulativen IRQ-Masken, Secure-/Debug-Freischaltungen oder geratenen MMIO-Schreibzugriffe werden verwendet.
- Drei TUN-Statistikabschnitte im Prozesskontext schließen Softirq-Schreiber aus. Lockdep bleibt aktiviert; OpenVPN/TUN und die vollständige Serverregression bestanden anschließend.

Der abschließende v32-Kernel bestand zehn reine Warmstarts und fünf kontrollierte Halt-/Kaltstarts mit normalen Argumenten. Jeder Start prüfte vier fortschreitende CPU-Timer, 351 Modulhashes, Boot-/Konfigurationsdateien und Systemzustand. Vollständige Servertests, normales unprivilegiertes io_uring, Ethernettransfer und interne Stereo-Codec-Schleife bestanden ohne neue Kernelwarnungen. Frühere I2S-RX-DMA- und fehlende optionale VBUS-Warnungen treten nicht mehr auf.

Physische Headset-Wiedergabe wurde an früheren Revisionen bestätigt; physischer Mikrofoneingang bleibt offen. Boot0, Boot1 und EXT_CSD wurden durch diese Kernelkorrekturen nicht verändert. Treiber und begrenzte Tests bestätigen weder sämtliche Peripherie noch Langzeitbetrieb. Siehe [Hardware](HARDWARE.de.md), [Audio](AUDIO.de.md) und [Sicherheit](SECURITY-REVIEW.de.md).

Überholte Versuchsprofile wurden aus dem aktuellen Quellbaum entfernt. Die [Git-Historie](https://github.com/the-ab/ODROID/commits/main/) erhält Untersuchung und passende Quellen; der kanonische Patch behält den Code der ausgelieferten Binärdatei. UART-Diagnose für neue Untersuchungen benötigt die 1,8-V-Schnittstelle und geprüfte Steckerorientierung. Siehe [Hardkernel-U3-Spezifikation](https://www.hardkernel.com/shop/odroid-u3/).
