# GIC static-key counter control, revision30

[Deutsch](README.de.md)

V29 measured an incorrect base for the original GIC type read: per-CPU storage was selected instead of its initialized register mapping, while the key RAM counter was already1. This control changes only the GIC base accessor condition from static_branch_unlikely to the supported static_key_enabled RAM-counter check. Normal key enable, per-CPU mapping and hardware initialization remain unchanged. No forced range, new MMIO operation, guessed address or secure/debug access.

The global CONFIG_JUMP_LABEL setting remains enabled because XFS online checking/repair selects it. All existing XFS/server capabilities and seven io_uring fixes are retained. Only LOCALVERSION changes in the resolved configuration. The precise early patch/cache mechanism is not proven; this is a targeted accessor workaround to qualify. Source/build/package and native acceptance remain separate. V25 is the direct rollback, v17 the reserve. No release acceptance.
