/* SPDX-License-Identifier: GPL-2.0-only */
/* Ordinary bounded io_uring functionality checks; no vulnerability reproducer. */
#define _GNU_SOURCE
#include <linux/io_uring.h>
#include <sys/syscall.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <poll.h>
#include <signal.h>
#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
static int ring;
static unsigned *stail,*smask,*sarray,*chead,*ctail,*cmask;
static struct io_uring_sqe *sqes;
static struct io_uring_cqe *cqes;
static unsigned load(unsigned *p){return __atomic_load_n(p,__ATOMIC_ACQUIRE);}
static void store(unsigned *p,unsigned x){__atomic_store_n(p,x,__ATOMIC_RELEASE);}
static void setup(void){
 struct io_uring_params p={0};ring=syscall(__NR_io_uring_setup,8,&p);assert(ring>=0);
 size_t sl=p.sq_off.array+p.sq_entries*sizeof(unsigned),cl=p.cq_off.cqes+p.cq_entries*sizeof(*cqes);
 void *s=mmap(NULL,(p.features&IORING_FEAT_SINGLE_MMAP)?(sl>cl?sl:cl):sl,PROT_READ|PROT_WRITE,MAP_SHARED,ring,IORING_OFF_SQ_RING);assert(s!=MAP_FAILED);
 void *c=(p.features&IORING_FEAT_SINGLE_MMAP)?s:mmap(NULL,cl,PROT_READ|PROT_WRITE,MAP_SHARED,ring,IORING_OFF_CQ_RING);assert(c!=MAP_FAILED);
 sqes=mmap(NULL,p.sq_entries*sizeof(*sqes),PROT_READ|PROT_WRITE,MAP_SHARED,ring,IORING_OFF_SQES);assert(sqes!=MAP_FAILED);
 stail=s+p.sq_off.tail;smask=s+p.sq_off.ring_mask;sarray=s+p.sq_off.array;
 chead=c+p.cq_off.head;ctail=c+p.cq_off.tail;cmask=c+p.cq_off.ring_mask;cqes=c+p.cq_off.cqes;
}
static struct io_uring_sqe *add(unsigned op,uint64_t id){
 unsigned t=load(stail),n=t&*smask;struct io_uring_sqe *s=&sqes[n];memset(s,0,sizeof(*s));s->opcode=op;s->user_data=id;sarray[n]=n;store(stail,t+1);return s;
}
static void submit(unsigned n){assert(syscall(__NR_io_uring_enter,ring,n,0,0,NULL,0)==(int)n);}
static struct io_uring_cqe take(void){
 while(load(chead)==load(ctail)){int r=syscall(__NR_io_uring_enter,ring,0,1,IORING_ENTER_GETEVENTS,NULL,0);assert(r>=0||errno==EINTR);}
 unsigned h=load(chead);struct io_uring_cqe c=cqes[h&*cmask];store(chead,h+1);return c;
}
static void expect(uint64_t id,int result){struct io_uring_cqe c=take();if(c.user_data!=id||c.res!=result){fprintf(stderr,"CQ id=%llu result=%d expected=%llu/%d\n",(unsigned long long)c.user_data,c.res,(unsigned long long)id,result);exit(1);}}
int main(void){
 alarm(20);setup();
 for(unsigned i=0;i<64;i++){add(IORING_OP_NOP,100+i);submit(1);expect(100+i,0);}
 char path[]="/tmp/odroid-iouring-XXXXXX";int fd=mkstemp(path);assert(fd>=0);char in[4096],out[4096];for(unsigned i=0;i<sizeof(in);i++)in[i]=(char)(i*37u);
 struct io_uring_sqe *s=add(IORING_OP_WRITE,1);s->fd=fd;s->addr=(uintptr_t)in;s->len=sizeof(in);s->flags=IOSQE_IO_LINK;
 s=add(IORING_OP_FSYNC,2);s->fd=fd;submit(2);expect(1,sizeof(in));expect(2,0);
 memset(out,0,sizeof(out));s=add(IORING_OP_READ,3);s->fd=fd;s->addr=(uintptr_t)out;s->len=sizeof(out);submit(1);expect(3,sizeof(out));assert(!memcmp(in,out,sizeof(in)));
 s=add(IORING_OP_OPENAT,4);s->fd=AT_FDCWD;s->addr=(uintptr_t)path;s->open_flags=O_RDONLY;submit(1);struct io_uring_cqe c=take();assert(c.user_data==4&&c.res>=0);int fd2=c.res;
 s=add(IORING_OP_CLOSE,5);s->fd=fd2;submit(1);expect(5,0);
 int pipefd[2];assert(pipe2(pipefd,O_CLOEXEC)==0);s=add(IORING_OP_POLL_ADD,6);s->fd=pipefd[0];s->poll_events=POLLIN;submit(1);
 s=add(IORING_OP_ASYNC_CANCEL,7);s->addr=6;submit(1);c=take();struct io_uring_cqe d=take();assert((c.user_data==6&&c.res==-ECANCELED&&d.user_data==7&&d.res==0)||(d.user_data==6&&d.res==-ECANCELED&&c.user_data==7&&c.res==0));
 pid_t child=fork();assert(child>=0);if(!child){usleep(50000);_exit(7);}siginfo_t info={0};
 s=add(IORING_OP_WAITID,8);s->fd=child;s->len=P_PID;s->file_index=WEXITED;s->addr2=(uintptr_t)&info;submit(1);expect(8,0);assert(info.si_pid==child&&info.si_status==7&&info.si_code==CLD_EXITED);
 close(fd);unlink(path);close(pipefd[0]);close(pipefd[1]);close(ring);
 puts("{\"normal_functionality_passed\":true,\"nop_completions\":64,\"linked_write_fsync\":true,\"read_data_exact\":4096,\"async_open_close\":true,\"poll_cancel\":true,\"child_waitid\":true,\"vulnerability_reproduction\":false}");return 0;
}
