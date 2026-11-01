import hashlib, subprocess
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate78-ks1868-analytics2-1893'
P=G+'/repo/Blockchain/Dev/services/analytics/src/services/'
FILES={'export':('exportService.ts','ks1868-export-service-db-save','DB save export failed'),
       'sched':('scheduledJobs.ts','ks1868-scheduled-jobs-save-alert-rule','DB save alert rule failed')}
MODE_ONLY=None
ORIG="reason = err instanceof Error ? err.message : String(err);"
FB="reason = 'unreadable thrown value';"
MUT={
 'M1 fallback constant changed': [(FB, "reason = 'x';")],
 'M2b instanceof hoisted outside inner try': [("let reason: string;","let reason: string; const isE = err instanceof Error;"),(ORIG,"reason = isE ? (err as Error).message : String(err);")],
 'M3 message->String(err)': [(ORIG, "reason = err instanceof Error ? String(err) : String(err);")],
 'M4 inner catch rethrows': [(FB, "throw new Error('rethrow');")],
 'M5 unguarded read in fallback': [(FB, "reason = String((err as any)?.message);")],
 'M6 non-Error branch constant': [(ORIG, "reason = err instanceof Error ? err.message : 'x';")],
 'M7 optional-chain message': [(ORIG, "reason = (err as any)?.message ?? String(err);")],
 'M8 key renamed': [("error: reason,","err: reason,"),("{ error: reason }","{ err: reason }")],
 'M9 log then rethrow (resolve contract)': [("{ error: reason });","{ error: reason });\n throw new Error('rethrow-after-log');")],
 'M10 level info->warn': [("logger.info('DB save","logger.warn('DB save")],
 'M11 log line removed': [("logger.info('DB save","void ('DB save")],
}
sha=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()
for fk,(fn,pat,marker) in FILES.items():
    path=P+fn; orig=open(path).read(); h0=sha(path)
    for name,reps in MUT.items():
        li=orig.index("logger.info('"+marker+"'"); le=orig.index('\n',li); ws=orig.rindex('catch (err: any)',0,li)
        win=orig[ws:le]; bad=False
        for a,b in reps:
            if win.count(a)!=1:
                print(fk,name,'PATTERN COUNT',win.count(a),repr(a)); bad=True; break
            win=win.replace(a,b)
        if bad: continue
        txt=orig[:ws]+win+orig[le:]
        open(path,'w').write(txt)
        log=f"{G}/logs/mut_{fk}_{name.split()[0]}.log"
        rc=subprocess.run(['bash',G+'/scripts/vt.sh',log,pat]).returncode
        open(path,'w').write(orig)
        assert sha(path)==h0,'RESTORE FAIL'
        tl=[l.strip() for l in open(log).read().splitlines() if l.strip().startswith('Tests ')]
        print(f"{fk} | {name} | rc={rc} | {'KILLED' if rc else 'SURVIVED'} | {tl} | sha_restored=OK {h0[:12]}", flush=True)
