import sys,subprocess,hashlib,json,os
G=sys.argv[1]; A=G+'/repo/Blockchain/Dev/services/auth'; F=A+'/src/routes/oauth.ts'; V=G+'/repo/Blockchain/Dev/node_modules/.bin/vitest'; T=G+'/repo/Blockchain/Dev/node_modules/.bin/tsc'
SEAT='src/__tests__/ks1797-authorize-post-refuses-an-array-state-or-code-challenge.test.ts'
src=open(F).read(); sha=hashlib.sha256(src.encode()).hexdigest()
GUARD="    if ((state !== undefined && typeof state !== 'string') || (code_challenge !== undefined && typeof code_challenge !== 'string')) {\n      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_request', description: 'state and code_challenge must each be a single string' } });\n    }\n"
PRED="(state !== undefined && typeof state !== 'string') || (code_challenge !== undefined && typeof code_challenge !== 'string')"
i=src.index('// KS-1797 (POST half)'); j=src.index(GUARD,i); assert src.count(GUARD)==2; k=j+len(GUARD)
def repl_pred(new): return src[:j]+GUARD.replace(PRED,new)+src[k:]
def moved(anchor):
    s=src[:j]+src[k:]; assert s.count(anchor)==1,anchor; return s.replace(anchor,anchor+GUARD)
DENY_END="      return respondAuthorizeRedirect(req, res, denyUrl.toString()); // KS-799\n    }\n"
LOOKUP_END="    if (!client.ok) return authorizeRefusal(res, client);\n"
M={
 'S1_approve_only':(repl_pred("action !== 'deny' && ("+PRED+")"),'P1,P4,P6 (the deny cells)'),
 'S2_isArray':(repl_pred("(state !== undefined && Array.isArray(state)) || (code_challenge !== undefined && Array.isArray(code_challenge))"),'P5 (object state)'),
 'S3_state_clause_dropped':(repl_pred("(code_challenge !== undefined && typeof code_challenge !== 'string')"),'P1,P2,P5,P6,P7'),
 'S4_or_to_and':(repl_pred("(state !== undefined && typeof state !== 'string') && (code_challenge !== undefined && typeof code_challenge !== 'string')"),'P1..P7'),
 'G1_after_deny_branch':(moved(DENY_END),'P1,P4,P6'),
 'G2_after_client_lookup':(moved(LOOKUP_END),'P1,P4,P6 by redirect; P2,P3,P5,P7? by getAppByClientId count (P7 asserts status only, so P7 stays green)'),
 'G3_loose_null_admitted':(repl_pred("(state != null && typeof state !== 'string') || (code_challenge != null && typeof code_challenge !== 'string')"),'NONE predicted: no seat cell sends null'),
 'G4_typeof_object_scalars_admitted':(repl_pred("(state !== undefined && typeof state === 'object') || (code_challenge !== undefined && typeof code_challenge === 'object')"),'NONE predicted: no seat cell sends a number or boolean'),
}
out=[]
try:
  for n,(m,pred) in M.items():
    assert m!=src
    open(F,'w').write(m)
    tsc=subprocess.run([T,'--noEmit','-p',A],capture_output=True,text=True).returncode
    jf=f'{G}/evidence/mut_{n}.json'
    r=subprocess.run([V,'run','--root',A,SEAT,'--reporter=json','--outputFile='+jf],capture_output=True,text=True)
    d=json.load(open(jf))
    a=d['testResults'][0]['assertionResults']
    red=[x['title'].split(' ')[2] for x in a if x['status']=='failed']
    line=f"{n}: tsc rc={tsc}; predicted red: {pred}; seat file {len(a)-len(red)} of {len(a)} pass; RED={red} {'SURVIVED' if not red else 'KILLED'}"
    print(line,flush=True); out.append(line)
    if n.startswith('G3') or n.startswith('G4'):
      o=f'{G}/evidence/table_{n}.jsonl'; open(o,'w').close()
      subprocess.run([V,'run','--root',A,'src/__tests__/gate212-table.test.ts'],env={**os.environ,'GATE_OUT':o},capture_output=True,text=True)
finally:
  open(F,'w').write(src)
print('restored',hashlib.sha256(open(F).read().encode()).hexdigest()==sha,sha)
