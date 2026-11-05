# Kombinierte U3-Serverkorrekturen, Revision31

[English](README.md)

Dieser Kandidat kombiniert den unveränderten GIC-RAM-Zählerzugriff aus v30 und sieben io_uring-Fixes mit vier geprüften Audio-/USB-Dateien aus v7: streambezogene Samsung-DMA-Zuordnung, physische Mikrofon-/Backendroute, HDMI nur für Wiedergabe und optionale USB-PHY-VBUS-Abfrage mit Weitergabe echter Fehler. Die originale sekundäre I2S-Topologie ohne zusätzliche Elternbeziehung bleibt erhalten.

V30 bestand Übergang und drei Diagnose-Warmstarts sowie einen normalen Start ohne Diagnoseausgabe. Dabei erschienen weiterhin die alten RX-DMA-/VBUS-Warnungen, weil die isolierte Basis die Audio-/USB-Korrekturen noch nicht enthielt. Die unten dokumentierte Bootqualifikation nutzt daher diesen vollständigen Kandidaten. Keine neuen Registermasken, Secure-/Debug-/Firmwareänderungen, erzwungene IRQ-Anzahl oder globales Abschalten von JUMP_LABEL. XFS-/Serverfunktionen bleiben enthalten. Quellen/Build/Paket, native Abnahme und physische Mikrofon-/Bildabnahme bleiben getrennt. V25 exakter direkter Rückfall, v17 Reserve; keine Release-Abnahme.

Gepinnter24-Datei-Replay, ARM-Build,101-Pflichtfähigkeiten und Tests tatsächlicher C-Ressourcenlogik/kompilierter Audio-DT-Graph bestanden. DTB bytegleich dem funktional getesteten v7. Konfiguration ändert nur LOCALVERSION; Paket und351 Module sind geprüft.

Am2026-11-05 bestand dieses exakte Binary den normalen Erststart, anschließend10 reine Warmstarts und5 kontrollierte Halt-Kaltstarts am nativen eMMC-Anschluss. Diagnose-Bootflags waren ausgeschaltet. Bei jedem Start liefen die Timer aller vier CPUs weiter;351 Modulhashes stimmten, Kernel-Fehlerjournal und fehlgeschlagene Dienste waren leer, Auditverlust und Taint jeweils0. Die alten I2S-RX-DMA- und USB-VBUS-Warnungen blieben aus. Jeder Kaltstart folgte auf ein per UART bestätigtes Halt und mindestens10 Sekunden unabhängig rückgelesenen AUS-Zustand. Vollständige UART-Intervalle und Gesundheits-/Stromnachweise sind privat hashgeprüft gesichert.

Der falsche ursprüngliche GIC-Basiszugriff wurde in v29 aufgezeichnet; der genaue Textpatch-/Instruktionscache-Mechanismus bleibt unbewiesen. Diese begrenzte Bootserie qualifiziert die geprüfte Korrektur mit normalen Parametern, keinen unbegrenzten Dauerbetrieb. Abschließende Server-/io_uring-/Audio-DMA-Regression, frische Images, Firmware-Weitergabeabdeckung und nötige menschliche Erststart-/Peripherieabnahme bleiben getrennt offen. Keine öffentliche Binär-/APT-/Main-Promotion.
