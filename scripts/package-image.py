#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Package a locally validated candidate as ZIP and verify its complete image stream."""
from pathlib import Path
import argparse,hashlib,json,zipfile,subprocess
if not __debug__:raise SystemExit('Run without Python optimization: validation must remain enabled')

p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
out=a.output;repo=Path(__file__).resolve().parent.parent;m=json.loads((out/'BUILD-MANIFEST.json').read_text());v=json.loads((out/'VALIDATION.json').read_text())
assert v['local_image_checks_passed'] and v['image_sha256']==m['image_sha256']
image=out/m['image'];archive=out/(image.stem+'.zip');assert not archive.exists()
readme=('ODROID-U3 Ubuntu '+m['ubuntu']+' '+m['variant']+'\nKernel: '+m['kernel']+'\n\nDefault login: odroid\nDefault password: odroid\nUse sudo with this password; root SSH accepts only your installed public keys; root password SSH is disabled.\nEthernet uses DHCP and a hardware-derived MAC. Root expands on first boot.\n\nWrite the complete IMG to the selected SD/eMMC user area. A normal SD-reader\nwrite does not update eMMC boot0. See the project eMMC recovery instructions.\n\nCandidate status: this new image still requires physical first-boot acceptance.\nDo not treat a ZIP checksum or offline validation as a successful hardware boot.\n')
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
    for path in [image,out/'BUILD-MANIFEST.json',out/'PACKAGES.tsv',out/'VALIDATION.json',out/(image.name+'.sha256'),out/m['emmc_boot0_payload']['file'],repo/'scripts/u3-emmc-boot0.py',repo/'LICENSE']:z.write(path,path.name)
    for path in sorted((repo/'docs').glob('*.md')):z.write(path,'docs/'+path.name)
    z.writestr('README.txt',readme)
with zipfile.ZipFile(archive) as z:
    with z.open(image.name) as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
    assert actual==m['image_sha256']
    assert z.testzip() is None
with archive.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
(out/(archive.name+'.sha256')).write_text(digest+'  '+archive.name+'\n')
docs_commit=subprocess.check_output(['git','-c','safe.directory='+str(repo),'-C',str(repo),'rev-parse','HEAD'],text=True).strip()
proof={'documentation_packaging_commit':docs_commit,'image_recipe_commit':m['recipe_commit'],'zip':archive.name,'zip_bytes':archive.stat().st_size,'zip_sha256':digest,'image_sha256':actual,'zip_crc_and_image_roundtrip_verified':True,'physical_boot_acceptance':False,'public_release_published':False}
(out/'ZIP-VERIFICATION.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
