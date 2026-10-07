#!/usr/bin/env python3
r"""c1_pin_gate73.py — PIN checks for ONE gate73 row. EVERY PR-specific value is a REQUIRED argument compared with kit.json; nothing defaults.
Usage: c1_pin_gate73.py --pr <1407|1409|1408|1410> --repo <YOUR clone> --head <40-hex> --base <40-hex> --parents-n <n> --end-tree <40-hex>
                        --develop <40-hex> [--others 1409=<40-hex>,...]   |   --selftest --repo <clone>
  P1  the head is a commit == kit head_expected (a different head refuses BY NAME: the kit's figures are for that head)
  P2a is a commit; P2b EXACT parent count == --parents-n (a merge commit cannot pass a first-parent read); P2c the parent == --base
  P3  the changed-path SET == kit numstat keys, and each path's +/- == kit numstat (the author's figures)
  P4  tree(head) == --end-tree == kit end_tree
  P5  trailers: `%(trailers)` raw bytes at the head == 1 (the newline) against the CONTROL commit's > 1 (the zero must discriminate)
  P6  0 Co-Authored-By lines in the message (CONTROL: the same grep on a planted line finds 1)
  P7  subject == kit subject; ASCII; carries no `(#`; LANDS len + len(" (#<pr>)") <= squash_max
  P8  only the row's own key(s) hyphenated in the WHOLE message; 0 closing-family words on any KS key (CONTROL planted `Fixes KS-1`)
  P9  modes base -> head == kit modes per code path (a new suite 100644 is RIGHT for run-shell-suites' `bash <file>` / vitest / jest)
  P10 NO-NEW-LEG: every kit tooling path identical base == head == develop (ls-tree object, absent is its own state), EXCEPT the row's
      own declared tooling change (#1407: systemTest/scripts/check-package-format.sh, base -> head only)
  P11 DISJOINT: this row's code paths share NO path with any other row's head diff (--others; the batch's premise)
  P12 base..develop: descends from the base; 0 of this row's code paths moved; whether either platform doc moved (=> a docs merge-in)
  P13 PRE-EXISTING MISMATCH files (Wednesday: base-state, not a finding) byte-identical base == head, blob prefixes == the authors' claim
rc 0 all PASS / 1 any FAIL / 2 refused by name / 11 a required argument != kit.json."""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate73 import K, ROWS, BASE, Tally, git, refuse_absent, opt, obj_at, mode_at, code_paths, row_arg


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
    subj = git(repo, 'log', '-1', '--format=%s', head).rstrip('\n'); lands = len(subj) + len(' (#%s)' % r)
    t.check('P7', subj == R['subject'] and subj.isascii() and '(#' not in subj and lands <= K['squash_max'],
            'subject %d chars == kit %s, ASCII %s, no `(#` %s, LANDS %d <= %d' % (len(subj), subj == R['subject'], subj.isascii(), '(#' not in subj, lands, K['squash_max']))
    hy = sorted(set(re.findall(r'\bKS-\d+\b', msg))); cl = re.findall(K['closing_rx'], msg, re.I); clc = re.findall(K['closing_rx'], msg + '\nFixes KS-1\n', re.I)
    t.check('P8', hy == sorted(R['keys_hyphenated_allowed']) and not cl and len(clc) == 1,
            'hyphenated keys in the message %s (want %s) | de-hyphenated %s | closing-family on a key %d | CONTROL planted `Fixes KS-1` %d' % (
                hy, R['keys_hyphenated_allowed'], sorted(set(re.findall(r'\bKS \d+\b', msg))), len(cl), len(clc)))
    md = {p: [mode_at(repo, base, p), mode_at(repo, head, p)] for p in code_paths(R)}
    t.check('P9', md == R['modes'], 'modes base->head %s == kit: %s' % ({os.path.basename(p): '%s->%s' % tuple(v) for p, v in md.items()}, md == R['modes']))
    own_tool = K['tooling_changed_by_row'].get(r, []); bad = []; n = 0
    for p in K['tooling_paths']:
        b, h, d = obj_at(repo, base, p), obj_at(repo, head, p), obj_at(repo, dev, p); n += 1
        if p in own_tool:
            if b == h or h != obj_at(repo, R['head_expected'], p) or b != d: bad.append('%s (own declared change: base %s head %s develop %s)' % (p, b[:8], h[:8], d[:8]))
        elif not (b == h == d) or not b: bad.append('%s base %s head %s develop %s' % (p, b[:8] or 'ABSENT', h[:8] or 'ABSENT', d[:8] or 'ABSENT'))
    t.check('P10', not bad, 'NO-NEW-LEG: %d tooling paths identical base == head == develop (own declared change %s accepted base->head only)%s' % (
        n, own_tool or 'none', '' if not bad else ' | MOVED: ' + '; '.join(bad)))
    if others:
        mine = set(code_paths(R)); shared = {}
        for o, oh in others.items():
            if o == r: continue
            od = set(l for l in git(repo, 'diff', '--name-only', base, oh).split('\n') if l and not l.startswith('Projects Documents/'))
            if mine & od: shared[o] = sorted(mine & od)
        t.check('P11', not shared, 'DISJOINT: code paths shared with %s: %s' % (sorted(o for o in others if o != r), shared or 'none'))
    else:
        t.info('P11', 'not run (no --others): disjointness across the batch NOT checked here')
    anc = git(repo, 'merge-base', '--is-ancestor', base, dev, check=False)[0] == 0
    moved = [p for p in code_paths(R) if obj_at(repo, base, p) != obj_at(repo, dev, p)]
    docs_moved = [p for p in (K['docs']['flow'], K['docs']['cheat']) if obj_at(repo, base, p) != obj_at(repo, dev, p)]
    npaths = len([l for l in git(repo, 'diff', '--name-only', base, dev).split('\n') if l])
    t.check('P12', anc and not moved, 'develop %s descends from the base: %s | base..develop %d path(s) | row code paths moved: %s | platform docs moved: %s%s' % (
        dev[:12], anc, npaths, moved or 'none', [os.path.basename(p) for p in docs_moved] or 'none',
        ' => a DOCS-ONLY KEEP-BOTH MERGE-IN is required (c4 chain/qm)' if docs_moved else ' => develop == base for the docs: NO merge-in, squash tree == END_TREE' if dev == base else ''))
    pm = K['preexisting_mismatch']['files']; bad13 = []
    for p, pre in pm.items():
        b, h = obj_at(repo, base, p), obj_at(repo, head, p)
        if not (b and b == h and b.startswith(pre)): bad13.append('%s base %s head %s claim %s' % (p, b[:12], h[:12], pre))
    t.check('P13', not bad13, 'PRE-EXISTING MISMATCH files byte-identical base == head and == the authors\' blob prefixes (%d files)%s' % (len(pm), '' if not bad13 else ': ' + '; '.join(bad13)))
    return t.end()


def selftest(repo):
    """planted arms that MUST fail, each run through run() with a wrong value; plus one green run per row."""
    import io, contextlib
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    def quiet(*a):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): rc = run(*a)
        return rc, buf.getvalue()
    others = {x: ROWS[x]['head_expected'] for x in ROWS}
    for r, R in ROWS.items():
        rc, o = quiet(repo, r, R['head_expected'], BASE, 1, R['end_tree'], BASE, others)
        rep(rc == 0, 'GREEN #%s at its pins: rc %d (%s)' % (r, rc, ' '.join(l for l in o.split('\n') if l.startswith(('CHECKED', '0 FAIL', '1 FAIL', '2 FAIL')))))
    R = ROWS['1407']
    rc, o = quiet(repo, '1407', ROWS['1409']['head_expected'], BASE, 1, R['end_tree'], BASE, others)
    rep(rc == 1 and 'FAIL P1 ' in o and 'FAIL P3 ' in o, 'PLANTED wrong head (#1409\'s) for #1407: P1 + P3 FAIL')
    rc, o = quiet(repo, '1407', R['head_expected'], BASE, 2, R['end_tree'], BASE, others)
    rep(rc == 1 and 'FAIL P2b ' in o, 'PLANTED --parents-n 2: P2b FAILS')
    rc, o = quiet(repo, '1407', R['head_expected'], BASE, 1, ROWS['1408']['end_tree'], BASE, others)
    rep(rc == 1 and 'FAIL P4 ' in o, 'PLANTED wrong --end-tree: P4 FAILS')
    parent = git(repo, 'rev-parse', BASE + '^1').strip()
    rc, o = quiet(repo, '1407', R['head_expected'], BASE, 1, R['end_tree'], parent, others)
    rep(rc == 1 and 'FAIL P12 ' in o, 'PLANTED ancestor develop %s: P12 FAILS (does not descend)' % parent[:12])
    # a planted "other row" that touches #1407's code path must break DISJOINT
    rc, o = quiet(repo, '1407', R['head_expected'], BASE, 1, R['end_tree'], BASE, {'1407': R['head_expected'], 'X': R['head_expected']})
    rep(rc == 1 and 'FAIL P11 ' in o, 'PLANTED other row sharing #1407\'s code paths: P11 FAILS')
    # #1408 run with #1407's tooling exception missing: kit edited in memory
    K['tooling_changed_by_row'] = {}
    rc, o = quiet(repo, '1407', R['head_expected'], BASE, 1, R['end_tree'], BASE, others)
    rep(rc == 1 and 'FAIL P10 ' in o and 'check-package-format.sh' in o, 'PLANTED: #1407\'s declared tooling change UNDECLARED -> P10 FAILS naming check-package-format.sh')
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
    rc = refuse_absent(repo, [('--head', head), ('--base', base), ('--develop', dev), ('trailer control', K['trailer_control'])] + [('--others ' + k, v) for k, v in others.items()])
    return rc or run(repo, r, head, base, int(npar), tree, dev, others)


if __name__ == '__main__':
    sys.exit(main())
