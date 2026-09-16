#!/usr/bin/env python3
"""controls_check.py — NEGATIVE CONTROLS for launch_qa_secuura_ks871_1011r2.sh, every run with --check ONLY (never a launch). Test inputs are written
into this gate set (neg_*); the launcher reads them through its QA1011R2_* overrides. Each replacement asserts its anchor count >= 1 and its absence
after. rc of each run printed on its own line."""
import subprocess, os, datetime
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1011r2'
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1011r2-ks871-tier1'
L = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks871_1011r2.sh'
H = '6dc8256448b50de6a15519001a4f7032ace1ae19'
SUBJ = '[QA -> Wednesday] TIER 1 GATE #1011 ROUND 2 (KS-871) 6dc825644'
R1 = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks871-1011-0a1f8900c-tier1-r1/'
prompt = open(B + '.prompt.txt').read(); brief = open(B + '.md').read()
def neg(name, text, old, new):
    n = text.count(old); assert n >= 1, (name, old, n); out = text.replace(old, new); assert old not in out; open(G + '/' + name, 'w').write(out); return n
print('controls_check', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
print('replacements:', {
    'nosubject': neg('neg_prompt_nosubject.txt', prompt, SUBJ, '[QA -> Wednesday] GATE #1011 6dc825644'),
    'notier': neg('neg_brief_notier.md', brief, 'TIER 1', 'TIER X'),
    'nosha': neg('neg_brief_nosha.md', brief, H, 'HEAD-SHA-REMOVED'),
    'nomail': neg('neg_prompt_nomail.txt', prompt, 'MAIL YOUR VERDICT', 'SEND YOUR RESULT'),
    'nofarm': neg('neg_prompt_nofarm.txt', prompt, 'node_modules per ENTRY', 'node_modules as needed'),
    'nor1report': neg('neg_prompt_nor1report.txt', prompt, R1, '<the round-1 report>'),
    'nodisposition': neg('neg_brief_nodisposition.md', brief, 'CLOSED / STILL OPEN / NEW', 'a disposition'),
    'noround2': neg('neg_brief_noround2.md', brief, 'ROUND 2', 'ROUND X'),
})
rows = [('N1 missing subject: prompt without the exact ROUND 2 verdict subject', {'QA1011R2_PROMPT': G + '/neg_prompt_nosubject.txt'}, 23),
        ('N2 missing tier: brief without TIER 1', {'QA1011R2_BRIEF': G + '/neg_brief_notier.md'}, 7),
        ('N3 missing SHA: brief without the head SHA', {'QA1011R2_BRIEF': G + '/neg_brief_nosha.md'}, 20),
        ('N4 missing mail step: prompt without MAIL YOUR VERDICT', {'QA1011R2_PROMPT': G + '/neg_prompt_nomail.txt'}, 12),
        ('N5 missing per-entry farm: prompt without node_modules per ENTRY', {'QA1011R2_PROMPT': G + '/neg_prompt_nofarm.txt'}, 22),
        ('N6 head override = the round-1 head 0a1f8900c', {'QA1011R2_HEAD': '0a1f8900c7094fbdaed1099799c029e351296b39'}, 6),
        ('N7 develop = the round-2 head (audit.ts 052131de0 LANDED)', {'QA1011R2_CUR_DEV': H}, 19),
        ('N8 develop = 0f489b7da (audit.ts a blob nobody pinned)', {'QA1011R2_CUR_DEV': '0f489b7da4e699e852a126bb41a922b8ca1b4462'}, 18),
        ('N9 prompt without the round-1 report path', {'QA1011R2_PROMPT': G + '/neg_prompt_nor1report.txt'}, 24),
        ('N10 brief without CLOSED / STILL OPEN / NEW', {'QA1011R2_BRIEF': G + '/neg_brief_nodisposition.md'}, 25),
        ('N11 brief without ROUND 2', {'QA1011R2_BRIEF': G + '/neg_brief_noround2.md'}, 15)]
bad = 0
for label, env, want in rows:
    e = dict(os.environ); e.update(env)
    p = subprocess.run([L, '--check'], env=e, stdin=subprocess.DEVNULL, capture_output=True, text=True)
    print(label, '| stderr:', (p.stderr.strip().splitlines() or [''])[0][:230])
    print('rc=%d' % p.returncode)
    ok = p.returncode == want; bad += (not ok)
    print('expected %d: %s' % (want, 'OK' if ok else 'UNEXPECTED'))
print('unexpected rows', bad)
print('end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
