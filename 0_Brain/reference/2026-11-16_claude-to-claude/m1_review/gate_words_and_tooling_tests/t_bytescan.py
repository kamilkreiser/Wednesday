#!/usr/bin/env python3
# usage: python3 -B -I t_bytescan.py <added-lines-file> <needle>...   needles come from argv only; regex classes are built in.
import re,sys,urllib.parse
b=open(sys.argv[1],'rb').read(); needles=[n for n in sys.argv[2:] if n]
RX={"uuid":re.compile(rb"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",re.I),"toolu_":re.compile(rb"toolu_"),"req_":re.compile(rb"\breq_[A-Za-z0-9]"),"msg_":re.compile(rb"\bmsg_[A-Za-z0-9]"),
    "mail":re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),"home/vol path":re.compile(rb"/(?:Users|home|Volumes)/[A-Za-z0-9_.-]+")}
forms={"raw":b,"no-backslash":b.replace(b"\\",b""),"url-decoded":urllib.parse.unquote_to_bytes(b),"slug":re.sub(rb"[^A-Za-z0-9]",b"-",b)}
tot=0
for fn,fb in forms.items():
    for n in needles:
        for variant in {n.encode(), re.sub(r"[^A-Za-z0-9]","-",n).encode()}:
            c=len(re.findall(re.escape(variant),fb,re.I))
            if c: print("HIT needle#%d form=%s count=%d"%(needles.index(n),fn,c)); tot+=c
    if fn=="raw":
        for k,rx in RX.items():
            m=rx.findall(fb)
            if m: print("HIT class=%s count=%d sample=%r"%(k,len(m),m[0][:40])); tot+=len(m)
print("TOTAL HITS",tot); sys.exit(1 if tot else 0)
