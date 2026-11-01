import json,sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900/logs/'
def load(n): return [json.loads(l) for l in open(W+f'probe_{n}.jsonl')]
B,H=load('base'),load('head')
def short(r):
    sql=[s.split(' [')[0].replace('DELETE FROM ','DEL ').replace(' WHERE ',' by ') for s in r.get('sql',[])]
    o=r.get('status',r.get('outcome'))
    extra=f" unhandled={r['unhandled']}" if 'unhandled' in r else (f" thrown={r['thrown']}" if r.get('thrown') else '')
    return f"{o}{extra} | sql={sql} | logger={r.get('logged')} | cascade={[c[:160] for c in r.get('cascadeLog',[])]}"
for b,h in zip(B,H):
    assert (b['probe'],b.get('mode'),b.get('kind'))==(h['probe'],h.get('mode'),h.get('kind'))
    print(f"### {b['probe']} {b.get('mode','')}/{b.get('kind','')}")
    if b['probe']=='handler_captured': print('  base',b,'\n  head',h); continue
    print('  BASE',short(b)); print('  HEAD',short(h))
