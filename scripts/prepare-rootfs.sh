#!/bin/bash
# SPDX-License-Identifier: GPL-2.0-only
set -euo pipefail
root=$(realpath -- "${1:?rootfs path required}")
variant=${2:?minimized or minimal required}
repo=$(cd -- "$(dirname -- "$0")/.." && pwd)
[[ $variant == minimized || $variant == minimal ]]
[[ $EUID == 0 && "$root" == */rootfs-"$variant" && -f "${root%/*}/.odroid-workspace" ]]
[[ -f "$root/etc/os-release" && ! -L "$root" ]]
[[ $(readlink /proc/self/ns/mnt) != $(readlink /proc/1/ns/mnt) ]]
setfacl -R -b -k "$root"
chmod 755 "$root"
mount --make-rprivate /
mount -t proc -o nosuid,nodev,noexec proc "$root/proc"
mount -t tmpfs -o mode=755,nosuid tmpfs "$root/dev"
mount -t tmpfs -o mode=755,nosuid,nodev tmpfs "$root/run"
for spec in 'null 1 3' 'zero 1 5' 'random 1 8' 'urandom 1 9' 'tty 5 0'; do
    read -r name major minor <<< "$spec"
    mknod -m 666 "$root/dev/$name" c "$major" "$minor"
done
ln -s /proc/self/fd "$root/dev/fd"
ln -s /proc/self/fd/0 "$root/dev/stdin"
ln -s /proc/self/fd/1 "$root/dev/stdout"
ln -s /proc/self/fd/2 "$root/dev/stderr"
printf '#!/bin/sh\nexit 101\n' > "$root/usr/sbin/policy-rc.d"
chmod 755 "$root/usr/sbin/policy-rc.d"
rm -f "$root/etc/resolv.conf"
cp /etc/resolv.conf "$root/etc/resolv.conf"
cat > "$root/etc/apt/sources.list.d/ubuntu.sources" <<'APT'
Types: deb
URIs: http://ports.ubuntu.com/ubuntu-ports/
Suites: resolute resolute-updates resolute-security
Components: main universe restricted multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
APT
chroot "$root" /usr/bin/env DEBIAN_FRONTEND=noninteractive SYSTEMD_OFFLINE=1 IMAGE_VARIANT="$variant" /bin/bash -eux <<'CHROOT'
apt-get update
apt-get dist-upgrade -y --no-install-recommends
apt-get install -y --no-install-recommends systemd-sysv systemd-timesyncd udev dbus openssh-server sudo \
    systemd-resolved netplan.io iproute2 iputils-ping ca-certificates kmod \
    e2fsprogs dosfstools less nano tzdata locales netbase cloud-guest-utils \
    wireless-regdb mmc-utils unminimize apparmor auditd
if [[ $IMAGE_VARIANT == minimal ]]; then
    apt-get install -y --no-install-recommends ubuntu-minimal ubuntu-standard \
        bash-completion manpages curl htop ethtool tcpdump
    python3 -c 'import subprocess; subprocess.run(["unminimize"],input="y\ny\n",text=True,check=True)'
    test ! -e /etc/dpkg/dpkg.cfg.d/excludes
    test ! -e /etc/dpkg/dpkg.cfg.d/excludes.dpkg-tmp
    test ! -e /etc/update-motd.d/60-unminimize
fi
dpkg --configure -a
printf 'odroid-u3\n' > /etc/hostname
printf '127.0.0.1 localhost\n127.0.1.1 odroid-u3\n::1 localhost ip6-localhost ip6-loopback\n' > /etc/hosts
ln -sf /usr/share/zoneinfo/Etc/UTC /etc/localtime
printf 'Etc/UTC\n' > /etc/timezone
printf 'en_US.UTF-8 UTF-8\n' > /etc/locale.gen
locale-gen
printf 'LANG=en_US.UTF-8\n' > /etc/default/locale
for group in video render audio dialout plugdev; do
    getent group "$group" >/dev/null || groupadd --system "$group"
done
id odroid >/dev/null 2>&1 || useradd -m -s /bin/bash -G sudo,video,render,audio,dialout,plugdev odroid
passwd -l root
printf 'odroid:odroid\n' | chpasswd
rm -f /etc/sudoers.d/90-odroid
rm -rf /root/.ssh /home/odroid/.ssh
mkdir -p /etc/ssh/sshd_config.d
printf 'PasswordAuthentication yes\nKbdInteractiveAuthentication no\nPermitRootLogin prohibit-password\n' > /etc/ssh/sshd_config.d/10-image-access.conf
cat > /etc/netplan/10-ethernet.yaml <<'NETPLAN'
network:
  version: 2
  renderer: networkd
  ethernets:
    wired:
      match:
        driver: "smsc95xx"
      dhcp4: true
      dhcp-identifier: mac
      dhcp6: true
      dhcp4-overrides:
        use-hostname: false
      dhcp6-overrides:
        use-hostname: false
      optional: true
NETPLAN
chmod 600 /etc/netplan/10-ethernet.yaml
# An upstream kernel lacks Ubuntu's optional downstream userns sysctl.
# Preserve the requested value if supported later; ignore only a missing key.
python3 - <<'COMPAT'
from pathlib import Path
p=Path('/usr/lib/sysctl.d/10-apparmor.conf')
if p.exists():
 s=p.read_text()
 s=s.replace('kernel.apparmor_restrict_unprivileged_userns =', '-kernel.apparmor_restrict_unprivileged_userns =').replace('kernel.apparmor_restrict_unprivileged_userns=', '-kernel.apparmor_restrict_unprivileged_userns=')
 Path('/etc/sysctl.d/10-apparmor.conf').write_text(s)
 Path('/etc/sysctl.d/10-apparmor.conf').chmod(0o644)
p=Path('/etc/default/cron')
if p.exists() and 'EXTRA_OPTS=' not in p.read_text():
 with p.open('a') as f:f.write('\nEXTRA_OPTS=""\n')
COMPAT
systemctl enable apparmor auditd
systemctl enable systemd-networkd systemd-resolved systemd-timesyncd ssh serial-getty@ttySAC1.service
cat > /etc/systemd/system/odroid-host-keys.service <<'UNIT'
[Unit]
Description=Generate unique SSH host keys on first boot
DefaultDependencies=no
After=local-fs.target systemd-random-seed.service
RequiresMountsFor=/etc/ssh
Before=ssh.service ssh.socket sshd-keygen.service shutdown.target
Conflicts=shutdown.target
[Service]
Type=oneshot
ExecStart=/usr/bin/ssh-keygen -A
RemainAfterExit=yes
[Install]
WantedBy=multi-user.target
UNIT
cat > /etc/systemd/system/odroid-grow-root.service <<'UNIT'
[Unit]
Description=Expand the new ODROID image to its SD or eMMC medium
After=local-fs.target
ConditionPathExists=!/var/lib/odroid-image/root-expanded
[Service]
Type=oneshot
ExecStart=/usr/local/sbin/odroid-grow-root
RemainAfterExit=yes
[Install]
WantedBy=multi-user.target
UNIT
mkdir -p /etc/systemd/system/ssh.service.d /etc/systemd/system/ssh.socket.d
for unit in ssh.service ssh.socket; do
    printf '[Unit]\nRequires=odroid-host-keys.service\nAfter=odroid-host-keys.service\n' > "/etc/systemd/system/$unit.d/host-keys.conf"
done
systemctl enable odroid-host-keys.service odroid-grow-root.service
apt-get clean
rm -rf /var/lib/apt/lists/*
rm -f /etc/ssh/ssh_host_* /etc/machine-id /var/lib/dbus/machine-id /var/lib/systemd/random-seed
touch /etc/machine-id
ln -sf /etc/machine-id /var/lib/dbus/machine-id
rm -f /usr/sbin/policy-rc.d /etc/resolv.conf
ln -s ../run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
CHROOT
python3 "$repo/scripts/install-u3-features.py" --root "$root"
chroot "$root" dpkg --audit
# dpkg-query expands these fields; the host shell must leave them literal.
# shellcheck disable=SC2016
chroot "$root" dpkg-query -W -f='${Package}\t${Version}\t${Architecture}\n' > "${root%/*}/packages-$variant.tsv"
echo "Fresh $variant rootfs prepared"
