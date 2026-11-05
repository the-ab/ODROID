# Kernel security review —2026-10-30

[Deutsch](SECURITY-REVIEW.de.md)


## Follow-up — 2026-11-05

Kernel.org still lists 7.3.1 as the latest stable release. The refreshed Linux CNA snapshot `b537cbcd0154f07e083400c5ba2f9826be84ee26` contains 18,204 published records: the existing conservative version-range checker classified 18,193 as unaffected, ten as affected and one as unknown. The eleven residuals comprise the four previously assessed cases below and seven additional io_uring cases: CVE-2026-99228, CVE-2026-99229, CVE-2026-99230, CVE-2026-99231, CVE-2026-99253, CVE-2026-99254 and CVE-2026-99255.

V25 enables `CONFIG_IO_URING=y`. Its `io_uring_cmd_del_cancelable()` still uses `hlist_del()` where CVE-2026-99230 requires removal that leaves the node unhashed. This v25 source gap is confirmed. All seven newly identified fixes are now carried in v26, assessed below. V25 has no final security acceptance. The dated assessment below remains historical and must not be read as current clearance for these new findings. Stable-version currency alone is insufficient for release approval.

### V26 source follow-up

[Revision 26](../boards/u3/kernel-candidates/7.3.1-iouring-v26/README.md) integrates the seven io_uring fixes referenced by this CNA snapshot. Its provenance manifest retains the canonical commits, exact effective patches and the API-compatible CVE-2026-99255 stable adaptation. A complete replay of the combined profile on the pinned signed 7.3.1 archive matches all 21 changed build-tree files byte for byte. The ARM build, 101 required server configuration capabilities and all 351 packaged modules pass; the DTB is unchanged.

The first native transition from v25 to v26 reproduced the previously observed early I2C/PMIC boot failure. The bounded series stopped at that first failure. After one controlled cold recovery, v26 passes native journal/module/configuration/four-CPU-timer checks and the ordinary non-root io_uring smoke test (64 NOPs, linked regular-file write/fsync, exact 4096-byte readback, asynchronous open/close, poll cancellation and child waitid). The direct rollback is the exact backed-up v25 boot set; v17 remains an additional reserve. The full observed UART interval includes an initial GIC report with four valid aliases, but no late watchdog report was emitted. This is not evidence that io_uring caused the early platform failure. Source fixes and successful compilation do not establish boot stability or release acceptance. No new image or public APT package is promoted. Device-specific URING_CMD runtime behavior was not tested because no suitable device is available; its patch is source/build checked. No vulnerability reproducer was used.

Candidate 7.3.1-odroidu3-v3 uses the complete signed Linux 7.3.1 stable source, rather than selected CVE cherry-picks. SHA256: `fa595aad93734f829c963c2a90ef7c3673224fd7fdae7b49406e397cde2de231`. Greg Kroah-Hartman's developer signature was verified against the key published through kernel.org WKD.95,979 upstream regular source files were checked; only the five documented U3 source changes differ. The running kernel configuration matched the reviewed profile.

Linux CNA data snapshot `6e051cebb25cdd17a28267fbf1a4de5c9c8164f8`:18,164 published records reviewed.18,160 are unaffected according to published non-Git version ranges. Four version-only residuals were manually assessed: CVE-2021-47645(Zoran not enabled), CVE-2026-68086(THP disabled; mainline code removed), CVE-2026-98938(Rust disabled; mainline refactor), CVE-2026-98941(filesystem encryption enabled in v3; CNA states the affected code applies through 7.2 and was refactored in7.3). No known applicable unresolved finding remains in this snapshot/profile.

CVE-2026-98432 is already fixed from 6.12.113 and 7.3. Both `inet_sock_destruct()` and `tcp_v4_reqsk_destructor()` use the required RCU-delayed release in our 6.12.114 and 7.3.1 source inputs. Ubuntu's package status is not automatically the status of this independently built kernel.

This is a dated published-data/configuration/source assessment, not a guarantee against undisclosed or future vulnerabilities or an independent complete audit of our local patches. Repeat the review when upstream versions, local patches or configuration change. The6.12.114 baseline version-range scan had residuals requiring separate applicability assessment; it is not presented as a count of exploitable U3 vulnerabilities. Keep all new stable changes together and provide exact matching sources when publishing packages.

Primary sources: [kernel releases](https://www.kernel.org/), [kernel CVE process](https://docs.kernel.org/process/cve.html), [Linux CNA repository](https://git.kernel.org/pub/scm/linux/security/vulns.git), [CVE-2026-98432 Ubuntu advisory](https://ubuntu.com/security/CVE-2026-98432).

Local revision v7 keeps the exact upstream source and server config (only LOCALVERSION changes). A full source comparison now finds eight modified files, including the optional-regulator/stream-DMA/capture-DT/HDMI capability corrections. Local review preserves provider error propagation, stream ownership and hardware power boundaries; it does not establish a complete independent security audit. The dated CNA snapshot above is not represented as newly refreshed data.
