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
