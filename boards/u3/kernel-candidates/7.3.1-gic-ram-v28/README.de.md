# RAM-Gegenprobe der GIC-Anzahl, Revision28

[English](README.md)

Erhält die sieben v26-io_uring-Fixes. Gegenüber v27 entfallen zusätzliche frühe MMIO-Rücklesezugriffe und frühe Logausgabe. Das Ergebnis des ursprünglichen einzelnen GICD_TYPER-Lesezugriffs, die berechnete IRQ-Anzahl und CPU werden nur in RAM gespeichert und im vorhandenen späteren Core-Bericht als U3GICRANGE ausgegeben. Distributorinitialisierung und MMIO-Aufrufreihenfolge entsprechen v26. Keine zusätzlichen Registerschreibzugriffe, IRQ-Masken, Secure-/Debug-Zugriffe oder Timer. Die Gegenprobe soll den frühen Anzahlwert im Fehlerfall mit geringerer Beobachterwirkung erfassen. Quell-/MMIO-Aufruf-Rückwärtsprüfung und ARM-/Serverprofil-Build bestanden; Paket-/Nativeprüfung ausstehend. V25 direkter exakter Rückfall, v17 zusätzliche Reserve. Keine Release-Abnahme.
