# MMC-Regulator-Fehlerweitergabe, Revision 23

[English](README.md)

Privater `7.3.1-odroidu3-v23` behält die korrigierte begrenzte Aufnahmezulassung aus [v22](../7.3.1-diag-budget-v22/README.de.md). Der erste native v22-Übergang scheiterte, lieferte aber drei vollständige späte Dumps: CPU0-Timerzähler blieb 1051, I²C0-INTID90 blieb aktiv. Auf I²C-Buszeitüberschreitungen folgte später ein CPU3-BUG in `regulator_check_voltage()`. Auflösung mit passenden Debugadressen lokalisiert den Aufrufer in `mmc_regulator_set_vqmmc()`. Dieser spätere Absturz beweist nicht die Ursache des früheren CPU0-Stillstands.

`regulator_is_supported_voltage()` kann einen negativen Rücklesefehler liefern; siehe [Regulator-API](https://docs.kernel.org/driver-api/regulator.html). Der MMC-Helper prüfte nur die boolesche Verneinung und konnte danach trotz Fehler die Spannungs-Triplet-API aufrufen. Bei der festen VMMC1,8V-/VQMMC2,8V-Topologie des Boards kann der erste Versuch für 3,3V-Signalisierung zudem einen umgekehrten Bereich 2,7–2,15V bilden. Ein I²C-Fehler konnte die Fähigkeitsprüfung passieren und diesen ungültigen Bereich zur BUG-Prüfung im Regulatorkern weiterreichen.

Die Korrektur weist umgekehrte Bereiche vor der Abfrage mit `-EINVAL` ab und reicht negative Fähigkeits-Abfragefehler vor jeder Spannungsänderungs-API weiter. Nicht unterstützte Bereiche bleiben `-EINVAL`. Die vorhandene optionale Istspannungsoptimierung und erfolgreichen Spannungsargumente bleiben gleich. Spannungswerte, Grenzen, DTB sowie Takt-/I²C-/GIC-Logik sind identisch. Derselbe Helper ist im gepinnten 6.12.114 bytegleich; dies ist ein bestehender Fehlerpfad, keine belegte Linux7-Regression.

```sh
python3 check-regulator.py --source /pfad/zum/gepatchten/linux/drivers/mmc/core/regulator.c --baseline /pfad/zu/v22/drivers/mmc/core/regulator.c
```

Der Hosttest kompiliert tatsächlichen Helper, OCR-Konvertierung und VQMMC-Aufrufer. 16 Fälle prüfen umgekehrte Bereiche, negative/null/positive Abfrageergebnisse, VMMC1,8V-Fallback,1,2V-/1,8V-Signalisierung, bisheriges optionales Rückleseverhalten und unveränderte erfolgreiche Argumente. Der ursprüngliche API-Fehlgebrauch wird ausschließlich mit API-Stubs beobachtet. Der Gesamtpatch betrifft 14 Dateien; die bisherigen 13 geänderten Dateien bleiben bytegleich zu v22. Die Konfiguration ändert nur den Versionssuffix; alle 101 Serverkriterien,351 Module und unveränderter DTB bleiben erforderlich.

Nativ vollständige Boot-/Modul-/Konfigurationsintegrität, feste 1,8V-/2,8V-Versorgung, vier fortschreitende Timer, sauberes Journal/Dienste und vollständigen UART prüfen. Die begrenzte Serie stoppt beim ersten Fehler; normale v17-Backups/Reinstall-/Debugdateien erhalten. Dies korrigiert einen konkreten zusätzlichen Fehlerpfad; die allgemeine Stillstandsursache bleibt offen. Dieser Kandidat ändert keinen APT-/Image-Standard.
