# QA-AUDIT-HOST-NOTES: compare QAHN SF lines of two runs with long hex values (digests, signatures,
# keys, random record content) masked; every other character must match.
import sys, re
def sf(p):
    out=[]
    for l in open(p,errors="replace"):
        i=l.find("QAHN SF ")
        if i>=0: out.append(re.sub(r"[0-9a-f]{16,}","<hex>",l[i:].rstrip("\n")))
    return out
a=sf(sys.argv[1]); b=sf(sys.argv[2])
d=[(x,y) for x,y in zip(a,b) if x!=y]
print(f"SF lines {len(a)} vs {len(b)}; differing after masking: {len(d)}")
for x,y in d[:3]: print("A",x[:400]); print("B",y[:400])
