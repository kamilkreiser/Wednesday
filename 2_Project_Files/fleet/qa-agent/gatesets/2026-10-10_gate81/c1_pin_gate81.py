#!/usr/bin/env python3
"""c1_pin_gate81.py — C1 PIN per PR for gate81 (#1443 KS-1346, #1444 KS-937, #1445 + #1446 KS-1410). Read verbs only. Carried from
c1_pin_gate80.py; [g81] marks this kit's changes (FOUR PRs selected by --pr; per-path MODES from the kit because #1444 edits two 100755 files;
`set` replaces `pair` and censuses all four: the docs are shared by all, audit-export.ts by exactly #1443 and #1446).

EVERY PIN IS A REQUIRED ARGUMENT (no default; a wrong value FAILS its check — the wrong-value arms are in --selftest and KIT_REPORT):
  --repo R --pr N --head H --base B --develop D --end-tree T --parents-n N   [--no-remote]
  c1_pin_gate81.py set --repo R --head1443 H --head1444 H --head1445 H --head1446 H --base B --develop D      (P13, the four-PR path census)

  P1  origin refs/pull/<n>/head == refs/heads/<branch> == --head   (ls-remote; NOT RUN by name with --no-remote)
  P2  head is a commit | EXACTLY --parents-n parents | first parent == --base   (three facts, three reasons)
  P2b develop descends from --base; merge-base(head, develop) printed
  P3  base..head paths == EXACTLY the kit's paths with the kit numstat
  P4  END_TREE == --end-tree (and kit end_tree printed beside it)
  P5  %(trailers) CONTENT 0 bytes on the head; CONTROL bf277eead268 prints > 0
  P6  0 Co-Authored-By in the message; CONTROL carries >= 1
  P7  subject == kit subject, len <= 92 AS DECLARED (no `(#n)` arithmetic), no `(#`; the subject carries the PR's own key
  P8  only the PR's OWN key hyphenated in the message; closing-family words counted (incl. the `fix(KS-n)` form, INFO)
  P9  PER-PATH modes at base and head == the kit's (1444: the script and its suite are 100755 at BOTH; everything else 100644);
      diff --summary == exactly the kit's `create mode 100644` list (1443/1445/1446: the new test; 1444: none)
  P10 NO-NEW-LEG: every kit tooling / code-surface path (minus the PR's own paths) PRESENT with the SAME (mode, blob) at base, head, develop
  P11 0 package.json / package-lock.json paths in base..head (locks and manifests)
  P12 base..develop intersected with the PR's paths is a subset of the known docs overlap — printed by name; any OTHER PR path or tooling path FAILS
  P13 (set) over the four PRs: every doc path is shared by all four; a NON-doc path shared by two PRs must be EXACTLY a kit `known_code_overlap` entry
      (audit-export.ts: #1443 and #1446) and nothing else; all four parents == base
rc 0 all pass / 1 a FAIL / 2 refused (missing argument, unresolvable sha)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate81 import K, PR, Tally, git, resolvable, blob, req, opt

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


def modes_ok(got, want):
    return sorted((p, m) for p, m in got.items() if want.get(p) != m)


def summary_ok(summ, added):
    want = sorted(' create mode 100644 %s' % p for p in added)
    got = sorted(l for l in summ.split('\n') if l.strip())
    return got == want, got


def overlap(adv, pr_paths, tooling, known):
    shared = sorted(set(adv) & set(pr_paths)); tool = sorted(set(adv) & set(tooling))
    return shared, [p for p in shared if p not in known], tool


def set_ok(path_sets, docs, known_code):
    """path_sets: {pr: [paths]}. Every doc path in every PR; a non-doc path in 2+ PRs must be exactly a known_code_overlap entry."""
    why = []; docs = set(docs)
    for n, ps in path_sets.items():
        if not docs <= set(ps): why.append('#%s lacks doc %s' % (n, sorted(docs - set(ps))))
    owners = {}
    for n, ps in path_sets.items():
        for x in ps:
            if x not in docs: owners.setdefault(x, []).append(n)
    shared = dict((x, sorted(v)) for x, v in owners.items() if len(v) > 1)
    want = dict((x, sorted(v)) for x, v in known_code.items())
    if shared != want: why.append('non-doc shared paths %s != the kit known_code_overlap %s' % (shared, want))
    return why, shared


def run(repo, p, head, base, develop, end_tree, n_par, remote):
    t = Tally()
    for s, n in ((head, 'head'), (base, 'base'), (develop, 'develop'), (K['trailer_control'], 'trailer control')):
        if not resolvable(repo, s):
            print('REFUSED: %s %s is not in %s (fetch it BY SHA into YOUR clone)' % (n, s, repo)); return 2
    if remote:
        ls = git(repo, 'ls-remote', K['github_url'], 'refs/pull/%s/head' % p['pr'], 'refs/heads/' + p['branch'])
        refs = dict((l.split('\t')[1], l.split('\t')[0]) for l in ls.strip().split('\n') if '\t' in l)
        a, b = refs.get('refs/pull/%s/head' % p['pr'], 'ABSENT'), refs.get('refs/heads/' + p['branch'], 'ABSENT')
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
    bad = numstat_ok(ns, p['numstat'])
    t.check('P3', not bad, '%d paths, +%d -%d (kit %d paths +%d -%d) %s' % (len(ns), sum(v[0] for v in ns.values()), sum(v[1] for v in ns.values()),
            p['file_count'], p['adds_dels'][0], p['adds_dels'][1], bad[:4] or 'exact'))
    tree = git(repo, 'rev-parse', head + '^{tree}').strip()
    t.check('P4', tree == end_tree, 'END_TREE %s == --end-tree %s (kit %s: %s)' % (tree[:12], end_tree[:12], p['end_tree'][:12], tree == p['end_tree']))
    tr = git(repo, 'log', '-1', '--format=%(trailers)', head)
    ctl = git(repo, 'log', '-1', '--format=%(trailers)', K['trailer_control'])
    t.check('P5', tr.strip() == '' and ctl.strip() != '', 'trailers content %d bytes (raw %d) | CONTROL %s content %d bytes' % (
        len(tr.strip()), len(tr), K['trailer_control'], len(ctl.strip())))
    msg = git(repo, 'log', '-1', '--format=%B', head)
    keys, closing, co, fixp = msg_findings(msg)
    co_ctl = msg_findings(git(repo, 'log', '-1', '--format=%B', K['trailer_control']))[2]
    t.check('P6', co == 0 and co_ctl >= 1, 'Co-Authored-By in the message %d | CONTROL %s carries %d' % (co, K['trailer_control'], co_ctl))
    subj = msg.split('\n', 1)[0]
    t.check('P7', subj == p['subject'] and len(subj) <= p['subject_max'] and '(#' not in subj and subj.startswith(p['ticket'] + ':'),
            'subject %r %d chars (<= %d AS DECLARED; no (#n) arithmetic), == kit %s, carries "(#": %s, starts with own key: %s' % (
                subj, len(subj), p['subject_max'], subj == p['subject'], '(#' in subj, subj.startswith(p['ticket'] + ':')))
    t.check('P8', keys == [p['ticket']], 'hyphenated keys in the message %s (want only %s) | de-hyphenated mentions %d | Refs lines %d' % (
        keys, p['ticket'], len(re.findall(r'\bKS \d+\b', msg)), len(re.findall(r'(?m)^Refs %s\s*$' % p['ticket'], msg))))
    t.info('P8-CLOSING', 'closing-family matches (incl. the conventional `fix(KS-n)` form): %s' % (closing or fixp or 'none'))
    got_h, got_b = {}, {}
    for rev, dst in ((head, got_h), (base, got_b)):
        out = git(repo, 'ls-tree', '-r', rev, '--', *sorted(ns)).strip()
        for l in out.split('\n'):
            if l:
                meta, path = l.split('\t'); dst[path] = meta.split()[0]
    summ = git(repo, 'diff', '--summary', base, head)
    sok, sgot = summary_ok(summ, p['added_paths'])
    bad_h, bad_b = modes_ok(got_h, p['modes']), modes_ok(got_b, p['modes_base'])
    t.check('P9', not bad_h and not bad_b and len(got_h) == len(ns) and len(got_b) == len(ns) - len(p['added_paths']) and sok,
            'per-path modes at head %s (wrong vs kit: %s) | at base %s (wrong: %s) over %d + %d blob readings | diff --summary %s (want %d create-mode line(s))' % (
                sorted(set(got_h.values())), bad_h or 'none', sorted(set(got_b.values())), bad_b or 'none', len(got_h), len(got_b), sgot, len(p['added_paths'])))
    tooling = [x for x in K['tooling_paths_unchanged'] if x not in ns]
    readings = dict((x, tuple(blob(repo, r, x) for r in (base, head, develop))) for x in tooling)
    moved = tooling_moved(readings)
    t.check('P10', not moved, 'NO-NEW-LEG: %d tooling / code-surface paths present and identical at base / head / develop %s' % (len(readings), moved[:4] or ''))
    man = [x for x in ns if x.endswith('package.json') or x.endswith('package-lock.json')]
    t.check('P11', not man, 'manifests / locks changed %s' % (man or 0))
    adv = [l for l in git(repo, 'diff', '--name-only', base, develop).split('\n') if l]
    shared, unknown, tool = overlap(adv, ns, K['tooling_paths_unchanged'], K['known_develop_overlap'])
    t.check('P12', not unknown and not tool, 'base..develop: %d path(s); shared with the PR %d %s (known docs overlap = the MERGE SEAT\'s keep-both); '
            'UNKNOWN overlap %s; tooling %s' % (len(adv), len(shared), shared, unknown or 0, tool or 0))
    return t.end()


def run_set(repo, heads, base, develop):
    t = Tally(); order = list(K['go_prs'])
    for n in order:
        if not resolvable(repo, heads[n]): print('REFUSED: head%s %s is not in %s' % (n, heads[n], repo)); return 2
    for s_, n in ((base, 'base'), (develop, 'develop')):
        if not resolvable(repo, s_): print('REFUSED: %s %s is not in %s' % (n, s_, repo)); return 2
    sets = dict((n, sorted(parse_numstat(git(repo, 'diff', '--numstat', base, heads[n])))) for n in order)
    why, shared = set_ok(sets, K['known_develop_overlap'], K['known_code_overlap'])
    t.check('P13', not why, '%s; the docs are shared by all %d; shared NON-doc paths %s (kit known_code_overlap %s) %s' % (
        ', '.join('#%s %d paths' % (n, len(sets[n])) for n in order), len(order), shared, K['known_code_overlap'], why or 'OK'))
    par = dict((n, git(repo, 'log', '-1', '--format=%P', heads[n]).split()) for n in order)
    t.check('P13b', all(x == [base] for x in par.values()), 'all four heads have the single parent %s: %s' % (base[:12], dict((n, [y[:12] for y in v]) for n, v in par.items())))
    trees = dict((n, git(repo, 'rev-parse', heads[n] + '^{tree}').strip()) for n in order)
    t.check('P13d', len(set(trees.values())) == 4 and len(set(heads.values())) == 4, 'four distinct heads and four distinct trees: %s' % dict((n, v[:12]) for n, v in trees.items()))
    bd = [x for x in git(repo, 'diff', '--name-only', base, develop).split('\n') if x]
    t.check('P13c', True, 'base..develop touches %d path(s): %s' % (len(bd), bd[:6]))
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    for n in K['go_prs']:
        p = PR(n); want = dict((x, list(v)) for x, v in p['numstat'].items())
        rep(not numstat_ok(dict(want), want), '#%s numstat: the exact %d-path set passes' % (n, len(want)))
        w2 = dict(want); w2[p['code_paths'][0]] = [want[p['code_paths'][0]][0] + 1, 0]
        rep(numstat_ok(w2, want), '#%s PLANTED +1 on %s FAILS' % (n, p['code_paths'][0].split('/')[-1]))
        w3 = dict(want); w3.pop(p['code_paths'][-1])
        rep(numstat_ok(w3, want), '#%s PLANTED missing path FAILS' % n)
        w4 = dict(want, **{'systemTest/akto/package.json': [1, 0]})
        rep(numstat_ok(w4, want), '#%s PLANTED manifest path in the diff FAILS' % n)
        rep(not modes_ok(p['modes'], p['modes']), '#%s modes: the kit modes pass' % n)
        m2 = dict(p['modes']); m2[p['code_paths'][0]] = '100755' if m2[p['code_paths'][0]] == '100644' else '100644'
        rep(modes_ok(m2, p['modes']), '#%s PLANTED mode flip on %s FAILS' % (n, p['code_paths'][0].split('/')[-1]))
    b = 'b' * 40
    rep(not parents_ok([b], 1, b), 'parents: one parent == base passes')
    rep(parents_ok([b, 'c' * 40], 1, b), 'PLANTED merge commit (2 parents, first == base) FAILS on the count')
    rep(parents_ok(['c' * 40], 1, b), 'WRONG-VALUE ARM --base FAILS the first-parent check')
    rep(parents_ok([b], 2, b), 'WRONG-VALUE ARM --parents-n 2 FAILS')
    rep(not tooling_moved({'x': ('100644 a', '100644 a', '100644 a')}), 'tooling: identical present blobs pass')
    rep(tooling_moved({'x': ('', '', '')}), 'PLANTED absent-everywhere tooling path FAILS (absent is a state)')
    rep(tooling_moved({'x': ('100644 a', '100644 b', '100644 b')}), 'PLANTED tooling path moved at head FAILS')
    ok, _ = summary_ok('', []); rep(ok, '#1444 summary: NO create mode passes')
    ok, _ = summary_ok(' create mode 100644 x.ts\n', []); rep(not ok, 'PLANTED create mode on #1444 (which declares none) FAILS')
    s = PR(1446)['added_paths']
    ok, _ = summary_ok(' create mode 100644 %s\n' % s[0], s); rep(ok, '#1446 summary: the one declared ADD passes')
    ok, _ = summary_ok(' create mode 100755 %s\n' % s[0], s); rep(not ok, 'PLANTED 100755 on the new test FAILS')
    ok, _ = summary_ok(' create mode 100644 %s\n delete mode 100644 x.ts\n' % s[0], s); rep(not ok, 'PLANTED extra delete in --summary FAILS')
    k, c, co, fx = msg_findings('KS-937: x\n\nRefs KS-937\nthe KS 739 file; KS 697.\n')
    rep(k == ['KS-937'] and co == 0 and not fx, 'message: de-hyphenated keys are not keys')
    k, c, co, fx = msg_findings('x\n\nFixes KS-739.\nCo-Authored-By: X <x@y>\n')
    rep(k == ['KS-739'] and c and co == 1, 'PLANTED `Fixes KS-739` + Co-Authored-By: foreign key, closing word and trailer all FIRE')
    sh, unk, tool = overlap(K['known_develop_overlap'], PR(1443)['numstat'], K['tooling_paths_unchanged'], K['known_develop_overlap'])
    rep(sh and not unk and not tool, 'P12: develop touching only the two known docs passes (named, not hidden)')
    for n, path in (('1443', PR(1443)['route_files'][2]), ('1446', PR(1446)['route_files'][0]), ('1445', PR(1445)['route_files'][0]), ('1444', PR(1444)['gate_script'])):
        sh, unk, tool = overlap([path], PR(n)['numstat'], K['tooling_paths_unchanged'], K['known_develop_overlap'])
        rep(unk == [path], 'PLANTED develop touching %s FAILS P12 for #%s (UNKNOWN overlap)' % (path.split('/')[-1], n))
    sh, unk, tool = overlap(['Blockchain/Dev/scripts/run-shell-suites.sh'], PR(1444)['numstat'], K['tooling_paths_unchanged'], K['known_develop_overlap'])
    rep(tool, 'PLANTED develop touching run-shell-suites.sh FAILS P12 (tooling)')
    real = dict((n, list(PR(n)['numstat'])) for n in K['go_prs'])
    why, shared = set_ok(real, K['known_develop_overlap'], K['known_code_overlap'])
    rep(not why and list(shared) == list(K['known_code_overlap']), 'P13: the real four share the two docs, and audit-export.ts is shared by exactly #1443 + #1446: %s' % shared)
    pl = dict(real); pl['1445'] = real['1445'] + [PR(1444)['gate_script']]
    rep(set_ok(pl, K['known_develop_overlap'], K['known_code_overlap'])[0], 'PLANTED #1445 touching #1444\'s gate script FAILS P13 (an unlisted shared code path)')
    pl = dict(real); pl['1444'] = [x for x in real['1444'] if x not in K['known_develop_overlap']]
    rep(set_ok(pl, K['known_develop_overlap'], K['known_code_overlap'])[0], 'PLANTED #1444 without the docs FAILS P13')
    pl = dict(real); pl['1446'] = [x for x in real['1446'] if x not in K['known_code_overlap']]
    rep(set_ok(pl, K['known_develop_overlap'], K['known_code_overlap'])[0], 'PLANTED #1446 NOT touching audit-export.ts FAILS P13 (the declared overlap vanished)')
    pl = dict(real); pl['1445'] = real['1445'] + list(K['known_code_overlap'])
    rep(set_ok(pl, K['known_develop_overlap'], K['known_code_overlap'])[0], 'PLANTED a THIRD PR (#1445) on audit-export.ts FAILS P13')
    for a in (['--repo', 'x'], ['--repo', 'x', '--head', 'abc']):
        try:
            req(a, '--head', hex40=True); rep(False, 'required --head missing/short was ACCEPTED')
        except SystemExit:
            rep(True, 'REQUIRED-ARG ARM %s -> refused' % a)
    try:
        PR(1437); rep(False, '--pr 1437 (a foreign PR) was ACCEPTED')
    except SystemExit:
        rep(True, 'WRONG-PR ARM --pr 1437 -> refused')
    try:
        PR(1441); rep(False, '--pr 1441 (the PREVIOUS gate\'s PR) was ACCEPTED')
    except SystemExit:
        rep(True, 'WRONG-PR ARM --pr 1441 (gate80\'s PR) -> refused')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A: print(__doc__); return 2
    try:
        if A[0] == 'set':
            return run_set(req(A, '--repo'), dict((n, req(A, '--head' + n, True)) for n in K['go_prs']), req(A, '--base', True), req(A, '--develop', True))
        repo = req(A, '--repo'); p = PR(req(A, '--pr')); head = req(A, '--head', True); base = req(A, '--base', True); develop = req(A, '--develop', True)
        end_tree = req(A, '--end-tree', True); n_par = int(req(A, '--parents-n'))
    except SystemExit as e:
        print(e); return 2
    print('C1 #%s head %s base %s develop %s end-tree %s parents-n %d repo %s' % (p['pr'], head, base, develop, end_tree, n_par, repo))
    return run(repo, p, head, base, develop, end_tree, n_par, '--no-remote' not in A)


if __name__ == '__main__':
    sys.exit(main())
