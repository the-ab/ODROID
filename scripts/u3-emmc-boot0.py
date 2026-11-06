#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Inspect, back up and explicitly update an ODROID-U3 eMMC boot0 partition.

Inspect is read-only. Firmware writes require booting the same eMMC through the
U3's SD-slot adapter, a complete verified backup, a payload checksum and its CID.
No boot configuration, boot1, user-area filesystem or eFuse is ever written.
"""
from pathlib import Path
import argparse,ctypes,datetime,fcntl,hashlib,json,os,re,signal,stat,struct

PREFIX_BYTES=1240064
def sha(data):return hashlib.sha256(data).hexdigest()
def require(condition,message):
    if not condition:raise RuntimeError(message)
def read_exact(fd,size,offset=0):
    parts=[]
    while size:
        data=os.pread(fd,min(size,1024*1024),offset)
        require(bool(data),'Unexpected end of device')
        parts.append(data);offset+=len(data);size-=len(data)
    return b''.join(parts)
def read_device(path,size):
    fd=os.open(path,os.O_RDONLY)
    try:
        require(stat.S_ISBLK(os.fstat(fd).st_mode),'Not a block device')
        return read_exact(fd,size)
    finally:os.close(fd)
def ext_csd(path):
    data=ctypes.create_string_buffer(512)
    cmd=bytearray(struct.pack('=16IQ',0,0,8,0,0,0,0,0,0xB5,512,1,0,0,0,0,0,ctypes.addressof(data)))
    fd=os.open(path,os.O_RDONLY)
    try:fcntl.ioctl(fd,0xC048B300,cmd,True)
    finally:os.close(fd)
    return data.raw
def inspect(device):
    require(os.geteuid()==0,'Run with sudo')
    compatible=Path('/sys/firmware/devicetree/base/compatible').read_bytes().split(b'\0')
    require(b'hardkernel,odroid-u3' in compatible,'Only ODROID-U3 is supported; never use on XU4')
    require(Path('/sys/devices/soc0/soc_id').read_text().strip()=='EXYNOS4412','Wrong SoC')
    require(not device.is_symlink() and re.fullmatch(r'mmcblk\d+',device.name),'Use the complete /dev/mmcblkN device')
    require(device.parent==Path('/dev') and stat.S_ISBLK(device.stat().st_mode),'Not a native MMC block device')
    sys=Path('/sys/class/block')/device.name
    require((sys/'device/type').read_text().strip()=='MMC','Selected card is not eMMC')
    cid=(sys/'device/cid').read_text().strip().lower();require(bool(re.fullmatch('[0-9a-f]{32}',cid)),'Invalid card CID')
    size=int((Path(str(sys)+'boot0')/'size').read_text())*512
    require(PREFIX_BYTES<=size<=16*1024*1024,'Unsupported hardware boot partition size')
    require(int((Path(str(sys)+'boot1')/'size').read_text())*512==size,'Boot partition sizes differ')
    ext=ext_csd(device)
    dev=os.stat('/').st_dev;root_sys=Path(f'/sys/dev/block/{os.major(dev)}:{os.minor(dev)}').resolve()
    root_on_card=root_sys.parent.name==device.name and root_sys.name==device.name+'p2'
    controller=str((sys/'device').resolve())
    return {'board':'ODROID-U3','device':str(device),'cid':cid,'name':(sys/'device/name').read_text().strip(),'boot_bytes':size,'controller':controller,'root_on_selected_card':root_on_card,'sd_adapter_path':'/12530000.mmc/' in controller,'partition_config':ext[179],'boot_bus_width':ext[177],'boot_write_protect':ext[173],'force_ro':(Path(str(sys)+'boot0')/'force_ro').read_text().strip(),'ext_csd':ext}
def write_guard(info,cid):
    require(cid==info['cid'],'CID confirmation differs from the selected card')
    require(info['sd_adapter_path'] and info['root_on_selected_card'],'For writes, boot THIS eMMC through the U3 SD-slot adapter')
    require(info['partition_config']&0xF8==0x48,'Boot selection differs from the tested boot0 + ACK configuration; inspect separately')
    require(info['boot_bus_width']==1 and info['boot_write_protect']==0,'Boot bus or write protection differs; inspect separately')
    require(info['force_ro']=='1','Expected boot0 force_ro=1 before the transaction')
def save(path,data,owner):
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    try:
        with os.fdopen(fd,'wb',closefd=False) as f:f.write(data);f.flush();os.fsync(f.fileno())
        os.fchown(fd,*owner)
    finally:os.close(fd)
    require(path.read_bytes()==data,'Backup readback differs')
def backup(info,directory):
    require(not directory.exists(),'Use a new backup directory')
    directory.mkdir(parents=True,mode=0o700)
    owner=(int(os.environ.get('SUDO_UID','0')),int(os.environ.get('SUDO_GID','0')));os.chown(directory,*owner)
    device=info['device'];data={'boot0.bin':read_device(device+'boot0',info['boot_bytes']),'boot1.bin':read_device(device+'boot1',info['boot_bytes']),'user-area-first-16MiB.bin':read_device(device,16*1024*1024),'ext-csd.bin':info['ext_csd']}
    for name,blob in data.items():save(directory/name,blob,owner)
    manifest={k:v for k,v in info.items() if k!='ext_csd'}
    manifest.update(created_at=datetime.datetime.now().astimezone().isoformat(),files={name:{'bytes':len(blob),'sha256':sha(blob)} for name,blob in data.items()})
    save(directory/'BACKUP.json',(json.dumps(manifest,indent=2)+'\n').encode(),owner)
    print(json.dumps({'backup':str(directory),'cid':info['cid'],'files':manifest['files'],'firmware_written':False},indent=2))
def load_backup(info,directory):
    require(directory.is_dir() and not directory.is_symlink(),'Invalid backup directory')
    m=json.loads((directory/'BACKUP.json').read_text());require(m['cid']==info['cid'] and m['boot_bytes']==info['boot_bytes'],'Backup belongs to a different module')
    data={}
    for name in ['boot0.bin','boot1.bin','user-area-first-16MiB.bin','ext-csd.bin']:
        p=directory/name;require(p.is_file() and not p.is_symlink(),'Invalid backup file: '+name)
        blob=p.read_bytes();require(len(blob)==m['files'][name]['bytes'] and sha(blob)==m['files'][name]['sha256'],'Corrupt backup: '+name);data[name]=blob
    require(len(data['boot0.bin'])==info['boot_bytes'],'Incomplete boot0 backup')
    require(read_device(info['device']+'boot1',info['boot_bytes'])==data['boot1.bin'],'boot1 has changed since backup')
    require(read_device(info['device'],16*1024*1024)==data['user-area-first-16MiB.bin'],'User-area boot prefix has changed since backup')
    ext=data['ext-csd.bin'];require(len(ext)==512 and (ext[179]&0xF8,ext[177],ext[173])==(info['partition_config']&0xF8,info['boot_bus_width'],info['boot_write_protect']),'Boot configuration differs from backup')
    return data
def write_all(fd,blob):
    offset=0
    while offset<len(blob):
        n=os.pwrite(fd,blob[offset:offset+65536],offset);require(n>0,'Short boot0 write');offset+=n
    os.fsync(fd)
def replace_prefix(fd,before,prefix,writer=write_all):
    """Keep the original tail; verify the complete partition, roll back on error."""
    require(len(prefix)==PREFIX_BYTES and len(before)>=PREFIX_BYTES,'Invalid prefix size')
    expected=prefix+before[PREFIX_BYTES:]
    try:
        writer(fd,prefix);require(read_exact(fd,len(before))==expected,'Full boot0 readback differs')
    except BaseException:
        write_all(fd,before[:PREFIX_BYTES]);require(read_exact(fd,len(before))==before,'Automatic rollback failed');raise
    return expected
def transaction(info,before,prefix,data):
    force=Path('/sys/class/block')/(Path(info['device']).name+'boot0')/'force_ro';fd=None
    # Defer ordinary termination until the short write/verify/relock completes.
    previous_mask=signal.pthread_sigmask(signal.SIG_BLOCK,{signal.SIGINT,signal.SIGTERM,signal.SIGHUP})
    try:
        force.write_text('0\n');require(force.read_text().strip()=='0','Cannot unlock boot0')
        fd=os.open(info['device']+'boot0',os.O_RDWR|os.O_EXCL)
        require(stat.S_ISBLK(os.fstat(fd).st_mode),'Not a block device')
        require(read_exact(fd,len(before))==before,'boot0 changed during preflight')
        expected=replace_prefix(fd,before,prefix)
    finally:
        try:
            if fd is not None:os.close(fd)
            force.write_text('1\n');require(force.read_text().strip()=='1','Cannot restore boot0 read-only protection')
        finally:signal.pthread_sigmask(signal.SIG_SETMASK,previous_mask)
    after=inspect(Path(info['device']))
    require(after['cid']==info['cid'],'Module identity changed')
    require((after['partition_config']&0xF8,after['boot_bus_width'],after['boot_write_protect'])==(info['partition_config']&0xF8,info['boot_bus_width'],info['boot_write_protect']),'Persistent boot configuration changed')
    require(read_device(info['device']+'boot0',info['boot_bytes'])==expected,'Final boot0 verification failed')
    require(read_device(info['device']+'boot1',info['boot_bytes'])==data['boot1.bin'],'boot1 changed')
    require(read_device(info['device'],16*1024*1024)==data['user-area-first-16MiB.bin'],'User-area boot prefix changed')
    return expected
def record(directory,kind,result):
    owner=(int(os.environ.get('SUDO_UID','0')),int(os.environ.get('SUDO_GID','0')))
    name=kind+'-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'.json';save(directory/name,(json.dumps(result,indent=2)+'\n').encode(),owner)
    print(json.dumps(result,indent=2))
def update(info,directory,payload,payload_hash,cid):
    write_guard(info,cid);data=load_backup(info,directory)
    require(bool(re.fullmatch('[0-9a-f]{64}',payload_hash or '')),'Provide the checksum from the verified release manifest')
    prefix=payload.read_bytes();require(len(prefix)==PREFIX_BYTES and sha(prefix)==payload_hash,'Wrong or corrupt boot0 payload')
    before=read_device(info['device']+'boot0',info['boot_bytes']);original=data['boot0.bin'];expected=prefix+original[PREFIX_BYTES:]
    if before==expected:
        print('Already at the requested boot0 state; no write');return
    require(before==original,'boot0 changed since backup; refusing an unknown firmware state')
    expected=transaction(info,before,prefix,data)
    result={'cid':cid,'prefix_bytes_written':PREFIX_BYTES,'before_sha256':sha(before),'after_sha256':sha(expected),'payload_sha256':payload_hash,'force_ro':'1','boot1_unchanged':True,'boot_configuration_unchanged':True,'reboot_performed':False}
    record(directory,'APPLY',result)
def restore(info,directory,cid,expected_current):
    write_guard(info,cid);data=load_backup(info,directory)
    before=read_device(info['device']+'boot0',info['boot_bytes']);original=data['boot0.bin']
    if before==original:print('Already at the saved original state; no write');return
    require(bool(re.fullmatch('[0-9a-f]{64}',expected_current or '')) and sha(before)==expected_current,'Current firmware differs from the confirmed update result')
    require(before[PREFIX_BYTES:]==original[PREFIX_BYTES:],'Tail differs from backup; refusing an unknown state')
    expected=transaction(info,before,original[:PREFIX_BYTES],data);require(expected==original,'Restore verification failed')
    record(directory,'RESTORE',{'cid':cid,'before_sha256':sha(before),'restored_sha256':sha(expected),'force_ro':'1','boot1_unchanged':True,'boot_configuration_unchanged':True,'reboot_performed':False})
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['inspect','backup','apply','restore']);p.add_argument('--device',type=Path,required=True);p.add_argument('--backup',type=Path);p.add_argument('--payload',type=Path);p.add_argument('--payload-sha256');p.add_argument('--confirm-cid');p.add_argument('--expect-current-sha256');a=p.parse_args()
    info=inspect(a.device)
    if a.action=='inspect':print(json.dumps({k:v for k,v in info.items() if k!='ext_csd'},indent=2))
    elif a.action=='backup':require(a.backup is not None,'--backup required');backup(info,a.backup)
    elif a.action=='restore':require(a.backup is not None,'--backup required');restore(info,a.backup,a.confirm_cid,a.expect_current_sha256)
    else:
        require(a.backup is not None and a.payload is not None,'--backup and --payload required')
        update(info,a.backup,a.payload,a.payload_sha256,a.confirm_cid)
if __name__=='__main__':
    try:main()
    except Exception as e:raise SystemExit('Refused/failed: '+str(e))
