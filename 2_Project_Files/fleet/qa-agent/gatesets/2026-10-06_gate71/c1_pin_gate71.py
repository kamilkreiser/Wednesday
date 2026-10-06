#!/usr/bin/env python3
"""c1_pin_gate71.py — C1 PIN for ONE ROW (`--pr 1404` KS-1436 T2, or `--pr 1398` KS-1136 T1; WIDENED 2026-10-07). THE HEAD IS A PARAMETER
(--head). Read verbs, plus ONE temp-index tree build in YOUR clone (P4b). Every figure below is the ROW's own (kit.json rows.<pr>).
  P10/P12 WIDENED: a tooling path develop moved is ACCEPTED only BY NAME at the exact blob pair in kit.json develop_tooling_accepted
  (the skill, eaf43dfd -> b59b74a5: section 6e only); any other move of a tooling path still FAILS (re-gate).

  P1  origin refs/pull/1398/head == refs/heads/<branch> == --head   (ls-remote; NOT RUN by name with --no-remote)
  P2  ONE parent == the kit base d75bfe2deb80;  P2b --develop descends from the base; merge-base(head, develop) printed
  P3  base..head == EXACTLY the kit's 4 paths with the kit numstat (+349 -0)
  P4  END_TREE == 2ee602cba3c9;  P4b the tree of base + the 2 CODE blobs (no docs) == the author's ITEM-0 prediction 074705eebd81
      (built with a TEMPORARY index file in YOUR clone; refused inside the forbidden root)
  P5  %(trailers) content 0 bytes; CONTROL bf277eead268 > 0        P6  0 Co-Authored-By; CONTROL carries >= 1
  P7  subject == kit (83 chars, <= 84), no `(#n)` suffix, key first; LANDS len + len(" (#1398)") <= 92 (printed: the author says 90)
  P8  the message: only KS-1136 hyphenated; 0 closing-family words before a key / #n; a `Refs KS-1136` line; no `Closes` line
  P9  modes == kit (09 100755 -> 100755; the test NEW 100644; docs 100644) and `diff --summary` == exactly the one create-mode line
  P10 NO-NEW-LEG: every kit tooling path (runner, hook, run-internal-audit, jobs 01-08, baselines, runner.ts, ci/aggregate.ts,
      orchestrate.sh, the sibling suites, the workflow, the skill) has the SAME blob at base, head and --develop
  P11 0 lock / manifest / baseline / spec / workflow paths in the PR; the only code paths are 09 + the new suite
  P12 base..develop disjoint from the 2 CODE paths and the tooling. A doc path moved on develop is INFO (a docs merge-in: c4 predict)
  --selftest   planted arms on synthetic input: each must FAIL.          rc 0 pass / 1 FAIL / 2 refused by name (an absent object)."""
import os, re, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate71 import K, P, D, Tally, git, wgit, refuse_absent, outside_forbidden, opt, blob_at

CLOSING = re.compile(K['closing_rx'], re.I)
CODE = [p for p in P['numstat'] if not p.startswith('Projects Documents/')]
DOCS = [D['flow'], D['cheat']]


def parse_numstat(text):
    out = {}
    for l in text.strip('\n').split('\n'):
        if l:
            a, d, p = l.split('\t'); out[p] = [int(a), int(d)]
    return out


def numstat_bad(got, want):
    bad = []
    if set(got) != set(want):
        bad.append('paths: extra %s missing %s' % (sorted(set(got) - set(want))[:4], sorted(set(want) - set(got))[:4]))
    bad += ['%s %s != kit %s' % (p, v, want[p]) for p, v in got.items() if p in want and list(v) != list(want[p])]
    return bad


def msg_findings(msg):
    return (sorted(set(re.findall(r'\bKS-\d+\b', msg))), CLOSING.findall(msg), len(re.findall(r'(?im)^co-authored-by:', msg)),
            len(re.findall(r'(?m)^Refs %s\b' % re.escape(P['ticket']), msg)), len(re.findall(r'(?im)^\s*(closes|fixes|resolves)\b', msg)))


def subject_check(subj):
    lands = len(subj) + len(P['squash_suffix'])
    ok = subj == P['subject'] and len(subj) <= P['subject_max_commit'] and subj.startswith(P['ticket'] + ':') \
        and not re.search(r'\(#\d+\)$', subj) and lands <= P['squash_max'] and subj.isascii()
    return ok, lands


def pre_docs_tree(repo, base, head):
    if not outside_forbidden(repo):
        return 'REFUSED (clone inside the forbidden root)'
    fd, idx = tempfile.mkstemp(prefix='g71idx.'); os.close(fd); os.unlink(idx)
    env = {'GIT_INDEX_FILE': idx}
    rc = wgit(repo, 'read-tree', base, env=env)[0]
    for p in CODE:
        mode = git(repo, 'ls-tree', head, '--', p).split()[0]
        blob = git(repo, 'rev-parse', '%s:%s' % (head, p)).strip()
        rc |= wgit(repo, 'update-index', '--add', '--cacheinfo', '%s,%s,%s' % (mode, blob, p), env=env)[0]
    r, o, e = wgit(repo, 'write-tree', env=env)
    try: os.unlink(idx)
    except OSError: pass
    return o.strip() if rc == 0 and r == 0 else 'FAILED rc %d/%d %s' % (rc, r, e.strip()[:120])


def tooling_verdict(blobs, accepted):
    """blobs {path: [base, head, develop]} -> (moved-not-accepted, accepted-by-name). A path is clean when all three are equal and present;
    it is ACCEPTED when base == head == accepted.base and develop == accepted.develop exactly; anything else is MOVED (fails)."""
    moved, acc = [], []
    for p, (b, h, d) in blobs.items():
        if b and b == h == d: continue
        a = accepted.get(p)
        if a and b == h == a['base'] and d == a['develop']: acc.append(p); continue
        moved.append('%s %s' % (p, [x[:12] for x in (b, h, d)]))
    return moved, acc


def run(repo, head, develop, remote):
    t = Tally(); base = P['parents'][0]
    rr = refuse_absent(repo, [('head', head), ('base', base), ('develop', develop), ('trailer control', K['trailer_control'])])
    if rr: return rr
    if remote:
        ls = git(repo, 'ls-remote', K['github_url'], 'refs/pull/%s/head' % P['pr'], 'refs/heads/' + P['branch'])
        refs = dict((l.split('\t')[1], l.split('\t')[0]) for l in ls.strip().split('\n') if '\t' in l)
        a, b = refs.get('refs/pull/%s/head' % P['pr'], 'ABSENT'), refs.get('refs/heads/' + P['branch'], 'ABSENT')
        t.check('P1', a == head and b == head, 'origin pull/head %s branch %s == head %s' % (a[:12], b[:12], head[:12]))
    else:
        t.info('P1', 'NOT RUN by name (--no-remote): the caller read origin itself')
    parents = git(repo, 'log', '-1', '--format=%P', head).split()
    t.check('P2', parents == [base], 'parents %s == [%s]' % ([x[:12] for x in parents], base[:12]))
    anc = git(repo, 'merge-base', '--is-ancestor', base, develop, check=False)[0] == 0
    t.check('P2b', anc, 'develop %s descends from the base %s; merge-base(head, develop) = %s' % (
        develop[:12], base[:12], git(repo, 'merge-base', head, develop).strip()[:12]))
    ns = parse_numstat(git(repo, 'diff', '--numstat', base, head)); bad = numstat_bad(ns, P['numstat'])
    t.check('P3', not bad, '%d paths +%d -%d (kit %d +%d -%d) %s' % (len(ns), sum(v[0] for v in ns.values()), sum(v[1] for v in ns.values()),
            P['file_count'], P['adds_dels'][0], P['adds_dels'][1], bad or 'exact'))
    tree = git(repo, 'rev-parse', head + '^{tree}').strip()
    t.check('P4', tree == P['end_tree'], 'END_TREE %s == kit %s' % (tree[:12], P['end_tree'][:12]))
    pdt = pre_docs_tree(repo, base, head)
    if P['pre_docs_tree']:
        t.check('P4b', pdt == P['pre_docs_tree'], 'base + the 2 code blobs (no docs) = tree %s == author ITEM-0 prediction %s' % (pdt[:40], P['pre_docs_tree'][:12]))
    else:
        t.check('P4b', bool(re.fullmatch(r'[0-9a-f]{40}', pdt)), 'base + the 2 code blobs (no docs) = tree %s (INFO: %s)' % (pdt[:40], P.get('pre_docs_tree_note', 'no author claim')))
    tr = git(repo, 'log', '-1', '--format=%(trailers)', head); ctl = git(repo, 'log', '-1', '--format=%(trailers)', K['trailer_control'])
    t.check('P5', tr.strip() == '' and ctl.strip() != '', 'trailers content %d bytes (raw %d) | CONTROL %s content %d bytes' % (
        len(tr.strip()), len(tr), K['trailer_control'][:12], len(ctl.strip())))
    msg = git(repo, 'log', '-1', '--format=%B', head)
    keys, closing, co, refs, closes_line = msg_findings(msg)
    co_ctl = msg_findings(git(repo, 'log', '-1', '--format=%B', K['trailer_control']))[2]
    t.check('P6', co == 0 and co_ctl >= 1, 'Co-Authored-By in the message %d | CONTROL %s carries %d' % (co, K['trailer_control'][:12], co_ctl))
    subj = msg.split('\n', 1)[0]; ok, lands = subject_check(subj)
    t.check('P7', ok, 'subject %r %d chars (<= %d), LANDS %d with %r (<= %d); == kit %s' % (
        subj, len(subj), P['subject_max_commit'], lands, P['squash_suffix'], P['squash_max'], subj == P['subject']))
    t.check('P8', keys == [P['ticket']] and not closing and refs == 1 and closes_line == 0,
            'hyphenated keys in the message %s (want only %s) | closing refs %s | `Refs %s` lines %d | Closes/Fixes/Resolves lines %d | de-hyphenated %s' % (
                keys, P['ticket'], closing or 'none', P['ticket'], refs, closes_line, sorted(set(re.findall(r'\bKS \d+\b', msg)))))
    modes_bad = []
    for p, (mb, mh) in P['modes'].items():
        gb = (git(repo, 'ls-tree', base, '--', p).split() or [None])[0]
        gh = (git(repo, 'ls-tree', head, '--', p).split() or [None])[0]
        if gb != mb or gh != mh: modes_bad.append('%s base %s head %s (kit %s %s)' % (p.split('/')[-1], gb, gh, mb, mh))
    summ = git(repo, 'diff', '--summary', base, head).strip()
    t.check('P9', not modes_bad and summ == P['summary_expected'], 'modes %s | diff --summary %r' % (modes_bad or '== kit', summ[:160]))
    tb = {p: [blob_at(repo, r, p) for r in (base, head, develop)] for p in P['tooling_paths_unchanged']}
    moved, accepted = tooling_verdict(tb, K.get('develop_tooling_accepted', {}))
    t.check('P10', not moved, 'NO-NEW-LEG: %d tooling paths: %d identical at base / head / develop, %d moved on develop ACCEPTED BY NAME at the exact blob pair %s%s' % (
        len(tb), len(tb) - len(accepted) - len(moved), len(accepted), accepted or '', (' | NOT ACCEPTED (FAIL): %s' % moved[:3]) if moved else ''))
    forb = [p for p in ns if re.search(r'(package(-lock)?\.json|audit-baseline\.json|\.ya?ml|openapi|/baselines/)', p)]
    code = sorted(p for p in ns if not p.startswith('Projects Documents/'))
    t.check('P11', not forb and code == sorted(CODE), 'forbidden-class paths %s | code paths %s' % (forb or 0, [c.split('/')[-1] for c in code]))
    adv = [l for l in git(repo, 'diff', '--name-only', base, develop).split('\n') if l]
    acc = set(p for p in accepted)
    hit = sorted((set(adv) & (set(CODE) | set(P['tooling_paths_unchanged']))) - acc)
    if acc & set(adv): t.info('P12a', 'base..develop moved %s: ACCEPTED BY NAME (kit develop_tooling_accepted; P10 asserted the exact blob pair)' % sorted(acc & set(adv)))
    dochit = sorted(set(adv) & set(DOCS))
    t.check('P12', not hit, 'base..develop: %d path(s); %d shared with the CODE paths / tooling %s' % (len(adv), len(hit), hit[:5]))
    if dochit: t.info('P12d', 'develop moved %d doc path(s) since the base: a DOCS MERGE-IN is required — run c4 predict + mergetree' % len(dochit))
    else: t.info('P12d', 'develop touched 0 doc paths since the base (%s): the squash applies the head tree exactly' % ('UNMOVED' if develop == base else 'moved'))
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    want = P['numstat']
    rep(not numstat_bad(dict(want), want), 'numstat: the exact kit set passes')
    rep(numstat_bad(dict(want, **{'x/package-lock.json': [1, 1]}), want), 'PLANTED extra lock path FAILS')
    rep(numstat_bad(dict(want, **{CODE[1]: [want[CODE[1]][0] + 1, want[CODE[1]][1]]}), want), 'PLANTED %s one extra line FAILS' % CODE[1].split('/')[-1])
    rep(numstat_bad({k: v for k, v in want.items() if 'Cheat' not in k}, want), 'PLANTED missing cheat FAILS')
    tk = P['ticket']
    k, c, co, r, cl = msg_findings('%s: x\n\nRefs %s\n\nKS 878 guarded 04.\n' % (tk, tk))
    rep(k == [tk] and not c and co == 0 and r == 1 and cl == 0, 'message: de-hyphenated KS 878 is not a key; one `Refs %s` line' % tk)
    k, c, co, r, cl = msg_findings('%s: x\n\nCloses %s\nFixes KS-878.\nCo-Authored-By: X <x@y>\n' % (tk, tk))
    rep(k == sorted([tk, 'KS-878']) and c and co == 1 and r == 0 and cl == 2, 'PLANTED `Closes %s` + `Fixes KS-878` + trailer: all FIRE' % tk)
    want_lands = P['subject_len'] + len(P['squash_suffix'])
    rep(subject_check(P['subject']) == (True, want_lands), 'subject (#%s): the kit subject passes and LANDS %d (%d + %d)' % (P['pr'], want_lands, P['subject_len'], len(P['squash_suffix'])))
    rep(not subject_check(P['subject'] + P['squash_suffix'])[0], 'PLANTED `%s` suffix FAILS' % P['squash_suffix'].strip())
    rep(not subject_check(P['subject'] + ' and more words here' + 'x' * 10)[0], 'PLANTED over-long subject FAILS')
    acc = {'S': {'base': 'a' * 40, 'develop': 'b' * 40}}
    rep(tooling_verdict({'S': ['a' * 40, 'a' * 40, 'b' * 40]}, acc) == ([], ['S']), 'tooling: a develop move at the EXACT accepted blob pair is ACCEPTED BY NAME')
    rep(tooling_verdict({'S': ['a' * 40, 'a' * 40, 'c' * 40]}, acc)[0], 'PLANTED develop blob other than the accepted one FAILS (re-gate)')
    rep(tooling_verdict({'T': ['a' * 40, 'a' * 40, 'b' * 40]}, acc)[0], 'PLANTED move of a tooling path NOT in the accepted list FAILS')
    rep(tooling_verdict({'S': ['a' * 40, 'c' * 40, 'b' * 40]}, acc)[0], 'PLANTED head that changed the accepted path FAILS (the PR may not touch it)')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not opt(A, '--repo'): print(__doc__); return 2
    head = opt(A, '--head', P['head_expected']); develop = opt(A, '--develop', K['develop_at_draft'])
    print('C1 row #%s (%s, %s) head %s develop %s repo %s' % (P['pr'], P['ticket'], P['tier'], head, develop, opt(A, '--repo')))
    return run(opt(A, '--repo'), head, develop, '--no-remote' not in A)


if __name__ == '__main__':
    sys.exit(main())
