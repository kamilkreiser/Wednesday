#!/usr/bin/env python3
"""controls_check_r2.py (ROUND 2 re-pin; fixtures under out/r2/fixtures) — ORIGINAL: controls_check.py — proves the #1026 launcher guards FIRE: every run is `--check` with stdin /dev/null (never a launch); fixtures are copies under out/fixtures."""
import os, subprocess, datetime
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1026'; FX = GS + '/out/r2/fixtures'; os.makedirs(FX, exist_ok=True)
L = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks839_1026.sh'
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1026-ks839-tier1-r2'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'; F = 'Blockchain/Dev/services/auth/src/services/oauth.ts'
def show(ref): return subprocess.run(['git', '-C', REPO, 'show', ref + ':' + F], capture_output=True).stdout
open(FX + '/oauth.develop.ts', 'wb').write(show('19f1e54750ce2b65312a687add2db4f5628edb7d'))
open(FX + '/oauth.round1.ts', 'wb').write(show('8ab493354bbdb3fa52d2eb14654492db1a891e4a'))
open(FX + '/oauth.head.ts', 'wb').write(show('df97c0def4b3f1be3db0172e3f0e464b53fc1d42'))
open(FX + '/oauth.other.ts', 'wb').write(show('19f1e54750ce2b65312a687add2db4f5628edb7d') + b'\n// qa1026 control: a develop edit nobody pinned\n')
def strip(src, needle, name, repl=''):
    s = open(src, encoding='utf-8').read(); assert s.count(needle) >= 1, (name, needle); p = FX + '/' + name; open(p, 'w', encoding='utf-8').write(s.replace(needle, repl)); return p
cases = [
 ('real --check', {}, 0),
 ('head override', {'QA1026_HEAD': '0' * 40}, 6),
 ('fixture: develop oauth.ts bytes', {'QA1026_OAUTH_FILE': FX + '/oauth.develop.ts'}, 0),
 ('fixture: #1026 ROUND 2 head oauth.ts bytes', {'QA1026_OAUTH_FILE': FX + '/oauth.head.ts'}, 19),
 ('fixture: #1026 ROUND 1 head oauth.ts bytes', {'QA1026_OAUTH_FILE': FX + '/oauth.round1.ts'}, 19),
 ('fixture: oauth.ts edited, unpinned', {'QA1026_OAUTH_FILE': FX + '/oauth.other.ts'}, 18),
 ('develop override = #1026 ROUND 2 head itself (landed)', {'QA1026_CUR_DEV': 'df97c0def4b3f1be3db0172e3f0e464b53fc1d42'}, 19),
 ('brief without TIER 1', {'QA1026_BRIEF': strip(B + '.md', 'TIER 1', 'brief_no_tier.md', 'TIER ONE')}, 7),
 ('prompt without ROUND 1', {'QA1026_PROMPT': strip(B + '.prompt.txt', 'ROUND 2', 'prompt_no_round.txt', 'ROUND TWO')}, 15),
 ('prompt without node_modules per ENTRY', {'QA1026_PROMPT': strip(B + '.prompt.txt', 'node_modules per ENTRY', 'prompt_no_farm.txt', 'node_modules wholesale')}, 22),
 ('prompt without the exact subject', {'QA1026_PROMPT': strip(B + '.prompt.txt', '[QA -> Wednesday] TIER 1 GATE #1026 ROUND 2 (KS-839) df97c0def', 'prompt_no_subject.txt', '[QA -> Wednesday] GATE #1026')}, 23),
 ('prompt without NOT-TESTED.written-first.md', {'QA1026_PROMPT': strip(B + '.prompt.txt', 'NOT-TESTED.written-first.md', 'prompt_no_nt.txt', 'NOT-TESTED.md')}, 24),
 ('prompt without MERGE ADDENDUM', {'QA1026_PROMPT': strip(B + '.prompt.txt', 'MERGE ADDENDUM', 'prompt_no_addendum.txt', 'MERGE NOTE')}, 25),
]
print('controls_check', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
fired = 0
for name, env, want in cases:
    p = subprocess.run([L, '--check'], stdin=subprocess.DEVNULL, capture_output=True, text=True, env=dict(os.environ, **env))
    ok = p.returncode == want; fired += ok
    last = (p.stderr.strip().splitlines() or p.stdout.strip().splitlines() or [''])[-1][:170]
    print('%-62s exit %2d want %2d %s | %s' % (name, p.returncode, want, 'OK' if ok else 'MISMATCH', last))
print('controls matching: %d / %d' % (fired, len(cases)), datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
