# U3-I2S/USB-Zwischenrevision 4

[English](README.md)

Kernel `7.3.1-odroidu3-v4`, Paket `7.3.1-5`, verwendet die signierte Linux-7.3.1-Basis und unveränderte 101-Fähigkeiten-Serverkonfiguration. Der native eMMC-Test beseitigte Dummy-Regulator- und doppelte I2S-RX-Anforderung. USB-Ethernet übertrug je 16 MiB mit SHA256-Prüfung; Kopfhörerwiedergabe wurde beidseitig bestätigt.

Mit ergänztem Backend ließ sich die Aufnahme öffnen, enthielt aber nur Nullen. DAPM zeigte den Mikrofoneingang als Kopfhörer-Senke und die Verbindung an IN1 statt am gewählten IN12-Vorverstärker; ADC/Bias blieben aus. Diese Zwischenrevision wurde nicht veröffentlicht. Weiterarbeit in [Revision 5](../7.3.1-i2s-usb-v5/README.de.md). Exakter Quellstand und Testpaket bleiben nachvollziehbar erhalten.
