# U3 deferred GIC diagnostic revision 11

[Deutsch](README.de.md)

Private candidate `7.3.1-odroidu3-v11` extends the v10 observer with `odroid_u3_gic_defer=1`. It retains the original GIC target-register read loop, zero-mask warning, distributor initialization and returned mask. Immediately after the original warning, a small opt-in helper stores the first two results for each CPU in that CPU's RAM slots. It adds no early MMIO reads, controller writes, logging, locks or inter-CPU calls. Added code and RAM stores can still affect timing; this is a diagnostic, not a correction.

An early initcall, after SMP startup, prints `U3GICDEFER software-map=...` and the saved slots. Bit8 (`0x100`) marks a recorded result: `100` means a real zero mask, `101` means mask1, and `000` means unused. On this single-GIC U3 boot path, CPU0's first call is distributor initialization and its second call is CPU-interface initialization. The output distinguishes a transient initial zero from a zero retained in the software CPU map, provided boot reaches the reporting point. The original warning is neither suppressed nor replaced, and no fallback mask is invented.

The existing optional v10 RCU-stall observer remains available through the separate `odroid_u3_irqdiag=1` argument. Use both arguments with the established serial early console and `loglevel=7` for the first diagnostic test, preserving matching boot-file rollback and local UART recording. Neither observer changes the release default or boot firmware.

Motivation: v10 completed three clean observer-enabled warmboots. With the identical binary and only its observer argument omitted, two warmboots were clean and a third reached userspace despite one early zero-mask warning; CPU0 timer and function-call IPI counters still progressed. The next ordinary v3 boot failed with GIC, PMIC voltage-read and CPU0 RCU/CPU2 soft-lockup reports. Neither a single warning nor its absence is a sufficient boot-health test. A healthy later register snapshot does not identify which early call returned zero. Reading the eight-byte software table through `/proc/kcore` was unavailable in this configuration; no access policy was changed.

Local compilation, the101-capability server gate, unchanged-DTB checks and source/patch checks passed on 2026-11-03. Native boot and the new reporting path remain unverified.
