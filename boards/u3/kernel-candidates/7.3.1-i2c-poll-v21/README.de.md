# U3-I²C0-Polling-Gegenprobe, Revision 21

[English](README.md)

Privater `7.3.1-odroidu3-v21` stammt unabhängig von [v17](../7.3.1-idle-gic-progress-v17/README.de.md) ab. Das standardmäßig ausgeschaltete Bootargument `i2c_s3c2410.u3_poll=1` führt das bestätigte U3-I²C0-Ziel durch die vorhandene Pollingschleife im Prozesskontext und lässt die IRQ-Handlerregistrierung dieses Controllers aus. IRQ-Zuordnung und Zielprüfung (U3, Adresse `0x13860000`, GIC-INTID90) bleiben vorgeschrieben; andere Controller behalten ihr Verhalten.

Die bestehende Folge aus `is_ack()` und `i2c_s3c_irq_nextbyte()`, normale/atomare Taktreferenzen, Busteiler und SDA-Konfiguration bleiben unverändert. Ein eigenes Adapterflag vermeidet die zusätzliche Teilereinstellung des SATA-PHY-Flags `QUIRK_POLL`. Der Abschluss weckt wie beim vorhandenen Pollingpfad keinen wartenden Prozess. Interruptfreigabe/Pending-Semantik innerhalb des Controllers bleiben für Polling erhalten; Linux fordert seinen zugeordneten GIC-IRQ nicht an und aktiviert ihn nicht. Keine direkte GIC-/PMIC-Registeränderung.

Lesbare Parameter zeigen `u3_poll_active` und den ungefähren Zähler erfolgreicher Übertragungen `u3_poll_xfers`. Die Hardwareprüfung muss Bootargument, Ziellog, Aktivflag, zunehmende erfolgreiche Übertragungen, fehlenden I²C0-Handler in `/proc/interrupts`, PMIC-/Regler-/RTC-Funktion, vier fortschreitende CPU-Timer und normale Journal-/Dienst-/Paketprüfungen bestätigen. Die unveränderte Pollingschleife kann schlafen und verändert Zeitverhalten und Scheduling. Wenige erfolgreiche Starts beweisen damit noch keine Ursache.

Die unabhängigen Gegenproben [v19-Synchronisierung](../7.3.1-i2c-sync-v19/README.de.md) und [v20-Taktreferenz](../7.3.1-i2c-clockhold-v20/README.de.md) reproduzierten beide den Hänger; ihre Eingriffe sind hier nicht enthalten. Alle sieben RAM-Kanäle, drei Cortex-A9-Workarounds und 101 Serverkriterien bleiben erhalten. In der Konfiguration ändert sich nur der Versionssuffix; der DTB muss bytegleich bleiben.

```sh
python3 check-control.py --source /pfad/zum/gepatchten/linux/drivers/i2c/busses/i2c-s3c2410.c
```

Quell-/Hostprüfung, ARM-Build/Paketintegrität und Hardwareabnahme sind getrennte Stufen. Exakte normale v17-Bootdateien, Reinstallpaket und passende Debug-/UART-Nachweise erhalten. Begrenzte Hardware-Serien beim ersten Fehler stoppen. Dieser Diagnosekandidat ändert keinen Image-/APT-Standard und ist kein bestätigter Fix.

Hardwareergebnis (2026-11-04): Übergangsstart und vier aufeinanderfolgende reine Warmstarts bestanden die vollständige Prüfung. RTC-Lesezugriffe erhöhten bei jedem gesunden Start den Polling-Erfolgszähler; kein I²C0-IRQ-Handler war registriert. Alle 351 Module, vier fortschreitende CPU-Timer, Regler, PMU, Audit, Journal und Dienste bestanden. Der fünfte reine Warmstart blieb nach dem Wechsel ins neue Root-Dateisystem hängen; die Serie stoppte (vier von fünf bestanden). Die späte Momentaufnahme zeigt I²C0-INTID90 deaktiviert und nicht aktiv, alle drei I²C0-IRQ-Kanäle weiterhin null. Stattdessen war MMC-INTID109 aktiv; CPU0 hatte zuletzt globale GIC-Rückkehr und Idle-Eintritt gespeichert. Die I²C0-GIC-Interruptzustellung ist für diesen beobachteten Hänger somit nicht erforderlich. Aktiver MMC-Interrupt und ungefähre RAM-Marker zeigen weder die eingefrorene Instruktion noch beweisen sie einen MMC-Treiberfehler. Polling ist kein verlässlicher Ausweg.

Nur eine späte Registeraufnahme wurde vollständig: Drei gleichzeitige Watchdog-Aufrufe verbrauchten das gemeinsame Versuchsbudget, während zwei am Busy-Schutz scheiterten. Für weitere Diagnose muss die Aufnahmezulassung so korrigiert werden, dass übersprungene gleichzeitige Aufrufe kein Budget vollständiger Aufnahmen verbrauchen. Die vorhandenen Daten sind keine mehrfachen unabhängigen späten Messungen.

Nach der fehlgeschlagenen Serie bestand eine gemessene Zehnsekunden-Kaltwiederherstellung die vollständige Pollingprüfung. Die vollständigen ursprünglichen normalen v17-Bootdateien und der Verwaltungszustand wurden bytegleich restauriert. Der anschließende native v17-Start bestand alle 351-Modul-, Vier-Timer-, PMU-, Audit-, Journal- und Dienstprüfungen. Passende Backups und das v17-Reinstallpaket bleiben erhalten. Es läuft keine weitere Bootserie.
