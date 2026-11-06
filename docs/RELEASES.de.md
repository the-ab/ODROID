# Veröffentlichungen

[English](RELEASES.md)

Das Quell- und Kernelrelease zum Imagerezept **1.0.3** verwendet `7.3.1-odroidu3-v32`, DEB-Version `7.3.1-33` und Aktivierungswerkzeuge `1.0.3`. [Kernelrelease](https://github.com/the-ab/ODROID/releases/tag/u3-kernel-7.3.1-33) · [APT-Pakete](https://the-ab.github.io/deb/) · [Prüfstand](CANDIDATE-1.0.3.de.md).

**Vollständige Image-ZIPs bleiben in einem Entwurf und sind keine öffentlichen Downloads.** Die aus dem Referenzimage übernommenen BL1-/BL2-/TrustZone-Bytes haben feste Hashes; ihre genauen Weitergabe- und Quellbedingungen sind weiterhin ungeklärt. Ein Herkunftshash ist keine Lizenzfreigabe. Die getrennten Kernel-DEBs und passenden Quellarchive enthalten keine Hersteller-Bootblobs. Ein firmwarefreier Bausatz zur lokalen Zusammensetzung wäre ein anderes, separat zu prüfendes Ergebnis; er ersetzt die geprüften Images nicht stillschweigend.

Veröffentlichte Pakete benennen Rezept-/Quellcommit, Konfiguration, Patch, Prüfsummen und das genau passende Linux-Quellarchiv. Vollständige Imagereleases benötigen zusätzlich Paketlisten, IMG-/ZIP-Hashes, Dateisystem-/Partitions-/Boot-Rückleseprüfung, vollständige ZIP-Prüfung, Ausschluss privater Zugangsschlüssel und Identitäten sowie belegte Firmwarebedingungen. Hardwarebelege müssen Variante und Bootmedium unterscheiden. Siehe [Hardwarestand](HARDWARE.de.md).

Der kompilierte v32-Kernel bestand die dokumentierte native Boot-/Serverqualifikation. Frisches Minimal 1.0.3 bestand die native eMMC-Basisprüfung; Minimized-/SD-Erststarts, aktuelle physische Grafik-/Mikrofonprüfung und ungenutzte Peripherie bleiben offen. Bauprüfungen ersetzen keinen physischen Start.

Imageversionen verwenden SemVer; Kernel behalten Upstream-Version und Boardrevision. Veränderte kompilierte Bytes benötigen einen neuen Boardsuffix. Neu verpackte Dokumentation kann den ZIP-Hash ändern, während der IMG-Hash gleich bleibt; maßgeblich ist die jeweilige Archivprüfsumme. Bestehende Releases und passende Quellhistorie bleiben erhalten. Veröffentlichung erfolgt bewusst und nie automatisch durch ein Bauskript.
