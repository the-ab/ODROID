# Installation und erste Anmeldung

[English](INSTALL.md)

Gewünschtes U3-ZIP und zugehörige `.sha256` unter [Releases](https://github.com/the-ab/ODROID/releases) herunterladen. Ein Kandidat ist kein stabiles Release; Releasehinweise und [Hardwarestand](HARDWARE.de.md) beachten.

```sh
sha256sum -c odroid-u3-ubuntu-26.04.1-armhf-minimized-v1.0.0.zip.sha256
unzip odroid-u3-ubuntu-26.04.1-armhf-minimized-v1.0.0.zip
sha256sum -c odroid-u3-ubuntu-26.04.1-armhf-minimized-v1.0.0.img.sha256
```

Für `minimal` die entsprechenden Dateinamen verwenden. Das **vollständige IMG** über einen Image-Schreiber auf die ausgewählte SD/eMMC mit Adapter schreiben. Dabei werden Partitionstabelle und Installation des Ziels überschrieben. Unter Linux zunächst Ziel feststellen und seine eingehängten Partitionen aushängen. `/dev/sdX` ist hier ein Platzhalter für das geprüfte ganze Medium, keine Partition:

```sh
lsblk -p -o NAME,SIZE,MODEL,TYPE,MOUNTPOINTS
sudo dd if=odroid-u3-ubuntu-26.04.1-armhf-minimized-v1.0.0.img \
  of=/dev/sdX bs=4M conv=fsync status=progress
sync
```

Vor Umstecken die Stromversorgung trennen. Nur das vorgesehene Bootmedium einsetzen. Startet eMMC nativ nicht, über den U3-SD-Adapter aber schon, der [boot0-Anleitung](EMMC-RECOVERY.de.md) folgen. Wiederholtes IMG-Schreiben des Benutzerbereichs aktualisiert boot0 nicht.

Ethernet bezieht DHCP. Anmeldung mit **odroid**, Passwort **odroid**; sudo verlangt dieses Passwort. Root-SSH ist gesperrt. SSH-Hostschlüssel und Maschinenidentität entstehen beim ersten Start neu. Eine Neuinstallation hat entsprechend andere SSH-Fingerabdrücke; die Geräteidentität prüfen, bevor ein alter Vertrauenseintrag ersetzt wird.

```sh
ssh odroid@HOST
passwd
sudo -v
uname -r
df -h /
systemctl --failed
sudo journalctl -b -p err --no-pager
odroid-fan status
```

Root wächst beim ersten Start auf die Mediengröße. Vorgaben sind UTC und `en_US.UTF-8`; eigene Zeitzone mit `sudo timedatectl set-timezone REGION/STADT` einstellen. Mit `sudo poweroff` oder dem unterstützten Taster sauber herunterfahren. Vor dem Umstecken von eMMC die Versorgung trennen.

Ubuntu-Pakete verwenden die normalen Ubuntu-26.04-Updatequellen. Der Board-Kernel stammt aus diesem Projekt und ist kein generisches Ubuntu-Kernelpaket. `minimized` enthält das offizielle Kommando `unminimize` zum Wiederherstellen entfernter Inhalte. `minimal` installiert zusätzlich Ubuntu-Minimal-/Standard-Metapakete und die in `PACKAGES.tsv` ausgewiesenen Administrationswerkzeuge.
