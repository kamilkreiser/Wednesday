# Resume of mutants.py (load gate shortened to one 20 s wait; skips mutants already in mutants_table_part1.log)
# Each mutant applied to ONE site of the product file only; tests untouched; sha restored and checked after each run.
import subprocess,hashlib,re
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate93-ks1868-pr1911'
M=G+'/repo/Blockchain/Dev/services/auth/src/routes/auth.ts'
HEAD=open(G+'/logs/head_auth.ts').read()
sha=lambda s: hashlib.sha256(s.encode()).hexdigest()
H=sha(HEAD); assert sha(open(M).read())==H, 'product not at head'
EXPR='err instanceof Error ? err.message : String(err)'
p=' '*6
g=(f"{p}let reason: string;\n{p}try {{\n{p}  reason = {EXPR};\n{p}}} catch {{\n{p}  reason = 'unreadable thrown value';\n{p}}}\n")
assert HEAD.count(g)==3, HEAD.count(g)
starts=[m.start() for m in re.finditer(re.escape(g),HEAD)]
SITES={'P1_register':0,'P2_login':1,'P3_reset':2}
def mut(src,site,m):
    i=starts[SITES[site]]; j=src.index('error: reason',i); k=src.index(');\n',j)+3
    block=src[i:k]
    if m=='M0_revert_guard':  nb=block.replace(g,'').replace('error: reason',f'error: {EXPR}')
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
DONE={tuple(l.split()[:2]) for l in open(G+'/logs/mutants_table_part1.log') if ' restore True' in l}
for site in SITES:
    for m in MUTS:
        if (site,m) in DONE: continue
        open(M,'w').write(mut(HEAD,site,m))
        log=f'{G}/logs/mut_{site}__{m}.log'
        r=subprocess.run(['bash',G+'/scripts/vt_fast.sh',log,'ks1868-auth-'],capture_output=True,text=True)
        open(M,'w').write(HEAD); ok=sha(open(M).read())==H
        t=open(log).read()
        summ=(re.findall(r'Tests\s+(.*)',t) or ['?'])[-1].strip()
        failed=[l.strip() for l in t.splitlines() if l.strip().startswith(('×','FAIL'))]
        cells=sorted(set(re.findall(r'\b(C1|C2|R1|R2)\b',' '.join(failed))))
        files=sorted(set(re.findall(r'ks1868-auth-(register|login|reset)',' '.join(failed))))
        kind=sorted(set(re.findall(r'^(AssertionError|TypeError|Error)\b',t,flags=re.M)))
        st='KILLED' if r.returncode!=0 else 'SURVIVED'
        print(site,m,st,summ,'cells',cells,'files',files,'kinds',kind,'restore',ok,flush=True)
        rows.append(st)
print('killed',rows.count('KILLED'),'survived',rows.count('SURVIVED'))
