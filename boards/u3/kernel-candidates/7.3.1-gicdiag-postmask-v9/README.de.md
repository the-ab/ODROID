# U3 GIC-Diagnoserevision 9 nach Maskenentscheidung

[English](README.md)

Privater Diagnosekandidat `7.3.1-odroidu3-v9` auf gepinnter v3-Serverbasis. Gegenüber v8 entfallen die vier zusätzlichen MMIO-Vorabzugriffe; `gic_dist_init()` bleibt bytegleich zur Basis. Die ursprünglichen Lesezugriffe, Maskenentscheidung und kritische Warnung in `gic_get_cpumask()` bleiben in gleicher Reihenfolge. Der zusätzliche Diagnoseaufruf steht erst unmittelbar vor dem unveränderten Rückgabewert. Keine Zielmaske und kein Routing-Schreibzugriff wird verändert. `GICPOST` zeigt die ursprüngliche Entscheidung und den anschließend nur gelesenen Kennungs-/Zielzustand.

V8 bestand drei Warmstarts, ohne damit eine Fehlerkorrektur zu beweisen. Messzugriffe, Ausgabe und Codelayout können das Timing beeinflussen. Diese Revision trennt Vorabmessung von nachgelagerter Beobachtung. Kein Releaseersatz; passender Bootdateirückfall und lokale UART-Aufzeichnung sind erforderlich. Standardimages/APT und Firmware bleiben unverändert. Bau- und Hardwareergebnisse separat nachweisen.
