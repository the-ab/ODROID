# Installation und erste Anmeldung

[English](INSTALL.md)

Gewünschtes U3-ZIP und zugehörige `.sha256` unter [Releases](https://github.com/the-ab/ODROID/releases) herunterladen. Ein Kandidat ist kein stabiles Release; Releasehinweise und [Hardwarestand](HARDWARE.de.md) beachten.

```sh
sha256sum -c odroid-u3-ubuntu-26.04.1-armhf-minimized-v1.0.1.zip.sha256
unzip odroid-u3-ubuntu-26.04.1-armhf-minimized-v1.0.1.zip
sha256sum -c odroid-u3-ubuntu-26.04.1-armhf-minimized-v1.0.1.img.sha256
```

Für `minimal` die entsprechenden Dateinamen verwenden. Das **vollständige IMG** über einen Image-Schreiber auf die ausgewählte SD/eMMC mit Adapter schreiben. Dabei werden Partitionstabelle und Installation des Ziels überschrieben. Unter Linux zunächst Ziel feststellen und seine eingehängten Partitionen aushängen. `/dev/sdX` ist hier ein Platzhalter für das geprüfte ganze Medium, keine Partition:

```sh
lsblk -p -o NAME,SIZE,MODEL,TYPE,MOUNTPOINTS
sudo dd if=odroid-u3-ubuntu-26.04.1-armhf-minimized-v1.0.1.img \
  of=/dev/sdX bs=4M conv=fsync status=progress
sync
```

Vor Umstecken die Stromversorgung trennen. Nur das vorgesehene Bootmedium einsetzen. Startet eMMC nativ nicht, über den U3-SD-Adapter aber schon, der [boot0-Anleitung](EMMC-RECOVERY.de.md) folgen. Wiederholtes IMG-Schreiben des Benutzerbereichs aktualisiert boot0 nicht.

Ethernet bezieht DHCP. Anmeldung mit **odroid**, Passwort **odroid**; sudo verlangt dieses Passwort. Root-SSH erlaubt selbst hinterlegte öffentliche Schlüssel; Root-Passwortanmeldung bleibt gesperrt. SSH-Hostschlüssel und Maschinenidentität entstehen beim ersten Start neu. Eine Neuinstallation hat entsprechend andere SSH-Fingerabdrücke; die Geräteidentität prüfen, bevor ein alter Vertrauenseintrag ersetzt wird.

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

## Persönlicher Root-Schlüsselzugang

Ab Image 1.0.1 gilt `PermitRootLogin prohibit-password`. Es wird kein autorisierter Schlüssel mitgeliefert. Als `odroid` das Verzeichnis anlegen und den eigenen **öffentlichen** Schlüssel in `authorized_keys` eintragen, jeweils eine vollständige Zeile pro Schlüssel:

```sh
sudo install -d -m 700 -o root -g root /root/.ssh
sudo touch /root/.ssh/authorized_keys
sudo nano /root/.ssh/authorized_keys
sudo chown root:root /root/.ssh/authorized_keys
sudo chmod 600 /root/.ssh/authorized_keys
sudo sshd -t
sudo sshd -T | grep '^permitrootlogin '
```

Danach vom eigenen Rechner mit dem zugehörigen privaten Schlüssel verbinden: `ssh -i /pfad/zum/privaten_schluessel root@HOST`. Zum Hinzufügen eines Schlüssels muss SSH nicht neu gestartet werden. Das Root-Passwort bleibt gesperrt. OpenSSH kann den gleichbedeutenden Wert `without-password` ausgeben.

Image 1.0.0 verwendete `PermitRootLogin no`. Dort ermöglicht eine frühere Datei `/etc/ssh/sshd_config.d/00-local-root-key.conf` mit `PermitRootLogin prohibit-password` nach `sudo sshd -t && sudo systemctl reload ssh` den Schlüsselzugang. OpenSSH nutzt den ersten Wert; eine spätere Zeile der Hauptdatei überschreibt einen früheren Include-Eintrag nicht.

Die signierte Projekt-APT-Quelle ist unter [Kernelupdates](KERNEL-UPDATES.de.md) beschrieben. Ubuntu-Pakete stammen weiterhin aus Ubuntu.
