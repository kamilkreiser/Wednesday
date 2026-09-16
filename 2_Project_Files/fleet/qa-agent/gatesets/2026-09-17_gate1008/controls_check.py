#!/usr/bin/env python3
"""controls_check.py — NEGATIVE CONTROLS for the #1008 launcher, every run with --check ONLY (never a launch). Test inputs are written
into this gate set (neg_*); the launcher reads them through its QA1008_* overrides. rc of each run printed on its own line."""
import subprocess, os, datetime
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1008'
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1008-ks1087-tier1'
L = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1087_1008.sh'
H = 'dd7086d5aa574285beffc515f9371a438621f25d'
prompt = open(B + '.prompt.txt').read(); brief = open(B + '.md').read()
assert prompt.count('MAIL YOUR VERDICT') == 1
open(G + '/neg_prompt_nomail.txt', 'w').write(prompt.replace('MAIL YOUR VERDICT', 'SEND YOUR RESULT'))
assert brief.count(H) >= 1
open(G + '/neg_brief_nosha.md', 'w').write(brief.replace(H, 'HEAD-SHA-REMOVED'))
rows = [('N1 head override (#1006 head)', {'QA1008_HEAD': '86fe59e6bf07108142fb3dbd06bef8747d2a4687'}, 6),
        ('N2 prompt without the mail step', {'QA1008_PROMPT': G + '/neg_prompt_nomail.txt'}, 12),
        ('N3 brief without the head SHA', {'QA1008_BRIEF': G + '/neg_brief_nosha.md'}, 20)]
print('controls_check', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
for label, env, want in rows:
    e = dict(os.environ); e.update(env)
    p = subprocess.run([L, '--check'], env=e, stdin=subprocess.DEVNULL, capture_output=True, text=True)
    print(label, '| stderr:', (p.stderr.strip().splitlines() or [''])[0][:160])
    print('rc=%d' % p.returncode)
    print('expected %d: %s' % (want, 'OK' if p.returncode == want else 'UNEXPECTED'))
print('end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
