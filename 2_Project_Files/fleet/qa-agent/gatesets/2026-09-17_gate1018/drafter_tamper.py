#!/usr/bin/env python3
"""drafter_tamper.py — #1018 (KS-1050) drafter runs in the drafter clone only (cwd inside the clone; never the Secuura checkout).
1. Whole auth vitest suite (json) + project tsc -p rc at BASE 7e89318bc and HEAD 267bd8624.
2. At HEAD: red-proof (users.ts = base bytes, the PR test in place) + the seat's tamper forms re-derived (TN, TS, TI) + gate-authored rows
   G-503 (status 500 -> 503), G-CODE (a different code), G-MSG (message reworded to the house 'could not be confirmed' wording), G-NULLONLY
   (=== null instead of !updated), and PROBE-ORTHROW (the house helper userRepo.updateUserOrThrow(..., 'Profile update') in place of the call +
   guard: a fix-SHAPE probe, not a tamper). Each row: anchor count 1 + marker, project tsc rc (VOID if != 0), WHOLE auth suite, reds per file,
   restore by bytes + sha256 + git diff --quiet.
3. The test-including tsc program (scratch tsconfig that drops the __tests__ exclude; errors in the touched files; planted control), eslint on
   users.ts (head/base) and the test file. Never rm; scratch configs left in the clone and named. Listeners: LISTEN rows counted before/after."""
import json, subprocess, datetime, os, hashlib, re
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1018'
paths = json.load(open(GS + '/out/drafter_paths.json'))
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
DEV = '/Blockchain/Dev'; HT = paths['trees']['head']; BT = paths['trees']['base']
T = 'src/__tests__/ks1050-profile-update-zero-rows-is-not-success.test.ts'
def listen_rows():
    o = subprocess.run(['lsof', '-nP', '-iTCP', '-sTCP:LISTEN'], capture_output=True, text=True).stdout.splitlines()[1:]
    stubs = subprocess.run(['pgrep', '-f', 'login_stub.mjs'], capture_output=True, text=True).stdout.split()
    return len(o), len(stubs)
P('drafter_tamper', now(), '| LISTEN rows / login_stub.mjs procs BEFORE', listen_rows())
def suite(tree, tag):
    A = tree + DEV + '/services/auth'; out = GS + '/out/suite_%s.json' % tag
    t0 = now()
    p = subprocess.run([tree + DEV + '/node_modules/.bin/vitest', 'run', '--reporter=json', '--outputFile=' + out], cwd=A, capture_output=True, text=True, env=dict(os.environ, CI='1'))
    try: j = json.load(open(out))
    except Exception as e:
        P(tag, 'vitest rc', p.returncode, 'json unreadable', type(e).__name__, (p.stdout + p.stderr)[-1200:]); return None, {}
    reds = {}
    for s in j['testResults']:
        n = sum(1 for a in s['assertionResults'] if a['status'] == 'failed')
        if n or s['status'] != 'passed':
            reds[s['name'].split('/src/')[-1]] = (n, s['status'], [a['title'][:60] + ' :: ' + re.sub(r'\s+', ' ', (a.get('failureMessages') or [''])[0])[:90] for a in s['assertionResults'] if a['status'] == 'failed'][:3] or (s.get('message') or '')[:200])
    P('  suite', tag, t0, '->', now(), 'rc', p.returncode, '| files', j['numTotalTestSuites'], 'failedFiles', j['numFailedTestSuites'], 'tests', j['numTotalTests'], 'failed', j['numFailedTests'], 'pending', j['numPendingTests'], 'todo', j.get('numTodoTests'))
    return j, reds
for name, tree in (('base', BT), ('head', HT)):
    A = tree + DEV + '/services/auth'
    j, reds = suite(tree, name); P('  ', name, 'non-passing files', reds)
    p = subprocess.run([tree + DEV + '/node_modules/.bin/tsc', '--noEmit', '-p', '.'], cwd=A, capture_output=True, text=True); P('  ', name, 'tsc --noEmit -p . rc', p.returncode, (p.stdout + p.stderr).strip()[-300:])
A = HT + DEV + '/services/auth'; BIN = HT + DEV + '/node_modules/.bin/'; F = A + '/src/routes/users.ts'
orig = open(F, 'rb').read(); SHA0 = hashlib.sha256(orig).hexdigest(); P('users.ts head sha256', SHA0[:16])
GUARD = ("    const updated = await userRepo.updateUser(user.id, updates);\n"
         "    // KS-1050: a 0-row UPDATE answers null since KS-943 — never report success over it.\n"
         "    if (!updated) {\n"
         "      throw new AppError('Profile update did not persist — the update matched no row', 500, 'PROFILE_UPDATE_NOT_PERSISTED');\n"
         "    }\n")
COND = "    if (!updated) {\n"
THROW = "      throw new AppError('Profile update did not persist — the update matched no row', 500, 'PROFILE_UPDATE_NOT_PERSISTED');\n"
FORMS = {
  'T0': None,
  'TN': (COND, "    if (false && !updated) { // QA-TAMPER TN\n"),
  'TS': (THROW, "      throw new AppError('Profile update did not persist — the update matched no row', 200, 'PROFILE_UPDATE_NOT_PERSISTED'); // QA-TAMPER TS\n"),
  'TI': (COND, "    if (!updated) { // QA-TAMPER TI inert\n"),
  'G-503': (THROW, "      throw new AppError('Profile update did not persist — the update matched no row', 503, 'PROFILE_UPDATE_NOT_PERSISTED'); // QA-TAMPER G-503\n"),
  'G-CODE': (THROW, "      throw new AppError('Profile update did not persist — the update matched no row', 500, 'INTERNAL_ERROR'); // QA-TAMPER G-CODE\n"),
  'G-MSG': (THROW, "      throw new AppError('Profile update could not be confirmed. Please retry.', 500, 'PROFILE_UPDATE_NOT_PERSISTED'); // QA-TAMPER G-MSG\n"),
  'G-NULLONLY': (COND, "    if (updated === null) { // QA-TAMPER G-NULLONLY\n"),
  'PROBE-ORTHROW': (GUARD, "    const updated = await userRepo.updateUserOrThrow(user.id, updates, 'Profile update'); // QA-TAMPER PROBE-ORTHROW\n"),
}
def restore():
    open(F, 'wb').write(orig); ok = hashlib.sha256(open(F, 'rb').read()).hexdigest() == SHA0
    rc = subprocess.run(['git', '-C', HT, 'diff', '--quiet', 'HEAD'], capture_output=True).returncode; return ok, rc
rows = {}
for tag, form in FORMS.items():
    s = orig.decode()
    if form:
        c = s.count(form[0]); assert c == 1, (tag, 'anchor', c); s = s.replace(form[0], form[1]); assert s.count('QA-TAMPER') == 1
        open(F, 'w').write(s)
    tsc = subprocess.run([BIN + 'tsc', '--noEmit', '-p', '.'], cwd=A, capture_output=True, text=True)
    j, reds = suite(HT, 'tamper_' + tag); ok, drc = restore()
    rows[tag] = dict(tsc=tsc.returncode, files=j and j['numTotalTestSuites'], tests=j and j['numTotalTests'], failed=j and j['numFailedTests'], pending=j and j['numPendingTests'], reds=reds, restored_sha=ok, diff_quiet_rc=drc)
    P(tag, now(), 'anchor 1' if form else 'no edit', '| tsc rc', tsc.returncode, (tsc.stdout + tsc.stderr).strip()[:200], '| reds', reds, '| restored sha', ok, 'diff --quiet rc', drc)
basebytes = subprocess.run(['git', '-C', HT, 'show', paths['sha']['base'] + ':Blockchain/Dev/services/auth/src/routes/users.ts'], capture_output=True).stdout
open(F, 'wb').write(basebytes); j, reds = suite(HT, 'redproof'); ok, drc = restore()
kt = [s for s in j['testResults'] if s['name'].endswith(T)][0]
P('RED-PROOF', now(), 'users.ts = base bytes | ks1050 file run', len(kt['assertionResults']), 'red', sum(1 for a in kt['assertionResults'] if a['status'] == 'failed'), 'green', sum(1 for a in kt['assertionResults'] if a['status'] == 'passed'),
  '| whole', j['numTotalTests'], 'failed', j['numFailedTests'], '| red cells', [(a['title'][:50], (a.get('failureMessages') or [''])[0].split('\n')[0][:60]) for a in kt['assertionResults'] if a['status'] == 'failed'], '| restored', ok, drc)
rows['REDPROOF'] = dict(run=len(kt['assertionResults']), red=sum(1 for a in kt['assertionResults'] if a['status'] == 'failed'), whole_failed=j['numFailedTests'])
json.dump(rows, open(GS + '/out/tamper_rows.json', 'w'), indent=1, ensure_ascii=False)
for name, tree in (('head', HT), ('base', BT)):
    ad = tree + DEV + '/services/auth'; cfg = ad + '/tsconfig.qa1018-with-tests.json'
    open(cfg, 'w').write(json.dumps({'extends': './tsconfig.json', 'compilerOptions': {'noEmit': True, 'rootDir': '.', 'types': ['vitest/globals', 'node']}, 'include': ['src/**/*'], 'exclude': ['node_modules', 'dist']}))
    lf = subprocess.run([tree + DEV + '/node_modules/.bin/tsc', '-p', cfg, '--listFilesOnly'], cwd=ad, capture_output=True, text=True).stdout
    p = subprocess.run([tree + DEV + '/node_modules/.bin/tsc', '-p', cfg], cwd=ad, capture_output=True, text=True)
    errs = [l for l in p.stdout.splitlines() if re.match(r'^src/.*\(\d+,\d+\): error', l)]
    by = {}
    for l in errs: by[l.split('(')[0]] = by.get(l.split('(')[0], 0) + 1
    P('TSC-WITH-TESTS', name, now(), 'rc', p.returncode, '| ks1050 test in program', 'ks1050-profile-update' in lf, '| __tests__ files', lf.count('/__tests__/'), '| error lines', len(errs), 'files', len(by), '| touched-file errors', {k: v for k, v in by.items() if k.endswith('routes/users.ts') or 'ks1050' in k})
    open(GS + '/out/tsc_with_tests_%s.out' % name, 'w').write(p.stdout + p.stderr)
tf = A + '/' + T; tb = open(tf, 'rb').read(); th = hashlib.sha256(tb).hexdigest()
open(tf, 'wb').write(tb + b"\nconst qaPlant1018: number = 'x'; // QA-PLANT\n")
p = subprocess.run([BIN + 'tsc', '-p', A + '/tsconfig.qa1018-with-tests.json'], cwd=A, capture_output=True, text=True)
open(tf, 'wb').write(tb); P('TSC PLANT', 'error lines naming ks1050 test', sum(1 for l in p.stdout.splitlines() if 'ks1050' in l and 'error' in l), '(want >= 1) | restored', hashlib.sha256(open(tf, 'rb').read()).hexdigest() == th)
for rel in ('src/routes/users.ts', T):
    for name, tree in (('head', HT), ('base', BT)):
        ad = tree + DEV + '/services/auth'
        if not os.path.exists(ad + '/' + rel): P('ESLINT', name, rel.split('/')[-1], 'ABSENT'); continue
        p = subprocess.run([tree + DEV + '/node_modules/.bin/eslint', '-f', 'json', rel], cwd=ad, capture_output=True, text=True)
        try:
            ms = json.loads(p.stdout)[0]['messages']; P('ESLINT', name, rel.split('/')[-1], 'rc', p.returncode, 'messages', len(ms), sorted({(m.get('ruleId'), m['message'][:60]) for m in ms})[:8])
        except Exception as e: P('ESLINT', name, rel, 'unparsed', type(e).__name__, (p.stdout + p.stderr)[:300])
os.makedirs(A + '/src/qa_probe', exist_ok=True); fc = A + '/src/qa_probe/qa1018-eslint-control.ts'; open(fc, 'w').write('const qaUnused1018 = 1;\nexport {};\n')
p = subprocess.run([BIN + 'eslint', '-f', 'json', 'src/qa_probe/qa1018-eslint-control.ts'], cwd=A, capture_output=True, text=True)
try: P('ESLINT firing control', [m.get('ruleId') for m in json.loads(p.stdout)[0]['messages']])
except Exception as e: P('ESLINT firing control unparsed', (p.stdout + p.stderr)[:300])
os.rename(fc, fc + '.quarantined')
P('drafter_tamper end', now(), '| LISTEN rows / login_stub.mjs procs AFTER', listen_rows())
