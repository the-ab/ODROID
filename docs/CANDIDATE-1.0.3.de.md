# Lokale U3-Imagekandidaten 1.0.3

[English](CANDIDATE-1.0.3.md)

Beide frisch gebauten Ubuntu 26.04.1-armhf-Varianten bestehen die lokalen Prüfungen. Rezept-/Paketquelle: `b8ce206a44451aa64452add634a3e6376b60d6be`. Kernel `7.3.1-odroidu3-v32`, Paket `7.3.1-33`, Aktivierungswerkzeuge `1.0.3`. Lokale Kandidaten, keine neue öffentliche Binär-/APT-/Main-Promotion.

| Variante | ZIP-Bytes | ZIP-SHA256 |
|---|---:|---|
| minimized | 143727324 | `cdb5ee3e75f01f2c16c2910a26c12c8b76c0935963005572b8938761bcb2e8b2` |
| minimal | 188176108 | `559f2ee46272ea2af0509600f7c92ce143743780786318927cd65c698ed449ec` |

Native Kernelprüfung auf der bisherigen Ubuntu 1.0.2-Testinstallation: zehn reine Warmstarts und fünf kontrollierte Halt-Kaltstarts mit normalen Parametern, vier wachsenden CPU-Timern, 351 passenden Modulen und aktivem Lockdep. Neun Funktionsfälle (Docker, VPN/Firewall, Dateien, Sicherheit, Module, begrenzte Last, interner Stereo-Loop, normale unprivilegierte io_uring-Aufrufe, echtes Ethernet) und zwei abschließende Gesundheits-/Rücklesefälle bestanden. Ethernet übertrug 16 MiB je Richtung; NFS verwendete im Journal bestätigtes nfsdcld-Tracking. Keine neuen Kernelwarnungen, fehlgeschlagenen Dienste, verlorenen Auditereignisse oder Änderungen der LAN-Firewall. Eigene Testdaten entfernt.

Abschlusspakete lokal installiert: geprüfte Kernel-/DTB-/Modulbytes, Bootdateien und Auswahlzustand unverändert, kein Neustart notwendig. V25 bleibt direkter Rückfall, v17 zusätzliche Reserve.

Jedes frische Image besteht ARM-Login/PAM, passwortgeschütztes sudo, Root-Schlüsselrichtlinie für selbst hinterlegte Schlüssel, einziges menschliches Standardkonto, Abwesenheit von Wartungs-/Hostschlüsseln und geklonter Identität, numerische Rechte ohne Host-ACLs, Systemd-/Netzwerk-/Zeit-/Sicherheitsreihenfolge, signierte APT-Quelle, vollständige Dateisystem-/Partitions-/Bootrückleseprüfung und ZIP-CRC/IMG-Hash-Roundtrip. Standardkonto odroid/odroid; eMMC-Werkzeug/Prefix/ausführliche Anleitungen und einstellbare 35/45/55°C-Lüftersteuerung enthalten.

Passende Originalquellen von Linux/U-Boot, geprüfte Konfiguration, Patches, Rezepte und Lizenzen stehen in `odroid-u3-v1.0.3-sources.zip` (SHA256 `c76fca8b28ce2b105d354172aafcbc037bdfb4ac6b08678cc2f35b8aa2c9e3de`). Eingänge sind hashgebunden; bytegleiche Nachbauten gegen später veränderte Ubuntu-Paketquellen werden nicht zugesagt.

Offen: physische Erststarts genau dieser ZIPs für jede zugesagte Variante/Medienart, genaue BL1-/BL2-/TrustZone-Weitergabe-/Quellbedingungen und ausdrückliche Veröffentlichungsfreigabe. Diese neuen Images wurden noch nicht physisch gebootet. Aktuelle physische HDMI-/Desktop-/Mikrofonabnahme, ungenutzte externe Peripherie und Langzeitzuverlässigkeit werden nicht abgeleitet. Der geprüfte Kernel läuft weiter; keine Firmwareänderung.
