import json,sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate92-ks1868-pr1910/logs/'
b=json.load(open(W+'probe_base.json')); h=json.load(open(W+'probe_head.json'))
print(len(b),len(h))
def s(r): return f"{r['status']} ur={r['unhandled']} log={[l[:90] for l in r['logs']]}"
for x,y in zip(b,h):
    print(f"{x['route']:22} {x['value']:15} BASE {s(x)}\n{'':38} HEAD {s(y)}")
