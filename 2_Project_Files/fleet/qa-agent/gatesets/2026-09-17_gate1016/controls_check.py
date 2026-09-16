#!/usr/bin/env python3
"""controls_check.py — NEGATIVE FIXTURES for launch_qa_secuura_ks1072_1016.sh, every run with --check ONLY (never a launch). Test inputs are written into
this gate set (neg_*); the launcher reads them through its QA1016_* overrides. Each replacement asserts its anchor count >= 1 and its absence after.
rc of each run printed on its own line."""
import subprocess, os, datetime
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1016'
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1016-ks1072-tier1'
L = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1072_1016.sh'
H = 'a226d94fe8c6fbfecb81de415feb645302cdd166'
SUBJ = '[QA -> Wednesday] TIER 1 GATE #1016 (KS-1072) a226d94fe'
prompt = open(B + '.prompt.txt').read(); brief = open(B + '.md').read()
def neg(name, text, old, new):
    n = text.count(old); assert n >= 1, (name, old, n); out = text.replace(old, new); assert old not in out; open(G + '/' + name, 'w').write(out); return n
print('controls_check', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
print('replacements:', {
    'nosubject': neg('neg_prompt_nosubject.txt', prompt, SUBJ, '[QA -> Wednesday] GATE #1016 a226d94fe'),
    'notier': neg('neg_brief_notier.md', brief, 'TIER 1', 'TIER X'),
    'nosha': neg('neg_brief_nosha.md', brief, H, 'HEAD-SHA-REMOVED'),
    'nomail': neg('neg_prompt_nomail.txt', prompt, 'MAIL YOUR VERDICT', 'SEND YOUR RESULT'),
    'nofarm': neg('neg_prompt_nofarm.txt', prompt, 'node_modules per ENTRY', 'node_modules as needed'),
    'noround1': neg('neg_brief_noround1.md', brief, 'ROUND 1', 'ROUND X'),
})
rows = [('N1 missing subject: prompt without the exact verdict subject', {'QA1016_PROMPT': G + '/neg_prompt_nosubject.txt'}, 23),
        ('N2 missing tier: brief without TIER 1', {'QA1016_BRIEF': G + '/neg_brief_notier.md'}, 7),
        ('N3 missing SHA: brief without the head SHA', {'QA1016_BRIEF': G + '/neg_brief_nosha.md'}, 20),
        ('N4 missing mail step: prompt without MAIL YOUR VERDICT', {'QA1016_PROMPT': G + '/neg_prompt_nomail.txt'}, 12),
        ('N5 missing per-entry farm: prompt without node_modules per ENTRY', {'QA1016_PROMPT': G + '/neg_prompt_nofarm.txt'}, 22),
        ('N6 head override = the PR parent 523f283c6', {'QA1016_HEAD': '523f283c6cd2550263ec9869dc5ee722be40df4e'}, 6),
        ('N7 develop = the #1016 head (verification.ts a7a6d4605 LANDED)', {'QA1016_CUR_DEV': H}, 19),
        ('N8 develop = dd66863dd (routes/verification.ts c83a2ae27, a blob nobody pinned)', {'QA1016_CUR_DEV': 'dd66863dd2858e97344652c1106d38f5e352a41b'}, 18),
        ('N9 develop = e0f41a8fa (every judged blob pinned, but behind the pin: the compare is not ahead)', {'QA1016_CUR_DEV': 'e0f41a8fafd64fa31524390cfeab320e822f3d15'}, 18),
        ('N10 brief without ROUND 1', {'QA1016_BRIEF': G + '/neg_brief_noround1.md'}, 15)]
bad = 0
for label, env, want in rows:
    e = dict(os.environ); e.update(env)
    p = subprocess.run([L, '--check'], env=e, stdin=subprocess.DEVNULL, capture_output=True, text=True)
    print(label, '| stderr:', (p.stderr.strip().splitlines() or [''])[0][:260])
    print('rc=%d' % p.returncode)
    ok = p.returncode == want; bad += (not ok)
    print('expected %d: %s' % (want, 'OK' if ok else 'UNEXPECTED'))
print('unexpected rows', bad)
print('end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
