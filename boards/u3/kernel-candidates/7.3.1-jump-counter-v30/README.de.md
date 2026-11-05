# GIC-Schlüsselzähler als Gegenprobe, Revision30

[English](README.md)

V29 erfasste für die ursprüngliche GIC-Typlesung den PerCPU-Speicherzeiger statt dessen initialisiertem Register-Mapping, obwohl der RAM-Schlüsselzähler bereits1 zeigte. Diese Gegenprobe ersetzt nur die Bedingung im GIC-Basiszugriff von static_branch_unlikely durch den regulären static_key_enabled-RAM-Zählertest. Normale Schlüsselaktivierung, PerCPU-Mapping und Hardwareinitialisierung bleiben erhalten. Kein erzwungener Bereich, neuer MMIO-Zugriff, geratene Adresse oder Secure-/Debug-Zugriff.

Global bleibt CONFIG_JUMP_LABEL aktiv, da XFS-Onlineprüfung/-reparatur es auswählt. Alle bisherigen XFS-/Serverfähigkeiten und sieben io_uring-Fixes bleiben erhalten. In der aufgelösten Konfiguration ändert sich nur LOCALVERSION. Exakter früher Patch-/Cache-Mechanismus nicht bewiesen; gezielter Zugriffs-Workaround zur Qualifikation. Quellen-/Build-/Paketprüfung und native Abnahme getrennt. V25 direkt, v17 Reserve; keine Release-Abnahme.

Quell-Replay, ARM-Build,101-Pflichtfähigkeiten und Paket-/351-Modulprüfung bestanden. Erster nativer Übergang und drei reine Warmstarts gesund: beide gemessenen Basen entsprechen dem initialisierten Register-Mapping, Typ/Bereichfc64/160, gemeinsame PrioritätenA0 und alle vier CPU-Timer laufen. Journal, Paketaudit und Kernel-Taint sauber. In dieser Phase keine Kaltzyklen. Laufender Kernel enthält alle sieben io_uring-Fixes. Normale Release-Bootparameter, mindestens zehn Warm-/fünf Halt-Kaltstarts sowie abschließende Server-/Peripheriequalifikation stehen aus; Diagnosekontrollen sind keine Release-Abnahme.
