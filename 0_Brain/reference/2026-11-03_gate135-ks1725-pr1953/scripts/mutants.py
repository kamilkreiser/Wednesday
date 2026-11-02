# Gate 135 mutants: product files only, tests untouched; each mutant = exact replacement(s), run cells, restore, sha256 assert.
import subprocess, hashlib, json, sys, os, re, time
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate135-ks1725-pr1953'; R=G+'/repo'; D=R+'/Blockchain/Dev'
C='packages/shared/src/validation/zod3-compat.ts'
def sh(cmd, log):
    with open(log,'w') as f: p=subprocess.run(cmd, shell=True, stdout=f, stderr=subprocess.STDOUT, executable='/bin/bash'); return p.returncode
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def tally(log):
    t=open(log,errors='replace').read()
    m=re.findall(r'Tests:?\s+(.*)',t); return (m[-1].strip() if m else 'NO-TALLY')[:90]
CELLS={
 'S': f"npm --prefix {D}/packages/shared run test -- src/__tests__/ks1725-zod3-compat.test.ts",
 'GOV': f"npm --prefix {D}/services/governance run test -- src/__tests__/ks1725-governance-zod-catches-keep-zod3-details.test.ts",
 'SS': f"npm --prefix {D}/services/shared run test -- --run src/__tests__/ks1725-accept-terms-literal-keeps-zod3-issue.test.ts",
 'TS': f"npm --prefix {D}/services/timestamping run test -- --run src/__tests__/ks1725-hash-pattern-text-and-case-insensitive.test.ts",
 'KYC': f"npm --prefix {D}/services/kyc run test -- --run src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts",
 'AUTH': f"npm --prefix {D}/services/auth run test -- --run",
 'SHAREDALL': f"npm --prefix {D}/packages/shared run test",
}
BUILD=f"npm --prefix {D}/packages/shared run build"
MUT=[
 ('M1 global error map dropped (no install call)', [(C, "\ninstallZod3IssueCompat();\n", "\n")], ['S','GOV','SS']),
 ('M1b map installed but returns undefined', [(C, "z.config({ customError: (iss) => zod3Annotate(iss as unknown as Raw) });", "z.config({ customError: (iss) => (void iss, undefined) });")], ['S','GOV','SS']),
 ('M2 datetime helper dropped (zod 4 native .datetime)', [(C, "  return z.stringFormat('datetime', (value: string) => re.test(value), options.message === undefined ? undefined : { error: options.message });", "  void re; return z.string().datetime({ offset: options.offset ?? false, local: options.local ?? false, precision: options.precision ?? undefined, message: options.message });")], ['S']),
 ('M3b users.ts:778 .guid() -> .uuid()', [('services/auth/src/routes/users.ts', "if (!z.string().guid().safeParse(id).success) {", "if (!z.string().uuid().safeParse(id).success) {")], ['S','AUTH']),
 ('M4a serializer: too_small key order (type before minimum)', [(C, "return { code: 'too_small', minimum: i.minimum, type: zod3Type(i.origin),", "return { code: 'too_small', type: zod3Type(i.origin), minimum: i.minimum,")], ['S','GOV']),
 ('M4b serializer: invalid_format keeps zod 4 code', [(C, "? { code: 'invalid_string', validation, message, path }\n        : { validation, code: 'invalid_string', message, path };", "? { code: 'invalid_format', validation, message, path }\n        : { validation, code: 'invalid_format', message, path };")], ['S','GOV']),
 ('M4c serializer: union branch paths not prefixed', [(C, "issues: zod3Issues(branch, path), name: 'ZodError'", "issues: zod3Issues(branch), name: 'ZodError'")], ['S']),
 ('M4d serializer: enum drops received', [(C, "return { received: i.received, code: 'invalid_enum_value', options: i.values, path, message };", "return { code: 'invalid_enum_value', options: i.values, path, message };")], ['S','GOV']),
 ('M4e serializer: guid validation name leaks', [(C, "{ guid: 'uuid', uuid: 'uuid',", "{ guid: 'guid', uuid: 'uuid',")], ['S']),
 ('M4f serializer: datetime key order', [(C, "new Set(['datetime', 'starts_with',", "new Set(['starts_with',")], ['S']),
 ('M5 governance vote catch back to error.errors (red-first proxy)', [('services/governance/src/routes/governance.ts', "message: 'Validation failed', details: zod3Issues(error.issues) } });", "message: 'Validation failed', details: error.errors } });")], ['GOV']),
]
if len(sys.argv)>1 and sys.argv[1]=='--uuid-all':
    MUT=[('M3a every product .guid( -> .uuid(', 'SEDALL', ['S','AUTH','KYC'])]
before={}
res=[]
for name, edits, cells in MUT:
    files = []
    if edits=='SEDALL':
        out=subprocess.run(['git','-C',R,'grep','-l','\\.guid(','HEAD','--','Blockchain/Dev/services/*/src/**','Blockchain/Dev/packages/shared/src/**',':!*__tests__*',':!*zod3-compat.ts'],capture_output=True,text=True).stdout.split()
        files=[f.split(':',1)[1].replace('Blockchain/Dev/','') for f in out]
        edits=[(f,'.guid(','.uuid(') for f in files]
    paths=sorted({D+'/'+f for f,_,_ in edits})
    h0={p:sha(p) for p in paths}
    nrep=0
    for f,a,b in edits:
        p=D+'/'+f; s=open(p).read()
        if name.startswith('M3a'): n=s.count(a); s=s.replace(a,b)
        elif name.startswith('M5'): n=1 if a in s else 0; s=s.replace(a,b,1)
        else: n=s.count(a); s=s.replace(a,b)
        assert n>=1, (name,f,'anchor not found'); nrep+=n; open(p,'w').write(s)
    compat_touched = any(p.endswith('zod3-compat.ts') for p in paths) or name.startswith('M3a')
    if compat_touched or name.startswith('M3a'): sh(BUILD, G+'/logs/mut_build.log')
    row={'mutant':name,'replacements':nrep,'cells':{}}
    for c in cells:
        log=G+'/logs/mut_%s_%s.log'%(re.sub(r'\W+','_',name.split(' ')[0]),c)
        rc=sh(CELLS[c],log); row['cells'][c]=('RED' if rc!=0 else 'green')+' rc=%d '%rc+tally(log)
    subprocess.run(['git','-C',R,'checkout','--']+paths)
    ok=all(sha(p)==h0[p] for p in paths)
    if compat_touched: sh(BUILD, G+'/logs/mut_build_restore.log')
    st=subprocess.run(['git','-C',R,'status','--porcelain','--untracked-files=no'],capture_output=True,text=True).stdout.strip()
    row['RESTORE_OK']=ok and st==''
    row['killed']=any(v.startswith('RED') for v in row['cells'].values())
    res.append(row); print(json.dumps(row), flush=True)
json.dump(res,open(G+'/logs/mutants%s.json'%('_uuid' if len(sys.argv)>1 else ''),'w'),indent=1)
