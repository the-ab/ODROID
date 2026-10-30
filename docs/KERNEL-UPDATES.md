# Kernel updates through APT

[Deutsch](KERNEL-UPDATES.de.md)

The signed repository is [the-ab/deb](https://the-ab.github.io/deb/), with shared `main` and board-specific `u3` components. The current server kernel is **7.3.1-odroidu3-v3**, package **7.3.1-4**, with activation tools **1.0.2**. Earlier kernel/metapackage versions were retired from the current APT pool at the owner's request after testing their replacement. Installed fallback kernels and local backups remain available; they are not automatically removed. Historical sources/Git history are preserved. [Package manifest](https://github.com/the-ab/deb/blob/main/publications/u3-server-2026-10-30.json) · [Complete matching sources](https://github.com/the-ab/ODROID/releases/tag/u3-server-kernel-7.3.1-4).

Images from1.0.1 include the public key and source below. Image1.0.1 originally shipped6.12.114-v1; fresh1.0.2 uses7.3.1-v3. The image version describes the original installation; use `uname -r` for the running kernel.

```text
Types: deb
URIs: https://the-ab.github.io/deb/
Suites: stable
Components: main u3
Architectures: armhf
Signed-By: /usr/share/keyrings/the-ab-archive-keyring.gpg
```

Archive fingerprint: `E85346CA2461E1FA45AC7C7CD85BC090497CE8B9`. It is independent of SSH login keys. No trust bypass is required.

```sh
sudo apt update
apt-cache policy linux-image-odroid-u3
sudo apt install linux-image-odroid-u3
odroid-kernel status
# After successful installation, reboot deliberately:
sudo reboot
uname -r
sudo journalctl -b -p err --no-pager
```

The tracking metapackage pulls a versioned kernel. Installation verifies U3/Exynos4412 identity, root partition2, the matching FAT partition1 mounted at `/boot`, module/payload hashes and uImage CRCs. It writes immutable versioned files directly under `/boot`: `vmlinuz-<release>`, `uImage-<release>`, `config-<release>`, `System.map-<release>` and `exynos4412-odroidu3-<release>.dtb`. Extlinux selects them and `/boot/uImage` remains the active legacy copy. Existing valid arguments and old boot copies are retained. No initramfs is needed for the shipped unencrypted ext4 root. Older installations' `/boot/odroid-kernels/` paths remain usable for existing recovery snapshots; new activations use the flat layout.

The tools verify all new files before switching the selectors. Ordinary write/readback failures restore the previous selectors. Boot0/U-Boot/BL1/BL2/TrustZone are never changed and installation never reboots automatically. Keep sufficient boot-partition space. Removal of the running, next-boot or saved rollback kernel is refused; versioned kernels are excluded from autoremove. A changed compiled payload always receives a new board suffix.

For the last saved selection:

```sh
sudo odroid-kernel rollback
odroid-kernel status
sudo reboot
```

For an already installed specific fallback:

```sh
sudo odroid-kernel activate 7.3.1-odroidu3-v2
odroid-kernel status
# Reboot only after checking the result.
```

That example requires v2 to be installed locally; it is not a download promise. Fresh images contain only their shipped kernel, so prepare a tested fallback/backup before a future update. Rollback is a local recovery operation, not an automatic rescue from an unbootable kernel. If SSH/console are unavailable, power off and mount the medium on another Linux system. Read `/var/lib/odroid-kernel/state.json` on root. Its `previous_snapshot` contains `uImage`, `extlinux/extlinux.conf` and `BACKUP.json`; verify hashes and matching root PARTUUID, restore the two named files to boot, sync and unmount. Keep the matching modules. Power-loss/media corruption can still require external recovery.

Signed native APT tests passed6.12.114→7.3.1-v1→6.12.114→7.3.1-v1, then the fresh reset baseline→server-v2→server-v3. v2/v3 retained fallback files and modules. v3 passed Docker, VPN, firewall, file-service and security tests; see [scope and limits](SERVER-KERNEL.md). Fresh image first boots are separate acceptance steps.

## Build and publish

Use committed recipes and matching artifact configuration. Build with `scripts/build-kernel-debs.py --kernel ARTIFACTS --keyring PUBLIC_KEY --output NEW_OUTPUT --tools-version 1.0.2`. Explicit pinned candidate profiles use `--profile`, `--release` and `--version`. Shared packages already published under a version must retain their exact bytes. Kernel DEBs contain no vendor boot firmware.

Fresh marked image roots use `sudo unshare --mount --pid --fork bash scripts/install-kernel-packages.sh ROOTFS DEBS`; activation is deferred only during image assembly. Never use that image-build bypass on an installed device. Publish exact complete Linux source, patch/configuration and packaging recipes/licenses/checksums alongside packages. Copy approved DEBs into the correct component, rebuild signed SHA256/SHA512 by-hash indices with `scripts/build-apt-repository.py`, verify downloads/signatures and deploy. Keep private signing material outside Git. Preserve old versions by default; removal needs the owner's explicit scope and a verified replacement. Other projects' components remain independent. Large sources/images belong in product Releases; individual DEBs here are limited to95MiB and overall Pages limits still apply.

Package7.3.1-4 adds the missing removal hook without changing the compiled kernel. Purge removes generated module indices and hash-matching boot copies, prunes inactive matching menu entries and preserves running/selected/rollback kernels, modified files, shared references and unknown modules. A real inactive-package apt-purge test on the U3 passed. Existing residue from older packages needs one controlled cleanup because their old scripts cannot retroactively gain the hook.
