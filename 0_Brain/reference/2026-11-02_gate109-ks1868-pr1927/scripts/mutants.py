import subprocess, json, hashlib
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate109-ks1868-pr1927'
N=W+'/repo/Blockchain/Dev/services/nft-certificate'
F=N+'/src/services/blockchain-verifier.service.ts'
orig=open(F).read(); sha=lambda s: hashlib.sha256(s.encode()).hexdigest()[:12]
S1="""      let reason: string;
      try {
        reason = err instanceof Error ? err.message : String(err);
      } catch {
        reason = 'unreadable thrown value';
      }
"""
S2="""      try {
        void (err as { status_code?: number }).status_code;
        void (err instanceof Error ? err.message : String(err));
        void (err as Error).message;
      } catch {
        logger.error('Error verifying transaction', { error: 'unreadable thrown value' });
        return { verified: false, status: 'error', error: 'unreadable thrown value' };
      }
"""
assert orig.count(S1)==1 and orig.count(S2)==1
M={
 'site1_undo': (S1, "      const reason = err instanceof Error ? err.message : String(err);\n"),
 'site1_const': (S1, "      const reason = 'x';\n"),
 'site1_rethrow': (S1, S1.replace("reason = 'unreadable thrown value';","throw new Error('rethrown');")),
 'site2_undo': (S2, ""),
 'site2_verified_true': (S2, S2.replace("verified: false, status: 'error'","verified: true, status: 'error'")),
 'site2_status_pending': (S2, S2.replace("status: 'error', error","status: 'pending', error")),
 'site2_drop_message_probe': (S2, S2.replace("        void (err as Error).message;\n","").replace("        void (err instanceof Error ? err.message : String(err));\n","")),
 'site2_rethrow': (S2, S2.replace("        logger.error('Error verifying transaction', { error: 'unreadable thrown value' });\n        return { verified: false, status: 'error', error: 'unreadable thrown value' };","        throw new Error('rethrown');")),
}
def run(tag):
  out=W+'/logs/mut_%s.json'%tag
  subprocess.run([N+'/node_modules/.bin/vitest','run','--root',N,'src/__tests__/ks1868-blockchain-verifier-unreadable-throw.test.ts','--reporter=json','--outputFile='+out],capture_output=True)
  d=json.load(open(out)); red=[]
  for f in d['testResults']:
    for a in f['assertionResults']:
      if a['status']!='passed': red.append(a['title'].split(':')[0].replace('control ks1868 ','').replace('RED ks1868 ',''))
    if not f['assertionResults'] and f['status']!='passed': red.append('SUITE')
  return red
print('head red',run('head'))
for k,(a,b) in M.items():
  m=orig.replace(a,b)
  assert m!=orig
  open(F,'w').write(m)
  try: r=run(k)
  finally: open(F,'w').write(orig)
  assert sha(open(F).read())==sha(orig)
  print(k,'sha',sha(m),'red',r if r else 'SURVIVED')
print('RESTORE_OK',sha(orig))
