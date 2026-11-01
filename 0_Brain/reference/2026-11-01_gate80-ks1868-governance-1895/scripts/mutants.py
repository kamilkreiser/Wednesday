import re, hashlib, subprocess, sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate80-ks1868-governance-1895'
F=W+'/wt_head/Blockchain/Dev/services/governance/src/services/governanceService.ts'
sha=lambda b: hashlib.sha256(b).hexdigest()
orig=open(F,'rb').read(); h0=sha(orig); src=orig.decode()
open(W+'/logs/mutants_orig.sha256','w').write(h0+'\n')
H=[ # msg, testfile, origline, ret
 ("DB get proposal failed","ks1868-db-get-proposal-unreadable-throw","logger.error('DB get proposal failed', { id, error: err instanceof Error ? err.message : String(err) });", None),
 ("DB get all proposals failed","ks1868-get-all-proposals-unreadable-throw","logger.error('DB get all proposals failed', { error: err instanceof Error ? err.message : String(err) });","return [];"),
 ("DB get all participants failed","ks1868-get-all-participants-unreadable-throw","logger.error('DB get all participants failed', { error: err instanceof Error ? err.message : String(err) });","return [];"),
 ("DB get active delegations failed","ks1868-get-active-delegations-unreadable-throw","logger.error('DB get active delegations failed', { error: err instanceof Error ? err.message : String(err) });","return [];"),
 ("DB get total vote power failed","ks1868-get-total-vote-power-unreadable-throw","logger.error('DB get total vote power failed', { error: err instanceof Error ? err.message : String(err) });","return 0;"),
]
out=open(W+'/logs/mutants_summary.log','w')
def run(tag,test):
    log=f"{W}/logs/mut_{tag}.log"
    subprocess.run([W+'/scripts/jt.sh','head',log,'__tests__/'+test+'.test'],check=False)
    t=open(log).read()
    m=re.search(r'Tests:\s+(.*)',t); rc=re.search(r'rc=(\d+)',t).group(1)
    return rc,(m.group(1) if m else '?')
for i,(msg,test,orig_line,ret) in enumerate(H,1):
    blk=re.compile(r"    let reason: string;\n    try \{\n      reason = err instanceof Error \? err\.message : String\(err\);\n    \} catch \{\n      reason = 'unreadable thrown value';\n    \}\n    (logger\.error\('"+re.escape(msg)+r"'[^\n]*)\n")
    m=blk.search(src); assert m, msg
    call=m.group(1)
    muts={}
    muts['A_revert_to_base']=src[:m.start()]+"    "+orig_line+"\n"+src[m.end():]
    seg=m.group(0)
    muts['B_empty_reason']=src.replace(seg,seg.replace("'unreadable thrown value'","''"))
    muts['E_drop_log']=src.replace(seg,seg.replace(call,"void reason;"))
    muts['F_inner_rethrows']=src.replace(seg,seg.replace("reason = 'unreadable thrown value';","reason = (err as any).message;"))
    if ret:
        end=m.end()
        j=src.index(ret,end); assert j-end<40,(msg,j-end)
        newret={"return [];":"return undefined as any;","return 0;":"return -1;"}[ret]
        muts['C_wrong_return']=src[:j]+newret+src[j+len(ret):]
    else:
        end=m.end(); j=src.index("return undefined;",end); assert j-end<40
        muts['C_wrong_return']=src[:j]+"return null as any;"+src[j+len("return undefined;"):]
    for name,body in muts.items():
        assert body!=src,name
        tag=f"H{i}_{name}"
        open(F,'w').write(body)
        try: rc,res=run(tag,test)
        finally:
            open(F,'wb').write(orig)
        ok=sha(open(F,'rb').read())==h0
        line=f"{tag}\tjest_rc={rc}\t{res}\trestored_sha_ok={ok}"
        print(line); out.write(line+'\n'); out.flush()
        assert ok
out.write('final sha '+sha(open(F,'rb').read())+' orig '+h0+'\n')
