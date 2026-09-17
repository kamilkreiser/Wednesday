#!/usr/bin/env python3
"""make_fixtures_1034.py — negative / positive fixtures for the #1034 launcher's --check controls, under fixtures/ (derived from make_fixtures_1032.py). Each
brief/prompt fixture differs from the live file ONLY at its guarded token (asserted replacement counts); auth.ts fixtures are exact blob bytes read with
`git show` (a READ verb) from the checkout, blob ids asserted; the unpinned fixture is develop's bytes plus one comment line (blob asserted different)."""
import hashlib, subprocess, os
GS = os.path.dirname(os.path.abspath(__file__)); FX = GS + '/fixtures'; os.makedirs(FX, exist_ok=True); B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'; AUTH = 'Blockchain/Dev/services/api-gateway/src/middleware/auth.ts'
brief = open(B + '2026-09-17_secuura-1034-ks1215-tier1.md').read(); prompt = open(B + '2026-09-17_secuura-1034-ks1215-tier1.prompt.txt').read()
print('live brief sha256', hashlib.sha256(brief.encode()).hexdigest()[:16], 'bytes', len(brief.encode()), '| live prompt sha256', hashlib.sha256(prompt.encode()).hexdigest()[:16], 'bytes', len(prompt.encode()))
H = 'fd81a75f0688f6cbe1e5f79b061bb1369c88f477'; PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1207-1023-2f74491eb-tier1-r1/'
def mut(src, old, new, want):
    n = src.count(old); assert n == want and n >= 1, (old[:50], n, want); return src.replace(old, new)
F = {
 'neg_prompt_nosubject.txt': mut(prompt, '[QA -> Wednesday] TIER 1 GATE #1034 (KS-1215) fd81a75f0', '[QA -> Wednesday] TIER 1 GATE #1034 KS-1215 fd81a75f0', 1),
 'neg_prompt_nofarm.txt': mut(prompt, 'node_modules per ENTRY', 'node_modules by entry', prompt.count('node_modules per ENTRY')),
 'neg_prompt_noprior.txt': mut(prompt, PRIOR, PRIOR.replace('ks1207-1023', 'ks1207-1023x'), prompt.count(PRIOR)),
 'neg_prompt_nottestedfirst.txt': mut(prompt, 'NOT-TESTED.written-first.md', 'NOT-TESTED.md', prompt.count('NOT-TESTED.written-first.md')),
 'neg_prompt_nocsn.txt': mut(prompt, 'CLOSED / STILL OPEN / NEW', 'CLOSED OR OPEN', prompt.count('CLOSED / STILL OPEN / NEW')),
 'neg_brief_noaddendum.md': mut(brief, 'MERGE ADDENDUM', 'MERGE NOTE', brief.count('MERGE ADDENDUM')),
 'neg_brief_nosha.md': mut(brief, H, H[:9], brief.count(H)),
 'neg_brief_round2.md': mut(brief, 'ROUND 1', 'ROUND 2', brief.count('ROUND 1')),
 'neg_brief_tier2.md': mut(brief, 'TIER 1', 'TIER 2', brief.count('TIER 1')),
}
for n, t in F.items():
    open(FX + '/' + n, 'w').write(t); print('fixture', n, 'bytes', len(t), 'sha256', hashlib.sha256(t.encode()).hexdigest()[:12])
def blob(b): return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
dev = subprocess.run(['git', '-C', REPO, 'show', '27e53ec3aa010b50cd9b2e4a1d15cbb34605ba7d:' + AUTH], capture_output=True).stdout
head = subprocess.run(['git', '-C', REPO, 'show', H + ':' + AUTH], capture_output=True).stdout
assert blob(dev).startswith('6e1668362') and blob(head).startswith('bf09d315a')
unp = dev + b'\n// qa1034 control: a develop auth.ts nobody pinned\n'; assert blob(unp)[:9] not in ('6e1668362', 'bf09d315a')
for n, b in (('pos_auth_develop_6e1668362.ts', dev), ('pos_auth_landed_bf09d315a.ts', head), ('neg_auth_unpinned_edit.ts', unp)):
    open(FX + '/' + n, 'wb').write(b); print('fixture', n, 'blob', blob(b)[:9])
