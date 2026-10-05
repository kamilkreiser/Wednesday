#!/usr/bin/env python3
"""c4_docs_gate64.py — C4 DOCS (Q-DOC (b): NO doc block) + the KEY-ANCHORED merge-in rule (Q-M) for #1389 (KS-1330).

WHY KEY-ANCHORED (tonight's rule, gate62 N-1387-5 / N-1387-6, gate63): the cheat sheet has NO readable ordering invariant (h2 order
on develop is append order; #1382's KS-1005 section landed UNWRAPPED). So nothing here places or compares a doc block by number,
by tail position or by `<div class="section">`. Sections are found by their h2 KS KEY (flow `(KS-n)</h2>`, cheat `&mdash; KS-n</h2>`).
#1389 carries NO doc hunk (Q-DOC (b), the builder's ruling accepted by Wednesday), so the key-anchored target is: every doc at the
merge-in == develop's doc, key for key and byte for byte, with NO KS-1330 key anywhere; the only paths that differ from develop are
the two kit paths, at the HEAD's blobs. The TARGET TREE `predict` writes is the authority (Q-M M1).

docs --repo <git dir> [--head <sha>] [--develop <sha>]          READ verbs only.
  D1  the skill at develop: blob == kit eaf43dfd4d98; §4 :362-:363 DEFINES "test change" (backend unit, integration, or systemTest)
      and :417-:418 says "say so explicitly and why" — the two quotes the PR body rests Q-DOC (b) on, asserted byte-present at the
      kit line numbers
  D2  parent..head names 0 paths under `Projects Documents/` (and 0 `.html`); both platform-k docs at head == at the head's parent
  D3  THE BODY'S TIMING-GREP CLAIM: `-i -E 'run-shell-suites|shell suites|leg 14|leg-14'` = 0 hits in EACH of both HTML docs,
      `Blockchain/Dev/CLAUDE.md`, `systemTest/CLAUDE.md` and the skill — measured at the HEAD tree, per file, each beside a
      must-hit control (`akto`, -i, must be > 0 in that same file) and an inverted control (an absent token, must be 0). A file
      ABSENT from the tree FAILS (a grep over a missing file is a blind zero). INFO: the body's control figures 70 / 82 / 16
  D4  INFO the same grep over both docs at DEVELOP: lines a merge-in will carry (develop's own KS-1388 run lines `# 67 suites`)
  D5  KEY CENSUS: 0 h2 keyed KS-1330 in either doc at the head; 0 flow h2 numbered 25.-32. at the head (RESERVED AND UNUSED, Q-DOC
      (b)); INFO the h2 key lists at develop
predict --repo <OWN scratch clone> --develop-after <D> [--order key|headdocs] [--out <dir>]   WRITE verbs (temp index); rc 2 in !CODING
  REFUSES unless: D's blobs at the 2 kit paths == the head's PARENT's (develop never touched them), and the head's docs == its
  parent's (no doc hunk). Then: D's tree, the 2 kit paths at the HEAD's blobs + modes, every doc KEY-checked == D's.
  `--order headdocs` is the CONTROL (the branch's stale docs kept, as an `-s ours`-shaped merge would): it must give a DIFFERENT tree
  whenever develop moved a doc. Positive controls: D == parent -> END_TREE 273ec1c0ee3a; D == the kit develop -> the kit's
  merge_in_predicted_tree bc8774cbe5cd (the drafter's `git merge-tree --write-tree`).
qm --repo <clone> --merge-in-head <M> --develop-after <D> [--predicted <tree>]
  M1 tree(M) == prediction (THE AUTHORITY) · M2 parents == [head, D] · M3 D..M names only the 2 kit paths, each at the head's blob
  · M4 0 trailers (raw 1 byte), 0 Co-Authored-By · M5 the head's parent AND the kit develop are ancestors of D · M6 parent..D is
  path-disjoint from the 2 kit paths and the 2 hook paths · M7 head..M not on D is exactly [M] · M8 KEY-ANCHORED docs: per doc, the
  h2 key LIST at M == at D (same keys, same order), every keyed section byte-identical, the doc blob == D's, KS-1330 keyed 0 times
--selftest [--scratch-clone <dir>]   docs arms on synthetic fixtures + (with a clone) predict/qm arms on SIM commits in that clone.
rc 0 all PASS / rc 1 any FAIL or 0 checked / rc 2 refused."""
import os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate64 import K, git, wgit, Tally, outside_forbidden, SCRATCH

DOCS = (K['flow'], K['cheat'])
KEYRX = {K['flow']: re.compile(K['flow_key_rx']), K['cheat']: re.compile(K['cheat_key_rx'])}
CODE = list(K['files'].keys())
HOOKS = list(K['hook_blobs'].keys())
GREP = re.compile(K['docs_grep_rx'], re.I)
CTL = re.compile('akto', re.I)
ABSENT = re.compile('zq-gate64-absent-token-zq', re.I)
SCOPE_Q = ['**Every test change updates its platform\'s two HTML docs, in the same commit —',
           '"Test change" means backend unit, integration, *or* systemTest.']
WHY_Q = ['If a change genuinely does not affect either doc, **say so explicitly and why** —', 'do not silently skip.']


class Refused(Exception):
    pass


def L(s): return s.split('\n')


def keyed(doc, text):
    """[(key, start, end)] in document order: a section runs from its keyed h2 line to the line before the next `<h2>` line."""
    lines = L(text); rx = KEYRX[doc]; h2 = [i for i, l in enumerate(lines) if '<h2>' in l]
    out = []
    for n, i in enumerate(h2):
        m = rx.search(lines[i])
        if m:
            out.append(('KS-' + m.group(1), i, h2[n + 1] if n + 1 < len(h2) else len(lines)))
    return out


def key_list(doc, text): return [k for k, _, _ in keyed(doc, text)]


def sections(doc, text):
    lines = L(text); d = {}
    for k, s, e in keyed(doc, text):
        if k in d: raise Refused('%s: key %s on more than one h2 (a key must be unique to anchor on)' % (os.path.basename(doc), k))
        d[k] = '\n'.join(lines[s:e])
    return d


def flow_numbers(text): return [int(x) for x in re.findall(r'<h2>\s*(\d+)\.', text)]


# ---------------- docs ----------------

def judge_docs(m, t):
    sk = m['skill_text']; sl = L(sk)
    a, b = K['skill_quote_lines']['s4_scope']; c, d = K['skill_quote_lines']['s4_say_why']
    scope = '\n'.join(sl[a - 1:b]); why = '\n'.join(sl[c - 1:d])
    q1 = all(q in scope for q in SCOPE_Q); q2 = all(q in why for q in WHY_Q)
    t.check('D1', m['skill_blob'] == K['skill_blob'] and q1 and q2, 'skill blob %s (want %s); §4 :%d-:%d defines "test change" %s; :%d-:%d "say so explicitly and why" %s' % (
        m['skill_blob'][:12], K['skill_blob'][:12], a, b, q1, c, d, q2))
    docp = [p for p in m['touched'] if p.startswith('Projects Documents/') or p.endswith('.html')]
    same = all(m['head_docs'][p] == m['parent_docs'][p] for p in DOCS)
    t.check('D2', not docp and same, 'parent..head doc paths %s (want none); both platform-k docs at head == at parent %s' % (docp, same))
    rows, bad = [], []
    for p in K['docs_grep_files']:
        x = m['grep_head'].get(p)
        if x is None:
            rows.append('%s ABSENT' % p); bad.append(p); continue
        h = [i + 1 for i, l in enumerate(L(x)) if GREP.search(l)]; c1 = sum(1 for l in L(x) if CTL.search(l)); c0 = sum(1 for l in L(x) if ABSENT.search(l))
        rows.append('%s hits %d %s | control akto %d | inverted %d' % (os.path.basename(p) if p in DOCS else p, len(h), h[:6], c1, c0))
        if h or c1 == 0 or c0 != 0: bad.append(p)
    t.check('D3', not bad, "the body's claim '0 hits in each of the 5 files' at the head: " + ' || '.join(rows) + ' ; failing files %s' % bad)
    t.info('D3-CTL', "the body's must-hit control figures 'Akto 70 / 82 / 16' — the per-file akto (-i) line counts above are the measured ones")
    for p in DOCS:
        x = m['develop_docs'][p]; h = [(i + 1, l.strip()[:110]) for i, l in enumerate(L(x)) if GREP.search(l)]
        t.info('D4', 'develop %s: %d grep line(s) a merge-in carries: %s' % (os.path.basename(p), len(h), h))
    k1330 = {os.path.basename(p): key_list(p, m['head_docs'][p]).count('KS-1330') for p in DOCS}
    resv = [n for n in flow_numbers(m['head_docs'][K['flow']]) if 25 <= n <= 32]
    t.check('D5', not any(k1330.values()) and not resv, 'h2 keyed KS-1330 at head %s (want 0); flow h2 numbered 25.-32. at head %s (want none: RESERVED AND UNUSED)' % (k1330, resv))
    for p in DOCS:
        t.info('D5-KEYS', 'develop %s h2 keys in order: %s' % (os.path.basename(p), key_list(p, m['develop_docs'][p])))


def blob_or_none(repo, rev, p):
    rc, o, e = git(repo, 'rev-parse', '--verify', '--quiet', '%s:%s' % (rev, p), check=False)
    return o.strip() if rc == 0 else None


def show_or_none(repo, rev, p):
    rc, o, e = git(repo, 'show', '%s:%s' % (rev, p), check=False)
    return o if rc == 0 else None


def docs_measure(repo, head, develop):
    par = git(repo, 'log', '-1', '--format=%P', head).split()[0]
    return {'skill_blob': git(repo, 'rev-parse', '%s:%s' % (develop, K['skill'])).strip(), 'skill_text': git(repo, 'show', '%s:%s' % (develop, K['skill'])),
            'touched': git(repo, 'diff', '--name-only', par, head).splitlines(),
            'head_docs': {p: git(repo, 'show', '%s:%s' % (head, p)) for p in DOCS}, 'parent_docs': {p: git(repo, 'show', '%s:%s' % (par, p)) for p in DOCS},
            'develop_docs': {p: git(repo, 'show', '%s:%s' % (develop, p)) for p in DOCS},
            'grep_head': {p: show_or_none(repo, head, p) for p in K['docs_grep_files']}}


# ---------------- predict / qm ----------------

def predict(repo, D, out, order='key', head=None):
    head = head or K['head']
    if not outside_forbidden(repo):
        print('REFUSED: predict writes objects; %s is inside %s — use your OWN scratch clone' % (repo, os.environ.get('G64_FORBIDDEN_ROOT', K['forbidden_root']))); raise SystemExit(2)
    par = git(repo, 'log', '-1', '--format=%P', head).split()[0]
    for p in CODE:
        if blob_or_none(repo, par, p) != blob_or_none(repo, D, p):
            print('PREDICT REFUSED: develop-after %s changed kit path %s since the head\'s parent (M6 fails: RE-GATE)' % (D[:12], p)); return None
    for p in DOCS:
        if blob_or_none(repo, par, p) != blob_or_none(repo, head, p):
            print('PREDICT REFUSED: the head %s carries a hunk in %s (Q-DOC (b) says it carries none: RE-DRAFT)' % (head[:12], p)); return None
    try:
        for p in DOCS:
            dt = git(repo, 'show', '%s:%s' % (D, p)); sd = sections(p, dt)
            if 'KS-1330' in sd: raise Refused('develop-after already carries a KS-1330 keyed section in %s' % os.path.basename(p))
    except Refused as e:
        print('PREDICT REFUSED: %s' % e); return None
    os.makedirs(out, exist_ok=True)
    idx = os.path.join(out, 'predict.index.%d' % os.getpid()); env = {'GIT_INDEX_FILE': idx}
    rc, o, e = wgit(repo, 'read-tree', D, env=env); assert rc == 0, e
    for p in CODE:   # the head's blob AND mode, read from the head's tree
        meta = git(repo, 'ls-tree', head, '--', p).split('\t')[0].split()
        rc, o, e = wgit(repo, 'update-index', '--add', '--cacheinfo', '%s,%s,%s' % (meta[0], meta[2], p), env=env); assert rc == 0, e
    if order == 'headdocs':   # CONTROL ONLY: keep the branch's (parent's) docs
        for p in DOCS:
            rc, o, e = wgit(repo, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (blob_or_none(repo, head, p), p), env=env); assert rc == 0, e
    rc, tree, e = wgit(repo, 'write-tree', env=env); assert rc == 0, e
    q = os.path.join(out, '_quarantine'); os.makedirs(q, exist_ok=True)
    shutil.move(idx, os.path.join(q, os.path.basename(idx) + '.' + tree.strip()[:8]))   # quarantine, never rm
    tree = tree.strip(); print('PREDICTED %s (order %s, develop-after %s)' % (tree, order, D[:12])); return tree


def qm(repo, M, D, pred, t, head=None):
    head = head or K['head']; par = git(repo, 'log', '-1', '--format=%P', head).split()[0]
    tm = git(repo, 'rev-parse', M + '^{tree}').strip()
    t.check('M1', pred is not None and tm == pred, 'tree(M) %s vs predicted %s — THE AUTHORITY' % (tm[:12], str(pred)[:12]))
    pp = git(repo, 'log', '-1', '--format=%P', M).split()
    t.check('M2', pp == [head, D], 'parents %s (want [%s, %s])' % ([p[:12] for p in pp], head[:12], D[:12]))
    names = git(repo, 'diff', '--name-only', D, M).splitlines()
    bad = [p for p in names if p not in CODE]; drift = [p for p in CODE if blob_or_none(repo, M, p) != blob_or_none(repo, head, p)]
    t.check('M3', not bad and not drift, 'D..M paths %d %s; non-kit %s; kit paths off the head blob %s' % (len(names), names[:4], bad, drift))
    tb = len(git(repo, 'log', '-1', '--format=%(trailers)', M).encode()); co = len(re.findall(r'(?im)^co-authored-by:', git(repo, 'log', '-1', '--format=%B', M)))
    t.check('M4', tb == 1 and co == 0, 'M trailers raw %d byte(s), Co-Authored-By %d (want 1 / 0)' % (tb, co))
    r1 = git(repo, 'merge-base', '--is-ancestor', par, D, check=False)[0]; r2 = git(repo, 'merge-base', '--is-ancestor', K['develop_at_draft'], D, check=False)[0]
    t.check('M5', r1 == 0 and r2 == 0, "head's parent %s ancestor of D %s: %s; kit develop %s ancestor-or-equal of D: %s" % (par[:12], D[:12], r1 == 0, K['develop_at_draft'][:12], r2 == 0))
    adv = git(repo, 'diff', '--name-only', par, D).splitlines(); hit = sorted(set(adv) & set(CODE + HOOKS))
    t.check('M6', not hit, "develop's advance %s..%s: %d path(s); kit / hook paths among them %s" % (par[:12], D[:12], len(adv), hit))
    new = git(repo, 'rev-list', '%s..%s' % (head, M), '^' + D).split()
    t.check('M7', new == [M], 'commits in head..M not on D: %s (want exactly [M])' % [c[:12] for c in new])
    res = []
    for p in DOCS:
        dm = show_or_none(repo, M, p); dd = show_or_none(repo, D, p)
        try:
            ok = (dm is not None and dd is not None and key_list(p, dm) == key_list(p, dd) and sections(p, dm) == sections(p, dd)
                  and blob_or_none(repo, M, p) == blob_or_none(repo, D, p) and 'KS-1330' not in key_list(p, dm))
        except Refused:
            ok = False
        res.append((os.path.basename(p)[:24], ok))
    t.check('M8', all(o for _, o in res), 'KEY-ANCHORED docs at M == at D (key list + order, every keyed section, blob; KS-1330 keyed 0): %s' % res)


# ---------------- self-test ----------------

def selftest(scratch=None):
    import io, contextlib, copy
    fx = os.path.join(SCRATCH, 'fixtures'); os.makedirs(fx, exist_ok=True)
    flow = ('<html>\n  <body>\n    <h2>13. A (KS-1345)</h2>\n    <p>a</p>\n    <h2>14. B (KS-1388)</h2>\n    <p>Akto run</p>\n'
            '    <h2>19. C (KS-1005)</h2>\n    <p>c</p>\n  </body>\n</html>\n')
    cheat = ('<html>\n  <body>\n      <h2>A &mdash; KS-1345</h2>\n      <p>Akto</p>\n      <h2>C &mdash; KS-1005</h2>\n  </body>\n</html>\n')
    sk = ['x'] * 430
    sk[361] = SCOPE_Q[0]; sk[362] = 'not a follow-up.** ' + SCOPE_Q[1]; sk[416] = '- ' + WHY_Q[0]; sk[417] = '  ' + WHY_Q[1]; sk[100] = 'Akto'
    skill = '\n'.join(sk)
    clean = {'skill_blob': K['skill_blob'], 'skill_text': skill, 'touched': list(CODE),
             'head_docs': {K['flow']: flow, K['cheat']: cheat}, 'parent_docs': {K['flow']: flow, K['cheat']: cheat},
             'develop_docs': {K['flow']: flow, K['cheat']: cheat},
             'grep_head': {K['flow']: flow, K['cheat']: cheat, 'Blockchain/Dev/CLAUDE.md': 'Akto here\n', 'systemTest/CLAUDE.md': 'akto\n', K['skill']: skill}}
    for k, v in (('flow', flow), ('cheat', cheat), ('skill', skill)):
        open(os.path.join(fx, 'c4_clean_%s.txt' % k), 'w', encoding='utf-8').write(v)
    def run(m):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): judge_docs(m, t)
        return t
    t0 = run(clean); ok = int(not t0.fails and t0.n == 4); total = 1
    print('SELFTEST %s T0 clean synthetic fixture (fixtures/c4_clean_*.txt): %d checked, fails %s' % ('OK' if ok else 'MISS', t0.n, t0.fails))
    def arm_grep(p, extra):
        def f(m): m['grep_head'][p] = m['grep_head'][p] + extra
        return f
    arms = [
        ('skill blob drifted', lambda m: m.update(skill_blob='0' * 40), ['D1']),
        ('§4 :362-:363 definition moved off its line', lambda m: m.update(skill_text=skill.replace(SCOPE_Q[1], 'moved')), ['D1']),
        ('§4 :417 "say so explicitly and why" removed', lambda m: m.update(skill_text=skill.replace('**say so explicitly and why**', 'say so')), ['D1']),
        ('the head touches the flow doc', lambda m: m['touched'].append(K['flow']), ['D2']),
        ('head flow != parent flow', lambda m: m['head_docs'].update({K['flow']: flow.replace('<p>a</p>', '<p>a2</p>')}), ['D2']),
        ('a `shell suites` line in systemTest/CLAUDE.md', arm_grep('systemTest/CLAUDE.md', 'for shell suites under __tests__\n'), ['D3']),
        ('a `run-shell-suites` line in the cheat doc', arm_grep(K['cheat'], 'bash run-shell-suites.sh # 67 suites\n'), ['D3']),
        ('a `leg 14` line in the skill', arm_grep(K['skill'], 'Leg 14 runs it\n'), ['D3']),
        ('Blockchain/Dev/CLAUDE.md ABSENT from the tree', lambda m: m['grep_head'].update({'Blockchain/Dev/CLAUDE.md': None}), ['D3']),
        ('blind must-hit control (no akto in systemTest/CLAUDE.md)', lambda m: m['grep_head'].update({'systemTest/CLAUDE.md': 'nothing\n'}), ['D3']),
        ('a KS-1330 block in the flow doc', lambda m: m['head_docs'].update({K['flow']: flow.replace('  </body>', '    <h2>25. Runner signals (KS-1330)</h2>\n  </body>')}), ['D2', 'D5']),
        ('a reserved number 26. used', lambda m: m['head_docs'].update({K['flow']: flow.replace('19. C (KS-1005)', '26. C (KS-1005)')}), ['D2', 'D5']),
        ('a KS-1330 cheat section', lambda m: m['head_docs'].update({K['cheat']: cheat.replace('  </body>', '      <h2>Signals &mdash; KS-1330</h2>\n  </body>')}), ['D2', 'D5']),
    ]
    for name, mut, want in arms:
        m = copy.deepcopy(clean); mut(m); assert m != clean, 'tamper did not land: ' + name
        t = run(m); total += 1; g = set(want) <= set(t.fails); ok += g
        print('SELFTEST %s %s (landed): want FAIL %s | got %s' % ('OK' if g else 'MISS', name, want, t.fails))
    # key parser arms (the anchor itself)
    total += 1; kl = key_list(K['flow'], flow); g = kl == ['KS-1345', 'KS-1388', 'KS-1005']; ok += g
    print('SELFTEST %s key parser on the flow fixture: %s' % ('OK' if g else 'MISS', kl))
    total += 1
    try:
        sections(K['cheat'], cheat.replace('C &mdash; KS-1005', 'C &mdash; KS-1345')); g = False
    except Refused:
        g = True
    ok += g; print('SELFTEST %s a DUPLICATED key refuses (never anchors on an ambiguous key): %s' % ('OK' if g else 'MISS', 'refused' if g else 'accepted'))
    if scratch:
        a, b = selftest_qm(scratch); ok += a; total += b
    else:
        print('SELFTEST NOTE predict/qm arms NOT run (no --scratch-clone given)')
    print('SELFTEST %s %d of %d' % ('OK' if ok == total else 'BROKEN', ok, total)); print('CHECKED %d arm(s)' % total)
    return 0 if ok == total else 1


def sim_commit(repo, parents, edits, msg, base, out):
    idx = os.path.join(out, 'sim.index.%d' % os.getpid()); env = {'GIT_INDEX_FILE': idx}
    assert wgit(repo, 'read-tree', base, env=env)[0] == 0
    for p, v in edits.items():
        rc, sha, e = wgit(repo, 'hash-object', '-w', '--stdin', input_bytes=v.encode('utf-8')); assert rc == 0, e
        assert wgit(repo, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (sha.strip(), p), env=env)[0] == 0
    rc, tree, e = wgit(repo, 'write-tree', env=env); assert rc == 0, e
    q = os.path.join(out, '_quarantine'); os.makedirs(q, exist_ok=True)
    shutil.move(idx, os.path.join(q, 'sim.index.%d.%s' % (os.getpid(), tree.strip()[:8])))
    args = ['commit-tree', tree.strip()]
    for p in parents: args += ['-p', p]
    rc, c, e = wgit(repo, *args, env={'GIT_AUTHOR_NAME': 'SIM', 'GIT_AUTHOR_EMAIL': 'sim@invalid', 'GIT_COMMITTER_NAME': 'SIM', 'GIT_COMMITTER_EMAIL': 'sim@invalid',
                                     'GIT_AUTHOR_DATE': '2026-10-05T00:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-05T00:00:00Z'}, input_bytes=msg.encode()); assert rc == 0, e
    return c.strip(), tree.strip()


def selftest_qm(repo):
    import io, contextlib
    if not outside_forbidden(repo):
        print('SELFTEST REFUSED scratch clone inside the forbidden root'); return 0, 1
    out = os.path.join(SCRATCH, 'sim'); os.makedirs(out, exist_ok=True)
    h, par, dv = K['head'], K['parent'], K['develop_at_draft']; ok = total = 0
    g = lambda r, p: git(repo, 'show', '%s:%s' % (r, p))
    def q(*a, **k):
        with contextlib.redirect_stdout(io.StringIO()): return predict(*a, **k)
    p0 = q(repo, par, out); total += 1; c = p0 == K['end_tree']; ok += c
    print("SELFTEST %s predict on D == the head's parent gives END_TREE: %s vs %s" % ('OK' if c else 'MISS', str(p0)[:12], K['end_tree'][:12]))
    pr = q(repo, dv, out); prh = q(repo, dv, out, order='headdocs'); total += 1
    c = pr == K['merge_in_predicted_tree'] and bool(prh) and prh != pr; ok += c
    print('SELFTEST %s the REAL develop %s: key prediction %s == kit merge_in_predicted_tree %s; headdocs CONTROL %s differs' % (
        'OK' if c else 'MISS', dv[:12], str(pr)[:12], K['merge_in_predicted_tree'][:12], str(prh)[:12]))
    # SIM develop: another docs PR lands a keyed block ABOVE 19. in the flow and an UNWRAPPED cheat section above KS-1005
    fl = g(dv, K['flow']); ce = g(dv, K['cheat'])
    a19 = '    <h2>19. change-password reads the hash it verifies (KS-1005)</h2>'; assert fl.count(a19) == 1
    fl2 = fl.replace(a19, '    <h2>18. SIM later block (KS-9918)</h2>\n    <p>SIM</p>\n' + a19)
    k5 = '      <h2>change-password reads its own hash &mdash; KS-1005</h2>'; assert ce.count(k5) == 1
    ce2 = ce.replace(k5, '      <h2>SIM later &mdash; KS-9918</h2>\n      <p>SIM unwrapped</p>\n' + k5)
    Dsim, _ = sim_commit(repo, [dv], {K['flow']: fl2, K['cheat']: ce2}, 'SIM develop: a later docs PR lands\n', dv, out)
    P = q(repo, Dsim, out); Ph = q(repo, Dsim, out, order='headdocs'); total += 1; c = bool(P) and P != pr and Ph != P; ok += c
    print('SELFTEST %s predict on SIM develop %s: %s differs from the real-develop prediction and from its headdocs CONTROL %s' % ('OK' if c else 'MISS', Dsim[:12], str(P)[:12], str(Ph)[:12]))
    Mgood, _ = sim_commit(repo, [h, Dsim], {}, 'Merge develop into KS-1330: docs carried from develop\n', P, out)
    def runqm(M, D, pred):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): qm(repo, M, D, pred, t)
        return t
    t = runqm(Mgood, Dsim, P); total += 1; c = not t.fails and t.n == 8; ok += c
    print('SELFTEST %s Q-M positive control (SIM merge-in at the predicted tree): %d checked, fails %s' % ('OK' if c else 'MISS', t.n, t.fails))
    arms = []
    Mh, _ = sim_commit(repo, [h, Dsim], {}, 'Merge\n', Ph, out); arms.append(("the branch's stale docs kept (-s ours shape)", Mh, Dsim, P, ['M1', 'M3', 'M8']))
    fl3 = fl2.replace('    <h2>18. SIM later block (KS-9918)</h2>\n    <p>SIM</p>\n', '').replace('  </body>', '    <h2>18. SIM later block (KS-9918)</h2>\n    <p>SIM</p>\n  </body>', 1)
    assert fl3 != fl2
    Mt, _ = sim_commit(repo, [h, Dsim], {K['flow']: fl3}, 'Merge\n', P, out); arms.append(('a keyed flow block moved to the TAIL (div/tail-anchored)', Mt, Dsim, P, ['M1', 'M3', 'M8']))
    ce3 = ce2.replace('<p>SIM unwrapped</p>', '<p>SIM unwrapped, edited</p>'); assert ce3 != ce2
    Me, _ = sim_commit(repo, [h, Dsim], {K['cheat']: ce3}, 'Merge\n', P, out); arms.append(('a keyed cheat section edited in the merge', Me, Dsim, P, ['M1', 'M3', 'M8']))
    ce4 = ce2.replace(k5, '      <h2>Runner signals &mdash; KS-1330</h2>\n      <p>SIM</p>\n' + k5)
    Mk, _ = sim_commit(repo, [h, Dsim], {K['cheat']: ce4}, 'Merge\n', P, out); arms.append(('a KS-1330 section slipped into the merge', Mk, Dsim, P, ['M1', 'M3', 'M8']))
    M1p, _ = sim_commit(repo, [Dsim], {}, 'squash-shaped\n', P, out); arms.append(('single parent', M1p, Dsim, P, ['M2']))
    Mx, _ = sim_commit(repo, [h, Dsim], {'README.md': 'SIM extra\n'}, 'Merge\n', P, out); arms.append(('an extra non-kit path', Mx, Dsim, P, ['M1', 'M3']))
    Mco, _ = sim_commit(repo, [h, Dsim], {}, 'Merge\n\nCo-Authored-By: X <x@invalid>\n', P, out); arms.append(('a Co-Authored-By trailer', Mco, Dsim, P, ['M4']))
    Dbad, _ = sim_commit(repo, [dv], {K['runner']: g(dv, K['runner']) + '\n# SIM\n'}, 'SIM develop touches the runner\n', dv, out)
    Mb, _ = sim_commit(repo, [h, Dbad], {}, 'Merge\n', P, out); arms.append(("develop's advance touches the runner", Mb, Dbad, None, ['M1', 'M6']))
    Dhk, _ = sim_commit(repo, [dv], {HOOKS[0]: g(dv, HOOKS[0]) + '\n# SIM\n'}, 'SIM develop touches pre-push\n', dv, out)
    Mhk, _ = sim_commit(repo, [h, Dhk], {}, 'Merge\n', q(repo, Dhk, out), out); arms.append(("develop's advance touches .githooks/pre-push", Mhk, Dhk, q(repo, Dhk, out), ['M6']))
    Mi, _ = sim_commit(repo, [h], {}, 'SIM intermediate\n', h, out)
    M2c, _ = sim_commit(repo, [Mi, Dsim], {}, 'Merge\n', P, out); arms.append(('two new commits', M2c, Dsim, P, ['M2', 'M7']))
    Dside, _ = sim_commit(repo, [K['parent']], {K['flow']: fl2}, 'SIM develop that does NOT contain the kit develop\n', K['parent'], out)
    Ms, _ = sim_commit(repo, [h, Dside], {}, 'Merge\n', q(repo, Dside, out), out); arms.append(('D does not descend from the kit develop', Ms, Dside, q(repo, Dside, out), ['M5']))
    for name, M, D, pred, want in arms:
        t = runqm(M, D, pred); total += 1; c = set(want) <= set(t.fails); ok += c
        print('SELFTEST %s Q-M %s: want FAIL %s | got %s' % ('OK' if c else 'MISS', name, want, t.fails))
    pb = q(repo, Dbad, out); total += 1; c = pb is None; ok += c
    print('SELFTEST %s predict REFUSES a develop that changed the runner: %s' % ('OK' if c else 'MISS', 'refused' if pb is None else pb[:12]))
    ce5 = ce.replace(k5, '      <h2>Runner &mdash; KS-1330</h2>\n' + k5)
    D30, _ = sim_commit(repo, [dv], {K['cheat']: ce5}, 'SIM develop already has a KS-1330 section\n', dv, out)
    pk = q(repo, D30, out); total += 1; c = pk is None; ok += c
    print('SELFTEST %s predict REFUSES a develop already carrying a KS-1330 keyed section: %s' % ('OK' if c else 'MISS', 'refused' if pk is None else pk[:12]))
    print('SELFTEST NOTE real develop %s predicted %s; SIM develop %s predicted %s; SIM merge-in %s (objects in %s only; no ref written)' % (
        dv[:12], str(pr)[:12], Dsim[:12], str(P)[:12], Mgood[:12], repo))
    return ok, total


if __name__ == '__main__':
    A = sys.argv[1:]
    if not A or '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    if '--selftest' in A: raise SystemExit(selftest(opt('--scratch-clone')))
    cmd = A[0]; repo = opt('--repo', K['checkout'])
    if cmd == 'docs':
        head = opt('--head', K['head']); dev = opt('--develop', K['develop'])
        print('c4_docs_gate64 docs repo %s head %s develop %s' % (repo, head, dev))
        t = Tally(); judge_docs(docs_measure(repo, head, dev), t); raise SystemExit(t.end())
    if cmd == 'predict':
        p = predict(repo, opt('--develop-after'), opt('--out', os.path.join(SCRATCH, 'predict')), opt('--order', 'key'))
        raise SystemExit(0 if p else 1)
    if cmd == 'qm':
        D = opt('--develop-after'); M = opt('--merge-in-head')
        pred = opt('--predicted') or predict(repo, D, opt('--out', os.path.join(SCRATCH, 'predict')))
        t = Tally(); qm(repo, M, D, pred, t); raise SystemExit(t.end())
    print(__doc__); raise SystemExit(2)
