#!/usr/bin/env python3
"""Compile the actual clock/IRQ helper and both call sites with host stubs.

This tests wait/clock ordering and forbidden-context exclusions, not hardware.
"""
import argparse,json,re,subprocess,tempfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',required=True,type=Path);a=p.parse_args();s=a.source.read_text();start=s.index('/* Opt-in U3 I2C0 IRQ/clock lifetime control;');end=s.index('\nstatic inline u32 u3_readl(',start);helper=s[start:end]
pairs=re.findall(r'u3_i2c_sync_before_clockoff\(i2c\);\n\s*clk_disable\(i2c->clk\);',s);assert len(pairs)==2
xfer_start=s.index('static int s3c24xx_i2c_xfer(');xfer_end=s.index('static int s3c24xx_i2c_xfer_atomic(',xfer_start);assert s[xfer_start:xfer_end].count('u3_i2c_sync_before_clockoff(i2c);')==2
prefix=r'''
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#define QUIRK_POLL 8
#define QUIRK_ATOMIC 16
#define module_param_named(...)
#define MODULE_PARM_DESC(...)
#define READ_ONCE(x) (x)
#define WRITE_ONCE(x,v) do { (x)=(v); } while(0)
struct s3c24xx_i2c { bool u3_diag_target; unsigned quirks,irq; void *clk; };
static bool can_preempt=true;
static unsigned events[32],pos,calls;
static bool preemptible(void) { return can_preempt; }
static void u3_i2c_mark(struct s3c24xx_i2c *i,unsigned stage,unsigned irq,unsigned quirks) {
 assert(irq==i->irq && quirks==i->quirks); events[pos++]=stage;
}
static void synchronize_irq(unsigned irq) { assert(irq==84); assert(can_preempt); events[pos++]=1000; calls++; }
static void clk_disable(void *clk) { assert(clk==NULL); events[pos++]=999; }
'''
funcs='\nstatic void actual_success_clockoff(struct s3c24xx_i2c *i2c) { '+pairs[0]+' }\nstatic void actual_retry_clockoff(struct s3c24xx_i2c *i2c) { '+pairs[1]+' }\n'
tests=r'''
int main(void) {
 struct s3c24xx_i2c i={true,0,84,NULL};
 assert(!u3_sync_irq && u3_sync_count==0 && u3_sync_skipped==0);
 actual_success_clockoff(&i); assert(calls==0 && pos==1 && events[0]==999);
 u3_sync_irq=true; i.u3_diag_target=false; pos=0;
 actual_success_clockoff(&i); assert(calls==0 && pos==1 && events[0]==999);
 i.u3_diag_target=true; i.quirks=QUIRK_POLL; pos=0;
 actual_success_clockoff(&i); assert(calls==0 && u3_sync_skipped==1 && pos==1);
 i.quirks=QUIRK_ATOMIC; pos=0;
 actual_success_clockoff(&i); assert(calls==0 && u3_sync_skipped==2 && pos==1);
 i.quirks=0; can_preempt=false; pos=0;
 actual_success_clockoff(&i); assert(calls==0 && u3_sync_skipped==3 && pos==1);
 can_preempt=true; pos=0;
 actual_success_clockoff(&i);
 assert(calls==1 && u3_sync_count==1 && pos==4);
 assert(events[0]==200 && events[1]==1000 && events[2]==201 && events[3]==999);
 pos=0; actual_retry_clockoff(&i);
 assert(calls==2 && u3_sync_count==2 && u3_sync_skipped==3 && pos==4);
 assert(events[0]==200 && events[1]==1000 && events[2]==201 && events[3]==999);
 u3_sync_irq=false; pos=0; actual_retry_clockoff(&i);
 assert(calls==2 && u3_sync_count==2 && pos==1 && events[0]==999);
 puts("8 actual IRQ/clock control cases passed"); return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='u3-i2csync-qa-') as t:
 c=Path(t)/'control.c';exe=Path(t)/'control';c.write_text(prefix+helper+funcs+tests);subprocess.run(['gcc','-std=gnu11','-Wall','-Wextra','-Werror','-fsanitize=undefined',str(c),'-o',str(exe)],check=True);subprocess.run([str(exe)],check=True)
print(json.dumps({'cases':8,'actual_helper_and_both_transfer_clockoff_sites':True,'wait_precedes_clockoff':True,'atomic_poll_nonpreemptible_excluded':True,'native_tested':False}))
