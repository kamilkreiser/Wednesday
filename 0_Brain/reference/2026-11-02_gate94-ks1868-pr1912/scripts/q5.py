import re,sys,subprocess,hashlib
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate94-ks1868-pr1912'
N='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night'
R=G+'/repo'
P='Blockchain/Dev/services/security/src/index.ts'
def product_hunks(text):
    # return list of hunks (header, body lines) for index.ts only
    out=[];cur=None;inprod=False
    for l in text.splitlines():
        if l.startswith('diff --git'): inprod=l.endswith('/src/index.ts'); cur=None; continue
        if l.startswith('```'): cur=None; continue
        if l.startswith('@@'):
            # in READY files without diff --git, decide by the previous '+++' line
            cur=[l,[]]; (out.append(cur) if inprod else None); continue
        if l.startswith('+++ '): inprod=l.rstrip().endswith('/src/index.ts'); continue
        if l.startswith('--- '): continue
        if cur is not None and inprod and (l[:1] in ' +-' or l==''): cur[1].append(l)
    return out
pr=subprocess.run(['git','-C',R,'diff','refs/gate/pr1912^','refs/gate/pr1912','--',P],capture_output=True,text=True).stdout
PRH=product_hunks(pr)
print('PR product hunks:',len(PRH),[h[0][:22] for h in PRH])
names={'O54-P1':(0,'ks_1868_o54_p1_security_key_register_save_catch_unreadable_throw','READY_KS-1868-KS-1868-O54-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-SECURITY-KEY-REGISTER-SAVE-CATCH-PASS-7of7_2026-11-02.diff.md'),
 'O56-P1':(1,None,'READY_KS-1868-KS-1868-O56-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-SECURITY-KEY-REVOKE-SAVE-CATCH-PASS-7of7_2026-11-02.diff.md'),
 'O56-P2':(2,None,'READY_KS-1868-KS-1868-O56-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-SECURITY-ADMIN-SCOPES-PUT-CATCH-PASS-7of7_2026-11-02.diff.md')}
import glob,os
for k,(idx,brief,ready) in names.items():
    rt=open(N+'/'+ready).read()
    has_dg=bool(re.search(r'^diff --git a/'+re.escape(P),rt,re.M))
    RH=product_hunks(rt)
    if not brief:
        c=[d for d in glob.glob(N+'/briefs/ks_1868_'+k.lower().replace('-','_')+'*')]; brief=os.path.basename(c[0]) if c else None
    gt=open(N+'/briefs/'+brief+'/golden.diff').read() if brief else ''
    GH=product_hunks(gt)
    def body(hs): return [h[1] for h in hs]
    def strip_trailing(hs): return [re.sub(r'(@@ [^@]+ @@).*',r'\1',h[0]) for h in hs]
    print(f'{k}: READY has diff --git line for index.ts: {has_dg}; hunks READY={len(RH)} golden={len(GH)}')
    print(f'  READY body == golden body: {body(RH)==body(GH)}; READY @@ (ranges) == golden: {strip_trailing(RH)==strip_trailing(GH)}; full @@ equal: {[h[0] for h in RH]==[h[0] for h in GH]}')
    print(f'  READY body == PR hunk {idx} body: {body(RH)==[PRH[idx][1]]}; @@ ranges equal PR: {strip_trailing(RH)==strip_trailing([PRH[idx]])}')
    print('   READY @@:',[h[0] for h in RH]); print('   golden@@:',[h[0] for h in GH]); print('   PR    @@:',PRH[idx][0])
