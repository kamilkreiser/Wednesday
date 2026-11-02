import json,sys,collections
rows=[json.loads(l) for l in open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate141-ks1868-pr1957/logs/probe_matrix.jsonl')]
d={}
for r in rows: d[(r['svc'],r['site'],r['kase'],r['variant'])]=r
def fmt(r):
    ln=[(l.get('message','')[:12],repr(l.get('error')) if l.get('hasErrorKey') else '<absent>') for l in r['lines']]
    return f"init={r['initDb']}/{r['initDbFlag']} avail={r['isDbAvailable']} unc={r['uncaught']} unh={r['unhandled']} lines={ln}"
for key in sorted({(r['svc'],r['site'],r['kase']) for r in rows}):
    b=d[key+('base',)]; h=d[key+('head',)]
    same = fmt(b)==fmt(h)
    print(('SAME ' if same else 'DIFF ')+' '.join(key))
    if not same or key[2] in('ordinary',):
        print('   base:',fmt(b)); print('   head:',fmt(h))
