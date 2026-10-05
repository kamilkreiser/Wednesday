#!/usr/bin/env python3
"""c3_tests_gate66.py — C3 TESTS for #1385 (KS-938, T1): red-first, tamper-per-conjunct, suite, tsc. The GATE runs this in ITS OWN
worktree (never the shared checkout: every write is refused inside the forbidden root). The drafter ran ONLY --selftest.

Worktree recipe (README section 6): in your own clone (`git clone --shared --no-checkout` of the checkout, origin re-pointed at GitHub,
develop fetched BY SHA), `git worktree add --detach <wt> f6b49d68209d`, then in <wt>/Blockchain/Dev: `npm ci --ignore-scripts` and
`npm run build --workspace=packages/shared` (without packages/shared/dist/index.js the cells cannot LOAD — a load failure, not a red).

  redfirst --wt <wt>   overlay mfa.ts + users.ts with the BASE (d784) blobs, keep the head test; run the KS-938 file; REQUIRE R1 R2 R3
                       failed BY ASSERTION (failureMessages non-empty), C1 C2 passed, 5 executed, 0 load failures; restore BY CONTENT
                       (bytes compared with the head blobs); run again at the head: 5 passed. Each run's JSON kept under --out.
  tamper --wt <wt>     T1..T7 (kit.json): each lands exactly once (anchor count 1), runs the file, REQUIRES its `reddens` cells red BY
                       ASSERTION and every other cell green, restores by content, porcelain re-read clean. One conjunct per tamper:
                       seed vs backup codes, per site, plus S3's key-removed AND key-undefined shapes.
  suite --wt <wt>      full services/auth `vitest run` at the head: files / tests / failed (claim at 79c87: 79 / 845 / 0 — the head now
                       carries develop d784's tests too, so the figure is RE-MEASURED, never compared to the claim as a pass condition);
                       0 failed is the pass condition; any failure is listed BY NAME with "pre-existing at d784?" to be answered by the
                       same run at the d784 overlay.
  tsc --wt <wt>        `npx tsc --noEmit -p services/auth` rc 0; CONTROL a planted `const __g66: number = 'x';` in mfa.ts -> rc != 0;
                       restored by content.
  --selftest           the JSON judge on synthetic vitest reports (assertion red / load failure / skipped / not-run arms) + every
                       tamper's anchor occurs EXACTLY once in the REAL head blob and lands (no vitest run).
rc 0 all PASS / rc 1 any FAIL / rc 2 refused (no worktree, worktree inside the forbidden root, worktree HEAD != kit head)."""
import io, contextlib, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate66 import K, git, wgit, Tally, outside_forbidden, SCRATCH

AUTH = K['suite_dir']; TEST = K['test']; CELLS = K['cells']


def cell_of(title):
    for cid, pre in CELLS.items():
        if pre in title: return cid
    return None


def judge_report(rep, want_red, t, label):
    """rep = vitest --reporter=json dict. want_red = set of cell ids that must be red BY ASSERTION; every other kit cell must pass."""
    files = rep.get('testResults', [])
    load = [f.get('name', '?') for f in files if f.get('status') == 'failed' and not f.get('assertionResults')]
    got = {}
    for f in files:
        for a in f.get('assertionResults', []):
            cid = cell_of(a.get('fullName', '') + ' ' + a.get('title', ''))
            if cid: got[cid] = (a.get('status'), bool(a.get('failureMessages')))
    missing = sorted(set(CELLS) - set(got))
    bad = []
    for cid in CELLS:
        st = got.get(cid)
        if st is None: continue
        if cid in want_red and not (st[0] == 'failed' and st[1]): bad.append('%s want RED-by-assertion got %s' % (cid, st))
        if cid not in want_red and st[0] != 'passed': bad.append('%s want PASS got %s' % (cid, st[0]))
    executed = sum(1 for v in got.values() if v[0] in ('passed', 'failed'))
    ok = not load and not missing and not bad and executed == len(CELLS)
    t.check(label, ok, 'executed %d/%d | red %s | load failures %s | missing %s | wrong %s' % (
        executed, len(CELLS), sorted(c for c, v in got.items() if v[0] == 'failed'), load, missing, bad))
    return ok


def check_wt(wt):
    if not wt or not os.path.isdir(wt): print('REFUSED: --wt <worktree> missing'); return False
    if not outside_forbidden(wt): print('REFUSED: the worktree %s is inside %s — use your OWN clone\'s worktree' % (wt, K['forbidden_root'])); return False
    h = git(wt, 'rev-parse', 'HEAD').strip()
    if h != K['head']: print('REFUSED: worktree HEAD %s != kit head %s' % (h[:12], K['head'][:12])); return False
    return True


def vitest(wt, out, tag, args):
    os.makedirs(out, exist_ok=True); f = os.path.join(out, 'vitest_%s.json' % tag)
    p = subprocess.run(['npx', 'vitest', 'run'] + args + ['--reporter=json', '--outputFile=' + f], cwd=os.path.join(wt, AUTH), capture_output=True, text=True)
    open(os.path.join(out, 'vitest_%s.log' % tag), 'w').write(p.stdout + '\n--- stderr\n' + p.stderr)
    try: return p.returncode, json.load(open(f))
    except Exception as e: return p.returncode, {'testResults': [{'name': 'NOT RUN: ' + str(e)[:120], 'status': 'failed', 'assertionResults': []}]}


def put(wt, path, data): open(os.path.join(wt, path), 'wb').write(data)
def head_bytes(wt, path): return subprocess.run(['git', '-C', wt, 'show', '%s:%s' % (K['head'], path)], capture_output=True).stdout
def clean(wt): return git(wt, 'status', '--porcelain', '--untracked-files=no').strip() == ''


def redfirst(wt, out, t):
    rel = [K['mfa_file'], K['users_file']]
    for p in rel: put(wt, p, subprocess.run(['git', '-C', wt, 'show', '%s:%s' % (K['base'], p)], capture_output=True).stdout)
    rc, rep = vitest(wt, out, 'redfirst_base', [TEST.split(AUTH + '/', 1)[1]])
    judge_report(rep, {'R1', 'R2', 'R3'}, t, 'R-BASE')
    for p in rel: put(wt, p, head_bytes(wt, p))
    restored = all(open(os.path.join(wt, p), 'rb').read() == head_bytes(wt, p) for p in rel) and clean(wt)
    t.check('R-RESTORE', restored, 'overlay restored by content (bytes == head blobs) and porcelain clean: %s' % restored)
    rc, rep = vitest(wt, out, 'redfirst_head', [TEST.split(AUTH + '/', 1)[1]])
    judge_report(rep, set(), t, 'R-HEAD')


def tamper(wt, out, t):
    for tid, tm in K['tampers'].items():
        p = os.path.join(wt, tm['file']); orig = open(p, 'rb').read(); s = orig.decode()
        n = s.count(tm['from'])
        if n != 1: t.check(tid, False, 'anchor found %d time(s) (want 1) — the tamper did NOT land' % n); continue
        open(p, 'w').write(s.replace(tm['from'], tm['to']))
        rc, rep = vitest(wt, out, 'tamper_' + tid, [TEST.split(AUTH + '/', 1)[1]])
        judge_report(rep, set(tm['reddens']), t, tid)
        open(p, 'wb').write(orig)
        t.check(tid + '-RESTORE', open(p, 'rb').read() == head_bytes(wt, tm['file']) and clean(wt), 'restored by content, porcelain clean')


def suite(wt, out, t):
    rc, rep = vitest(wt, out, 'suite_head', [])
    files = rep.get('testResults', []); fails = [(f.get('name', '').split('/src/')[-1], a.get('title')) for f in files for a in f.get('assertionResults', []) if a.get('status') == 'failed']
    load = [f.get('name', '').split('/src/')[-1] for f in files if f.get('status') == 'failed' and not f.get('assertionResults')]
    t.check('S-SUITE', rc == 0 and not fails and not load, 'services/auth at head: rc %d | files %d | tests %s | failed %d %s | load failures %s (claim at 79c87: 79 / 845 / 0)' % (
        rc, len(files), rep.get('numTotalTests'), len(fails), fails[:6], load))


def tsc(wt, out, t):
    run = lambda: subprocess.run(['npx', 'tsc', '--noEmit', '-p', '.'], cwd=os.path.join(wt, AUTH), capture_output=True, text=True)
    p = run(); p_ok = p.returncode == 0
    f = os.path.join(wt, K['mfa_file']); orig = open(f, 'rb').read()
    open(f, 'wb').write(orig + b"\nconst __g66: number = 'x';\n"); c = run(); open(f, 'wb').write(orig)
    t.check('TSC', p_ok and c.returncode != 0 and clean(wt), 'tsc rc %d at head; planted TS2322 control rc %d (want != 0); restored clean %s' % (p.returncode, c.returncode, clean(wt)))


def selftest():
    ok = total = 0
    def rep_(c, m):
        nonlocal ok, total
        total += 1; ok += bool(c); print('SELFTEST %s %s' % ('OK' if c else 'MISS', m))
    titles = {'R1': 'RED KS-938 site 1 - the setup-verify REVERT', 'R2': 'RED KS-938 site 2 - POST /api/auth/mfa/disable', 'R3': 'RED KS-938 site 3 - POST /api/users/me/mfa/disable',
              'C1': 'CONTROL - the SAME real updateUser still SKIPS an `undefined` field', 'C2': 'CONTROL - an unrelated caller is untouched'}
    def mk(st, load=False):
        if load: return {'testResults': [{'name': 'ks938.test.ts', 'status': 'failed', 'message': 'Cannot find module', 'assertionResults': []}]}
        return {'testResults': [{'name': 'ks938.test.ts', 'status': 'failed', 'assertionResults': [
            {'fullName': 'KS-938 ' + titles[c], 'title': titles[c], 'status': st.get(c, 'passed'), 'failureMessages': ['AssertionError'] if st.get(c) == 'failed' else []} for c in titles]}]}
    def j(r, red):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): judge_report(r, red, t, 'X')
        return not t.fails
    rep_(j(mk({'R1': 'failed', 'R2': 'failed', 'R3': 'failed'}), {'R1', 'R2', 'R3'}), 'positive: base shape 3 red by assertion / 2 pass -> PASS')
    rep_(not j(mk({}, load=True), {'R1', 'R2', 'R3'}), 'a LOAD FAILURE is NOT a red -> FAIL')
    rep_(not j(mk({'R1': 'failed', 'R2': 'failed'}), {'R1', 'R2', 'R3'}), 'R3 green at base -> FAIL')
    rep_(not j(mk({'R1': 'failed', 'R2': 'failed', 'R3': 'failed', 'C1': 'failed'}), {'R1', 'R2', 'R3'}), 'a control red -> FAIL')
    rep_(not j(mk({'R1': 'skipped'}), set()), 'a SKIPPED cell is never a pass -> FAIL')
    r = mk({'R1': 'failed'}); r['testResults'][0]['assertionResults'][0]['failureMessages'] = []
    rep_(not j(r, {'R1'}), 'failed with NO failure message (not by assertion) -> FAIL')
    r = mk({}); r['testResults'][0]['assertionResults'] = r['testResults'][0]['assertionResults'][:4]
    rep_(not j(r, set()), 'a cell missing from the report (NOT RUN) -> FAIL')
    rep_(not j({'testResults': [{'name': 'NOT RUN: no json', 'status': 'failed', 'assertionResults': []}]}, set()), 'no JSON at all (NOT RUN) -> FAIL')
    for tid, tm in K['tampers'].items():
        s = git(K['checkout'] if os.path.isdir(K['checkout']) else '.', 'show', '%s:%s' % (K['head'], tm['file']))
        n = s.count(tm['from']); landed = n == 1 and s.replace(tm['from'], tm['to']) != s
        rep_(landed, 'tamper %s (%s) anchor occurs %d time(s) in the REAL head blob and lands: %s' % (tid, tm['what'], n, landed))
    print('SELFTEST %s %d of %d' % ('OK' if ok == total else 'BROKEN', ok, total)); print('CHECKED %d arm(s)' % total)
    return 0 if ok == total else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if not A or '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    if '--selftest' in A: raise SystemExit(selftest())
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    wt = opt('--wt'); out = opt('--out', os.path.join(SCRATCH, 'c3'))
    if not check_wt(wt): raise SystemExit(2)
    t = Tally(); {'redfirst': redfirst, 'tamper': tamper, 'suite': suite, 'tsc': tsc}[A[0]](wt, out, t); raise SystemExit(t.end())
