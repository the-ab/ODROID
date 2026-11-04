# U3 I²C0 interrupt affinity control, revision 18

[Deutsch](README.de.md)

Private `7.3.1-odroidu3-v18` extends [v17](../7.3.1-idle-gic-progress-v17/README.md). The boot argument `i2c_s3c2410.u3_irq_cpu=1` requests CPU1 for U3 I²C0 through `irq_set_affinity()`. The default is disabled (`-1`). The existing U3 diagnostic target must be enabled and match this board, I²C0 at `0x13860000`, and GIC INTID90. Other controllers retain their original path.

The request runs after IRQ registration, before adapter/client registration. Only an online, valid CPU is accepted. Invalid/offline CPU or API failure warns and preserves normal initialization. No raw register write, invented GIC mask, clock change or transfer/IRQ-handler rewrite is added. An accepted API request does not prove hardware routing: native tests must inspect requested/effective IRQ affinity and per-CPU interrupt progress.

This separates CPU0-specific behavior from behavior associated with I²C interrupts. It does not identify a root cause or promise a fix. A full v17 initcall trace stopped at ARM performance-unit registration; a second start failed earlier during I²C/PMIC initialization with that initcall blacklisted. The PMU initcall is not required for the observed failure. Both controls recovered after cold starts; a common cause of all failures is not established.

All seven v17 RAM diagnostic channels, three Cortex-A9 errata options, four-CPU support and 101 server criteria remain. Configuration changes only the release suffix; the DTB must remain byte-identical. The cumulative patch affects the same 13 files. Removing the new helper, includes and call restores v17's modified driver exactly; the other 12 files are unchanged.

Run the host check against the patched driver:

```sh
python3 check-control.py --source /path/to/patched/linux/drivers/i2c/busses/i2c-s3c2410.c
```

It compiles the actual helper with IRQ API stubs and exercises seven cases: disabled, untargeted, invalid/offline CPU, success, API failure and CPU0. ARM compilation, package integrity and native routing/boot acceptance remain separate checks. Retain matching debug ELF, packages, UART evidence and a verified full-function fallback. Stop a bounded reboot series at its first failure. This candidate changes no image default and has no public binary release qualification.
