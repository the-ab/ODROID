# Kernelupdates über APT

[English](KERNEL-UPDATES.md)

Die signierte Paketquelle [the-ab/deb](https://the-ab.github.io/deb/) enthält die gemeinsame Komponente `main` und `u3`. Aktueller Serverkernel: **7.3.1-odroidu3-v3**, Paket **7.3.1-4**, Aktivierungswerkzeuge **1.0.2**. Frühere Kernel-/Metapaketversionen wurden nach Prüfung des Ersatzes auf Nutzerwunsch aus dem aktuellen APT-Pool entfernt. Installierte Rückfallkernel und lokale Sicherungen werden dadurch nicht gelöscht. Quell-Releases und Git-Historie bleiben erhalten. [Paketmanifest](https://github.com/the-ab/deb/blob/main/publications/u3-server-2026-10-30.json) · [Vollständige passende Quellen](https://github.com/the-ab/ODROID/releases/tag/u3-server-kernel-7.3.1-4).

Images ab1.0.1 enthalten Archivschlüssel und Quelle. Image1.0.1 wurde ursprünglich mit6.12.114-v1 ausgeliefert; das frische1.0.2 verwendet7.3.1-v3. Die Imageversion bezeichnet den Ausgangsstand; `uname -r` zeigt den laufenden Kernel.

```text
Types: deb
URIs: https://the-ab.github.io/deb/
Suites: stable
Components: main u3
Architectures: armhf
Signed-By: /usr/share/keyrings/the-ab-archive-keyring.gpg
```

Signaturfingerabdruck: `E85346CA2461E1FA45AC7C7CD85BC090497CE8B9`. Er ist unabhängig von SSH-Anmeldeschlüsseln. Keine Umgehung der Signaturprüfung nötig.

```sh
sudo apt update
apt-cache policy linux-image-odroid-u3
sudo apt install linux-image-odroid-u3
odroid-kernel status
# Nach erfolgreicher Installation bewusst neu starten:
sudo reboot
uname -r
sudo journalctl -b -p err --no-pager
```

Das Metapaket zieht den versionierten Kernel nach. Die Installation prüft U3/Exynos4412, Root auf Partition2, die zugehörige FAT-Partition1 unter `/boot`, Modul-/Payload-Hashes und uImage-CRCs. Neue Dateien liegen direkt unter `/boot`: `vmlinuz-<release>`, `uImage-<release>`, `config-<release>`, `System.map-<release>` und `exynos4412-odroidu3-<release>.dtb`. Extlinux wählt sie; `/boot/uImage` bleibt aktive Legacy-Kopie. Vorhandene gültige Startparameter und alte Bootkopien bleiben erhalten. Das unverschlüsselte ext4-Root benötigt keine Initramfs. Alte `/boot/odroid-kernels/`-Pfade bleiben für vorhandene Rückfallsicherungen nutzbar; neue Aktivierungen verwenden das flache Layout.

Alle neuen Dateien werden vor dem Umschalten geprüft. Gewöhnliche Schreib-/Rücklesefehler stellen die bisherigen Auswahldateien wieder her. Boot0/U-Boot/BL1/BL2/TrustZone werden nicht verändert; kein automatischer Neustart. Freien Bootspeicher beachten. Laufender, nächster und gesicherter Rückfallkernel können nicht entfernt werden; versionierte Kernel sind vor Autoremove geschützt. Geänderter Kernelinhalt bekommt immer einen neuen Board-Suffix.

Letzte gesicherte Auswahl wiederherstellen:

```sh
sudo odroid-kernel rollback
odroid-kernel status
sudo reboot
```

Gezielt einen bereits installierten Rückfall wählen:

```sh
sudo odroid-kernel activate 7.3.1-odroidu3-v2
odroid-kernel status
# Erst nach Prüfung neu starten.
```

Das Beispiel setzt lokal installiertes v2 voraus und verspricht keinen Download. Frische Images enthalten nur ihren ausgelieferten Kernel; vor späteren Updates einen geprüften Rückfall/ein Backup vorbereiten. Rollback ist eine lokale Wiederherstellung, keine automatische Rettung bei fehlgeschlagenem Boot. Ohne SSH/Konsole ausschalten und das Medium an einem anderen Linuxsystem einhängen. `/var/lib/odroid-kernel/state.json` nennt `previous_snapshot`; darin liegen `uImage`, `extlinux/extlinux.conf` und `BACKUP.json`. Hashes und Root-PARTUUID prüfen, die beiden Auswahldateien nach Boot zurückkopieren, synchronisieren und aushängen. Passende Module behalten. Stromausfall/Medienfehler können weiterhin externe Wiederherstellung erfordern.

Echte signierte APT-Tests bestanden6.12.114→7.3.1-v1→6.12.114→7.3.1-v1, danach frisch zurückgesetzter Ausgangsstand→Server-v2→Server-v3. Rückfalldateien und Module blieben erhalten. v3 bestand Docker-, VPN-, Firewall-, Dateidienst- und Sicherheitsprüfungen; siehe [Umfang und Grenzen](SERVER-KERNEL.de.md). Erststarts frischer Images werden separat abgenommen.

## Bauen und veröffentlichen

Nur committete Rezepte und passende Artefakte verwenden. `scripts/build-kernel-debs.py --kernel ARTEFAKTE --keyring OEFFENTLICHER_SCHLUESSEL --output NEUES_ZIEL --tools-version 1.0.2` baut Pakete; explizite gepinnte Profile verwenden zusätzlich `--profile`, `--release`, `--version`. Bereits veröffentlichte gemeinsame Paketversionen behalten exakt ihre Bytes. Kernel-DEBs enthalten keine Hersteller-Bootfirmware.

Frische markierte Imagewurzeln verwenden `sudo unshare --mount --pid --fork bash scripts/install-kernel-packages.sh ROOTFS DEBS`; nur dort wird Aktivierung auf die Imageassemblierung verschoben. Diesen Build-Bypass nicht am installierten Gerät verwenden. Vollständige passende Linuxquellen, Patch/Konfiguration, Paketierungsrezepte, Lizenzen und Prüfsummen mitliefern. Freigegebene DEBs in die richtige Komponente kopieren, mit `scripts/build-apt-repository.py` signierte SHA256/SHA512-By-Hash-Indizes erzeugen und Downloads/Signaturen prüfen. Private Signaturschlüssel bleiben außerhalb von Git. Alte Versionen standardmäßig erhalten; Entfernen braucht den ausdrücklichen Nutzerumfang und geprüften Ersatz. Andere Projektkomponenten bleiben unabhängig. Große Quellen/Images gehören in Produkt-Releases; einzelne DEBs sind hier auf95MiB begrenzt, weitere Pages-Grenzen gelten zusätzlich.

Paket7.3.1-4 ergänzt den fehlenden Entfernungshook bei unverändertem kompiliertem Kernel. Purge entfernt erzeugte Modulindizes und hashgleiche Bootkopien sowie zugehörige inaktive Menüeinträge. Laufende/ausgewählte Rückfallkernel, geänderte Dateien, gemeinsam referenzierte Dateien und fremde Module bleiben geschützt. Ein echter apt-purge-Test eines inaktiven Pakets auf dem U3 bestand. Reste bereits entfernter älterer Pakete brauchen eine einmalige kontrollierte Bereinigung; deren alte Skripte erhalten den Hook nicht rückwirkend.
