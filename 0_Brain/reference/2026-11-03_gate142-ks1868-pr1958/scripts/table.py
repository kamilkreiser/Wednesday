import json
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate142-ks1868-pr1958/logs/'
rows=[json.loads(l) for l in open(W+'probe_matrix.jsonl')]
d={(r['site'],r['kase'],r['variant']):r for r in rows}
def fmt(r):
    ln=[(l.get('level'),(l.get('message') or l.get('raw') or '')[:34],repr(l.get('error')) if l.get('hasErrorKey') else '<absent>', l.get('status')) for l in r['lines']]
    res=r['result']
    if isinstance(res,dict): res={k:res[k] for k in ('confirmed','polled','errored','blockHash') if k in res}
    return f"{r['outcome']} res={res} calls={r['getTxCalls']}/{r['queryCalls']} unc={r['uncaught']} unh={r['unhandled']} st={r['statuses']} lines={ln}"
nd=0
for key in sorted({(r['site'],r['kase']) for r in rows}):
    b=d[key+('base',)]; h=d[key+('head',)]
    same=fmt(b)==fmt(h); nd+= (not same)
    print(('SAME ' if same else 'DIFF ')+' '.join(key))
    if not same or key[1]=='ordinary':
        print('   base:',fmt(b)); print('   head:',fmt(h))
print('diffs',nd)
