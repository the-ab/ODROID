# Release requirements

[Deutsch](RELEASES.de.md)

Image version: SemVer, first candidate `1.0.0`. Kernel: upstream version plus board revision, currently `7.3.1-odroidu3-v32`. U3 and XU4 releases have separate hardware evidence.

A release must identify the source commit, exact package manifest, IMG/ZIP checksums, kernel/modules/DTB and boot0 payload. ZIP CRC and complete decompressed IMG hash are checked. Matching kernel/U-Boot sources, configuration, local patches and build instructions accompany binary distribution; package and firmware licenses remain available.

Before stable publication:

1. Fresh minimized/minimal builds pass ARM login/PAM, sudo, SSH, netplan and complete systemd ordering checks.
2. Images contain only the default human account, no authorized/host keys, no copied machine identity and no inherited host workspace ACLs. Ordinary odroid access to root configuration remains read-only.
3. Partition readback, boot offsets/CRCs, filesystem checks, kernel/module version checks and ZIP roundtrip pass.
4. New images receive physical first-boot acceptance on the intended medium; report SD, native eMMC, root expansion, DHCP identity, SSH/sudo, journal, fan and any desktop tests separately.
5. Exact BL1/BL2/TrustZone binary redistribution and source coverage are documented. Current source recipes accept the hash-pinned reference image; that alone is not a firmware license statement. No vendor boot blobs are checked into Git.
6. Source review and explicit release approval precede tag/publication. Build scripts do not publish automatically.

Connected-HDMI Xorg/Weston output on the prototype was accepted separately. Minimal v1 native eMMC first boot and basic runtime checks subsequently passed; minimized/SD, any additional claimed scope and firmware provenance remain open. Downloads must describe remaining limitations accurately.

Image candidate 1.0.1 adds owner-installed root SSH keys and locally installed APT kernel packages. Minimal 1.0.1 has passed native-eMMC basic checks, including owner root-key login, installed kernel packages and APT source/signature. The subsequent7.3.1 APT update/rollback/return test passed; minimized/SD remain pending.

Fresh image1.0.2 minimal/minimized candidates now pass local ARM login/PAM/sudo/SSH, systemd, filesystem, full partition/boot/package readback and ZIP roundtrip checks. They contain server kernel 7.3.1-odroidu3-v3, package 7.3.1-4 with tested purge cleanup. Native server-kernel service tests passed on the installed1.0.1 test system; the fresh minimal1.0.2 image has now passed native-eMMC first-boot checks. Minimized/SD and the other release gates remain open.

Local 1.0.3 preparation selects the natively qualified v32 kernel: ten pure warmboots and five controlled halt/cold starts, all four CPU timers and 351 matching modules; full listed server tests, ordinary non-root io_uring,16 MiB Ethernet roundtrip and internal stereo codec loop pass with lockdep enabled and no new warnings. Its fresh image/ZIP gates and first boots are separate. Exact vendor boot-firmware distribution coverage and explicit public promotion remain open.
