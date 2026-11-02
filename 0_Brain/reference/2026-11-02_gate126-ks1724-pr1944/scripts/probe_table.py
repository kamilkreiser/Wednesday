import json,sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate126-ks1724-pr1944/logs/'
svc=sys.argv[1]
rows={t:[json.loads(l) for l in open(G+f'probe_{svc}_{t}.jsonl')] for t in ('base','repo')}
key=lambda r:(r.get('route'),r['case'],r.get('signed'))
B={key(r):r for r in rows['base']}; H={key(r):r for r in rows['repo']}
def side(r):
    return ' '.join(f'{k}={r[k]}' for k in r if k in ('recorderCalls','tsaCalls','storeDelta','reached'))
for k in [key(r) for r in rows['repo']]:
    b=B.get(k); h=H[k]
    same='SAME' if b and (b['status'],b['body'][:200] if b['status']>=400 else '',side(b))==(h['status'],h['body'][:200] if h['status']>=400 else '',side(h)) else 'DIFF'
    print(f"{same} | {k[0]} | {k[1]}{' signed' if k[2] else ''} | nodes={h.get('nodes')} | base {b['status'] if b else '-'} {side(b) if b else ''} {b['body'][:110] if b else ''} | head {h['status']} {side(h)} {h['body'][:110]} | capLines head={h['capLines']} base={len(b['capLines']) if b else '-'} | ms b/h {b['ms'] if b else '-'}/{h['ms']}")
