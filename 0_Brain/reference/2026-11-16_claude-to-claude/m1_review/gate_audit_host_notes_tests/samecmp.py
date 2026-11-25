# QA-AUDIT-HOST-NOTES: compare the QAHN SAME lines of two trees (base, head) case by case.
import sys, re
def load(p):
    d={}
    for l in open(p, errors="replace"):
        i=l.find("QAHN SAME ")
        if i<0: continue
        l=l[i+10:].rstrip("\n"); k=l[:2]; d[k]=l
    return d
b=load(sys.argv[1]); h=load(sys.argv[2])
same=diff=0
for k in sorted(set(b)|set(h)):
    if b.get(k)==h.get(k): same+=1; continue
    diff+=1
    print("DIFF", k); print("  base:", b.get(k)); print("  head:", h.get(k))
print(f"cases base {len(b)} head {len(h)}: same {same}, different {diff}")
