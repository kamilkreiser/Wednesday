#!/usr/bin/env python3
"""drafter_nodetect_probe.py — Q4 (is the security.ts detector ordering load-bearing for the door?): on the HEAD tree, neuter the `../` suspicious pattern in
config/services.ts (anchor count 1, marker), run round 1's GATE harness prod + test stages (label nodetect_head), restore by bytes (sha) + git diff --quiet, then
compare against the untampered head rows: every changed row, and every no-scope door / W / undetermined row's status and hits under the tamper."""
import hashlib, json, os, subprocess, sys, collections, datetime
GSD = os.path.dirname(os.path.abspath(__file__))
PA = json.load(open(GSD + '/drafter_paths.json')); WT = PA['trees']['head']
SV = WT + '/Blockchain/Dev/services/api-gateway/src/config/services.ts'
A = '    /(\\.\\.\\/)/, // Path traversal\n'; B = '    /(\\.\\.\\/)(?!)/, // Path traversal (QA tamper: never matches)\n'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
print('nodetect probe', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
orig = open(SV, 'rb').read(); o = sha(SV); s = orig.decode(); assert s.count(A) == 1, s.count(A)
open(SV, 'wb').write(s.replace(A, B).encode()); print('tamper applied, marker', sha(SV) != o)
try:
    env = dict(os.environ); env['QA_STAGES'] = 'test,prod'; env['QA_LABEL'] = 'nodetect'
    p = subprocess.run(['python3', GSD + '/drafter_run.py', 'probe', 'head'], env=env, capture_output=True, text=True); print(p.stdout[-1500:], p.stderr[-800:])
finally:
    open(SV, 'wb').write(orig); print('restored sha equal', sha(SV) == o, '| git diff --quiet', subprocess.run(['git', '-C', WT, 'diff', '--quiet', 'HEAD']).returncode == 0)
t = json.load(open(GSD + '/rows/rows_nodetect.json')); h = json.load(open(GSD + '/rows/rows_head_head.json'))
for st in ('test', 'prod'):
    a = h[st]; b = t[st]; assert len(a) == len(b), (st, len(a), len(b))
    ch = [(x['id'], x['tok'], x.get('rep'), (x['status'], x['code'], len(x['hits'])), (y['status'], y['code'], len(y['hits']))) for x, y in zip(a, b) if (x['status'], x['code'], x['hits']) != (y['status'], y['code'], y['hits'])]
    print('==', st, 'rows', len(a), '| rows changed by neutering the detector:', len(ch))
    for c in ch: print('   ', c)
    bad = [(y['id'], y['tok'], y['status'], y['code'], y['hits']) for y in b if y['cls'] in ('door', 'W', 'undetermined') and y['tok'] in ('noscope', 'user', 'noemail_noscope', 'none') and (y['hits'] or y['status'] not in (400, 401, 403, 405))]
    print('   no-scope door/W/undetermined rows answering other than 400/401/403/405 or with >=1 hit under the tamper:', len(bad), bad[:10])
