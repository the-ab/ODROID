# io_uring-Sicherheitsrückportierungen, Revision 26

[English](README.md)

Der private Kandidat `7.3.1-odroidu3-v26` erweitert [v25](../7.3.1-gic-alias-v25/README.de.md) um die folgenden CNA-referenzierten io_uring-Korrekturen. IO_URING bleibt aktiviert. Die sieben wirksamen Patches bestehen strikte Quellkontextprüfungen und eine exakte Rückwärtsgegenprobe auf den 7.3.1-Quellen. ARM-Cross-Build und Server-Konfigurationsprüfung sind bestanden. Die Paketprüfung für alle 351 Module, Image-CRCs und unveränderten DTB ist bestanden. Der erste native Übergang reproduziert den früheren Plattform-Startfehler; die native Qualifikation ist bis Diagnose/Wiederherstellung gestoppt. Keine Image- oder öffentliche APT-Promotion allein aus Quellprüfungen.

| CVE | Ursprüngliche Upstream-Korrektur |
|---|---|
| CVE-2026-99231 | [`c254eec4364b`](https://git.kernel.org/stable/c/c254eec4364b9f4b4cbdce43be3fb4df5a651a70) |
| CVE-2026-99230 | [`4c83e39f4d19`](https://git.kernel.org/stable/c/4c83e39f4d1944d7146fd06094f2c8053238d55c) |
| CVE-2026-99229 | [`34f5a664c34d`](https://git.kernel.org/stable/c/34f5a664c34d3cb62f6bec7f4156754594a7d25b) |
| CVE-2026-99228 | [`63c103279a95`](https://git.kernel.org/stable/c/63c103279a95e82280092f2f4232e91e8117a252) |
| CVE-2026-99255 | [`436d48a2ed13`](https://git.kernel.org/stable/c/436d48a2ed13112d2d27085325838e5bce6b4507) |
| CVE-2026-99254 | [`22e643e61b9b`](https://git.kernel.org/stable/c/22e643e61b9b6299b42ff7d88bab48bccada8a5d) |
| CVE-2026-99253 | [`76a82c666abf`](https://git.kernel.org/stable/c/76a82c666abf155ad52d5f41043eac77dd3e41d8) |

Für CVE-2026-99255 verwendet `io_uring.c` den CNA-referenzierten Stable-Rückport `92e20e9c72bdf6cfa6f84eded7b33399bc7061da` und erhält das vorhandene Link-Prädikat. Die originalen Mainline-Hunks für `io-wq.c` und den Header erhalten den KCOV-Kontext. Eine nicht zugehörige Änderung der REQ_F_CQE_SKIP-API wird damit nicht eingeführt. Original-/Kompatibilitätspatches, wirksamer Patch und Metadaten/Prüfsummen liegen unter `security/`.

Die v25-Plattform-/Treiberpatches und alle Serverfunktionen bleiben gleich; nur sieben io_uring-Dateien und der Revisionssuffix unterscheiden sich. Auf Nutzerwunsch ist v25 der direkte Rückfall, v17 bleibt zusätzlich erhalten. Der begrenzte normale [io_uring-Funktionstest](../../../../tests/iouring_smoke.c) prüft NOP-Abschlüsse, verknüpftes Schreiben/fsync regulärer Dateien, Rücklesen, asynchrones Öffnen/Schließen, Poll-Abbruch und waitid für einen Kindprozess. Er ist keine Schwachstellen-Reproduktion. Vor neuen Images die Revision mit begrenzten Bootserien und normalen io_uring-Funktionstests prüfen. Die ursprüngliche CPU-/Interruptursache und der automatische Start nach Poweroff bleiben getrennte offene Befunde. Zur Prüfung der Patchherkunft und normalen Funktion sind keine Schwachstellen-Reproduktionen nötig.

Auf dem U3 vom Repository-Stamm mit `cc -O2 -Wall -Wextra -Werror tests/iouring_smoke.c -o /tmp/odroid-iouring-smoke` übersetzen und `/tmp/odroid-iouring-smoke` als normaler Benutzer ausführen. liburing ist nicht erforderlich. Der Test ist auf 20 Sekunden begrenzt und entfernt seine temporäre reguläre Datei bei Erfolg.

Nativer Stand: Der erste Warmübergang scheitert mit den früheren I2C-/PMIC-/Plattformsymptomen. Nach einem kontrollierten Kaltwiederanlauf bestehen alle351 Module, laufende Konfiguration, Journal, Audit und vier CPU-Timer sowie der normale io_uring-Test ohne Rootrechte. Bootstabilität ist nicht abgenommen. Der exakte v25-Bootsatz ist direkter Rückfall, v17 bleibt zusätzliche Reserve. Gerätespezifisches URING_CMD-Laufzeitverhalten ist ungeprüft.
