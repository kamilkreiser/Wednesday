# gate 124 mutants: product only (certifications.ts), tests untouched, sha256 restore asserted after every run.
import subprocess, hashlib, json, sys, os
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate124-ks1868-pr1942'
A=W+'/repo/Blockchain/Dev/services/originate'; L=W+'/logs'; F=A+'/src/routes/certifications.ts'
ALLT=['ks1868-certifications-issue-anchoring-catch-o79p2','ks1868-certifications-issue-compensating-delete-catch-o79p5','ks1868-certifications-issue-holder-check-and-legacy-update-catches-o79p4','ks1868-certifications-issue-reserve-save-charge-catches-o79p3','ks1868-certifications-recertify-anchoring-catch-o79p1']
# (name, var, thrown, base expression)
SITES=[('A4:holder','errMsg','err',"err instanceof Error ? err.message : String(err)"),
       ('A3:reserveErr','reason','reserveErr',"reserveErr instanceof Error ? reserveErr.message : String(reserveErr)"),
       ('A2:issueAnchor','reason','err',"err?.message"),
       ('A5:delErr','reason','delErr',"delErr instanceof Error ? delErr.message : String(delErr)"),
       ('A3:saveErr','reason','saveErr',"saveErr instanceof Error ? saveErr.message : String(saveErr)"),
       ('A4:updateErr','reason','updateErr',"updateErr instanceof Error ? updateErr.message : String(updateErr)"),
       ('A3:chargeErr','reason','chargeErr',"chargeErr instanceof Error ? chargeErr.message : String(chargeErr)"),
       ('A1:recertifyAnchor','reason','err',"err?.message")]
MUT=['M0_revert','M1_drop_try','M2_fallback_x','M3_constant_for_all','M4_log_String_of_value','M5_rethrow_in_fallback','M6_fallback_undefined']
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def locate(ls):
    hits=[i for i,l in enumerate(ls) if l.strip().startswith(('reason = String(','errMsg = String(')) and ' instanceof Error ? ' in l and 'String(error instanceof' not in l]
    assert len(hits)==8, hits; return hits
def mutate(ls, k, m):
    name,var,x,basex=SITES[k]; ls=list(ls); i=locate(ls)[k]
    assert f'{var} = String({x} instanceof Error ? {x}.message : {x});' == ls[i].strip(), ls[i]
    assert ls[i-1].strip()=='try {' and ls[i+1].strip()=='} catch {' and ls[i+2].strip()==f"{var} = 'unreadable thrown value';" and ls[i+3].strip()=='}'
    ind=ls[i][:len(ls[i])-len(ls[i].lstrip())]
    if m=='M0_revert': ls[i-1]=ind[:-2]+'{'; ls[i]=ind+f'{var} = {basex};'; ls[i+1]=ind[:-2]+'}'; ls[i+2]=''; ls[i+3]=''
    elif m=='M1_drop_try': ls[i-1]=ind[:-2]+'{'; ls[i+1]=ind[:-2]+'}'; ls[i+2]=''; ls[i+3]=''
    elif m=='M2_fallback_x': ls[i+2]=ind+f"{var} = 'x';"
    elif m=='M3_constant_for_all': ls[i]=ind+f"{var} = 'unreadable thrown value';"
    elif m=='M4_log_String_of_value': ls[i]=ind+f'{var} = String({x});'
    elif m=='M5_rethrow_in_fallback': ls[i+2]=ind+f'throw {x};'
    elif m=='M6_fallback_undefined': ls[i+2]=ind+f'{var} = undefined as any;'
    elif m=='M7_fallback_uuid': ls[i+2]=ind+f"{var} = 'uuid';"
    return ls
s0=sha(F); rows=[]; only=sys.argv[1:]
plan=[(k,m) for k in range(8) for m in MUT]+[(0,'M7_fallback_uuid')]
for k,m in plan:
    tag=f"{SITES[k][0]}__{m}".replace(':','_')
    if only and tag not in only: continue
    orig=open(F).read(); new='\n'.join(mutate(orig.split('\n'),k,m)); assert new!=orig
    open(F,'w').write(new)
    jo=f"{L}/mut_{tag}.json"; lo=f"{L}/mut_{tag}.log"
    subprocess.run(['bash',W+'/scripts/jest.sh',jo,lo]+ALLT)
    open(F,'w').write(orig); ok=sha(F)==s0
    res={'site':SITES[k][0],'mutant':m,'restore':ok}
    try:
        d=json.load(open(jo)); fails=[]
        for tr in d['testResults']:
            fn=tr['name'].split('/')[-1].replace('ks1868-certifications-','')[:34]
            if not tr['assertionResults'] and tr.get('message'): fails.append((fn,'SUITE_FAIL:'+tr['message'][:160].replace('\n',' ')))
            for a in tr['assertionResults']:
                if a['status']!='passed':
                    fm=' '.join(a['failureMessages']); fails.append((fn,a['title'][:70],'expect(' in fm))
        res['killed']=bool(fails); res['fails']=fails; res['nfail']=len(fails)
        res['by_assertion']=bool(fails) and all(len(f)==3 and f[2] for f in fails)
    except Exception as e: res['killed']=None; res['err']=str(e)
    rows.append(res); print(json.dumps(res)[:500], flush=True)
    if not ok: print('RESTORE FAILED'); sys.exit(3)
json.dump(rows,open(L+'/mutants_rows.json','w'),indent=1)
print('DONE', len(rows), 'killed', sum(1 for r in rows if r.get('killed')), 'survived', [ (r['site'],r['mutant']) for r in rows if r.get('killed') is False])
