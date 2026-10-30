# U3 Linux7.3.1 Serverrevision2

Explizites Serverprofil, Kernel7.3.1-odroidu3-v2/Paket7.3.1-2. Gleiche geprüfte Upstreamquellen und fünf Boardpatches wie v1. Ergänzt Container-Dateisysteme/Netzwerk/cgroup-Controller, nftables/iptables, VPN, Dateidienst-/Speichermodule, AppArmor/Landlock/Audit sowie zusätzliche Speicher-/Netzwerkhärtung. Hardwarestart und Lüfter35/45/55 bleiben erhalten. Bestehende1.0.1-Images und veröffentlichte v1-Pakete bleiben unverändert.

Native Docker-, VPN-, Firewall- und Dateidiensttests sind vor einer Funktionszusage nötig. Eine gesetzte Option bestätigt noch keinen laufenden Dienst. Nur aus dem festgelegten Archiv mit vollständiger Konfiguration/Patch bauen. Viele Diensttreiber sind Module; Sicherheitsrichtlinien und CPU-/Speichercontroller sind fest eingebaut. Historische Kconfig-Symbole wurden upstream teilweise geändert: requested-options.json dokumentiert Anfragen, maßgeblich ist kernel.config. Das Profil veröffentlicht sich nicht automatisch.
