#!/usr/bin/env python3
"""c3_tamper_gate77.py — the RED-PROOF instrument for every gate77 row, driven by the recipe in kit.json rows.<n>.redproof[]. ONE parser for
the green and the red (the runner's own summary line, matched by the recipe's needles). RESTORE TO THE HEAD STATE, NEVER THE BASE.

  c3_tamper_gate77.py run --pr <n> --recipe <name> --wt <YOUR worktree at the row's head> --out <FRESH json path>
  c3_tamper_gate77.py list                                     every row's recipes, with the claim each re-measures
  c3_tamper_gate77.py selftest --scratch <FRESH dir>           planted arms in a throwaway repo: each refusal MUST refuse, the red MUST fire

run, in order (any failure stops with rc 1 and the worktree RESTORED; a refusal before the tamper leaves it untouched):
  W0  the worktree is OUTSIDE !CODING (lexical + realpath), HEAD == the row's head, HEAD^{tree} == END_TREE, porcelain EMPTY  (else REFUSED rc 16/11)
  S1  needs_s1 recipes: Blockchain/Dev/node_modules and packages/shared/dist/index.js present   (else REFUSED rc 12: do S-1 first, NOT a red)
  G   the command at the head: rc 0 AND every want_green needle present                      (a green with no needle is NOT a green)
  T   SAVE each file's bytes, assert hash-object == the HEAD blob; apply the tamper (revert_to_base: the raise_base blob; replace_once:
      `old` must occur EXACTLY once, else REFUSED); ASSERT THE TAMPER LANDED (hash != HEAD blob; for replace_once, `new` present)
  R   the command on the tamper: rc == want_red_rc AND every want_red needle present, every want_red_cells line marked FAIL and every
      want_ok_both line marked ok (shell suites); a run with NO summary line is a LOADFAIL, never a red
  X   RESTORE the saved bytes; assert hash-object == the HEAD blob for every file and porcelain EMPTY; G2 the command again == green
The JSON records every run's rc, the summary lines, the needles hit/missed, the blob shas, and the UTC times.
"""
import datetime, hashlib, json, os, re, subprocess, sys
import lib_gate77 as L
from lib_gate77 import K, ROWS, RAISE_BASE, opt

SUMMARY_RX = re.compile(r'(Tests?\s+.*\(\d+\)|Test Files\s+.*\(\d+\)|\d+ passed, \d+ failed|passed \(\d+\))')


def now(): return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def g(wt, *a, inp=None):
    p = subprocess.run(['git', '-C', wt] + list(a), capture_output=True, input=inp)
    return p.returncode, p.stdout.decode('utf-8', 'replace').strip()


def run_cmd(wt, rec, label, log):
    env = dict(os.environ, TMPDIR=os.environ.get('GATE77_TMPDIR', '/tmp'), CI='1', NO_COLOR='1', FORCE_COLOR='0')
    env.pop('GIT_SSH_COMMAND', None)
    cwd = os.path.join(wt, rec['cwd'])
    p = subprocess.run(rec['cmd'], cwd=cwd, capture_output=True, env=env, timeout=int(rec.get('timeout', 900)))
    out = p.stdout.decode('utf-8', 'replace') + p.stderr.decode('utf-8', 'replace')
    out = re.sub(r'\x1b\[[0-9;]*m', '', out)
    open(log, 'w').write(out)
    summ = [l.strip() for l in out.split('\n') if SUMMARY_RX.search(l)]
    return dict(label=label, rc=p.returncode, at=now(), log=log, summary=summ[-6:], out=out)


def needles(res, want):
    hit = [n for n in want if n in res['out']]; return hit, [n for n in want if n not in hit]


def cell_marks(out, cells, mark):
    """shell-suite cells: a line carrying the cell text must start with `ok`/`PASS`/`FAIL` per the suite's own printer."""
    got = {}
    for c in cells:
        ls = [l.strip() for l in out.split('\n') if c in l]
        got[c] = ls[0][:12] if ls else '(absent)'
    if mark == 'FAIL': ok = all(v.upper().startswith('FAIL') for v in got.values())
    else: ok = all(v.lower().startswith(('ok', 'pass', '✓')) for v in got.values())
    return ok, got


def do_run(n, name, wt, outp):
    R = ROWS[n]; recs = [r for r in R['redproof'] if r['name'] == name]
    if len(recs) != 1: print('REFUSED: row #%s has no recipe %r (have %s)' % (n, name, [r['name'] for r in R['redproof']])); return 9
    rec = recs[0]; res = dict(pr=n, recipe=name, claim=rec['claim'], head=R['head_expected'], end_tree=R['end_tree'], runs=[], started=now())
    def fin(rc, verdict):
        res['verdict'] = verdict; res['rc'] = rc; res['ended'] = now()
        for r in res['runs']: r.pop('out', None)
        json.dump(res, open(outp, 'w'), indent=1); print('VERDICT %s rc %d -> %s' % (verdict, rc, outp)); return rc
    if not L.outside_forbidden(wt): print('REFUSED W0: worktree %s is under %s (YOUR scratch worktrees only)' % (wt, L.FORBIDDEN)); return 16
    if os.path.exists(outp): print('REFUSED: --out %s exists (FRESH path only)' % outp); return 9
    _, head = g(wt, 'rev-parse', 'HEAD'); _, tree = g(wt, 'rev-parse', 'HEAD^{tree}'); _, por = g(wt, 'status', '--porcelain', '--untracked-files=all')
    print('W0 wt %s HEAD %s tree %s porcelain %r' % (wt, head[:12], tree[:12], por[:80]))
    if head != R['head_expected'] or tree != R['end_tree']: print('REFUSED W0: HEAD/tree != row #%s head %s / END_TREE %s' % (n, R['head_expected'][:12], R['end_tree'][:12])); return 11
    if por: print('REFUSED W0: the worktree is not clean (porcelain non-empty) — never tamper a dirty tree'); return 11
    if rec.get('needs_s1'):
        miss = [p for p in ('Blockchain/Dev/node_modules', 'Blockchain/Dev/packages/shared/dist/index.js') if not os.path.exists(os.path.join(wt, p))]
        if miss: print('REFUSED S1: %s absent — run S-1 (npm ci --ignore-scripts in Blockchain/Dev; npm run build --workspace=packages/shared) first. NOT a red.' % miss); return 12
    logs = outp + '.logs'; os.makedirs(logs, exist_ok=True)
    G = run_cmd(wt, rec, 'G', os.path.join(logs, 'G.out')); hit, miss = needles(G, rec.get('want_green', []))
    G.update(needles_hit=hit, needles_missed=miss); res['runs'].append(G)
    print('G  rc %d summary %s | green needles missed %s' % (G['rc'], G['summary'][-2:], miss))
    if G['rc'] != rec.get('want_green_rc', 0) or miss or (not G['summary'] and rec.get('want_green')): return fin(1, 'GREEN-NOT-GREEN')
    saved = {}
    for f in rec['files']:
        p = os.path.join(wt, f); b = open(p, 'rb').read(); _, hb = g(wt, 'rev-parse', 'HEAD:' + f)
        _, hh = g(wt, 'hash-object', '--stdin', inp=b)
        if hh != hb: return fin(1, 'SAVED-BYTES-NOT-HEAD %s' % f)
        saved[f] = (b, hb, os.stat(p).st_mode)
    res['saved'] = {f: v[1] for f, v in saved.items()}
    try:
        for f in rec['files']:
            p = os.path.join(wt, f)
            if rec['kind'] == 'revert_to_base':
                b = subprocess.run(['git', '-C', wt, 'show', '%s:%s' % (RAISE_BASE, f)], capture_output=True).stdout
                open(p, 'wb').write(b)
            elif rec['kind'] == 'replace_once':
                t = saved[f][0].decode('utf-8'); c = t.count(rec['old'])
                if c != 1: return fin(1, 'REFUSED-ANCHOR %s: `old` occurs %d times (want exactly 1)' % (f, c))
                open(p, 'wb').write(t.replace(rec['old'], rec['new'], 1).encode('utf-8'))
            else: return fin(9, 'UNKNOWN-KIND %s' % rec['kind'])
            _, ht = g(wt, 'hash-object', p); landed = ht != saved[f][1] and (rec['kind'] != 'replace_once' or rec['new'] in open(p, encoding='utf-8').read())
            print('T  %s tampered (%s): blob %s -> %s | LANDED %s' % (f, rec['kind'], saved[f][1][:12], ht[:12], landed))
            res.setdefault('tamper', {})[f] = dict(blob=ht, landed=landed)
            if not landed: return fin(1, 'TAMPER-DID-NOT-LAND %s' % f)
        Rr = run_cmd(wt, rec, 'R', os.path.join(logs, 'R.out')); hit, miss = needles(Rr, rec.get('want_red', []))
        cells_ok, cells = cell_marks(Rr['out'], rec.get('want_red_cells', []), 'FAIL')
        both_ok, both = cell_marks(Rr['out'], rec.get('want_ok_both', []), 'ok')
        Rr.update(needles_hit=hit, needles_missed=miss, red_cells=cells, ok_both=both); res['runs'].append(Rr)
        print('R  rc %d summary %s | red needles missed %s | red cells %s | controls ok %s' % (Rr['rc'], Rr['summary'][-2:], miss, cells_ok, both_ok))
        loadfail = not Rr['summary'] and bool(rec.get('want_red'))
        red_ok = Rr['rc'] == rec.get('want_red_rc', 1) and not miss and cells_ok and both_ok and not loadfail
    finally:
        for f, (b, hb, mode) in saved.items():
            p = os.path.join(wt, f); open(p, 'wb').write(b); os.chmod(p, mode & 0o7777)
        back = {f: g(wt, 'hash-object', os.path.join(wt, f))[1] for f in saved}; _, por = g(wt, 'status', '--porcelain', '--untracked-files=all')
        res['restored'] = dict(blobs=back, equal_head=all(back[f] == saved[f][1] for f in saved), porcelain=por)
        print('X  restored: every blob == HEAD %s | porcelain %r' % (res['restored']['equal_head'], por[:80]))
    if not (res['restored']['equal_head'] and not por): return fin(1, 'RESTORE-FAILED')
    G2 = run_cmd(wt, rec, 'G2', os.path.join(logs, 'G2.out')); hit, miss = needles(G2, rec.get('want_green', []))
    G2.update(needles_hit=hit, needles_missed=miss); res['runs'].append(G2)
    print('G2 rc %d summary %s | green needles missed %s' % (G2['rc'], G2['summary'][-2:], miss))
    if G2['rc'] != rec.get('want_green_rc', 0) or miss: return fin(1, 'GREEN-NOT-REPRODUCED-AFTER-RESTORE')
    if loadfail: return fin(1, 'LOADFAIL (no summary line on the tamper: a broken instrument, not a red)')
    return fin(0 if red_ok else 1, 'RED-PROVED' if red_ok else 'RED-NOT-AS-WANTED')


def selftest(scratch):
    """A throwaway repo under --scratch: a 2-cell shell suite over a one-line product. Arms: the red fires on a revert; each refusal refuses."""
    if os.path.exists(scratch) and os.listdir(scratch): print('REFUSED: --scratch must be FRESH'); return 9
    os.makedirs(scratch, exist_ok=True); repo = os.path.join(scratch, 'repo'); os.makedirs(os.path.join(repo, 'Blockchain/Dev/scripts/__tests__'))
    env = dict(os.environ, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t.invalid', GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t.invalid')
    def sh(*a): return subprocess.run(a, cwd=repo, env=env, capture_output=True, text=True)
    sh('git', 'init', '-q'); prod = os.path.join(repo, 'Blockchain/Dev/scripts/prod.sh')
    open(prod, 'w').write('echo 3\n'); suite = os.path.join(repo, 'Blockchain/Dev/scripts/__tests__/prod.test.sh')
    open(suite, 'w').write('p=0; f=0\nif [ "$(bash Blockchain/Dev/scripts/prod.sh)" = 2 ]; then echo "  ok   RED two"; p=$((p+1)); else echo "  FAIL RED two"; f=$((f+1)); fi\n'
                           'echo "  ok   CONTROL always"; p=$((p+1))\necho "  $p passed, $f failed"; [ $f -eq 0 ]\n')
    sh('git', 'add', '-A'); sh('git', 'commit', '-q', '-m', 'base (product prints 3: the suite is red here)'); b2 = sh('git', 'rev-parse', 'HEAD').stdout.strip()
    open(prod, 'w').write('echo 2\n'); sh('git', 'commit', '-qam', 'head (the fix)'); h = sh('git', 'rev-parse', 'HEAD').stdout.strip(); t = sh('git', 'rev-parse', 'HEAD^{tree}').stdout.strip()
    global RAISE_BASE
    RAISE_BASE = b2
    rec = dict(name='p', kind='revert_to_base', files=['Blockchain/Dev/scripts/prod.sh'], cwd='.', cmd=['bash', 'Blockchain/Dev/scripts/__tests__/prod.test.sh'],
               needs_s1=False, want_green=['2 passed, 0 failed'], want_red_rc=1, want_red=['1 passed, 1 failed'], want_red_cells=['RED two'], want_ok_both=['CONTROL always'], claim='selftest')
    ROWS['9999'] = dict(head_expected=h, end_tree=t, redproof=[rec, dict(rec, name='anchor0', kind='replace_once', old='NOT-THERE', new='x'),
                                                               dict(rec, name='wrongneedle', want_red=['7 passed, 9 failed'])])
    import contextlib, io
    arms = []
    def arm(name, fn, want_rc, want_line):
        # an arm counts only if it refuses at ITS OWN assert (STANDING_LINES, R 17th): rc AND the asserting line are both compared
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): got = fn()
        text = buf.getvalue(); sys.stdout.write(text)
        f = got == want_rc and want_line in text; arms.append((name, f))
        print('ARM %-40s rc %s want %s | asserting line %r %s | %s' % (name, got, want_rc, want_line, 'SEEN' if want_line in text else 'ABSENT', 'FIRED' if f else 'DID NOT FIRE'))
    o = lambda k: os.path.join(scratch, k + '.json')
    arm('POSITIVE red proved', lambda: do_run('9999', 'p', repo, o('pos')), 0, 'VERDICT RED-PROVED')
    arm('restore landed (porcelain empty)', lambda: sh('git', 'status', '--porcelain').stdout or print('porcelain-empty') or '', '', 'porcelain-empty')
    arm('anchor absent refuses', lambda: do_run('9999', 'anchor0', repo, o('anchor')), 1, 'REFUSED-ANCHOR')
    arm('wrong red needle -> not as wanted', lambda: do_run('9999', 'wrongneedle', repo, o('needle')), 1, 'RED-NOT-AS-WANTED')
    open(prod, 'a').write('# dirty\n'); arm('dirty worktree refuses', lambda: do_run('9999', 'p', repo, o('dirty')), 11, 'the worktree is not clean')
    open(prod, 'w').write('echo 2\n')
    arm('existing --out refuses', lambda: do_run('9999', 'p', repo, o('pos')), 9, 'exists (FRESH path only)')
    open(prod, 'w').write('echo 2\n# a later commit: HEAD moves off the pinned head\n'); sh('git', 'commit', '-qam', 'moved')
    arm('moved HEAD refuses', lambda: do_run('9999', 'p', repo, o('moved')), 11, 'HEAD/tree != row #9999')
    sh('git', 'checkout', '-q', h)
    os.environ['GATE77_FORBIDDEN_ROOT'] = scratch; L.FORBIDDEN = scratch
    arm('worktree under forbidden root refuses', lambda: do_run('9999', 'p', repo, o('forbidden')), 16, 'REFUSED W0: worktree')
    L.FORBIDDEN = K['forbidden_root']
    print('SELFTEST arms fired %d/%d' % (sum(f for _, f in arms), len(arms)))
    return 0 if all(f for _, f in arms) else 1


def main():
    A = sys.argv; mode = A[1] if len(A) > 1 else ''
    if mode == 'list':
        for n, R in ROWS.items():
            for r in R['redproof']: print('#%s %-9s %-15s %s :: %s' % (n, r['name'], r['kind'], ' '.join(r['cmd']), r['claim']))
        return 0
    if mode == 'selftest': return selftest(opt(A, '--scratch') or '')
    if mode == 'run':
        n = L.row_arg(); name = opt(A, '--recipe'); wt = opt(A, '--wt'); outp = opt(A, '--out')
        if not (name and wt and outp): print(__doc__); return 9
        return do_run(n, name, os.path.abspath(wt), os.path.abspath(outp))
    print(__doc__); return 9


if __name__ == '__main__':
    sys.exit(main())
