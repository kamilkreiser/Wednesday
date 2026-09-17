#!/usr/bin/env python3
"""make_fixtures_1035.py — fixtures for check_launcher_1035.sh (derived from the real brief / prompt / repo blobs by asserted substitutions). Writes GS/fixtures/."""
import os, subprocess, hashlib
GS = os.path.dirname(os.path.abspath(__file__)); F = GS + '/fixtures'; os.makedirs(F, exist_ok=True)
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'; B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1035-ks1204-tier1'
VER = 'Blockchain/Dev/services/api-gateway/src/routes/verification.ts'
def blob(b): return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()
def show(x): return subprocess.run(['git', '-C', REPO, 'show', x], capture_output=True).stdout
dev = show('3961c2add:' + VER); head = show('4b1fb0621:' + VER)
for name, data, want in (('pos_ver_develop_28fb58343.ts', dev, '28fb58343'), ('pos_ver_landed_f888e8cd0.ts', head, 'f888e8cd0'), ('neg_ver_unpinned_edit.ts', dev + b'// qa1035 fixture: one unpinned line\n', None)):
    open(F + '/' + name, 'wb').write(data); b = blob(data); print(name, b[:9], 'expected' if (want is None or b.startswith(want)) else 'MISMATCH', want)
    assert want is None or b.startswith(want)
pr = open(B + '.prompt.txt').read(); br = open(B + '.md').read()
def neg(src, name, old, new, n=None):
    c = src.count(old); assert c >= 1 and (n is None or c == n), (name, c)
    out = src.replace(old, new); open(F + '/' + name, 'w').write(out); print(name, 'replaced', c, '| residual', out.count(old))
neg(pr, 'neg_prompt_nosubject.txt', '[QA -> Wednesday] TIER 1 GATE #1035 (KS-1204) 4b1fb0621', '[QA -> Wednesday] TIER 1 GATE #1035 (KS-1204) <sha>', 1)
neg(pr, 'neg_prompt_nofarm.txt', 'node_modules per ENTRY', 'node_modules as available')
neg(pr, 'neg_prompt_noprior.txt', '2026-09-17-ks1176-1014r2-9ba0caf78-tier1-r2/', '<prior>/')
neg(pr, 'neg_prompt_nottestedfirst.txt', 'NOT-TESTED.written-first.md', 'NOT-TESTED.md')
neg(pr, 'neg_prompt_nocsn.txt', 'CLOSED / STILL OPEN / NEW', 'dispositions')
neg(br, 'neg_brief_noaddendum.md', 'MERGE ADDENDUM', 'MERGE NOTE')
neg(br, 'neg_brief_nosha.md', '4b1fb0621e58ff00bba096751130bc6e53df4714', '4b1fb0621')
neg(br, 'neg_brief_round2.md', 'ROUND 1', 'ROUND 2')
neg(br, 'neg_brief_tier2.md', 'TIER 1', 'TIER 2')
