import re, subprocess, hashlib, json, sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate104-ks1868-pr1923'
A=W+'/repo/Blockchain/Dev/services/originate'
L=W+'/logs'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
S='src/routes/signatories.ts'; T='src/routes/thirdPartyVerifiers.ts'; RS='src/services/retentionScheduler.ts'
SITES=[('O67-P1 list',S,'ks1868-signatories-read-routes-p1',0),('O67-P1 check',S,'ks1868-signatories-read-routes-p1',1),('O67-P1 get',S,'ks1868-signatories-read-routes-p1',2),
 ('O67-P2 patch',S,'ks1868-signatories-write-routes-p2',3),('O67-P2 revoke',S,'ks1868-signatories-write-routes-p2',4),('O67-P2 reinstate',S,'ks1868-signatories-write-routes-p2',5),
 ('O67-P3 list',T,'ks1868-third-party-verifiers-admin-routes-p3',0),('O67-P3 suspend',T,'ks1868-third-party-verifiers-admin-routes-p3',1),('O67-P3 reinstate',T,'ks1868-third-party-verifiers-admin-routes-p3',2),
 ('O67-P4 verify',T,'ks1868-third-party-verifiers-verify-routes-p4',3),('O67-P4 records',T,'ks1868-third-party-verifiers-verify-routes-p4',4),
 ('O68-P3 runEnforcement',RS,'ks1868-retention-scheduler-run-enforcement-p3',0)]
GUARD=re.compile(r"(?P<ind>[ ]*)let reason: string;\n[ ]*try \{\n[ ]*reason = (?P<x>[^\n]+);\n[ ]*\} catch \{\n[ ]*reason = 'unreadable thrown value';\n[ ]*\}\n")
def muts(src, occ):
    ms=list(GUARD.finditer(src)); m=ms[occ]; ind=m.group('ind'); x=m.group('x'); g=m.group(0)
    var='err' if 'String(err)' in x else 'error'
    def rep(t): return src[:m.start()]+t+src[m.end():]
    out={}
    out['M0 revert guard']=rep(f"{ind}let reason: string = {x};\n")
    out['M1 drop try']=rep(f"{ind}let reason: string;\n{ind}reason = {x};\n")
    out['M2 catch -> String(v)']=rep(g.replace("reason = 'unreadable thrown value';",f"reason = String({var});"))
    out['M3 catch rethrows']=rep(g.replace("reason = 'unreadable thrown value';",f"throw {var};"))
    out['M4 constant for all']=rep(g.replace(f"reason = {x};","reason = 'unreadable thrown value';",1))
    y=re.sub(r"String\((err|error)\)","'x'",x)
    out['M6 readable branch -> x']=rep(g.replace(f"reason = {x};",f"reason = {y};",1))
    out['M8 constant text changed']=rep(g.replace("'unreadable thrown value'","'x'"))
    tail=src[m.end():]; k=tail.find('error: reason')
    out['M7 log ignores reason']=src[:m.end()]+tail[:k]+"error: (reason ? 'x' : 'x')"+tail[k+len('error: reason'):]
    out['M9 log removed']=src[:m.end()]+re.sub(r"logger\.error\([^\n]*error: reason \}\);\n","void reason;\n",tail,count=1)
    return out
rows=[]
for sid,f,pat,occ in SITES:
    p=A+'/'+f; orig=open(p).read(); h0=sha(p)
    for name,txt in muts(orig,occ).items():
        if txt==orig: rows.append((sid,name,'NOOP')); print(sid,name,'NOOP',flush=True); continue
        open(p,'w').write(txt)
        r=None
        try:
            r=subprocess.run(['npx','jest','--forceExit','--json','--outputFile=/dev/stdout',pat],cwd=A,capture_output=True,text=True,timeout=240); out=r.stdout; err=r.stderr; to=False
        except subprocess.TimeoutExpired as e:
            out=''; err='TIMEOUT'; to=True
        open(p,'w').write(orig); ok=sha(p)==h0
        compile_err=False
        try:
            j=json.loads(out[out.index('{'):out.rindex('}')+1]); failed=[a['title'][:50] for t in j['testResults'] for a in t['assertionResults'] if a['status']=='failed']; nt=j['numTotalTests']; compile_err=(j['numFailedTestSuites']>0 and nt==0)
            byexp=sum(1 for t in j['testResults'] for a in t['assertionResults'] if a['status']=='failed' and any('expect(' in mm for mm in a['failureMessages']))
        except Exception:
            failed=['PARSEFAIL' if not to else 'TIMEOUT']; nt=-1; byexp=0
        res='INCONCLUSIVE-TIMEOUT' if to else ('COMPILEERR' if compile_err else ('KILLED' if failed else 'SURVIVED'))
        lg=f"{L}/mut_{sid.replace(' ','_')}__{name.split()[0]}.log"; open(lg,'w').write(json.dumps({'failed':failed,'byExpect':byexp,'nt':nt,'stderrtail':err[-800:]},indent=1))
        rows.append((sid,name,res,len(failed),byexp,ok)); print(sid,'|',name,'|',res,len(failed),'byExpect',byexp,'restore',ok,flush=True)
json.dump(rows,open(L+'/mutants_table.json','w'))
