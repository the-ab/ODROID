# Releaseanforderungen

[English](RELEASES.md)

Imageversion: SemVer, erster Kandidat `1.0.0`. Kernel: Upstream-Version mit Boardrevision, derzeit `6.12.114-odroidu3-v1`. U3-/XU4-Releases erhalten eigene Hardwarenachweise.

Ein Release benennt Quellcommit, Paketmanifest, IMG-/ZIP-Prüfsummen, Kernel/Module/DTB und boot0-Präfix. ZIP-CRC und vollständige entpackte IMG-Prüfsumme werden geprüft. Passende Kernel-/U-Boot-Quellen, Konfiguration, lokale Patches und Baubefehle begleiten Binärdateien; Paket- und Firmwarelizenzen bleiben verfügbar.

Vor stabiler Veröffentlichung:

1. Frische minimized-/minimal-Builds bestehen ARM-Login/PAM, sudo, SSH, Netplan und die gesamte systemd-Startreihenfolge.
2. Nur Defaultkonto als menschlicher Benutzer, keine Authorized-/Hostschlüssel, kopierte Maschinenidentität oder geerbten Host-Workspace-ACLs. odroid erhält ohne sudo keine Schreibrechte auf Root-Konfiguration.
3. Partitionen zurücklesen, Bootoffsets/CRCs, Dateisysteme, Kernel-/Modulversionen und ZIP-Roundtrip prüfen.
4. Neue Images auf dem vorgesehenen Medium real starten; SD, natives eMMC, Root-Vergrößerung, DHCP-Identität, SSH/sudo, Journal, Lüfter und Desktopprüfungen getrennt dokumentieren.
5. Genaue Binär-Weitergabe-/Quellbedingungen von BL1/BL2/TrustZone belegen. Ein hashgebundenes Referenzimage als Baueingang ersetzt keine Firmware-Lizenzaussage. Hersteller-Bootblobs werden nicht in Git eingecheckt.
6. Quellprüfung und ausdrückliche Releasefreigabe erfolgen vor Tag/Veröffentlichung. Baurezepte veröffentlichen nicht automatisch.

Die Xorg-/Weston-Ausgabe am angeschlossenen HDMI des Prototyps wurde gesondert abgenommen. Minimal v1 bestand anschließend nativen eMMC-Erststart und Basisprüfung; minimized/SD, zusätzliche zugesagte Prüfumfänge und Firmware-Herkunft bleiben offen. Downloads weisen verbliebene Grenzen zutreffend aus.

Imagekandidat 1.0.1 ergänzt selbst hinterlegte Root-SSH-Schlüssel und lokal installierte APT-Kernelpakete. Physischer Start und Paketupdate auf einen anderen Kernel bleiben offen; die Abnahme von 1.0.0 deckt diese Änderungen nicht ab.
