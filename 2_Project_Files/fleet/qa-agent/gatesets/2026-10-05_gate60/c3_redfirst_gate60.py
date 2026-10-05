#!/usr/bin/env python3
"""c3_redfirst_gate60.py — gate60 C3 for #1384 (KS-1210, T1): red-first BY ASSERTION at develop vs head for the 24 cells, the two sibling
fixes proved NECESSARY and FIXTURE-ONLY, the services/auth vitest suite before / after (0 NEW reds; the ks949 timeout class NAMED and its
blob proved byte-identical, never silently passed), tsc with a positive control, and `npm run check:openapi`.
Runs ONLY in YOUR installed scratch worktree (lib guard_scratch refuses anything under /Volumes/DevMASTER); the worktree must be clean.
Install once at the head (develop and head share root lock blob 40ea58aeaf39): `npm ci --ignore-scripts` at Blockchain/Dev, then
`npm run build --workspace=packages/shared`; this script asserts packages/shared/dist/index.js present and non-empty before any run.
MODES
  redfirst --repo <clone> --worktree <wt> --out <dir> [--head sha]
    R1 worktree at DEVELOP with the HEAD's ks1210 test written in (a NEW file): vitest JSON -> EXACTLY the kit's 17 red cells
       (A1-A4 A6 B1 B2 B5 C1-C4 C8 D1 E1 E2 E4), each red for the kit's NAMED reason (the status received, e.g. `expected 201 to be 400`;
       the three drift cells by the reader's thrown `declaration not found: const OAUTH_…` — printed as THROWN, the gate rules it); never
       'Test timed out', never a load failure; the 7 green (A5 B3 B4 C5 C6 C7 E3) PASSED; 24 cells ran.
    R1b the test file MOVED out to <out>/quarantine/ (never deleted), status clean.   R2 worktree at HEAD: 24 / 24 passed.
  siblings --repo --worktree --out [--head sha]
    R3 NECESSARY: at HEAD with DEVELOP's ks431 / ks451 written over the head's, each file has >= 1 red (the fixes were needed, not cosmetic);
       restored by `git checkout -- <path>`, status clean.   R4 FIXTURE-ONLY: at DEVELOP with the HEAD's ks431 / ks451 written over, both
       files all green (the new fixtures hold against the old product: no assertion was bent to the new code). Restored, status clean.
  suite    --repo --worktree --out [--head sha]
    S1 the WHOLE services/auth vitest suite at develop and at HEAD: tests(head) == tests(develop) + 24, files(head) == files(develop) + 1.
    S2 0 NEW reds at head outside the kit's known class (ks949-platform-admin-seed-identity + 'Test timed out'); a known-class red is
       printed NAMED with file, cell and duration.   S3 the 24 ks1210 cells all passed inside the full run.
    S4 the ks949 test blob is byte-identical develop/head (CONTROL: routes/oauth.ts's blob differs) — a ks949 red cannot be this diff's.
  tsc      --repo --worktree --out [--head sha]
    T1 the named tsc binary `--noEmit -p .` in services/auth: rc 0 at develop and at head (version printed).
    T2 POSITIVE CONTROL at head: `const __g60: number = 'x';` appended to routes/oauth.ts -> rc != 0 naming TS2322; tamper LANDING asserted
       first; restored BY CONTENT (sha256), `git status --porcelain` empty.   T3 tsconfig excludes src/__tests__ (the tests are not typechecked).
  openapi  --repo --worktree --out [--head sha]
    O1 `npm run check:openapi` at Blockchain/Dev at HEAD: rc 0 (its example-block count printed).   O2 0 spec / YAML paths in the diff
       (kit spec_paths_rx) — CONTROL: the same regex matches `docs/openapi/secuura-api.yaml` (it can fire) and the diff has 6 paths.
  --selftest  the judges on PLANTED vitest JSON (no install): the real 17|7 shape PASSES R1; a load failure, a green A5 turned red, C1 red by
              TIMEOUT, a green develop, A1 red for the wrong status (500), E1 red for a different throw, 23 cells ran each FAIL R1; the suite
              judge PASSES a known-class ks949 timeout as NAMED and FAILS an unknown new red and a missing ks1210 file; the siblings judge
              FAILS a develop-ks451 that stays green at head (R3) and a head-ks431 red at develop (R4).
Usage: c3_redfirst_gate60.py redfirst|siblings|suite|tsc|openapi --repo <clone> --worktree <wt> --out <dir> [--head sha]  |  --selftest
rc 0 PASS / 1 FAIL / 2 usage"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate60 import K, git, wgit, now, Checks, opt_factory, show, sha256, guard_scratch, guard_out, run, has_commit, move_out, selftest_arm, blob

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A:
    print(__doc__); raise SystemExit(0 if A else 2)
opt = opt_factory(A); X = K['redfirst']; KC = K['known_red_class']
MODE = next((m for m in ('redfirst', 'siblings', 'suite', 'tsc', 'openapi') if m in A), None)
REPO = opt('--repo'); WT = opt('--worktree'); OUT = opt('--out'); HEAD = opt('--head', K['head']); DEV = K['develop']
LOADFAIL = ['Failed to load', 'Cannot find module', 'SyntaxError', 'Failed to resolve import', 'Test suite failed to run']
STRIP = lambda s: re.sub(r'\x1b\[[0-9;]*m', '', s or '')
RED = X['red_at_develop']; GREEN = X['green_both']; THROWN = X['thrown_not_assertion']


def cells(j):
    c = {}; ferr = []
    for t in j.get('testResults', []):
        msg = STRIP(t.get('message'))
        if t.get('status') == 'failed' and (not t.get('assertionResults') or any(s in msg for s in LOADFAIL)):
            ferr.append((t.get('name', '').split('/src/')[-1], msg[:200]))
        for a in t.get('assertionResults', []):
            c[a.get('fullName') or a['title']] = (a['status'], STRIP(((a.get('failureMessages') or ['']) + [''])[0]), t.get('name', '').split('/src/')[-1], a.get('duration'))
    return c, ferr


def by_id(c):
    """{cell id 'A1'..'E4': value} from the ks1210 titles `A1 refuses …` (the id is the first token of the title)"""
    out = {}
    for n, v in c.items():
        m = re.search(r'(?:^|\s)([A-E]\d)\s', n)
        if m: out.setdefault(m.group(1), []).append(v)
    return {k: v[0] if len(v) == 1 else ('ambiguous', '', '', None) for k, v in out.items()}


def judge_red(C, j):
    c, ferr = cells(j); b = by_id(c)
    red = sorted(k for k, v in b.items() if v[0] == 'failed'); green = sorted(k for k, v in b.items() if v[0] == 'passed')
    why = {}
    for k, rx in RED.items():
        v = b.get(k, ('absent', '', '', None))
        why[k] = v[0] == 'failed' and re.search(re.escape(rx) if k in THROWN else rx, v[1]) is not None and 'Test timed out' not in v[1]
    ok = red == sorted(RED) and green == sorted(GREEN) and all(why.values()) and not ferr and len(c) == X['cells']
    C.chk('R1 red-first BY ASSERTION at develop', ok,
          '%d cell(s) ran (want %d) | red %d %s (want the kit 17) | green %d %s (want %s) | each red for its NAMED reason: %s | load failures %s' % (
              len(c), X['cells'], len(red), red, len(green), green, GREEN, [k for k, v in why.items() if not v] or 'ALL', ferr or 'NONE'))
    for k in sorted(RED):
        v = b.get(k, ('absent', '', '', None))
        print('INFO R1 %s %s%s: %s' % (k, v[0], ' (THROWN by the drift reader, not an AssertionError)' if k in THROWN else '', ' '.join(v[1].split())[:160]))


def judge_green(C, tag, j, n):
    c, ferr = cells(j); bad = [k for k, v in c.items() if v[0] != 'passed']
    C.chk(tag, len(c) == n and not bad and not ferr, '%d cell(s) ran (want %d) | not passed %s | load failures %s' % (len(c), n, [x[-60:] for x in bad] or 'NONE', ferr or 'NONE'))


def judge_sib(C, tag, j, want_red, name):
    c, ferr = cells(j); red = [k for k, v in c.items() if v[0] == 'failed']
    # R3 (necessary): a red cell OR a load failure both prove the old file cannot stand at head (a load failure is NAMED, the gate rules it);
    # R4 (fixture-only): all green, nothing failed to load.
    ok = (len(red) >= 1 or bool(ferr)) if want_red else (not red and len(c) > 0 and not ferr)
    C.chk(tag, ok, '%s: %d cell(s), red %d (want %s) | load failures %s' % (name, len(c), len(red), '>= 1 or a NAMED load failure' if want_red else '0', ferr or 'NONE'))
    for k in red[:6]: print('INFO %s %s red: %s | %s' % (tag.split()[0], name, k[-70:], ' '.join(c[k][1].split())[:120]))


def fails(j):
    c, ferr = cells(j)
    return {'%s :: %s' % (v[2], n): v for n, v in c.items() if v[0] == 'failed'}, ferr, c


def judge_suite(C, jd, jh, blobs):
    fd, ed, cd = fails(jd); fh, eh, ch = fails(jh)
    nd, nh = jd.get('numTotalTests'), jh.get('numTotalTests'); sd, sh = len(jd.get('testResults', [])), len(jh.get('testResults', []))
    C.chk('S1 totals', nh == (nd or 0) + X['cells'] and sh == sd + 1, 'develop %s tests / %s files | head %s tests / %s files (want +%d / +1; kit expectation %s)' % (
        nd, sd, nh, sh, X['cells'], K['suite_expect']))
    new = {k: v for k, v in fh.items() if k not in fd}
    known = {k: v for k, v in new.items() if re.search(KC['file_rx'], v[2]) and re.search(KC['message_rx'], v[1])}
    unknown = {k: v for k, v in new.items() if k not in known}
    for k, v in known.items(): print('NAMED known class (%s): %s | %s ms | %s' % (KC['file_rx'], k[-110:], v[3], ' '.join(v[1].split())[:120]))
    for k, v in fd.items(): print('INFO red at develop too: %s | %s' % (k[-110:], ' '.join(v[1].split())[:100]))
    C.chk('S2 no NEW reds', not unknown and not eh, 'NEW reds outside the known class %s | NAMED known-class %d | load-failure files develop %s head %s' % (
        [k[-90:] for k in unknown] or 'NONE', len(known), ed or 'NONE', eh or 'NONE'))
    ks = {n: v for n, v in ch.items() if 'ks1210' in v[2]}
    C.chk('S3 the 24 cells in the full run', len(ks) == X['cells'] and all(v[0] == 'passed' for v in ks.values()), '%d ks1210 cell(s) in the head run, all passed: %s' % (len(ks), all(v[0] == 'passed' for v in ks.values())))
    C.chk('S4 ks949 byte-identical', blobs['ks949_dev'] == blobs['ks949_head'] and blobs['oauth_dev'] != blobs['oauth_head'],
          'ks949 blob develop %s head %s equal: %s | CONTROL routes/oauth.ts %s -> %s differs: %s' % (
              (blobs['ks949_dev'] or '-')[:12], (blobs['ks949_head'] or '-')[:12], blobs['ks949_dev'] == blobs['ks949_head'], (blobs['oauth_dev'] or '-')[:12], (blobs['oauth_head'] or '-')[:12], blobs['oauth_dev'] != blobs['oauth_head']))


def vitest(cwd, args, prefix):
    jf = prefix + '.json'; vb = os.path.join(WT, K['install_dir'], 'node_modules', '.bin', 'vitest')
    rc, o, e = run([vb, 'run'] + args + ['--reporter=json', '--outputFile=' + jf], cwd, prefix)
    try:
        return rc, json.load(open(jf))
    except Exception as ex:
        return rc, {'testResults': [{'name': 'NO JSON', 'status': 'failed', 'message': 'Failed to load: ' + str(ex), 'assertionResults': []}]}


TITLES = {'A1': 'refuses subjects:erase', 'A2': 'refuses the wildcard', 'A3': 'refuses a string', 'A4': 'refuses subjects:erase even', 'A5': 'still accepts', 'A6': 'the UPDATE path is closed',
          'B1': 'a plain user asking admin:write', 'B2': 'ORG_ADMIN also gets 403', 'B3': 'a platform admin may register', 'B4': 'certifications:write is NOT privileged', 'B5': 'the UPDATE path enforces',
          'C1': 'a non-owner GET', 'C2': 'a non-owner PATCH', 'C3': 'a non-owner DELETE', 'C4': 'a non-owner rotate-secret', 'C5': 'the OWNER still gets', 'C6': 'the OWNER may still PATCH',
          'C7': 'ORG_ADMIN may PATCH', 'C8': 'an app that does not exist', 'D1': 'a NON-OWNER asking a privileged', 'E1': 'the FOUR-role', 'E2': 'the SIX-role', 'E3': 'the drift reader is not vacuous', 'E4': 'the reader handles'}
if '--selftest' in A:
    st = {'ok': 0, 'n': 0}
    def cl(k, s, m=''): return {'title': '%s %s' % (k, TITLES[k]), 'fullName': 'KS-1210 x %s %s' % (k, TITLES[k]), 'status': s, 'failureMessages': [m] if m else [], 'duration': 10}
    def msg(k): return ('Error: ' + RED[k]) if k in THROWN else 'AssertionError: %s // Object.is equality' % RED[k]
    def J(o=None, drop=None, name='/x/src/__tests__/ks1210-oauth-app-scopes-and-ownership.test.ts'):
        o = o or {}; cs = []
        for k in TITLES:
            if k == drop: continue
            s, m = o.get(k, ('failed', msg(k)) if k in RED else ('passed', ''))
            cs.append(cl(k, s, m))
        return {'numTotalTests': len(cs), 'testResults': [{'name': name, 'status': 'failed' if any(c['status'] == 'failed' for c in cs) else 'passed', 'message': '', 'assertionResults': cs}]}
    ALLG = {k: ('passed', '') for k in TITLES}
    selftest_arm(st, 'R-0 the real 17|7 shape (positive control)', lambda C: judge_red(C, J()), None)
    selftest_arm(st, 'R-1 a load failure', lambda C: judge_red(C, {'testResults': [{'name': 'x', 'status': 'failed', 'message': 'Failed to load url @secuura/shared', 'assertionResults': []}]}), 'R1')
    selftest_arm(st, 'R-2 A5 (a green control) red at develop', lambda C: judge_red(C, J({'A5': ('failed', 'AssertionError: expected 400 to be 201')})), 'R1')
    selftest_arm(st, 'R-3 C1 red by TIMEOUT, not assertion', lambda C: judge_red(C, J({'C1': ('failed', 'Error: Test timed out in 5000ms. expected 200 to be 404')})), 'R1')
    selftest_arm(st, 'R-4 green at develop (nothing red)', lambda C: judge_red(C, J(ALLG)), 'R1')
    selftest_arm(st, 'R-5 A1 red for the wrong status (500)', lambda C: judge_red(C, J({'A1': ('failed', 'AssertionError: expected 500 to be 400')})), 'R1')
    selftest_arm(st, 'R-6 E1 red for a different throw', lambda C: judge_red(C, J({'E1': ('failed', 'TypeError: Cannot read properties of undefined')})), 'R1')
    selftest_arm(st, 'R-7 23 cells ran (D1 missing)', lambda C: judge_red(C, J(drop='D1')), 'R1')
    selftest_arm(st, 'R-8 24/24 green at head (positive control)', lambda C: judge_green(C, 'R2 green', J(ALLG), 24), None)
    one = lambda nm, s, m='': {'numTotalTests': 1, 'testResults': [{'name': '/x/src/__tests__/%s.test.ts' % nm, 'status': s, 'message': '', 'assertionResults': [{'title': 't', 'fullName': 't', 'status': s, 'failureMessages': [m] if m else []}]}]}
    selftest_arm(st, 'G-0 siblings: develop-ks451 red at head, head-ks431 green at develop (positive control)', lambda C: (judge_sib(C, 'R3 necessary', one('ks451', 'failed', 'AssertionError: expected false to be true'), True, 'ks451'), judge_sib(C, 'R4 fixture-only', one('ks431', 'passed'), False, 'ks431')), None)
    selftest_arm(st, 'G-1 develop-ks451 stays GREEN at head', lambda C: judge_sib(C, 'R3 necessary', one('ks451', 'passed'), True, 'ks451'), 'R3')
    selftest_arm(st, 'G-2 head-ks431 RED at develop', lambda C: judge_sib(C, 'R4 fixture-only', one('ks431', 'failed', 'AssertionError: expected 404 to be 200'), False, 'ks431'), 'R4')
    base = {'numTotalTests': 4, 'testResults': [{'name': '/x/src/__tests__/a.test.ts', 'status': 'passed', 'message': '', 'assertionResults': [{'title': 'a%d' % i, 'fullName': 'a%d' % i, 'status': 'passed', 'failureMessages': []} for i in range(4)]}]}
    k949 = {'name': '/x/src/__tests__/ks949-platform-admin-seed-identity.test.ts', 'status': 'failed', 'message': '', 'assertionResults': [{'title': 'walk', 'fullName': 'seed walk', 'status': 'failed', 'failureMessages': ['Error: Test timed out in 5000ms.'], 'duration': 5009}]}
    k949p = dict(k949, status='passed', assertionResults=[{'title': 'walk', 'fullName': 'seed walk', 'status': 'passed', 'failureMessages': []}])
    ks = J(ALLG)['testResults'][0]
    B2 = {'numTotalTests': 5, 'testResults': base['testResults'] + [k949p]}
    H2 = lambda last, extra=None: {'numTotalTests': 29, 'testResults': base['testResults'] + [ks, last] + ([extra] if extra else [])}
    BL = {'ks949_dev': '4f03e6f4f132', 'ks949_head': '4f03e6f4f132', 'oauth_dev': '3ae75ea1351a', 'oauth_head': '72819e0e7622'}
    unk = dict(k949p, assertionResults=[{'title': 'walk', 'fullName': 'seed walk', 'status': 'failed', 'failureMessages': ['AssertionError: expected 1 to be 2']}], status='failed')
    selftest_arm(st, 'S-0 clean suite (positive control)', lambda C: judge_suite(C, B2, H2(k949p), BL), None)
    selftest_arm(st, 'S-1 a ks949 TIMEOUT at head is NAMED and does not fail S2', lambda C: judge_suite(C, B2, H2(k949), BL), None)
    selftest_arm(st, 'S-2 an unknown NEW red (ks949 by ASSERTION)', lambda C: judge_suite(C, B2, H2(unk), BL), 'S2')
    selftest_arm(st, 'S-3 the ks1210 file missing from the head run', lambda C: judge_suite(C, B2, {'numTotalTests': 5, 'testResults': base['testResults'] + [k949p]}, BL), 'S3')
    selftest_arm(st, 'S-4 the ks949 blob changed by the diff', lambda C: judge_suite(C, B2, H2(k949p), dict(BL, ks949_head='ffffffffffff')), 'S4')
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
print('c3_redfirst_gate60 %s %s | worktree %s | develop %s | head %s | shared dist %d bytes' % (MODE, now(), WT, DEV[:12], HEAD[:12], os.path.getsize(DIST)))
SD = os.path.join(WT, K['suite_dir']); TP = os.path.join(WT, K['test']); TREL = os.path.relpath(TP, SD); C = Checks()
if MODE == 'redfirst':
    wgit(WT, 'checkout', '--quiet', '--detach', DEV)
    if os.path.exists(TP):
        print('REFUSING: the ks1210 test already exists at develop — the red-first premise (a NEW file) is false'); raise SystemExit(2)
    open(TP, 'w', encoding='utf-8').write(show(REPO, HEAD, K['test']))
    try:
        rc, j = vitest(SD, [TREL], os.path.join(OUT, 'c3_r1_develop_plus_test'))
        judge_red(C, j)
    finally:
        q = move_out(TP, os.path.join(OUT, 'quarantine'), 'ks1210.develop.%s.test.ts' % now().replace(':', ''))
    stt = wgit(WT, 'status', '--porcelain').strip()
    C.chk('R1b moved out', not stt and not os.path.exists(TP), 'git status --porcelain %r | the test still in the worktree: %s | quarantined at %s' % (stt[:100], os.path.exists(TP), q))
    wgit(WT, 'checkout', '--quiet', '--detach', HEAD)
    rc, j = vitest(SD, [TREL], os.path.join(OUT, 'c3_r2_head'))
    judge_green(C, 'R2 green at head', j, X['cells'])
elif MODE == 'siblings':
    for tag, at, src, want_red in (('R3 necessary', HEAD, DEV, True), ('R4 fixture-only', DEV, HEAD, False)):
        wgit(WT, 'checkout', '--quiet', '--detach', at)
        for t in K['sibling_tests']:
            p = os.path.join(WT, t); orig = open(p, encoding='utf-8').read(); txt = show(REPO, src, t)
            open(p, 'w', encoding='utf-8').write(txt)
            landed = open(p, encoding='utf-8').read() == txt and txt != orig
            try:
                rc, j = vitest(SD, [os.path.relpath(p, SD)], os.path.join(OUT, 'c3_%s_%s' % (tag.split()[0].lower(), t.split('/')[-1][:5])))
                C.chk('%s LANDED %s' % (tag.split()[0], t.split('/')[-1][:5]), landed, 'the %s version of %s is in place at %s and differs from the checked-out one: %s' % (src[:12], t.split('/')[-1], at[:12], landed))
                judge_sib(C, '%s %s' % (tag, t.split('/')[-1][:5]), j, want_red, t.split('/')[-1])
            finally:
                wgit(WT, 'checkout', '--quiet', '--', t)
        stt = wgit(WT, 'status', '--porcelain').strip()
        C.chk('%s restored' % tag.split()[0], not stt, 'git status --porcelain after restoring both files at %s: %r' % (at[:12], stt[:100]))
elif MODE == 'suite':
    res = {}
    for name, sha in (('develop', DEV), ('head', HEAD)):
        wgit(WT, 'checkout', '--quiet', '--detach', sha)
        rc, res[name] = vitest(SD, [], os.path.join(OUT, 'c3_suite_' + name))
        print('INFO suite %s at %s rc %d | tests %s failed %s files %s' % (name, sha[:12], rc, res[name].get('numTotalTests'), res[name].get('numFailedTests'), len(res[name].get('testResults', []))))
    bl = {'ks949_dev': blob(REPO, DEV, K['known_flake_test']), 'ks949_head': blob(REPO, HEAD, K['known_flake_test']), 'oauth_dev': blob(REPO, DEV, K['product']), 'oauth_head': blob(REPO, HEAD, K['product'])}
    judge_suite(C, res['develop'], res['head'], bl)
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
        open(PF, 'w', encoding='utf-8').write(src + "\nconst __g60: number = 'x';\n")
        landed = "const __g60: number = 'x';" in open(PF, encoding='utf-8').read()
        rc, o, e = run([TSC, '--noEmit', '-p', '.'], SD, os.path.join(OUT, 'c3_tsc_positive_control'))
    finally:
        open(PF, 'w', encoding='utf-8').write(src)
    stt = wgit(WT, 'status', '--porcelain').strip()
    C.chk('T2 positive control', landed and rc != 0 and 'TS2322' in o + e and sha256(open(PF, encoding='utf-8').read()) == before and not stt,
          'tamper landed: %s | planted TS2322 -> rc %d, TS2322 printed: %s | restored by content sha256 %s | git status %r' % (landed, rc, 'TS2322' in o + e, before[:16], stt[:80]))
    tc = open(os.path.join(SD, 'tsconfig.json'), encoding='utf-8').read(); exc = re.search(r'"exclude"\s*:\s*\[[^\]]*src/__tests__', tc) is not None
    C.chk('T3 tests excluded (stated)', exc, 'services/auth/tsconfig.json excludes src/__tests__: %s — tsc does NOT typecheck the ks1210 / ks431 / ks451 tests; say so' % exc)
elif MODE == 'openapi':
    wgit(WT, 'checkout', '--quiet', '--detach', HEAD)
    NPM = os.environ.get('G60_NPM', 'npm')
    rc, o, e = run([NPM, 'run', 'check:openapi'], os.path.join(WT, K['install_dir']), os.path.join(OUT, 'c3_openapi_head'))
    m = re.findall(r'(\d[\d,]*)\s+example', o + e)
    C.chk('O1 check:openapi', rc == 0, 'npm run check:openapi at %s rc %d | example-block count(s) printed %s' % (HEAD[:12], rc, m or 'NONE'))
    paths = git(REPO, 'diff', '--name-only', DEV, HEAD).splitlines(); spec = [p for p in paths if re.search(K['spec_paths_rx'], p)]
    ctl = re.search(K['spec_paths_rx'], 'docs/openapi/secuura-api.yaml') is not None
    C.chk('O2 no spec path in the diff', not spec and ctl and len(paths) == len(K['files']), 'spec / YAML paths in the diff %s | CONTROL the regex matches docs/openapi/secuura-api.yaml: %s | CHECKED %d diff path(s)' % (spec or 'NONE', ctl, len(paths)))
    stt = wgit(WT, 'status', '--porcelain').strip()
    C.chk('O3 clean after', not stt, 'git status --porcelain after check:openapi %r (a generator that writes files is a finding)' % stt[:120])
wgit(WT, 'checkout', '--quiet', '--detach', HEAD)
n = C.nfail()
print('C3 %s %s: %d FAIL of %d checks | head %s' % (MODE.upper(), 'PASS' if n == 0 else 'FAIL', n, len(C.res), HEAD[:12]))
raise SystemExit(1 if n else 0)
