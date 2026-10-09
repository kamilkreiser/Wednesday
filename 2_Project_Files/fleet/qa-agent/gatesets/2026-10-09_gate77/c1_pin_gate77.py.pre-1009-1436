#!/usr/bin/env python3
"""c1_pin_gate77.py — PIN one row (or --all) of gate77 against kit.json, on the develop you read NOW. READ verbs only.

  c1_pin_gate77.py --pr <n> --repo <your clone> --develop <40-hex>      one row
  c1_pin_gate77.py --all --repo <clone> --develop <40-hex>             every row (rc 1 if any row fails)
  c1_pin_gate77.py --selftest --repo <clone> --develop <40-hex>        planted arms: every one MUST fail (rc 0 only if all fire)

P1 head resolvable and == kit head_expected          (fails: a moved head / a wrong pin)
P2 ONE parent == kit raise_base                       (fails: a rebased or multi-commit branch)
P3 tree == kit end_tree                               (fails: any content change at the same parent)
P4 numstat (base..head) == kit numstat EXACTLY        (fails: a file added / dropped / resized)
P5 doc paths == the two platform docs; code paths under Blockchain/   (fails: a stray path outside the declared surface)
P6 0 trailers (bytes of %(trailers) <= 1) vs the trailer CONTROL commit (> 1 bytes, else the instrument is blind)
P7 develop descends from raise_base, AND develop's advance (base..develop) touches NO code path of this row (fails: RE-GATE needed)
P8 merge-tree head vs develop: conflict set SUBSET of the two docs (fails: a code conflict) — with the KNOWN-CONFLICT control pair
   reading rc 1 naming both docs, and head vs raise_base reading rc 0 with tree == END_TREE (else the instrument is broken)
INFO subject opens with `<own key>:` (the squash subject is re-declared at the gate either way), closing adjacency (both regexes),
     foreign hyphenated keys in the commit message, hyphenated keys in the row's ADDED code lines (SKILL §5d: does the own key appear?)
"""
import re, sys
from lib_gate77 import K, ROWS, RAISE_BASE, DOC_PATHS, git, wgit, opt, numstat, changed_paths, resolvable, refuse_absent, Tally


def merge_tree(repo, a, b):
    rc, o, e = wgit(repo, 'merge-tree', '--write-tree', '--name-only', '--no-messages', a, b)
    lines = [l for l in o.split('\n') if l]
    return rc, (lines[0] if lines else ''), sorted(lines[1:]), e


def pin_row(repo, n, dev, R=None, T=None, quiet=False):
    R = R or ROWS[n]; T = T or Tally(); h = R['head_expected']
    print('--- row #%s %s %s head %s' % (n, R['ticket'], R['author_seat'], h))
    if not resolvable(repo, h):
        T.check('P1', False, '#%s head %s ABSENT from %s (fetch by sha)' % (n, h[:12], repo)); return T
    T.check('P1', git(repo, 'rev-parse', h).strip() == h, '#%s head resolvable == kit %s' % (n, h[:12]))
    par = git(repo, 'log', '-1', '--format=%P', h).split()
    T.check('P2', par == [RAISE_BASE], '#%s parents %s == [raise_base %s]' % (n, [p[:12] for p in par], RAISE_BASE[:12]))
    tr = git(repo, 'rev-parse', h + '^{tree}').strip()
    T.check('P3', tr == R['end_tree'], '#%s tree %s == END_TREE %s' % (n, tr[:12], R['end_tree'][:12]))
    N = numstat(repo, RAISE_BASE, h)
    T.check('P4', N == R['numstat'], '#%s numstat %d paths +%d/-%d == kit %d paths +%d/-%d%s' % (
        n, len(N), sum(v[0] for v in N.values()), sum(v[1] for v in N.values()), len(R['numstat']), R['plus'], R['minus'],
        '' if N == R['numstat'] else ' DIFF paths %s' % sorted(p for p in set(N) | set(R['numstat']) if N.get(p) != R['numstat'].get(p))))
    docs = sorted(p for p in N if p in DOC_PATHS); code = sorted(p for p in N if p not in DOC_PATHS)
    T.check('P5', docs == sorted(DOC_PATHS) and all(p.startswith('Blockchain/') for p in code),
            '#%s docs %d/2, code paths %d all under Blockchain/' % (n, len(docs), len(code)))
    tb = len(git(repo, 'log', '-1', '--format=%(trailers)', h)); cb = len(git(repo, 'log', '-1', '--format=%(trailers)', K['trailer_control']))
    T.check('P6', tb <= 1 and cb > 1, '#%s trailer bytes %d (want <= 1) | CONTROL %s %d bytes (want > 1)' % (n, tb, K['trailer_control'][:12], cb))
    anc = git(repo, 'merge-base', '--is-ancestor', RAISE_BASE, dev, check=False)[0] == 0
    adv = changed_paths(repo, RAISE_BASE, dev); hit = sorted(set(adv) & set(code))
    T.check('P7', anc and not hit, '#%s develop %s descends from raise_base: %s | advance %d paths, touching this row\'s code: %s' % (
        n, dev[:12], anc, len(adv), hit or 'none'))
    rc, t, conf, _ = merge_tree(repo, dev, h)
    rc0, t0, conf0, _ = merge_tree(repo, RAISE_BASE, h)
    c = K['merge_tree_control']; rcc, _, confc, _ = merge_tree(repo, c['ours'], c['theirs'])
    ctl_ok = rcc == 1 and confc == sorted(c['files']) and rc0 == 0 and t0 == R['end_tree']
    T.check('P8', set(conf) <= set(DOC_PATHS) and ctl_ok,
            '#%s merge-tree vs develop %s: rc %d, conflicted %s (want SUBSET of the 2 docs) | CONTROLS: known pair rc %d %d docs; vs raise_base rc %d tree==END_TREE %s' % (
                n, dev[:12], rc, [p.split('/')[-1] for p in conf] or 'none', rcc, len(confc), rc0, t0 == R['end_tree']))
    msg = git(repo, 'log', '-1', '--format=%B', h); subj = msg.split('\n', 1)[0]
    T.info('SUBJ', '#%s head subject (%d chars) opens with `%s:`: %s — %r' % (n, len(subj), R['ticket'], subj.startswith(R['ticket'] + ':'), subj))
    cl = [m.group(0) for rx in (K['closing_rx'], K['closing_rx_broad']) for m in re.finditer(rx, msg)]
    T.info('CLOSE', '#%s closing adjacency in the commit message (both regexes): %s' % (n, cl or 0))
    fk = sorted(set(re.findall(r'KS-\d+', msg)) - set(R['own_keys']))
    T.info('MSGKEYS', '#%s foreign HYPHENATED keys in the commit message: %s' % (n, fk or 0))
    add = [l for l in git(repo, 'diff', RAISE_BASE, h, '--', *code).split('\n') if l.startswith('+') and not l.startswith('+++')]
    ks = {}
    for l in add:
        for k in re.findall(r'KS-\d+', l): ks[k] = ks.get(k, 0) + 1
    T.info('CODEKEYS', '#%s hyphenated keys in ADDED code lines: %s | own key %s count %d' % (n, ks or 0, R['ticket'], ks.get(R['ticket'], 0)))
    return T


def selftest(repo, dev):
    """Each planted arm corrupts ONE pin in a COPY of a row; c1 must FAIL that pin. The real row must pass (positive control)."""
    import copy
    base = ROWS['1431']; arms = []
    def arm(name, mut, want):
        R = copy.deepcopy(base); mut(R); T = Tally()
        print('=== ARM %s (want %s to FAIL)' % (name, want)); pin_row(repo, '1431', dev, R=R, T=T)
        fired = want in T.fails; arms.append((name, fired)); print('ARM %s %s' % (name, 'FIRED' if fired else 'DID NOT FIRE'))
    arm('wrong-tree', lambda R: R.update(end_tree=ROWS['1430']['end_tree']), 'P3')
    arm('dropped-path', lambda R: R['numstat'].pop('Blockchain/Dev/scripts/stack_guard.sh'), 'P4')
    arm('resized-path', lambda R: R['numstat'].__setitem__('Blockchain/Dev/scripts/stack_guard.sh', [19, 1]), 'P4')
    # P7 red: pretend develop is #1431's own head (its advance then touches #1431's code paths)
    R = copy.deepcopy(base); T = Tally(); print('=== ARM develop-touches-code (want P7 to FAIL)')
    pin_row(repo, '1431', base['head_expected'], R=R, T=T); f = 'P7' in T.fails; arms.append(('develop-touches-code', f)); print('ARM develop-touches-code', 'FIRED' if f else 'DID NOT FIRE')
    # P8 red: the row's REAL conflict (both docs) must read as out-of-subset once the allowed set is shrunk to the flow doc alone
    # (the list is mutated IN PLACE, so pin_row sees it; restored right after). A code-path conflict on a SIM develop is c2's arm.
    import lib_gate77 as L
    saved = list(L.DOC_PATHS); L.DOC_PATHS[:] = [saved[0]]
    R = copy.deepcopy(base); T = Tally(); print('=== ARM conflict-outside-subset (doc subset shrunk to the flow doc; want P8 to FAIL)')
    pin_row(repo, '1431', dev, R=R, T=T); f = 'P8' in T.fails; arms.append(('conflict-outside-subset', f)); print('ARM conflict-outside-subset', 'FIRED' if f else 'DID NOT FIRE')
    L.DOC_PATHS[:] = saved
    T = Tally(); print('=== POSITIVE CONTROL: the real row #1431 must pass'); pin_row(repo, '1431', dev, T=T)
    pos = not T.fails and T.n >= 8
    print('SELFTEST arms fired %d/%d | positive control %s' % (sum(f for _, f in arms), len(arms), 'PASS' if pos else 'FAIL'))
    return 0 if all(f for _, f in arms) and pos else 1


def main():
    A = sys.argv; repo = opt(A, '--repo'); dev = opt(A, '--develop')
    if not repo or not dev or not re.fullmatch(r'[0-9a-f]{40}', dev):
        print(__doc__); return 9
    if refuse_absent(repo, [('develop', dev), ('raise_base', RAISE_BASE), ('trailer_control', K['trailer_control']),
                            ('merge_tree_control.ours', K['merge_tree_control']['ours']), ('merge_tree_control.theirs', K['merge_tree_control']['theirs'])]):
        return 2
    if '--selftest' in A: return selftest(repo, dev)
    rows = list(ROWS) if '--all' in A else [opt(A, '--pr')]
    if rows == [None] or any(r not in ROWS for r in rows): print('REFUSED — pass --pr <%s> or --all' % '|'.join(ROWS)); return 9
    if refuse_absent(repo, [('head #' + r, ROWS[r]['head_expected']) for r in rows]): return 2
    T = Tally()
    for r in rows: pin_row(repo, r, dev, T=T)
    return T.end()


if __name__ == '__main__':
    sys.exit(main())
