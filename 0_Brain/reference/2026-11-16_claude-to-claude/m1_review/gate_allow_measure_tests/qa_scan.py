#!/usr/bin/env python3
"""QA-ALLOW-MEASURE item 6: independent names/secrets scan (not the builder's redact.py).
Names are read from this machine at run time and never printed: hits print class, file, count only.
Each file is scanned in three forms: as is; with ANSI/OSC escape sequences removed (pane.bytes); with shell
backslash-escapes removed (command.txt). Extra classes over the builder's: API message ids (msg_), the owner's
short first name as a word, the two known mail addresses (read from env QA_MAILS, never printed), long hex/base64 tokens.
usage: qa_scan.py selftest | qa_scan.py scan <files...>"""
import os, re, subprocess, sys
def sh(*a):
    try: return subprocess.run(a, capture_output=True, text=True).stdout.strip()
    except OSError: return ""
USER=sh("id","-un"); FULL=sh("id","-F"); HOME=os.path.expanduser("~")
HOSTS={h for h in (sh("hostname"),sh("hostname","-s"),sh("scutil","--get","ComputerName"),sh("scutil","--get","LocalHostName")) if h}
HOSTS|={h.replace("’","'") for h in HOSTS}|{h.split('.')[0] for h in HOSTS}
parts=[p for p in FULL.split() if len(p)>=3]
MAILS=[m for m in os.environ.get("QA_MAILS","").split(",") if m]
CFG=os.environ.get("CLAUDE_CONFIG_DIR","")
E=re.escape
C={
 "account_name":[re.compile(E(p),re.I) for p in parts+[USER]]+[re.compile(r"\b"+E(parts[0][:3])+r"\b")] if parts else [],
 "email":[re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")]+[re.compile(E(m),re.I) for m in MAILS],
 "home_path":[re.compile(E(HOME)), re.compile(r"/Users/[A-Za-z0-9._-]+")],
 "machine_name":[re.compile(E(h),re.I) for h in sorted(HOSTS,key=len,reverse=True)],
 "config_dir_literal":[re.compile(E(CFG))] if CFG else [],
 "token":[re.compile(r"sk-ant-[A-Za-z0-9_-]{8,}"),re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{12,}"),re.compile(r"\b[A-Fa-f0-9]{40,}\b"),re.compile(r"\b[A-Za-z0-9+/_-]{48,}={0,2}")],
 "session_uuid":[re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",re.I)],
 "request_id":[re.compile(r"\breq_[A-Za-z0-9]{8,}")],
 "message_id":[re.compile(r"\bmsg_[A-Za-z0-9]{8,}")],
}
ANSI=re.compile(r"\x1b\][^\x07\x1b]*(\x07|\x1b\\)|\x1b\[[0-9;?<>=]*[ -/]*[@-~]|\x1b[()][A-Za-z0-9]|\x1b[=>78DEHMNOc]")
def forms(s):
    a=ANSI.sub("",s); b=s.replace("\\","")
    return {"asis":s,"noansi":a,"unescaped":b,"noansi_nocr":re.sub(r"[\r\x00-\x08\x0b-\x1f]","",a)}
def count(s): return {k:sum(len(r.findall(s)) for r in v) for k,v in C.items()}
if sys.argv[1]=="selftest":
    planted=" ".join([FULL,USER,"x@example.org",(MAILS[0] if MAILS else "y@example.org"),HOME+"/x",sorted(HOSTS)[0],CFG+"/x","sk-ant-abcdefgh12345678","a"*48,
        "123e4567-e89b-12d3-a456-426614174000","req_011ABCDEFGH","msg_01ABCDEFGHIJ"])
    split="\x1b[1m"+parts[0][:2]+"\x1b[0m"+parts[0][2:]+" "+HOME.replace("/","\\/")  # name split by an escape; shell-escaped home
    c=count(planted); print("planted per class:",{k:(v>=1) for k,v in c.items()})
    ok=all(v>=1 for v in c.values())
    s=forms(split); print("split-by-escape name: asis account_name=%d, noansi=%d; escaped home: asis=%d unescaped=%d"%(count(s['asis'])['account_name'],count(s['noansi'])['account_name'],count(s['asis'])['home_path'],count(s['unescaped'])['home_path']))
    print("selftest","PASS" if ok and count(s['noansi'])['account_name']>=1 and count(s['unescaped'])['home_path']>=1 else "FAIL")
else:
    tot={}
    for f in sys.argv[2:]:
        s=open(f,encoding="utf-8",errors="replace").read()
        for fn,t in forms(s).items():
            for k,v in count(t).items():
                if v: tot.setdefault((k,fn),[]).append((f.split("/raw/")[-1] if "/raw/" in f else f.split("/")[-1],v))
    print("files scanned:",len(sys.argv)-2)
    for (k,fn),hits in sorted(tot.items()): print("HIT class=%s form=%s files=%d total=%d e.g. %s"%(k,fn,len(hits),sum(v for _,v in hits),hits[:4]))
    if not tot: print("0 hits in every class and form")
