import json, sys
P = sys.argv[1]
def load(f): return [json.loads(l) for l in open(f)]
def err(r):
    out = []
    for s in r['logs']:
        if 'handler failed' not in s: continue
        i = s.find('{')
        try: j = json.loads(s[i:]); out.append(json.dumps(j.get('error', '<absent>'))[:40])
        except Exception: out.append('RAW')
    return out
def row(r, left):
    fo = [o for o in r['outcomes'] if not o['ok']]
    e = err(r)
    return f"att={r['attempts']} fail={len(fo)} same={'Y' if fo and all(o['sameAsThrown'] for o in fo) else ('N:'+fo[0]['kind'] if fo else '-')} DL={len(r['deadLetter'])} left={left} lines={len(e)}:{e[0] if e else ''}"
print('== kyc | fail point | value | base | head')
kb, kh = load(P + '/kyc_base.jsonl'), load(P + '/kyc_head.jsonl')
L = lambda r: '/'.join(f"{k[0]}{len(v)}" for k, v in r['subjectLeft'].items()) + ('' if all(r['otherLeft'].values()) else ' OTHER-GONE') + f" ev{r['evicted']}"
for b, h in zip(kb, kh):
    print(f"{b['fail']:20} {b['value']:16} | B {row(b, L(b))} | H {row(h, L(h))}")
for fmt in ('dev', 'prod'):
    print(f'== wallet-connector {fmt}')
    for b, h in zip(load(f'{P}/wc_base_{fmt}.jsonl'), load(f'{P}/wc_head_{fmt}.jsonl')):
        Lw = lambda r: f"s{len(r['subjectSessionsLeft'])}" + ('' if r['otherLeft'] else ' OTHER-GONE')
        print(f"{b['fail']:13} {b['value']:16} | B {row(b, Lw(b))} | H {row(h, Lw(h))}")
