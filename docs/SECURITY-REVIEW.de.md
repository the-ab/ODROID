# Kernel-Sicherheitsprüfung

[English](SECURITY-REVIEW.md)

Prüfdatum: **5. November 2026**. Ziel: Linux `7.3.1-odroidu3-v32`, DEB `7.3.1-33`, das gepinnte Quellarchiv und die ausgelieferte Konfiguration. Dies ist eine datierte Quell-/Konfigurationsbewertung, keine Garantie für zukünftige oder unveröffentlichte Schwachstellen.

Der Linux-CNA-Snapshot `b537cbcd0154f07e083400c5ba2f9826be84ee26` enthielt 18.204 veröffentlichte Einträge. Konservative Versionsbereichsprüfungen ordneten vor manueller Bewertung und lokalen Korrekturen 18.193 als nicht betroffen, zehn als betroffen und einen als unbekannt ein. Diese Restzahlen zählen keine ausnutzbaren U3-Schwachstellen.

Sieben zusätzliche io_uring-Korrekturen sind enthalten: **CVE-2026-99228, -99229, -99230, -99231, -99253, -99254 und -99255**. [Herkunft und genaue Patches](../boards/u3/security/upstream-fixes.json) halten kanonische Commits und die API-kompatible wirksame 7.3.1-Anpassung für CVE-2026-99255 fest. Der kombinierte wirksame Patch steht in `boards/u3/patches/platform.patch`; die einzelnen Referenzpatches nicht erneut anwenden.

Die vier früheren Restfälle wurden gesondert bewertet: CVE-2021-47645 (Zoran deaktiviert), CVE-2026-68086 (THP deaktiviert; Mainline-Code entfernt), CVE-2026-98938 (Rust deaktiviert; Mainline-Umbau) und CVE-2026-98941 (Dateisystemverschlüsselung aktiv; CNA beschreibt betroffenen Code bis 7.2 und dessen Umbau in 7.3). CVE-2026-98432 ist in der gepinnten 7.3.1-Basis korrigiert: Die betroffenen Socket-Destruktoren verwenden die nötige RCU-verzögerte Freigabe. Ubuntus Paketstatus beschreibt diesen selbst gebauten Kernel nicht automatisch.

Quell-Replay, ARM-Bau, 101 Server-Konfigurationsanforderungen und alle 351 paketierten Module bestanden. Der native normale io_uring-Test ohne Rootrechte umfasst NOPs, verkettetes Dateischreiben/fsync/Rücklesen, asynchrones Öffnen/Schließen, Poll-Abbruch und Child-waitid. Gerätespezifisches URING_CMD ist nur quell-/baugeprüft; ein passendes Laufzeitgerät fehlte. Es wurde kein Exploit-Reproducer verwendet. Native Boot-/Serverprüfungen liefen mit Lockdep und ohne neue Kernelwarnungen.

Lokale GIC-, Audio-/USB-, MMC- und TUN-Änderungen bleiben in den passenden Quellen erhalten. Funktionstests und ein sauberes Warnungsprotokoll sind kein vollständiges unabhängiges Sicherheitsaudit. Bei Änderungen an Quellen, Konfiguration oder veröffentlichten CVE-Daten die Bewertung erneuern.

Primärquellen: [Linux-CNA-Repository](https://git.kernel.org/pub/scm/linux/security/vulns.git), [Kernel-CVE-Verfahren](https://docs.kernel.org/process/cve.html), [Kernelreleases](https://www.kernel.org/releases.html), [CVE-2026-98432](https://ubuntu.com/security/CVE-2026-98432).
