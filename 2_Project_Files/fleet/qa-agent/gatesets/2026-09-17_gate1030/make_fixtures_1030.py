#!/usr/bin/env python3
"""make_fixtures_1030.py — negative brief/prompt fixtures for the #1030 launcher's --check controls. Each fixture removes ONE guarded phrase
(case-insensitive, every occurrence) and asserts the phrase is gone (case-insensitive count 0) while the real file still carries it."""
import re, sys
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1030-ks1211-vitest-tier2'
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1030'
brief, prompt = open(B + '.md').read(), open(B + '.prompt.txt').read()
FIX = [('neg_prompt_nofarm.txt', prompt, 'farmed per ENTRY', 'shared per install'),
       ('neg_prompt_nosubject.txt', prompt, '[QA -> Wednesday] TIER 2 GATE #1030 (KS-1211) e43af4934 — ', '[QA -> Wednesday] GATE #1030 — '),
       ('neg_prompt_nottestedfirst.txt', prompt, 'NOT-TESTED.written-first.md', 'NOT-TESTED.md'),
       ('neg_prompt_nodocker.txt', prompt, 'Docker is NOT available', 'Docker may be used'),
       ('neg_prompt_nomail.txt', prompt, 'MAIL YOUR VERDICT', 'Report your verdict'),
       ('neg_prompt_nopushban.txt', prompt, 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout', 'Avoid pushing from the Secuura checkout'),
       ('neg_brief_noaddendum.md', brief, 'MERGE ADDENDUM', 'merge note'),
       ('neg_brief_notier1.md', brief, 'TIER 1 TRIGGERED', 'tier might change'),
       ('neg_brief_nosha.md', brief, 'e43af493418a1f13cfb60c994380fb74d79ad07e', 'e43af4934')]
for name, src, phrase, repl in FIX:
    n0 = len(re.findall(re.escape(phrase), src, flags=re.I))
    out = re.sub(re.escape(phrase), repl, src, flags=re.I)
    n1 = len(re.findall(re.escape(phrase), out, flags=re.I))
    if n0 == 0 or n1 != 0: print('FIXTURE FAILED', name, n0, n1); sys.exit(1)
    open(G + '/' + name, 'w').write(out)
    print('fixture %-30s phrase %r removed %d -> %d' % (name, phrase[:50], n0, n1))
