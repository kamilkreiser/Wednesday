import json,collections,re,sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate135-ks1725-pr1953'
r=[x for x in json.load(open(G+'/logs/corpus_diffs.json')) if x['kind']==(sys.argv[1] if len(sys.argv)>1 else 'product')]
def sig(x):
    if x['cls'] in ('ACC->REJ','REJ->ACC'):
        e = x['head'] if x['cls']=='ACC->REJ' else x['base']
        codes=re.findall(r'"code":"(\w+)"',e); msgs=re.findall(r'"message":"([^"]{0,60})',e)
        return (x['cls'], tuple(sorted(set(codes))), tuple(sorted(set(msgs)))[:3])
    if x['cls']=='ERR-BODY':
        bj=json.loads(x['base'][4:]) if len(x['base'])<700 else None
        hj=json.loads(x['head'][4:]) if len(x['head'])<700 else None
        if bj is None or hj is None: return ('ERR-BODY','truncated')
        if len(bj)!=len(hj): return ('ERR-BODY','count %d->%d'%(len(bj),len(hj)), tuple(i.get('code') for i in bj), tuple(i.get('code') for i in hj))
        d=[]
        for a,c in zip(bj,hj):
            if a!=c:
                keys=sorted(set(a)|set(c)); diffk=tuple(k for k in keys if a.get(k)!=c.get(k))
                d.append((a.get('code'),c.get('code'),diffk, list(a.keys())==list(c.keys())))
        return ('ERR-BODY',tuple(d[:2]))
    return (x['cls'],)
c=collections.defaultdict(list)
for x in r: c[sig(x)].append(x)
for k,v in sorted(c.items(), key=lambda kv:-len(kv[1])):
    files=collections.Counter(x['id'].split('#')[0].split('/src/')[0].split('/')[-1] for x in v)
    print(len(v), k, dict(files.most_common(6)))
    ex=v[0]; print('     e.g.', ex['id'], 'L', ex['line'], 'input=', json.dumps(ex['input'])[:150]); print('       base', ex['base'][:300]); print('       head', ex['head'][:300])
