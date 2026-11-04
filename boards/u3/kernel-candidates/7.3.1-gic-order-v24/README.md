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
