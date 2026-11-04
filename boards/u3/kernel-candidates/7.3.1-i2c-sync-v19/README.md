# U3 I²C IRQ/clock completion control, revision 19

[Deutsch](README.de.md)

Private `7.3.1-odroidu3-v19` derives from [v17](../7.3.1-idle-gic-progress-v17/README.md). The opt-in boot argument `i2c_s3c2410.u3_sync_irq=1` waits for I²C0 IRQ completion with `synchronize_irq()` immediately before the two existing transfer-path `clk_disable()` calls. Default is disabled. The v18 CPU-affinity experiment is not included.

The existing driver wakes its transfer waiter before its IRQ handler has finished the remaining controller accesses. A concurrently scheduled waiter can therefore reach clock disable while the handler is still running. This ordering also exists in the older driver; it is a candidate lifetime race, not proof that Linux 7 introduced it or that it explains the observed stalls. This control tests the missing synchronization directly.

Only the existing diagnostic target matching U3, I²C0 at `0x13860000`, and GIC INTID90 is eligible. Polling, atomic and non-preemptible calls retain their original behavior. The IRQ handler does not require the adapter bus lock held by normal transfer callers. The [generic IRQ API](https://docs.kernel.org/core-api/genericirq.html#c.synchronize_irq) requires preemptible context and warns against holding a resource needed by the IRQ handler; these restrictions are part of the control's admission checks. No direct register workaround, IRQ mask, affinity, voltage setting or new clock reference is introduced.

Read-only module parameters expose `u3_sync_count` (completed waits) and `u3_sync_skipped` (excluded contexts). Existing process-channel stages 200/201 bracket the wait. Counters are diagnostic observations, not atomic global snapshots. All seven RAM channels, three Cortex-A9 workarounds and 101 server configuration criteria remain. Configuration changes only the release suffix; the DTB must remain byte-identical. The cumulative patch affects the same 13 files; removing the new helper/includes/calls/log restores v17 exactly.

Host check against the patched driver:

```sh
python3 check-control.py --source /path/to/patched/linux/drivers/i2c/busses/i2c-s3c2410.c
```

It compiles the actual helper and both clock-off call sites with API stubs: eight cases check exclusions, completed-wait accounting and wait-before-clock-off ordering. ARM build, package integrity and native repeated boot/transfer acceptance remain separate gates. Preserve matching debug files, all failure captures and the original v17 fallback. Stop each bounded series at its first failure. No image default or public binary/APT release is changed by this candidate.
