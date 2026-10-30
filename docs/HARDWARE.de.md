# U3-Hardwareprüfung

[English](HARDWARE.md)

Quell-/Konfigurationsunterstützung, Betrieb des Prototyps und Abnahme eines neuen Images sind getrennte Aussagen. Am 30.10.2026 startete **minimal v1.0.0 und v1.0.1** nativ von einer 16-GB-eMMC mit **6.12.114-odroidu3-v1**. Defaultlogin odroid und sudo, Root-Vergrößerung, stabile Ethernetidentität, Netzwerkzeit, Lüfterstufen, Bootdatei-Prüfsummen und exakte Paketstände wurden geprüft. Keine Journalfehler oder fehlgeschlagenen Dienste. Minimized und SD-Start der neuen Images bleiben getrennt offen.

| Komponente | Nachweis / Grenze |
|---|---|
| SD und natives eMMC | Minimal v1.0.0 und v1.0.1 haben nativen eMMC-Erststart und Basisprüfung bestanden. Frühere Prototypen starteten von SD/eMMC; boot0-Reparatur auf zwei 16-GB-SDW16G-Modulen abgenommen. Normales Leser-Schreiben erfasst nur den Benutzerbereich. |
| CPU/RAM/Speicher/Netzwerk | Frühere Prototyp-Stabilitätsprüfung mit CPU-/Speicherlast, Speichermustern, Datei-Schreib-/Direktlese-Prüfsummen und Netztransfer bestanden. Grafiktests ersetzen diese Prüfung nicht. |
| Ethernetidentität | Hardware-MAC blieb über SD/eMMC stabil. Eine vom Treiber gelieferte permanente Adresse hat Vorrang. |
| Lüfter/Thermik/Taster | Alle vier Lüfterstufen beobachtet; einstellbare eigene Trips 35/45/55 °C, CPU-Schutz erhalten; sauberes Herunterfahren per Taster bestätigt. |
| Pincontroller | Aufräumen verbrauchter Wakeup-IRQ-fwnode-Links beseitigte den vorherigen Device-Link-Fehler bei realen SD-/eMMC-Starts. |
| Mali/HDMI/X11/Wayland | Siehe [Grafik](GRAPHICS.de.md). Angeschlossenes HDMI bei 1080p60 mit Xorg und nativem Weston DRM/GL einschließlich Sichtabnahme durch den Nutzer bestätigt. Neue v1-Images und vollständige Desktopumgebungen behalten eigene Abnahme. |
| USB, Eingabe, GPIO/I²C/SPI, RTC | Treiber aktiviert. Bestätigt sind nur tatsächlich genutzte USB-/Netz-/Eingabepfade, keine pauschale Peripherieabnahme. |
| MAX98090-Audio / Samsung-MFC-Video | Kernelunterstützung und MFC-Firmware enthalten; Audioausgabe und Hardwaredekodierung nicht geprüft. |
| XU4 | Vorgemerkt, noch kein Image oder Hardwarenachweis. |

Lokale Kerneländerungen sind keine als upstream-übernommen bezeichneten Fixes: Hardwareseriennummer, eigene Lüfter-Trips/ungeeignete OPP ausblenden, EHCI-PHY-Lebenszyklus, DWC2-Hardwarevorgaben sowie Wakeup-IRQ-Linkbereinigung/Diagnose. Der v1-DTB ist bytegleich mit dem zuvor getesteten DTB. Minimal hat inzwischen native eMMC-Basisprüfungen bestanden; dies wird nicht pauschal auf jede Variante, jeden Startweg oder jede Peripherie übertragen.

Images enthalten keine persönliche feste MAC, Hostschlüssel oder Wartungs-Authorized-Keys. Dasselbe Image leitet auf einem anderen U3 dessen Identität ab. Die MAC-Ableitung ist ein deterministischer Ersatzweg, keine Behauptung einer programmierten Werksadresse im LAN-EEPROM.

Der minimal-Erststart protokollierte bekannte Plattform-/Lockdep- und fehlende optionale Kamerasensor-Meldungen sowie die nicht gesetzte optionale Cron-Variable `EXTRA_OPTS`. Cron lief mit Resultat success; der Pincontroller-Device-Link-Fehler trat nicht erneut auf. Der Cron-Hinweis ist für eine spätere Rezeptkorrektur erfasst.

Die native eMMC-Nachprüfung von Minimal 1.0.1 bestand ebenfalls: eigener Root-Public-Key vom Nutzer hinterlegt, Login bestätigt und mit SSH-Journal abgeglichen; die ausgelieferte Schlüsselregel wirkte ohne lokalen Override, das Root-Passwort blieb gesperrt. Kernel-/Meta-/Werkzeug-/Keyringpakete, sämtliche Modul-/Payload-/Bootdatei-Prüfsummen und das vollständige Image-Paketmanifest stimmten überein. Board-/Medien-/Payload-Zulässigkeitsprüfungen bestanden ohne Aktivierung. Die konfigurierte APT-Adresse war vom Board erreichbar; ihre geladene Signatur wurde gegen den bytegleichen installierten Archivschlüssel geprüft. Listen derzeit leer. Keine Live-Cacheaktualisierung, Paketaktualisierung oder Konfigurationsänderung vorgenommen; ein echter Kernelwechsel mit Neustart bleibt offen.

Linux 7.3.1-odroidu3-v1 bestand echte signierte APT-Installation, nativen eMMC-Start, Rückfall/Start auf 6.12.114 und Rückkehr/Start auf 7.3.1. Netzwerk/MAC/Zeit/Lüfter/Speicher, Paketdateien, keine failedUnits/Journalfehler und Taint 0 geprüft. Kurzer 4-Kern-/128 MiB-/32 MiB-fsync-Test bestanden, maximal 71 °C. Analoge MAX98090-Kopfhörer mit 48 kHz Stereo vom Nutzer auf beiden Kanälen als hörbar bestätigt. Aufnahme/Mikrofon, GPU-Rendering und vollständige Peripherie bleiben getrennt. Neue I2S-RX-DMA-Warnung(-19) und PFKEY-Abkündigung erfasst; Wiedergabe funktionierte trotz RX-Warnung. Siehe [Audio](AUDIO.de.md) und [Sicherheitsprüfung](SECURITY-REVIEW.de.md).
