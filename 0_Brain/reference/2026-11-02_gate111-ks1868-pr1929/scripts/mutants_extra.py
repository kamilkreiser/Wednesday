import subprocess,hashlib,json,shutil
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate111-ks1868-pr1929'
G=W+'/repo/Blockchain/Dev/services/governance'
SVC=G+'/src/services/governanceService.ts'
orig=open(SVC).read(); osha=hashlib.sha256(orig.encode()).hexdigest()
OLD="""    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.error('Failed to seed proposal counter from DB', { error: reason });"""
assert orig.count(OLD)==1
M={'string_branch_unguarded': """    let reason: string;
    let isErr = true;
    try { isErr = err instanceof Error; } catch { /* mutant */ }
    if (!isErr) {
      reason = String(err);
    } else {
      try { reason = err.message; } catch { reason = 'unreadable thrown value'; }
    }
    logger.error('Failed to seed proposal counter from DB', { error: reason });"""}
out=[]
for name,new in M.items():
  open(SVC,'w').write(orig.replace(OLD,new))
  j=W+f'/logs/mut_{name}.json'
  p=subprocess.run([G+'/node_modules/.bin/jest','--config',G+'/jest.config.js','--rootDir',G,'--testPathPattern','ks1868-verify-db-ready','--json','--outputFile',j],capture_output=True,text=True)
  open(SVC,'w').write(orig)
  assert hashlib.sha256(open(SVC).read().encode()).hexdigest()==osha
  try:
    d=json.load(open(j)); res=d['testResults'][0]
    red=[a['title'].split(' ')[2] if a['title'].startswith('RED') else a['title'].split(' ')[2] for a in res['assertionResults'] if a['status']!='passed']
    if not res['assertionResults']: red=['SUITE_FAILED:'+res['message'][:120].replace('\n',' ')]
  except Exception as e: red=['NOJSON '+str(e)]
  out.append(f"{name.ljust(22)} rc {p.returncode} red {red} {'KILLED' if red else 'SURVIVED'}")
out.append('RESTORE_OK '+osha[:12])
print('\n'.join(out))
