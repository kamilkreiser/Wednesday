#!/usr/bin/env python3
"""Shape of each token / workspace hit (never the value of a name): file, line, length, a masked preview, and the
words before it, so each can be judged by kind (hash, path segment, signature).  usage: qa2_hitshape.py <files...>"""
import os, re, sys
sys.argv_saved=sys.argv; here=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(here,"qa2_scan.py")).read().split('if sys.argv[1]=="selftest":')[0]; exec(src)
for f in sys.argv_saved[1:]:
    s=open(f,"rb").read().decode("utf-8","replace")
    for k in ("token","workspace_path"):
        for rx in C[k]:
            for m in rx.finditer(s):
                ln=s.count("\n",0,m.start())+1; ctx=re.sub(r"\s+"," ",s[max(0,m.start()-40):m.start()])[-40:]
                v=m.group(0); prev=(v[:4]+"…"+v[-4:]) if k=="token" else "<path len %d>"%len(v)
                print("%s %s:%d len=%d %s | before: %r" % (k, f.split("U-B1-hook-allow-silent/")[-1], ln, len(v), prev, ctx if k=="token" else ctx.replace(os.path.expanduser("~"),"<H>")[-25:]))
