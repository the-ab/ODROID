#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Fetch hash-pinned sources and extract only the required reference boot blocks."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,urllib.request,zipfile
if not __debug__:raise SystemExit('Run without Python optimization: validation must remain enabled')

p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cache',type=Path,required=True);p.add_argument('--boot-reference',type=Path);a=p.parse_args()
repo=Path(__file__).resolve().parent.parent;lock=json.loads((repo/'sources.lock.json').read_text());a.cache.mkdir(parents=True,exist_ok=True)
def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
for item in lock['sources']:
    target=a.cache/item['filename']
    if not target.exists():
        partial=target.with_suffix(target.suffix+'.partial')
        assert not partial.exists()
        try:
            with urllib.request.urlopen(item['url'],timeout=60) as r,partial.open('xb') as f:shutil.copyfileobj(r,f)
            assert sha(partial)==item['sha256'],item['filename']
            partial.rename(target)
        finally:
            if partial.exists():partial.unlink()
    assert sha(target)==item['sha256'],item['filename']
    print('Verified',target)
if a.boot_reference:
    reference_hash=sha(a.boot_reference)
    if reference_hash==lock['boot_reference']['sha256']:
        with zipfile.ZipFile(a.boot_reference) as z:
            images=[n for n in z.namelist() if n.lower().endswith('.img')];assert len(images)==1
            with z.open(images[0]) as f:head=f.read(2423*512)
    else:
        assert reference_hash==lock['boot_reference']['image_sha256'],'Reference ZIP/image differs'
        with a.boot_reference.open('rb') as f:head=f.read(2423*512)
    for item in lock['boot_reference']['component_layout']:
        if item['name']=='u-boot':continue
        start=item['sd_sector']*512;blob=head[start:start+item['sectors']*512]
        assert hashlib.sha256(blob).hexdigest()==item['sha256'],item['name']
        target=a.cache/(item['name']+'.bin')
        if target.exists():assert target.read_bytes()==blob
        else:target.write_bytes(blob)
        print('Verified reference component',target)
