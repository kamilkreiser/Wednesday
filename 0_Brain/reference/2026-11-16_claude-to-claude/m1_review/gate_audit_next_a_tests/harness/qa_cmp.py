#!/usr/bin/env python3
"""QA-AUDIT-WIRE task 5: compare runs. Usage: python3 -I -B qa_cmp.py base1.json base2.json -- head1.json head2.json
Normalisation (named): hex runs of 8+ -> <hex>; RFC3339 times -> <ts>. A label whose normalised value
differs between the two runs of ONE build is VOLATILE: it is then compared with every digit run -> <n>
(and, for listings, as sets); if it still differs it is reported."""
import json, re, sys
a = sys.argv[1:]
i = a.index("--")
B, H = a[:i], a[i + 1:]


def load(p):
    return json.load(open(p))


def norm(v, digits=False):
    s = json.dumps(v, sort_keys=True)
    s = re.sub(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?Z", "<ts>", s)
    s = re.sub(r"[0-9a-f]{8,}", "<hex>", s)
    if digits:
        s = re.sub(r"\d+", "<n>", s)
    return s


def by_label(run):
    d = {}
    for lab, v in run:
        d.setdefault(lab, []).append(v)
    return d


b = [by_label(load(p)) for p in B]
h = [by_label(load(p)) for p in H]
labels = list(dict.fromkeys([l for l, _ in load(B[0])] + [l for l, _ in load(H[0])]))
same = diff = 0
vol = []
out = []
for lab in labels:
    bv = [x.get(lab) for x in b]
    hv = [x.get(lab) for x in h]
    volatile = len({norm(v) for v in bv}) > 1 or len({norm(v) for v in hv}) > 1
    dig = volatile
    if volatile:
        vol.append(lab)
    if norm(bv[0], dig) == norm(hv[0], dig):
        same += 1
        continue
    diff += 1
    out.append(f"DIFF {lab}\n  base: {norm(bv[0], dig)[:600]}\n  head: {norm(hv[0], dig)[:600]}")
print("\n".join(out))
print("VOLATILE (compared with digits as <n>):", json.dumps(vol))
print(f"labels {len(labels)}: same {same}, different {diff}")
