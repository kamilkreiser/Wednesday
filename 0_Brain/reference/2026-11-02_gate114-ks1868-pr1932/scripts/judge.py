import json,re,sys,copy
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate114-ks1868-pr1932/logs/'
tamper=sys.argv[1] if len(sys.argv)>1 else None
def load(p): return [json.loads(l) for l in open(G+p)]
fails=[];checks=0
def ck(cond,msg):
    global checks; checks+=1
    if not cond: fails.append(msg)
A={s:load(f'probe_anch_{s}.jsonl') for s in ('base','head')}
O={(s,e):load(f'probe_orig_{s}_{e}.jsonl') for s in ('base','head') for e in ('test','production')}
if tamper=='verified_true':
    for r in A['head']:
        if r['cell']=='verify_post' and r['kind']=='revokedProxy': r['res']['body']=r['res']['body'].replace('"verified":false','"verified":true')
if tamper=='write':
    for r in O[('head','test')]:
        if r['cell']=='get_lookup_throws' and r['kind']=='getterThrows': r['writes']=1
if tamper=='orig_200':
    for r in O[('head','production')]:
        if r['cell']=='get_lookup_throws' and r['kind']=='revokedProxy': r['res']={'status':200,'body':'{"documentId":"x","verified":true}'}
def body(r):
    try: return json.loads(r['res'].get('body') or 'null')
    except Exception: return None
def norm_logs(r):
    out=[]
    for l in r.get('logs',[]):
        if isinstance(l,dict): l=l.get('line') or ''
        l=re.sub(r'^\d{4}-\d\d-\d\d \S+ ','',l)
        l=re.sub(r'"timestamp":"[^"]*",?','',l)
        out.append(l)
    return out
def mask(ls): return [re.sub(r'("error":)("[^"]*"|\{[^}]*\})',r'\1<E>',l) for l in ls]
def strip_hash(b):
    if isinstance(b,dict): return {k:('<H>' if k in('hash','contentHash') else strip_hash(v)) for k,v in b.items()}
    return b
UN_A={'revokedProxy','getterThrows'}; UN_O={'revokedProxy','getterThrows','nullProto'}
# anchoring
for s in ('base','head'):
    for r in A[s]:
        if r['cell']=='network':
            ck(r['outbound']==[],f'anch {s} outbound {r["outbound"]}'); continue
        ck(len(r['writes'])==0 and r['submits']==0,f'anch {s} {r["cell"]} {r["kind"]} writes/submits')
        b=body(r); st=r['res'].get('status')
        if r['kind'].startswith('none'): ck(st==200,f'anch control {s} {r["cell"]} not 200'); continue
        if r['cell']=='tx': ck(st!=200,f'anch {s} tx {r["kind"]} answered found')
        if r['cell'].startswith('hash'):
            v=isinstance(b,dict) and b.get('verified') is True
            ck((not v) or (r['cell']=='hash_chain_hit' and b.get('source')=='chain'),f'anch {s} {r["cell"]} {r["kind"]} verified without chain')
        if r['cell']=='verify_post':
            ck(not (isinstance(b,dict) and isinstance(b.get('data'),dict) and b['data'].get('verified') is True),f'anch {s} verify_post {r["kind"]} verified true')
H={(r['cell'],r['kind']):r for r in A['head'] if r['cell']!='network'}
B={(r['cell'],r['kind']):r for r in A['base'] if r['cell']!='network'}
for (c,k),r in H.items():
    if k.startswith('none'): continue
    if k in UN_A:
        o=H[(c,'ordinary')]
        ck(r['res']['status']==o['res']['status'] and strip_hash(body(r))==strip_hash(body(o)),f'anch head {c} {k} != ordinary response')
        ck(r['unhandled']==0 and mask(norm_logs(r))==mask(norm_logs(o)),f'anch head {c} {k} logs/unhandled != ordinary')
        ck(any('"error":"unreadable thrown value"' in l for l in norm_logs(r)),f'anch head {c} {k} no constant')
        ck('getter boom' not in (r['res'].get('body') or '') and 'proxy' not in (r['res'].get('body') or ''),f'anch head {c} {k} body leaks')
        ck(B[(c,k)]['res']['status']!=r['res']['status'] or B[(c,k)]['unhandled']!=r['unhandled'],f'anch base {c} {k} did not differ (no red at base)')
    else:
        ck(r['res']['status']==B[(c,k)]['res']['status'] and strip_hash(body(r))==strip_hash(body(B[(c,k)])) and norm_logs(r)==norm_logs(B[(c,k)]) and r['unhandled']==B[(c,k)]['unhandled'],f'anch base!=head {c} {k}')
# originate
for (s,e),recs in O.items():
    for r in recs:
        if r['cell']=='network': ck(r['outbound']==[],f'orig {s} {e} outbound'); continue
        ck(r['writes']==0,f'orig {s} {e} {r["cell"]} {r["kind"]} writes')
        if r['cell']=='get_control_found': ck(r['res']['status']==200 and (body(r) or {}).get('verified') is True,f'orig {s} {e} positive control not found')
        if r['cell']=='get_control_absent': ck(r['res']['status']==404,f'orig {s} {e} absent control not 404')
        if r['cell']=='get_lookup_throws':
            b=body(r) or {}
            ck(r['res']['status']!=200 and b.get('verified') is not True and 'transactionId' not in b,f'orig {s} {e} get {r["kind"]} positive answer')
            ck(r['res']['status']!=404,f'orig {s} {e} get {r["kind"]} fault read as absent (KS-1657)')
    HH={(r['cell'],r['kind']):r for r in O[('head',e)] if r['cell']!='network'}
    BB={(r['cell'],r['kind']):r for r in O[('base',e)] if r['cell']!='network'}
    if s!='head': continue
    for (c,k),r in HH.items():
        if k=='none':
            na=lambda x: re.sub(r'"anchoredAt":"[^"]*"','"anchoredAt":"<T>"',x['res']['body'])
            ck(r['res']['status']==BB[(c,k)]['res']['status'] and na(r)==na(BB[(c,k)]),f'orig control {e} {c} base!=head'); continue
        if k in UN_O:
            o=HH[(c,'ordinary')]
            ck(r.get('res')==o.get('res') and r.get('out')==o.get('out') and r['unhandled']==o['unhandled'],f'orig head {e} {c} {k} != ordinary outcome')
            ck(mask(norm_logs(r))==mask(norm_logs(o)),f'orig head {e} {c} {k} log shape != ordinary')
            ck(all(('unreadable thrown value' in l) for l in norm_logs(r) if 'Some database connections' not in l),f'orig head {e} {c} {k} constant missing')
        else:
            ck(r.get('res')==BB[(c,k)].get('res') and r.get('out')==BB[(c,k)].get('out') and norm_logs(r)==norm_logs(BB[(c,k)]),f'orig base!=head {e} {c} {k}')
print('checks',checks,'fails',len(fails))
for f in fails: print('FAIL',f)
sys.exit(1 if fails else 0)
