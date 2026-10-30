# U3-I2S/USB-Revision4

[English](README.md)

Release7.3.1-odroidu3-v4/Paket7.3.1-5 verwendet dieselbe signierte Linux7.3.1-Basis mit vollständigem101-Fähigkeiten-Serverprofil. Der Gesamtpatch behält die fünf bisherigen Boardänderungen und korrigiert die optionale VBUS-Anforderung, die streambezogene DMA-Zuordnung/Elternbeziehung des sekundären I2S-PCM und den fehlenden MAX98090-Aufnahmepfad im alten U3-Audiographen. Keine pauschale Logunterdrückung, erfundene Versorgung oder entfernte Audiofunktion.

Primäres TX/RX waren auf v3 vorhanden; die doppelte RX-Warnung kam vom ungenutzten sekundären Wiedergabe-PCM. Ein echter Aufnahmeversuch zeigte zusätzlich den fehlenden Backendpfad. Ressourcenlogik-Prüfung und ARM-Build gehen der getrennten nativen USB-/Wiedergabe-/Aufnahmeprüfung voraus. Geprüfte v3-Pakete samt zur aktuellen Rootidentität passendem Backup als Rückfall behalten. Quellkonfiguration allein bestätigt keine Hardwareabnahme.
