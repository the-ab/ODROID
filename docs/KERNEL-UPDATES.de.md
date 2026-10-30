# Kernelupdates über APT

[English](KERNEL-UPDATES.md)

Das gemeinsame Repository [the-ab/deb](https://github.com/the-ab/deb) liegt unter **https://the-ab.github.io/deb/**. Weitere Projekte können eigene Komponenten erhalten. `main` enthält gemeinsame Pakete; `u3` ist für ODROID-U3 reserviert. XU4 benötigt eigene Pakete und Prüfungen. Die getesteten Kernel **7.3.1-1** und **6.12.114-1** sind veröffentlicht. Das Metapaket wählt 7.3.1; 6.12.114 bleibt separat als Rückfall verfügbar. [Paket-/Quellmanifest](https://github.com/the-ab/deb/blob/main/publications/u3-2026-10-30.json) · [Passende Quellen](https://github.com/the-ab/ODROID/releases/tag/u3-kernels-2026.10.30).

Images ab 1.0.1 installieren lokal `the-ab-archive-keyring`, `odroid-u3-kernel-tools`, `linux-image-6.12.114-odroidu3-v1` und das Metapaket `linux-image-odroid-u3`. Die Datei `/etc/apt/sources.list.d/the-ab-odroid-u3.sources` enthält:

```text
Types: deb
URIs: https://the-ab.github.io/deb/
Suites: stable
Components: main u3
Architectures: armhf
Signed-By: /usr/share/keyrings/the-ab-archive-keyring.gpg
```

Signaturfingerabdruck: `E85346CA2461E1FA45AC7C7CD85BC090497CE8B9`. Dieser öffentliche Archivschlüssel prüft Pakete und ist unabhängig von SSH-Anmeldeschlüsseln. Eine Umgehung der Signaturprüfung ist nicht nötig. Ein neueres freigegebenes Metapaket zieht den passenden versionierten Kernel nach:

```sh
sudo apt update
apt-cache policy linux-image-odroid-u3
sudo apt install linux-image-odroid-u3
odroid-kernel status
# Nach erfolgreichem Update zu einem passenden Zeitpunkt neu starten:
sudo reboot
uname -r
odroid-kernel status
sudo journalctl -b -p err --no-pager
```

Die Werkzeuge prüfen U3/Exynos4412, Root auf SD/eMMC-Partition 2 und die passende FAT-Partition 1 unter `/boot`. Vor dem Wechsel der versionierten extlinux-Dateien und der bisherigen `uImage` werden Kernel, DTB, Module und uImage über Prüfsummen/CRCs geprüft. Bootargumente und eine Sicherung der bisherigen Bootdateien bleiben erhalten. Gewöhnliche Schreib-/Rücklesefehler stellen den vorherigen Stand wieder her. Ein anderes Board oder eine nicht eingehängte Bootpartition führen zum Abbruch. Boot0, U-Boot, BL1/BL2 und TrustZone werden nicht aktualisiert. Es erfolgt kein automatischer Neustart.

Laufenden Kernel sowie Kernel für nächsten Start und Rückfall nicht entfernen. Versionierte Kernel sind von APT-Autoremove ausgenommen. Alte Pakete und verwaltete Bootkopien bleiben erhalten; vor Updates den freien Platz prüfen. Geänderte kompilierte Dateien benötigen einen neuen Kernel-Revisionssuffix, damit sie keinen Rückfall unter demselben Verzeichnisnamen überschreiben.

Solange das System erreichbar ist, lassen sich die vorherigen Bootdateien wiederherstellen:

```sh
sudo odroid-kernel rollback
odroid-kernel status
sudo reboot
```

Rollback ist eine lokale Wiederherstellung, keine automatische Rettung nach einem nicht bootfähigen Kernel. Ohne SSH/Konsole ausschalten und das Medium an einem anderen Linux-System einhängen. Auf der Rootpartition `/var/lib/odroid-kernel/state.json` prüfen: Das Verzeichnis aus `previous_snapshot` enthält `uImage`, `extlinux/extlinux.conf` und `BACKUP.json` mit SHA256-Werten. Sicherung und Root-PARTUUID abgleichen, die beiden Dateien in die Bootpartition zurückschreiben, synchronisieren und aushängen. Die passenden `/usr/lib/modules/<release>` auf der Rootpartition erhalten. Stromausfall während Dateisystemänderungen kann eine Reparatur erfordern; gewöhnliches Fehlerrollback garantiert keinen Schutz vor Medienkorruption.

## Bauen und veröffentlichen

Nur committete Rezepte bauen. Das Linux-Artefaktverzeichnis muss zur Boardversion passen und zImage, DTB, config, System.map sowie Module enthalten:

```sh
python3 scripts/build-kernel-debs.py --kernel /pfad/zu/kernel-artifacts \
  --keyring /pfad/zu/deb/the-ab-archive-keyring.gpg --output /neue/paketausgabe
```

In frischen markierten Imageroots vor dem Zusammensetzen `sudo unshare --mount --pid --fork bash scripts/install-kernel-packages.sh ROOTFS PAKETAUSGABE` verwenden. Dort wird die Aktivierung auf dem Bauhost ausdrücklich unterdrückt. Diesen ausschließlich zum Imagebau vorgesehenen Schalter nicht auf installierten Geräten verwenden.

Für ein freigegebenes Kernelrelease das genaue Linux-Upstreamarchiv, vollständigen Patch/Config und Packaging-Quellcommit mit Prüfsummen im Quellrelease bereitstellen. Kernel-DEBs enthalten keine Hersteller-Bootfirmware. Geprüfte gemeinsame DEBs nach `deb/pool/main/`, U3-DEBs nach `deb/pool/u3/` kopieren und alte Versionen erhalten. Mit `scripts/build-apt-repository.py --root /pfad/zu/deb --gpg-home /privater/signaturschluessel --signing-key FINGERABDRUCK` Listen erstellen und signieren, alle Änderungen prüfen und erst danach veröffentlichen. Der private Signaturschlüssel bleibt außerhalb beider Repositories. Images und große Quellarchive gehören in die Produkt-Releases statt in die Pages-Seite. Der Listenbauer begrenzt einzelne DEBs auf 95 MiB; bei weiteren Projekten auch die gesamte GitHub-Pages-Größe beachten.

Lokale Paketinstallation, Signaturprüfung und Datei-Rollbacktests sind geprüft. Ein echtes signiertes APT-Update auf Linux 7.3.1, nativer Start, Rückfall auf 6.12.114 und erneuter Start auf 7.3.1 haben auf dem Test-eMMC bestanden. Kandidaten werden nie automatisch nach `stable` veröffentlicht.

Minimal-Image 1.0.1 hat inzwischen nativ von eMMC gestartet. Installierte Paketversionen/-dateien, laufender v1-Kernel, Board-/Medien-/Payload-Prüfungen des Werkzeugs und APT-Quelle/Schlüssel/Signatur wurden geprüft. Damit sind die im Image vorinstallierten Pakete bestätigt; der anschließende signierte APT-Wechsel mit Rückfall und Rückkehr ist inzwischen ebenfalls geprüft.

Am 30.10.2026 erfolgte 6.12.114 → 7.3.1 → 6.12.114 → 7.3.1 über signierte private APT-Pakete und echte native eMMC-Starts. Abschließend aktiv: 7.3.1-odroidu3-v1. Boot0/boot1, SSH-Schlüssel und vorhandene Quelldateien blieben unverändert. 6.12.114 samt Modulen bleibt Rückfall. Der Test selbst war privat; am 30.10. wurden beide getesteten Kernelpakete nach ausdrücklichem Nutzerauftrag in stable veröffentlicht. Vorhandene 1.0.1-Imageartefakte bleiben unverändert. Versionierte Dateien liegen unter `/boot/odroid-kernels/<release>/`; extlinux wählt sie aus, zusätzlich bedient `/boot/uImage` den bisherigen Startweg. Image-Metadaten beschreiben das ursprüngliche Image; für den aktiven Kernel `uname -r` und `odroid-kernel status` verwenden.

Der 6.12-Kernel lässt sich separat mit `sudo apt install linux-image-6.12.114-odroidu3-v1` installieren. Die Erstinstallation aktiviert ihn für den nächsten Start; ist er bereits installiert, mit `sudo odroid-kernel activate 6.12.114-odroidu3-v1` ausdrücklich auswählen und vor dem Neustart den Status prüfen. Für die zuletzt gesicherten Bootdateien weiterhin `odroid-kernel rollback` verwenden. Das Metapaket folgt 7.3.1 und künftigen freigegebenen Versionen. Boardwerkzeuge setzen Python 3.11 oder neuer voraus; unterstütztes/testetes Ziel ist Ubuntu 26.04 armhf.
