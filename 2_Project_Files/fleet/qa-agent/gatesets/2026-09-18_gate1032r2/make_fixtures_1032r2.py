#!/usr/bin/env python3
"""make_fixtures_1032r2.py — negative / positive fixtures for the #1032 ROUND 2 launcher's --check controls, under fixtures/ (from the round-1
make_fixtures_1032.py). Each brief/prompt fixture differs from the live file ONLY at its guarded token (asserted replacement counts); users.ts fixtures are
exact blob bytes read with `git show` (a READ verb) from the checkout, blob ids asserted; the unpinned fixture is develop's bytes plus one comment line."""
import hashlib, subprocess, os
GS = os.path.dirname(os.path.abspath(__file__)); FX = GS + '/fixtures'; os.makedirs(FX, exist_ok=True); B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'; USERS = 'Blockchain/Dev/services/auth/src/routes/users.ts'
brief = open(B + '2026-09-18_secuura-1032r2-ks1194-tier1.md').read(); prompt = open(B + '2026-09-18_secuura-1032r2-ks1194-tier1.prompt.txt').read()
H = '4306726977b55171a7c8c0eb5e42de078587a725'; R1 = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1194-1032-70ee7b6c0-tier1-r1/'
def mut(src, old, new, want):
    n = src.count(old); assert n == want and n >= 1, (old[:50], n, want); return src.replace(old, new)
F = {
 'neg_prompt_nosubject.txt': mut(prompt, '[QA -> Wednesday] TIER 1 GATE #1032 ROUND 2 (KS-1194) 430672697', '[QA -> Wednesday] TIER 1 GATE #1032 (KS-1194) 430672697', 1),
 'neg_prompt_nofarm.txt': mut(prompt, 'node_modules per ENTRY', 'node_modules by entry', prompt.count('node_modules per ENTRY')),
 'neg_prompt_nor1report.txt': mut(prompt, R1, R1.replace('70ee7b6c0-tier1-r1', '70ee7b6c0-tier1-rX'), prompt.count(R1)),
 'neg_prompt_nottestedfirst.txt': mut(prompt, 'NOT-TESTED.written-first.md', 'NOT-TESTED.md', prompt.count('NOT-TESTED.written-first.md')),
 'neg_prompt_nocsn.txt': mut(prompt, 'CLOSED / STILL OPEN / NEW', 'CLOSED OR OPEN', prompt.count('CLOSED / STILL OPEN / NEW')),
 'neg_prompt_nokamstap.txt': mut(prompt, "Kam's tap", "the seat's merge", prompt.count("Kam's tap")),
 'neg_brief_noaddendum.md': mut(brief, 'MERGE ADDENDUM', 'MERGE NOTE', brief.count('MERGE ADDENDUM')),
 'neg_brief_nokamstap.md': mut(brief, "Kam's tap", "the seat's merge", brief.count("Kam's tap")),
 'neg_brief_nosha.md': mut(brief, H, H[:9], brief.count(H)),
 'neg_brief_round1.md': mut(brief, 'ROUND 2', 'ROUND 1', brief.count('ROUND 2')),
 'neg_brief_tier2.md': mut(brief, 'TIER 1', 'TIER 2', brief.count('TIER 1')),
}
for n, t in F.items():
    open(FX + '/' + n, 'w').write(t); print('fixture', n, 'bytes', len(t), 'sha256', hashlib.sha256(t.encode()).hexdigest()[:12])
def blob(b): return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
show = lambda ref: subprocess.run(['git', '-C', REPO, 'show', ref + ':' + USERS], capture_output=True).stdout
dev = show('3961c2add8e1637b32e638f8f0952c328c00833e'); r1 = show('70ee7b6c03eeb7ef0609d6fc8fa5223e3647c039'); r2 = show(H)
assert blob(dev).startswith('c723a68af') and blob(r1).startswith('8299a2558') and blob(r2).startswith('3bfa47dcd')
unp = dev + b'\n// qa1032r2 control: a develop users.ts nobody pinned\n'; assert blob(unp)[:9] not in ('c723a68af', '8299a2558', '3bfa47dcd')
for n, b in (('pos_users_develop_c723a68af.ts', dev), ('pos_users_landed_r1_8299a2558.ts', r1), ('pos_users_landed_r2_3bfa47dcd.ts', r2), ('neg_users_unpinned_edit.ts', unp)):
    open(FX + '/' + n, 'wb').write(b); print('fixture', n, 'blob', blob(b)[:9])
