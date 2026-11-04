#!/usr/bin/env python3
"""Check actual polling/IRQ policy with host API stubs."""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
s = p.parse_args().source.read_text()
start = s.index('/* Opt-in U3 I2C0 process-context polling control;')
end = s.index('\nstatic void i2c_s3c_irq_nextbyte(', start)
helper = s[start:end]
assert s.count('if (!u3_i2c_polling(i2c)) {') == 1
assert s.count('if (u3_i2c_polling(i2c)) {') == 1
assert s.count('ret = u3_i2c_request_irq(pdev, i2c);') == 1
assert s.index('irq_get_irq_data(i2c->irq)') < s.index('ret = u3_i2c_request_irq(pdev, i2c);')
assert 'if (i2c->quirks & QUIRK_POLL)\n\t\tiiccon |= S3C2410_IICCON_SCALE(2);' in s
prefix = r'''
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#define module_param_named(...)
#define MODULE_PARM_DESC(...)
#define WRITE_ONCE(x,v) do { (x)=(v); } while(0)
#define QUIRK_POLL 8
#define QUIRK_ATOMIC 16
struct device { int unused; };
struct platform_device { struct device dev; };
struct s3c24xx_i2c { bool u3_diag_target,u3_poll_target; unsigned irq,quirks; struct device *dev; };
static int request_calls,request_result,info_calls;
static int s3c24xx_i2c_irq(int n,void *p) { (void)n; (void)p; return 0; }
static const char *dev_name(struct device *d) { (void)d; return "target"; }
static int devm_request_irq(struct device *d,unsigned irq,int (*f)(int,void *),unsigned flags,const char *name,void *data) {
 (void)d; (void)name; assert(irq==84 && flags==0 && f==s3c24xx_i2c_irq && data!=NULL);
 request_calls++; return request_result;
}
#define dev_info(...) do { info_calls++; } while(0)
'''
tests = r'''
int main(void) {
 struct platform_device p={0}; struct s3c24xx_i2c i={true,false,84,0,&p.dev};
 assert(!u3_poll && !u3_poll_active && !u3_poll_xfers);
 assert(!u3_i2c_polling(&i));
 assert(u3_i2c_request_irq(&p,&i)==0 && request_calls==1 && !i.u3_poll_target && !u3_poll_active);
 u3_poll=true; i.u3_diag_target=false;
 assert(u3_i2c_request_irq(&p,&i)==0 && request_calls==2 && !i.u3_poll_target);
 i.u3_diag_target=true;
 assert(u3_i2c_request_irq(&p,&i)==0 && request_calls==2 && i.u3_poll_target && u3_poll_active && info_calls==1);
 assert(u3_i2c_polling(&i));
 i.u3_poll_target=false; i.quirks=QUIRK_POLL; assert(u3_i2c_polling(&i));
 i.quirks=QUIRK_ATOMIC; assert(u3_i2c_polling(&i));
 i.quirks=1; assert(!u3_i2c_polling(&i));
 u3_poll=false; request_result=-12;
 assert(u3_i2c_request_irq(&p,&i)==-12 && request_calls==3 && !i.u3_poll_target);
 puts("9 polling and IRQ-policy cases passed"); return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='u3-poll-qa-') as td:
    c = Path(td) / 'control.c'
    exe = Path(td) / 'control'
    c.write_text(prefix + helper + tests)
    subprocess.run(['gcc', '-std=gnu11', '-Wall', '-Wextra', '-Werror',
                    '-fsanitize=undefined', str(c), '-o', str(exe)], check=True)
    subprocess.run([str(exe)], check=True)
print(json.dumps({'cases': 9, 'actual_helper_compiled': True,
                  'irq_target_validation_precedes_control': True,
                  'legacy_poll_and_atomic_paths_preserved': True,
                  'sata_divisor_quirk_not_enabled': True, 'native_tested': False}))
