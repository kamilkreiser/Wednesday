# QA harness: evaluates the launcher's prompt region for a seat WITHOUT running the launcher.
# It takes, from the ORIGINAL and from the PATCHED scratch copy: the seat-file mapping block, (patched only) hunk A,
# the SEAT_LEDGER case, and the INITIAL_PROMPT assignment up to the line before `clear` (which, patched, includes hunk B).
# Everything else the prompt expands is stubbed with a sentinel. python3 is a shell function stub; the backtick pair in
# step 5 runs a STUB note_entry.sh in a scratch cwd (never the real one).
import os, re, subprocess, sys, hashlib
D=os.path.dirname(os.path.abspath(__file__))
def region(path):
    L=open(path,encoding="utf-8").read().split("\n")
    def find(pred,start=0):
        for i in range(start,len(L)):
            if pred(L[i]): return i
        raise SystemExit("anchor not found in "+path)
    # seat-file mapping: from the first 'PICKUP_FILE=' back to its 'if', forward to 'fi'
    p=find(lambda l:"PICKUP_FILE=" in l); a=p
    while not L[a].startswith("if "): a-=1
    b=find(lambda l:l=="fi",p)
    seatmap=L[a:b+1]
    hunkA=[]
    if any(l.startswith("# --- Wake pack (WED-170") for l in L):
        s=find(lambda l:l.startswith("# --- Wake pack (WED-170")); e=find(lambda l:l=="fi",s)
        hunkA=L[s:e+1]
    c=find(lambda l:l.startswith('SEAT_HOST="$(hostname')); ce=find(lambda l:l=="esac",c)
    ledger=L[c:ce+1]
    ps=find(lambda l:l.startswith('INITIAL_PROMPT="ultrathink')); pe=find(lambda l:l=="clear",ps)
    return seatmap,hunkA,ledger,L[ps:pe]
def harness(path,seat,py_rc,py_out,write_pack,wake_py_exists=True,extra_pre=""):
    seatmap,hunkA,ledger,prompt=region(path)
    used=set(re.findall(r"\$\{?([A-Za-z_][A-Za-z0-9_]*)",("\n".join(seatmap+hunkA+ledger+prompt))))
    assigned=set(re.findall(r"^\s*([A-Za-z_][A-Za-z0-9_]*)=",("\n".join(seatmap+hunkA+ledger+prompt)),re.M))|set(re.findall(r"[;)] *([A-Z_][A-Z0-9_]*)=",("\n".join(seatmap+hunkA+ledger+prompt))))
    root=os.path.join(D,"run2_%s"%seat); tag=os.path.basename(path).split(".")[0]; os.makedirs(os.path.join(root,"2_Project_Files/tools"),exist_ok=True); os.makedirs(os.path.join(root,"2_Project_Files/wake"),exist_ok=True); os.makedirs(os.path.join(root,"0_Brain/wake"),exist_ok=True)
    open(os.path.join(root,"2_Project_Files/tools/note_entry.sh"),"w").write("#!/bin/bash\necho STUB-NOTE-ENTRY-WHERE\n")
    wpy=os.path.join(root,"2_Project_Files/wake/wake_pack.py")
    if wake_py_exists: open(wpy,"w").write("# stub\n")
    elif os.path.exists(wpy): os.rename(wpy,wpy+".gone_qa")
    pk=os.path.join(root,"0_Brain/wake/WAKE-%s.md"%seat)
    if os.path.exists(pk): os.rename(pk,pk+".gone_qa.%d"%len(os.listdir(os.path.dirname(pk))))
    pre=["set -u","AGENT=%s"%seat,"AGENT_UPPER=%s"%seat.upper(),'PROJECT_DIR="%s"'%root,'BRAIN_DIR="$PROJECT_DIR/0_Brain"']
    for v in sorted(used-assigned-{"AGENT","AGENT_UPPER","PROJECT_DIR","BRAIN_DIR","BASH_SOURCE","WAKE_PACK_OK"}):
        pre.append("%s='<<%s>>'"%(v,v))
    pre.append("python3() { printf '%%s\\n' \"called: python3 $*\" >> \"%s/python3_calls.txt\"; %s printf '%%s\\n' %s; return %d; }"%(root,("printf 'PACK\\n' > \"%s\";"%pk) if write_pack else "",shq(py_out),py_rc))
    pre.append("hostname() { echo stubhost; }")
    if extra_pre: pre.append(extra_pre)
    body="\n".join(pre+seatmap+hunkA+ledger+prompt)+"\nprintf '%s' \"$INITIAL_PROMPT\" > \"$QA_OUT\"\n"
    hp=os.path.join(root,"harness_%s.sh"%tag); open(hp,"w").write(body)
    out=os.path.join(root,"prompt.txt")
    if os.path.exists(out): os.rename(out,out+".prev.%d"%len(os.listdir(root)))
    calls=os.path.join(root,"python3_calls.txt")
    if os.path.exists(calls): os.rename(calls,calls+".prev.%d"%len(os.listdir(root)))
    p=subprocess.run(["/bin/bash",hp],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={"PATH":"/usr/bin:/bin","QA_OUT":out,"HOME":root})
    prm=open(out,"rb").read() if os.path.exists(out) else None
    return p.returncode,p.stdout.decode("utf-8","replace"),p.stderr.decode("utf-8","replace"),prm,root,(open(calls).read() if os.path.exists(calls) else "")
def shq(s): return "'"+s.replace("'","'\\''")+"'"
def h(b): return hashlib.sha256(b).hexdigest()[:16] if b is not None else "NONE"
ORIG=os.path.join(D,"orig.command"); PAT=os.path.join(D,"patched.command")
SUMMARY="/x/0_Brain/wake/WAKE-wednesday.md  bytes: 61206  ~tokens: 15302 of 60000  state: legacy pickup, first block only  grants kept 22 of 76 (12 unclassified)  dropped rows listed in WAKE-wednesday.dropped.txt  ledger rows: 19"
print("## A. other seats: prompt bytes, original vs patched (python3 stub would succeed if called)")
for seat in ("tuesday","friday"):
    rc0,o0,e0,p0,_,c0=harness(ORIG,seat,0,SUMMARY,True)
    rc1,o1,e1,p1,root,c1=harness(PAT,seat,0,SUMMARY,True)
    print("%s: original rc %d, %d bytes, sha %s | patched rc %d, %d bytes, sha %s | BYTE-IDENTICAL %s | harness stdout identical %s (patched stdout: %r) | stderr orig %r patched %r | python3 called by the patched region: %r | pack file created: %s"%(
        seat,rc0,len(p0 or b""),h(p0),rc1,len(p1 or b""),h(p1),p0==p1 and p0 is not None,o0==o1,o1[:80],e0[:120],e1[:120],c1.strip(),os.path.exists(os.path.join(root,"0_Brain/wake/WAKE-%s.md"%seat))))
    print("   control: the prompt carries the seat's own files: %s"%( [x for x in (b"NEXT-PICKUP-TUESDAY",b"NEXT-PICKUP-FRIDAY",b"_ledger_laptop_datasec",b"_ledger_friday") if x in (p0 or b"")] ))
print("## B. wednesday: original prompt, then each build outcome on the patched copy")
rc0,o0,e0,pw,_,_=harness(ORIG,"wednesday",0,SUMMARY,True); print("original wednesday prompt: rc %d, %d bytes, sha %s; stderr %r"%(rc0,len(pw),h(pw),e0[:100]))
def case(label,**kw):
    rc,o,e,p,root,calls=harness(PAT,"wednesday",**kw)
    kind="LEGACY (byte-identical to the original)" if p==pw else ("WAKE-PACK prompt" if p and b"WAKE PACK boot" in p else "OTHER")
    print("- %s: rc %d; prompt %d bytes sha %s -> %s; names the pack path %s; says anything about the failure IN THE PROMPT %s\n    stdout: %s\n    stderr: %r"%(label,rc,len(p or b""),h(p),kind,(b"WAKE-wednesday.md" in (p or b"")),bool(p and re.search(rb"did not build|legacy read list|over budget|OVER BUDGET",p)),o.strip().replace("\n"," / ")[:330],e[:160]))
    return p,root
pn,rootn=case("build OK (rc 0, pack written)",py_rc=0,py_out=SUMMARY,write_pack=True)
case("build OVER BUDGET (rc 3)",py_rc=3,py_out="wake_pack: OVER BUDGET — nothing written. The pack would be 300000 bytes",write_pack=False)
case("build crashes (rc 1, traceback)",py_rc=1,py_out="Traceback (most recent call last):\nPermissionError: [Errno 13]",write_pack=False)
case("required source missing (rc 2)",py_rc=2,py_out="wake_pack: REFUSED — required source missing",write_pack=False)
case("wake_pack.py missing",py_rc=0,py_out=SUMMARY,write_pack=False,wake_py_exists=False)
case("rc 0 but NO pack file on disk (deleted or never written)",py_rc=0,py_out=SUMMARY,write_pack=False)
case("rc 0 with EMPTY output",py_rc=0,py_out="",write_pack=True)
case("python3 not found (rc 127)",py_rc=127,py_out="bash: python3: command not found",write_pack=False)
hostile="x  bytes: 1 `touch \"$PROJECT_DIR/PWNED_BACKTICK\"` $(touch \"$PROJECT_DIR/PWNED_DOLLAR\") \"; touch \"$PROJECT_DIR/PWNED_QUOTE\"; echo \" ${PROJECT_DIR} \\$(id)"
ph,rooth=case("rc 0 with a HOSTILE summary line (backticks, $( ), quotes)",py_rc=0,py_out=hostile,write_pack=True)
print("    files named PWNED* created by the hostile summary: %s ; the text arrived literally in the prompt: %s"%([f for f in os.listdir(rooth) if f.startswith("PWNED")], b"`touch" in ph and b"$(touch" in ph))
# marker drift: edit a copy of the patched launcher
s=open(PAT,encoding="utf-8").read(); assert s.count("FIRST ACTIONS (token cost is accepted — do the full reads")==1
DR=os.path.join(D,"patched_drift.command"); open(DR,"w",encoding="utf-8").write(s.replace("FIRST ACTIONS (token cost is accepted — do the full reads","FIRST ACTIONS (the token cost is accepted — do the full reads"))
rc,o,e,p,_,_=harness(DR,"wednesday",0,SUMMARY,True); s2=open(DR,encoding="utf-8").read()
print("- marker M1 reworded in the legacy text: rc %d; prompt is the (reworded) legacy text %s; contains 'WAKE PACK boot' %s\n    stdout: %s"%(rc,p is not None and b"the token cost is accepted" in p,b"WAKE PACK boot" in p,o.strip().replace("\n"," / ")[:300]))
open(os.path.join(D,"prompt_wednesday_new.txt"),"wb").write(pn); open(os.path.join(D,"prompt_wednesday_legacy.txt"),"wb").write(pw)
print("## C. the new wednesday prompt against the legacy one")
i=pn.find(b"FIRST ACTIONS"); j=pw.find(b"FIRST ACTIONS"); print("head before FIRST ACTIONS identical: %s (%d bytes)"%(pn[:i]==pw[:j],i))
k=pn.find(b"\n5. Read yesterday's and today's notes"); m=pw.find(b"\n5. Read yesterday's and today's notes"); print("tail from step 5 identical: %s (%d bytes)"%(pn[k:]==pw[m:],len(pn)-k))
print("middle (steps 1 to 4): legacy %d bytes -> new %d bytes"%(m-j,k-i))
print("unexpanded sentinel check: every <<VAR>> in the new middle: %s"%sorted(set(re.findall(rb"<<([A-Z_]+)>>",pn[i:k]))))
print("backticks in the new middle: %d ; '$(' in the new middle: %d ; STUB-NOTE-ENTRY-WHERE occurrences new/legacy: %d/%d (the legacy backtick pair, unchanged, ran the STUB)"%(pn[i:k].count(b"`"),pn[i:k].count(b"$("),pn.count(b"STUB-NOTE-ENTRY-WHERE"),pw.count(b"STUB-NOTE-ENTRY-WHERE")))
