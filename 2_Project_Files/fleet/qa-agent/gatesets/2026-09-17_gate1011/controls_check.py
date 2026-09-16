#!/usr/bin/env python3
"""controls_check.py — NEGATIVE CONTROLS for launch_qa_secuura_ks871_1011.sh, every run with --check ONLY (never a launch). Test inputs are
written into this gate set (neg_*); the launcher reads them through its QA1011_* overrides. rc of each run printed on its own line."""
import subprocess, os, datetime
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1011'
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1011-ks871-tier1'
L = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks871_1011.sh'
H = '0a1f8900c7094fbdaed1099799c029e351296b39'
SUBJ = '[QA -> Wednesday] TIER 1 GATE #1011 (KS-871) 0a1f8900c'
prompt = open(B + '.prompt.txt').read(); brief = open(B + '.md').read()
def neg(name, text, old, new):
    n = text.count(old); assert n >= 1, (name, old, n); out = text.replace(old, new); assert old not in out; open(G + '/' + name, 'w').write(out); return n
print('controls_check', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
print('replacements:', {'nomail': neg('neg_prompt_nomail.txt', prompt, 'MAIL YOUR VERDICT', 'SEND YOUR RESULT'),
                        'nosha': neg('neg_brief_nosha.md', brief, H, 'HEAD-SHA-REMOVED'),
                        'notier': neg('neg_brief_notier.md', brief, 'TIER 1', 'TIER X'),
                        'nofarm': neg('neg_prompt_nofarm.txt', prompt, 'node_modules per ENTRY', 'node_modules as needed'),
                        'nosubject': neg('neg_prompt_nosubject.txt', prompt, SUBJ, '[QA -> Wednesday] GATE #1011 0a1f8900c')})
rows = [('N1 head override (#1010 head c3213b04e)', {'QA1011_HEAD': 'c3213b04e3ad96068c367f7e0ba426822d32cda9'}, 6),
        ('N2 prompt without the mail step', {'QA1011_PROMPT': G + '/neg_prompt_nomail.txt'}, 12),
        ('N3 brief without the head SHA', {'QA1011_BRIEF': G + '/neg_brief_nosha.md'}, 20),
        ('N4 brief without TIER 1', {'QA1011_BRIEF': G + '/neg_brief_notier.md'}, 7),
        ('N5 prompt without per-ENTRY farm', {'QA1011_PROMPT': G + '/neg_prompt_nofarm.txt'}, 22),
        ('N6 prompt without the exact verdict subject', {'QA1011_PROMPT': G + '/neg_prompt_nosubject.txt'}, 23),
        ('N7 develop = the #1011 head (audit.ts f5a83ba2c LANDED)', {'QA1011_CUR_DEV': H}, 19),
        ('N8 develop = 0f489b7da (KS-28: audit.ts a blob nobody pinned)', {'QA1011_CUR_DEV': '0f489b7da4e699e852a126bb41a922b8ca1b4462'}, 18)]
bad = 0
for label, env, want in rows:
    e = dict(os.environ); e.update(env)
    p = subprocess.run([L, '--check'], env=e, stdin=subprocess.DEVNULL, capture_output=True, text=True)
    print(label, '| stderr:', (p.stderr.strip().splitlines() or [''])[0][:220])
    print('rc=%d' % p.returncode)
    ok = p.returncode == want; bad += (not ok)
    print('expected %d: %s' % (want, 'OK' if ok else 'UNEXPECTED'))
print('unexpected rows', bad)
print('end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
