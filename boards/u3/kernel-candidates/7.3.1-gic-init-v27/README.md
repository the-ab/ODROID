# U3 early GIC initialization diagnosis, revision27

[Deutsch](README.de.md)

Extends v26 with read-only, U3-only snapshots of the original GICD_TYPER result and computed IRQ range, plus distributor fields before and after the existing initialization. The seven io_uring fixes remain unchanged. No additional hardware write, IRQ mask or secure/debug unlock is introduced. Enabled only with the existing odroid_u3_gic_defer option. A zero priority read can reflect access restrictions; this candidate does not assume corruption or repair it. Source roundtrip and ARM/server-profile build pass; package/native checks pending. V25 is the primary exact rollback; v17 stays an additional reserve. Not release accepted.
