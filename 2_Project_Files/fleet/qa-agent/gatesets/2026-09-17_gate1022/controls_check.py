#!/usr/bin/env python3
"""controls_check.py — negative controls for launch_qa_secuura_ks1211_1022.sh, `--check` ONLY (never a launch). Each plants one defect via the
launcher's QA1022_* test overrides into a copy under GS/ and asserts the expected exit code."""
import os, subprocess, datetime
Q = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent'; GS = Q + '/gatesets/2026-09-17_gate1022'
L = Q + '/launchers/launch_qa_secuura_ks1211_1022.sh'
B = open(Q + '/briefs/2026-09-17_secuura-1022-ks1211-hono-tier1.md').read(); P = open(Q + '/briefs/2026-09-17_secuura-1022-ks1211-hono-tier1.prompt.txt').read()
H = 'ff49d0242a8ae764155d427232b15647c6bfa849'   # re-pinned
def w(name, text): open(GS + '/' + name, 'w').write(text); return GS + '/' + name
nb_sha = w('neg_brief_nosha.md', B.replace(H, H[:9])); assert H not in open(nb_sha).read()
nb_tier = w('neg_brief_notier1.md', B.replace('TIER 1', 'TIER 2')); assert 'TIER 1' not in open(nb_tier).read()
np_mail = w('neg_prompt_nomail.txt', P.replace('MAIL YOUR VERDICT', 'SEND YOUR VERDICT')); assert 'MAIL YOUR VERDICT' not in open(np_mail).read().upper()
np_push = w('neg_prompt_nopushban.txt', P.replace('NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout', 'Avoid pushing'))
np_round = w('neg_prompt_noround1.txt', P.replace('ROUND 1', 'ROUND 2')); assert 'ROUND 1' not in open(np_round).read()
cases = [('head override', {'QA1022_HEAD': '0' * 40}, 6), ('OLD head 58684e653 override', {'QA1022_HEAD': '58684e6534b4d420c9fb9ea246d3a32c70c70828'}, 6), ('brief without full SHA', {'QA1022_BRIEF': nb_sha}, 20),
         ('brief without TIER 1', {'QA1022_BRIEF': nb_tier}, 7), ('prompt without MAIL', {'QA1022_PROMPT': np_mail}, 12),
         ('prompt without push/preflight ban', {'QA1022_PROMPT': np_push}, 11), ('prompt without ROUND 1', {'QA1022_PROMPT': np_round}, 15)]
ok = True
for name, env, want in cases:
    p = subprocess.run([L, '--check'], env=dict(os.environ, **env), capture_output=True, text=True, timeout=180)
    good = p.returncode == want; ok &= good
    print('%s %-36s rc %d expected %d %s | %s' % (datetime.datetime.now().astimezone().strftime('%H:%M:%S'), name, p.returncode, want, 'OK' if good else 'MISMATCH', (p.stderr.strip().splitlines() or [''])[0][:150]))
print('ALL CONTROLS', 'PASS' if ok else 'FAIL')
