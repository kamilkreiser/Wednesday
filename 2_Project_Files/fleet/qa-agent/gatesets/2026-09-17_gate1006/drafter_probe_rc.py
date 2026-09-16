#!/usr/bin/env python3
"""drafter_probe_rc.py — why did the head probe exit rc 1 with 2/2 passed? Re-run it once with the DEFAULT reporter, capture stdout+stderr, print the unhandled-error lines. Quarantine by rename after."""
import sys, os, shutil, subprocess
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1006')
from drafterlib import *
REL = 'Blockchain/Dev/services/demo-service/src/__tests__/qa1006-drafter-probe.test.ts'; Q = W + '/_quarantine'
P('drafter_probe_rc start', ts()); before = porcelain('head')
dst = T['head'] + '/' + REL; shutil.copyfile(GS + '/qa1006-drafter-probe.test.ts', dst)
env = dict(os.environ); env.pop('NODE_ENV', None); env['QA_OUT'] = W + '/probe_rows_rc_rerun.json'
p = subprocess.run([T['head'] + '/Blockchain/Dev/node_modules/.bin/vitest', 'run', 'src/__tests__/qa1006-drafter-probe.test.ts'], cwd=T['head'] + '/Blockchain/Dev/services/demo-service', env=env, capture_output=True, text=True)
os.rename(dst, Q + '/qa1006-drafter-probe.head.rc-rerun.test.ts')
P('rc', p.returncode, '| porcelain restored', porcelain('head') == before)
txt = p.stdout + '\n' + p.stderr
keep = [l for l in txt.splitlines() if any(k in l for k in ('Unhandled', 'RangeError', 'ERR_', 'Error:', 'Tests ', 'Test Files', 'Errors ', 'errorHandler.ts', 'This error originated'))]
for l in keep[:40]: P('  |', l[:260])
P('drafter_probe_rc end', ts())
