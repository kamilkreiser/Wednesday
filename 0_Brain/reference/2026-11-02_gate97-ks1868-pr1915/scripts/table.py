import json,sys
P='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate97-ks1868-pr1915/logs/'
b={c['cell']:c for c in json.load(open(P+'probe_base.json'))}
h={c['cell']:c for c in json.load(open(P+'probe_head.json'))}
def s(c): return (c['status'], c['body'][:150], c['fetchCalls'], [(l['lvl'],l['m'],l['meta']) for l in c['logs']], c['unhandled'])
for k in b:
    same = s(b[k])==s(h[k])
    print('##',k,'IDENTICAL' if same else 'DIFFERS')
    print('  base:',s(b[k])); 
    if not same: print('  head:',s(h[k]))
