import sys,subprocess,hashlib,json,os
D=sys.argv[1]
V=f"{D}/repo/Blockchain/Dev/services/vc-issuer"; F=f"{V}/src/routes/status.ts"
VT=f"{D}/repo/Blockchain/Dev/node_modules/.bin/vitest"
orig=open(F).read(); osha=hashlib.sha256(orig.encode()).hexdigest()
M={
 'M1_check_removed_on_revoke':[("    await refuseUnlessCallerMayChange(req, credentialId);\n\n    // KS-444/KS-445: revoking","    // KS-444/KS-445: revoking")],
 'M6_refusal_403':[("    throw new AppError('Credential not found in status list', 404);\n  }\n}","    throw new AppError('Credential not found in status list', 403);\n  }\n}")],
 'M8_ownerless_admitted_to_anyone':[("if (!record || !mayReadCredential(req, record.owner))","if (!record || (record.owner.userId !== null && !mayReadCredential(req, record.owner)))")],
 'M10_exemption_every_POST':[("&& CREATOR_BOUND_WRITE.test(path)) {","&& (CREATOR_BOUND_WRITE.test(path) || true)) {")],
 'G1_own_mayRead_not_KS1906':[("import { mayReadCredential } from '../ownership';","import { mayReadCredential, mayRead } from '../ownership';"),("if (!record || !mayReadCredential(req, record.owner))","if (!record || !mayRead(req, record.owner))")],
 'G2_own_widen_to_any_POST_id_verb':[("const CREATOR_BOUND_WRITE = /^\\/[^/]+\\/(?:revoke|unrevoke)\\/?$/i;","const CREATOR_BOUND_WRITE = /^\\/[^/]+\\/[^/]+\\/?$/i;")],
}
def table(path):
  out={}
  for l in open(path):
    r=json.loads(l); k=(r['kind'],r.get('op') or r.get('name'),r.get('cred',''),r['caller'])
    out[k]=(r['status'],r['writes'], r['body'] if r['kind']=='cell' and r['status']>=400 else '')
  return out
headT=table(f"{D}/evidence/authz_repo.jsonl")
res=[]
for name,reps in M.items():
  s=orig
  for a,b in reps:
    assert s.count(a)==1,(name,a,s.count(a)); s=s.replace(a,b)
  open(F,'w').write(s)
  try:
    out=f"{D}/evidence/mut_{name}.jsonl"; open(out,'w').close()
    env=dict(os.environ,GATE_OUT=out)
    r1=subprocess.run([VT,'run','--root',V,'--testTimeout','60000','src/__tests__/gate208-authz.test.ts'],env=env,capture_output=True,text=True)
    r2=subprocess.run([VT,'run','--root',V,'--testTimeout','60000','src/__tests__/ks692-status-revoke-and-unrevoke-bound-to-the-creator.test.ts'],capture_output=True,text=True)
    open(f"{D}/evidence/mut_{name}_seatfile.log",'w').write(r2.stdout+r2.stderr)
    mt=table(out)
    diffs=[(k,headT.get(k),mt.get(k)) for k in set(headT)|set(mt) if headT.get(k)!=mt.get(k)]
    seat=[l.strip() for l in (r2.stdout).splitlines() if l.strip().startswith('Tests ')]
    res.append((name,len(diffs),seat,diffs[:4]))
  finally:
    open(F,'w').write(orig)
  assert hashlib.sha256(open(F).read().encode()).hexdigest()==osha
for name,n,seat,ex in res:
  print(f"{name}: my-table cells differing from head = {n}; seat ks692 file: {seat}")
  for e in ex: print("    ",e)
print("restored sha256 equal:",osha)
