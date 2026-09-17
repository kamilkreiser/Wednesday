#!/usr/bin/env python3
"""drafter_tamper_r2.py — #1026 ROUND 2 (KS-839) re-pin of drafter_tamper.py (r2 clone, head df97c0def, develop 19f1e5475; the seat's 10 rows + drafter rows; a second-regex runtime arm; a second test-including tsconfig shape). ORIGINAL DOC: #1026 (KS-839) drafter: suites (develop + head), project tsc, the test-including tsc program (--listFilesOnly + plant), eslint by rule
and message with a firing control, then the tamper table at head on the WHOLE services/auth suite (vitest json, absolute output path), tsc -p rc per row,
sha-restored + git diff --quiet per row, and the red-proof (oauth.ts = develop bytes). Every edit asserts its anchor count = 1. Probe files quarantined by
rename first. Never rm. cwd inside the drafter clone only."""
import hashlib, json, os, subprocess, datetime, sys
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1026'
paths = json.load(open(GS + '/out/r2/drafter_paths.json'))
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S')
SVC = 'src/services/oauth.ts'; TEST = 'src/__tests__/ks839-a-wildcard-allow-list-grants-nothing.test.ts'
def A(tree): return paths['trees'][tree] + '/Blockchain/Dev/services/auth'
def BIN(tree, b): return paths['trees'][tree] + '/Blockchain/Dev/node_modules/.bin/' + b
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def quarantine(tree):
    q = A(tree) + '/src/qa_probe'
    if os.path.isdir(q):
        for f in sorted(os.listdir(q)):
            if f.endswith('.probe.ts'): os.rename(q + '/' + f, q + '/' + f + '.quarantined'); P('  quarantined', tree, f)
def suite(tree, tag):
    out = GS + '/out/r2/suite_%s_%s.json' % (tree, tag)
    p = subprocess.run([BIN(tree, 'vitest'), 'run', '--reporter=json', '--outputFile=' + out], cwd=A(tree), capture_output=True, text=True, env=dict(os.environ, CI='1'))
    try:
        j = json.load(open(out))
    except Exception as e:
        return dict(rc=p.returncode, err=type(e).__name__, tail=(p.stdout + p.stderr)[-800:])
    failed = []
    for f in j['testResults']:
        for t in f['assertionResults']:
            if t['status'] == 'failed': failed.append((f['name'].split('/src/')[-1], t['title'][:70], (t.get('failureMessages') or [''])[0].split('\n')[0][:140]))
    loadfail = [f['name'].split('/src/')[-1] for f in j['testResults'] if f['status'] == 'failed' and not f['assertionResults']]
    return dict(rc=p.returncode, files=j['numTotalTestSuites'], tests=j['numTotalTests'], failed=j['numFailedTests'], pending=j['numPendingTests'] + j.get('numTodoTests', 0), loadfail=loadfail, failed_cells=failed)
def tsc(tree, extra=None):
    p = subprocess.run([BIN(tree, 'tsc'), '--noEmit'] + (extra or ['-p', '.']), cwd=A(tree), capture_output=True, text=True)
    return p.returncode, [l for l in (p.stdout + p.stderr).splitlines() if 'error TS' in l]
P('drafter_tamper start', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
for t in ('head', 'dev'): quarantine(t)
# ---- suites + project tsc ----
for t in ('dev', 'head'):
    t0 = now(); s = suite(t, 'T0'); rc, errs = tsc(t)
    P('SUITE', t, t0, '->', now(), {k: v for k, v in s.items() if k != 'failed_cells'}, 'failed_cells', s.get('failed_cells'), '| tsc -p rc', rc, 'errors', len(errs))
# ---- test-including tsc program ----
CFG = '{\n  "extends": "./tsconfig.json",\n  "compilerOptions": { "noEmit": true, "rootDir": "." },\n  "include": ["src/**/*"],\n  "exclude": ["node_modules", "dist"]\n}\n'
CFGB = '{\n  "extends": "./tsconfig.json",\n  "include": ["src/**/*"],\n  "exclude": []\n}\n'
for t in ('head', 'dev'):
    open(A(t) + '/tsconfig.qa1026b-seatshape.json', 'w').write(CFGB)
    rcb, errsb = tsc(t, ['-p', 'tsconfig.qa1026b-seatshape.json'])
    P('TSC-WITH-TESTS seat-shape (extends, include src, exclude [], NO rootDir override)', t, now(), 'rc', rcb, 'error lines', len(errsb), '| in ks839 test', sum('ks839-' in e for e in errsb), '| in oauth.ts', sum('services/oauth.ts' in e for e in errsb), '| rootDir TS6059 lines', sum('TS6059' in e for e in errsb))
for t in ('head', 'dev'):
    open(A(t) + '/tsconfig.qa1026-with-tests.json', 'w').write(CFG)
    p = subprocess.run([BIN(t, 'tsc'), '-p', 'tsconfig.qa1026-with-tests.json', '--listFilesOnly'], cwd=A(t), capture_output=True, text=True); lf = p.stdout.splitlines()
    q = subprocess.run([BIN(t, 'tsc'), '-p', 'tsconfig.json', '--listFilesOnly'], cwd=A(t), capture_output=True, text=True); lq = q.stdout.splitlines()
    rc, errs = tsc(t, ['-p', 'tsconfig.qa1026-with-tests.json'])
    P('TSC-WITH-TESTS', t, now(), 'rc', rc, 'error lines', len(errs), '| in ks839 test', sum('ks839-' in e for e in (errs if t == 'head' else [])), '| in oauth.ts', sum('services/oauth.ts' in e for e in errs), '| ks839 test in program:', any(x.endswith('ks839-a-wildcard-allow-list-grants-nothing.test.ts') for x in lf), '| in project program:', any(x.endswith('ks839-a-wildcard-allow-list-grants-nothing.test.ts') for x in lq), '| __tests__ files', sum('/src/__tests__/' in x for x in lf), 'vs', sum('/src/__tests__/' in x for x in lq), '| probe .ts in program', sum('/qa_probe/' in x for x in lf))
f = A('head') + '/' + TEST; orig = open(f, 'rb').read(); s = orig.decode()
anchor = "const EXPECTED_CELLS = 6;\n"; assert s.count(anchor) == 1
open(f, 'w').write(s.replace(anchor, anchor + "const qaPlant1026: number = 'x';\n"))
rc, errs = tsc('head', ['-p', 'tsconfig.qa1026-with-tests.json']); P('TSC-WITH-TESTS PLANT head rc', rc, 'errors', len(errs), [e.split('/src/')[-1][:140] for e in errs])
open(f, 'wb').write(orig); P('  restored sha-equal', sha(f) == hashlib.sha256(orig).hexdigest())
# ---- eslint ----
for t in ('head', 'dev'):
    files = [SVC] + ([TEST] if t == 'head' else [])
    p = subprocess.run([BIN(t, 'eslint'), '-f', 'json'] + files, cwd=A(t), capture_output=True, text=True)
    try:
        j = json.loads(p.stdout); msgs = [(r['filePath'].split('/src/')[-1], m.get('ruleId'), m['message'][:90]) for r in j for m in r['messages']]
        P('ESLINT', t, now(), 'rc', p.returncode, 'files', len(j), 'messages', len(msgs), msgs[:6])
    except Exception as e:
        P('ESLINT', t, 'rc', p.returncode, 'unparsed', type(e).__name__, (p.stdout + p.stderr)[-600:])
ctl = A('head') + '/src/qa1026-eslint-control.ts'; open(ctl, 'w').write('export function qa(): number {\n  const unusedQa1026 = 1;\n  return 2;\n}\n')
p = subprocess.run([BIN('head', 'eslint'), '-f', 'json', 'src/qa1026-eslint-control.ts'], cwd=A('head'), capture_output=True, text=True)
try:
    j = json.loads(p.stdout); P('ESLINT CONTROL fires:', [(m.get('ruleId'), m['message'][:80]) for r in j for m in r['messages']])
except Exception as e:
    P('ESLINT CONTROL unparsed', (p.stdout + p.stderr)[-400:])
os.rename(ctl, ctl + '.quarantined')
# ---- tampers at head ----
def git_quiet(tree):
    return subprocess.run(['git', '-C', paths['trees'][tree], 'diff', '--quiet', 'HEAD'], capture_output=True).returncode
L353 = "  if (allowed.some(entry => parseScopeString(entry).includes('*'))) return []; // KS-839: a wildcard grants nothing, padded or not (' *', 'openid,*' split to '*' on the way to the token)\n"
DEVL = "  if (allowed.includes('*')) return requested; // Wildcard — all scopes\n"
L354 = "  return requested.filter(s => allowed.includes(s));\n"
ROUTE = "    requestedScopes.length > 0 ? requestedScopes : app.allowedScopes,\n    app.allowedScopes,\n  );\n"
def edit(rel, a, b):
    def f(tree):
        p = A(tree) + '/' + rel; s = open(p, encoding='utf-8').read(); assert s.count(a) == 1, (rel, a[:50], s.count(a))
        open(p, 'w', encoding='utf-8').write(s.replace(a, b)); return p
    return f
ROWS = [
  ('T0', None, '0'),
  ('RP-DEV oauth.ts = 19f1e5475 bytes', 'blob:19f1e54750ce2b65312a687add2db4f5628edb7d', 'R1 R2 R3 R4'),
  ('RP-R1 oauth.ts = 8ab493354 bytes', 'blob:8ab493354bbdb3fa52d2eb14654492db1a891e4a', 'R3 R4'),
  ('DEL353', edit(SVC, L353, ''), 'R2 R3 R4'),
  ('REVERT', edit(SVC, L353, DEVL), 'R1 R2 R3 R4'),
  ('NEVERFIRES', edit(SVC, L353, L353.replace("includes('*')))", "includes('**')))")), 'R2 R3 R4'),
  ('NOCOUNT', edit(TEST, "  it('KS-839 R1 - a wildcard app asking for a scope nobody registered is granted nothing', () => {\n    CELLS_RUN += 1;\n", "  it('KS-839 R1 - a wildcard app asking for a scope nobody registered is granted nothing', () => {\n"), 'COMPLETENESS'),
  ('TI inert comment after 354', edit(SVC, L354, L354 + "  // qa1026r2 TI inert\n"), '0'),
  ('G-TRIMSTAR-REVERSED', edit(SVC, L353, "  if (allowed.includes('*')) return [];\n"), 'R3 R4'),
  ('G-TRIM-ONLY', edit(SVC, L353, "  if (allowed.some(entry => entry.trim() === '*')) return [];\n"), 'R3'),
  ('G-SECOND-REGEX (drafter: split on [ tab newline comma] only)', edit(SVC, L353, "  if (allowed.some(entry => entry.split(/[ \\t\\n,]+/).includes('*'))) return [];\n"), '0'),
  ('G-ROUTE-DEFAULT-BYPASS (drafter, carried)', edit('src/routes/oauth.ts', "  const grantedScopes = validateScopes(\n" + ROUTE, "  const grantedScopes = requestedScopes.length > 0 ? validateScopes(\n" + ROUTE.replace(");\n", ") : app.allowedScopes;\n")), '0'),
]
table = []
for name, fn, pred in ROWS:
    snaps = {rel: open(A('head') + '/' + rel, 'rb').read() for rel in (SVC, TEST, 'src/routes/oauth.ts')}
    t0 = now()
    if isinstance(fn, str) and fn.startswith('blob:'): open(A('head') + '/' + SVC, 'wb').write(subprocess.run(['git', '-C', paths['C'], 'show', fn[5:] + ':Blockchain/Dev/services/auth/src/services/oauth.ts'], capture_output=True).stdout)
    elif fn: fn('head')
    s = suite('head', name.split(' ')[0]); rc, errs = tsc('head')
    for rel, b in snaps.items(): open(A('head') + '/' + rel, 'wb').write(b)
    restored = all(sha(A('head') + '/' + rel) == hashlib.sha256(b).hexdigest() for rel, b in snaps.items()); dq = git_quiet('head')
    reds = s.get('failed'); names = ' '.join(sorted(c[1].split(' - ')[0].replace('KS-839 ', '') for c in (s.get('failed_cells') or []))) or '0'
    P('ROW %-70s %s->%s pred %s | reds %s = %s | MATCH %s | files %s tests %s pending %s loadfail %s tsc rc %s (%d err) restored %s git diff --quiet rc %s' % (name, t0, now(), pred, reds, names, names == pred, s.get('files'), s.get('tests'), s.get('pending'), s.get('loadfail'), rc, len(errs), restored, dq))
    for c in s.get('failed_cells') or []: P('     red:', c)
    if errs: P('     tsc:', [e.split('/src/')[-1][:140] for e in errs[:3]])
    table.append(dict(row=name, pred=pred, reds=reds, names=names, match=names == pred, suite={k: v for k, v in s.items() if k != 'failed_cells'}, cells=s.get('failed_cells'), tsc=rc, restored=restored, gitquiet=dq))
json.dump(table, open(GS + '/out/r2/tamper_rows.json', 'w'), indent=1)
# ---- runtime arm: G-SECOND-REGEX applied, the drafter hunt probe re-run at head (does a cell-green tamper leak at runtime?) ----
hp = A('head') + '/src/qa_probe/qa1026r2-drafter-hunt.probe.ts'
os.rename(hp + '.quarantined', hp)
snap = open(A('head') + '/' + SVC, 'rb').read()
edit(SVC, L353, "  if (allowed.some(entry => entry.split(/[ \\t\\n,]+/).includes('*'))) return [];\n")('head')
outj = GS + '/out/r2/rows_hunt_under_G-SECOND-REGEX.json'
p = subprocess.run([BIN('head', 'vitest'), 'run', '--config', 'vitest.qa1026.config.mts', 'src/qa_probe/qa1026r2-drafter-hunt.probe.ts'], cwd=A('head'), capture_output=True, text=True, env=dict(os.environ, QA_OUT=outj, CI='1'))
open(A('head') + '/' + SVC, 'wb').write(snap); os.rename(hp, hp + '.quarantined')
j = json.load(open(outj)); P('RUNTIME ARM G-SECOND-REGEX hunt rc', p.returncode, 'checked', j['checked'], 'leakCount', j.get('leakCount', 0), 'first', j['leaks'][:4], '| restored sha-equal', sha(A('head') + '/' + SVC) == hashlib.sha256(snap).hexdigest(), 'git diff --quiet rc', git_quiet('head'))
P('drafter_tamper end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
