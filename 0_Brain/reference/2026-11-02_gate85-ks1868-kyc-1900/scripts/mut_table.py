import re,glob,os
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900/logs/'
S=['saveVerification','getVerification','getVerificationsByUser','getVerificationStats','saveConsent']
MS=['M0_revert_hunk','M1_drop_inner_try','M2_fallback_String_err','M3_rethrow_all_after_log','M4_rethrow_only_unreadable','M5_constant_for_ALL_values','M6_nonError_branch_const_x','M7_msg_dropped_String_err','M10_log_removed']
k=s_=0
print('| Mutant | '+' | '.join(S)+' |'); print('|'+'---|'*(len(S)+1))
for m in MS:
    row=[]
    for s in S:
        p=W+f'mut_{s}__{m}.log'
        if not os.path.exists(p): row.append('n/a'); continue
        t=open(p).read()
        rc=re.search(r'^rc=(\d+)',t,re.M).group(1)
        tl=re.search(r'^\s+Tests\s+(.*)$',t,re.M); tl=tl.group(1).strip() if tl else '?'
        fails=sorted(set(re.findall(r'FAIL\s+src/__tests__/ks1868-kyc-([\w-]+?)-unreadable-throw\.test\.ts > [^>]+> (\S+ ks1868 \w+)',t)))
        cells=','.join(sorted(set(c.split()[-1] for _,c in fails)))
        files=sorted(set(f for f,_ in fails))
        v='KILLED' if rc!='0' else 'SURVIVED'
        k+=v=='KILLED'; s_+=v=='SURVIVED'
        row.append(f"{v} ({tl}; cells {cells or '-'}; files {'/'.join(files) or '-'})")
    print(f'| {m} | '+' | '.join(row)+' |')
print(f'killed {k}, survived {s_}')
