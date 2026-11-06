#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Independently read back image partitions, boot headers and security settings."""
from pathlib import Path
import argparse,hashlib,json,re,struct,subprocess,zlib
if not __debug__:raise SystemExit('Run without Python optimization: validation must remain enabled')

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--output',type=Path,required=True);p.add_argument('--qa-log',type=Path,required=True);a=p.parse_args()
out=a.output;manifest=json.loads((out/'BUILD-MANIFEST.json').read_text());image=out/manifest['image'];checks={}
qa=a.qa_log.read_text()
assert 'Fresh ARM rootfs access/configuration validation passed' in qa
assert 'Default odroid password matches Unix hash; wrong password rejected' in qa
assert 'Network time synchronization enabled' in qa
assert 'Local kernel packages, payloads, APT source and archive signing fingerprint verified' in qa
for service in ['login','sshd','sudo']:assert service+' ARM PAM authentication and account checks passed' in qa
assert 'ordering cycle' not in qa.lower()
with image.open('rb') as f:
    header=f.read(512);assert header[510:512]==b'\x55\xaa'
    assert struct.unpack_from('<I',header,440)[0]==int(manifest['disk_id'],16)
    for i,partition in enumerate(manifest['partitions']):
        start,size=struct.unpack_from('<II',header,446+i*16+8)
        assert (start,size)==(partition['start_sector'],partition['sectors'])
        f.seek(start*512);count=size*512;h=hashlib.sha256()
        while count:
            blob=f.read(min(count,1024*1024));assert blob;h.update(blob);count-=len(blob)
        stage=out/'stage'/('boot-partition.img' if i==0 else 'root-partition.img')
        with stage.open('rb') as s:assert h.hexdigest()==hashlib.file_digest(s,'sha256').hexdigest()
        checks['partition_'+str(i+1)+'_readback']=h.hexdigest()
    payload=(out/manifest['emmc_boot0_payload']['file']).read_bytes()
    assert len(payload)==1240064 and hashlib.sha256(payload).hexdigest()==manifest['emmc_boot0_payload']['sha256']
    for item in manifest['firmware_components']:
        f.seek(item['sd_sector']*512);blob=f.read(item['sectors']*512)
        assert hashlib.sha256(blob).hexdigest()==item['sha256']
        start=item['emmc_boot0_sector']*512;assert payload[start:start+len(blob)]==blob
checks['sd_and_boot0_offsets']=True
for name,kind in [('uImage',2),('boot.scr',6)]:
    blob=(out/'stage/boot'/name).read_bytes();v=struct.unpack('>7I4B32s',blob[:64])
    header=bytearray(blob[:64]);header[4:8]=b'\0'*4
    assert v[0]==0x27051956 and v[1]==zlib.crc32(header) and v[3]==len(blob)-64
    assert v[6]==zlib.crc32(blob[64:]) and v[9]==kind
    checks[name+'_crc']=True
root=out/'stage/root-partition.img'
def read(path):return subprocess.run(['debugfs','-R','cat '+path,str(root)],check=True,capture_output=True).stdout
def listing(path):return subprocess.run(['debugfs','-R','ls -p '+path,str(root)],check=True,capture_output=True,text=True).stdout
passwd=[line.split(':') for line in read('/etc/passwd').decode().splitlines()]
assert [x[0] for x in passwd if 1000<=int(x[2])<65534]==['odroid']
assert [x[0] for x in passwd if int(x[2])==0]==['root']
shadow={x.split(':')[0]:x.split(':')[1] for x in read('/etc/shadow').decode().splitlines()}
assert shadow['root'].startswith(('!','*')) and not shadow['odroid'].startswith(('!','*'))
assert 'PermitRootLogin prohibit-password\n' in read('/etc/ssh/sshd_config.d/10-image-access.conf').decode()
assert 'PasswordAuthentication yes\n' in read('/etc/ssh/sshd_config.d/10-image-access.conf').decode()
assert not read('/etc/machine-id')
for path in ['/root','/home/odroid']:assert '/.ssh/' not in listing(path)
assert 'ssh_host_' not in listing('/etc/ssh')
assert 'random-seed' not in listing('/var/lib/systemd')
assert 'systemd-timesyncd.service' in listing('/etc/systemd/system/sysinit.target.wants')
for path in ['/','/etc','/etc/hosts','/etc/passwd','/etc/default/odroid-fan','/usr/share/odroid-u3/fan-layout.json','/usr/lib/modules']:
    attrs=subprocess.run(['debugfs','-R','ea_list '+path,str(root)],check=True,capture_output=True,text=True).stdout
    assert 'system.posix_acl' not in attrs,path
sudo_path='/usr/bin/sudo'
for _ in range(12):
    info=subprocess.run(['debugfs','-R','stat '+sudo_path,str(root)],check=True,capture_output=True,text=True).stdout
    if 'Type: symlink' not in info:break
    target=re.search(r'Fast link dest: "([^"]+)"',info).group(1)
    import posixpath
    sudo_path=posixpath.normpath(target if target.startswith('/') else posixpath.join(posixpath.dirname(sudo_path),target))
else:raise AssertionError('sudo symlink loop in image')
assert 'Type: regular' in info
assert int(re.search(r'Mode:\s+([0-7]+)',info).group(1),8)==0o4755
assert int(re.search(r'User:\s+(\d+)',info).group(1))==0
groups=read('/etc/group').decode().splitlines()
for group in ['sudo','video','render']:
    assert 'odroid' in next(x for x in groups if x.startswith(group+':')).split(':')[3].split(',')
version=manifest['kernel'];assert '-test' not in version
assert f'CONFIG_LOCALVERSION="-{version.split("-",1)[1]}"' in read('/boot/config-'+version).decode()
assert read('/usr/lib/modules/'+version+'/modules.dep')
boot=out/'stage/boot'
assert (boot/('vmlinuz-'+version)).is_file() and (boot/('uImage-'+version)).is_file()
assert (boot/('exynos4412-odroidu3-'+version+'.dtb')).is_file()
boot_text=(boot/'extlinux/extlinux.conf').read_text()
assert 'LINUX /vmlinuz-'+version in boot_text and 'audit=1 audit_backlog_limit=8192 psi=1' in boot_text
payload=json.loads(read('/usr/lib/odroid-u3/kernels/'+version+'/MANIFEST.json'))
assert hashlib.sha256((boot/('uImage-'+version)).read_bytes()).hexdigest()==payload['files']['uImage']
assert (boot/'uImage').read_bytes()==(boot/('uImage-'+version)).read_bytes()
assert 'apparmor.service' in listing('/etc/systemd/system/sysinit.target.wants')+listing('/etc/systemd/system/multi-user.target.wants')
assert 'auditd.service' in listing('/etc/systemd/system/multi-user.target.wants')
checks['flat_versioned_boot_and_security_services']=True
image_release=read('/etc/odroid-image-release').decode();assert 'ROOT_UUID='+manifest['root_uuid'] in image_release
assert 'IMAGE_VARIANT='+manifest['variant'] in image_release
assert 'KERNEL='+version in image_release
network=read('/etc/netplan/10-ethernet.yaml').decode();assert network.count('use-hostname: false')==2 and 'dhcp-identifier: mac' in network
layout=json.loads(read('/usr/share/odroid-u3/fan-layout.json'));assert layout['fan_trip_ids']==[4,5,6] and layout['cpu_protection_trip_ids']==[0,1,2,3]
assert layout['default_temperatures_celsius']==[35,45,55] and layout['kernel_release']==version
for name in ['odroid-fan','odroid-network-identity','odroid-grow-root']:assert read('/usr/local/sbin/'+name).startswith(b'#!')
assert read('/usr/local/bin/odroid-gpu').startswith(b'#!')
assert 'https://the-ab.github.io/deb/' in read('/etc/apt/sources.list.d/the-ab-odroid-u3.sources').decode()
assert read('/usr/share/keyrings/the-ab-archive-keyring.gpg')
assert read('/usr/sbin/odroid-kernel').startswith(b'#!')
checks['local_kernel_packages_and_signed_apt_source']=True
checks.update(only_odroid_human_account=True,root_password_locked_and_key_only_ssh=True,no_authorized_or_host_keys=True,no_host_workspace_acls=True,unique_machine_identity_on_boot=True,odroid_sudo_and_graphics_groups=True,sudo_executable_setuid_root_in_image=True,kernel_and_modules_version_match=True,board_support=True,arm_pam_and_full_boot_qa=True)
with image.open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==manifest['image_sha256']
result={'local_image_checks_passed':True,'image_sha256':manifest['image_sha256'],'checks':checks,'physical_boot_acceptance':False,'public_binary_distribution_clearance':False}
(out/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
