# U3 GIC diagnostic revision 8

[Deutsch](README.de.md)

`7.3.1-odroidu3-v8` is a private diagnostic candidate based on the pinned v3 server profile. It adds `ODROID-U3 GICDIAG` output for the original CPU-mask decision, logical CPU/MPIDR, distributor-bank offset, control/type/ID/group state and private IRQ target registers. A snapshot before distributor disable is printed after the original mask read, avoiding a printk delay before that first decision. The mask decision, CPU map and routing writes are unchanged; no interrupt-acknowledge or EOI register is read.

A full UART capture on 2 November 2026 reproduced a v3 warm-start failure with two zero-mask warnings before SMP startup and an incomplete RCU Tasks Trace self-test. The same v3 kernel and arguments cold-booted without those warnings. This revises the earlier assumption that v3 was a reliable hardware fallback. It does not prove a firmware, kernel or electrical root cause.

Use only for controlled diagnosis with the matching original boot-file backup and local UART logging. No boot0, persistent U-Boot environment or eMMC setting is changed. Extra output changes timing and does not establish release acceptance. Default board/image/APT profiles remain v3; this candidate is not promoted or automatically published. Build/runtime results belong in the private diagnostic evidence until qualification.
