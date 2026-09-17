#!/usr/bin/env python3
"""make_fixtures_1031.py — negative / positive fixtures for the #1031 launcher's --check controls, under fixtures/. Each brief/prompt fixture differs from
the live file ONLY at its guarded token (asserted replacement counts); documents.ts fixtures are exact blob bytes read with `git show` (a READ verb) from the
checkout, blob ids asserted; the unpinned fixture is develop's bytes plus one comment line (its blob asserted different from both pins)."""
import hashlib, subprocess, os
GS = os.path.dirname(os.path.abspath(__file__)); FX = GS + '/fixtures'; os.makedirs(FX, exist_ok=True); B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'; DOCS = 'Blockchain/Dev/services/originate/src/routes/documents.ts'
brief = open(B + '2026-09-17_secuura-1031-ks1213-tier1.md').read(); prompt = open(B + '2026-09-17_secuura-1031-ks1213-tier1.prompt.txt').read()
H = 'be8596a29af15477cb0cbf4b8684e35e63c38e9f'; PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1202-1024-d1a328088-tier1-r1/'
def mut(src, old, new, want):
    n = src.count(old); assert n == want and n >= 1, (old[:50], n, want); return src.replace(old, new)
F = {
 'neg_prompt_nosubject.txt': mut(prompt, '[QA -> Wednesday] TIER 1 GATE #1031 (KS-1213) be8596a29', '[QA -> Wednesday] TIER 1 GATE #1031 KS-1213 be8596a29', 1),
 'neg_prompt_nofarm.txt': mut(prompt, 'node_modules per ENTRY', 'node_modules by entry', prompt.count('node_modules per ENTRY')),
 'neg_prompt_noprior.txt': mut(prompt, PRIOR, PRIOR.replace('ks1202-1024', 'ks1202-1024x'), prompt.count(PRIOR)),
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
dev = subprocess.run(['git', '-C', REPO, 'show', '75ad0e55c6335a5f34f6d0b74dfe00b334b2eb2e:' + DOCS], capture_output=True).stdout
head = subprocess.run(['git', '-C', REPO, 'show', H + ':' + DOCS], capture_output=True).stdout
assert blob(dev).startswith('de9b5ae25') and blob(head).startswith('e3eeb5a68')
unp = dev + b'\n// qa1031 control: a develop documents.ts nobody pinned\n'; assert blob(unp)[:9] not in ('de9b5ae25', 'e3eeb5a68')
for n, b in (('pos_docs_develop_de9b5ae25.ts', dev), ('pos_docs_landed_e3eeb5a68.ts', head), ('neg_docs_unpinned_edit.ts', unp)):
    open(FX + '/' + n, 'wb').write(b); print('fixture', n, 'blob', blob(b)[:9])
