#!/usr/bin/env python3
"""drafter_probe_outside_1031.py — proves the #1018 F-3 probe placement for an ORIGINATE (jest + ts-jest) gate, in the drafter clone only:
1. quarantine the drafter's earlier in-service probe dir (services/originate/src/qa_probe, used by drafter_probe_1031.py / drafter_tamper_1031.py) by MOVE
   outside the service root (never rm);
2. write the same probe to <tree>/Blockchain/Dev/qa_probe_1031/ with every relative module path rewritten ABSOLUTE (asserted counts), plus a scratch jest
   config there (rootDir = the originate service dir, roots/testMatch = the probe path only, the service's uuid moduleNameMapper, ts-jest with an inline
   tsconfig and diagnostics off because the probe sits outside originate's rootDir ./src);
3. run it on head and dev, compare its rows with the in-service run (out/rows_probe_<tree>.json) row by row;
4. prove it is out of both collectors: originate `jest --listTests` 0 qa_probe (control: the ks1213 test listed at head) and `tsc -p . --listFilesOnly`
   0 qa_probe (control: routes/documents.ts listed)."""
import json, subprocess, datetime, os, hashlib
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1031'
paths = json.load(open(GS + '/out/drafter_paths.json'))
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def now(): return datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')
P('drafter_probe_outside_1031', now())
src = open(GS + '/src/qa1031-drafter-probe.test.ts').read()
for name in ('head', 'dev'):
    T = paths['trees'][name]; DEV = T + '/Blockchain/Dev'; O = DEV + '/services/originate'; BIN = DEV + '/node_modules/.bin/'
    old = O + '/src/qa_probe'
    if os.path.isdir(old):
        q = paths['W'] + '/quarantine_%s_src_qa_probe_%s' % (name, datetime.datetime.now().strftime('%H%M%S')); os.rename(old, q); P(name, 'in-service probe dir MOVED outside the service root ->', q)
    t = src; n_rel = t.count("'../"); t = t.replace("'../", "'" + O + "/src/")
    assert t.count("'../") == 0 and n_rel == 18, ('relative module paths rewritten', n_rel)
    PD = DEV + '/qa_probe_1031'; os.makedirs(PD, exist_ok=True)
    open(PD + '/qa1031-drafter-probe.test.ts', 'w').write(t)
    cfg = {'rootDir': O, 'roots': [PD], 'testMatch': [PD + '/*.test.ts'], 'testEnvironment': 'node', 'moduleFileExtensions': ['ts', 'js', 'json'],
           'moduleNameMapper': {'^uuid$': O + '/src/testUtils/uuid-cjs.ts'},
           'transform': {'^.+\\.ts$': ['ts-jest', {'diagnostics': False, 'tsconfig': {'target': 'ES2022', 'module': 'commonjs', 'esModuleInterop': True, 'skipLibCheck': True, 'resolveJsonModule': True}}]}}
    open(PD + '/jest.qa1031.config.json', 'w').write(json.dumps(cfg, indent=1))
    out = GS + '/out/rows_probe_outside_%s.json' % name
    p = subprocess.run([BIN + 'jest', '--config', PD + '/jest.qa1031.config.json', '--json', '--outputFile', GS + '/out/probe_outside_jest_%s.json' % name], cwd=O, capture_output=True, text=True, env=dict(os.environ, QA1031_ROWS_OUT=out, CI='1'))
    open(GS + '/out/probe_outside_jest_%s.stderr' % name, 'w').write(p.stderr)
    try:
        j = json.load(open(GS + '/out/probe_outside_jest_%s.json' % name)); P(name, now(), 'outside-service probe: jest rc', p.returncode, 'suites', j['numTotalTestSuites'], 'tests', j['numTotalTests'], 'failed', j['numFailedTests'])
    except Exception as e:
        P(name, 'outside-service probe json unreadable', type(e).__name__, p.stderr[-1500:]); continue
    a = {(r['who'], r['id']): r for r in json.load(open(out))}; b = {(r['who'], r['id']): r for r in json.load(open(GS + '/out/rows_probe_%s.json' % name))}
    diff = [k for k in b if k not in a or {x: y for x, y in a[k].items()} != b[k]]
    P('   rows outside', len(a), 'rows in-service', len(b), 'rows differing', len(diff), diff[:4])
    lt = subprocess.run([BIN + 'jest', '--listTests'], cwd=O, capture_output=True, text=True).stdout
    lf = subprocess.run([BIN + 'tsc', '-p', '.', '--listFilesOnly'], cwd=O, capture_output=True, text=True).stdout
    P('   originate jest --listTests: files', len([l for l in lt.splitlines() if l.strip()]), 'qa_probe', lt.count('qa_probe'), '| control ks1213 test listed', 'ks1213-a-derived' in lt,
      '| tsc -p . --listFilesOnly qa_probe', lf.count('qa_probe'), '| control documents.ts listed', 'routes/documents.ts' in lf)
P('end', now())
