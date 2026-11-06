# ODROID

[English](README.md)

Community-Images, Kernelpakete und Baurezepte für **ODROID-U3 / Exynos4412**. Das aktuelle Rezept verwendet **Ubuntu 26.04.1 armhf, Image 1.0.3**, **Linux 7.3.1-odroidu3-v32** (Paket `7.3.1-33`) und U-Boot 2026.10. XU4-Unterstützung ist separat geplant.

[Kernelpakete und passende Quellen](https://github.com/the-ab/ODROID/releases/tag/u3-kernel-7.3.1-33) · [Signiertes APT-Repository](https://the-ab.github.io/deb/) · [Installation](docs/INSTALL.de.md)

**Image-Downloads:** Die vollständigen 1.0.3-Image-ZIPs bleiben unveröffentlicht, solange die genauen Weitergabe- und Quellbedingungen für Samsung-/Hardkernel-BL1, BL2 und TrustZone ungeklärt sind. Die separat angebotenen Kernelpakete enthalten diese Bootblobs nicht. Siehe [Veröffentlichungsstand](docs/RELEASES.de.md).

| Variante | Inhalt |
|---|---|
| `minimized` | Ubuntu Base, SSH, sudo, Netzwerk und Board-Unterstützung; Dokumentation bleibt minimiert. Enthält das offizielle `unminimize`. |
| `minimal` | Ubuntu-Minimal-/Standard-Metapakete, übliche Administrationswerkzeuge, Dokumentation, Manpages und Shell-Vervollständigung. |

Beide starten Konsole und SSH. Das menschliche Standardkonto ist **`odroid` / `odroid`**, mit passwortgeschütztem sudo. Nach dem ersten Login das Passwort ändern. Das Rootpasswort ist gesperrt; Besitzer können eigene öffentliche Schlüssel in `/root/.ssh/authorized_keys` hinterlegen. Wartungsschlüssel, feste SSH-Hostschlüssel und kopierte Maschinenidentitäten werden nicht ausgeliefert.

Ethernet verwendet DHCP und bei fehlender permanenter Treiberadresse eine stabile hardwareabgeleitete MAC. Netzwerk-Zeitsynchronisierung ist aktiviert; die Rootpartition wächst beim ersten Start. Natives eMMC kann die getrennte boot0-Reparatur benötigen: Das Schreiben des IMG über einen Leser aktualisiert nur den Benutzerbereich.

- [Installation und Root-Schlüsselzugang](docs/INSTALL.de.md)
- [eMMC-boot0-Reparatur, Sicherung und Wiederherstellung](docs/EMMC-RECOVERY.de.md)
- [Lüfterstufen 35/45/55 °C einstellen](docs/FAN.de.md)
- [Kernelinstallation, Updates und Rückfall](docs/KERNEL-UPDATES.de.md)
- [Hardwareprüfung](docs/HARDWARE.de.md) und [1.0.3-Prüfstand](docs/CANDIDATE-1.0.3.de.md)
- [Serverfähigkeiten](docs/SERVER-KERNEL.de.md), [Sicherheitsprüfung](docs/SECURITY-REVIEW.de.md), [Audio](docs/AUDIO.de.md) und [Grafik](docs/GRAPHICS.de.md)
- [Bauanleitung](docs/BUILD.de.md) und [Plattformkorrekturen](docs/I2S-USB.de.md)

Der v32-Kernel bestand zehn reine Warmstarts, fünf kontrollierte Halt-/Kaltstarts und die dokumentierten Servertests mit aktiviertem Lockdep und ohne neue Kernelwarnungen. Ein frisch geschriebenes Minimal-1.0.3 bestand zusätzlich die native eMMC-Basisprüfung. Minimized-/SD-Erststarts und aktuelle physische Grafik-/Mikrofonabnahme bleiben getrennt offen; diese Prüfungen sind keine Langzeitgarantie.

Linux, U-Boot, Ubuntu-Pakete und Firmware behalten ihre jeweiligen Lizenzen. Passende Kernelquellen, Konfiguration, Patches und Paketrezepte begleiten das Kernelrelease. Überholte Versuchsprofile wurden aus dem aktuellen Baum entfernt; historische Commits und Quellreleases bleiben erhalten.
