import subprocess,re,collections
C='/private/tmp/b1818-gate/clone'
X='2a58dc5d9c62cc021b01e3fe5ebdcd09e76d7f9a'; MAIN='b4681297d974ac3d8e74a4a12baeb9ea41962c52'; BASE='308b7aa60cd8d2a8576b29e0422538cbaf140f24'; OLD='851057291ffb019baee6c3c51a50d7b8833f5b3a'
def g(*a): return subprocess.run(['git','-C',C,*a],capture_output=True).stdout.decode('utf-8','replace')
pr=set(g('diff','--name-only',BASE,OLD).split()); mn=set(g('diff','--name-only',BASE,MAIN).split())
REL=re.compile(r'real-resolution|real-content|release-demo|release-draft|CONTENT_HASH|content_release_hash')
TEST=re.compile(r'(\.test\.|\.spec\.|/test/|/e2e/)')
files=[p for p in g('ls-tree','-r','--name-only',X).splitlines() if TEST.search(p) and not p.startswith('content/') and p!='package-lock.json']
hit={}
for p in files:
    t=g('show',f'{X}:{p}')
    if REL.search(t): hit[p]=t
inpr=[p for p in hit if p in pr]; inmn=[p for p in hit if p in mn]; neither=[p for p in hit if p not in pr and p not in mn]
print('test files naming a release',len(hit),'PR',len(inpr),'main',len(inmn),'neither',len(neither))
print('main 7:'); [print('  ',p) for p in sorted(inmn)]
OLDPIN=re.compile(r'05070f1d|62cf4932')
allf=[p for p in g('ls-tree','-r','--name-only',X).splitlines() if not p.startswith('content/') and p!='package-lock.json']
pins=[]
for p in allf:
    t=g('show',f'{X}:{p}')
    for i,l in enumerate(t.splitlines(),1):
        if OLDPIN.search(l): pins.append((p,i,l.strip()[:160]))
pf=sorted(set(p for p,_,_ in pins)); print('old-pin files at merge',len(pf))
for p in pf: print('  ',p,'PR' if p in pr else ('main' if p in mn else 'neither'))
print('-- old-pin lines in files the PR does not edit:')
for p,i,l in pins:
    if p not in pr: print('  %s:%d: %s'%(p,i,l))
# suspicious count assertions in main7 + neither
NUM=re.compile(r'(toHaveLength|toBe|toEqual|toBeGreaterThan|toBeLessThan)\(\s*(55|123|11|12|5|132|137|351|98)\s*\)')
print('-- count assertions with release-ish numbers in main7+neither files:')
n=0
for p in sorted(inmn+neither):
    for i,l in enumerate(hit[p].splitlines(),1):
        if NUM.search(l): n+=1; print('  %s:%d: %s'%(p,i,l.strip()[:150]))
print('total',n)
import json; json.dump({'main':sorted(inmn),'neither':sorted(neither)},open('/private/tmp/b1818-gate/logs/census_sets.json','w'))
