# U3 GIC-Diagnoserevision 8

[English](README.md)

`7.3.1-odroidu3-v8` ist ein privater Diagnosekandidat auf der gepinnten v3-Serverbasis. Die zusätzliche Ausgabe `ODROID-U3 GICDIAG` zeigt die unveränderte CPU-Maskenentscheidung, logische CPU/MPIDR, den Distributor-Bankoffset, Steuer-/Typ-/Kennungs-/Gruppenwerte und die Zielregister der privaten Interrupts. Eine vor dem Deaktivieren aufgenommene Momentaufnahme wird erst nach der ursprünglichen Maskenabfrage ausgegeben. CPU-Zuordnung und Routing-Schreibzugriffe bleiben unverändert; Quittierungs- und EOI-Register werden nicht gelesen.

Ein vollständiger UART-Trace vom 2. November 2026 reproduzierte den v3-Fehlwarmstart mit zwei Nullmaskenmeldungen vor dem SMP-Start und unvollständigem RCU-Tasks-Trace-Selbsttest. Derselbe v3-Kernel mit gleichen Argumenten startete kalt ohne diese Fehler. Die frühere Annahme eines zuverlässig startenden v3-Hardwarerückfalls ist damit überholt. Eine Firmware-, Kernel- oder elektrische Ursache ist noch nicht bewiesen.

Nur mit passendem ursprünglichem Bootdatei-Backup und lokaler UART-Aufzeichnung kontrolliert testen. Kein Boot0-, gespeicherter U-Boot-ENV- oder eMMC-Einstellungswechsel. Zusätzliche Ausgabe verändert das Timing und ersetzt keine Releaseabnahme. Board-/Image-/APT-Standard bleiben v3; dieser Kandidat wird nicht automatisch veröffentlicht. Bau- und Runtime-Nachweise bleiben zunächst in der privaten Diagnoseablage.
