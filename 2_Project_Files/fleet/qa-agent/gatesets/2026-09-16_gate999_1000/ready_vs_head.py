#!/usr/bin/env python3
"""Compare each READY diff's + lines against the PR head file bytes (from the contents API, saved by gh_read.py). Read-only."""
import re, difflib, glob, sys
N='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/'
G='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9aed5a67-2729-4892-b685-13ab87142a58/scratchpad/g9991000/gh/'
pairs=[('READY_KS-1130-E1twin_*.diff.md','pr999_head_*ks1130-tier2-e1-twin.test.ts'),
       ('READY_KS-1130-E7twin_*.diff.md','pr999_head_*ks1130-tier2-e7-twin.test.ts'),
       ('READY_KS-1130-E3twin_*.diff.md','pr999_head_*ks1130-tier2-e3-twin.test.ts'),
       ('READY_KS-960_*.diff.md','pr1000_head_*ks960-two-schema-sources-disagree-on-whether.test.ts')]
for r,h in pairs:
    rp=glob.glob(N+r); hp=[p for p in glob.glob(G+h) if not p.endswith('.patch')]
    assert len(rp)==1 and len(hp)==1, (r,rp,hp)
    txt=open(rp[0],encoding='utf-8').read()
    blocks=re.findall(r'```diff\n(.*?)```', txt, re.S)
    plus=[]
    for b in blocks:
        for l in b.split('\n'):
            if l.startswith('+++'): continue
            if l.startswith('+'): plus.append(l[1:])
    head=open(hp[0],encoding='utf-8').read().split('\n')
    if head and head[-1]=='': head=head[:-1]
    d=[x for x in difflib.unified_diff(plus, head, 'READY+', 'head', n=0, lineterm='')]
    print(f"{r}: diff blocks={len(blocks)} READY+ lines={len(plus)} head lines={len(head)} identical={plus==head}")
    for x in d[:40]: print('   ', x[:160])
