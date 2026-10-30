# Build U3 candidates

[Deutsch](BUILD.de.md)

Use a Linux build host with Python 3.11+, root access for an isolated chroot, a working ARM hard-float binfmt/QEMU interpreter and sufficient disk space for kernel/rootfs/image staging. The verified cross compiler was GCC 13.3.0. Example Ubuntu build dependencies:

```sh
sudo apt install build-essential python3 gnupg patch util-linux xz-utils gcc-arm-linux-gnueabihf binutils-arm-linux-gnueabihf \
  bc bison flex libssl-dev libgnutls28-dev device-tree-compiler u-boot-tools \
  qemu-user-static binfmt-support mtools dosfstools e2fsprogs kmod acl unzip zip shellcheck
```

Start in this repository. Use a **new** work directory outside Git; scripts refuse existing output directories. The workspace marker limits rootfs operations to explicit image roots.

```sh
repo=$(pwd)
work=$(realpath -m ../ODROID-build-v1)
mkdir -p "$work/cache"
touch "$work/.odroid-workspace"
python3 scripts/fetch-sources.py --cache "$work/cache" \
  --boot-reference /path/to/odroid_u3-armv7l-ubuntu20.04minimal-1601403301.zip
```

The matching extracted reference IMG is also accepted. The reference is used only for hash-checked BL1/BL2/TrustZone blocks; its OS, users and access keys are never copied. Vendor boot blobs are not in Git, and binary redistribution coverage remains a release requirement. All upstream source/base/firmware downloads are pinned in `sources.lock.json`. The Ubuntu Base input was checked against its signed manifest using Ubuntu CD Image key `843938DF228D22F7B3742BC0D94AA3F0EFE21092`.

```sh
bash scripts/build-kernel.sh "$work/cache/linux-6.12.114.tar.xz" "$work/linux-v1"
sudo bash scripts/prepare-kernel-artifacts.sh "$work/linux-v1" "$work/kernel-v1"

mkdir "$work/u-boot"
tar -xzf "$work/cache/u-boot-v2026.10.tar.gz" --strip-components=1 -C "$work/u-boot"
make -C "$work/u-boot" ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- odroid_defconfig
make -C "$work/u-boot" ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j4
```

The U-Boot binary must fit its 1 MiB reserved region. Build-time/compiler differences can change its hash; record the actual binary and retain the matching source/configuration. A rebuilt bootloader is not automatically hardware-accepted because its source tag matches an earlier build.

For each variant, using `variant=minimized` or `variant=minimal`:

```sh
variant=minimized
root="$work/rootfs-$variant"
out="$work/output-$variant"
sudo mkdir "$root"
sudo tar --numeric-owner -xpf "$work/cache/ubuntu-base-26.04.1-base-armhf.tar.gz" -C "$root"
sudo unshare --mount --pid --fork bash "$repo/scripts/prepare-rootfs.sh" "$root" "$variant"
sudo unshare --mount --pid --fork bash "$repo/scripts/install-kernel-packages.sh" "$root" "$work/kernel-debs"
sudo python3 "$repo/scripts/assemble-image.py" --root "$root" \
  --kernel "$work/kernel-v1" --uboot "$work/u-boot/u-boot-dtb.bin" \
  --firmware "$work/cache" --output "$out" --variant "$variant"
sudo unshare --mount --pid --fork bash "$repo/scripts/validate-rootfs.sh" "$root" "$variant" \
  > "$work/qa-$variant.log" 2>&1
sudo python3 "$repo/scripts/verify-image.py" --output "$out" --qa-log "$work/qa-$variant.log"
sudo python3 "$repo/scripts/package-image.py" --output "$out"
```

Assembly accepts regular output files only. A 2 GiB IMG has a 256 MiB FAT16 boot partition at sector 32768 and an ext4 root partition; first boot expands root. No initrd is required by this configuration. Host ACLs are removed from image trees while file capabilities and required Unix permissions are preserved.

APT uses current signed Ubuntu 26.04 repositories; `PACKAGES.tsv` captures each build's actual versions. Pinned source inputs and build steps are provided, but identical bytes across later moving package repositories/build environments are not claimed.

Run source checks with `python3 -m unittest discover -s tests -v`, Python compilation and shellcheck. Offline ARM/image/ZIP checks do not replace physical first-boot acceptance. See [release requirements](RELEASES.md).

Build the local `kernel-debs` directory as described in [kernel updates](KERNEL-UPDATES.md) before image assembly.
