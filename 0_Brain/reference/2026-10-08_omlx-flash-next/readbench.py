import os,sys,time,fcntl,random
path=sys.argv[1]; F_NOCACHE=48
fd=os.open(path,os.O_RDONLY); fcntl.fcntl(fd,F_NOCACHE,1)
size=os.fstat(fd).st_size
# sequential 1 GiB from a random offset, 16 MiB chunks
start=random.randrange(0,size-2**31)//16384*16384
t=time.time(); n=0
while n<2**30:
    b=os.pread(fd,16*2**20,start+n); n+=len(b)
seq=n/(time.time()-t)/1e9
# 3000 random 16 KiB reads, QD1
offs=[random.randrange(0,size-16384)//16384*16384 for _ in range(3000)]
t=time.time()
for o in offs: os.pread(fd,16384,o)
dt=time.time()-t
# 3000 random 16KiB with 8 threads (QD~8)
from concurrent.futures import ThreadPoolExecutor
offs2=[random.randrange(0,size-16384)//16384*16384 for _ in range(3000)]
t2=time.time()
with ThreadPoolExecutor(8) as ex: list(ex.map(lambda o: os.pread(fd,16384,o),offs2))
dt2=time.time()-t2
print(f"{path}\n  seq read 1 GiB: {seq:.2f} GB/s\n  rand 16KiB QD1: {3000/dt:.0f} IOPS, {dt/3000*1e6:.0f} us avg\n  rand 16KiB 8 threads: {3000/dt2:.0f} IOPS")
