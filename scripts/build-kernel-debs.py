#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Build locally installable U3 kernel, update-tool, meta and archive-keyring packages."""
from pathlib import Path
import argparse,hashlib,json,os,re,shutil,struct,subprocess,time,zlib
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--kernel',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--keyring',type=Path,required=True);p.add_argument('--profile',type=Path,help='Explicit pinned candidate source/config/patch profile');p.add_argument('--release',help='Explicit candidate release override; board/image default is unchanged');p.add_argument('--version',help='Debian version; defaults to upstream version plus numeric board revision');a=p.parse_args();repo=Path(__file__).resolve().parents[1];board=json.loads((repo/'boards/u3/board.json').read_text());kernel=a.kernel.resolve();out=a.output.resolve();assert not out.exists();out.mkdir(parents=True);release=(kernel/'kernel.release').read_text().strip();assert release==(a.release or board['kernel_release']) and re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+-odroidu3-v[0-9]+',release);a.version=a.version or release.split('-odroidu3-v')[0]+'-'+release.split('-odroidu3-v')[1];assert re.fullmatch('[0-9A-Za-z.+:~_-]+',a.version)
assert not subprocess.check_output(['git','-c','safe.directory='+str(repo),'-C',str(repo),'status','--porcelain'],text=True).strip(),'Commit the packaging recipe before building'
profile=a.profile.resolve() if a.profile else None
source_spec=json.loads((profile/'source.json').read_text()) if profile else next(x for x in json.loads((repo/'sources.lock.json').read_text())['sources'] if x['id']=='kernel')
if profile:assert release==source_spec['kernel_release']
source_commit=subprocess.check_output(['git','-c','safe.directory='+str(repo),'-C',str(repo),'rev-parse','HEAD'],text=True).strip();tools_version=board['image_version'];epoch=int(os.environ.get('SOURCE_DATE_EPOCH',str(int(time.time()))));results=[]
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def put(root,name,data,mode=0o644):
 f=root/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data.encode() if isinstance(data,str) else data);f.chmod(mode);return f
def package(name,version,arch,depends,description):
 root=out/('stage-'+name);root.mkdir();(root/'DEBIAN').mkdir();control=f'Package: {name}\nVersion: {version}\nArchitecture: {arch}\nMaintainer: the-ab <the-ab@users.noreply.github.com>\nSection: kernel\nPriority: optional\nHomepage: https://github.com/the-ab/ODROID\n'
 if depends:control+='Depends: '+depends+'\n'
 put(root,'DEBIAN/control',control+'Description: '+description+'\n');put(root,'usr/share/doc/'+name+'/copyright','ODROID project scripts: GPL-2.0-only. Linux has its upstream licenses.\nMatching source and configuration are provided alongside kernel releases.\nSee /usr/share/common-licenses/GPL-2 and https://github.com/the-ab/ODROID\n');return root
keyname='the-ab-archive-keyring';key=package(keyname,'2026.10.30','all','','Public archive key for the-ab packages');put(key,'usr/share/keyrings/the-ab-archive-keyring.gpg',a.keyring.read_bytes())
toolname='odroid-u3-kernel-tools';tools=package(toolname,tools_version,'all','python3, kmod, util-linux, the-ab-archive-keyring','Kernel activation and recovery tools for ODROID-U3');put(tools,'usr/sbin/odroid-kernel',(repo/'boards/u3/support/odroid-kernel').read_bytes(),0o755)
put(tools,'etc/apt/sources.list.d/the-ab-odroid-u3.sources','Types: deb\nURIs: https://the-ab.github.io/deb/\nSuites: stable\nComponents: main u3\nArchitectures: armhf\nSigned-By: /usr/share/keyrings/the-ab-archive-keyring.gpg\n')
put(tools,'etc/apt/apt.conf.d/50-odroid-u3-kernels','// Keep versioned board kernels until the owner explicitly removes them.\nAPT::NeverAutoRemove { "^linux-image-[0-9].*-odroidu3-v[0-9]+$"; };\n');put(tools,'DEBIAN/conffiles','/etc/apt/sources.list.d/the-ab-odroid-u3.sources\n/etc/apt/apt.conf.d/50-odroid-u3-kernels\n')
name='linux-image-'+release;image=package(name,a.version,'armhf','odroid-u3-kernel-tools (>= '+tools_version+'), kmod','Linux '+release+' for ODROID-U3')
modules=image/'usr/lib/modules'/release;modules.parent.mkdir(parents=True,exist_ok=True)
generated={'modules.alias','modules.alias.bin','modules.dep','modules.dep.bin','modules.devname','modules.softdep','modules.symbols','modules.symbols.bin','modules.builtin.alias.bin','modules.builtin.bin'}
shutil.copytree(kernel/'usr/lib/modules'/release,modules,symlinks=True,ignore=shutil.ignore_patterns(*generated,'build','source'))
base='usr/lib/odroid-u3/kernels/'+release
for src,target in [('zImage','zImage'),('exynos4412-odroidu3.dtb','exynos4412-odroidu3.dtb'),('config','config'),('System.map','System.map')]:put(image,base+'/'+target,(kernel/src).read_bytes())
data=(kernel/'zImage').read_bytes()+(kernel/'exynos4412-odroidu3.dtb').read_bytes();header=bytearray(struct.pack('>7I4B32s',0x27051956,0,0,len(data),0x40008000,0x40008000,zlib.crc32(data),5,2,2,0,('U3 '+release).encode()[:32]));struct.pack_into('>I',header,4,zlib.crc32(header));put(image,base+'/uImage',bytes(header)+data)
lock=json.loads((repo/'sources.lock.json').read_text());manifest={'schema':1,'board':'ODROID-U3','architecture':'armhf','kernel_release':release,'deb_version':a.version,'candidate_release_override':release!=board['kernel_release'],'packaging_source_commit':source_commit,'upstream_linux':source_spec,'kernel_config_sha256':sha(kernel/'config'),'kernel_patch_sha256':sha(profile/'platform.patch' if profile else repo/'boards/u3/patches/platform.patch'),'files':{n:sha(image/base/n) for n in ['zImage','exynos4412-odroidu3.dtb','uImage','config','System.map']},'modules':{str(f.relative_to(modules)):sha(f) for f in sorted(modules.rglob('*.ko'))},'boot0_update':False};put(image,base+'/MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
put(image,'DEBIAN/postinst',f'''#!/bin/sh
set -eu
if [ "$1" = configure ]; then
    depmod -a {release}
    if [ "${{ODROID_IMAGE_BUILD:-0}}" != 1 ]; then
        /usr/sbin/odroid-kernel activate {release}
    fi
fi
''',0o755)
put(image,'DEBIAN/prerm',f'''#!/bin/sh
set -eu
if [ "$1" = remove ] && [ "${{ODROID_IMAGE_BUILD:-0}}" != 1 ]; then
    python3 - {release} <<'CHECK'
import json,os,sys
from pathlib import Path
state=Path('/var/lib/odroid-kernel/state.json')
s=json.loads(state.read_text()) if state.exists() else {{}}
protected={{os.uname().release,s.get('active_release'),s.get('previous_running')}}
if sys.argv[1] in protected:
    raise SystemExit('Refusing to remove a running, next-boot or rollback kernel')
CHECK
fi
''',0o755)
meta=package('linux-image-odroid-u3',a.version,'armhf',name+' (= '+a.version+')','Latest released board kernel for ODROID-U3')
for root in [key,tools,image,meta]:
 for d in [root,*[x for x in root.rglob('*') if x.is_dir()]]:d.chmod(0o755)
 subprocess.run(['setfacl','-R','-b','-k',str(root)],check=True)
 sums=''.join(hashlib.md5(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(root))+'\n' for f in sorted(root.rglob('*')) if f.is_file() and 'DEBIAN' not in f.relative_to(root).parts);put(root,'DEBIAN/md5sums',sums)
 control=dict(l.split(': ',1) for l in (root/'DEBIAN/control').read_text().splitlines() if ': ' in l);filename=control['Package']+'_'+control['Version']+'_'+control['Architecture']+'.deb';target=out/filename
 subprocess.run(['dpkg-deb','--root-owner-group','-Zxz','--build',str(root),str(target)],check=True,env={**os.environ,'SOURCE_DATE_EPOCH':str(epoch)})
 results.append({'package':control['Package'],'version':control['Version'],'architecture':control['Architecture'],'file':filename,'bytes':target.stat().st_size,'sha256':sha(target)})
(out/'PACKAGES.json').write_text(json.dumps({'packaging_source_commit':source_commit,'kernel_release':release,'packages':results,'public_kernel_release':False},indent=2)+'\n');print(json.dumps(results,indent=2))
