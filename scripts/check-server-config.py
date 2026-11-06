#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Fail when a resolved U3 server configuration loses mandatory capabilities."""
from pathlib import Path
import argparse,hashlib,json
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--config',type=Path,required=True);p.add_argument('--requirements',type=Path,default=Path(__file__).resolve().parents[1]/'boards/u3/server-requirements.json');a=p.parse_args()
requirements=json.loads(a.requirements.read_text());cfg={}
for line in a.config.read_text().splitlines():
 if line.startswith('CONFIG_') and '=' in line:
  k,v=line.split('=',1);cfg[k[7:]]=v
 elif line.startswith('# CONFIG_') and line.endswith(' is not set'):cfg[line.split()[1][7:]]='n'
missing={k:cfg.get(k,'absent') for k in requirements['required_builtin'] if cfg.get(k)!='y'}
missing.update({k:cfg.get(k,'absent') for k in requirements['required_available'] if cfg.get(k) not in ('y','m')})
lsms=cfg.get('LSM','').strip('"').split(',')
for name in requirements['required_lsms']:
 if name not in lsms:missing['LSM:'+name]='absent'
result={'server_config_passed':not missing,'required_capabilities':len(requirements['required_builtin'])+len(requirements['required_available']),'missing':missing,'config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest(),'runtime_tests_required_separately':True}
print(json.dumps(result,indent=2))
if missing:raise SystemExit(1)
