#!/usr/bin/env python3
"""c3_tests_gate68.py — gate68 C3 (#1393 ROUND 2, KS-1278, T1). --head is a PARAMETER (env G68_HEAD; default the stand-in 97ce2f).
Every mode runs jest IN THE GATE'S OWN INSTALLED SCRATCH WORKTREE (npm ci --ignore-scripts + build packages/shared, X1) — never the
builder's worktree, never the shared checkout (refused: worktree and out dir must lie outside !CODING).

MODES
  redfirst --repo <clone> --worktree <wt> --out <dir> [--head H] [--expect-red N1[,R2…]]
    RF1 worktree at ROUND 1 (4a1620588819: round 1's product, the OLD key) with the HEAD's ks1278 test file written over it
        (ks1293 is the same blob at 4a16 and the head): the ks1278 file executes EXACTLY as many cells as the head file declares
        (`it('` count), the FAILED set == --expect-red (default the author's claim: N1 only) BY ASSERTION, every other cell PASSED,
        0 load-failure signatures; ks1293 10/10
    RF1b restored by CONTENT (the overlay MOVED to <out>/quarantine, never deleted), `git status --porcelain` empty
    RF2 worktree at the HEAD: ks1278 + ks1293 all passed, executed == cells + 10
  tamper   --repo --worktree --out [--head H] [--only G7,G8,K1,T5,…]
    each kit tamper ALONE at the HEAD: LANDED (each edit's `from` occurs exactly `count` times; the `nth` one replaced; sha256 changed);
    ks1278 EXECUTED == the head's cell count — 0 EXECUTED (or any load signature) IS A LOAD FAILURE, NEVER "NOT CAUGHT";
    the FAILED set vs the kit's `expect`: printed CAUGHT BY [...] / NOT CAUGHT / LOAD FAILURE; the check FAILS unless FAILED == expect
    exactly (for a blind-spot probe, expect == []); restored by content, status clean; a final un-tampered run is all green.
    The round-2 matrix rows are G7, G8, K1 (corrected: key reverted AND the unused idAsUuid removed), T5.
  suite    --repo --worktree --out [--head H]   the WHOLE originate jest suite at ROUND 1 and the HEAD: totals printed vs the claim
           (91 / 1070 / 0 at the head; 91 / 1067 at round 1); 0 NEW reds; same node + jest binary at both ends (printed)
  tsc      --repo --worktree --out [--head H]   tsc --noEmit -p services/originate at round 1 + head rc 0; --listFilesOnly lists
           documentRepo.ts (and the ks1278 test file 0 times: TYPE-UNCHECKED); planted TS2322 -> rc != 0, restored
  --selftest [--repo <clone>]   judges on planted jest JSON (shape, LOAD failure, 0 executed, wrong red, tamper caught / not caught /
           load-failed) + (with --repo) every tamper's edits LAND on the real stand-in head.
Usage: c3_tests_gate68.py redfirst|tamper|suite|tsc --repo <clone> --worktree <wt> --out <dir> [--head H]  |  --selftest [--repo <clone>]
rc 0 PASS / 1 FAIL / 2 usage or refused."""
import hashlib, json, os, re, shutil, subprocess, sys, io, contextlib
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate68 import K, git, wgit, Tally, outside_forbidden, resolvable

LOADFAIL = ['Test suite failed to run', 'Cannot find module', 'SyntaxError', 'is not a function', 'TS6133', 'TS2', 'error TS']
CELLS = K['cells']
T1278 = os.path.basename(K['test']); T1293 = os.path.basename(K['manifest_test'])


def now(): return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def sha256(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()


def run(cmd, cwd, prefix):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if prefix:
        open(prefix + '.out', 'w').write(p.stdout); open(prefix + '.err', 'w').write(p.stderr); open(prefix + '.rc', 'w').write('%d\n' % p.returncode)
    return p.returncode, p.stdout, p.stderr


def ncells(test_src): return len(re.findall(r"^\s*it\('", test_src, re.M))


def cells(j):
    out = {}; ferr = []
    for t in j.get('testResults', []):
        msg = t.get('message') or ''; name = os.path.basename(t.get('name', ''))
        if t.get('status') == 'failed' and (not t.get('assertionResults') or any(s in msg for s in LOADFAIL)):
            ferr.append((name, ' '.join(msg.split())[:200]))
        for a in t.get('assertionResults', []):
            out[(name, a.get('fullName') or a['title'])] = (a['status'], re.sub(r'\x1b\[[0-9;]*m', '', ((a.get('failureMessages') or ['']) + [''])[0]))
    return out, ferr


def by_cell(cs, fname):
    r = {}
    for (f, title), v in cs.items():
        if f != fname: continue
        for k, pre in CELLS.items():
            if pre + ':' in title or title.endswith(pre) or (pre + ' ') in title: r[k] = v
    return r


def executed(cs, fname): return sum(1 for (f, _), v in cs.items() if f == fname and v[0] in ('passed', 'failed'))


def judge_redfirst(t, j, n, expect):
    cs, ferr = cells(j); c = by_cell(cs, T1278); ex = executed(cs, T1278)
    reds = sorted(k for k, v in c.items() if v[0] == 'failed'); greens = sorted(k for k, v in c.items() if v[0] == 'passed')
    asrt = all('expect(' in c[k][1] or 'Expected' in c[k][1] for k in reds)
    m1293 = [v[0] for (f, _), v in cs.items() if f == T1293]
    t.check('RF1', ex == n and ex > 0 and reds == sorted(expect) and len(reds) + len(greens) == n and asrt and not ferr
            and len(m1293) == K['manifest_cells'] and all(s == 'passed' for s in m1293),
            'ks1278 EXECUTED %d (want %d) | red %s (want %s) by assertion %s | green %s | ks1293 %d cells all passed %s | loadfail %s' % (
                ex, n, reds, sorted(expect), asrt, greens, len(m1293), all(s == 'passed' for s in m1293), ferr or 'NONE'))
    for k in reds: t.info('RF1-' + k, ' '.join(c[k][1].split())[:240])


def judge_green(t, tag, j, n):
    cs, ferr = cells(j); bad = [k for k, v in cs.items() if v[0] != 'passed']
    t.check(tag, len(cs) == n and not bad and not ferr, '%d cell(s) ran (want %d) | not passed %s | loadfail %s' % (len(cs), n, [b[1][-50:] for b in bad] or 'NONE', ferr or 'NONE'))


def judge_tamper(t, tid, j, n, want):
    cs, ferr = cells(j); c = by_cell(cs, T1278); ex = executed(cs, T1278)
    reds = sorted(k for k, v in c.items() if v[0] == 'failed')
    if ex == 0 or ferr:
        verdict = 'LOAD FAILURE (0 executed or a load signature) — NEVER "not caught"; fix the tamper so the file loads, re-run'
    elif reds:
        verdict = 'CAUGHT BY %s' % reds
    else:
        verdict = 'NOT CAUGHT (every cell green, %d executed)' % ex
    t.check(tid, ex == n and not ferr and reds == sorted(want), '%s: EXECUTED %d (want %d) | %s | kit expects %s | loadfail %s' % (
        K['tampers'][tid]['what'][:90], ex, n, verdict, sorted(want) or '[] (blind-spot probe)', ferr or 'NONE'))
    return verdict


def judge_suite(t, jb, jh):
    tb = (jb.get('numTotalTestSuites'), jb.get('numTotalTests'), jb.get('numFailedTests'), jb.get('numPendingTests'))
    th = (jh.get('numTotalTestSuites'), jh.get('numTotalTests'), jh.get('numFailedTests'), jh.get('numPendingTests'))
    t.check('S1', th[2] == 0 and th[3] == 0 and tb[2] == 0, 'round1 %s | head %s [suites, tests, failed, skipped] | claim head 91/1070/0/0, round1 91/1067/0' % (tb, th))
    fb = {k for k, v in cells(jb)[0].items() if v[0] == 'failed'}; fh = {k for k, v in cells(jh)[0].items() if v[0] == 'failed'}
    t.check('S2', not (fh - fb) and not cells(jh)[1], 'NEW reds at head %s | load failures at head %s' % (sorted(x[1][:50] for x in fh - fb) or 'NONE', cells(jh)[1] or 'NONE'))


def jest(cwd, args, prefix):
    jf = prefix + '.json'
    rc, o, e = run(['npx', 'jest'] + args + ['--json', '--outputFile=' + jf], cwd, prefix)
    try:
        return rc, json.load(open(jf))
    except Exception as ex:
        return rc, {'testResults': [{'name': 'NO JSON', 'status': 'failed', 'message': 'Test suite failed to run: ' + str(ex), 'assertionResults': []}]}


def apply_edits(src, edits):
    """-> (landed_all, new_src, notes). Each edit: `from` must occur exactly `count` times; the `nth` occurrence is replaced."""
    notes = []; ok = True
    for e in edits:
        c = src.count(e['from'])
        if c != e['count']:
            ok = False; notes.append('`from` occurs %d (want %d): %r' % (c, e['count'], e['from'][:60])); continue
        i = -1
        for _ in range(e['nth']): i = src.index(e['from'], i + 1)
        src = src[:i] + e['to'] + src[i + len(e['from']):]
        notes.append('edit landed (occurrence %d of %d)' % (e['nth'], c))
    return ok, src, notes


def selftest(repo, head):
    ok = n = 0
    def arm(name, fn, want):
        nonlocal ok, n
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): fn(t)
        good = (not t.fails) if want is None else (want in t.fails)
        n += 1; ok += good; print('SELFTEST %s %s: want %s | failed %s' % ('OK' if good else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, t.fails or 'NONE'))
    def cell(k, s, m=''): return {'title': CELLS[k] + ': x', 'fullName': 'KS-1278 /revoke is one atomic transition ' + CELLS[k] + ': x', 'status': s, 'failureMessages': [m] if m else []}
    EM = 'expect(received).toEqual(expected)\nExpected [200,null,1]\nReceived [400,"BAD_REQUEST",0]'
    def J(c1278, n1293=10, msg=''):
        return {'testResults': [{'name': '/w/src/__tests__/' + T1278, 'status': 'failed' if any(c['status'] == 'failed' for c in c1278) else 'passed', 'message': msg, 'assertionResults': c1278},
                                {'name': '/w/src/__tests__/' + T1293, 'status': 'passed', 'message': '', 'assertionResults': [{'title': 'm%d' % i, 'status': 'passed', 'failureMessages': []} for i in range(n1293)]}]}
    ks = list(CELLS)
    green = [cell(k, 'passed') for k in ks]
    rf = [cell(k, 'failed', EM) if k == 'N1' else cell(k, 'passed') for k in ks]
    arm('RF-a the claimed red-first shape (N1 only, 7 executed)', lambda t: judge_redfirst(t, J(rf), 7, ['N1']), None)
    arm('RF-b LOAD failure (0 cells)', lambda t: judge_redfirst(t, {'testResults': [{'name': '/w/' + T1278, 'status': 'failed', 'message': 'Test suite failed to run\nerror TS6133', 'assertionResults': []}]}, 7, ['N1']), 'RF1')
    arm('RF-c R2 also red', lambda t: judge_redfirst(t, J([cell(k, 'failed', EM) if k in ('N1', 'R2') else cell(k, 'passed') for k in ks]), 7, ['N1']), 'RF1')
    arm('RF-d no red at all', lambda t: judge_redfirst(t, J(green), 7, ['N1']), 'RF1')
    arm('RF-e red without an assertion message', lambda t: judge_redfirst(t, J([cell(k, 'failed', 'TypeError: boom') if k == 'N1' else cell(k, 'passed') for k in ks]), 7, ['N1']), 'RF1')
    arm('G-a 17/17 green', lambda t: judge_green(t, 'RF2', J(green), 17), None)
    arm('G-b a skipped cell is not a pass', lambda t: judge_green(t, 'RF2', J(green[:-1] + [dict(green[-1], status='pending')]), 17), 'RF2')
    arm('TM-a G7 caught exactly by R2', lambda t: judge_tamper(t, 'G7', J([cell(k, 'failed', EM) if k == 'R2' else cell(k, 'passed') for k in ks]), 7, ['R2']), None)
    arm('TM-b G7 NOT caught (all green)', lambda t: judge_tamper(t, 'G7', J(green), 7, ['R2']), 'G7')
    arm('TM-c K1 0 EXECUTED is a LOAD FAILURE, not "not caught"', lambda t: judge_tamper(t, 'K1', {'testResults': [{'name': '/w/' + T1278, 'status': 'failed', 'message': "Test suite failed to run\nerror TS6133: 'idAsUuid' is declared but its value is never read.", 'assertionResults': []}]}, 7, ['N1']), 'K1')
    v = []
    t = Tally()
    with contextlib.redirect_stdout(io.StringIO()):
        v.append(judge_tamper(t, 'K1', {'testResults': [{'name': '/w/' + T1278, 'status': 'failed', 'message': 'Test suite failed to run', 'assertionResults': []}]}, 7, ['N1']))
    n += 1; g = v[0].startswith('LOAD FAILURE'); ok += g; print('SELFTEST %s TM-d the 0-executed verdict string reads LOAD FAILURE: %r' % ('OK' if g else 'MISS', v[0][:40]))
    arm('TM-e U1 blind-spot probe: 0 reds expected and got', lambda t: judge_tamper(t, 'U1', J(green), 7, []), None)
    arm('TM-f U1 probe reddens N2 (disagrees with the kit)', lambda t: judge_tamper(t, 'U1', J([cell(k, 'failed', EM) if k == 'N2' else cell(k, 'passed') for k in ks]), 7, []), 'U1')
    SB = {'numTotalTestSuites': 91, 'numTotalTests': 1067, 'numFailedTests': 0, 'numPendingTests': 0, 'testResults': []}
    SH = {'numTotalTestSuites': 91, 'numTotalTests': 1070, 'numFailedTests': 0, 'numPendingTests': 0, 'testResults': []}
    arm('S-a claimed totals', lambda t: judge_suite(t, SB, SH), None)
    arm('S-b a skipped test at head', lambda t: judge_suite(t, SB, dict(SH, numPendingTests=1)), 'S1')
    if repo:
        for fk in ('repo', 'route'):
            src = git(repo, 'show', '%s:%s' % (head, K['tamper_files'][fk]))
            for tid, tp in K['tampers'].items():
                if tp['file'] != fk: continue
                landed, new, notes = apply_edits(src, tp['edits'])
                g = landed and new != src; n += 1; ok += g
                print('SELFTEST %s tamper %s LANDS on the real head %s %s: %s' % ('OK' if g else 'MISS', tid, head[:12], os.path.basename(K['tamper_files'][fk]), notes))
        bad = {'edits': [{'from': 'THIS TEXT IS NOT IN THE FILE', 'to': '', 'nth': 1, 'count': 1}]}
        landed, _, notes = apply_edits(src, bad['edits']); n += 1; ok += (not landed)
        print('SELFTEST %s PLANTED a tamper whose `from` is absent is REFUSED as not-landed: %s' % ('OK' if not landed else 'MISS', notes))
        tsrc = git(repo, 'show', '%s:%s' % (head, K['test'])); nc = ncells(tsrc); n += 1; ok += (nc == len(CELLS))
        print('SELFTEST %s the head test file declares %d it( cells (kit names %d)' % ('OK' if nc == len(CELLS) else 'MISS', nc, len(CELLS)))
    else:
        print('SELFTEST NOTE: the tamper-landing arms need --repo; NOT RUN')
    print('SELFTEST %s %d of %d' % ('OK' if ok == n else 'BROKEN', ok, n)); print('CHECKED %d arm(s)' % n)
    return 0 if ok == n else 1


def main():
    A = sys.argv[1:]
    if not A or '--help' in A or '-h' in A: print(__doc__); return 0 if A else 2
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    head = opt('--head', os.environ.get('G68_HEAD', K['head_expected']))
    if '--selftest' in A: return selftest(opt('--repo'), head)
    MODE = next((m for m in ('redfirst', 'tamper', 'suite', 'tsc') if m in A), None)
    REPO, WT, OUT = opt('--repo'), opt('--worktree'), opt('--out')
    if not (MODE and REPO and WT and OUT): print(__doc__); return 2
    for nm, s in (('head', head), ('round-1 head', K['round1_head'])):
        if not resolvable(REPO, s):
            print('REFUSED: %s unresolvable: %s not in %s — fetch it by sha into YOUR clone (X7)' % (nm, s, REPO)); return 2
    if not outside_forbidden(WT) or not outside_forbidden(OUT):
        print('REFUSED: the worktree / out dir must lie OUTSIDE %s (your own scratch)' % K['forbidden_root']); return 2
    os.makedirs(OUT, exist_ok=True); Q = os.path.join(OUT, 'quarantine'); os.makedirs(Q, exist_ok=True)
    if wgit(WT, 'status', '--porcelain')[1].strip():
        print('REFUSED: the worktree is not clean'); return 2
    if not os.path.exists(os.path.join(WT, 'Blockchain/Dev/packages/shared/dist/index.js')):
        print('REFUSED: packages/shared/dist/index.js absent — `npm ci --ignore-scripts` + `npm run build --workspace=packages/shared` first (X1); a missing dist is a LOAD failure, not a red'); return 2
    R1 = K['round1_head']
    tsrc = git(REPO, 'show', '%s:%s' % (head, K['test'])); NC = ncells(tsrc)
    print('c3_tests_gate68 %s %s | repo %s | wt %s | head %s | round1 %s | head test declares %d cell(s)' % (MODE, now(), REPO, WT, head[:12], R1[:12], NC))
    SD = os.path.join(WT, K['suite_dir']); rel = lambda p: os.path.relpath(os.path.join(WT, p), SD)
    T = Tally(); co = lambda s: wgit(WT, 'checkout', '--quiet', '--detach', s)
    if MODE == 'redfirst':
        co(R1); p78 = os.path.join(WT, K['test']); base78 = open(p78, encoding='utf-8').read()
        try:
            open(p78, 'w', encoding='utf-8').write(tsrc)
            print('INFO overlay: ks1278 == head blob %s; product at round 1: documentRepo sha256/16 %s' % (
                sha256(open(p78, encoding='utf-8').read()) == sha256(tsrc), sha256(open(os.path.join(WT, K['repo_file']), encoding='utf-8').read())[:16]))
            rc, j = jest(SD, [rel(K['test']), rel(K['manifest_test'])], os.path.join(OUT, 'c3_redfirst_round1'))
            print('INFO jest rc %d at round1+head-test' % rc)
            judge_redfirst(T, j, NC, (opt('--expect-red') or 'N1').split(','))
        finally:
            shutil.copy(p78, os.path.join(Q, T1278 + '.overlay.' + now().replace(':', '')))
            open(p78, 'w', encoding='utf-8').write(base78)
        st = wgit(WT, 'status', '--porcelain')[1].strip()
        T.check('RF1b', sha256(open(p78, encoding='utf-8').read()) == sha256(git(REPO, 'show', '%s:%s' % (R1, K['test']))) and not st,
                'ks1278 restored == round-1 blob; overlay copy kept in %s; git status --porcelain %r' % (Q, st[:80]))
        co(head); rc, j = jest(SD, [rel(K['test']), rel(K['manifest_test'])], os.path.join(OUT, 'c3_green_head'))
        judge_green(T, 'RF2', j, NC + K['manifest_cells'])
    elif MODE == 'tamper':
        co(head); only = (opt('--only') or ','.join(K['tampers'])).split(',')
        for tid in only:
            tp = K['tampers'][tid]; pf = os.path.join(WT, K['tamper_files'][tp['file']]); src = open(pf, encoding='utf-8').read()
            landed, new, notes = apply_edits(src, tp['edits'])
            try:
                open(pf, 'w', encoding='utf-8').write(new)
                T.check(tid + '-landed', landed and sha256(open(pf, encoding='utf-8').read()) != sha256(src), '%s; file sha256/16 %s -> %s' % (notes, sha256(src)[:16], sha256(new)[:16]))
                if landed:
                    rc, j = jest(SD, [rel(K['test'])], os.path.join(OUT, 'c3_tamper_' + tid))
                    judge_tamper(T, tid, j, NC, tp['expect'])
            finally:
                open(pf, 'w', encoding='utf-8').write(src)
            st = wgit(WT, 'status', '--porcelain')[1].strip()
            T.check(tid + '-restored', sha256(open(pf, encoding='utf-8').read()) == sha256(src) and not st, 'restored by content; status %r' % st[:80])
        rc, j = jest(SD, [rel(K['test'])], os.path.join(OUT, 'c3_tamper_restored'))
        judge_green(T, 'TR', j, NC)
    elif MODE == 'suite':
        res = {}
        print('INFO node %s | jest %s' % (run(['node', '--version'], SD, None)[1].strip(), run(['npx', 'jest', '--version'], SD, None)[1].strip()))
        for name, s in (('round1', R1), ('head', head)):
            co(s); rc, res[name] = jest(SD, [], os.path.join(OUT, 'c3_suite_' + name))
            print('INFO suite %s at %s rc %d | suites %s tests %s failed %s skipped %s' % (name, s[:12], rc, res[name].get('numTotalTestSuites'), res[name].get('numTotalTests'), res[name].get('numFailedTests'), res[name].get('numPendingTests')))
        judge_suite(T, res['round1'], res['head'])
    elif MODE == 'tsc':
        TD = os.path.join(WT, K['tsc_dir']); TSC = next((d for d in (os.path.join(TD, 'node_modules/.bin/tsc'), os.path.join(WT, 'Blockchain/Dev/node_modules/.bin/tsc')) if os.path.exists(d)), None)
        if not TSC: print('REFUSED: no tsc in the worktree node_modules'); return 2
        ver = run([TSC, '--version'], TD, None)[1].strip(); rcs = {}
        for name, s in (('round1', R1), ('head', head)):
            co(s); rcs[name] = run([TSC, '--noEmit', '-p', '.'], TD, os.path.join(OUT, 'c3_tsc_' + name))[0]
        T.check('T1', rcs == {'round1': 0, 'head': 0}, '%s (%s) | rc round1 %d head %d' % (TSC, ver, rcs['round1'], rcs['head']))
        lf = run([TSC, '--noEmit', '-p', '.', '--listFilesOnly'], TD, os.path.join(OUT, 'c3_tsc_listfiles'))[1]
        T.check('T2', 'repositories/documentRepo.ts' in lf and T1278 not in lf, '--listFilesOnly: documentRepo.ts listed %s | %s listed %d time(s) (want 0: TYPE-UNCHECKED, a NAMED NOT TESTED item)' % (
            'repositories/documentRepo.ts' in lf, T1278, lf.count(T1278)))
        pf = os.path.join(WT, K['repo_file']); src = open(pf, encoding='utf-8').read()
        try:
            open(pf, 'w', encoding='utf-8').write(src + "\nconst __g68: number = 'x';\n"); rc, o, e = run([TSC, '--noEmit', '-p', '.'], TD, os.path.join(OUT, 'c3_tsc_positive_control'))
        finally:
            open(pf, 'w', encoding='utf-8').write(src)
        st = wgit(WT, 'status', '--porcelain')[1].strip()
        T.check('T3', rc != 0 and 'TS2322' in o + e and not st, 'planted TS2322 -> rc %d, TS2322 printed %s | restored, status %r' % (rc, 'TS2322' in o + e, st[:80]))
    co(R1)
    return T.end()


if __name__ == '__main__':
    raise SystemExit(main())
