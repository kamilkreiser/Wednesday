#!/usr/bin/env python3
r"""c3_suites_gate74.py — gate74's suites for #1423 (KS-1164), INCLUDING THE PREFLIGHT'S WEIGHT.
Carried in shape from c3_suites_gate73.py (one parser for before/after, subset compare, arm with landed+restored asserted, --system-tmp)
and re-written for this row by the gate74 drafter. #1423's push ran NO preflight (.githooks/pre-push selects it only on ^Blockchain/Dev/),
so this script runs, BY HAND and exactly as the hook would, every leg a Blockchain/Dev push would have run — at the head, at the base, and
on the SIM squash tree — plus the package's OWN suites through its OWN script and config (never a bare `vitest run`: R 13th measured a
bare run ignoring vitest.unit.config.ts — 5,000 ms timeout instead of 15,000, no setupFiles — and producing a FALSE timeout failure).

EVERY worktree is YOURS, outside !CODING (refused otherwise), and is BOUND to a pin: `--expect-tree <40-hex>` must equal the worktree's
HEAD^{tree} or the mode refuses (rc 11). TMPDIR is forced to /tmp for every child (Q-X9 carried: a long scratch TMPDIR breaks tsx's IPC
socket, 104-byte limit, identically at base and head).

MODES
  perf     --wt W --expect-tree T --out J           `npm run test:unit -- --reporter=default --reporter=json --outputFile.json=J` in
                                                    systemTest/performance. Parsed from J ONLY (one parser): files, tests, passed,
                                                    failed, pending, the failing SET (file::title). rc = the run's rc.
  perfcmp  --a J_before --b J_after [--new-file F --new-tests N]
                                                    the after-failing SET is a SUBSET of the before-failing set; +passed / +files
                                                    printed; F (the new suite) present in after with N tests, all passed, absent before.
                                                    CONTROL in-process: a fabricated failure added to `after` must break the subset.
  onefile  --wt W --expect-tree T --out J           the new suite ALONE, through the package script: 3 tests, 3 passed; the titles
                                                    RED KS-1164 F-3 / CONTROL F-3c / CONTROL F-3r each present once.
  tamper   --wt W --expect-tree T --arm both|passes|fails --out J
                                                    report.ts:104: drop `.toLocaleString()` from both counts (both), or one (passes /
                                                    fails — one arm PER CONJUNCT, STANDING_LINES S65). Anchor count asserted == 1 BEFORE,
                                                    tamper asserted LANDED, the suite run, the file RESTORED and its sha256 asserted ==
                                                    the pre-tamper hash, `git status --porcelain` asserted empty. Expect: exactly 1 failed
                                                    (RED F-3), 2 passed (both CONTROLs), 3 total — a load failure reads 0 total.
  tsc      --wt W --expect-tree T                   the `lint` script's two tsc legs (tsconfig.json, tsconfig.node.json) --noEmit: rc and
                                                    line count each.
  format   --wt W --expect-tree T --paths P1,P2,..  the pre-push FORMAT GATE (systemTest/scripts/check-package-format.sh) fed the push's
                                                    changed list on stdin exactly as the hook does; parses `N package(s) checked` (0 checked
                                                    is a FAIL, never clean) and the rc.
  preflight --wt W --expect-tree T --out J [--tag X] the WHOLE preflight as the hook invokes it (source systemTest/slot-target.sh at the root,
                                                    then Blockchain/Dev/scripts/preflight/preflight.sh). Requires S-1 already done in W
                                                    (Blockchain/Dev `npm ci --ignore-scripts` + `npm run build --workspace=packages/shared`
                                                    with dist/index.js PRESENT, and `npm ci --ignore-scripts` in EVERY systemTest/* with a
                                                    package.json) — refuses rc 12 naming what is missing. Parsed into J: verdict line, legs
                                                    ran / of, SKIPPED legs, FAILED legs, `shell suites: P passed, F failed, S skipped (of N)`,
                                                    every `FAILED: <suite>` line, the `MISMATCH` lines.
  pfcmp    --a J_ref --b J_subject                  subject's FAILED legs SUBSET of ref's; subject's failed shell suites SUBSET of ref's;
                                                    ran-legs and shell `of` printed side by side; a NEW failing leg or suite is a FAIL.
  leg14    --wt W --expect-tree T                   systemTest/__tests__/no_hardcoded_slot_literals.test.sh alone in a REAL worktree (an
                                                    archive is refused by the suite itself — 'not a git work tree', 0 files scanned, a FALSE
                                                    red the drafter hit): passed / failed / `scanned N files`, the planted CONTROL line
                                                    present, and the count of `slot2` lines in the schemathesis baseline file.
  --selftest                                        every parser on CAPTURED real lines (drafter runs 2026-10-07/08), plus planted arms.
rc 0 PASS / 1 FAIL / 2 refused / 11 the worktree is not the pinned tree / 12 S-1 not done."""
import hashlib, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate74 import K, ROWS, Tally, opt, outside_forbidden

R = ROWS['1423']
NEW_FILE = [p for p in R['numstat'] if p.endswith('.test.ts')][0]
NEW_REL = NEW_FILE.split('systemTest/performance/', 1)[1]
PERF = 'systemTest/performance'
REPORT = 'systemTest/performance/gate/report.ts'
ANCHOR = '? `${name} ${label} passes=${metric.passes.toLocaleString()} fails=${metric.fails.toLocaleString()}`'
TAMPERS = {
    'both':   '? `${name} ${label} passes=${metric.passes} fails=${metric.fails}`',
    'passes': '? `${name} ${label} passes=${metric.passes} fails=${metric.fails.toLocaleString()}`',
    'fails':  '? `${name} ${label} passes=${metric.passes.toLocaleString()} fails=${metric.fails}`',
}
TITLES = ('RED KS-1164 F-3', 'CONTROL KS-1164 F-3c', 'CONTROL KS-1164 F-3r')
ENV = dict(os.environ); ENV.pop('GIT_SSH_COMMAND', None); ENV['TMPDIR'] = '/tmp'


def bind(wt, tree):
    if not (wt and tree): raise SystemExit('REFUSED: --wt and --expect-tree are REQUIRED')
    if not outside_forbidden(wt): print('REFUSED: --wt %s is under %s — use YOUR worktree in YOUR clone' % (wt, K['forbidden_root'])); sys.exit(2)
    p = subprocess.run(['git', '-C', wt, 'rev-parse', 'HEAD^{tree}'], capture_output=True, text=True)
    got = p.stdout.strip()
    if p.returncode != 0 or got != tree:
        print('REFUSED (rc 11): worktree %s HEAD^{tree} %r != --expect-tree %s — the run would not be about the pinned tree' % (wt, got[:12], tree[:12])); sys.exit(11)
    st = subprocess.run(['git', '-C', wt, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout
    if st.strip(): print('REFUSED (rc 11): worktree %s has tracked modifications before the run:\n%s' % (wt, st[:400])); sys.exit(11)
    print('BOUND: %s HEAD^{tree} == %s, 0 tracked modifications' % (wt, tree[:12]))


def npm_unit(wt, out, extra=()):
    args = ['npm', 'run', 'test:unit', '--', *extra, '--reporter=default', '--reporter=json', '--outputFile.json=' + out]
    p = subprocess.run(args, cwd=os.path.join(wt, PERF), capture_output=True, text=True, env=ENV)
    open(out + '.console.txt', 'w').write(p.stdout + '\n--- stderr ---\n' + p.stderr)
    return p.returncode


def parse_vitest_json(path):
    d = json.load(open(path))
    fails = sorted('%s::%s' % (os.path.basename(tr['name']), a['title']) for tr in d['testResults'] for a in tr['assertionResults'] if a['status'] == 'failed')
    files = sorted(os.path.relpath(tr['name']).split('systemTest/performance/')[-1] for tr in d['testResults'])
    per = {}
    for tr in d['testResults']:
        k = tr['name'].split('systemTest/performance/')[-1]
        per[k] = [(a['title'], a['status']) for a in tr['assertionResults']]
    return {'files': len(d['testResults']), 'tests': d['numTotalTests'], 'passed': d['numPassedTests'], 'failed': d['numFailedTests'],
            'pending': d['numPendingTests'], 'fail_set': fails, 'file_list': files, 'per_file': per, 'success': d.get('success')}


def perfcmp(a, b, new_file=None, new_n=None, t=None):
    t = t or Tally()
    sub = set(b['fail_set']) <= set(a['fail_set'])
    t.check('C1', sub, 'after failing SET (%d) SUBSET of before (%d): %s | new reds %s' % (len(b['fail_set']), len(a['fail_set']), sub, sorted(set(b['fail_set']) - set(a['fail_set']))[:5]))
    t.info('C2', 'files %d -> %d (+%d) | tests %d -> %d (+%d) | passed %d -> %d (+%d) | failed %d -> %d' % (
        a['files'], b['files'], b['files'] - a['files'], a['tests'], b['tests'], b['tests'] - a['tests'], a['passed'], b['passed'], b['passed'] - a['passed'], a['failed'], b['failed']))
    if new_file:
        rel = new_file.split('systemTest/performance/', 1)[-1]
        cells = b['per_file'].get(rel); before = rel in a['per_file']
        ok = cells is not None and not before and (new_n is None or len(cells) == new_n) and all(s == 'passed' for _, s in cells or [])
        t.check('C3', ok, 'the new suite %s: present after %s (%s cells, all passed %s) | absent before %s' % (
            os.path.basename(rel), cells is not None, len(cells or []), all(s == 'passed' for _, s in cells or []), not before))
    ctl = dict(b); ctl['fail_set'] = b['fail_set'] + ['fabricated.test.ts::gate74 planted red']
    t.check('C0', not set(ctl['fail_set']) <= set(a['fail_set']), 'CONTROL: a fabricated red added to `after` BREAKS the subset (the compare can fail)')
    return t


def onefile(wt, out):
    t = Tally()
    rc = npm_unit(wt, out, (NEW_REL,))
    d = parse_vitest_json(out)
    titles = [ti for cells in d['per_file'].values() for ti, _ in cells]
    t.check('O1', rc == 0 and d['tests'] == 3 and d['passed'] == 3 and d['files'] == 1, 'the new suite alone through `npm run test:unit`: rc %d, files %d, %d/%d passed' % (rc, d['files'], d['passed'], d['tests']))
    t.check('O2', all(sum(1 for ti in titles if ti.startswith(x)) == 1 for x in TITLES), 'each named cell present once: %s' % [(x, sum(1 for ti in titles if ti.startswith(x))) for x in TITLES])
    return t


def tamper(wt, arm, out):
    t = Tally(); f = os.path.join(wt, REPORT)
    raw = open(f, encoding='utf-8').read(); h0 = hashlib.sha256(raw.encode()).hexdigest()
    n = raw.count(ANCHOR)
    if not t.check('T0', n == 1, 'anchor count in report.ts == 1 BEFORE tampering: %d (a non-unique anchor would tamper the wrong line — :133/:135 carry similar text)' % n): return t
    new = TAMPERS[arm]
    try:
        open(f, 'w', encoding='utf-8').write(raw.replace(ANCHOR, new))
        tt = open(f, encoding='utf-8').read()
        t.check('T1', tt.count(new) == 1 and tt.count(ANCHOR) == 0, 'TAMPER LANDED (arm %s): new form 1, anchor 0' % arm)
        rc = npm_unit(wt, out, (NEW_REL,))
    finally:
        open(f, 'w', encoding='utf-8').write(raw)
    h1 = hashlib.sha256(open(f, 'rb').read()).hexdigest()
    st = subprocess.run(['git', '-C', wt, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout
    t.check('T2', h1 == h0 and not st.strip(), 'RESTORED: sha256 %s == pre-tamper %s; tracked modifications after: %r' % (h1[:16], h0[:16], st.strip()[:80]))
    d = parse_vitest_json(out)
    reds = [x.split('::', 1)[1] for x in d['fail_set']]
    t.check('T3', rc != 0 and d['tests'] == 3 and d['failed'] == 1 and d['passed'] == 2 and len(reds) == 1 and reds[0].startswith(TITLES[0]),
            'arm %s: rc %d, %d total, %d passed, %d failed, red = %s (want exactly RED F-3; both CONTROLs pass; 3 total, so NOT a load failure)' % (
                arm, rc, d['tests'], d['passed'], d['failed'], [r_[:40] for r_ in reds]))
    return t


def tsc(wt):
    t = Tally()
    for cfg in ('tsconfig.json', 'tsconfig.node.json'):
        p = subprocess.run(['npx', '--no-install', 'tsc', '-p', cfg, '--noEmit'], cwd=os.path.join(wt, PERF), capture_output=True, text=True, env=ENV)
        lines = [l for l in (p.stdout + p.stderr).split('\n') if l.strip()]
        t.check('K-%s' % cfg, p.returncode == 0 and not lines, 'tsc -p %s --noEmit: rc %d, %d output line(s) %s' % (cfg, p.returncode, len(lines), lines[:2]))
    return t


def fmt(wt, paths):
    t = Tally()
    p = subprocess.run(['bash', 'systemTest/scripts/check-package-format.sh'], cwd=wt, input='\n'.join(paths) + '\n', capture_output=True, text=True, env=ENV)
    out = p.stdout + p.stderr
    m = re.findall(r'(\d+) package\(s\) checked', out)
    n = int(m[-1]) if m else 0
    t.check('F1', p.returncode == 0 and n >= 1, 'format gate on the push list %s: rc %d, `%s package(s) checked` (0 checked is a FAIL) | SKIP lines %d' % (
        [os.path.basename(x) for x in paths], p.returncode, n, len(re.findall(r'(?i)\bSKIP\b', out))))
    return t, out


PF_VERDICT = re.compile(r'^(PREFLIGHT (?:PASSED|FAILED|INCOMPLETE)[^\n]*)', re.M)
PF_RAN = re.compile(r'\((\d+)/(\d+) legs ran\)|(\d+)/(\d+) legs ran')
PF_FAILED_LEGS = re.compile(r'PREFLIGHT FAILED on leg\(s\)\s*([0-9 ]+)')
PF_SHELL = re.compile(r'^shell suites: (\d+) passed, (\d+) failed, (\d+) skipped \(of (\d+)\)', re.M)
PF_FAILED_SUITE = re.compile(r'^FAILED: (\S+)', re.M)
PF_SKIPPED = re.compile(r'(\d+) SKIPPED')


def parse_preflight(text):
    v = PF_VERDICT.findall(text); r = PF_RAN.findall(text); fl = PF_FAILED_LEGS.findall(text); sh = PF_SHELL.findall(text)
    ran = None
    if r:
        x = r[-1]; ran = (int(x[0] or x[2]), int(x[1] or x[3]))
    return {'verdict': v[-1] if v else None, 'ran': ran, 'failed_legs': sorted(set(int(y) for y in (fl[-1].split() if fl else []))),
            'shell': [int(y) for y in sh[-1]] if sh else None, 'failed_suites': sorted(set(PF_FAILED_SUITE.findall(text))),
            'skipped': int(PF_SKIPPED.findall(v[-1])[0]) if v and PF_SKIPPED.findall(v[-1]) else 0,
            'mismatch_lines': len(re.findall(r'VERDICT: MISMATCH', text))}


def s1_missing(wt):
    miss = []
    dev = os.path.join(wt, 'Blockchain/Dev')
    if not os.path.isdir(os.path.join(dev, 'node_modules')): miss.append('Blockchain/Dev node_modules (npm ci --ignore-scripts)')
    if not os.path.isfile(os.path.join(dev, 'packages/shared/dist/index.js')): miss.append('packages/shared/dist/index.js (npm run build --workspace=packages/shared)')
    st = os.path.join(wt, 'systemTest')
    for p in sorted(os.listdir(st)):
        if os.path.isfile(os.path.join(st, p, 'package.json')) and not os.path.isdir(os.path.join(st, p, 'node_modules')):
            miss.append('systemTest/%s node_modules (npm ci --ignore-scripts)' % p)
    return miss


def preflight(wt, out):
    t = Tally()
    miss = s1_missing(wt)
    if miss: print('REFUSED (rc 12): S-1 not done in %s: %s' % (wt, miss)); sys.exit(12)
    script = ('. systemTest/slot-target.sh >/dev/null 2>&1 || true\n'
              'builtin pushd Blockchain/Dev >/dev/null || exit 1\n'
              'bash scripts/preflight/preflight.sh\n')
    p = subprocess.run(['bash', '-c', script], cwd=wt, capture_output=True, text=True, env=ENV)
    text = p.stdout + p.stderr
    open(out + '.console.txt', 'w').write(text)
    d = parse_preflight(text); d['rc'] = p.returncode
    json.dump(d, open(out, 'w'), indent=1)
    t.check('PF0', d['verdict'] is not None and d['ran'] is not None and d['shell'] is not None,
            'parsed: verdict %r | legs ran %s | shell %s (a None means the parser did not read the run — never a pass)' % (d['verdict'], d['ran'], d['shell']))
    t.info('PF1', 'rc %d | FAILED legs %s | SKIPPED %d | failed shell suites %s | MISMATCH lines %d' % (p.returncode, d['failed_legs'] or 'none', d['skipped'], d['failed_suites'] or 'none', d['mismatch_lines']))
    return t


def pfcmp(a, b):
    t = Tally()
    t.check('Q1', set(b['failed_legs']) <= set(a['failed_legs']), 'subject FAILED legs %s SUBSET of ref %s' % (b['failed_legs'], a['failed_legs']))
    t.check('Q2', set(b['failed_suites']) <= set(a['failed_suites']), 'subject failed shell suites %s SUBSET of ref %s' % (b['failed_suites'], a['failed_suites']))
    t.info('Q3', 'legs ran ref %s subject %s | shell ref %s subject %s (passed, failed, skipped, of)' % (a['ran'], b['ran'], a['shell'], b['shell']))
    ctl = dict(b); ctl['failed_legs'] = b['failed_legs'] + [99]
    t.check('Q0', not set(ctl['failed_legs']) <= set(a['failed_legs']), 'CONTROL: a fabricated failing leg 99 breaks the subset')
    return t


def leg14(wt):
    t = Tally()
    if not os.path.exists(os.path.join(wt, '.git')):
        print('REFUSED: %s is not a git work tree (no .git): the suite refuses an archive and scans 0 files — a FALSE red' % wt); sys.exit(2)
    p = subprocess.run(['bash', 'systemTest/__tests__/no_hardcoded_slot_literals.test.sh'], cwd=wt, capture_output=True, text=True,
                       env={'HOME': os.environ.get('HOME', ''), 'PATH': os.environ.get('PATH', ''), 'TMPDIR': '/tmp'})
    out = p.stdout + p.stderr
    m = re.findall(r'no_hardcoded_slot_literals: (\d+) passed, (\d+) failed', out); sc = re.findall(r'scanned (\d+) files', out)
    ctl = 'POSITIVE CONTROL: a planted literal is found' in out
    bl = os.path.join(wt, K['leg14']['file']); txt = open(bl, encoding='utf-8').read() if os.path.isfile(bl) else None; n2 = sum(1 for l in txt.split('\n') if 'slot2' in l) if txt is not None else -1; o2 = txt.count('slot2') if txt is not None else -1
    pas, fai = (int(m[-1][0]), int(m[-1][1])) if m else (None, None)
    t.check('L1', m and sc and ctl and int(sc[-1]) > 0, 'parsed: %s passed, %s failed, rc %d | scanned %s files | planted-literal CONTROL ran: %s' % (pas, fai, p.returncode, sc[-1] if sc else None, ctl))
    t.info('L2', 'leg-14 suite at this tree: %s | LINES containing `slot2` in %s: %d (%d occurrences) (KS-1450: 0 lines before #1424, 8 lines / 14 occurrences after)' % (
        'GREEN' if fai == 0 and p.returncode == 0 else 'RED', os.path.basename(bl), n2, o2))
    return t


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    # CAPTURED real lines (drafter runs, verbatim)
    head_pf = ('shell suites: 71 passed, 0 failed, 0 skipped (of 71)\nshell suites wall-clock: 302s\n'
               'PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.\n')
    r14_pf = ('shell suites: 70 passed, 1 failed, 0 skipped (of 71)\nFAILED: systemTest/__tests__/no_hardcoded_slot_literals.test.sh\n'
              'shell suites wall-clock: 313s\nPREFLIGHT FAILED on leg(s) 14 - fix the above before pushing. (12/15 legs ran)\n')
    a = parse_preflight(head_pf); b = parse_preflight(r14_pf)
    rep(a['ran'] == (12, 15) and a['shell'] == [71, 0, 0, 71] and a['failed_legs'] == [] and a['skipped'] == 3, 'parse CAPTURED head preflight (drafter 16:47Z): %s' % a)
    rep(b['ran'] == (12, 15) and b['failed_legs'] == [14] and b['failed_suites'] == ['systemTest/__tests__/no_hardcoded_slot_literals.test.sh'], 'parse CAPTURED R 14th leg-14 refusal: %s' % b)
    rep(parse_preflight('nothing here')['verdict'] is None, 'parse of an EMPTY/foreign console reads None (PF0 then FAILS — never a pass)')
    t = pfcmp(b, b); rep(not t.fails, 'pfcmp develop-shaped vs itself: subset holds')
    t = pfcmp(a, b); rep('Q1' in t.fails and 'Q2' in t.fails, 'pfcmp PLANTED: a subject failing leg 14 against a clean ref: Q1 + Q2 FAIL')
    base = {'files': 75, 'tests': 1360, 'passed': 1360, 'failed': 0, 'pending': 0, 'fail_set': [], 'per_file': {}}
    head = {'files': 76, 'tests': 1363, 'passed': 1363, 'failed': 0, 'pending': 0, 'fail_set': [], 'per_file': {NEW_REL: [(TITLES[0], 'passed'), (TITLES[1], 'passed'), (TITLES[2], 'passed')]}}
    t = perfcmp(base, head, NEW_FILE, 3); rep(not t.fails, 'perfcmp CAPTURED base 1360 -> head 1363 (+1 file): GREEN')
    bad = json.loads(json.dumps(head)); bad['fail_set'] = ['x.test.ts::new red']
    t = perfcmp(base, bad, NEW_FILE, 3); rep('C1' in t.fails, 'perfcmp PLANTED a new red at head: C1 FAILS')
    t = perfcmp(head, head, NEW_FILE, 3); rep('C3' in t.fails, 'perfcmp PLANTED the new suite ALREADY present before: C3 FAILS')
    rep(len(set(TAMPERS.values())) == 3 and all(ANCHOR != v for v in TAMPERS.values()), 'three distinct tamper arms, none equal to the anchor')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    mode = A[0] if A else ''
    wt, tree, out = opt(A, '--wt'), opt(A, '--expect-tree'), opt(A, '--out')
    if mode in ('perf', 'onefile', 'tamper', 'tsc', 'format', 'preflight', 'leg14'):
        bind(wt, tree)
    if mode == 'perf':
        rc = npm_unit(wt, out); d = parse_vitest_json(out); t = Tally()
        t.check('U1', d['tests'] > 0 and d['files'] > 0, 'parsed %s: files %d tests %d passed %d failed %d pending %d (rc %d)' % (os.path.basename(out), d['files'], d['tests'], d['passed'], d['failed'], d['pending'], rc))
        t.info('U2', 'failing SET %s' % (d['fail_set'][:8] or 'empty'))
        return t.end()
    if mode == 'perfcmp':
        return perfcmp(parse_vitest_json(opt(A, '--a')), parse_vitest_json(opt(A, '--b')), opt(A, '--new-file'), int(opt(A, '--new-tests')) if opt(A, '--new-tests') else None).end()
    if mode == 'onefile': return onefile(wt, out).end()
    if mode == 'tamper':
        arm = opt(A, '--arm')
        if arm not in TAMPERS: print('REFUSED: --arm must be one of %s' % sorted(TAMPERS)); return 2
        return tamper(wt, arm, out).end()
    if mode == 'tsc': return tsc(wt).end()
    if mode == 'format':
        paths = [p for p in (opt(A, '--paths') or '').split(',') if p]
        if not paths: print('REFUSED: --paths is REQUIRED (the push changed list)'); return 2
        t, o = fmt(wt, paths); print(o[-1500:]); return t.end()
    if mode == 'preflight': return preflight(wt, out).end()
    if mode == 'pfcmp': return pfcmp(json.load(open(opt(A, '--a'))), json.load(open(opt(A, '--b')))).end()
    if mode == 'leg14': return leg14(wt).end()
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
