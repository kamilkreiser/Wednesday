import json,sys
L='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate104-ks1868-pr1923/logs/'
def load(p): return [json.loads(l) for l in open(L+p)]
B=load('probe_base.jsonl'); H=load('probe_head.jsonl')
def short(r):
    b=r['body']
    try: b=json.loads(b); b=b.get('error',{}).get('message') if not b.get('success') else 'success'
    except Exception: pass
    errs=[ (l[1], l[2].get('error') if isinstance(l[2],dict) else l[2]) for l in r['logs'] if l[0]=='error']
    return dict(status=r['status'],body=b,state={'sig':r['state']['sig'],'ver':r['state']['ver'],'records':r['state']['records']},calls=r['calls'],err=errs)
print('ROUTES: route | mode | kind || base || head')
fails=0
hk={(r['route'],r['mode'],r['kind']):r for r in H}
for b in B:
    h=hk[(b['route'],b['mode'],b['kind'])]
    sb,sh=short(b),short(h)
    print(f"{b['route']} | {b['mode']} | {b['kind']}\n   base {sb}\n   head {sh}  leak={h.get('leak')}")
# equality check: at head, unreadable kinds equal ordinaryError in status, body, state, calls, error-log context
print('\nCHECK head unreadable == head ordinaryError (status, body, state, calls, log context), and head ordinary/string == base')
ok=0;bad=0
for (route,mode,kind),h in hk.items():
    if kind in ('revokedProxy','throwingGetter'):
        o=short(hk[(route,mode,'ordinaryError')]); u=short(h)
        same = o['status']==u['status'] and o['body']==u['body'] and o['state']==u['state'] and o['calls']==u['calls'] and [e[0] for e in o['err']]==[e[0] for e in u['err']] and all(e[1]=='unreadable thrown value' for e in u['err']) and len(u['err'])==1
        print(('OK ' if same else 'DIFF ')+route,mode,kind); ok+=same; bad+= (not same)
    if kind in ('ordinaryError','string','none'):
        bb=short([x for x in B if (x['route'],x['mode'],x['kind'])==(route,mode,kind)][0]); u=short(h)
        same= bb==u
        print(('OK ' if same else 'DIFF ')+'base==head',route,mode,kind); ok+=same; bad+=(not same)
    if h.get('leak') and any(h['leak'].values()) and kind!='ordinaryError': print('LEAK',route,mode,kind,h['leak'])
print('ok',ok,'bad',bad)
print('\nRETENTION')
B2=load('probe2_base.jsonl'); H2=load('probe2_head.jsonl')
for b,h in zip(B2,H2):
    def s(r):
        return dict(calls=r.get('enforceCalls'),stmts=r.get('stmts'),err=[(l[1],l[2]) for l in r['logs'] if l[0]=='error'],unhandled=r['unhandled'])
    print(b['probe'],b.get('target',''),b['kind'],'\n   base',s(b),'\n   head',s(h))
