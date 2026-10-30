# Kernel-Sicherheitsprüfung —30.10.2026

[English](SECURITY-REVIEW.md)

Kandidat 7.3.1-odroidu3-v3 verwendet die vollständigen signierten Linux 7.3.1-Stablequellen. SHA256: `fa595aad93734f829c963c2a90ef7c3673224fd7fdae7b49406e397cde2de231`. Entwicklersignatur von Greg Kroah-Hartman gegen den über kernel.org-WKD bezogenen Schlüssel geprüft.95.979 reguläre Upstream-Quelldateien verglichen; nur fünf dokumentierte U3-Quelldateien geändert. Die laufende Kernelkonfiguration stimmt mit dem geprüften Profil überein.

Linux-CNA-Datensatz `6e051cebb25cdd17a28267fbf1a4de5c9c8164f8`:18.164 veröffentlichte Einträge geprüft.18.160 laut veröffentlichten Versionsbereichen nicht betroffen. Vier verbleibende Versionszuordnungen manuell bewertet: CVE-2021-47645(Zoran nicht aktiviert), CVE-2026-68086(THP deaktiviert, Code upstream entfernt), CVE-2026-98938(Rust deaktiviert, upstream überarbeitet), CVE-2026-98941(Dateisystemverschlüsselung in v3 aktiviert; laut CNA betroffener Code bis 7.2, ab 7.3überarbeitet). Für dieses Profil verbleibt kein bekannter anwendbarer offener Treffer dieses Datenstands.

CVE-2026-98432 ist bereits ab 6.12.113 und 7.3 behoben. Die korrigierte RCU-verzögerte Freigabe in `inet_sock_destruct()` und `tcp_v4_reqsk_destructor()` wurde in unseren 6.12.114- und 7.3.1-Quellen direkt geprüft. Der Ubuntu-Paketstatus ist nicht automatisch der Status dieses selbst gebauten Kernels.

Dies ist eine datierte Prüfung veröffentlichter Daten, Konfiguration und Quellen, keine Garantie gegen unbekannte/künftige Lücken oder ein unabhängiges vollständiges Audit unserer lokalen Patches. Bei neuer Upstreamversion, geänderten Patches oder Konfiguration erneut bewerten. Die automatisierte6.12.114-Versionsprüfung hatte gesondert zu bewertende Restfälle; sie wird nicht als Zahl tatsächlich ausnutzbarer U3-Lücken dargestellt. Vollständige neue Stableänderungen zusammen übernehmen und passende Quellen zu veröffentlichten Paketen bereitstellen.

Primärquellen: [Kernelreleases](https://www.kernel.org/), [Kernel-CVE-Verfahren](https://docs.kernel.org/process/cve.html), [Linux-CNA-Repository](https://git.kernel.org/pub/scm/linux/security/vulns.git), [Ubuntu-Hinweis zu CVE-2026-98432](https://ubuntu.com/security/CVE-2026-98432).
