# Kernel security review

[Deutsch](SECURITY-REVIEW.de.md)

Assessment date: **5 November 2026**. Target: Linux `7.3.1-odroidu3-v32`, DEB `7.3.1-33`, the pinned source archive and shipped configuration. This is a dated source/configuration assessment, not a guarantee that all future or undisclosed vulnerabilities are fixed.

The Linux CNA snapshot `b537cbcd0154f07e083400c5ba2f9826be84ee26` contained 18,204 published records. Conservative published version-range checks classified 18,193 as unaffected, ten as affected and one as unknown before manual/configuration review and the local fixes. Those residual counts are not counts of exploitable U3 vulnerabilities.

Seven additional io_uring fixes are included: **CVE-2026-99228, -99229, -99230, -99231, -99253, -99254 and -99255**. [Provenance and exact patches](../boards/u3/security/upstream-fixes.json) retain the canonical commits and the API-compatible effective 7.3.1 adaptation for CVE-2026-99255. The combined effective patch is in `boards/u3/patches/platform.patch`; do not apply the individual reference patches a second time.

The four earlier residuals were assessed separately: CVE-2021-47645 (Zoran disabled), CVE-2026-68086 (THP disabled; mainline code removed), CVE-2026-98938 (Rust disabled; mainline refactor), and CVE-2026-98941 (filesystem encryption enabled; CNA describes affected code through 7.2 and its refactor in 7.3). CVE-2026-98432 is fixed in the pinned 7.3.1 base: the affected socket destructors use the required RCU-delayed release. Ubuntu's package status does not automatically describe this independently built kernel.

Source replay, ARM build, 101 server configuration requirements and all 351 packaged modules passed. The native ordinary non-root io_uring test covers NOPs, linked file write/fsync/readback, asynchronous open/close, poll cancellation and child waitid. Device-specific URING_CMD is source/build checked only; no suitable runtime device was available. No exploit reproducer was used. Native boot/server checks ran with lockdep enabled and no new kernel warnings.

Local GIC, audio/USB, MMC and TUN changes are retained in the matching sources. Functional tests and a clean warning log are not an independent complete security audit. Refresh the assessment when source/configuration or published CVE data change.

Primary sources: [Linux CNA repository](https://git.kernel.org/pub/scm/linux/security/vulns.git), [kernel CVE process](https://docs.kernel.org/process/cve.html), [kernel releases](https://www.kernel.org/releases.html), [CVE-2026-98432](https://ubuntu.com/security/CVE-2026-98432).
