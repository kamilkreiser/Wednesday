import json,re,sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate137-ks1868-pr1955/logs/'
def load(p): return [json.loads(l) for l in open(G+p)]
def errs(r):
    out=[]
    for l in r.get('logs',[]):
        if isinstance(l,dict): l=(l.get('transport') or '')[:4]+':'+(l.get('line') or '')
        m=re.findall(r'"error":("[^"]*"|\{[^}]*\}|null|[^,}]+)',l)
        out.append(('E='+m[0]) if m else ('noerr' if 'lookup' in l or 'anchor' in l.lower() else '')+'')
    return out
def sb(r):
    res=r.get('res') or {}
    b=res.get('body','') or ''
    b=re.sub(r'[0-9a-f]{64}','<H>',b)
    return f"{res.get('status')} {b[:110]}"
print('ANCHORING')
A={s:{(r['cell'],r['kind']):r for r in load(f'probe_anch_{s}.jsonl') if r['cell']!='network'} for s in ('base','head')}
for k in A['head']:
    b,h=A['base'][k],A['head'][k]
    same='SAME' if sb(b)==sb(h) and errs(b)==errs(h) and b['unhandled']==h['unhandled'] else 'DIFF'
    print(f"{k[0]:16} {k[1]:18} {same}\n   base u{b['unhandled']} gr{b.get('getterReads')} {sb(b)} {errs(b)}\n   head u{h['unhandled']} gr{h.get('getterReads')} {sb(h)} {errs(h)}")
for e in ('development','production'):
    print('ORIGINATE',e)
    O={s:{(r['cell'],r['kind']):r for r in load(f'probe_orig_{s}_{e}.jsonl') if r['cell']!='network'} for s in ('base','head')}
    for k in O['head']:
        b,h=O['base'][k],O['head'][k]
        f=lambda r: (sb(r) if 'res' in r else str(r.get('out')))+f" u{r.get('unhandled')} gr{r.get('getterReads')} "+str(errs(r))
        print(f"{k[0]:18} {k[1]:18} {'SAME' if f(b)==f(h) else 'DIFF'}\n   base {f(b)}\n   head {f(h)}")
