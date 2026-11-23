#!/usr/bin/env python3
"""QA-ALLOW-MEASURE-R3: independent byte scan of every COMMITTED file of a tree path at a given commit.
Adapted from the r2 check's qa2_scan.py (same classes and five forms), changed to read blobs straight from git
(`git ls-tree -r -z` + `git cat-file blob`), never from a working tree, and with two extra classes:
  volume_path  : any "/Volumes/<name>" spelling (plain, escaped, URL-encoded, slug "-Volumes-<name>")
  tmp_user_dir : "claude-<uid>" scratch-dir spelling (this machine's uid)
Names, mails and paths are read from this machine / env at run time and NEVER printed: a hit prints class, form,
file, count only (use --shape for masked shapes).
Run: python3 -I -B qa3_scan.py selftest
     python3 -I -B qa3_scan.py git <clone> <rev> <pathspec>        (exit 1 on any hit)
     python3 -I -B qa3_scan.py files <file>...                      (positive controls from disk)
     python3 -I -B qa3_scan.py planted <out-file>                   (write a planted BINARY control)
Env: QA_WS="root1|root2|..." workspace roots; QA_MAILS="a,b" owner's mail addresses (never written to disk).
"""
import os, re, subprocess, sys, urllib.parse
sys.dont_write_bytecode = True
def sh(*a):
    try: return subprocess.run(a, capture_output=True, text=True).stdout.strip()
    except OSError: return ""
USER=sh("id","-un"); FULL=sh("id","-F"); HOME=os.path.expanduser("~"); UID=str(os.getuid())
HOSTS={h for h in (sh("hostname"),sh("hostname","-s"),sh("scutil","--get","ComputerName"),sh("scutil","--get","LocalHostName")) if h}
HOSTS|={h.replace("\u2019","'") for h in HOSTS}|{h.split('.')[0] for h in HOSTS}
parts=[p for p in FULL.split() if len(p)>=3]
MAILS=[m for m in os.environ.get("QA_MAILS","").split(",") if m]
CFG=os.environ.get("CLAUDE_CONFIG_DIR","")
WS=[p for p in os.environ.get("QA_WS","").split("|") if p]
E=re.escape
def path_forms(p):
    alt={" ":r"(?:\\ | |%20)","!":r"(?:\\!|!|%21)"}
    yield re.compile("".join(alt.get(c,E(c)) for c in p),re.I)
    yield re.compile(E(re.sub(r"[^A-Za-z0-9]","-",p)),re.I)
C={
 "account_name":([re.compile(E(p),re.I) for p in parts+[USER]]+[re.compile(r"\b"+E(parts[0][:3])+r"\b")]) if parts else [re.compile(E(USER),re.I)],
 "email":[re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")]+[re.compile(E(m),re.I) for m in MAILS],
 "home_path":[re.compile(E(HOME)), re.compile(r"/Users/[A-Za-z0-9._-]+")],
 "machine_name":[re.compile(E(h),re.I) for h in sorted(HOSTS,key=len,reverse=True)],
 "workspace_path":[rx for p in WS+([CFG] if CFG else []) for rx in path_forms(p)],
 "volume_path":[re.compile(r"/Volumes/[^/\s\"'<>]+"), re.compile(r"%2FVolumes%2F",re.I), re.compile(r"-Volumes-[A-Za-z0-9]")],
 "tmp_user_dir":[re.compile(r"claude-"+E(UID)+r"\b")],
 "token":[re.compile(r"sk-ant-[A-Za-z0-9_-]{8,}"),re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{12,}"),re.compile(r"\b[A-Fa-f0-9]{40,}\b"),re.compile(r"\b[A-Za-z0-9+/_-]{48,}={0,2}")],
 "session_uuid":[re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",re.I)],
 "request_id":[re.compile(r"\breq_[A-Za-z0-9]{8,}")],
 "message_id":[re.compile(r"\bmsg_[A-Za-z0-9]{8,}")],
}
ANSI=re.compile(r"\x1b\][^\x07\x1b]*(\x07|\x1b\\)|\x1b\[[0-9;?<>=]*[ -/]*[@-~]|\x1b[()][A-Za-z0-9]|\x1b[=>78DEHMNOc]")
def forms(s):
    a=ANSI.sub("",s)
    return {"asis":s,"noansi":a,"unescaped":s.replace("\\",""),"urldecoded":urllib.parse.unquote(s),"noctl":re.sub(r"[\r\x00-\x08\x0b-\x1f\x7f]","",a)}
def count(s): return {k:sum(len(r.findall(s)) for r in v) for k,v in C.items()}
def scan(name,b):
    s=b.decode("utf-8","replace"); hits={}
    for fn,t in forms(s).items():
        for k,v in count(t).items():
            if v: hits[k]=max(hits.get(k,0),v); hits.setdefault("_forms",set()).add(fn)
    return hits
def shape(name,b):
    s=b.decode("utf-8","replace")
    for t_name,t in forms(s).items():
        if t_name not in ("asis","noctl"): continue
        for k,rxs in C.items():
            for rx in rxs:
                for m in rx.finditer(t):
                    v=m.group(0); ln=t.count("\n",0,m.start())+1
                    pv=(v[:4]+"\u2026"+v[-4:]) if k in ("token","session_uuid","request_id","message_id") else "<%s len %d>"%(k,len(v))
                    ctx=re.sub(r"\s+"," ",t[max(0,m.start()-30):m.start()])[-30:]
                    for w in WS+([CFG] if CFG else [])+[HOME]+parts+[USER]+sorted(HOSTS):
                        if w: ctx=re.sub(E(w),"<X>",ctx,flags=re.I)
                    ctx=re.sub(r"/Volumes/[^/\s]+","/Volumes/<V>",ctx)
                    print("  SHAPE %s form=%s %s:%d %s | before: %r"%(k,t_name,name,ln,pv,ctx))
def git(c,*a): return subprocess.run(["git","-C",c,*a],capture_output=True).stdout
def show(h): return {k:(sorted(v) if k=="_forms" else v) for k,v in h.items()}
a=sys.argv[1:]
if a[0]=="selftest":
    ws=WS[0] if WS else "/nonexistent path!/x"
    esc=subprocess.run(["bash","-c",'printf %q "$1"',"_",ws+"/x"],capture_output=True,text=True).stdout
    planted=" ".join([FULL,USER,"x@example.org",(MAILS[0] if MAILS else "y@example.org"),HOME+"/x",sorted(HOSTS)[0],"sk-ant-abcdefgh12345678","a"*48,
        "123e4567-e89b-12d3-a456-426614174000","req_011ABCDEFGH","msg_01ABCDEFGHIJ","/Volumes/Foo/x","/tmp/claude-"+UID+"/x"])
    c=count(planted); print("planted line, class >=1:",{k:(v>=1) for k,v in c.items() if k!="workspace_path"})
    ok=all(v>=1 for k,v in c.items() if k!="workspace_path")
    arms={"workspace plain":ws+"/x","workspace shell-escaped":esc,"workspace URL-encoded":"file://"+ws.replace(" ","%20").replace("!","%21")+"/x",
          "workspace slug":"-"+re.sub(r"[^A-Za-z0-9]","-",ws)[1:]+"-x","workspace in binary (NUL-framed)":"\x00\x00t"+ws+"/redact.py\x00z"}
    for n,s in arms.items():
        hit=max(count(t)["workspace_path"] for t in forms(s).values()); print("arm %-36s hit=%d"%(n,hit)); ok=ok and hit>=1
    print("WS roots given: %d; config dir set: %s"%(len(WS),bool(CFG))); ok=ok and len(WS)>=1
    neg=count("<RUN>/M8-fresh-ask/cwd <WORKTREE>/x <COAGENT> <CLAUDE_CONFIG_DIR>/projects/-RUN--M8-cwd/<ID-1>.jsonl")
    print("negative control (placeholders only):",{k:v for k,v in neg.items() if v} or "0 in every class"); ok=ok and not any(neg.values())
    print("selftest","PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
if a[0]=="planted":
    ws=WS[0]; b=(b"\xe3\x0d\x0d\x0a\x00\x00\x00\x00\xda"+(ws+"/spikes/x/redact.py").encode()+b"\x00\x00"+FULL.encode()+b"\x00"+sorted(HOSTS)[0].encode()+b"\x00"+HOME.encode()+b"\x00")
    open(a[1],"wb").write(b); print("planted binary written: %d bytes, NUL in it: %s"%(len(b),b"\x00" in b)); sys.exit(0)
SHAPE="--shape" in a; a=[x for x in a if x!="--shape"]
if a[0]=="files":
    tot=0
    for f in a[1:]:
        b=open(f,"rb").read(); h=scan(f,b); print("CONTROL %s binary=%s -> %s"%(os.path.basename(f),b"\x00" in b,show(h))); tot+=bool(h)
        if SHAPE: shape(os.path.basename(f),b)
    sys.exit(0 if tot==len(a)-1 else 1)
if a[0]=="git":
    clone,rev,spec=a[1],a[2],a[3]
    ents=[e for e in git(clone,"ls-tree","-r","-z",rev,"--",spec).split(b"\x00") if e]
    nfiles=0; nbin=0; bad=0; per={}
    for e in ents:
        meta,path=e.split(b"\t",1); mode,typ,oid=meta.split()
        if typ!=b"blob": continue
        b=git(clone,"cat-file","blob",oid.decode()); nfiles+=1; nbin+=(b"\x00" in b)
        h=scan(path.decode(),b)
        if h:
            bad+=1; print("HIT %s %s"%(path.decode(),show(h)))
            for k,v in h.items():
                if k!="_forms": per[k]=per.get(k,0)+v
            if SHAPE: shape(path.decode(),b)
    print("scan of %s:%s : %d committed files (%d binary), files with a hit: %d; per class: %s"%(rev[:10],spec,nfiles,nbin,bad,per or "0 in every class"))
    sys.exit(1 if bad else 0)
