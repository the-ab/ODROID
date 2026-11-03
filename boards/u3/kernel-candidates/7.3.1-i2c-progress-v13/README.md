# U3 I2C interrupt progress diagnostic, revision 13

[Deutsch](README.de.md)

Private candidate `7.3.1-odroidu3-v13` extends v12 after a fully observed warmboot failed despite correct original GIC masks and software CPU map. Three RCU-stall snapshots showed CPU0's local timer count stopped at218, its timer/IPIs pending and shared INTID90 active. The device tree maps INTID90 to I2C0, the controller used by the PMIC. An active interrupt alone does not establish whether the controller, its handler, generic IRQ handling or another dependency caused the stall.

Enable `odroid_u3_i2cdiag=1` together with `odroid_u3_irqdiag=1`, `odroid_u3_gic_defer=1`, the serial early console and `loglevel=7`. Progress is enabled only after the existing observer validates the U3 GIC/MCT resources. The I2C driver binds only the U3 controller at0x13860000 with hardware INTID90. Board/image defaults and boot firmware are unchanged.

The added marks store stage, count, values, task ID and jiffies in RAM. They add no controller reads/writes, acknowledgment, locks, allocation, sleeping, cross-CPU call or serial output to the observed IRQ path. The original41 I2C MMIO operations retain their width, operands and order; wrappers record immediately before/after each original operation. GIC dispatch and generic fasteoi control flow are retained. Added instructions, memory accesses and the diagnostic observer's output can affect timing: this is a measurement candidate, not a fix.

| Channel | Meaning / stages |
|---|---|
|0: GIC |1 after the existing IAR read,2 before generic dispatch,3 after return; original IRQ status is recorded. |
|1: generic fasteoi |1 before descriptor lock,2 after lock,3/4 before/after event dispatch,5/6 before/after unmask/EOI,7 early return,8 final return before automatic lock cleanup. GIC stage3 confirms complete return including cleanup. |
|2: I2C hard IRQ |1 handler entry,2 status available,3/4 before/after next-byte handling,5 return;30 completion entry,31/32 before/after wakeup. |
|2: MMIO stages |100/101 before/after32-bit read,102/103 before/after32-bit write,104/105 byte read,106/107 byte write. `value` is the register offset; `aux` is state before reads or transferred value for other records. |
|3: transfer/clock |1/2 before/after clock enable,3/4 around the normal completed-transfer clock disable,5/6 around other existing process-context clock disables. Values retain return/state information. |

I2C MMIO/completion marks are restricted to hard-IRQ context so a timed-out process cannot overwrite the last stalled handler stage. Transfer marks are separate. Records are approximate last-progress observations, without synchronization or atomic snapshot guarantees; process migration and concurrent updates can leave mixed fields. They are not a total event history.

The existing bounded RCU hook copies these records before console output and prints `U3I2CPROG` lines with its GIC/MCT snapshot. With the feature enabled, root may also read the RAM records through `/sys/kernel/debug/odroid-u3-i2c-progress` (0400); this file does not read hardware registers or change configuration. A process-context bind message reports the mapped Linux IRQ.

Build, package and actual hardware qualification are recorded separately. Preserve matching source/debug ELF, local UART capture and verified v12/v3 boot-file recovery before testing. This profile is not a public kernel/image replacement.

On2026-11-03 the final ARM build completed without compiler warnings; all101 server configuration gates,351 module vermagic checks, unchanged-DTB and source/control-flow checks passed. Native qualification is still pending.
