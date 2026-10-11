#!/usr/bin/env python3
"""c1_pin_gate85.py — C1 PIN for gate85: ONE PR, #1453 (KS-1432), TIER 1 proposed, the gate decides. Read verbs only. Ported from c1_pin_gate84.py; [g85] marks this kit's changes:
the head is ONE commit directly on develop (its ONE parent == the base == develop at the draft), so the gate84 prev_head machinery is gone; `docsbase` keeps the G83-1 control (the parent a docs
instrument uses is merge-base(develop, head), asserted == --base) with controls that a WRONG base is detected (an unrelated older commit, the head given as its own base, and, once develop has
moved, develop given as the base) and a byte-flipped fragment is detected by its sha.

EVERY PIN IS A REQUIRED ARGUMENT (no default; a wrong value FAILS its check — the wrong-value arms are in --selftest):
  --repo R --pr 1453 --head H --base B --develop D --end-tree T --parents-n N   [--no-remote]
  c1_pin_gate85.py docsbase --repo R --head H --base B --develop D

  P1  origin refs/pull/<n>/head == refs/heads/<branch> == --head   (ls-remote; NOT RUN by name with --no-remote)
  P2  head is a commit | EXACTLY --parents-n parents | its parent == --base == the kit's base | rev-list base..head == the kit's commits_n (1)
  P2b develop descends from --base; merge-base(head, develop) == --base (the branch point); develop's distance from the base is printed (0 = unmoved since the draft)
  P3  base..head paths == EXACTLY the kit's paths with the kit numstat
  P4  END_TREE == --end-tree (and kit end_tree printed beside it)
  P5  %(trailers) CONTENT 0 bytes on the commit; CONTROL bf277eead268 prints > 0
  P6  0 Co-Authored-By in the message; CONTROL carries >= 1
  P7  the commit's subject == the kit's declared squash subject (= the PR title, 71 chars): <= 92 AS DECLARED, no `(#`, starts with the own key
  P8  only the PR's own key hyphenated in the message; closing-family words counted (incl. the `fix(KS-n)` form, INFO)
  P9  PER-PATH modes at base and head == the kit's (everything 100644: no mode change, no path created or deleted: diff --summary EMPTY)
  P10 NO-NEW-LEG: every kit tooling / code-surface path (minus the PR's own paths) PRESENT with the SAME (mode, blob) at base, head, develop
  P11 0 package.json / package-lock.json paths in base..head
  P12 base..develop intersected with the PR's paths is a subset of the known docs overlap — printed by name; either CODE path or any tooling path FAILS
  DB1..DB3 (docsbase) the docs base = merge-base(develop, head) == --base (== head^ here); each doc head == base + ONE exact insert immediately before `</body>\\n</html>\\n`; the fragment byte size AND sha256/16
      equal the kit's (5,350 / 2,251 B); CONTROLS: the same extraction against an unrelated older commit / against the head itself reads NOT an exact insert, and a one-byte-flipped fragment fails the sha
rc 0 all pass / 1 a FAIL / 2 refused (missing argument, unresolvable sha)."""
import hashlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate85 import K, PR, Tally, git, resolvable, blob, req, opt, docs_base, show, exact_tail_insert, TAIL

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
    """[g85] the head's ONE parent is the BASE (a single commit directly on develop)."""
    why = []
    if len(parents) != n: why.append('parent count %d != %d' % (len(parents), n))
    if not parents or parents[0] != base: why.append('parent %s != the base %s' % ((parents or ['NONE'])[0][:12], base[:12]))
    return why


def tooling_moved(readings):
    return ['%s %s' % (p, [x[-12:] if x else 'ABSENT' for x in r]) for p, r in readings.items() if not (r[0] and len(set(r)) == 1)]


def modes_ok(got, want):
    return sorted((p, m) for p, m in got.items() if want.get(p) != m)


def summary_ok(summ, added):
    want = sorted(' create mode 100644 %s' % p for p in added)
    got = sorted(l for l in summ.split('\n') if l.strip())
    return got == want, got


def overlap(adv, pr_paths, tooling, known):
    shared = sorted(set(adv) & set(pr_paths)); tool = sorted(set(adv) & set(tooling))
    return shared, [p for p in shared if p not in known], tool


def run(repo, p, head, base, develop, end_tree, n_par, remote):
    t = Tally()
    for s_, n in ((head, 'head'), (base, 'base'), (develop, 'develop'), (K['trailer_control'], 'trailer control')):
        if not resolvable(repo, s_):
            print('REFUSED: %s %s is not in %s (fetch it BY SHA into YOUR clone)' % (n, s_, repo)); return 2
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
    commits = [c for c in git(repo, 'rev-list', '--reverse', '%s..%s' % (base, head)).split() if c]
    isanc = git(repo, 'merge-base', '--is-ancestor', base, head, check=False)[0] == 0
    t.check('P2', typ == 'commit' and not why and len(commits) == p['commits_n'] and isanc and commits == [head] and base == p['base'],
            'type %s | %d parent(s) (want %d) | parent %s (want the base %s) %s | commits base..head %d %s (want %d: the head only) | base is an ancestor of head: %s | --base == kit base: %s' % (
                typ, len(parents), n_par, (parents or ['NONE'])[0][:12], base[:12], why or '', len(commits), [c[:12] for c in commits], p['commits_n'], isanc, base == p['base']))
    mb = git(repo, 'merge-base', head, develop).strip()
    anc = git(repo, 'merge-base', '--is-ancestor', base, develop, check=False)[0] == 0
    gap = len([c for c in git(repo, 'rev-list', '%s..%s' % (base, develop)).split() if c])
    t.check('P2b', anc and mb == base,
            'develop %s descends from the base %s: %s | merge-base(head, develop) = %s == base: %s | develop is %d commit(s) past the base (0 = unmoved since the draft; >0 = develop MOVED: P12 names what it touched)' % (
                develop[:12], base[:12], anc, mb[:12], mb == base, gap))
    ns = parse_numstat(git(repo, 'diff', '--numstat', base, head))
    bad = numstat_ok(ns, p['numstat'])
    t.check('P3', not bad, '%d paths, +%d -%d (kit %d paths +%d -%d) %s' % (len(ns), sum(v[0] for v in ns.values()), sum(v[1] for v in ns.values()),
            p['file_count'], p['adds_dels'][0], p['adds_dels'][1], bad[:4] or 'exact'))
    tree = git(repo, 'rev-parse', head + '^{tree}').strip()
    t.check('P4', tree == end_tree, 'END_TREE %s == --end-tree %s (kit %s: %s)' % (tree, end_tree, p['end_tree'], tree == p['end_tree']))
    ctl = git(repo, 'log', '-1', '--format=%(trailers)', K['trailer_control'])
    trs = [(c, git(repo, 'log', '-1', '--format=%(trailers)', c)) for c in commits]
    t.check('P5', all(x.strip() == '' for _, x in trs) and ctl.strip() != '', 'trailers content per commit %s | CONTROL %s content %d bytes' % (
        [(c[:12], len(x.strip()), len(x)) for c, x in trs], K['trailer_control'], len(ctl.strip())))
    msgs = [(c, git(repo, 'log', '-1', '--format=%B', c)) for c in commits]
    co_ctl = msg_findings(git(repo, 'log', '-1', '--format=%B', K['trailer_control']))[2]
    cos = [(c[:12], msg_findings(m)[2]) for c, m in msgs]
    t.check('P6', all(n == 0 for _, n in cos) and co_ctl >= 1, 'Co-Authored-By per commit %s | CONTROL %s carries %d' % (cos, K['trailer_control'], co_ctl))
    subj = msgs[0][1].split('\n', 1)[0] if msgs else ''
    g = subj == p['subject'] and len(subj) <= p['subject_max'] and '(#' not in subj and subj.startswith(p['ticket'] + ':')
    t.check('P7', g, 'commit subject %r %d chars == kit: %s, <= %d AS DECLARED, "(#" %s, starts with own key %s | the declared SQUASH subject is the commit\'s = the PR title (%r): the merge tools append nothing' % (
        subj, len(subj), subj == p['subject'], p['subject_max'], '(#' in subj, subj.startswith(p['ticket'] + ':'), p['title_observed']))
    known = sorted(K.get('known_foreign_keys', {}).get(p['pr'], []))
    allkeys = sorted(set(k for _, m in msgs for k in msg_findings(m)[0]))
    t.check('P8', allkeys == sorted(set([p['ticket']] + known)), 'hyphenated keys over %d message(s) %s (want only %s%s) | de-hyphenated mentions %d | Refs lines per commit %s' % (
        len(msgs), allkeys, p['ticket'], (' + KNOWN FOREIGN %s' % known) if known else '', sum(len(re.findall(r'\bKS \d+\b', m)) for _, m in msgs),
        [len(re.findall(r'(?m)^Refs %s\b' % p['ticket'], m)) for _, m in msgs]))
    t.info('P8-CLOSING', 'closing-family matches per commit (incl. the conventional `fix(KS-n)` form): %s' % ([(c[:12], msg_findings(m)[1] or msg_findings(m)[3] or 'none') for c, m in msgs]))
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
            'per-path modes at head %s (wrong vs kit: %s) | at base %s (wrong: %s) over %d + %d blob readings | diff --summary %s (want %d create-mode line(s): none created, none deleted, no mode change)' % (
                sorted(set(got_h.values())), bad_h or 'none', sorted(set(got_b.values())), bad_b or 'none', len(got_h), len(got_b), sgot, len(p['added_paths'])))
    tooling = [x for x in K['tooling_paths_unchanged'] if x not in ns]
    readings = dict((x, tuple(blob(repo, r, x) for r in (base, head, develop))) for x in tooling)
    moved = tooling_moved(readings)
    t.check('P10', not moved, 'NO-NEW-LEG: %d tooling / code-surface paths present and identical at base / head / develop %s' % (len(readings), moved[:4] or ''))
    man = [x for x in ns if x.endswith('package.json') or x.endswith('package-lock.json')]
    t.check('P11', not man, 'manifests / locks changed %s (none)' % (man or 0))
    adv = [l for l in git(repo, 'diff', '--name-only', base, develop).split('\n') if l]
    shared, unknown, tool = overlap(adv, ns, K['tooling_paths_unchanged'], K['known_develop_overlap'])
    t.check('P12', not unknown and not tool, 'base..develop: %d path(s); shared with the PR %d %s (known docs overlap = the MERGE SEAT\'s keep-both); '
            'UNKNOWN overlap (a code path of the PR) %s; tooling %s' % (len(adv), len(shared), shared, unknown or 0, tool or 0))
    return t.end()


def run_docsbase(repo, p, head, base, develop):
    """[g85] THE G83-1 CONTROL (kept). Which parent does a docs instrument use, and does it read the right one? The right one is merge-base(develop, head) == --base; here head^ is the same commit."""
    t = Tally(); docs = list(K['known_develop_overlap'])
    try:
        mb, info = docs_base(repo, develop, head, base)
    except SystemExit as e:
        print(e); return 2
    t.check('DB1', mb == base and info['merge_base_is_head_parent'] and info['head_parent'] == base,
            'docs_base = merge-base(develop %s, head %s) = %s == --base %s; head^ = %s (a single commit directly on the base: head^ == the base HERE; the gate84 PR was different)' % (develop[:12], head[:12], mb[:12], base[:12], info['head_parent'][:12]))
    wrong = K['trailer_control']
    for i, d in enumerate(docs):
        bd, hd, dd, wd = show(repo, mb, d), show(repo, head, d), show(repo, develop, d), show(repo, wrong, d)
        ok, frag, why = exact_tail_insert(bd, hd)
        fb = len(frag.encode('utf-8')) if ok else -1; fh = hashlib.sha256(frag.encode('utf-8')).hexdigest()[:16] if ok else ''
        want = K['docfacts'][d]['fragment_bytes']; wsha = K['docfacts'][d]['fragment_sha256_16']
        t.check('DB2', ok and fb == want and fh == wsha and (frag.count('<h2>%s ' % p['flow_block']) == 1 if i == 0 else len([l for l in frag.split('\n') if '<h2' in l and p['cheat_key'] in l]) == 1),
                '%s: head doc == base prefix + ONE fragment + %r: %s (%s) | fragment %d B (kit %d) sha256/16 %s (kit %s) | %s' % (
                    d.split('/')[-1][:40], TAIL, ok, why, fb, want, fh, wsha, ('flow heading `<h2>%s` x%d' % (p['flow_block'], frag.count('<h2>%s ' % p['flow_block']))) if i == 0 else 'cheat <h2> carrying `%s` x%d (mentions %d)' % (p['cheat_key'], len([l for l in frag.split('\n') if '<h2' in l and p['cheat_key'] in l]), frag.count(p['cheat_key']))))
        ok_w, frag_w, why_w = exact_tail_insert(wd, hd)
        t.check('DB3-CONTROL', not (ok_w and len(frag_w.encode('utf-8')) == want), '%s CONTROL (an unrelated OLDER commit %s given as the base): the same extraction reads %s (%d B != the real %d B) -> the instrument can tell a wrong base from the right one' % (
            d.split('/')[-1][:40], wrong, 'an exact insert' if ok_w else 'NOT an exact insert (%s)' % why_w, len(frag_w.encode('utf-8')) if ok_w else -1, want))
        ok_s, frag_s, why_s = exact_tail_insert(hd, hd)
        t.check('DB3b-CONTROL', not ok_s, '%s CONTROL (the head given as its own base): %s (%s) -> an empty fragment is refused' % (d.split('/')[-1][:40], 'an exact insert?!' if ok_s else 'NOT an exact insert', why_s))
        flipped = hd[:len(bd) - len(TAIL) + 20] + ('X' if hd[len(bd) - len(TAIL) + 20] != 'X' else 'Y') + hd[len(bd) - len(TAIL) + 21:]
        okf, fragf, _ = exact_tail_insert(bd, flipped)
        t.check('DB3c-CONTROL', okf and len(fragf.encode()) == want and hashlib.sha256(fragf.encode()).hexdigest()[:16] != wsha, '%s CONTROL (ONE byte of the fragment flipped): the size still equals the kit\'s %d B but the sha256/16 reads %s != %s -> the sha, not the size, is the instrument' % (
            d.split('/')[-1][:40], want, hashlib.sha256(fragf.encode()).hexdigest()[:16], wsha))
        if develop != base:
            ok_d, _, why_d = exact_tail_insert(dd, hd)
            t.check('DB3d-CONTROL', not ok_d, '%s CONTROL (develop %s itself given as the base): %s' % (d.split('/')[-1][:40], develop[:12], 'an exact insert?!' if ok_d else 'NOT an exact insert (%s)' % why_d))
        okd, fragd, whyd = exact_tail_insert(bd, dd)
        t.info('DB4', '%s: develop %s doc vs base: %s%s' % (d.split('/')[-1][:40], develop[:12], 'identical' if dd == bd else ('a pure tail insert of %d B' % len(fragd.encode()) if okd else 'NOT a pure tail insert (%s)' % whyd),
               (' | flow numbers in document order, last 8: %s' % re.findall(r'<h2>(\d+)\. ', dd)[-8:]) if i == 0 else ''))
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    n = '1453'; p = PR(n); want = dict((x, list(v)) for x, v in p['numstat'].items())
    rep(not numstat_ok(dict(want), want), '#%s numstat: the exact %d-path set passes' % (n, len(want)))
    w2 = dict(want); w2[p['code_paths'][0]] = [want[p['code_paths'][0]][0] + 1, want[p['code_paths'][0]][1]]
    rep(numstat_ok(w2, want), '#%s PLANTED +1 on %s FAILS' % (n, p['code_paths'][0].split('/')[-1]))
    w3 = dict(want); w3.pop(p['code_paths'][-1])
    rep(numstat_ok(w3, want), '#%s PLANTED missing path FAILS' % n)
    w4 = dict(want, **{'Blockchain/Dev/services/api-gateway/package-lock.json': [1, 0]})
    rep(numstat_ok(w4, want), '#%s PLANTED lock path in the diff FAILS' % n)
    w5 = dict(want, **{'Blockchain/Dev/services/api-gateway/src/__tests__/zz_new.test.ts': [5, 0]})
    rep(numstat_ok(w5, want), '#%s PLANTED extra test file in the diff FAILS' % n)
    rep(not modes_ok(p['modes'], p['modes']), '#%s modes: the kit modes pass' % n)
    m2 = dict(p['modes']); m2[p['product']] = '100755'
    rep(modes_ok(m2, p['modes']), '#%s PLANTED mode flip 100644 -> 100755 on %s FAILS' % (n, p['product'].split('/')[-1]))
    ok, _ = summary_ok('', p['added_paths']); rep(ok, '#%s summary: NO create mode passes (the PR creates nothing)' % n)
    ok, _ = summary_ok(' create mode 100644 x.ts\n', p['added_paths']); rep(not ok, '#%s PLANTED create mode where none is declared FAILS' % n)
    ok, _ = summary_ok(' mode change 100644 => 100755 x.ts\n', p['added_paths']); rep(not ok, '#%s PLANTED mode change line in --summary FAILS' % n)
    b = p['base']
    rep(not parents_ok([b], 1, b), '[g85] parents: ONE parent == the base passes (a single commit directly on develop)')
    rep(parents_ok([b, 'c' * 40], 1, b), 'PLANTED merge commit (2 parents, first == base) FAILS on the count')
    rep(parents_ok(['c' * 40], 1, b), 'WRONG-VALUE ARM an unrelated parent FAILS')
    rep(parents_ok([b], 2, b), 'WRONG-VALUE ARM --parents-n 2 FAILS')
    rep(not tooling_moved({'x': ('100644 a', '100644 a', '100644 a')}), 'tooling: identical present blobs (3 readings) pass')
    rep(tooling_moved({'x': ('', '', '')}), 'PLANTED absent-everywhere tooling path FAILS (absent is a state)')
    rep(tooling_moved({'x': ('100644 a', '100644 b', '100644 b')}), 'PLANTED tooling path moved at head FAILS')
    k, c, co, fx = msg_findings('KS-1432: x\n\nRefs KS-1432\nthe KS 808 item; KS 1031.\n')
    rep(k == ['KS-1432'] and co == 0 and not fx, 'message: de-hyphenated keys are not keys')
    k, c, co, fx = msg_findings('x\n\nFixes KS-808.\nCo-Authored-By: X <x@y>\n')
    rep(k == ['KS-808'] and c and co == 1, 'PLANTED `Fixes KS-808` + Co-Authored-By: foreign key, closing word and trailer all FIRE')
    sh, unk, tool = overlap(K['known_develop_overlap'], p['numstat'], K['tooling_paths_unchanged'], K['known_develop_overlap'])
    rep(sh and not unk and not tool, 'P12: develop touching only the two known docs passes (named, not hidden)')
    for path in (p['product'], p['test_file']):
        sh, unk, tool = overlap([path], p['numstat'], K['tooling_paths_unchanged'], K['known_develop_overlap'])
        rep(unk == [path], 'PLANTED develop touching %s FAILS P12 (UNKNOWN overlap)' % path.split('/')[-1])
    for tp in ('.githooks/pre-push', '.github/workflows/pr-platform-suites.yml', 'Blockchain/Dev/services/api-gateway/vitest.config.ts'):
        sh, unk, tool = overlap([tp], p['numstat'], K['tooling_paths_unchanged'], K['known_develop_overlap'])
        rep(tool == [tp], 'PLANTED develop touching the tooling path %s FAILS P12 (tooling)' % tp.split('/')[-1])
    base_ = 'A\nB\n' + TAIL; head_ = 'A\nB\nFRAG\n' + TAIL
    ok, fr, _ = exact_tail_insert(base_, head_); rep(ok and fr == 'FRAG\n', 'exact_tail_insert: base + FRAG\\n before the tail reads an exact insert of FRAG\\n')
    rep(not exact_tail_insert(base_, 'A\nB\nFRAG\n</body>\n')[0], 'PLANTED head without the `</html>` tail FAILS')
    rep(not exact_tail_insert(base_, 'a\nB\nFRAG\n' + TAIL)[0], 'PLANTED altered base byte FAILS (a second edit elsewhere)')
    rep(not exact_tail_insert(base_, base_)[0], 'PLANTED no change FAILS (empty fragment)')
    rep(not exact_tail_insert(base_, 'A\nB\nFRAG\n' + TAIL + 'X')[0], 'PLANTED trailing byte after the tail FAILS')
    rep(not exact_tail_insert(base_, 'A\nFRAG\nB\n' + TAIL)[0], 'PLANTED insert in the middle (not before the tail) FAILS')
    f1 = exact_tail_insert(base_, 'A\nB\nFRAG1\n' + TAIL)[1]; f2 = exact_tail_insert(base_, 'A\nB\nFRAG2\n' + TAIL)[1]
    rep(len(f1) == len(f2) and hashlib.sha256(f1.encode()).hexdigest() != hashlib.sha256(f2.encode()).hexdigest(), '[g85] a one-byte-flipped fragment keeps its SIZE but changes its sha256 (the kit pins the sha as well as the size)')
    for a in (['--repo', 'x'], ['--repo', 'x', '--head', 'abc']):
        try:
            req(a, '--head', hex40=True); rep(False, 'required --head missing/short was ACCEPTED')
        except SystemExit:
            rep(True, 'REQUIRED-ARG ARM %s -> refused' % a)
    for foreign in (1441, 1443, 1444, 1445, 1446, 1447, 1448, 1449, 1450, 1451, 1452):
        try:
            PR(foreign); rep(False, '--pr %s (not the gated PR) was ACCEPTED' % foreign)
        except SystemExit:
            rep(True, 'WRONG-PR ARM --pr %s (not the gated PR; a companion or an earlier gate\'s PR) -> refused' % foreign)
    rep(K['companions'] == {} and K['companions_list'] == [], '[g85] the kit carries NO companion (the batch is #1453 alone)')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A: print(__doc__); return 2
    try:
        if A[0] == 'docsbase':
            return run_docsbase(req(A, '--repo'), PR('1453'), req(A, '--head', True), req(A, '--base', True), req(A, '--develop', True))
        repo = req(A, '--repo'); p = PR(req(A, '--pr')); head = req(A, '--head', True); base = req(A, '--base', True); develop = req(A, '--develop', True)
        end_tree = req(A, '--end-tree', True); n_par = int(req(A, '--parents-n'))
    except SystemExit as e:
        print(e); return 2
    print('C1 #%s head %s base %s develop %s end-tree %s parents-n %d repo %s' % (p['pr'], head, base, develop, end_tree, n_par, repo))
    return run(repo, p, head, base, develop, end_tree, n_par, '--no-remote' not in A)


if __name__ == '__main__':
    sys.exit(main())
