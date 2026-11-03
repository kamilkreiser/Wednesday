import re,subprocess,json
O='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator97/'
C='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src'
TIP='de8d208a8426747b3a752309e08167fa0de4b2ff'
held=set(open(O+'held_paths.out').read().split())
prs=json.load(open(O+'open_prs_start.json')); prf=set(f for v in prs.values() for f in v['files'])
files=subprocess.run(['git','-C',C,'grep','-l','-I','-E',r'catch \(',TIP,'--','Blockchain/Dev/services','Blockchain/Dev/packages'],capture_output=True,text=True).stdout.split()
tot=0
for f in files:
    p=f[len(TIP)+1:]
    if not p.endswith('.ts') or re.search(r'\.d\.ts|\.(test|spec)\.|/__tests__/|/tests?/|/node_modules/|/dist/|/e2e/|/fixtures/|/services/auth/',p): continue
    if p in held or p in prf: continue
    src=subprocess.run(['git','-C',C,'show',TIP+':'+p],capture_output=True,text=True).stdout.splitlines()
    hits=[]
    for i,l in enumerate(src):
        m=re.search(r'catch \((\w+)(?:: \w+)?\)',l)
        if not m: continue
        v=m.group(1); body=src[i+1:i+14]
        for j,b in enumerate(body):
            if re.search(r'\b'+v+r'\b',b) and re.search(r'\$\{[^}]*\b'+v+r'\b|\b'+v+r'\)?\??\.message|String\('+v+r'\)|\b'+v+r'\??\.toString|\+ *'+v+r'\b|'+v+r'\)?\??\.stack|JSON\.stringify\('+v+r'\)',b):
                hits.append((i+1+j+1,b.strip()[:110])); break
        # stop at next catch handled by window
    if hits:
        tot+=len(hits); print(p.replace('Blockchain/Dev/',''),len(hits))
        for n,t in hits: print('    ',n,t)
print('TOTAL',tot)
