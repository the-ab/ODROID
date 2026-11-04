#!/usr/bin/env python3
"""Exercise actual report admission and reproduce the old concurrent loss."""
import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--baseline', type=Path, required=True)
a = p.parse_args()
s = a.source.read_text()
start = s.index('/* Serialize first:')
end = s.index('\nstatic void u3_diag_dump(', start)
helper = s[start:end]
assert s.count('u3_diag_begin_report(limited)') == 1
assert s.count('u3_diag_end_report(limited)') == 1
assert s.index('U3IRQDIAG report-complete=') < s.index('u3_diag_end_report(limited)')
assert 'atomic_inc_return(&u3_diag_reports)' not in s
assert 'u3_diag_dump("armed", false);' in s
assert 'u3_diag_dump("SoftLockup", true);' in s
assert 'u3_diag_dump(message, true);' in s
old = a.baseline.read_text()
hook = re.search(r'void odroid_u3_i2cdiag_softlockup\(void\)\n\{.*?\n\}', old, re.S).group()
prefix = r'''
#define _GNU_SOURCE
#include <assert.h>
#include <pthread.h>
#include <sched.h>
#include <stdatomic.h>
#include <stdbool.h>
#include <stdio.h>
typedef struct { atomic_int counter; } atomic_t;
#define ATOMIC_INIT(v) { ATOMIC_VAR_INIT(v) }
static inline int atomic_cmpxchg(atomic_t *a,int old,int value) {
 atomic_compare_exchange_strong(&a->counter,&old,value); return old;
}
#define atomic_read(a) atomic_load_explicit(&(a)->counter,memory_order_relaxed)
#define atomic_inc(a) ((void)atomic_fetch_add_explicit(&(a)->counter,1,memory_order_relaxed))
#define atomic_inc_return(a) (atomic_fetch_add_explicit(&(a)->counter,1,memory_order_seq_cst)+1)
#define atomic_set(a,v) atomic_store_explicit(&(a)->counter,v,memory_order_relaxed)
#define atomic_set_release(a,v) atomic_store_explicit(&(a)->counter,v,memory_order_release)
static atomic_t u3_diag_busy=ATOMIC_INIT(0),u3_diag_reports=ATOMIC_INIT(0);
'''
tests = r'''
static pthread_barrier_t gate;
static atomic_int accepted;
static void *contender(void *unused) {
 (void)unused;
 if(u3_diag_begin_report(true)) { atomic_fetch_add(&accepted,1); u3_diag_end_report(true); }
 return NULL;
}
static void *racer(void *unused) {
 int rc=pthread_barrier_wait(&gate); assert(rc==0 || rc==PTHREAD_BARRIER_SERIAL_THREAD);
 return contender(unused);
}
static void concurrent(bool held) {
 pthread_t t[32];
 if(!held) assert(pthread_barrier_init(&gate,NULL,33)==0);
 for(int i=0;i<32;i++) assert(pthread_create(&t[i],NULL,held?contender:racer,NULL)==0);
 if(!held) { int rc=pthread_barrier_wait(&gate); assert(rc==0 || rc==PTHREAD_BARRIER_SERIAL_THREAD); }
 for(int i=0;i<32;i++) assert(pthread_join(t[i],NULL)==0);
 if(!held) assert(pthread_barrier_destroy(&gate)==0);
}
int main(void) {
 assert(u3_diag_begin_report(false)); concurrent(true);
 assert(atomic_read(&u3_diag_reports)==0 && atomic_load(&accepted)==0);
 u3_diag_end_report(false); assert(atomic_read(&u3_diag_busy)==0);
 assert(u3_diag_begin_report(true)); concurrent(true);
 assert(atomic_read(&u3_diag_reports)==0 && atomic_load(&accepted)==0);
 u3_diag_end_report(true); assert(atomic_read(&u3_diag_reports)==1);
 for(int n=1;n<3;n++) { assert(u3_diag_begin_report(true)); u3_diag_end_report(true); }
 for(int n=0;n<100000;n++) assert(!u3_diag_begin_report(true));
 assert(atomic_read(&u3_diag_reports)==3 && atomic_read(&u3_diag_busy)==0);
 assert(u3_diag_begin_report(false));u3_diag_end_report(false);
 assert(atomic_read(&u3_diag_reports)==3);
 for(int round=0;round<20;round++) {
  atomic_set(&u3_diag_reports,0); atomic_store(&accepted,0); concurrent(false);
  int n=atomic_load(&accepted);assert(n>=1 && n<=3 && atomic_read(&u3_diag_reports)==n);
  while(atomic_read(&u3_diag_reports)<3) { assert(u3_diag_begin_report(true));u3_diag_end_report(true); }
  assert(!u3_diag_begin_report(true) && atomic_read(&u3_diag_busy)==0);
 }
 puts("admission: held-guard contention, completed-budget bound, 640 concurrent racers passed");
 return 0;
}
'''
old_stub = r'''
static atomic_int started,release_dump,completed;
static bool odroid_u3_i2cdiag_on(void) { return true; }
static void u3_diag_dump(const char *reason) {
 (void)reason;if(atomic_cmpxchg(&u3_diag_busy,0,1)) return;
 atomic_store(&started,1);while(!atomic_load(&release_dump)) sched_yield();
 atomic_fetch_add(&completed,1);atomic_set(&u3_diag_busy,0);
}
'''
old_test = r'''
static void *caller(void *unused) { (void)unused;odroid_u3_i2cdiag_softlockup();return NULL; }
int main(void) {
 pthread_t owner,t[2];assert(pthread_create(&owner,NULL,caller,NULL)==0);
 while(!atomic_load(&started)) sched_yield();
 for(int i=0;i<2;i++) assert(pthread_create(&t[i],NULL,caller,NULL)==0);
 for(int i=0;i<2;i++) assert(pthread_join(t[i],NULL)==0);
 assert(atomic_read(&u3_diag_reports)==3 && atomic_load(&completed)==0);
 atomic_store(&release_dump,1);assert(pthread_join(owner,NULL)==0);
 assert(atomic_load(&completed)==1);odroid_u3_i2cdiag_softlockup();
 assert(atomic_load(&completed)==1 && atomic_read(&u3_diag_reports)==4);
 puts("baseline regression reproduced: three attempts, one completed dump, no remaining budget");
 return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='u3-admission-qa-') as td:
    for name, text in [('fixed', prefix + helper + tests),
                       ('baseline', prefix + old_stub + hook + old_test)]:
        c = Path(td) / (name + '.c')
        exe = Path(td) / name
        c.write_text(text)
        subprocess.run(['gcc', '-std=gnu11', '-Wall', '-Wextra', '-Werror',
                        '-pthread', '-fsanitize=undefined', str(c), '-o', str(exe)], check=True)
        subprocess.run([str(exe)], check=True)
print(json.dumps({'actual_fixed_helper_compiled': True, 'actual_old_hook_regression_reproduced': True,
                  'held_guard_contenders': 64, 'racing_threads': 640,
                  'post_limit_rejections': 100000, 'init_not_charged': True,
                  'three_completed_report_bound': True, 'native_tested': False}))
