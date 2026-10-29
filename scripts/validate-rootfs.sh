#!/bin/bash
# SPDX-License-Identifier: GPL-2.0-only
set -euo pipefail
root=$(realpath -- "${1:?rootfs required}")
variant=${2:?variant required}
repo=$(cd -- "$(dirname -- "$0")/.." && pwd)
[[ $EUID == 0 && "$root" == */rootfs-"$variant" && -f "${root%/*}/.odroid-workspace" ]]
[[ $(readlink /proc/self/ns/mnt) != $(readlink /proc/1/ns/mnt) ]]
mount --make-rprivate /
mount -t proc -o nosuid,nodev,noexec proc "$root/proc"
mount -t tmpfs -o mode=755,nosuid tmpfs "$root/dev"
mount -t tmpfs -o mode=755,nosuid,nodev tmpfs "$root/run"
for spec in 'null 1 3' 'zero 1 5' 'random 1 8' 'urandom 1 9'; do
    read -r name major minor <<< "$spec"
    mknod -m 666 "$root/dev/$name" c "$major" "$minor"
done
mkdir -p "$root/run/sshd"
python3 - "$root" "$variant" <<'PY'
from pathlib import Path
import json,os,re,stat,sys
r=Path(sys.argv[1]);variant=sys.argv[2]
for directory,dirs,files in os.walk(r,followlinks=False):
    if Path(directory)==r:dirs[:]=[d for d in dirs if d not in ['proc','sys','dev','run']]
    for path in [Path(directory),*[Path(directory)/f for f in files]]:
        assert not any(x.startswith('system.posix_acl') for x in os.listxattr(path,follow_symlinks=False)),str(path)
users=[x.split(':') for x in (r/'etc/passwd').read_text().splitlines()]
assert [x[0] for x in users if 1000<=int(x[2])<65534]==['odroid']
assert [x[0] for x in users if int(x[2])==0]==['root']
shadow={x.split(':')[0]:x.split(':')[1] for x in (r/'etc/shadow').read_text().splitlines()}
assert shadow['root'].startswith(('!','*'))
assert shadow['odroid'] and not shadow['odroid'].startswith(('!','*'))
assert not any(r.rglob('authorized_keys')) and not any(r.rglob('authorized_keys2'))
assert not any((r/'etc/ssh').glob('ssh_host_*'))
assert not (r/'etc/machine-id').read_bytes()
assert not (r/'var/lib/systemd/random-seed').exists()
# Resolve merged-/usr and alternatives links relative to the target, not the host.
path='/usr/bin/sudo'
for _ in range(12):
    target=r/path.lstrip('/')
    if target.is_symlink():
        link=os.readlink(target)
        path=os.path.normpath(link if link.startswith('/') else str(Path(path).parent/link))
    else:break
else:raise AssertionError('sudo symlink loop')
assert target.stat().st_uid==0 and stat.S_IMODE(target.stat().st_mode)==0o4755
assert (r/'usr/bin/unminimize').is_file()
if variant=='minimal':
    assert not (r/'etc/dpkg/dpkg.cfg.d/excludes').exists()
    assert not (r/'etc/update-motd.d/60-unminimize').exists()
else:
    assert (r/'etc/dpkg/dpkg.cfg.d/excludes').exists()
    assert (r/'etc/update-motd.d/60-unminimize').exists()
print('Only odroid human login; root locked; sudo setuid; no authorized/host keys or cloned machine identity')
PY
chroot "$root" /usr/bin/ssh-keygen -q -t ed25519 -N '' -f /run/qa_host_key
chroot "$root" /usr/sbin/sshd -t -h /run/qa_host_key
chroot "$root" /usr/sbin/sshd -T -h /run/qa_host_key -C user=odroid,host=odroid-u3,addr=127.0.0.1 > "$root/run/sshd-effective.conf"
grep -x 'passwordauthentication yes' "$root/run/sshd-effective.conf"
grep -x 'permitrootlogin no' "$root/run/sshd-effective.conf"
chroot "$root" /usr/bin/python3 - < "$repo/scripts/pam-smoke.py"
chroot "$root" /usr/sbin/visudo -c
chroot "$root" /usr/bin/id odroid
chroot "$root" /usr/sbin/runuser -u odroid -- /bin/sh -c 'test -r /etc/hosts && test ! -w /etc/hosts && test ! -w /etc/passwd && test -r /etc/default/odroid-fan && test ! -w /etc/default/odroid-fan && test -r /usr/share/odroid-u3/fan-layout.json'
chroot "$root" /usr/bin/sudo -l -U odroid > "$root/run/sudo-policy.txt"
cat "$root/run/sudo-policy.txt"
if grep -q NOPASSWD "$root/run/sudo-policy.txt"; then exit 1; fi
chroot "$root" /usr/sbin/netplan generate
grep -x 'ClientIdentifier=mac' "$root/run/systemd/network/10-netplan-wired.network"
grep -x 'Driver=smsc95xx' "$root/run/systemd/network/10-netplan-wired.network"
grep -x 'UseHostname=false' "$root/run/systemd/network/10-netplan-wired.network"
chroot "$root" /usr/bin/systemd-analyze verify --man=no default.target ssh.socket ssh.service \
    odroid-host-keys.service odroid-grow-root.service odroid-network-identity.service odroid-fan.service \
    systemd-udevd.service systemd-udev-trigger.service > "$root/run/boot-verify.log" 2>&1
cat "$root/run/boot-verify.log"
if grep -Ei 'ordering cycle|Job .* deleted' "$root/run/boot-verify.log"; then exit 1; fi
test -z "$(chroot "$root" dpkg --audit)"
systemctl --root="$root" is-enabled ssh.service systemd-networkd.service systemd-resolved.service systemd-timesyncd.service \
    serial-getty@ttySAC1.service odroid-host-keys.service odroid-grow-root.service odroid-network-identity.service odroid-fan.service
if [[ $variant == minimal ]]; then
    chroot "$root" dpkg-query -W ubuntu-minimal ubuntu-standard
    chroot "$root" man -w ls
    chroot "$root" /usr/sbin/runuser -u odroid -- man -w ls
fi
echo 'Network time synchronization enabled'
echo 'Fresh ARM rootfs access/configuration validation passed; physical image boot remains separate'
