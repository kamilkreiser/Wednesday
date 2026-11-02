import re,subprocess,hashlib,sys,os,glob,json
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate152-ks1868-pr1968'
D=W+'/repo/Blockchain/Dev'
V=D+'/node_modules/.bin/vitest'
BLK=re.compile(r"( *)let reason: string \| null \| undefined;\n.*?\n\1\} catch \{\n.*?\n\1\}\n",re.S)
M={
 'M0_revert':None,
 'M1_inner_try_dropped':[('try {','if (true) {'),('} catch {','} else {')],
 'M2_const_text':[("'unreadable thrown value'","'x'")],
 'M3_no_String':[('String(m)','m')],
 'M4_no_optional_chain':[('err?.message','err.message')],
 'M5_String_for_all':[('m === undefined || m === null ? m : String(m)','String(m)')],
 'M6_null_becomes_text':[('m === undefined || m === null ? m : String(m)','m === undefined ? m : String(m)')],
 'M7_undefined_becomes_text':[('m === undefined || m === null ? m : String(m)','m === null ? m : String(m)')],
 'M8_always_constant':[('const m = err?.message;','const m = (() => { throw 0; })();')],
 'M9_catch_rethrows':[("reason = 'unreadable thrown value';",'throw new Error("mut");')],
 'M10_log_drops_error':[('{ error: reason }','{}')],
}
SITES=[('src/db.ts',0,'ks1868-vc-issuer-db-pool-error-and-ready-hook-unreadable-throw.test.ts','err.message'),('src/db.ts',1,'ks1868-vc-issuer-db-pool-error-and-ready-hook-unreadable-throw.test.ts','err?.message'),
('src/repositories/credentialRepo.ts',0,'ks1868-credentialrepo-read-catches-unreadable-throw.test.ts','err?.message'),('src/repositories/credentialRepo.ts',1,'ks1868-credentialrepo-read-catches-unreadable-throw.test.ts','err?.message'),('src/repositories/credentialRepo.ts',2,'ks1868-credentialrepo-read-catches-unreadable-throw.test.ts','err?.message')]
sha=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()
res=[]
for rel,k,tf,origexpr in SITES:
    svc='vc-issuer'
    P=f'{D}/services/vc-issuer/{rel}'; orig=open(P).read(); h=sha(P)
    T=f'{D}/services/vc-issuer/src/__tests__/{tf}'
    blocks=list(BLK.finditer(orig)); b=blocks[k]
    nb=len(blocks)
    for name,reps in M.items():
        blk=b.group(0)
        if reps is None:
            ind=b.group(1)
            new=f'{ind}const reason = {origexpr};\n'
        else:
            new=blk
            for a_,c in (reps if name!='M10_log_drops_error' else []):
                assert a_ in new,(rel,k,name,a_); new=new.replace(a_,c)
        tail=orig[b.end():]
        if name=='M10_log_drops_error':
            assert '{ error: reason }' in tail[:200]; tail=tail.replace('{ error: reason }','{}',1); new=blk
        open(P,'w').write(orig[:b.start()]+new+tail)
        tag=rel.replace('/','_')
        log=f'{W}/logs/mut_{tag}{k}__{name}.log'
        r=subprocess.run(['nice','-n','10',V,'run','--root',f'{D}/services/vc-issuer',os.path.relpath(T,f'{D}/services/vc-issuer'),'--maxWorkers=2'],capture_output=True,text=True)
        open(log,'w').write(r.stdout+r.stderr+f'\nrc={r.returncode}\n')
        txt=r.stdout+r.stderr
        failed=re.findall(r'(?:FAIL|×)\s+.*?(?:control|RED) ks1868 (\w+)',txt)
        open(P,'w').write(orig)
        ok=sha(P)==h
        tmo=txt.count('timed out'); asr=txt.count('AssertionError')
        res.append((rel,k,name,'KILLED' if r.returncode!=0 else 'SURVIVED',sorted(set(failed)),ok,'timeouts=%d'%tmo,'assertionerr=%d'%asr,'blocks=%d'%nb))
        print(*res[-1],flush=True)
json.dump(res,open(W+'/logs/mutants.json','w'))
