#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Build signed static APT indices, preserving existing package components and by-hash indices."""
from pathlib import Path
import argparse,datetime,hashlib,json,lzma,os,re,subprocess,tempfile
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True);p.add_argument('--gpg-home',type=Path,required=True);p.add_argument('--signing-key',required=True);a=p.parse_args()
root=a.root.resolve();assert not a.gpg_home.resolve().is_relative_to(root),'Private key directory must be outside the public repository'
config=json.loads((root/'repository.json').read_text());suite=config['suite'];assert re.fullmatch('[a-z0-9-]+',suite)
dist=root/'dists'/suite;dist.mkdir(parents=True,exist_ok=True)
def digest(data,name='sha256'):return hashlib.new(name,data).hexdigest()
for component,architectures in config['components'].items():
 assert re.fullmatch('[a-z0-9-]+',component)
 pool=root/'pool'/component;pool.mkdir(parents=True,exist_ok=True);packages=[]
 for deb in sorted(pool.rglob('*.deb')):
  assert deb.stat().st_size<95*1024*1024,'Package exceeds the chosen static hosting file limit'
  meta=subprocess.check_output(['dpkg-deb','-f',str(deb)],text=True);fields=dict(line.split(': ',1) for line in meta.splitlines() if ': ' in line and not line.startswith(' '));data=deb.read_bytes();packages.append((fields['Architecture'],meta.rstrip()+'\nFilename: '+str(deb.relative_to(root))+'\nSize: '+str(len(data))+'\nSHA256: '+digest(data)+'\nSHA512: '+digest(data,'sha512')+'\n'))
 for arch in architectures:
  assert re.fullmatch('[a-z0-9-]+',arch)
  target=dist/component/('binary-'+arch);target.mkdir(parents=True,exist_ok=True);content=('\n'.join(meta for architecture,meta in packages if architecture in (arch,'all'))+'\n').encode() if packages else b''
  for name,data in [('Packages',content),('Packages.xz',lzma.compress(content))]:
   (target/name).write_bytes(data);
   for algorithm in ['sha256','sha512']:
    byhash=target/'by-hash'/algorithm.upper();byhash.mkdir(parents=True,exist_ok=True);(byhash/digest(data,algorithm)).write_bytes(data)
indices=sorted(p for p in dist.glob('*/binary-*/Packages*') if p.is_file())
architectures=sorted(set(arch for values in config['components'].values() for arch in values));now=datetime.datetime.now(datetime.timezone.utc)
release='Origin: the-ab\nLabel: the-ab packages\nSuite: '+suite+'\nCodename: '+suite+'\nDate: '+now.strftime('%a, %d %b %Y %H:%M:%S +0000')+'\nArchitectures: '+' '.join(architectures)+'\nComponents: '+' '.join(config['components'])+'\nAcquire-By-Hash: yes\nDescription: Signed packages maintained by the-ab\n'
for field,algorithm in [('SHA256','sha256'),('SHA512','sha512')]:
 release+=field+':\n'
 for path in indices:
  data=path.read_bytes();release+=' '+digest(data,algorithm)+' '+str(len(data))+' '+str(path.relative_to(dist))+'\n'
(dist/'Release').write_text(release)
base=['gpg','--homedir',str(a.gpg_home),'--batch','--yes','--pinentry-mode','loopback','--passphrase','','--local-user',a.signing_key,'--digest-algo','SHA256']
subprocess.run(base+['--clearsign','--output',str(dist/'InRelease'),str(dist/'Release')],check=True)
subprocess.run(base+['--armor','--detach-sign','--output',str(dist/'Release.gpg'),str(dist/'Release')],check=True)
subprocess.run(['gpgv','--keyring',str(root/'the-ab-archive-keyring.gpg'),str(dist/'InRelease')],check=True,capture_output=True)
print(json.dumps({'suite':suite,'components':config['components'],'public_fingerprint':a.signing_key,'signed_indices_valid':True,'packages':sum(1 for _ in (root/'pool').rglob('*.deb'))},indent=2))
