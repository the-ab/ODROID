# Reihenfolge der GIC-Diagnose, Revision24

[English](README.md)

Privater Kandidat `7.3.1-odroidu3-v24` erweitert [v23](../7.3.1-mmc-regulator-v23/README.de.md). CPU0-Timerstillstand und aktiver gemeinsamer Interrupt blieben ohne späteren Regulator-BUG bestehen. Die frühere Polling-Gegenprobe hing auch bei deaktiviertem I²C0-IRQ90. Ein aktiver IRQ allein identifiziert daher keinen fehlerhaften Gerätetreiber.

Die optionalen GIC-Fortschrittsmarken werden jetzt unmittelbar vor dem zustandsändernden IAR-Lesevorgang und nach der Marke mit bestätigter Interruptnummer, vor dem Handleraufruf, durch `dsb(sy)` abgeschlossen. Das korrigiert eine Beobachtungslücke zwischen normalen RAM-Speicherungen und relaxed-MMIO. Daraus folgt kein fehlender Barrier im funktionalen Upstream-GIC-Pfad. Die übrigen Fortschrittszeilen bleiben ungefähre, nicht atomare Aufnahmen und liefern keinen abgetasteten Programmzähler. Barrieren verändern möglicherweise das Timing; erfolgreiche Starts allein beweisen keine Ursache.

Der vorhandene begrenzte Beobachter liest zusätzlich Prioritätswörter für SGI0–15 und PPI28–31 pro validierter Exynos-GIC-Bank sowie Prioritäts-/Ziel-/Konfigurationswörter für gemeinsame INTIDs90 und109. `U3IRQATTR` bewahrt die Rohwerte. Vor den Zusatzlesevorgängen wird die implementierte IRQ-Anzahl aus GIC_TYPER geprüft. Kein IAR-/EOI-Zugriff im Beobachter und kein Schreiben von Prioritäten, Zielen, Masken, Pending-/Active-Bits. Keine CPU-Debug-/Secure-Register. Registerdefinitionen stammen aus dem gepinnten Linux-Header `arm-gic.h` und der [Arm-GIC-Spezifikation, Abschnitte4.3.11–13](https://documentation-service.arm.com/static/5f8ff196f86e16515cdbf969).

Nur Beobachter und zwei optionale GIC-Markengrenzen ändern sich gegenüber v23; die übrigen12 Patchdateien, MMC-Korrektur, I²C-Treiber, DTB, Takte, Spannungspolitik, Budget abgeschlossener Aufnahmen und101 Serverkriterien bleiben gleich. Die Konfiguration ändert nur den Revisionssuffix.

```sh
python3 check-order.py --tree /pfad/zum/gepatchten/linux
```

Der Test kompiliert den tatsächlichen Lesehelper mit lesenden Stubs, prüft130 Registeroffsetfälle und die tatsächliche Reihenfolge um IAR. Im ARM-Disassembly beide DSB-SY-Instruktionen prüfen. Build-/Paketprüfungen und native Abnahme bleiben getrennt. Exakten normalen v17-Bootsatz/Zustand sowie Reinstall-/Debugdateien erhalten; begrenzte Warmstartserie beim ersten Fehler stoppen. Keine Image-/APT-Promotion.
