#!/usr/bin/env python3
"""c3_tests_gate65.py — gate65 C3 (#1393 KS-1278, T1): red-first BY ASSERTION at the base, green at the head, ONE TAMPER PER CONJUNCT
(the builder's table) plus the gate's own blind-spot probes, the originate suite before / after, tsc with a positive control.
Every mode runs jest IN THE GATE'S OWN INSTALLED SCRATCH WORKTREE (npm ci --ignore-scripts + build packages/shared, X1) — never the
builder's worktree, never the shared checkout (refused: the worktree must lie outside !CODING).
MODES
  redfirst --repo <clone> --worktree <wt> --out <dir>
    R1 worktree at the BASE 32e058975d4e with BOTH of the head's test files written over it (the new ks1278 file + the head's ks1293
       register) and NEITHER product hunk: ks1278 executes EXACTLY 4 cells, R1 and R2 FAILED BY ASSERTION, C1 and C2 PASSED, 0 load-
       failure signatures; ks1293 10 / 10 passed (its manifest names the new file, so MANIFEST-DRIFT stays green)
    R1b restored by CONTENT: ks1293 == the base blob (sha256), the ks1278 file MOVED to <out>/quarantine/ (never deleted),
       `git status --porcelain` empty
    R2 worktree at the HEAD: ks1278 + ks1293 = 14 / 14 passed
  tamper   --repo --worktree --out [--only T1,T2,…]
    for each kit tamper ALONE at the HEAD: LANDED (the `from` text occurs exactly once before, 0 times after; the file's sha256 changed);
    ks1278 executes 4 cells; the FAILED set == the kit's `reddens` for that tamper EXACTLY (T1/T2 -> R2, T3 -> C2, T4 -> R1: the
    builder's table; T6 -> R1: the route ignoring the null); then restored by content and status clean.
    T5 is the GATE'S BLIND-SPOT PROBE: the guard made a no-op (`TRUE OR …`) while its text survives — the kit EXPECTS 0 reds (the cells
    pin SQL TEXT, not SQL semantics); a 0 here is a finding about the instrument, not a pass of the product. The gate rules it.
  suite    --repo --worktree --out
    S1 the WHOLE originate jest suite at the BASE and the HEAD: totals vs the claim (90 / 1063 -> 91 / 1067, 0 failed both ends);
    S2 the failing set at the head is a subset of the base's (0 NEW reds); the delta is +1 suite / +4 tests
  tsc      --repo --worktree --out
    T1 `tsc --noEmit -p .` in services/originate at BASE and HEAD rc 0, version printed; T2 POSITIVE CONTROL: a planted TS2322 in
    documentRepo.ts -> rc != 0 naming TS2322, restored by content, status clean; T3 whether tsconfig excludes src/__tests__ (said so)
  --selftest [--repo <clone>]   the judges on planted jest JSON (a loadfail, 3 reds, a green base, a C2 red at base, a wrong-cell tamper
              red, 5 executed, a T5 that reddens) + (with --repo) every kit tamper's `from` occurs EXACTLY once in the real head blob and
              its application changes the bytes.
Usage: c3_tests_gate65.py redfirst|tamper|suite|tsc --repo <clone> --worktree <wt> --out <dir>  |  --selftest [--repo <clone>]
rc 0 PASS / 1 FAIL / 2 usage or refused."""
import hashlib, json, os, re, shutil, subprocess, sys, io, contextlib
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate65 import K, git, wgit, Tally, outside_forbidden

LOADFAIL = ['Test suite failed to run', 'Cannot find module', 'SyntaxError', 'is not a function']
CELLS = K['cells']; CL = K['claims']
T1278 = os.path.basename(K['test']); T1293 = os.path.basename(K['manifest_test'])


def now(): return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def sha256(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()


def run(cmd, cwd, prefix):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if prefix:
        open(prefix + '.out', 'w').write(p.stdout); open(prefix + '.err', 'w').write(p.stderr); open(prefix + '.rc', 'w').write('%d\n' % p.returncode)
    return p.returncode, p.stdout, p.stderr


def cells(j):
    out = {}; ferr = []
    for t in j.get('testResults', []):
        msg = t.get('message') or ''; name = os.path.basename(t.get('name', ''))
        if t.get('status') == 'failed' and (not t.get('assertionResults') or any(s in msg for s in LOADFAIL)):
            ferr.append((name, msg[:160]))
        for a in t.get('assertionResults', []):
            out[(name, a.get('fullName') or a['title'])] = (a['status'], re.sub(r'\x1b\[[0-9;]*m', '', ((a.get('failureMessages') or ['']) + [''])[0]))
    return out, ferr


def by_cell(cs, fname):
    r = {}
    for (f, title), v in cs.items():
        if f != fname: continue
        for k, pre in CELLS.items():
            if pre in title: r[k] = v
    return r


def judge_redfirst(t, j):
    cs, ferr = cells(j); c = by_cell(cs, T1278); n1278 = sum(1 for (f, _) in cs if f == T1278)
    reds = sorted(k for k, v in c.items() if v[0] == 'failed'); greens = sorted(k for k, v in c.items() if v[0] == 'passed')
    asrt = all('expect(' in c[k][1] or 'Expected' in c[k][1] for k in reds)
    m1293 = [v[0] for (f, _), v in cs.items() if f == T1293]
    t.check('R1', n1278 == 4 and reds == ['R1', 'R2'] and greens == ['C1', 'C2'] and asrt and not ferr and len(m1293) == K['manifest_cells'] and all(s == 'passed' for s in m1293),
            'ks1278 executed %d (want 4) | red %s (want [R1, R2]) by assertion %s | green %s (want [C1, C2]) | ks1293 %d cells, all passed %s (want %d) | loadfail %s' % (
                n1278, reds, asrt, greens, len(m1293), all(s == 'passed' for s in m1293), K['manifest_cells'], ferr or 'NONE'))
    for k in reds: t.info('R1-' + k, ' '.join(c[k][1].split())[:220])


def judge_green(t, tag, j, n):
    cs, ferr = cells(j); bad = [k for k, v in cs.items() if v[0] != 'passed']
    t.check(tag, len(cs) == n and not bad and not ferr, '%d cell(s) ran (want %d) | not passed %s | loadfail %s' % (len(cs), n, [b[1][-50:] for b in bad] or 'NONE', ferr or 'NONE'))


def judge_tamper(t, tid, j, want):
    cs, ferr = cells(j); c = by_cell(cs, T1278); n = sum(1 for (f, _) in cs if f == T1278)
    reds = sorted(k for k, v in c.items() if v[0] == 'failed')
    t.check(tid, n == 4 and reds == sorted(want) and not ferr, '%s: executed %d (want 4) | red %s (want exactly %s) | loadfail %s' % (
        K['tampers'][tid]['what'], n, reds, sorted(want) or 'NONE (blind-spot probe)', ferr or 'NONE'))


def judge_suite(t, jb, jh):
    tb = (jb.get('numTotalTestSuites'), jb.get('numTotalTests'), jb.get('numFailedTests')); th = (jh.get('numTotalTestSuites'), jh.get('numTotalTests'), jh.get('numFailedTests'))
    kb = tuple(CL['suite_base'][x] for x in ('suites', 'tests', 'failed')); kh = tuple(CL['suite_head'][x] for x in ('suites', 'tests', 'failed'))
    t.check('S1', tb == kb and th == kh, 'base %s (claim %s) | head %s (claim %s) [suites, tests, failed]' % (tb, kb, th, kh))
    fb = {k for k, v in cells(jb)[0].items() if v[0] == 'failed'}; fh = {k for k, v in cells(jh)[0].items() if v[0] == 'failed'}
    t.check('S2', not (fh - fb) and not cells(jh)[1], 'NEW reds at head %s | base reds %d | load failures at head %s' % (sorted(x[1][:50] for x in fh - fb) or 'NONE', len(fb), cells(jh)[1] or 'NONE'))


def jest(cwd, args, prefix):
    jf = prefix + '.json'
    rc, o, e = run(['npx', 'jest'] + args + ['--json', '--outputFile=' + jf], cwd, prefix)
    try:
        return rc, json.load(open(jf))
    except Exception as ex:
        return rc, {'testResults': [{'name': 'NO JSON', 'status': 'failed', 'message': 'Test suite failed to run: ' + str(ex), 'assertionResults': []}]}


def apply_tamper(src, tp):
    a = tp['from']
    return src.count(a), src.replace(a, tp['to'], 1)


def selftest(repo):
    ok = n = 0
    def arm(name, fn, want):
        nonlocal ok, n
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): fn(t)
        good = (not t.fails) if want is None else (want in t.fails)
        n += 1; ok += good; print('SELFTEST %s %s: want %s | failed %s' % ('OK' if good else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, t.fails or 'NONE'))
    def cell(title, s, m=''): return {'title': title, 'fullName': 'KS-1278 /revoke is one atomic transition ' + title, 'status': s, 'failureMessages': [m] if m else []}
    EM = 'expect(received).toEqual(expected)\nExpected [400,"BAD_REQUEST",0]\nReceived [200,null,1]'
    def J(c1278, n1293=10, s1293='passed', msg=''):
        return {'testResults': [{'name': '/w/src/__tests__/' + T1278, 'status': 'failed' if any(c['status'] == 'failed' for c in c1278) else 'passed', 'message': msg, 'assertionResults': c1278},
                                {'name': '/w/src/__tests__/' + T1293, 'status': 'passed', 'message': '', 'assertionResults': [cell('manifest %d' % i, s1293) for i in range(n1293)]}]}
    R1, R2, C1, C2 = [CELLS[k] + ': x' for k in ('R1', 'R2', 'C1', 'C2')]
    good = [cell(R1, 'failed', EM), cell(R2, 'failed', EM), cell(C1, 'passed'), cell(C2, 'passed')]
    arm('RF-a the real red-first shape', lambda t: judge_redfirst(t, J(good)), None)
    arm('RF-b a LOAD failure (0 cells)', lambda t: judge_redfirst(t, {'testResults': [{'name': '/w/' + T1278, 'status': 'failed', 'message': 'Test suite failed to run\nCannot find module @secuura/shared', 'assertionResults': []}]}), 'R1')
    arm('RF-c C2 red at base too', lambda t: judge_redfirst(t, J(good[:3] + [cell(C2, 'failed', EM)])), 'R1')
    arm('RF-d R2 green at base (no red)', lambda t: judge_redfirst(t, J([good[0], cell(R2, 'passed')] + good[2:])), 'R1')
    arm('RF-e 5 cells executed', lambda t: judge_redfirst(t, J(good + [cell('extra', 'passed')])), 'R1')
    arm('RF-f ks1293 MANIFEST-DRIFT red', lambda t: judge_redfirst(t, J(good, 10, 'failed')), 'R1')
    arm('G-a 14/14 green', lambda t: judge_green(t, 'R2', J([dict(c, status='passed', failureMessages=[]) for c in good]), 14), None)
    arm('G-b 13 cells', lambda t: judge_green(t, 'R2', J([dict(c, status='passed', failureMessages=[]) for c in good], 9), 14), 'R2')
    G4 = [cell(R1, 'passed'), cell(R2, 'passed'), cell(C1, 'passed'), cell(C2, 'passed')]
    arm('TM-a T3 reddens exactly C2', lambda t: judge_tamper(t, 'T3', J(G4[:3] + [cell(C2, 'failed', EM)]), ['C2']), None)
    arm('TM-b T3 reddens C2 AND R1 (not exact)', lambda t: judge_tamper(t, 'T3', J([cell(R1, 'failed', EM)] + G4[1:3] + [cell(C2, 'failed', EM)]), ['C2']), 'T3')
    arm('TM-c T1 reddens nothing (the cell is blind)', lambda t: judge_tamper(t, 'T1', J(G4), ['R2']), 'T1')
    arm('TM-d T5 blind-spot probe: 0 reds expected', lambda t: judge_tamper(t, 'T5', J(G4), []), None)
    arm('TM-e T5 reddens R2 (the probe disagrees with the kit)', lambda t: judge_tamper(t, 'T5', J([G4[0], cell(R2, 'failed', EM)] + G4[2:]), []), 'T5')
    SB = {'numTotalTestSuites': 90, 'numTotalTests': 1063, 'numFailedTests': 0, 'testResults': []}; SH = {'numTotalTestSuites': 91, 'numTotalTests': 1067, 'numFailedTests': 0, 'testResults': []}
    arm('S-a the claimed totals', lambda t: judge_suite(t, SB, SH), None)
    arm('S-b head 1066 tests', lambda t: judge_suite(t, SB, dict(SH, numTotalTests=1066)), 'S1')
    arm('S-c a NEW red at head', lambda t: judge_suite(t, SB, dict(SH, testResults=[{'name': '/w/x.test.ts', 'status': 'failed', 'message': '', 'assertionResults': [cell('y', 'failed', EM)]}])), 'S2')
    if repo:
        for tid, tp in K['tampers'].items():
            src = git(repo, 'show', '%s:%s' % (K['head'], tp['file'])); cnt, new = apply_tamper(src, tp)
            g = cnt == 1 and new != src
            n += 1; ok += g
            print('SELFTEST %s tamper %s lands on the REAL head %s: `from` occurs %d (want 1), bytes change %s' % ('OK' if g else 'MISS', tid, os.path.basename(tp['file']), cnt, new != src))
    else:
        print('SELFTEST NOTE: the tamper-landing arms need --repo <clone with the head>; NOT RUN')
    print('SELFTEST %s %d of %d' % ('OK' if ok == n else 'BROKEN', ok, n)); print('CHECKED %d arm(s)' % n)
    return 0 if ok == n else 1


def main():
    A = sys.argv[1:]
    if not A or '--help' in A or '-h' in A: print(__doc__); return 0 if A else 2
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    if '--selftest' in A: return selftest(opt('--repo'))
    MODE = next((m for m in ('redfirst', 'tamper', 'suite', 'tsc') if m in A), None)
    REPO, WT, OUT = opt('--repo'), opt('--worktree'), opt('--out')
    if not (MODE and REPO and WT and OUT): print(__doc__); return 2
    for s in (K['head'], K['base']):
        if git(REPO, 'rev-parse', '--verify', '--quiet', s + '^{commit}', check=False)[0] != 0:
            print('REFUSED: %s unresolvable in %s — fetch it by sha into YOUR clone (X7)' % (s, REPO)); return 2
    if not outside_forbidden(WT) or not outside_forbidden(OUT):
        print('REFUSED: the worktree / out dir must lie OUTSIDE %s (your own scratch)' % K['forbidden_root']); return 2
    os.makedirs(OUT, exist_ok=True); Q = os.path.join(OUT, 'quarantine'); os.makedirs(Q, exist_ok=True)
    if wgit(WT, 'status', '--porcelain')[1].strip():
        print('REFUSED: the worktree is not clean'); return 2
    if not os.path.exists(os.path.join(WT, 'Blockchain/Dev/packages/shared/dist/index.js')):
        print('REFUSED: packages/shared/dist/index.js absent in the worktree — `npm ci --ignore-scripts` + `npm run build --workspace=packages/shared` first (X1); a missing dist is a LOAD failure, not a red'); return 2
    print('c3_tests_gate65 %s %s | repo %s | wt %s | head %s | base %s' % (MODE, now(), REPO, WT, K['head'][:12], K['base'][:12]))
    SD = os.path.join(WT, K['suite_dir']); rel = lambda p: os.path.relpath(os.path.join(WT, p), SD)
    T = Tally(); co = lambda sha: wgit(WT, 'checkout', '--quiet', '--detach', sha)
    if MODE == 'redfirst':
        co(K['base']); p78 = os.path.join(WT, K['test']); p93 = os.path.join(WT, K['manifest_test'])
        base93 = open(p93, encoding='utf-8').read(); assert not os.path.exists(p78), 'ks1278 already present at base'
        try:
            open(p78, 'w', encoding='utf-8').write(git(REPO, 'show', '%s:%s' % (K['head'], K['test'])))
            open(p93, 'w', encoding='utf-8').write(git(REPO, 'show', '%s:%s' % (K['head'], K['manifest_test'])))
            landed = sha256(open(p78, encoding='utf-8').read()) == sha256(git(REPO, 'show', '%s:%s' % (K['head'], K['test'])))
            print('INFO overlay landed: ks1278 == head blob %s; product at base: documentRepo sha256 %s' % (landed, sha256(open(os.path.join(WT, K['repo_file']), encoding='utf-8').read())[:16]))
            rc, j = jest(SD, [rel(K['test']), rel(K['manifest_test'])], os.path.join(OUT, 'c3_redfirst_base'))
            print('INFO jest rc %d at base+tests' % rc); judge_redfirst(T, j)
        finally:
            open(p93, 'w', encoding='utf-8').write(base93)
            if os.path.exists(p78): shutil.move(p78, os.path.join(Q, T1278 + '.redfirst.' + now().replace(':', '')))
        st = wgit(WT, 'status', '--porcelain')[1].strip()
        T.check('R1b', sha256(open(p93, encoding='utf-8').read()) == sha256(git(REPO, 'show', '%s:%s' % (K['base'], K['manifest_test']))) and not os.path.exists(p78) and not st,
                'ks1293 restored == base blob; ks1278 moved to %s; git status --porcelain %r' % (Q, st[:80]))
        co(K['head']); rc, j = jest(SD, [rel(K['test']), rel(K['manifest_test'])], os.path.join(OUT, 'c3_green_head'))
        judge_green(T, 'R2', j, CL['green_cells'])
    elif MODE == 'tamper':
        co(K['head']); only = (opt('--only') or ','.join(K['tampers'])).split(',')
        for tid in only:
            tp = K['tampers'][tid]; pf = os.path.join(WT, tp['file']); src = open(pf, encoding='utf-8').read()
            cnt, new = apply_tamper(src, tp)
            try:
                open(pf, 'w', encoding='utf-8').write(new)
                landed = cnt == 1 and sha256(open(pf, encoding='utf-8').read()) != sha256(src)
                T.check(tid + '-landed', landed, '`from` occurred %d time(s) before (want 1); file sha256 %s -> %s' % (cnt, sha256(src)[:12], sha256(new)[:12]))
                rc, j = jest(SD, [rel(K['test'])], os.path.join(OUT, 'c3_tamper_' + tid))
                judge_tamper(T, tid, j, tp['reddens'])
            finally:
                open(pf, 'w', encoding='utf-8').write(src)
            st = wgit(WT, 'status', '--porcelain')[1].strip()
            T.check(tid + '-restored', sha256(open(pf, encoding='utf-8').read()) == sha256(src) and not st, 'restored by content; status %r' % st[:80])
        rc, j = jest(SD, [rel(K['test'])], os.path.join(OUT, 'c3_tamper_restored'))
        judge_green(T, 'TR', j, 4)
    elif MODE == 'suite':
        res = {}
        for name, sha in (('base', K['base']), ('head', K['head'])):
            co(sha); rc, res[name] = jest(SD, [], os.path.join(OUT, 'c3_suite_' + name))
            print('INFO suite %s at %s rc %d | suites %s tests %s failed %s' % (name, sha[:12], rc, res[name].get('numTotalTestSuites'), res[name].get('numTotalTests'), res[name].get('numFailedTests')))
        judge_suite(T, res['base'], res['head'])
    elif MODE == 'tsc':
        TD = os.path.join(WT, K['tsc_dir']); TSC = next((d for d in (os.path.join(TD, 'node_modules/.bin/tsc'), os.path.join(WT, 'Blockchain/Dev/node_modules/.bin/tsc')) if os.path.exists(d)), None)
        if not TSC: print('REFUSED: no tsc in the worktree node_modules'); return 2
        ver = run([TSC, '--version'], TD, None)[1].strip(); rcs = {}
        for name, sha in (('base', K['base']), ('head', K['head'])):
            co(sha); rcs[name] = run([TSC, '--noEmit', '-p', '.'], TD, os.path.join(OUT, 'c3_tsc_' + name))[0]
        T.check('T1', rcs == {'base': 0, 'head': 0}, '%s (%s) | rc base %d head %d' % (TSC, ver, rcs['base'], rcs['head']))
        pf = os.path.join(WT, K['repo_file']); src = open(pf, encoding='utf-8').read()
        try:
            open(pf, 'w', encoding='utf-8').write(src + "\nconst __g65: number = 'x';\n"); rc, o, e = run([TSC, '--noEmit', '-p', '.'], TD, os.path.join(OUT, 'c3_tsc_positive_control'))
        finally:
            open(pf, 'w', encoding='utf-8').write(src)
        st = wgit(WT, 'status', '--porcelain')[1].strip()
        T.check('T2', rc != 0 and 'TS2322' in o + e and not st, 'planted TS2322 -> rc %d, TS2322 printed %s | restored, status %r' % (rc, 'TS2322' in o + e, st[:80]))
        tc = open(os.path.join(TD, 'tsconfig.json'), encoding='utf-8').read()
        T.info('T3', 'tsconfig excludes src/__tests__: %s — if so tsc does NOT typecheck the new test file (ts-jest does at run time)' % bool(re.search(r'"exclude"\s*:\s*\[[^\]]*__tests__', tc)))
    co(K['base'])
    return T.end()


if __name__ == '__main__':
    raise SystemExit(main())
