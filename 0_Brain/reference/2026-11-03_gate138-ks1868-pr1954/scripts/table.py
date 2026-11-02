import json,sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate138-ks1868-pr1954/logs/'
suf=sys.argv[1] if len(sys.argv)>1 else ''
def load(v): return {(r['route'],r['thrown']):r for r in map(json.loads,open(W+'probe_%s%s.jsonl'%(v,suf)))}
b,h=load('base'),load('head')
def sig(r):
    return dict(s=r['status'],t=r['text'],q=[x['text'][:22]+'/'+str(x['n']) for x in r['queries']],em=r['emitted'],lt=r['logThrew'],u=r['unhandled'],rw=r['redisWrites'],si=r['seedInserts'])
def short(r):
    s=sig(r); return "%s | body=%s | q=%d | log=%s | lt=%d unh=%d rw=%d si=%d"%(s['s'],(s['t'] or '')[:90],len(s['q']),[e[:110] for e in s['em']][:2],s['lt'],s['u'],s['rw'],s['si'])
routes=sorted({k[0] for k in h}); thr=[k[1] for k in h if k[0]==routes[0] and not k[1].startswith('AUTH:')]
out=[]
for r in routes:
    for t in thr:
        B,H=sig(b[(r,t)]),sig(h[(r,t)]); same=B==H
        out.append("%s / %s  %s\n   BASE: %s\n   HEAD: %s"%(r,t,'SAME' if same else 'DIFF',short(b[(r,t)]),short(h[(r,t)])))
open(W+'table%s.log'%suf,'w').write("\n".join(out))
# summary: head vs head ordinary (status/body/queries)
res=[]
for r in routes:
    oh=sig(h[(r,'ordinaryError')]); ob=sig(b[(r,'ordinaryError')])
    res.append("%s: ordinary base==head (all fields): %s"%(r,oh==ob))
    for t in thr:
        B,H=sig(b[(r,t)]),sig(h[(r,t)])
        eq=lambda x,y,f=('s','t','q'):all(x[k]==y[k] for k in f)
        res.append("   %-16s base:%-11s head:%-11s base==head:%-5s head==ordinaryHead(s,t,q):%-5s logThrew b/h %d/%d unh b/h %d/%d"%(t,B['s'],H['s'],B==H,eq(H,oh),B['lt'],H['lt'],B['u'],H['u']))
for r in routes:
    for role in ['null','USER','ORG_ADMIN','SYSTEM_ADMIN']:
        k=(r,'AUTH:'+role); res.append("AUTH %-26s %-12s base=%s head=%s q=%d,%d"%(r,role,b[k]['status'],h[k]['status'],len(b[k]['queries']),len(h[k]['queries'])))
open(W+'judge%s.log'%suf,'w').write("\n".join(res))
