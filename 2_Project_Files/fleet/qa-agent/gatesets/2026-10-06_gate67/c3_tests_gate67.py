#!/usr/bin/env python3
"""c3_tests_gate67.py — C3 for #1394 (KS-723), gate67: RED-FIRST, SUITE AT BOTH ENDS, SPEC REGENERATED, TSC. NOT RUN BY THE DRAFTER.
The gate runs it in ITS OWN worktree (a clone OUTSIDE /Volumes/DevMASTER/!CODING, detached at the head a94ec8f6a2c6, after
`npm ci --ignore-scripts` in Blockchain/Dev and `npm run build --workspace=packages/shared`). Refuses (rc 2) a worktree inside the
forbidden root, a worktree not at the head, or a dirty worktree. Every overlay is restored BY CONTENT from the head blob and its
sha re-checked; the run ends with `git status --porcelain` empty or it FAILS.

  redfirst  overlay the BASE anchoring.openapi.ts (product hunk absent), keep the head test file, run that ONE file with vitest JSON:
            want 5 EXECUTED, 3 failed == the 3 `RED KS-723 TX*` cells, each with an assertion failure message (a LOAD FAILURE — a failed
            file with 0 assertion results — is NOT a red), 2 passed == the 2 `control` cells. Restore; re-run: 5 passed of 5.
  suite     services/anchoring `vitest run` JSON at the HEAD and at the BASE state (base registry overlaid + the new test file moved to
            the gate's scratch, both restored by content), SAME node + SAME vitest binary (paths and versions printed). Want: head files =
            base + 1, tests = base + 5, the failing FILE set identical at both ends (expected: threadTokenMint.test.ts only — pre-existing,
            BACKLOG.md:182), 0 new reds.
  spec      Blockchain/Dev `npm run generate-openapi` then the yaml must be byte-identical to the head blob (REGENERATED == COMMITTED,
            never pasted); `wc -c` of the yaml (bytes, not the generator's printed character count); `npm run check:openapi` rc 0; DRIFT
            CONTROL: append one byte to the yaml -> check:openapi rc != 0 (prints the line naming the failure), restore by content, cmp.
  tsc       `npx tsc -p services/anchoring --noEmit` rc 0; CONTROL planted TS2322 in anchoring.openapi.ts -> rc != 0; BLIND-SPOT PROOF
            planted TS2322 in the new test file -> rc 0 (it is not in the program: tsconfig excludes src/__tests__), and
            `--listFilesOnly` lists the test file 0 times. That is reported as NOT TESTED, never as a pass.
--selftest   the vitest-JSON judge on synthetic fixtures (assertion red / load failure / skipped / missing cell / wrong count).
Usage: c3_tests_gate67.py <redfirst|suite|spec|tsc|all> --worktree <dir> --scratch <dir>   |   --selftest
rc 0 PASS / rc 1 FAIL / rc 2 refused."""
import hashlib, json, os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate67 import K, Tally, outside_forbidden

DEV = 'Blockchain/Dev'
ANCH = 'Blockchain/Dev/services/anchoring'
TEST_REL = os.path.relpath(K['test'], ANCH)
RED = ['RED KS-723 TX1', 'RED KS-723 TX2', 'RED KS-723 TX3']
CTL = ['control KS-723 TC1', 'control KS-723 TC2']
PRE_RED_FILE = 'threadTokenMint.test.ts'


def sh(cmd, cwd, timeout=1800):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, shell=isinstance(cmd, str))
    return p.returncode, p.stdout, p.stderr


def blob_bytes(wt, rev, path):
    return subprocess.run(['git', '-C', wt, 'show', '%s:%s' % (rev, path)], capture_output=True, check=True).stdout


def put(wt, path, data):
    open(os.path.join(wt, path), 'wb').write(data)


def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def judge(js, want_red, want_green, want_exec):
    """(ok, why) — the vitest JSON judge. A file with status failed and 0 assertionResults is a LOAD FAILURE, never a red."""
    why = []
    files = js.get('testResults', [])
    for f in files:
        if f.get('status') == 'failed' and not f.get('assertionResults'):
            why.append('LOAD FAILURE in %s (0 assertions): %s' % (os.path.basename(f.get('name', '?')), (f.get('message') or '')[:120]))
    cells = {}
    for f in files:
        for a in f.get('assertionResults', []):
            cells[a.get('title', '')] = a
    def find(prefix):
        hit = [v for k, v in cells.items() if k.startswith(prefix)]
        return hit[0] if len(hit) == 1 else None
    executed = sum(1 for a in cells.values() if a.get('status') in ('passed', 'failed'))
    if executed != want_exec: why.append('executed %d (want %d)' % (executed, want_exec))
    skipped = [k for k, a in cells.items() if a.get('status') not in ('passed', 'failed')]
    if skipped: why.append('NOT EXECUTED (skip/todo/pending is never a pass): %s' % skipped)
    for p in want_red:
        a = find(p)
        if a is None: why.append('cell %r missing' % p)
        elif a.get('status') != 'failed': why.append('%r is %s, want failed' % (p, a.get('status')))
        elif not any(re.search(r'AssertionError|expected', m or '') for m in a.get('failureMessages', [])):
            why.append('%r failed WITHOUT an assertion message (not a red by assertion)' % p)
    for p in want_green:
        a = find(p)
        if a is None: why.append('cell %r missing' % p)
        elif a.get('status') != 'passed': why.append('%r is %s, want passed' % (p, a.get('status')))
    return not why, why


def vitest_json(wt, cwd_rel, args, out):
    rc, o, e = sh(['npx', 'vitest', 'run', '--reporter=json', '--outputFile=%s' % out] + args, os.path.join(wt, cwd_rel))
    try:
        js = json.load(open(out))
    except Exception as x:
        js = None
    return rc, js, (o + e)[-600:]


def guard(wt):
    if not outside_forbidden(wt): print('REFUSED: worktree %s is inside %s' % (wt, K['forbidden_root'])); return False
    h = subprocess.run(['git', '-C', wt, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    if h != K['head']: print('REFUSED: worktree HEAD %s is not the gated head %s' % (h, K['head'])); return False
    st = subprocess.run(['git', '-C', wt, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout
    if st.strip(): print('REFUSED: worktree is dirty:\n' + st); return False
    return True


def clean(wt, t, cid):
    st = subprocess.run(['git', '-C', wt, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout.strip()
    t.check(cid, st == '', 'worktree restored, git status --porcelain empty: %r' % st[:200])


def redfirst(wt, scratch, t):
    reg = K['registry_file']; head_reg = blob_bytes(wt, K['head'], reg); base_reg = blob_bytes(wt, K['base'], reg)
    put(wt, reg, base_reg)
    try:
        rc, js, tail = vitest_json(wt, ANCH, [TEST_REL], os.path.join(scratch, 'redfirst_base.json'))
        ok, why = judge(js or {}, RED, CTL, 5)
        t.check('R1', js is not None and ok and rc != 0, 'product hunk ABSENT: vitest rc %d | %s' % (rc, why or '3 RED by assertion, 2 controls green, 5 executed'))
    finally:
        put(wt, reg, head_reg)
    t.check('R2', hashlib.sha1(b'blob %d\0' % len(head_reg) + head_reg).hexdigest() == K['head_blobs'][reg], 'registry restored BY CONTENT to the head blob %s' % K['head_blobs'][reg][:12])
    rc, js, tail = vitest_json(wt, ANCH, [TEST_REL], os.path.join(scratch, 'redfirst_head.json'))
    ok, why = judge(js or {}, [], RED + CTL, 5)
    t.check('R3', js is not None and ok and rc == 0, 'product hunk PRESENT: vitest rc %d | %s' % (rc, why or '5 passed of 5'))
    clean(wt, t, 'R4')


def failing_files(js):
    return sorted(os.path.basename(f['name']) for f in js.get('testResults', []) if f.get('status') == 'failed')


def suite(wt, scratch, t):
    rc, o, e = sh(['node', '--version'], wt); node = o.strip()
    rc, o, e = sh(['npx', 'vitest', '--version'], os.path.join(wt, ANCH)); vv = (o + e).strip()[-60:]
    vb = os.path.realpath(os.path.join(wt, DEV, 'node_modules', '.bin', 'vitest'))
    print('INFO binary node %s | vitest %s | %s' % (node, vv, vb))
    rc_h, jh, _ = vitest_json(wt, ANCH, [], os.path.join(scratch, 'suite_head.json'))
    reg = K['registry_file']; head_reg = blob_bytes(wt, K['head'], reg)
    tp = os.path.join(wt, K['test']); parked = os.path.join(scratch, 'parked_' + os.path.basename(tp)); head_test = open(tp, 'rb').read()
    put(wt, reg, blob_bytes(wt, K['base'], reg)); shutil.move(tp, parked)
    try:
        rc_b, jb, _ = vitest_json(wt, ANCH, [], os.path.join(scratch, 'suite_base.json'))
    finally:
        put(wt, reg, head_reg); shutil.move(parked, tp)
    t.check('S0', open(tp, 'rb').read() == head_test and sha(os.path.join(wt, reg)) == hashlib.sha256(head_reg).hexdigest(), 'both overlays restored byte-identical (sha256)')
    if not (jh and jb):
        t.check('S1', False, 'no vitest JSON at one end (head %s, base %s)' % (bool(jh), bool(jb))); return
    fh, fb = len(jh['testResults']), len(jb['testResults'])
    th, tb = jh['numTotalTests'], jb['numTotalTests']
    rh, rb = failing_files(jh), failing_files(jb)
    t.check('S1', fh == fb + 1 and th == tb + 5, 'files %d -> %d (want +1), tests %d -> %d (want +5)' % (fb, fh, tb, th))
    t.check('S2', rh == rb and set(rh) <= {PRE_RED_FILE}, 'failing files base %s == head %s, only the pre-existing %s (BACKLOG.md:182) allowed; failed tests base %d head %d' % (
        rb, rh, PRE_RED_FILE, jb['numFailedTests'], jh['numFailedTests']))
    for f in jh['testResults']:
        if os.path.basename(f['name']) == PRE_RED_FILE:
            t.info('S2-kind', '%s at head: %s, %d assertion(s) — %s' % (PRE_RED_FILE, f.get('status'), len(f.get('assertionResults', [])), 'LOAD FAILURE' if not f.get('assertionResults') else 'assertion failures'))
    clean(wt, t, 'S3')


def spec(wt, scratch, t):
    y = os.path.join(wt, K['spec']); head_y = blob_bytes(wt, K['head'], K['spec'])
    rc, o, e = sh(['npm', 'run', 'generate-openapi'], os.path.join(wt, DEV))
    regen = open(y, 'rb').read()
    gen_chars = re.findall(r'(\d[\d,]*) (?:bytes|chars|characters)', o + e)
    t.check('P1', rc == 0 and regen == head_y, 'generate-openapi rc %d; regenerated yaml == committed head blob: %s; wc -c %d bytes (generator printed %s — a CHARACTER count if it differs)' % (
        rc, regen == head_y, len(regen), gen_chars[-1:] or 'nothing'))
    put(wt, K['spec'], head_y)
    rc, o, e = sh(['npm', 'run', 'check:openapi'], os.path.join(wt, DEV))
    t.check('P2', rc == 0, 'check:openapi rc %d' % rc)
    put(wt, K['spec'], head_y + b'#')
    try:
        rc2, o2, e2 = sh(['npm', 'run', 'check:openapi'], os.path.join(wt, DEV))
        line = [l for l in (o2 + e2).splitlines() if re.search(r'FAIL|drift|differ', l, re.I)][:1]
        t.check('P3', rc2 != 0, 'DRIFT CONTROL (one byte appended): check:openapi rc %d, says %s' % (rc2, line))
    finally:
        put(wt, K['spec'], head_y)
    t.check('P4', open(y, 'rb').read() == head_y, 'yaml restored, cmp-identical to the head blob')
    clean(wt, t, 'P5')


def tsc(wt, scratch, t):
    reg = os.path.join(wt, K['registry_file']); tf = os.path.join(wt, K['test'])
    regb, tfb = open(reg, 'rb').read(), open(tf, 'rb').read()
    cmd = ['npx', 'tsc', '-p', 'services/anchoring', '--noEmit']
    rc, o, e = sh(cmd, os.path.join(wt, DEV)); t.check('T1', rc == 0, 'tsc -p services/anchoring --noEmit rc %d' % rc)
    plant = b'\nconst __gate67_plant: number = "not a number";\n'
    open(reg, 'wb').write(regb + plant)
    try:
        rc, o, e = sh(cmd, os.path.join(wt, DEV)); t.check('T2', rc != 0 and 'TS2322' in o + e, 'CONTROL planted TS2322 in anchoring.openapi.ts: rc %d, TS2322 %s' % (rc, 'TS2322' in o + e))
    finally:
        open(reg, 'wb').write(regb)
    open(tf, 'wb').write(tfb + plant)
    try:
        rc, o, e = sh(cmd, os.path.join(wt, DEV))
        t.info('T3', 'BLIND SPOT: planted TS2322 in the NEW TEST FILE -> tsc rc %d (rc 0 = the file is not type-checked) — NOT TESTED, never a pass' % rc)
    finally:
        open(tf, 'wb').write(tfb)
    rc, o, e = sh(cmd + ['--listFilesOnly'], os.path.join(wt, DEV))
    t.info('T4', '--listFilesOnly: the new test file listed %d time(s); %d files in the program' % (o.count(os.path.basename(tf)), len(o.splitlines())))
    clean(wt, t, 'T5')


def selftest():
    res = []
    def rep(c, m): res.append(c); print('%s %s' % ('PASS' if c else 'FAIL', m))
    def cell(title, st, msg=None): return {'title': title, 'status': st, 'failureMessages': [msg] if msg else []}
    good = {'testResults': [{'name': 'x/ks723.test.ts', 'status': 'failed', 'assertionResults':
            [cell(RED[0] + ': a', 'failed', 'AssertionError: expected [] to deeply equal'), cell(RED[1] + ': b', 'failed', 'AssertionError: expected'),
             cell(RED[2] + ': c', 'failed', 'AssertionError: expected undefined to be defined'), cell(CTL[0] + ': d', 'passed'), cell(CTL[1] + ': e', 'passed')]}]}
    rep(judge(good, RED, CTL, 5)[0], 'judge: 3 assertion reds + 2 controls green, 5 executed -> PASS')
    load = {'testResults': [{'name': 'x/ks723.test.ts', 'status': 'failed', 'message': 'Failed to load @secuura/shared', 'assertionResults': []}]}
    ok, why = judge(load, RED, CTL, 5); rep(not ok and any('LOAD FAILURE' in w for w in why), 'judge: a LOAD FAILURE is not a red: %s' % why[:1])
    import copy
    sk = copy.deepcopy(good); sk['testResults'][0]['assertionResults'][3]['status'] = 'skipped'
    ok, why = judge(sk, RED, CTL, 5); rep(not ok, 'judge: a SKIPPED control is never a pass: %s' % why[:2])
    nm = copy.deepcopy(good); nm['testResults'][0]['assertionResults'][0]['failureMessages'] = ['TypeError: cannot read x']
    ok, why = judge(nm, RED, CTL, 5); rep(not ok, 'judge: a red without an assertion message is not a red by assertion: %s' % why[:1])
    ms = copy.deepcopy(good); del ms['testResults'][0]['assertionResults'][2]
    ok, why = judge(ms, RED, CTL, 5); rep(not ok, 'judge: a missing RED cell fails: %s' % why[:2])
    rep(not outside_forbidden('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'), 'guard: the shared checkout is refused as a worktree')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A or '--worktree' not in A or '--scratch' not in A: print(__doc__); return 2
    wt = os.path.abspath(A[A.index('--worktree') + 1]); sc = os.path.abspath(A[A.index('--scratch') + 1]); os.makedirs(sc, exist_ok=True)
    if not outside_forbidden(sc): print('REFUSED: scratch inside the forbidden root'); return 2
    if not guard(wt): return 2
    t = Tally(); steps = {'redfirst': redfirst, 'suite': suite, 'spec': spec, 'tsc': tsc}
    for s in (list(steps) if A[0] == 'all' else [A[0]]):
        print('--- %s' % s); steps[s](wt, sc, t)
    return t.end()


if __name__ == '__main__':
    sys.exit(main())
