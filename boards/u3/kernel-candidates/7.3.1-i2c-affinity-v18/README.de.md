# U3-I²C0-Interruptzuordnung, Revision 18

[English](README.md)

Der private `7.3.1-odroidu3-v18` ergänzt [v17](../7.3.1-idle-gic-progress-v17/README.de.md). Die Bootoption `i2c_s3c2410.u3_irq_cpu=1` fordert über `irq_set_affinity()` CPU1 für U3-I²C0 an. Vorgabe ist ausgeschaltet (`-1`). Das bestehende U3-Diagnoseziel muss aktiviert sein und zu diesem Board, I²C0 bei `0x13860000` und GIC-INTID90 passen. Andere Controller behalten ihren bisherigen Ablauf.

Die Anforderung erfolgt nach der IRQ-Registrierung, vor der Adapter-/Clientregistrierung. Nur eine gültige, online befindliche CPU wird akzeptiert. Bei ungültiger/ausgeschalteter CPU oder API-Fehler folgt eine Warnung; die normale Initialisierung bleibt bestehen. Keine neuen direkten Registerzugriffe, erfundenen GIC-Masken, Taktänderungen oder Änderungen am Transfer-/IRQ-Handler. Ein erfolgreicher API-Aufruf beweist keine Hardwarezuordnung: Nativ müssen angeforderte/effektive IRQ-Affinität und Interruptfortschritt je CPU geprüft werden.

Die Gegenprobe trennt CPU0-bezogenes Verhalten von Verhalten im Zusammenhang mit I²C-Interrupts. Sie belegt keine Ursache und verspricht keinen Fix. Eine vollständige v17-Initcall-Aufzeichnung endete bei der Registrierung der CPU-Leistungsmessung; ein weiterer Start scheiterte trotz ausgelassener Registrierung schon bei I²C/PMIC. Dieser PMU-Initcall ist keine notwendige Voraussetzung des beobachteten Fehlers. Beide Kontrollen erholten sich nach Kaltstarts; eine gemeinsame Ursache aller Ausfälle ist nicht bewiesen.

Alle sieben v17-RAM-Diagnosekanäle, drei Cortex-A9-Errata-Optionen, Vierkernunterstützung und 101 Serverkriterien bleiben erhalten. Die Konfiguration ändert nur den Versionssuffix; der DTB muss bytegleich bleiben. Der kumulative Patch betrifft dieselben 13 Dateien. Entfernen von Hilfsfunktion, Includes und Aufruf stellt den geänderten v17-Treiber exakt wieder her; die anderen zwölf Dateien bleiben unverändert.

Hostprüfung am gepatchten Treiber:

```sh
python3 check-control.py --source /pfad/zum/gepatchten/linux/drivers/i2c/busses/i2c-s3c2410.c
```

Sie kompiliert die tatsächliche Hilfsfunktion mit IRQ-API-Stubs und prüft sieben Fälle: ausgeschaltet, fremdes Ziel, ungültige/ausgeschaltete CPU, Erfolg, API-Fehler und CPU0. ARM-Bau, Paketintegrität und native Zuordnung/Bootabnahme bleiben getrennte Prüfungen. Passendes Debug-ELF, Pakete, UART-Nachweise und einen geprüften Rückfall mit allen Funktionen erhalten. Begrenzte Neustartserie beim ersten Fehler stoppen. Dieser Kandidat ändert keine Imagevorgabe und hat keine Abnahme als öffentliche Binärversion.

Natives Ergebnis am2026-11-04: Der erste Übergang bestand alle351 Modul-/Konfigurationsprüfungen, vier fortschreitende CPU-Timer, aktive PMU/Auditfunktion, fehlerfreies Journal/Dienste und angeforderte/effektive I²C-IRQ-ZuordnungCPU1. Der erste weitere Warmstart mit demselben Kernel hing; die geplante Fünferserie wurde bei0/1 gestoppt. Zwei anschließende Kaltstartversuche scheiterten; der dritte gelang und ermöglichte die Rückkehr samt geprüftem Start der ursprünglichen vollständigen v17-Konfiguration.

In einem fehlgeschlagenen Kaltstart zeigen zwei späte Momentaufnahmen I²C-IRQ-Fortschritt ausschließlich aufCPU1, deren lokalen Timer unverändert bei698 Interrupts, GIC-Laufpriorität0 und aktiven INTID90; andere CPUs warten laut Stack in `multi_cpu_stop`. Dass der Stillstand der gewählten IRQ-CPU folgt, ist ein wichtiger Zusammenhang, aber kein erfasster CPU1-Programmzähler und kein Beweis für einen bestimmten I²C-/GIC-Befehl. Der letzte globale GIC-Marker zeigt Handler-Rückkehr, der spätere Idle-Marker Eintritt. Diese Kontrolle ist kein Fix und nicht releasefähig.
