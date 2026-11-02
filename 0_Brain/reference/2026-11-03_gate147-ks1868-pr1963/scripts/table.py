import json, sys
P = sys.argv[1]
def load(f): return [json.loads(l) for l in open(f)]
def lg(r):
    out = []
    for s in r['logs']:
        if 'handler failed' not in s: continue
        try:
            j = json.loads(s); out.append('error=' + json.dumps(j.get('error', '<absent>')))
        except Exception:
            i = s.find('{'); 
            try: j = json.loads(s[i:]); out.append('error=' + json.dumps(j.get('error', '<absent>')))
            except Exception: out.append('raw:' + s[-80:])
    return out
print('== kyc (real index.ts dbDeleteUserData + real bus loop)')
kb, kh = load(P + '/kyc_base.jsonl'), load(P + '/kyc_head.jsonl')
for b, h in zip(kb, kh):
    assert (b['fail'], b['value']) == (h['fail'], h['value'])
    for r in (b, h):
        print(f"{r['ver']:4} | {r['fail']:20} | {r['value']:16} | att={r['attempts']} ok={[o['ok'] for o in r['outcomes']].count(True)} same={[o.get('sameAsThrown') for o in r['outcomes'] if not o['ok']][:1]} kind={[o.get('kind') for o in r['outcomes'] if not o['ok']][:1]} | DL={[d['error'] for d in r['deadLetter']]} acked={r['acked']} | left={r['subjectLeft']} other={all(r['otherLeft'].values())} evict={r['evicted']} | stmts={len(r['stmts'])} | failLines={len(lg(r))} {lg(r)[:1]}")
    same = {k: b[k] == h[k] for k in ('attempts', 'deadLetter', 'subjectLeft', 'otherLeft', 'evicted', 'stmts')}
    print('      base==head on', [k for k, v in same.items() if v], ' DIFF on', [k for k, v in same.items() if not v])
for fmt in ('dev', 'prod'):
    print(f'== wallet-connector ({fmt} format, real winston)')
    for b, h in zip(load(f'{P}/wc_base_{fmt}.jsonl'), load(f'{P}/wc_head_{fmt}.jsonl')):
        for r in (b, h):
            print(f"{r['ver']:4} | {r['fail']:13} | {r['value']:16} | att={r['attempts']} ok={[o['ok'] for o in r['outcomes']].count(True)} same={[o.get('sameAsThrown') for o in r['outcomes'] if not o['ok']][:1]} kind={[o.get('kind') for o in r['outcomes'] if not o['ok']][:1]} | DL={[d['error'] for d in r['deadLetter']]} acked={r['acked']} | left={r['subjectSessionsLeft']} other={r['otherLeft']} stmts={r['stmts']} | failLines={len(lg(r))} {lg(r)[:1]}")
