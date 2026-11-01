# Each mutant applied to ONE site of the product file only; tests untouched; sha restored and checked after each run.
import subprocess,hashlib,re,sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate94-ks1868-pr1912'
M=G+'/repo/Blockchain/Dev/services/security/src/index.ts'
HEAD=open(G+'/logs/head_index.ts').read()
sha=lambda s: hashlib.sha256(s.encode()).hexdigest()
H=sha(HEAD)
MINT='KS-888: API key mint refused'; REVOKE='KS-888: API key revoke not stored'
def site_block(src, anchor_after, start_marker, ind):
    # the guard block that ends just before the log line carrying anchor_after
    j=src.index(anchor_after); i=src.rindex(' '*ind+start_marker, 0, j)
    k=src.index('\n', j)+1
    return i,k
def guard_mut(src, anchor, m):
    ind=6 if anchor==MINT else 4
    i,k=site_block(src, anchor, 'let infra = false;', ind); b=src[i:k]; p=' '*ind
    if m=='M0_revert': nb=f"{p}const infra = isInfrastructureDbError(saveErr);\n" + b[b.index(p+"log('error'"):].replace('code, infra }','code: saveErr?.code, infra }')
    elif m=='M1_drop_inner_try': nb=f"{p}const infra = isInfrastructureDbError(saveErr);\n{p}const code: unknown = saveErr?.code;\n" + b[b.index(p+"log('error'"):]
    elif m=='M2_catch_rethrows': nb=b.replace('} catch {\n', '} catch (e) {\n'+p+'  throw e;\n',1)
    elif m=='M3_catch_marks_infra': nb=b.replace('} catch {\n', '} catch {\n'+p+'  infra = true;\n',1)
    elif m=='M4_log_thrown_object': nb=b.replace('{ keyId: apiKey.id, code, infra }','{ keyId: apiKey.id, code, infra, error: saveErr }')
    elif m=='M5_log_removed': nb=b[:b.index(p+"log('error'")]
    else: raise SystemExit(m)
    assert nb!=b,(anchor,m); return src[:i]+nb+src[k:]
SC_OLD="""      // A thrown value that cannot be read cannot be classified: hand the error handler an ordinary Error, as for any non-infrastructure error.
      return next(new Error('unreadable thrown value'));"""
def scope_mut(src,m):
    assert src.count(SC_OLD)==1
    if m=='M0_revert':
        i=src.index("    let isZod = false;\n    let infra = false;\n"); k=src.index("    if (isZod) return badRequestFromZod(res, error as z.ZodError);\n")+len("    if (isZod) return badRequestFromZod(res, error as z.ZodError);\n")
        s=src[:i]+"    if (error instanceof z.ZodError) return badRequestFromZod(res, error);\n"+src[k:]
        return s.replace("    if (infra) {\n      // Read off the request","    if (isInfrastructureDbError(error)) {\n      // Read off the request",1)
    if m=='M1_next_raw_value': return src.replace(SC_OLD,"      return next(error);")
    if m=='M2_catch_rethrows': return src.replace(SC_OLD,"      throw new Error('unreadable thrown value');")
    if m=='M3_catch_falls_to_infra': return src.replace(SC_OLD,"      infra = true;")
    if m=='M4_zod_probe_dropped': return src.replace("      isZod = error instanceof z.ZodError;\n","",1)
    if m=='M5_zod_branch_dropped': return src.replace("    if (isZod) return badRequestFromZod(res, error as z.ZodError);\n","",1)
    if m=='M6_catch_answers_400': return src.replace(SC_OLD,"      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'x' } });")
    raise SystemExit(m)
GM=['M0_revert','M1_drop_inner_try','M2_catch_rethrows','M3_catch_marks_infra','M4_log_thrown_object','M5_log_removed']
SM=['M0_revert','M1_next_raw_value','M2_catch_rethrows','M3_catch_falls_to_infra','M4_zod_probe_dropped','M5_zod_branch_dropped','M6_catch_answers_400']
plan=[('register',m) for m in GM]+[('revoke',m) for m in GM]+[('scopes',m) for m in SM]
only=sys.argv[1:]
FILES=['ks1868-security-key-register-save','ks1868-security-key-revoke-save','ks1868-security-admin-scopes-put']
for site,m in plan:
    tag=f'{site}__{m}'
    if only and tag not in only: continue
    src=guard_mut(HEAD,MINT if site=='register' else REVOKE,m) if site!='scopes' else scope_mut(HEAD,m)
    assert src!=HEAD
    open(M,'w').write(src)
    log=f'{G}/logs/mut_{tag}.log'
    args=['bash',G+'/scripts/vt.sh',log]+([] if '--whole' in only else FILES)
    r=subprocess.run(args,capture_output=True,text=True)
    open(M,'w').write(HEAD); ok=sha(open(M).read())==H
    t=open(log).read()
    summ=(re.findall(r'Tests\s+(.*)',t) or ['?'])[-1].strip()
    cells=sorted(set(re.findall(r'(C\d|R\d) ',' '.join(l for l in t.splitlines() if l.strip().startswith('×')))))
    files=sorted(set(re.findall(r'FAIL\s+src/__tests__/(ks1868-security-[a-z-]+)\.test\.ts',t)))
    kinds=sorted(set(re.findall(r'^(AssertionError|TypeError|Error)\b',t,flags=re.M)))
    st='KILLED' if r.returncode!=0 else 'SURVIVED'
    print(tag,st,summ,'cells',cells,'files',[f.replace('ks1868-security-','') for f in files],'kinds',kinds,'restore',ok,flush=True)
