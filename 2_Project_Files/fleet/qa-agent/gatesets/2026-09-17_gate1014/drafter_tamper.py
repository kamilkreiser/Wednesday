#!/usr/bin/env python3
"""drafter_tamper.py — two gate-aimed tampers on the HEAD tree of the drafter clone, whole api-gateway suite each, project tsc rc per row, anchor count asserted = 1,
marker asserted, restore by `git checkout --` in the CLONE worktree with sha256 asserted equal to the pristine file. Rows:
  G-ROUTE  routes/verification.ts: the enforcement call is skipped (a literal ok result, cast to the helper's return type; first form VOID at tsc rc 2 — drafter_tamper.first-run-G-ROUTE-VOID-tsc2.out)                       — aimed at the ROUTE cells
  G-CTRL   services/enforcement.ts: the registered-catalogue 400 never fires (registered.length > 999999)     — aimed at the D 'unregistered type answers 400' CONTROL
Never rm; stderr kept."""
import subprocess, os, json, hashlib, datetime, sys
sys.argv = [sys.argv[0], 'suite']
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1014'
PATHS = json.load(open(GS + '/drafter_paths.json')); T = PATHS['trees']; W = PATHS['W']
GW = T['head'] + '/Blockchain/Dev/services/api-gateway'
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
ROWS = [
 ('G-ROUTE', 'src/routes/verification.ts', 'const enforcement = await enforceDocumentTypeRules(body, req.user);', "void enforceDocumentTypeRules; const enforcement = ({ ok: true, docType: {} }) as Awaited<ReturnType<typeof enforceDocumentTypeRules>>; /* QA-TAMPER-G-ROUTE */"),
 ('G-CTRL', 'src/services/enforcement.ts', 'if (registered.length > 0) {', 'if (registered.length > 999999) { /* QA-TAMPER-G-CTRL */'),
]
print('drafter_tamper start', ts(), flush=True)
ONLY = os.environ.get('QA_ONLY')
if ONLY: ROWS = [r for r in ROWS if r[0] == ONLY]; print('only', ONLY, len(ROWS))
for rid, rel, old, new in ROWS:
    path = GW + '/' + rel; pristine = sha(path); s = open(path).read(); n = s.count(old)
    assert n == 1, (rid, n)
    open(path, 'w').write(s.replace(old, new)); assert open(path).read().count('QA-TAMPER-' + rid) == 1 and sha(path) != pristine
    print(rid, 'landed: anchor 1, marker 1, sha', pristine[:12], '->', sha(path)[:12], flush=True)
    tsc = subprocess.run([T['head'] + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', '.'], cwd=GW, capture_output=True, text=True)
    print('   project tsc rc', tsc.returncode, (tsc.stdout + tsc.stderr).strip()[:300], flush=True)
    out = W + '/json_tamper_%s.json' % rid
    env = dict(os.environ); env.pop('NODE_ENV', None)
    p = subprocess.run([T['head'] + '/Blockchain/Dev/node_modules/.bin/vitest', 'run', '--reporter=json', '--outputFile=' + out], cwd=GW, env=env, capture_output=True, text=True)
    j = json.load(open(out))
    red = [(tr['name'].split('/src/')[-1], a['fullName'], (a.get('failureMessages') or [''])[0].split('\n')[0][:160]) for tr in j['testResults'] for a in tr['assertionResults'] if a['status'] == 'failed']
    print('   suite rc %d files %d tests %d failed %d pending %s failed_suites %s' % (p.returncode, len(j['testResults']), j['numTotalTests'], j['numFailedTests'], j.get('numPendingTests'), j.get('numFailedTestSuites')), flush=True)
    for r in red: print('     RED', r, flush=True)
    rc = subprocess.run(['git', '-C', T['head'], 'checkout', '--', 'Blockchain/Dev/services/api-gateway/' + rel], capture_output=True, text=True)
    assert rc.returncode == 0, rc.stderr
    assert sha(path) == pristine, 'restore sha mismatch'
    print('   restored sha-identical', pristine[:12], flush=True)
print('drafter_tamper end', ts())
