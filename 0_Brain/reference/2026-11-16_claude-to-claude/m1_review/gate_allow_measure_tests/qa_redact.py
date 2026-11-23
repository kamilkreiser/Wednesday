#!/usr/bin/env python3
"""QA-ALLOW-MEASURE: redact my own reproduction captures into the tests folder. Names read from this machine at run
time, never written here. UUIDs -> <ID-n> (consistent across one call), config dir -> <CCD>, home -> <HOME>,
names/hosts -> <NAME>/<HOST>, mail -> <EMAIL>, req_/msg_ ids -> <REQ>/<MSG>, sk-ant/bearer -> <TOKEN>.
usage: qa_redact.py <dst-dir> <src>..."""
import os,re,subprocess,sys
def sh(*a):
    try: return subprocess.run(a,capture_output=True,text=True).stdout.strip()
    except OSError: return ""
HOME=os.path.expanduser("~"); USER=sh("id","-un"); FULL=sh("id","-F"); CFG=os.environ.get("CLAUDE_CONFIG_DIR","")
HOSTS={h for h in (sh("hostname"),sh("hostname","-s"),sh("scutil","--get","ComputerName"),sh("scutil","--get","LocalHostName")) if h}
HOSTS|={h.replace("’","'") for h in HOSTS}
ids={}
def uu(m): k=m.group(0).lower(); ids.setdefault(k,"<ID-%d>"%(len(ids)+1)); return ids[k]
def red(s):
    for p,r in ((CFG,"<CCD>"),(HOME,"<HOME>")):
        if p: s=s.replace(p,r); s=s.replace(re.sub(r"[^A-Za-z0-9]","-",p),r.replace("<","-").replace(">","-"))
    s=re.sub(r"sk-ant-[A-Za-z0-9_-]{8,}","<TOKEN>",s); s=re.sub(r"(?i)bearer\s+[A-Za-z0-9._-]{12,}","<TOKEN>",s)
    s=re.sub(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",uu,s,flags=re.I)
    s=re.sub(r"\breq_[A-Za-z0-9]{8,}","<REQ>",s); s=re.sub(r"\bmsg_[A-Za-z0-9]{8,}","<MSG>",s)
    s=re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}","<EMAIL>",s)
    for h in sorted(HOSTS,key=len,reverse=True): s=re.sub(re.escape(h),"<HOST>",s,flags=re.I)
    for p in sorted({x for x in FULL.split() if len(x)>=3}|{USER},key=len,reverse=True): s=re.sub(re.escape(p),"<NAME>",s,flags=re.I)
    return s
dst=sys.argv[1]; os.makedirs(dst,exist_ok=True)
for src in sys.argv[2:]:
    out=os.path.join(dst,os.path.basename(src))
    open(out,"w",encoding="utf-8").write(red(open(src,encoding="utf-8",errors="replace").read()))
print("redacted %d files into %s; ids mapped %d"%(len(sys.argv)-2,dst,len(ids)))
