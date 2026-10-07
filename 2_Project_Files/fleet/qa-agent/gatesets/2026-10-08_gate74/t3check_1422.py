#!/usr/bin/env python3
r"""t3check_1422.py — the merge seat's READ-BACK instrument for #1422 (§5d WHY comments), which lands on Wednesday's TIER-3 authority
(her through-code read; no gate). Written by the gate74 drafter. It REPEATS the through-code facts at the moment of landing so the seat
never lands on a stale read; it is NOT a gate and grants nothing — the authority is Wednesday's tier-3 GO mail.
Usage: t3check_1422.py --repo <YOUR clone> --head <40-hex> --base <40-hex> --develop <40-hex> [--expect-tree <40-hex>]  |  --selftest --repo <clone>
  C1 head == kit t3_1422.head; ONE parent == --base; numstat == kit (3 files, +9/-0); the three -U0 hunk headers == kit (located BY HUNK)
  C2 COMMENT-ONLY: `git diff -U0 -w base head` — removed lines 0; added lines whose stripped text does not start with `//` or `#`: 0.
     CONTROL 1: total added lines == 9 (the zero is over a non-empty population). CONTROL 2: a planted `+  const x = 1;` reads NON-comment.
  C3 0 platform docs touched (no §4 block owed: the PR body's own reading, Wednesday accepted it through-code)
  C4 merge-tree --write-tree <develop> <head> in YOUR clone: rc 0; diff(develop, merged) == the 3 paths; each merged blob == the head's
  C5 base..develop moved 0 of the 3 paths (the through-code read still describes what lands)
  C6 LEG-14 EXPOSURE, stated: the PR's own changed set carries 2 Blockchain/Dev/ paths, so ANY push to its branch (a merge-in) runs the
     full preflight and is refused while KS-1450 is open; the squash itself is an API call and runs no local hook.
  C7 --expect-tree given: merged tree == it
rc 0 all PASS / 1 any FAIL / 2 refused / 11 a value != kit."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate74 import K, Tally, git, wgit, obj_at, opt, refuse_absent, outside_forbidden

T3 = K['t3_1422']


def comment_only(diff_text):
    added = [l[1:] for l in diff_text.split('\n') if l.startswith('+') and not l.startswith('+++')]
    removed = [l for l in diff_text.split('\n') if l.startswith('-') and not l.startswith('---')]
    nonc = [a for a in added if a.strip() and not a.strip().startswith(('//', '#'))]
    return added, removed, nonc


def run(repo, head, base, dev, expect_tree=None):
    t = Tally()
    par = git(repo, 'log', '-1', '--format=%P', head).split()
    ns = {}
    for l in git(repo, 'diff', '--numstat', base, head).strip().split('\n'):
        if l: a, d, p = l.split('\t', 2); ns[p] = [int(a), int(d)]
    hunks = {}
    for p in T3['numstat']:
        hunks[p] = [l.split(' @@')[0] + ' @@' for l in git(repo, 'diff', '-U0', base, head, '--', p).split('\n') if l.startswith('@@')]
    t.check('C1', head == T3['head'] and par == [base] and ns == T3['numstat'] and all(hunks[p] == [T3['hunks'][p]] for p in T3['numstat']),
            'head %s == kit %s | parents %s == [base %s] | numstat == kit %s | hunks by -U0 header %s' % (
                head[:12], T3['head'][:12], [x[:12] for x in par], base[:12], ns == T3['numstat'], {os.path.basename(p): h for p, h in hunks.items()}))
    added, removed, nonc = comment_only(git(repo, 'diff', '-U0', '-w', base, head))
    _, _, ctl = comment_only('+  const x = 1;\n')
    t.check('C2', not removed and not nonc and len(added) == 9 and len(ctl) == 1,
            'COMMENT-ONLY: removed %d | non-comment added %d %s | CONTROL total added %d (want 9) | CONTROL planted `const x = 1;` reads non-comment: %d' % (
                len(removed), len(nonc), nonc[:2], len(added), len(ctl)))
    docs = [p for p in ns if p.startswith('Projects Documents/')]
    t.check('C3', not docs, 'platform docs touched: %s' % (docs or 'none'))
    if not outside_forbidden(repo):
        t.check('C4', False, 'REFUSED: --repo %s is under %s; merge-tree writes objects' % (repo, K['forbidden_root'])); return t
    rc, o, e = wgit(repo, 'merge-tree', '--write-tree', '--name-only', dev, head)
    tree = o.split('\n')[0].strip()
    moved = sorted(l for l in git(repo, 'diff', '--name-only', dev, tree).split('\n') if l) if rc == 0 else []
    beq = rc == 0 and all(obj_at(repo, tree, p) == obj_at(repo, head, p) for p in T3['numstat'])
    t.check('C4', rc == 0 and moved == sorted(T3['numstat']) and beq, 'merge-tree develop %s + head: rc %d tree %s | diff(develop, merged) %d paths == the 3: %s | blobs == head %s' % (
        dev[:12], rc, tree[:12], len(moved), moved == sorted(T3['numstat']), beq))
    bm = [p for p in T3['numstat'] if obj_at(repo, base, p) != obj_at(repo, dev, p)]
    t.check('C5', not bm, 'base..develop moved %d of the 3 paths %s' % (len(bm), bm or ''))
    bdev = [p for p in ns if p.startswith('Blockchain/Dev/')]
    t.info('C6', 'LEG-14 EXPOSURE: the PR\'s own changed set carries %d Blockchain/Dev/ path(s) %s — a PUSH to its branch runs the full preflight (refused while KS-1450 is open); the SQUASH is an API call (no hook). MERGE-IN NEEDED: %s' % (
        len(bdev), [os.path.basename(p) for p in bdev], 'no' if rc == 0 else 'yes — STOP'))
    if expect_tree: t.check('C7', tree == expect_tree, 'merged tree %s == --expect-tree %s' % (tree[:12], expect_tree[:12]))
    print('PREDICTED_TREE=%s' % tree)
    return t


def selftest(repo):
    import io, contextlib
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    def quiet(*a):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): tt = run(*a)
        return tt, buf.getvalue()
    dev = K['develop_at_draft']; b = T3['base']; h = T3['head']
    tt, o = quiet(repo, h, b, dev, K['predicted_both']['1422_onto_develop'])
    rep(not tt.fails and tt.n == 6, 'GREEN at the pins: %d checked, fails %s' % (tt.n, tt.fails))
    sim = K['predicted_squash']['sim_commit_in_drafter_scratch']
    have_sim = git(repo, 'cat-file', '-t', sim, check=False)[0] == 0
    tt, o = quiet(repo, h, b, sim if have_sim else dev, K['predicted_both']['1422_onto_develop_plus_1423' if have_sim else '1422_onto_develop'])
    rep(not tt.fails, 'GREEN onto the SIM develop + #1423 (when the drafter SIM commit is in this clone; else develop): fails %s' % tt.fails)
    r23 = K['rows']['1423']['head_expected']
    tt, o = quiet(repo, r23, b, dev)
    rep('C1' in tt.fails and 'C2' in tt.fails, 'PLANTED #1423\'s head (a real code/doc change): C1 + C2 FAIL')
    _, _, n = comment_only('+// fine\n+# fine\n+   \n+  return x;\n')
    rep(n == ['  return x;'], 'comment_only reads exactly the one code line among comments/blank: %s' % n)
    tt, o = quiet(repo, h, b, dev, '0' * 40)
    rep('C7' in tt.fails, 'PLANTED wrong --expect-tree: C7 FAILS')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]; repo = opt(A, '--repo')
    if not repo: print(__doc__); return 2
    if '--selftest' in A: return selftest(repo)
    head, base, dev = opt(A, '--head'), opt(A, '--base'), opt(A, '--develop')
    if not (head and base and dev): print('REFUSED: --head --base --develop are REQUIRED'); return 2
    if head != T3['head'] or base != T3['base']: print('REFUSED: WRONG VALUE head/base != kit t3_1422 (%s / %s)' % (T3['head'][:12], T3['base'][:12])); return 11
    rc = refuse_absent(repo, [('--head', head), ('--base', base), ('--develop', dev)])
    return rc or run(repo, head, base, dev, opt(A, '--expect-tree')).end()


if __name__ == '__main__':
    sys.exit(main())
