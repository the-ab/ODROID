# Kernel security review —2026-10-30

[Deutsch](SECURITY-REVIEW.de.md)

Candidate 7.3.1-odroidu3-v3 uses the complete signed Linux 7.3.1 stable source, rather than selected CVE cherry-picks. SHA256: `fa595aad93734f829c963c2a90ef7c3673224fd7fdae7b49406e397cde2de231`. Greg Kroah-Hartman's developer signature was verified against the key published through kernel.org WKD.95,979 upstream regular source files were checked; only the five documented U3 source changes differ. The running kernel configuration matched the reviewed profile.

Linux CNA data snapshot `6e051cebb25cdd17a28267fbf1a4de5c9c8164f8`:18,164 published records reviewed.18,160 are unaffected according to published non-Git version ranges. Four version-only residuals were manually assessed: CVE-2021-47645(Zoran not enabled), CVE-2026-68086(THP disabled; mainline code removed), CVE-2026-98938(Rust disabled; mainline refactor), CVE-2026-98941(filesystem encryption enabled in v3; CNA states the affected code applies through 7.2 and was refactored in7.3). No known applicable unresolved finding remains in this snapshot/profile.

CVE-2026-98432 is already fixed from 6.12.113 and 7.3. Both `inet_sock_destruct()` and `tcp_v4_reqsk_destructor()` use the required RCU-delayed release in our 6.12.114 and 7.3.1 source inputs. Ubuntu's package status is not automatically the status of this independently built kernel.

This is a dated published-data/configuration/source assessment, not a guarantee against undisclosed or future vulnerabilities or an independent complete audit of our local patches. Repeat the review when upstream versions, local patches or configuration change. The6.12.114 baseline version-range scan had residuals requiring separate applicability assessment; it is not presented as a count of exploitable U3 vulnerabilities. Keep all new stable changes together and provide exact matching sources when publishing packages.

Primary sources: [kernel releases](https://www.kernel.org/), [kernel CVE process](https://docs.kernel.org/process/cve.html), [Linux CNA repository](https://git.kernel.org/pub/scm/linux/security/vulns.git), [CVE-2026-98432 Ubuntu advisory](https://ubuntu.com/security/CVE-2026-98432).

Local revision v7 keeps the exact upstream source and server config (only LOCALVERSION changes). A full source comparison now finds eight modified files, including the optional-regulator/stream-DMA/capture-DT/HDMI capability corrections. Local review preserves provider error propagation, stream ownership and hardware power boundaries; it does not establish a complete independent security audit. The dated CNA snapshot above is not represented as newly refreshed data.
