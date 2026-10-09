#!/usr/bin/env python3
"""c1_pin_gate79.py — C1 PIN for #1437 (KS-1402). Read verbs only. Carried from c1_pin_gate78.py; [g79] marks this kit's changes
(8 code / test / spec / doc paths, one ADD; no lock, no sibling ticket; auth untouched; the known docs + yaml overlap with develop).

EVERY PIN IS A REQUIRED ARGUMENT (no default; a wrong value FAILS its check — the wrong-value arms are in --selftest and KIT_REPORT):
  --repo R --head H --base B --develop D --end-tree T --parents-n N   [--no-remote]

  P1  origin refs/pull/<n>/head == refs/heads/<branch> == --head   (ls-remote; NOT RUN by name with --no-remote)
  P2  head is a commit | EXACTLY --parents-n parents | first parent == --base   (three facts, three reasons)
  P2b develop descends from --base; merge-base(head, develop) printed
  P3  base..head paths == EXACTLY the kit's 8 with the kit numstat (+852 -289)
  P4  END_TREE == --end-tree (and kit end_tree printed beside it)
  P5  %(trailers) CONTENT 0 bytes on the head; CONTROL bf277eead268 prints > 0
  P6  0 Co-Authored-By in the message; CONTROL carries >= 1
  P7  [g79] subject == kit subject, len <= 92 AS DECLARED (STANDING_LINES 2026-10-07: the merge tools append nothing; NO `(#n)`
      arithmetic), and the subject carries no `(#`
  P8  only KS-1402 hyphenated in the message; closing-family words counted INCLUDING the conventional-commit form `fix(KS-n)` —
      [g79] a hit is printed as P8-FIXPREFIX INFO for the gate to rule (Q-FIXPREFIX), never silently passed or failed
  P9  [g79] modes 100644; diff --summary == exactly one `create mode 100644` for the kit's added test file, nothing else
  P10 NO-NEW-LEG: every kit tooling / code-surface path (hooks, preflight, manifests, locks, originate index/db/rbac/jest/tsconfig/
      Dockerfile, the shared mock helper, AUTH's users.ts + userRepo.ts, shared encryptedField + tenant-context + index, 3 workflows,
      the skill, CLAUDE.md) PRESENT with the SAME (mode, blob) at base, head and develop
  P11 [g79] AUTH UNCHANGED: 0 paths under services/auth/ in base..head; 0 package.json / package-lock.json paths
  P12 [g79] base..develop ∩ the PR's paths ⊆ kit known_develop_overlap (the 2 docs + the yaml: the MERGE SEAT's keep-both / regen,
      Q-DOCSMERGE) — printed by name; any OTHER PR path or any tooling path in base..develop FAILS
  --selftest   planted arms (incl. the wrong-value arms for every required pin): each must FAIL.
rc 0 all pass / 1 a FAIL / 2 refused (missing argument, unresolvable sha)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate79 import K, Tally, git, resolvable, blob, req

P = K['pr']
CLOSING = re.compile(K['closing_rx'], re.I)
FIXPREFIX = re.compile(r'\b(fix|close|resolve|complete)[a-z]*\(\s*KS-\d+\s*\)', re.I)


def numstat_ok(got, want):
    bad = []
    if set(got) != set(want):
        bad.append('paths: extra %s missing %s' % (sorted(set(got) - set(want))[:5], sorted(set(want) - set(got))[:5]))
    for p, v in got.items():
        if p in want and list(v) != list(want[p]):
            bad.append('%s %s != kit %s' % (p, v, want[p]))
    return bad


def msg_findings(msg):
    keys = sorted(set(re.findall(r'\bKS-\d+\b', msg)))
    return keys, CLOSING.findall(msg), len(re.findall(r'(?im)^co-authored-by:', msg)), FIXPREFIX.findall(msg)


def parse_numstat(text):
    out = {}
    for l in text.strip('\n').split('\n'):
        if l:
            a, d, p = l.split('\t'); out[p] = [int(a), int(d)]
    return out


def parents_ok(parents, n, base):
    why = []
    if len(parents) != n: why.append('parent count %d != %d' % (len(parents), n))
    if not parents or parents[0] != base: why.append('first parent %s != base %s' % ((parents or ['NONE'])[0][:12], base[:12]))
    return why


def tooling_moved(readings):
    return ['%s %s' % (p, [x[-12:] if x else 'ABSENT' for x in r]) for p, r in readings.items() if not (r[0] and r[0] == r[1] == r[2])]


def summary_ok(summ, added):
    want = sorted(' create mode 100644 %s' % p for p in added)
    got = sorted(l for l in summ.split('\n') if l.strip())
    return got == want, got


def overlap(adv, pr_paths, tooling, known):
    shared = sorted(set(adv) & set(pr_paths)); tool = sorted(set(adv) & set(tooling))
    return shared, [p for p in shared if p not in known], tool


def run(repo, head, base, develop, end_tree, n_par, remote):
    t = Tally()
    for s, n in ((head, 'head'), (base, 'base'), (develop, 'develop'), (K['trailer_control'], 'trailer control')):
        if not resolvable(repo, s):
            print('REFUSED: %s %s is not in %s (fetch it BY SHA into YOUR clone)' % (n, s, repo)); return 2
    if remote:
        ls = git(repo, 'ls-remote', K['github_url'], 'refs/pull/%s/head' % P['pr'], 'refs/heads/' + P['branch'])
        refs = dict((l.split('\t')[1], l.split('\t')[0]) for l in ls.strip().split('\n') if '\t' in l)
        a, b = refs.get('refs/pull/%s/head' % P['pr'], 'ABSENT'), refs.get('refs/heads/' + P['branch'], 'ABSENT')
        t.check('P1', a == head and b == head, 'origin pull/head %s branch %s == head %s' % (a[:12], b[:12], head[:12]))
    else:
        t.info('P1', 'NOT RUN by name (--no-remote): the caller read origin itself')
    typ = git(repo, 'cat-file', '-t', head).strip()
    parents = git(repo, 'log', '-1', '--format=%P', head).split()
    why = parents_ok(parents, n_par, base)
    t.check('P2', typ == 'commit' and not why, 'type %s | %d parent(s) (want %d) | first %s (want %s) %s' % (
        typ, len(parents), n_par, (parents or ['NONE'])[0][:12], base[:12], why or ''))
    mb = git(repo, 'merge-base', head, develop).strip()
    anc = git(repo, 'merge-base', '--is-ancestor', base, develop, check=False)[0] == 0
    t.check('P2b', anc, 'develop %s descends from the base %s; merge-base(head, develop) = %s' % (develop[:12], base[:12], mb[:12]))
    ns = parse_numstat(git(repo, 'diff', '--numstat', base, head))
    bad = numstat_ok(ns, P['numstat'])
    t.check('P3', not bad, '%d paths, +%d -%d (kit %d paths +%d -%d) %s' % (len(ns), sum(v[0] for v in ns.values()), sum(v[1] for v in ns.values()),
            P['file_count'], P['adds_dels'][0], P['adds_dels'][1], bad[:4] or 'exact'))
    tree = git(repo, 'rev-parse', head + '^{tree}').strip()
    t.check('P4', tree == end_tree, 'END_TREE %s == --end-tree %s (kit %s: %s)' % (tree[:12], end_tree[:12], P['end_tree'][:12], tree == P['end_tree']))
    tr = git(repo, 'log', '-1', '--format=%(trailers)', head)
    ctl = git(repo, 'log', '-1', '--format=%(trailers)', K['trailer_control'])
    t.check('P5', tr.strip() == '' and ctl.strip() != '', 'trailers content %d bytes (raw %d) | CONTROL %s content %d bytes' % (
        len(tr.strip()), len(tr), K['trailer_control'], len(ctl.strip())))
    msg = git(repo, 'log', '-1', '--format=%B', head)
    keys, closing, co, fixp = msg_findings(msg)
    co_ctl = msg_findings(git(repo, 'log', '-1', '--format=%B', K['trailer_control']))[2]
    t.check('P6', co == 0 and co_ctl >= 1, 'Co-Authored-By in the message %d | CONTROL %s carries %d' % (co, K['trailer_control'], co_ctl))
    subj = msg.split('\n', 1)[0]
    t.check('P7', subj == P['subject'] and len(subj) <= P['subject_max'] and '(#' not in subj,
            'subject %r %d chars (<= %d AS DECLARED; no (#n) arithmetic), == kit %s, carries "(#": %s' % (subj, len(subj), P['subject_max'], subj == P['subject'], '(#' in subj))
    t.check('P8', keys == [P['ticket']], 'hyphenated keys in the message %s (want only %s) | de-hyphenated mentions %d | Refs lines %d' % (
        keys, P['ticket'], len(re.findall(r'\bKS \d+\b', msg)), len(re.findall(r'(?m)^Refs %s\s*$' % P['ticket'], msg))))
    t.info('P8-FIXPREFIX', 'closing-family matches (incl. the conventional `fix(KS-n)` form): %s | FOR THE GATE TO RULE (Q-FIXPREFIX): '
           'the kit does NOT know whether Linear treats `fix(KS-1402):` as a closing magic word' % (closing or fixp or 'none'))
    modes = []
    for rev in (base, head):
        out = git(repo, 'ls-tree', '-r', rev, '--', *sorted(ns)).strip()
        for l in out.split('\n'):
            if l: modes.append(l.split()[0])
    summ = git(repo, 'diff', '--summary', base, head)
    sok, sgot = summary_ok(summ, P['added_paths'])
    t.check('P9', set(modes) == {'100644'} and len(modes) == 2 * len(ns) - len(P['added_paths']) and sok,
            'modes %s over %d blob readings (want 100644 x %d) | diff --summary %s' % (sorted(set(modes)), len(modes), 2 * len(ns) - len(P['added_paths']), sgot))
    readings = dict((p, tuple(blob(repo, r, p) for r in (base, head, develop))) for p in K['tooling_paths_unchanged'])
    moved = tooling_moved(readings)
    t.check('P10', not moved, 'NO-NEW-LEG: %d tooling / code-surface paths present and identical at base / head / develop %s' % (len(readings), moved[:4] or ''))
    auth = [p for p in ns if p.startswith(K['auth_prefix'])]
    man = [p for p in ns if p.endswith('package.json') or p.endswith('package-lock.json')]
    t.check('P11', not auth and not man, 'AUTH paths changed %s | manifests / locks changed %s' % (auth or 0, man or 0))
    adv = [l for l in git(repo, 'diff', '--name-only', base, develop).split('\n') if l]
    shared, unknown, tool = overlap(adv, ns, K['tooling_paths_unchanged'], K['known_develop_overlap'])
    t.check('P12', not unknown and not tool, 'base..develop: %d path(s); shared with the PR %d %s (known docs/yaml overlap = the MERGE SEAT\'s '
            'keep-both, Q-DOCSMERGE); UNKNOWN overlap %s; tooling %s' % (len(adv), len(shared), shared, unknown or 0, tool or 0))
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    want = dict((p, list(v)) for p, v in P['numstat'].items())
    rep(not numstat_ok(dict(want), want), 'numstat: the exact 8-path set passes')
    rep(numstat_ok(dict(want, **{K['auth_prefix'] + 'src/routes/users.ts': [1, 0]}), want), 'PLANTED auth path in the diff FAILS')
    w2 = dict(want); w2[K['route_file']] = [125, 102]
    rep(numstat_ok(w2, want), 'PLANTED documents.ts +125 (kit +124) FAILS')
    w3 = dict(want); w3.pop(K['test_files']['ks697'])
    rep(numstat_ok(w3, want), 'PLANTED missing ks697 path FAILS')
    b = 'b' * 40
    rep(not parents_ok([b], 1, b), 'parents: one parent == base passes')
    rep(parents_ok([b, 'c' * 40], 1, b), 'PLANTED merge commit (2 parents, first == base) FAILS on the count')
    rep(parents_ok(['c' * 40], 1, b), 'WRONG-VALUE ARM --base FAILS the first-parent check')
    rep(parents_ok([b], 2, b), 'WRONG-VALUE ARM --parents-n 2 FAILS')
    rep(not tooling_moved({'x': ('100644 a', '100644 a', '100644 a')}), 'tooling: identical present blobs pass')
    rep(tooling_moved({'x': ('', '', '')}), 'PLANTED absent-everywhere tooling path FAILS (absent is a state)')
    rep(tooling_moved({'x': ('100644 a', '100644 b', '100644 b')}), 'PLANTED auth users.ts moved at head FAILS')
    ok, _ = summary_ok(' create mode 100644 %s\n' % P['added_paths'][0], P['added_paths']); rep(ok, 'summary: the one declared ADD passes')
    ok, _ = summary_ok(' create mode 100644 %s\n delete mode 100644 x.ts\n' % P['added_paths'][0], P['added_paths']); rep(not ok, 'PLANTED extra delete in --summary FAILS')
    ok, _ = summary_ok(' create mode 100755 %s\n' % P['added_paths'][0], P['added_paths']); rep(not ok, 'PLANTED 100755 on the added file FAILS')
    k, c, co, fx = msg_findings('fix(KS-1402): x\n\nRefs KS-1402\nthe KS 739 file; KS 697.\n')
    rep(k == ['KS-1402'] and co == 0 and fx, 'message: de-hyphenated keys are not keys; the `fix(KS-1402)` form IS counted (P8-FIXPREFIX)')
    k, c, co, fx = msg_findings('x\n\nFixes KS-739.\nCo-Authored-By: X <x@y>\n')
    rep(k == ['KS-739'] and c and co == 1, 'PLANTED `Fixes KS-739` + Co-Authored-By: foreign key, closing word and trailer all FIRE')
    sh, unk, tool = overlap(K['known_develop_overlap'][:2], P['numstat'], K['tooling_paths_unchanged'], K['known_develop_overlap'])
    rep(sh and not unk and not tool, 'P12: develop touching only the two known docs passes (named, not hidden)')
    sh, unk, tool = overlap([K['route_file']], P['numstat'], K['tooling_paths_unchanged'], K['known_develop_overlap'])
    rep(unk == [K['route_file']], 'PLANTED develop touching documents.ts FAILS P12 (UNKNOWN overlap)')
    sh, unk, tool = overlap(['Blockchain/Dev/services/auth/src/routes/users.ts'], P['numstat'], K['tooling_paths_unchanged'], K['known_develop_overlap'])
    rep(tool, 'PLANTED develop touching auth users.ts FAILS P12 (tooling)')
    for a in (['--repo', 'x'], ['--repo', 'x', '--head', 'abc']):
        try:
            req(a, '--head', hex40=True); rep(False, 'required --head missing/short was ACCEPTED')
        except SystemExit:
            rep(True, 'REQUIRED-ARG ARM %s -> refused' % a)
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A: print(__doc__); return 2
    try:
        repo = req(A, '--repo'); head = req(A, '--head', True); base = req(A, '--base', True); develop = req(A, '--develop', True)
        end_tree = req(A, '--end-tree', True); n_par = int(req(A, '--parents-n'))
    except SystemExit as e:
        print(e); return 2
    print('C1 #%s head %s base %s develop %s end-tree %s parents-n %d repo %s' % (P['pr'], head, base, develop, end_tree, n_par, repo))
    return run(repo, head, base, develop, end_tree, n_par, '--no-remote' not in A)


if __name__ == '__main__':
    sys.exit(main())
