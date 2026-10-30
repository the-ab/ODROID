#!/usr/bin/python3
# SPDX-License-Identifier: GPL-2.0-only
"""Remove generated files of an uninstalled, inactive U3 kernel conservatively."""
from pathlib import Path
import hashlib,json,os,re,subprocess,sys,tempfile
PACKAGE_SPEC = None  # populated by build-kernel-debs.py
GENERATED = {'modules.alias','modules.alias.bin','modules.dep','modules.dep.bin','modules.devname','modules.softdep','modules.weakdep','modules.symbols','modules.symbols.bin','modules.builtin.alias.bin','modules.builtin.bin'}
BOOT_NAMES={'zImage':'vmlinuz-{release}','uImage':'uImage-{release}','exynos4412-odroidu3.dtb':'exynos4412-odroidu3-{release}.dtb','config':'config-{release}','System.map':'System.map-{release}'}
def need(ok,message):
    if not ok:raise RuntimeError(message)
def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def safe_file(path,base):
    return path.is_file() and not any(p.is_symlink() for p in [path,*path.parents] if p==base or base in p.parents)
def prune_menu(text,kernels):
    head=[];blocks=[];current=None;default=None
    for line in text.splitlines():
        f=line.strip().split(None,1)
        if f and f[0].upper()=='DEFAULT':default=f[1] if len(f)>1 else None
        if f and f[0].upper()=='LABEL':current=[f[1],[line]];blocks.append(current)
        elif current:current[1].append(line)
        else:head.append(line)
    removed=[];kept=[]
    if default is None and blocks:default=blocks[0][0]
    for label,lines in blocks:
        old=any(len(f:=line.strip().split(None,1))==2 and f[0].upper() in ('LINUX','KERNEL') and f[1] in kernels for line in lines)
        if old:
            need(label!=default,'Refusing to remove the selected extlinux entry');removed.append(label)
        else:kept+=lines
    return '\n'.join([*head,*kept])+'\n',removed

def cleanup(root,release,hashes,running):
    need(re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+-odroidu3-v[0-9]+',release),'Invalid kernel release')
    state=root/'var/lib/odroid-kernel/state.json';s=json.loads(state.read_text()) if state.exists() else {}
    need(release not in {running,s.get('active_release'),s.get('previous_running')},'Running, selected or rollback kernel is protected')
    need(not (root/'usr/lib/odroid-u3/kernels'/release).exists(),'Kernel payload still installed; use apt purge first')
    modules=root/'usr/lib/modules'/release
    if modules.exists() or modules.is_symlink():need(modules.is_dir() and not modules.is_symlink() and not modules.parent.is_symlink(),'Unsafe module directory')
    boot=root/'boot';need(not boot.is_symlink(),'Unsafe boot path')
    candidates={BOOT_NAMES[n].format(release=release):h for n,h in hashes.items() if n in BOOT_NAMES}
    candidates.update({'odroid-kernels/'+release+'/'+n:h for n,h in hashes.items() if n in BOOT_NAMES})
    # Early images used these unversioned aliases; active shared uImage is never removed.
    candidates.update({n:hashes[n] for n in ['zImage','exynos4412-odroidu3.dtb'] if n in hashes})
    matched={name for name,h in candidates.items() if safe_file(boot/name,boot) and sha(boot/name)==h}
    kernels={'/'+n for n in matched if n in ['zImage','vmlinuz-'+release,'odroid-kernels/'+release+'/zImage']}
    conf=boot/'extlinux/extlinux.conf';removed_entries=[];references=set()
    if conf.exists():
        need(safe_file(conf,boot),'Unsafe extlinux path');before=conf.read_text();after,removed_entries=prune_menu(before,kernels)
        if removed_entries:
            backups=root/'var/lib/odroid-kernel/removed';need(not backups.is_symlink(),'Unsafe cleanup backup path');backups.mkdir(parents=True,exist_ok=True);backups.chmod(0o700)
            fd,name=tempfile.mkstemp(prefix=release+'-',suffix='.extlinux.conf',dir=backups)
            with os.fdopen(fd,'w') as f:f.write(before);f.flush();os.fsync(f.fileno())
            fd,name=tempfile.mkstemp(prefix='.cleanup-',dir=conf.parent)
            try:
                with os.fdopen(fd,'w') as f:f.write(after);f.flush();os.fsync(f.fileno())
                os.chmod(name,0o644);os.replace(name,conf)
            finally:
                if os.path.exists(name):os.unlink(name)
        for line in after.splitlines():
            f=line.strip().split(None,1)
            if len(f)==2 and f[0].upper() in ('LINUX','KERNEL','FDT','INITRD'):references.update(f[1].split())
    removed=[];kept=[name for name in candidates if name not in matched and ((boot/name).exists() or (boot/name).is_symlink())]
    for name in sorted(matched):
        if '/'+name in references:kept.append(name);continue
        (boot/name).unlink();removed.append('boot/'+name)
    modules=root/'usr/lib/modules'/release
    if modules.exists():
        need(modules.is_dir() and not modules.is_symlink() and not modules.parent.is_symlink(),'Unsafe module directory')
        for p in modules.iterdir():
            if p.name in GENERATED and p.is_file() and not p.is_symlink():p.unlink();removed.append('usr/lib/modules/'+release+'/'+p.name)
        try:modules.rmdir()
        except OSError:kept.append(str(modules.relative_to(root)))
    legacy=boot/'odroid-kernels'/release
    if legacy.exists() and not legacy.is_symlink():
        try:legacy.rmdir()
        except OSError:kept.append(str(legacy.relative_to(root)))
    return {'release':release,'removed':removed,'removed_inactive_menu_entries':removed_entries,'preserved_modified_referenced_or_unknown_files':kept,'shared_uImage_and_boot0_untouched':True}

def main():
    if len(sys.argv)<2 or sys.argv[1] not in ('remove','purge') or os.environ.get('ODROID_IMAGE_BUILD')=='1':return
    need(PACKAGE_SPEC is not None,'Missing package cleanup specification')
    # Only inspect the boot partition when the supported board and matching mount are present.
    compatible=Path('/sys/firmware/devicetree/base/compatible')
    need(compatible.exists() and b'hardkernel,odroid-u3' in compatible.read_bytes().split(b'\0'),'Only ODROID-U3 is supported')
    device=Path('/sys/dev/block/%s:%s'%(os.major(os.stat('/').st_dev),os.minor(os.stat('/').st_dev))).resolve();need(re.fullmatch('mmcblk[0-9]+p2',device.name),'Unexpected root medium')
    mounted=subprocess.check_output(['findmnt','-n','-o','SOURCE,FSTYPE','/boot'],text=True).split();need(len(mounted)==2 and Path(mounted[0]).resolve()==Path('/dev')/(device.parent.name+'p1') and mounted[1]=='vfat','Mount the matching boot partition before purging kernel files')
    print(json.dumps(cleanup(Path('/'),PACKAGE_SPEC['release'],PACKAGE_SPEC['files'],os.uname().release),indent=2))
if __name__=='__main__':main()
