#!/usr/bin/env python3
"""Compile actual affinity helper with host IRQ API stubs; no hardware claim."""
import argparse,json,subprocess,tempfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);a=p.parse_args()
s=a.source.read_text();start=s.index('/* Opt-in U3 I2C0 routing experiment;');end=s.index('\nstatic inline void u3_i2c_mark',start);helper=s[start:end]
assert s.count('u3_i2c_set_test_affinity(i2c);')==1
assert s.index('devm_request_irq(')<s.index('u3_i2c_set_test_affinity(i2c);')<s.index('ret = i2c_add_numbered_adapter(')
prefix=r'''
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#define module_param_named(...)
#define MODULE_PARM_DESC(...)
struct s3c24xx_i2c { bool u3_diag_target; unsigned irq; void *dev; };
static unsigned nr_cpu_ids=4;
static bool online[4]={true,true,true,true};
static int calls,warns,infos,api_result;
static unsigned actual_irq,actual_cpu;
static bool cpu_online(unsigned cpu) { assert(cpu<4); return online[cpu]; }
static unsigned cpumask_of(unsigned cpu) { assert(cpu<4); return cpu; }
static int irq_set_affinity(unsigned irq,unsigned cpu) {
 calls++; actual_irq=irq; actual_cpu=cpu; return api_result;
}
#define dev_warn(...) do { warns++; } while(0)
#define dev_info(...) do { infos++; } while(0)
'''
tests=r'''
int main(void) {
 struct s3c24xx_i2c target={true,84,NULL};
 assert(u3_irq_cpu==-1);
 u3_i2c_set_test_affinity(&target);
 assert(calls==0 && warns==0 && infos==0);
 u3_irq_cpu=1; target.u3_diag_target=false;
 u3_i2c_set_test_affinity(&target);
 assert(calls==0 && warns==0 && infos==0);
 target.u3_diag_target=true; u3_irq_cpu=4;
 u3_i2c_set_test_affinity(&target);
 assert(calls==0 && warns==1 && infos==0);
 u3_irq_cpu=1; online[1]=false;
 u3_i2c_set_test_affinity(&target);
 assert(calls==0 && warns==2 && infos==0);
 online[1]=true;
 u3_i2c_set_test_affinity(&target);
 assert(calls==1 && actual_irq==84 && actual_cpu==1 && infos==1);
 api_result=-22;
 u3_i2c_set_test_affinity(&target);
 assert(calls==2 && warns==3 && infos==1);
 api_result=0; u3_irq_cpu=0;
 u3_i2c_set_test_affinity(&target);
 assert(calls==3 && actual_cpu==0 && infos==2);
 puts("7 affinity helper cases passed"); return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='odroid-affinity-qa-') as t:
 c=Path(t)/'control.c';exe=Path(t)/'control';c.write_text(prefix+helper+tests)
 subprocess.run(['gcc','-std=gnu11','-Wall','-Wextra','-Werror','-fsanitize=undefined',str(c),'-o',str(exe)],check=True)
 subprocess.run([str(exe)],check=True)
print(json.dumps({'cases':7,'actual_helper_extracted':True,'placement_verified':True,'native_routing_verified':False}))
