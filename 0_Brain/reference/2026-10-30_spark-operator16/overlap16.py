import os,sys,re,glob,json,time,fnmatch
NIGHT='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night'
PR=json.load(open('/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/52e2783b-09e1-49d1-9200-c6e9ede3ba54/scratchpad/op16/prs.json'))
prs={}
for p in PR:
    for f in p['files']: prs.setdefault(f['path'],[]).append(p['number'])
held={}
T=time.mktime(time.strptime(os.environ.get('HELD_SINCE','2026-10-28'),'%Y-%m-%d'))
for f in glob.glob(NIGHT+'/READY_*.diff.md'):
    if os.path.getmtime(f)<T: continue
    t=open(f,encoding='utf-8',errors='replace').read()
    for p in set(re.findall(r'^\+\+\+ b/(\S+)',t,re.M)): held.setdefault(p,set()).add(os.path.basename(f)[:44])
PART=['Blockchain/Dev/services/nft-certificate/*','package-lock.json','Blockchain/Dev/package-lock.json','Blockchain/Dev/frontend/*/package-lock.json','Blockchain/Dev/frontend/*','Blockchain/Dev/services/api-gateway/Dockerfile','Blockchain/Dev/services/anchoring/src/index.ts','*DEVELOPMENT.md','*BACKLOG.md','Blockchain/Dev/services/originate/src/routes/documents.ts',
 'Blockchain/Dev/services/originate/src/__tests__/ks1780-*','Blockchain/Dev/services/originate/src/routes/gdpr.ts','Blockchain/Dev/services/originate/src/__tests__/ks445-gdpr-write-guards.test.ts','Blockchain/Dev/services/governance/src/__tests__/ks1722-*','Blockchain/Dev/services/anchoring/src/reconciler.ts','Blockchain/Dev/services/anchoring/src/__tests__/ks1816*','Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts']
def files_of(t): return set(re.findall(r'^\+\+\+ b/(\S+)',t,re.M))|set(re.findall(r'^--- a/(\S+)',t,re.M))
print('open PRs',len(PR),'files',len(prs),'held files',len(held))
if os.environ.get('CONTROL'):
    for c in ['Blockchain/Dev/services/auth/src/routes/users.ts','Blockchain/Dev/services/originate/src/routes/documents.ts']: print('CONTROL',c,prs.get(c),c in held,[x for x in PART if fnmatch.fnmatch(c,x)])
bad=0
for b in sys.argv[1:]:
    g=open(f'{NIGHT}/briefs/{b}/golden.diff',encoding='utf-8').read()
    tam=re.search(r'^tier=test_only',open(f'{NIGHT}/briefs/{b}/spark.pins').read(),re.M)
    fs=files_of(g)
    if tam:
        pin=open(f'{NIGHT}/briefs/{b}/spark.pins').read()
        md=glob.glob(f'{NIGHT}/briefs/{b}/KS-*.md')[0]; m=re.search(r'^File: `([^`]+)`',open(md).read(),re.M); fs.add(m.group(1))
    for p in sorted(fs):
        hit=[]
        if p in prs: hit.append(('openPR',prs[p]))
        if p in held: hit.append(('held',sorted(held[p])))
        pp=[x for x in PART if fnmatch.fnmatch(p,x)]
        if pp: hit.append(('partition',pp))
        print(b,p.replace('Blockchain/Dev/',''),'->',hit or 'clear'); bad+=bool(hit)
print('OVERLAPS',bad)
