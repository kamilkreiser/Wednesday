import subprocess, json, hashlib, sys, re
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate108-ks1868-pr1926'
N=W+'/repo/Blockchain/Dev/services/nft-certificate'
F=N+'/src/services/ipfs.service.ts'
orig=open(F).read()
sha=lambda s: hashlib.sha256(s.encode()).hexdigest()[:12]
BLK="""      let reason: string;
      try {
        reason = (error as Error).message;
      } catch {
        reason = 'unreadable thrown value';
      }
"""
assert orig.count(BLK)==3
pos=[m.start() for m in re.finditer(re.escape(BLK),orig)]
forms={
 'undo': "      const reason = (error as Error).message;\n",
 'const': "      const reason = 'x';\n",
 'swallow_wrong': "      let reason: string;\n      try {\n        reason = (error as Error).message;\n      } catch {\n        throw new Error('rethrown');\n      }\n",
}
def run(tag):
  out=W+'/logs/mut_%s.json'%tag
  subprocess.run([N+'/node_modules/.bin/vitest','run','--root',N,'src/__tests__/ks1868-ipfs-upload-unreadable-throw.test.ts','src/__tests__/ipfs.service.test.ts','src/__tests__/ks1240b-ipfs-fetches-are-bounded-and-a-body-stall-maps-to-503.test.ts','--reporter=json','--outputFile='+out],capture_output=True)
  d=json.load(open(out)); red=[]
  for f in d['testResults']:
    for a in f['assertionResults']:
      if a['status']!='passed': red.append(a['title'][:30])
    if not f['assertionResults'] and f['status']!='passed': red.append('SUITE:'+f['name'][-40:])
  return red
base=run('head'); print('head red',base)
for name,rep in forms.items():
  for i,p in enumerate(pos,1):
    # replace i-th block
    m=orig[:p]+rep+orig[p+len(BLK):]
    open(F,'w').write(m)
    try: r=run('%s_%d'%(name,i)); 
    finally: open(F,'w').write(orig)
    assert sha(open(F).read())==sha(orig)
    print(name,'site',i,'sha',sha(m),'red',len(r),r)
print('RESTORE_OK',sha(orig))
