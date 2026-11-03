import re,subprocess,json,sys
O='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator97/'
C='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src'
TIP='de8d208a8426747b3a752309e08167fa0de4b2ff'
held=set(open(O+'held_paths.out').read().split())
prs=json.load(open(O+'open_prs_start.json')); prf=set(f for v in prs.values() for f in v['files'])
rx=r"instanceof Error ?\? ?[A-Za-z_]+\??\.message ?: ?String\(|String\((err|error|e)\)|\b(err|error|e)\??\.message\b"
r=subprocess.run(['git','-C',C,'grep','-n','-E','-I',rx,TIP,'--','Blockchain/Dev/services','Blockchain/Dev/packages','Blockchain/Dev/scripts'],capture_output=True,text=True).stdout
res={}
for l in r.splitlines():
    l=l[len(TIP)+1:]; p,n,_=l.split(':',2)
    if not p.endswith('.ts') or p.endswith('.d.ts') or re.search(r'\.(test|spec)\.|/__tests__/|/tests?/|/node_modules/|/dist/|/e2e/|/fixtures/',p): continue
    res.setdefault(p,[]).append(int(n))
for p,h in sorted(res.items()):
    print(('HELD ' if p in held else '     ')+('PR ' if p in prf else '   ')+p.replace('Blockchain/Dev/','')+' '+','.join(map(str,h[:25])))
