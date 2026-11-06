#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Install generic board support into a fresh build root, never the host."""
from pathlib import Path
import argparse,json,os,shutil,subprocess
if not __debug__:raise SystemExit('Run without Python optimization: validation must remain enabled')

p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True);args=p.parse_args()
root=args.root.resolve();repo=Path(__file__).resolve().parent.parent
assert os.geteuid()==0 and root.name in ('rootfs-minimized','rootfs-minimal')
assert (root.parent/'.odroid-workspace').is_file() and (root/'etc/os-release').is_file()
support=repo/'boards/u3/support'
# Order our recovery-capable generator before Ubuntu's first-boot-only helper.
unit=root/'etc/systemd/system/odroid-host-keys.service'
unit.write_text(unit.read_text().replace('Before=ssh.service ssh.socket shutdown.target',
                                       'Before=ssh.service ssh.socket sshd-keygen.service shutdown.target'))
for name in ['odroid-fan','odroid-network-identity','odroid-grow-root']:
    target=root/'usr/local/sbin'/name;shutil.copyfile(support/name,target);target.chmod(0o755)
for name in ['odroid-fan.service','odroid-network-identity.service']:
    target=root/'etc/systemd/system'/name;shutil.copyfile(support/name,target);target.chmod(0o644)
target=root/'usr/local/bin/odroid-gpu';shutil.copyfile(support/'odroid-gpu',target);target.chmod(0o755)
for name in ['systemd-udevd.service','systemd-udev-trigger.service','systemd-networkd.service']:
    directory=root/'etc/systemd/system'/(name+'.d');directory.mkdir(parents=True,exist_ok=True)
    (directory/'10-odroid-identity.conf').write_text('[Unit]\nWants=odroid-network-identity.service\nAfter=odroid-network-identity.service\n')
(root/'etc/default/odroid-fan').write_text('# Celsius, dedicated fan trips; CPU protection is preserved.\nFAN_LOW=35\nFAN_MEDIUM=45\nFAN_HIGH=55\n')
directory=root/'usr/share/odroid-u3';directory.mkdir(parents=True,exist_ok=True)
layout={'thermal_type':'cpu-thermal','fan_trip_ids':[4,5,6],'cpu_protection_trip_ids':[0,1,2,3],'default_temperatures_celsius':[35,45,55],'hysteresis_celsius':3,'pwm_levels':[0,102,170,255],'kernel_release':json.loads((repo/'boards/u3/board.json').read_text())['kernel_release']}
(directory/'fan-layout.json').write_text(json.dumps(layout,indent=2)+'\n')
for unit in ['odroid-network-identity.service','odroid-fan.service']:
    subprocess.run(['systemctl','--root='+str(root),'enable',unit],check=True)
assert not any(root.rglob('authorized_keys'))
print('Generic U3 identity, fan, expansion and optional GPU command installed')
