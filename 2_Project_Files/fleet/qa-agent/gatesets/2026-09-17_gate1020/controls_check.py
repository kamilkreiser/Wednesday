#!/usr/bin/env python3
"""controls_check.py — negative controls for launch_qa_secuura_ks769_1020.sh, --check ONLY: head override, prompt without MAIL, brief without the
head SHA, brief without TIER 2, prompt without the preflight prohibition. Negative copies are written into this gateset folder, never over the real files."""
import subprocess, os, datetime
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1020'
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1020-ks769-tier2'
L = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks769_1020.sh'
H = '71bd80a35b406b9c99c7b96955a7521032d33c20'
brief = open(B + '.md').read(); prompt = open(B + '.prompt.txt').read()
assert prompt.count('MAIL YOUR VERDICT') == 1 and brief.count(H) >= 1 and brief.count('TIER 2') >= 1
assert prompt.count('NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout') == 1
open(GS + '/neg_prompt_nomail.txt', 'w').write(prompt.replace('MAIL YOUR VERDICT', 'REPORT YOUR VERDICT'))
open(GS + '/neg_brief_nosha.md', 'w').write(brief.replace(H, '71bd80a35'))
open(GS + '/neg_brief_notier2.md', 'w').write(brief.replace('TIER 2', 'TIER X'))
open(GS + '/neg_prompt_nopushban.txt', 'w').write(prompt.replace('NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout', 'Avoid pushing from the Secuura checkout'))
print('controls', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
for label, env, want in (('head override', {'QA1020_HEAD': '0' * 40}, 6),
                         ('prompt without MAIL', {'QA1020_PROMPT': GS + '/neg_prompt_nomail.txt'}, 12),
                         ('brief without head SHA', {'QA1020_BRIEF': GS + '/neg_brief_nosha.md'}, 20),
                         ('brief without TIER 2', {'QA1020_BRIEF': GS + '/neg_brief_notier2.md'}, 7),
                         ('prompt without push ban', {'QA1020_PROMPT': GS + '/neg_prompt_nopushban.txt'}, 11)):
    e = dict(os.environ); e.update(env)
    p = subprocess.run([L, '--check'], env=e, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    print('%-24s exit %d (expected %d) %s | %s' % (label, p.returncode, want, 'OK' if p.returncode == want else 'MISMATCH', (p.stderr.strip().splitlines() or [''])[0][:120]))
