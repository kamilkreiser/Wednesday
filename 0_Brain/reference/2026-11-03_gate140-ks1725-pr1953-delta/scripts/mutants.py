# Gate 140: mutants on the FIX lines only (a6e0fb3c81f2), product only, tests untouched. Each mutant is an exact
# one-occurrence replacement (or a line-number replacement); the file's ORIGINAL BYTES are written back and sha256
# asserted equal, and `git status --porcelain` must be empty after every restore. packages/shared rebuilt around
# compat mutants. argv: [mutant ids...] ; special id REDFIRST = the three product files at ea6d924eb5de.
import hashlib, json, subprocess, sys, os
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate140-ks1725-pr1953-delta'; R=G+'/repo'; D=R+'/Blockchain/Dev'; L=G+'/logs'
C='packages/shared/src/validation/zod3-compat.ts'; NFT='services/nft-certificate/src/routes/nft.routes.ts'; VC='services/vc-issuer/src/routes/credentials.ts'
COMPAT=['shared:src/__tests__/ks1725-zod3-compat.test.ts']
M={
 'MF1a': (C, "{ error: (iss) => (iss.code === 'invalid_format' ? message : undefined) }", "{ error: message }", COMPAT, 'F1 fix reverted (message on every issue)'),
 'MF1b': (C, "iss.code === 'invalid_format' ? message", "iss.code !== 'invalid_format' ? message", COMPAT, 'F1 condition inverted'),
 'MF2a': (C, "  if (failed.length === 0) return out;\n", "  return out;\n", COMPAT, 'F2 post-pass disabled'),
 'MF2b': (C, "i.code === 'invalid_type' && i.expected !== 'integer'", "i.code === 'invalid_type'", COMPAT, 'F2: the .int() exclusion removed'),
 'MF2c': (C, "!(isLength(i) && failed", "!(i.code === 'too_small' && failed", COMPAT, 'F2 drops too_small only (too_big kept)'),
 'MF3a': (C, "if (to !== -1 && to < from) {", "if (false) {", COMPAT, 'F3 post-pass disabled'),
 'MF3b': (C, "if (!isLength(issue) || issue.type !== 'array') continue;", "if (!isLength(issue)) continue;", COMPAT, 'F3 also moves non-array length issues'),
 'MF3c': (C, "return arrayLengthFirst(dropLengthAfterTypeFailure(issues.map((i) => toZod3(i as Raw, prefix))));", "return dropLengthAfterTypeFailure(arrayLengthFirst(issues.map((i) => toZod3(i as Raw, prefix))));", COMPAT, 'pass order swapped (F3 then F2)'),
 'MF3d': (C, "issues: zod3Issues(branch, path)", "issues: branch.map((b) => toZod3(b as Raw, path))", COMPAT, 'post-passes NOT applied inside union branches'),
 'MF3e': (C, "q.length > p.length && p.every", "q.length >= p.length && p.every", COMPAT, 'strictlyUnder admits the same path'),
 'MF3f': (C, "list.splice(to, 0, issue);", "list.splice(to + 1, 0, issue);", COMPAT, 'F3 inserts one place late'),
 'MF4a': (C, "      raw.zod3NativeEnum = true;\n", "", COMPAT, 'F4 helper does not mark the issue'),
 'MF4b': (C, " && !Number.isNaN(iss.input)", "", COMPAT, 'F4 NaN guard removed'),
 'MF4c': (C, "      return zod3Annotate(raw);\n    },\n  });", "      return undefined;\n    },\n  });", COMPAT, 'F4 helper error fn returns undefined'),
 'MF4d': (C, "typeof iss.input === 'number' && !Number.isNaN", "typeof iss.input !== 'string' && !Number.isNaN", COMPAT, 'F4 rule over-reaches to every non-string'),
 'MF4e': (NFT, 34, "  storageTier: z.nativeEnum(StorageTier),", COMPAT+['svc:services/nft-certificate'], 'site nft.routes.ts:34 back to raw z.nativeEnum'),
 'MF4f': (VC, 39, "  documentType: z.nativeEnum(SecuuraCredentialType),", COMPAT+['svc:services/vc-issuer'], 'site credentials.ts:39 back to raw z.nativeEnum'),
}
sha=lambda b: hashlib.sha256(b).hexdigest()
def sh(cmd, log):
    with open(log,'w') as f: return subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT).returncode
def build(tag): return sh(['npm','--prefix',D+'/packages/shared','run','build'], L+'/mut_build_%s.log'%tag)
def run_tests(tests, tag):
    res=[]
    for t in tests:
        kind,arg=t.split(':',1)
        if kind=='shared': rc=sh(['npm','--prefix',D+'/packages/shared','run','test','--',arg], L+'/mut_%s_shared.log'%tag); log=L+'/mut_%s_shared.log'%tag
        else: n=arg.split('/')[-1]; rc=sh(['npm','--prefix',D+'/'+arg,'run','test'], L+'/mut_%s_%s.log'%(tag,n)); log=L+'/mut_%s_%s.log'%(tag,n)
        tl=[l.strip() for l in open(log, errors='replace') if l.strip().startswith('Tests ')]
        res.append({'test':t,'rc':rc,'tests':tl[-1] if tl else None})
    return res
def status(): return subprocess.run(['git','-C',R,'status','--porcelain'],capture_output=True,text=True).stdout
out=json.load(open(L+'/mutants.json')) if os.path.exists(L+'/mutants.json') else {}
for mid in sys.argv[1:]:
    assert status()=='', 'tree not clean before '+mid
    if mid=='REDFIRST':
        files=[C,NFT,VC]; orig={f:open(D+'/'+f,'rb').read() for f in files}
        for f in files:
            old=subprocess.run(['git','-C',R,'show','ea6d924eb5de:Blockchain/Dev/'+f],capture_output=True).stdout; assert old
            open(D+'/'+f,'wb').write(old)
        tests=COMPAT+['auth:services/auth']; desc='the three product files at ea6d924eb5de (unfixed), tests at head'
        tests=[t if not t.startswith('auth:') else 'svcf:services/auth' for t in tests]
    else:
        f,old,new,tests,desc=M[mid]; files=[f]; orig={f:open(D+'/'+f,'rb').read()}
        txt=orig[f].decode()
        if isinstance(old,int):
            lines=txt.split('\n'); assert 'zod3NativeEnum(' in lines[old-1], lines[old-1]; lines[old-1]=new; txt2='\n'.join(lines)
        else:
            assert txt.count(old)==1, (mid, txt.count(old)); txt2=txt.replace(old,new)
        open(D+'/'+f,'wb').write(txt2.encode())
    shared_touched=any(x.startswith('packages/shared') for x in files)
    brc=build(mid) if shared_touched else None
    if mid=='REDFIRST':
        res=run_tests(COMPAT, mid)
        rc=sh(['npm','--prefix',D+'/services/auth','run','test','--','--run','ks1725-guid-acceptance-patch-route'], L+'/mut_REDFIRST_auth_guid.log')
        tl=[l.strip() for l in open(L+'/mut_REDFIRST_auth_guid.log',errors='replace') if l.strip().startswith('Tests ')]
        res.append({'test':'auth ks1725-guid-acceptance-patch-route','rc':rc,'tests':tl[-1] if tl else None})
    else: res=run_tests(tests, mid)
    for f in files: open(D+'/'+f,'wb').write(orig[f])
    ok=all(sha(open(D+'/'+f,'rb').read())==sha(orig[f]) for f in files) and status()==''
    rb=build(mid+'_restore') if shared_touched else None
    out[mid]={'desc':desc,'files':files,'build_rc':brc,'results':res,'restore_sha256_equal_and_clean':ok,'rebuild_rc':rb}
    print(mid, desc, json.dumps(res), 'RESTORE_OK' if ok else 'RESTORE_FAILED', flush=True)
    json.dump(out,open(L+'/mutants.json','w'),indent=1)
    if not ok: sys.exit('restore failed at '+mid)
