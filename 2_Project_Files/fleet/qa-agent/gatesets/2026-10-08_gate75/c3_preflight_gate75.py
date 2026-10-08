#!/usr/bin/env python3
r"""c3_preflight_gate75.py — the preflight, the format gate and the baseline's consumer for gate75 (#1426 KS-1450).
The parser, S-1 detector, preflight runner, pfcmp and format modes are CARRIED from c3_suites_gate74.py (gate74 kit.json script_sha256
e8227d57ced4…) with their CAPTURED-line self-tests; the vitest modes are dropped (#1426 touches no vitest suite) and a `baseline` mode is
added (jq -e plus scripts/runner/baseline_gate.py's own loader, the baseline's REAL consumer).

EVERY worktree is YOURS, outside !CODING (refused otherwise), and is BOUND: `--expect-tree <40-hex>` must equal HEAD^{tree} (rc 11).
TMPDIR is forced to /tmp for every child (Q-X9 carried).

MODES
  preflight --wt W --expect-tree T --out J  the WHOLE preflight as the hook invokes it (source systemTest/slot-target.sh at the root, then
                                            Blockchain/Dev/scripts/preflight/preflight.sh). Requires S-1 (rc 12 naming what is missing).
                                            Parsed into J: verdict, legs ran/of, SKIPPED, FAILED legs, `shell suites:` tuple, FAILED suites.
  pfcmp     --a J_ref --b J_subject         subject's FAILED legs and failed shell suites each a SUBSET of the ref's (CONTROL: a fabricated
                                            leg 99 breaks it).
  format    --wt W --expect-tree T --paths P1,P2,..   the pre-push format gate fed the push list on stdin (0 checked is a FAIL).
  baseline  --wt W --expect-tree T [--ref-wt W2 --ref-tree T2]
                                            `jq -e .` on the baseline (CONTROL: a 1-byte-broken COPY must read rc != 0); then
                                            baseline_gate.py's loader (imported by path, registered in sys.modules BEFORE exec_module —
                                            R 16th's lesson 10) on W and, if given, W2: entry count, key-set equality, entries that differ
                                            and which FIELDS differ.
  --selftest                                parsers on CAPTURED real lines.
rc 0 PASS / 1 FAIL / 2 refused / 11 not the pinned tree / 12 S-1 not done."""
import importlib.util, json, os, re, shutil, subprocess, sys, tempfile

FORBIDDEN = '/Volumes/DevMASTER/!CODING'
BASELINE = 'systemTest/schemathesis/config/schemathesis-baseline.json'
GATE_PY = 'systemTest/schemathesis/scripts/runner/baseline_gate.py'
ENV = dict(os.environ); ENV.pop('GIT_SSH_COMMAND', None); ENV['TMPDIR'] = '/tmp'


def opt(A, k, d=None):
    return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d


class Tally:
    def __init__(self): self.n = 0; self.fails = []
    def check(self, cid, ok, msg):
        self.n += 1; print('%s %s %s' % ('PASS' if ok else 'FAIL', cid, msg))
        if not ok: self.fails.append(cid)
    def info(self, cid, msg): print('INFO %s %s' % (cid, msg))
    def end(self):
        print('CHECKED %d' % self.n); print('%d FAIL%s' % (len(self.fails), (' (' + ' '.join(self.fails) + ')') if self.fails else ''))
        if self.n == 0: print('FAIL: 0 checked'); return 1
        return 1 if self.fails else 0


def under_forbidden(p):
    return any(q == FORBIDDEN or q.startswith(FORBIDDEN + '/') for q in (os.path.abspath(p), os.path.realpath(p)))


def bind(wt, tree):
    if not (wt and tree): raise SystemExit('REFUSED: --wt and --expect-tree are REQUIRED')
    if under_forbidden(wt): print('REFUSED: --wt %s is under %s — use YOUR worktree in YOUR clone' % (wt, FORBIDDEN)); sys.exit(2)
    p = subprocess.run(['git', '-C', wt, 'rev-parse', 'HEAD^{tree}'], capture_output=True, text=True)
    if p.returncode != 0 or p.stdout.strip() != tree:
        print('REFUSED (rc 11): worktree %s HEAD^{tree} %r != --expect-tree %s' % (wt, p.stdout.strip()[:12], tree[:12])); sys.exit(11)
    st = subprocess.run(['git', '-C', wt, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout
    if st.strip(): print('REFUSED (rc 11): worktree %s has tracked modifications:\n%s' % (wt, st[:400])); sys.exit(11)
    print('BOUND: %s HEAD^{tree} == %s, 0 tracked modifications' % (wt, tree[:12]))


PF_VERDICT = re.compile(r'^(PREFLIGHT (?:PASSED|FAILED|INCOMPLETE)[^\n]*)', re.M)
PF_RAN = re.compile(r'\((\d+)/(\d+) legs ran\)|(\d+)/(\d+) legs ran')
PF_FAILED_LEGS = re.compile(r'PREFLIGHT FAILED on leg\(s\)\s*([0-9 ]+)')
PF_SHELL = re.compile(r'^shell suites: (\d+) passed, (\d+) failed, (\d+) skipped \(of (\d+)\)', re.M)
PF_FAILED_SUITE = re.compile(r'^FAILED: (\S+)', re.M)
PF_SKIPPED = re.compile(r'(\d+) SKIPPED')
PF_SKIPLEGS = re.compile(r'^\s*legs? ([0-9 ]+?) — ', re.M)
PF_LEG14 = re.compile(r'no_hardcoded_slot_literals: (\d+) passed, (\d+) failed')


def parse_preflight(text):
    v = PF_VERDICT.findall(text); r = PF_RAN.findall(text); fl = PF_FAILED_LEGS.findall(text); sh = PF_SHELL.findall(text)
    ran = None
    if r: x = r[-1]; ran = (int(x[0] or x[2]), int(x[1] or x[3]))
    sl = PF_SKIPLEGS.findall(text); l14 = PF_LEG14.findall(text)
    return {'verdict': v[-1] if v else None, 'ran': ran, 'failed_legs': sorted(set(int(y) for y in (fl[-1].split() if fl else []))),
            'shell': [int(y) for y in sh[-1]] if sh else None, 'failed_suites': sorted(set(PF_FAILED_SUITE.findall(text))),
            'skipped': int(PF_SKIPPED.findall(v[-1])[0]) if v and PF_SKIPPED.findall(v[-1]) else 0,
            'skipped_legs': sorted(set(int(y) for y in sl[-1].split())) if sl else [],
            'leg14_line': [int(a) for a in l14[-1]] if l14 else None,
            'fail_lines': len(re.findall(r'^FAIL', text, re.M)),
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
    t = Tally(); miss = s1_missing(wt)
    if miss: print('REFUSED (rc 12): S-1 not done in %s: %s' % (wt, miss)); sys.exit(12)
    script = ('. systemTest/slot-target.sh >/dev/null 2>&1 || true\n'
              'builtin pushd Blockchain/Dev >/dev/null || exit 1\n'
              'bash scripts/preflight/preflight.sh\n')
    p = subprocess.run(['bash', '-c', script], cwd=wt, capture_output=True, text=True, env=ENV)
    open(out + '.stdout.txt', 'w').write(p.stdout); open(out + '.stderr.txt', 'w').write(p.stderr)
    text = p.stdout + p.stderr
    d = parse_preflight(text); d['rc'] = p.returncode
    json.dump(d, open(out, 'w'), indent=1)
    t.check('PF0', d['verdict'] is not None and d['ran'] is not None and d['shell'] is not None,
            'parsed: verdict %r | legs ran %s | shell %s (a None means the parser did not read the run — never a pass)' % (d['verdict'], d['ran'], d['shell']))
    t.info('PF1', 'rc %d | FAILED legs %s | SKIPPED %d %s | failed shell suites %s | leg-14 line %s | ^FAIL lines %d | MISMATCH lines %d' % (
        p.returncode, d['failed_legs'] or 'none', d['skipped'], d['skipped_legs'], d['failed_suites'] or 'none', d['leg14_line'], d['fail_lines'], d['mismatch_lines']))
    return t


def pfcmp(a, b):
    t = Tally()
    t.check('Q1', set(b['failed_legs']) <= set(a['failed_legs']), 'subject FAILED legs %s SUBSET of ref %s' % (b['failed_legs'], a['failed_legs']))
    t.check('Q2', set(b['failed_suites']) <= set(a['failed_suites']), 'subject failed shell suites %s SUBSET of ref %s' % (b['failed_suites'], a['failed_suites']))
    t.info('Q3', 'legs ran ref %s subject %s | shell ref %s subject %s (passed, failed, skipped, of)' % (a['ran'], b['ran'], a['shell'], b['shell']))
    ctl = dict(b); ctl['failed_legs'] = b['failed_legs'] + [99]
    t.check('Q0', not set(ctl['failed_legs']) <= set(a['failed_legs']), 'CONTROL: a fabricated failing leg 99 breaks the subset')
    return t


def fmt(wt, paths):
    t = Tally()
    p = subprocess.run(['bash', 'systemTest/scripts/check-package-format.sh'], cwd=wt, input='\n'.join(paths) + '\n', capture_output=True, text=True, env=ENV)
    out = p.stdout + p.stderr
    m = re.findall(r'(\d+) package\(s\) checked', out); n = int(m[-1]) if m else 0
    t.check('F1', p.returncode == 0, 'format gate on the push list %s: rc %d, `%s package(s) checked` | SKIP lines %d | NOTHING CHECKED lines %d' % (
        [os.path.basename(x) for x in paths], p.returncode, n, len(re.findall(r'(?i)\bSKIP\b', out)), len(re.findall(r'NOTHING CHECKED', out))))
    t.info('F2', 'a push list with NO package path may legitimately check 0 packages: quote the gate\'s own words, never read 0 as clean')
    return t, out


def load_gate(wt):
    path = os.path.join(wt, GATE_PY)
    name = 'g75_baseline_gate_%d' % abs(hash(wt))
    spec = importlib.util.spec_from_file_location(name, path); mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # BEFORE exec_module: @dataclass needs it (R 16th lesson 10)
    spec.loader.exec_module(mod)
    return mod


def baseline(wt, ref):
    t = Tally(); bl = os.path.join(wt, BASELINE)
    p = subprocess.run(['jq', '-e', '.', bl], capture_output=True, text=True)
    tmpd = tempfile.mkdtemp(prefix='g75_jqctl_'); broken = os.path.join(tmpd, 'broken.json')
    raw = open(bl, 'rb').read(); open(broken, 'wb').write(raw[:-3])
    q = subprocess.run(['jq', '-e', '.', broken], capture_output=True, text=True)
    t.check('B1', p.returncode == 0 and q.returncode != 0, 'jq -e . on the baseline rc %d | CONTROL a 3-byte-truncated COPY rc %d (must be != 0)' % (p.returncode, q.returncode))
    mod = load_gate(wt)
    fn = getattr(mod, 'load_baseline', None)
    t.check('B2', callable(fn), '%s exposes load_baseline: %s' % (GATE_PY, callable(fn)))
    if not callable(fn): return t
    import inspect
    t.info('B2s', 'load_baseline%s' % str(inspect.signature(fn)))
    import pathlib
    cur = fn(pathlib.Path(bl))
    def as_map(x):
        if isinstance(x, dict): return x
        if hasattr(x, 'entries'): x = x.entries
        if isinstance(x, dict): return x
        return {getattr(e, 'key', i): e for i, e in enumerate(x)}
    cm = as_map(cur); t.check('B3', len(cm) > 0, 'load_baseline on %s: %d entries' % (wt, len(cm)))
    if ref:
        rbl = os.path.join(ref, BASELINE); rmod = load_gate(ref); rm = as_map(rmod.load_baseline(pathlib.Path(rbl)))
        same_keys = set(rm) == set(cm)
        diff = sorted(k for k in cm if k in rm and repr(cm[k]) != repr(rm[k]))
        fields = set()
        for k in diff:
            a, b = rm[k], cm[k]
            da = a if isinstance(a, dict) else getattr(a, '__dict__', {}); db = b if isinstance(b, dict) else getattr(b, '__dict__', {})
            fields |= {f for f in set(da) | set(db) if da.get(f) != db.get(f)}
        t.check('B4', same_keys, 'ref %d entries vs subject %d; identical key set %s' % (len(rm), len(cm), same_keys))
        t.info('B5', 'entries that differ: %d %s | fields that differ: %s' % (len(diff), [str(k)[:60] for k in diff], sorted(fields)))
    return t


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    head_pf = ('no_hardcoded_slot_literals: 11 passed, 0 failed\nshell suites: 71 passed, 0 failed, 0 skipped (of 71)\nshell suites wall-clock: 346s\n\n'
               'PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.\n  legs 3 4 8 — local stack not up; you can clear this by starting it.\n')
    dev_pf = ('shell suites: 70 passed, 1 failed, 0 skipped (of 71)\nFAILED: systemTest/__tests__/no_hardcoded_slot_literals.test.sh\n'
              'shell suites wall-clock: 313s\nPREFLIGHT FAILED on leg(s) 14 - fix the above before pushing. (12/15 legs ran)\n')
    a = parse_preflight(head_pf); b = parse_preflight(dev_pf)
    rep(a['ran'] == (12, 15) and a['shell'] == [71, 0, 0, 71] and a['failed_legs'] == [] and a['skipped'] == 3 and a['skipped_legs'] == [3, 4, 8] and a['leg14_line'] == [11, 0],
        'parse CAPTURED R 16th head preflight (READY mail): %s' % a)
    rep(b['ran'] == (12, 15) and b['failed_legs'] == [14] and b['failed_suites'] == ['systemTest/__tests__/no_hardcoded_slot_literals.test.sh'], 'parse CAPTURED develop-shaped leg-14 refusal: %s' % b)
    rep(parse_preflight('nothing here')['verdict'] is None, 'parse of an EMPTY/foreign console reads None (PF0 then FAILS)')
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()): t1 = pfcmp(b, a); t2 = pfcmp(a, b)
    rep(not t1.fails, 'pfcmp head-shaped subject vs develop-shaped ref: subset holds (leg 14 leaves the failing set)')
    rep('Q1' in t2.fails and 'Q2' in t2.fails, 'pfcmp PLANTED a subject failing leg 14 against a clean ref: Q1 + Q2 FAIL')
    rep(under_forbidden('/Volumes/DevMASTER/!CODING/x') and not under_forbidden('/private/tmp/x'), 'the !CODING refusal')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    mode = A[0] if A else ''
    wt, tree, out = opt(A, '--wt'), opt(A, '--expect-tree'), opt(A, '--out')
    if mode in ('preflight', 'format', 'baseline'): bind(wt, tree)
    if mode == 'preflight':
        if not out: print('REFUSED: --out is REQUIRED'); return 2
        return preflight(wt, out).end()
    if mode == 'pfcmp': return pfcmp(json.load(open(opt(A, '--a'))), json.load(open(opt(A, '--b')))).end()
    if mode == 'format':
        paths = [p for p in (opt(A, '--paths') or '').split(',') if p]
        if not paths: print('REFUSED: --paths is REQUIRED'); return 2
        t, o = fmt(wt, paths); print(o[-1500:]); return t.end()
    if mode == 'baseline':
        ref = opt(A, '--ref-wt')
        if ref: bind(ref, opt(A, '--ref-tree'))
        return baseline(wt, ref).end()
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
