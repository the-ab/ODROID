# ODROID

[Deutsch](README.de.md)

Community Ubuntu images, kernel packages and build recipes for **ODROID-U3 / Exynos4412**. The current recipe is **Ubuntu 26.04.1 armhf, image 1.0.3**, with **Linux 7.3.1-odroidu3-v32** (package `7.3.1-33`) and U-Boot 2026.10. XU4 support is planned separately.

[Kernel downloads and matching sources](https://github.com/the-ab/ODROID/releases/tag/u3-kernel-7.3.1-33) · [Signed APT repository](https://the-ab.github.io/deb/) · [Installation](docs/INSTALL.md)

**Image downloads:** the full 1.0.3 image ZIPs remain unpublished while the exact Samsung/Hardkernel BL1, BL2 and TrustZone redistribution/source conditions are unresolved. The kernel packages contain none of these boot blobs and are distributed separately. See [release status](docs/RELEASES.md). The [boot firmware review](docs/BOOT-FIRMWARE.md) records the exact matched archive and remaining evidence.

| Variant | Contents |
|---|---|
| `minimized` | Ubuntu Base, SSH, sudo, networking and board support; documentation remains minimized. Includes the official `unminimize` command. |
| `minimal` | Ubuntu minimal/standard metapackages, usual administration tools, documentation, man pages and shell completion. |

Both boot to console and SSH. The default human account is **`odroid` / `odroid`**, with password-protected sudo. Change the password after first login. Root's password is locked; owners can install their own public keys in `/root/.ssh/authorized_keys`. No maintenance keys, fixed SSH host keys or cloned machine identity are shipped.

Ethernet uses DHCP and a stable hardware-derived MAC when the driver has no permanent address. Network time synchronization is enabled and the root partition expands on first boot. Native eMMC may need the separate boot0 repair; writing the IMG through a reader updates only the user area.

- [Installation and root-key access](docs/INSTALL.md)
- [eMMC boot0 repair, backup and restore](docs/EMMC-RECOVERY.md)
- [Fan thresholds: 35/45/55 °C and customization](docs/FAN.md)
- [Kernel installation, updates and rollback](docs/KERNEL-UPDATES.md)
- [Hardware verification](docs/HARDWARE.md) and [1.0.3 validation](docs/CANDIDATE-1.0.3.md)
- [Server capabilities](docs/SERVER-KERNEL.md), [security review](docs/SECURITY-REVIEW.md), [audio](docs/AUDIO.md) and [graphics](docs/GRAPHICS.md)
- [Build instructions](docs/BUILD.md) and [platform fixes](docs/I2S-USB.md)

The v32 kernel passed ten pure warmstarts, five controlled halt/cold starts and the documented server tests with lockdep enabled and no new kernel warnings. A freshly written minimal 1.0.3 image also passed native-eMMC basic checks. Minimized/SD first boots and current physical graphics/microphone acceptance remain separate; these tests are not a long-duration reliability guarantee.

Linux, U-Boot, Ubuntu packages and firmware retain their respective licenses. Matching kernel sources, configuration, patches and packaging recipes accompany the kernel release. Obsolete experiment profiles have been removed from the current tree; historical commits and corresponding-source releases remain available.
