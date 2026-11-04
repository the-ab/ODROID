#!/usr/bin/env python3
"""Exercise the actual managed clock helper with host clock/devres stubs."""
import argparse,json,subprocess,tempfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);a=p.parse_args();s=a.source.read_text();start=s.index('/* Opt-in U3 I2C0 clock lifetime control;');end=s.index('\nstatic inline u32 u3_readl(',start);helper=s[start:end]
assert s.count('ret = u3_i2c_hold_clock(i2c);')==1
assert s.index('irq_get_irq_data(i2c->irq)')<s.index('ret = u3_i2c_hold_clock(i2c);')<s.index('ret = devm_request_irq(')
prefix=r'''
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#define module_param_named(...)
#define MODULE_PARM_DESC(...)
#define WRITE_ONCE(x,v) do { (x)=(v); } while(0)
struct clock { int prepared,enabled; };
struct s3c24xx_i2c { bool u3_diag_target; unsigned irq; struct clock *clk; void *dev; };
static int prepare_error,action_error,prepare_calls,info_calls;
static void (*action)(void *); static void *action_data;
static int clk_prepare_enable(struct clock *c) { prepare_calls++; if(prepare_error) return prepare_error; c->prepared++; c->enabled++; return 0; }
static void clk_disable_unprepare(struct clock *c) { assert(c->prepared>0 && c->enabled>0); c->enabled--; c->prepared--; }
static int devm_add_action_or_reset(void *dev,void (*fn)(void *),void *data) {
 assert(dev==NULL); if(action_error) { fn(data); return action_error; } action=fn; action_data=data; return 0;
}
static unsigned long clk_get_rate(struct clock *c) { assert(c->prepared>0 && c->enabled>0); return 100000000UL; }
#define dev_info(...) do { info_calls++; } while(0)
'''
tests=r'''
int main(void) {
 struct clock c={1,0}; struct s3c24xx_i2c i={true,84,&c,NULL};
 assert(!u3_hold_clock && !u3_clock_held);
 assert(u3_i2c_hold_clock(&i)==0 && prepare_calls==0 && c.prepared==1 && c.enabled==0);
 u3_hold_clock=true; i.u3_diag_target=false;
 assert(u3_i2c_hold_clock(&i)==0 && prepare_calls==0);
 i.u3_diag_target=true; prepare_error=-12;
 assert(u3_i2c_hold_clock(&i)==-12 && c.prepared==1 && c.enabled==0 && action==NULL);
 prepare_error=0; action_error=-12;
 assert(u3_i2c_hold_clock(&i)==-12 && c.prepared==1 && c.enabled==0 && !u3_clock_held && action==NULL);
 action_error=0;
 assert(u3_i2c_hold_clock(&i)==0 && c.prepared==2 && c.enabled==1 && u3_clock_held && u3_clock_rate==100000000UL && info_calls==1 && action!=NULL);
 for(int n=0;n<8;n++) { c.enabled++; assert(c.enabled==2); c.enabled--; assert(c.enabled==1); }
 /* Driver removes original prepare reference; devres releases extra pair. */
 c.prepared--; assert(c.prepared==1 && c.enabled==1); action(action_data);
 assert(c.prepared==0 && c.enabled==0 && !u3_clock_held);
 /* IRQ registration error: original prepare cleanup then devres callback. */
 action=NULL; c.prepared=1; c.enabled=0;
 assert(u3_i2c_hold_clock(&i)==0 && c.prepared==2 && c.enabled==1);
 c.prepared--; action(action_data);
 assert(c.prepared==0 && c.enabled==0 && !u3_clock_held);
 puts("8 managed clock lifetime cases passed"); return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='u3-clockhold-qa-') as td:
 c=Path(td)/'control.c';exe=Path(td)/'control';c.write_text(prefix+helper+tests);subprocess.run(['gcc','-std=gnu11','-Wall','-Wextra','-Werror','-fsanitize=undefined',str(c),'-o',str(exe)],check=True);subprocess.run([str(exe)],check=True)
print(json.dumps({'cases':8,'actual_helper_compiled':True,'target_checked_before_irq_registration':True,'balanced_prepare_enable_normal_remove_and_error_cleanup':True,'native_tested':False}))
