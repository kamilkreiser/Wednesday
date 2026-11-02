import json,collections
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate138-ks1868-pr1954/logs/'
L=lambda v:{(r['route'],r['thrown']):r for r in map(json.loads,open(W+'probe_%s.jsonl'%v))}
b,h=L('base'),L('head')
q=lambda r:[(x['text'],x['n']) for x in r['queries']]
core=lambda r:(r['status'],q(r),r['redisWrites'],r['seedInserts'],r['logThrew'],r['unhandled'])
routes=sorted({k[0] for k in h})
thr=[k[1] for k in h if k[0]==routes[0] and not k[1].startswith('AUTH:')]
# 1. auth identical
bad=[k for k in h if k[1].startswith('AUTH:') and (b[k]['status'],len(b[k]['queries']))!=(h[k]['status'],len(h[k]['queries']))]
print('AUTH cells',sum(1 for k in h if k[1].startswith('AUTH:')),'differing base/head:',len(bad))
# 2. For every thrown value: head core == head ordinary core? (ordinary Error row)
BODYCONST={'POST org','PUT org','DELETE org','GET audit export','PATCH identity level'}
for r in routes:
    oh=h[(r,'ordinaryError')]; ob=b[(r,'ordinaryError')]
    diffs=[]
    for t in thr:
        if t in('ok','ordinaryError'): continue
        x=h[(r,t)]; d=[]
        if core(x)!=core(oh): d.append('core')
        if r in BODYCONST and x['text']!=oh['text']: d.append('body')
        if r in('GET identity users (seed)','GET identity orgs (seed)') and x['text']!=oh['text']: d.append('body')
        if d: diffs.append((t,d))
    print('%-26s ordinary base==head core:%s | head rows whose core/body != head ordinary: %s'%(r,core(ob)==core(oh),diffs))
# 3. rows where base!=ordinary base (defects at base) 
print('--- base rows deviating from base-ordinary (core) / head rows deviating from head-ordinary (core), counts')
for r in routes:
    nb=[t for t in thr if t not in('ok','ordinaryError') and core(b[(r,t)])!=core(b[(r,'ordinaryError')])]
    nh=[t for t in thr if t not in('ok','ordinaryError') and core(h[(r,t)])!=core(h[(r,'ordinaryError')])]
    print('%-26s base:%s | head:%s'%(r,nb,nh))
# 4. persisted state: any thrown row where queries at head != base
pd=[(k) for k in h if not k[1].startswith('AUTH:') and q(h[k])!=q(b[k])]
print('rows where statements issued differ base vs head:',pd)
rw=[k for k in h if h[k]['redisWrites']!=b[k]['redisWrites'] or h[k]['seedInserts']!=b[k]['seedInserts']]
print('rows where redis writes / seed inserts differ:',rw)
