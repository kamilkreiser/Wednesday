import os,sys,subprocess,shutil,re,collections
sys.dont_write_bytecode=True
D=os.path.dirname(os.path.abspath(__file__)); BASE=sys.argv[1]
import importlib.util
spec=importlib.util.spec_from_file_location("ht", os.path.join(D,"ho_lib.py")); ht=importlib.util.module_from_spec(spec); spec.loader.exec_module(ht); ht.BASE=BASE
mk,ho,blk,rd,st,ar,body,T=ht.mk,ht.ho,ht.blk,ht.rd,ht.st,ht.ar,ht.body,ht.T
print("## a. why one writer is refused in the natural race (40 trials, stderr of the refused writer)")
c=collections.Counter(); lost=0
for i in range(40):
    root=mk("WEDNESDAY","race2/%03d"%i); ho(root,"write","--stdin",data=blk(b"S0",pad=9000))
    sh=os.path.join(root,"2_Project_Files","wake","handover.sh"); e=dict(os.environ,PYTHONDONTWRITEBYTECODE="1"); [e.pop(k,None) for k in ("WED_AGENT","HANDOVER_TREE")]
    ps=[subprocess.Popen(["/bin/bash",sh,"write","--stdin"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=e) for _ in (0,1)]
    datas=[blk(b"A%d"%i,pad=9000),blk(b"B%d"%i,pad=9000)]
    for p,d in zip(ps,datas): p.stdin.write(d); p.stdin.close()
    for p,d in zip(ps,datas):
        rc=p.wait(); err=p.stderr.read().decode("utf-8","replace")
        if rc: c[(rc,re.sub(r"/\S+","<path>",err.strip().split("\n")[0])[:150])]+=1
        else:
            a=rd(ar(root)) or b""
    a=rd(ar(root)) or b""; s=body(root)
    for p,d in zip(ps,datas):
        if p.returncode==0 and s!=d and d not in a: lost+=1
    left=[f for f in os.listdir(T(root)) if ".tmp." in f]
    if left: c[("temp files left",len(left))]+=1
for k,v in c.items(): print("  %d x %s"%(v,k))
print("  acknowledged blocks lost in these 40 trials: %d"%lost)
print("## e. seed --run on a scratch WEDNESDAY tree holding a COPY of the real legacy pickup")
root=mk("WEDNESDAY","seedrun"); shutil.copy("/Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/NEXT-PICKUP.md",os.path.join(T(root),"NEXT-PICKUP.md"))
import hashlib
h0=hashlib.sha256(rd(os.path.join(T(root),"NEXT-PICKUP.md"))).hexdigest()
rc,o,e=ho(root,"seed","--from-legacy","--run"); print("  seed --run rc %d | %s"%(rc,o.strip().split("\n")[-1][:120]))
rc2,o2,e2=ho(root,"check"); print("  check rc %d | %s"%(rc2,o2.strip()[:120]))
rc3,o3,e3=ho(root,"seed","--from-legacy","--run"); print("  second seed --run rc %d | %s"%(rc3,e3.strip()[:110]))
print("  legacy copy unchanged: %s; files: %s"%(hashlib.sha256(rd(os.path.join(T(root),"NEXT-PICKUP.md"))).hexdigest()==h0,sorted(os.listdir(T(root)))))
leg=rd(os.path.join(T(root),"NEXT-PICKUP.md")).decode().split("\n"); b=body(root).decode()
i1=[i for i,l in enumerate(leg) if l.startswith("## OWED")]; i2=[i for i,l in enumerate(leg) if l.startswith("## STANDING")]
tail=[l for l in leg[i1[0]:] if l.strip() and not l.startswith("## ")] if i1 else []
print("  legacy file-level sections '## OWED' at line %s and '## STANDING' at line %s: %d non-blank body lines, %d bytes; of those lines present in the seeded STATE block: %d; the seed report mentions them: %s"%([x+1 for x in i1],[x+1 for x in i2],len(tail),len("\n".join(tail).encode()),sum(1 for l in tail if l in b),("STANDING" in o+e)))
