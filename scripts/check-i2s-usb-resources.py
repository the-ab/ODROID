#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
from pathlib import Path
import argparse,subprocess,tempfile
p=argparse.ArgumentParser(description='Exercise the actual patched I2S wrapper and USB acquisition branch with host API stubs');p.add_argument('--kernel-source',type=Path,required=True);a=p.parse_args();temporary=tempfile.TemporaryDirectory();w=Path(temporary.name);tree=a.kernel_source;source=(tree/'sound/soc/samsung/dmaengine.c').read_text();source='\n'.join(x for x in source.splitlines() if not x.startswith('#include'))
preamble=r'''
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#define GFP_KERNEL 0
#define ENOMEM 12
#define ENODEV 19
#define EPROBE_DEFER 517
#define EIO 5
#define BIT(n) (1U<<(n))
#define SND_DMAENGINE_PCM_FLAG_COMPAT BIT(0)
#define SNDRV_PCM_STREAM_PLAYBACK 0
#define SNDRV_PCM_STREAM_CAPTURE 1
#define MODULE_AUTHOR(x)
#define MODULE_DESCRIPTION(x)
#define MODULE_LICENSE(x)
#define EXPORT_SYMBOL_GPL(x)
#define IS_ERR(p) ((uintptr_t)(p)>=(uintptr_t)-4095)
#define ERR_PTR(n) ((void *)(intptr_t)(n))
struct device { void *of_node; };
struct dma_chan { int value; };
struct snd_pcm_substream {int stream;};
struct snd_dmaengine_dai_dma_data {const char *chan_name;};
struct snd_soc_dai {struct device *dev;struct snd_dmaengine_dai_dma_data *data[2];};
struct snd_soc_pcm_runtime {struct snd_soc_dai *cpu;};
typedef bool (*dma_filter_fn)(void *,void *);
struct snd_dmaengine_pcm_config {void *prepare_slave_config;dma_filter_fn compat_filter_fn;struct device *dma_dev;const char *chan_names[2];struct dma_chan *(*compat_request_channel)(struct snd_soc_pcm_runtime *,struct snd_pcm_substream *);};
static struct snd_dmaengine_pcm_config *registered;
static struct device *requested_device;
static const char *requested_name;
static int requests,request_error;
static struct dma_chan channel;
static void *devm_kzalloc(struct device *d,size_t n,int flags){return calloc(1,n);}
static void snd_dmaengine_pcm_prepare_slave_config(void){}
static struct snd_soc_dai *snd_soc_rtd_to_cpu(struct snd_soc_pcm_runtime *r,int n){return r->cpu;}
static struct snd_dmaengine_dai_dma_data *snd_soc_dai_get_dma_data(struct snd_soc_dai *d,struct snd_pcm_substream *s){return d->data[s->stream];}
static struct dma_chan *dma_request_chan(struct device *d,const char *name){requests++;requested_device=d;requested_name=name;return request_error?ERR_PTR(-request_error):&channel;}
static int devm_snd_dmaengine_pcm_register(struct device *d,struct snd_dmaengine_pcm_config *c,unsigned int flags){assert(flags&SND_DMAENGINE_PCM_FLAG_COMPAT);registered=c;return 0;}
'''
tests=r'''
static bool filter(void *a,void *b){return true;}
int main(void){
 struct device main_dev={.of_node=(void *)1},child={0},legacy={0};
 struct snd_dmaengine_dai_dma_data tx={.chan_name="tx-sec"};
 struct snd_soc_dai cpu={.dev=&main_dev,.data={&tx,NULL}};
 struct snd_soc_pcm_runtime runtime={.cpu=&cpu};
 struct snd_pcm_substream playback={.stream=0},capture={.stream=1};
 assert(!samsung_asoc_dma_platform_register(&main_dev,filter,"tx","rx",NULL));
 assert(registered->compat_filter_fn==filter && !registered->compat_request_channel && !registered->dma_dev);
 assert(!strcmp(registered->chan_names[0],"tx") && !strcmp(registered->chan_names[1],"rx"));free(registered);
 assert(!samsung_asoc_dma_platform_register(&child,filter,"tx-sec",NULL,&main_dev));
 assert(registered->compat_request_channel && !registered->dma_dev && !registered->chan_names[0] && !registered->chan_names[1] && requests==0);
 assert(!registered->compat_request_channel(&runtime,&capture) && requests==0);
 assert(registered->compat_request_channel(&runtime,&playback)==&channel && requests==1 && requested_device==&main_dev && !strcmp(requested_name,"tx-sec"));
 request_error=ENODEV;assert(!registered->compat_request_channel(&runtime,&playback));
 tx.chan_name=NULL;int before=requests;assert(!registered->compat_request_channel(&runtime,&playback) && requests==before);free(registered);
 assert(!samsung_asoc_dma_platform_register(&child,filter,"tx-sec",NULL,&legacy));assert(!registered->compat_request_channel && registered->dma_dev==&legacy);free(registered);
 return 0;
}
'''
c=w/'test-dma-resource-logic.c';c.write_text(preamble+'\n'+source+'\n'+tests);exe=w/'test-dma-resource-logic';subprocess.run(['cc','-Wall','-Wextra','-Wno-unused-parameter','-Werror',str(c),'-o',str(exe)],check=True);subprocess.run([str(exe)],check=True);print('Actual patched Samsung wrapper: primary/legacy preservation, no eager secondary RX, correct CPU-DAI TX mapping and error/null cases passed')

usb=(tree/'drivers/phy/samsung/phy-samsung-usb2.c').read_text();start=usb.index('\tdrv->vbus = devm_regulator_get_optional');end=usb.index('\n\tfor (i = 0;',start);branch=usb[start:end]
usb_stubs=r"""
#include <assert.h>
#include <stdint.h>
#define ENODEV 19
#define EPROBE_DEFER 517
#define EIO 5
#define IS_ERR(p) ((uintptr_t)(p)>=(uintptr_t)-4095)
#define PTR_ERR(p) ((long)(p))
#define ERR_PTR(n) ((void *)(intptr_t)(n))
#define NULL ((void *)0)
struct device {int unused;};
struct regulator {int unused;};
struct samsung_usb2_phy_driver {struct regulator *vbus;};
static struct regulator supply;
static int error_code,errors_reported;
static struct regulator *devm_regulator_get_optional(struct device *dev,const char *name){return error_code?ERR_PTR(-error_code):&supply;}
static int dev_err_probe(struct device *dev,int error,const char *message){errors_reported++;return error;}
"""
usb_test=usb_stubs+'\nstatic int acquire(struct device *dev,struct samsung_usb2_phy_driver *drv){int ret;\n'+branch+'\nreturn 0;}\n'+r"""
int main(void){
 struct device dev={0};struct samsung_usb2_phy_driver drv={0};
 error_code=0;assert(acquire(&dev,&drv)==0 && drv.vbus==&supply && !errors_reported);
 error_code=ENODEV;assert(acquire(&dev,&drv)==0 && !drv.vbus && !errors_reported);
 error_code=EPROBE_DEFER;assert(acquire(&dev,&drv)==-EPROBE_DEFER && errors_reported==1);
 error_code=EIO;assert(acquire(&dev,&drv)==-EIO && errors_reported==2);
 return 0;
}
"""
c=w/'test-optional-vbus.c';c.write_text(usb_test);exe=w/'test-optional-vbus';subprocess.run(['cc','-Wall','-Wextra','-Wno-unused-parameter','-Werror',str(c),'-o',str(exe)],check=True);subprocess.run([str(exe)],check=True);print('Actual USB acquisition branch: present/absent provider, probe deferral and I/O error propagation passed');temporary.cleanup()
