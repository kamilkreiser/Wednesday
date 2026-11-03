import re,subprocess,json,sys
O='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator99/'
C='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src'
TIP='1cbf260548e7fd534603725f9fc6b05c5cdd9907'
held=set(open(O+'held_paths.out').read().split())|set(open(O+'r79_queue_paths.txt').read().split())
prs=json.load(open(O+'prs.json')); prf=set(f for v in prs.values() for f in v['files'])
rx=r"\([A-Za-z_]+ as Error\)\??\.message|\$\{(err|error|e|ex|exception)\}|\b[A-Za-z_]*([Ee]rr|[Ee]rror|[Ee]x|[Ee]xception|[Cc]ause)[A-Za-z_]*\??\.message\b|String\([A-Za-z_]*([Ee]rr|[Ee]rror|ex|[Cc]ause)[A-Za-z_]*\)"
r=subprocess.run(['git','-C',C,'grep','-n','-E','-I',rx,TIP,'--','Blockchain/Dev/services','Blockchain/Dev/packages','Blockchain/Dev/scripts'],capture_output=True,text=True).stdout
res={}
for l in r.splitlines():
    l=l[len(TIP)+1:]; p,n,_=l.split(':',2)
    if not p.endswith('.ts') or p.endswith('.d.ts') or re.search(r'\.(test|spec)\.|/__tests__/|/tests?/|/node_modules/|/dist/|/e2e/|/fixtures/',p): continue
    res.setdefault(p,[]).append(int(n))
for p,h in sorted(res.items()):
    print(('HELD ' if re.search(r'/services/auth/|restore-local-secrets',p) else '')+('HELD ' if p in held else '     ')+('PR ' if p in prf else '   ')+p.replace('Blockchain/Dev/','')+' '+','.join(map(str,h[:25])))
