#!/usr/bin/env python3
r"""c4_docs_gate71.py — the two platform docs for #1398 (KS-1136) and the MERGE-IN PREDICTION. THE HEAD IS A PARAMETER.
READERS: composee5's newline-tolerant h2 readers, extracted at the pinned lines by lib_gate71 (the OLD same-line reader is a negative arm only).

MODES (all: --repo <YOUR clone> --head <40-hex>)
  docs      D1 BOUNDARY-FREE: per doc, the head minus ONE contiguous byte span == the base blob byte for byte, the span occurs exactly once
               in the head; CONTROL: the same span with ONE byte altered does NOT reproduce the base (FALSE).
            D2 LINE-ANCHORED: the block = the head's lines from its own h2 (flow `23.`; cheat `&mdash; KS-1136`, from the
               `<div class="section">` line directly above it) up to `  </body>`; head minus block == base line for line; the block is LAST.
            D3 ORDER (newline-tolerant): flow == base + [23] (1-16, 18-23: `17.` still a GAP, ascending); cheat == base + [KS-1136].
               CONTROL: a planted `<h2>\n  99.` block is HIT by the tolerant reader and MISSED by the same-line reader.
            D4 KEYS: inside each block the only HYPHENATED key is KS-1136 (de-hyphenated mentions printed); CONTROL: a planted KS-9999
               is found by the same regex; the doc-wide distinct-key count printed (the author says 88).
            D5 `<h2` openings == numbered/keyed h2s at head (no unkeyed h2 the lazy reader could straddle); div balance unchanged.
  predict   --develop-after D [--out FILE]   D == the base: NO MERGE-IN, the squash tree == END_TREE (stated). Otherwise: D must descend
            from the base; the 2 CODE paths must be untouched on base..D (else REFUSED: re-gate); each doc's block goes immediately before
            D's `  </body>` (TAIL, key-anchored, gate69 P4/Q2); read-back own exactly once and LAST, D's sequence the prefix; ascent INFO.
            Prints the predicted tree (built with a temporary index in YOUR clone).
  mergetree --develop-after D   `git merge-tree --write-tree --name-only D head`: tree or conflicts, vs predict: AGREE / DIVERGENCE (per doc).
  qm        --merge-in-head M --develop-after D   M's parents == [head, D]; tree(M) == the prediction; read-back; M's doc minus the block
            == D's doc byte for byte; the code paths at M == the head's blobs. REFUSES BY NAME on any absent object.
  --selftest  SIM develop = base + a planted foreign block (flow `24.`, cheat KS-9998) committed as OBJECTS ONLY in YOUR clone, then
            predict / read-back / wrong-order / split-h2 / altered-fragment / code-path-touched arms. Planted arms must FAIL.
rc 0 PASS / 1 FAIL or DIVERGENCE / 2 refused by name."""
import os, re, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate71 import (K, P, D, Tally, git, git_bytes, wgit, refuse_absent, resolvable, outside_forbidden, opt, blob_at,
                        flow_nums, flow_num_pos, cheat_keys, cheat_key_pos, old_sameline_nums, h2_open_count)

CLOSE = D['close_tag']; BASE = P['parents'][0]
DOCS = {'flow': D['flow'], 'cheat': D['cheat']}
CODE = [p for p in P['numstat'] if not p.startswith('Projects Documents/')]
SECTION_OPEN = re.compile(r'^\s*<div class="section">\s*$')
SIM_ENV = {'GIT_AUTHOR_NAME': 'gate71 SIM', 'GIT_AUTHOR_EMAIL': 'sim@gate71.invalid', 'GIT_COMMITTER_NAME': 'gate71 SIM',
           'GIT_COMMITTER_EMAIL': 'sim@gate71.invalid', 'GIT_AUTHOR_DATE': '2026-10-06T00:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-06T00:00:00Z'}


class Refused(Exception): pass


def own(doc): return D['flow_num'] if doc == 'flow' else D['cheat_key']
def seq(text, doc): return flow_nums(text) if doc == 'flow' else cheat_keys(text)


def positions(text, doc):
    raw = flow_num_pos(text) if doc == 'flow' else cheat_key_pos(text)
    T = text.split('\n')
    return [(k, ln - 1 if ln > 0 and SECTION_OPEN.match(T[ln - 1]) else ln) for k, ln in raw]


def close_line(L):
    c = [i for i, l in enumerate(L) if l == CLOSE]
    if len(c) != 1: raise Refused('close tag %r found %d time(s) (want 1)' % (CLOSE, len(c)))
    return c[0]


def block(doc, htext, btext):
    H = htext.split('\n'); pos = positions(htext, doc)
    idx = [i for i, (k, _) in enumerate(pos) if k == own(doc)]
    if len(idx) != 1: raise Refused('%s: own %s found %d time(s) at the head (want 1)' % (doc, own(doc), len(idx)))
    s = pos[idx[0]][1]; e = pos[idx[0] + 1][1] if idx[0] + 1 < len(pos) else close_line(H)
    if H[:s] + H[e:] != btext.split('\n'): raise Refused('%s: head minus the %s block != base (not ONE pure insertion)' % (doc, own(doc)))
    return H[s:e], e == close_line(H)


def boundary_free(hb, bb):
    i = 0
    while i < len(bb) and hb[i] == bb[i]: i += 1
    j = 0
    while j < len(bb) - i and hb[-1 - j] == bb[-1 - j]: j += 1
    frag = hb[i:len(hb) - j]
    return frag, hb.replace(frag, b'', 1) == bb, hb.count(frag)


def insert(doc, dtext, blk, order='tail'):
    Dl = dtext.split('\n'); pos = positions(dtext, doc)
    if own(doc) in [k for k, _ in pos]: raise Refused('%s: develop ALREADY carries %s (merged twice? re-gate)' % (doc, own(doc)))
    at = pos[-1][1] if order == 'wrong' else close_line(Dl)
    return '\n'.join(Dl[:at] + blk + Dl[at:])


def readback(doc, text, dtext=None):
    try: s = seq(text, doc)
    except ValueError as x: return False, 'reader refused: %s' % x
    o = own(doc); ok = s.count(o) == 1 and s[-1] == o
    pre = dtext is None or [x for x in s if x != o] == seq(dtext, doc)
    asc = s == sorted(s) if doc == 'flow' else None
    return ok and pre, 'own %s x%d, LAST %s, develop prefix kept %s, tail %s%s' % (o, s.count(o), s[-1:] == [o], pre, s[-3:],
                                                                                 (', ascending %s (INFO)' % asc) if doc == 'flow' else '')


# ---------------- docs ----------------
def docs(repo, head):
    t = Tally()
    for doc, path in DOCS.items():
        bb, hb = git_bytes(repo, BASE, path), git_bytes(repo, head, path)
        frag, ok, n = boundary_free(hb, bb)
        alt = bytearray(frag); k = len(alt) // 2; alt[k] = (alt[k] + 1) % 256; ctl = hb.replace(bytes(alt), b'', 1) == bb
        t.check('D1-%s' % doc, ok and n == 1 and not ctl, 'head minus ONE span (%d B) == base: %s; span occurs %d time(s); CONTROL 1-byte-altered span reproduces base: %s' % (len(frag), ok, n, ctl))
        bt, ht = bb.decode(), hb.decode()
        try:
            blk, last = block(doc, ht, bt)
            t.check('D2-%s' % doc, last, 'line block %d lines, head minus block == base line for line, block is LAST before `  </body>`: %s' % (len(blk), last))
        except Refused as x:
            t.check('D2-%s' % doc, False, str(x)); blk = []
        sb, sh = seq(bt, doc), seq(ht, doc)
        if doc == 'flow':
            t.check('D3-flow', sh == sb + [23] and 17 not in sh and sh == sorted(sh) and sb == D['flow_seq_base'],
                    'base %s.. -> head ..%s; 17 a GAP: %s; ascending %s; base == kit %s' % (sb[:3], sh[-4:], 17 not in sh, sh == sorted(sh), sb == D['flow_seq_base']))
            plant = ht.replace(CLOSE, '  <h2>\n    99. planted split heading</h2>\n' + CLOSE, 1)
            t.check('D3-flow-ctl', 99 in flow_nums(plant) and 99 not in old_sameline_nums(plant) and 23 in old_sameline_nums(ht),
                    'PLANTED `<h2>\\n  99.`: tolerant reader HIT %s, same-line reader MISSED %s (the same-line reader still sees 23: %s)' % (
                        99 in flow_nums(plant), 99 not in old_sameline_nums(plant), 23 in old_sameline_nums(ht)))
        else:
            t.check('D3-cheat', sh == sb + ['KS-1136'] and sb == D['cheat_seq_base'], 'base tail %s -> head tail %s; base == kit %s' % (sb[-2:], sh[-3:], sb == D['cheat_seq_base']))
        btxt = '\n'.join(blk)
        hy = sorted(set(re.findall(r'\bKS-\d+\b', btxt))); de = sorted(set(re.findall(r'\bKS \d+\b', btxt)))
        ctl = re.findall(r'\bKS-\d+\b', btxt + ' KS-9999 ')
        t.check('D4-%s' % doc, hy == ['KS-1136'] and 'KS-9999' in ctl, 'hyphenated keys in the block %s (want only KS-1136) | de-hyphenated %s | CONTROL planted KS-9999 found %s | doc-wide distinct hyphenated keys %d' % (
            hy, de, 'KS-9999' in ctl, len(set(re.findall(r'\bKS-\d+\b', ht)))))
        try: nk = len(seq(ht, doc))
        except ValueError as x: nk = -1
        dv = lambda s: len(re.findall(r'<div\b', s)) - len(re.findall(r'</div>', s))
        t.check('D5-%s' % doc, h2_open_count(ht) == nk and dv(ht) == dv(bt), '`<h2` openings %d == numbered/keyed %d; div balance %d == base %d' % (h2_open_count(ht), nk, dv(ht), dv(bt)))
    return t.end()


# ---------------- predict / mergetree / qm ----------------
def build_tree(repo, dev, blobs):
    """dev's tree with {path: (mode, blob)} applied, via a TEMPORARY index in YOUR clone."""
    if not outside_forbidden(repo): raise Refused('clone inside the forbidden root')
    fd, idx = tempfile.mkstemp(prefix='g71idx.'); os.close(fd); os.unlink(idx); env = {'GIT_INDEX_FILE': idx}
    try:
        if wgit(repo, 'read-tree', dev, env=env)[0]: raise Refused('read-tree %s failed' % dev[:12])
        for p, (mode, b) in blobs.items():
            if wgit(repo, 'update-index', '--add', '--cacheinfo', '%s,%s,%s' % (mode, b, p), env=env)[0]: raise Refused('update-index %s' % p)
        rc, o, e = wgit(repo, 'write-tree', env=env)
        if rc: raise Refused('write-tree: %s' % e.strip()[:120])
        return o.strip()
    finally:
        try: os.unlink(idx)
        except OSError: pass


def hash_blob(repo, data):
    rc, o, e = wgit(repo, 'hash-object', '-w', '--stdin', inp=data)
    if rc: raise Refused('hash-object: %s' % e.strip()[:120])
    return o.strip()


def predict(repo, head, dev, quiet=False):
    """(tree, {doc: text}, lines) — refuses if develop touched a code path since the base."""
    out = []
    if dev == BASE:
        out.append('develop == the base %s: NO MERGE-IN NEEDED; the squash tree == END_TREE %s' % (BASE[:12], P['end_tree'][:12]))
        return git(repo, 'rev-parse', head + '^{tree}').strip(), None, out
    if git(repo, 'merge-base', '--is-ancestor', BASE, dev, check=False)[0] != 0: raise Refused('develop %s does not descend from the base' % dev[:12])
    moved = [p for p in CODE if blob_at(repo, BASE, p) != blob_at(repo, dev, p)]
    if moved: raise Refused('develop moved a CODE path of this PR since the base %s: RE-GATE' % moved)
    blobs, texts = {}, {}
    for p in CODE: blobs[p] = (git(repo, 'ls-tree', head, '--', p).split()[0], git(repo, 'rev-parse', '%s:%s' % (head, p)).strip())
    for doc, path in DOCS.items():
        bt, ht, dt = (git_bytes(repo, r, path).decode() for r in (BASE, head, dev))
        if dt == bt:
            texts[doc] = ht; out.append('%s: develop UNCHANGED since the base -> the head blob' % doc)
        else:
            blk, _ = block(doc, ht, bt); m = insert(doc, dt, blk); texts[doc] = m
            ok, why = readback(doc, m, dt); out.append('%s: TAIL insert into develop -> read-back %s: %s' % (doc, 'OK' if ok else 'FAIL', why))
            if not ok: raise Refused('%s read-back FAILED: %s' % (doc, why))
        blobs[path] = ('100644', hash_blob(repo, texts[doc].encode()))
    return build_tree(repo, dev, blobs), texts, out


def mergetree(repo, head, dev):
    rc, o, e = wgit(repo, 'merge-tree', '--write-tree', '--name-only', dev, head)
    lines = o.strip().split('\n'); return rc, (lines[0] if lines else ''), lines[1:], e.strip()


def run_predict(repo, head, dev, outf):
    t = Tally()
    try:
        tree, texts, lines = predict(repo, head, dev)
    except Refused as x:
        print('REFUSED: %s' % x); return 1
    for l in lines: print('  ' + l)
    t.check('M1', bool(re.fullmatch(r'[0-9a-f]{40}', tree)), 'PREDICTED squash tree on develop %s: %s' % (dev[:12], tree))
    if outf: open(outf, 'w').write('develop %s\nhead %s\npredicted_tree %s\n' % (dev, head, tree))
    return t.end()


def run_mergetree(repo, head, dev):
    t = Tally()
    try: tree, texts, _ = predict(repo, head, dev)
    except Refused as x: print('REFUSED: %s' % x); return 1
    rc, mt, rest, err = mergetree(repo, head, dev)
    print('  git merge-tree rc %d tree %s conflicts/paths %s' % (rc, mt[:12], rest[:6]))
    agree = rc == 0 and mt == tree
    if not agree and rc == 0:
        for doc, path in DOCS.items():
            a = blob_at(repo, mt, path)
            b = blob_at(repo, tree, path)
            print('  %s: merge-tree blob %s vs predicted %s -> %s' % (doc, a[:12], b[:12], 'AGREE' if a == b else 'DIVERGENCE'))
    t.check('MT', agree, '%s: merge-tree %s vs predicted %s' % ('AGREE' if agree else 'DIVERGENCE (printed, never picked: the TAIL prediction is the target, RULINGS Q-M)', mt[:12], tree[:12]))
    return t.end()


def run_qm(repo, head, dev, m):
    t = Tally()
    rr = refuse_absent(repo, [('merge-in head', m), ('develop', dev)])
    if rr: return rr
    pr = git(repo, 'log', '-1', '--format=%P', m).split()
    t.check('Q1', pr == [head, dev], 'parents %s == [head, develop]' % [x[:12] for x in pr])
    try: tree, texts, _ = predict(repo, head, dev)
    except Refused as x: print('REFUSED: %s' % x); return 1
    mt = git(repo, 'rev-parse', m + '^{tree}').strip()
    t.check('Q2', mt == tree, 'tree(M) %s == predicted %s' % (mt[:12], tree[:12]))
    for doc, path in DOCS.items():
        mtext, dtext = git_bytes(repo, m, path).decode(), git_bytes(repo, dev, path).decode()
        ok, why = readback(doc, mtext, dtext); t.check('Q3-%s' % doc, ok, why)
        try:
            blk, _ = block(doc, mtext, dtext); t.check('Q4-%s' % doc, True, 'M minus its block == develop byte for byte')
        except Refused as x: t.check('Q4-%s' % doc, False, str(x))
    cb = [p for p in CODE if git(repo, 'rev-parse', '%s:%s' % (m, p)).strip() != git(repo, 'rev-parse', '%s:%s' % (head, p)).strip()]
    t.check('Q5', not cb, 'code paths at M == the head blobs %s' % (cb or ''))
    return t.end()


# ---------------- selftest ----------------
def sim_develop(repo, head):
    """base + a foreign flow block 24. and a cheat KS-9998 section before `  </body>`, committed as objects only."""
    blobs = {}
    for doc, path in DOCS.items():
        t = git_bytes(repo, BASE, path).decode()
        add = ('  <h2>24. A planted foreign block (KS 9998)</h2>\n    <p>sim</p>\n' if doc == 'flow' else
               '  <div class="section">\n      <h2>Planted foreign section &mdash; KS-9998</h2>\n      <p>sim</p>\n    </div>\n')
        blobs[path] = ('100644', hash_blob(repo, t.replace(CLOSE, add.rstrip('\n') + '\n' + CLOSE, 1).encode()))
    tree = build_tree(repo, BASE, blobs)
    rc, o, e = wgit(repo, 'commit-tree', tree, '-p', BASE, '-m', 'gate71 SIM develop: foreign block 24 / KS-9998', env=SIM_ENV)
    if rc: raise Refused('commit-tree: %s' % e.strip()[:120])
    return o.strip()


def selftest(repo, head):
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    rr = refuse_absent(repo, [('head', head), ('base', BASE)])
    if rr: return rr
    sim = sim_develop(repo, head); print('SIM develop %s (objects only, parent %s)' % (sim, BASE[:12]))
    tree, texts, lines = predict(repo, head, sim)
    for l in lines: print('  ' + l)
    ok, why = readback('flow', texts['flow'], git_bytes(repo, sim, DOCS['flow']).decode())
    rep(ok and flow_nums(texts['flow'])[-2:] == [24, 23], 'TAIL on SIM: flow ...24 23 (own LAST, NOT ascending — INFO), read-back OK: %s' % why)
    ok, why = readback('cheat', texts['cheat'], git_bytes(repo, sim, DOCS['cheat']).decode())
    rep(ok and cheat_keys(texts['cheat'])[-2:] == ['KS-9998', 'KS-1136'], 'TAIL on SIM: cheat ...KS-9998 KS-1136, read-back OK')
    ht, bt, st = (git_bytes(repo, r, DOCS['flow']).decode() for r in (head, BASE, sim))
    blk, _ = block('flow', ht, bt)
    w = insert('flow', st, blk, order='wrong'); ok, why = readback('flow', w, st)
    rep(not ok, 'PLANTED WRONG ORDER (block before develop\'s last section) FAILS the read-back: %s' % why)
    rep(boundary_free(git_bytes(repo, head, DOCS['cheat']), git_bytes(repo, BASE, DOCS['cheat']))[1], 'boundary-free: the real cheat insertion reproduces the base')
    hb = git_bytes(repo, head, DOCS['flow']); bb = git_bytes(repo, BASE, DOCS['flow'])
    edited = hb.replace(b'<h2>1.', b'<h2>1 .', 1)
    rep(edited != hb and not boundary_free(edited, bb)[1], 'PLANTED edit of a PRE-EXISTING heading: NOT one pure insertion (boundary-free FALSE)')
    try: block('flow', edited.decode(), bb.decode()); rep(False, 'line-anchored block must refuse an edited pre-existing line')
    except Refused: rep(True, 'PLANTED edit of a pre-existing line: the line-anchored block REFUSES')
    plant = ht.replace(CLOSE, '  <h2>\n    99. x</h2>\n' + CLOSE, 1)
    rep(99 in flow_nums(plant) and 99 not in old_sameline_nums(plant), 'split `<h2>\\n 99.`: tolerant HIT, same-line MISSED')
    try:
        insert('flow', ht, blk); rep(False, 'inserting into a develop that already has 23 must refuse')
    except Refused: rep(True, 'PLANTED develop already carrying 23.: insert REFUSES (merged twice)')
    # a develop that touched a CODE path must refuse (objects only)
    cb = {K['product']['path']: ('100755', hash_blob(repo, git_bytes(repo, BASE, K['product']['path']) + b'# sim\n'))}
    t2 = build_tree(repo, sim, cb); rc, o, e = wgit(repo, 'commit-tree', t2, '-p', sim, '-m', 'gate71 SIM: code path touched', env=SIM_ENV)
    try: predict(repo, head, o.strip()); rep(False, 'a develop that touched 09 must refuse')
    except Refused as x: rep('RE-GATE' in str(x), 'PLANTED develop touching 09-aggregate-report.sh: predict REFUSES (%s)' % str(x)[:60])
    rep(predict(repo, head, BASE)[0] == P['end_tree'], 'develop == base: predicted tree == END_TREE (positive control)')
    rep(refuse_absent(repo, [('x', 'deadbeef' * 5)]) == 2, 'an ABSENT object is refused BY NAME (rc 2)')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    repo = opt(A, '--repo'); head = opt(A, '--head', P['head_expected'])
    if not A or not repo: print(__doc__); return 2
    named = [('head', head), ('base', BASE)]
    dev = opt(A, '--develop-after')
    if dev: named.append(('develop', dev))
    rr = refuse_absent(repo, named)
    if rr: return rr
    try:
        if '--selftest' in A: return selftest(repo, head)
        if A[0] == 'docs': return docs(repo, head)
        if A[0] == 'predict' and dev: return run_predict(repo, head, dev, opt(A, '--out'))
        if A[0] == 'mergetree' and dev: return run_mergetree(repo, head, dev)
        if A[0] == 'qm' and dev and opt(A, '--merge-in-head'): return run_qm(repo, head, dev, opt(A, '--merge-in-head'))
    except Refused as x:
        print('REFUSED: %s' % x); return 1
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
