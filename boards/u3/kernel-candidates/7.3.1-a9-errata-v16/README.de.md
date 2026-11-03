# Cortex-A9-Errata-Kandidat, Revision 16

[English](README.md)

Das private `7.3.1-odroidu3-v16` behält die begrenzte Diagnose aus [v15](../7.3.1-i2c-progress-v15/README.de.md) und aktiviert drei vorhandene Upstream-Optionen:

| Option | Alter5.4-Kernel | v15 | v16 |
|---|---|---|---|
| `CONFIG_ARM_ERRATA_754322` | y | n | y |
| `CONFIG_ARM_ERRATA_764369` | y | n | y |
| `CONFIG_ARM_ERRATA_775420` | y | n | y |

Die beobachtete U3-CPU ist Cortex-A9 r3p0. Linux-Kconfig und [Arms r3-Errata-Unterlage](https://documentation-service.arm.com/static/608117fa5e70d934bc69f139?token=), Abschnitte2.3.3–2.3.5, beschreiben passende Übersetzungs-/Cache-Workarounds. Die Konfigurationslücken sind belegt, die Ursache des sporadischen U3-Hängers nicht. Andere alte Optionen werden nicht blind übernommen:754327 betrifft CPUs vor r2p0.

Der Patch ist bytegleich v15. Keine manuelle Registerkorrektur oder Treiberneuschreibung: ausgewählt werden vorhandene Upstream-Implementierungen. Alle übrigen Konfigurationswerte einschließlich Server-/Sicherheitsfunktionen bleiben bis auf den neuen Versionssuffix erhalten. DTB, Firmware und Imagevorgaben bleiben unverändert. Diagnoseausgabe kann das Timing beeinflussen; v15 als Kontrolle und passende Debug-ELF/UART-Nachweise erhalten.

Das ursprüngliche Ubuntu20 dient einem getrennt dokumentierten Warmstartvergleich. Dort keine Paket-, Konfigurations- oder Bootdateiänderungen; nur die vom Nutzer freigegebenen Neustarts ändern den Betriebszustand. Bau-/Paketprüfung und native v16-Abnahme bleiben getrennt. Keine Veröffentlichung oder Umstellung der Imagevorgaben ohne Hardwareprüfung.

Bauprüfung am2026-11-03: alle101 Serverkriterien ohne Compilerwarnungen. ARM-Disassembly bestätigt zusätzliche Kontextwechsel-/Cachebarrieren und SCU-Diagnoseschreibzugriff; späte debugfs-Reihenfolge weiterhin korrekt. Paket-/Hardwareprüfung getrennt.
