#!/bin/bash
# SPDX-License-Identifier: GPL-2.0-only
set -euo pipefail
root=$(realpath -- "${1:?fresh rootfs required}")
debs=$(realpath -- "${2:?local package directory required}")
[[ $EUID == 0 && "$root" == */rootfs-* && -f "${root%/*}/.odroid-workspace" && ! -L "$root" ]]
[[ $(readlink /proc/self/ns/mnt) != $(readlink /proc/1/ns/mnt) ]]
[[ -f "$debs/PACKAGES.json" && ! -e "$root/usr/sbin/policy-rc.d" ]]
mount --make-rprivate /
mount -t proc -o nosuid,nodev,noexec proc "$root/proc"
mount -t tmpfs -o mode=755,nosuid tmpfs "$root/dev"
mount -t tmpfs -o mode=755,nosuid,nodev tmpfs "$root/run"
for spec in 'null 1 3' 'zero 1 5' 'random 1 8' 'urandom 1 9'; do
    read -r name major minor <<< "$spec"
    mknod -m 666 "$root/dev/$name" c "$major" "$minor"
done
mkdir "$root/run/kernel-debs"
mount --bind "$debs" "$root/run/kernel-debs"
mount -o remount,bind,ro "$root/run/kernel-debs"
printf '#!/bin/sh\nexit 101\n' > "$root/usr/sbin/policy-rc.d"
chmod 755 "$root/usr/sbin/policy-rc.d"
rm "$root/etc/resolv.conf"
cp /etc/resolv.conf "$root/etc/resolv.conf"
finish() {
    rm -f "$root/usr/sbin/policy-rc.d" "$root/etc/resolv.conf"
    ln -s ../run/systemd/resolve/stub-resolv.conf "$root/etc/resolv.conf"
}
trap finish EXIT
chroot "$root" /usr/bin/env ODROID_IMAGE_BUILD=1 DEBIAN_FRONTEND=noninteractive SYSTEMD_OFFLINE=1 /bin/bash -eu <<'CHROOT'
cd /run/kernel-debs
dpkg -i ./the-ab-archive-keyring_*.deb ./odroid-u3-kernel-tools_*.deb ./linux-image-[0-9]*.deb ./linux-image-odroid-u3_*.deb
apt-get update -o Dir::Etc::sourcelist=/etc/apt/sources.list.d/the-ab-odroid-u3.sources -o Dir::Etc::sourceparts=-
apt-cache policy linux-image-odroid-u3
test -z "$(dpkg --audit)"
test ! -e /var/lib/odroid-kernel/state.json
rm -rf /var/lib/apt/lists/*
CHROOT
# shellcheck disable=SC2016
chroot "$root" dpkg-query -W -f='${Package}\t${Version}\t${Architecture}\n' > "${root%/*}/packages-${root##*/rootfs-}.tsv"
echo 'Local kernel packages installed and public APT signature verified; boot activation deferred to image assembly'
