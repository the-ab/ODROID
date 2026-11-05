# RAM-Gegenprobe zur GIC-Basiswahl, Revision29

[English](README.md)

V28 erfasste beim fehlgeschlagenen Warmstart eine ursprüngliche GICD_TYPER-Lesung0 (32IDs), während später alle vier validierten Aliase160IDs zeigten. Diese Gegenprobe speichert die tatsächlich für diese ursprüngliche Lesung und die normale Distributorinitialisierung verwendete Basis. Verglichen werden initialisierter PerCPU-Eintrag, Raw-Mapping, Speicherzeiger und Mappingformel; zusätzlich werden RAM-Zähler des statischen Schlüssels und IRQ-Anzahl festgehalten. Nur Gleichheitsergebnisse erscheinen im vorhandenen späten Core-Bericht, keine Kerneladressen.

Originale einmalige Typlesung und Distributor-MMIO-Operationen bleiben erhalten. Keine zusätzlichen frühen MMIO-Proben, frühen printk-Aufrufe, Timer, erzwungenen Interruptzahlen oder Korrekturschreibzugriffe. Die sieben io_uring-Fixes aus v26 bleiben enthalten. Quellen-/Build-/Paketprüfung und native Abnahme bleiben getrennt; Diagnosekandidat ohne Release- oder Fixbehauptung. V25 bleibt direkter Rückfall, v17 zusätzliche Reserve.

Gepinnter21-Datei-Patch-Replay, gleichwertige originale MMIO-Folge, ARM-Kernel/Module/DTBs und101-Pflichtfähigkeiten des Serverprofils sind bestanden. Paket- und native Prüfung stehen noch aus.

Erster Übergang mit nativer Laufzeitprüfung und beiden korrekten Basiswahlen bestanden. Erster reiner Warmstart gescheitert, begrenzte Serie beim ersten Fehler gestoppt. Die ursprüngliche Typlesung wählt den PerCPU-Speicherzeiger statt des initialisierten Register-Mappings, obwohl der RAM-Zähler des statischen Schlüssels bereits1 zeigt und der erwartete Eintrag zur Mappingformel passt. Die normale Distributorinitialisierung wählt später im selben Boot die richtige Registerbasis. Der Nullwert/32 stammt somit aus einer falschen ursprünglichen Basiswahl. Anfangsbericht und alle drei späten Berichte sind gesichert.

Exakter Patch-/Instruktionscache-Mechanismus bleibt ungeklärt. Ein geprüfter Konfigurationsunterschied ist relevant: Die stabil getestete6.12-Basis hat `CONFIG_JUMP_LABEL` aus, das7.3.1-Serverprofil an. Der unterstützte zählerbasierte Zweig ohne diese Optimierung ist die nächste gezielte Gegenprobe. Kein erzwungener IRQ-Bereich, geratener Registerzugriff oder Releasebeweis. Die sieben io_uring-Fixes bleiben erforderlich.
