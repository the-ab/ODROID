# Bounded diagnostic report admission, revision 22

[Deutsch](README.de.md)

Private `7.3.1-odroidu3-v22` derives directly from [v17](../7.3.1-idle-gic-progress-v17/README.md). The [v21 polling control](../7.3.1-i2c-poll-v21/README.md) also hung, with I²C0 INTID90 disabled/not active and MMC INTID109 active. Three concurrent watchdog hooks consumed the old report-attempt budget while only one register dump completed. The active interrupt and approximate RAM markers did not establish a stopped CPU instruction or a device-driver cause.

This revision fixes that diagnostic admission defect. A caller first tries the existing nonblocking busy guard. Busy-rejected calls consume no budget; after acquiring the guard, a late report is accepted only if fewer than three have completed. The counter advances after the complete output. A release store publishes this completion before the next caller can acquire the guard. The initial `armed` dump does not consume the three-late-report budget. A `report-complete=N reason=...` footer identifies each finished dump (initial0, late1–3).

Both existing RCU and watchdog hooks share the same admission and completion path. No sleeping, spinning, timer, allocation, cross-CPU request, new MMIO access or hardware workaround is added. Original register reads, I²C/IRQ handling, clocks, idle calls, seven RAM channels and three Cortex-A9 workarounds remain unchanged. The cumulative patch affects the same 13 files; all other 12 files are byte-identical to v17, including the I²C driver. Removing the admission/footer changes restores v17's observer exactly. The configuration changes only the release suffix; all 101 server criteria and the identical DTB remain required.

```sh
python3 check-admission.py --source /path/to/patched/linux/arch/arm/mach-exynos/odroid-u3-irqdiag.c --baseline /path/to/v17/arch/arm/mach-exynos/odroid-u3-irqdiag.c
```

The host check compiles the actual new helpers and reproduces the old defect with the actual v17 watchdog hook. It covers held-guard contention,640 racing threads,100,000 rejections after the limit, initial-dump exclusion and release ordering in the API model. ARM build/package integrity and native qualification are separate gates. Native validation must retain complete numbered UART dumps, verify all 351 modules/four timers/journal and stop the bounded boot series at its first failure. Preserve the exact normal v17 fallback and matching reinstall/debug files. This improves observation; it is not an accepted correction of the boot hang and does not promote APT/image defaults.
