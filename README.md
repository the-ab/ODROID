# ODROID

[Deutsch](README.de.md)

Community Ubuntu images, build recipes and board support for ODROID systems. The first target is **ODROID-U3 / Exynos4412**, running Ubuntu **26.04.1 armhf** with Linux **6.12.114-odroidu3-v1** and U-Boot **2026.10**. XU4 support is planned separately.

**Release preparation:** new images are candidates until their first-boot acceptance and release checks are complete. See [releases](https://github.com/the-ab/ODROID/releases) for published downloads and [hardware status](docs/HARDWARE.md) for what has actually been tested.

| Variant | Contents |
|---|---|
| `minimized` | Reduced Ubuntu Base, SSH, sudo, networking and board support; documentation remains minimized. Includes the real `unminimize` command. |
| `minimal` | `ubuntu-minimal`, `ubuntu-standard`, usual administration tools, restored documentation/man pages and shell completion. |

Both variants boot to a console and SSH. There is one human account: **`odroid` / `odroid`**, with password-protected sudo. Root's password is locked; SSH accepts a public key that the owner installs in `/root/.ssh/authorized_keys` (since image 1.0.1). No maintenance authorized keys, fixed SSH host keys or cloned machine identity are included. Set your own password after the first login with `passwd`.

Ethernet uses DHCP and a stable MAC derived from the board's hardware identity when the driver has no permanent address. Both variants enable automatic network time synchronization. The root partition expands on first boot. SD and eMMC user-area layouts use the same image format; native eMMC may need the separate boot0 repair described below.

- [Install and first login](docs/INSTALL.md)
- [Native eMMC boot0 repair, backup and restore](docs/EMMC-RECOVERY.md)
- [Fan control: 35/45/55 °C and changing thresholds](docs/FAN.md)
- [Graphics, Mesa and desktop limitations](docs/GRAPHICS.md)
- [Build from pinned inputs](docs/BUILD.md)
- [Hardware verification and release requirements](docs/HARDWARE.md)

The kernel and scripts are provided with their source and licenses. Vendor boot firmware is not stored in this Git repository; its exact distribution/source coverage must be documented before public binary releases. Ubuntu packages and firmware retain their own licenses. See [release requirements](docs/RELEASES.md).

Kernel packages and signed APT updates: [guide](docs/KERNEL-UPDATES.md).

A separate [Linux 7.3.1 candidate](boards/u3/kernel-candidates/7.3.1/README.md) has passed native APT/rollback/return and headphone tests. The existing1.0.1 image artifacts remain unchanged. See [security review](docs/SECURITY-REVIEW.md) and [audio](docs/AUDIO.md).
