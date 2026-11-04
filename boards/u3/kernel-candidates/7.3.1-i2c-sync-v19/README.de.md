# U3-I²C-Interrupt-/Taktabschluss, Revision 19

[English](README.md)

Der private `7.3.1-odroidu3-v19` basiert auf [v17](../7.3.1-idle-gic-progress-v17/README.de.md). Die einzeln aktivierbare Bootoption `i2c_s3c2410.u3_sync_irq=1` wartet unmittelbar vor den beiden vorhandenen `clk_disable()`-Aufrufen des Transferpfades mit `synchronize_irq()` auf den Abschluss des I²C0-Interrupts. Vorgabe ist ausgeschaltet. Die CPU-Affinitätsgegenprobe aus v18 wird nicht übernommen.

Der bisherige Treiber weckt den wartenden Transfer auf, bevor sein Interrupt-Handler alle verbleibenden Controllerzugriffe abgeschlossen hat. Ein parallel eingeplanter wartender Prozess kann somit die Taktabschaltung erreichen, während der Handler noch läuft. Diese Reihenfolge existiert auch im älteren Treiber; sie ist eine mögliche Race Condition, kein Nachweis einer Einführung durch Linux 7 oder einer Erklärung der beobachteten Hänger. Die Gegenprobe testet die fehlende Synchronisation gezielt.

Nur das bestehende Diagnoseziel mit U3, I²C0 bei `0x13860000` und GIC-INTID90 wird berücksichtigt. Polling, atomare und nicht präemptierbare Aufrufe behalten ihr Verhalten. Der IRQ-Handler benötigt die vom normalen Transferaufrufer gehaltene Adapter-Bussperre nicht. Die [generische IRQ-API](https://docs.kernel.org/core-api/genericirq.html#c.synchronize_irq) verlangt präemptierbaren Kontext und warnt vor Ressourcen, die der IRQ-Handler selbst benötigt; diese Bedingungen werden vor dem Warten geprüft. Es gibt keine direkten Registerkorrekturen, IRQ-Masken, Affinitätsänderungen, Spannungseinstellungen oder zusätzlichen Taktreferenzen.

Nur lesbare Modulparameter zeigen `u3_sync_count` (abgeschlossene Warteoperationen) und `u3_sync_skipped` (ausgenommene Kontexte). Stufen 200/201 des vorhandenen Prozesskanals umschließen die Warteoperation. Zähler sind Diagnosebeobachtungen, keine atomaren globalen Momentaufnahmen. Alle sieben RAM-Kanäle, drei Cortex-A9-Workarounds und 101 Serverkriterien bleiben erhalten. Die Konfiguration ändert nur den Versionssuffix, der DTB muss bytegleich bleiben. Der kumulative Patch betrifft dieselben 13 Dateien; Entfernen von Hilfsfunktion, Includes, Aufrufen und Log stellt v17 exakt wieder her.

Hostprüfung am gepatchten Treiber:

```sh
python3 check-control.py --source /pfad/zum/gepatchten/linux/drivers/i2c/busses/i2c-s3c2410.c
```

Sie kompiliert die tatsächliche Hilfsfunktion und beide Abschaltstellen mit API-Stubs: Acht Fälle prüfen Ausnahmen, abgeschlossene Warteoperationen und Warten vor Taktabschaltung. ARM-Bau, Paketintegrität und wiederholte native Boot-/Transferabnahme bleiben getrennte Prüfungen. Passende Debugdateien, Fehleraufzeichnungen und ursprünglichen v17-Rückfall erhalten. Jede begrenzte Serie beim ersten Fehler stoppen. Dieser Kandidat ändert keine Imagevorgabe und keine öffentliche Binär-/APT-Veröffentlichung.
