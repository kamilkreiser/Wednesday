import re,subprocess,hashlib,sys,os,glob,json
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate139-ks1868-pr1956'
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
sites=[('analytics',0),('analytics',1),('api-gateway',0),('api-gateway',1),('anchoring',0),('kyc',0)]
sha=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()
res=[]
for svc,k in sites:
    P=f'{D}/services/{svc}/src/db.ts'; orig=open(P).read(); h=sha(P)
    T=glob.glob(f'{D}/services/{svc}/src/__tests__/ks1868-*db-pool*.test.ts')[0]
    blocks=list(BLK.finditer(orig)); assert len(blocks)==(2 if svc in('analytics','api-gateway') else 1),(svc,len(blocks))
    b=blocks[k]
    for name,reps in M.items():
        blk=b.group(0)
        if reps is None:
            ind=b.group(1); expr='err.message' if k==0 else 'err?.message'
            new=f'{ind}const reason = {expr};\n'
        else:
            new=blk
            for a,c in (reps if name!='M10_log_drops_error' else []):
                assert a in new,(svc,k,name,a); new=new.replace(a,c)
        tail=orig[b.end():]
        if name=='M10_log_drops_error':
            assert '{ error: reason }' in tail[:200]; tail=tail.replace('{ error: reason }','{}',1); new=blk
        open(P,'w').write(orig[:b.start()]+new+tail)
        log=f'{W}/logs/mut_{svc}{k}__{name}.log'
        r=subprocess.run(['nice','-n','10',V,'run','--root',f'{D}/services/{svc}',os.path.relpath(T,f'{D}/services/{svc}'),'--maxWorkers=2'],capture_output=True,text=True)
        open(log,'w').write(r.stdout+r.stderr+f'\nrc={r.returncode}\n')
        txt=r.stdout+r.stderr
        failed=re.findall(r'(?:FAIL|×)\s+.*?(?:control|RED) ks1868 (\w+)',txt)
        open(P,'w').write(orig)
        ok=sha(P)==h
        tmo=txt.count('timed out'); asr=txt.count('AssertionError')
        res.append((svc,k,name,'KILLED' if r.returncode!=0 else 'SURVIVED',sorted(set(failed)),ok,'timeouts=%d'%tmo,'assertionerr=%d'%asr))
        print(*res[-1],flush=True)
json.dump(res,open(W+'/logs/mutants.json','w'))
