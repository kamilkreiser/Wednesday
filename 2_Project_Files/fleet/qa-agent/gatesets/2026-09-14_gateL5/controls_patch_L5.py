#!/usr/bin/env python3
"""controls_patch_L5.py — re-point the prior set's controls_check.sh at develop M20 (QAL5_ overrides) by asserted substitutions,
and write the neg-token copy (two controls inverted). Template sha256 asserted."""
import hashlib, os
O='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gateL5'
src=O+'/prior/controls_check.sh'; dst=O+'/controls_check.sh'
s=open(src,encoding='utf-8').read(); got=hashlib.sha256(s.encode()).hexdigest()[:16]
assert got=='d5891925ed19b0b0', got; print('template controls_check.sh sha256', got, '(asserted)')
n=0
def sub(old,new,count=1):
    global s,n; c=s.count(old); assert c==count, f'{c}!={count}: {old[:80]!r}'; s=s.replace(old,new); n+=1
sub('# controls_check.sh — re-grep every §4 positive-control token of the #799 / #880 / #985 (L5) brief at the PINNED SHAs through',
    '# controls_check.sh — re-grep every §4 positive-control token of the L5 (#799 / #880 / #985) brief at the PINNED SHAs through')
sub('# fcd8a01e4 and its parent 6da848891. Tokens were derived',
    '# fcd8a01e4 and its parent 6da848891. develop is read at M20 a53343502 (the L5 launcher\'s pin; every develop blob below must\n# read as at M18 — the M18 == M20 equality the brief rests on is asserted HERE, through the API, file by file). Tokens were derived')
sub('DEV="${QA799_DEVELOP:-6e78961e1d04277ecbdb0537e630afa0bf63b13c}"   # M19 (#982\'s squash, services/auth only) — every develop blob below must read as at M18',
    'DEV="${QAL5_DEVELOP:-a5334350221c819f54d4a20a3308daeb9ca09617}"   # M20 (#903\'s squash; M19 = #982\'s, services/auth only) — every develop blob below must read as at M18')
sub('QA799_','QAL5_',5)   # HEAD, MERGE, P38, HEAD_880, HEAD_985 (DEVELOP was rewritten above) — grep -n read 6 in the template
sub('qa799ctl.XXXXXX','qaL5ctl.XXXXXX')
assert 'QA799_' not in s and '6e78961e1' not in s
open(dst,'w',encoding='utf-8').write(s); os.chmod(dst,0o755)
print(f'{n} substitutions asserted; written {dst} sha256 {hashlib.sha256(s.encode()).hexdigest()[:16]}')
t=s
old='chk yaml880 "retires the prior active keys of the same" 1'; assert t.count(old)==1
t=t.replace(old,'chk yaml880 "retires the prior active keys of the same" 0\nchk yaml880 "a token that is NOT in this yaml" 1')
open(O+'/controls_check.neg-token.sh','w',encoding='utf-8').write(t); print('neg-token copy written (2 controls inverted: a present token demanded 0, an absent token demanded 1)')
