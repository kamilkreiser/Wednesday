#!/usr/bin/env python3
r"""c4_docs_gate66.py — C4 DOCS + the NEWLINE-TOLERANT, KEY-ANCHORED second-merge-in predictor + Q-M for #1385 (KS-938), gate66.

WHY NEWLINE-TOLERANT: develop c5101866ef54 (#1390, KS-1408) reformatted BOTH platform-k docs and SPLITS `<h2>` across lines
(`<h2>` / `  13. A failed webhooks ... list` / `  (KS-1345)` / `</h2>`). Every earlier kit read h2s with a SAME-LINE regex
(`<h2[^>]*>(\d+)\.`, or `'<h2>' in line and line.endswith('(KS-n)</h2>')`) and silently UNDER-COUNTS on this develop. Here every h2
is read from the WHOLE TEXT with `<h2\b[^>]*>(.*?)</h2\s*>` (DOTALL): inner tags stripped, whitespace (incl. newlines) collapsed to one
space, then the number (`^(\d+)\.`) and the KS key (flow `\(KS-(\d+)\)$`, cheat `&mdash; KS-(\d+)$`) are read from the normalised text.
The reader REFUSES if the count of `<h2` opening tags differs from the count it parsed (an unclosed / malformed h2 is never skipped).

SECTION of a doc for a key = from the LINE where its `<h2` opens up to the line where the next `<h2` opens, or the `  </body>` line;
trailing blank / `<div class="section">` lines are handed to what follows (gate65's rule, unchanged). The PR's BLOCK at the head = the
gap after its predecessor's section + its own KS-938 section; head minus BLOCK must equal the head's develop parent (d784) BYTE FOR BYTE.

h2proof --repo <git dir> [--develop <D>]     READ verbs only. Per doc at the kit base (d784) and at D: h2 count (tolerant) vs
  old same-line regex count; then plants `<h2>\n      99. planted ... (KS-99999)\n    </h2>` before the close tag of D's doc and
  requires: tolerant reader HITS 99 / KS-99999, old regex MISSES 99. rc 0 only if both directions hold on both docs.
docs --repo <git dir> [--head <sha>]         READ verbs only. D1 skill blob · D2 per doc head minus the KS-938 BLOCK == base (d784) ·
  D3 flow: one new h2 == kit `20. ... (KS-938)`, predecessor 19. (KS-1005), numbered h2 ascending, close tag once · D4 cheat: one new
  h2 == kit, predecessor KS-1005, LAST · D5 each block names the test file + `3 failed | 2 passed (5)` + `5 passed (5)` + `845` ·
  INFO D6 the blob the blocks cite for users.ts (ea9f8da97a04 = the ORIGINAL base 46c3e20cfbd2, not d784's 68f402bb56f0)
predict --repo <OWN clone> --develop-after <D> [--order key|num|tail] [--out <dir>]    WRITE verbs (temp index) — refused in !CODING
  REFUSES BY NAME, rc 2: `develop unresolvable` / `head unresolvable` / `base unresolvable`. Content refusals rc 1: D changed a code /
  hook path since the base (re-gate) / D already carries KS-938 / the predecessor key is not exactly once in D / the PR's doc change
  is not ONE keyed block / the flow's ascending invariant breaks / the h2 reader refuses.
  TREE = D's tree, the 3 code paths at the HEAD's blobs, each doc = D's doc with the head's BLOCK inserted: `key` after the
  predecessor key's section (flow KS-1005 = 19., cheat KS-1005 — tonight's rule); `num` (flow only, cheat falls back to key) before the
  first numbered h2 above 20 else after the last numbered section; `tail` (CONTROL) just before the close tag.
mergetree --repo <OWN clone> --develop-after <D>   `git merge-tree --write-tree --name-only <head> <D>`: rc, tree, conflicted paths,
  per-doc key order of ITS blobs, compared with predict(key). Prints AGREE or DIVERGENCE (never picks).
qm --repo <clone> --merge-in-head <M> --develop-after <D> [--predicted <tree>]
  REFUSES BY NAME (rc 2), checked in this order: `develop unresolvable`, `head unresolvable`, `base unresolvable`,
  `merge-in head unresolvable` — gate63's defect (an absent develop read as None blobs -> a FALSE re-gate) cannot recur.
  M1 tree(M) == prediction (THE AUTHORITY) · M2 parents == [head, D] · M3 D..M names only the 5 kit paths, every code path at the head
  blob · M4 0 trailers (raw 1 byte), 0 Co-Authored-By · M5 base d784 ancestor of D, D != base · M6 base..D disjoint from the 3 code +
  2 hook paths, D carries no KS-938 h2 · M7 head..M not on D is exactly [M] · M8 KEY-ANCHORED docs at M (tolerant reader): key list ==
  D's with 938 right after 1005, every D keyed section byte-identical at M, M's KS-938 section == the head's, 0 conflict markers, flow
  numbered h2 ascending, `<div` opens == `</div>` closes per doc whenever develop's doc balances.
--selftest --scratch-clone <dir>   the h2 proof, docs arms on fixtures, predict / mergetree / qm arms on SIM commits (objects only).
rc 0 all PASS / rc 1 any FAIL, a content refusal, or 0 checked / rc 2 refused by name."""
import io, contextlib, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate66 import K, git, wgit, Tally, outside_forbidden, SCRATCH

CLOSE = K['close_tag']
OWN = K['own_key']
KRX = {'flow': re.compile(K['flow_key_rx']), 'cheat': re.compile(K['cheat_key_rx'])}
NUMRX = re.compile(K['num_rx'])
OLDRX = re.compile(K['old_sameline_rx'])
H2RX = re.compile(r'<h2\b[^>]*>(.*?)</h2\s*>', re.S | re.I)
OPENRX = re.compile(r'<h2\b', re.I)
PRED = {'flow': K['flow_pred_key'], 'cheat': K['cheat_pred_key']}
OWNH2 = {'flow': K['flow_own_h2'], 'cheat': K['cheat_own_h2']}
MARK = re.compile(r'^(<<<<<<<|=======|>>>>>>>)( |$)', re.M)


class Refused(Exception):
    pass


def L(s): return s.split('\n')


# ---------------- the NEWLINE-TOLERANT h2 reader ----------------

def headings(doc, text):
    """[{line (0-based, where `<h2` opens), end (line of `</h2>`), text (normalised), num, key}] in document order."""
    out = []
    for m in H2RX.finditer(text):
        inner = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(1))).strip()
        n = NUMRX.match(inner); k = KRX[doc].search(inner)
        out.append({'line': text.count('\n', 0, m.start()), 'end': text.count('\n', 0, m.end()), 'text': inner,
                    'num': int(n.group(1)) if n else None, 'key': k.group(1) if k else None})
    opened = len(OPENRX.findall(text))
    if opened != len(out):
        raise Refused('%s: h2 reader: %d `<h2` opening tag(s) but %d parsed h2 element(s) — a malformed / unclosed h2 is never skipped' % (doc, opened, len(out)))
    return out


def old_sameline_nums(text):
    return [int(m.group(1)) for l in L(text) for m in [OLDRX.search(l)] if m]


def nums(doc, text): return [h['num'] for h in headings(doc, text) if h['num'] is not None]
def keys(doc, text): return [h['key'] for h in headings(doc, text) if h['key'] is not None]
def divbal(text): return len(re.findall(r'<div\b', text)) - len(re.findall(r'</div>', text))
def ascending(xs): return xs == sorted(xs) and len(set(xs)) == len(xs)


def section(doc, text, key):
    hs = headings(doc, text); lines = L(text)
    hits = [i for i, h in enumerate(hs) if h['key'] == key]
    if len(hits) != 1:
        raise Refused('%s: key KS-%s found on %d h2 element(s) (want exactly 1)' % (doc, key, len(hits)))
    i = hits[0]; s = hs[i]['line']
    if i + 1 < len(hs):
        e = hs[i + 1]['line']
    else:
        c = [j for j, l in enumerate(lines) if l == CLOSE and j > s]
        if len(c) != 1: raise Refused('%s: close tag %r after KS-%s found %d time(s)' % (doc, CLOSE, key, len(c)))
        e = c[0]
    while e > s + 1 and lines[e - 1].strip() in ('', '<div class="section">'):
        e -= 1
    return s, e


def block(doc, htext):
    """(start, end, pred_key) of the PR's BLOCK in the head: the gap after the predecessor's section + the KS-938 section."""
    hs = headings(doc, htext)
    own = [i for i, h in enumerate(hs) if h['key'] == OWN]
    if len(own) != 1: raise Refused('%s: KS-%s on %d h2 at the head (want 1)' % (doc, OWN, len(own)))
    if own[0] == 0: raise Refused('%s: no h2 precedes KS-%s' % (doc, OWN))
    pk = hs[own[0] - 1]['key']
    if pk is None: raise Refused('%s: the h2 before KS-%s carries no KS key (%r): nothing to anchor on' % (doc, OWN, hs[own[0] - 1]['text'][:60]))
    ps, pe = section(doc, htext, pk); sh, eh = section(doc, htext, OWN)
    return pe, eh, pk


def resolve_doc(doc, dtext, btext, htext, order='key'):
    D, B, H = L(dtext), L(btext), L(htext)
    s, e, pk = block(doc, htext)
    if H[:s] + H[e:] != B:
        raise Refused('%s: the head changes something besides its one KS-%s block vs the base — not a pure keyed insertion' % (doc, OWN))
    if OWN in keys(doc, dtext):
        raise Refused('%s: develop ALREADY carries a KS-%s h2 (merged twice? re-gate)' % (doc, OWN))
    blk = H[s:e]
    if order == 'key' or (order == 'num' and doc == 'cheat'):
        try:
            ds, de = section(doc, dtext, pk)
        except Refused as x:
            raise Refused('%s: the predecessor key KS-%s is not exactly once in develop (%s): re-gate' % (doc, pk, x))
        at = de
    elif order == 'num':
        hs = headings(doc, dtext); own = K['flow_own_num']
        above = [h for h in hs if h['num'] is not None and h['num'] > own]
        if above:
            at = above[0]['line']
            while at > 0 and D[at - 1].strip() in ('', '<div class="section">'): at -= 1
        else:
            last = [h for h in hs if h['num'] is not None][-1]
            if last['key'] is None: raise Refused('flow: the last numbered h2 carries no key')
            at = section(doc, dtext, last['key'])[1]
    elif order == 'tail':
        c = [i for i, l in enumerate(D) if l == CLOSE]
        if len(c) != 1: raise Refused('%s: close tag count %d' % (doc, len(c)))
        at = c[0]
    else:
        raise Refused('unknown order %r' % order)
    N = '\n'.join(D[:at] + blk + D[at:])
    if doc == 'flow' and order in ('key', 'num') and not ascending(nums(doc, N)):
        raise Refused('flow: the %s result breaks the ascending invariant %s — re-gate' % (order, nums(doc, N)))
    return N


def resolvable(repo, sha):
    return bool(sha) and git(repo, 'rev-parse', '--verify', '--quiet', sha + '^{commit}', check=False)[0] == 0


def unresolved(repo, pairs):
    for name, s in pairs:
        if not resolvable(repo, s):
            return '%s unresolvable: %r is not a commit in %s — fetch it BY SHA into YOUR clone, then re-run' % (name, s, repo)
    return None


def predict(repo, D, out, order='key', head=None, quiet=False):
    head = head or K['head']; base = K['base']
    if not outside_forbidden(repo):
        print('REFUSED: predict writes objects; %s is inside %s — use your OWN scratch clone' % (repo, K['forbidden_root'])); return 'REFUSED'
    u = unresolved(repo, (('develop', D), ('head', head), ('base', base)))
    if u:
        print('PREDICT REFUSED: ' + u); return 'UNRESOLVABLE'
    adv = set(git(repo, 'diff', '--name-only', base, D).splitlines()); hit = sorted(adv & (set(K['code_paths']) | set(K['hook_blobs'])))
    if hit:
        print('PREDICT REFUSED: develop-after changed code / hook path(s) %s since the base (M6 fails: re-gate)' % hit); return None
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
        meta = git(repo, 'ls-tree', head, '--', p).split('\t')[0].split()
        rc, o, e = wgit(repo, 'update-index', '--add', '--cacheinfo', '%s,%s,%s' % (meta[0], meta[2], p), env=env); assert rc == 0, e
    rc, tree, e = wgit(repo, 'write-tree', env=env); assert rc == 0, e
    q = os.path.join(out, '_quarantine'); os.makedirs(q, exist_ok=True)
    shutil.move(idx, os.path.join(q, os.path.basename(idx) + '.' + tree.strip()[:8]))   # quarantine, never rm
    tree = tree.strip()
    if not quiet: print('PREDICTED %s (order %s, develop-after %s)' % (tree, order, D[:12]))
    return tree


def ok_tree(x): return x not in (None, 'REFUSED', 'UNRESOLVABLE')


def doc_report(repo, tree, label):
    """per-doc h2 key order + numbers + markers of a tree, tolerant reader."""
    rows = []
    for doc in ('flow', 'cheat'):
        rc, txt, e = git(repo, 'show', '%s:%s' % (tree, K[doc]), check=False)
        if rc: rows.append('  %s %s: ABSENT' % (label, doc)); continue
        try:
            hs = headings(doc, txt)
            ks = ['KS-%s' % h['key'] for h in hs if h['key']]; ns = [h['num'] for h in hs if h['num'] is not None]
            rows.append('  %s %s blob %s: %d h2 | key order %s | numbers %s | conflict markers %d | div open-close %+d' % (
                label, doc, git(repo, 'rev-parse', '%s:%s' % (tree, K[doc])).strip()[:12], len(hs), ' '.join(ks), ns if doc == 'flow' else '-', len(MARK.findall(txt)), divbal(txt)))
        except Refused as x:
            rows.append('  %s %s: READER REFUSED %s (conflict markers %d)' % (label, doc, x, len(MARK.findall(txt))))
    return rows


def mergetree(repo, D, out, head=None):
    head = head or K['head']
    if not outside_forbidden(repo):
        print('REFUSED: merge-tree writes objects; use your OWN scratch clone'); return 2
    u = unresolved(repo, (('develop', D), ('head', head)))
    if u: print('MERGETREE REFUSED: ' + u); return 2
    rc, o, e = wgit(repo, 'merge-tree', '--write-tree', '--name-only', head, D)
    parts = o.split('\n\n', 1); first = parts[0].split('\n'); mt = first[0].strip(); conflicted = [x for x in first[1:] if x]
    msgs = [x for x in (parts[1] if len(parts) > 1 else '').split('\n') if x]
    print('GIT MERGE-TREE `merge-tree --write-tree --name-only %s %s` rc %d tree %s' % (head[:12], D[:12], rc, mt))
    print('  conflicted paths (%d): %s' % (len(conflicted), conflicted))
    for m in msgs: print('  | ' + m[:200])
    pk = predict(repo, D, out, 'key', head, quiet=True); pn = predict(repo, D, out, 'num', head, quiet=True)
    print('KEY-ANCHORED (tonight\'s rule) tree %s | flow-NUMBERING reading tree %s | key == num: %s' % (pk, pn, pk == pn))
    for r in doc_report(repo, mt, 'merge-tree'): print(r)
    if ok_tree(pk):
        for r in doc_report(repo, pk, 'key-anchored'): print(r)
        for doc in ('flow', 'cheat'):
            a = git(repo, 'rev-parse', '--verify', '--quiet', '%s:%s' % (mt, K[doc]), check=False)[1].strip()
            b = git(repo, 'rev-parse', '%s:%s' % (pk, K[doc])).strip()
            print('  %s blob: merge-tree %s vs key-anchored %s -> %s%s' % (doc, a[:12], b[:12], 'SAME' if a == b else 'DIFFERENT',
                  ' (git CONFLICTED this doc: it has no resolved blob to compare)' if K[doc] in conflicted else ''))
        oth = sorted(set(git(repo, 'diff', '--name-only', mt, pk).splitlines()))
        print('  paths differing merge-tree vs key-anchored: %s' % oth)
        # a THIRD reading, for the record: a hand resolution of git's conflict = THEIRS hunk + OURS hunk from the KS-938 section on
        for doc in ('flow', 'cheat'):
            if K[doc] not in conflicted: continue
            m = L(git(repo, 'show', '%s:%s' % (mt, K[doc])))
            a = [i for i, l in enumerate(m) if l.startswith('<<<<<<< ')]; b = [i for i, l in enumerate(m) if l == '=======']; c = [i for i, l in enumerate(m) if l.startswith('>>>>>>> ')]
            if not (len(a) == len(b) == len(c) == 1):
                print('  HAND-RESOLUTION reading of %s: %d conflict region(s) — not computed (needs exactly 1)' % (doc, len(a))); continue
            ours, theirs = m[a[0] + 1:b[0]], m[b[0] + 1:c[0]]
            oi = [i for i, l in enumerate(ours) if '<h2' in l and ('KS-%s' % OWN) in ''.join(ours[i:i + 4])]
            if not oi: print('  HAND-RESOLUTION reading of %s: KS-%s not in the OURS hunk' % (doc, OWN)); continue
            s = oi[0] - 1 if oi[0] > 0 and ours[oi[0] - 1].strip() == '<div class="section">' else oi[0]
            hand = '\n'.join(m[:a[0]] + theirs + ours[s:] + m[c[0] + 1:])
            idx = os.path.join(out, 'hand.index.%d' % os.getpid()); env = {'GIT_INDEX_FILE': idx}
            assert wgit(repo, 'read-tree', pk, env=env)[0] == 0
            rc2, hb, e = wgit(repo, 'hash-object', '-w', '--stdin', input_bytes=hand.encode('utf-8')); assert rc2 == 0, e
            assert wgit(repo, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (hb.strip(), K[doc]), env=env)[0] == 0
            rc2, ht, e = wgit(repo, 'write-tree', env=env); assert rc2 == 0, e
            q = os.path.join(out, '_quarantine'); os.makedirs(q, exist_ok=True); shutil.move(idx, os.path.join(q, os.path.basename(idx) + '.' + ht.strip()[:8]))
            import difflib
            d = [x for x in difflib.unified_diff(L(git(repo, 'show', '%s:%s' % (pk, K[doc]))), L(hand), lineterm='', n=0) if x[:1] in '+-' and x[:3] not in ('+++', '---')]
            print('  HAND-RESOLUTION reading of %s (THEIRS hunk + OURS hunk from the KS-%s section on, git\'s trailing context kept): blob %s tree %s -> %s the key-anchored tree; line diff vs key: %s' % (
                doc, OWN, hb.strip()[:12], ht.strip(), 'EQUALS' if ht.strip() == pk else 'DIFFERS from', d[:4]))
            for r in doc_report(repo, ht.strip(), 'hand-resolution'):
                if doc in r.split(' blob ')[0]: print(r)
    verdict = 'AGREE' if ok_tree(pk) and mt == pk and rc == 0 else 'DIVERGENCE'
    print('%s: merge-tree %s (rc %d) vs key-anchored %s%s' % (verdict, mt[:12], rc, str(pk)[:12], '' if verdict == 'AGREE' else ' — Wednesday rules; this kit does not pick'))
    return 0 if verdict == 'AGREE' else 1


# ---------------- qm ----------------

def doc_expect_ok(repo, M, D, head, doc):
    tm = git(repo, 'show', '%s:%s' % (M, K[doc])); td = git(repo, 'show', '%s:%s' % (D, K[doc])); th = git(repo, 'show', '%s:%s' % (head, K[doc]))
    why = []
    if MARK.search(tm): why.append('conflict markers %d' % len(MARK.findall(tm)))
    try:
        km, kd = keys(doc, tm), keys(doc, td)
        p = PRED[doc]
        want = kd[:kd.index(p) + 1] + [OWN] + kd[kd.index(p) + 1:] if p in kd else None
        if km != want: why.append('key order %s != want %s' % (km, want))
        for k in kd:
            sm, em = section(doc, tm, k); sd, ed = section(doc, td, k)
            if L(tm)[sm:em] != L(td)[sd:ed]: why.append('KS-%s section differs from develop' % k)
        sm, em = section(doc, tm, OWN); sh, eh = section(doc, th, OWN)
        if L(tm)[sm:em] != L(th)[sh:eh]: why.append('KS-%s section differs from the head' % OWN)
        if doc == 'flow' and not ascending(nums(doc, tm)): why.append('flow numbers not ascending %s' % nums(doc, tm))
        if divbal(td) == 0 and divbal(tm) != 0: why.append('div balance %+d (develop balanced)' % divbal(tm))
    except (Refused, ValueError) as x:
        why.append('reader: %s' % x)
    return why


def qm(repo, M, D, pred, t, head=None):
    head = head or K['head']; base = K['base']
    u = unresolved(repo, (('develop', D), ('head', head), ('base', base), ('merge-in head', M)))
    if u:
        print('QM REFUSED: ' + u); return 'UNRESOLVABLE'
    # full 40-hex for every comparison (ex1 of the CLI arm false-failed M7 on an abbreviated M)
    M = git(repo, 'rev-parse', M + '^{commit}').strip(); D = git(repo, 'rev-parse', D + '^{commit}').strip()
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
    adv = git(repo, 'diff', '--name-only', base, D).splitlines(); hit = sorted(set(adv) & (set(K['code_paths']) | set(K['hook_blobs'])))
    carries = []
    for doc in ('flow', 'cheat'):
        try:
            if OWN in keys(doc, git(repo, 'show', '%s:%s' % (D, K[doc]))): carries.append(doc)
        except Refused as x:
            carries.append('%s (reader refused: %s)' % (doc, x))
    t.check('M6', not hit and not carries, "develop's advance %d path(s); code / hook paths among them %s; D carries KS-%s in %s" % (len(adv), hit, OWN, carries))
    new = git(repo, 'rev-list', '%s..%s' % (head, M), '^' + D).split()
    t.check('M7', new == [M], 'commits in head..M not on D: %s (want exactly [M])' % [c[:12] for c in new])
    res = {doc: doc_expect_ok(repo, M, D, head, doc) for doc in ('flow', 'cheat')}
    t.check('M8', not res['flow'] and not res['cheat'], 'KEY-ANCHORED docs at M (newline-tolerant): flow %s | cheat %s' % (res['flow'] or 'OK', res['cheat'] or 'OK'))


# ---------------- docs + h2proof ----------------

def plant(text):
    assert text.count('\n' + CLOSE + '\n') == 1, 'close tag must occur exactly once'
    return text.replace('\n' + CLOSE + '\n', '\n    <h2>\n      99. planted split heading for the reader proof (KS-99999)\n    </h2>\n' + CLOSE + '\n')


def h2proof(repo, D, t):
    for doc in ('flow', 'cheat'):
        rows = []
        for label, rev in (('base d784', K['base']), ('develop', D)):
            txt = git(repo, 'show', '%s:%s' % (rev, K[doc]))
            hs = headings(doc, txt)
            split = sum(1 for h in hs if h['end'] != h['line'])
            okey = re.compile(r'\(KS-\d+\)</h2>$' if doc == 'flow' else r'&mdash; KS-\d+</h2>$')
            oldk = sum(1 for l in L(txt) if '<h2>' in l and okey.search(l.rstrip()))
            rows.append('%s %s: tolerant %d h2 (%d split across lines, %d numbered, %d keyed) | old same-line regex %d numbered, old same-line key finder %d keyed' % (
                label, rev[:12], len(hs), split, len([h for h in hs if h['num'] is not None]), len([h for h in hs if h['key']]), len(old_sameline_nums(txt)), oldk))
        print('INFO H2COUNT-%s %s' % (doc, ' || '.join(rows)))
        txt = git(repo, 'show', '%s:%s' % (D, K[doc])); p = plant(txt)
        hs = headings(doc, p)
        hit = any(h['num'] == 99 and h['key'] == '99999' for h in hs) if doc == 'flow' else any(h['num'] == 99 for h in hs)
        miss = 99 not in old_sameline_nums(p)
        t.check('H2-HIT-' + doc, hit, 'tolerant reader on develop %s %s + planted `<h2>\\n      99. ... (KS-99999)\\n    </h2>`: HIT %s (parsed %d h2, was %d)' % (D[:12], doc, hit, len(hs), len(headings(doc, txt))))
        t.check('H2-OLDMISS-' + doc, miss, 'old same-line regex %r on the same planted text: MISSES 99 %s (it reads %d numbered h2, tolerant reads %d)' % (
            K['old_sameline_rx'], miss, len(old_sameline_nums(p)), len([h for h in hs if h['num'] is not None])))


def judge_docs(fb, fh, cb, ch, t, skill=None):
    if skill is not None:
        t.check('D1', skill[0] == K['skill_blob'] and K['flow'] in skill[1] and K['cheat'] in skill[1], 'SKILL.md blob %s (want %s); names both docs' % (skill[0][:12], K['skill_blob'][:12]))
    out = {}
    for doc, b, h, cid in (('flow', fb, fh, 'D3'), ('cheat', cb, ch, 'D4')):
        B, H = L(b), L(h)
        try:
            s, e, pk = block(doc, h); hs = headings(doc, h); hb = headings(doc, b)
        except Refused as x:
            t.check('D2-' + doc, False, str(x)); t.check(cid, False, str(x)); out[doc] = ''; continue
        t.check('D2-' + doc, H[:s] + H[e:] == B, '%s: head minus the KS-%s BLOCK (head :%d-:%d) == base d784 byte for byte' % (doc, OWN, s + 1, e))
        new = [x['text'] for x in hs if x['text'] not in [y['text'] for y in hb]]
        cl = (B.count(CLOSE), H.count(CLOSE))
        if doc == 'flow':
            ok = new == [OWNH2[doc]] and pk == PRED[doc] and ascending(nums(doc, h)) and cl == (1, 1)
            t.check(cid, ok, 'flow: new h2 %s | predecessor KS-%s (want %s) | numbered ascending %s %s | close tag %s' % ([x[:50] for x in new], pk, PRED[doc], ascending(nums(doc, h)), nums(doc, h), cl))
        else:
            last = hs[-1]['key'] == OWN
            ok = new == [OWNH2[doc]] and pk == PRED[doc] and last and cl == (1, 1)
            t.check(cid, ok, 'cheat: new h2 %s | predecessor KS-%s (want %s) | KS-%s LAST %s | close tag %s' % ([x[:50] for x in new], pk, PRED[doc], OWN, last, cl))
        out[doc] = '\n'.join(H[s:e])
    for doc in ('flow', 'cheat'):
        txt = out.get(doc, ''); flat = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', txt))
        need = {'test file': 'ks938-mfa-disable-nulls-seed-and-backup-codes.test.ts' in txt, 'red 3 failed | 2 passed (5)': '3 failed | 2 passed (5)' in flat,
                'green 5 passed (5)': '5 passed (5)' in flat, 'suite 845': '845' in flat}
        miss = [k for k, v in need.items() if not v]
        t.check('D5-' + doc, bool(txt) and not miss, '%s block (%d chars) missing %s' % (doc, len(txt), miss))
        t.info('D6-' + doc, 'blobs cited: users.ts ea9f8da97a04 (ORIGINAL base 46c3) %s / 68f402bb56f0 (d784) %s; mfa.ts 87d3ee1079fe %s' % (
            'ea9f8da97a04' in txt, '68f402bb56f0' in txt, '87d3ee1079fe' in txt))


def docs_repo(repo, head, t):
    b = K['base']; g = lambda r, p: git(repo, 'show', '%s:%s' % (r, p))
    sb = git(repo, 'rev-parse', '%s:%s' % (b, K['skill'])).strip()
    judge_docs(g(b, K['flow']), g(head, K['flow']), g(b, K['cheat']), g(head, K['cheat']), t, skill=(sb, g(b, K['skill'])))


# ---------------- self-test ----------------

SIMENV = {'GIT_AUTHOR_NAME': 'SIM', 'GIT_AUTHOR_EMAIL': 'sim@invalid', 'GIT_COMMITTER_NAME': 'SIM', 'GIT_COMMITTER_EMAIL': 'sim@invalid',
          'GIT_AUTHOR_DATE': '2026-10-06T00:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-06T00:00:00Z'}


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


def selftest(scratch):
    if not scratch or not outside_forbidden(scratch):
        print('SELFTEST REFUSED: --scratch-clone <your OWN clone outside %s> is required' % K['forbidden_root']); return 2
    R = scratch; ok = total = 0
    def rep(cond, msg):
        nonlocal ok, total
        total += 1; ok += bool(cond); print('SELFTEST %s %s' % ('OK' if cond else 'MISS', msg))
    u = unresolved(R, (('develop', K['develop_at_draft']), ('head', K['head']), ('base', K['base'])))
    if u: print('SELFTEST REFUSED: ' + u); return 2
    # 1. the h2 proof on the real docs
    t = Tally()
    with contextlib.redirect_stdout(io.StringIO()) as buf: h2proof(R, K['develop_at_draft'], t)
    rep(not t.fails and t.n == 4, 'h2 proof on develop %s: %d checks, fails %s' % (K['develop_at_draft'][:12], t.n, t.fails))
    for line in buf.getvalue().splitlines(): print('    ' + line[:260])
    # reader refuses an unclosed h2
    try:
        headings('flow', '<h2>1. a (KS-1)</h2>\n<h2>2. never closed\n'); rep(False, 'reader refuses an unclosed h2')
    except Refused as x:
        rep('opening tag' in str(x), 'reader REFUSES an unclosed h2: %s' % x)
    # 2. docs on the real head + arms
    g = lambda r, p: git(R, 'show', '%s:%s' % (r, p))
    real = {'fb': g(K['base'], K['flow']), 'fh': g(K['head'], K['flow']), 'cb': g(K['base'], K['cheat']), 'ch': g(K['head'], K['cheat'])}
    def run(d):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): judge_docs(d['fb'], d['fh'], d['cb'], d['ch'], t)
        return t
    t0 = run(real); rep(not t0.fails, 'docs positive control (real base d784 / head blobs): %d checked, fails %s' % (t0.n, t0.fails))
    def sub(s, a, b):
        assert s.count(a) == 1, 'tamper anchor must occur EXACTLY once (found %d): %r' % (s.count(a), a[:60]); return s.replace(a, b)
    F20 = '<h2>' + K['flow_own_h2'] + '</h2>'; C38 = '<h2>' + K['cheat_own_h2'] + '</h2>'
    arms = [
        ('flow an edit OUTSIDE the block (in 19.)', 'fh', lambda s: sub(s, '<h2>19. change-password reads', '<h2>19. change-password  reads'), ['D2-flow']),
        ('flow 20. renumbered 17. (ascending broken)', 'fh', lambda s: sub(s, F20, F20.replace('>20.', '>17.')), ['D3']),
        ('flow own h2 SPLIT across lines (reader must still find it)', 'fh', lambda s: sub(s, F20, '<h2>\n      ' + K['flow_own_h2'] + '\n    </h2>'), []),
        ('cheat KS-938 h2 duplicated', 'ch', lambda s: s.replace('      <h3>Running the cells</h3>\n      <pre><code>cd Blockchain/Dev/services/auth\nnpx vitest run src/__tests__/ks938', '      <h2>dup &mdash; KS-938</h2>\n      <h3>Running the cells</h3>\n      <pre><code>cd Blockchain/Dev/services/auth\nnpx vitest run src/__tests__/ks938', 1), ['D4']),
        ('cheat block drops the red-first figure', 'ch', lambda s: s.replace('3 failed | 2 passed (5)', '3 red / 2 green'), ['D5-cheat']),
    ]
    for name, key, fn, want in arms:
        d = dict(real); d[key] = fn(d[key]); assert d[key] != real[key], 'tamper did not land: ' + name
        t = run(d); new = set(t.fails) - set(t0.fails)
        good = (set(want) <= new) if want else not new
        rep(good, 'docs arm %s: want NEW FAIL %s | got %s' % (name, want or 'NONE (must-NOT-fire arm)', sorted(new)))
    # 3. predict / mergetree / qm on SIM commits
    out = os.path.join(SCRATCH, 'sim'); os.makedirs(out, exist_ok=True)
    h, b, dv = K['head'], K['base'], K['develop_at_draft']
    def q(*a, **k):
        with contextlib.redirect_stdout(io.StringIO()) as buf: r = predict(*a, **k)
        return r, buf.getvalue()
    p0, _ = q(R, b, out); rep(p0 == K['end_tree'], 'predict on D == base d784 reproduces END_TREE: %s vs %s' % (str(p0)[:12], K['end_tree'][:12]))
    pk, _ = q(R, dv, out); pn, _ = q(R, dv, out, order='num'); pt, _ = q(R, dv, out, order='tail')
    rep(ok_tree(pk), 'predict(key) on the REAL develop %s: %s' % (dv[:12], pk))
    rep(pk == pn, 'flow-NUMBERING reading == KEY reading on the real develop: %s vs %s' % (str(pn)[:12], str(pk)[:12]))
    print('SELFTEST NOTE tail CONTROL on the real develop %s (%s the key tree — KS-1005 is the last section in both docs, so the tail coincides)' % (str(pt)[:12], 'EQUALS' if pt == pk else 'DIFFERS from'))
    # SIM develop where a section follows KS-1005 in both docs: key / num / tail must separate
    fl = g(dv, K['flow']); ce = g(dv, K['cheat'])
    fl2 = fl.replace('\n' + CLOSE + '\n', '\n    <div class="section">\n    <h2>\n      21. SIM later section\n      (KS-77777)\n    </h2>\n    <p>SIM</p>\n    </div>\n' + CLOSE + '\n')
    ce2 = ce.replace('\n' + CLOSE + '\n', '\n    <h2>\n      SIM later &mdash; KS-77777\n    </h2>\n    <p>SIM</p>\n' + CLOSE + '\n')
    Dl, _ = sim_commit(R, [dv], {K['flow']: fl2, K['cheat']: ce2}, 'SIM develop: a SPLIT-h2 section after KS-1005 in both docs\n', dv, out)
    a, _ = q(R, Dl, out); an, _ = q(R, Dl, out, order='num'); at_, _ = q(R, Dl, out, order='tail')
    ka = keys('cheat', git(R, 'show', '%s:%s' % (a, K['cheat']))) if ok_tree(a) else []
    rep(ok_tree(a) and at_ != a and ka[-2:] == [OWN, '77777'], 'SIM develop with a split-h2 KS-77777 after KS-1005: key tree %s puts KS-938 ABOVE it %s; tail CONTROL %s differs' % (str(a)[:12], ka[-3:], str(at_)[:12]))
    rep(ok_tree(an) and an == a, 'SIM: flow-numbering (20 < 21) agrees with key: %s' % str(an)[:12])
    # refusals by name / content
    pu, ou = q(R, 'f' * 40, out); rep(pu == 'UNRESOLVABLE' and 'develop unresolvable' in ou, 'predict REFUSES an absent develop BY NAME: %r' % ou.strip()[:120])
    Dc, _ = sim_commit(R, [dv], {K['users_file']: g(dv, K['users_file']) + '\n// SIM\n'}, 'SIM develop touches users.ts\n', dv, out)
    pc, oc = q(R, Dc, out); rep(pc is None and 'code / hook path' in oc, 'predict REFUSES a develop that changed users.ts: %r' % oc.strip()[:110])
    Dk, _ = sim_commit(R, [dv], {K['cheat']: ce.replace('\n' + CLOSE + '\n', '\n    <h2>\n      already &mdash; KS-938\n    </h2>\n' + CLOSE + '\n')}, 'SIM develop already carries KS-938 (split h2)\n', dv, out)
    pq, oq = q(R, Dk, out); rep(pq is None and 'ALREADY carries' in oq, 'predict REFUSES a develop already carrying a SPLIT KS-938 h2: %r' % oq.strip()[:110])
    Dp, _ = sim_commit(R, [dv], {K['cheat']: ce.replace('&mdash; KS-1005</h2>', '&mdash; KS-10050</h2>', 1)}, 'SIM develop loses KS-1005\n', dv, out)
    pp, op = q(R, Dp, out); rep(pp is None and 'predecessor key' in op, 'predict REFUSES a develop without the predecessor KS-1005: %r' % op.strip()[:110])
    # mergetree runs and prints a verdict
    with contextlib.redirect_stdout(io.StringIO()) as buf: mrc = mergetree(R, dv, out)
    mo = buf.getvalue(); rep(('DIVERGENCE' in mo or 'AGREE' in mo) and 'GIT MERGE-TREE' in mo, 'mergetree on the real develop prints a verdict (%s)' % ('AGREE' if mrc == 0 else 'DIVERGENCE'))
    # qm
    if not ok_tree(pk):
        rep(False, 'qm arms need a real-develop prediction'); return 1
    def runqm(M, D, pred, repo=R):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()) as buf: r = qm(repo, M, D, pred, t)
        return t, r, buf.getvalue()
    Mgood, _ = sim_commit(R, [h, dv], {}, 'Merge develop (c5101866ef54) into the KS-938 branch — docs-only\n', None, out, tree=pk)
    t, r, _ = runqm(Mgood, dv, pk); rep(r is None and not t.fails and t.n == 8, 'Q-M GOOD SIM (merge-in at the predicted tree): %d checked, fails %s' % (t.n, t.fails))
    # wrong order: KS-938 cheat section placed ABOVE KS-1005 (the old same-line-anchored error shape)
    pc_ = git(R, 'show', '%s:%s' % (pk, K['cheat'])); s38, e38 = section('cheat', pc_, OWN); s05, e05 = section('cheat', pc_, '1005')
    LL = L(pc_); wrong = '\n'.join(LL[:s05] + LL[s38:e38] + LL[s05:s38] + LL[e38:])
    Mw, _ = sim_commit(R, [h, dv], {K['cheat']: wrong}, 'Merge\n', pk, out)
    t, r, _ = runqm(Mw, dv, pk); rep({'M1', 'M8'} <= set(t.fails), 'Q-M WRONG-ORDER SIM (cheat KS-938 above KS-1005): want FAIL M1 (+M8) | got %s' % t.fails)
    # the HAND-RESOLUTION reading (THEIRS hunk + OURS from KS-938 on, git's trailing `</div>` context kept): same key order, one div unclosed
    with contextlib.redirect_stdout(io.StringIO()) as buf: mergetree(R, dv, out)
    hm = re.search(r'HAND-RESOLUTION reading of cheat .*? tree ([0-9a-f]{40})', buf.getvalue())
    if hm:
        Mh, _ = sim_commit(R, [h, dv], {}, 'Merge\n', None, out, tree=hm.group(1))
        t, r, _ = runqm(Mh, dv, pk); rep({'M1', 'M8'} <= set(t.fails), 'Q-M HAND-RESOLUTION SIM (key order right, one `</div>` short): want FAIL M1 M8 | got %s' % t.fails)
    else:
        rep(False, 'Q-M HAND-RESOLUTION SIM: mergetree printed no hand-resolution tree')
    # git-conflict tree committed as M (markers in the cheat)
    mt = wgit(R, 'merge-tree', '--write-tree', h, dv)[1].split('\n')[0].strip()
    Mc, _ = sim_commit(R, [h, dv], {}, 'Merge\n', None, out, tree=mt)
    t, r, _ = runqm(Mc, dv, pk); rep({'M1', 'M8'} <= set(t.fails), 'Q-M CONFLICT-MARKERS SIM (git merge-tree tree committed as is): want FAIL M1 M8 | got %s' % t.fails)
    Mt, _ = sim_commit(R, [h, dv], {}, 'Merge\n\nCo-Authored-By: X <x@invalid>\n', None, out, tree=pk)
    t, r, _ = runqm(Mt, dv, pk); rep(t.fails == ['M4'], 'Q-M TRAILER SIM (Co-Authored-By): want FAIL exactly [M4] | got %s' % t.fails)
    Mt2, _ = sim_commit(R, [h, dv], {}, 'Merge\n\nSigned-off-by: X <x@invalid>\n', None, out, tree=pk)
    t, r, _ = runqm(Mt2, dv, pk); rep(t.fails == ['M4'], 'Q-M TRAILER SIM (Signed-off-by, raw trailers > 1 byte): want FAIL exactly [M4] | got %s' % t.fails)
    M1p, _ = sim_commit(R, [dv], {}, 'squash-shaped\n', None, out, tree=pk)
    t, r, _ = runqm(M1p, dv, pk); rep('M2' in t.fails, 'Q-M single parent: want FAIL M2 | got %s' % t.fails)
    Mx, _ = sim_commit(R, [h, dv], {'README.md': 'SIM extra\n'}, 'Merge\n', pk, out)
    t, r, _ = runqm(Mx, dv, pk); rep({'M1', 'M3'} <= set(t.fails), 'Q-M extra non-kit path: want FAIL M1 M3 | got %s' % t.fails)
    Mi, _ = sim_commit(R, [h], {}, 'SIM intermediate\n', None, out, tree=K['end_tree'])
    M2c, _ = sim_commit(R, [Mi, dv], {}, 'Merge\n', None, out, tree=pk)
    t, r, _ = runqm(M2c, dv, pk); rep({'M2', 'M7'} <= set(t.fails), 'Q-M two new commits: want FAIL M2 M7 | got %s' % t.fails)
    # absent develop: (a) fabricated sha in the clone, (b) the REAL develop in a repo that lacks it (the shared checkout, read verbs only)
    t, r, o = runqm(Mgood, 'f' * 40, pk); rep(r == 'UNRESOLVABLE' and 'develop unresolvable' in o and t.n == 0, 'qm REFUSES an absent develop BY NAME (0 checks run, no false re-gate): %r' % o.strip()[:120])
    if not resolvable(K['checkout'], dv):
        t, r, o = runqm(K['head'], dv, pk, repo=K['checkout'])
        rep(r == 'UNRESOLVABLE' and 'develop unresolvable' in o and t.n == 0, 'qm on the SHARED CHECKOUT, where develop %s is genuinely absent: refuses BY NAME: %r' % (dv[:12], o.strip()[:120]))
    else:
        print('SELFTEST NOTE the shared checkout now holds develop %s: the genuinely-absent arm is not available' % dv[:12])
    t, r, o = runqm('e' * 40, dv, pk); rep(r == 'UNRESOLVABLE' and 'merge-in head unresolvable' in o, 'qm REFUSES an absent merge-in head BY NAME: %r' % o.strip()[:110])
    print('SELFTEST NOTE real develop %s: key %s num %s tail %s; GOOD SIM M %s (objects in %s only; no ref written)' % (dv[:12], str(pk)[:12], str(pn)[:12], str(pt)[:12], Mgood[:12], R))
    print('SELFTEST %s %d of %d' % ('OK' if ok == total else 'BROKEN', ok, total)); print('CHECKED %d arm(s)' % total)
    return 0 if ok == total else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if not A or '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    if '--selftest' in A: raise SystemExit(selftest(opt('--scratch-clone')))
    cmd = A[0]; repo = opt('--repo', K['checkout']); out = opt('--out', os.path.join(SCRATCH, 'sim'))
    if cmd == 'h2proof':
        D = opt('--develop', K['develop_at_draft']); u = unresolved(repo, (('develop', D), ('base', K['base'])))
        if u: print('REFUSED: ' + u); raise SystemExit(2)
        t = Tally(); h2proof(repo, D, t); raise SystemExit(t.end())
    if cmd == 'docs':
        head = opt('--head', K['head']); u = unresolved(repo, (('head', head), ('base', K['base'])))
        if u: print('REFUSED: ' + u); raise SystemExit(2)
        t = Tally(); docs_repo(repo, head, t); raise SystemExit(t.end())
    if cmd == 'predict':
        tr = predict(repo, opt('--develop-after'), out, opt('--order', 'key'))
        raise SystemExit(2 if tr in ('REFUSED', 'UNRESOLVABLE') else 0 if tr else 1)
    if cmd == 'mergetree':
        raise SystemExit(mergetree(repo, opt('--develop-after'), out))
    if cmd == 'qm':
        D = opt('--develop-after'); M = opt('--merge-in-head')
        u = unresolved(repo, (('develop', D), ('head', K['head']), ('base', K['base']), ('merge-in head', M)))
        if u: print('QM REFUSED: ' + u); raise SystemExit(2)
        pred = opt('--predicted') or predict(repo, D, out)
        if pred in ('REFUSED', 'UNRESOLVABLE'): raise SystemExit(2)
        t = Tally(); r = qm(repo, M, D, pred, t)
        raise SystemExit(2 if r == 'UNRESOLVABLE' else t.end())
    print(__doc__); raise SystemExit(2)
