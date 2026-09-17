#!/usr/bin/env python3
"""make_fixtures_1028.py — negative / positive fixtures for the #1028 launcher's --check controls. Each brief/prompt fixture differs from the live file ONLY at
its guarded token (asserted replacement counts); auth.ts fixtures are exact blob bytes read with `git show` (a READ verb) from the checkout, blob ids asserted."""
import hashlib, subprocess, os
GS = os.path.dirname(os.path.abspath(__file__)); B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'; AU = 'Blockchain/Dev/services/api-gateway/src/middleware/auth.ts'
brief = open(B + '2026-09-17_secuura-1028-ks744-tier1.md').read(); prompt = open(B + '2026-09-17_secuura-1028-ks744-tier1.prompt.txt').read()
H = 'e39521cfb54cb5fd47c6bdae64ce707b3c9befce'; PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1207-1023-2f74491eb-tier1-r1/'
def mut(src, old, new, want):
    n = src.count(old); assert n == want, (old[:50], n, want); return src.replace(old, new)
F = {
 'neg_prompt_nosubject.txt': mut(prompt, '[QA -> Wednesday] TIER 1 GATE #1028 (KS-744) e39521cfb', '[QA -> Wednesday] TIER 1 GATE #1028 KS-744 e39521cfb', 1),
 'neg_prompt_nofarm.txt': mut(prompt, 'node_modules per ENTRY', 'node_modules by entry', 1),
 'neg_prompt_noprior.txt': mut(prompt, PRIOR, PRIOR.replace('ks1207-1023', 'ks1207-1023x'), 1),
 'neg_prompt_nottestedfirst.txt': mut(prompt, 'NOT-TESTED.written-first.md', 'NOT-TESTED.md', 1),
 'neg_brief_noaddendum.md': mut(brief, 'MERGE ADDENDUM', 'MERGE NOTE', 1),
 'neg_brief_nosha.md': mut(brief, H, H[:9], brief.count(H)),
 'neg_brief_round2.md': mut(brief, 'ROUND 1', 'ROUND 2', brief.count('ROUND 1')),
}
assert brief.count(H) >= 1 and brief.count('ROUND 1') >= 1
for n, t in F.items():
    open(GS + '/' + n, 'w').write(t); print('fixture', n, 'bytes', len(t), 'sha256', hashlib.sha256(t.encode()).hexdigest()[:12])
for n, ref, want in (('pos_auth_develop_b8fce678a.ts', '19f1e54750ce2b65312a687add2db4f5628edb7d', 'b8fce678a'), ('pos_auth_landed_6e1668362.ts', H, '6e1668362'),
                     ('neg_auth_unpinned_c673f9c9e.ts', 'fb503741a7481bf659705cfcfa661f64b8e4ab4d', 'c673f9c9e')):
    b = subprocess.run(['git', '-C', REPO, 'show', ref + ':' + AU], capture_output=True).stdout
    blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(); assert blob.startswith(want), (n, blob)
    open(GS + '/' + n, 'wb').write(b); print('fixture', n, 'blob', blob[:9])
