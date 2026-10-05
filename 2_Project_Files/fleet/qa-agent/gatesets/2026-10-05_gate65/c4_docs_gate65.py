#!/usr/bin/env python3
r"""c4_docs_gate65.py — C4 DOCS + the KEY-ANCHORED merge-in predictor / Q-M for #1393 (KS-1278).

WHY KEY-ANCHORED: the cheat sheet has NO readable ordering invariant (committed KS order 1404, 1333, 1345, 1388, [1210,] 1005, appended
order, some sections wrapped in `<div class="section">`, KS-1005 unwrapped), and gate63's predict / B 62nd's own inference reproduced a
WRONG tree byte for byte from a div-anchored reading. So nothing here places a block by `<div class="section">`, by tail position or by
number: the PR's new section is found by its h2 KS KEY, and it is inserted immediately after the section of the KEY THAT PRECEDES IT AT
THE HEAD (flow KS-1388 = 14.; cheat KS-1005). The TARGET TREE this writes is the authority (Q-M M1).

SECTION of a doc for a key = from the ONE `<h2>` line ending in the key (flow `(KS-1278)</h2>`, cheat `&mdash; KS-1278</h2>`) up to
the next line holding `<h2>` OR the `  </body>` close tag, with trailing blank / `<div class="section">` lines handed to what follows.
The PR's BLOCK = the gap after its predecessor's section + its own section; head minus the BLOCK must equal the base BYTE FOR BYTE.

docs  --repo <git dir> [--head <sha>]                      READ verbs only
  D1  skill §4 at the BASE: SKILL.md blob == kit eaf43dfd4d98; it names both platform-k docs
  D2  ONE commit base..head carries the new test AND both platform-k docs (§4: the same commit); 0 platform-s docs
  D3  flow: head minus the KS-1278 BLOCK == base (the ONLY change); exactly one new h2 == kit `15. /revoke is one atomic transition
      (KS-1278)`; its predecessor h2 is 14. (KS-1388) and its successor 19. (KS-1005); every numbered h2 ascending; `  </body>` once
  D4  cheat: head minus the KS-1278 BLOCK == base; exactly one new h2 == kit; it is the LAST h2 (the next structural line is the
      close tag); its predecessor is KS-1005; `  </body>` once
  D5  each new block names: the test file, the base sha 32e058975d4e, the red-first figure (2 failed / 2 passed or 2 red / 2 pass), the
      suite delta 91 / 1067, the date 2026-10-05, the host (Mac Studio), UNMEASURED serialisation, and the 400-vs-404 residual
  D6  the cheat block claims NO ordering invariant for the cheat sheet (no "ascending" / "in KS order" / "ordered by" sentence)
  D7  the TIMING claim at the base: `grep -c -i -E 'originate.*unit suite'` 0 flow / 0 cheat; must-hit controls auth 76 / 75, Akto 71 / 83
  INFO D8 whether either block names the residual ticket KS 1419 (it was filed AFTER the raise), and the "a null can only mean the row
       became revoked" sentence (C3b N2 / N3 are other meanings)
predict --repo <OWN scratch clone> --develop-after <D> [--order key|tail|succ] [--out <dir>]     WRITE verbs (temp index), refused in !CODING
  REFUSES BY NAME, rc 2: `develop unresolvable` when <D> is not a commit in --repo (fetch it by sha into YOUR clone first — gate63's
  predict died inside `git show` instead). Content refusals, rc 1: D changed a CODE path (re-gate) / D already carries KS-1278 / the
  predecessor key is absent in D / the PR's doc change is not ONE keyed block / the flow's ascending invariant breaks.
  TREE = D's tree, the 4 code paths at the HEAD's blobs, each doc = D's doc with the head's BLOCK inserted after the predecessor key's
  section in D. CONTROLS: `--order tail` (block just before the close tag) and `--order succ` (block just before the head successor's
  h2) are DIFFERENT readings: the selftest proves at least one of them gives a different tree on the real develop. DIVERGENCE INFO: when D
  has keyed sections AFTER the predecessor (a section develop appended after KS-1005), the key tree puts KS-1278 ABOVE them (OURS above
  THEIRS, the #1387 ruling) while "LAST" would put it below: printed, Wednesday rules.
qm --repo <clone> --merge-in-head <M> --develop-after <D> [--predicted <tree>]
  M1 tree(M) == prediction (THE AUTHORITY) · M2 parents == [head, D] · M3 D..M names only the 6 kit paths, every code path at the head's
  blob · M4 0 trailers (raw 1 byte), 0 Co-Authored-By · M5 base 32e058975d4e is an ancestor of D and D != base · M6 base..D is
  path-disjoint from the 4 code paths and D carries no KS-1278 key · M7 head..M not on D is exactly [M]. Refuses BY NAME (rc 2) when M or D
  is unresolvable.
--selftest --scratch-clone <dir>   docs arms on fixture copies + predict / qm arms on SIM commits in that clone (objects only, no ref).
rc 0 all PASS / rc 1 any FAIL, a content refusal, or 0 checked / rc 2 refused by name (unresolvable object, forbidden root)."""
import difflib, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate65 import K, git, wgit, Tally, outside_forbidden, SCRATCH

CLOSE = K['close_tag']
KEY = {'flow': K['flow_key_h2'], 'cheat': K['cheat_key_h2']}
KRX = {'flow': re.compile(K['flow_key_rx']), 'cheat': re.compile(K['cheat_key_rx'])}
PRED = {'flow': K['flow_pred_key'], 'cheat': K['cheat_pred_key']}


class Refused(Exception):
    pass


def L(s): return s.split('\n')


def section(lines, keytail):
    hits = [i for i, l in enumerate(lines) if '<h2>' in l and l.rstrip().endswith(keytail)]
    if len(hits) != 1:
        raise Refused('key %r found on %d h2 lines (want exactly 1)' % (keytail, len(hits)))
    s = hits[0]; e = len(lines)
    for i in range(s + 1, len(lines)):
        if '<h2>' in lines[i] or lines[i] == CLOSE:
            e = i; break
    while e > s + 1 and lines[e - 1].strip() in ('', '<div class="section">'):
        e -= 1
    return s, e


def keytail(doc, num): return '(KS-%s)</h2>' % num if doc == 'flow' else '&mdash; KS-%s</h2>' % num


def h2s(lines): return [(i, l.strip()) for i, l in enumerate(lines) if '<h2>' in l]


def block(head_lines, doc):
    """(start, end, pred_key, succ_h2) of the PR's BLOCK in the head: the gap after the predecessor section + the KS-1278 section."""
    sh, eh = section(head_lines, KEY[doc])
    prev = [(i, t) for i, t in h2s(head_lines) if i < sh]
    if not prev:
        raise Refused('%s: no h2 precedes the KS-1278 section' % doc)
    m = KRX[doc].search(prev[-1][1])
    if not m:
        raise Refused('%s: the h2 before KS-1278 carries no KS key (%r): no key to anchor on' % (doc, prev[-1][1][:60]))
    pk = m.group(1); ps, pe = section(head_lines, keytail(doc, pk))
    nxt = [t for i, t in h2s(head_lines) if i > sh]
    return pe, eh, pk, (nxt[0] if nxt else None)


def nums(lines): return [int(m.group(1)) for _, t in h2s(lines) for m in [re.match(r'<h2>(\d+)\.', t)] if m]


def judge_docs(fb, fh, cb, ch, t, skill=None, commits=None, touched=None):
    if skill is not None:
        sb, stext = skill
        t.check('D1', sb == K['skill_blob'] and K['flow'] in stext and K['cheat'] in stext,
                'SKILL.md blob %s (want %s); names flow %s, cheat %s' % (sb[:12], K['skill_blob'][:12], K['flow'] in stext, K['cheat'] in stext))
    if commits is not None:
        ps = [p for p in touched if p.startswith('docs/platform_s')]
        t.check('D2', commits == 1 and all(p in touched for p in (K['test'], K['flow'], K['cheat'])) and not ps,
                'commits base..head %d (want 1); test+flow+cheat in it %s; platform-s docs %s' % (commits, all(p in touched for p in (K['test'], K['flow'], K['cheat'])), ps))
    out = {}
    for doc, b, h, newh2, cid in (('flow', fb, fh, K['flow_new_h2'], 'D3'), ('cheat', cb, ch, K['cheat_new_h2'], 'D4')):
        B, H = L(b), L(h)
        try:
            s, e, pk, succ = block(H, doc)
        except Refused as x:
            t.check(cid, False, '%s: %s' % (doc, x)); out[doc] = ''; continue
        only = H[:s] + H[e:] == B
        new = [x for _, x in h2s(H) if x not in [y for _, y in h2s(B)]]
        cl = (B.count(CLOSE), H.count(CLOSE))
        if doc == 'flow':
            asc = nums(H) == sorted(nums(H)) and len(set(nums(H))) == len(nums(H))
            ok = only and new == [newh2.strip()] and pk == K['flow_pred_key'] and succ is not None and succ.endswith('(KS-%s)</h2>' % K['flow_succ_key']) and asc and cl == (1, 1)
            t.check(cid, ok, 'flow: head minus the KS-1278 block (head :%d-:%d) == base %s | new h2 %s | predecessor KS-%s (want %s) | successor %r | numbered h2 ascending %s %s | close tag %s' % (
                s + 1, e, only, [x[:60] for x in new], pk, K['flow_pred_key'], (succ or '')[:40], asc, nums(H), cl))
        else:
            last = succ is None and H[e:][:3] and CLOSE in H[e:e + 3]
            ok = only and new == [newh2.strip()] and pk == K['cheat_pred_key'] and bool(last) and cl == (1, 1)
            t.check(cid, ok, 'cheat: head minus the KS-1278 block (head :%d-:%d) == base %s | new h2 %s | predecessor KS-%s (want %s) | LAST h2, close tag follows %s | close tag %s' % (
                s + 1, e, only, [x[:60] for x in new], pk, K['cheat_pred_key'], bool(last), cl))
        out[doc] = '\n'.join(H[s:e])
    for doc in ('flow', 'cheat'):
        txt = out.get(doc, ''); flat = re.sub(r'<[^>]+>', '', txt)
        need = {'test file': 'ks1278-revoke-is-one-atomic-transition' in txt, 'base sha': '32e058975d4e' in txt,
                'red-first 2/2': bool(re.search(r'2 failed / 2 passed|2 red / 2 pass', flat)), 'suite 91 / 1067': bool(re.search(r'91\s*/\s*1067', flat)),
                'date': '2026-10-05' in txt, 'host': 'Mac Studio' in txt, 'UNMEASURED': 'UNMEASURED' in flat,
                '400-vs-404 residual': bool(re.search(r'404', flat)) and bool(re.search(r'deleted', flat))}
        miss = [k for k, v in need.items() if not v]
        t.check('D5-' + doc, bool(txt) and not miss, '%s block (%d chars) missing %s' % (doc, len(txt), miss))
    cflat = re.sub(r'<[^>]+>', '', out.get('cheat', ''))
    inv = re.findall(r'[^.]{0,60}\b(ascending|in (?:KS|key|ticket) order|ordered by|ordering invariant)\b[^.]{0,40}', cflat, re.I)
    t.check('D6', bool(out.get('cheat')) and not inv, 'ordering-invariant claims in the cheat block: %s' % (inv or 'none'))
    for doc in ('flow', 'cheat'):
        txt = re.sub(r'<[^>]+>', '', out.get(doc, ''))
        t.info('D8-' + doc, 'names KS 1419: %s | "can only mean the row became revoked": %s' % (
            bool(re.search(r'KS.?1419', txt)), bool(re.search(r'can only mean the row became revoked', txt))))


def timing(fb, cb, t):
    c = lambda s, rx: sum(1 for l in s.split('\n') if re.search(rx, l, re.I))
    got = (c(fb, r'originate.*unit suite'), c(cb, r'originate.*unit suite'), c(fb, r'auth'), c(cb, r'auth'), c(fb, r'Akto'), c(cb, r'Akto'))
    t.check('D7', got == (0, 0, 76, 75, 71, 83), "base 32e058975d4e, line counts -i: 'originate.*unit suite' flow %d cheat %d | must-hit auth %d / %d (claim 76 / 75), Akto %d / %d (claim 71 / 83)" % got)


def docs_repo(repo, head, t):
    b = K['base']; g = lambda r, p: git(repo, 'show', '%s:%s' % (r, p))
    sb = git(repo, 'rev-parse', '%s:%s' % (b, K['skill'])).strip()
    fb, cb = g(b, K['flow']), g(b, K['cheat'])
    judge_docs(fb, g(head, K['flow']), cb, g(head, K['cheat']), t, skill=(sb, g(b, K['skill'])),
               commits=len(git(repo, 'rev-list', '%s..%s' % (b, head)).split()), touched=git(repo, 'diff', '--name-only', b, head).splitlines())
    timing(fb, cb, t)


# ---------------- predict / qm ----------------

def resolvable(repo, sha):
    return bool(sha) and git(repo, 'rev-parse', '--verify', '--quiet', sha + '^{commit}', check=False)[0] == 0


def resolve_doc(doc, dtext, btext, htext, order='key'):
    D, B, H = L(dtext), L(btext), L(htext)
    s, e, pk, succ = block(H, doc)
    if H[:s] + H[e:] != B:
        raise Refused('%s: the PR changes something besides its one KS-1278 block — not a pure keyed insertion' % doc)
    if any(l.rstrip().endswith(KEY[doc]) and '<h2>' in l for l in D):
        raise Refused('%s: develop ALREADY carries a KS-1278 h2 (merged twice? re-gate)' % doc)
    blk = H[s:e]
    if order == 'key':
        try:
            ds, de = section(D, keytail(doc, pk))
        except Refused as x:
            raise Refused('%s: the predecessor key KS-%s is not exactly once in develop (%s): nothing to anchor on, re-gate' % (doc, pk, x))
        at = de
        after = [t for i, t in h2s(D) if i >= de and KRX[doc].search(t)]
        if after and doc == 'cheat':   # the flow is governed by its readable ascending invariant (checked below), not by this
            print('INFO DIVERGENCE %s: develop has %d keyed section(s) AFTER KS-%s %s — the key tree puts KS-1278 ABOVE them (OURS above THEIRS); "LAST" would put it below (see --order tail). Wednesday rules.' % (
                doc, len(after), pk, [KRX[doc].search(t).group(1) for t in after]))
    elif order == 'tail':
        c = [i for i, l in enumerate(D) if l == CLOSE]
        if len(c) != 1: raise Refused('%s: close tag count %d' % (doc, len(c)))
        at = c[0]
    elif order == 'succ':
        if succ is None:
            c = [i for i, l in enumerate(D) if l == CLOSE]; at = c[0]
        else:
            hits = [i for i, l in enumerate(D) if l.strip() == succ]
            if len(hits) != 1: raise Refused('%s: successor h2 not exactly once in develop' % doc)
            at = hits[0]
    else:
        raise Refused('unknown order %r' % order)
    N = D[:at] + blk + D[at:]
    if doc == 'flow' and order == 'key' and not (nums(N) == sorted(nums(N)) and len(set(nums(N))) == len(nums(N))):
        raise Refused('flow: the key-anchored result breaks the readable ascending invariant %s — the anchor and the invariant disagree, re-gate' % nums(N))
    return '\n'.join(N)


def predict(repo, D, out, order='key', head=None):
    head = head or K['head']; base = K['base']
    if not outside_forbidden(repo):
        print('REFUSED: predict writes objects; %s is inside %s — use your OWN scratch clone' % (repo, K['forbidden_root'])); return 'REFUSED'
    for name, s in (('develop', D), ('head', head), ('base', base)):
        if not resolvable(repo, s):
            print('PREDICT REFUSED: %s unresolvable: %r is not a commit in %s — fetch it BY SHA into YOUR clone (X7), then re-run' % (name, s, repo))
            return 'UNRESOLVABLE'
    adv = set(git(repo, 'diff', '--name-only', base, D).splitlines()); hit = sorted(adv & set(K['code_paths']))
    if hit:
        print('PREDICT REFUSED: develop-after changed code path(s) %s since the base (M6 fails: re-gate)' % hit); return None
    g = lambda r, p: git(repo, 'show', '%s:%s' % (r, p))
    try:
        nf = resolve_doc('flow', g(D, K['flow']), g(base, K['flow']), g(head, K['flow']), order)
        nc = resolve_doc('cheat', g(D, K['cheat']), g(base, K['cheat']), g(head, K['cheat']), order)
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


def ok_tree(x): return x not in (None, 'REFUSED', 'UNRESOLVABLE')


def qm(repo, M, D, pred, t, head=None):
    head = head or K['head']; base = K['base']
    for name, s in (('merge-in head', M), ('develop', D)):
        if not resolvable(repo, s):
            print('QM REFUSED: %s unresolvable: %r is not a commit in %s — fetch it BY SHA into YOUR clone (X7)' % (name, s, repo)); return 'UNRESOLVABLE'
    tm = git(repo, 'rev-parse', M + '^{tree}').strip()
    t.check('M1', ok_tree(pred) and tm == pred, 'tree(M) %s vs predicted %s — THE AUTHORITY' % (tm[:12], str(pred)[:12]))
    par = git(repo, 'log', '-1', '--format=%P', M).split()
    t.check('M2', par == [head, D], 'parents %s (want [%s, %s])' % ([p[:12] for p in par], head[:12], D[:12]))
    names = git(repo, 'diff', '--name-only', D, M).splitlines()
    bad = [p for p in names if p not in K['files']]
    drift = [p for p in K['code_paths'] if git(repo, 'rev-parse', '--verify', '--quiet', '%s:%s' % (M, p), check=False)[1].strip() != K['head_blobs'][p]]
    t.check('M3', not bad and not drift, 'D..M paths %d; non-kit %s; code paths off the head blob %s' % (len(names), bad, drift))
    tb = len(git(repo, 'log', '-1', '--format=%(trailers)', M).encode()); co = len(re.findall(r'(?im)^co-authored-by:', git(repo, 'log', '-1', '--format=%B', M)))
    t.check('M4', tb == 1 and co == 0, 'M trailers raw %d byte(s), Co-Authored-By %d (want 1 / 0)' % (tb, co))
    rc = git(repo, 'merge-base', '--is-ancestor', base, D, check=False)[0]
    t.check('M5', rc == 0 and D != base, 'base %s is an ancestor of D %s: %s; D moved: %s' % (base[:12], D[:12], rc == 0, D != base))
    adv = git(repo, 'diff', '--name-only', base, D).splitlines(); hit = sorted(set(adv) & set(K['code_paths']))
    carries = [doc for doc in ('flow', 'cheat') if any('<h2>' in l and l.rstrip().endswith(KEY[doc]) for l in L(git(repo, 'show', '%s:%s' % (D, K[doc]))))]
    t.check('M6', not hit and not carries, "develop's advance %d path(s); code paths among them %s; D already carries KS-1278 in %s" % (len(adv), hit, carries))
    new = git(repo, 'rev-list', '%s..%s' % (head, M), '^' + D).split()
    t.check('M7', new == [M], 'commits in head..M not on D: %s (want exactly [M])' % [c[:12] for c in new])


# ---------------- self-test ----------------

def selftest(scratch=None):
    import io, contextlib
    fx = os.path.join(SCRATCH, 'fixtures'); os.makedirs(fx, exist_ok=True)
    R = scratch or K['checkout']; ok = total = 0
    real = {k: git(R, 'show', '%s:%s' % (rev, K[doc])) for k, rev, doc in
            (('fb', K['base'], 'flow'), ('fh', K['head'], 'flow'), ('cb', K['base'], 'cheat'), ('ch', K['head'], 'cheat'))}
    for k, v in real.items(): open(os.path.join(fx, 'c4_real_%s.html' % k), 'w', encoding='utf-8').write(v)
    def run(d):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): judge_docs(d['fb'], d['fh'], d['cb'], d['ch'], t); timing(d['fb'], d['cb'], t)
        return t
    t0 = run(real); ok += not t0.fails; total += 1
    print('SELFTEST %s T0 positive control (the REAL blobs, fixtures c4_real_*.html): %d checked, fails %s' % ('OK' if not t0.fails else 'MISS', t0.n, t0.fails))
    def sub(s, a, b):
        assert s.count(a) == 1, 'tamper anchor must occur EXACTLY once (found %d): %r' % (s.count(a), a[:60]); return s.replace(a, b)
    F15 = K['flow_new_h2']; C78 = K['cheat_new_h2']
    arms = [
        ('flow an edit OUTSIDE the block (in 14.)', 'fh', lambda s: sub(s, '<h2>14. Both observability env examples', '<h2>14. Both  observability env examples'), ['D3']),
        ('flow 15. renumbered 16.', 'fh', lambda s: sub(s, F15, F15.replace('15.', '16.')), ['D3']),
        ('flow block placed AFTER 19. (ascending broken)', 'fh', lambda s: sub(sub(s, F15, '    <h2>X</h2>'), '  </body>', F15 + '\n  </body>'), ['D3']),
        ('flow close tag rewritten', 'fh', lambda s: sub(s, '\n  </body>', '\n</body>'), ['D3']),
        ('flow block drops UNMEASURED', 'fh', lambda s: s.replace('<strong>UNMEASURED</strong> here', '<strong>unknown</strong> here', 1), ['D5-flow']),
        ('cheat block not LAST (moved above KS-1005)', 'ch', lambda s: sub(sub(s, C78, '      <h2>gone</h2>'), '      <h2>change-password reads its own hash &mdash; KS-1005</h2>', C78 + '\n      <p>x</p>\n      <h2>change-password reads its own hash &mdash; KS-1005</h2>'), ['D4']),
        ('cheat an edit in the KS-1388 section', 'ch', lambda s: sub(s, '<h2>Observability nginx status port &mdash; KS-1388</h2>\n', '<h2>Observability nginx status port &mdash; KS-1388</h2>\n \n'), ['D4']),
        ('cheat KS-1278 h2 duplicated', 'ch', lambda s: sub(s, '      <h3>Running the cells</h3>\n      <pre><code>cd Blockchain/Dev\n', '      <h2>dup &mdash; KS-1278</h2>\n      <h3>Running the cells</h3>\n      <pre><code>cd Blockchain/Dev\n'), ['D4']),
        ('cheat block claims an ordering invariant', 'ch', lambda s: sub(s, '<code>Refs KS-1278</code>; the row-lock', 'Sections are in ascending KS order. <code>Refs KS-1278</code>; the row-lock'), ['D6']),
        ('cheat block drops the base sha', 'ch', lambda s: s.replace('<code>32e058975d4e</code>', '<code>base</code>'), ['D5-cheat']),
        ('base flow timing control blinded (auth renamed)', 'fb', lambda s: re.sub(r'auth', 'aXth', s, flags=re.I), ['D7']),
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


SIMENV = {'GIT_AUTHOR_NAME': 'SIM', 'GIT_AUTHOR_EMAIL': 'sim@invalid', 'GIT_COMMITTER_NAME': 'SIM', 'GIT_COMMITTER_EMAIL': 'sim@invalid',
          'GIT_AUTHOR_DATE': '2026-10-05T00:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-05T00:00:00Z'}


def sim_commit(repo, parents, edits, msg, base, out, tree=None):
    if tree is None:
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
    rc, c, e = wgit(repo, *args, env=SIMENV, input_bytes=msg.encode()); assert rc == 0, e
    return c.strip(), tree.strip()


def selftest_qm(repo):
    import io, contextlib
    if not outside_forbidden(repo):
        print('SELFTEST REFUSED scratch clone inside the forbidden root'); return 0, 1
    out = os.path.join(SCRATCH, 'sim'); os.makedirs(out, exist_ok=True)
    h, b, dv = K['head'], K['base'], K['develop_at_draft']; ok = total = 0
    g = lambda r, p: git(repo, 'show', '%s:%s' % (r, p))
    def q(*a, **k):
        with contextlib.redirect_stdout(io.StringIO()) as buf: r = predict(*a, **k)
        return r, buf.getvalue()
    def rep(cond, msg):
        nonlocal ok, total
        total += 1; ok += bool(cond); print('SELFTEST %s %s' % ('OK' if cond else 'MISS', msg))
    p0, _ = q(repo, b, out); rep(p0 == K['end_tree'], 'predict on D == base gives END_TREE: %s vs %s' % (str(p0)[:12], K['end_tree'][:12]))
    pr, _ = q(repo, dv, out); prt, _ = q(repo, dv, out, order='tail'); prs, _ = q(repo, dv, out, order='succ')
    rep(ok_tree(pr) and (prt != pr or prs != pr), 'the REAL develop %s: key %s | tail CONTROL %s | succ CONTROL %s (at least one differs)' % (dv[:12], str(pr)[:12], str(prt)[:12], str(prs)[:12]))
    # independent cross-check: git merge-tree auto-merges the CHEAT on the real develop (the flow conflicts): its cheat blob must equal ours
    rc, o, e = wgit(repo, 'merge-tree', '--write-tree', dv, h)
    mt = o.split('\n')[0].strip() if o else ''
    mcb = git(repo, 'rev-parse', '--verify', '--quiet', '%s:%s' % (mt, K['cheat']), check=False)[1].strip() if mt else ''
    pcb = git(repo, 'rev-parse', '%s:%s' % (pr, K['cheat'])).strip() if ok_tree(pr) else ''
    rep(mcb and mcb == pcb, 'cross-check: `git merge-tree --write-tree` rc %d (flow conflicts) — its CHEAT blob %s == the key prediction\'s %s' % (rc, mcb[:12], pcb[:12]))
    pflow = L(git(repo, 'show', '%s:%s' % (pr, K['flow']))) if ok_tree(pr) else []
    rep(pflow and nums(pflow) == sorted(nums(pflow)) and 15 in nums(pflow), 'predicted flow h2 numbers ascending with 15.: %s' % nums(pflow))
    # SIM post-#1388 develop: a squash-shaped commit with #1388's merge-in tree on top of the READY's develop (3cb9). #1388 then really
    # merged (12:24:04Z) as d784b613c81e with that same tree, so the SIM prediction must DIFFER from predict(3cb9) and EQUAL predict(real d784).
    c88 = K['contended_prs']['1388']; dr = K['develop_at_ready']
    if resolvable(repo, c88['merge_in']) and resolvable(repo, dr):
        D88, _ = sim_commit(repo, [dr], {}, 'SIM squash of #1388 merge-in %s\n' % c88['merge_in'][:12], None, out, tree=c88['merge_in_tree'])
        p88, _ = q(repo, D88, out); pr3, _ = q(repo, dr, out)
        same = git(repo, 'rev-parse', dv + '^{tree}').strip() == c88['merge_in_tree']
        rep(ok_tree(p88) and p88 != pr3 and (p88 == pr if same else True), 'SIM post-#1388 develop %s (tree %s on %s): predicted %s | differs from predict(%s) %s | == predict(real develop %s) %s (real develop tree == the SIM tree: %s)' % (
            D88[:12], c88['merge_in_tree'][:12], dr[:12], str(p88)[:12], dr[:12], str(pr3)[:12], dv[:12], str(pr)[:12], same))
    else:
        rep(False, 'SIM post-#1388: the merge-in %s or the READY develop %s is not in this clone (clone --shared the checkout, fetch both by sha)' % (c88['merge_in'][:12], dr[:12]))
    # SIM develop with a section appended AFTER KS-1005 in the cheat (a #1385-shaped landing): key puts KS-1278 ABOVE it, tail below
    ce = g(dv, K['cheat']); assert ce.count('\n' + CLOSE) == 1
    ce2 = ce.replace('\n' + CLOSE, '\n      <h2>SIM MFA &mdash; KS-938</h2>\n      <p>SIM</p>\n' + CLOSE)
    Dapp, _ = sim_commit(repo, [dv], {K['cheat']: ce2}, 'SIM develop: a cheat section appended after KS-1005\n', dv, out)
    pa, outa = q(repo, Dapp, out); pat, _ = q(repo, Dapp, out, order='tail')
    ca = L(git(repo, 'show', '%s:%s' % (pa, K['cheat']))) if ok_tree(pa) else []
    pos = [i for i, l in enumerate(ca) if l.rstrip().endswith('KS-1278</h2>')] + [i for i, l in enumerate(ca) if l.rstrip().endswith('KS-938</h2>')]
    rep(ok_tree(pa) and pat != pa and len(pos) == 2 and pos[0] < pos[1] and 'DIVERGENCE cheat' in outa, 'SIM appended-after-KS-1005 develop: key tree %s puts KS-1278 ABOVE KS-938 %s, DIVERGENCE printed %s; tail CONTROL %s differs' % (
        str(pa)[:12], pos, 'DIVERGENCE cheat' in outa, str(pat)[:12]))
    # refusals by name
    pu, outu = q(repo, 'f' * 40, out); rep(pu == 'UNRESOLVABLE' and 'develop unresolvable' in outu, 'predict REFUSES an absent develop BY NAME: %r' % outu.strip()[:110])
    rt = g(dv, K['route_file']) + '\n// SIM\n'
    Dcode, _ = sim_commit(repo, [dv], {K['route_file']: rt}, 'SIM develop touches documents.ts\n', dv, out)
    pc, outc = q(repo, Dcode, out); rep(pc is None and 'code path' in outc, 'predict REFUSES a develop that changed documents.ts: %r' % outc.strip()[:100])
    Dk, _ = sim_commit(repo, [dv], {K['cheat']: ce.replace('\n' + CLOSE, '\n' + K['cheat_new_h2'] + '\n' + CLOSE)}, 'SIM develop already carries KS-1278\n', dv, out)
    pk, outk = q(repo, Dk, out); rep(pk is None and 'ALREADY carries' in outk, 'predict REFUSES a develop already carrying KS-1278: %r' % outk.strip()[:100])
    fl = g(dv, K['flow']); a14 = [l for l in L(fl) if l.rstrip().endswith('(KS-1388)</h2>')]
    Dp, _ = sim_commit(repo, [dv], {K['flow']: fl.replace(a14[0], a14[0].replace('(KS-1388)', '(KS-13888)'))}, 'SIM develop loses the predecessor key\n', dv, out)
    pp, outp = q(repo, Dp, out); rep(pp is None and 'predecessor key' in outp, 'predict REFUSES a develop without the predecessor key KS-1388: %r' % outp.strip()[:100])
    # Q-M on SIM merge-ins over the REAL develop
    if not ok_tree(pr):
        rep(False, 'Q-M arms need a real-develop prediction'); return ok, total
    Mgood, _ = sim_commit(repo, [h, dv], {}, 'Merge develop into KS-1278: docs only\n', None, out, tree=pr)
    def runqm(M, D, pred):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): qm(repo, M, D, pred, t)
        return t
    t = runqm(Mgood, dv, pr); rep(not t.fails and t.n == 7, 'Q-M positive control (SIM merge-in at the predicted tree): fails %s' % t.fails)
    arms = []
    Mtail, _ = sim_commit(repo, [h, dv], {}, 'Merge\n', None, out, tree=prs if prs != pr else prt); arms.append(('block at the wrong place (control tree)', Mtail, dv, pr, ['M1']))
    M1p, _ = sim_commit(repo, [dv], {}, 'squash-shaped\n', None, out, tree=pr); arms.append(('single parent', M1p, dv, pr, ['M2']))
    Mx, _ = sim_commit(repo, [h, dv], {'README.md': 'SIM extra\n'}, 'Merge\n', pr, out); arms.append(('an extra non-kit path', Mx, dv, pr, ['M1', 'M3']))
    Mt, _ = sim_commit(repo, [h, dv], {}, 'Merge\n\nCo-Authored-By: X <x@invalid>\n', None, out, tree=pr); arms.append(('a Co-Authored-By trailer', Mt, dv, pr, ['M4']))
    Mb, _ = sim_commit(repo, [h, Dcode], {}, 'Merge\n', None, out, tree=pr); arms.append(("develop's advance touches documents.ts", Mb, Dcode, None, ['M1', 'M6']))
    Mi, _ = sim_commit(repo, [h], {}, 'SIM intermediate\n', None, out, tree=K['end_tree'])
    M2c, _ = sim_commit(repo, [Mi, dv], {}, 'Merge\n', None, out, tree=pr); arms.append(('two new commits', M2c, dv, pr, ['M2', 'M7']))
    Mb2, _ = sim_commit(repo, [h, b], {}, 'Merge\n', None, out, tree=K['end_tree']); arms.append(('D == base (no advance)', Mb2, b, K['end_tree'], ['M5']))
    for name, M, D, pred, want in arms:
        t = runqm(M, D, pred); c = set(want) <= set(t.fails)
        rep(c, 'Q-M %s: want FAIL %s | got %s' % (name, want, t.fails))
    t = Tally()
    with contextlib.redirect_stdout(io.StringIO()) as buf: r = qm(repo, 'e' * 40, dv, pr, t)
    rep(r == 'UNRESOLVABLE' and 'merge-in head unresolvable' in buf.getvalue(), 'qm REFUSES an absent merge-in head BY NAME: %r' % buf.getvalue().strip()[:100])
    print('SELFTEST NOTE real develop %s key %s tail %s succ %s; SIM merge-in %s (objects in %s only; no ref written)' % (dv[:12], str(pr)[:12], str(prt)[:12], str(prs)[:12], Mgood[:12], repo))
    return ok, total


if __name__ == '__main__':
    A = sys.argv[1:]
    if not A or '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    if '--selftest' in A: raise SystemExit(selftest(opt('--scratch-clone')))
    cmd = A[0]; repo = opt('--repo', K['checkout'])
    if cmd == 'docs':
        head = opt('--head', K['head'])
        for s in (head, K['base']):
            if not resolvable(repo, s): print('REFUSED: %s unresolvable in %s' % (s, repo)); raise SystemExit(2)
        t = Tally(); docs_repo(repo, head, t); raise SystemExit(t.end())
    if cmd == 'predict':
        tr = predict(repo, opt('--develop-after'), opt('--out', os.path.join(SCRATCH, 'sim')), opt('--order', 'key'))
        raise SystemExit(2 if tr in ('REFUSED', 'UNRESOLVABLE') else 0 if tr else 1)
    if cmd == 'qm':
        D = opt('--develop-after'); pred = opt('--predicted') or predict(repo, D, opt('--out', os.path.join(SCRATCH, 'sim')))
        if pred in ('REFUSED', 'UNRESOLVABLE'): raise SystemExit(2)
        t = Tally(); r = qm(repo, opt('--merge-in-head'), D, pred, t)
        raise SystemExit(2 if r == 'UNRESOLVABLE' else t.end())
    print(__doc__); raise SystemExit(2)
