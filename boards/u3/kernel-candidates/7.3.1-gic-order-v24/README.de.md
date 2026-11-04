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

Natives Ergebnis (2026-11-04): Der Übergang bestand351-Modul-, Vier-Timer-, Audit-/PMU-, Festspannungs- sowie Journal-/Dienstprüfungen. Der erste reine Warmstart hing, die Serie stoppte (0/1 bestanden). Drei vollständige Aufnahmen bei36,586,39,026 und64,586 Sekunden zeigten konstanten CPU0-Timer772, RPR0 und aktiven INTID90. CPU0s letzter GIC-Kanal blieb auf Stufe15 (Rückkehr, vorherige ID1023), der Idle-Kanal auf Stufe1 (Eintritt). Diese Marken identifizieren weiterhin keine genaue blockierte Instruktion; ein Halt vor Abschluss eines neuen Vor-IAR-DSB ist darin eingeschlossen. Kein späterer Kernel-BUG im Fehlstartmitschnitt.

Private Prioritätswörter blieben`a0a0a0a0`; gemeinsame90/109-Wörter wurden spät als null gelesen, anfänglich als`a0a0a0a0`. Anfangs beobachtete CPU0, spät CPU2 über den bisherigen Bank0-Alias. Der GIC-Treiber verwendet auf dieser Exynos-Implementierung mit getrennten Registern kernrelative Distributor-Aliasse. Vor einer Deutung als tatsächliche Prioritätsänderung oder Korruption sind deshalb Alias- und gesunde Fremd-CPU-Gegenproben nötig. Zusätzlich definiert die [Arm-Spezifikation, Abschnitt4.4.6](https://documentation-service.arm.com/static/5f8ff196f86e16515cdbf969) bei bestimmten Non-secure-Sichten einen RPR-Nullwert. Daraus folgt kein Anlass für Secure-Registerzugriffe oder spekulatives Zurücksetzen von Prioritäten.

Der Fehlstartmitschnitt wurde vor einer verifizierten10,138-Sekunden-AC-Ausphase gesichert. Die native v24-Wiederherstellung bestand; anschließend wurden normaler v17-Bootsatz und Zustand exakt restauriert und nach verifizierter10,105-Sekunden-Ausphase gestartet. Abschließend bestanden351 Module,vier fortschreitende Timer,PMU/Audit ohne Verlust sowie sauberes Journal/Dienste. Keine Firmware-/APT-/Image-Promotion.

Bootzeit: Die beiden gesunden v24-Starts mit voller Diagnose benötigten39,754/39,876 Sekunden bis zum systemd-Ziel (Kernel16,617/16,619;Userspace23,136/23,256). Der restaurierte normale v17 benötigte28,504 Sekunden (Kernel5,137;Userspace23,366). Geräteerkennung und Netzwerkaufbau im Userspace bleiben wesentlich; dieser Vergleich unterscheidet Diagnosecode und Ausgabe und ist kein isolierter Logging-Versuch. Die Nutzerbeobachtung von etwa5 Sekunden bei Ubuntu20 wurde in diesem Durchgang nicht mit demselben Bereitschaftskriterium neu gemessen.
