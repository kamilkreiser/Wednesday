import hashlib, subprocess, sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate74-ks1868-analytics-1889'
P=G+'/repo/Blockchain/Dev/services/analytics/src/services/'
FILES={'export':('exportService.ts','ks1868-export-service-load'),'sched':('scheduledJobs.ts','ks1868-scheduled-jobs-load')}
ORIG="reason = err instanceof Error ? err.message : String(err);"
FB="reason = 'unreadable thrown value';"
MUT={
 'M1 fallback constant changed': (FB, "reason = 'x';"),
 'M2 instanceof hoisted outside try': (ORIG, "const isE = (() => { return err instanceof Error; })(); reason = isE ? (err as Error).message : String(err);"),
 'M3 message->String(err)': (ORIG, "reason = err instanceof Error ? String(err) : String(err);"),
 'M4 inner catch rethrows': (FB, "throw new Error('rethrow');"),
 'M5 no try: unguarded read restored': ("      reason = 'unreadable thrown value';", "      reason = String((err as any)?.message);"),
 'M6 non-Error branch constant (String(err)->"x")': (ORIG, "reason = err instanceof Error ? err.message : 'x';"),
 'M7 getter guarded only via optional chain (err as any)?.message': (ORIG, "reason = (err as any)?.message ?? String(err);"),
 'M8 WARN key renamed': ("error: reason,", "err: reason,"),
}
sha=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()
for fk,(fn,pat) in FILES.items():
    path=P+fn; orig=open(path).read(); h0=sha(path)
    for name,(a,b) in MUT.items():
        if orig.count(a)!=1: print(fk,name,'PATTERN COUNT',orig.count(a)); continue
        open(path,'w').write(orig.replace(a,b))
        log=f"{G}/logs/mut_{fk}_{name.split()[0]}.log"
        rc=subprocess.run([G+'/scripts/vt.sh',log,pat]).returncode
        open(path,'w').write(orig)
        assert sha(path)==h0, 'RESTORE FAIL'
        txt=open(log).read()
        tl=[l.strip() for l in txt.splitlines() if l.strip().startswith('Tests ')]
        print(f"{fk} {name}: rc={rc} {'KILLED' if rc else 'SURVIVED'} {tl} sha_restored=OK")
