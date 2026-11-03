# Cortex-A9 errata candidate, revision 16

[Deutsch](README.de.md)

Private `7.3.1-odroidu3-v16` retains [v15](../7.3.1-i2c-progress-v15/README.md)'s bounded diagnostics and enables three existing upstream options:

| Option | Original 5.4 kernel | v15 | v16 |
|---|---|---|---|
| `CONFIG_ARM_ERRATA_754322` | y | n | y |
| `CONFIG_ARM_ERRATA_764369` | y | n | y |
| `CONFIG_ARM_ERRATA_775420` | y | n | y |

The observed U3 CPU is Cortex-A9 r3p0. Linux Kconfig and [Arm's r3 errata notice](https://documentation-service.arm.com/static/608117fa5e70d934bc69f139?token=), sections2.3.3–2.3.5, describe applicable translation/cache-maintenance workarounds. This identifies configuration gaps, not the proven cause of the intermittent U3 hang. Other original options are not copied blindly:754327 targets pre-r2p0 CPUs.

The patch is byte-identical to v15. No manual register workaround or driver rewrite is added: the existing upstream implementations are selected. All other configuration values, including server/security features, are retained except the new release suffix. DTB, firmware and image defaults are unchanged. Diagnostic output can affect timing; preserve v15 as a control and matching debug ELF/UART evidence.

The original Ubuntu20 system is used for a separately recorded warmboot comparison. No packages, configuration or boot files are changed there; user-authorized restarts are the only state-changing operations. Build/package validation and native v16 qualification remain separate. Do not publish this candidate or promote image defaults without hardware validation.

Build verification on2026-11-03 passed all101 server gates with no compiler warnings. Linked ARM disassembly confirms the additional context-switch/cache barriers and SCU diagnostic store, and late debugfs ordering remains correct. Package/native qualification is recorded separately.
