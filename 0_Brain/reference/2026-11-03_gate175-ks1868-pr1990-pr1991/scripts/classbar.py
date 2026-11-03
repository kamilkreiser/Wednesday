# For each site: reference = base outcome for V01 (ordinary Error), sentinel count and value-specific text excluded.
import json,sys,re,collections
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate175-ks1868-pr1990-pr1991/results/'
pr=sys.argv[1]
def load(t): return sorted([json.loads(l) for l in open(W+f'p{pr}_{t}.jsonl')], key=lambda r:(r['q'],r['site'],r['value']))
b,h=load('base'),load('head')
IGN=('tag','q','site','value','sentinelLines','body','bodyHasSentinel','logged')
def key(r):
    d={k:v for k,v in r.items() if k not in IGN}
    s=json.dumps(d,sort_keys=True)
    s=re.sub(r'err0=[^"]*','err0=<text>',s)  # recorded error text carries the value
    return s
ref={}
for r in b:
    if r['value'].startswith('V01'): ref[(r['q'],r['site'])]=key(r)
by=collections.defaultdict(list)
tot=eqo=0; chg=0
lines=[]
for x,y in zip(b,h):
    s=(x['q'],x['site'])
    if x['value'].startswith('V01'): continue
    tot+=1
    he=key(y)==ref[s]; be=key(x)==ref[s]; changed=key(x)!=key(y)
    eqo+=he; chg+=changed
    tag=('head=ORD' if he else 'head!=ORD')+(' base=ORD' if be else ' base!=ORD')+(' CHANGED' if changed else '')
    by[s].append((x['value'][:3],tag))
    if not he: lines.append(f"  head!=base-ordinary: {s[1]} {x['value']} :: base={key(x)} head={key(y)} ref={ref[s]}")
for s,v in by.items():
    c=collections.Counter(t for _,t in v)
    print(s[0],s[1],dict(c))
print(f'TOTAL non-ordinary cells {tot}; head equals base-ordinary {eqo}; base->head changed {chg}')
print('\n'.join(lines))
