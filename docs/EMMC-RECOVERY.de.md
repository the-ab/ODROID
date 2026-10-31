# ODROID-U3: eMMC-boot0 reparieren

[English](EMMC-RECOVERY.md)

Dieser Weg ist für ein Modul gedacht, das über den eMMC-auf-microSD-Adapter im SD-Steckplatz des U3 startet, am nativen eMMC-Anschluss aber nicht. Ein normales Image-Schreiben über einen SD-/USB-Leser aktualisiert üblicherweise nur den **Benutzerbereich** des eMMC. Die native U3-Bootkette liegt in einer separaten Hardwarepartition, unter Linux `mmcblkNboot0`.

Die Aktualisierung bleibt auf diesem Modul gespeichert. Erneutes normales Schreiben des Benutzerbereichs erhält boot0. Das neue Image muss weiterhin passende U3-Bootdateien enthalten. Beschrieben wird wiederbeschreibbarer Flash; SoC-Sicherungen werden nicht verändert.

## Dateien und unterstützter Zugriffsweg

Das Image-ZIP enthält IMG, `BUILD-MANIFEST.json`, `u3-boot0-prefix.bin`, diese Anleitung und `u3-emmc-boot0.py`. Vor dem Entpacken die ZIP-Prüfsumme kontrollieren. Der Präfix muss **1.240.064 Bytes** groß sein; seine genaue SHA256 steht im Manifest.

Das Python-Werkzeug läuft **auf dem U3**, während dasselbe eMMC über den Adapter direkt im U3-SD-Steckplatz gestartet ist. Ein USB-Leser mit `/dev/sdX` stellt die Hardware-Bootpartitionen meist nicht bereit. Das Werkzeug verweigert andere Boards, SD-Karten, `/dev/sdX`, abweichende CIDs und Firmware-Schreibzugriffe beim nativen eMMC-Start. Die U3-Dateien niemals auf einem XU4 verwenden.

Der abgesicherte Schreibweg verlangt die geprüfte Konfiguration: boot0 mit Boot-Bestätigung gewählt (`PARTITION_CONFIG & 0xf8 == 0x48`), 4-Bit-Legacy-Bootbus (`BOOT_BUS_WIDTH == 0x01`) und keinen Boot-Schreibschutz. Diese Einstellungen werden nicht automatisch geändert. Abweichungen müssen gesondert untersucht werden.

## 1. Dasselbe Modul über den SD-Adapter starten

1. Das vollständige Projekt-IMG über Adapter und Image-Schreiber in den **Benutzerbereich** des eMMC schreiben.
2. Bei getrennter Stromversorgung den nativen eMMC-Anschluss leer lassen und das Testmodul mit Adapter in den U3-SD-Steckplatz einsetzen.
3. Starten, als `odroid` mit Passwort `odroid` anmelden und Werkzeug, Präfix und Manifest in ein Arbeitsverzeichnis auf dem U3 kopieren.
4. Karte und Root-Dateisystem feststellen:

```sh
findmnt -n -o SOURCE,FSTYPE /
lsblk -p -o NAME,SIZE,TYPE,MOUNTPOINTS
```

Beim geprüften Adapterstart lag Root auf `/dev/mmcblk2p2`; die **gesamte Karte** hieß `/dev/mmcblk2`. Die Nummerierung am eigenen laufenden System prüfen. Das folgende Beispiel verwendet dieses festgestellte Gerät:

```sh
device=/dev/mmcblk2
sudo python3 u3-emmc-boot0.py inspect --device "$device"
```

`root_on_selected_card: true`, `sd_adapter_path: true`, Modulname, CID, Bootpartitionsgröße und Konfiguration kontrollieren. Ein geprüftes SDW16G-Modul hat jeweils 4 MiB boot0/boot1. Der Präfix ersetzt ausschließlich die ersten 1,24 MB von boot0.

## 2. Eigenes Backup erstellen und extern sichern

```sh
cid=$(cat "/sys/class/block/${device##*/}/device/cid")
backup_dir="$HOME/emmc-backups/$cid-$(date +%Y%m%d-%H%M%S)"
sudo python3 u3-emmc-boot0.py backup \
  --device "$device" --backup "$backup_dir"
```

Das Werkzeug sichert und prüft durch erneutes Lesen:

- vollständige `boot0.bin` und `boot1.bin`;
- die ersten 16 MiB des Benutzerbereichs einschließlich Partitionstabelle und SD-Bootkette;
- rein lesend ermittelte EXT_CSD-Rohdaten sowie `BACKUP.json` mit Modulidentität, Größen und SHA256-Werten.

Das ist ein Boot-Backup, keine Sicherung aller Betriebssystem- und Nutzdaten. Vor dem Firmware-Schreiben das gesamte Backup **vom Modul herunterkopieren**, beispielsweise auf dem PC:

```sh
scp -r odroid@HOST:~/emmc-backups ./
```

Die CID aus dieser Adapter-Sitzung verwenden. Kein Backup oder keine CID eines anderen Moduls übernehmen; auch nicht ungeprüft die Ausgabe eines anderen Controllers kopieren.

## 3. Präfix prüfen und anwenden

Im Verzeichnis mit entpacktem Manifest und Präfix:

```sh
payload_sha256=$(python3 -c 'import json; print(json.load(open("BUILD-MANIFEST.json"))["emmc_boot0_payload"]["sha256"])')
printf '%s  %s\n' "$payload_sha256" u3-boot0-prefix.bin | sha256sum -c -
wc -c u3-boot0-prefix.bin

sudo python3 u3-emmc-boot0.py apply \
  --device "$device" --backup "$backup_dir" \
  --payload u3-boot0-prefix.bin --payload-sha256 "$payload_sha256" \
  --confirm-cid "$cid"
```

Dieser Aufruf gibt das Firmware-Schreiben auf das identifizierte Modul ausdrücklich frei. Das Werkzeug prüft Backup und Ausgangszustand, entsperrt vorübergehend `force_ro`, öffnet boot0 exklusiv, schreibt nur den Präfix, führt `fsync` aus und vergleicht die **vollständige** boot0-Partition. Ihr restlicher Inhalt, boot1, der Boot-Präfix im Benutzerbereich und die dauerhafte Bootkonfiguration müssen unverändert bleiben. Ein bereits passender Stand wird nicht erneut geschrieben.

Abgefangene Schreib-/Rücklesefehler stellen den ursprünglichen Präfix wieder her. Übliche Abbruchsignale werden bis zum Ende der kurzen Schreib-, Prüf- und Sperrtransaktion zurückgestellt. Stromausfall oder hartes Beenden lassen sich nicht durch Software absichern. Die SD-Bootkette im Benutzerbereich wird bei dieser Aktion nicht beschrieben.

Die Erfolgsausgabe enthält `force_ro: "1"`, `boot1_unchanged: true`, `boot_configuration_unchanged: true` und die neue vollständige boot0-SHA256. Im Backup-Verzeichnis entsteht `APPLY-*.json`. Das Werkzeug startet nicht automatisch neu.

## 4. Nativ von eMMC testen

```sh
sudo poweroff
```

Herunterfahren abwarten, 5-V-Versorgung trennen, SD-Adapter entfernen und das Modul nativ aufstecken. SD-Steckplatz leer lassen und einschalten. Heartbeat-LED, DHCP-/SSH-Anmeldung und anschließend prüfen:

```sh
findmnt -n -o SOURCE,FSTYPE /
uname -r
systemctl --failed
sudo journalctl -b -p err --no-pager
odroid-fan status
```

Natives Root lag beim geprüften U3 auf `/dev/mmcblk0p2`. Tatsächliche Zuordnung kontrollieren und die Beispielnummer nicht voraussetzen.

## Gesicherten Stand wiederherstellen

Falls erforderlich, ausschalten und dasselbe Modul erneut über den SD-Adapter starten. Eigenes Backup und die vollständige `after_sha256` aus der zugehörigen `APPLY-*.json` verwenden:

```sh
sudo python3 u3-emmc-boot0.py restore \
  --device "$device" --backup "$backup_dir" --confirm-cid "$cid" \
  --expect-current-sha256 VOLLSTAENDIGE_AFTER_SHA256_AUS_DEM_APPLY_PROTOKOLL
```

Ein unbekannter Firmwarestand oder veränderter Restbereich wird abgewiesen. Restore schreibt nur den gesicherten Präfix, prüft die gesamte Partition, erhält boot1/Konfiguration und aktiviert den Leseschutz erneut. Ein nach einer früheren Reparatur erstelltes Backup enthält entsprechend den reparierten Stand; Restore ist kein Werksreset. Das externe Backup für manuelle Wiederherstellung nach unterbrochenen oder unbekannten Zuständen aufbewahren.

## Unterschiedliche Offsets

Die [offizielle U-Boot-ODROID-Anleitung](https://github.com/u-boot/u-boot/blob/v2026.10/doc/README.odroid) beschreibt folgende **512-Byte-Sektoren**:

| Baustein | Start SD/Benutzerbereich | Start eMMC-boot0 | Reservierte Sektoren |
|---|---:|---:|---:|
| BL1 | 1 | 0 | 30 |
| BL2 | 31 | 30 | 29 |
| U-Boot | 63 | 62 | 2048 |
| TrustZone | 2111 | 2110 | 312 |

Der Präfix umfasst boot0-Sektoren 0–2421 einschließlich Zwischenräumen. Niemals das vollständige IMG nach boot0 schreiben oder eine gesamte 4-MiB-Partition mit einem kürzeren Präfix überschreiben. Das Werkzeug erhält den modulspezifischen Restbereich.

Für diesen Adapterweg ist kein UART erforderlich. Bei einer separat verwendeten seriellen Konsole gilt: U3-UART mit **1,8 V**, 115200 8N1.

Der Präfix startete nach modulspezifischem Backup und geprüfter Aktualisierung auf zwei 16-GB-SDW16G-Modulen nativ. Für das generische Werkzeug liegen lesende Hardwareprüfungen und dateibasierte Fehler-/Rollback-Tests vor. Andere Module und Bootkonfigurationen sind dadurch nicht automatisch abgenommen. Siehe [Hardwarestand](HARDWARE.de.md) und [Releaseanforderungen](RELEASES.de.md).
