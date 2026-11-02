import subprocess, hashlib, re, os, sys, shutil
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate125-ks1868-pr1943'
S=W+'/repo/Blockchain/Dev/services/originate'
PF=S+'/src/repositories/certificationRepo.ts'
T=S+'/src/__tests__/ks1868-certification-repo-list-and-shares-catches-o79p6-unreadable-throw.test.ts'
orig=open(PF).read(); h0=hashlib.sha256(orig.encode()).hexdigest()
G="""    let reason: string;
    try {
      reason = String(err instanceof Error ? err.message : err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.warn('%s', { error: reason });
    throw err;"""
sites={'list':'DB list failed','shares':'Failed to fetch shares from DB'}
def muts(msg):
    g=G%msg
    return {
 'M0_revert_to_base': (g,"    logger.warn('%s', { error: err instanceof Error ? err.message : String(err) });\n    throw err;"%msg),
 'M1_drop_inner_try': (g,"    const reason = String(err instanceof Error ? err.message : err);\n    logger.warn('%s', { error: reason });\n    throw err;"%msg),
 'M2_constant_for_all': (g,g.replace("reason = String(err instanceof Error ? err.message : err);","reason = 'unreadable thrown value';")),
 'M3_no_String_coerce': (g,g.replace("reason = String(err instanceof Error ? err.message : err);","reason = (err instanceof Error ? err.message : err) as string;")),
 'M4_readable_nonError_to_x': (g,g.replace("err instanceof Error ? err.message : err","err instanceof Error ? err.message : 'x'")),
 'M5_swallow_no_rethrow': (g,g.replace("    throw err;","    return undefined as any;")),
 'M6_rethrow_reason_not_err': (g,g.replace("    throw err;","    throw new Error(reason);")),
 'M7_rethrow_only_readable': (g,g.replace("    throw err;","    if (reason !== 'unreadable thrown value') throw err;\n    return undefined as any;")),
 'M8_log_removed': (g,g.replace("    logger.warn('%s', { error: reason });\n"%msg,"    void reason;\n")),
 'M9_wrong_context': (g,g.replace("logger.warn('%s'"%msg,"logger.warn('x'")),
 'M10_log_level_error': (g,g.replace("logger.warn(","logger.error(")),
}
rows=[]
for site,msg in sites.items():
    for name,(a,b) in muts(msg).items():
        if name!='M8_log_removed': continue
        # the site must be located by its unique message: find occurrence in orig
        if orig.count(a)!=1: print('LOCATE FAIL',site,name,orig.count(a)); continue
        open(PF,'w').write(orig.replace(a,b))
        r=subprocess.run([S+'/node_modules/.bin/jest','--rootDir',S,'-c',S+'/jest.config.js','--runTestsByPath',T],capture_output=True,text=True)
        out=r.stdout+r.stderr
        open(W+'/logs/mut_%s__%s.log'%(site,name),'w').write(out)
        failed=sorted(set(re.findall(r'✕ (control|RED) ks1868 (\w+) (\w+)',out)))
        tsfail='error TS' in out
        open(PF,'w').write(orig)
        ok=hashlib.sha256(open(PF).read().encode()).hexdigest()==h0
        line='%s %s rc=%d failed=%s tsc_error=%s restore=%s'%(site,name,r.returncode,[x[1]+':'+x[2][:5] for x in failed],tsfail,ok)
        print(line,flush=True); rows.append(line)
open(W+'/logs/mutants_table_M8.log','w').write('\n'.join(rows)+'\n')
