# Each mutant applied to ONE site of the product file only; tests untouched; sha restored and checked after each run.
import subprocess,hashlib,re,json,shutil
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate90-ks1868-security-1908'
M=G+'/repo/Blockchain/Dev/services/security/src/index.ts'
HEAD=open(G+'/logs/head_index.ts').read()
sha=lambda s: hashlib.sha256(s.encode()).hexdigest()
H=sha(HEAD)
EXPR='err instanceof Error ? err.message : String(err)'
def guard(ind):
    p=' '*ind
    return (f"{p}let reason: string;\n{p}try {{\n{p}  reason = {EXPR};\n{p}}} catch {{\n{p}  reason = 'unreadable thrown value';\n{p}}}\n")
SITES={'P1_revokePriorConnectorKeys':4,'P2_saveKeyAndRetirePriors':8}
def mut(src,site,m):
    ind=SITES[site]; p=' '*ind; g=guard(ind)
    assert src.count(g)==1, (site,src.count(g))
    i=src.index(g); j=src.index('error: reason,\n',i)+len('error: reason,\n')
    k=src.index('});\n',j)+len('});\n')   # end of the log call
    block=src[i:k]
    if m=='M0_revert_guard':  nb=block.replace(g,'').replace('error: reason,',f'error: {EXPR},')
    elif m=='M1_drop_inner_try': nb=block.replace(g,f"{p}const reason: string = {EXPR};\n")
    elif m=='M2_constant_to_String_err': nb=block.replace("reason = 'unreadable thrown value';","reason = String(err);")
    elif m=='M3_rethrow_only_unreadable': nb=block.replace("reason = 'unreadable thrown value';","throw err;")
    elif m=='M4_constant_for_all': nb=block.replace(f"reason = {EXPR};","reason = 'unreadable thrown value';")
    elif m=='M5_rethrow_all_after_log': nb=block+f"{p}throw err;\n"
    elif m=='M6_nonError_branch_x': nb=block.replace(f"reason = {EXPR};","reason = err instanceof Error ? err.message : 'x';")
    elif m=='M7_log_removed': nb=g
    else: raise SystemExit(m)
    assert nb!=block
    return src[:i]+nb+src[k:]
MUTS=['M0_revert_guard','M1_drop_inner_try','M2_constant_to_String_err','M3_rethrow_only_unreadable','M4_constant_for_all','M5_rethrow_all_after_log','M6_nonError_branch_x','M7_log_removed']
rows=[]
for site in SITES:
    for m in MUTS:
        open(M,'w').write(mut(HEAD,site,m))
        log=f'{G}/logs/mut_{site}__{m}.log'
        r=subprocess.run(['bash',G+'/scripts/vt.sh',log,'ks1868-security-'],capture_output=True,text=True)
        open(M,'w').write(HEAD); ok=sha(open(M).read())==H
        t=open(log).read()
        summ=(re.findall(r'Tests\s+(.*)',t) or ['?'])[-1].strip()
        cells=sorted(set(re.findall(r'(C1|R1|R2) ',' '.join(l for l in t.splitlines() if l.strip().startswith('×')))))
        files=sorted(set(re.findall(r'FAIL\s+src/__tests__/(ks1868-security-[a-z-]+)\.test\.ts',t)))
        kind=sorted(set(re.findall(r'^(AssertionError|TypeError|Error)\b',t,flags=re.M)))
        st='KILLED' if r.returncode!=0 else 'SURVIVED'
        rows.append((site,m,st,summ,cells,files,kind,ok))
        print(site,m,st,summ,'cells',cells,'files',[f.replace('ks1868-security-','') for f in files],'kinds',kind,'restore',ok,flush=True)
print('killed',sum(r[2]=='KILLED' for r in rows),'survived',sum(r[2]=='SURVIVED' for r in rows))
