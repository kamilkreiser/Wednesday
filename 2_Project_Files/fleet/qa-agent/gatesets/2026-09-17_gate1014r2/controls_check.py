#!/usr/bin/env python3
"""controls_check.py — NEGATIVE FIXTURES for launch_qa_secuura_ks1176_1014r2.sh (second form, pin 7e89318bc), every run with --check ONLY (never a launch).
Test inputs are written into this gate set (neg_* / pos_*); the launcher reads them through its QA1014R2_* overrides. Each replacement asserts its anchor
count (>= 1 for token removals, == 1 for the verification.ts fixtures) and its absence after. rc of each run printed on its own line.
The three verification.ts fixtures start from develop's own blob a7a6d4605 (src/P16.routes_verification.ts, sha-asserted)."""
import subprocess, os, datetime, hashlib
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1014r2'
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1014r2-ks1176-tier1'
L = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1176_1014r2.sh'
H = '9ba0caf78b8ddb737541df38303b776c982521d2'
SUBJ = '[QA -> Wednesday] TIER 1 GATE #1014 ROUND 2 (KS-1176) 9ba0caf78'
R1 = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1176-1014-616c766a5-tier1-r1/'
prompt = open(B + '.prompt.txt').read(); brief = open(B + '.md').read()
def neg(name, text, old, new):
    n = text.count(old); assert n >= 1, (name, old, n); out = text.replace(old, new); assert old not in out; open(G + '/' + name, 'w').write(out); return n
def gitblob(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
dev = open(G + '/src/P16.routes_verification.ts', 'rb').read(); assert gitblob(dev).startswith('a7a6d4605'), gitblob(dev)
def vfix(name, old, new):
    s = dev.decode(); assert s.count(old) == 1, (name, s.count(old)); out = s.replace(old, new); open(G + '/' + name, 'w').write(out); return gitblob(out.encode())[:9]
print('controls_check', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
print('replacements:', {
    'nosubject': neg('neg_prompt_nosubject.txt', prompt, SUBJ, '[QA -> Wednesday] GATE #1014 9ba0caf78'),
    'notier': neg('neg_brief_notier.md', brief, 'TIER 1', 'TIER X'),
    'nosha': neg('neg_brief_nosha.md', brief, H, 'HEAD-SHA-REMOVED'),
    'nomail': neg('neg_prompt_nomail.txt', prompt, 'MAIL YOUR VERDICT', 'SEND YOUR RESULT'),
    'nofarm': neg('neg_prompt_nofarm.txt', prompt, 'node_modules per ENTRY', 'node_modules as needed'),
    'nor1report': neg('neg_prompt_nor1report.txt', prompt, R1, '<the round-1 report>'),
    'nodisposition': neg('neg_brief_nodisposition.md', brief, 'CLOSED / STILL OPEN / NEW', 'a disposition'),
    'noround2': neg('neg_brief_noround2.md', brief, 'ROUND 2', 'ROUND X'),
})
print('verification.ts fixtures (git blob):', {
    'INTO the #1014 hunk region': vfix('neg_verif_into_1014_hunk.ts', 'if (allowedTypes.length > 0 && body.documentType && !allowedTypes.includes(body.documentType as string)) {',
                                       'if (allowedTypes.length > 0 && (body.documentType || body.type) && !allowedTypes.includes((body.documentType || body.type) as string)) {'),
    'INTO the verify gate': vfix('neg_verif_into_verify_gate.ts', "if (verifierLevel !== 'none') {", "if (verifierLevel !== 'none' && verifierLevel !== '') {"),
    'OUTSIDE both regions': vfix('pos_verif_outside_regions.ts', '// Latest = highest blockNumber, fall back to most-recent confirmedAt.', '// Latest = highest blockNumber, fall back to most-recent confirmedAt. (QA fixture: a move outside both regions)'),
})
rows = [('N1 missing subject: prompt without the exact ROUND 2 verdict subject', {'QA1014R2_PROMPT': G + '/neg_prompt_nosubject.txt'}, 23, None),
        ('N2 missing tier: brief without TIER 1', {'QA1014R2_BRIEF': G + '/neg_brief_notier.md'}, 7, None),
        ('N3 missing SHA: brief without the head SHA', {'QA1014R2_BRIEF': G + '/neg_brief_nosha.md'}, 20, None),
        ('N4 missing mail step: prompt without MAIL YOUR VERDICT', {'QA1014R2_PROMPT': G + '/neg_prompt_nomail.txt'}, 12, None),
        ('N5 missing per-entry farm: prompt without node_modules per ENTRY', {'QA1014R2_PROMPT': G + '/neg_prompt_nofarm.txt'}, 22, None),
        ('N6 head override = the round-1 head 616c766a5', {'QA1014R2_HEAD': '616c766a57a51238450c99bbf1d59bb109e3841c'}, 6, None),
        ('N7 develop = the #1014 round-2 head (enforcement.ts be466fbf4 LANDED)', {'QA1014R2_CUR_DEV': H}, 19, 'has landed'),  # the launcher's case arm strips the LANDED prefix before printing (QA-EDIT-N7-NEEDLE)
        ('N8 develop = eb1051fd3, the pre-#1016 pin (verification.ts 04b3d980f CLEARED by region; the ks1072 test ABSENT refuses)', {'QA1014R2_CUR_DEV': 'eb1051fd39fe3edab4e0b1d1967515b758d4ba3f'}, 18, 'ks1072'),
        ('N9 develop = a226d94fe, #1016 branch head (every blob pinned; the compare pinned...develop is not ahead)', {'QA1014R2_CUR_DEV': 'a226d94fe8c6fbfecb81de415feb645302cdd166'}, 18, 'UNJUDGEABLE'),
        ('N10 develop verification.ts moved INTO the #1014 hunk region (fixture)', {'QA1014R2_VERIF_FILE': G + '/neg_verif_into_1014_hunk.ts'}, 18, 'hunk region'),
        ('N11 develop verification.ts moved INTO the verify gate (fixture)', {'QA1014R2_VERIF_FILE': G + '/neg_verif_into_verify_gate.ts'}, 18, 'hunk region'),
        ('P12 POSITIVE: develop verification.ts moved OUTSIDE both regions (fixture) must PASS', {'QA1014R2_VERIF_FILE': G + '/pos_verif_outside_regions.ts'}, 0, 'moved OUTSIDE'),
        ('N13 prompt without the round-1 report path', {'QA1014R2_PROMPT': G + '/neg_prompt_nor1report.txt'}, 24, None),
        ('N14 brief without CLOSED / STILL OPEN / NEW', {'QA1014R2_BRIEF': G + '/neg_brief_nodisposition.md'}, 25, None),
        ('N15 brief without ROUND 2', {'QA1014R2_BRIEF': G + '/neg_brief_noround2.md'}, 15, None)]
bad = 0
for label, env, want, needle in rows:
    e = dict(os.environ); e.update(env)
    p = subprocess.run([L, '--check'], env=e, stdin=subprocess.DEVNULL, capture_output=True, text=True)
    line = (p.stderr.strip().splitlines() or [''])[0] if p.returncode else next((l for l in p.stdout.splitlines() if 'develop' in l and ('OK' in l or 'origin develop' in l)), '')
    print(label, '| ' + ('stderr' if p.returncode else 'stdout') + ':', line[:420])
    print('rc=%d' % p.returncode)
    ok = p.returncode == want and (needle is None or needle in (p.stderr + p.stdout)); bad += (not ok)
    print('expected %d%s: %s' % (want, (" + text '" + needle + "'") if needle else '', 'OK' if ok else 'UNEXPECTED'))
print('unexpected rows', bad)
print('end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
