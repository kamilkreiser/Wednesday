#!/usr/bin/env python3
"""c3_redfirst_gate59.py — gate59 C3 for #1382 (KS-1005, T1): red-first BY ASSERTION at develop vs head for the 6 cells, the services/auth
vitest suite before / after (0 NEW reds; the ks949 timeout class NAMED if it recurs, never silently passed), tsc with a positive control.
Runs ONLY in YOUR installed scratch worktree (lib guard_scratch refuses anything under /Volumes/DevMASTER); the worktree must be clean.
Install once at the head (develop and head share the root lock blob 40ea58aeaf39): `npm ci --ignore-scripts` at Blockchain/Dev, then
`npm run build --workspace=packages/shared`; this script asserts packages/shared/dist/index.js present and non-empty before any run.
MODES
  redfirst --repo <clone> --worktree <wt> --out <dir> [--head sha]
    R1 worktree at DEVELOP with the HEAD's ks1005 test file written in (it is a NEW file): vitest JSON -> exactly the kit's 4 red cells
       (A, B, C, D) FAILED, each BY ASSERTION (AssertionError / expected...; never 'Test timed out', never a load failure); A and B name the
       404 they received; E and F PASSED; 6 cells ran.  R1b the test file MOVED out to <out>/quarantine/ (never deleted), status clean.
    R2 worktree at HEAD: the same file, 6 / 6 passed.
  suite    --repo --worktree --out [--head sha]
    S1 the WHOLE services/auth vitest suite at develop and at HEAD: tests(head) == tests(develop) + 6, files(head) == files(develop) + 1.
    S2 0 NEW reds at head outside the kit's known class (ks949-platform-admin-seed-identity + 'Test timed out'); a known-class red is
       printed as NAMED with its file, cell and duration — the gate rules it.   S3 the 6 ks1005 cells all passed inside the full run.
  tsc      --repo --worktree --out [--head sha]
    T1 the named tsc binary `--noEmit -p .` in services/auth: rc 0 at develop and at head (version printed).
    T2 POSITIVE CONTROL at head: `const __g59: number = 'x';` appended to routes/users.ts -> rc != 0 naming TS2322; restored BY CONTENT
       (sha256) and `git status --porcelain` empty.   T3 tsconfig excludes src/__tests__: the new test is NOT typechecked by tsc (stated).
  --selftest  the judges on PLANTED vitest JSON (no install): the real red shape PASSES; a load failure, a 5th red (F red), a red that is a
              timeout, a green develop (no red at all), E red at develop, and a red for the wrong status (500 not 404) each FAIL R1; the
              suite judge PASSES a known-class ks949 timeout as NAMED and FAILS an unknown new red.
Usage: c3_redfirst_gate59.py redfirst|suite|tsc --repo <clone> --worktree <wt> --out <dir> [--head sha]  |  --selftest
rc 0 PASS / 1 FAIL / 2 usage"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate59 import K, wgit, now, Checks, opt_factory, show, sha256, guard_scratch, guard_out, run, has_commit, move_out, selftest_arm

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A:
    print(__doc__); raise SystemExit(0 if A else 2)
opt = opt_factory(A); X = K['redfirst']; KC = K['known_red_class']
MODE = next((m for m in ('redfirst', 'suite', 'tsc') if m in A), None)
REPO = opt('--repo'); WT = opt('--worktree'); OUT = opt('--out'); HEAD = opt('--head', K['head']); DEV = K['develop']
LOADFAIL = ['Failed to load', 'Cannot find module', 'SyntaxError', 'Failed to resolve import', 'Test suite failed to run']
STRIP = lambda s: re.sub(r'\x1b\[[0-9;]*m', '', s or '')


def cells(j):
    c = {}; ferr = []
    for t in j.get('testResults', []):
        msg = STRIP(t.get('message'))
        if t.get('status') == 'failed' and (not t.get('assertionResults') or any(s in msg for s in LOADFAIL)):
            ferr.append((t.get('name', '').split('/src/')[-1], msg[:200]))
        for a in t.get('assertionResults', []):
            c[a.get('fullName') or a['title']] = (a['status'], STRIP(((a.get('failureMessages') or ['']) + [''])[0]), t.get('name', '').split('/src/')[-1], a.get('duration'))
    return c, ferr


def pick(c, prefix):
    k = [n for n in c if prefix in n]
    return c[k[0]] if len(k) == 1 else ('absent' if not k else 'ambiguous', '', '', None)


def judge_red(C, j):
    c, ferr = cells(j); red = sorted(n for n, v in c.items() if v[0] == 'failed')
    want = X['red_at_develop']; ok_set = len(red) == len(want) and all(any(w in r for r in red) for w in want)
    by_assert = all(('AssertionError' in pick(c, w)[1] or 'expected' in pick(c, w)[1]) and 'Test timed out' not in pick(c, w)[1] for w in want)
    s404 = all(re.search(r'\b404\b', pick(c, w)[1]) for w in want[:2])
    green = all(pick(c, g)[0] == 'passed' for g in X['green_both'])
    C.chk('R1 red-first BY ASSERTION at develop', ok_set and by_assert and s404 and green and not ferr and len(c) == X['cells'],
          '%d cell(s) ran (want %d) | failed %s (want exactly A, B, C, D) | every red an assertion, none a timeout: %s | A and B name the 404 received: %s | E, F passed: %s | load failures %s' % (
              len(c), X['cells'], [(re.search(r'(cell|control) [A-F]', r) or re.search('.{0,22}$', r)).group(0) for r in red], by_assert, bool(s404), green, ferr or 'NONE'))
    for w in want:
        print('INFO R1 %s: %s' % (w, ' '.join(pick(c, w)[1].split())[:200]))


def judge_green(C, tag, j, n):
    c, ferr = cells(j); bad = [k for k, v in c.items() if v[0] != 'passed']
    C.chk(tag, len(c) == n and not bad and not ferr, '%d cell(s) ran (want %d) | not passed %s | load failures %s' % (len(c), n, [b[-50:] for b in bad] or 'NONE', ferr or 'NONE'))


def fails(j):
    c, ferr = cells(j)
    return {'%s :: %s' % (v[2], n): v for n, v in c.items() if v[0] == 'failed'}, ferr, c


def judge_suite(C, jd, jh):
    fd, ed, cd = fails(jd); fh, eh, ch = fails(jh)
    nd, nh = jd.get('numTotalTests'), jh.get('numTotalTests'); sd, sh = len(jd.get('testResults', [])), len(jh.get('testResults', []))
    C.chk('S1 totals', nh == (nd or 0) + X['cells'] and sh == sd + 1, 'develop %s tests / %s files | head %s tests / %s files (want +%d / +1)' % (nd, sd, nh, sh, X['cells']))
    new = {k: v for k, v in fh.items() if k not in fd}
    known = {k: v for k, v in new.items() if re.search(KC['file_rx'], v[2]) and re.search(KC['message_rx'], v[1])}
    unknown = {k: v for k, v in new.items() if k not in known}
    for k, v in known.items(): print('NAMED known class (%s): %s | %s ms | %s' % (KC['file_rx'], k[-110:], v[3], ' '.join(v[1].split())[:120]))
    for k, v in fd.items(): print('INFO red at develop too: %s | %s' % (k[-110:], ' '.join(v[1].split())[:100]))
    C.chk('S2 no NEW reds', not unknown and not eh, 'NEW reds outside the known class %s | NAMED known-class %d | load-failure files develop %s head %s' % (
        [k[-90:] for k in unknown] or 'NONE', len(known), ed or 'NONE', eh or 'NONE'))
    ks = {n: v for n, v in ch.items() if 'ks1005' in v[2] and 'KS-1005' in n}   # the ks1005 FILE's cells (a cell elsewhere naming the key does not count)
    C.chk('S3 the 6 cells in the full run', len(ks) == X['cells'] and all(v[0] == 'passed' for v in ks.values()), '%d KS-1005 cell(s) in the head run, all passed: %s' % (len(ks), all(v[0] == 'passed' for v in ks.values())))


def vitest(cwd, args, prefix):
    jf = prefix + '.json'; vb = os.path.join(WT, K['install_dir'], 'node_modules', '.bin', 'vitest')
    rc, o, e = run([vb, 'run'] + args + ['--reporter=json', '--outputFile=' + jf], cwd, prefix)
    try:
        return rc, json.load(open(jf))
    except Exception as ex:
        return rc, {'testResults': [{'name': 'NO JSON', 'status': 'failed', 'message': 'Failed to load: ' + str(ex), 'assertionResults': []}]}


if '--selftest' in A:
    st = {'ok': 0, 'n': 0}
    def cl(t, s, m=''): return {'title': t, 'fullName': 'KS-1005 — change-password reads the hash it verifies ' + t, 'status': s, 'failureMessages': [m] if m else [], 'duration': 10}
    AE = lambda got, want: 'AssertionError: a correct current password must not read as a missing user: expected %d to be %d' % (got, want)
    def J(cs, name='/x/src/__tests__/ks1005.test.ts', msg=''):
        return {'numTotalTests': len(cs), 'testResults': [{'name': name, 'status': 'failed' if any(c['status'] == 'failed' for c in cs) else 'passed', 'message': msg, 'assertionResults': cs}]}
    REAL = lambda **o: [cl('RED KS-1005 cell A — x', o.get('A', 'failed'), o.get('Am', AE(404, 200))), cl('RED KS-1005 cell B — x', 'failed', o.get('Bm', AE(404, 400))),
                        cl('RED KS-1005 cell C — x', 'failed', 'AssertionError: no SELECT asked: expected 0 to be greater than 0'), cl('RED KS-1005 cell D — x', o.get('D', 'failed'), o.get('Dm', AE(404, 200))),
                        cl('GREEN KS-1005 control E — x', o.get('E', 'passed'), AE(200, 404) if o.get('E') == 'failed' else ''), cl('GREEN KS-1005 control F — x', o.get('F', 'passed'), AE(404, 400) if o.get('F') == 'failed' else '')]
    selftest_arm(st, 'R-0 the real red shape (positive control)', lambda C: judge_red(C, J(REAL())), None)
    selftest_arm(st, 'R-1 a load failure', lambda C: judge_red(C, {'testResults': [{'name': 'x', 'status': 'failed', 'message': 'Failed to load url @secuura/shared', 'assertionResults': []}]}), 'R1')
    selftest_arm(st, 'R-2 a 5th red (F red at develop)', lambda C: judge_red(C, J(REAL(F='failed'))), 'R1')
    selftest_arm(st, 'R-3 D red by TIMEOUT, not assertion', lambda C: judge_red(C, J(REAL(Dm='Error: Test timed out in 5000ms.'))), 'R1')
    selftest_arm(st, 'R-4 green at develop (nothing red)', lambda C: judge_red(C, J([dict(c, status='passed', failureMessages=[]) for c in REAL()])), 'R1')
    selftest_arm(st, 'R-5 control E red at develop', lambda C: judge_red(C, J(REAL(E='failed'))), 'R1')
    selftest_arm(st, 'R-6 A red for the wrong status (500)', lambda C: judge_red(C, J(REAL(Am=AE(500, 200)))), 'R1')
    selftest_arm(st, 'R-7 6/6 green at head', lambda C: judge_green(C, 'R2 green', J([dict(c, status='passed', failureMessages=[]) for c in REAL()]), 6), None)
    base = {'numTotalTests': 4, 'testResults': [{'name': '/x/src/__tests__/a.test.ts', 'status': 'passed', 'message': '', 'assertionResults': [cl('a%d' % i, 'passed') for i in range(4)]}]}
    k949 = {'name': '/x/src/__tests__/ks949-platform-admin-seed-identity.test.ts', 'status': 'failed', 'message': '', 'assertionResults': [cl('seed walk', 'failed', 'Error: Test timed out in 5000ms.')]}
    unk = {'name': '/x/src/__tests__/oauth.test.ts', 'status': 'failed', 'message': '', 'assertionResults': [cl('scopes', 'failed', 'AssertionError: expected 400 to be 201')]}
    ks = {'name': '/x/src/__tests__/ks1005.test.ts', 'status': 'passed', 'message': '', 'assertionResults': [dict(c, status='passed', failureMessages=[]) for c in REAL()]}
    k949p = dict(k949, status='passed', assertionResults=[cl('seed walk', 'passed')])
    B2 = {'numTotalTests': 5, 'testResults': base['testResults'] + [k949p]}
    H2 = lambda last, extra=(): {'numTotalTests': 11 + sum(len(e['assertionResults']) for e in extra), 'testResults': base['testResults'] + [ks, last] + list(extra)}
    selftest_arm(st, 'S-0 clean suite (positive control)', lambda C: judge_suite(C, B2, H2(k949p)), None)
    selftest_arm(st, 'S-1 a ks949 TIMEOUT at head is NAMED and does not fail S2', lambda C: judge_suite(C, B2, H2(k949)), None)
    selftest_arm(st, 'S-2 an unknown NEW red', lambda C: judge_suite(C, B2, dict(H2(k949p), numTotalTests=11)) or judge_suite(C, B2, H2(k949p) | {'testResults': H2(k949p)['testResults'][:-1] + [dict(k949p, assertionResults=[cl('seed walk', 'failed', 'AssertionError: expected 1 to be 2')])]}), 'S2')
    selftest_arm(st, 'S-3 the ks1005 file missing from the head run', lambda C: judge_suite(C, B2, {'numTotalTests': 11, 'testResults': base['testResults'] + [k949p, unk]}), 'S3')
    print('SELFTEST %s %d of %d' % ('OK' if st['ok'] == st['n'] else 'BROKEN', st['ok'], st['n'])); raise SystemExit(0 if st['ok'] == st['n'] else 1)

if MODE is None or not REPO or not WT or not OUT:
    print(__doc__); raise SystemExit(2)
for s in (HEAD, DEV):
    if not re.fullmatch(r'[0-9a-f]{40}', s) or not has_commit(REPO, s):
        print('REFUSING: %s is not a 40-hex commit present in %s' % (s, REPO)); raise SystemExit(2)
WT = guard_scratch(WT, 'worktree'); OUT = guard_out(OUT)
DIST = os.path.join(WT, K['shared_dist'])
if not (os.path.isfile(DIST) and os.path.getsize(DIST) > 0):
    print('REFUSING: %s missing or empty — npm ci --ignore-scripts + build packages/shared first (a load failure is not a red)' % DIST); raise SystemExit(2)
if wgit(WT, 'status', '--porcelain').strip():
    print('REFUSING: the worktree is not clean'); raise SystemExit(2)
print('c3_redfirst_gate59 %s %s | worktree %s | develop %s | head %s | shared dist %d bytes' % (MODE, now(), WT, DEV[:12], HEAD[:12], os.path.getsize(DIST)))
SD = os.path.join(WT, K['suite_dir']); TP = os.path.join(WT, K['test']); TREL = os.path.relpath(TP, SD); C = Checks()
if MODE == 'redfirst':
    wgit(WT, 'checkout', '--quiet', '--detach', DEV)
    if os.path.exists(TP):
        print('REFUSING: the ks1005 test already exists at develop — the red-first premise (a NEW file) is false'); raise SystemExit(2)
    open(TP, 'w', encoding='utf-8').write(show(REPO, HEAD, K['test']))
    try:
        rc, j = vitest(SD, [TREL], os.path.join(OUT, 'c3_r1_develop_plus_test'))
        judge_red(C, j)
    finally:
        q = move_out(TP, os.path.join(OUT, 'quarantine'), 'ks1005.develop.%s.test.ts' % now().replace(':', ''))
    stt = wgit(WT, 'status', '--porcelain').strip()
    C.chk('R1b moved out', not stt and not os.path.exists(TP), 'git status --porcelain %r | the test still in the worktree: %s | quarantined at %s' % (stt[:100], os.path.exists(TP), q))
    wgit(WT, 'checkout', '--quiet', '--detach', HEAD)
    rc, j = vitest(SD, [TREL], os.path.join(OUT, 'c3_r2_head'))
    judge_green(C, 'R2 green at head', j, X['cells'])
elif MODE == 'suite':
    res = {}
    for name, sha in (('develop', DEV), ('head', HEAD)):
        wgit(WT, 'checkout', '--quiet', '--detach', sha)
        rc, res[name] = vitest(SD, [], os.path.join(OUT, 'c3_suite_' + name))
        print('INFO suite %s at %s rc %d | tests %s failed %s files %s' % (name, sha[:12], rc, res[name].get('numTotalTests'), res[name].get('numFailedTests'), len(res[name].get('testResults', []))))
    judge_suite(C, res['develop'], res['head'])
elif MODE == 'tsc':
    TSC = os.path.join(WT, K['install_dir'], 'node_modules', '.bin', 'tsc')
    if not os.path.exists(TSC):
        print('REFUSING: no tsc binary at %s (install first)' % TSC); raise SystemExit(2)
    ver = run([TSC, '--version'], SD, None)[1].strip(); rcs = {}
    for name, sha in (('develop', DEV), ('head', HEAD)):
        wgit(WT, 'checkout', '--quiet', '--detach', sha)
        rcs[name] = run([TSC, '--noEmit', '-p', '.'], SD, os.path.join(OUT, 'c3_tsc_' + name))[0]
    C.chk('T1 tsc rc 0 develop and head', rcs == {'develop': 0, 'head': 0}, '%s (%s) | rc develop %d head %d' % (TSC, ver, rcs['develop'], rcs['head']))
    PF = os.path.join(WT, K['product']); src = open(PF, encoding='utf-8').read(); before = sha256(src)
    try:
        open(PF, 'w', encoding='utf-8').write(src + "\nconst __g59: number = 'x';\n")
        landed = "const __g59: number = 'x';" in open(PF, encoding='utf-8').read()   # assert the tamper LANDED before reading its result
        rc, o, e = run([TSC, '--noEmit', '-p', '.'], SD, os.path.join(OUT, 'c3_tsc_positive_control'))
    finally:
        open(PF, 'w', encoding='utf-8').write(src)
    stt = wgit(WT, 'status', '--porcelain').strip()
    C.chk('T2 positive control', landed and rc != 0 and 'TS2322' in o + e and sha256(open(PF, encoding='utf-8').read()) == before and not stt,
          'tamper landed: %s | planted TS2322 -> rc %d, TS2322 printed: %s | restored by content sha256 %s | git status %r' % (landed, rc, 'TS2322' in o + e, before[:16], stt[:80]))
    tc = open(os.path.join(SD, 'tsconfig.json'), encoding='utf-8').read(); exc = re.search(r'"exclude"\s*:\s*\[[^\]]*src/__tests__', tc) is not None
    C.chk('T3 tests excluded (stated)', exc, 'services/auth/tsconfig.json excludes src/__tests__: %s — tsc does NOT typecheck the ks1005 test (vitest transpiles it without a typecheck); say so' % exc)
wgit(WT, 'checkout', '--quiet', '--detach', HEAD)
n = C.nfail()
print('C3 %s %s: %d FAIL of %d checks | head %s' % (MODE.upper(), 'PASS' if n == 0 else 'FAIL', n, len(C.res), HEAD[:12]))
raise SystemExit(1 if n else 0)
