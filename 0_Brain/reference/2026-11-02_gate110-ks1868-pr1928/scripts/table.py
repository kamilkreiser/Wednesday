import json,sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate110-ks1868-pr1928/logs/'
def load(v): return {(r['route'],r['thrown']):r for r in map(json.loads,open(W+'probe_%s.jsonl'%v))}
b,h=load('base'),load('head')
def sig(r):
    q=[x['text'][:22]+'/'+str(x['n']) for x in r['queries']]
    em=[e[:90] for e in r['emitted']]
    return dict(s=r['status'],t=r['text'],q=q,em=em,lt=r['logThrew'],u=r['unhandled'],rw=r['redisWrites'],si=r['seedInserts'])
def short(r):
    s=sig(r); return "%s | body=%s | q=%d | log=%s | logThrew=%d unh=%d rw=%d seedIns=%d"%(s['s'],(s['t'] or '')[:70],len(s['q']),[e[10:60] if False else e[:70] for e in s['em']][:2],s['lt'],s['u'],s['rw'],s['si'])
out=[]
for k in h:
    if k[1].startswith('AUTH:'): continue
    out.append("%s / %s\n   BASE: %s\n   HEAD: %s"%(k[0],k[1],short(b[k]),short(h[k])))
open(W+'probe_table.log','w').write("\n".join(out))
# judgements
res=[]
routes=sorted({k[0] for k in h})
unread=['revokedProxy','getterThrows']
hostile=['msgRevokedProxy','msgSymbol','msgToStringThrows','msgNullProto','msgPlainObject','undefinedThrown']
def cmp(a,b_,fields=('s','t','q')):
    A,B=sig(a),sig(b_); return all(A[f]==B[f] for f in fields)
for r in routes:
    o_b=b[(r,'ordinaryError')]; o_h=h[(r,'ordinaryError')]
    res.append("%s: ordinary base==head status/body/queries/logs: %s"%(r,cmp(o_b,o_h,('s','t','q','em'))))
    for t in unread+hostile+['ok']:
        hb,hh=b[(r,t)],h[(r,t)]
        res.append("   %-18s base: %-12s head: %-12s head==headOrdinary(status,body,queries)=%s ; head==baseOrdinary=%s ; base==head(all)=%s ; head logThrew=%d unh=%d"%(t,sig(hb)['s'],sig(hh)['s'],cmp(hh,o_h),cmp(hh,o_b),cmp(hb,hh,('s','t','q','em')),sig(hh)['lt'],sig(hh)['u']))
# auth
for r in routes:
    for role in ['None','USER','ORG_ADMIN','SYSTEM_ADMIN']:
        kk=(r,'AUTH:'+('null' if role=='None' else role))
        res.append("AUTH %-26s %-12s base=%s head=%s q(base,head)=%d,%d"%(r,role,b[kk]['status'],h[kk]['status'],len(b[kk]['queries']),len(h[kk]['queries'])))
open(W+'judge.log','w').write("\n".join(res))
