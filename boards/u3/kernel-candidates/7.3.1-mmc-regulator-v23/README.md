# MMC regulator error propagation, revision 23

[Deutsch](README.de.md)

Private `7.3.1-odroidu3-v23` retains [v22](../7.3.1-diag-budget-v22/README.md)'s corrected bounded report admission. The first native v22 transition failed, but produced three complete late dumps: CPU0's timer count stayed 1051 and I²C0 INTID90 remained active. A later CPU3 BUG in `regulator_check_voltage()` followed I²C bus timeouts. Matching debug-address resolution places the caller in `mmc_regulator_set_vqmmc()`. This later crash does not establish the cause of the earlier CPU0 stall.

`regulator_is_supported_voltage()` may return a negative readback error, as documented in the [regulator API](https://docs.kernel.org/driver-api/regulator.html). The MMC helper tested only its Boolean negation, allowing such an error to proceed to the voltage-triplet API. For the board's fixed VMMC1.8V/VQMMC2.8V topology, the first 3.3V-signaling trial can also construct an inverted 2.7–2.15V range. An I²C error could bypass the capability check and pass this invalid range to the regulator core's BUG check.

The correction rejects inverted ranges with `-EINVAL` before the query and propagates negative capability-query errors before calling any voltage-change API. Unsupported ranges still return `-EINVAL`. The existing optional current-voltage optimization and successful voltage arguments remain unchanged. Voltage values, constraints, DTB, clock and I²C/GIC logic remain identical. The same helper is byte-identical in pinned 6.12.114; this is an existing error-path defect, not a demonstrated Linux7 regression.

```sh
python3 check-regulator.py --source /path/to/patched/linux/drivers/mmc/core/regulator.c --baseline /path/to/v22/drivers/mmc/core/regulator.c
```

The host test compiles the actual helper, OCR conversion and VQMMC caller. Sixteen cases cover inverted ranges, negative/zero/positive query results, VMMC1.8V fallback,1.2V/1.8V signaling, existing optional-read behavior and unchanged successful arguments. The original API misuse is observed with API stubs only. The cumulative source patch touches 14 files; the previous 13 modified files stay byte-identical to v22. Configuration changes only the release suffix; all 101 server criteria,351 modules and the unchanged DTB remain required.

Native qualification must check full boot/module/configuration integrity, the fixed 1.8V/2.8V supply readings, four advancing timers, clean journal/services and complete UART evidence. Stop the bounded series at its first failure and retain normal v17 backups/reinstall/debug files. This addresses a concrete secondary error path; the general start-stall cause remains open. No APT/image default is promoted by this candidate.

Native result (2026-11-04): the transition and first pure warmboot passed all 351-module/configuration, four-timer, journal/service/audit/PMU and UART checks. Supply readback was exactly VMMC1.8V and VQMMC2.8V. The second pure warmboot hung; the series stopped (one of two passed). Three complete late dumps showed CPU0 timer count 735 unchanged and INTID90 active. No kernel BUG appeared in that failing trace, which contained four I²C bus-idle timeouts. A first measured ten-second cold recovery also failed and supplied three complete dumps with CPU0 count 701 and INTID90 active, again without a kernel BUG. The absence of the earlier BUG alone does not prove that all its former conditions recurred; host checks establish the specific error/range admission behavior. The original CPU0 start stall remains unresolved.

A second measured ten-second cold recovery reached healthy v23 userspace and passed all supply/module/timer/journal checks. The original complete normal v17 boot files and management state were then restored byte for byte. The final native v17 boot passed all 351-module, four-timer, PMU, active-audit, journal and service checks. No further reboot/power-test job is running. Matching debug files, reinstall packages, backups and all failure captures remain retained.
