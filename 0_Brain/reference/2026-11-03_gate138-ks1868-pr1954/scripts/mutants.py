import re, subprocess, json, hashlib
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate138-ks1868-pr1954'
A=W+'/repo/Blockchain/Dev/services/api-gateway'
F=A+'/src/routes/admin.ts'
orig=open(F).read(); sha=lambda s: hashlib.sha256(s.encode()).hexdigest()[:12]
pat=re.compile(r"(?P<i>[ ]*)let reason: string;\n(?P=i)try \{\n(?P=i)  reason = (?P<x>String\([^\n]+\));\n(?P=i)\} catch \{\n(?P=i)  reason = 'unreadable thrown value';\n(?P=i)\}\n")
ms=list(pat.finditer(orig)); assert len(ms)==10, len(ms)
names=['integ_test','seed','id_users','id_orgs','id_level','org_post','org_put','forward','org_delete','audit_export']
def mut(m,form):
    i=m.group('i'); x=m.group('x')
    if form=='undo': rep=m.group(0).replace(x, x[len('String('):-1])
    elif form=='const': rep="%sconst reason = 'x';\n"%i
    elif form=='rethrow': rep=m.group(0).replace("reason = 'unreadable thrown value';","throw new Error('rethrown');")
    elif form=='wrongconst': rep=m.group(0).replace("'unreadable thrown value'","'redacted'")
    return orig[:m.start()]+rep+orig[m.end():]
T=['ks1868-admin-forward-export-message-coercion','ks1868-admin-identity-routes-message-coercion','ks1868-admin-identity-seed-message-coercion','ks1868-admin-organization-message-coercion']
def run(tag):
  out=W+'/logs/mut_%s.json'%tag
  subprocess.run([W+'/repo/Blockchain/Dev/node_modules/.bin/vitest','run','--root',A,*T,'--reporter=json','--outputFile='+out],capture_output=True)
  d=json.load(open(out)); red=[]
  for f in d['testResults']:
    for a in f['assertionResults']:
      if a['status']!='passed': red.append(a['title'][:40])
  return red,d['numTotalTests']
print('head red',run('head'))
for k,m in enumerate(ms):
  for form in ['undo','const','rethrow','wrongconst']:
    mm=mut(m,form); assert mm!=orig
    open(F,'w').write(mm)
    try: r=run('%s_%s'%(names[k],form))
    finally: open(F,'w').write(orig)
    assert sha(open(F).read())==sha(orig)
    print(names[k],form,'sha',sha(mm),'red %d of %d'%(len(r[0]),r[1]) if r[0] else 'SURVIVED', r[0][:3],flush=True)
print('RESTORE_OK',sha(orig))
