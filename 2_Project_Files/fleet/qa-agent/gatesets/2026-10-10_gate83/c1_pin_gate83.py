#!/usr/bin/env python3
"""c1_pin_gate83.py — C1 PIN for gate83: ONE PR, #1450 (KS-1426, Seat F 10th, tier 2): lockfile-cleanroom.sh gains report_surface(). Read verbs only. Carried from
c1_pin_gate82.py; [g83] marks this kit's changes (ONE PR, so no `set` census of the gated PRs; instead `companions` censuses #1450 against the OTHER writers of the two
shared docs, #1444 / #1447 / #1449 / #1448, whose flow numbers 50 / 51 / 52 / 54 bracket #1450's 53).

EVERY PIN IS A REQUIRED ARGUMENT (no default; a wrong value FAILS its check — the wrong-value arms are in --selftest and KIT_REPORT):
  --repo R --pr 1450 --head H --base B --develop D --end-tree T --parents-n N   [--no-remote]
  c1_pin_gate83.py companions --repo R --head1450 H --base1450 B --develop D --comp-head-1444 H --comp-head-1447 H --comp-head-1449 H --comp-head-1448 H   (P13, the census)

  P1  origin refs/pull/<n>/head == refs/heads/<branch> == --head   (ls-remote; NOT RUN by name with --no-remote)
  P2  head is a commit | EXACTLY --parents-n parents | first parent == --base   (three facts, three reasons)
  P2b develop descends from --base; merge-base(head, develop) printed
  P3  base..head paths == EXACTLY the kit's paths with the kit numstat
  P4  END_TREE == --end-tree (and kit end_tree printed beside it)
  P5  %(trailers) CONTENT 0 bytes on the head; CONTROL bf277eead268 prints > 0
  P6  0 Co-Authored-By in the message; CONTROL carries >= 1
  P7  subject == kit subject, len <= 92 AS DECLARED (no `(#n)` arithmetic), no `(#`; the subject carries the PR's own key
  P8  only the PR's own key hyphenated in the message; closing-family words counted (incl. the `fix(KS-n)` form, INFO)
  P9  PER-PATH modes at base and head == the kit's (everything 100644, lockfile-cleanroom.sh included: it is run as `bash <file>`);
      diff --summary == exactly the kit's `create mode 100644` list (the ONE new test)
  P10 NO-NEW-LEG: every kit tooling / code-surface path (minus the PR's own paths) PRESENT with the SAME (mode, blob) at base, head, develop
  P11 0 package.json / package-lock.json paths in base..head (locks and manifests; also what keeps the path-filtered pr-lockfiles.yml from running)
  P12 base..develop intersected with the PR's paths is a subset of the known docs overlap — printed by name; any OTHER PR path or tooling path FAILS
  P13 (companions) the docs are shared by #1450 and every companion; NO non-doc path is shared by #1450 and any companion (the kit's known_code_overlap is EMPTY);
      every companion head resolvable; each companion's flow number is not 53 and not another companion's
rc 0 all pass / 1 a FAIL / 2 refused (missing argument, unresolvable sha)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate83 import K, PR, COMP, Tally, git, resolvable, blob, req, opt

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


def companion_ok(own_nondoc, comps, docs, known_code):
    """own_nondoc: set of #1450's non-doc paths; comps: {n: {'paths': [...], 'flow': int}}. -> (why, shared)."""
    why = []; shared = {}; docs = set(docs); flows = {}
    for n, c in comps.items():
        ps = set(c['paths'])
        if not docs <= ps: why.append('#%s lacks doc %s' % (n, sorted(docs - ps)))
        sh = sorted(own_nondoc & (ps - docs))
        if sh: shared[n] = sh
        flows.setdefault(c['flow'], []).append(n)
    if shared != dict((n, sorted(v)) for n, v in known_code.items()): why.append('non-doc paths shared with #1450 %s != the kit known_code_overlap %s' % (shared, known_code))
    dup = dict((f, v) for f, v in flows.items() if len(v) > 1 or f == int(K['prs']['1450']['flow_block'].rstrip('.')))
    if dup: why.append('flow number collision %s (#1450 owns %s)' % (dup, K['prs']['1450']['flow_block']))
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
    known = sorted(K.get('known_foreign_keys', {}).get(p['pr'], []))
    t.check('P8', keys == sorted(set([p['ticket']] + known)), 'hyphenated keys in the message %s (want only %s%s) | de-hyphenated mentions %d | Refs lines %d' % (
        keys, p['ticket'], (' + the kit-pinned KNOWN FOREIGN key(s) %s' % known) if known else '', len(re.findall(r'\bKS \d+\b', msg)), len(re.findall(r'(?m)^Refs %s\b' % p['ticket'], msg))))
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
    t.check('P11', not man, 'manifests / locks changed %s (none: the PR matches neither `paths:` filter of pr-lockfiles.yml)' % (man or 0))
    adv = [l for l in git(repo, 'diff', '--name-only', base, develop).split('\n') if l]
    shared, unknown, tool = overlap(adv, ns, K['tooling_paths_unchanged'], K['known_develop_overlap'])
    t.check('P12', not unknown and not tool, 'base..develop: %d path(s); shared with the PR %d %s (known docs overlap = the MERGE SEAT\'s keep-both); '
            'UNKNOWN overlap %s; tooling %s' % (len(adv), len(shared), shared, unknown or 0, tool or 0))
    return t.end()


def own_paths(repo, develop, head, parent_hint):
    """a PR's OWN changed paths: head against merge-base(develop, head), else against its pinned parent (a head that merged develop in has merge-base == develop)."""
    mb = git(repo, 'merge-base', develop, head).strip()
    base = mb if mb != head else parent_hint
    return base, parse_numstat(git(repo, 'diff', '--numstat', base, head))


def run_companions(repo, head, base, develop, comp_heads):
    t = Tally(); docs = list(K['known_develop_overlap']); order = sorted(K['companions'])
    for lab, sha_ in [('head1450', head), ('base1450', base), ('develop', develop)] + [('comp-head-' + n, comp_heads[n]) for n in order]:
        if not resolvable(repo, sha_): print('REFUSED: %s %s is not in %s' % (lab, sha_, repo)); return 2
    ns = parse_numstat(git(repo, 'diff', '--numstat', base, head)); own = set(ns) - set(docs)
    comps = {}; rows = []
    for n in order:
        c = COMP(n); b_, cns = own_paths(repo, develop, comp_heads[n], c['parents'][0])
        m = re.findall(r'(?m)^\+<h2>(\d+)\. ', git(repo, 'diff', b_, comp_heads[n], '--', docs[0]))
        flow = int(m[-1]) if m else -1
        comps[n] = {'paths': sorted(cns), 'flow': flow}
        frag = '\n'.join(l[1:] for l in git(repo, 'diff', b_, comp_heads[n], '--', docs[0]).split('\n') if l.startswith('+') and not l.startswith('+++'))
        landed = bool(frag) and frag in git(repo, 'show', '%s:%s' % (develop, docs[0]))
        rows.append('#%s flow %s (kit %s) head %s base %s own non-doc paths %s | LANDED in develop %s: %s (%s)' % (
            n, flow, c['flow'], comp_heads[n][:12], b_[:12], sorted(set(cns) - set(docs)), develop[:12], landed, 'the block is in develop; c3 compose / docs EXCLUDE it' if landed else 'still open'))
    for r in rows: t.info('P13-ROW', r)
    why, shared = companion_ok(own, comps, docs, K['known_code_overlap'])
    t.check('P13', not why, '#1450 owns %d non-doc path(s) %s; shared with %d companion(s): %s; kit known_code_overlap %s %s' % (len(own), sorted(own), len(comps), shared or 'NONE', K['known_code_overlap'], why or 'OK'))
    t.check('P13b', all(comps[n]['flow'] == COMP(n)['flow'] for n in order), 'each companion\'s flow heading on its head == the kit\'s: %s' % dict((n, (comps[n]['flow'], COMP(n)['flow'])) for n in order))
    t.check('P13c', len(set(comp_heads.values()) | {head}) == len(order) + 1, '%d distinct heads (#1450 + %d companions)' % (len(order) + 1, len(order)))
    for n in order:
        mb = git(repo, 'merge-base', '--is-ancestor', COMP(n)['parents'][0], develop, check=False)[0] == 0
        t.info('P13d', '#%s parent %s is %s an ancestor of develop %s' % (n, COMP(n)['parents'][0][:12], '' if mb else 'NOT', develop[:12]))
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    n = '1450'; p = PR(n); want = dict((x, list(v)) for x, v in p['numstat'].items())
    rep(not numstat_ok(dict(want), want), '#%s numstat: the exact %d-path set passes' % (n, len(want)))
    w2 = dict(want); w2[p['code_paths'][0]] = [want[p['code_paths'][0]][0] + 1, 0]
    rep(numstat_ok(w2, want), '#%s PLANTED +1 on %s FAILS' % (n, p['code_paths'][0].split('/')[-1]))
    w3 = dict(want); w3.pop(p['code_paths'][-1])
    rep(numstat_ok(w3, want), '#%s PLANTED missing path FAILS' % n)
    w4 = dict(want, **{'systemTest/akto/package-lock.json': [1, 0]})
    rep(numstat_ok(w4, want), '#%s PLANTED lock path in the diff FAILS' % n)
    rep(not modes_ok(p['modes'], p['modes']), '#%s modes: the kit modes pass' % n)
    m2 = dict(p['modes']); m2[p['gate_script']] = '100755'
    rep(modes_ok(m2, p['modes']), '#%s PLANTED mode flip 100644 -> 100755 on %s FAILS (the script is run as `bash <file>`; nothing executable gained)' % (n, p['gate_script'].split('/')[-1]))
    ok, _ = summary_ok(' create mode 100644 %s\n' % p['added_paths'][0], p['added_paths']); rep(ok, '#%s summary: the one declared ADD passes' % n)
    ok, _ = summary_ok(' create mode 100755 %s\n' % p['added_paths'][0], p['added_paths']); rep(not ok, '#%s PLANTED 100755 on the new test FAILS' % n)
    b = 'b' * 40
    rep(not parents_ok([b], 1, b), 'parents: one parent == base passes')
    rep(parents_ok([b, 'c' * 40], 1, b), 'PLANTED merge commit (2 parents, first == base) FAILS on the count')
    rep(parents_ok(['c' * 40], 1, b), 'WRONG-VALUE ARM --base FAILS the first-parent check')
    rep(parents_ok([K['bases']['1450']], 1, K['develop_at_draft']), '[g83] WRONG-VALUE ARM the develop (87f005901b00) given as --base FAILS the first-parent check (the PR branches from a78413d3de3e, develop has moved)')
    rep(parents_ok([b], 2, b), 'WRONG-VALUE ARM --parents-n 2 FAILS')
    rep(not tooling_moved({'x': ('100644 a', '100644 a', '100644 a')}), 'tooling: identical present blobs pass')
    rep(tooling_moved({'x': ('', '', '')}), 'PLANTED absent-everywhere tooling path FAILS (absent is a state)')
    rep(tooling_moved({'x': ('100644 a', '100644 b', '100644 b')}), 'PLANTED tooling path moved at head FAILS')
    ok, _ = summary_ok('', []); rep(ok, 'summary: NO create mode passes when none is declared')
    ok, _ = summary_ok(' create mode 100644 x.ts\n', []); rep(not ok, 'PLANTED create mode where none is declared FAILS')
    ok, _ = summary_ok(' create mode 100644 %s\n delete mode 100644 x.ts\n' % p['added_paths'][0], p['added_paths']); rep(not ok, 'PLANTED extra delete in --summary FAILS')
    k, c, co, fx = msg_findings('KS-1426: x\n\nRefs KS-1426\nthe KS 808 item; KS 1031.\n')
    rep(k == ['KS-1426'] and co == 0 and not fx, 'message: de-hyphenated keys are not keys')
    k, c, co, fx = msg_findings('x\n\nFixes KS-808.\nCo-Authored-By: X <x@y>\n')
    rep(k == ['KS-808'] and c and co == 1, 'PLANTED `Fixes KS-808` + Co-Authored-By: foreign key, closing word and trailer all FIRE')
    sh, unk, tool = overlap(K['known_develop_overlap'], p['numstat'], K['tooling_paths_unchanged'], K['known_develop_overlap'])
    rep(sh and not unk and not tool, 'P12: develop touching only the two known docs passes (named, not hidden)')
    for path in (p['gate_script'], p['suite']):
        sh, unk, tool = overlap([path], p['numstat'], K['tooling_paths_unchanged'], K['known_develop_overlap'])
        rep(unk == [path], 'PLANTED develop touching %s FAILS P12 (UNKNOWN overlap)' % path.split('/')[-1])
    for tp in ('Blockchain/Dev/scripts/preflight/preflight.sh', '.github/workflows/pr-lockfiles.yml', 'Blockchain/Dev/scripts/run-shell-suites.sh'):
        sh, unk, tool = overlap([tp], p['numstat'], K['tooling_paths_unchanged'], K['known_develop_overlap'])
        rep(tool == [tp], 'PLANTED develop touching the tooling path %s FAILS P12 (tooling)' % tp.split('/')[-1])
    docs = K['known_develop_overlap']; own = set(p['code_paths'])
    real = dict((c_, {'paths': list(COMP(c_)['numstat']), 'flow': COMP(c_)['flow']}) for c_ in sorted(K['companions']))
    why, shared = companion_ok(own, real, docs, K['known_code_overlap'])
    rep(not why and not shared and K['known_code_overlap'] == {}, 'P13: #1450 and the four companions share the two docs and NO non-doc path: %s' % shared)
    pl = dict(real); pl['1447'] = {'paths': real['1447']['paths'] + [p['gate_script']], 'flow': 51}
    rep(companion_ok(own, pl, docs, K['known_code_overlap'])[0], 'PLANTED companion #1447 touching lockfile-cleanroom.sh FAILS P13 (an unlisted shared code path)')
    pl = dict(real); pl['1448'] = {'paths': [x for x in real['1448']['paths'] if x not in docs], 'flow': 54}
    rep(companion_ok(own, pl, docs, K['known_code_overlap'])[0], 'PLANTED companion without the docs FAILS P13')
    pl = dict(real); pl['1449'] = {'paths': real['1449']['paths'], 'flow': 53}
    rep(companion_ok(own, pl, docs, K['known_code_overlap'])[0], 'PLANTED companion that also numbers its flow block 53 FAILS P13 (a flow-number collision with #1450)')
    pl = dict(real); pl['1449'] = {'paths': real['1449']['paths'], 'flow': 51}
    rep(companion_ok(own, pl, docs, K['known_code_overlap'])[0], 'PLANTED two companions on flow 51 FAILS P13')
    for a in (['--repo', 'x'], ['--repo', 'x', '--head', 'abc']):
        try:
            req(a, '--head', hex40=True); rep(False, 'required --head missing/short was ACCEPTED')
        except SystemExit:
            rep(True, 'REQUIRED-ARG ARM %s -> refused' % a)
    for foreign in (1441, 1443, 1444, 1445, 1446, 1447, 1448, 1449):
        try:
            PR(foreign); rep(False, '--pr %s (not the gated PR) was ACCEPTED' % foreign)
        except SystemExit:
            rep(True, 'WRONG-PR ARM --pr %s (not the gated PR; a companion or an earlier gate\'s PR) -> refused' % foreign)
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A: print(__doc__); return 2
    try:
        if A[0] == 'companions':
            return run_companions(req(A, '--repo'), req(A, '--head1450', True), req(A, '--base1450', True), req(A, '--develop', True),
                                  dict((n, req(A, '--comp-head-' + n, True)) for n in sorted(K['companions'])))
        repo = req(A, '--repo'); p = PR(req(A, '--pr')); head = req(A, '--head', True); base = req(A, '--base', True); develop = req(A, '--develop', True)
        end_tree = req(A, '--end-tree', True); n_par = int(req(A, '--parents-n'))
    except SystemExit as e:
        print(e); return 2
    print('C1 #%s head %s base %s develop %s end-tree %s parents-n %d repo %s' % (p['pr'], head, base, develop, end_tree, n_par, repo))
    return run(repo, p, head, base, develop, end_tree, n_par, '--no-remote' not in A)


if __name__ == '__main__':
    sys.exit(main())
