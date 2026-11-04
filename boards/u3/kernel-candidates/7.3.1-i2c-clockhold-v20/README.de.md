# Verwaltete U3-I²C0-Taktreferenz, Revision 20

[English](README.md)

Der private `7.3.1-odroidu3-v20` basiert auf [v17](../7.3.1-idle-gic-progress-v17/README.de.md). Die einzeln aktivierbare Bootoption `i2c_s3c2410.u3_hold_clock=1` hält für das geprüfte U3-I²C0-Ziel eine zusätzliche, ausgeglichene `clk_prepare_enable()`-Referenz. Vorgabe ist ausgeschaltet. Normale und atomare Transferfunktionen, IRQ-Behandlung und deren vorhandene Taktaufrufe bleiben unverändert. Weder die Affinitätsänderung aus v18 noch die Synchronisationswarteoperation aus v19 wird übernommen.

Die zusätzliche Referenz wird nach Identifikation von I²C0 bei `0x13860000` und GIC-INTID90 angefordert, vor IRQ- und Clientregistrierung. Eine verwaltete Aktion gibt sie mit `clk_disable_unprepare()` frei. Registrierung dieser Aktion vor der IRQ-Ressource stellt sicher, dass die umgekehrte devres-Freigabe zuerst den IRQ entfernt. Die zusätzliche Prepare-Referenz hält auch den bisherigen `clk_unprepare()`-Aufruf des Remove-/Fehlerpfades ausgeglichen. Fehler beim Anfordern oder Registrieren der Aktion brechen Probe mit ausgeglichener Freigabe ab und täuschen keine aktive Gegenprobe vor.

Nur lesbare Modulparameter zeigen `u3_clock_held` und `u3_clock_rate`. Nativ sind Bootparameter, Halteflag, Rate sowie Enable-/Prepare-Zähler des I²C0-Takts neben tatsächlichem Busfortschritt und wiederholter Bootgesundheit zu prüfen. Die Gegenprobe trennt dynamische Taktabschaltung von anderen IRQ-Fehlern; sie beweist keine Ursache oder akzeptierte Umgehung. Ein erfolgreicher `clk_prepare_enable()`-Aufruf ist eine Beobachtung der Taktverwaltung, keine externe elektrische Messung.

Die v19-Synchronisation vor der Taktabschaltung scheiterte beim ersten Übergang mit CPU0-Stillstand, aktivem INTID90 und einem weiteren Kern am Synchronisationsmarker. Das Abwarten eines Handlers schließt einen später eintreffenden Interrupt oder jede Taktlebensdauerfrage nicht aus. Die getrennte Gegenprobe hält den Takt deshalb über alle Transferkontexte verfügbar. Keine direkten GIC-/PMIC-Registerzugriffe, Spannungsänderungen, IRQ-Masken oder Transferänderungen werden ergänzt.

Alle sieben RAM-Diagnosekanäle, drei Cortex-A9-Workarounds und 101 Serverkriterien bleiben erhalten. Die Konfiguration ändert nur den Versionssuffix, der DTB muss bytegleich bleiben. Der kumulative Patch betrifft dieselben 13 Dateien; Entfernen von Hilfsfunktion und Probe-Aufruf stellt den geänderten v17-Treiber exakt wieder her.

```sh
python3 check-control.py --source /pfad/zum/gepatchten/linux/drivers/i2c/busses/i2c-s3c2410.c
```

Die Hostprüfung kompiliert die tatsächliche Hilfsfunktion mit Takt-/devres-Stubs und prüft acht Fälle, darunter Ausnahmen, Anforderungs-/Aktionsfehler, erhaltene Taktreferenz bei Transferpaaren sowie ausgeglichene Remove-/IRQ-Registrierungsfehlerpfade. ARM-Bau, Paketintegrität und native Abnahme bleiben getrennte Prüfungen. Passende Debugdateien und ursprünglichen v17-Rückfall erhalten, begrenzte Serie beim ersten Fehler stoppen und diesen Kandidaten nicht als abgenommenen Image-/APT-Fix veröffentlichen.
