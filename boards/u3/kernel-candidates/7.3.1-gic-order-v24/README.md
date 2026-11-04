# GIC diagnostic ordering, revision 24

[Deutsch](README.de.md)

Private candidate `7.3.1-odroidu3-v24` extends [v23](../7.3.1-mmc-regulator-v23/README.md). The CPU0 timer freeze and active shared interrupt persisted without a later regulator BUG. Earlier polling reproduced the stall while I²C0 IRQ90 was disabled, so an active IRQ alone does not identify a faulty device driver.

The opt-in GIC progress marks now complete through `dsb(sy)` immediately before the side-effecting IAR read and after the acknowledged-ID mark, before handler dispatch. This corrects an observation-order gap between normal RAM stores and relaxed MMIO. It does not claim a missing barrier in the upstream GIC functional path. Other progress rows remain approximate, not atomic snapshots or a sampled program counter. Barriers can change timing; successful boots alone would not prove the cause.

The existing bounded observer also reads priority words for SGIs0–15 and PPI28–31 in each validated Exynos GIC bank, plus priority/target/configuration words for shared INTIDs90 and109. `U3IRQATTR` lines preserve raw words. A GIC_TYPER implementation-range gate precedes these extra reads. No IAR/EOI access is added to the observer; no priority, target, mask, pending or active register is written. CPU/debug/Secure registers are not accessed. Register definitions follow the pinned Linux `arm-gic.h` and the [Arm GIC specification, sections4.3.11–13](https://documentation-service.arm.com/static/5f8ff196f86e16515cdbf969).

Only the observer and two opt-in GIC mark boundaries change from v23; the other12 patched files, MMC correction, I²C driver, device tree, clocks, voltage policy, completed-report budget and101 server criteria remain unchanged. The configuration changes only its revision suffix.

```sh
python3 check-order.py --tree /path/to/patched/linux
```

The test compiles the actual read helper with read-only stubs, verifies130 register-offset cases and checks the actual IAR mark/barrier order. Inspect the compiled ARM function for both DSB SY instructions. Build/package checks and native qualification remain separate. Keep exact normal v17 boot/state backups and reinstall/debug files; stop the bounded warmboot series at the first failure. This candidate is not promoted to images or APT.

Native result (2026-11-04): the transition boot passed351-module, four advancing timer, audit/PMU, fixed-supply and journal/service checks. The first pure warmboot failed and the series stopped (0/1 passed). Three complete snapshots at36.586,39.026 and64.586 seconds showed CPU0 timer772 unchanged, RPR0 and active INTID90. CPU0's last GIC channel remained stage15 (return, previous ID1023); the idle channel remained stage1 (entry). These marks still do not identify the frozen instruction, including a possible stop before a new pre-IAR DSB completes. No later kernel BUG occurred in the captured failure.

Private priority words remained`a0a0a0a0`; late shared90/109 words read zero, versus`a0a0a0a0` in the initial snapshot. Initial observation ran on CPU0, late observations on CPU2 through the existing bank0 alias. The GIC driver uses core-relative distributor aliases on this non-banked Exynos implementation. These raw results therefore require alias and healthy remote-observer controls before calling them an actual priority change or corruption. Additionally, the [Arm specification, section4.4.6](https://documentation-service.arm.com/static/5f8ff196f86e16515cdbf969) defines a zero RPR result for some Non-secure views. No Secure register access or speculative priority reset is justified by this trace.

The failed warmboot trace was secured before a verified10.138-second AC OFF recovery. Native v24 recovery passed, then the exact normal v17 boot/state was restored and booted after a verified10.105-second OFF interval. Final v17 checks passed351 modules, four advancing timers, PMU/audit without loss and clean journal/services. No firmware, APT or image promotion.

Boot timing: the two healthy full-diagnostic v24 boots took39.754/39.876 seconds to the systemd target (kernel16.617/16.619, userspace23.136/23.256). The restored normal v17 took28.504 seconds (kernel5.137, userspace23.366). Userspace device discovery and network setup remain substantial; this comparison differs in both diagnostic code and logging and is not an isolated logging experiment. The owner's approximately5-second Ubuntu20 observation was not remeasured against the same readiness criterion in this pass.
