# U3-TUN-Statistikschutz, Revision32

[English](README.md)

V31 bestand zehn reine Warmstarts und fünf kontrollierte Halt-Kaltstarts mit normalen Releaseparametern. Docker-, WireGuard-/OpenVPN-, Firewall-, Dateidienst-, Sicherheits- und interne Codec-Datentests liefen durch; OpenVPN löste jedoch eine Lockdep-IRQ-Kontextwarnung bei den TUN-Prozessorstatistiken aus. Damit ist die Endqualifikation trotz erfolgreicher Übertragungen nicht bestanden. Ein tatsächlicher Deadlock wurde nicht beobachtet. Im NFS-Test fehlte außerdem der Recovery-Daemon; dieses Fixtureproblem wird getrennt korrigiert.

Der32-Bit-u64_stats-Vertrag im signierten Upstream verlangt Schreibschutz gegen Interruptkontexte. Drei TUN-Zählerabschnitte im Prozesskontext sperren bislang nur die Präemption; ein vorhandener XDP-Sender schreibt dieselben Statistiken mit gesperrten Bottom Halves. Die gemeinsame Netzwerk-Statistik-Lockklasse umfasst auch USB-Softirq-Abschlüsse, passend zur aufgezeichneten Warnung. Dieser lokale Kandidat ändert genau die drei kurzen Zählerabschnitte auf local_bh_disable()/local_bh_enable(); Kopier- und Paketoperationen bleiben außerhalb. Alle v31-Fixes und die Konfiguration außer LOCALVERSION bleiben erhalten. Lockdep bleibt aktiv. Der genaue frühere GIC-Textpatch-/Cache-Mechanismus bleibt unbewiesen.

Paketprüfung, frische native Warnungs-/Lockdep-Prüfung und normale Boot-/Dienstqualifikation stehen aus. V25 bleibt exakt direkt, v17 Reserve; v31-Belege/Debug-/Reinstallbytes sind gesichert. Keine Firmwareänderung oder öffentliche Binär-/APT-/Main-Promotion.

Gepinnter25-Datei-Replay, aufgelöste Konfiguration,101-Pflichtfähigkeiten und ARM-Kernel-/Modulbau bestanden. Die DTB bleibt bytegleich v31. Paket-/Hardwareprüfung steht weiterhin aus.
