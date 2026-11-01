import json
P='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate91-ks1868-pr1909/logs/'
b=json.load(open(P+'probe_base.json')); h=json.load(open(P+'probe_head.json'))
for x,y in zip(b,h):
    print('##',x['cell'])
    for tag,r in (('base',x),('head',y)):
        print(' ',tag,'status',r['status'],'| body',r['body'][:170].replace('\n',' '))
        print('     sql',r['sql'],'chain',r.get('chain'),'unhandled',r['unhandled'])
        for l in r['logs']: print('     log',l['lvl'],l['m'][:70],json.dumps(l['meta'])[:120])
