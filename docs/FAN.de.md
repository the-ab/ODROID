# U3-Lüftersteuerung

[English](FAN.md)

Der Thermal-Governor des Kernels regelt den PWM-Lüfter. Vorgabe: **35 / 45 / 55 °C**, beim Abkühlen mit **3 °C Hysterese**. Eigene Lüfter-Trips erhalten die ursprünglichen Schutz- und Drosselstufen der CPU.

| Stufe | Temperatur beim Erwärmen | PWM, 0–255 |
|---:|---:|---:|
| 0 | Unterhalb der ersten Schwelle | 0 |
| 1 | 35 °C | 102 |
| 2 | 45 °C | 170 |
| 3 | 55 °C | 255 |

```sh
odroid-fan status
sudo odroid-fan set 40 50 60
odroid-fan status
```

`set` übernimmt die Stufen sofort und speichert sie für weitere Starts in `/etc/default/odroid-fan`. Erlaubt sind aufsteigende ganze Werte von 30 bis 85 °C mit mindestens 5 °C Abstand. Vorgaben wiederherstellen:

```sh
sudo odroid-fan set 35 45 55
```

Alternativ `FAN_LOW`, `FAN_MEDIUM`, `FAN_HIGH` in der Datei bearbeiten und `sudo systemctl restart odroid-fan.service` ausführen. Ungültige Werte werden abgewiesen. Die CPU-Schutz-Trips werden dabei nicht verändert.

`status` zeigt aktuelle Temperatur, wirksame/gespeicherte Schwellen, Lüfterstufe und PWM. RPM werden in dieser Hardwarekonfiguration nicht gemessen. PWM beschreibt das Tastverhältnis, keine gemessene Drehzahl. Durch die Hysterese bleibt beim Abkühlen eine höhere Stufe zeitweise unterhalb ihrer Einschaltschwelle aktiv.
