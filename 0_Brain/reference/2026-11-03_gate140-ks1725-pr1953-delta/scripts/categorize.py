# Gate 140: ONE class per differing cell (gate 135's tags, plus F5 recognised as a whole), argv: LBL [kind]
import json,collections,sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate140-ks1725-pr1953-delta'
LBL=sys.argv[1]; KIND=sys.argv[2] if len(sys.argv)>2 else 'product'
r=[x for x in json.load(open(G+'/logs/corpus_diffs_%s.json'%LBL)) if x['kind']==KIND]
J=lambda s: json.loads(s[4:]) if s.startswith('ERR') else None
key=lambda i: json.dumps(i,sort_keys=True)
cats=collections.Counter(); ex={}; perfile=collections.defaultdict(collections.Counter)
def add(c,x):
    cats[c]+=1; perfile[c][x['id'].split('#')[0].replace('Blockchain/Dev/','')+':'+str(x['hline'])]+=1
    ex.setdefault(c,x)
for x in r:
    if x['cls']=='ACC->REJ':
        h=J(x['head']); codes={i['code'] for i in h}; msgs={i['message'] for i in h}
        if codes<={'too_big','too_small'} and all('9007199254740991' in m for m in msgs): add('T1 safe-int refused (accepted 1)',x)
        elif codes<={'not_finite'}: add('T2 coerce Infinity refused (accepted 2)',x)
        else: add('ACC->REJ OTHER',x)
        continue
    if x['cls']!='ERR-BODY': add(x['cls'],x); continue
    b=J(x['base']); h=J(x['head']); bk=[key(i) for i in b]; hk=[key(i) for i in h]
    extra=[i for i in h if key(i) not in bk]; missing=[i for i in b if key(i) not in hk]
    if not extra and not missing: add('F3? ORDER or KEY-ORDER only',x); continue
    tags=set()
    for e in extra:
        p=e.get('path'); same=[m for m in missing if m.get('path')==p]
        if e['code'] in('too_small','too_big') and str(e.get('maximum',e.get('minimum'))).lstrip('-')=='9007199254740991': tags.add('T1b safe-int bound (F7a)'); continue
        if e['code']=='not_finite': tags.add('T2b not_finite (F7b)'); continue
        if e['code'] in('too_small','too_big') and any(i['code']=='invalid_type' and i.get('path')==p for i in h) and not same: tags.add('F2 extra length issue after invalid_type'); continue
        if e['code']=='invalid_type' and 'received' not in e and same: tags.add('F1 custom message on invalid_type: '+e['message'][:40]); continue
        if e['code']=='invalid_type' and same and same[0]['code']=='invalid_enum_value': tags.add('F4 nativeEnum number'); continue
        if e['code']=='too_big' and e.get('type')=='array' and e in [i for i in h] and all(len(m['path'])>len(p) and m['path'][:len(p)]==p for m in missing if m.get('path')!=p): tags.add('F5 over-max array drops element issues'); continue
        tags.add('X extra %s'%json.dumps(e)[:160])
    for m in missing:
        p=m.get('path')
        if [e for e in extra if e.get('path')==p]: continue
        if m['code'] in('too_small','too_big') and any(i['code']=='invalid_type' and i.get('expected')=='integer' and i.get('path')==p for i in h): tags.add('T3 int stops chain (accepted 3)'); continue
        if m['code'] in('too_small','too_big') and any(i['code']=='not_finite' and i.get('path')==p for i in h): tags.add('T2b not_finite (F7b)'); continue
        par=[i for i in h if i['code']=='too_big' and i.get('type')=='array' and len(i['path'])<len(p) and p[:len(i['path'])]==i['path']]
        if par: tags.add('F5 over-max array drops element issues'); continue
        tags.add('X missing %s'%json.dumps(m)[:160])
    add(' + '.join(sorted(tags)),x)
print('kind',KIND,'differing cells',len(r))
for c,n in cats.most_common():
    print(n,c); print('     sites',dict(perfile[c].most_common(6)))
    x=ex[c]; print('     e.g.',x['id'],'L',x['hline'],x['text'][:100]); print('       in  ',json.dumps(x['input'])[:200]); print('       base',x['base'][:260]); print('       head',x['head'][:260])
