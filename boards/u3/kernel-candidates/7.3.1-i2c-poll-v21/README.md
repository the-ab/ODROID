# U3 I²C0 polling control, revision 21

[Deutsch](README.de.md)

Private `7.3.1-odroidu3-v21` derives independently from [v17](../7.3.1-idle-gic-progress-v17/README.md). The opt-in boot argument `i2c_s3c2410.u3_poll=1` routes the verified U3 I²C0 target through the driver's existing process-context polling loop and skips registration of that controller's IRQ handler. Default is disabled. IRQ mapping and target validation (U3, address `0x13860000`, GIC INTID90) remain mandatory. Other controllers retain their existing behavior.

The existing `is_ack()` and `i2c_s3c_irq_nextbyte()` sequence, normal/atomic clock references, bus divisor and SDA configuration remain unchanged. A separate per-adapter flag selects polling, avoiding the extra divisor setting carried by the existing SATA-PHY `QUIRK_POLL`. Normal transfer completion bypasses the waiter wakeup just as the original polling path does. The controller's own interrupt-enable/pending semantics are retained for polling; Linux does not request or unmask its mapped GIC IRQ. No direct GIC/PMIC register change is added.

Read-only parameters expose `u3_poll_active` and an approximate successful-transfer counter `u3_poll_xfers`. Qualification must verify the boot argument, target log, active flag, increasing completed-transfer count, absence of an I²C0 handler in `/proc/interrupts`, PMIC/regulator/RTC operation, four advancing CPU timers and normal journal/service/package checks. The unchanged polling loop can sleep and changes scheduling/transaction latency; this control cannot isolate every timing variable or establish a root cause from a few successful boots.

The previous independent [v19 synchronization](../7.3.1-i2c-sync-v19/README.md) and [v20 clock-hold](../7.3.1-i2c-clockhold-v20/README.md) controls both reproduced the stall. Neither is included here. All seven RAM channels, three Cortex-A9 workarounds and 101 server criteria remain; configuration changes only the release suffix and the DTB must stay byte-identical.

```sh
python3 check-control.py --source /path/to/patched/linux/drivers/i2c/busses/i2c-s3c2410.c
```

Source/host checks, ARM build/package integrity and native qualification are separate gates. Keep the exact normal v17 boot files, reinstall package and matching debug/UART evidence. Stop a bounded native series at its first failure. No image/APT default or accepted-fix claim is changed by this diagnostic candidate.

Native result (2026-11-04): the transition and four consecutive pure warmboots passed full checks. Successful RTC reads increased the polled-transfer counter on every healthy boot; no I²C0 IRQ handler was registered, and all 351 modules, four advancing CPU timers, regulators, PMU, audit, journal and services passed. The fifth pure warmboot hung after the new root filesystem was entered; the series stopped (four of five passed). Its late snapshot showed I²C0 INTID90 disabled and not active, with all three I²C0 IRQ channels still zero. MMC INTID109 was active instead; CPU0 last recorded global GIC return and idle entry. I²C0 GIC interrupt delivery is therefore not required for this observed hang. The active MMC interrupt and approximate RAM markers do not identify the frozen instruction or prove an MMC-driver cause. Polling is not a reliable workaround.

Only one late register dump completed: three concurrent watchdog calls consumed the shared report-attempt budget while two lost the busy guard. Future diagnosis must fix report admission so skipped concurrent calls do not consume the completed-dump budget. Existing evidence must not be described as multiple independent late samples.

After the failed series, one measured ten-second cold recovery passed the full polling checks. The original complete normal v17 boot files and management state were restored byte for byte. The subsequent native v17 boot passed all 351-module, four-timer, PMU, audit, journal and service checks; matching backups and the v17 reinstall package remain retained. No further boot series is running.
