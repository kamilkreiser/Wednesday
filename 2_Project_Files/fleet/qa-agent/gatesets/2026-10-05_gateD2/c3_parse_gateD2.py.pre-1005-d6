#!/usr/bin/env python3
"""c3_parse_gateD2.py — parse a vitest JSON report (`npx vitest run ... --reporter=default --reporter=json --outputFile=<f>`) and judge it
against gateD2's expectations (a NEW COPY of c2_parse_gate54a.py, re-keyed for the KS 1404 file's 25 cells). Two instruments: the JSON and
the console summary (`Test Files N` / `Tests N`, --console <stdout file>); they must agree or the reading is refused.
  cells <json> base|head [--console f]
      HEAD: every cell in the KS 1404 file PASSED, count == kit cells_head (25), 0 skipped, 0 failed.
      BASE: each kit red_set_commission cell (1, 3, 11 indefiniteLength, 12, 14) is FAILED BY ASSERTION (message ~ kit red_msg_rx), never by a
      load error (`Cannot find package|module`, SyntaxError, a 500); cell 13b's red and cell 13's green are reported against the builder's
      claim; SKIPPED cells are counted and reported as a FAILED beforeAll (never a pass, never a red); totals vs kit cells_base_claim.
  suite <json> [--console f] [--expect-files N --expect-tests N --expect-fail 0]
  diff-suites <base.json> <head.json>   head files == base + 1; head tests == base + 25 and the new tests are exactly the KS 1404 file's;
                                        0 tests green at base are red at head (by file + fullName)
  mutation <json> <arm> [--allow-extra] each arm's MUST-GO-RED cells (see ARMS) failed, every other cell passed; REPORT arms print only
  probe-forgery <json> [--console f]    the kit probe's MANDATORY arms passed; REPORT lines (`GD2 REPORT ...`) printed for the gate
  probe-mock <json> base|head           M1..M4 passed (the probe encodes the side's expectation itself)
  --selftest                            synthetic reports: each failure shape must be caught and a clean reading must pass
rc 0 PASS / 1 FAIL / 2 usage or unreadable"""
import json, os, re, sys, io, contextlib
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
TESTF = os.path.basename(K['test_file']); CRX = re.compile(K['cell_rx']); RED = re.compile(K['red_msg_rx'])
LOADERR = re.compile(r'Cannot find (package|module)|SyntaxError|ERR_MODULE_NOT_FOUND|is not a function|expected 500')
ARMS = {   # mutation arm -> cells that MUST go red when the guarded line is disabled (None = REPORT only)
    'sig': ['cell 2'], 'indef': ['cell 11f'], 'imprint': ['cell 3b'], 'chain': ['cell 6'], 'anchors': ['cell 7'],
    'eku': ['cell 8'], 'md': ['cell 10b'], 'validity': ['cell 9'], 'mockpath': None,
}
FORGERY_MANDATORY = ['NETC', 'G0', 'PF1 ', 'PF1C', 'PF2 ', 'PF2b', 'PF3 ', 'PF3b', 'PF4 ', 'PF4b', 'PF4c', 'PF9', 'PF10', 'NET ']


def load(p):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception as e: print('UNREADABLE %s: %s' % (p, e)); raise SystemExit(2)


def counts(j):
    tr = j.get('testResults') or []; st = {'passed': 0, 'failed': 0, 'skipped': 0, 'other': 0}
    for f in tr:
        for a in f.get('assertionResults') or []:
            s = a.get('status'); st[s if s in ('passed', 'failed') else 'skipped' if s in ('skipped', 'pending', 'todo') else 'other'] += 1
    return dict(files=len(tr), tests=sum(st.values()), failed_files=sum(1 for f in tr if f.get('status') == 'failed'), **st)


def console_counts(p):
    t = re.sub(r'\x1b\[[0-9;]*m', '', open(p, encoding='utf-8', errors='replace').read())
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
            m = CRX.match(a.get('title') or '')
            k = m.group(1) if m else (a.get('title') or '?')[:40]
            k = re.sub(r' (RED|GREEN|CONTROL|MUTATION)$', '', k)
            out[k] = (a.get('status'), ' '.join(((a.get('failureMessages') or [''])[0] or '').split('\n')[:1])[:200])
    return out


def judge_cells(j, side, con=None):
    ok, why = agree(j, con); res = [ok]; print('%s console/JSON agreement: %s' % ('PASS' if ok else 'FAIL', why))
    cs = cells_of(j)
    if not cs: print('FAIL LOAD: the KS 1404 file produced 0 cells — a load failure is never a red'); return False
    st = {s: sorted(k for k, v in cs.items() if v[0] == s) for s in ('passed', 'failed', 'skipped')}
    print('INFO %s: %d cells | passed %d | failed %d %s | skipped %d' % (side, len(cs), len(st['passed']), len(st['failed']), st['failed'], len(st['skipped'])))
    if side == 'head':
        g = len(cs) == K['cells_head'] and len(st['passed']) == len(cs)
        res.append(g); print('%s HEAD all %d cells green, 0 skipped, 0 failed: got %d cells, %d passed, %d skipped, %d failed' % ('PASS' if g else 'FAIL', K['cells_head'], len(cs), len(st['passed']), len(st['skipped']), len(st['failed'])))
        return all(res)
    for c, what in sorted(K['red_set_commission'].items()):
        s, m = cs.get(c, ('ABSENT', ''))
        g = s == 'failed' and RED.search(m) is not None and not LOADERR.search(m); res.append(g)
        print('%s BASE %s (%s) RED BY ASSERTION: got %s | %s' % ('PASS' if g else 'FAIL', c, what, s, m[:150]))
    for c, want in (('cell 13b', 'failed'), ('cell 13', 'passed')):
        s, m = cs.get(c, ('ABSENT', ''))
        print('INFO BASE %s builder-claim %s: got %s%s | %s' % (c, want, s, '' if s == want else '  <- DIFFERS from the builder', m[:120]))
    loaders = sorted(k for k, v in cs.items() if v[0] == 'failed' and LOADERR.search(v[1]))
    if loaders: print('FAIL BASE %d cell(s) failed on a LOAD error, not an assertion: %s — fix the INSTRUMENT (workspace install), never count them' % (len(loaders), loaders)); res.append(False)
    cl = K['cells_base_claim']
    print('INFO BASE totals: red %d pass %d skipped %d of %d | builder red %d pass %d skipped %d of %d (%s) | SKIPPED are a failed beforeAll: never a pass, never a red' % (
        len(st['failed']), len(st['passed']), len(st['skipped']), len(cs), cl['red'], cl['pass'], cl['skipped'], cl['total'], cl['skipped_reason']))
    return all(res)


def judge_suite(j, con=None, ef=None, et=None, efail=None):
    ok, why = agree(j, con); c = counts(j); res = [ok]
    print('%s console/JSON agreement: %s' % ('PASS' if ok else 'FAIL', why))
    print('INFO suite: files %(files)d (failed files %(failed_files)d) | tests %(tests)d | passed %(passed)d failed %(failed)d skipped %(skipped)d other %(other)d' % c)
    for name, want, got in (('files', ef, c['files']), ('tests', et, c['tests']), ('failed', efail, c['failed'])):
        if want is not None:
            g = int(want) == got; res.append(g); print('%s suite %s: want %s got %d' % ('PASS' if g else 'FAIL', name, want, got))
    if c['failed_files'] and not c['failed']: print('FAIL suite: %d file(s) failed with 0 failed tests — a LOAD failure (the cheat sheet\'s own gotcha)' % c['failed_files']); res.append(False)
    return all(res)


def names(j):
    return {(os.path.basename(f.get('name') or ''), a.get('fullName') or a.get('title')): a.get('status') for f in j.get('testResults') or [] for a in f.get('assertionResults') or []}


def judge_diff(bj, hj):
    b, h = counts(bj), counts(hj); nb, nh = names(bj), names(hj); res = []; N = K['cells_head']
    new = sorted(k for k in nh if k not in nb); gone = sorted(k for k in nb if k not in nh)
    reg = sorted(k for k in nb if nb[k] == 'passed' and nh.get(k) not in (None, 'passed'))
    g1 = h['files'] == b['files'] + 1 and h['tests'] == b['tests'] + N
    print('%s counts: base %d/%d -> head %d/%d (want +1 file, +%d tests) | builder %s/%s -> %s/%s' % ('PASS' if g1 else 'FAIL', b['files'], b['tests'], h['files'], h['tests'], N,
          K['suite_claim']['base_files'], K['suite_claim']['base_tests'], K['suite_claim']['head_files'], K['suite_claim']['head_tests'])); res.append(g1)
    g2 = len(new) == N and all(k[0] == TESTF for k in new) and not gone
    print('%s the new tests are exactly the KS 1404 file: new %d (outside it %d) | vanished %d %s' % ('PASS' if g2 else 'FAIL', len(new), sum(1 for k in new if k[0] != TESTF), len(gone), gone[:4])); res.append(g2)
    g3 = not reg; print('%s 0 base-green tests red at head: %d %s' % ('PASS' if g3 else 'FAIL', len(reg), reg[:4])); res.append(g3)
    g4 = h['failed'] == 0 and h['skipped'] == 0; print('%s head failed 0 and skipped 0: %d / %d' % ('PASS' if g4 else 'FAIL', h['failed'], h['skipped'])); res.append(g4)
    print('INFO base failed %d (a base red is pre-existing: NAME it)' % b['failed'])
    return all(res)


def judge_mutation(j, arm):
    cs = cells_of(j); must = ARMS.get(arm, 'UNKNOWN')
    if must == 'UNKNOWN': print('FAIL unknown arm %r (known %s)' % (arm, sorted(ARMS))); return False
    red = sorted(k for k, v in cs.items() if v[0] == 'failed'); skipped = sorted(k for k, v in cs.items() if v[0] != 'passed' and v[0] != 'failed')
    if must is None:
        print('REPORT MUTATION %s: red cells %s | skipped %s (no cell is expected to guard this line alone; the gate rules)' % (arm, red, skipped)); return True
    extra = sorted(set(red) - set(must)); allow = '--allow-extra' in sys.argv
    g = set(must) <= set(red) and not skipped and len(cs) == K['cells_head'] and (allow or not extra)
    print('%s MUTATION %s: want %s RED, nothing else red, no skip | red %s | extra reds %s%s | skipped %s | cells %d' % ('PASS' if g else 'FAIL', arm, must, red, extra or 'NONE',
          ' (ALLOWED by --allow-extra: the drafter\'s scratch has no workspace, so the route cells load-fail)' if allow and extra else '', skipped, len(cs)))
    return g


def judge_probe_forgery(j, con=None):
    rows = [(a.get('title') or '', a.get('status'), ((a.get('failureMessages') or [''])[0] or '').split('\n')[0][:160]) for f in j.get('testResults') or [] if 'zz-gD2-probe-forgery' in (f.get('name') or '') for a in f.get('assertionResults') or []]
    if not rows: print('FAIL LOAD: the forgery probe produced 0 arms'); return False
    res = []
    for pre in FORGERY_MANDATORY:
        hit = [r for r in rows if (r[0] + ' ').startswith(pre)]
        g = len(hit) == 1 and hit[0][1] == 'passed'; res.append(g)
        print('%s %s: %s' % ('PASS' if g else 'FAIL', pre.strip(), (hit[0][1] + ' | ' + hit[0][0][:80] + (' | ' + hit[0][2] if hit[0][2] else '')) if hit else 'ABSENT'))
    for t, s, m in rows:
        if t.startswith('REPORT'): print('REPORT-ARM %s: %s %s' % (t[:60], s, m))
    if con and os.path.isfile(con):
        for l in open(con, encoding='utf-8', errors='replace'):
            if l.startswith('GD2 REPORT') or l.startswith('GD2 ARM'): print('  ' + l.rstrip())
    return all(res)


def judge_probe_mock(j, side):
    rows = [(a.get('title') or '', a.get('status')) for f in j.get('testResults') or [] if 'zz-gD2-probe-mock' in (f.get('name') or '') for a in f.get('assertionResults') or []]
    g = len(rows) == 4 and all(s == 'passed' and ('at %s' % side) in t for t, s in rows)
    print('%s MOCK probe at %s: %d arms, all passed with the %s expectation: %s' % ('PASS' if g else 'FAIL', side, len(rows), side, [(t[:30], s) for t, s in rows]))
    return g


def synth(cells, files=None):
    tr = [{'name': '/x/src/__tests__/f%d.test.ts' % i, 'status': 'passed', 'assertionResults': [{'title': 't%d' % i, 'fullName': 'f%d t' % i, 'status': 'passed', 'failureMessages': []}]} for i in range(files or 0)]
    if cells is not None:
        tr.append({'name': '/x/src/__tests__/' + TESTF, 'status': 'failed' if any(s != 'passed' for s, _ in cells.values()) else 'passed',
                   'assertionResults': [{'title': '%s [x]: y' % n, 'fullName': 'KS 1404 %s' % n, 'status': s, 'failureMessages': [m] if m else []} for n, (s, m) in cells.items()]})
    return {'testResults': tr}


def selftest():
    names25 = ['cell 1', 'cell 3', 'cell 4', 'cell 11 truncated', 'cell 11 trailingBytes', 'cell 11 wrongOuterTag', 'cell 11 indefiniteLength', 'cell 11e', 'cell 12', 'cell 12b',
               'cell 5', 'cell 6', 'cell 7', 'cell 2', 'cell 10', 'cell 10b', 'cell 8', 'cell 9', 'cell 3b', 'cell 11f', 'cell 11g', 'cell 16', 'cell 14', 'cell 13', 'cell 13b']
    G25 = {n: ('passed', '') for n in names25}
    A = 'AssertionError: expected true to be false // Object.is equality'
    BASE = dict(G25)
    for n in ('cell 1', 'cell 3', 'cell 12', 'cell 14', 'cell 13b'): BASE[n] = ('failed', A)
    BASE['cell 11 indefiniteLength'] = ('failed', 'AssertionError: indefiniteLength must not verify: expected true to be false')
    for n in names25[10:22]: BASE[n] = ('skipped', '')
    LOAD = dict(BASE); LOAD['cell 14'] = ('failed', "Error: Cannot find package '@secuura/shared'")
    arms = [
        ('T0 head 25/25 green', lambda: judge_cells(synth(G25), 'head'), True),
        ('T1 head with a skipped cell', lambda: judge_cells(synth(dict(G25, **{'cell 5': ('skipped', '')})), 'head'), False),
        ('T2 head with 24 cells', lambda: judge_cells(synth({k: v for k, v in G25.items() if k != 'cell 16'}), 'head'), False),
        ('T3 base: the claimed red set by assertion', lambda: judge_cells(synth(BASE), 'base'), True),
        ('T4 base: cell 14 red on a LOAD error is not red-first', lambda: judge_cells(synth(LOAD), 'base'), False),
        ('T5 base: cell 12 green (the mock door already shut)', lambda: judge_cells(synth(dict(BASE, **{'cell 12': ('passed', '')})), 'base'), False),
        ('T6 0 cells (load failure)', lambda: judge_cells(synth({}), 'base'), False),
        ('T7 clean suite pair 5 -> 6 files, +25', lambda: judge_diff(synth(None, 5), synth(G25, 5)), True),
        ('T8 a base-green test red at head', lambda: judge_diff(synth(None, 5), (lambda h: (h['testResults'][0]['assertionResults'][0].update(status='failed'), h)[1])(synth(G25, 5))), False),
        ('T9 mutation sig: cell 2 red', lambda: judge_mutation(synth(dict(G25, **{'cell 2': ('failed', A)})), 'sig'), True),
        ('T10 mutation sig that stays green (vacuous)', lambda: judge_mutation(synth(G25), 'sig'), False),
        ('T11 suite 2 files failed with 0 failed tests (load)', lambda: judge_suite({'testResults': [{'name': 'a', 'status': 'failed', 'assertionResults': []}]}), False),
    ]
    ok = 0
    for name, fn, want in arms:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): got = fn()
        good = got == want; ok += good
        print('SELFTEST %s %s: want %s got %s' % ('OK' if good else 'MISS', name, 'PASS' if want else 'FAIL', 'PASS' if got else 'FAIL'))
        for l in buf.getvalue().splitlines():
            if l.startswith('FAIL') and not want: print('    ' + l[:200])
    print('SELFTEST %s %d of %d' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms))); return ok == len(arms)


A = sys.argv[1:]
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
if not A or A[0] in ('-h', '--help'): print(__doc__); raise SystemExit(0 if A else 2)
if A[0] == '--selftest': raise SystemExit(0 if selftest() else 1)
if A[0] == 'cells' and len(A) >= 3: r = judge_cells(load(A[1]), A[2], opt('--console'))
elif A[0] == 'suite' and len(A) >= 2: r = judge_suite(load(A[1]), opt('--console'), opt('--expect-files'), opt('--expect-tests'), opt('--expect-fail'))
elif A[0] == 'diff-suites' and len(A) >= 3: r = judge_diff(load(A[1]), load(A[2]))
elif A[0] == 'mutation' and len(A) >= 3: r = judge_mutation(load(A[1]), A[2])
elif A[0] == 'probe-forgery' and len(A) >= 2: r = judge_probe_forgery(load(A[1]), opt('--console'))
elif A[0] == 'probe-mock' and len(A) >= 3: r = judge_probe_mock(load(A[1]), A[2])
else: print(__doc__); raise SystemExit(2)
print('C3-PARSE %s %s' % (A[0], 'PASS' if r else 'FAIL')); raise SystemExit(0 if r else 1)
