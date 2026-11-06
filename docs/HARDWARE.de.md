# U3-Hardwareprüfung

[English](HARDWARE.md)

Stand: 6. November 2026. Kernel `7.3.1-odroidu3-v32`, Paket `7.3.1-33`, Werkzeuge `1.0.3`. Quellunterstützung, Kernelqualifikation und Erststart eines neuen Images sind getrennte Aussagen.

| Komponente | Nachweis / Grenze |
|---|---|
| Natives eMMC / Start | Der qualifizierte Kernel bestand zehn reine Warmstarts und fünf kontrollierte Halt-/Kaltstarts mit normalen Argumenten. Jeder Start prüfte vier fortschreitende CPU-Timer, 351 Modulhashes, Boot-/Konfigurationsdateien, Lockdep, Audit, Dienste und Journal. Frisches Minimal 1.0.3 bestand zusätzlich die native eMMC-Basisprüfung; der Besitzer meldete einen erfolgreichen Warmstart. |
| Neue Imagevarianten | Beide Varianten bestanden ARM-/Rootfs-, Dateisystem-, vollständige Partitions-/Boot-Rücklese- und ZIP-Prüfungen. Minimized- und SD-Erststarts sind noch nicht bestätigt. Frühere SD-Prototypen belegen diese Dateien nicht. |
| Serverfunktionen | Docker, WireGuard, OpenVPN/TUN, IPv4-/IPv6-Firewall, Samba/CIFS, NFS4.2, SSHFS, Sicherheitsschnittstellen, Module, begrenzte Last, normales unprivilegiertes io_uring und je 16 MiB Ethernettransfer bestanden. Siehe [Serverumfang](SERVER-KERNEL.de.md). |
| Ethernet / Zeit | DHCP, stabile hardwareabgeleitete Ersatz-MAC und NTP bestanden. Eine permanente Treiberadresse hat Vorrang. Keine persönliche MAC wird ausgeliefert. |
| Lüfter / Temperatur / Taster | Vier Lüfterzustände geprüft; eigene einstellbare 35/45/55-°C-Schwellen, CPU-Schutz bleibt erhalten. Sauberes Herunterfahren per Taster wurde an früheren Images bestätigt. Siehe [Lüfter](FAN.de.md). |
| Pincontroller | Korrektur des bereits verbrauchten Wakeup-IRQ-Gerätelinks bestätigt; der frühere Linkfehler trat nicht erneut auf. |
| Audio | Aktuelle interne Stereo-Codec-Schleife bestanden. Kopfhörerausgabe wurde an früheren Kerneln physisch bestätigt. Aktueller Mikrofoneingang ist nicht abgenommen. Siehe [Audio](AUDIO.de.md). |
| Mali / HDMI / X11 / Wayland | Frühere 1080p60-Xorg-/Weston- und Shaderprüfungen bestanden, einschließlich Sichtkontrolle. Aktuelle physische v32-Ausgabe und vollständiger Desktop sind nicht neu abgenommen. Siehe [Grafik](GRAPHICS.de.md). |
| USB / GPIO / I²C / SPI / RTC | Treiber aktiviert, nur tatsächlich geprüfte Pfade bestätigt. USB-Hostreset beim Neustart ist vorgesehen; eine Spannungsunterbrechung externer Geräte wurde nicht gemessen. |
| Samsung MFC | Treiber und lizenzierte Firmware enthalten; Hardware-Videodekodierung nicht abgenommen. |
| XU4 | Geplant; U3-Bootoffsets und Abnahmen gelten nicht für XU4. |

Frisches Minimal 1.0.3 entsprach der vollständigen ausgelieferten Paketliste und allen Kernel-/Modul-/Boot-/Konfigurationshashes. Rootvergrößerung, Standardlogin/sudo, selbst ergänzter Root-Schlüsselzugang, DHCP-Identität, NTP, Lüfter, AppArmor/Audit, vier CPU-Timer sowie fehlerfreie Dienste und Journal bestanden. Das Image enthält keinen Wartungsschlüssel. Ein frisch geschriebenes Image enthält nur seinen ausgelieferten Kernel; vor weiteren Kernelversuchen eine zum Medium passende Sicherung anlegen.

Die begrenzten Prüfungen bestätigen weder Langzeitzuverlässigkeit noch sämtliche Peripherie. Lokale Patches werden nicht als upstream akzeptiert dargestellt. Die vollständigen Quellen behalten den in der geprüften Binärdatei enthaltenen inaktiven Diagnosecode; seine Aktivierung verändert die Prüfbedingungen.
