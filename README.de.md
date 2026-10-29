# ODROID

[English](README.md)

Community-Ubuntu-Images, Baurezepte und Board-Unterstützung für ODROID-Systeme. Erstes Ziel ist **ODROID-U3 / Exynos4412** mit Ubuntu **26.04.1 armhf**, Linux **6.12.114-odroidu3-v1** und U-Boot **2026.10**. XU4 wird gesondert vorbereitet.

**Releasevorbereitung:** Neue Images bleiben bis zur Erststart-Abnahme und den Releaseprüfungen Kandidaten. Veröffentlichte Downloads stehen unter [Releases](https://github.com/the-ab/ODROID/releases); der [Hardwarestand](docs/HARDWARE.de.md) beschreibt tatsächlich erfolgte Prüfungen.

| Variante | Inhalt |
|---|---|
| `minimized` | Reduzierte Ubuntu-Base-Basis mit SSH, sudo, Netzwerk und Board-Unterstützung; Dokumentation bleibt minimiert. Das tatsächliche Kommando `unminimize` ist enthalten. |
| `minimal` | `ubuntu-minimal`, `ubuntu-standard`, übliche Administrationsprogramme, wiederhergestellte Dokumentation/Manpages und Shell-Vervollständigung. |

Beide Varianten starten mit Konsole und SSH. Einziges menschliches Konto: **`odroid` / `odroid`**, mit passwortgeschütztem sudo. Root-Passwort und Root-SSH sind gesperrt. Es werden keine Wartungsschlüssel, festen SSH-Hostschlüssel oder geklonten Maschinenidentitäten eingebaut. Nach der ersten Anmeldung mit `passwd` ein eigenes Passwort setzen.

Ethernet verwendet DHCP und eine stabile MAC aus der Hardwareidentität, sofern der Treiber keine permanente Adresse liefert. Root wächst beim ersten Start auf die Mediengröße. SD und eMMC-Benutzerbereich verwenden dasselbe Imageformat; für natives eMMC kann die separate boot0-Reparatur erforderlich sein.

- [Installation und erste Anmeldung](docs/INSTALL.de.md)
- [eMMC-boot0 mit Backup und Wiederherstellung reparieren](docs/EMMC-RECOVERY.de.md)
- [Lüfter: 35/45/55 °C und Stufen ändern](docs/FAN.de.md)
- [Grafik, Mesa und Desktopgrenzen](docs/GRAPHICS.de.md)
- [Bauen aus festgelegten Quellen](docs/BUILD.de.md)
- [Hardwareprüfung und Releaseanforderungen](docs/HARDWARE.de.md)

Kernel und Skripte werden mit Quellen und Lizenzen bereitgestellt. Hersteller-Bootfirmware liegt nicht in diesem Git-Repository; genaue Weitergabe-/Quellbedingungen müssen vor öffentlichen Binärreleases dokumentiert sein. Ubuntu-Pakete und Firmware behalten ihre eigenen Lizenzen. Siehe [Releaseanforderungen](docs/RELEASES.de.md).
