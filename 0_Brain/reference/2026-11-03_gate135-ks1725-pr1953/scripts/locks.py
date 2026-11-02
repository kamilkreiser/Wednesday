import json,subprocess,collections
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate135-ks1725-pr1953'; R=G+'/repo'
BASE='8150eeb3802bd9cfe5242ffbc49278c1a3739a84'; HEAD='ea6d924eb5de309482cbb586d97285fc4851fbdb'
def ls(rev): return [l.split('\t')[1] for l in subprocess.run(['git','-C',R,'ls-tree','-r',rev],capture_output=True,text=True).stdout.splitlines() if l.split('\t')[1].endswith(('package-lock.json','npm-shrinkwrap.json','yarn.lock','pnpm-lock.yaml'))]
def show(rev,p): return subprocess.run(['git','-C',R,'show',f'{rev}:{p}'],capture_output=True,text=True).stdout
def pk(txt):
    d=json.loads(txt); out={}
    for k,v in (d.get('packages') or {}).items():
        if k=='' : continue
        name=k.split('node_modules/')[-1]; out[k]=(name,v.get('version'))
    return out
lb=ls(BASE); lh=ls(HEAD)
print('lockfiles tracked: base',len(lb),'head',len(lh),'non-npm:',[p for p in lh if not p.endswith('package-lock.json')])
print('added',sorted(set(lh)-set(lb)),'removed',sorted(set(lb)-set(lh)))
def vt(v): return tuple(int(x) for x in v.split('-')[0].split('.'))
bad=[]; zodsummary=collections.Counter(); moved=collections.Counter(); movedlocks=collections.defaultdict(set); added=collections.Counter(); removed=collections.Counter()
changed_files=set(subprocess.run(['git','-C',R,'diff','--name-only',BASE,HEAD],capture_output=True,text=True).stdout.split())
for p in lh:
    if not p.endswith('package-lock.json'): continue
    H=pk(show(HEAD,p)); B=pk(show(BASE,p)) if p in lb else {}
    for k,(n,v) in H.items():
        if n=='zod':
            zodsummary[(v)]+=1
            if v is None or vt(v)<(4,6,6): bad.append((p,k,v))
    if p not in changed_files: continue
    for k in set(H)|set(B):
        hv=H.get(k); bv=B.get(k)
        if hv and bv and hv[1]!=bv[1]: moved[(hv[0],bv[1],hv[1])]+=1; movedlocks[(hv[0],bv[1],hv[1])].add(p)
        elif hv and not bv: added[(hv[0],hv[1],k)]+=1
        elif bv and not hv: removed[(bv[0],bv[1],k)]+=1
print('zod entries across ALL head locks by version:',dict(zodsummary))
print('zod entries below 4.6.6 at head:',len(bad)); [print('  BAD',b) for b in bad]
print('locks changed by the PR:',sum(1 for p in lh if p in changed_files))
print('version moves (package, base -> head): count of lock entries')
for (n,a,b),c in sorted(moved.items()): print('  %-40s %s -> %s  x%d  in %d locks'%(n,a,b,c,len(movedlocks[(n,a,b)])))
print('entries added (path-level):'); [print('  ',k,c) for k,c in sorted(added.items())]
print('entries removed (path-level):'); [print('  ',k,c) for k,c in sorted(removed.items())]
