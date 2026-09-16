#!/usr/bin/env python3
"""drafter_pins.py — the ks781 body-parser line pins (packages/shared) vs api-gateway index.ts, head tree: (1) SOLO at head (pins 845/858/891 over index db127dbfa);
(2) CONTROL: head pins over BASE index.ts bytes (6f38c819e, sites at 846/859/892) -> must go red; restore by sha + git diff --quiet. c1 (973eb49ef: new index, old pins)
is the seat's own red, measured in drafter_shared.out. Never rm."""
import os, sys, hashlib, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import drafter_run as R
T = R.T; idx = T['head'] + '/Blockchain/Dev/services/api-gateway/src/index.ts'
R.vitest('head', ['src/__tests__/ks781-p3-3-body-parser-order.test.ts'], 'pins_head_solo', pkg=R.SH)
saved = open(idx, 'rb').read(); before = hashlib.sha256(saved).hexdigest()
base_idx = subprocess.run(['git', '-C', T['base'], 'show', 'HEAD:Blockchain/Dev/services/api-gateway/src/index.ts'], capture_output=True).stdout
R.P('base index.ts git blob', hashlib.sha1(b'blob %d\0' % len(base_idx) + base_idx).hexdigest()[:9]); open(idx, 'wb').write(base_idx)
R.vitest('head', ['src/__tests__/ks781-p3-3-body-parser-order.test.ts'], 'pins_head_over_base_index_CONTROL', pkg=R.SH)
open(idx, 'wb').write(saved); R.P('restored sha identical', hashlib.sha256(open(idx, 'rb').read()).hexdigest() == before)
dq = subprocess.run(['git', '-C', T['head'], 'diff', '--quiet'], capture_output=True); R.P('git diff --quiet rc', dq.returncode); assert dq.returncode == 0
