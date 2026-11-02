# Each mutant at ONE site of the product only; tests untouched; sha256 restored and checked after each run.
import subprocess,hashlib,re
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate103-ks1868-pr1921'
M=G+'/repo/Blockchain/Dev/services/kyc/src/index.ts'
HEAD=open(G+'/logs/head_index.ts').read(); sha=lambda s: hashlib.sha256(s.encode()).hexdigest(); H=sha(HEAD)
SITES={'P1_dbSaveImage':("err instanceof Error ? err.message : String(err)","logger.error('DB save image failed', { error: reason });"),
       'P2_verifyDbReady':("err?.message","logger.warn('KYC DB verification query failed', { error: reason });")}
def guard(expr,p='    '): return f"{p}let reason: string;\n{p}try {{\n{p}  reason = {expr};\n{p}}} catch {{\n{p}  reason = 'unreadable thrown value';\n{p}}}\n"
def mut(site,m):
    expr,logl=SITES[site]; g=guard(expr); assert HEAD.count(g+'    '+logl)==1,(site,)
    i=HEAD.index(g+'    '+logl); k=i+len(g)+4+len(logl)+1; block=HEAD[i:k]
    if m=='M0_revert': nb='    '+logl.replace('error: reason',f'error: {expr}')+'\n'
    elif m=='M1_drop_inner_try': nb=f"    const reason: string = {expr};\n    {logl}\n"
    elif m=='M2_constant_to_reread': nb=block.replace("reason = 'unreadable thrown value';",f"reason = String({expr});" if site=='P1_dbSaveImage' else "reason = err?.message;")
    elif m=='M3_rethrow_only_unreadable': nb=block.replace("reason = 'unreadable thrown value';","throw err;")
    elif m=='M4_constant_for_all': nb=block.replace(f"reason = {expr};","reason = 'unreadable thrown value';")
    elif m=='M5_rethrow_all_after_log': nb=block+"    throw err;\n"
    elif m=='M6_nonError_branch_x': nb=block.replace(f"reason = {expr};","reason = err instanceof Error ? err.message : 'x';")
    elif m=='M7_log_removed': nb=g
    else: raise SystemExit(m)
    assert nb!=block; return HEAD[:i]+nb+HEAD[k:]
MUTS={'P1_dbSaveImage':['M0_revert','M1_drop_inner_try','M2_constant_to_reread','M3_rethrow_only_unreadable','M4_constant_for_all','M5_rethrow_all_after_log','M6_nonError_branch_x','M7_log_removed'],
      'P2_verifyDbReady':['M0_revert','M1_drop_inner_try','M2_constant_to_reread','M3_rethrow_only_unreadable','M4_constant_for_all','M5_rethrow_all_after_log','M7_log_removed']}
assert sha(open(M).read())==H
k=s=0
for site,ms in MUTS.items():
    for m in ms:
        open(M,'w').write(mut(site,m)); log=f'{G}/logs/mut_{site}__{m}.log'
        r=subprocess.run(['bash',G+'/scripts/vt.sh',log,'ks1868-kyc-save-image-attestation','ks1868-kyc-verify-db-ready-boot-probe'],capture_output=True,text=True)
        open(M,'w').write(HEAD); ok=sha(open(M).read())==H
        t=open(log).read(); summ=(re.findall(r'Tests\s+(.*)',t) or ['?'])[-1].strip()
        cells=sorted(set(re.findall(r'× (?:RED |control )?ks1868 (C1|R1|R2) .*?(upload|boot probe)',t)))
        kinds=sorted(set(re.findall(r'^(AssertionError|TypeError|Error)\b',t,flags=re.M)))
        st='KILLED' if r.returncode!=0 else 'SURVIVED'; k+=st=='KILLED'; s+=st=='SURVIVED'
        print(site,m,st,summ,'cells',cells,'kinds',kinds,'restore',ok,flush=True)
print('killed',k,'survived',s)
