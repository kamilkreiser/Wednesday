import re, subprocess, hashlib, json, sys, os
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate101-ks1868-pr1919'
A=W+'/repo/Blockchain/Dev/services/originate'
L=W+'/logs'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
SITES=[ # (id, file, testpattern, kind, occurrence)
 ('O63-P2','src/services/errorTrackingService.ts','ks1868-error-tracking','guard',0),
 ('O65-P1','src/repositories/certificationRepo.ts','ks1868-certification-repo','guard',0),
 ('O65-P2','src/repositories/documentRepo.ts','ks1868-document-repo','guard',0),
 ('O68-P2','src/routes/metering.ts','ks1868-metering','guard',0),
 ('O68-P1a','src/utils/notificationClient.ts','ks1868-notification','guard',0),
 ('O68-P1b','src/utils/notificationClient.ts','ks1868-notification','guard',1),
 ('O63-P1a','src/routes/systemErrors.ts','ks1868-system-errors','fail',0),
 ('O63-P1b','src/routes/systemErrors.ts','ks1868-system-errors','fail',1),
]
GUARD=re.compile(r"(?P<ind>[ ]*)let reason: string;\n[ ]*try \{\n[ ]*reason = (?P<x>[^\n]+);\n[ ]*\} catch \{\n[ ]*reason = 'unreadable thrown value';\n[ ]*\}\n")
def guard_muts(src, occ):
    ms=list(GUARD.finditer(src)); m=ms[occ]; ind=m.group('ind'); x=m.group('x')
    def rep(t): return src[:m.start()]+t+src[m.end():]
    out={}
    out['M0 revert guard']=rep(f"{ind}let reason: string = {x};\n")
    out['M1 drop try']=rep(f"{ind}let reason: string;\n{ind}reason = {x};\n")
    ev="error" if "(error)" in x or "error instanceof" in x else "err"
    out['M2 catch -> String(err)']=rep(m.group(0).replace("reason = 'unreadable thrown value';",f"reason = String({ev});"))
    out['M3 catch rethrows']=rep(m.group(0).replace("reason = 'unreadable thrown value';",f"throw {ev};"))
    out['M4 constant for all']=rep(m.group(0).replace(f"reason = {x};","reason = 'unreadable thrown value';",1))
    if 'String(err)' in x or 'String(error)' in x:
        y=re.sub(r"String\((err|error)\)","'x'",x)
        out['M6 readable branch -> x']=rep(m.group(0).replace(f"reason = {x};",f"reason = {y};",1))
    out['M8 constant text changed']=rep(m.group(0).replace("'unreadable thrown value'","'x'"))
    # M7 log removed: next 'error: reason' occurrence after the guard
    tail=src[m.end():]
    k=tail.find('error: reason')
    out['M7 log drops reason']=src[:m.end()]+tail[:k]+"error: (reason ? 'x' : 'x')"+tail[k+len('error: reason'):]
    return out
def fail_muts(src, occ):
    pat=re.compile(r"fail500\(res, '([^']+)', err\);")
    ms=list(pat.finditer(src)); m=ms[occ]
    def rep(t): return src[:m.start()]+t+src[m.end():]
    ctx=m.group(1)
    old=("logger.error('%s', { error: err instanceof Error ? err.message : String(err) });\n    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });"%ctx)
    return {
     'M0 revert to inline': rep(old),
     'M1 no call (no answer)': rep('void err;'),
     'M2 context text changed': rep(f"fail500(res, 'x', err);"),
     'M3 arg is String(err)': rep(f"fail500(res, '{ctx}', String(err));"),
     'M5 rethrow after': rep(f"fail500(res, '{ctx}', err); throw err;"),
    }
rows=[]
only=sys.argv[1:]
KEEP=('M7','M2','M3')
for sid,f,pat,kind,occ in SITES:
    if only and sid not in only: continue
    p=A+'/'+f; orig=open(p).read(); h0=sha(p)
    muts=(guard_muts if kind=='guard' else fail_muts)(orig,occ)
    for name,txt in muts.items():
        if name.split()[0] not in KEEP: continue
        if sid in ('O63-P1a','O63-P1b'): continue
        if name.split()[0] in ('M2','M3') and sid!='O68-P2': continue
        if txt==orig: rows.append((sid,name,'NOOP')); print(sid,name,'NOOP',flush=True); continue
        open(p,'w').write(txt)
        lg=f"{L}/mut2_{sid}__{name.split()[0]}.log"
        r=subprocess.run(['npx','jest','--json','--outputFile=/dev/stdout',pat],cwd=A,capture_output=True,text=True)
        open(p,'w').write(orig)
        ok=sha(p)==h0
        try:
            j=json.loads(r.stdout[r.stdout.index('{'):r.stdout.rindex('}')+1]); failed=[a['title'][:60] for t in j['testResults'] for a in t['assertionResults'] if a['status']=='failed']; nt=j['numTotalTests']; compile_err = (j['numFailedTestSuites']>0 and nt==0)
        except Exception as e:
            failed=['PARSEFAIL']; nt=-1; compile_err=False
        open(lg,'w').write(json.dumps({'failed':failed,'nt':nt,'stderrtail':r.stderr[-600:]},indent=1))
        res='KILLED' if failed and not compile_err else ('COMPILEERR' if compile_err else 'SURVIVED')
        rows.append((sid,name,res,len(failed),ok)); print(sid,name,res,len(failed),'restore',ok,flush=True)
json.dump(rows,open(L+'/mutants_table2.json','w'))
