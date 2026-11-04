#!/usr/bin/env python3
"""Compile the actual SPI attribute reader and check actual IAR mark/barrier order."""
from pathlib import Path
import argparse,json,re,subprocess,tempfile
p=argparse.ArgumentParser();p.add_argument('--tree',type=Path,required=True);a=p.parse_args()
obs=(a.tree/'arch/arm/mach-exynos/odroid-u3-irqdiag.c').read_text();gic=(a.tree/'drivers/irqchip/irq-gic.c').read_text()
start=obs.index('struct u3_diag_spi {');end=obs.index('\nstatic void u3_diag_dump',start);helper=obs[start:end]
assert helper.count('readl_relaxed(')==3 and 'writel' not in helper
start=gic.index('static void __exception_irq_entry gic_handle_irq(');end=gic.index('\nstatic void gic_handle_cascade_irq',start);fn=gic[start:end]
parts=['odroid_u3_i2cdiag_mark(U3DIAG_GIC_ALL, 10, 0, 0);','dsb(sy);','irqstat = readl_relaxed(cpu_base + GIC_CPU_INTACK);','odroid_u3_i2cdiag_mark(U3DIAG_GIC_ALL, 11, irqstat, 0);','dsb(sy);','generic_handle_domain_irq(gic->domain, irqnr);']
pos=0
for token in parts:pos=fn.index(token,pos)+len(token)
assert fn.count('dsb(sy);')==2
assert re.search(r'if \(u3_diag\) \{\s*odroid_u3_i2cdiag_mark\(U3DIAG_GIC_ALL, 10, 0, 0\);.*?dsb\(sy\);\s*}',fn,re.S)
assert 'GIC_CPU_INTACK' not in obs and 'GIC_CPU_EOI' not in obs and 'writel' not in obs
assert 'GIC_DIST_CTR) & 0x1f) + 1) * 32 <= 109' in obs
c='''#include <stdint.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
typedef uint32_t u32;
#define __iomem
#define GIC_DIST_PRI 0x400
#define GIC_DIST_TARGET 0x800
#define GIC_DIST_CONFIG 0xc00
static unsigned char regs[0x1000];
static unsigned offsets[3],count;
static u32 readl_relaxed(void *p) { uintptr_t n=(unsigned char*)p-regs; assert(n+4<=sizeof(regs) && (n&3)==0 && count<3); offsets[count++]=n; return (u32)n^0xa55aa55a; }
'''+helper+'''
int main(void) {
 unsigned ids[]={90,109};
 for(unsigned n=0;n<2;n++) {unsigned id=ids[n];struct u3_diag_spi out;count=0;u3_diag_read_spi(regs,id,&out);assert(count==3);assert(offsets[0]==0x400+(id/4)*4);assert(offsets[1]==0x800+(id/4)*4);assert(offsets[2]==0xc00+(id/16)*4);assert(out.priority==(offsets[0]^0xa55aa55a));assert(out.target==(offsets[1]^0xa55aa55a));assert(out.config==(offsets[2]^0xa55aa55a));}
 for(unsigned id=32;id<160;id++) {struct u3_diag_spi out;count=0;u3_diag_read_spi(regs,id,&out);assert(offsets[0]>=0x420 && offsets[0]<0x4a0);assert(offsets[1]>=0x820 && offsets[1]<0x8a0);assert(offsets[2]>=0xc08 && offsets[2]<0xc28);}
 puts("130 actual-helper register-offset cases passed");return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='u3-gic-order-') as td:
 f=Path(td)/'check.c';f.write_text(c);out=Path(td)/'check';subprocess.run(['gcc','-std=gnu11','-Wall','-Wextra','-Werror','-fsanitize=undefined','-fno-sanitize-recover=all','-O2',str(f),'-o',str(out)],check=True);subprocess.run([str(out)],check=True)
print(json.dumps({'actual_helper_cases':130,'actual_source_pre_and_post_IAR_DSB_order':True,'observer_read_only':True,'implemented_SPI_range_gate':True}))
