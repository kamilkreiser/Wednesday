import json,sys,re
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate103-ks1868-pr1921/logs/'
name=sys.argv[1]
def load(v): return [json.loads(l) for l in open(W+f'probe_{name}_{v}.jsonl') if l.strip()]
b,hd=load('base'),load('head')
print('positive controls', b[0], hd[0])
B={r['cell']:r for r in b[1:]}; H={r['cell']:r for r in hd[1:]}
def strip(lines):
    out=[]
    for s in lines:
        j=json.loads(s)
        t=j.get('text') or json.dumps({'level':j.get('level'),'message':j.get('message'),'meta':j.get('meta')})
        t=re.sub(r'"timestamp":"[^"]+",?','',t); t=re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}','<uuid>',t)
        out.append(j['src']+' '+t)
    return out
KEYS=['init','status','imageInsertAttempts','imageRowsPersisted','upsertsAfterInitiate','rowStatus','rowDocumentsCipherPresent','livenessCompleted','livenessScore','checks','subjectKeysMinted','unhandled']
def state(r): return {k:r[k] for k in KEYS}
def body(r):
    bd=r['body']; return json.dumps(bd.get('error') if isinstance(bd,dict) and bd.get('error') else ('success' if isinstance(bd,dict) and bd.get('success') else bd))
for c in B:
    print('\n##',c)
    for v,R in (('base',B[c]),('head',H[c])):
        print(f'  {v}: status={R["status"]} body={body(R)}')
        print(f'        state={json.dumps({k:R[k] for k in KEYS if k not in ("init","status")})}')
        for l in strip(R['logLines']): print('        log:',l[:300])
# rules
print('\nRULES')
fails=0
for c in B:
    route,fo,kind=c.split('/')
    if kind in ('revokedProxy','throwingGetter'):
        o=f'{route}/{fo}/ordinary'
        eq = state(H[c])==state(H[o]) and body(H[c])==body(H[o])
        print(f'head {c} == head {o} (status,body,state): {eq}'); fails+= not eq
        logc=[l for l in strip(H[c]['logLines'])]; logo=[l.replace('db down','unreadable thrown value') for l in strip(H[o]['logLines'])]
        print(f'   log lines head unreadable == ordinary with constant: {logc==logo}'); fails+= logc!=logo
        pers = {k:B[c][k] for k in KEYS if k not in ('status',)} == {k:H[c][k] for k in KEYS if k not in ('status',)}
        print(f'   persisted state base == head: {pers}'); fails+= not pers
    else:
        same = state(B[c])==state(H[c]) and body(B[c])==body(H[c]) and strip(B[c]['logLines'])==strip(H[c]['logLines'])
        print(f'readable {c} base == head (status,body,state,logs): {same}'); fails+= not same
print('RULE FAILURES', fails)
