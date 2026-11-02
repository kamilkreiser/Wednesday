# Per-site mutants on the PR's changed lines only (product files), tests untouched, sha256-restored after every run.
import subprocess, hashlib, re, sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate112-ks1868-pr1930'
A=G+'/repo/Blockchain/Dev/services/security/src'
HEAD={'index.ts':open(G+'/logs/index_head.ts').read(),'db.ts':open(G+'/logs/db_head.ts').read()}
sha=lambda s: hashlib.sha256(s.encode()).hexdigest()
T='src/__tests__/ks1868-security-'
GUARD_SITES={  # label: (file, unique text of the line after the guard, test file)
 'S1_runDbReadyHook':('db.ts',"dbLog('error', 'DB ready boot work failed', { error: reason });",'db-probe-and-hook-catches-unreadable-throw'),
 'S2_probeDb':('db.ts',"return { ok: false, error: reason };",'db-probe-and-hook-catches-unreadable-throw'),
 'S3_dbSaveAuditLog':('index.ts',"logger.error('DB save audit log failed', { error: reason });",'audit-and-event-save-catches-unreadable-throw'),
 'S4_dbSaveSecurityEvent':('index.ts',"logger.error('DB save event failed', { error: reason });",'audit-and-event-save-catches-unreadable-throw'),
 'S5_dbSaveApiKey':('index.ts',"logger.error('DB save API key failed', { error: reason });\n    // KS-888",'save-api-key-catch-unreadable-throw'),
 'S6_dbRecordApiKeyUsage':('index.ts',"logger.error('DB save API key failed', { error: reason });\n  }\n}",'validate-route-catches-unreadable-throw'),
 'S8_validate_storedRead':('index.ts',"logger.error('KS-1370: stored API key state could not be read', { error: reason });",'validate-route-catches-unreadable-throw'),
 'S9_validate_lookup':('index.ts',"logger.warn('DB fallback for api-key validation failed', { error: reason });",'validate-route-catches-unreadable-throw'),
}
def guard_block(src, after):
    j=src.index(after); assert src.count(after)==1,(after,src.count(after))
    i=src.rindex('let reason: string;',0,j); i=src.rindex('\n',0,i)+1
    return i,j
def mut_guard(src, after, m):
    i,j=guard_block(src,after); blk=src[i:j]; tail=src[j:]
    if m=='M0_revert':
        nb=re.sub(r"[ ]*let reason: string;\n[ ]*try \{\n[ ]*reason = err\?\.message;\n[ ]*\} catch \{\n[ ]*reason = 'unreadable thrown value';\n[ ]*\}\n",'',blk,count=1)
        assert nb!=blk
        tail=after.replace('error: reason','error: err?.message')+src[j+len(after):]
    elif m=='M1_constant_for_all': nb=blk.replace('reason = err?.message;',"reason = 'unreadable thrown value';")
    elif m=='M2_fallback_String_err': nb=blk.replace("reason = 'unreadable thrown value';",'reason = String(err);')
    elif m=='M3_inner_rethrow': nb=blk.replace("reason = 'unreadable thrown value';",'throw err;')
    elif m=='M4_fallback_text_x': nb=blk.replace("reason = 'unreadable thrown value';","reason = 'x';")
    else: raise SystemExit(m)
    out=src[:i]+nb+tail
    assert out!=src,(after,m)
    return out
S7_NEW="""    let isZod: boolean;
    try {
      isZod = error instanceof z.ZodError;
    } catch {
      return next(new Error('unreadable thrown value'));
    }
    if (isZod) return badRequestFromZod(res, error as z.ZodError);
"""
S7={'M0_revert':"    if (error instanceof z.ZodError) return badRequestFromZod(res, error);\n",
    'M1_next_raw_error':S7_NEW.replace("return next(new Error('unreadable thrown value'));","return next(error);"),
    'M2_swallow_isZod_false':S7_NEW.replace("return next(new Error('unreadable thrown value'));","isZod = false;"),
    'M3_inner_rethrow':S7_NEW.replace("return next(new Error('unreadable thrown value'));","throw error;"),
    'M4_answers_400':S7_NEW.replace("return next(new Error('unreadable thrown value'));","return res.status(400).json({ success: false });"),
    'M5_error_text_x':S7_NEW.replace("new Error('unreadable thrown value')","new Error('x')")}
runs=[]
for site,(f,after,tf) in GUARD_SITES.items():
    for m in ['M0_revert','M1_constant_for_all','M2_fallback_String_err','M3_inner_rethrow','M4_fallback_text_x']:
        runs.append((site,m,f,tf,lambda s,after=after,m=m: mut_guard(s,after,m)))
for m,txt in S7.items():
    def fn(s,txt=txt):
        assert s.count(S7_NEW)==1; return s.replace(S7_NEW,txt)
    runs.append(('S7_adminScopesGet',m,'index.ts','admin-scopes-get-catch-unreadable-throw',fn))
only=sys.argv[1:] 
killed=surv=0
for site,m,f,tf,fn in runs:
    if only and site not in only: continue
    P=A+'/'+f; src=HEAD[f]; out=fn(src)
    open(P,'w').write(out)
    log=f'{G}/logs/mut_{site}__{m}.log'
    r=subprocess.run(['bash',G+'/scripts/vt.sh',log,T+tf+'.test.ts'],capture_output=True,text=True)
    open(P,'w').write(src); ok=sha(open(P).read())==sha(src)
    t=open(log).read()
    summ=(re.findall(r'Tests\s+(.*)',t) or ['?'])[-1].strip()
    cells=sorted(set(re.findall(r'(?:RED|CONTROL|ks1868) ks1868 ([CR]\d+)|ks1868 ([CR]\d+)',' '.join(l for l in t.splitlines() if '×' in l or 'FAIL' in l))))
    cells=sorted(set(a or b for a,b in cells))
    st='KILLED' if r.returncode!=0 else 'SURVIVED'
    killed+=st=='KILLED'; surv+=st=='SURVIVED'
    print(site,m,st,summ,'cells',cells,'restore',ok,flush=True)
print('killed',killed,'survived',surv)
