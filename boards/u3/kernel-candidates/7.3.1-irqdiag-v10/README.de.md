# U3-Interrupt-/Timer-Diagnose, Revision 10

[English](README.md)

Privater Diagnosekandidat `7.3.1-odroidu3-v10` auf dem gepinnten v3-Serverprofil. GIC-, MCT-, RCU- und Resettreiber sowie die Konfiguration von v3 bleiben bis auf den Kernel-Versionssuffix unverändert. Ein eigener, fest eingebauter U3-Beobachter wird über das Exynos-Board-Makefile übersetzt. Ohne den ausdrücklichen Bootparameter `odroid_u3_irqdiag=1` bleibt er inaktiv.

Der Beobachter prüft Boardkennung, genaue GIC-/MCT-Ressourcen, CPU-Bankabstand und lokalen Timerinterrupt, bevor er Register abbildet. Während der Core-Initialisierung registriert er eine Probe am vorhandenen Tracepoint `rcu_stall_warning` und erfasst einmal `U3IRQDIAG reason=armed`. Bei einem RCU-Stillstand folgen höchstens drei weitere Aufnahmen auf der meldenden CPU, ohne auf CPU0 zu warten. Es wird keine RCU-Notifier-Option oder absichtliche Warnung mit Taint eingeführt.

Vor jeder Konsolenausgabe erfasst er alle vier privaten GIC-Bänke und CPU-Schnittstellen, lokale MCT-Steuerung/-Status und Linux-Timer-IRQ-Zähler, vier gemeinsame Interruptgruppen sowie den globalen MCT-Zähler. Gelesen werden Konfiguration, Pending-/Active-Status, RPR und HPPIR. IAR/AIAR werden nicht gelesen; Acknowledge-, Clear-, EOI-, Routing-, Timer- und Resetregister werden nicht geschrieben. Der Stall-Callback reserviert keinen Speicher, schläft nicht, wartet nicht auf andere CPUs und erzeugt keine Timer. Die bestehenden Treiber behalten die normale Controllersteuerung.

Für den Test die bereits bewährte serielle Frühkonsole mit `loglevel=7`, geprüfter lokaler UART-Aufzeichnung und passendem Bootdatei-Rückfall verwenden. Die Aufnahme besteht aus mehreren Registerzugriffen und ist kein atomarer Blick über alle CPUs. Tickless Idle kann lokale Ticks regulär anhalten; ein Zähler allein beweist keinen Fehler. Zusätzlicher Code, Registerabbildungen, Lesezugriffe und Ausgabe können das Timing verändern. Dies ist eine Messung, keine Fehlerbehebung oder Releasefreigabe. Öffentliche APT-/Image-Dateien und Bootfirmware werden durch die Profilvorbereitung nicht verändert. Bau und tatsächlicher Hardwarelauf sind getrennt nachzuweisen.

Lokale Übersetzung und die 101 Server-Konfigurationskriterien bestanden am 03.11.2026. Hardwareboot und Aufnahme eines tatsächlichen Fehlstarts sind noch ungeprüft.
