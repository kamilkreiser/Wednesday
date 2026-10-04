#!/usr/bin/env python3
"""c2_parse_gate54a.py — parse a vitest JSON report (written by `npx vitest run ... --reporter=default --reporter=json --outputFile=<f>`) and
judge it against the kit's expectations. Two instruments in one: the JSON, and the console summary lines `Test Files  N ...` / `Tests  N ...`
from the same run's stdout (--console <file>); the two must agree or the reading is refused.
  cells <json> <base|head> [--console f]   the KS-1402 file: CELL 1..4 status vs kit cells.<n>.<side>; at base each red must be an ASSERTION
                                           naming kit base_msg (`expected 401 to be 200` ...), never a load failure (0 tests / file error)
  suite <json> [--console f] [--expect-files N --expect-tests N] [--expect-fail 0]   counts: files, tests, passed, failed, skipped
  diff-suites <base.json> <head.json>      head files == base + 1, head tests == base + 4, the 4 new ones are exactly the ks1402 file's cells,
                                           0 tests that passed at base fail at head (by fullName)
  mutation <json> <arm>                    arm users: cells 1 and 2 RED (4 also red, it is 401 there); arm authmw: 4/4 GREEN (the PR's own
                                           claim that authenticate.ts is covered by no cell)
  probe <json> <base|head>                 the C3 runtime probe's arms: per-arm status; at head P1 P1C P2* P2C P3 P4 green, P5/P5b REPORTED
  --selftest                               synthetic reports: a real red, a load failure, a skipped cell, a count mismatch, a console/JSON
                                           disagreement, a base-pass-head-fail regression — each must be caught; a clean pair must pass
rc 0 PASS / 1 FAIL / 2 usage or unreadable"""
import json, os, re, sys
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
TESTF = os.path.basename(K['test_file'])

def load(p):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception as e: print('UNREADABLE %s: %s' % (p, e)); raise SystemExit(2)

def counts(j):
    tr = j.get('testResults') or []
    st = {'passed': 0, 'failed': 0, 'skipped': 0, 'other': 0}
    for f in tr:
        for a in f.get('assertionResults') or []:
            s = a.get('status'); st[s if s in ('passed', 'failed') else 'skipped' if s in ('skipped', 'pending', 'todo') else 'other'] += 1
    return {'files': len(tr), 'tests': sum(st.values()), 'numTotalTests': j.get('numTotalTests'), 'failed_files': sum(1 for f in tr if f.get('status') == 'failed'), **st}

def console_counts(p):
    t = open(p, encoding='utf-8', errors='replace').read(); t = re.sub(r'\x1b\[[0-9;]*m', '', t)
    mf = re.search(r'Test Files\s+(.*?)\((\d+)\)', t); mt = re.search(r'^\s*Tests\s+(.*?)\((\d+)\)', t, re.M)
    return (int(mf.group(2)) if mf else None, int(mt.group(2)) if mt else None)

def agree(j, con):
    if not con: return True, 'no console file given'
    cf, ct = console_counts(con); c = counts(j)
    return (cf == c['files'] and ct == c['tests']), 'console Test Files %s / Tests %s vs JSON files %d / tests %d' % (cf, ct, c['files'], c['tests'])

def cells_of(j):
    out = {}
    for f in j.get('testResults') or []:
        if not (f.get('name') or '').endswith(TESTF): continue
        for a in f.get('assertionResults') or []:
            m = re.match(r'(CELL \d+)', a.get('title') or '')
            if m: out[m.group(1)] = (a.get('status'), ((a.get('failureMessages') or [''])[0] or '').split('\n')[0][:160])
        out['_file_status'] = f.get('status'); out['_file_message'] = (f.get('message') or '')[:200]
    return out

def judge_cells(j, side, con=None):
    ok, why = agree(j, con); res = []
    print('%s console/JSON agreement: %s' % ('PASS' if ok else 'FAIL', why)); res.append(ok)
    cs = cells_of(j)
    if not [k for k in cs if k.startswith('CELL')]:
        print('FAIL LOAD: the ks1402 file produced 0 cells (file status %s: %s) — a load failure is never a red' % (cs.get('_file_status'), cs.get('_file_message'))); return False
    for n in sorted(K['cells']):
        want = K['cells'][n][side]; got = cs.get(n, ('ABSENT', ''))
        good = (got[0] == 'passed') if want == 'pass' else (got[0] == 'failed' and K['cells'][n]['base_msg'] is not None and K['cells'][n]['base_msg'] in got[1])
        print('%s %s at %s: want %s%s | got %s %s' % ('PASS' if good else 'FAIL', n, side, want, (' with %r' % K['cells'][n]['base_msg']) if want == 'fail' else '', got[0], ('| ' + got[1]) if got[1] else ''))
        res.append(good)
    extra = sorted(k for k in cs if k.startswith('CELL') and k not in K['cells'])
    if extra: print('FAIL unexpected cells %s' % extra); res.append(False)
    return all(res)

def judge_suite(j, con=None, ef=None, et=None, efail=None):
    ok, why = agree(j, con); c = counts(j); res = [ok]
    print('%s console/JSON agreement: %s' % ('PASS' if ok else 'FAIL', why))
    print('INFO suite: files %(files)d (failed files %(failed_files)d) | tests %(tests)d (numTotalTests %(numTotalTests)s) | passed %(passed)d failed %(failed)d skipped %(skipped)d other %(other)d' % c)
    for name, want, got in (('files', ef, c['files']), ('tests', et, c['tests']), ('failed', efail, c['failed'])):
        if want is not None:
            g = int(want) == got; res.append(g); print('%s suite %s: want %s got %d' % ('PASS' if g else 'FAIL', name, want, got))
    return all(res)

def names(j):
    d = {}
    for f in j.get('testResults') or []:
        for a in f.get('assertionResults') or []:
            d[(os.path.basename(f.get('name') or ''), a.get('fullName') or a.get('title'))] = a.get('status')
    return d

def judge_diff(bj, hj):
    b, h = counts(bj), counts(hj); nb, nh = names(bj), names(hj); res = []
    new = sorted(k for k in nh if k not in nb); gone = sorted(k for k in nb if k not in nh)
    reg = sorted(k for k in nb if nb[k] == 'passed' and nh.get(k) not in (None, 'passed'))
    g1 = h['files'] == b['files'] + 1 and h['tests'] == b['tests'] + 4
    print('%s counts: base %d files / %d tests -> head %d / %d (want +1 / +4) | builder %s/%s -> %s/%s' % ('PASS' if g1 else 'FAIL', b['files'], b['tests'], h['files'], h['tests'],
          K['suite_claim']['base_files'], K['suite_claim']['base_tests'], K['suite_claim']['head_files'], K['suite_claim']['head_tests'])); res.append(g1)
    g2 = len(new) == 4 and all(k[0] == TESTF for k in new) and not gone
    print('%s new tests are exactly the ks1402 cells: new %d %s | vanished %d %s' % ('PASS' if g2 else 'FAIL', len(new), [k[1][:50] for k in new], len(gone), gone[:5])); res.append(g2)
    g3 = not reg; print('%s no base-green test is red at head: %d regression(s) %s' % ('PASS' if g3 else 'FAIL', len(reg), reg[:5])); res.append(g3)
    g4 = h['failed'] == 0; print('%s head failed == 0: %d' % ('PASS' if g4 else 'FAIL', h['failed'])); res.append(g4)
    print('INFO base failed %d (a base red outside the ks1402 file is pre-existing; NAME it)' % b['failed'])
    return all(res)

def judge_mutation(j, arm):
    cs = cells_of(j); st = {n: cs.get(n, ('ABSENT', ''))[0] for n in sorted(K['cells'])}
    if arm == 'users':
        good = st['CELL 1'] == 'failed' and st['CELL 2'] == 'failed' and st['CELL 3'] == 'passed'
        print('%s MUTATION users.ts reverted at head: cells %s (want 1 and 2 RED, 3 GREEN; 4 also red at 401)' % ('PASS' if good else 'FAIL', st))
    else:
        good = all(v == 'passed' for v in st.values())
        print('%s MUTATION authenticate.ts reverted at head: cells %s (want 4/4 GREEN — the PR says no cell covers the label; a RED would mean it is covered)' % ('PASS' if good else 'FAIL', st))
    return good

def judge_probe(j, side):
    rows = []
    for f in j.get('testResults') or []:
        if 'zz-g54a-probe' not in (f.get('name') or ''): continue
        for a in f.get('assertionResults') or []:
            m = re.match(r'(P\d+[a-zA-Z]?)', a.get('title') or ''); rows.append((m.group(1) if m else '?', a.get('title'), a.get('status'), ((a.get('failureMessages') or [''])[0] or '').split('\n')[0][:140]))
    if not rows: print('FAIL LOAD: the probe produced 0 arms'); return False
    res = []
    for arm, title, st, msg in rows:
        if arm in ('P5', 'P5b'):
            print('REPORT %s at %s: %s %s | %s' % (arm, side, st, title[:70], msg)); continue
        want = 'passed' if side == 'head' or arm in ('P1C', 'P2', 'P3') else 'failed'
        good = st == want; res.append(good)
        print('%s %s at %s: want %s got %s | %s %s' % ('PASS' if good else 'FAIL', arm, side, want, st, title[:70], msg))
    return all(res)

def synth(cells, extra_pass=836, extra_fail=0, files=77, cfile=True, load_fail=False):
    tr = []
    per = max(1, extra_pass // max(1, files))
    left = extra_pass
    for i in range(files):
        n = per if i < files - 1 else left; left -= n
        ar = [{'title': 't%d_%d' % (i, k), 'fullName': 'f%d t%d' % (i, k), 'status': 'passed', 'failureMessages': []} for k in range(max(0, n))]
        if i == 0 and extra_fail: ar[0]['status'] = 'failed'
        tr.append({'name': '/x/src/__tests__/f%d.test.ts' % i, 'status': 'passed', 'assertionResults': ar})
    if cfile:
        ar = [] if load_fail else [{'title': '%s — x' % n, 'fullName': 'KS-1402 %s' % n, 'status': s, 'failureMessages': [m] if m else []} for n, (s, m) in cells.items()]
        tr.append({'name': '/x/src/__tests__/' + TESTF, 'status': 'failed' if load_fail or any(s == 'failed' for s, _ in cells.values()) else 'passed', 'message': 'Error: Cannot find module' if load_fail else '', 'assertionResults': ar})
    return {'numTotalTests': sum(len(f['assertionResults']) for f in tr), 'testResults': tr}

def selftest():
    import io, contextlib
    R = {'CELL 1': ('failed', 'AssertionError: expected 401 to be 200 // Object.is equality'), 'CELL 2': ('failed', 'AssertionError: expected 401 to be 403'),
         'CELL 3': ('passed', ''), 'CELL 4': ('failed', 'AssertionError: expected 401 to be 404')}
    Gr = {k: ('passed', '') for k in R}
    con = os.path.join(G, 'c2_selftest_console.fixture.txt')   # a READ-ONLY fixture shipped in the kit (vitest's summary shape, ANSI-free)
    base_pristine = synth({}, 836, 0, 77, cfile=False); head_full = synth(Gr, 836, 0, 77)
    arms = [
        ('T0 real red at base', lambda: judge_cells(synth(R, 1, 0, 1), 'base'), True),
        ('T1 green at head', lambda: judge_cells(synth(Gr, 1, 0, 1), 'head'), True),
        ('T2 load failure is never a red', lambda: judge_cells(synth(R, 1, 0, 1, load_fail=True), 'base'), False),
        ('T3 a red with the wrong message (a 500, not the 401 door)', lambda: judge_cells(synth(dict(R, **{'CELL 1': ('failed', 'expected 500 to be 200')}), 1, 0, 1), 'base'), False),
        ('T4 a skipped cell at head is not a pass', lambda: judge_cells(synth(dict(Gr, **{'CELL 4': ('skipped', '')}), 1, 0, 1), 'head'), False),
        ('T5 the control cell red at base', lambda: judge_cells(synth(dict(R, **{'CELL 3': ('failed', 'expected 401 to be 200')}), 1, 0, 1), 'base'), False),
        ('T6 clean suite pair 77/836 -> 78/840', lambda: judge_diff(base_pristine, head_full), True),
        ('T7 a base-green test red at head', lambda: judge_diff(base_pristine, synth(Gr, 836, 1, 77)), False),
        ('T8 +5 tests (a fifth cell or a stray file)', lambda: judge_diff(base_pristine, synth(dict(Gr, **{'CELL 5': ('passed', '')}), 836, 0, 77)), False),
        ('T9 console agrees with JSON', lambda: judge_suite(head_full, con, 78, 840, 0), True),
        ('T10 console disagrees with JSON', lambda: judge_suite(synth(Gr, 835, 0, 77), con), False),
        ('T11 mutation users: 1/2 red', lambda: judge_mutation(synth(R, 1, 0, 1), 'users'), True),
        ('T12 mutation users that stays green (a vacuous cell set)', lambda: judge_mutation(synth(Gr, 1, 0, 1), 'users'), False),
        ('T13 mutation authmw 4/4 green', lambda: judge_mutation(synth(Gr, 1, 0, 1), 'authmw'), True),
    ]
    ok = 0
    for name, fn, want in arms:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): got = fn()
        good = got == want; ok += good
        print('SELFTEST %s %s: want %s got %s' % ('OK' if good else 'MISS', name, 'PASS' if want else 'FAIL', 'PASS' if got else 'FAIL'))
        for l in buf.getvalue().splitlines():
            if l.startswith('FAIL') or not want: print('    ' + l[:220])
    print('SELFTEST %s %d of %d (fixture %s)' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms), os.path.basename(con)))
    return ok == len(arms)

A = sys.argv[1:]
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
if not A or A[0] in ('-h', '--help'): print(__doc__); raise SystemExit(0 if A else 2)
if A[0] == '--selftest': raise SystemExit(0 if selftest() else 1)
if A[0] == 'cells' and len(A) >= 3: r = judge_cells(load(A[1]), A[2], opt('--console'))
elif A[0] == 'suite' and len(A) >= 2: r = judge_suite(load(A[1]), opt('--console'), opt('--expect-files'), opt('--expect-tests'), opt('--expect-fail'))
elif A[0] == 'diff-suites' and len(A) >= 3: r = judge_diff(load(A[1]), load(A[2]))
elif A[0] == 'mutation' and len(A) >= 3: r = judge_mutation(load(A[1]), A[2])
elif A[0] == 'probe' and len(A) >= 3: r = judge_probe(load(A[1]), A[2])
else: print(__doc__); raise SystemExit(2)
print('C2-PARSE %s %s' % (A[0], 'PASS' if r else 'FAIL')); raise SystemExit(0 if r else 1)
