#!/usr/bin/env python3
"""Compile the actual alias capture helper and exercise range/alias isolation."""
from pathlib import Path
import argparse,json,re,subprocess,tempfile

p=argparse.ArgumentParser();p.add_argument('--observer',type=Path,required=True);a=p.parse_args()
obs=a.observer.read_text();start=obs.index('struct u3_diag_spi {');end=obs.index('\nstatic void u3_diag_dump',start);helper=obs[start:end]
assert 'writel' not in obs and 'GIC_CPU_INTACK' not in obs and 'GIC_CPU_EOI' not in obs
assert not re.search(r'\b(smp_call_function|on_each_cpu|ioremap|writel)\s*\(',helper)
dump=obs[obs.index('static void u3_diag_dump'):obs.index('/* Called only from an existing watchdog report')]
assert dump.index('u3_diag_read_shared(d, &shared[cpu]);')<dump.index('pr_info(')
assert 'u3_dist + cpu * 0x4000' in dump and 'observer_begin' in dump and 'observer_end' in dump
assert 'if (!d->valid)' in dump and 'U3IRQALIAS bank=%u intid=%u' in dump
assert 'static struct u3_diag_bank bank[4];' in dump
assert 'static struct u3_diag_shared shared[4];' in dump
assert 'static struct u3_i2c_progress progress[4][U3DIAG_CHANNELS];' in dump
assert dump.index('if (!u3_diag_begin_report(limited))') < dump.index('u3_progress_copy(progress);')
assert dump.rindex('pr_info(') < dump.index('u3_diag_end_report(limited);')
c='''#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef uint32_t u32;
#define __iomem
#define ARRAY_SIZE(a) (sizeof(a)/sizeof((a)[0]))
#define GIC_DIST_CTR 0x004
#define GIC_DIST_IIDR 0x008
#define GIC_DIST_ENABLE_SET 0x100
#define GIC_DIST_PENDING_SET 0x200
#define GIC_DIST_ACTIVE_SET 0x300
#define GIC_DIST_PRI 0x400
#define GIC_DIST_TARGET 0x800
#define GIC_DIST_CONFIG 0xc00
static unsigned char regs[0x10000];
static unsigned bank,typer,count;
static const unsigned expected[]={4,8,0x104,0x204,0x304,0x108,0x208,0x308,0x10c,0x20c,0x30c,0x110,0x210,0x310,0x458,0x858,0xc14,0x46c,0x86c,0xc18};
static u32 readl_relaxed(void *p) {
 uintptr_t n=(unsigned char*)p-regs; unsigned off=n-bank*0x4000;
 assert(n+4<=sizeof(regs) && !(n&3) && count<ARRAY_SIZE(expected));
 assert(off==expected[count++]);
 return off==4 ? 0xfc60|typer : (u32)n^0xa55aa55a;
}
'''+helper+'''
int main(void) {
 for(bank=0;bank<4;bank++) for(typer=0;typer<32;typer++) {
  struct u3_diag_shared out; memset(&out,0xcc,sizeof(out));count=0;
  u3_diag_read_shared(regs+bank*0x4000,&out);
  assert(out.typer==(0xfc60|typer));assert(out.iidr==((bank*0x4000+8)^0xa55aa55a));
  assert(out.valid==(typer>=4));assert(count==(out.valid?20:2));
  if(!out.valid) {
   for(unsigned i=0;i<4;i++) assert(!out.enabled[i] && !out.pending[i] && !out.active[i]);
   for(unsigned i=0;i<2;i++) assert(!out.spi[i].priority && !out.spi[i].target && !out.spi[i].config);
  } else {
   for(unsigned i=0;i<4;i++) {
    assert(out.enabled[i]==((bank*0x4000+0x104+i*4)^0xa55aa55a));
    assert(out.pending[i]==((bank*0x4000+0x204+i*4)^0xa55aa55a));
    assert(out.active[i]==((bank*0x4000+0x304+i*4)^0xa55aa55a));
   }
   const unsigned off[][3]={{0x458,0x858,0xc14},{0x46c,0x86c,0xc18}};
   for(unsigned i=0;i<2;i++) {
    assert(out.spi[i].priority==((bank*0x4000+off[i][0])^0xa55aa55a));
    assert(out.spi[i].target==((bank*0x4000+off[i][1])^0xa55aa55a));
    assert(out.spi[i].config==((bank*0x4000+off[i][2])^0xa55aa55a));
   }
  }
 }
 puts("128 actual-helper alias/range cases passed");return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='u3-alias-v25-') as td:
    src=Path(td)/'check.c';src.write_text(c);out=Path(td)/'check'
    subprocess.run(['gcc','-std=gnu11','-O2','-Wall','-Wextra','-Werror','-fsanitize=undefined','-fno-sanitize-recover=all',str(src),'-o',str(out)],check=True)
    subprocess.run([str(out)],check=True)
print(json.dumps({'actual_helper_cases':128,'all_four_aliases':True,'invalid_range_does_not_read_SPI_state':True,'observer_read_only':True,'snapshot_before_output':True}))
