# RAM-only GIC range control, revision28

[Deutsch](README.de.md)

This control retains the seven v26 io_uring fixes. Compared with v27 it removes the extra early MMIO readbacks and early logging. The original single GICD_TYPER result, computed IRQ count and CPU are saved in RAM; the existing core-phase deferred report prints them as U3GICRANGE. The distributor setup and its MMIO calls remain the v26 sequence. No corrective register write, IRQ mask, secure/debug access or new timer is added. This tests whether the early range is wrong in a failing boot while reducing observer perturbation. Source/MMIO-call roundtrip and ARM/server-profile build pass; package/native checks pending. V25 remains the direct exact rollback and v17 an additional reserve. Not release accepted.
