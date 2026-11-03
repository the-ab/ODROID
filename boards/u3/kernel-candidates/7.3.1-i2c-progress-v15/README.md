# U3 I2C progress and softlockup diagnostic, revision 15

[Deutsch](README.de.md)

Private candidate `7.3.1-odroidu3-v15` retains [v14](../7.3.1-i2c-progress-v14/README.md)'s RAM progress records, late debugfs registration and validated U3 GIC/MCT observer. Four v14 warmboots passed journal, service, CPU-timer and module checks. The next warmboot stalled before userspace with softlockups; it emitted no RCU-stall snapshot. A manual cold start recovered v14 and passed the same health checks. This does not establish a platform fix.

V15 adds one call at the **existing softlockup reporting site**, after the normal reporting-period update and before acquiring the printk CPU synchronization lock. The hook returns immediately unless the existing U3 progress option was enabled after resource validation. It shares the existing three-report budget with the RCU hook and prints `U3IRQDIAG reason=SoftLockup` plus the stored `U3I2CPROG` records. The existing atomic busy guard prevents concurrent recursive snapshots. The regular watchdog warning, thresholds, backtraces, taint and panic behavior remain unchanged.

No new timer, lock, allocation, sleeping operation, cross-CPU request or I2C register access is added to the observed progress paths. GIC dispatch, generic fasteoi and the I2C driver are byte-identical to v14. The snapshot reads the same status-only GIC/MCT registers as the existing RCU observer, before console output; it does not acknowledge interrupts or clear status. Measurements and serial output can change timing. RAM records are approximate last-stage values, not an atomic event history; see v14 for channel/stage meanings.

Enable `odroid_u3_irqdiag=1 odroid_u3_gic_defer=1 odroid_u3_i2cdiag=1 earlycon loglevel=7` with the serial console. The read-only progress view remains `/sys/kernel/debug/odroid-u3-i2c-progress`. Non-Exynos builds receive a no-op stub. Board/image defaults, DTB and boot firmware are unchanged. Preserve matching sources/debug ELF, local UART logs and verified boot-file/package fallbacks before testing. Build/package checks and native qualification remain separate; this is not a public kernel/image replacement.

ARM build on2026-11-03 passed without compiler warnings, all101 server configuration gates passed, and linked ELF confirmed the late debugfs order and watchdog hook. Package and native qualification remain separate.
