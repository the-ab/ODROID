# U3 image 1.0.3 validation

[Deutsch](CANDIDATE-1.0.3.de.md)

Ubuntu 26.04.1 armhf; kernel `7.3.1-odroidu3-v32`, DEB `7.3.1-33`, activation tools `1.0.3`. Original compiled/package recipe: `b8ce206a44451aa64452add634a3e6376b60d6be`. The cleaned source retains identical canonical kernel configuration, effective patch and packaged runtime scripts; obsolete experiment profiles are retained in history only.

| Variant | Exact IMG SHA256 |
|---|---|
| minimized | `9315325dca3de5de9afa393b259020dedf2ebe2232be250be87680de458e6d0f` |
| minimal | `98160d764b5e5fa6f022c1d06df63c49893a42f29c152d66494dacb4fa19ee26` |

The ZIP may be repacked with updated documentation without changing these IMG bytes. Use its accompanying `.sha256` file; hashes of earlier ZIP packaging are not interchangeable. Full image ZIPs remain draft-only pending documented boot-firmware redistribution/source coverage.

The same compiled kernel/DTB/module bytes passed ten pure warmstarts and five controlled halt/cold starts on the retained 1.0.2 test installation. Nine functional cases (Docker, VPN/firewall, files, security, modules, bounded load, internal stereo loop, ordinary non-root io_uring, real Ethernet) and two final health/readback cases passed. Every boot verified four CPU timers and all 351 modules. Lockdep remained enabled; no new kernel warnings, failed units or audit loss remained. NFS used journal-confirmed nfsdcld tracking. Ethernet verified 16 MiB each way. Owned test fixtures were removed.

Both freshly built variants passed ARM login/PAM, password-protected sudo, root-key policy, default-human-account-only, no maintenance/host keys or copied identity, numeric ownership/no inherited host ACLs, systemd/network/time/security ordering, signed APT configuration, complete filesystem/partition/boot readback and ZIP CRC/IMG roundtrip.

**Physical first boot:** the owner wrote the exact minimal IMG to native eMMC. Its complete installed package manifest, 351 module/payload/boot/configuration hashes, root expansion, default access, owner-installed root key, DHCP identity, NTP, fan, AppArmor/audit, CPU timers, journal and services passed. The owner reported a successful warmstart. Fresh minimized/SD first boots remain open. The new installation contains only v32; historic rollback backups are not a preinstalled fallback for a freshly written medium.

Matching complete Linux/U-Boot source archives, tested configuration, patches, recipes and licenses accompany the kernel source release as `odroid-u3-v1.0.3-corresponding-sources.zip`. Its manifest maps original package provenance to the cleaned source. Identical later Ubuntu package builds are not promised because upstream APT contents move. Current physical HDMI/desktop/microphone, unexercised external peripherals and long-duration reliability are not inferred. See [release conditions](RELEASES.md).
