import json,sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate175-ks1868-pr1990-pr1991/results/'
pr=sys.argv[1]
def load(t): return sorted([json.loads(l) for l in open(W+f'p{pr}_{t}.jsonl')], key=lambda r:(r['q'],r['site'],r['value']))
b,h=load('base'),load('head')
assert len(b)==len(h),(len(b),len(h))
out=open(W+f'p{pr}_table.md','w')
out.write('| q | site | value | base | head | same |\n|---|---|---|---|---|---|\n')
nd=0
for x,y in zip(b,h):
    assert x['site']==y['site'] and x['value']==y['value']
    f=lambda r:'; '.join(f'{k}={v}' for k,v in r.items() if k not in('tag','q','site','value'))
    same=f(x)==f(y); nd+= not same
    out.write(f"| {x['q']} | {x['site']} | {x['value']} | {f(x)} | {f(y)} | {'=' if same else 'DIFF'} |\n")
print('cells',len(b),'differ',nd)
