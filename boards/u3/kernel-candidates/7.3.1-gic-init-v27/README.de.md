# U3-Diagnose der frühen GIC-Initialisierung, Revision27

[English](README.md)

Erweitert v26 um ausschließlich lesende U3-Aufnahmen des ursprünglichen GICD_TYPER-Ergebnisses und der berechneten IRQ-Anzahl sowie der Distributor-Felder vor/nach der vorhandenen Initialisierung. Die sieben io_uring-Fixes bleiben unverändert. Keine zusätzlichen Hardwareschreibzugriffe, IRQ-Masken oder Secure-/Debug-Freischaltungen. Nur bei bestehender Option odroid_u3_gic_defer aktiv. Null-Prioritätslesewerte können Zugriffsbeschränkungen darstellen; der Kandidat unterstellt keine Korruption und schreibt keine Reparaturwerte. Quell-Rückwärtsprüfung und ARM-/Serverprofil-Build bestanden; Paket-/Nativeprüfung ausstehend. V25 ist exakter direkter Rückfall, v17 zusätzliche Reserve. Keine Release-Abnahme.
