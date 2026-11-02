import json,collections,sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate135-ks1725-pr1953'
KIND=sys.argv[1] if len(sys.argv)>1 else 'product'
r=[x for x in json.load(open(G+'/logs/corpus_diffs_fix.json')) if x['kind']==KIND]
J=lambda s: json.loads(s[4:]) if s.startswith('ERR') else None
def key(i): return json.dumps(i,sort_keys=True)
cats=collections.Counter(); ex={}; perfile=collections.defaultdict(collections.Counter)
def add(c,x,detail=''):
    cats[c]+=1; perfile[c][x['id'].split('#')[0].replace('Blockchain/Dev/','')]+=1
    if c not in ex: ex[c]=(x,detail)
for x in r:
    if x['cls']=='ACC->REJ':
        h=J(x['head']); codes={i['code'] for i in h}; msgs={i['message'] for i in h}
        if codes<= {'too_big'} and all('9007199254740991' in m for m in msgs): add('T1 safe-int too_big (accepted 1)',x)
        elif codes<={'not_finite'}: add('T2 not_finite (accepted 2)',x)
        else: add('ACC->REJ OTHER',x,json.dumps(h)[:300])
        continue
    if x['cls']!='ERR-BODY': add(x['cls'],x); continue
    b=J(x['base']); h=J(x['head'])
    bk=[key(i) for i in b]; hk=[key(i) for i in h]
    extra=[i for i in h if key(i) not in bk]; missing=[i for i in b if key(i) not in hk]
    if not extra and not missing:
        add('ORDER or KEY-ORDER only',x); continue
    tags=set()
    # pair same-path issues
    for e in extra:
        p=e.get('path'); same=[m for m in missing if m.get('path')==p]
        if e['code'] in('too_small','too_big') and any(i['code']=='invalid_type' and i.get('path')==p for i in h) and not same: tags.add('B extra length issue after invalid_type'); continue
        if e['code']=='too_big' and str(e.get('maximum'))=='9007199254740991': tags.add('T1 safe-int too_big'); 
        elif e['code']=='not_finite': tags.add('T2 not_finite')
        elif e['code']=='invalid_type' and 'received' not in e and same: tags.add('A custom message on invalid_type, received dropped: '+e['message'][:40])
        elif same: tags.add('X changed %s->%s: %s'%(same[0]['code'],e['code'],json.dumps(e)[:150]))
        else: tags.add('X extra %s'%json.dumps(e)[:160])
    for m in missing:
        p=m.get('path'); same=[e for e in extra if e.get('path')==p]
        if same: continue
        if m['code'] in('too_small','too_big') and any(i['code']=='invalid_type' and i.get('expected')=='integer' and i.get('path')==p for i in h): tags.add('T3 int stops chain (accepted 3)'); continue
        if m['code'] in('too_small','too_big') and any(i['code']=='not_finite' and i.get('path')==p for i in h): tags.add('T2 not_finite'); continue
        tags.add('X missing %s'%json.dumps(m)[:160])
    for t in tags: add(t,x)
for c,n in cats.most_common():
    print(n,c); print('     files',dict(perfile[c].most_common(8)))
    x,d=ex[c]; print('     e.g.',x['id'],'L',x['line'],x['text'][:100]); print('       in ',json.dumps(x['input'])[:200]); print('       base',x['base'][:260]); print('       head',x['head'][:260])
