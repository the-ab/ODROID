# U3-I2C-Fortschritts- und Softlockup-Diagnose, Revision 15

[English](README.md)

Der private Kandidat `7.3.1-odroidu3-v15` übernimmt die RAM-Marken, späte debugfs-Registrierung und geprüfte U3-GIC/MCT-Beobachtung aus [v14](../7.3.1-i2c-progress-v14/README.de.md). Vier v14-Warmstarts bestanden Journal-, Dienst-, CPU-Timer- und Modulprüfungen. Der nächste Warmstart hing vor Userspace mit Softlockups; der RCU-Auslöser lieferte keine Momentaufnahme. Nach manuellem Kaltstart war v14 wieder gesund. Eine Plattformkorrektur ist damit nicht belegt.

V15 ergänzt einen Aufruf an der **vorhandenen Softlockup-Meldestelle**, nach der normalen Aktualisierung der Meldeperiode und vor der printk-CPU-Synchronisierungssperre. Ohne die nach Ressourcenprüfung aktivierte U3-Fortschrittsoption kehrt der Aufruf sofort zurück. Er teilt das bestehende Limit von drei Meldungen mit dem RCU-Hook und gibt `U3IRQDIAG reason=SoftLockup` samt gespeicherten `U3I2CPROG`-Marken aus. Die bestehende atomare Busy-Sperre verhindert gleichzeitige rekursive Aufnahmen. Reguläre Watchdog-Warnung, Schwellen, Backtraces, Taint und Panic-Verhalten bleiben erhalten.

Keine neuen Timer, Sperren, Allokationen, Schlafoperationen, CPU-übergreifenden Anforderungen oder I2C-Registerzugriffe kommen in den beobachteten Fortschrittspfaden hinzu. GIC-Dispatch, generisches Fasteoi und I2C-Treiber sind bytegleich v14. Die Aufnahme liest dieselben GIC/MCT-Statusregister wie die RCU-Beobachtung vor der Konsolenausgabe; keine Interruptquittierung oder Statuslöschung. Messung und serielle Ausgabe können das Timing beeinflussen. RAM-Marken sind ungefähre letzte Phasen, keine atomare Ereignishistorie; Kanal-/Phasenbedeutung siehe v14.

Aktivierung: `odroid_u3_irqdiag=1 odroid_u3_gic_defer=1 odroid_u3_i2cdiag=1 earlycon loglevel=7` mit serieller Konsole. Die schreibgeschützte Ansicht bleibt `/sys/kernel/debug/odroid-u3-i2c-progress`. Andere Architekturen erhalten einen leeren Inline-Aufruf. Board-/Imagevorgaben, DTB und Bootfirmware bleiben unverändert. Passende Quellen/Debug-ELF, lokale UART-Aufzeichnung und geprüfte Bootdatei-/Paketrückfälle vor Tests erhalten. Bau/Paketprüfung und native Abnahme bleiben getrennt; kein öffentlicher Kernel-/Imageersatz.

ARM-Bau am2026-11-03 ohne Compilerwarnungen, alle101 Serverkriterien erfüllt; Link-ELF bestätigt späte debugfs-Reihenfolge und Watchdog-Hook. Paketprüfung und native Abnahme separat.
