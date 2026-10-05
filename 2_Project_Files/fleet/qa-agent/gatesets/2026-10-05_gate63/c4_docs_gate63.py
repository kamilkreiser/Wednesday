#!/usr/bin/env python3
"""c4_docs_gate63.py — C4 DOCS + the KEY-ANCHORED Q-M merge-in rule for #1388 (KS-1404 wiring).

WHY KEY-ANCHORED (gate62's findings N-1387-5 / N-1387-6): the cheat sheet has NO readable ordering invariant — #1382's KS-1005
section landed UNWRAPPED on develop 0f2422925317, and h2 order on develop is append order. So this predictor never places a block by
number or by `<div class="section">`: it finds the section by its h2 KS KEY, proves the PR changed ONLY inside that section, proves
develop did NOT touch that section, and swaps the head's section in. The TARGET TREE it writes is the authority (Q-M M1).

SECTION of a doc for a key = from the ONE h2 line carrying the key (flow `(KS-1404)</h2>`, cheat `&mdash; KS-1404</h2>`) to the next
line containing `<h2>`, with trailing blank / `<div class="section">` lines handed to the next section.

docs  --repo <git dir> [--head <sha>]         READ verbs only. Or offline: --flow-base F --flow-head F --cheat-base F --cheat-head F
  D1  skill §4 at the BASE: SKILL.md blob == kit; it names both platform-k docs and "the host"
  D2  ONE commit (base..head) carries the test AND both platform-k docs; 0 platform-s docs touched                    (repo mode)
  D3  flow: `  </body>` once and byte-identical; every h2 line identical base vs head (nothing renumbered, no new top-level number);
      every changed line lies INSIDE the KS-1404 section (11.); every line outside it byte-identical
  D4  flow h3s in 11.: base [11.1, 11.2, 11.3] -> head [11.1, 11.2, 11.3, 11.4], 11.4 LAST and keyed KS-1404; the 11.2 and 11.3
      corrections say what they USED to claim ("previously read" in 11.2, "used to end" in the 11.3 row)
  D5  cheat: `  </body>` once and byte-identical; every h2 identical; every changed line INSIDE the KS-1404 section; exactly ONE new
      `<tr>` row keyed KS-1404 (the wiring row); the corrected sentences say what they used to claim
  D6  each new text (flow 11.4, cheat wiring row) names: the test file, the red/green figures (3 failed / 3 passed, 6 passed), the base
      sha f01c1da5717f, the D-Trust digest 4d24807b, a NOT-proved note, and the date 2026-10-05
  D7  INFO §4 "every figure with its date AND the host": host spellings found in each new text (none is a finding for the gate)
  D8  INFO direction words: every "row below"/"see … below" in the cheat KS-1404 section, and whether the wiring row is in fact BELOW it
predict --repo <OWN scratch clone> --develop-after <D> [--order key|tail] [--out <dir>]   WRITE verbs (temp index), refused in !CODING
  D's tree, with the 7 non-doc kit paths at the HEAD's blobs (asserted: D has the BASE's blobs there, or the path is absent on both)
  and each doc's KS-1404 section replaced by the HEAD's (asserted: D's section == the BASE's, and base/head differ only inside it).
  `--order tail` is the CONTROL (the head's section moved to just before `  </body>`): must give a DIFFERENT tree.
  Positive control: D == base -> END_TREE 979926afe755.
qm --repo <clone> --merge-in-head <M> --develop-after <D> [--predicted <tree>]
  M1 tree(M) == prediction (THE AUTHORITY) · M2 parents == [head, D] · M3 D..M names only kit paths, every non-doc one at the head's
  blob · M4 0 trailers (raw 1 byte), 0 Co-Authored-By · M5 base is an ancestor of D and D != base · M6 base..D path-disjoint from the 7
  non-doc kit paths AND both KS-1404 sections untouched by develop · M7 head..M not on D is exactly [M]
--selftest [--scratch-clone <dir>]   docs arms on fixture copies + (with a clone) predict/qm arms on SIM commits in that clone.
rc 0 all PASS / rc 1 any FAIL or 0 checked / rc 2 refused."""
import difflib, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate63 import K, git, wgit, Tally, outside_forbidden, SCRATCH

CLOSE = K['close_tag']
KEYS = {'flow': K['flow_key_h2'], 'cheat': K['cheat_key_h2']}


class Refused(Exception):
    pass


def L(s): return s.split('\n')


def section(lines, key):
    hits = [i for i, l in enumerate(lines) if '<h2>' in l and l.rstrip().endswith(key)]
    if len(hits) != 1:
        raise Refused('key %r found on %d h2 lines (want exactly 1)' % (key, len(hits)))
    s = hits[0]; e = len(lines)
    for i in range(s + 1, len(lines)):
        if '<h2>' in lines[i]:
            e = i; break
    while e > s + 1 and lines[e - 1].strip() in ('', '<div class="section">'):
        e -= 1
    return s, e


def ops(a, b): return [o for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if o[0] != 'equal']


def confined(base, head, key):
    """True iff every base->head change lies inside the key's section (an insert AT the section end counts as inside)."""
    sb, eb = section(base, key); sh, eh = section(head, key)
    return (base[:sb] == head[:sh] and base[eb:] == head[eh:]), (sb, eb, sh, eh)


def h2s(lines): return [l.strip() for l in lines if '<h2>' in l]


def judge_docs(fb, fh, cb, ch, t, skill=None, commits=None, touched=None):
    if skill is not None:
        sb, stext = skill
        t.check('D1', sb == K['skill_blob_at_base'] and K['flow'] in stext and K['cheat'] in stext and 'the host' in stext,
                'SKILL.md blob %s (want %s); names flow %s, cheat %s, "the host" %s' % (sb[:12], K['skill_blob_at_base'][:12], K['flow'] in stext, K['cheat'] in stext, 'the host' in stext))
    if commits is not None:
        ps = [p for p in touched if p.startswith('docs/platform_s')]
        t.check('D2', commits == 1 and all(p in touched for p in (K['test'], K['flow'], K['cheat'])) and not ps,
                'commits base..head %d (want 1); test+flow+cheat in it %s; platform-s docs %s' % (commits, all(p in touched for p in (K['test'], K['flow'], K['cheat'])), ps))
    A, B = L(fb), L(fh)
    try:
        ok_c, (sb, eb, sh, eh) = confined(A, B, KEYS['flow'])
    except Refused as e:
        ok_c, sb, eb, sh, eh = False, 0, 0, 0, 0; t.info('D3-key', str(e))
    cl = (A.count(CLOSE), B.count(CLOSE))
    t.check('D3', ok_c and cl == (1, 1) and h2s(A) == h2s(B),
            'flow: changes confined to the KS-1404 section (base :%d-:%d, head :%d-:%d) %s; `  </body>` lines base/head %s; h2 lines identical %s (%d h2)' % (
                sb + 1, eb, sh + 1, eh, ok_c, cl, h2s(A) == h2s(B), len(h2s(B))))
    sec = B[sh:eh]; secb = A[sb:eb]
    h3 = lambda ls: re.findall(r'<h3>(\d+\.\d+)', '\n'.join(ls))
    h3b, h3h = h3(secb), h3(sec)
    t4 = [i for i, l in enumerate(sec) if l.strip().startswith('<h3>11.4')]
    s112 = '\n'.join(sec[[i for i, l in enumerate(sec) if '<h3>11.2' in l][0]:[i for i, l in enumerate(sec) if '<h3>11.3' in l][0]]) if '11.2' in h3h and '11.3' in h3h else ''
    s113 = '\n'.join(sec[[i for i, l in enumerate(sec) if '<h3>11.3' in l][0]:(t4[0] if t4 else len(sec))]) if '11.3' in h3h else ''
    ok4 = (h3b == K['flow_h3_base'] and h3h == K['flow_h3_head'] and bool(t4) and 'KS-1404' in sec[t4[0]] and
           'previously read' in s112 and 'used to end' in s113)
    t.check('D4', ok4, 'flow h3 base %s head %s (want %s -> %s); 11.4 keyed KS-1404 %s; 11.2 says "previously read" %s; 11.3 says "used to end" %s' % (
        h3b, h3h, K['flow_h3_base'], K['flow_h3_head'], bool(t4) and 'KS-1404' in sec[t4[0]], 'previously read' in s112, 'used to end' in s113))
    flow_new = '\n'.join(sec[t4[0]:]) if t4 else ''
    C, D_ = L(cb), L(ch)
    try:
        ok_cc, (csb, ceb, csh, ceh) = confined(C, D_, KEYS['cheat'])
    except Refused as e:
        ok_cc, csb, ceb, csh, ceh = False, 0, 0, 0, 0; t.info('D5-key', str(e))
    csec_b, csec_h = C[csb:ceb], D_[csh:ceh]
    rows_b = [l for l in csec_b if l.strip().startswith('<tr>')]; rows_h = [l for l in csec_h if l.strip().startswith('<tr>')]
    new_rows = [l for l in rows_h if l not in rows_b]
    wiring = [l for l in new_rows if re.match(r'\s*<tr><td>(<strong>)?[^<]*KS-1404', l)]
    corr = '\n'.join(csec_h)
    ok5 = (ok_cc and C.count(CLOSE) == 1 and D_.count(CLOSE) == 1 and h2s(C) == h2s(D_) and len(wiring) == 1 and len(rows_h) == len(rows_b) + 1
           and 'was true of #1376 and is now false' in corr and 'previously read' in corr)
    t.check('D5', ok5, 'cheat: confined to the KS-1404 section (base :%d-:%d) %s; close tag %s/%s; h2 identical %s; rows %d -> %d, new rows keyed KS-1404 %d; corrections say what they claimed %s' % (
        csb + 1, ceb, ok_cc, C.count(CLOSE), D_.count(CLOSE), h2s(C) == h2s(D_), len(rows_b), len(rows_h), len(wiring),
        'was true of #1376 and is now false' in corr and 'previously read' in corr))
    cheat_new = wiring[0] if wiring else ''
    for name, txt in (('flow-11.4', flow_new), ('cheat-row', cheat_new)):
        need = {'test file': 'ks1404-wiring.test.ts' in txt, '3 failed / 3 passed': '3 failed / 3 passed' in txt, '6 passed': '6 passed' in txt,
                'base f01c1da5717f': 'f01c1da5717f' in txt or name == 'cheat-row', 'D-Trust digest': '4d24807b' in txt,
                'NOT proved': bool(re.search(r'NOT prove', txt)), 'date 2026-10-05': '2026-10-05' in txt}
        miss = [k for k, v in need.items() if not v]
        t.check('D6-' + name, bool(txt) and not miss, '%s (%d chars) missing %s' % (name, len(txt), miss))
        hosts = re.findall(r"Kamil'?s[ -]Mac[ -]Studio(?: \(2\))?|Mac Studio", txt)
        t.info('D7-' + name, 'host named %d time(s) %s — skill §4 asks every figure for its date AND host: the gate rules' % (len(hosts), hosts[:3]))
    below = [i for i, l in enumerate(csec_h) if re.search(r'row below', l)]
    wi = [i for i, l in enumerate(csec_h) if l in wiring]
    t.info('D8', 'cheat KS-1404 section: "row below" at section lines %s; wiring row at %s; references whose wiring row is NOT below them: %s' % (
        [csh + i + 1 for i in below], [csh + i + 1 for i in wi], [csh + i + 1 for i in below if wi and wi[0] < i]))


def docs_repo(repo, head, t):
    b = K['base']; g = lambda r, p: git(repo, 'show', '%s:%s' % (r, p))
    sb = git(repo, 'rev-parse', '%s:%s' % (b, K['skill'])).strip()
    judge_docs(g(b, K['flow']), g(head, K['flow']), g(b, K['cheat']), g(head, K['cheat']), t, skill=(sb, g(b, K['skill'])),
               commits=len(git(repo, 'rev-list', '%s..%s' % (b, head)).split()), touched=git(repo, 'diff', '--name-only', b, head).splitlines())


# ---------------- predict / qm ----------------

def resolve_doc(dtext, btext, htext, key, order='key'):
    D, B, H = L(dtext), L(btext), L(htext)
    ok, (sb, eb, sh, eh) = confined(B, H, key)
    if not ok:
        raise Refused('the PR changes %s outside its KS-1404 section' % key)
    sd, ed = section(D, key)
    if D[sd:ed] != B[sb:eb]:
        raise Refused('develop changed the KS-1404 section (%s): M6 fails, RE-GATE' % key)
    if order == 'key':
        return '\n'.join(D[:sd] + H[sh:eh] + D[ed:])
    rest = D[:sd] + D[ed:]; c = [i for i, l in enumerate(rest) if l == CLOSE]
    if len(c) != 1:
        raise Refused('close tag count %d' % len(c))
    return '\n'.join(rest[:c[0]] + H[sh:eh] + rest[c[0]:])


def blob_or_none(repo, rev, p):
    rc, o, e = git(repo, 'rev-parse', '--verify', '--quiet', '%s:%s' % (rev, p), check=False)
    return o.strip() if rc == 0 else None


def predict(repo, D, out, order='key', head=None):
    head = head or K['head']; base = K['base']
    if not outside_forbidden(repo):
        print('REFUSED: predict writes objects; %s is inside %s — use your OWN scratch clone' % (repo, K['forbidden_root'])); raise SystemExit(2)
    for p in K['code_paths']:
        if blob_or_none(repo, base, p) != blob_or_none(repo, D, p):   # ex1 history: rev-parse echoes an ABSENT path's arg to stdout
            print('PREDICT REFUSED: develop-after changed %s (M6 fails: re-gate)' % p); return None
    g = lambda r, p: git(repo, 'show', '%s:%s' % (r, p))
    try:
        nf = resolve_doc(g(D, K['flow']), g(base, K['flow']), g(head, K['flow']), KEYS['flow'], order)
        nc = resolve_doc(g(D, K['cheat']), g(base, K['cheat']), g(head, K['cheat']), KEYS['cheat'], order)
    except Refused as e:
        print('PREDICT REFUSED: %s' % e); return None
    os.makedirs(out, exist_ok=True)
    idx = os.path.join(out, 'predict.index.%d' % os.getpid()); env = {'GIT_INDEX_FILE': idx}
    rc, o, e = wgit(repo, 'read-tree', D, env=env); assert rc == 0, e
    for path, text in ((K['flow'], nf), (K['cheat'], nc)):
        rc, sha, e = wgit(repo, 'hash-object', '-w', '--stdin', input_bytes=text.encode('utf-8')); assert rc == 0, e
        rc, o, e = wgit(repo, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (sha.strip(), path), env=env); assert rc == 0, e
    for p in K['code_paths']:
        sha = git(repo, 'rev-parse', '%s:%s' % (head, p)).strip()
        rc, o, e = wgit(repo, 'update-index', '--add', '--cacheinfo', '%s,%s,%s' % (K['modes_all'], sha, p), env=env); assert rc == 0, e
    rc, tree, e = wgit(repo, 'write-tree', env=env); assert rc == 0, e
    q = os.path.join(out, '_quarantine'); os.makedirs(q, exist_ok=True)
    shutil.move(idx, os.path.join(q, os.path.basename(idx) + '.' + tree.strip()[:8]))   # quarantine, never rm
    tree = tree.strip(); print('PREDICTED %s (order %s, develop-after %s)' % (tree, order, D[:12])); return tree


def qm(repo, M, D, pred, t, head=None):
    head = head or K['head']; base = K['base']
    tm = git(repo, 'rev-parse', M + '^{tree}').strip()
    t.check('M1', pred is not None and tm == pred, 'tree(M) %s vs predicted %s — THE AUTHORITY' % (tm[:12], str(pred)[:12]))
    par = git(repo, 'log', '-1', '--format=%P', M).split()
    t.check('M2', par == [head, D], 'parents %s (want [%s, %s])' % ([p[:12] for p in par], head[:12], D[:12]))
    names = git(repo, 'diff', '--name-only', D, M).splitlines()
    bad = [p for p in names if p not in K['files']]
    drift = [p for p in K['code_paths'] if blob_or_none(repo, M, p) != blob_or_none(repo, head, p)]
    t.check('M3', not bad and not drift, 'D..M paths %d; non-kit %s; non-doc paths off the head blob %s' % (len(names), bad, drift))
    tb = len(git(repo, 'log', '-1', '--format=%(trailers)', M).encode()); co = len(re.findall(r'(?im)^co-authored-by:', git(repo, 'log', '-1', '--format=%B', M)))
    t.check('M4', tb == 1 and co == 0, 'M trailers raw %d byte(s), Co-Authored-By %d (want 1 / 0)' % (tb, co))
    rc = git(repo, 'merge-base', '--is-ancestor', base, D, check=False)[0]
    t.check('M5', rc == 0 and D != base, 'base %s is an ancestor of D %s: %s; D moved: %s' % (base[:12], D[:12], rc == 0, D != base))
    adv = git(repo, 'diff', '--name-only', base, D).splitlines(); hit = sorted(set(adv) & set(K['code_paths']))
    g = lambda r, p: git(repo, 'show', '%s:%s' % (r, p)); secs = []
    for doc, key in ((K['flow'], KEYS['flow']), (K['cheat'], KEYS['cheat'])):
        try:
            a = L(g(base, doc)); d = L(g(D, doc)); sa = section(a, key); sd = section(d, key); secs.append(a[sa[0]:sa[1]] == d[sd[0]:sd[1]])
        except Refused:
            secs.append(False)
    t.check('M6', not hit and all(secs), "develop's advance touches %d path(s); kit non-doc paths among them %s; KS-1404 sections untouched by develop (flow, cheat) %s" % (len(adv), hit, secs))
    new = git(repo, 'rev-list', '%s..%s' % (head, M), '^' + D).split()
    t.check('M7', new == [M], 'commits in head..M not on D: %s (want exactly [M])' % [c[:12] for c in new])


# ---------------- self-test ----------------

def selftest(scratch=None):
    import io, contextlib
    fx = os.path.join(SCRATCH, 'fixtures'); os.makedirs(fx, exist_ok=True)
    R = K['checkout']; ok = total = 0
    real = {k: git(R, 'show', '%s:%s' % (rev, K[doc])) for k, rev, doc in
            (('fb', K['base'], 'flow'), ('fh', K['head'], 'flow'), ('cb', K['base'], 'cheat'), ('ch', K['head'], 'cheat'))}
    for k, v in real.items(): open(os.path.join(fx, 'c4_real_%s.html' % k), 'w', encoding='utf-8').write(v)
    def run(d):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): judge_docs(d['fb'], d['fh'], d['cb'], d['ch'], t)
        return t
    t0 = run(real); ok += not t0.fails; total += 1
    print('SELFTEST %s T0 positive control (the REAL blobs, fixtures c4_real_*.html): %d checked, fails %s' % ('OK' if not t0.fails else 'MISS', t0.n, t0.fails))
    def sub(s, a, b):
        assert s.count(a) == 1, 'tamper anchor must occur EXACTLY once (found %d): %r' % (s.count(a), a[:60]); return s.replace(a, b)
    arms = [
        ('flow 11.4 promoted to a new h2 33.', 'fh', lambda s: sub(s, '<h3>11.4 Compose and per-environment wiring (KS-1404, Seat D 8th)</h3>', '<h2>33. Compose and per-environment wiring (KS-1404)</h2>'), ['D3', 'D4']),
        ('flow an edit OUTSIDE 11. (in 12.)', 'fh', lambda s: sub(s, '<h2>12. GET /api/anchors/:id reports blockNumber as a number (KS-1333)</h2>\n    <p>', '<h2>12. GET /api/anchors/:id reports blockNumber as a number (KS-1333)</h2>\n    <p> '), ['D3']),
        ('flow close tag rewritten', 'fh', lambda s: sub(s, '\n  </body>', '\n</body>'), ['D3']),
        ('flow 11.2 correction loses "previously read"', 'fh', lambda s: sub(s, 'this sentence previously read', 'this sentence once said'), ['D4']),
        ('flow 11.4 drops the base sha', 'fh', lambda s: sub(s, '<strong>3 failed / 3 passed at base <code>f01c1da5717f</code>; 6 passed at head.</strong>', '<strong>3 failed / 3 passed at base; 6 passed at head.</strong>'), ['D6-flow-11.4']),
        ('cheat a second new KS-1404 row', 'ch', lambda s: sub(s, '<tr><td><strong>Compose + image wiring (KS-1404, Seat D 8th)</strong></td>', '<tr><td>KS-1404 extra</td><td>x</td></tr>\n        <tr><td><strong>Compose + image wiring (KS-1404, Seat D 8th)</strong></td>'), ['D5']),
        ('cheat an edit in the KS-1333 section', 'ch', lambda s: sub(s, '<h2>GET /api/anchors/:id blockNumber &mdash; KS-1333</h2>\n', '<h2>GET /api/anchors/:id blockNumber &mdash; KS-1333</h2>\n \n'), ['D5']),
        ('cheat wiring row loses the D-Trust digest', 'ch', lambda s: sub(s, '(DER SHA-256 <code>4d24807b&hellip;aef6</code>); nothing fetched', '(DER SHA-256 elided); nothing fetched'), ['D6-cheat-row']),
        ('cheat KS-1404 h2 duplicated (key not unique)', 'ch', lambda s: sub(s, '<h2>GET /api/anchors/:id blockNumber &mdash; KS-1333</h2>', '<h2>Again &mdash; KS-1404</h2>'), ['D5']),
    ]
    for name, key, fn, want in arms:
        d = dict(real); d[key] = fn(d[key]); assert d[key] != real[key], 'tamper did not land: ' + name
        p = os.path.join(fx, 'c4_arm_%02d_%s.html' % (total, key)); open(p, 'w', encoding='utf-8').write(d[key])
        t = run(d); total += 1; new = set(t.fails) - set(t0.fails); g = set(want) <= new; ok += g
        print('SELFTEST %s %s (landed, fixture %s): want NEW FAIL %s | got %s' % ('OK' if g else 'MISS', name, os.path.basename(p), want, sorted(new)))
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
    h, b, dv = K['head'], K['base'], K['develop_at_draft']; ok = total = 0
    g = lambda r, p: git(repo, 'show', '%s:%s' % (r, p))
    q = lambda *a, **k: predict(*a, **k)
    with contextlib.redirect_stdout(io.StringIO()): p0 = q(repo, b, out)
    total += 1; c = p0 == K['end_tree']; ok += c
    print('SELFTEST %s predict on D == base gives END_TREE: %s vs %s' % ('OK' if c else 'MISS', str(p0)[:12], K['end_tree'][:12]))
    with contextlib.redirect_stdout(io.StringIO()): pr = q(repo, dv, out); prt = q(repo, dv, out, order='tail')
    total += 1; c = bool(pr) and bool(prt) and pr != prt; ok += c
    print('SELFTEST %s the REAL develop %s: key-order %s != tail-order CONTROL %s' % ('OK' if c else 'MISS', dv[:12], str(pr)[:12], str(prt)[:12]))
    # SIM develop: #1387-shaped landing on top of the real develop (14. above 19. in the flow; an UNWRAPPED cheat section above KS-1005)
    fl = g(dv, K['flow']); ce = g(dv, K['cheat'])
    a19 = '    <h2>19. change-password reads the hash it verifies (KS-1005)</h2>'; assert fl.count(a19) == 1
    fl = fl.replace(a19, '    <h2>14. SIM nginx status uri (KS-1388)</h2>\n    <p>SIM</p>\n' + a19)
    k5 = '      <h2>change-password reads its own hash &mdash; KS-1005</h2>'; assert ce.count(k5) == 1
    ce = ce.replace(k5, '      <h2>SIM nginx &mdash; KS-1388</h2>\n      <p>SIM unwrapped</p>\n' + k5)
    Dsim, _ = sim_commit(repo, [dv], {K['flow']: fl, K['cheat']: ce}, 'SIM develop: #1387-shaped landing after #1382\n', dv, out)
    with contextlib.redirect_stdout(io.StringIO()): P = q(repo, Dsim, out)
    total += 1; c = bool(P) and P != pr; ok += c
    print('SELFTEST %s predict on SIM develop (#1387-shaped, unwrapped cheat) %s differs from the real-develop prediction %s' % ('OK' if c else 'MISS', str(P)[:12], str(pr)[:12]))
    Mgood, _ = sim_commit(repo, [h, Dsim], {}, 'Merge develop into KS-1404 wiring: docs only\n', P, out)
    def runqm(M, D, pred):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): qm(repo, M, D, pred, t)
        return t
    t = runqm(Mgood, Dsim, P); total += 1; c = not t.fails and t.n == 7; ok += c
    print('SELFTEST %s Q-M positive control (SIM merge-in at the predicted tree): fails %s' % ('OK' if c else 'MISS', t.fails))
    arms = []
    with contextlib.redirect_stdout(io.StringIO()): Ptail = q(repo, Dsim, out, order='tail')
    Mtail, _ = sim_commit(repo, [h, Dsim], {}, 'Merge\n', Ptail, out); arms.append(('11.4 placed at the tail (wrong tree)', Mtail, Dsim, P, ['M1']))
    M1p, _ = sim_commit(repo, [Dsim], {}, 'squash-shaped\n', P, out); arms.append(('single parent', M1p, Dsim, P, ['M2']))
    Mx, _ = sim_commit(repo, [h, Dsim], {'README.md': 'SIM extra\n'}, 'Merge\n', P, out); arms.append(('an extra non-kit path', Mx, Dsim, P, ['M1', 'M3']))
    Mt, _ = sim_commit(repo, [h, Dsim], {}, 'Merge\n\nCo-Authored-By: X <x@invalid>\n', P, out); arms.append(('a Co-Authored-By trailer', Mt, Dsim, P, ['M4']))
    Dbad, _ = sim_commit(repo, [dv], {K['compose']: g(dv, K['compose']) + '\n# SIM\n'}, 'SIM develop touches compose\n', dv, out)
    Mb, _ = sim_commit(repo, [h, Dbad], {}, 'Merge\n', P, out); arms.append(("develop's advance touches docker-compose.yml", Mb, Dbad, None, ['M6']))
    fsec = g(dv, K['flow']).replace('<h3>11.3 Test surface and timings</h3>', '<h3>11.3 Test surface and timings (SIM edit)</h3>', 1)
    Dsec, _ = sim_commit(repo, [dv], {K['flow']: fsec}, 'SIM develop edits 11.3\n', dv, out)
    Ms, _ = sim_commit(repo, [h, Dsec], {}, 'Merge\n', P, out); arms.append(("develop edited the KS-1404 flow section", Ms, Dsec, None, ['M6']))
    Mi, _ = sim_commit(repo, [h], {}, 'SIM intermediate\n', h, out)
    M2c, _ = sim_commit(repo, [Mi, Dsim], {}, 'Merge\n', P, out); arms.append(('two new commits', M2c, Dsim, P, ['M2', 'M7']))
    for name, M, D, pred, want in arms:
        t = runqm(M, D, pred); total += 1; c = set(want) <= set(t.fails); ok += c
        print('SELFTEST %s Q-M %s: want FAIL %s | got %s' % ('OK' if c else 'MISS', name, want, t.fails))
    for name, D in (('compose', Dbad), ('KS-1404 flow section', Dsec)):
        with contextlib.redirect_stdout(io.StringIO()): pb = q(repo, D, out)
        total += 1; c = pb is None; ok += c
        print('SELFTEST %s predict REFUSES a develop that changed %s: %s' % ('OK' if c else 'MISS', name, 'refused' if pb is None else pb[:12]))
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
        t = Tally()
        if opt('--flow-base'):
            rd = lambda k: open(opt(k), encoding='utf-8').read()
            judge_docs(rd('--flow-base'), rd('--flow-head'), rd('--cheat-base'), rd('--cheat-head'), t)
        else:
            docs_repo(repo, opt('--head', K['head']), t)
        raise SystemExit(t.end())
    if cmd == 'predict':
        tr = predict(repo, opt('--develop-after'), opt('--out', os.path.join(SCRATCH, 'sim')), opt('--order', 'key'))
        raise SystemExit(0 if tr else 1)
    if cmd == 'qm':
        D = opt('--develop-after'); pred = opt('--predicted') or predict(repo, D, opt('--out', os.path.join(SCRATCH, 'sim')))
        t = Tally(); qm(repo, opt('--merge-in-head'), D, pred, t); raise SystemExit(t.end())
    print(__doc__); raise SystemExit(2)
