# U3-I2S/USB-Revision 5

[English](README.md)

Kernel `7.3.1-odroidu3-v5`, Paket `7.3.1-6`, behält die signierte Linux-7.3.1-Basis und das vollständige 101-Fähigkeiten-Serverprofil. Der Gesamtpatch behandelt optionale USB-VBUS-Versorgung korrekt, reicht echte Providerfehler weiter, fordert sekundäre I2S-DMA nur für angebundene Streams an und ergänzt das fehlende Aufnahmebackend. Ein eigenes Microphone-Objekt verbindet MICBIAS und den tatsächlichen IN12-Vorverstärker mit dem Headset-Mikrofoneingang; die Kopfhörerwiedergabe bleibt separat.

`scripts/check-i2s-usb-resources.py --kernel-source BUILD` prüft die tatsächliche geänderte C-Ressourcenlogik und den kompilierten Aufnahmegraphen. ARM-Bau und diese Prüfungen ersetzen keine native Boot-/USB-/Wiedergabe-/Aufnahme- und physische Mikrofonabnahme. Revision 4 bestätigte die Ressourcenbehebung, zeigte aber erst im nativen Test den fehlenden Mikrofonquellknoten. V3 bleibt geprüfter Rückfall; das Paket verändert boot0 nicht.
