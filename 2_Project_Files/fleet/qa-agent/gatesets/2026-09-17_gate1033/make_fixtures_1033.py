#!/usr/bin/env python3
"""make_fixtures_1033.py — negative brief/prompt fixtures for the #1033 launcher's --check controls. Each fixture removes ONE guarded phrase
(case-insensitive, every occurrence) and asserts the phrase is gone (case-insensitive count 0) while the real file still carries it."""
import re, sys
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1033-ks763-mysql2-tier1'
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1033/fixtures'
brief, prompt = open(B + '.md').read(), open(B + '.prompt.txt').read()
FIX = [('neg_prompt_nofarm.txt', prompt, 'farmed per ENTRY', 'shared per install'),
       ('neg_prompt_nosubject.txt', prompt, '[QA -> Wednesday] TIER 1 GATE #1033 (KS-763) 2cab54988 — ', '[QA -> Wednesday] GATE #1033 — '),
       ('neg_prompt_nottestedfirst.txt', prompt, 'NOT-TESTED.written-first.md', 'NOT-TESTED.md'),
       ('neg_prompt_nocontainer.txt', prompt, 'name it uniquely', 'use any container'),
       ('neg_prompt_nomail.txt', prompt, 'MAIL YOUR VERDICT', 'Report your verdict'),
       ('neg_prompt_nopushban.txt', prompt, 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout', 'Avoid pushing from the Secuura checkout'),
       ('neg_prompt_nonpmver.txt', prompt, 'npm-version dependent', 'reproducible with any npm'),
       ('neg_brief_noaddendum.md', brief, 'MERGE ADDENDUM', 'merge note'),
       ('neg_brief_noreach.md', brief, 'RUNTIME REACH FIRST', 'reach, eventually'),
       ('neg_brief_nosha.md', brief, '2cab54988b4e7b71d403576719f5fd80e470fa92', '2cab54988')]
for name, src, phrase, repl in FIX:
    n0 = len(re.findall(re.escape(phrase), src, flags=re.I))
    out = re.sub(re.escape(phrase), repl, src, flags=re.I)
    n1 = len(re.findall(re.escape(phrase), out, flags=re.I))
    if n0 == 0 or n1 != 0: print('FIXTURE FAILED', name, n0, n1); sys.exit(1)
    open(G + '/' + name, 'w').write(out)
    print('fixture %-30s phrase %r removed %d -> %d' % (name, phrase[:50], n0, n1))
