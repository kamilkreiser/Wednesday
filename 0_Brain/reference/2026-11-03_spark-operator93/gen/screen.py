import os,re,sys,json
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator93/'
S=W+'repo/'
held=set(open(W+'held_paths.out').read().split())
prs=json.load(open(W+'open_prs_start.json')); prf=set(f for v in prs.values() for f in v['files'])
rx=re.compile(r"instanceof Error\s*\?\s*\w+(\?)?\.message\s*:\s*String\(|\b(err|error|e)\??\.message\b|String\((err|error|e)\)")
out=[]
for root,ds,fs in os.walk(S+'Blockchain/Dev/services'):
    ds[:]=[d for d in ds if d not in('node_modules','dist','__tests__','tests','test','build')]
    for f in fs:
        if not f.endswith('.ts') or f.endswith('.d.ts') or '.test.' in f or '.spec.' in f: continue
        p=os.path.join(root,f); rel=p[len(S):]
        L=open(p,encoding='utf-8',errors='replace').read().split('\n')
        hits=[i+1 for i,l in enumerate(L) if rx.search(l)]
        if hits: out.append((rel,hits,rel in held,rel in prf))
for rel,h,hd,pr in sorted(out):
    print(('HELD ' if hd else '     ')+('PR ' if pr else '   ')+rel.replace('Blockchain/Dev/services/','')+' '+','.join(map(str,h[:30])))
