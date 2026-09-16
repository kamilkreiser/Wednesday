#!/usr/bin/env python3
"""drafter_tsc.py — #1016 INCLUDING tsc (the #1011 gates' program verbatim: {"extends": "./tsconfig.json", "include": ["src/**/*"], "exclude": ["node_modules",
"dist"]}, run from services/api-gateway) on base / head of the drafter clone (merged tree = head tree while develop is 523f283c6): --listFilesOnly inclusion of enforcement.ts + the ks1176 test, error lines,
errors in the PR files, NEW vs base (line-number-free). Config written in the clone, quarantined by rename. No plant (the gate plants its own). Never rm."""
import os, re, json, subprocess, collections, datetime
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1016'
PATHS = json.load(open(GS + '/drafter_paths.json')); W = PATHS['W']; T = PATHS['trees']
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
CFG = '{"extends": "./tsconfig.json", "include": ["src/**/*"], "exclude": ["node_modules", "dist"]}'
PR = ['src/routes/verification.ts', 'src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts']
res = {}
print('drafter_tsc start', ts(), 'program', CFG, flush=True)
for t in ('base', 'head'):
    d = T[t] + '/Blockchain/Dev/services/api-gateway'; cfg = d + '/tsconfig.qa-including.json'; open(cfg, 'w').write(CFG)
    tsc = T[t] + '/Blockchain/Dev/node_modules/.bin/tsc'
    lfp = subprocess.run([tsc, '-p', 'tsconfig.qa-including.json', '--listFilesOnly'], cwd=d, capture_output=True, text=True); lf = lfp.stdout.splitlines()
    inc = {p.split('/')[-1]: any(x.endswith('/' + p) for x in lf) for p in PR}
    p = subprocess.run([tsc, '--noEmit', '-p', 'tsconfig.qa-including.json'], cwd=d, capture_output=True, text=True)
    errs = [l for l in (p.stdout + p.stderr).splitlines() if 'error TS' in l]
    byf = collections.Counter(l.split('(')[0] for l in errs)
    res[t] = errs
    print(ts(), t, '| listFiles', len(lf), 'stderr', len(lfp.stderr), '| tests-in-program', sum(1 for x in lf if '/__tests__/' in x), '| PR files included', inc, '| including rc', p.returncode, 'error lines', len(errs), 'files', len(byf), 'in PR files', sum(v for k, v in byf.items() if k in PR), flush=True)
    os.makedirs(W + '/_quarantine_2026-09-17', exist_ok=True); os.rename(cfg, W + '/_quarantine_2026-09-17/tsconfig.qa-including.%s.json' % t)
norm = lambda ls: collections.Counter(re.sub(r'\(\d+,\d+\)', '', l) for l in ls)
for t in ('head',):
    new = norm(res[t]) - norm(res['base']); gone = norm(res['base']) - norm(res[t])
    print('NEW vs base', t, sum(new.values()), list(new)[:5], '| GONE', sum(gone.values()), list(gone)[:5])
    for l in res[t]:
        if any(x in l for x in PR): print('   PR-file error line:', l)
print('drafter_tsc end', ts())
