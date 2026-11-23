#!/usr/bin/env python3
"""QA-ALLOW-MEASURE-R2 item 5: independent names/secrets scan (not the builder's redact.py, not the first check's alone).
Names and paths are read from this machine at run time and NEVER printed: a hit prints class, form, file, count only.
Every file is read as BYTES (binary files too, e.g. .pyc) and scanned in five forms: as is; ANSI/OSC removed;
shell backslashes removed; URL-decoded; control bytes removed. Classes: account name (+ short first name as a word),
email (generic + the owner's addresses from env QA_MAILS), home path and any /Users/<x>, machine names, workspace path
(the project folder, the coordinator folder, the config dir; plain, shell-escaped, URL-encoded and Claude's slug form),
token, session uuid, request id, message id (msg_).   usage: qa2_scan.py selftest | qa2_scan.py scan <files...>"""
import os, re, subprocess, sys, urllib.parse
def sh(*a):
    try: return subprocess.run(a, capture_output=True, text=True).stdout.strip()
    except OSError: return ""
USER=sh("id","-un"); FULL=sh("id","-F"); HOME=os.path.expanduser("~")
HOSTS={h for h in (sh("hostname"),sh("hostname","-s"),sh("scutil","--get","ComputerName"),sh("scutil","--get","LocalHostName")) if h}
HOSTS|={h.replace("’","'") for h in HOSTS}|{h.split('.')[0] for h in HOSTS}
parts=[p for p in FULL.split() if len(p)>=3]
MAILS=[m for m in os.environ.get("QA_MAILS","").split(",") if m]
CFG=os.environ.get("CLAUDE_CONFIG_DIR","")
WS=[p for p in os.environ.get("QA_WS","").split("|") if p]      # workspace roots, passed in, never printed
E=re.escape
def path_forms(p):
    alt={" ":r"(?:\\ | |%20)","!":r"(?:\\!|!|%21)"}
    yield re.compile("".join(alt.get(c,E(c)) for c in p),re.I)
    yield re.compile(E(re.sub(r"[^A-Za-z0-9]","-",p)),re.I)       # Claude Code project-slug form
C={
 "account_name":([re.compile(E(p),re.I) for p in parts+[USER]]+[re.compile(r"\b"+E(parts[0][:3])+r"\b")]) if parts else [],
 "email":[re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")]+[re.compile(E(m),re.I) for m in MAILS],
 "home_path":[re.compile(E(HOME)), re.compile(r"/Users/[A-Za-z0-9._-]+")],
 "machine_name":[re.compile(E(h),re.I) for h in sorted(HOSTS,key=len,reverse=True)],
 "workspace_path":[rx for p in WS+([CFG] if CFG else []) for rx in path_forms(p)],
 "token":[re.compile(r"sk-ant-[A-Za-z0-9_-]{8,}"),re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{12,}"),re.compile(r"\b[A-Fa-f0-9]{40,}\b"),re.compile(r"\b[A-Za-z0-9+/_-]{48,}={0,2}")],
 "session_uuid":[re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",re.I)],
 "request_id":[re.compile(r"\breq_[A-Za-z0-9]{8,}")],
 "message_id":[re.compile(r"\bmsg_[A-Za-z0-9]{8,}")],
}
ANSI=re.compile(r"\x1b\][^\x07\x1b]*(\x07|\x1b\\)|\x1b\[[0-9;?<>=]*[ -/]*[@-~]|\x1b[()][A-Za-z0-9]|\x1b[=>78DEHMNOc]")
def forms(s):
    a=ANSI.sub("",s)
    return {"asis":s,"noansi":a,"unescaped":s.replace("\\",""),"urldecoded":urllib.parse.unquote(s),"noctl":re.sub(r"[\r\x00-\x08\x0b-\x1f]","",a)}
def count(s): return {k:sum(len(r.findall(s)) for r in v) for k,v in C.items()}
def read(f): return open(f,"rb").read().decode("utf-8","replace")
if sys.argv[1]=="selftest":
    ws=WS[0] if WS else "/nonexistent path!/x"
    esc=subprocess.run(["bash","-c",'printf %q "$1"',"_",ws+"/x"],capture_output=True,text=True).stdout
    planted=" ".join([FULL,USER,"x@example.org",(MAILS[0] if MAILS else "y@example.org"),HOME+"/x",sorted(HOSTS)[0],"sk-ant-abcdefgh12345678","a"*48,
        "123e4567-e89b-12d3-a456-426614174000","req_011ABCDEFGH","msg_01ABCDEFGHIJ"])
    c=count(planted); print("planted line, class >=1:",{k:(v>=1) for k,v in c.items() if k!="workspace_path"})
    arms={"workspace plain":ws+"/x","workspace shell-escaped":esc,"workspace URL-encoded":"file://"+ws.replace(" ","%20").replace("!","%21")+"/x",
          "workspace slug":"-"+re.sub(r"[^A-Za-z0-9]","-",ws)[1:]+"-x","workspace in binary (NUL-framed, like a .pyc)":"\x00\x00t"+ws+"/redact.py\x00z"}
    ok=all(v>=1 for k,v in c.items() if k!="workspace_path")
    for n,s in arms.items():
        hit=max(count(t)["workspace_path"] for t in forms(s).values()); print("arm %-46s hit=%d"%(n,hit)); ok=ok and hit>=1
    split="\x1b[1m"+parts[0][:2]+"\x1b[0m"+parts[0][2:]
    hs=count(forms(split)["noansi"])["account_name"]; print("arm name split by an escape (noansi form) hit=%d"%hs); ok=ok and hs>=1
    neg=count("<RUN>/M8-fresh-ask/cwd <WORKTREE>/x <COAGENT> <CLAUDE_CONFIG_DIR>/projects/-RUN--M8-cwd/<ID-1>.jsonl")
    print("negative control (placeholders only):",{k:v for k,v in neg.items() if v} or "0 in every class"); ok=ok and not any(neg.values())
    print("selftest","PASS" if ok else "FAIL")
else:
    tot={}
    for f in sys.argv[2:]:
        s=read(f)
        for fn,t in forms(s).items():
            for k,v in count(t).items():
                if v: tot.setdefault((k,fn),[]).append((f.split("U-B1-hook-allow-silent/")[-1],v))
    print("files scanned:",len(sys.argv)-2)
    for (k,fn),hits in sorted(tot.items()): print("HIT class=%s form=%s files=%d total=%d files: %s"%(k,fn,len(hits),sum(v for _,v in hits),[h[0] for h in hits][:8]))
    if not tot: print("0 hits in every class and form")
