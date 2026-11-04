#!/usr/bin/env python3
"""Test the actual MMC helper and VQMMC caller using regulator API stubs."""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--baseline', type=Path, required=True)
a = p.parse_args()
s = a.source.read_text()
old = a.baseline.read_text()

def function(text, name, end):
    start = text.index(name)
    return text[start:text.index(end, start)]

helper = function(s, 'static int mmc_regulator_set_voltage_if_supported', '\n/**')
baseline = function(old, 'static int mmc_regulator_set_voltage_if_supported', '\n/**')
ocr = function(s, 'static int mmc_ocrbitnum_to_vdd', '\n/**')
vqmmc = function(s, 'int mmc_regulator_set_vqmmc(', '\nEXPORT_SYMBOL_GPL')
assert helper.index('if (min_uV > max_uV)') < helper.index('regulator_is_supported_voltage(')
assert helper.index('if (ret < 0)') < helper.index('regulator_get_voltage(')
assert helper[helper.index('\t/*\n\t * The voltage is already set'): ] == baseline[baseline.index('\t/*\n\t * The voltage is already set'): ]
prefix = r'''
#include <assert.h>
#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#define max(a,b) ((a)>(b)?(a):(b))
#define min(a,b) ((a)<(b)?(a):(b))
#define ilog2(a) __builtin_ctz((unsigned)(a))
#define MMC_VDD_165_195 (1U<<7)
#define MMC_SIGNAL_VOLTAGE_330 0
#define MMC_SIGNAL_VOLTAGE_180 1
#define MMC_SIGNAL_VOLTAGE_120 2
#define IS_ERR(p) ((uintptr_t)(p)>(uintptr_t)-4096)
#define dev_dbg(dev,...) ((void)(dev))
struct regulator { int unused; };
struct device { int unused; };
struct mmc_ios { int signal_voltage,vdd; };
struct mmc_host { struct { struct regulator *vqmmc; } supply; struct mmc_ios ios; struct device dev; };
static struct device *mmc_dev(struct mmc_host *m) { return &m->dev; }
static int supported,current,triplet_result,queries,reads,sets,invalid_ranges,low,target,high;
static int regulator_is_supported_voltage(struct regulator *r,int lo,int hi) {
 (void)r;queries++;low=lo;high=hi;return supported;
}
static int regulator_get_voltage(struct regulator *r) { (void)r;reads++;return current; }
static int regulator_set_voltage_triplet(struct regulator *r,int lo,int aim,int hi) {
 (void)r;sets++;low=lo;target=aim;high=hi;
 if(lo>hi || aim>hi) invalid_ranges++;
 return triplet_result;
}
static void reset(void) { supported=1;current=2800000;triplet_result=0;queries=reads=sets=invalid_ranges=0;low=target=high=0; }
'''
tests = r'''
int main(void) {
 struct regulator r={0};int cases=0;
 struct mmc_host m={.supply={&r},.ios={MMC_SIGNAL_VOLTAGE_330,7},.dev={0}};
 reset();supported=-ETIMEDOUT;
 assert(mmc_regulator_set_voltage_if_supported(&r,2700000,1650000,2150000)==-EINVAL && queries==0 && reads==0 && sets==0);cases++;
 reset();supported=-EIO;assert(mmc_regulator_set_voltage_if_supported(&r,2700000,2800000,3600000)==-EIO && reads==0 && sets==0);cases++;
 reset();supported=-ETIMEDOUT;assert(mmc_regulator_set_voltage_if_supported(&r,2700000,2800000,3600000)==-ETIMEDOUT && reads==0 && sets==0);cases++;
 reset();supported=-517;assert(mmc_regulator_set_voltage_if_supported(&r,2700000,2800000,3600000)==-517 && reads==0 && sets==0);cases++;
 reset();supported=0;assert(mmc_regulator_set_voltage_if_supported(&r,2700000,2800000,3600000)==-EINVAL && reads==0 && sets==0);cases++;
 reset();assert(mmc_regulator_set_voltage_if_supported(&r,2700000,2800000,3600000)==1 && reads==1 && sets==0);cases++;
 reset();current=2700000;assert(mmc_regulator_set_voltage_if_supported(&r,2700000,2800000,3600000)==0 && sets==1 && low==2700000 && target==2800000 && high==3600000);cases++;
 reset();current=2700000;triplet_result=-EIO;assert(mmc_regulator_set_voltage_if_supported(&r,2700000,2800000,3600000)==-EIO && sets==1);cases++;
 reset();supported=2;assert(mmc_regulator_set_voltage_if_supported(&r,2700000,2800000,3600000)==1 && sets==0);cases++;
 /* The existing optional current-read optimization is intentionally retained. */
 reset();current=-EIO;assert(mmc_regulator_set_voltage_if_supported(&r,2700000,2800000,3600000)==0 && sets==1);cases++;
 /* Real VMMC1.8 / VQMMC2.8 caller: reject inverted first range, propagate fallback read error. */
 reset();supported=-ETIMEDOUT;assert(mmc_regulator_set_vqmmc(&m,&m.ios)==-ETIMEDOUT && queries==1 && reads==0 && sets==0);cases++;
 reset();assert(mmc_regulator_set_vqmmc(&m,&m.ios)==0 && sets==1 && low==2700000 && target==1650000 && high==3600000 && invalid_ranges==0);cases++;
 reset();m.ios.signal_voltage=MMC_SIGNAL_VOLTAGE_180;current=1800000;assert(mmc_regulator_set_vqmmc(&m,&m.ios)==1 && low==1700000 && high==1950000 && sets==0);cases++;
 reset();m.ios.signal_voltage=MMC_SIGNAL_VOLTAGE_120;current=1200000;assert(mmc_regulator_set_vqmmc(&m,&m.ios)==1 && low==1100000 && high==1300000 && sets==0);cases++;
 reset();m.ios.signal_voltage=99;assert(mmc_regulator_set_vqmmc(&m,&m.ios)==-EINVAL && queries==0);cases++;
 reset();m.supply.vqmmc=(void *)(intptr_t)-517;assert(mmc_regulator_set_vqmmc(&m,&m.ios)==-EINVAL && queries==0);cases++;
 assert(cases==16);printf("%d MMC regulator error/range/caller cases passed\n",cases);return 0;
}
'''
regression = r'''
int main(void) {
 struct regulator r={0};reset();supported=-ETIMEDOUT;current=-ETIMEDOUT;
 assert(mmc_regulator_set_voltage_if_supported(&r,2700000,2800000,3600000)==0 && sets==1);
 reset();supported=-ETIMEDOUT;current=-ETIMEDOUT;
 assert(mmc_regulator_set_voltage_if_supported(&r,2700000,1650000,2150000)==0 && invalid_ranges==1);
 puts("baseline API-stub regression: negative support result reaches voltage API, including inverted range");return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='u3-mmc-regulator-qa-') as td:
    for name, text in [('fixed', prefix + ocr + helper + vqmmc + tests),
                       ('baseline', prefix + ocr + baseline + vqmmc + regression)]:
        c = Path(td) / (name + '.c')
        exe = Path(td) / name
        c.write_text(text)
        subprocess.run(['gcc', '-std=gnu11', '-Wall', '-Wextra', '-Werror',
                        '-fsanitize=undefined', str(c), '-o', str(exe)], check=True)
        subprocess.run([str(exe)], check=True)
print(json.dumps({'cases': 16, 'actual_helper_and_vqmmc_caller_compiled': True,
                  'baseline_error_path_observed_with_api_stubs_only': True,
                  'negative_support_errors_propagated_without_voltage_call': True,
                  'inverted_range_rejected_without_hardware_api_call': True,
                  'healthy_voltage_arguments_and_optional_read_behavior_unchanged': True,
                  'native_tested': False}))
