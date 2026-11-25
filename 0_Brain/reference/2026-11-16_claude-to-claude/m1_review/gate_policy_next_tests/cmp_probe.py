# QA-POLICY-NEXT: compare the probe's base and head outputs, masking the fixture pid and input hashes (the hash covers
# paths holding the pid). usage: python3 -B -I cmp_probe.py base.txt head.txt
import sys,re
def rd(p):
    out=[]
    for l in open(p):
        l=re.sub(r'qpx-probe-\d+','qpx-probe-<pid>',l)
        out.append(re.sub(r'sha256:[0-9a-f]{64}','sha256:<h>',l))
    return out
a,b=rd(sys.argv[1]),rd(sys.argv[2])
print("rows base",len(a),"head",len(b),"identical after masking pid+hash:",sum(1 for x,y in zip(a,b) if x==y), "REAL differences:",sum(1 for x,y in zip(a,b) if x!=y))
for x,y in zip(a,b):
    if x!=y: print("REAL\n B",x,"\n H",y)
