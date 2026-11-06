# U3-Bootfirmware: Herkunft und Lizenzprüfung

[English](BOOT-FIRMWARE.md)

Geprüft am 6. November 2026. Die Startkette lautet `Exynos-iROM -> BL1 -> BL2 / TrustZone -> U-Boot -> Linux -> Ubuntu`. BL1 lädt die nächste Stufe, BL2 initialisiert früh Board und Arbeitsspeicher, TrustZone unterstützt die abgesicherte Prozessorwelt. Diese Teile sind vom Linuxkernel und Ubuntu-Dateisystem getrennt.

## Genaue Herkunft

Die gepinnte [U-Boot-U3/X2-Anleitung](https://github.com/u-boot/u-boot/blob/v2026.10/doc/README.odroid#L25-L32) verlinkt [boot.tar.gz](https://odroid.in/guides/ubuntu-lfs/boot.tar.gz). Archiv: 174080 Bytes, SHA256 `e0db737d9e49f937425e4778b0ab892623bcc389d7c26329ba2e97ae7bb475c4`.

| Gespeicherte Imagekomponente | Bytes | SHA256 |
|---|---:|---|
| BL1 | 15360 | `0fcf68a3ff3e47af7c6d91103d5797e4aefbefd32b1d267daff69eb6e69d2a84` |
| BL2 | 14848 | `7b1bab8c9ee7d495ab75b2e0a7a0c6295c13f06c86320c25ba379f47d0ec3b57` |
| TZSW | 159744 | `777e0efdd626863b2a6e83cd24b42ae028158aecbfec7843dad00f1b458958c3` |

`boot/E4412_S.bl1.HardKernel.bin` und `boot/E4412_S.tzsw.signed.bin` stimmen genau überein. Die ersten 14848 Bytes von `boot/bl2.signed.bin` entsprechen BL2; die restlichen 1536 Bytes sind null. Mit der folgenden nullgefüllten Imagelücke ergibt das die vollständige offizielle 16384-Byte-BL2-Datei, SHA256 `8f459e654ec4c1a33185ba3f8e04a13da8c6def79362948a6648f96c48897015`. Es wurde kein von null verschiedener Inhalt weggelassen.

## Verbleibender Nachweis

Das Archiv enthält drei Bootbinärdateien, einen älteren U-Boot und `sd_fusing.sh`, aber keine gesonderte Binärlizenz. Das Skript trägt einen Samsung-GPL-2-Hinweis. Öffentliche Downloadverfügbarkeit und Skripthinweis werden nicht als Weitergabe-/Quellaussage für benachbarte Binärdateien behandelt. In den geprüften Materialien wurde keine ausdrückliche Weitergabeerlaubnis für diese genauen Dateien festgestellt; die Quellzuordnung des älteren signierten BL2 bleibt offen. Das beschreibt einen fehlenden Nachweis und entscheidet weder, dass Weitergabe verboten ist, noch dass alle drei Dateien proprietär sind.

Hardkernels [XU4-Diskussion](https://github.com/hardkernel/u-boot/issues/49#issuecomment-464464173) und [C2-Erlaubnis](https://github.com/hardkernel/u-boot/issues/39#issuecomment-296126525) betreffen andere Boards; sie werden nicht als U3-Freigabe übertragen. Die geprüften [Website-/Bestellbedingungen](https://www.hardkernel.com/agreement/) enthalten keine festgestellte U3-Firmwarefreigabe. Unser neues U-Boot-Quellrelease identifiziert nicht die Quellen des älteren BL2.

Nach den Projektbedingungen bleiben vollständige Image-ZIPs und das boot0-Reparaturpräfix unveröffentlicht, bis passende Bedingungen und Quellabdeckung dokumentiert sind. Kernel-DEBs enthalten diese Bootbinärdateien nicht und sind über signiertes APT verfügbar. Ein separat umgesetzter Download-Bausatz könnte diese Komponenten auslassen und lokal aus einer berechtigt verfügbaren Referenz ergänzen; dafür wären genaue Zusammensetzungsprüfung und klare Anleitung nötig. Das geprüfte vollständige IMG wird nicht stillschweigend durch ein anderes Format ersetzt.
