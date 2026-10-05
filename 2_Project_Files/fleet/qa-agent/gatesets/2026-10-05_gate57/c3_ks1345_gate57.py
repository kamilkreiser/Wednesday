#!/usr/bin/env python3
"""c3_ks1345_gate57.py — gate57 C3 (#1381 KS-1345, T1, a BEHAVIOUR CHANGE): exactly the described change in webhooks.ts, red-first by
assertion, the gate's own probe of BOTH described flips, the originate suite before / after, tsc with a positive control.
MODES
  shape    --repo <clone> [--head sha]   (git objects only)
    W1 webhooks.ts base -> head: the ONLY non-comment change is the list query's `.catch(... return []; })` line -> "    `;" (kit
       removed_code_line / added_code_line); every other added / removed line is a `//` comment; the comment lines carry KS-1345 (§5d);
       '.catch(' count drops by EXACTLY 1 and every other .catch line (the deliveries half :412, dispatchEvent :513) is byte-identical;
       'webhooks list query failed' 1 -> 0. FIRING CONTROL: the same judge on a planted copy that also edits the deliveries .catch FAILS.
    W2 the test file: `it(` titles base -> head differ by EXACTLY: control A0 (swallow) removed; 'RED KS-1345 A0' and 'control KS-1345 C'
       added; every other title byte-identical.
  redfirst --repo --worktree <YOUR installed scratch worktree> --out <dir> [--head sha]
    R1 worktree at cut_base, the HEAD's ks1341a test written over the base test (test section only): jest JSON -> exactly ONE failed cell,
       it is 'RED KS-1345 A0', its message shows 500 expected / 200 received, the file ran 9 cells (0 loadfail signatures: 'Test suite failed
       to run', 'Cannot find module', 'SyntaxError', 'is not a function'); the test restored BY CONTENT (sha256 == the base blob's).
    R2 worktree at HEAD: the same file 9 / 9 passed.
  probe    --repo --worktree --out [--head sha]
    Q1 the kit probe (c3_probe_ks1345_gate57.test.ts.txt) at cut_base: P1 (a rejected list query) and P2 (a NON-UUID userId, 22P02 on
       ::uuid) FAIL by assertion with 200 / {success: true, webhooks: []}; controls C1 (resolved rows) and C2 (the userId reaches the ::uuid
       bind) PASS.   Q2 at HEAD: 4 / 4 pass.  The probe file is MOVED to <out>/quarantine/ after each run (never left, never deleted).
  suite    --repo --worktree --out [--head sha]
    S1 the WHOLE originate jest suite at cut_base and HEAD: totals vs kit (1062 -> 1063, 90 suites, 0 failed); S2 failing set at HEAD is a
       subset of the base's (0 NEW reds).
  tsc      --repo --worktree --out [--head sha]
    T1 `node_modules/.bin/tsc --noEmit -p .` in services/originate at cut_base and HEAD: rc 0 both, the binary's version printed;
    T2 POSITIVE CONTROL at HEAD: a planted `const __g57: number = 'x';` appended to webhooks.ts -> rc != 0 naming TS2322; restored by
       content (sha256) and `git status --porcelain` empty; T3 tsconfig excludes src/__tests__ (the test file is NOT typechecked: said so).
  --selftest  the judges with planted jest JSON / planted webhooks.ts copies (no install): a red that is a loadfail, two reds, a green base,
              a wrong-status red, the deliveries .catch also edited, a code (non-comment) line added, a title renamed.
Usage: c3_ks1345_gate57.py shape|redfirst|probe|suite|tsc --repo <clone> [--worktree wt --out dir] [--head sha]  |  --selftest --repo <clone>
rc 0 PASS / 1 FAIL / 2 usage"""
import json, os, re, sys, io, contextlib, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate57 import K, git, wgit, now, Checks, opt_factory, show, sha256, guard_scratch, guard_out, run, has_commit, opcodes

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A:
    print(__doc__); raise SystemExit(0 if A else 2)
opt = opt_factory(A); X = K['ks1345']; P = K['prs']['pr2']
MODE = next((m for m in ('shape', 'redfirst', 'probe', 'suite', 'tsc') if m in A), None)
REPO = opt('--repo'); WT = opt('--worktree'); OUT = opt('--out'); HEAD = opt('--head', P['ready_head']); CUT = K['cut_base']
LOADFAIL = ['Test suite failed to run', 'Cannot find module', 'SyntaxError', 'is not a function']
G = os.path.dirname(os.path.abspath(__file__))


def is_comment(l):
    s = l.strip()
    return s.startswith('//') or s == ''


def judge_shape(C, b, h):
    bl, hl = b.split('\n'), h.split('\n'); ops = opcodes(bl, hl)
    rem = [bl[i] for op, i1, i2, j1, j2 in ops for i in range(i1, i2)]; add = [hl[j] for op, i1, i2, j1, j2 in ops for j in range(j1, j2)]
    code_rem = [l for l in rem if not is_comment(l)]; code_add = [l for l in add if not is_comment(l)]
    com_add = [l for l in add if is_comment(l) and l.strip()]
    cb = [l for l in bl if '.catch(' in l]; ch = [l for l in hl if '.catch(' in l]
    others_same = [l for l in cb if l != X['removed_code_line']] == ch
    C.chk('W1 webhooks.ts exactly the described change', code_rem == [X['removed_code_line']] and code_add == [X['added_code_line']] and len(cb) == len(ch) + 1 and others_same
          and b.count('webhooks list query failed') == 1 and h.count('webhooks list query failed') == 0 and any('KS-1345' in l for l in com_add),
          'non-comment lines removed %r | added %r | comment lines added %d (carry KS-1345: %s) | .catch( lines %d -> %d, every other .catch line byte-identical and in order: %s | "webhooks list query failed" %d -> %d' % (
              [l.strip()[:70] for l in code_rem], [l.strip()[:30] for l in code_add], len(com_add), any('KS-1345' in l for l in com_add), len(cb), len(ch), others_same,
              b.count('webhooks list query failed'), h.count('webhooks list query failed')))
    for l in rem: print('INFO W1 - %s' % l.rstrip()[:150])
    for l in add: print('INFO W1 + %s' % l.rstrip()[:150])


def titles(src):
    return re.findall(r"(?m)^\s*it(?:\.each\([^)]*\))?\(\s*'([^']+)'", src)


def judge_titles(C, b, h):
    tb, th = titles(b), titles(h); rem = [t for t in tb if t not in th]; add = [t for t in th if t not in tb]
    ok = len(rem) == 1 and rem[0].startswith('control KS-1341 A0') and sorted(t.split(':')[0] for t in add) == ['RED KS-1345 A0', 'control KS-1345 C']
    C.chk('W2 test titles', ok and len(tb) == len(th) - 1, '`it(` titles %d -> %d | removed %s | added %s' % (len(tb), len(th), [t[:50] for t in rem], [t[:50] for t in add]))


def jest_cells(j):
    cells = {}; ferr = []
    for t in j.get('testResults', []):
        msg = t.get('message') or ''
        if t.get('status') == 'failed' and (not t.get('assertionResults') or any(s in msg for s in LOADFAIL)):
            ferr.append((t.get('name', '').split('/src/')[-1], msg[:200]))
        for a in t.get('assertionResults', []):
            cells[a.get('fullName') or a['title']] = (a['status'], re.sub(r'\x1b\[[0-9;]*m', '', ((a.get('failureMessages') or ['']) + [''])[0]))
    return cells, ferr


def judge_red(C, j):
    cells, ferr = jest_cells(j); red = [(k, v) for k, v in cells.items() if v[0] == 'failed']
    one = len(red) == 1 and X['red_cell'] in red[0][0]; m = red[0][1][1] if red else ''
    s500 = re.search(r'"?status"?:\s*500', m) is not None and re.search(r'"?status"?:\s*200', m) is not None
    C.chk('R1 red-first BY ASSERTION at base', one and s500 and not ferr and len(cells) == X['test_cells_head'],
          '%d cell(s) ran (want %d) | failed %s (want exactly [%s]) | message shows 500 expected AND 200 received: %s | loadfail signatures %s' % (
              len(cells), X['test_cells_head'], [k[-60:] for k, v in red], X['red_cell'], s500, ferr or 'NONE'))


def judge_green(C, tag, j, n):
    cells, ferr = jest_cells(j); bad = [k for k, v in cells.items() if v[0] != 'passed']
    C.chk(tag, len(cells) == n and not bad and not ferr, '%d cell(s) ran (want %d) | not passed %s | loadfail %s' % (len(cells), n, [b[-60:] for b in bad] or 'NONE', ferr or 'NONE'))


def judge_probe_base(C, j):
    cells, ferr = jest_cells(j); st = {k.split('gate57 ')[-1][:2]: v for k, v in cells.items()}
    p_red = all(st.get(p, ('absent',))[0] == 'failed' and re.search(r'"?status"?:\s*200', st[p][1]) and 'webhooks' in st[p][1] for p in ('P1', 'P2'))
    c_ok = all(st.get(c, ('absent',))[0] == 'passed' for c in ('C1', 'C2'))
    C.chk('Q1 probe at base', len(cells) == 4 and p_red and c_ok and not ferr, 'cells %s | P1 / P2 red BY ASSERTION with 200 and an empty webhooks list: %s | controls C1 / C2 green: %s | loadfail %s' % (
        {k: v[0] for k, v in st.items()}, bool(p_red), c_ok, ferr or 'NONE'))
    for k, v in st.items():
        if v[0] == 'failed': print('INFO Q1 %s received: %s' % (k, ' '.join(v[1].split())[:240]))


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
    fb, eb = suite_fails(jb); fh, eh = suite_fails(jh); kb, kh = X['suite_base'], X['suite_head']
    tb = (jb.get('numTotalTests'), jb.get('numFailedTests'), jb.get('numTotalTestSuites')); th = (jh.get('numTotalTests'), jh.get('numFailedTests'), jh.get('numTotalTestSuites'))
    C.chk('S1 suite totals', tb == (kb['tests'], kb['failed'], kb['suites']) and th == (kh['tests'], kh['failed'], kh['suites']),
          'base %s (kit %s) | head %s (kit %s) [tests, failed, suites]' % (tb, (kb['tests'], kb['failed'], kb['suites']), th, (kh['tests'], kh['failed'], kh['suites'])))
    C.chk('S2 no NEW reds', not (fh - fb) and not eh, 'NEW reds at head %s | base reds %s | runtime-error suites base %s head %s' % (sorted(fh - fb) or 'NONE', sorted(fb) or 'NONE', eb or 'NONE', eh or 'NONE'))


def jest(cwd, args, prefix):
    jf = prefix + '.json'
    rc, o, e = run(['npx', 'jest'] + args + ['--json', '--outputFile=' + jf], cwd, prefix)
    try:
        return rc, json.load(open(jf))
    except Exception as ex:
        return rc, {'testResults': [{'name': 'NO JSON', 'status': 'failed', 'message': 'Test suite failed to run: ' + str(ex), 'assertionResults': []}]}


if '--selftest' in A:
    ok = n = 0
    def arm(name, fn, want):
        global ok, n
        buf = io.StringIO(); C = Checks()
        with contextlib.redirect_stdout(buf): fn(C)
        f = C.failed(); good = (not f) if want is None else any(x.startswith(want) for x in f)
        n += 1; ok += good; print('SELFTEST %s %s: want %s | failed %s' % ('OK' if good else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, f or 'NONE'))
        if not good: print(buf.getvalue()[:800])
    def cell(t, s, m=''):
        return {'title': t, 'fullName': t, 'status': s, 'failureMessages': [m] if m else []}
    RM = 'expect(received).toEqual(expected)\n- "status": 500,\n+ "status": 200,'
    J = lambda cs, msg='': {'testResults': [{'name': '/x/src/__tests__/ks1341a.test.ts', 'status': 'failed' if any(c['status'] == 'failed' for c in cs) else 'passed', 'message': msg, 'assertionResults': cs}]}
    g8 = [cell('KS-1341 part A cell %d' % i, 'passed') for i in range(8)]
    arm('R-a real red shape', lambda C: judge_red(C, J(g8 + [cell('KS-1341 part A RED KS-1345 A0: a REJECTED list query', 'failed', RM)])), None)
    arm('R-b loadfail', lambda C: judge_red(C, {'testResults': [{'name': 'x', 'status': 'failed', 'message': 'Test suite failed to run\nCannot find module', 'assertionResults': []}]}), 'R1')
    arm('R-c two reds', lambda C: judge_red(C, J(g8[:7] + [cell('A1 x', 'failed', RM), cell('RED KS-1345 A0: x', 'failed', RM)])), 'R1')
    arm('R-d green at base (no red)', lambda C: judge_red(C, J(g8 + [cell('RED KS-1345 A0: x', 'passed')])), 'R1')
    arm('R-e red for the wrong reason (a 404)', lambda C: judge_red(C, J(g8 + [cell('RED KS-1345 A0: x', 'failed', '- "status": 500,\n+ "status": 404,')])), 'R1')
    arm('R-f 9/9 green at head', lambda C: judge_green(C, 'R2 green', J(g8 + [cell('RED KS-1345 A0: x', 'passed')]), 9), None)
    PB = lambda p1, p2, c1='passed': J([cell('gate57 probe gate57 P1: rejected', p1, '- "status": 500 + "status": 200, "webhooks": []' if p1 == 'failed' else ''),
                                      cell('gate57 probe gate57 P2: non-uuid', p2, '- "status": 500 + "status": 200, "webhooks": []' if p2 == 'failed' else ''),
                                      cell('gate57 probe gate57 C1 (control', c1), cell('gate57 probe gate57 C2 (control', 'passed')])
    arm('Q-a probe base shape', lambda C: judge_probe_base(C, PB('failed', 'failed')), None)
    arm('Q-b P2 already green at base (no flip)', lambda C: judge_probe_base(C, PB('failed', 'passed')), 'Q1')
    arm('Q-c control C1 red at base', lambda C: judge_probe_base(C, PB('failed', 'failed', 'failed')), 'Q1')
    if REPO and has_commit(REPO, P['ready_head']):
        b = show(REPO, CUT, X['product']); h = show(REPO, P['ready_head'], X['product'])
        tb = show(REPO, CUT, X['test']); th = show(REPO, P['ready_head'], X['test'])
        dl = [l for l in b.split('\n') if '.catch(' in l and l != X['removed_code_line']][0]
        arm('W-a real webhooks.ts', lambda C: judge_shape(C, b, h), None)
        arm('W-b the deliveries .catch also removed', lambda C: judge_shape(C, b, h.replace(dl, dl.split('.catch(')[0] + ';', 1)), 'W1')
        arm('W-c a code line added (a status change elsewhere)', lambda C: judge_shape(C, b, h.replace("res.json({ success: true, webhooks: rows });", "res.status(200).json({ success: true, webhooks: rows });", 1)), 'W1')
        arm('W-d the .catch kept (no behaviour change)', lambda C: judge_shape(C, b, b.replace('// no operator).', '// no operator). KS-1345 note', 1)), 'W1')
        arm('W-e real test titles', lambda C: judge_titles(C, tb, th), None)
        arm('W-f another title renamed', lambda C: judge_titles(C, tb, th.replace("'RED KS-1341 A2", "'RED KS-1341 A2x", 1)), 'W2')
    else:
        print('SELFTEST NOTE: the W arms need --repo <clone with #1381>; NOT RUN')
    print('SELFTEST %s %d of %d' % ('OK' if ok == n else 'BROKEN', ok, n)); raise SystemExit(0 if ok == n else 1)

if MODE is None or not REPO:
    print(__doc__); raise SystemExit(2)
for s in (HEAD, CUT):
    if not re.fullmatch(r'[0-9a-f]{40}', s) or not has_commit(REPO, s):
        print('REFUSING: %s is not a 40-hex commit present in %s' % (s, REPO)); raise SystemExit(2)
print('c3_ks1345_gate57 %s %s | repo %s | head %s | cut_base %s' % (MODE, now(), REPO, HEAD[:12], CUT[:12]))
C = Checks()
if MODE == 'shape':
    judge_shape(C, show(REPO, CUT, X['product']), show(REPO, HEAD, X['product']))
    judge_titles(C, show(REPO, CUT, X['test']), show(REPO, HEAD, X['test']))
else:
    if not WT or not OUT:
        print('REFUSING: %s needs --worktree and --out' % MODE); raise SystemExit(2)
    WT = guard_scratch(WT, 'worktree'); OUT = guard_out(OUT)
    if wgit(WT, 'status', '--porcelain').strip():
        print('REFUSING: the worktree is not clean'); raise SystemExit(2)
    SD = os.path.join(WT, X['suite_dir']); TPATH = os.path.join(WT, X['test']); TREL = os.path.relpath(TPATH, SD)
    if MODE == 'redfirst':
        wgit(WT, 'checkout', '--quiet', '--detach', CUT); base_src = open(TPATH, encoding='utf-8').read()
        try:
            open(TPATH, 'w', encoding='utf-8').write(show(REPO, HEAD, X['test']))
            rc, j = jest(SD, [TREL], os.path.join(OUT, 'c3_r1_base_plus_test'))
            judge_red(C, j)
        finally:
            open(TPATH, 'w', encoding='utf-8').write(base_src)
        rest = sha256(open(TPATH, encoding='utf-8').read()) == sha256(show(REPO, CUT, X['test']))
        st = wgit(WT, 'status', '--porcelain').strip()
        C.chk('R1b restored', rest and not st, 'the base test restored by content == the base blob: %s | git status --porcelain %r' % (rest, st[:100]))
        wgit(WT, 'checkout', '--quiet', '--detach', HEAD)
        rc, j = jest(SD, [TREL], os.path.join(OUT, 'c3_r2_head'))
        judge_green(C, 'R2 green at head', j, X['test_cells_head'])
    elif MODE == 'probe':
        PR = os.path.join(SD, 'src', '__tests__', X['probe_name']); Q = os.path.join(OUT, 'quarantine'); os.makedirs(Q, exist_ok=True)
        for name, sha in (('base', CUT), ('head', HEAD)):
            wgit(WT, 'checkout', '--quiet', '--detach', sha)
            shutil.copyfile(os.path.join(G, X['probe_template']), PR)
            try:
                rc, j = jest(SD, [os.path.relpath(PR, SD)], os.path.join(OUT, 'c3_probe_' + name))
            finally:
                os.replace(PR, os.path.join(Q, '%s.%s.%s' % (X['probe_name'], name, now().replace(':', ''))))
            if name == 'base': judge_probe_base(C, j)
            else: judge_green(C, 'Q2 probe at head', j, 4)
        st = wgit(WT, 'status', '--porcelain').strip()
        C.chk('Q3 probe moved out', not st and not os.path.exists(PR), 'git status --porcelain %r | probe still in the worktree: %s | quarantined copies in %s' % (st[:100], os.path.exists(PR), Q))
    elif MODE == 'suite':
        res = {}
        for name, sha in (('base', CUT), ('head', HEAD)):
            wgit(WT, 'checkout', '--quiet', '--detach', sha)
            rc, res[name] = jest(SD, [], os.path.join(OUT, 'c3_suite_' + name))
            print('INFO suite %s at %s rc %d | tests %s failed %s suites %s' % (name, sha[:12], rc, res[name].get('numTotalTests'), res[name].get('numFailedTests'), res[name].get('numTotalTestSuites')))
        judge_suite(C, res['base'], res['head'])
    elif MODE == 'tsc':
        TD = os.path.join(WT, X['tsc_dir']); TSC = None
        for d in (os.path.join(TD, 'node_modules', '.bin', 'tsc'), os.path.join(WT, 'Blockchain', 'Dev', 'node_modules', '.bin', 'tsc')):
            if os.path.exists(d): TSC = d; break
        if not TSC:
            print('REFUSING: no tsc binary in the worktree node_modules (install first)'); raise SystemExit(2)
        ver = run([TSC, '--version'], TD, None)[1].strip(); rcs = {}
        for name, sha in (('base', CUT), ('head', HEAD)):
            wgit(WT, 'checkout', '--quiet', '--detach', sha)
            rcs[name] = run([TSC, '--noEmit', '-p', '.'], TD, os.path.join(OUT, 'c3_tsc_' + name))[0]
        C.chk('T1 tsc rc 0 base and head', rcs == {'base': 0, 'head': 0}, '%s (%s) | rc base %d head %d' % (TSC, ver, rcs['base'], rcs['head']))
        PF = os.path.join(WT, X['product']); src = open(PF, encoding='utf-8').read(); before = sha256(src)
        try:
            open(PF, 'w', encoding='utf-8').write(src + "\nconst __g57: number = 'x';\n")
            rc, o, e = run([TSC, '--noEmit', '-p', '.'], TD, os.path.join(OUT, 'c3_tsc_positive_control'))
        finally:
            open(PF, 'w', encoding='utf-8').write(src)
        st = wgit(WT, 'status', '--porcelain').strip()
        C.chk('T2 positive control', rc != 0 and 'TS2322' in o + e and sha256(open(PF, encoding='utf-8').read()) == before and not st,
              'planted TS2322 -> rc %d, TS2322 printed: %s | restored by content sha256 %s | git status %r' % (rc, 'TS2322' in o + e, before[:16], st[:80]))
        tc = open(os.path.join(TD, 'tsconfig.json'), encoding='utf-8').read(); exc = re.search(r'"exclude"\s*:\s*\[[^\]]*src/__tests__', tc) is not None
        C.chk('T3 tests excluded (stated)', exc, 'services/originate/tsconfig.json excludes src/__tests__: %s — so tsc does NOT typecheck the changed test file (ts-jest does at run time); say so' % exc)
    wgit(WT, 'checkout', '--quiet', '--detach', CUT)
n = C.nfail()
print('C3 %s %s: %d FAIL of %d checks | head %s' % (MODE.upper(), 'PASS' if n == 0 else 'FAIL', n, len(C.res), HEAD[:12]))
raise SystemExit(1 if n else 0)
