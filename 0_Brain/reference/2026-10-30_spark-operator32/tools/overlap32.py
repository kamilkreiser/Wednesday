import os,sys,json,subprocess,tempfile,glob,re
env={}
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'):
    if l.startswith('GH_TOKEN='): env['GH_TOKEN']=l.split('=',1)[1].strip().strip('"\'')
e=dict(os.environ,GH_CONFIG_DIR=tempfile.mkdtemp(),**env)
out=subprocess.run(['gh','pr','list','-R','Secuura/Distributed_Secuura','--state','open','--limit','300','--json','number,files,title'],capture_output=True,text=True,env=e)
if out.returncode: sys.exit('gh failed: '+out.stderr[:300])
prs=json.loads(out.stdout)
files={}
for p in prs:
    for f in p['files']: files.setdefault(f['path'],[]).append(p['number'])
O=sys.argv[1]
with open(O+'/open_pr_files.tsv','w') as fh:
    for p,n in sorted(files.items()): fh.write(p+'\t'+','.join(map(str,n))+'\n')
print('open PRs',len(prs),'file rows',sum(len(v) for v in files.values()),'(each PR files list may be capped at 100 by gh)')
big=[p['number'] for p in prs if len(p['files'])>=100]; print('PRs with >=100 files (possible truncation):',big)
T='Blockchain/Dev/services/api-gateway/src/__tests__/'
names=['csrf.test.ts','ks1165-api-gateway-csrf-excludedpaths-carries-no.test.ts','rateLimitEnforce.test.ts','ks1457-audit-finish-reads-use-the-entry-path.test.ts','ks1464-limiter-key-hygiene.test.ts','ks1374-global-limiter-at-demo-limit.test.ts','ks695-ask3-erase-connector-door.test.ts']
# positive control: an api-gateway file from some open PR
ctl=[p for p in files if p.startswith('Blockchain/Dev/services/api-gateway/')]
print('CONTROL api-gateway files in open PRs:',[(p,files[p]) for p in ctl[:3]] if ctl else 'none in api-gateway; using first file', [ (p,files[p]) for p in list(files)[:1]] if not ctl else '')
for n in names: print(n,'->',files.get(T+n,[]) or 'no open PR')
# any open PR touching api-gateway/src/__tests__ at all
print('open-PR files under api-gateway/src/__tests__:',[(p,files[p]) for p in files if 'api-gateway/src/__tests__' in p])
# held READYs
for f in glob.glob('/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_*.diff.md'):
    t=open(f,errors='replace').read()
    for n in names:
        if n in t: print('HELD READY mentions',n,os.path.basename(f)[:80])
