# Interrupt and idle progress candidate, revision 17

[Deutsch](README.de.md)

Private `7.3.1-odroidu3-v17` extends [v16](../7.3.1-a9-errata-v16/README.md)'s bounded RAM diagnostics. v16 passed four consecutive same-kernel warmboots, then failed on the fifth. Its last I²C IRQ markers show handler return; they do not establish CPU0's eventual program counter. The errata options alone did not resolve the hang.

Seven per-CPU channels appear in `odroid-u3-i2c-progress` and the bounded RCU/soft-lockup snapshots. Existing channels 0–3 remain compatible. Channel 4 separates process-context I²C MMIO/completion markers from IRQ channel 2. Channel 5 records the global GIC path: 10 before IAR read, 11 after it, 12 before dispatch, 13 after dispatch, 14 spurious interrupt, 15 handler return. Channel 6 records ARM fallback idle entry (1) and return (2). Transfer channel 3 additionally records set-master, message start, completion wait, wait-idle and cleanup boundaries (10–19).

This adds RAM stores around existing operations. The original MMIO accesses, IRQ acknowledgment/EOI logic, waits and idle calls remain in place. No new register access, timer, lock, cross-CPU request or hardware workaround is introduced. The same three Cortex-A9 errata options and all 101 server criteria are retained; only the release suffix changes in the configuration. The DTB remains byte-identical to v16. Instrumentation may affect timing; records are approximate and not an atomic CPU snapshot.

The cumulative patch reapplies to 13 original source files. Removing only the new annotations restores v16's modified code exactly. Source/build/package checks and native hardware qualification are separate. Keep matching debug ELF, payload and UART evidence. This diagnostic candidate does not change the image default and must not be published as an accepted fix.
