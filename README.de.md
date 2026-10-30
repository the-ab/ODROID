# ODROID

[English](README.md)

Community-Ubuntu-Images, Baurezepte und Board-Unterstützung für ODROID-Systeme. Erstes Ziel ist **ODROID-U3 / Exynos4412** mit Ubuntu **26.04.1 armhf**, Linux **7.3.1-odroidu3-v3** und U-Boot **2026.10**. XU4 wird gesondert vorbereitet.

**Releasevorbereitung:** Neue Images bleiben bis zur Erststart-Abnahme und den Releaseprüfungen Kandidaten. Veröffentlichte Downloads stehen unter [Releases](https://github.com/the-ab/ODROID/releases); der [Hardwarestand](docs/HARDWARE.de.md) beschreibt tatsächlich erfolgte Prüfungen.

| Variante | Inhalt |
|---|---|
| `minimized` | Reduzierte Ubuntu-Base-Basis mit SSH, sudo, Netzwerk und Board-Unterstützung; Dokumentation bleibt minimiert. Das tatsächliche Kommando `unminimize` ist enthalten. |
| `minimal` | `ubuntu-minimal`, `ubuntu-standard`, übliche Administrationsprogramme, wiederhergestellte Dokumentation/Manpages und Shell-Vervollständigung. |

Beide Varianten starten mit Konsole und SSH. Einziges menschliches Konto: **`odroid` / `odroid`**, mit passwortgeschütztem sudo. Das Root-Passwort ist gesperrt; SSH erlaubt ab Image 1.0.1 einen vom Eigentümer in `/root/.ssh/authorized_keys` hinterlegten öffentlichen Schlüssel. Es werden keine Wartungsschlüssel, festen SSH-Hostschlüssel oder geklonten Maschinenidentitäten eingebaut. Nach der ersten Anmeldung mit `passwd` ein eigenes Passwort setzen.

Ethernet verwendet DHCP und eine stabile MAC aus der Hardwareidentität, sofern der Treiber keine permanente Adresse liefert. Beide Varianten aktivieren die automatische Netzwerk-Zeitsynchronisierung. Root wächst beim ersten Start auf die Mediengröße. SD und eMMC-Benutzerbereich verwenden dasselbe Imageformat; für natives eMMC kann die separate boot0-Reparatur erforderlich sein.

- [Installation und erste Anmeldung](docs/INSTALL.de.md)
- [eMMC-boot0 mit Backup und Wiederherstellung reparieren](docs/EMMC-RECOVERY.de.md)
- [Lüfter: 35/45/55 °C und Stufen ändern](docs/FAN.de.md)
- [Grafik, Mesa und Desktopgrenzen](docs/GRAPHICS.de.md)
- [Bauen aus festgelegten Quellen](docs/BUILD.de.md)
- [Hardwareprüfung und Releaseanforderungen](docs/HARDWARE.de.md)

Kernel und Skripte werden mit Quellen und Lizenzen bereitgestellt. Hersteller-Bootfirmware liegt nicht in diesem Git-Repository; genaue Weitergabe-/Quellbedingungen müssen vor öffentlichen Binärreleases dokumentiert sein. Ubuntu-Pakete und Firmware behalten ihre eigenen Lizenzen. Siehe [Releaseanforderungen](docs/RELEASES.de.md).

Kernelpakete und signierte APT-Updates: [Anleitung](docs/KERNEL-UPDATES.de.md).

Ein separater [Linux 7.3.1-Kandidat](boards/u3/kernel-candidates/7.3.1/README.de.md) hat native APT-/Rückfall-/Rückkehr- und Kopfhörertests bestanden. Vorhandene1.0.1-Imageartefakte bleiben unverändert. Siehe [Sicherheitsprüfung](docs/SECURITY-REVIEW.de.md) und [Audio](docs/AUDIO.de.md).

Das frische 1.0.2-Rezept verwendet das erweiterte [Serverprofil](boards/u3/kernel-candidates/7.3.1-server-v3/README.de.md) mit verbindlicher Prüfung von 101 Fähigkeiten. Native Docker-/VPN-/Firewall-/Dateidienst-/Sicherheitstests bestanden auf v2; v3- und Imageabnahme werden gesondert geführt. Frühere 6.12-/v1-Kernel sind Hardware-/Rückfallprofile und keine vollständigen Serverprofile.
