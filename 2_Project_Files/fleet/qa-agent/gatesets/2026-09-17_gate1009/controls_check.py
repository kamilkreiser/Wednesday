#!/usr/bin/env python3
"""controls_check.py — negative controls for launch_qa_secuura_ks864_1009.sh, --check ONLY: head override, prompt without MAIL, brief without the head SHA, brief without TIER 2."""
import subprocess, os, datetime
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1009'
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1009-ks864-tier2'
L = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks864_1009.sh'
brief = open(B + '.md').read(); prompt = open(B + '.prompt.txt').read()
open(GS + '/neg_prompt_nomail.txt', 'w').write(prompt.replace('MAIL YOUR VERDICT', 'REPORT YOUR VERDICT'))
open(GS + '/neg_brief_nosha.md', 'w').write(brief.replace('6ec0cb19834407887daa7bf5994f2da169abd30e', '6ec0cb198'))
open(GS + '/neg_brief_notier2.md', 'w').write(brief.replace('TIER 2', 'TIER X'))
print('controls', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
for label, env, want in (('head override', {'QA1009_HEAD': '0' * 40}, 6), ('prompt without MAIL', {'QA1009_PROMPT': GS + '/neg_prompt_nomail.txt'}, 12),
                         ('brief without head SHA', {'QA1009_BRIEF': GS + '/neg_brief_nosha.md'}, 20), ('brief without TIER 2', {'QA1009_BRIEF': GS + '/neg_brief_notier2.md'}, 7)):
    e = dict(os.environ); e.update(env)
    p = subprocess.run([L, '--check'], env=e, capture_output=True, text=True)
    print('%-24s exit %d (expected %d) %s | %s' % (label, p.returncode, want, 'OK' if p.returncode == want else 'MISMATCH', (p.stderr.strip().splitlines() or [''])[0][:120]))
