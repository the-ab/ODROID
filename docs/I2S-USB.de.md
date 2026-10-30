# U3-I2S-/USB-Untersuchung

[English](I2S-USB.md)

Der gepinnte [Kandidat Revision 6](../boards/u3/kernel-candidates/7.3.1-i2s-usb-v6/README.de.md) nutzt Linux `7.3.1-odroidu3-v6` / DEB `7.3.1-7`. Noch keine Übernahme in öffentliche APT-Quelle oder Imagevorgabe; veröffentlichte v3-Pakete und unveränderliche 1.0.2-Images bleiben erhalten.

Die USB-PHY-Bindung macht `vbus-supply` optional, der Treiber forderte die Versorgung jedoch zwingend an. Der Patch nutzt die optionale Regulator-API, akzeptiert ausschließlich ENODEV als fehlende Versorgung und reicht echte Fehler/Probe-Verzögerung weiter. Keine erfundene Versorgung und keine Verbindung der gemeinsamen PHY mit der separat geschalteten OTG-Schiene. USB-Ethernet, Hub und HID werden nativ erkannt. Je 16 MiB über USB-Ethernet wurden beidseitig mit SHA256 geprüft, ohne RX-/TX-Interfacefehler. Währenddessen stieg RX-dropped um sechs; deshalb keine Behauptung völlig verlustfreier Paketzähler. Unbenutzte USB-Speicher-/OTG-Rollen sind nicht pauschal abgenommen.

Die primären I2S-TX-/RX-Kanäle waren bereits vorhanden. Ein sekundäres Software-Wiedergabe-PCM forderte den primären RX-Kanal zusätzlich an. Der Wrapper fordert nun nur den tatsächlich angebundenen Stream über den DMA-Namen seiner CPU-DAI an; das sekundäre Gerät erhält den Controller als Elternteil. Primärer/alter Pfad bleiben erhalten. Sekundäre Funktionalität wird nicht zur Warnungsunterdrückung deaktiviert. Native DMA-Diagnose zeigt korrekt belegte primäre TX-/RX-Kanäle ohne Doppelanforderung.

Echte Aufnahmeversuche zeigten außerdem den fehlenden Backendpfad und eine falsche Gerätebaum-Verbindung: Mikrofon an Kopfhörersenke/IN1 statt an eigener Mikrofonquelle und dem gewählten IN12-Vorverstärker. Ein eigener Mic-Jack-Knoten verbindet MICBIAS und IN12 mit der Aufnahme. DAPM schaltet Versorgung, Vorverstärker, ADCs und I2S-Aufnahme nun tatsächlich ein.

Der Exynos-HDMI-Sender meldete zusätzlich fälschlich eine Aufnahmefähigkeit. Im gemeinsamen Multi-Codec-Backend belegte dieser erfundene Stream die Einzelstream-Reservierung von hdmi-codec und blockierte analogen Voll-Duplex-Betrieb. `no_i2s_capture` beschreibt nun die tatsächliche Senderfähigkeit. Die native interne Codec-Schleife mit 48 kHz/S16/Stereo lieferte 400 Hz links und 600 Hz rechts korrekt zurück: über 99,9999 % Referenztonenergie und vernachlässigbares Übersprechen. Kopfhörerwiedergabe wurde auf v6 beidseitig bestätigt. Das ungeprüfte Headset lieferte bisher nur sehr geringen analogen Pegel; eine physische Sprachaufnahme ist noch nicht abgenommen.

Ressourcenprüfungen führen den tatsächlich geänderten C-Wrapper/Regulatorzweig mit Host-API-Stubs aus, prüfen den kompilierten Aufnahmegraphen und die HDMI-Fähigkeit. ARM-Bau, unverändertes 101-Fähigkeiten-Servergate, 23 Paket-/Bootschutztests und Quellvergleich sind getrennte Nachweise. Alle 95.979 regulären Upstream-Dateien verglichen: 95.970 unverändert, genau neun dokumentierte Änderungen. Die vollständige Konfiguration unterscheidet sich von v3 nur in LOCALVERSION.

Ein Warmstart nach v6 kam nicht zurück: blaue LED dauerhaft an, HDMI schwarz. Derselbe unveränderte Stand bootete nach Stromtrennung mit fehlerfreiem Journal, ohne fehlgeschlagene Units/Taint. Das vorherige Journal zeigt geordnetes Userspace-Herunterfahren, aber keine Diagnose nach Ende der Protokollierung. Warmstartabnahme bleibt offen und blockiert die Veröffentlichung. Daraus folgt kein boot0-Flashbedarf; boot0 blieb bytegleich.

Quellen: [optionale Regulator-API](https://docs.kernel.org/driver-api/regulator.html), exakte Upstream-Bindungs-/Treiberdateien im passenden Linux-Quellpaket und vollständige lokale Patches. Lokale geprüfte Korrekturen, keine behauptete Upstream-Übernahme.

Nachprüfung: Ein zweiter v6-Warmstart scheiterte ebenfalls, nachdem ein Warmstart dazwischen gelang. Zwei Stromtrennungen brachten denselben unveränderten v6-Stand zurück. Hardware-Reset ist bereits dauerhaft aktiviert (`RST_N_FUNCTION=0x01`), pwrseq_emmc ist gebunden, der aktiv niedrige Reset-GPIO korrekt zugeordnet/high. Keine EXT_CSD-Einstellung verändert. Kontrollierter Vergleich mit erhaltenem v3 vorbereitet; Reset-/Frühbootursache noch nicht bewiesen.
