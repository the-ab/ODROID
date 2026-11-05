# io_uring security backports, revision 26

[Deutsch](README.de.md)

Private candidate `7.3.1-odroidu3-v26` extends [v25](../7.3.1-gic-alias-v25/README.md) with the following CNA-referenced io_uring fixes. IO_URING remains enabled. The seven effective patches pass strict source-context checks and an exact reverse roundtrip on the 7.3.1 source. The ARM cross-build and server configuration check pass. Package and native acceptance are still pending. No image or public APT promotion follows from source checks.

| CVE | Original upstream fix |
|---|---|
| CVE-2026-99231 | [`c254eec4364b`](https://git.kernel.org/stable/c/c254eec4364b9f4b4cbdce43be3fb4df5a651a70) |
| CVE-2026-99230 | [`4c83e39f4d19`](https://git.kernel.org/stable/c/4c83e39f4d1944d7146fd06094f2c8053238d55c) |
| CVE-2026-99229 | [`34f5a664c34d`](https://git.kernel.org/stable/c/34f5a664c34d3cb62f6bec7f4156754594a7d25b) |
| CVE-2026-99228 | [`63c103279a95`](https://git.kernel.org/stable/c/63c103279a95e82280092f2f4232e91e8117a252) |
| CVE-2026-99255 | [`436d48a2ed13`](https://git.kernel.org/stable/c/436d48a2ed13112d2d27085325838e5bce6b4507) |
| CVE-2026-99254 | [`22e643e61b9b`](https://git.kernel.org/stable/c/22e643e61b9b6299b42ff7d88bab48bccada8a5d) |
| CVE-2026-99253 | [`76a82c666abf`](https://git.kernel.org/stable/c/76a82c666abf155ad52d5f41043eac77dd3e41d8) |

For CVE-2026-99255, `io_uring.c` uses the CNA-referenced stable backport `92e20e9c72bdf6cfa6f84eded7b33399bc7061da`, preserving the target's existing link predicate. The original mainline `io-wq.c` and header hunks preserve its KCOV context. This avoids importing an unrelated REQ_F_CQE_SKIP API change. Original and compatibility patches, effective patch and metadata/checksums are retained under `security/`.

The v25 board/driver patches and all server features remain unchanged; only seven io_uring files and the revision suffix differ. V25 is the direct rollback baseline requested by the owner; v17 remains an additional preserved reserve. Test the new revision before preparing images, with bounded boot series and benign io_uring functionality checks. The original CPU/interrupt cause and poweroff automatic-power-on behavior remain separate open results. No vulnerability reproduction is needed to verify patch provenance and ordinary functionality.
