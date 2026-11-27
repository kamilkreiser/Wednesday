import os, shutil, subprocess, sys, hashlib, stat, time
sys.dont_write_bytecode=True
LANE="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/wake"; REAL="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files"
BASE=None
def mk(name, sub=""):
    root=os.path.join(BASE, sub, name) if sub else os.path.join(BASE,name)
    for rel in ("tools/seat_note.sh","fleet/cockpit/seat_resolve.sh"):
        d=os.path.join(root,"2_Project_Files",rel); os.makedirs(os.path.dirname(d),exist_ok=True); shutil.copy(os.path.join(REAL,rel),d)
    os.makedirs(os.path.join(root,"2_Project_Files","wake"),exist_ok=True)
    for f in ("handover.sh","handover_core.py"): shutil.copy(os.path.join(LANE,f),os.path.join(root,"2_Project_Files","wake",f))
    os.makedirs(os.path.join(root,"0_Brain","tasks"),exist_ok=True)
    return root
def ho(root,*args,data=b"",env=None):
    e=dict(os.environ)
    for k in ("WED_AGENT","HANDOVER_TREE","HANDOVER_CAP_BYTES","HANDOVER_TEST_BREAK","HANDOVER_TEST_STAMP","HANDOVER_ALLOW_XCLOCK"): e.pop(k,None)
    e["PYTHONDONTWRITEBYTECODE"]="1"; e.update(env or {})
    p=subprocess.run(["/bin/bash",os.path.join(root,"2_Project_Files","wake","handover.sh")]+list(args),input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=e)
    return p.returncode,p.stdout.decode("utf-8","replace"),p.stderr.decode("utf-8","replace")
def blk(tag,pad=0,nl=b"\n",end=True):
    b=nl.join([b"## FLOOR",b"floor "+tag,b"## FIRST WORK",b"first "+tag,b"## OWED",b"owed "+tag,b"## OPEN CARDS",b"cards "+tag,b"## GRANTS IN PLAY",b"grants "+tag+b"x"*0])
    b+= b"y"*pad
    return b+(nl if end else b"")
def rd(p):
    return open(p,"rb").read() if os.path.exists(p) else None
def T(root): return os.path.join(root,"0_Brain","tasks")
def st(root,seat="wednesday"): return os.path.join(T(root),"STATE-%s.md"%seat)
def ar(root,seat="wednesday"): return os.path.join(T(root),"STATE-%s-archive.md"%seat)
def body(root,seat="wednesday"):
    d=rd(st(root,seat)); 
    if d is None: return None
    i=d.find(b"\n---\n",3); return d[i+5:]
def say(tid,ok,msg): print("%s %s :: %s"%("PASS" if ok else "FAIL",tid,msg)); sys.stdout.flush()
def first(s): return (s.strip().split("\n") or [""])[0][:230]

