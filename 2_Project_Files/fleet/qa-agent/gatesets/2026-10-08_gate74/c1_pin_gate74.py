#!/usr/bin/env python3
r"""c1_pin_gate74.py — PIN checks for gate74's ONE row (#1423 KS-1164). EVERY PR-specific value is a REQUIRED argument compared with
kit.json; nothing defaults. Carried from c1_pin_gate73.py (P1-P13) and re-keyed by the gate74 drafter: one row; P10 re-shaped (develop
moved tooling paths since the base, so the invariant is head == base, with develop's moves REPORTED); P11 is disjointness from #1422
(the other PR landing in the same merge round, tier 3); P14 is new (the PR's TEST-ONLY claim and the earlier KS-1164 fix).
Usage: c1_pin_gate74.py --pr 1423 --repo <YOUR clone> --head <40-hex> --base <40-hex> --parents-n <n> --end-tree <40-hex>
                        --develop <40-hex> [--others 1422=<40-hex>]   |   --selftest --repo <clone>
  P1  the head is a commit == kit head_expected (a different head refuses BY NAME: the kit's figures are for that head)
  P2a is a commit; P2b EXACT parent count == --parents-n (a merge commit cannot pass a first-parent read); P2c the parent == --base
  P3  the changed-path SET == kit numstat keys, and each path's +/- == kit numstat (the author's figures)
  P4  tree(head) == --end-tree == kit end_tree
  P5  trailers: `%(trailers)` raw bytes at the head == 1 (the newline) against the CONTROL commit's > 1 (the zero must discriminate)
  P6  0 Co-Authored-By lines in the message (CONTROL: the same grep on a planted line finds 1)
  P7  subject == kit subject; ASCII; carries no `(#`; len(subject) <= squash_max (MG-11 as superseded 2026-10-07: no suffix arithmetic)
  P8  only the row's own key hyphenated in the WHOLE message; 0 closing-family words on any KS key (CONTROL planted `Fixes KS-1`)
  P9  modes base -> head == kit modes per code path (the new vitest suite 100644)
  P10 NO-NEW-LEG: every kit tooling path identical base == head (ls-tree object; absent is its own state, and absent at BOTH is
      reported, not failed). develop's moves of tooling paths since the base are REPORTED by name: they are why every suite also runs
      on the SIM squash tree (c3 `--tree merged`).
  P11 DISJOINT: this row's paths share NO path with #1422's head diff (--others 1422=<head>)
  P12 base..develop: descends from the base; 0 of this row's code paths moved; whether either platform doc moved (c4 `merged` then
      decides by BYTES whether a merge-in is needed — a moved doc is not by itself a merge-in)
  P13 PRE-EXISTING MISMATCH files (gate73 R3: base-state) byte-identical base == head == develop, blob prefixes == the kit's
  P14 TEST-ONLY: 0 product paths in the diff (every path is the new suite or a platform doc); systemTest/performance/gate/report.ts
      blob == kit report_ts_blob at base, head AND develop; the KS-1164 fix commit (#1271) is an ANCESTOR of the base.
rc 0 all PASS / 1 any FAIL / 2 refused by name / 11 a required argument != kit.json."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate74 import K, ROWS, BASE, Tally, git, refuse_absent, opt, obj_at, mode_at, code_paths, row_arg


def run(repo, r, head, base, npar, tree, dev, others):
    R = ROWS[r]; t = Tally()
    print('ROW #%s (%s) head %s base %s develop %s' % (r, R['ticket'], head[:12], base[:12], dev[:12]))
    t.check('P1', head == R['head_expected'], 'head %s == kit head_expected %s' % (head[:12], R['head_expected'][:12]))
    typ = git(repo, 'cat-file', '-t', head).strip()
    par = git(repo, 'log', '-1', '--format=%P', head).split()
    t.check('P2a', typ == 'commit', 'object type %s' % typ)
    t.check('P2b', len(par) == npar, 'parent count %d == --parents-n %d (whole %%P read, never a first-parent read)' % (len(par), npar))
    t.check('P2c', par[:1] == [base], 'parent %s == --base %s' % ([p[:12] for p in par], base[:12]))
    ns = {}
    for l in git(repo, 'diff', '--numstat', base, head).strip().split('\n'):
        if l: a, d, p = l.split('\t', 2); ns[p] = [int(a), int(d)]
    want = {p: v for p, v in R['numstat'].items()}
    t.check('P3', ns == want, 'numstat %d paths == kit %d: %s%s' % (len(ns), len(want), ns == want,
            '' if ns == want else ' | extra %s missing %s differing %s' % (sorted(set(ns) - set(want)), sorted(set(want) - set(ns)),
                                                                          sorted(p for p in ns if p in want and ns[p] != want[p]))))
    ht = git(repo, 'rev-parse', head + '^{tree}').strip()
    t.check('P4', ht == tree == R['end_tree'], 'tree %s == --end-tree %s == kit %s' % (ht[:12], tree[:12], R['end_tree'][:12]))
    tb = len(git(repo, 'log', '-1', '--format=%(trailers)', head).encode()); cb = len(git(repo, 'log', '-1', '--format=%(trailers)', K['trailer_control']).encode())
    t.check('P5', tb == 1 and cb > 1, 'trailers raw bytes at the head %d (want 1 = the newline) | CONTROL %s %d raw bytes' % (tb, K['trailer_control'][:12], cb))
    msg = git(repo, 'log', '-1', '--format=%B', head)
    co = len(re.findall(r'(?im)^co-authored-by:', msg)); coc = len(re.findall(r'(?im)^co-authored-by:', msg + '\nCo-Authored-By: planted <p@x>\n'))
    t.check('P6', co == 0 and coc == 1, 'Co-Authored-By lines %d | CONTROL planted line found %d' % (co, coc))
    subj = git(repo, 'log', '-1', '--format=%s', head).rstrip('\n')
    t.check('P7', subj == R['subject'] and subj.isascii() and '(#' not in subj and len(subj) <= K['squash_max'],
            'subject %d chars == kit %s, ASCII %s, no `(#` %s, len %d <= %d (no suffix arithmetic: MG-11 as superseded)' % (
                len(subj), subj == R['subject'], subj.isascii(), '(#' not in subj, len(subj), K['squash_max']))
    hy = sorted(set(re.findall(r'\bKS-\d+\b', msg))); cl = re.findall(K['closing_rx'], msg, re.I); clc = re.findall(K['closing_rx'], msg + '\nFixes KS-1\n', re.I)
    t.check('P8', hy == sorted(R['keys_hyphenated_allowed']) and not cl and len(clc) == 1,
            'hyphenated keys in the message %s (want %s) | de-hyphenated %s | closing-family on a key %d | CONTROL planted `Fixes KS-1` %d' % (
                hy, R['keys_hyphenated_allowed'], sorted(set(re.findall(r'\bKS \d+\b', msg))), len(cl), len(clc)))
    md = {p: [mode_at(repo, base, p), mode_at(repo, head, p)] for p in code_paths(R)}
    t.check('P9', md == R['modes'], 'modes base->head %s == kit: %s' % ({os.path.basename(p): '%s->%s' % tuple(v) for p, v in md.items()}, md == R['modes']))
    bad, devmoved, absent_both, n = [], [], [], 0
    for p in K['tooling_paths']:
        b, h, d = obj_at(repo, base, p), obj_at(repo, head, p), obj_at(repo, dev, p); n += 1
        if b != h: bad.append('%s base %s head %s' % (p, b[:8] or 'ABSENT', h[:8] or 'ABSENT'))
        if not b and not h: absent_both.append(p)
        if b != d: devmoved.append(os.path.basename(p))
    t.check('P10', not bad, 'NO-NEW-LEG: %d tooling paths identical base == head%s' % (n, '' if not bad else ' | MOVED BY THE PR: ' + '; '.join(bad)))
    t.info('P10d', 'develop moved %d tooling path(s) since the base: %s (=> every suite ALSO runs on the SIM squash tree)%s' % (
        len(devmoved), devmoved or 'none', (' | absent at base AND head: %s' % absent_both) if absent_both else ''))
    if others:
        mine = set(R['numstat']); shared = {}
        for o, oh in others.items():
            if o == r: continue
            od = set(l for l in git(repo, 'diff', '--name-only', git(repo, 'merge-base', base, oh).strip(), oh).split('\n') if l)
            if mine & od: shared[o] = sorted(mine & od)
        t.check('P11', not shared, 'DISJOINT from %s (three-dot): shared paths %s' % (sorted(o for o in others if o != r), shared or 'none'))
    else:
        t.info('P11', 'not run (no --others): disjointness from #1422 NOT checked here')
    anc = git(repo, 'merge-base', '--is-ancestor', base, dev, check=False)[0] == 0
    moved = [p for p in code_paths(R) if obj_at(repo, base, p) != obj_at(repo, dev, p)]
    docs_moved = [p for p in (K['docs']['flow'], K['docs']['cheat']) if obj_at(repo, base, p) != obj_at(repo, dev, p)]
    bd = [l for l in git(repo, 'diff', '--name-only', base, dev).split('\n') if l]
    bdev = [p for p in bd if p.startswith('Blockchain/Dev/')]
    t.check('P12', anc and not moved, 'develop %s descends from the base: %s | base..develop %d path(s), %d under Blockchain/Dev/ | row code paths moved: %s | platform docs moved: %s%s' % (
        dev[:12], anc, len(bd), len(bdev), moved or 'none', [os.path.basename(p) for p in docs_moved] or 'none',
        ' => c4 `merged` decides by BYTES whether a merge-in is needed' if docs_moved else ' => develop == base for the docs: squash tree == END_TREE' if dev == base else ''))
    pm = K['preexisting_mismatch']['files']; bad13 = []
    for p, pre in pm.items():
        b, h, d = obj_at(repo, base, p), obj_at(repo, head, p), obj_at(repo, dev, p)
        if not (b and b == h == d and b.startswith(pre)): bad13.append('%s base %s head %s develop %s kit %s' % (p, b[:12], h[:12], d[:12], pre))
    t.check('P13', not bad13, 'PRE-EXISTING MISMATCH files byte-identical base == head == develop and == the kit\'s blob prefixes (%d files)%s' % (len(pm), '' if not bad13 else ': ' + '; '.join(bad13)))
    product = [p for p in R['numstat'] if not p.startswith('Projects Documents/') and '/tests/' not in p]
    rp = 'systemTest/performance/gate/report.ts'
    rb = {k: obj_at(repo, v, rp) for k, v in (('base', base), ('head', head), ('develop', dev))}
    fx = git(repo, 'merge-base', '--is-ancestor', R['ks1164_fix_commit'], base, check=False)[0] == 0
    t.check('P14', not product and all(v == R['report_ts_blob'] for v in rb.values()) and fx,
            'TEST-ONLY: product paths in the diff %s | report.ts blob %s (kit %s) | KS-1164 fix %s (#%s) is an ancestor of the base: %s' % (
                product or 'none', {k: v[:12] for k, v in rb.items()}, R['report_ts_blob'][:12], R['ks1164_fix_commit'][:12], R['ks1164_fix_pr'], fx))
    return t.end()


def selftest(repo):
    """planted arms that MUST fail, each run through run() with a wrong value; plus one green run."""
    import io, contextlib
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    def quiet(*a):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): rc = run(*a)
        return rc, buf.getvalue()
    R = ROWS['1423']; DEV = K['develop_at_draft']; H22 = K['t3_1422']['head']
    others = {'1422': H22}
    rc, o = quiet(repo, '1423', R['head_expected'], BASE, 1, R['end_tree'], DEV, others)
    rep(rc == 0, 'GREEN #1423 at its pins on develop %s: rc %d (%s)' % (DEV[:12], rc, ' '.join(l for l in o.split('\n') if l.startswith(('CHECKED', '0 FAIL', '1 FAIL', '2 FAIL')))))
    rc, o = quiet(repo, '1423', H22, BASE, 1, R['end_tree'], DEV, others)
    rep(rc == 1 and 'FAIL P1 ' in o and 'FAIL P3 ' in o, 'PLANTED wrong head (#1422\'s) for #1423: P1 + P3 FAIL')
    rc, o = quiet(repo, '1423', R['head_expected'], BASE, 2, R['end_tree'], DEV, others)
    rep(rc == 1 and 'FAIL P2b ' in o, 'PLANTED --parents-n 2: P2b FAILS')
    rc, o = quiet(repo, '1423', R['head_expected'], BASE, 1, K['predicted_squash']['tree'], DEV, others)
    rep(rc == 1 and 'FAIL P4 ' in o, 'PLANTED wrong --end-tree (the squash tree): P4 FAILS')
    parent = git(repo, 'rev-parse', BASE + '^1').strip()
    rc, o = quiet(repo, '1423', R['head_expected'], BASE, 1, R['end_tree'], parent, others)
    rep(rc == 1 and 'FAIL P12 ' in o, 'PLANTED ancestor develop %s: P12 FAILS (does not descend)' % parent[:12])
    rc, o = quiet(repo, '1423', R['head_expected'], BASE, 1, R['end_tree'], DEV, {'X': R['head_expected']})
    rep(rc == 1 and 'FAIL P11 ' in o, 'PLANTED an "other" PR sharing #1423\'s paths: P11 FAILS')
    keep = R['report_ts_blob']; R['report_ts_blob'] = '0' * 40
    rc, o = quiet(repo, '1423', R['head_expected'], BASE, 1, R['end_tree'], DEV, others)
    R['report_ts_blob'] = keep
    rep(rc == 1 and 'FAIL P14 ' in o, 'PLANTED wrong report.ts blob in the kit: P14 FAILS')
    keep = K['tooling_paths']; K['tooling_paths'] = keep + [list(R['numstat'])[0]]
    rc, o = quiet(repo, '1423', R['head_expected'], BASE, 1, R['end_tree'], DEV, others)
    K['tooling_paths'] = keep
    rep(rc == 1 and 'FAIL P10 ' in o, 'PLANTED: a path the PR changes declared as tooling -> P10 FAILS (the PR would be adding a leg)')
    keep = R['ks1164_fix_commit']; R['ks1164_fix_commit'] = R['head_expected']
    rc, o = quiet(repo, '1423', R['head_expected'], BASE, 1, R['end_tree'], DEV, others)
    R['ks1164_fix_commit'] = keep
    rep(rc == 1 and 'FAIL P14 ' in o, 'PLANTED the fix commit = the head (NOT an ancestor of the base): P14 FAILS')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]; repo = opt(A, '--repo')
    if not repo: print(__doc__); return 2
    if '--selftest' in A: return selftest(repo)
    r = row_arg(); R = ROWS[r]
    head, base, npar, tree, dev = opt(A, '--head'), opt(A, '--base'), opt(A, '--parents-n'), opt(A, '--end-tree'), opt(A, '--develop')
    miss = [k for k, v in (('--head', head), ('--base', base), ('--parents-n', npar), ('--end-tree', tree), ('--develop', dev)) if not v]
    if miss: print('REFUSED: required argument(s) missing: %s' % miss); return 2
    for k, v, want in (('--base', base, R['parents'][0]), ('--parents-n', npar, str(R['parent_count'])), ('--end-tree', tree, R['end_tree'])):
        if v != want: print('REFUSED: WRONG VALUE %s %s != kit.json %s' % (k, v, want)); return 11
    others = {}
    for kv in (opt(A, '--others') or '').split(','):
        if '=' in kv: k, v = kv.split('=', 1); others[k] = v
    rc = refuse_absent(repo, [('--head', head), ('--base', base), ('--develop', dev), ('trailer control', K['trailer_control']),
                              ('KS-1164 fix', R['ks1164_fix_commit'])] + [('--others ' + k, v) for k, v in others.items()])
    return rc or run(repo, r, head, base, int(npar), tree, dev, others)


if __name__ == '__main__':
    sys.exit(main())
