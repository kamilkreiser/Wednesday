#!/usr/bin/env python3
"""drafter_pins.py — #1019 ROUND 2 red-before-green, derived from round 1's GATE pins.py. (1) head: ks1187 SOLO + ks843-erasure-scope-gate SOLO (green, 70 / 10);
(2) head with routes/proxy.ts swapped to ROUND-1 bytes (8b8996f8b, blob db1534753): ks1187 SOLO (the seat's prediction 24 red / 46 green, all AssertionError);
(3) head with the ks1187 test swapped to ROUND-1 bytes (389e51e1d) over the round-2 proxy: are round 1's 39 cells still green (no cell weakened)?
restore by sha + git diff --quiet after each; (4) packages/shared whole suite at head. Failure messages classified by error type. Never rm."""
import os, sys, hashlib, subprocess, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import drafter_run as R
T = R.T; K1187 = 'src/__tests__/ks1187-erasure-door-judges-the-canonical-path.test.ts'; K843 = 'src/__tests__/ks843-erasure-scope-gate.test.ts'
def kinds(r): return dict(collections.Counter((x[3].split(':')[0][:40] if x[3] else 'no-message') for x in (r or {}).get('notpassed', [])))
def swap(rel, from_tree, label, files):
    p = T['head'] + '/' + R.GW + '/' + rel; saved = open(p, 'rb').read(); before = hashlib.sha256(saved).hexdigest()
    other = subprocess.run(['git', '-C', T[from_tree], 'show', 'HEAD:' + R.GW + '/' + rel], capture_output=True).stdout
    R.P('swap', rel, '<- blob', hashlib.sha1(b'blob %d\0' % len(other) + other).hexdigest()[:9], 'from', from_tree); open(p, 'wb').write(other)
    try:
        for f in files:
            r = R.vitest('head', [f], label + '_' + f.split('/')[-1][:10]); R.P('   error kinds', kinds(r))
    finally:
        open(p, 'wb').write(saved); R.P('restored sha identical', hashlib.sha256(open(p, 'rb').read()).hexdigest() == before)
    dq = subprocess.run(['git', '-C', T['head'], 'diff', '--quiet'], capture_output=True); R.P('git diff --quiet rc', dq.returncode); assert dq.returncode == 0
r = R.vitest('head', [K1187], 'pins_head_ks1187'); R.P('   error kinds', kinds(r))
r = R.vitest('head', [K843], 'pins_head_ks843'); R.P('   error kinds', kinds(r))
swap('src/routes/proxy.ts', 'r1', 'pins_r2test_over_R1_proxy', [K1187])
swap(K1187, 'r1', 'pins_R1test_over_r2_proxy', [K1187])
R.vitest('head', [], 'shared_head', pkg=R.SH)
