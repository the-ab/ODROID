# GIC base-selection RAM control, revision29

[Deutsch](README.de.md)

V28 captured an original GICD_TYPER result of zero (32 IDs) in a failed warmboot, while all four later validated aliases reported160 IDs. This control records the actual base used by that original read and by normal distributor initialization. It compares the selected base with the initialized per-CPU slot, the raw mapping, the storage pointer and the mapping formula; it also records the static-key RAM counter and IRQ count. Only equality results are printed at the existing later core report, never kernel addresses.

The original single type read and distributor MMIO operations remain unchanged. There are no additional early MMIO probes, early printk calls, new timers, forced interrupt counts or corrective writes. The seven v26 io_uring fixes are retained. Source/build/package and native acceptance are separate; this is a diagnostic candidate, not a release or a proven correction. V25 remains the direct rollback and v17 the additional reserve.

The pinned21-file patch replay, equivalent original MMIO sequence, ARM kernel/modules/DTBs and101-capability server configuration gate pass. Package and native checks are still pending.

The first transition passes native health and both base checks. The first pure warmboot fails; the bounded series stops immediately. Its original type-read selection equals the per-CPU storage pointer and differs from the initialized register mapping, although the static-key RAM counter is already1 and the expected slot matches the driver's mapping formula. Normal distributor initialization later selects the correct register mapping in the same boot. The recorded zero/32 therefore came from an incorrect original base selection. The initial report and all three late reports are secured.

The exact patch-application/instruction-cache mechanism is still unproven. A verified configuration difference is relevant: the stable-tested6.12 baseline has `CONFIG_JUMP_LABEL` disabled; the7.3.1 server profile enables it. The supported counter-based branch path with this optimization disabled is the next focused control. This finding does not authorize a forced IRQ count, guessed register access or a release claim. The seven io_uring fixes must remain present.
