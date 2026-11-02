import json, sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate99-ks1868-pr1917/logs'
def load(v):
    out={}
    for l in open(f'{W}/probe_{v}.jsonl'):
        j=json.loads(l)
        if 'route' in j: out[(j['route'],j['scenario'])]=j
    return out
B,H=load('base'),load('head')
def short(j):
    body=j['body']
    try: body=json.loads(body); body=json.dumps(body.get('error',{}).get('message') if not body.get('success') else 'success')
    except Exception: body=body[:40]
    return f"{j['status']} {body} erase={j['erasing']} after={j['after']} unh={j['unhandled']}"
print('# base vs head per cell')
for k in H:
    b,h=B[k],H[k]
    same = all(b[x]==h[x] for x in ('status','body','sql','after','unhandled'))
    print(f"{k[0]:14s} {k[1]:40s} {'SAME' if same else 'DIFF'}")
    print('   base:',short(b)); print('   head:',short(h))
    if not same and b['sql']!=h['sql']: print('   sqlbase:',b['sql'][-5:]); print('   sqlhead:',h['sql'][-5:])
print('\n# head: unreadable vs ordinary (status, bodySha, sql, after, unhandled)')
for (r,s),h in H.items():
    for k in ('revokedProxy','throwingGetter','throwingToString','stackGetterThrows','plainString'):
        if s.endswith('/'+k) or s==k:
            o=s[:-len(k)]+'ordinary'
            if (r,o) in H:
                oo=H[(r,o)]
                eq={x:(h[x]==oo[x]) for x in ('status','bodySha','sql','after','unhandled')}
                print(f"{r:14s} {s:40s} vs ordinary: {'EQUAL' if all(eq.values()) else 'DIFFERS '+str({k2:v for k2,v in eq.items() if not v})}")
print('\n# erasing statements on DELETE route')
for v,D in (('base',B),('head',H)):
    tot=sum(j['erasing'] for (r,s),j in D.items() if r=='DELETE'); n=sum(1 for (r,s) in D if r=='DELETE')
    print(v,'DELETE records',n,'erasing statements total',tot)
