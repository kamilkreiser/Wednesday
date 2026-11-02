import os,re,json
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator91/'
S=W+'repo/'
held=set(open(W+'held_paths.out').read().split())
extra=set(l.split()[0] for l in open(W+'brief_paths_extra.out') if l.strip())
prs=json.load(open(W+'open_prs_start.json')); prf=set(f for v in prs.values() for f in v['files'])
rc=re.compile(r"catch\s*\((\w+)(?::\s*\w+)?\)\s*\{")
rc2=re.compile(r"\.catch\(\s*\(?(\w+)(?::\s*\w+)?\)?\s*=>")
res=[]
for root,ds,fs in os.walk(S+'Blockchain/Dev/services'):
    ds[:]=[d for d in ds if d not in('node_modules','dist','__tests__','tests','test','build','shared')]
    for f in fs:
        if not f.endswith('.ts') or f.endswith('.d.ts') or '.test.' in f: continue
        p=os.path.join(root,f); rel=p[len(S):]
        if rel in held or rel in extra: continue
        L=open(p,encoding='utf-8',errors='replace').read().split('\n')
        hits=[]
        for i,l in enumerate(L):
            m=rc.search(l) or rc2.search(l)
            if not m: continue
            v=m.group(1)
            if v in('_','e_'): continue
            win='\n'.join(L[i:i+7])
            if re.search(r'\b%s\??\.(message|code|stack)\b|String\(%s\)|%s instanceof'%(v,v,v),win):
                hits.append(i+1)
        if hits: res.append((rel.replace('Blockchain/Dev/services/',''),hits,rel in prf))
for r,h,pr in sorted(res): print(('PR ' if pr else '   ')+r,len(h),','.join(map(str,h[:12])))
