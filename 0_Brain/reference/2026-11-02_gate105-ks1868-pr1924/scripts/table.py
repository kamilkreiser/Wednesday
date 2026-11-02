import json,sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate105-ks1868-pr1924/logs/'
def load(n): return {(r['route'],r['fault'],r['v']):r for r in map(json.loads,open(W+n))}
B=load(sys.argv[1] if len(sys.argv)>1 else 'probe_base.jsonl'); H=load(sys.argv[2] if len(sys.argv)>2 else 'probe_head.jsonl')
ok=diff=0; notes=[]
def chk(cond,msg):
    global ok,diff
    if cond: ok+=1
    else: diff+=1; notes.append('DIFF '+msg)
KNOWN={('recertify','anchor fetch rejects')}
CMP=['status','body','state','sql','anchorCalls','notifies','disposition']
assert set(B)==set(H)
for k,h in H.items():
    route,fault,v=k; b=B[k]
    chk(h['status']!='NO ANSWER', f'{k} head NO ANSWER')
    chk(h['fired'] in (True,None), f'{k} fault did not fire')
    if v in ('ord','str','none'):
        for f in CMP+['routeErr','allLogs']: chk(b[f]==h[f], f'{k} base!=head {f}')
    else:
        o=H[(route,fault,'ord')]
        if (route,fault) in KNOWN:
            for f in CMP: chk(b[f]==h[f], f'{k} known-divergence base!=head {f}')
            notes.append(f'KNOWN {k}: head {h["status"]} state={h["state"]["documents"]} vs ord {o["status"]} {o["state"]["documents"]} (base identical)')
            continue
        for f in CMP: chk(h[f]==o[f], f'{k} head-unreadable != head-ord {f}')
        chk(len(h['routeErr'])==len(o['routeErr'])<=1, f'{k} route error lines {len(h["routeErr"])}')
        e=h['routeErr'][0]['error'] if h['routeErr'] else None
        chk(e is None and not o['routeErr'] or e in ('unreadable thrown value',"Cannot perform 'get' on a proxy that has been revoked","Cannot perform 'getPrototypeOf' on a proxy that has been revoked",'g105 message getter threw'), f'{k} reason {e}')
        chk(b['state']==h['state'], f'{k} base state != head state')
        if b['status']!='NO ANSWER':
            for f in CMP+['routeErr']: chk(b[f]==h[f], f'{k} base answered but differs {f}')
    # ks1346: unreadable route error lines carry no value
    for l in h['routeErr']:
        s=json.dumps(l)
        for bad in ['HOLDER','G105 certificate','HOLDERSECRET','example.test','g105 note','score']:
            chk(bad not in s, f'{k} route error line carries {bad}')
nb=sum(1 for r in B.values() if r['status']=='NO ANSWER'); nh=sum(1 for r in H.values() if r['status']=='NO ANSWER')
print(f'cells {len(H)}; base NO ANSWER {nb}; head NO ANSWER {nh}')
cons=sum(1 for r in H.values() if r['v'] in('rp','tg') and r['routeErr'] and r['routeErr'][0]['error']=='unreadable thrown value')
print(f'head unreadable cells logging the constant: {cons} of {sum(1 for r in H.values() if r["v"] in("rp","tg"))}')
for n in notes: print(n)
print(f'{ok} OK, {diff} DIFF')
