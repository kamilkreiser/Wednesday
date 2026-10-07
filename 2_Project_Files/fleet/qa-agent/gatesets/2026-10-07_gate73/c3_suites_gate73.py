#!/usr/bin/env python3
r"""c3_suites_gate73.py — each row's OWN suites, re-run by the gate in ITS OWN pinned worktrees, base AND head, ONE parser for both.

  run   --pr R --wt W --label base|head --out DIR [--ids K1,K2] [--skip-heavy] [--system-tmp V2,...]
        runs the row's command table (SUITES below) in W, each command's stdout / stderr / rc in SEPARATE files under DIR, counts parsed
        by ONE parser per runner kind (shell summary line / vitest JSON report / jest JSON report / tsc rc+bytes / list count) — never by
        a human-output regex where the runner can write JSON (KS-1313's own lesson). Prints `want` beside `got` per label; a missing
        report or 0 executed is LOADFAIL, never a pass. Heavy ids (whole-package / whole-set runs) run unless --skip-heavy.
  arm   --pr R --wt W --repo C --swap p1[,p2] (--swap-rev REV | --old ANCHOR --new TEXT) --id K --out DIR --tag T
        RED-FIRST / mutation arm on a SWAP: the named path(s) in W are replaced by their blobs at REV (from YOUR clone C), the
        command K runs, the head blobs are RESTORED, and the restore is ASSERTED (sha256 per path == the head blob; `git status
        --porcelain` empty). The swap is asserted LANDED before the result is read (sha changed).
  compare --base-report B.json --head-report H.json   head failing SET a SUBSET of base's (CONTROL planted extra fails); passed delta.
  table --pr R            print the row's command table (id, cwd, command, want base / head, heavy, X1 needed).
W must be a worktree of YOUR clone at that row's head (or the base), with X1 installed where the table says so.
rc 0 every non-INFO command == want / 1 a mismatch or LOADFAIL / 2 refused."""
import hashlib, json, os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate73 import K, ROWS, BASE, Tally, git_bytes, opt, row_arg

# kind: shell (name: P passed, F failed) | vitest (--reporter=json) | jest (--json) | tsc (rc 0 and 0 bytes) | list (non-empty lines)
# want: {'base': (passed, failed) | int | None, 'head': ...}; None = INFO (printed, never asserted). X1 = needs installed deps.
SUITES = {
 '1407': [
  ('K1', '.', ['bash', 'systemTest/__tests__/ks998_format_gate_push_label_is_literal.test.sh'], 'shell', 'ks998_format_gate_push_label_is_literal', {'base': None, 'head': (8, 0)}, False, False),
  ('K2', '.', ['bash', 'systemTest/__tests__/package_format_gate.test.sh'], 'shell', 'package_format_gate', {'base': (33, 0), 'head': (33, 0)}, False, False),
  ('K3', '.', ['bash', 'Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh'], 'shell', None, {'base': (28, 0), 'head': (28, 0)}, False, False),
  ('K4', '.', ['bash', 'Blockchain/Dev/scripts/__tests__/pre_push_hook_current_develop.test.sh'], 'shell', None, {'base': (4, 0), 'head': (4, 0)}, False, False),
  ('K5', '.', ['bash', 'systemTest/__tests__/html_docs_matrix.test.sh'], 'shell', None, {'base': (12, 0), 'head': (12, 0)}, False, False),
  ('K6', '.', ['bash', 'Blockchain/Dev/scripts/run-shell-suites.sh', '--list'], 'list', None, {'base': 70, 'head': 71}, False, False),
  ('K7', '.', ['bash', '-n', 'systemTest/scripts/check-package-format.sh'], 'tsc', None, {'base': 0, 'head': 0}, False, False),
  ('K8', '.', ['bash', '-n', 'systemTest/__tests__/ks998_format_gate_push_label_is_literal.test.sh'], 'tsc', None, {'base': None, 'head': 0}, False, False),
  ('K9', '.', ['bash', 'Blockchain/Dev/scripts/run-shell-suites.sh'], 'shellset', None, {'base': (70, 0), 'head': (71, 0)}, True, True),
 ],
 '1409': [
  ('V1', 'systemTest/performance', ['npx', '--no-install', 'vitest', 'run', '--config', 'vitest.unit.config.ts', 'tests/unit/utils/unitSuiteSlotIndependence.test.ts'], 'vitest', None, {'base': None, 'head': None}, False, True),
  ('V2', 'systemTest/performance', ['npx', '--no-install', 'vitest', 'run', '--config', 'vitest.unit.config.ts'], 'vitest', None, {'base': (1353, 0), 'head': (1360, 0)}, True, True),
  ('V3', 'systemTest/performance', ['npx', '--no-install', 'tsc', '--noEmit', '-p', 'tsconfig.node.json'], 'tsc', None, {'base': 0, 'head': 0}, False, True),
  ('V4', 'systemTest/performance', ['npx', '--no-install', 'eslint', '--config', 'eslint.config.js', 'tests/unit/utils/unitSuiteSlotIndependence.test.ts'], 'tsc', None, {'base': 0, 'head': 0}, False, True),
  ('V5', 'systemTest/performance', ['npx', '--no-install', 'prettier', '--check', 'tests/unit/utils/unitSuiteSlotIndependence.test.ts'], 'tscrc', None, {'base': 0, 'head': 0}, False, True),
 ],
 '1408': [
  ('T1', 'Blockchain/Dev/services/transfer', ['npx', '--no-install', 'vitest', 'run', 'src/__tests__/transfer.test.ts'], 'vitest', None, {'base': (52, 0), 'head': (55, 0)}, False, True),
  ('T2', 'Blockchain/Dev/services/transfer', ['npx', '--no-install', 'vitest', 'run', '-t', 'TRC1', 'src/__tests__/transfer.test.ts'], 'vitest', None, {'base': None, 'head': (1, 0)}, False, True),
  ('T3', 'Blockchain/Dev/services/transfer', ['npx', '--no-install', 'vitest', 'run'], 'vitest', None, {'base': (76, 0), 'head': (79, 0)}, True, True),
  ('T4', 'Blockchain/Dev/services/transfer', ['npx', '--no-install', 'tsc', '--noEmit', '-p', '.'], 'tsc', None, {'base': 0, 'head': 0}, False, True),
 ],
 '1410': [
  ('J1', 'Blockchain/Dev/services/originate', ['npx', '--no-install', 'jest', 'src/__tests__/ks591-transfer-custody-new-holder-id-is-a-uuid.test.ts'], 'jest', None, {'base': None, 'head': (3, 0)}, False, True),
  ('J2', 'Blockchain/Dev/services/originate', ['npx', '--no-install', 'jest'], 'jest', None, {'base': (1074, 0), 'head': (1077, 0)}, True, True),
  ('J3', 'Blockchain/Dev/services/originate', ['npx', '--no-install', 'tsc', '--noEmit', '-p', '.'], 'tsc', None, {'base': 0, 'head': 0}, False, True),
  # J4 = `npm run check:openapi` split into its two legs and run WITHOUT the tsx CLI: the CLI opens an IPC socket under $TMPDIR, and a
  # scratchpad TMPDIR makes the socket path exceed macOS's 104-byte sun_path (measured 2026-10-07: `listen EINVAL … tsx-501/464.pipe`).
  # `node --import tsx` is the same loader without the IPC server. packages/shared must be BUILT first (the npm script builds it).
  ('J4a', 'Blockchain/Dev', ['node', '--import', 'tsx', 'scripts/generate-openapi.ts', '--check'], 'tscrc', None, {'base': 0, 'head': 0}, False, True),
  ('J4b', 'Blockchain/Dev', ['node', 'scripts/spec-examples/check-spec-examples.mjs'], 'tscrc', None, {'base': 0, 'head': 0}, False, True),
 ],
}


def sh(cmd, cwd, env, out_prefix):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, env=env)
    open(out_prefix + '.stdout', 'wb').write(p.stdout); open(out_prefix + '.stderr', 'wb').write(p.stderr)
    open(out_prefix + '.rc', 'w').write('%d\n' % p.returncode)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def parse(kind, name, rc, o, e, rep):
    """-> (got, detail). ONE parser per kind, the same for base and head."""
    if kind == 'shell':
        ms = re.findall(r'^\s*(?:(\S+): )?(\d+) passed, (\d+) failed\s*$', o, re.M)
        ms = [m for m in ms if name is None or m[0] == name]
        if len(ms) != 1: return 'LOADFAIL', 'summary lines matched %d (want 1) rc %d' % (len(ms), rc)
        return (int(ms[0][1]), int(ms[0][2])), 'rc %d' % rc
    if kind == 'shellset':
        m = re.search(r'shell suites: (\d+) passed, (\d+) failed, (\d+) skipped \(of (\d+)\)', o + e)
        if not m: return 'LOADFAIL', 'no `shell suites:` verdict line rc %d' % rc
        return (int(m.group(1)), int(m.group(2))), 'rc %d skipped %s of %s: %s' % (rc, m.group(3), m.group(4), m.group(0))
    if kind in ('vitest', 'jest'):
        if not os.path.exists(rep) or os.path.getsize(rep) == 0: return 'LOADFAIL', 'no JSON report written (rc %d) — 0 executed is never a pass' % rc
        j = json.load(open(rep))
        p, f = j.get('numPassedTests'), j.get('numFailedTests')
        if not isinstance(p, int) or not isinstance(f, int) or (p + f == 0 and j.get('numPendingTests', 0) == 0):
            return 'LOADFAIL', 'report carries no counts / 0 executed (rc %d)' % rc
        fails = [a.get('fullName') or a.get('title') for s in j.get('testResults', []) for a in s.get('assertionResults', []) if a.get('status') == 'failed']
        return (p, f), 'rc %d suites %s/%s pending %s todo %s%s' % (rc, j.get('numPassedTestSuites'), j.get('numTotalTestSuites'), j.get('numPendingTests'),
                                                                     j.get('numTodoTests'), (' FAILED: %s' % fails[:6]) if fails else '')
    if kind == 'tsc':
        return (0 if rc == 0 and len(o.strip()) == 0 else rc or 1), 'rc %d, %d stdout bytes' % (rc, len(o.strip()))
    if kind == 'tscrc':
        return rc, 'rc %d (%s)' % (rc, (o + e).strip().split('\n')[-1][:160] if (o + e).strip() else 'no output')
    if kind == 'list':
        n = len([l for l in o.split('\n') if l.strip()])
        return n if rc == 0 else 'LOADFAIL', 'rc %d, %d listed' % (rc, n)
    raise ValueError(kind)


SYSTEM_TMP = set()


def run_one(entry, wt, label, out, tag=None):
    cid, cwd, cmd, kind, name, want, heavy, x1 = entry
    os.makedirs(out, exist_ok=True); tmp = os.path.join(out, 'tmp'); os.makedirs(tmp, exist_ok=True)
    pre = os.path.join(out, '%s_%s%s' % (label, cid, ('_' + tag) if tag else ''))
    rep = pre + '.report.json'; cmd = list(cmd)
    if kind == 'vitest': cmd += ['--reporter=default', '--reporter=json', '--outputFile.json=' + rep]
    if kind == 'jest': cmd += ['--json', '--outputFile=' + rep]
    env = dict(os.environ, TMPDIR=tmp, CI='1'); env.pop('GIT_SSH_COMMAND', None)
    if cid in SYSTEM_TMP:
        # NAMED EXCEPTION (--system-tmp): suites that spawn the tsx CLI need a TMPDIR short enough for its IPC socket (macOS sun_path
        # 104 B); a scratchpad TMPDIR fails 26 perf cells at base AND head identically (measured 2026-10-07). The caller opted in BY ID.
        env.pop('TMPDIR', None); print('NOTE %s runs with the SYSTEM TMPDIR (--system-tmp, named exception)' % cid)
    rc, o, e = sh(cmd, os.path.join(wt, cwd), env, pre)
    got, detail = parse(kind, name, rc, o, e, rep)
    return got, detail, ' '.join(cmd), pre


def run(r, wt, label, out, ids=None, skip_heavy=False):
    t = Tally()
    for entry in SUITES[r]:
        cid, cwd, cmd, kind, name, want, heavy, x1 = entry
        if ids and cid not in ids: continue
        if heavy and skip_heavy: t.info(cid, 'NOT RUN (--skip-heavy): %s — NOT RUN is never a pass' % ' '.join(cmd)); continue
        got, detail, full, pre = run_one(entry, wt, label, out)
        w = want.get(label)
        if w is None: t.info(cid, '%s @%s: got %s (%s) [INFO: no assertion for %s]' % (' '.join(cmd), label, got, detail, label))
        else: t.check(cid, got == (tuple(w) if isinstance(w, (list, tuple)) else w), '%s @%s: got %s want %s (%s) [files %s.*]' % (' '.join(cmd), label, got, w, detail, os.path.basename(pre)))
    return t.end()


def porcelain(wt):
    return subprocess.run(['git', '-C', wt, 'status', '--porcelain'], capture_output=True, text=True).stdout.strip()


def arm(r, wt, repo, swaps, rev, cid, out, tag, old=None, new=None):
    """rev given: each swap path takes its blob at rev.  old/new given (one path): a MUTATION — the anchor `old` must occur EXACTLY
    once, is replaced by `new`, and the replacement is asserted present before the result is read."""
    t = Tally(); entry = [e for e in SUITES[r] if e[0] == cid]
    if len(entry) != 1: print('REFUSED: no command %s in row %s' % (cid, r)); return 2
    if porcelain(wt): print('REFUSED: %s is not clean before the arm:\n%s' % (wt, porcelain(wt))); return 2
    before = {p: hashlib.sha256(open(os.path.join(wt, p), 'rb').read()).hexdigest() for p in swaps}
    if old is not None:
        if len(swaps) != 1: print('REFUSED: a mutation arm takes exactly one path'); return 2
        fp = os.path.join(wt, swaps[0]); src = open(fp, 'rb').read(); n = src.count(old.encode())
        if n != 1: print('REFUSED: the mutation anchor occurs %d time(s) in %s (want exactly 1)' % (n, swaps[0])); return 2
        open(fp, 'wb').write(src.replace(old.encode(), new.encode(), 1))
        after = {swaps[0]: hashlib.sha256(open(fp, 'rb').read()).hexdigest()}
        landed = after[swaps[0]] != before[swaps[0]] and open(fp, 'rb').read().count(new.encode()) >= 1
        t.check('A0', landed, 'MUTATION LANDED in %s: anchor x1 replaced, sha changed %s' % (os.path.basename(swaps[0]), landed))
    else:
        for p in swaps: open(os.path.join(wt, p), 'wb').write(git_bytes(repo, rev, p))
        after = {p: hashlib.sha256(open(os.path.join(wt, p), 'rb').read()).hexdigest() for p in swaps}
        landed = all(before[p] != after[p] and after[p] == hashlib.sha256(git_bytes(repo, rev, p)).hexdigest() for p in swaps)
        t.check('A0', landed, 'SWAP LANDED: %s now == %s blobs (sha changed %s)' % ([os.path.basename(p) for p in swaps], rev[:12], landed))
    try:
        got, detail, full, pre = run_one(entry[0], wt, 'arm', out, tag)
        t.info('A1', 'ARM %s (%s -> %s): %s => got %s (%s)' % (tag, [os.path.basename(p) for p in swaps], (rev or 'MUTATION')[:12], full, got, detail))
    finally:
        for p in swaps:
            # restore the HEAD blob of the worktree (HEAD is the row head the worktree was added at)
            hb = subprocess.run(['git', '-C', wt, 'show', 'HEAD:' + p], capture_output=True).stdout
            open(os.path.join(wt, p), 'wb').write(hb)
        rest = {p: hashlib.sha256(open(os.path.join(wt, p), 'rb').read()).hexdigest() for p in swaps}
        t.check('A2', rest == before and porcelain(wt) == '', 'RESTORED sha256-identical %s; porcelain empty %s' % (rest == before, porcelain(wt) == ''))
    print('ARM RESULT %s %s' % (tag, got))
    return t.end()


def main():
    A = sys.argv[1:]; mode = A[0] if A else ''
    if mode == 'compare':
        # failing-SET comparison of one id's JSON reports: head's failing set must be a SUBSET of base's (never equality), and the
        # passed delta is printed. CONTROL: a planted extra failing name in head must break the subset.
        b, h = opt(A, '--base-report'), opt(A, '--head-report')
        def fs(f):
            j = json.load(open(f)); return set((s_['name'].split('/')[-1], a['title']) for s_ in j['testResults'] for a in s_['assertionResults'] if a['status'] == 'failed'), j['numPassedTests'], j['numFailedTests'], j['numTotalTestSuites']
        (bf, bp, bn, bs), (hf, hp, hn, hs) = fs(b), fs(h)
        t = Tally()
        t.check('C1', hf <= bf and not (hf | {('planted', 'x')}) <= bf, 'head failing set (%d) SUBSET of base failing set (%d): %s; head-only %s | CONTROL planted extra failure breaks the subset: %s' % (
            len(hf), len(bf), hf <= bf, sorted(hf - bf)[:5], not (hf | {('planted', 'x')}) <= bf))
        t.info('C2', 'passed base %d -> head %d (delta %+d); suites %d -> %d; failed %d -> %d' % (bp, hp, hp - bp, bs, hs, bn, hn))
        return t.end()
    if mode == 'table':
        r = row_arg()
        for e in SUITES[r]: print('%s cwd=%s cmd=%s kind=%s want=%s heavy=%s X1=%s' % (e[0], e[1], ' '.join(e[2]), e[3], e[5], e[6], e[7]))
        return 0
    if mode == 'run':
        r = row_arg(); wt, lab, out = opt(A, '--wt'), opt(A, '--label'), opt(A, '--out')
        if not (wt and lab in ('base', 'head') and out): print(__doc__); return 2
        ids = [x for x in (opt(A, '--ids') or '').split(',') if x]
        SYSTEM_TMP.update(x for x in (opt(A, '--system-tmp') or '').split(',') if x)
        return run(r, wt, lab, out, ids, '--skip-heavy' in A)
    if mode == 'arm':
        r = row_arg(); wt, repo, rev, cid, out, tag = (opt(A, k) for k in ('--wt', '--repo', '--swap-rev', '--id', '--out', '--tag'))
        swaps = [x for x in (opt(A, '--swap') or '').split(',') if x]
        old, new = opt(A, '--old'), opt(A, '--new')
        if not all((wt, repo, cid, out, tag, swaps)) or not (rev or (old is not None and new is not None)): print(__doc__); return 2
        return arm(r, wt, repo, swaps, rev, cid, out, tag, old, new)
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
