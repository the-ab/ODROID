# U3-I2C-Interrupt-Ablaufmessung, Revision 14

[English](README.md)

Der private Kandidat `7.3.1-odroidu3-v14` ergänzt v12 nach einem vollständig beobachteten Fehlwarmstart trotz korrekter ursprünglicher GIC-Masken und Softwaretabelle. Drei RCU-Stillstandsaufnahmen zeigten unverändert218 CPU0-Timerinterrupts, wartende Timer/IPIs und einen aktiven gemeinsamen INTID90. Laut Device Tree gehört dieser zu I2C0, dem vom PMIC verwendeten Controller. Ein aktiver Interrupt beweist noch nicht, ob Controller, Handler, allgemeine IRQ-Bearbeitung oder eine andere Abhängigkeit den Stillstand verursachten.

`odroid_u3_i2cdiag=1` zusammen mit `odroid_u3_irqdiag=1`, `odroid_u3_gic_defer=1`, serieller Frühkonsole und `loglevel=7` aktivieren. Die Ablaufmessung startet erst nach der vorhandenen U3-GIC-/MCT-Ressourcenprüfung. Der I2C-Treiber bindet ausschließlich den U3-Controller bei0x13860000 mit Hardware-INTID90. Board-/Image-Standard und Bootfirmware bleiben erhalten.

Die Marken speichern Phase, Zähler, Werte, Task-ID und jiffies im RAM. Sie ergänzen im beobachteten IRQ-Pfad keine Controller-Lese-/Schreibzugriffe, Quittierung, Sperren, Speicherallokation, Wartefunktion, CPU-übergreifenden Aufruf oder serielle Ausgabe. Die ursprünglichen41 I2C-MMIO-Zugriffe behalten Breite, Operanden und Reihenfolge; Helfer markieren unmittelbar davor/danach. GIC-Weiterleitung und allgemeiner Fasteoi-Kontrollfluss bleiben erhalten. Zusätzliche Befehle, Speicherzugriffe und die Diagnoseausgabe können das Timing verändern: Dies ist ein Messkandidat, kein Fix.

| Kanal | Bedeutung / Phasen |
|---|---|
|0: GIC |1 nach vorhandenem IAR-Lesen,2 vor allgemeiner Weiterleitung,3 nach Rückkehr; ursprünglicher IRQ-Status wird gespeichert. |
|1: allgemeines Fasteoi |1 vor Deskriptorsperre,2 nach Sperre,3/4 vor/nach Ereignisaufruf,5/6 vor/nach Freigabe/EOI,7 früher Rücksprung,8 letzter Rücksprung vor automatischer Sperrfreigabe. GIC-Phase3 bestätigt die vollständige Rückkehr einschließlich Freigabe. |
|2: I2C-Hard-IRQ |1 Handler-Eintritt,2 Status verfügbar,3/4 vor/nach nächstem Byte,5 Rückkehr;30 Completion-Eintritt,31/32 vor/nach Aufwecken. |
|2: MMIO-Phasen |100/101 vor/nach32-Bit-Lesen,102/103 vor/nach32-Bit-Schreiben,104/105 Byte-Lesen,106/107 Byte-Schreiben. `value` ist der Registeroffset; `aux` enthält vor Lesezugriffen den Zustand, sonst den übertragenen Wert. |
|3: Transfer/Takt |1/2 vor/nach Taktaktivierung,3/4 um die normale Taktabschaltung nach abgeschlossenem Transfer,5/6 um weitere vorhandene Taktabschaltungen im Prozesskontext. Rückgabe-/Zustandswerte bleiben sichtbar. |

I2C-MMIO-/Completion-Marken gelten nur im Hard-IRQ-Kontext, damit ein abgelaufener wartender Prozess die letzte Phase des festhängenden Handlers nicht überschreibt. Transfermarken sind getrennt. Die Datensätze zeigen den ungefähren letzten Fortschritt ohne Synchronisierung oder atomare Gesamtaufnahme; Prozessmigration und gleichzeitige Änderungen können gemischte Felder hinterlassen. Dies ist kein vollständiger Ereignisverlauf.

Der vorhandene begrenzte RCU-Hook kopiert die RAM-Daten vor der Konsolenausgabe und meldet sie als `U3I2CPROG` zusammen mit GIC/MCT. Bei aktivierter Messung kann Root die RAM-Daten zusätzlich über `/sys/kernel/debug/odroid-u3-i2c-progress` lesen (0400). Diese Datei liest keine Hardwareregister und ändert keine Konfiguration. Eine Bindungsmeldung im Prozesskontext nennt den zugeordneten Linux-IRQ.

Bau, Paketprüfung und tatsächliche Hardwareabnahme bleiben getrennt. Passende Quellen/Debug-ELF, lokale UART-Aufzeichnung und geprüften v12-/v3-Bootdatei-Rückfall vor dem Test erhalten. Dieses Profil ersetzt keine öffentlichen Kernel oder Images.


Dies ersetzt das bereits gebootete v13: Dessen optionale debugfs-Datei wurde laut verlinkter Core-Initcall-Reihenfolge vor debugfs_init angefordert. V14 behält frühe RAM-Marken und RCU-Beobachtung bei, erstellt die Datei aber in einem getrennten Late-Initcall und prüft Fehler. Die genaue Reihenfolge ist vor dem Hardwaretest im verlinkten ELF zu prüfen.

Der ARM-Bau bestand am03.11.2026 ohne Compilerwarnungen. Im verlinkten ELF liegt die optionale Dateiinitialisierung ausdrücklich auf Stufe7 nach debugfs_init auf Stufe1; der frühe Beobachter bleibt auf Stufe1. Konfigurations-/DTB-Prüfungen bestanden; Hardwareprüfung steht noch aus.

Native Prüfung am2026-11-03: RAM-Datei und alle vier Kanäle verfügbar, vier Warmstarts gesund. Der nächste Start hing vor Userspace mit Watchdog-Softlockups ohne RCU-Momentaufnahme. Nutzer-Kaltstart stellte gesundes v14 wieder her. Revision15 ergänzt die begrenzte Aufnahme an der vorhandenen Softlockup-Meldestelle; Plattformursache weiterhin offen.
