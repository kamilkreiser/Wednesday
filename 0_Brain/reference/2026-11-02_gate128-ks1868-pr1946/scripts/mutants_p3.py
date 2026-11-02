import subprocess, hashlib, re
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate128-ks1868-pr1946'
S=W+'/repo/Blockchain/Dev/services/originate'
PF=S+'/src/services/retentionScheduler.ts'
T=S+'/src/__tests__/ks1868-retention-scheduler-run-enforcement-p3-unreadable-throw.test.ts'
orig=open(PF).read(); h0=hashlib.sha256(orig.encode()).hexdigest()
A="      reason = String(err instanceof Error ? err.message : err);"
L="    logger.error('Scheduled enforcement failed', { error: reason });"
M={
'M0_revert_to_base': (A,"      reason = err instanceof Error ? err.message : String(err);"),
'M1_drop_String': (A,"      reason = (err instanceof Error ? err.message : err) as string;"),
'M2_constant_always': (A,"      reason = 'unreadable thrown value';"),
'M3_String_err_only': (A,"      reason = String(err);"),
'M4_nonError_to_x': (A,"      reason = String(err instanceof Error ? err.message : 'x');"),
'M5_error_msg_to_x': (A,"      reason = String(err instanceof Error ? 'x' : err);"),
'M6_fallback_text_changed': ("      reason = 'unreadable thrown value';","      reason = 'x';"),
'M7_drop_inner_try': ("    let reason: string;\n    try {\n"+A+"\n    } catch {\n      reason = 'unreadable thrown value';\n    }\n","    const reason = "+A.strip()[len('reason = '):]+"\n"),
'M8_log_removed': (L,"    void reason;"),
'M9_wrong_context': ("'Scheduled enforcement failed'","'x'"),
'M10_level_warn': ("logger.error('Scheduled","logger.warn('Scheduled"),
'M11_rethrow': (L,L+"\n    throw err;"),
'M12_stop_scheduler_on_failure': (L,L+"\n    stopRetentionScheduler();"),
}
rows=[]
for name,(a,b) in M.items():
    if orig.count(a)!=1: print('LOCATE FAIL',name,orig.count(a)); continue
    open(PF,'w').write(orig.replace(a,b))
    r=subprocess.run([S+'/node_modules/.bin/jest','--rootDir',S,'-c',S+'/jest.config.js','--runInBand','--runTestsByPath',T],capture_output=True,text=True)
    out=r.stdout+r.stderr
    open(W+'/logs/mutP3_%s.log'%name,'w').write(out)
    failed=sorted(set(re.findall(r'✕ (?:control|RED) ks1868 (\w+)',out)))
    ts='error TS' in out
    open(PF,'w').write(orig)
    ok=hashlib.sha256(open(PF).read().encode()).hexdigest()==h0
    line='%s rc=%d failed=%s tsc_error=%s restore=%s'%(name,r.returncode,failed,ts,ok); print(line,flush=True); rows.append(line)
open(W+'/logs/mutants_p3_table.log','w').write('\n'.join(rows)+'\n')
