# GIC-Alias-Beobachtung, Revision 25

[English](README.md)

Der private Kandidat `7.3.1-odroidu3-v25` erweitert [v24](../7.3.1-gic-order-v24/README.de.md) um eine lesende Gegenprobe im begrenzten Fehlerbeobachter. Er ist keine vorgeschlagene funktionale Interruptkorrektur. Vollständiger Kernelbau, Paketprüfung und native v25-Abnahme stehen noch aus.

Eine native Gegenprobe auf gesundem v17 hat den Leser nacheinander an jede der vier CPUs gebunden und in drei Durchgängen alle vier dokumentierten Exynos-GIC-Aliasse gelesen. Alle 48 Datensätze lieferten für INTID90/109 die Prioritätswörter `a0a0a0a0`, Zielwörter `01010101` und Konfigurationswörter `55555555`. Private Zielwörter folgten unabhängig von der lesenden CPU der ausgewählten Bank (`01`, `02`, `04`, `08` je Byte). Beide UART-Marker kamen an; Modul-, Bootsatz-, Timer- und Journalprüfung blieben unauffällig. Der normale Zugriff einer fremden CPU über einen anderen Alias reproduziert die späten v24-Nullwerte somit nicht. Die gesunde Gegenprobe allein belegt weder Registerkorruption im Fehlerfall noch einen Wechsel des Sicherheitszustands oder die angehaltene Instruktion.

V25 erfasst gemeinsame Enable-/Pending-/Active-Wörter und die Attribute von INTID90/109 über **jeden** validierten Distributor-Alias. TYPER/IIDR jeder Bank und die lesende CPU vor/nach den Zugriffen werden mitgesichert. Eine individuelle Bereichsprüfung verlangt die Abdeckung von INTID32–159; ungültige Sichten werden markiert und ihre gemeinsamen Nutzdaten nicht gelesen. Die bisherige Bank0-Ausgabe bleibt nur bei gültiger Bank0-Sicht erhalten. Zusätzliche Datensätze tragen den Präfix `U3IRQALIAS`.

Alle Aufnahmen erfolgen vor der Konsolenausgabe. Feste Aufnahmebuffer werden durch die bestehende Berichtszulassung serialisiert und entlasten den IRQ-Stack; der Beobachter benötigt keine CPU-Fernaufrufe, neuen Timer oder Speicherallokation. Das Budget von drei abgeschlossenen Berichten bleibt unverändert. Gegenüber v24 ändert sich ausschließlich der Beobachter: Die anderen 13 gepatchten Dateien, IAR-Diagnosebarrieren, Device Tree, Spannungen, I²C-Treiber und das Serverprofil bleiben gleich. Keine neuen MMIO-Ressourcen, IAR-/EOI-Zugriffe, Prioritäts-/Ziel-/Maskenschreibzugriffe, Secure-/Debug-Zugriffe oder Bootfirmwareänderungen. Registeroffsets folgen dem gepinnten Linux-Header `arm-gic.h` und [Arm IHI0048B, Kapitel4](https://documentation-service.arm.com/static/5f8ff21df86e16515cdbfafe).

```sh
python3 check-alias.py --observer /pfad/zum/gepatchten/linux/arch/arm/mach-exynos/odroid-u3-irqdiag.c
```

Die Prüfung kompiliert den tatsächlichen Aufnahmehelfer mit strikt lesenden Registerattrappen und prüft 128 Kombinationen aus Alias und Implementierungsbereich. Ungültige Bereiche dürfen keine gemeinsamen Zustände lesen; gültige Zugriffe müssen innerhalb des ausgewählten Alias mit den dokumentierten Offsets bleiben. ARM-Kompilierung und Stackverbrauch werden separat geprüft. Vor nativen Tests den exakten normalen v17-Bootsatz/Zustand und das Reinstallpaket erhalten, Board-/Medienidentität frisch prüfen und Boot-/Power-Beobachter auf die Pi-UART-Aufnahme umstellen. Beim ersten Serienfehler anhalten und vollständige Diagnose vor der Wiederherstellung sichern. Quellenprüfungen allein erlauben keine APT-/Imagepromotion.

Der Beobachter wurde außerdem ohne Warnung mit den vorhandenen v24-Kbuild-Headern und derselben Konfiguration kompiliert; das neue Profil ändert nur den Revisionssuffix. `u3_diag_dump` benötigt laut Compiler mit serialisierten festen Aufnahmebuffern 128 Byte Stack. Diese isolierte Objektprüfung ersetzt keinen vollständigen v25-Kernelbau oder Hardwarestart.
