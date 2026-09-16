#!/usr/bin/env python3
"""drafter_tsc.py — #1011 ROUND 2 INCLUDING tsc (round-1 gate program verbatim: {"extends": "./tsconfig.json", "include": ["src/**/*"], "exclude":
["node_modules", "dist"]}, run from services/api-gateway) on base / head / merged of the drafter clone: --listFilesOnly inclusion of audit.ts + the
three ks871 files, error lines per file, errors in the PR files, NEW vs base. The config file is written in the clone and quarantined by rename. No plant
(the gate plants its own control). Never rm."""
import sys, os, re, json, subprocess, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drafterlib import *
CFG = '{"extends": "./tsconfig.json", "include": ["src/**/*"], "exclude": ["node_modules", "dist"]}'
PR = ['src/middleware/audit.ts', 'src/__tests__/ks871-audit-path-captured-at-entry.test.ts', 'src/__tests__/ks871-the-audit-log-records-req-path.test.ts', 'src/__tests__/ks871-real-app-canonical-audit-rows.test.ts']
res = {}
P('drafter_tsc start', ts(), 'program', CFG)
for t in ('base', 'head', 'merged'):
    d = T[t] + '/' + PKG['gw']; cfg = d + '/tsconfig.qa-including.json'; open(cfg, 'w').write(CFG)
    tsc = T[t] + '/Blockchain/Dev/node_modules/.bin/tsc'
    lf = subprocess.run([tsc, '-p', 'tsconfig.qa-including.json', '--listFilesOnly'], cwd=d, capture_output=True, text=True).stdout.splitlines()
    inc = {p: any(x.endswith('/' + p) for x in lf) for p in PR}
    p = subprocess.run([tsc, '--noEmit', '-p', 'tsconfig.qa-including.json'], cwd=d, capture_output=True, text=True)
    errs = [l for l in (p.stdout + p.stderr).splitlines() if 'error TS' in l]
    byf = collections.Counter(l.split('(')[0] for l in errs)
    proj = subprocess.run([tsc, '--noEmit', '-p', '.'], cwd=d, capture_output=True, text=True).returncode
    res[t] = errs
    P(ts(), t, '| listFiles', len(lf), 'tests-in-program', sum(1 for x in lf if '/__tests__/' in x), '| PR files included', inc, '| including rc', p.returncode, 'error lines', len(errs), 'files', len(byf), 'in PR files', sum(v for k, v in byf.items() if k in PR), '| project tsc -p . rc', proj)
    os.makedirs(W + '/_quarantine', exist_ok=True); os.rename(cfg, W + '/_quarantine/tsconfig.qa-including.%s.json' % t)
norm = lambda ls: collections.Counter(re.sub(r'\(\d+,\d+\)', '', l) for l in ls)
for t in ('head', 'merged'):
    new = norm(res[t]) - norm(res['base']); gone = norm(res['base']) - norm(res[t])
    P('NEW vs base', t, sum(new.values()), list(new)[:5], '| GONE', sum(gone.values()), list(gone)[:5])
P('drafter_tsc end', ts())
