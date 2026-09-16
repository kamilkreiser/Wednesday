#!/usr/bin/env python3
"""controls_check.py — NEGATIVE CONTROLS for the #1010 launcher, every run with --check ONLY (never a launch), stdin /dev/null. Test inputs are
written into this gate set (neg_*); the launcher reads them through its QA1010_* overrides. rc of each run printed on its own line."""
import subprocess, os, datetime, re
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1010'
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1010-ks1183-tier1'
L = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1183_1010.sh'
H = 'c3213b04e3ad96068c367f7e0ba426822d32cda9'
prompt = open(B + '.prompt.txt').read(); brief = open(B + '.md').read()
def ci_count(text, s): return text.lower().count(s.lower())
assert ci_count(prompt, 'MAIL YOUR VERDICT') == 1
open(G + '/neg_prompt_nomail.txt', 'w').write(prompt.replace('MAIL YOUR VERDICT', 'SEND YOUR RESULT'))
assert brief.count(H) >= 1
open(G + '/neg_brief_nosha.md', 'w').write(brief.replace(H, 'HEAD-SHA-REMOVED'))
assert brief.count('TIER 1') >= 1
open(G + '/neg_brief_notier.md', 'w').write(brief.replace('TIER 1', 'TIER-ONE'))
assert ci_count(prompt, 'node_modules per ENTRY') >= 1  # first run asserted == 1; the prompt says it 3 times (farm sentence + two packages)
open(G + '/neg_prompt_nofarm.txt', 'w').write(re.sub('(?i)node_modules per ENTRY', 'node_modules as needed', prompt))
SUBJ = '[QA -> Wednesday] TIER 1 GATE #1010 (KS-1183) c3213b04e'
assert prompt.count(SUBJ) == 1
open(G + '/neg_prompt_nosubject.txt', 'w').write(prompt.replace(SUBJ, '[QA] verdict #1010'))
rows = [('N1 head override (#1008 head dd7086d5a)', {'QA1010_HEAD': 'dd7086d5aa574285beffc515f9371a438621f25d'}, 6),
        ('N2 prompt without the mail step', {'QA1010_PROMPT': G + '/neg_prompt_nomail.txt'}, 12),
        ('N3 brief without the head SHA', {'QA1010_BRIEF': G + '/neg_brief_nosha.md'}, 20),
        ('N4 brief without TIER 1', {'QA1010_BRIEF': G + '/neg_brief_notier.md'}, 7),
        ('N5 prompt without per-ENTRY farm', {'QA1010_PROMPT': G + '/neg_prompt_nofarm.txt'}, 22),
        ('N6 prompt without the exact verdict subject', {'QA1010_PROMPT': G + '/neg_prompt_nosubject.txt'}, 23),
        ('N7 develop = the #1010 head (both #1010 blobs LANDED on develop)', {'QA1010_CUR_DEV': H}, 19),
        ('N8 develop = 73d3fcb90 (pre-#1008: verification.ts de34b2de7 nobody pinned)', {'QA1010_CUR_DEV': '73d3fcb902d2a78fe68a4349903ff6c6bd24d4d5'}, 18)]
print('controls_check', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
bad = 0
for label, env, want in rows:
    e = dict(os.environ); e.update(env)
    p = subprocess.run([L, '--check'], env=e, stdin=subprocess.DEVNULL, capture_output=True, text=True)
    print(label, '| stderr:', (p.stderr.strip().splitlines() or [''])[0][:200])
    print('rc=%d' % p.returncode)
    ok = p.returncode == want; bad += 0 if ok else 1
    print('expected %d: %s' % (want, 'OK' if ok else 'UNEXPECTED'))
print('unexpected rows', bad)
print('end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
