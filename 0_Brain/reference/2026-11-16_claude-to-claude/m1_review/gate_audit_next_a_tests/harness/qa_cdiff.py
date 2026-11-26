# compare qa_an.py runs: base1 base2 -- head1 head2; volatile = differs between the two runs of one build
import json, re, sys
a = sys.argv[1:]; i = a.index("--"); B, H = a[:i], a[i+1:]
def load(p):
    d = {}
    for l in open(p):
        r = json.loads(l); d.setdefault((r["case"], r["step"]), []).append(r["v"])
    return d
def norm(v, dig=False):
    s = json.dumps(v, sort_keys=True)
    s = re.sub(r"[0-9a-f]{16,}", "<hex>", s)
    if dig: s = re.sub(r"\d+", "<n>", s)
    return s
b = [load(p) for p in B]; h = [load(p) for p in H]
keys = list(dict.fromkeys(list(b[0]) + list(h[0])))
diff = 0; vol = []
for k in keys:
    bv = [x.get(k) for x in b]; hv = [x.get(k) for x in h]
    v = len({norm(x) for x in bv}) > 1 or len({norm(x) for x in hv}) > 1
    if v: vol.append(k)
    if norm(bv[0], v) != norm(hv[0], v):
        diff += 1
        print(f"DIFF {k}\n  base: {norm(bv[0], v)[:420]}\n  head: {norm(hv[0], v)[:420]}")
print("VOLATILE:", vol)
print(f"keys {len(keys)}, different {diff}")
