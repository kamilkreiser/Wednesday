#!/usr/bin/env python3
"""controls_check.py — NEGATIVE CONTROLS for the #1015 launcher, every run with --check ONLY (never a launch), stdin /dev/null. Test inputs are
written into this gate set (neg_*); the launcher reads them through its QA1015_* overrides. rc of each run printed on its own line."""
import subprocess, os, datetime, re
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1015'
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1015-ks1018-tier1'
L = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1018_1015.sh'
H = '77145ce84353534ba381688d5bbd16ff9ff27aef'
prompt = open(B + '.prompt.txt').read(); brief = open(B + '.md').read()
def ci_count(text, s): return text.lower().count(s.lower())
print('controls_check', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
print('counts: MAIL YOUR VERDICT', ci_count(prompt, 'MAIL YOUR VERDICT'), '| head SHA in brief', brief.count(H), '| TIER 1 in brief', brief.count('TIER 1'), '| node_modules per ENTRY in prompt', ci_count(prompt, 'node_modules per ENTRY'))
assert ci_count(prompt, 'MAIL YOUR VERDICT') >= 1
open(G + '/neg_prompt_nomail.txt', 'w').write(re.sub('(?i)MAIL YOUR VERDICT', 'SEND YOUR RESULT', prompt))
assert brief.count(H) >= 1
open(G + '/neg_brief_nosha.md', 'w').write(brief.replace(H, 'HEAD-SHA-REMOVED'))
assert brief.count('TIER 1') >= 1
open(G + '/neg_brief_notier.md', 'w').write(brief.replace('TIER 1', 'TIER-ONE'))
assert ci_count(prompt, 'node_modules per ENTRY') >= 1
open(G + '/neg_prompt_nofarm.txt', 'w').write(re.sub('(?i)node_modules per ENTRY', 'node_modules as needed', prompt))
SUBJ = '[QA -> Wednesday] TIER 1 GATE #1015 (KS-1018) 77145ce84'
assert prompt.count(SUBJ) == 1, prompt.count(SUBJ)
open(G + '/neg_prompt_nosubject.txt', 'w').write(prompt.replace(SUBJ, '[QA] verdict #1015'))
rows = [('N1 head override (#1013 head 5fbfb66a9)', {'QA1015_HEAD': '5fbfb66a927ea50a8ad0531f344b58a33f7bd9c2'}, 6),
        ('N2 prompt without the mail step', {'QA1015_PROMPT': G + '/neg_prompt_nomail.txt'}, 12),
        ('N3 brief without the head SHA', {'QA1015_BRIEF': G + '/neg_brief_nosha.md'}, 20),
        ('N4 brief without TIER 1', {'QA1015_BRIEF': G + '/neg_brief_notier.md'}, 7),
        ('N5 prompt without per-ENTRY farm', {'QA1015_PROMPT': G + '/neg_prompt_nofarm.txt'}, 22),
        ('N6 prompt without the exact verdict subject', {'QA1015_PROMPT': G + '/neg_prompt_nosubject.txt'}, 23),
        ('N7 develop = the #1015 head (users.ts 8ef9065e2 LANDED on develop)', {'QA1015_CUR_DEV': H}, 19),
        ('N8 develop = commit-1 6e30fe9f5 (users.ts LANDED — the commit-1 test blob is judged LANDED too)', {'QA1015_CUR_DEV': '6e30fe9f5ea3abd8414bfe69db2356d31c2da4d6'}, 19),
        ('N9 develop = 1125607e9 (pre-#1013: userRepo.ts blob 822b3fcd8 nobody pinned -> GUARDED, the blob arm)', {'QA1015_CUR_DEV': '1125607e978d6ad637720c985e43e3d79fecdf88'}, 18)]
bad = 0
for label, env, want in rows:
    e = dict(os.environ); e.update(env)
    p = subprocess.run([L, '--check'], env=e, stdin=subprocess.DEVNULL, capture_output=True, text=True)
    print(label, '| stderr:', (p.stderr.strip().splitlines() or [''])[0][:260])
    print('rc=%d' % p.returncode)
    ok = p.returncode == want; bad += 0 if ok else 1
    print('expected %d: %s' % (want, 'OK' if ok else 'UNEXPECTED'))
print('unexpected rows', bad)
print('end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
