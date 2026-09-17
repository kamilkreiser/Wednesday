#!/usr/bin/env python3
"""drafter_probe_r2.py (ROUND 2 re-pin: r2 clone paths, outputs under out/r2/) — ORIGINAL: drafter_probe.py — places src/qa1026-drafter-authorize.probe.ts at services/auth/src/qa_probe/ in the head and dev drafter worktrees, writes
services/auth/vitest.qa1026.config.mts (merges the real vitest.config.ts; include = src/qa_probe/**/*.probe.ts only), runs it per tree with cwd inside the
clone, QA_OUT = out/rows_probe_<tree>.json. lsof TCP LISTEN census before/after. Never rm; nothing in the Secuura checkout."""
import json, os, shutil, subprocess, datetime, hashlib
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1026'
paths = json.load(open(GS + '/out/r2/drafter_paths.json'))
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def census(tag):
    p = subprocess.run(['lsof', '-nP', '-iTCP', '-sTCP:LISTEN'], capture_output=True, text=True)
    rows = [l for l in p.stdout.splitlines()[1:]]
    ps = subprocess.run(['ps', '-axo', 'pid=,command='], capture_output=True, text=True).stdout.splitlines()
    stubs = [l for l in ps if 'login_stub.mjs' in l and 'grep' not in l]
    mine = [l for l in ps if paths['W'] in l]
    P('census', tag, now(), '| LISTEN rows', len(rows), '| login_stub.mjs procs', len(stubs), '| procs with argv in drafter scratch', len(mine), '| ps rows parsed', len(ps))
CFG = """import { defineConfig, mergeConfig } from 'vitest/config';
import base from './vitest.config';
export default mergeConfig(base, defineConfig({ test: { include: ['src/qa_probe/**/*.probe.ts'] } }));
"""
census('START')
import sys
PROBE = sys.argv[1] if len(sys.argv) > 1 else 'qa1026-drafter-authorize'
src = GS + '/src/' + PROBE + '.probe.ts'; P('probe sha256', hashlib.sha256(open(src, 'rb').read()).hexdigest()[:16])
for name in ('head', 'dev'):
    a = paths['trees'][name] + '/Blockchain/Dev/services/auth'
    os.makedirs(a + '/src/qa_probe', exist_ok=True)
    shutil.copyfile(src, a + '/src/qa_probe/' + PROBE + '.probe.ts')
    open(a + '/vitest.qa1026.config.mts', 'w').write(CFG)
    out = GS + '/out/r2/rows_' + PROBE + '_%s.json' % name
    t0 = now()
    p = subprocess.run([paths['trees'][name] + '/Blockchain/Dev/node_modules/.bin/vitest', 'run', '--config', 'vitest.qa1026.config.mts', 'src/qa_probe/' + PROBE + '.probe.ts', '--reporter', 'verbose'], cwd=a, capture_output=True, text=True, env=dict(os.environ, QA_OUT=out, CI='1'))
    open(GS + '/out/r2/' + PROBE + '_%s.vitest.log' % name, 'w').write(p.stdout + '\n--- stderr ---\n' + p.stderr)
    P(name, t0, '->', now(), 'vitest rc', p.returncode, '| tail', (p.stdout + p.stderr).strip().splitlines()[-6:])
census('CLOSE')
