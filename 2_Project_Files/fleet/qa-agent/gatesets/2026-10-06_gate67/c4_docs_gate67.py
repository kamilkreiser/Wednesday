#!/usr/bin/env python3
r"""c4_docs_gate67.py — C4 DOCS for #1394 (KS-723), gate67: the NEWLINE-TOLERANT h2 proof, the KEY-ANCHORED docs-only merge-in
predictor, git merge-tree cross-check (AGREE / DIVERGENCE), and Q-M.

THE READERS are Seat E 5th's, not this kit's: lib_gate67 extracts them from composee5_copy.py (sha256 f9ab42d9fc25f189…, pinned)
at :66 (flow numbers  `<h2[^>]*>\s*(\d+)\.`  re.S|re.I) and :82 (cheat keys  `<h2[^>]*>.*?&mdash;\s*(KS-\d+)\s*</h2>`  re.S|re.I).
`\s` and `.*?` under re.S cross newlines, so `<h2>\n  18. …` (develop c5101866+, #1390's split) is read. The OLD same-line reader
(`<h2[^>]*>(\d+)\.` per line) is kept ONLY as the proof's negative arm.

THE CONSTRUCTION (Wednesday's rule for #1394, not div- or tail-anchored):
  FLOW  — #1394's block = the head's lines from its `16.` h2 up to (not incl.) the head's next numbered h2 (`18.`); head minus the
          block must equal the base d784 BYTE FOR BYTE. It is inserted in develop immediately BEFORE the line where develop's first
          numbered h2 ABOVE 16 opens (`18.`), and develop's numbered h2 just below that must be 14 (nothing in 15..17 on develop).
          Read back: numbers ascending, 16 exactly once, neighbours 14 and 18.
  CHEAT — #1394's block = the head's lines from its KS-723 h2 up to (not incl.) the `  </body>` line; head minus block == base.
          It is inserted in develop immediately before develop's `  </body>` (once), i.e. AFTER develop's LAST keyed section.
          Read back: keys == develop's keys + [KS-723], KS-723 LAST, predecessor == develop's last key.
  CODE  — develop's tree with the 3 code paths (spec yaml, registry, test) at the HEAD's blobs. Refused if develop touched any of
          them, or a hook path, since the base (that is a RE-GATE, not a merge-in).
  WRONG-ORDER CONTROL (`--order wrong`): flow block placed before develop's `19.` (after 18.), cheat block placed BEFORE develop's last
          keyed section. It must give a DIFFERENT tree and FAIL the read-back.

h2proof   --repo R --develop D           per doc at d784 and D: `<h2` opens, split h2s, tolerant count, old same-line count; then
          a planted `<h2>\n      99. planted split heading &mdash; KS-99999\n    </h2>` before D's close tag: tolerant HIT, old MISS.
predict   --repo OWN --develop-after D [--order key|wrong] [--out DIR]     prints the tree + per-doc read-back.
mergetree --repo OWN --develop-after D   `git merge-tree --write-tree --name-only head D`: rc, tree, conflicts, read-back; vs predict.
          Prints AGREE or DIVERGENCE (never picks).
qm        --repo R --merge-in-head M --develop-after D [--predicted TREE]
          REFUSES BY NAME, rc 2, 0 checks run, in this order: `develop unresolvable`, `head unresolvable`, `base unresolvable`,
          `merge-in head unresolvable` (gate63/gate64's defect — an absent develop read as None blobs -> a FALSE M6 re-gate — cannot
          recur: nothing about D is read before D resolves).
          M1 tree(M) == the key-anchored prediction on D (THE AUTHORITY) · M2 parents == [head, D] · M3 D..M names only the 5 kit paths,
          the 3 code paths at the head blobs · M4 0 trailers (raw 1 byte), 0 Co-Authored-By · M5 base ancestor of D · M6 base..D touches
          no code / hook path (`RE-GATE: develop advance touches kit path(s) …`) and D carries no KS-723 · M7 head..M not on D == [M] ·
          M8 read-back at M with the composee5 readers: flow numbers == D's with 16 between 14 and 18, ascending; cheat keys == D's +
          [KS-723] LAST; 0 conflict markers; `<div` balance == D's.
--selftest   all arms on SIM commits (objects only, in the kit's own clone).
rc 0 PASS / rc 1 FAIL or content refusal / rc 2 refused by name."""
import os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate67 import (K, git, wgit, Tally, outside_forbidden, resolvable, SCRATCH, flow_nums, flow_num_pos, cheat_keys,
                        cheat_key_pos, old_sameline_nums, h2_open_count, split_h2_count, OLD_SAMELINE_RX)

CLOSE = K['close_tag']; OWN = K['own_key']; OWNN = K['flow_own_num']; LO = K['flow_num_lo']; HI = K['flow_num_hi']
MARK = re.compile(r'^(<<<<<<<|=======|>>>>>>>)( |$)', re.M)
OLD_SAMELINE_KEY = re.compile(r'<h2[^>]*>.*?&mdash;\s*(KS-\d+)\s*</h2>', re.I)   # :82's pattern WITHOUT re.S, per line: negative arm only
SIM_ENV = {'GIT_AUTHOR_NAME': 'gate67 SIM', 'GIT_AUTHOR_EMAIL': 'sim@gate67.invalid', 'GIT_COMMITTER_NAME': 'gate67 SIM',
           'GIT_COMMITTER_EMAIL': 'sim@gate67.invalid', 'GIT_AUTHOR_DATE': '2026-10-06T00:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-06T00:00:00Z'}


class Refused(Exception):
    pass


def L(s): return s.split('\n')
def divbal(t): return len(re.findall(r'<div\b', t)) - len(re.findall(r'</div>', t))
def show(repo, rev, p): return git(repo, 'show', '%s:%s' % (rev, p))


def unresolved(repo, pairs):
    for name, s in pairs:
        if not resolvable(repo, s):
            return '%s unresolvable: %r is not a commit in %s — fetch it BY SHA into YOUR clone, then re-run' % (name, s, repo)
    return None


# ---------------- blocks ----------------
def flow_block(htext, btext):
    pos = flow_num_pos(htext); H = L(htext)
    own = [i for i, (n, _, _) in enumerate(pos) if n == OWNN]
    if len(own) != 1: raise Refused('flow: %d. found %d time(s) at the head (want 1)' % (OWNN, len(own)))
    i = own[0]
    if i + 1 >= len(pos): raise Refused('flow: no numbered h2 after %d. at the head' % OWNN)
    s, e = pos[i][2], pos[i + 1][2]
    if H[:s] + H[e:] != L(btext): raise Refused('flow: head minus the %d. block != base d784 (not one pure insertion)' % OWNN)
    return H[s:e]


def cheat_block(htext, btext):
    pos = cheat_key_pos(htext); H = L(htext)
    own = [i for i, (k, _, _) in enumerate(pos) if k == OWN]
    if len(own) != 1: raise Refused('cheat: %s found %d time(s) at the head (want 1)' % (OWN, len(own)))
    if own[0] != len(pos) - 1: raise Refused('cheat: %s is not the LAST keyed h2 at the head' % OWN)
    c = [j for j, l in enumerate(H) if l == CLOSE]
    if len(c) != 1: raise Refused('cheat: close tag at the head %d time(s)' % len(c))
    s, e = pos[own[0]][2], c[0]
    if H[:s] + H[e:] != L(btext): raise Refused('cheat: head minus the %s block != base d784 (not one pure insertion)' % OWN)
    return H[s:e]


def resolve_flow(dtext, blk, order):
    D = L(dtext); pos = flow_num_pos(dtext); ns = [n for n, _, _ in pos]
    if OWNN in ns: raise Refused('flow: develop ALREADY carries %d. (merged twice? re-gate)' % OWNN)
    if order == 'key':
        above = [p for p in pos if p[0] > OWNN]
        if not above: raise Refused('flow: develop has no numbered h2 above %d' % OWNN)
        j = pos.index(above[0])
        if above[0][0] != HI or j == 0 or pos[j - 1][0] != LO:
            raise Refused('flow: develop neighbours around the slot are %s / %s, want %d / %d — re-gate' % (pos[j - 1][0] if j else None, above[0][0], LO, HI))
        at = above[0][2]
    elif order == 'wrong':
        after = [p for p in pos if p[0] > HI]
        if not after: raise Refused('flow: no numbered h2 above %d for the wrong-order control' % HI)
        at = after[0][2]
    else:
        raise Refused('unknown order %r' % order)
    return '\n'.join(D[:at] + blk + D[at:])


def resolve_cheat(dtext, blk, order):
    D = L(dtext); pos = cheat_key_pos(dtext)
    if OWN in [k for k, _, _ in pos]: raise Refused('cheat: develop ALREADY carries %s (merged twice? re-gate)' % OWN)
    c = [j for j, l in enumerate(D) if l == CLOSE]
    if len(c) != 1: raise Refused('cheat: develop close tag %r found %d time(s)' % (CLOSE, len(c)))
    if not pos: raise Refused('cheat: develop has no keyed h2')
    if order == 'key':
        at = c[0]
    elif order == 'wrong':
        at = pos[-1][2]
    else:
        raise Refused('unknown order %r' % order)
    return '\n'.join(D[:at] + blk + D[at:])


def readback(doc, text):
    """(ok, description) for a doc at a merge result, given ONLY the text."""
    if doc == 'flow':
        ns = flow_nums(text)
        if OWNN not in ns: return False, 'numbers %s: %d. absent' % (ns, OWNN)
        i = ns.index(OWNN)
        ok = ns == sorted(set(ns)) and ns.count(OWNN) == 1 and i > 0 and ns[i - 1] == LO and i + 1 < len(ns) and ns[i + 1] == HI
        return ok, 'numbers %s | strictly ascending %s | %d. once %s | neighbours %s/%s' % (
            ' '.join(map(str, ns)), ns == sorted(set(ns)), OWNN, ns.count(OWNN) == 1, ns[i - 1] if i else None, ns[i + 1] if i + 1 < len(ns) else None)
    try:
        ks = [k for k, _, _ in cheat_key_pos(text)]
    except ValueError as x:
        return False, 'reader refused: %s' % x
    ok = bool(ks) and ks[-1] == OWN and ks.count(OWN) == 1
    return ok, 'keys %s | %s LAST %s | predecessor %s' % (' '.join(ks), OWN, ks[-1:] == [OWN], ks[-2] if len(ks) > 1 else None)


def predict(repo, D, out, order='key', head=None, quiet=False):
    head = head or K['head']; base = K['base']
    if not outside_forbidden(repo):
        print('PREDICT REFUSED: predict writes objects; %s is inside %s — use your OWN scratch clone' % (repo, K['forbidden_root'])); return 'REFUSED'
    u = unresolved(repo, (('develop', D), ('head', head), ('base', base)))
    if u:
        print('PREDICT REFUSED: ' + u); return 'UNRESOLVABLE'
    adv = set(git(repo, 'diff', '--name-only', base, D).splitlines())
    hit = sorted(adv & (set(K['code_paths']) | set(K['hook_blobs'])))
    if hit:
        print('PREDICT REFUSED: RE-GATE: develop advance touches kit path(s) %s since the base' % hit); return None
    try:
        nf = resolve_flow(show(repo, D, K['flow']), flow_block(show(repo, head, K['flow']), show(repo, base, K['flow'])), order)
        nc = resolve_cheat(show(repo, D, K['cheat']), cheat_block(show(repo, head, K['cheat']), show(repo, base, K['cheat'])), order)
    except (Refused, ValueError) as e:
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
    tree = tree.strip()
    q = os.path.join(out, '_quarantine'); os.makedirs(q, exist_ok=True)
    shutil.move(idx, os.path.join(q, os.path.basename(idx) + '.' + order + '.' + tree[:8]))   # quarantine, never rm
    if not quiet:
        print('PREDICTED %s (order %s, develop-after %s, head %s)' % (tree, order, D[:12], head[:12]))
        for r in doc_report(repo, tree, order): print(r)
    return tree


def ok_tree(x): return x not in (None, 'REFUSED', 'UNRESOLVABLE')


def doc_report(repo, rev, label):
    rows = []
    for doc in ('flow', 'cheat'):
        rc, txt, e = git(repo, 'show', '%s:%s' % (rev, K[doc]), check=False)
        if rc: rows.append('  %s %s: ABSENT' % (label, doc)); continue
        ok, why = readback(doc, txt)
        rows.append('  %s %s blob %s: h2 %d | %s | markers %d | div %+d | READ-BACK %s' % (
            label, doc, git(repo, 'rev-parse', '%s:%s' % (rev, K[doc])).strip()[:12], h2_open_count(txt), why,
            len(MARK.findall(txt)), divbal(txt), 'OK' if ok else 'FAIL'))
    return rows


def mergetree(repo, D, out, head=None):
    head = head or K['head']
    if not outside_forbidden(repo):
        print('MERGETREE REFUSED: merge-tree writes objects; use your OWN scratch clone'); return 2
    u = unresolved(repo, (('develop', D), ('head', head)))
    if u: print('MERGETREE REFUSED: ' + u); return 2
    rc, o, e = wgit(repo, 'merge-tree', '--write-tree', '--name-only', head, D)
    parts = o.split('\n\n', 1); first = parts[0].split('\n'); mt = first[0].strip(); conflicted = [x for x in first[1:] if x]
    msgs = [x for x in (parts[1] if len(parts) > 1 else '').split('\n') if x]
    print('GIT `merge-tree --write-tree --name-only %s %s` rc %d tree %s' % (head[:12], D[:12], rc, mt))
    print('  conflicted paths (%d): %s' % (len(conflicted), conflicted))
    for m in msgs: print('  | ' + m[:200])
    pk = predict(repo, D, out, 'key', head, quiet=True)
    print('KEY-ANCHORED tree %s' % pk)
    for r in doc_report(repo, mt, 'merge-tree'): print(r)
    if ok_tree(pk):
        for r in doc_report(repo, pk, 'key-anchored'): print(r)
        for doc in ('flow', 'cheat'):
            a = git(repo, 'rev-parse', '--verify', '--quiet', '%s:%s' % (mt, K[doc]), check=False)[1].strip()
            b = git(repo, 'rev-parse', '%s:%s' % (pk, K[doc])).strip()
            print('  %s blob: merge-tree %s vs key-anchored %s -> %s%s' % (doc, a[:12], b[:12], 'SAME' if a == b else 'DIFFERENT',
                  ' (git CONFLICTED this doc)' if K[doc] in conflicted else ''))
        print('  paths differing merge-tree vs key-anchored: %s' % sorted(set(git(repo, 'diff', '--name-only', mt, pk).splitlines())))
        # the readings a seat would reach BY HAND on git's conflict, for Wednesday's ruling (INFO; none is picked)
        for doc in ('flow', 'cheat'):
            if K[doc] not in conflicted: continue
            m = L(git(repo, 'show', '%s:%s' % (mt, K[doc])))
            a = [i for i, l in enumerate(m) if l.startswith('<<<<<<< ')]; b = [i for i, l in enumerate(m) if l == '=======']; c = [i for i, l in enumerate(m) if l.startswith('>>>>>>> ')]
            if not (len(a) == len(b) == len(c) == 1):
                print('  HAND readings of %s: %d conflict region(s) — not computed (needs exactly 1)' % (doc, len(a))); continue
            ours, theirs = m[a[0] + 1:b[0]], m[b[0] + 1:c[0]]
            keyt = git(repo, 'show', '%s:%s' % (pk, K[doc]))
            print('  HAND readings of %s: conflict region :%d-:%d, OURS %d line(s), THEIRS %d line(s)' % (doc, a[0] + 1, c[0] + 1, len(ours), len(theirs)))
            for nm, mid in (('take OURS', ours), ('take THEIRS', theirs), ('OURS then THEIRS', ours + theirs), ('THEIRS then OURS', theirs + ours)):
                txt = '\n'.join(m[:a[0]] + mid + m[c[0] + 1:])
                okr, desc = readback(doc, txt)
                print('    %-17s == key-anchored blob: %-5s | READ-BACK %s | %s' % (nm, txt == keyt, 'OK' if okr else 'FAIL', desc[:150]))
    verdict = 'AGREE' if ok_tree(pk) and mt == pk and rc == 0 else 'DIVERGENCE'
    print('%s: merge-tree %s (rc %d) vs key-anchored %s%s' % (verdict, mt[:12], rc, str(pk)[:12], '' if verdict == 'AGREE' else ' — Wednesday rules; this kit does not pick'))
    return 0 if verdict == 'AGREE' else 1


# ---------------- qm ----------------
def qm(repo, M, D, pred, t, head=None, out=None):
    head = head or K['head']; base = K['base']
    u = unresolved(repo, (('develop', D), ('head', head), ('base', base), ('merge-in head', M)))
    if u:
        print('QM REFUSED: ' + u); return 'UNRESOLVABLE'
    M = git(repo, 'rev-parse', M + '^{commit}').strip(); D = git(repo, 'rev-parse', D + '^{commit}').strip()
    if pred is None:
        if outside_forbidden(repo):
            pred = predict(repo, D, out or os.path.join(SCRATCH, 'qm'), 'key', head, quiet=True)
        else:
            pred = None; print('INFO qm: repo is the shared checkout; no --predicted given and predict cannot write there -> M1 cannot pass')
    tm = git(repo, 'rev-parse', M + '^{tree}').strip()
    t.check('M1', ok_tree(pred) and tm == pred, 'tree(M) %s vs key-anchored prediction %s — THE AUTHORITY' % (tm[:12], str(pred)[:12]))
    par = git(repo, 'log', '-1', '--format=%P', M).split()
    t.check('M2', par == [head, D], 'parents %s (want [%s, %s])' % ([p[:12] for p in par], head[:12], D[:12]))
    names = git(repo, 'diff', '--name-only', D, M).splitlines()
    bad = [p for p in names if p not in K['files']]
    drift = [p for p in K['code_paths'] if git(repo, 'rev-parse', '--verify', '--quiet', '%s:%s' % (M, p), check=False)[1].strip() != K['head_blobs'][p]]
    t.check('M3', not bad and not drift, 'D..M paths %d; non-kit %s; code paths off the head blob %s' % (len(names), bad, drift))
    tb = len(git(repo, 'log', '-1', '--format=%(trailers)', M).encode())
    co = len(re.findall(r'(?im)^co-authored-by:', git(repo, 'log', '-1', '--format=%B', M)))
    t.check('M4', tb == 1 and co == 0, 'M trailers raw %d byte(s), Co-Authored-By %d (want 1 / 0)' % (tb, co))
    rc = git(repo, 'merge-base', '--is-ancestor', base, D, check=False)[0]
    t.check('M5', rc == 0, 'base %s is an ancestor of D %s: %s (D moved: %s)' % (base[:12], D[:12], rc == 0, D != base))
    adv = git(repo, 'diff', '--name-only', base, D).splitlines()
    hit = sorted(set(adv) & (set(K['code_paths']) | set(K['hook_blobs'])))
    carries = []
    fd, cd = show(repo, D, K['flow']), show(repo, D, K['cheat'])
    if OWNN in flow_nums(fd): carries.append('flow %d.' % OWNN)
    if OWN in cheat_keys(cd): carries.append('cheat %s' % OWN)
    t.check('M6', not hit and not carries, ('RE-GATE: develop advance touches kit path(s) %s' % hit if hit else "develop's advance %d path(s), kit paths among them none" % len(adv))
            + ('; D already carries %s' % carries if carries else ''))
    new = git(repo, 'rev-list', '%s..%s' % (head, M), '^' + D).split()
    t.check('M7', new == [M], 'commits in head..M not on D: %s (want exactly [M])' % [c[:12] for c in new])
    why = []
    for doc, dtext in (('flow', fd), ('cheat', cd)):
        mt = show(repo, M, K[doc])
        ok, desc = readback(doc, mt)
        if not ok: why.append('%s %s' % (doc, desc))
        if MARK.search(mt): why.append('%s conflict markers %d' % (doc, len(MARK.findall(mt))))
        if doc == 'flow':
            want = sorted(flow_nums(dtext) + [OWNN]); got = flow_nums(mt)
            if got != want: why.append('flow numbers %s != develop+16 %s' % (got, want))
        else:
            want = cheat_keys(dtext) + [OWN]; got = cheat_keys(mt)
            if got != want: why.append('cheat keys %s != develop+[%s] %s' % (got, OWN, want))
        hb = show(repo, head, K[doc]); bb = show(repo, base, K[doc])
        # M minus the head's block must be develop BYTE FOR BYTE (catches a "take OURS" resolution that reads back right but
        # reverts develop's own reformatting — the composee5 readers alone cannot see that; see mergetree's HAND readings)
        try:
            blk = flow_block(hb, bb) if doc == 'flow' else cheat_block(hb, bb)
            ML = L(mt); n = len(blk)
            at = [i for i in range(len(ML) - n + 1) if ML[i:i + n] == blk]
            if len(at) != 1: why.append('%s: the head block occurs %d time(s) in M (want 1)' % (doc, len(at)))
            elif ML[:at[0]] + ML[at[0] + n:] != L(dtext): why.append('%s: M minus the KS-723 block != develop byte for byte' % doc)
        except (Refused, ValueError) as x:
            why.append('%s block: %s' % (doc, x))
        if divbal(mt) - divbal(dtext) != divbal(hb) - divbal(bb):
            why.append('%s div delta %+d != the block\'s %+d' % (doc, divbal(mt) - divbal(dtext), divbal(hb) - divbal(bb)))
    t.check('M8', not why, 'READ-BACK at M (composee5 readers): %s' % ('; '.join(why) if why else 'flow 16 between 14/18 strictly ascending, cheat KS-723 LAST, M minus the block == develop on both docs, 0 markers, div deltas == the block\'s'))
    return 'DONE'


# ---------------- h2 proof ----------------
PLANT = '    <h2>\n      99. planted split heading &mdash; KS-99999\n    </h2>'


def plant(text):
    if text.count('\n' + CLOSE + '\n') != 1 and not text.endswith('\n' + CLOSE): raise Refused('close tag must occur exactly once')
    return text.replace('\n' + CLOSE, '\n' + PLANT + '\n' + CLOSE, 1)


def h2proof(repo, D, t):
    for doc in ('flow', 'cheat'):
        for label, rev in (('d784', K['base']), ('develop %s' % D[:12], D)):
            txt = show(repo, rev, K[doc])
            tol = flow_nums(txt) if doc == 'flow' else cheat_keys(txt)
            old = old_sameline_nums(txt) if doc == 'flow' else [m.group(1) for l in L(txt) for m in [OLD_SAMELINE_KEY.search(l)] if m]
            print('COUNT %s @ %s: <h2 opens %d | split across lines %d | tolerant (composee5 %s) %d | old same-line %d | tolerant %s' % (
                doc, label, h2_open_count(txt), split_h2_count(txt), ':66' if doc == 'flow' else ':82', len(tol), len(old),
                ' '.join(map(str, tol))))
        txt = show(repo, D, K[doc]); p = plant(txt)
        if doc == 'flow':
            hit = 99 in flow_nums(p); miss = 99 not in old_sameline_nums(p)
        else:
            hit = 'KS-99999' in cheat_keys(p); miss = 'KS-99999' not in [m.group(1) for l in L(p) for m in [OLD_SAMELINE_KEY.search(l)] if m]
        t.check('H-%s' % doc, hit and miss, 'planted split h2 before %s close tag @ develop %s: tolerant HIT %s, old same-line MISS %s' % (doc, D[:12], hit, miss))
        # control: the SAME plant on ONE line is hit by BOTH readers (the old reader is not simply broken)
        one = txt.replace('\n' + CLOSE, '\n    <h2>99. planted one-line heading &mdash; KS-99999</h2>\n' + CLOSE, 1)
        both = (99 in flow_nums(one) and 99 in old_sameline_nums(one)) if doc == 'flow' else (
            'KS-99999' in cheat_keys(one) and 'KS-99999' in [m.group(1) for l in L(one) for m in [OLD_SAMELINE_KEY.search(l)] if m])
        t.check('H-%s-ctl' % doc, both, 'CONTROL one-line plant: BOTH readers hit (%s)' % both)


# ---------------- self-test ----------------
def sim_commit(repo, parents, msg, tree):
    args = ['commit-tree', tree]
    for p in parents: args += ['-p', p]
    rc, o, e = wgit(repo, *args, '-m', msg, env=SIM_ENV)
    assert rc == 0, e
    return o.strip()


def sim_develop_touching(repo, D, path, out):
    """a SIM develop: D plus one byte appended to a kit code path (objects only)."""
    idx = os.path.join(out, 'simdev.index.%d' % os.getpid()); env = {'GIT_INDEX_FILE': idx}
    assert wgit(repo, 'read-tree', D, env=env)[0] == 0
    txt = show(repo, D, path) + '// SIM develop edit\n'
    rc, sha, e = wgit(repo, 'hash-object', '-w', '--stdin', input_bytes=txt.encode()); assert rc == 0
    assert wgit(repo, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (sha.strip(), path), env=env)[0] == 0
    rc, tree, e = wgit(repo, 'write-tree', env=env); assert rc == 0
    q = os.path.join(out, '_quarantine'); os.makedirs(q, exist_ok=True); shutil.move(idx, os.path.join(q, os.path.basename(idx) + '.' + tree.strip()[:8]))
    return sim_commit(repo, [D], 'SIM develop: touches %s\n' % path, tree.strip())


def take_ours_tree(repo, D, out):
    """git merge-tree's tree with every single-region conflict resolved as OURS (the head's side)."""
    rc, o, e = wgit(repo, 'merge-tree', '--write-tree', '--name-only', K['head'], D)
    first = o.split('\n\n', 1)[0].split('\n'); mt = first[0].strip(); conflicted = [x for x in first[1:] if x]
    idx = os.path.join(out, 'ours.index.%d' % os.getpid()); env = {'GIT_INDEX_FILE': idx}
    assert wgit(repo, 'read-tree', mt, env=env)[0] == 0
    for p in conflicted:
        m = L(git(repo, 'show', '%s:%s' % (mt, p)))
        a = [i for i, l in enumerate(m) if l.startswith('<<<<<<< ')]; b = [i for i, l in enumerate(m) if l == '=======']; c = [i for i, l in enumerate(m) if l.startswith('>>>>>>> ')]
        if not (len(a) == len(b) == len(c) == 1): return None
        txt = '\n'.join(m[:a[0]] + m[a[0] + 1:b[0]] + m[c[0] + 1:])
        rc, sha, e = wgit(repo, 'hash-object', '-w', '--stdin', input_bytes=txt.encode()); assert rc == 0
        assert wgit(repo, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (sha.strip(), p), env=env)[0] == 0
    rc, tree, e = wgit(repo, 'write-tree', env=env); assert rc == 0
    q = os.path.join(out, '_quarantine'); os.makedirs(q, exist_ok=True); shutil.move(idx, os.path.join(q, os.path.basename(idx) + '.' + tree.strip()[:8]))
    return tree.strip()


def selftest(repo, D):
    out = os.path.join(SCRATCH, 'selftest'); os.makedirs(out, exist_ok=True)
    res = []
    def rep(cond, msg):
        res.append(cond); print('%s %s' % ('PASS' if cond else 'FAIL', msg))
    import io, contextlib
    def quiet(f, *a, **k):
        b = io.StringIO()
        with contextlib.redirect_stdout(b): r = f(*a, **k)
        return r, b.getvalue()
    t = Tally(); _, o = quiet(h2proof, repo, D, t)
    rep(not t.fails and t.n == 4, 'h2proof: 4/4 (tolerant HIT / old MISS on both docs + one-line controls) | %s' % t.fails)
    pk, _ = quiet(predict, repo, D, out, 'key'); pw, _ = quiet(predict, repo, D, out, 'wrong')
    rep(ok_tree(pk), 'predict key-anchored on %s -> %s' % (D[:12], pk))
    rep(ok_tree(pw) and pw != pk, 'WRONG-ORDER CONTROL tree %s DIFFERS from the key tree' % pw)
    fo, _ = readback('flow', show(repo, pw, K['flow'])); co_, _ = readback('cheat', show(repo, pw, K['cheat']))
    rep(not fo and not co_, 'WRONG-ORDER CONTROL fails the read-back on BOTH docs (flow ok=%s, cheat ok=%s)' % (fo, co_))
    pb, _ = quiet(predict, repo, K['base'], out, 'key')
    rep(pb == K['end_tree'], 'POSITIVE CONTROL: predict on develop = the base d784 reproduces END_TREE %s (got %s)' % (K['end_tree'][:12], str(pb)[:12]))
    r, o = quiet(predict, repo, 'f' * 40, out, 'key')
    rep(r == 'UNRESOLVABLE' and 'develop unresolvable' in o, 'predict refuses an absent develop BY NAME: %r' % o.strip()[:110])
    r, o = quiet(predict, K['checkout'], D, out, 'key')
    rep(r == 'REFUSED', 'predict refuses to write in the shared checkout: %r' % o.strip()[:90])

    def runqm(M, Dx, pred=None):
        tt = Tally(); r, o = quiet(qm, repo, M, Dx, pred, tt, None, out); return tt, r, o
    good = sim_commit(repo, [K['head'], D], 'Merge develop %s into KS-723 (docs-only merge-in)\n' % D[:12], pk)
    tt, r, o = runqm(good, D)
    rep(tt.n == 8 and not tt.fails, 'Q-M GOOD SIM %s: 8/8 PASS | fails %s' % (good[:12], tt.fails))
    wrong = sim_commit(repo, [K['head'], D], 'Merge develop (wrong order)\n', pw)
    tt, r, o = runqm(wrong, D)
    rep({'M1', 'M8'} <= set(tt.fails) and 'M4' not in tt.fails, 'Q-M WRONG-ORDER SIM: FAIL M1 + M8 (order) | got %s' % tt.fails)
    ours = take_ours_tree(repo, D, out)
    if ours:
        so = sim_commit(repo, [K['head'], D], 'Merge develop (take OURS on both conflicts)\n', ours)
        tt, r, o = runqm(so, D)
        rep({'M1', 'M8'} <= set(tt.fails), 'Q-M TAKE-OURS SIM (reads back right on both docs, reverts #1390 formatting): FAIL M1 + M8 | got %s' % tt.fails)
    else:
        rep(False, 'TAKE-OURS SIM could not be built')
    tr = sim_commit(repo, [K['head'], D], 'Merge develop\n\nCo-Authored-By: Someone <x@y.z>\n', pk)
    tt, r, o = runqm(tr, D)
    rep(tt.fails == ['M4'], 'Q-M TRAILER SIM (Co-Authored-By): FAIL exactly [M4] | got %s' % tt.fails)
    tt, r, o = runqm(good, 'f' * 40)
    rep(r == 'UNRESOLVABLE' and 'develop unresolvable' in o and tt.n == 0, 'Q-M ABSENT DEVELOP (fabricated sha): refuses BY NAME, 0 checks run: %r' % o.strip()[:130])
    absent_msg = o.strip()
    simdev = sim_develop_touching(repo, D, K['registry_file'], out)
    goodx = sim_commit(repo, [K['head'], simdev], 'Merge SIM develop\n', pk)
    tt, r, o = runqm(goodx, simdev)
    m6 = [l for l in o.split('\n') if l.startswith('FAIL M6')]
    rep('M6' in tt.fails and m6 and 'RE-GATE: develop advance touches kit path(s)' in m6[0] and 'unresolvable' not in o,
        'Q-M REAL KIT-PATH CHANGE (SIM develop %s edits anchoring.openapi.ts): M6 RE-GATE by content: %r' % (simdev[:12], (m6 or [''])[0][:140]))
    rep(bool(m6) and m6[0] != absent_msg and 'develop unresolvable' in absent_msg and 'RE-GATE' not in absent_msg,
        'the two messages DIFFER: absent -> "develop unresolvable" (rc 2, no checks) vs kit-path -> "RE-GATE: … touches kit path(s)" (M6 FAIL)')
    tt, r, o = runqm('e' * 40, D)
    rep(r == 'UNRESOLVABLE' and 'merge-in head unresolvable' in o, 'Q-M absent merge-in head refuses BY NAME: %r' % o.strip()[:100])
    sp = sim_commit(repo, [D], 'squash-shaped\n', pk)
    tt, r, o = runqm(sp, D); rep('M2' in tt.fails, 'Q-M single-parent SIM: FAIL M2 | got %s' % tt.fails)
    print('SELFTEST %d/%d' % (sum(res), len(res)))
    return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    repo = opt('--repo', os.path.join(SCRATCH, 'clone'))
    if not A: print(__doc__); return 2
    if A[0] == '--selftest': return selftest(repo, opt('--develop-after', K['develop_at_draft']))
    if A[0] == 'h2proof':
        D = opt('--develop', K['develop_at_draft']); u = unresolved(repo, (('develop', D), ('base', K['base'])))
        if u: print('H2PROOF REFUSED: ' + u); return 2
        t = Tally(); h2proof(repo, D, t); return t.end()
    if A[0] == 'predict':
        r = predict(repo, opt('--develop-after'), opt('--out', os.path.join(SCRATCH, 'predict')), opt('--order', 'key'))
        return 2 if r in ('UNRESOLVABLE', 'REFUSED') else (0 if ok_tree(r) else 1)
    if A[0] == 'mergetree':
        return mergetree(repo, opt('--develop-after'), opt('--out', os.path.join(SCRATCH, 'mergetree')))
    if A[0] == 'qm':
        t = Tally(); r = qm(repo, opt('--merge-in-head'), opt('--develop-after'), opt('--predicted'), t, None, opt('--out', os.path.join(SCRATCH, 'qm')))
        if r == 'UNRESOLVABLE': print('CHECKED 0 (refused by name)'); return 2
        return t.end()
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
