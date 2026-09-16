#!/usr/bin/env python3
"""controls_check.py — NEGATIVE (and one POSITIVE) CONTROLS for the #1012 launcher, every run with --check ONLY (never a launch), stdin /dev/null.
Test inputs are written into this gate set (neg_*); the launcher reads them through its QA1012_* overrides. rc of each run printed on its own line."""
import subprocess, os, datetime, re
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1012'
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1012-ks745-tier1'
L = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks745_1012.sh'
H = 'e225a49480e16bb77251a5d7cbd16afdf2929550'
prompt = open(B + '.prompt.txt').read(); brief = open(B + '.md').read()
def ci_count(text, s): return text.lower().count(s.lower())
print('controls_check', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
print('counts: MAIL YOUR VERDICT (ci)', ci_count(prompt, 'MAIL YOUR VERDICT'), '| head SHA in brief', brief.count(H), '| TIER 1 in brief', brief.count('TIER 1'), '| node_modules per ENTRY (ci) in prompt', ci_count(prompt, 'node_modules per ENTRY'))
assert ci_count(prompt, 'MAIL YOUR VERDICT') >= 1
open(G + '/neg_prompt_nomail.txt', 'w').write(re.sub('(?i)MAIL YOUR VERDICT', 'SEND YOUR RESULT', prompt))
assert brief.count(H) >= 1
open(G + '/neg_brief_nosha.md', 'w').write(brief.replace(H, 'HEAD-SHA-REMOVED'))
assert brief.count('TIER 1') >= 1
open(G + '/neg_brief_notier.md', 'w').write(brief.replace('TIER 1', 'TIER-ONE'))
assert ci_count(prompt, 'node_modules per ENTRY') >= 1
open(G + '/neg_prompt_nofarm.txt', 'w').write(re.sub('(?i)node_modules per ENTRY', 'node_modules as needed', prompt))
SUBJ = '[QA -> Wednesday] TIER 1 GATE #1012 (KS-745) e225a4948'
assert prompt.count(SUBJ) == 1
open(G + '/neg_prompt_nosubject.txt', 'w').write(prompt.replace(SUBJ, '[QA] verdict #1012'))
rows = [('N1 head override (#1010 head c3213b04e)', {'QA1012_HEAD': 'c3213b04e3ad96068c367f7e0ba426822d32cda9'}, 6),
        ('N2 prompt without the mail step', {'QA1012_PROMPT': G + '/neg_prompt_nomail.txt'}, 12),
        ('N3 brief without the head SHA', {'QA1012_BRIEF': G + '/neg_brief_nosha.md'}, 20),
        ('N4 brief without TIER 1', {'QA1012_BRIEF': G + '/neg_brief_notier.md'}, 7),
        ('N5 prompt without per-ENTRY farm', {'QA1012_PROMPT': G + '/neg_prompt_nofarm.txt'}, 22),
        ('N6 prompt without the exact verdict subject', {'QA1012_PROMPT': G + '/neg_prompt_nosubject.txt'}, 23),
        ('N7 develop = the #1012 head (both #1012 blobs LANDED on develop)', {'QA1012_CUR_DEV': H}, 19),
        ('N8 develop = 58f9e0571 (security index.ts blob 1bb567a09 nobody pinned, GUARDED)', {'QA1012_CUR_DEV': '58f9e0571c49a78891c8f393323f5562552b5a00'}, 18),
        ('N9 develop = the #1010 head c3213b04e (diverged from d067725ff: unjudgeable)', {'QA1012_CUR_DEV': 'c3213b04e3ad96068c367f7e0ba426822d32cda9'}, 18),
        ('P1 POSITIVE: develop = the #1011 head 0a1f8900c (audit.ts f5a83ba2c cleared by blob)', {'QA1012_CUR_DEV': '0a1f8900c7094fbdaed1099799c029e351296b39'}, 0)]
bad = 0
for label, env, want in rows:
    e = dict(os.environ); e.update(env)
    p = subprocess.run([L, '--check'], env=e, stdin=subprocess.DEVNULL, capture_output=True, text=True)
    first = (p.stderr.strip().splitlines() or [''])[0][:240] if p.returncode else [l for l in p.stdout.splitlines() if 'develop' in l][-1][:400]
    print(label, '|', 'stderr:' if p.returncode else 'stdout:', first)
    print('rc=%d' % p.returncode)
    ok = p.returncode == want; bad += 0 if ok else 1
    print('expected %d: %s' % (want, 'OK' if ok else 'UNEXPECTED'))
print('unexpected rows', bad)
print('end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
