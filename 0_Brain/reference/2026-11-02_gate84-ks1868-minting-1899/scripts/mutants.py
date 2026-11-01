import re,subprocess,hashlib,sys,shutil,os
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate84-ks1868-minting-1899'
M=W+'/repo/Blockchain/Dev/services/nft-certificate/src/services/minting.service.ts'
ORIG=open(W+'/logs/head_minting.service.ts').read()
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
H0=sha(ORIG)
assert sha(open(M).read())==H0,'working file not at head'
# one guard block per site
BLK=re.compile(r"(?P<i>[ ]*)let reason: string;\n[ ]*try \{\n[ ]*reason = (?P<expr>[^\n]*);\n[ ]*\} catch \{\n[ ]*reason = 'unreadable thrown value';\n[ ]*\}\n[ ]*(?P<log>logger\.(?P<lvl>\w+)\((?P<msg>'[^\n]*?'), \{ error: reason \}\);)")
blocks=list(BLK.finditer(ORIG)); assert len(blocks)==4,len(blocks)
NAMES=['dbSave','loadFromDb','getNFT','getUser']
def mk(name,fn):
    return name,fn
def mutants(b):
    i=b['i']; e=b['expr']; lg=b['log']; lvl=b['lvl']
    return {
 'M1_drop_inner_try':   f"{i}const reason = {e};\n{i}{lg}",
 'M2_ctor_String_err':  f"{i}let reason: string;\n{i}try {{\n{i}  reason = {e};\n{i}}} catch {{\n{i}  reason = String((undefined as any, arguments_placeholder));\n{i}}}\n{i}{lg}".replace("String((undefined as any, arguments_placeholder))","String(err)"),
 'M3_rethrow_all_after_log': f"{i}let reason: string;\n{i}try {{\n{i}  reason = {e};\n{i}}} catch {{\n{i}  reason = 'unreadable thrown value';\n{i}}}\n{i}{lg}\n{i}throw err;",
 'M4_rethrow_only_unreadable': f"{i}let reason: string;\n{i}let unreadable = false;\n{i}try {{\n{i}  reason = {e};\n{i}}} catch {{\n{i}  reason = 'unreadable thrown value';\n{i}  unreadable = true;\n{i}}}\n{i}{lg}\n{i}if (unreadable) throw new Error('rethrown');",
 'M5_constant_for_ALL_values': f"{i}const reason = 'unreadable thrown value';\n{i}{lg}",
 'M6_nonError_branch_const_x': f"{i}let reason: string;\n{i}try {{\n{i}  reason = err instanceof Error ? err.message : 'x';\n{i}}} catch {{\n{i}  reason = 'unreadable thrown value';\n{i}}}\n{i}{lg}",
 'M7_msg_dropped_String_err': f"{i}let reason: string;\n{i}try {{\n{i}  reason = String(err);\n{i}}} catch {{\n{i}  reason = 'unreadable thrown value';\n{i}}}\n{i}{lg}",
 'M8_const_text_changed': f"{i}let reason: string;\n{i}try {{\n{i}  reason = {e};\n{i}}} catch {{\n{i}  reason = 'unreadable';\n{i}}}\n{i}{lg}",
 'M9_key_renamed': f"{i}let reason: string;\n{i}try {{\n{i}  reason = {e};\n{i}}} catch {{\n{i}  reason = 'unreadable thrown value';\n{i}}}\n{i}{lg.replace('{ error: reason }','{ err: reason }')}",
 'M10_log_removed': f"{i}let reason: string;\n{i}try {{\n{i}  reason = {e};\n{i}}} catch {{\n{i}  reason = 'unreadable thrown value';\n{i}}}\n{i}void reason;",
 'M11_level_swapped': f"{i}let reason: string;\n{i}try {{\n{i}  reason = {e};\n{i}}} catch {{\n{i}  reason = 'unreadable thrown value';\n{i}}}\n{i}{lg.replace('logger.'+lvl,'logger.'+('info' if lvl!='info' else 'warn'))}",
 'M12_unguarded_inline_fallback': f"{i}let reason: string;\n{i}try {{\n{i}  reason = {e};\n{i}}} catch {{\n{i}  reason = (err as any).message;\n{i}}}\n{i}{lg}",
 'M13_return_in_catch_before_log': None,
    }
only=sys.argv[1:] 
res=[]
for k,b in enumerate(blocks):
    ms=mutants(b.groupdict())
    for mn,rep in ms.items():
        if rep is None: continue
        tag=f"{NAMES[k]}__{mn}"
        if only and not any(o in tag for o in only): continue
        new=ORIG[:b.start()]+rep+ORIG[b.end():]
        open(M,'w').write(new)
        log=f"{W}/logs/mut_{tag}.log"
        r=subprocess.run(['bash',W+'/scripts/vt.sh',log,'ks1868-nft-db-save','ks1868-nft-get-nft','ks1868-nft-get-user','ks1868-nft-load-from'])
        open(M,'w').write(ORIG)
        ok=sha(open(M).read())==H0
        txt=open(log).read()
        m=re.search(r'Tests\s+(.*)',txt)
        failed=re.findall(r'FAIL\s+(\S+).*?>\s*(.*)',txt)
        verdict='KILLED' if r.returncode!=0 else 'SURVIVED'
        line=f"{tag} | {verdict} | rc={r.returncode} | {m.group(1).strip() if m else '?'} | restore={'OK' if ok else 'FAIL'}"
        print(line,flush=True); res.append(line)
        if not ok: sys.exit('restore failed')
open(W+'/logs/mutants_table.log','a').write('\n'.join(res)+'\n')
