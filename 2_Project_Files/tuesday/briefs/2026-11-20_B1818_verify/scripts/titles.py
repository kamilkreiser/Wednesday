import subprocess,re,collections
C='/private/tmp/b1818-gate/clone'
M='2a58dc5d9c62cc021b01e3fe5ebdcd09e76d7f9a'; MAIN='b4681297d974ac3d8e74a4a12baeb9ea41962c52'; BASE='308b7aa60cd8d2a8576b29e0422538cbaf140f24'; OLD='851057291ffb019baee6c3c51a50d7b8833f5b3a'
def g(*a): return subprocess.run(['git','-C',C,*a],capture_output=True).stdout.decode('utf-8','replace')
T=re.compile(r'\b(?:it|test)(?:\.(?:skip|only|concurrent|fails|todo|skipIf\([^)]*\)|runIf\([^)]*\)))*\(\s*(["\'`])((?:\\.|(?!\1).)*)\1',re.S)
def titles(c):
    out=collections.Counter()
    for p in g('ls-tree','-r','--name-only',c).splitlines():
        if re.search(r'\.(test|spec)\.(ts|tsx|js|mjs)$',p) and '/e2e/' not in p:
            for m in T.finditer(g('show',f'{c}:{p}')): out[(p,m.group(2))]+=1
    return out
a=titles(MAIN); b=titles(M)
print('literal titles main',sum(a.values()),'merged',sum(b.values()))
lost=a-b; add=b-a
print('lost',sum(lost.values()))
for (p,t) in lost: print('  L',p,'|',t)
print('added',sum(add.values()))
print('added files',collections.Counter(p for p,t in add.elements()).most_common())
pr=set(g('diff','--name-only',BASE,OLD).split()); mn=set(g('diff','--name-only',BASE,MAIN).split())
for (p,t) in lost: print('  file in PR 57:',p in pr,' in main 87:',p in mn)
# control
ctl=b.copy(); k=next(iter(a)); ctl[k]-=1; print('control lost',sum((a-ctl).values()))
