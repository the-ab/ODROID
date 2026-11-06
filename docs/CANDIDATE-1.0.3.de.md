# U3-Image 1.0.3 – Prüfstand

[English](CANDIDATE-1.0.3.md)

Ubuntu 26.04.1 armhf; Kernel `7.3.1-odroidu3-v32`, DEB `7.3.1-33`, Aktivierungswerkzeuge `1.0.3`. Ursprüngliches Kompilier-/Paketrezept: `b8ce206a44451aa64452add634a3e6376b60d6be`. Bereinigte Quellen behalten identische kanonische Kernelkonfiguration, wirksamen Patch und paketierte Laufzeitskripte; überholte Versuchsprofile verbleiben nur in der Historie.

| Variante | Genaues IMG-SHA256 |
|---|---|
| minimized | `9315325dca3de5de9afa393b259020dedf2ebe2232be250be87680de458e6d0f` |
| minimal | `98160d764b5e5fa6f022c1d06df63c49893a42f29c152d66494dacb4fa19ee26` |

Das ZIP kann mit aktueller Dokumentation neu gepackt werden, ohne diese IMG-Bytes zu verändern. Maßgeblich ist seine `.sha256`-Datei; frühere ZIP-Prüfsummen sind nicht austauschbar. Vollständige Image-ZIPs bleiben Entwürfe, bis die Weitergabe-/Quellbedingungen der Bootfirmware belegt sind.

Dieselben kompilierten Kernel-/DTB-/Modulbytes bestanden zehn reine Warmstarts und fünf kontrollierte Halt-/Kaltstarts auf der vorherigen 1.0.2-Testinstallation. Neun Funktionsfälle (Docker, VPN/Firewall, Dateien, Sicherheit, Module, begrenzte Last, interne Stereoschleife, normales unprivilegiertes io_uring, reales Ethernet) und zwei abschließende Zustands-/Rückleseprüfungen bestanden. Jeder Start bestätigte vier CPU-Timer und alle 351 Module. Lockdep blieb aktiv; keine neuen Kernelwarnungen, fehlgeschlagenen Dienste oder Auditverluste blieben zurück. NFS verwendete per Journal bestätigtes nfsdcld-Tracking. Ethernet prüfte je 16 MiB in beide Richtungen. Eigene Testdateien wurden entfernt.

Beide frisch gebauten Varianten bestanden ARM-Login/PAM, passwortgeschütztes sudo, Root-Schlüsselrichtlinie, ausschließlich das menschliche Standardkonto, Ausschluss von Wartungs-/Hostschlüsseln und kopierter Identität, numerische Besitzrechte ohne geerbte Host-ACLs, systemd-/Netzwerk-/Zeit-/Sicherheitsreihenfolge, signierte APT-Konfiguration, vollständige Dateisystem-/Partitions-/Boot-Rückleseprüfung und ZIP-CRC-/IMG-Prüfung.

**Physischer Erststart:** Der Besitzer schrieb das genaue Minimal-IMG auf natives eMMC. Vollständige installierte Paketliste, 351 Modul-/Payload-/Boot-/Konfigurationshashes, Rootvergrößerung, Standardzugang, selbst hinterlegter Rootschlüssel, DHCP-Identität, NTP, Lüfter, AppArmor/Audit, CPU-Timer, Journal und Dienste bestanden. Der Besitzer meldete einen erfolgreichen Warmstart. Neue Minimized-/SD-Erststarts bleiben offen. Die neue Installation enthält nur v32; historische Rückfallsicherungen sind kein vorinstallierter Rückfall für frisch beschriebene Medien.

Passende vollständige Linux-/U-Boot-Quellarchive, geprüfte Konfiguration, Patches, Rezepte und Lizenzen begleiten das Kernel-Quellrelease als `odroid-u3-v1.0.3-corresponding-sources.zip`. Das Manifest ordnet den ursprünglichen Paketstand den bereinigten Quellen zu. Identische spätere Ubuntu-Paketbauten werden wegen beweglicher APT-Inhalte nicht zugesagt. Aktuelle physische HDMI-/Desktop-/Mikrofonprüfung, ungenutzte externe Peripherie und Langzeitzuverlässigkeit werden daraus nicht abgeleitet. Siehe [Veröffentlichungsbedingungen](RELEASES.de.md).
