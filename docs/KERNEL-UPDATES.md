# Kernel updates through APT

[Deutsch](KERNEL-UPDATES.de.md)

The shared repository is [the-ab/deb](https://github.com/the-ab/deb), served at **https://the-ab.github.io/deb/**. It can host separate components for other projects. `main` contains shared packages; `u3` is reserved for ODROID-U3. XU4 requires its own packages and acceptance. The initial published repository contains signed empty indices; creating it does not publish a kernel release.

Images from 1.0.1 install these packages locally: `the-ab-archive-keyring`, `odroid-u3-kernel-tools`, `linux-image-6.12.114-odroidu3-v1`, and the tracking metapackage `linux-image-odroid-u3`. They also install `/etc/apt/sources.list.d/the-ab-odroid-u3.sources`:

```text
Types: deb
URIs: https://the-ab.github.io/deb/
Suites: stable
Components: main u3
Architectures: armhf
Signed-By: /usr/share/keyrings/the-ab-archive-keyring.gpg
```

Archive signing fingerprint: `E85346CA2461E1FA45AC7C7CD85BC090497CE8B9`. This public archive key verifies packages; it is unrelated to SSH login keys. No trust bypass is needed. A newer approved metapackage pulls the corresponding versioned kernel:

```sh
sudo apt update
apt-cache policy linux-image-odroid-u3
sudo apt upgrade
odroid-kernel status
# Reboot when convenient, after a successful update:
sudo reboot
uname -r
odroid-kernel status
sudo journalctl -b -p err --no-pager
```

The tools check the U3/Exynos4412 identity, root on SD/eMMC partition 2, and the matching FAT partition 1 mounted at `/boot`. They verify kernel, DTB, modules and uImage hashes/CRCs before switching versioned extlinux files and the legacy `uImage`. Existing boot arguments and a backup of the previous boot files are retained. Ordinary write/readback failures restore the prior files. Installation fails rather than activating on a different board or unmounted boot partition. Boot0, U-Boot, BL1/BL2 and TrustZone are not updated. There is no automatic reboot.

Do not remove the running kernel or the next-boot/rollback kernel. Versioned kernels are excluded from APT autoremove. Older packages and managed boot copies are retained; check free space before updates. A changed compiled payload requires a new kernel release suffix, so it cannot overwrite a previous fallback under the same directory name.

While the machine is still accessible, restore the previous boot files with:

```sh
sudo odroid-kernel rollback
odroid-kernel status
sudo reboot
```

Rollback is a local recovery action, not an automatic rescue from a kernel that cannot boot. If SSH and the console are unavailable, power down and mount the medium on another Linux system. Inspect `/var/lib/odroid-kernel/state.json` on its root partition; the `previous_snapshot` directory contains `uImage`, `extlinux/extlinux.conf` and a SHA256 `BACKUP.json`. Verify the named snapshot belongs to this root PARTUUID, restore those two files to its boot partition, sync and unmount. Retain the corresponding `/usr/lib/modules/<release>` on the root partition. Power loss during filesystem writes still requires recovery; ordinary error rollback cannot guarantee survival of media corruption.

## Build and publication

Build committed recipes only. The Linux artifact directory must match the board release and include `zImage`, DTB, config, System.map and modules. Build locally with:

```sh
python3 scripts/build-kernel-debs.py --kernel /path/to/kernel-artifacts \
  --keyring /path/to/deb/the-ab-archive-keyring.gpg --output /new/package-output
```

For fresh marked image roots, use `sudo unshare --mount --pid --fork bash scripts/install-kernel-packages.sh ROOTFS PACKAGE_OUTPUT` before assembly. This explicitly defers activation on the build host. Do not use that build-only bypass on installed devices.

For an approved kernel release, provide the exact upstream Linux archive, complete local patch/configuration and packaging source commit with checksums in the product's source release. Kernel DEBs contain no vendor boot firmware. Copy reviewed shared DEBs to `deb/pool/main/` and U3 DEBs to `deb/pool/u3/`, preserving previous versions. Run `scripts/build-apt-repository.py --root /path/to/deb --gpg-home /private/signing/home --signing-key FINGERPRINT`, review all signed index changes and then publish. The private signing key must stay outside both repositories. Images and large source archives belong in product Releases, not the Pages site. The index builder limits individual DEBs to 95 MiB; respect the overall GitHub Pages size limits as additional projects grow.

Local package installation, signature checks and file rollback tests have passed. A real signed APT update to Linux 7.3.1, a native boot, rollback to 6.12.114 and return to 7.3.1 have passed on the test eMMC. A candidate build is never automatically published into `stable`.

Minimal image 1.0.1 has now booted natively from eMMC. The installed package versions/files, running v1 kernel, update-tool board/media/payload checks and APT source/key/signature were verified. This accepts the preinstalled image packages; the subsequent signed APT update/rollback/return test has also passed, as documented below.

On 2026-10-30, signed private APT packages performed6.12.114 → 7.3.1 → 6.12.114 → 7.3.1 with real native eMMC boots. Final runtime:7.3.1-odroidu3-v1. Boot0/boot1, SSH keys and existing source configuration were unchanged. v1 and its modules remain as fallback. Public stable package publication is a separate approval; this test did not publish the candidate. Versioned files live in `/boot/odroid-kernels/<release>/`; extlinux selects them, while `/boot/uImage` also serves the legacy path. Image-release metadata describes the original image; use `uname -r` and `odroid-kernel status` for the active kernel.
