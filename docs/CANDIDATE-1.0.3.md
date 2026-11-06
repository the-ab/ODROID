# U3 image 1.0.3 local candidate review

[Deutsch](CANDIDATE-1.0.3.de.md)

Both fresh Ubuntu 26.04.1 armhf variants pass local validation. Recipe and package source: `b8ce206a44451aa64452add634a3e6376b60d6be`. Kernel `7.3.1-odroidu3-v32`, package `7.3.1-33`, activation tools `1.0.3`. This is a local candidate, with no new public binary/APT/Main promotion.

| Variant | ZIP bytes | ZIP SHA256 |
|---|---:|---|
| minimized | 143727324 | `cdb5ee3e75f01f2c16c2910a26c12c8b76c0935963005572b8938761bcb2e8b2` |
| minimal | 188176108 | `559f2ee46272ea2af0509600f7c92ce143743780786318927cd65c698ed449ec` |

Native kernel qualification on the retained Ubuntu 1.0.2 test installation passed ten pure warmboots and five controlled halt/cold starts, with normal boot arguments, four advancing CPU timers, 351 matching modules and enabled lockdep. Nine functional cases (Docker, VPN/firewall, files, security, modules, bounded load, internal stereo loop, ordinary non-root io_uring, real Ethernet) and two final health/readback cases passed. The Ethernet transfer checked 16 MiB each way; NFS used journal-confirmed nfsdcld tracking. No new kernel warnings, failed units, lost audit records or LAN firewall changes remained. Own test data was removed.

Final packages were installed locally without recompiling/changing the tested kernel/DTB/module bytes, altering boot files/state or rebooting. V25 remains the direct rollback; v17 the additional reserve.

Each fresh image passes ARM login/PAM, password-protected sudo, owner-installed root-key policy, default-account-only, absence of maintenance/host keys and cloned identity, numeric ownership/no inherited host ACLs, systemd/network/time/security ordering, signed APT source, full filesystem/partition/boot readback and full ZIP CRC/image hash roundtrip. Both ship only odroid/odroid as human access, and include the detailed eMMC recovery tool/prefix/guides and configurable 35/45/55°C fan instructions.

Matching original Linux/U-Boot sources, tested configuration, patches, recipes and licenses are supplied in `odroid-u3-v1.0.3-sources.zip` (SHA256 `c76fca8b28ce2b105d354172aafcbc037bdfb4ac6b08678cc2f35b8aa2c9e3de`). The kernel/U-Boot/input hashes are pinned; byte-identical rebuilds against later moving Ubuntu package repositories are not claimed.

Open gates: physical first boots of these exact ZIPs for every claimed variant/medium; exact BL1/BL2/TrustZone redistribution/source coverage; explicit publication approval. These new images have not yet been physically booted. Current physical HDMI/desktop/microphone, unused external peripherals and long-duration reliability are not inferred. The tested kernel remains running; no firmware change was made.
