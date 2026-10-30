# U3-Hardwareprüfung

[English](HARDWARE.md)

Quell-/Konfigurationsunterstützung, Betrieb des Prototyps und Abnahme eines neuen Images sind getrennte Aussagen. Die aktuellen v1-Kandidaten wurden noch nicht physisch gestartet. Der Kernel-Patchsatz lief im vorausgehenden 6.12.114-Prototyp.

| Komponente | Nachweis / Grenze |
|---|---|
| SD und natives eMMC | Prototyp auf beiden Wegen gestartet; boot0-Reparatur auf zwei 16-GB-SDW16G-Modulen nativ abgenommen. Normales Leser-Schreiben erfasst nur den Benutzerbereich. |
| CPU/RAM/Speicher/Netzwerk | Frühere Prototyp-Stabilitätsprüfung mit CPU-/Speicherlast, Speichermustern, Datei-Schreib-/Direktlese-Prüfsummen und Netztransfer bestanden. Grafiktests ersetzen diese Prüfung nicht. |
| Ethernetidentität | Hardware-MAC blieb über SD/eMMC stabil. Eine vom Treiber gelieferte permanente Adresse hat Vorrang. |
| Lüfter/Thermik/Taster | Alle vier Lüfterstufen beobachtet; einstellbare eigene Trips 35/45/55 °C, CPU-Schutz erhalten; sauberes Herunterfahren per Taster bestätigt. |
| Pincontroller | Aufräumen verbrauchter Wakeup-IRQ-fwnode-Links beseitigte den vorherigen Device-Link-Fehler bei realen SD-/eMMC-Starts. |
| Mali/HDMI/X11/Wayland | Siehe [Grafik](GRAPHICS.de.md). Angeschlossenes HDMI bei 1080p60 mit Xorg und nativem Weston DRM/GL einschließlich Sichtabnahme durch den Nutzer bestätigt. Neue v1-Images und vollständige Desktopumgebungen behalten eigene Abnahme. |
| USB, Eingabe, GPIO/I²C/SPI, RTC | Treiber aktiviert. Bestätigt sind nur tatsächlich genutzte USB-/Netz-/Eingabepfade, keine pauschale Peripherieabnahme. |
| MAX98090-Audio / Samsung-MFC-Video | Kernelunterstützung und MFC-Firmware enthalten; Audioausgabe und Hardwaredekodierung nicht geprüft. |
| XU4 | Vorgemerkt, noch kein Image oder Hardwarenachweis. |

Lokale Kerneländerungen sind keine als upstream-übernommen bezeichneten Fixes: Hardwareseriennummer, eigene Lüfter-Trips/ungeeignete OPP ausblenden, EHCI-PHY-Lebenszyklus, DWC2-Hardwarevorgaben sowie Wakeup-IRQ-Linkbereinigung/Diagnose. Der v1-DTB ist bytegleich mit dem zuvor getesteten DTB. Neu gebauter Kernel und frische Rootfs benötigen dennoch eigene Startprüfungen.

Images enthalten keine persönliche feste MAC, Hostschlüssel oder Wartungs-Authorized-Keys. Dasselbe Image leitet auf einem anderen U3 dessen Identität ab. Die MAC-Ableitung ist ein deterministischer Ersatzweg, keine Behauptung einer programmierten Werksadresse im LAN-EEPROM.
