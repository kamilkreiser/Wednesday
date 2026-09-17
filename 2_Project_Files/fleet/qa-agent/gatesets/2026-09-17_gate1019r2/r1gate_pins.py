#!/usr/bin/env python3
"""drafter_pins.py — red-before-green and the ks843 source-pin change (brief item 7). (1) head: ks1187 SOLO + ks843-erasure-scope-gate SOLO (green controls);
(2) head with routes/proxy.ts swapped to BASE bytes (b99f45a4c): ks1187 SOLO (the seat's 39 run / 7 green / 13 AssertionError / 19 TypeError) and
ks843-erasure-scope-gate SOLO (the new pin over the old door); restore by sha + git diff --quiet; (3) c1 (50a4b749a: new proxy.ts, OLD ks843 pin a3c554121):
ks843-erasure-scope-gate SOLO = the seat's first-run T0 red. Failure messages classified by error type. Never rm."""
import os, sys, hashlib, subprocess, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import run as R  # QA gate copy of drafter_pins.py, bound to THIS gate clone
T = R.T; K1187 = 'src/__tests__/ks1187-erasure-door-judges-the-canonical-path.test.ts'; K843 = 'src/__tests__/ks843-erasure-scope-gate.test.ts'
def kinds(r):
    return dict(collections.Counter((x[3].split(':')[0][:40] if x[3] else 'no-message') for x in (r or {}).get('notpassed', [])))
r = R.vitest('head', [K1187], 'pins_head_ks1187'); R.P('   error kinds', kinds(r))
r = R.vitest('head', [K843], 'pins_head_ks843'); R.P('   error kinds', kinds(r))
px = T['head'] + '/' + R.GW + '/src/routes/proxy.ts'; saved = open(px, 'rb').read(); before = hashlib.sha256(saved).hexdigest()
base_px = subprocess.run(['git', '-C', T['base'], 'show', 'HEAD:' + R.GW + '/src/routes/proxy.ts'], capture_output=True).stdout
R.P('base proxy.ts git blob', hashlib.sha1(b'blob %d\0' % len(base_px) + base_px).hexdigest()[:9]); open(px, 'wb').write(base_px)
try:
    r = R.vitest('head', [K1187], 'pins_ks1187_over_BASE_proxy'); R.P('   error kinds', kinds(r))
    r = R.vitest('head', [K843], 'pins_ks843_new_pin_over_BASE_proxy'); R.P('   error kinds', kinds(r))
finally:
    open(px, 'wb').write(saved); R.P('restored sha identical', hashlib.sha256(open(px, 'rb').read()).hexdigest() == before)
dq = subprocess.run(['git', '-C', T['head'], 'diff', '--quiet'], capture_output=True); R.P('git diff --quiet rc', dq.returncode); assert dq.returncode == 0
R.P('restored blob == HEAD blob', subprocess.run(['git', 'hash-object', px], capture_output=True, text=True).stdout.strip() == subprocess.run(['git', '-C', T['head'], 'rev-parse', 'HEAD:' + R.GW + '/src/routes/proxy.ts'], capture_output=True, text=True).stdout.strip())
r = R.vitest('c1', [K843], 'pins_c1_OLD_ks843_pin_over_NEW_proxy'); R.P('   error kinds', kinds(r))
r = R.vitest('base', [K843], 'pins_base_OLD_ks843_pin_over_OLD_proxy'); R.P('   error kinds', kinds(r))
