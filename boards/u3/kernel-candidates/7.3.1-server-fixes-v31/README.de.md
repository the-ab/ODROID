# Kombinierte U3-Serverkorrekturen, Revision31

[English](README.md)

Dieser Kandidat kombiniert den unveränderten GIC-RAM-Zählerzugriff aus v30 und sieben io_uring-Fixes mit vier geprüften Audio-/USB-Dateien aus v7: streambezogene Samsung-DMA-Zuordnung, physische Mikrofon-/Backendroute, HDMI nur für Wiedergabe und optionale USB-PHY-VBUS-Abfrage mit Weitergabe echter Fehler. Die originale sekundäre I2S-Topologie ohne zusätzliche Elternbeziehung bleibt erhalten.

V30 bestand Übergang und drei Diagnose-Warmstarts sowie einen normalen Start ohne Diagnoseausgabe. Dabei erschienen weiterhin die alten RX-DMA-/VBUS-Warnungen, weil die isolierte Basis die Audio-/USB-Korrekturen noch nicht enthielt. Zehn Warm-/fünf Halt-Kaltstarts sollen daher diesen vollständigen Kandidaten qualifizieren. Keine neuen Registermasken, Secure-/Debug-/Firmwareänderungen, erzwungene IRQ-Anzahl oder globales Abschalten von JUMP_LABEL. XFS-/Serverfunktionen bleiben enthalten. Quellen/Build/Paket, native Abnahme und physische Mikrofon-/Bildabnahme bleiben getrennt. V25 exakter direkter Rückfall, v17 Reserve; keine Release-Abnahme.

Gepinnter24-Datei-Replay, ARM-Build,101-Pflichtfähigkeiten und Tests tatsächlicher C-Ressourcenlogik/kompilierter Audio-DT-Graph bestanden. DTB bytegleich dem funktional getesteten v7. Konfiguration ändert nur LOCALVERSION; Paket-/Hardwarequalifikation noch offen.
