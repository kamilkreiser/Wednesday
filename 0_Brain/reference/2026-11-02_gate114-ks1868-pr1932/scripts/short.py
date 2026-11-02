import json,re,sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate114-ks1868-pr1932/logs/'
def load(p): return [json.loads(l) for l in open(G+p)]
def resp(r):
    res=r.get('res') or {}
    st=res.get('status'); b=res.get('body','')
    try:
        j=json.loads(b)
        if 'verified' in j: v=f"verified={j['verified']} src={j.get('source')} {('reason='+j.get('reason','')[:28]) if j.get('reason') else ''}{(' err='+str(j.get('error'))[:30]+' details='+str(j.get('details'))[:50]) if 'details' in j else ''}"
        elif 'data' in j: v=f"data.verified={j['data'].get('verified')}"
        elif 'error' in j: v=f"err={j['error'].get('code') if isinstance(j['error'],dict) else j['error']}"
        else: v=b[:60]
    except Exception: v=(b or res.get('err',''))[:60]
    return f"{st} {v}"
print('ANCHORING (stage | cell | kind | response | writes submits unhandled | log errors)')
for st in ['base','head']:
    for r in load(f'probe_anch_{st}.jsonl'):
        if r['cell']=='network': print(st,'NETWORK',json.dumps({k:r[k] for k in ('outbound','fetchUrls','connects')})[:400]); continue
        le=[]
        for l in r['logs']:
            m=re.search(r'"message":"([^"]+)".*?"error":("[^"]*"|\{\}|null)',l)
            le.append(f"{m.group(1)[:30]}:{m.group(2)[:40]}" if m else l[:90])
        print(st,'|',r['cell'],'|',r['kind'],'|',resp(r),'|',len(r['writes']),r['submits'],r['unhandled'],r.get('uncaught'),'|',' ; '.join(le))
print()
print('ORIGINATE')
for st in ['base','head']:
  for e in ['test','production']:
    for r in load(f'probe_orig_{st}_{e}.jsonl'):
        if r['cell']=='network': print(st,e,'NETWORK',json.dumps(r)[:300]); continue
        out=resp(r) if 'res' in r else json.dumps(r.get('out'))[:90]
        le=[f"{(x.get('level') or '')}:{(x.get('line') or '')[24:140]}" for x in r['logs']]
        print(st,e,'|',r['cell'],'|',r['kind'],'|',out,'|',r['writes'],r['unhandled'],'|',' ; '.join(le))
