#!/usr/bin/env python3
"""c3_parse_gate55.py — judge a vitest JSON report (`npx vitest run ... --reporter=default --reporter=json --outputFile=<f>`) against the
gate55 expectations for KS-1015's six cells. Two instruments in one: the JSON and the console summary (`Test Files  N ...` / `Tests  N ...`)
of the SAME run (--console <file>); if they disagree the reading is refused. (A NEW COPY of c2_parse_gate54a.py, re-keyed: six cells named
D1-D3 / C1-C3 by kit cell_title_rx, the reds must be AssertionErrors.)
  cells <json> <base|head> [--console f]   the ks1015 file: each cell vs kit cells.<id>.<side>. At base D1-D3 must be RED and each red an
                                           AssertionError (kit red_must_be) with 0 load-failure markers (kit load_failure_markers); C1-C3
                                           GREEN. At head all six GREEN. 0 cells (a load failure) is NEVER a red. A skipped cell is not a pass.
  suite <json> [--console f] [--expect-files N --expect-tests N] [--expect-fail N]
  diff-suites <base.json> <head.json>      head = base + 1 file + 6 tests; the new tests are exactly the ks1015 file's six cells; 0 tests
                                           green at base are red at head (by file + fullName); head failed == 0. (C3 0 NEW REDS)
  --selftest                               synthetic reports through every judge: each defect must be caught, a clean pair must pass
rc 0 PASS / 1 FAIL / 2 usage or unreadable"""
import json, os, re, sys
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
TESTF = os.path.basename(K['test_file']); CRX = re.compile(K['cell_title_rx'])

def load(p):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception as e: print('UNREADABLE %s: %s' % (p, e)); raise SystemExit(2)

def counts(j):
    tr = j.get('testResults') or []
    st = {'passed': 0, 'failed': 0, 'skipped': 0, 'other': 0}
    for f in tr:
        for a in f.get('assertionResults') or []:
            s = a.get('status'); st[s if s in ('passed', 'failed') else 'skipped' if s in ('skipped', 'pending', 'todo') else 'other'] += 1
    return dict(files=len(tr), tests=sum(st.values()), numTotalTests=j.get('numTotalTests'), failed_files=sum(1 for f in tr if f.get('status') == 'failed'), **st)

def console_counts(p):
    t = re.sub(r'\x1b\[[0-9;]*m', '', open(p, encoding='utf-8', errors='replace').read())
    mf = re.search(r'Test Files\s+(.*?)\((\d+)\)', t); mt = re.search(r'^\s*Tests\s+(.*?)\((\d+)\)', t, re.M)
    return (int(mf.group(2)) if mf else None, int(mt.group(2)) if mt else None)

def agree(j, con):
    if not con: return True, 'no console file given'
    cf, ct = console_counts(con); c = counts(j)
    return (cf == c['files'] and ct == c['tests']), 'console Test Files %s / Tests %s vs JSON files %d / tests %d' % (cf, ct, c['files'], c['tests'])

def cells_of(j):
    out = {}; meta = {}
    for f in j.get('testResults') or []:
        if not (f.get('name') or '').endswith(TESTF): continue
        meta = {'file_status': f.get('status'), 'file_message': (f.get('message') or '')[:300]}
        for a in f.get('assertionResults') or []:
            m = CRX.match(a.get('title') or '')   # a test in the file whose title is NOT a kit cell id is kept as '?<title>' -> FAIL unexpected
            out[m.group(1) if m else '?' + (a.get('title') or '')[:60]] = (a.get('status'), '\n'.join(a.get('failureMessages') or [])[:2000])
    return out, meta

def judge_cells(j, side, con=None):
    ok, why = agree(j, con); res = [ok]
    print('%s console/JSON agreement: %s' % ('PASS' if ok else 'FAIL', why))
    cs, meta = cells_of(j)
    blob = ' '.join([meta.get('file_message', '')] + [m for _, m in cs.values()])
    lf = [m for m in K['load_failure_markers'] if m in blob]
    if not cs:
        print('FAIL LOAD: the ks1015 file produced 0 cells (file status %s: %r) — a load failure is never a red' % (meta.get('file_status'), meta.get('file_message'))); return False
    g = not lf; res.append(g); print('%s load-failure markers in the file / its failures: %s (want none)' % ('PASS' if g else 'FAIL', lf or 'NONE'))
    for cid in sorted(K['cells']):
        want = K['cells'][cid][side]; got = cs.get(cid, ('ABSENT', ''))
        if want == 'pass':
            good = got[0] == 'passed'
        else:
            good = got[0] == 'failed' and got[1].lstrip().startswith(K['red_must_be'])
        first = got[1].strip().split('\n')[0][:150]
        print('%s %s at %s: want %s%s | got %s%s' % ('PASS' if good else 'FAIL', cid, side, want, ' (an %s)' % K['red_must_be'] if want == 'fail' else '', got[0], (' | ' + first) if first else ''))
        res.append(good)
    extra = sorted(k for k in cs if k not in K['cells'])
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
    b, h = counts(bj), counts(hj); nb, nh = names(bj), names(hj); res = []; ncell = len(K['cells'])
    new = sorted(k for k in nh if k not in nb); gone = sorted(k for k in nb if k not in nh)
    reg = sorted(k for k in nb if nb[k] == 'passed' and nh.get(k) not in (None, 'passed'))
    sc = K['suite_claim']
    g1 = h['files'] == b['files'] + 1 and h['tests'] == b['tests'] + ncell
    print('%s counts: base %d files / %d tests -> head %d / %d (want +1 / +%d) | builder %s/%s -> %s/%s' % ('PASS' if g1 else 'FAIL', b['files'], b['tests'], h['files'], h['tests'], ncell,
          sc['base_files'], sc['base_tests'], sc['head_files'], sc['head_tests'])); res.append(g1)
    g2 = len(new) == ncell and all(k[0] == TESTF for k in new) and not gone
    print('%s the new tests are exactly the ks1015 cells: new %d %s | vanished %d %s' % ('PASS' if g2 else 'FAIL', len(new), [k[1][-48:] for k in new], len(gone), gone[:5])); res.append(g2)
    g3 = not reg; print('%s 0 NEW REDS (no base-green test red at head): %d %s' % ('PASS' if g3 else 'FAIL', len(reg), reg[:5])); res.append(g3)
    g4 = h['failed'] == 0; print('%s head failed == 0: %d' % ('PASS' if g4 else 'FAIL', h['failed'])); res.append(g4)
    print('INFO base failed %d (a base red is pre-existing; NAME it)' % b['failed'])
    return all(res)

def synth(cells, n_other=70, files=4, cfile=True, load_fail=False, extra_fail=0):
    tr = []; left = n_other; per = max(1, n_other // max(1, files))
    for i in range(files):
        n = per if i < files - 1 else left; left -= n
        ar = [{'title': 't%d_%d' % (i, k), 'fullName': 'f%d t%d' % (i, k), 'status': 'passed', 'failureMessages': []} for k in range(max(0, n))]
        if i == 0 and extra_fail and ar: ar[0]['status'] = 'failed'
        tr.append({'name': '/x/src/__tests__/f%d.test.ts' % i, 'status': 'passed', 'assertionResults': ar})
    if cfile:
        ar = [] if load_fail else [{'title': '%s KS-1015 %s: x' % ('RED' if c[0] == 'D' else 'control', c), 'fullName': 'KS-1015 %s' % c, 'status': s, 'failureMessages': [m] if m else []} for c, (s, m) in cells.items()]
        tr.append({'name': '/x/src/__tests__/' + TESTF, 'status': 'failed' if load_fail or any(s == 'failed' for s, _ in cells.values()) else 'passed',
                   'message': 'Error: Cannot find module \'@secuura/shared\'' if load_fail else '', 'assertionResults': ar})
    return {'numTotalTests': sum(len(f['assertionResults']) for f in tr), 'testResults': tr}

def selftest():
    import io, contextlib
    AE = 'AssertionError: expected { ref: \'#/components/schemas/Delegation\' } to deeply equal { ref: undefined }'
    R = {'D1': ('failed', AE), 'D2': ('failed', AE), 'D3': ('failed', AE), 'C1': ('passed', ''), 'C2': ('passed', ''), 'C3': ('passed', '')}
    Gr = {k: ('passed', '') for k in R}
    con = os.path.join(G, 'c3_selftest_console.fixture.txt')
    base_p = synth({}, 70, 4, cfile=False); head_f = synth(Gr, 70, 4)
    arms = [
        ('T0 real reds at base (AssertionError x3, controls green)', lambda: judge_cells(synth(R, 1, 1), 'base'), True),
        ('T1 6/6 green at head', lambda: judge_cells(synth(Gr, 1, 1), 'head'), True),
        ('T2 a load failure (0 cells) is never a red', lambda: judge_cells(synth(R, 1, 1, load_fail=True), 'base'), False),
        ('T3 a red that is a TypeError, not an assertion', lambda: judge_cells(synth(dict(R, D2=('failed', 'TypeError: Cannot read properties of undefined')), 1, 1), 'base'), False),
        ('T4 a red carrying a load-failure marker', lambda: judge_cells(synth(dict(R, D3=('failed', 'AssertionError: x\nSyntaxError: Unexpected token')), 1, 1), 'base'), False),
        ('T5 a control cell red at base', lambda: judge_cells(synth(dict(R, C2=('failed', AE)), 1, 1), 'base'), False),
        ('T6 a skipped cell at head is not a pass', lambda: judge_cells(synth(dict(Gr, D1=('skipped', '')), 1, 1), 'head'), False),
        ('T7 a D cell GREEN at base (the cell does not bite)', lambda: judge_cells(synth(dict(R, D1=('passed', '')), 1, 1), 'base'), False),
        ('T8 clean suite pair 4/70 -> 5/76', lambda: judge_diff(base_p, head_f), True),
        ('T9 a base-green test red at head (a NEW RED)', lambda: judge_diff(base_p, synth(Gr, 70, 4, extra_fail=1)), False),
        ('T10 a seventh cell / +7 tests', lambda: judge_diff(base_p, synth(dict(Gr, C4=('passed', '')), 70, 4)), False),
        ('T11 console agrees with JSON (5 / 76)', lambda: judge_suite(head_f, con, 5, 76, 0), True),
        ('T12 console disagrees with JSON', lambda: judge_suite(synth(Gr, 69, 4), con), False),
        ('T13 an unexpected cell id', lambda: judge_cells(synth(dict(Gr, D4=('passed', '')), 1, 1), 'head'), False),
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
if A[0] == 'cells' and len(A) >= 3 and A[2] in ('base', 'head'): r = judge_cells(load(A[1]), A[2], opt('--console'))
elif A[0] == 'suite' and len(A) >= 2: r = judge_suite(load(A[1]), opt('--console'), opt('--expect-files'), opt('--expect-tests'), opt('--expect-fail'))
elif A[0] == 'diff-suites' and len(A) >= 3: r = judge_diff(load(A[1]), load(A[2]))
else: print(__doc__); raise SystemExit(2)
print('C3-PARSE %s %s' % (A[0], 'PASS' if r else 'FAIL')); raise SystemExit(0 if r else 1)
