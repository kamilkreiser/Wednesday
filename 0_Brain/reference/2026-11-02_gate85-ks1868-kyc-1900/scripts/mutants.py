import re,subprocess,hashlib,sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900'
M=W+'/repo/Blockchain/Dev/services/kyc/src/index.ts'
ORIG=open(W+'/logs/head_index.ts').read()
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
H0=sha(ORIG)
assert sha(open(M).read())==H0,'working file not at head'
BLK=re.compile(r"(?P<i>[ ]*)let reason: string;\n[ ]*try \{\n[ ]*reason = (?P<expr>[^\n]*);\n[ ]*\} catch \{\n[ ]*reason = 'unreadable thrown value';\n[ ]*\}\n[ ]*(?P<log>logger\.(?P<lvl>\w+)\((?P<msg>'[^\n]*?'), \{ (?P<pre>(?:\w+, )?)error: reason \}\);)")
blocks=list(BLK.finditer(ORIG)); assert len(blocks)==5,len(blocks)
NAMES=['saveVerification','getVerification','getVerificationsByUser','getVerificationStats','saveConsent']
FILES={'saveVerification':'ks1868-kyc-save-verification','getVerification':'ks1868-kyc-get-verification-unreadable','getVerificationsByUser':'ks1868-kyc-get-verifications-by-user','getVerificationStats':'ks1868-kyc-get-verification-stats','saveConsent':'ks1868-kyc-save-consent'}
def guard(i,e,lg,fallback="'unreadable thrown value'",after=''):
    return f"{i}let reason: string;\n{i}try {{\n{i}  reason = {e};\n{i}}} catch {{\n{i}  reason = {fallback};\n{i}}}\n{i}{lg}{after}"
def mutants(b):
    i=b['i']; e=b['expr']; lg=b['log']; lvl=b['lvl']; msg=b['msg']; pre=b['pre']
    return {
 'M0_revert_hunk': f"{i}logger.{lvl}({msg}, {{ {pre}error: {e} }});",
 'M1_drop_inner_try': f"{i}const reason = {e};\n{i}{lg}",
 'M2_fallback_String_err': guard(i,e,lg,'String(err)'),
 'M3_rethrow_all_after_log': guard(i,e,lg,after=f"\n{i}throw err;"),
 'M4_rethrow_only_unreadable': f"{i}let reason: string;\n{i}let unreadable = false;\n{i}try {{\n{i}  reason = {e};\n{i}}} catch {{\n{i}  reason = 'unreadable thrown value';\n{i}  unreadable = true;\n{i}}}\n{i}{lg}\n{i}if (unreadable) throw new Error('rethrown');",
 'M5_constant_for_ALL_values': f"{i}const reason = 'unreadable thrown value';\n{i}{lg}",
 'M6_nonError_branch_const_x': guard(i,"err instanceof Error ? err.message : 'x'",lg),
 'M7_msg_dropped_String_err': guard(i,'String(err)',lg),
 'M10_log_removed': f"{i}let reason: string;\n{i}try {{\n{i}  reason = {e};\n{i}}} catch {{\n{i}  reason = 'unreadable thrown value';\n{i}}}\n{i}void reason;",
    }
only=sys.argv[1:]
for k,b in enumerate(blocks):
    for mn,rep in mutants(b.groupdict()).items():
        tag=f"{NAMES[k]}__{mn}"
        if only and not any(o in tag for o in only): continue
        new=ORIG[:b.start()]+rep+ORIG[b.end():]
        open(M,'w').write(new)
        log=f"{W}/logs/mut_{tag}.log"
        r=subprocess.run(['bash',W+'/scripts/vt.sh',log,'ks1868-kyc-'])
        open(M,'w').write(ORIG)
        ok=sha(open(M).read())==H0
        txt=open(log).read()
        m=re.search(r'Tests\s+(.*)',txt)
        failfiles=sorted(set(re.findall(r'FAIL\s+src/__tests__/(ks1868-kyc-[\w-]+)\.test\.ts',txt)))
        own=FILES[NAMES[k]]
        others=[f for f in failfiles if not f.startswith(own)]
        verdict='KILLED' if r.returncode!=0 else 'SURVIVED'
        line=f"{tag} | {verdict} | rc={r.returncode} | {m.group(1).strip() if m else '?'} | failing files={failfiles} | other-site files failing={others} | restore={'OK' if ok else 'FAIL'}"
        print(line,flush=True)
        open(W+'/logs/mutants_table.log','a').write(line+'\n')
        if not ok: sys.exit('restore failed')
