#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Assemble regular image files only; never open a block device for writing."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,stat,struct,subprocess,uuid,zipfile
if not __debug__:raise SystemExit('Run without Python optimization: validation must remain enabled')

p=argparse.ArgumentParser(description=__doc__)
for arg in ['root','kernel','uboot','firmware','output']:p.add_argument('--'+arg,type=Path,required=True)
p.add_argument('--variant',choices=['minimized','minimal'],required=True)
a=p.parse_args();repo=Path(__file__).resolve().parent.parent
board=json.loads((repo/'boards/u3/board.json').read_text());lock=json.loads((repo/'sources.lock.json').read_text())
root=a.root.resolve();kernel=a.kernel.resolve();out=a.output.resolve()
assert not subprocess.check_output(['git','-c','safe.directory='+str(repo),'-C',str(repo),'status','--porcelain'],text=True).strip(),'Commit image recipes before assembly'
recipe_commit=subprocess.check_output(['git','-c','safe.directory='+str(repo),'-C',str(repo),'rev-parse','HEAD'],text=True).strip()
assert os.geteuid()==0 and root.name=='rootfs-'+a.variant and (root.parent/'.odroid-workspace').is_file()
subprocess.run(['python3',str(repo/'scripts/normalize-rootfs.py'),'--root',str(root)],check=True)
assert not out.exists();out.mkdir(parents=True);stage=out/'stage';stage.mkdir();boot=stage/'boot';boot.mkdir();(boot/'extlinux').mkdir()
release=board['kernel_release'];assert (kernel/'kernel.release').read_text().strip()==release
package_manifest=json.loads((root/'usr/lib/odroid-u3/kernels'/release/'MANIFEST.json').read_text())
for name in ['zImage','exynos4412-odroidu3.dtb','config','System.map']:
    assert hashlib.sha256((kernel/name).read_bytes()).hexdigest()==package_manifest['files'][name]
assert not any(root.rglob('authorized_keys')) and not any((root/'etc/ssh').glob('ssh_host_*'))
assert (root/'etc/machine-id').read_bytes()==b''
assert not (root/'root/.ssh').exists() and not (root/'home/odroid/.ssh').exists()
image_id=f"odroid-u3-ubuntu-{board['ubuntu']}-armhf-{a.variant}-v{board['image_version']}"
disk_id=int(hashlib.sha256(image_id.encode()).hexdigest()[:8],16)
root_uuid=str(uuid.uuid5(uuid.NAMESPACE_URL,'https://github.com/the-ab/ODROID/'+image_id))
boot_start=32768;boot_sectors=524288;root_start=boot_start+boot_sectors;disk_sectors=4194304;root_sectors=disk_sectors-root_start
def run(*cmd):subprocess.run([str(x) for x in cmd],check=True)
def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def newfile(path,size):
    with path.open('xb') as f:f.truncate(size)
    assert stat.S_ISREG(path.stat().st_mode)
def sparse_copy(src,stream,offset):
    stream.seek(offset)
    with src.open('rb') as f:
        while chunk:=f.read(1024*1024):
            if chunk.count(0)==len(chunk):stream.seek(len(chunk),1)
            else:stream.write(chunk)

os.chown(root,0,0);root.chmod(0o755)
shutil.copytree(kernel/'usr/lib/modules',root/'usr/lib/modules',dirs_exist_ok=True)
for path in (root/'usr/lib/modules').rglob('*'):
    if not path.is_symlink():
        os.chown(path,0,0);path.chmod(0o755 if path.is_dir() else 0o644)
os.chown(root/'usr/lib/modules',0,0);(root/'usr/lib/modules').chmod(0o755)
run('depmod','-b',root,release)
for name,target in [('zImage','vmlinuz-'+release),('exynos4412-odroidu3.dtb','exynos4412-odroidu3-'+release+'.dtb')]:
    shutil.copy2(kernel/name,boot/target)
for name in ['config','System.map']:
    shutil.copy2(kernel/name,boot/(name+'-'+release))
shutil.copy2(kernel/'config',root/'boot'/('config-'+release))
(root/'boot'/('config-'+release)).chmod(0o644)
arguments=f'console=ttySAC1,115200n8 console=tty1 mem=2047M root=PARTUUID={disk_id:08x}-02 rootfstype=ext4 rootwait ro net.ifnames=0 fsck.repair=yes loglevel=4 audit=1 audit_backlog_limit=8192 psi=1'
(boot/'extlinux/extlinux.conf').write_text(f'TIMEOUT 30\nDEFAULT ubuntu26\nMENU TITLE ODROID-U3 Ubuntu {board["ubuntu"]}\n\nLABEL ubuntu26\n  MENU LABEL Ubuntu {board["ubuntu"]} / {release}\n  LINUX /vmlinuz-{release}\n  FDT /exynos4412-odroidu3-{release}.dtb\n  APPEND {arguments}\n')
appended=stage/'zImage-appended-dtb';appended.write_bytes((boot/('vmlinuz-'+release)).read_bytes()+(boot/('exynos4412-odroidu3-'+release+'.dtb')).read_bytes())
shutil.copy2(root/'usr/lib/odroid-u3/kernels'/release/'uImage',boot/'uImage')
shutil.copy2(boot/'uImage',boot/('uImage-'+release))
assert sha(boot/'uImage')==package_manifest['files']['uImage']
(boot/'boot.txt').write_text('setenv initrd_high 0xffffffff\nsetenv fdt_high 0xffffffff\nsetenv bootdev 0\nif test -n "${devnum}"; then setenv bootdev ${devnum}; fi\n'+f'setenv bootargs "{arguments}"\n'+'setenv bootcmd "fatload mmc ${bootdev}:1 0x40008000 uImage; bootm 0x40008000"\nboot\n')
run('mkimage','-A','arm','-O','linux','-T','script','-C','none','-a','0','-e','0','-n','ODROID-U3 boot','-d',boot/'boot.txt',boot/'boot.scr')
(root/'etc/fstab').write_text(f'UUID={root_uuid} / ext4 defaults,noatime,errors=remount-ro 0 1\nPARTUUID={disk_id:08x}-01 /boot vfat defaults,noatime,umask=0077 0 2\n')
(root/'etc/fstab').chmod(0o644)
(root/'etc/odroid-image-release').write_text(f'IMAGE_ID={image_id}\nIMAGE_VERSION={board["image_version"]}\nIMAGE_VARIANT={a.variant}\nKERNEL={release}\nTARGET=ODROID-U3-armhf\nROOT_UUID={root_uuid}\nSTATUS=release-candidate-hardware-acceptance-pending\n')
(root/'etc/odroid-image-release').chmod(0o644)
firmware=a.firmware.resolve()
mfc=firmware/'s5p-mfc.fw';assert sha(mfc)==next(x['sha256'] for x in lock['sources'] if x['id']=='samsung-mfc')
(root/'usr/lib/firmware').mkdir(parents=True,exist_ok=True);shutil.copy2(mfc,root/'usr/lib/firmware/s5p-mfc.fw')
(root/'usr/lib/firmware/s5p-mfc.fw').chmod(0o644)
docs=root/'usr/share/doc/odroid-u3-firmware';docs.mkdir(parents=True,exist_ok=True);shutil.copy2(firmware/'LICENSE.s5p-mfc',docs/'LICENSE.s5p-mfc')
(docs/'LICENSE.s5p-mfc').chmod(0o644)
subprocess.run(['setfacl','-R','-b','-k',str(root)],check=True)
boot_fs=stage/'boot-partition.img';root_fs=stage/'root-partition.img'
newfile(boot_fs,boot_sectors*512);newfile(root_fs,root_sectors*512)
run('mkfs.vfat','-F','16','-n','BOOT','-i',f'{disk_id:08X}',boot_fs)
run('mcopy','-i',boot_fs,'-s',*sorted(boot.iterdir()),'::')
run('mkfs.ext4','-F','-L','rootfs','-U',root_uuid,'-m','1','-O','^64bit,^metadata_csum','-E','lazy_itable_init=0,lazy_journal_init=0','-d',root,root_fs)
run('fsck.vfat','-n',boot_fs);run('e2fsck','-fn',root_fs)
head=bytearray(boot_start*512);prefix=bytearray(1240064);components=[]
for spec in lock['boot_reference']['component_layout']:
    item=dict(spec);size=item['sectors']*512
    if item['name']=='u-boot':
        binary=a.uboot.read_bytes();assert len(binary)<=size;blob=binary.ljust(size,b'\0')
        item['source']='U-Boot v2026.10 / odroid_defconfig';item['sha256']=hashlib.sha256(blob).hexdigest()
        item['binary_bytes']=len(binary)
    else:
        blob=(firmware/(item['name']+'.bin')).read_bytes();assert len(blob)==size and hashlib.sha256(blob).hexdigest()==item['sha256']
    item['nonzero_bytes']=len(blob)-blob.count(0)
    start=item['sd_sector']*512;head[start:start+size]=blob
    start=item['emmc_boot0_sector']*512;prefix[start:start+size]=blob;components.append(item)
struct.pack_into('<I',head,440,disk_id)
for i,(status,kind,start,count) in enumerate([(0x80,6,boot_start,boot_sectors),(0,0x83,root_start,root_sectors)]):
    head[446+i*16:462+i*16]=struct.pack('<B3sB3sII',status,b'\xfe\xff\xff',kind,b'\xfe\xff\xff',start,count)
head[510:512]=b'\x55\xaa'
image=out/(image_id+'.img');newfile(image,disk_sectors*512)
with image.open('r+b') as f:
    f.write(head);sparse_copy(boot_fs,f,boot_start*512);sparse_copy(root_fs,f,root_start*512)
payload=out/'u3-boot0-prefix.bin';payload.write_bytes(prefix)
manifest={'schema':1,'recipe_commit':recipe_commit,'kernel_packaging_commit':package_manifest['packaging_source_commit'],'image':image.name,'image_sha256':sha(image),'image_bytes':image.stat().st_size,'ubuntu':board['ubuntu'],'variant':a.variant,'image_version':board['image_version'],'kernel':release,'disk_id':f'{disk_id:08x}','root_uuid':root_uuid,'built_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'partitions':[{'number':1,'start_sector':boot_start,'sectors':boot_sectors,'filesystem':'FAT16'},{'number':2,'start_sector':root_start,'sectors':root_sectors,'filesystem':'ext4'}],'firmware_components':components,'emmc_boot0_payload':{'file':payload.name,'bytes':len(prefix),'sha256':sha(payload),'separate_hardware_boot_partition':True},'access':{'human_users':['odroid'],'default_password':'odroid','sudo':'password required','root_password':'locked','root_ssh':True,'root_ssh_authentication':'public key only','root_password_ssh':False,'authorized_keys_included':False,'ssh_host_keys':'generated on first boot'},'hardware_acceptance':'this new image not yet physically boot-tested','boot_firmware_distribution':lock['boot_reference']['distribution_status']}
(out/'BUILD-MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
shutil.copy2(root.parent/('packages-'+a.variant+'.tsv'),out/'PACKAGES.tsv')
(out/(image.name+'.sha256')).write_text(manifest['image_sha256']+'  '+image.name+'\n')
print(json.dumps(manifest,indent=2))
