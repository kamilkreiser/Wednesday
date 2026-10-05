#!/usr/bin/env python3
"""c2a_ks1333_gate57.py — gate57 C2 (#1380 KS-1333), the TEST half: golden byte-identity, red BY TAMPER, the anchoring suite.
MODES
  golden   --repo <clone> [--head sha]   (no install, no network)
    G1 the new test file at HEAD is BYTE-EQUAL to the Spark golden, three ways: (a) the '+' lines of the r2 run's patch.diff (sha256 prefix
       == kit), (b) the ```ts block of the night brief KS-1333.md, (c) the '+' lines of the night brief's golden.diff; 33 lines, 2341 bytes,
       LF-terminated. FIRING CONTROL in the same run: a 1-character mutation of the head bytes differs in exactly 1 line, and a dropped
       trailing newline is NOT equal.
    G2 HEAD changes NO product file: index.ts blob at HEAD == kit product_blob_base (the test is test-only; the tamper is the red-proof).
  tamper   --repo <clone> --worktree <YOUR installed scratch worktree> [--head sha] --out <dir>
    T1 checkout --detach HEAD in the worktree (it must be clean first); the anchor line is UNIQUE in index.ts and sits at kit tamper_line;
    T2 the test file alone at HEAD: 3/3 pass (vitest JSON); T3 TAMPER index.ts:1317's Number(...) -> B1 FAILS with kit red_message, C1 and C2
       PASS, 3 cells RAN (not a load failure: a file-level error or 0 tests is a FAIL); T4 restored BY CONTENT, sha256 == before, `git status
       --porcelain` empty; T5 3/3 again after the restore.
  suite    --repo <clone> --worktree <wt> --out <dir> [--head sha]
    S1 the WHOLE anchoring vitest suite at cut_base and at HEAD (JSON): totals vs kit suite_base / suite_head; S2 the failing-test set at HEAD
       is a SUBSET of the base's (0 NEW reds) and the base's single red is kit known_red (KS 562), named.
  --selftest  the judges driven with planted vitest JSON (no install): a tamper that leaves B1 green, a load failure, C1 red too, a 2/3 run,
              a wrong red message, a new red in the suite, a lost red; the golden judge with a 1-char and a newline plant.
Every run writes each command's .out / .err / .rc and the vitest JSON into --out (a guarded dir; never under the Secuura tree). The worktree
must be YOUR scratch worktree (lib guard_scratch refuses anything under /Volumes/DevMASTER); index.ts is restored by content before exit, on
every path.
Usage: c2a_ks1333_gate57.py golden|tamper|suite --repo <clone> [--worktree wt] [--out dir] [--head sha]   |   --selftest
rc 0 PASS / 1 FAIL / 2 usage"""
import json, os, re, sys, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate57 import K, git, wgit, now, Checks, opt_factory, show_bytes, blob, sha256, guard_scratch, guard_out, run, has_commit

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A:
    print(__doc__); raise SystemExit(0 if A else 2)
opt = opt_factory(A); X = K['ks1333']; P = K['prs']['pr1']
MODE = next((m for m in ('golden', 'tamper', 'suite') if m in A), None)
REPO = opt('--repo'); WT = opt('--worktree'); OUT = opt('--out'); HEAD = opt('--head', P['ready_head']); CUT = K['cut_base']


def golden_texts():
    p = open(X['golden_patch'], 'rb').read().decode('utf-8')
    a = ('\n'.join(l[1:] for l in p.split('\n') if l.startswith('+') and not l.startswith('+++')) + '\n').encode()
    md = open(X['golden_brief_md'], encoding='utf-8').read(); m = re.findall(r'```ts\n(.*?)```', md, re.S)
    b = m[-1].encode() if len(m) == 1 else None
    gd = open(X['golden_brief_diff'], encoding='utf-8').read()
    c = ('\n'.join(l[1:] for l in gd.split('\n') if l.startswith('+') and not l.startswith('+++')) + '\n').encode()
    return p, {'r2 patch.diff + lines': a, 'brief ```ts block': b, 'brief golden.diff + lines': c}, len(m)


def judge_golden(C, h, gold, patch_text, nts):
    C.chk('G1 golden byte-equal', h is not None and all(g == h for g in gold.values()) and sha256(patch_text)[:16] == X['golden_patch_sha256_prefix']
          and h.count(b'\n') == X['golden_lines'] and len(h) == X['golden_bytes'] and h.endswith(b'\n'),
          'head %s bytes / %s lines | %s | r2 patch sha256 %s (kit %s) | brief ```ts blocks %d' % (
              len(h) if h else None, h.count(b'\n') if h else None, ' | '.join('%s == head: %s' % (k, v == h) for k, v in gold.items()),
              sha256(patch_text)[:16], X['golden_patch_sha256_prefix'], nts))
    if h:
        mut = bytearray(h); i = h.index(b'Number()'); mut[i + 1] = ord('U')
        nd = sum(1 for x, y in zip(bytes(mut).split(b'\n'), h.split(b'\n')) if x != y)
        C.chk('G1c firing control', nd == 1 and bytes(mut) != gold['r2 patch.diff + lines'] and h[:-1] != gold['r2 patch.diff + lines'],
              'a 1-character mutation differs in %d line(s) (want 1) and is unequal; the head minus its final newline is unequal: %s' % (nd, h[:-1] != gold['r2 patch.diff + lines']))


def vitest_cells(j):
    """(ran, {title: (status, first failure message)}, file-level errors)"""
    cells = {}; ferr = []
    for t in j.get('testResults', []):
        if t.get('status') == 'failed' and not t.get('assertionResults'):
            ferr.append((t.get('name'), (t.get('message') or '')[:200]))
        for a in t.get('assertionResults', []):
            cells[a['title']] = (a['status'], ((a.get('failureMessages') or ['']) + [''])[0])
    return len(cells), cells, ferr


def find(cells, prefix):
    m = [(k, v) for k, v in cells.items() if k.startswith(prefix)]
    return m[0][1] if len(m) == 1 else None


def judge_green(C, tag, j):
    ran, cells, ferr = vitest_cells(j); bad = [k for k, v in cells.items() if v[0] != 'passed']
    C.chk(tag, ran == 3 and not bad and not ferr, '%d cell(s) ran, failed %s, file-level errors %s' % (ran, bad or 'NONE', ferr or 'NONE'))


def judge_tamper(C, j):
    ran, cells, ferr = vitest_cells(j); b1 = find(cells, X['red_cell']); gs = [find(cells, g) for g in X['green_cells_under_tamper']]
    msg = re.sub(r'\x1b\[[0-9;]*m', '', b1[1]) if b1 else ''
    C.chk('T3 red BY TAMPER', ran == 3 and not ferr and b1 is not None and b1[0] == 'failed' and X['red_message'] in msg and all(g is not None and g[0] == 'passed' for g in gs),
          '%d cell(s) ran (want 3: a load failure is not a red) | file-level errors %s | B1 %s with %r (want failed with %r) | C1/C2 %s (want passed)' % (
              ran, ferr or 'NONE', b1[0] if b1 else 'ABSENT', msg.split('\n')[0][:110], X['red_message'], [g[0] if g else 'ABSENT' for g in gs]))


def suite_fails(j):
    out = set(); ferr = []
    for t in j.get('testResults', []):
        if t.get('status') == 'failed' and not t.get('assertionResults'):
            ferr.append(t.get('name', '').split('/src/')[-1])
        for a in t.get('assertionResults', []):
            if a['status'] == 'failed':
                out.add('%s :: %s' % (t.get('name', '').split('/src/')[-1], a.get('fullName') or a['title']))
    return out, ferr


def judge_suite(C, jb, jh):
    fb, eb = suite_fails(jb); fh, eh = suite_fails(jh); new = sorted(fh - fb); lost = sorted(fb - fh)
    tb = (jb.get('numTotalTests'), jb.get('numPassedTests'), jb.get('numFailedTests')); th = (jh.get('numTotalTests'), jh.get('numPassedTests'), jh.get('numFailedTests'))
    kb = X['suite_base']; kh = X['suite_head']
    C.chk('S1 suite totals', tb == (kb['tests'], kb['passed'], kb['failed']) and th == (kh['tests'], kh['passed'], kh['failed']),
          'base %s (kit %s) | head %s (kit %s) [tests, passed, failed]' % (tb, (kb['tests'], kb['passed'], kb['failed']), th, (kh['tests'], kh['passed'], kh['failed'])))
    known = all('threadTokenMint' in f for f in fb)
    C.chk('S2 no NEW reds', not new and not eh and len(fb) == 1 and known, 'NEW reds at head %s | base reds %s (kit known_red: %s) | reds lost %s | file-level errors base %s head %s' % (
        new or 'NONE', sorted(fb), X['known_red'], lost or 'NONE', eb or 'NONE', eh or 'NONE'))


def vitest(cwd, args, prefix):
    jf = prefix + '.json'
    rc, o, e = run(['npx', 'vitest', 'run'] + args + ['--reporter=json', '--outputFile=' + jf], cwd, prefix)
    try:
        return rc, json.load(open(jf))
    except Exception as ex:
        return rc, {'testResults': [{'name': 'NO JSON', 'status': 'failed', 'message': str(ex), 'assertionResults': []}]}


if '--selftest' in A:
    ok = n = 0
    def arm(name, fn, want):
        global ok, n
        buf = io.StringIO(); C = Checks()
        with contextlib.redirect_stdout(buf): fn(C)
        f = C.failed(); good = (not f) if want is None else any(x.startswith(want) for x in f)
        n += 1; ok += good; print('SELFTEST %s %s: want %s | failed %s' % ('OK' if good else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, f or 'NONE'))
        if not good: print(buf.getvalue()[:600])
    def cell(t, s, m=''):
        return {'title': t, 'fullName': t, 'status': s, 'failureMessages': [m] if m else []}
    B1 = 'RED KS-1333 B1: rowToAnchor converts'; C1 = 'CONTROL KS-1333 C1: the handler'; C2 = 'CONTROL KS-1333 C2: the lookup'
    RM = 'AssertionError: ' + X['red_message']
    J = lambda *cs: {'testResults': [{'name': '/x/src/__tests__/ks1333.test.ts', 'status': 'failed', 'assertionResults': list(cs)}]}
    arm('T-a real tamper shape', lambda C: judge_tamper(C, J(cell(B1, 'failed', RM), cell(C1, 'passed'), cell(C2, 'passed'))), None)
    arm('T-b tamper inert (B1 green)', lambda C: judge_tamper(C, J(cell(B1, 'passed'), cell(C1, 'passed'), cell(C2, 'passed'))), 'T3')
    arm('T-c load failure (0 cells)', lambda C: judge_tamper(C, {'testResults': [{'name': 'x', 'status': 'failed', 'message': 'SyntaxError', 'assertionResults': []}]}), 'T3')
    arm('T-d C1 red as well', lambda C: judge_tamper(C, J(cell(B1, 'failed', RM), cell(C1, 'failed', 'x'), cell(C2, 'passed'))), 'T3')
    arm('T-e wrong red message', lambda C: judge_tamper(C, J(cell(B1, 'failed', 'TypeError: x'), cell(C1, 'passed'), cell(C2, 'passed'))), 'T3')
    arm('T-f only 2 cells ran', lambda C: judge_tamper(C, J(cell(B1, 'failed', RM), cell(C1, 'passed'))), 'T3')
    arm('T-g green 3/3', lambda C: judge_green(C, 'T2 green', J(cell(B1, 'passed'), cell(C1, 'passed'), cell(C2, 'passed'))), None)
    arm('T-h green check sees a red', lambda C: judge_green(C, 'T2 green', J(cell(B1, 'failed', RM), cell(C1, 'passed'), cell(C2, 'passed'))), 'T2')
    kb, kh = X['suite_base'], X['suite_head']
    red = {'title': 'mint', 'fullName': 'threadTokenMint emulator round-trip', 'status': 'failed'}
    S = lambda tot, pas, fl, cs: {'numTotalTests': tot, 'numPassedTests': pas, 'numFailedTests': fl, 'testResults': [{'name': '/x/src/__tests__/threadTokenMint.test.ts', 'status': 'failed', 'assertionResults': cs}]}
    jb = S(kb['tests'], kb['passed'], kb['failed'], [red]); jh = S(kh['tests'], kh['passed'], kh['failed'], [red])
    arm('S-a real suite shape', lambda C: judge_suite(C, jb, jh), None)
    arm('S-b a NEW red at head', lambda C: judge_suite(C, jb, S(kh['tests'], kh['passed'] - 1, 2, [red, {'title': 'n', 'fullName': 'new red', 'status': 'failed'}])), 'S')
    arm('S-c head totals off by one', lambda C: judge_suite(C, jb, S(kh['tests'] - 1, kh['passed'] - 1, 1, [red])), 'S1')
    if REPO and has_commit(REPO, P['ready_head']):
        h = show_bytes(REPO, P['ready_head'], X['test']); pt, gold, nts = golden_texts()
        arm('G-a real head vs golden', lambda C: judge_golden(C, h, gold, pt, nts), None)
        arm('G-b head with a 1-char plant', lambda C: judge_golden(C, h.replace(b'Number()', b'NUmber()', 1), gold, pt, nts), 'G1')
        arm('G-c head without its final newline', lambda C: judge_golden(C, h[:-1], gold, pt, nts), 'G1')
    else:
        print('SELFTEST NOTE: golden arms need --repo <clone with #1380>; NOT RUN')
    print('SELFTEST %s %d of %d' % ('OK' if ok == n else 'BROKEN', ok, n)); raise SystemExit(0 if ok == n else 1)

if MODE is None or not REPO:
    print(__doc__); raise SystemExit(2)
for s in (HEAD, CUT):
    if not re.fullmatch(r'[0-9a-f]{40}', s) or not has_commit(REPO, s):
        print('REFUSING: %s is not a 40-hex commit present in %s' % (s, REPO)); raise SystemExit(2)
print('c2a_ks1333_gate57 %s %s | repo %s | head %s | cut_base %s' % (MODE, now(), REPO, HEAD[:12], CUT[:12]))
C = Checks()
if MODE == 'golden':
    h = show_bytes(REPO, HEAD, X['test']); pt, gold, nts = golden_texts()
    judge_golden(C, h, gold, pt, nts)
    pb = blob(REPO, HEAD, X['product'])
    C.chk('G2 no product file', pb is not None and pb[1] == X['product_blob_base'], 'index.ts at HEAD %s == base %s: %s' % (pb[1][:12] if pb else None, X['product_blob_base'][:12], pb is not None and pb[1] == X['product_blob_base']))
else:
    if not WT or not OUT:
        print('REFUSING: %s needs --worktree and --out' % MODE); raise SystemExit(2)
    WT = guard_scratch(WT, 'worktree'); OUT = guard_out(OUT)
    st = wgit(WT, 'status', '--porcelain', '--untracked-files=normal')
    if st.strip():
        print('REFUSING: the worktree is not clean:\n' + st[:600]); raise SystemExit(2)
    SD = os.path.join(WT, X['suite_dir']); PROD = os.path.join(WT, X['product']); TESTREL = os.path.relpath(os.path.join(WT, X['test']), SD)
    if MODE == 'tamper':
        wgit(WT, 'checkout', '--quiet', '--detach', HEAD)
        src = open(PROD, encoding='utf-8').read(); L = src.split('\n'); hits = [i + 1 for i, l in enumerate(L) if l == X['tamper_anchor']]
        before = sha256(src)
        C.chk('T1 anchor unique', hits == [X['tamper_line']] and wgit(WT, 'rev-parse', 'HEAD').strip() == HEAD,
              'worktree at %s | anchor %r at line(s) %s (want exactly [%d]) | index.ts sha256 %s' % (HEAD[:12], X['tamper_anchor'].strip()[:60], hits, X['tamper_line'], before[:16]))
        rc, j = vitest(SD, [TESTREL], os.path.join(OUT, 'c2a_t2_head'))
        judge_green(C, 'T2 green at head', j)
        try:
            if hits == [X['tamper_line']]:
                L[X['tamper_line'] - 1] = X['tamper_replacement']; open(PROD, 'w', encoding='utf-8').write('\n'.join(L))
                rc, j = vitest(SD, [TESTREL], os.path.join(OUT, 'c2a_t3_tamper'))
                judge_tamper(C, j)
            else:
                C.chk('T3 red BY TAMPER', False, 'NOT RUN: the anchor is not unique at the kit line')
        finally:
            open(PROD, 'w', encoding='utf-8').write(src)
        after = sha256(open(PROD, encoding='utf-8').read()); st = wgit(WT, 'status', '--porcelain')
        C.chk('T4 restored', after == before and not st.strip(), 'index.ts sha256 before %s after %s | git status --porcelain %r' % (before[:16], after[:16], st.strip()[:100]))
        rc, j = vitest(SD, [TESTREL], os.path.join(OUT, 'c2a_t5_restored'))
        judge_green(C, 'T5 green after restore', j)
    else:
        res = {}
        for name, sha in (('base', CUT), ('head', HEAD)):
            wgit(WT, 'checkout', '--quiet', '--detach', sha)
            rc, res[name] = vitest(SD, [], os.path.join(OUT, 'c2a_suite_' + name))
            print('INFO suite %s at %s rc %d | tests %s passed %s failed %s' % (name, sha[:12], rc, res[name].get('numTotalTests'), res[name].get('numPassedTests'), res[name].get('numFailedTests')))
        judge_suite(C, res['base'], res['head'])
    wgit(WT, 'checkout', '--quiet', '--detach', CUT)
n = C.nfail()
print('C2a %s %s: %d FAIL of %d checks | head %s' % (MODE.upper(), 'PASS' if n == 0 else 'FAIL', n, len(C.res), HEAD[:12]))
raise SystemExit(1 if n else 0)
