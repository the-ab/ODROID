# U3 post-decision GIC diagnostic revision 9

[Deutsch](README.de.md)

Private diagnostic candidate `7.3.1-odroidu3-v9`, based on the pinned v3 server profile. In contrast to v8 it removes the four additional pre-disable MMIO reads and leaves `gic_dist_init()` byte-identical to the baseline. `gic_get_cpumask()` keeps its original reads, decision and critical warning in the original order; the added diagnostic call runs immediately before the unchanged return. No target mask or routing write is changed. The `GICPOST` lines report the original selected mask and subsequent read-only identification/target state.

V8 booted warm three times without the sporadic error. That does not establish a correction: sampling, output and code layout can affect timing. This revision separates pre-decision sampling from later observations. Neither diagnostic candidate is a release replacement. Use matching boot-file rollback and local UART capture. Default images/APT and firmware remain unchanged. Build and native outcomes require separate evidence.
