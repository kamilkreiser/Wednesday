import os, sys, subprocess, time, shutil
sys.dont_write_bytecode=True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
BASE=sys.argv[1]
import importlib.util
spec=importlib.util.spec_from_file_location("ht", os.path.join(os.path.dirname(os.path.abspath(__file__)),"ho_lib.py")); ht=importlib.util.module_from_spec(spec); spec.loader.exec_module(ht)
ht.BASE=BASE
mk,ho,blk,rd,st,ar,body,T=ht.mk,ht.ho,ht.blk,ht.rd,ht.st,ht.ar,ht.body,ht.T
WRAP=os.path.join(os.path.dirname(os.path.abspath(__file__)),"wrap.py")
def eng(root,mode,data,stamp):
    core=os.path.join(root,"2_Project_Files","wake","handover_core.py")
    return subprocess.Popen([sys.executable,WRAP,mode,core,"write","--seat","wednesday","--tasks-dir",T(root),"--stamp",stamp,"--cap","10000"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1"))
# 1. crash between the two renames
root=mk("WEDNESDAY","crash"); ho(root,"write","--stdin",data=blk(b"S0")); ho(root,"write","--stdin",data=blk(b"S1"))
p=eng(root,"crash-before-2nd",blk(b"S2"),"QA-CRASH"); o,e=p.communicate(blk(b"S2"))
a=rd(ar(root)); files=sorted(os.listdir(T(root)))
print("CRASH: engine rc %d (killed by os._exit between the archive rename and the state rename)"%p.returncode)
print("  after the crash: state block is S1 %s; S1 in archive %d time(s); S0 in archive %d; S2 anywhere on disk as state/archive %s; files %s"%(body(root)==blk(b"S1"),a.count(blk(b"S1")),a.count(blk(b"S0")),blk(b"S2") in a or body(root)==blk(b"S2"),files))
rc,o,e=ho(root,"check"); print("  check after crash: rc %d %s"%(rc,o.strip()[:120]))
rc,o,e=ho(root,"write","--stdin",data=blk(b"S3")); a=rd(ar(root))
print("  next normal write rc %d: state S3 %s; archive now holds S1 x%d, S0 x%d (a duplicate, nothing lost)"%(rc,body(root)==blk(b"S3"),a.count(blk(b"S1")),a.count(blk(b"S0"))))
# 2. deterministic interleave: B pauses after its changed-on-disk check, A writes whole, B resumes
root=mk("WEDNESDAY","interleave"); ho(root,"write","--stdin",data=blk(b"S0"))
gate=os.path.join(BASE,"interleave","gate")
pb=eng(root,"barrier:"+gate,blk(b"B"),"QA-B"); pb.stdin.write(blk(b"B")); pb.stdin.close()
while not os.path.exists(gate+".waiting"): time.sleep(0.01)
rcA,oA,eA=ho(root,"write","--stdin",data=blk(b"A"))
open(gate,"w").close(); rcB=pb.wait(); oB=pb.stdout.read().decode(); eB=pb.stderr.read().decode()
a=rd(ar(root)) or b""
print("INTERLEAVE: writer A rc %d (%s); writer B rc %d (%s)"%(rcA,oA.strip().split("\n")[-1],rcB,oB.strip().split("\n")[-1]))
print("  final state is B %s; S0 in archive x%d; A in archive x%d; A is the state %s  => block A %s"%(body(root)==blk(b"B"),a.count(blk(b"S0")),a.count(blk(b"A")),body(root)==blk(b"A"),"LOST (acknowledged 'written', now in neither file)" if a.count(blk(b"A"))==0 and body(root)!=blk(b"A") else "conserved"))
# 3. natural race: two handover.sh writes started together, N trials, big blocks
N=int(sys.argv[2]); lost=0; both_ok=0; refused=0; dup=0
for i in range(N):
    root=mk("WEDNESDAY","race/%03d"%i); ho(root,"write","--stdin",data=blk(b"S0",pad=9000))
    sh=os.path.join(root,"2_Project_Files","wake","handover.sh")
    e=dict(os.environ,PYTHONDONTWRITEBYTECODE="1"); [e.pop(k,None) for k in ("WED_AGENT","HANDOVER_TREE")]
    ps=[subprocess.Popen(["/bin/bash",sh,"write","--stdin"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=e) for _ in (0,1)]
    datas=[blk(b"A%d"%i,pad=9000),blk(b"B%d"%i,pad=9000)]
    for p,d in zip(ps,datas): p.stdin.write(d); p.stdin.close()
    rcs=[p.wait() for p in ps]
    a=rd(ar(root)) or b""; s=body(root)
    acked=[d for d,rc in zip(datas,rcs) if rc==0]
    if len(acked)==2: both_ok+=1
    if any(rc!=0 for rc in rcs): refused+=1
    for d in acked:
        if s!=d and d not in a: lost+=1
    if a.count(blk(b"S0",pad=9000))!=1: dup+=1
print("NATURAL RACE: %d trials of two simultaneous writes: both acknowledged %d; one refused/errored %d; acknowledged block LOST %d; base block not exactly once in archive %d"%(N,both_ok,refused,lost,dup))
