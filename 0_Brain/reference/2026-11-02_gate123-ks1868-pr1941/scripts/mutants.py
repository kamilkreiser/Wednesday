# gate 123 mutants: product only, tests untouched, sha256 restore asserted after every run.
import subprocess, hashlib, json, sys, os, re
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate123-ks1868-pr1941'
A=W+'/repo/Blockchain/Dev/services/originate'; L=W+'/logs'
V1=A+'/src/routes/verification.ts'; V2=A+'/src/routes/verificationV2.ts'
BLINE="reason = String(error instanceof Error ? error.message : error);"
TESTS={'B1':'ks1868-verification-verify-hash-status-guards-coerce-message-o79b1','B2':'ks1868-verification-verify-file-guard-coerces-message-o79b2','B3':'ks1868-verification-v2-guards-coerce-message-o79b3','P3':'ks1868-verification-v2-chain-fact-catch-o78p3'}
ALLT=list(TESTS.values())
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def lines_of(p): return open(p).read().split('\n')
def idx_nth(ls, needle, n):
    hits=[i for i,l in enumerate(ls) if needle in l]; return hits[n]
# sites: (name, file, pass, locate) ; B occurrences in order of appearance
SITES=[('B2:758',V1,'B2',0),('B1:1443',V1,'B1',1),('B1:1478',V1,'B1',2),('B1:1506',V1,'B1',3),('B3:446',V2,'B3',0),('B3:488',V2,'B3',1),('P3:111',V2,'P3',None)]
def mutate(ls, site, m):
    name,f,ps,n=site; ls=list(ls)
    if ps=='P3':
        i=idx_nth(ls,'reason = err?.message;',0); ind=ls[i][:len(ls[i])-len(ls[i].lstrip())]
        assert ls[i-1].strip()=='try {' and ls[i+1].strip()=='} catch {' and "unreadable thrown value" in ls[i+2]
        logi=i+4; assert 'chain-fact read failed' in ls[logi]
        if m=='M0_revert_log_read': ls[logi]=ls[logi].replace('{ error: reason }','{ error: err?.message }')
        elif m=='M1_drop_try': ls[i-1]=ind[:-2]+'{'; ls[i+1]=ind[:-2]+'}'; ls[i+2]=''; ls[i+3]=''
        elif m=='M2_fallback_wrong_constant': ls[i+2]=ls[i+2].replace("'unreadable thrown value'","'x'")
        elif m=='M3_constant_for_all': ls[i]=ind+"reason = 'unreadable thrown value';"
        elif m=='M4_log_wrong_value': ls[i]=ind+'reason = String(err);'
        elif m=='M5_rethrow_when_unreadable': ls[i+2]=ind+'throw err;'
        elif m=='M6_fallback_undefined': ls[i+2]=ind+'reason = undefined;'
        return ls
    i=idx_nth(ls,BLINE,n); ind=ls[i][:len(ls[i])-len(ls[i].lstrip())]
    assert ls[i-1].strip()=='try {' and ls[i+1].strip()=='} catch {' and "unreadable thrown value" in ls[i+2]
    if m=='M0_revert': ls[i]=ind+'reason = error instanceof Error ? error.message : String(error);'
    elif m=='M1_drop_try': ls[i-1]=ind[:-2]+'{'; ls[i+1]=ind[:-2]+'}'; ls[i+2]=''; ls[i+3]=''
    elif m=='M2_fallback_wrong_constant': ls[i+2]=ls[i+2].replace("'unreadable thrown value'","'x'")
    elif m=='M3_constant_for_all': ls[i]=ind+"reason = 'unreadable thrown value';"
    elif m=='M4_log_wrong_value': ls[i]=ind+'reason = String(error);'
    elif m=='M5_rethrow_when_unreadable': ls[i+2]=ind+'throw error;'
    elif m=='M6_coerce_error_not_message': ls[i]=ind+'reason = error instanceof Error ? String(error) : String(error);'
    return ls
MB=['M0_revert','M1_drop_try','M2_fallback_wrong_constant','M3_constant_for_all','M4_log_wrong_value','M5_rethrow_when_unreadable']
MP=['M0_revert_log_read','M1_drop_try','M2_fallback_wrong_constant','M3_constant_for_all','M4_log_wrong_value','M5_rethrow_when_unreadable','M6_fallback_undefined']
s0={V1:sha(V1),V2:sha(V2)}
rows=[]
only=sys.argv[1:]
for site in SITES:
    for m in (MP if site[2]=='P3' else MB):
        tag=f"{site[0]}__{m}".replace(':','_')
        if only and tag not in only: continue
        f=site[1]; orig=open(f).read()
        new='\n'.join(mutate(orig.split('\n'),site,m)); assert new!=orig
        open(f,'w').write(new)
        jo=f"{L}/mut_{tag}.json"; lo=f"{L}/mut_{tag}.log"
        if os.path.exists(jo): os.remove(jo)
        subprocess.run(['bash',W+'/scripts/jest.sh',jo,lo]+ALLT)
        open(f,'w').write(orig); ok=sha(V1)==s0[V1] and sha(V2)==s0[V2]
        res={'site':site[0],'mutant':m,'restore':ok}
        try:
            d=json.load(open(jo)); fails=[]
            for tr in d['testResults']:
                fn=tr['name'].split('/')[-1].replace('ks1868-verification-','')[:30]
                if not tr['assertionResults'] and tr.get('message'): fails.append((fn,'SUITE_FAIL:'+tr['message'][:120].replace('\n',' ')))
                for a in tr['assertionResults']:
                    if a['status']!='passed':
                        fm=' '.join(a['failureMessages']); fails.append((fn,a['title'][:60],'expect(' in fm))
            res['killed']=bool(fails); res['fails']=fails; res['nfail']=len(fails)
        except Exception as e: res['killed']=None; res['err']=str(e)
        rows.append(res); print(json.dumps(res)[:400], flush=True)
        if not ok: print('RESTORE FAILED'); sys.exit(3)
json.dump(rows,open(L+'/mutants_rows.json','w'),indent=1)
