# U3 I²C0 managed clock lifetime control, revision 20

[Deutsch](README.de.md)

Private `7.3.1-odroidu3-v20` derives from [v17](../7.3.1-idle-gic-progress-v17/README.md). The opt-in boot argument `i2c_s3c2410.u3_hold_clock=1` keeps one extra balanced `clk_prepare_enable()` reference for the verified U3 I²C0 target. Default is disabled. Normal and atomic transfer functions, IRQ handling and their original clock calls remain unchanged. Neither v18's affinity change nor v19's synchronization wait is included.

The extra reference is acquired after identifying I²C0 at `0x13860000` and GIC INTID90, before requesting its IRQ or registering clients. A managed action releases the reference with `clk_disable_unprepare()`. Registering that action before the IRQ resource ensures reverse devres cleanup frees the IRQ first. The extra prepare reference also keeps the original driver's remove/error `clk_unprepare()` balanced. Clock acquisition/action-registration errors fail probe with balanced cleanup; they do not silently claim the control is active.

Read-only module parameters expose `u3_clock_held` and `u3_clock_rate`. Native qualification must verify the boot parameter, held flag, rate and I²C0 clock enable/prepare counts, as well as actual bus progress and repeated boot health. The test distinguishes dynamic clock gating from other IRQ failures; it does not establish a root cause or an accepted workaround. A successful `clk_prepare_enable()` is a clock-framework observation, not an external electrical measurement.

The v19 wait-before-clock-off control failed its first transition with CPU0 stalled, INTID90 active and another CPU waiting at its synchronization marker. Waiting for a handler does not by itself exclude a later interrupt or every clock-lifetime issue. This independent control keeps the clock available across all transfer contexts instead. No direct GIC/PMIC register write, voltage change, IRQ mask or transfer rewrite is added.

All seven RAM diagnostic channels, three Cortex-A9 workarounds and 101 server criteria remain. Configuration changes only the release suffix; the DTB must remain byte-identical. The cumulative patch affects the same 13 files; removing the helper and probe call restores v17's modified driver exactly.

```sh
python3 check-control.py --source /path/to/patched/linux/drivers/i2c/busses/i2c-s3c2410.c
```

The host check compiles the actual helper with clock/devres stubs and checks eight cases including exclusions, acquisition/action failures, retained clock references during transfer pairs and balanced remove/IRQ-registration-error cleanup. ARM build, package integrity and native acceptance remain separate gates. Retain matching debug files and the original v17 rollback, stop a bounded series at its first failure, and do not publish this as an accepted image/APT fix.
