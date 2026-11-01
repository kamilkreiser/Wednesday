import subprocess,hashlib,json,re
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate96-ks1868-pr1914'
A=W+'/repo/Blockchain/Dev/services/analytics'; PROD=A+'/src/routes/analytics.ts'
orig=open(PROD).read(); sha=hashlib.sha256(orig.encode()).hexdigest(); assert sha.startswith('d5afff9c')
pat=re.compile(r"(error: \{ code: 'BAD_REQUEST', message: '[^']+'), details: error\.errors( \},)")
ms=list(pat.finditer(orig)); print('400 bodies',len(ms)); assert len(ms)==9
def run():
    p=subprocess.run(['npx','vitest','run','src/__tests__/ks1868-analytics-routes','--reporter=json'],cwd=A,capture_output=True,text=True)
    j=json.loads(p.stdout[p.stdout.index('{'):])
    return [t['title'][:60] for f in j['testResults'] for t in f['assertionResults'] if t['status']=='failed']
for kind,fn in [('details_dropped',lambda m:m.group(1)+m.group(2)),('details_empty',lambda m:m.group(1)+', details: []'+m.group(2)),('code_changed',lambda m:m.group(0).replace("'BAD_REQUEST'","'BAD'"))]:
    for i,m in enumerate(ms):
        new=orig[:m.start()]+fn(m)+orig[m.end():]
        open(PROD,'w').write(new)
        try: f=run()
        finally: open(PROD,'w').write(orig)
        assert hashlib.sha256(open(PROD).read().encode()).hexdigest()==sha
        print(kind,i,'KILLED' if f else 'SURVIVED',sorted(set(re.sub(r' ks1868 (\w\d).*',r'\1',t) for t in f)),flush=True)
