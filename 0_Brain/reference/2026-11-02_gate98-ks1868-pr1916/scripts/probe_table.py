import json,sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate98-ks1868-pr1916/logs/'
b=[json.loads(l) for l in open(G+'probe_base.jsonl')]; h=[json.loads(l) for l in open(G+'probe_head.jsonl')]
def sig(x): return (x['status'], x['text'], json.dumps(x['queries']), x['unhandled'])
for x,y in zip(b,h):
    assert (x['route'],x['thrown'])==(y['route'],y['thrown'])
    same = sig(x)==sig(y)
    print(f"{x['route']:12} {x['thrown']:16} base={x['status']} head={y['status']} q={len(x['queries'])}/{len(y['queries'])} unh={x['unhandled']}/{y['unhandled']} logs_base={[l['meta'] for l in x['logs']]} logs_head={[l['meta'] for l in y['logs']]} {'SAME' if same else 'DIFF'}")
    if x['text'] != y['text'] or x['queries']!=y['queries']: print('   body/q differ', x['text'], y['text'])
