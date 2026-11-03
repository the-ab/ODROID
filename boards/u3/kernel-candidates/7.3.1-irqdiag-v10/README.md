# U3 interrupt/timer diagnostic revision 10

[Deutsch](README.de.md)

Private diagnostic candidate `7.3.1-odroidu3-v10`, based on the pinned v3 server profile. The v3 GIC, MCT, RCU and reset driver sources and configuration remain unchanged except for the kernel release suffix. A separate built-in U3 observer is compiled through the Exynos board Makefile. It is inactive unless the explicit boot argument `odroid_u3_irqdiag=1` is present.

The observer checks the board compatible string, exact GIC/MCT resources, CPU-bank stride and local timer interrupt before mapping anything. During core initialization it registers a probe at the existing `rcu_stall_warning` tracepoint and takes one `U3IRQDIAG reason=armed` snapshot. An RCU stall takes up to three more snapshots on the detecting CPU, without waiting for CPU0. No RCU notifier option or deliberate warning/taint is introduced.

Each snapshot captures all four GIC private banks and CPU interfaces, local MCT control/status and Linux timer IRQ counts, four shared interrupt groups and the global MCT counter before any console output. It reads configuration, pending/active status, RPR and HPPIR; it never reads IAR/AIAR or writes acknowledge, clear, EOI, routing, timer or reset registers. The stall callback performs no allocation, sleeping, cross-CPU call or timer creation. Normal controller operations remain with the existing drivers.

Use the established serial early-console arguments with `loglevel=7`, verified local UART recording and matching boot-file rollback. A sample spans several register reads and is not an atomic view across CPUs. Tickless idle can legitimately stop local ticks; a timer count alone does not prove failure. Added code, mapping, reads and output can change timing. This is observation, not a correction or release replacement. Neither public APT/images nor boot firmware are changed by preparing this profile. Build and native outcomes require separate evidence.

Local compilation and the 101-capability server configuration gate passed on 2026-11-03. Native boot and an actual stalled-boot snapshot remain unverified.
