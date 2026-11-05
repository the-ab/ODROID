# GIC alias observation, revision 25

[Deutsch](README.de.md)

Private candidate `7.3.1-odroidu3-v25` extends [v24](../7.3.1-gic-order-v24/README.md). It adds a read-only control to the bounded failure observer; it is not a proposed functional interrupt fix. The full kernel and package checks passed; the transition boot and one pure warmboot passed. Repeated stability qualification remains pending.

A native healthy-v17 control pinned its reader successively to each of four CPUs and read all four documented Exynos GIC aliases, in three rounds. All 48 rows returned shared INTID90/109 priority words `a0a0a0a0`, target words `01010101` and configuration words `55555555`. Private target words followed the selected bank (`01`, `02`, `04`, `08` per byte) independently of the observing CPU. Both UART markers were received, and subsequent module/boot/timer/journal checks remained healthy. Thus normal cross-CPU/cross-alias access did not reproduce v24's late zero priority words. The healthy control alone does not establish failure-time register corruption, security-state changes or the stalled instruction.

V25 captures shared enable/pending/active words and INTID90/109 attributes through **each** validated distributor alias. It records each alias's TYPER/IIDR and the observing CPU before and after the reads. An individual implementation-range gate requires coverage of INTIDs32–159; an invalid view is marked and its shared payload is skipped. Existing bank0 output is retained only for a valid bank0 view. `U3IRQALIAS` records distinguish the additional observations from legacy output.

Snapshots complete before console output. Fixed snapshot buffers are serialized by the existing report-admission guard, reducing IRQ-stack pressure; no cross-CPU calls, new timers or allocation occur in the observer. The three-completed-report budget is unchanged. Only the observer source changes from v24: the other 13 patched files, IAR diagnostic barriers, device tree, voltages, I²C driver and server profile remain unchanged. No MMIO resource, IAR/EOI access, priority/target/mask write, Secure/debug access or boot firmware change is added. Offsets follow the pinned Linux `arm-gic.h` and [Arm IHI0048B, chapter4](https://documentation-service.arm.com/static/5f8ff21df86e16515cdbfafe).

```sh
python3 check-alias.py --observer /path/to/patched/linux/arch/arm/mach-exynos/odroid-u3-irqdiag.c
```

The test compiles the actual capture helper with strict read-only stubs and checks 128 combinations of alias and implementation range. It checks that invalid ranges skip shared reads and that valid reads stay in the selected alias, with exact documented offsets. Inspect ARM compilation and stack usage separately. Before native testing, retain the exact normal v17 boot/state and reinstall package, refresh board/media identity, and adapt the boot/power observers to the Pi UART capture. Stop the bounded series at its first failure and secure complete diagnostics before recovery. No APT/image promotion follows from these source checks.

The observer also compiled without warnings against the existing v24 Kbuild headers/configuration (the observer object uses the same runtime configuration). Reported stack usage of `u3_diag_dump` is 128 bytes with serialized fixed capture buffers. This isolated object check does not link or boot a v25 kernel.

The complete build additionally detects `CC_CAN_LINK=y` and `ARCH_CC_CAN_LINK=y` after ARM userspace development headers became available on the build host. The pinned profile records these two compiler-link capability probes. The remaining configuration is unchanged apart from the revision suffix; these probes do not enable a new runtime server feature.

Native results (2026-11-05): 351 modules/configuration matched; all four timers advanced, audit lost no records, and journal/services/taint checks were clean. Initial alias snapshots were complete and valid on both boots. Full-diagnostic systemd readiness took 40.289 and 39.906 seconds. One pure warmboot is not a stability proof or an identified fix. No public binary promotion.
