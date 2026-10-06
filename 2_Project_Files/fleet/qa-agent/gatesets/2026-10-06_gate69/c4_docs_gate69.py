#!/usr/bin/env python3
r"""c4_docs_gate69.py — C4 DOCS for the gate69 BATCH (#1395 KS-1305 = PR A; KS-1256 = PR B, a PARAMETER): the NEWLINE-TOLERANT h2
proof, the TAIL merge-in predictor (each PR alone on develop, AND the second PR on the first's predicted squash, both orders), git
merge-tree cross-check (AGREE / DIVERGENCE — printed, never picked), containment, and Q-M.

THE READERS are Seat E 5th's (lib_gate69 extracts them from composee5_copy.py, sha256 f9ab42d9…, pinned): :66 flow numbers
`<h2[^>]*>\s*(\d+)\.` and :82 cheat keys `<h2[^>]*>.*?&mdash;\s*(KS-\d+)\s*</h2>`, both re.S|re.I. The OLD same-line reader is kept
ONLY as the h2 proof's negative arm.

THE RULE (TAIL — kit.json doc_rule): a PR's BLOCK on a doc = the head's lines from its own h2 (or the `<div class="section">`
line directly above it, which the cheat uses for every section) (flow `<num>.`, cheat `&mdash; <KEY>`)
up to (not incl.) the head's NEXT numbered / keyed h2, or the `  </body>` line when it is the last. head minus block must equal the
doc at the PR's merge-base BYTE FOR BYTE (one pure insertion). The block is inserted into develop IMMEDIATELY BEFORE develop's
`  </body>` (exactly once): last in MERGE ORDER. Numbers are by ticket, never renumbered. READ-BACK: own number / key exactly once,
LAST among the numbered / keyed h2s, and develop's sequence is the prefix. Numeric ascent is printed as INFO (if #1395 lands first,
KS-1256's 21. lands AFTER 22. — RULINGS Q2), never a pass condition. CODE: develop's tree with the PR's code paths at the head's blobs
(refused if develop touched any of them, or a hook path, since the merge-base).
For the #1394 SIMULATION ONLY (sim_prs.X1394): `--sim-rule key` places 16. before develop's first numbered h2 above 16 (gate67's
KEY-ANCHORED rule); `--sim-rule tail` places it last.

MODES (every mode: --repo <your OWN scratch clone>; --pr A|B; --head <40-hex> (THE HEAD IS A PARAMETER; default A head_expected / B
head_standin); for B also --b-pr <n> where the PR number is printed)
  h2proof   --develop D                    per doc at the merge-base and D: `<h2` opens, split h2s, tolerant vs old counts; a PLANTED split
                                           h2 is HIT by the tolerant reader and MISSED by the old; a one-line CONTROL is hit by both.
  containment                              merge-base..head -U0 regions per doc ALL inside the PR's block; head minus block == merge-base;
                                           per-commit skill §4 table (which commits touch tests / flow / cheat).
  predict   --develop-after D [--order tail|wrong] [--out DIR]   one PR alone on D: the tree + per-doc read-back.
  chain     --develop-after D [--head-a H] [--head-b H]   BOTH orders: A on D, then B on SIM squash(A); B on D, then A on SIM squash(B).
                                           Prints every tree, the read-back of each, and the flow / cheat tails. (B's head defaults to the
                                           stand-in; with no B available pass --a-only.)
  mergetree --develop-after D [--over-sim-of A|B --head-a H --head-b H]   `git merge-tree --write-tree --name-only head D` vs the TAIL
                                           prediction: AGREE / DIVERGENCE. `--over-sim-of A` measures PR B over the SIM squash of A on D.
  qm        --merge-in-head M --develop-after D [--predicted TREE]   M1-M8 (README / prompt). REFUSES BY NAME (rc 2, 0 checks) on an
                                           unresolvable develop / head / merge-base / merge-in head.
  sim1394   --develop-after D              builds SIM develops = D + #1394 under the KEY rule and the TAIL rule (objects only) and runs
                                           `chain` over each. Prints the SIM commit shas so the gate can repeat any figure.
  --selftest [--develop-after D]           every arm on SIM commits (objects only, in YOUR clone). Arms MUST be able to FAIL.
rc 0 PASS / rc 1 FAIL, DIVERGENCE or content refusal / rc 2 refused by name."""
import io, contextlib, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate69 import (K, git, wgit, Tally, outside_forbidden, resolvable, SCRATCH, flow_nums, flow_num_pos, cheat_keys,
                        cheat_key_pos, old_sameline_nums, h2_open_count, split_h2_count, spec)

CLOSE = K['close_tag']
MARK = re.compile(r'^(<<<<<<<|=======|>>>>>>>)( |$)', re.M)
OLD_SAMELINE_KEY = re.compile(r'<h2[^>]*>.*?&mdash;\s*(KS-\d+)\s*</h2>', re.I)
SIM_ENV = {'GIT_AUTHOR_NAME': 'gate69 SIM', 'GIT_AUTHOR_EMAIL': 'sim@gate69.invalid', 'GIT_COMMITTER_NAME': 'gate69 SIM',
           'GIT_COMMITTER_EMAIL': 'sim@gate69.invalid', 'GIT_AUTHOR_DATE': '2026-10-06T00:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-06T00:00:00Z'}
DOCS = ('flow', 'cheat')


class Refused(Exception):
    pass


def L(s): return s.split('\n')
def divbal(t): return len(re.findall(r'<div\b', t)) - len(re.findall(r'</div>', t))
def show(repo, rev, p): return git(repo, 'show', '%s:%s' % (rev, p))
def ok_tree(x): return x not in (None, 'REFUSED', 'UNRESOLVABLE')


def unresolved(repo, pairs):
    for name, s in pairs:
        if not resolvable(repo, s):
            return '%s unresolvable: %r is not a commit in %s — fetch it BY SHA into YOUR clone (X7), then re-run' % (name, s, repo)
    return None


def own(sp, doc): return sp['flow_num'] if doc == 'flow' else sp['cheat_key']


def seq(text, doc):
    return flow_nums(text) if doc == 'flow' else [k for k, _, _ in cheat_key_pos(text)]


SECTION_OPEN = re.compile(r'^\s*<div class="section">\s*$')


def positions(text, doc):
    """[(number|key, START line of its section)]. The cheat wraps every keyed h2 in `<div class="section">` on the line ABOVE the h2
    (measured at 3f9ff4e1e1b9 and at both heads): the section starts THERE, so the wrapper line moves with its h2."""
    raw = [(n, ln) for n, _, ln in flow_num_pos(text)] if doc == 'flow' else [(k, ln) for k, _, ln in cheat_key_pos(text)]
    T = L(text)
    return [(k, ln - 1 if ln > 0 and SECTION_OPEN.match(T[ln - 1]) else ln) for k, ln in raw]


def close_line(lines):
    c = [j for j, l in enumerate(lines) if l == CLOSE]
    if len(c) != 1: raise Refused('close tag %r found %d time(s) (want 1)' % (CLOSE, len(c)))
    return c[0]


# ---------------- blocks ----------------
def block(sp, doc, htext, btext):
    """the PR's block on this doc at the head; refuses unless head minus block == merge-base byte for byte."""
    H = L(htext); pos = positions(htext, doc); o = own(sp, doc)
    idx = [i for i, (k, _) in enumerate(pos) if k == o]
    if len(idx) != 1: raise Refused('%s: %s found %d time(s) at the head (want 1)' % (doc, o, len(idx)))
    s = pos[idx[0]][1]
    e = pos[idx[0] + 1][1] if idx[0] + 1 < len(pos) else close_line(H)
    if H[:s] + H[e:] != L(btext): raise Refused('%s: head minus the %s block != merge-base (not ONE pure insertion)' % (doc, o))
    return H[s:e]


def block_span(sp, doc, text):
    H = L(text); pos = positions(text, doc); o = own(sp, doc)
    idx = [i for i, (k, _) in enumerate(pos) if k == o]
    if len(idx) != 1: raise Refused('%s: %s found %d time(s)' % (doc, o, len(idx)))
    e = pos[idx[0] + 1][1] if idx[0] + 1 < len(pos) else close_line(H)
    return pos[idx[0]][1] + 1, e


def insert(sp, doc, dtext, blk, order, rule='tail'):
    D = L(dtext); pos = positions(dtext, doc); o = own(sp, doc)
    if o in [k for k, _ in pos]: raise Refused('%s: develop ALREADY carries %s (merged twice? re-gate)' % (doc, o))
    if not pos: raise Refused('%s: develop has no numbered / keyed h2' % doc)
    c = close_line(D)
    if order == 'wrong':
        at = pos[-1][1]                      # BEFORE develop's last section: must fail the read-back
    elif rule == 'key' and doc == 'flow':
        above = [p for p in pos if p[0] > o]
        if not above: raise Refused('flow: develop has no numbered h2 above %s (KEY rule)' % o)
        at = above[0][1]
    else:
        at = c
    return '\n'.join(D[:at] + blk + D[at:])


def readback(sp, doc, text, dtext=None, rule='tail'):
    """(ok, description). TAIL: own exactly once and LAST; develop's sequence (if given) is the prefix. Ascent is INFO."""
    try:
        s = seq(text, doc)
    except ValueError as x:
        return False, 'reader refused: %s' % x
    o = own(sp, doc)
    once = s.count(o) == 1
    last = bool(s) and s[-1] == o
    pre = True
    if dtext is not None:
        ds = seq(dtext, doc); pre = [x for x in s if x != o] == ds
    if rule == 'key' and doc == 'flow':
        last = once and s == sorted(s)
    asc = (s == sorted(s)) if doc == 'flow' else None
    ok = once and last and pre
    tail = ' '.join(map(str, s[-5:]))
    return ok, '%s tail [%s] | %s once %s | LAST %s | develop prefix kept %s%s' % (
        'numbers' if doc == 'flow' else 'keys', tail, o, once, last if rule == 'tail' else '(key rule)', pre,
        (' | INFO numerically ascending %s' % asc) if doc == 'flow' else '')


# ---------------- predict ----------------
def predict(repo, sp, D, out, order='tail', quiet=False, rule='tail'):
    head, base = sp['head'], sp['merge_base']
    if not outside_forbidden(repo):
        print('PREDICT REFUSED: predict writes objects; %s is inside %s — use your OWN scratch clone' % (repo, K['forbidden_root'])); return 'REFUSED'
    u = unresolved(repo, (('develop', D), ('head', head), ('merge-base', base)))
    if u: print('PREDICT REFUSED: ' + u); return 'UNRESOLVABLE'
    adv = set(git(repo, 'diff', '--name-only', base, D).splitlines())
    hit = sorted(adv & (set(sp.get('code_paths', [])) | set(K['hook_blobs'])))
    if hit: print('PREDICT REFUSED: RE-GATE: develop advance touches kit path(s) %s since the merge-base' % hit); return None
    new = {}
    try:
        for doc in DOCS:
            blk = block(sp, doc, show(repo, head, K[doc]), show(repo, base, K[doc]))
            new[doc] = insert(sp, doc, show(repo, D, K[doc]), blk, order, rule)
    except (Refused, ValueError) as e:
        print('PREDICT REFUSED: %s' % e); return None
    os.makedirs(out, exist_ok=True)
    idx = os.path.join(out, 'predict.index.%d' % os.getpid()); env = {'GIT_INDEX_FILE': idx}
    rc, o, e = wgit(repo, 'read-tree', D, env=env); assert rc == 0, e
    for doc in DOCS:
        rc, sha, e = wgit(repo, 'hash-object', '-w', '--stdin', input_bytes=new[doc].encode('utf-8')); assert rc == 0, e
        rc, o, e = wgit(repo, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (sha.strip(), K[doc]), env=env); assert rc == 0, e
    for p in sp.get('code_paths', []):
        meta = git(repo, 'ls-tree', head, '--', p).split('\t')[0].split()
        rc, o, e = wgit(repo, 'update-index', '--add', '--cacheinfo', '%s,%s,%s' % (meta[0], meta[2], p), env=env); assert rc == 0, e
    rc, tree, e = wgit(repo, 'write-tree', env=env); assert rc == 0, e
    tree = tree.strip()
    q = os.path.join(out, '_quarantine'); os.makedirs(q, exist_ok=True)
    shutil.move(idx, os.path.join(q, os.path.basename(idx) + '.' + sp['key'] + '.' + order + '.' + tree[:8]))   # quarantine, never rm
    if not quiet:
        print('PREDICTED %s (PR %s %s, order %s, rule %s, develop-after %s, head %s)' % (tree, sp['key'], sp['ticket'], order, rule, D[:12], head[:12]))
        for r in doc_report(repo, sp, tree, 'predict', D): print(r)
    return tree


def doc_report(repo, sp, rev, label, D=None, rule='tail'):
    rows = []
    for doc in DOCS:
        rc, txt, e = git(repo, 'show', '%s:%s' % (rev, K[doc]), check=False)
        if rc: rows.append('  %s %s: ABSENT' % (label, doc)); continue
        dt = show(repo, D, K[doc]) if D else None
        ok, why = readback(sp, doc, txt, dt, rule)
        rows.append('  %s %s blob %s: h2 %d | %s | markers %d | div %+d | READ-BACK %s' % (
            label, doc, git(repo, 'rev-parse', '%s:%s' % (rev, K[doc])).strip()[:12], h2_open_count(txt), why,
            len(MARK.findall(txt)), divbal(txt), 'OK' if ok else 'FAIL'))
    return rows


def sim_commit(repo, parents, msg, tree):
    args = ['commit-tree', tree]
    for p in parents: args += ['-p', p]
    rc, o, e = wgit(repo, *args, '-m', msg, env=SIM_ENV)
    assert rc == 0, e
    return o.strip()


# ---------------- chain: both orders ----------------
def chain(repo, D, spA, spB, out):
    """-> dict of trees. A on D; B on SIM squash(A); B on D; A on SIM squash(B)."""
    r = {}
    print('CHAIN on develop %s (TAIL rule) — A %s %s, B %s %s' % (D[:12], spA['ticket'], spA['head'][:12], spB['ticket'] if spB else '-', spB['head'][:12] if spB else 'NOT INCLUDED'))
    r['A|D'] = predict(repo, spA, D, out, quiet=True)
    print('  A alone on D          -> %s' % r['A|D'])
    for x in doc_report(repo, spA, r['A|D'], '    A|D', D) if ok_tree(r['A|D']) else []: print(x)
    if not spB:
        return r
    r['B|D'] = predict(repo, spB, D, out, quiet=True)
    print('  B alone on D          -> %s' % r['B|D'])
    for x in doc_report(repo, spB, r['B|D'], '    B|D', D) if ok_tree(r['B|D']) else []: print(x)
    if ok_tree(r['A|D']):
        sa = sim_commit(repo, [D], 'SIM squash of %s (gate69)\n' % spA['ticket'], r['A|D']); r['simA'] = sa
        r['B|A'] = predict(repo, spB, sa, out, quiet=True)
        print('  B on SIM squash(A) %s -> %s   [order: A first, then B]' % (sa[:12], r['B|A']))
        for x in doc_report(repo, spB, r['B|A'], '    B|A', sa) if ok_tree(r['B|A']) else []: print(x)
    if ok_tree(r['B|D']):
        sb = sim_commit(repo, [D], 'SIM squash of %s (gate69)\n' % spB['ticket'], r['B|D']); r['simB'] = sb
        r['A|B'] = predict(repo, spA, sb, out, quiet=True)
        print('  A on SIM squash(B) %s -> %s   [order: B first, then A]' % (sb[:12], r['A|B']))
        for x in doc_report(repo, spA, r['A|B'], '    A|B', sb) if ok_tree(r['A|B']) else []: print(x)
    if ok_tree(r.get('B|A')) and ok_tree(r.get('A|B')):
        same_code = git(repo, 'diff', '--name-only', r['B|A'], r['A|B']).split('\n')
        same_code = [p for p in same_code if p]
        print('  FINAL trees by order: A-then-B %s | B-then-A %s | paths differing %s (docs only expected: the ORDER of 21./22. and KS-1256/KS-1305)'
              % (r['B|A'][:12], r['A|B'][:12], same_code))
    return r


# ---------------- mergetree ----------------
def mergetree(repo, sp, D, out, label=''):
    head = sp['head']
    if not outside_forbidden(repo):
        print('MERGETREE REFUSED: merge-tree writes objects; use your OWN scratch clone'); return 2
    u = unresolved(repo, (('develop', D), ('head', head)))
    if u: print('MERGETREE REFUSED: ' + u); return 2
    rc, o, e = wgit(repo, 'merge-tree', '--write-tree', '--name-only', head, D)
    parts = o.split('\n\n', 1); first = parts[0].split('\n'); mt = first[0].strip(); conflicted = [x for x in first[1:] if x]
    msgs = [x for x in (parts[1] if len(parts) > 1 else '').split('\n') if x]
    print('GIT %s`merge-tree --write-tree --name-only %s %s` (PR %s) rc %d tree %s' % (label, head[:12], D[:12], sp['key'], rc, mt))
    print('  conflicted paths (%d): %s' % (len(conflicted), conflicted))
    for m in msgs[:12]: print('  | ' + m[:200])
    pk = predict(repo, sp, D, out, 'tail', quiet=True)
    print('TAIL-PREDICTED tree %s' % pk)
    for r in doc_report(repo, sp, mt, 'merge-tree', D): print(r)
    if ok_tree(pk):
        for r in doc_report(repo, sp, pk, 'tail-pred', D): print(r)
        for doc in DOCS:
            a = git(repo, 'rev-parse', '--verify', '--quiet', '%s:%s' % (mt, K[doc]), check=False)[1].strip()
            b = git(repo, 'rev-parse', '%s:%s' % (pk, K[doc])).strip()
            print('  %s blob: merge-tree %s vs tail-predicted %s -> %s%s' % (doc, a[:12], b[:12], 'SAME' if a == b else 'DIFFERENT',
                  ' (git CONFLICTED this doc)' if K[doc] in conflicted else ''))
        print('  paths differing merge-tree vs tail-predicted: %s' % sorted(set(x for x in git(repo, 'diff', '--name-only', mt, pk).splitlines() if x)))
        for doc in DOCS:
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
                okr, desc = readback(sp, doc, txt, show(repo, D, K[doc]))
                print('    %-17s == tail-predicted blob: %-5s | READ-BACK %s | %s' % (nm, txt == keyt, 'OK' if okr else 'FAIL', desc[:150]))
    verdict = 'AGREE' if ok_tree(pk) and mt == pk and rc == 0 else 'DIVERGENCE'
    print('%s: %smerge-tree %s (rc %d) vs tail-predicted %s%s' % (verdict, label, mt[:12], rc, str(pk)[:12], '' if verdict == 'AGREE' else ' — Wednesday rules; this kit does not pick'))
    return 0 if verdict == 'AGREE' else 1


# ---------------- qm ----------------
def qm(repo, sp, M, D, pred, t, out=None):
    head, base = sp['head'], sp['merge_base']
    u = unresolved(repo, (('develop', D), ('head', head), ('merge-base', base), ('merge-in head', M)))
    if u: print('QM REFUSED: ' + u); return 'UNRESOLVABLE'
    M = git(repo, 'rev-parse', M + '^{commit}').strip(); D = git(repo, 'rev-parse', D + '^{commit}').strip()
    if pred is None:
        pred = predict(repo, sp, D, out or os.path.join(SCRATCH, 'qm'), 'tail', quiet=True) if outside_forbidden(repo) else None
    tm = git(repo, 'rev-parse', M + '^{tree}').strip()
    t.check('M1', ok_tree(pred) and tm == pred, 'tree(M) %s vs TAIL prediction %s — THE AUTHORITY' % (tm[:12], str(pred)[:12]))
    par = git(repo, 'log', '-1', '--format=%P', M).split()
    t.check('M2', par == [head, D], 'parents %s (want [%s, %s])' % ([p[:12] for p in par], head[:12], D[:12]))
    names = [x for x in git(repo, 'diff', '--name-only', D, M).splitlines() if x]
    bad = [p for p in names if p not in sp['files']]
    drift = [p for p in sp['code_paths'] if git(repo, 'rev-parse', '--verify', '--quiet', '%s:%s' % (M, p), check=False)[1].strip() != git(repo, 'rev-parse', '%s:%s' % (head, p)).strip()]
    t.check('M3', not bad and not drift, 'D..M paths %d; non-PR %s; code paths off the head blob %s' % (len(names), bad, drift))
    tb = len(git(repo, 'log', '-1', '--format=%(trailers)', M).encode())
    co = len(re.findall(r'(?im)^co-authored-by:', git(repo, 'log', '-1', '--format=%B', M)))
    t.check('M4', tb == 1 and co == 0, 'M trailers raw %d byte(s), Co-Authored-By %d (want 1 / 0)' % (tb, co))
    rc = git(repo, 'merge-base', '--is-ancestor', base, D, check=False)[0]
    t.check('M5', rc == 0, 'merge-base %s is an ancestor of D %s: %s' % (base[:12], D[:12], rc == 0))
    adv = [x for x in git(repo, 'diff', '--name-only', base, D).splitlines() if x]
    hit = sorted(set(adv) & (set(sp['code_paths']) | set(K['hook_blobs'])))
    fd, cd = show(repo, D, K['flow']), show(repo, D, K['cheat'])
    carries = (['flow %s.' % sp['flow_num']] if sp['flow_num'] in flow_nums(fd) else []) + (['cheat %s' % sp['cheat_key']] if sp['cheat_key'] in cheat_keys(cd) else [])
    t.check('M6', not hit and not carries, ('RE-GATE: develop advance touches kit path(s) %s' % hit if hit else "develop's advance %d path(s), PR paths among them none" % len(adv))
            + ('; D already carries %s' % carries if carries else ''))
    new = git(repo, 'rev-list', '%s..%s' % (head, M), '^' + D).split()
    t.check('M7', new == [M], 'commits in head..M not on D: %s (want exactly [M])' % [c[:12] for c in new])
    why = []
    for doc, dtext in (('flow', fd), ('cheat', cd)):
        mt = show(repo, M, K[doc])
        ok, desc = readback(sp, doc, mt, dtext)
        if not ok: why.append('%s %s' % (doc, desc))
        if MARK.search(mt): why.append('%s conflict markers %d' % (doc, len(MARK.findall(mt))))
        hb = show(repo, head, K[doc]); bb = show(repo, base, K[doc])
        try:
            blk = block(sp, doc, hb, bb); ML = L(mt); n = len(blk)
            at = [i for i in range(len(ML) - n + 1) if ML[i:i + n] == blk]
            if len(at) != 1: why.append('%s: the head block occurs %d time(s) in M (want 1)' % (doc, len(at)))
            elif ML[:at[0]] + ML[at[0] + n:] != L(dtext): why.append('%s: M minus the %s block != develop byte for byte' % (doc, own(sp, doc)))
        except (Refused, ValueError) as x:
            why.append('%s block: %s' % (doc, x))
        if divbal(mt) - divbal(dtext) != divbal(hb) - divbal(bb):
            why.append('%s div delta %+d != the block\'s %+d' % (doc, divbal(mt) - divbal(dtext), divbal(hb) - divbal(bb)))
    t.check('M8', not why, 'READ-BACK at M: %s' % ('; '.join(why) if why else 'own block once and LAST on both docs, develop prefix kept, M minus the block == develop on both docs, 0 markers, div deltas == the block\'s'))
    return 'DONE'


# ---------------- containment ----------------
def regions(repo, a, b, path):
    d = git(repo, 'diff', '-U0', a, b, '--', path); out = []
    for m in re.finditer(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', d, re.M):
        qs, qc = int(m.group(3)), int(m.group(4) if m.group(4) is not None else 1)
        out.append((qs, qs + max(qc, 1) - 1, int(m.group(2) if m.group(2) is not None else 1)))
    return out


def containment(repo, sp, t):
    base, head = sp['merge_base'], sp['head']
    for doc in DOCS:
        rg = regions(repo, base, head, K[doc]); ht = show(repo, head, K[doc])
        try:
            b = block_span(sp, doc, ht); spn = True
        except (Refused, ValueError) as x:
            b = (0, 0); spn = False; print('INFO %s span: %s' % (doc, x))
        inside = spn and all(b[0] <= q0 and q1 <= b[1] and removed == 0 for q0, q1, removed in rg)
        t.check('CT-' + doc, bool(rg) and inside, 'merge-base..head %s: %d -U0 region(s) %s | %s block at head :%d-:%d | every region inside it, 0 lines removed: %s' % (
            doc, len(rg), ['+%d..%d (-%d)' % (q0, q1, r) for q0, q1, r in rg], own(sp, doc), b[0], b[1], inside))
        try:
            block(sp, doc, ht, show(repo, base, K[doc])); ok, why = True, 'head minus the block == merge-base byte for byte'
        except (Refused, ValueError) as x:
            ok, why = False, str(x)
        t.check('CB-' + doc, ok, why)
        okr, desc = readback(sp, doc, ht, show(repo, base, K[doc]))
        t.check('CR-' + doc, okr, 'at the head: %s' % desc)
    commits = git(repo, 'rev-list', '--reverse', '--first-parent', '%s..%s' % (base, head)).split()
    rows = []
    for c in commits:
        ps = git(repo, 'log', '-1', '--format=%P', c).split()
        ns = set(x for x in git(repo, 'diff', '--name-only', ps[0], c).splitlines() if x)
        tests = sum(1 for p in ns if '__tests__' in p); fl = K['flow'] in ns; ch = K['cheat'] in ns
        rows.append('%s%s tests %d flow %s cheat %s' % (c[:12], ' (MERGE)' if len(ps) > 1 else '', tests, fl, ch))
    split = [r for r in rows if ' tests 0 ' not in r and 'flow False' in r and '(MERGE)' not in r]
    t.info('CS', 'skill §4 per commit (first-parent, vs first parent): %s%s' % (rows, (' | TEST COMMIT(S) WITHOUT DOCS: %s — the squash makes ONE commit; the gate RULES whether §4 "IN THE SAME COMMIT" is met by the squash' % split) if split else ''))


# ---------------- h2 proof ----------------
PLANT = '    <h2>\n      99. planted split heading &mdash; KS-99999\n    </h2>'


def plant(text):
    if text.count('\n' + CLOSE + '\n') != 1 and not text.endswith('\n' + CLOSE): raise Refused('close tag must occur exactly once')
    return text.replace('\n' + CLOSE, '\n' + PLANT + '\n' + CLOSE, 1)


def oldkeys(txt): return [m.group(1) for l in L(txt) for m in [OLD_SAMELINE_KEY.search(l)] if m]


def h2proof(repo, sp, D, t):
    for doc in DOCS:
        for label, rev in (('merge-base %s' % sp['merge_base'][:12], sp['merge_base']), ('develop %s' % D[:12], D), ('head %s' % sp['head'][:12], sp['head'])):
            txt = show(repo, rev, K[doc])
            tol = flow_nums(txt) if doc == 'flow' else cheat_keys(txt)
            old = old_sameline_nums(txt) if doc == 'flow' else oldkeys(txt)
            print('COUNT %s @ %s: <h2 opens %d | split across lines %d | tolerant (composee5 %s) %d | old same-line %d | tolerant %s' % (
                doc, label, h2_open_count(txt), split_h2_count(txt), ':66' if doc == 'flow' else ':82', len(tol), len(old), ' '.join(map(str, tol))))
        txt = show(repo, D, K[doc]); p = plant(txt)
        if doc == 'flow':
            hit = 99 in flow_nums(p); miss = 99 not in old_sameline_nums(p)
        else:
            hit = 'KS-99999' in cheat_keys(p); miss = 'KS-99999' not in oldkeys(p)
        t.check('H-%s' % doc, hit and miss, 'planted split h2 before %s close tag @ develop %s: tolerant HIT %s, old same-line MISS %s' % (doc, D[:12], hit, miss))
        one = txt.replace('\n' + CLOSE, '\n    <h2>99. planted one-line heading &mdash; KS-99999</h2>\n' + CLOSE, 1)
        both = (99 in flow_nums(one) and 99 in old_sameline_nums(one)) if doc == 'flow' else ('KS-99999' in cheat_keys(one) and 'KS-99999' in oldkeys(one))
        t.check('H-%s-ctl' % doc, both, 'CONTROL one-line plant: BOTH readers hit (%s)' % both)


# ---------------- #1394 simulation ----------------
def sim_develop_with(repo, sx, D, out, rule):
    """D + sim PR sx landed under `rule` (objects only) -> SIM develop commit, or None."""
    tr = predict(repo, sx, D, out, 'tail', quiet=True, rule=rule)
    if not ok_tree(tr): return None, tr
    return sim_commit(repo, [D], 'SIM develop: %s landed under the %s rule (gate69)\n' % (sx['ticket'], rule.upper()), tr), tr


def sim1394(repo, D, spA, spB, out):
    sx = spec('X1394')
    for rule in ('key', 'tail'):
        sd, tr = sim_develop_with(repo, sx, D, out, rule)
        print('SIM1394 rule %s: #1394 %s on %s -> tree %s, SIM develop commit %s' % (rule.upper(), sx['head'][:12], D[:12], tr, sd))
        if not sd: continue
        f = seq(show(repo, sd, K['flow']), 'flow'); c = seq(show(repo, sd, K['cheat']), 'cheat')
        print('  SIM develop flow tail %s | cheat tail %s' % (f[-5:], c[-4:]))
        chain(repo, sd, spA, spB, out)


# ---------------- self-test ----------------
def selftest(repo, D, spA, spB):
    out = os.path.join(SCRATCH, 'selftest'); os.makedirs(out, exist_ok=True)
    res = []
    def rep(cond, msg): res.append(bool(cond)); print('%s %s' % ('PASS' if cond else 'FAIL', msg))
    def quiet(f, *a, **k):
        b = io.StringIO()
        with contextlib.redirect_stdout(b): r = f(*a, **k)
        return r, b.getvalue()
    for sp in [x for x in (spA, spB) if x]:
        t = Tally(); _, o = quiet(h2proof, repo, sp, D, t)
        rep(not t.fails and t.n == 4, 'PR %s h2proof 4/4 (tolerant HIT / old MISS on both docs + one-line controls) | %s' % (sp['key'], t.fails))
        pk, _ = quiet(predict, repo, sp, D, out, 'tail'); pw, _ = quiet(predict, repo, sp, D, out, 'wrong')
        rep(ok_tree(pk), 'PR %s predict TAIL on %s -> %s' % (sp['key'], D[:12], pk))
        rep(ok_tree(pw) and pw != pk, 'PR %s WRONG-ORDER CONTROL tree %s DIFFERS from the TAIL tree' % (sp['key'], str(pw)[:12]))
        if ok_tree(pw):
            fo, _ = readback(sp, 'flow', show(repo, pw, K['flow']), show(repo, D, K['flow'])); co_, _ = readback(sp, 'cheat', show(repo, pw, K['cheat']), show(repo, D, K['cheat']))
            rep(not fo and not co_, 'PR %s WRONG-ORDER CONTROL fails the read-back on BOTH docs (flow ok=%s, cheat ok=%s)' % (sp['key'], fo, co_))
        pb, _ = quiet(predict, repo, sp, sp['merge_base'], out, 'tail')
        ht = git(repo, 'rev-parse', sp['head'] + '^{tree}').strip()
        rep(pb == ht, 'PR %s POSITIVE CONTROL: TAIL predict on its merge-base %s reproduces the head tree %s (got %s)' % (sp['key'], sp['merge_base'][:12], ht[:12], str(pb)[:12]))
        r, o = quiet(predict, repo, sp, 'f' * 40, out, 'tail')
        rep(r == 'UNRESOLVABLE' and 'develop unresolvable' in o, 'PR %s predict refuses an absent develop BY NAME: %r' % (sp['key'], o.strip()[:100]))
        r, o = quiet(predict, K['checkout'], sp, D, out, 'tail')
        rep(r == 'REFUSED', 'PR %s predict refuses to write in the shared checkout' % sp['key'])
        t = Tally(); quiet(containment, repo, sp, t)
        rep(not t.fails and t.n == 6, 'PR %s containment 6/6 at its head | %s' % (sp['key'], t.fails))
    if spA and spB:
        r, o = quiet(chain, repo, D, spA, spB, out)
        rep(all(ok_tree(r.get(k)) for k in ('A|D', 'B|D', 'B|A', 'A|B')), 'CHAIN both orders produce 4 trees: %s' % {k: str(v)[:12] for k, v in r.items()})
        if ok_tree(r.get('B|A')):
            fl = seq(show(repo, r['B|A'], K['flow']), 'flow')
            rep(fl[-2:] == [spA['flow_num'], spB['flow_num']] and fl != sorted(fl), 'A-then-B flow tail %s: 21. lands AFTER 22. under TAIL (numeric ascent FALSE — the ruling Q2 is real, not hypothetical)' % fl[-3:])
        if ok_tree(r.get('A|B')):
            fl = seq(show(repo, r['A|B'], K['flow']), 'flow'); ck = seq(show(repo, r['A|B'], K['cheat']), 'cheat')
            rep(fl[-2:] == [spB['flow_num'], spA['flow_num']] and fl == sorted(fl) and ck[-2:] == [spB['cheat_key'], spA['cheat_key']], 'B-then-A: flow tail %s ascending, cheat tail %s' % (fl[-3:], ck[-3:]))
        # Q-M on the SECOND PR over the first's SIM squash: GOOD merge-in passes 8/8; git's own merge, take-OURS, trailer, 1-parent FAIL
        sa = r.get('simA'); pred = r.get('B|A')
        if sa and ok_tree(pred):
            def runqm(M, Dx, p=None):
                tt = Tally(); rr, oo = quiet(qm, repo, spB, M, Dx, p, tt, out); return tt, rr, oo
            good = sim_commit(repo, [spB['head'], sa], 'Merge develop into KS-1256 (docs-only merge-in, SIM)\n', pred)
            tt, rr, oo = runqm(good, sa)
            rep(tt.n == 8 and not tt.fails, 'Q-M (B over SIM squash(A)) GOOD SIM %s: 8/8 PASS | fails %s' % (good[:12], tt.fails))
            rc0, o0, e0 = wgit(repo, 'merge-tree', '--write-tree', '--name-only', spB['head'], sa)
            conf0 = [x for x in o0.split('\n\n', 1)[0].split('\n')[1:] if x]
            rep(K['flow'] in conf0 and K['cheat'] in conf0, 'git merge-tree B over SIM squash(A) CONFLICTS on BOTH docs (same insertion point): %s' % [os.path.basename(x)[:20] for x in conf0])
            # take-OURS (B's side) on both conflicts: drops A's block -> M1 + M8
            mt0 = o0.split('\n', 1)[0].strip(); idx = os.path.join(out, 'ours.index.%d' % os.getpid()); env = {'GIT_INDEX_FILE': idx}
            assert wgit(repo, 'read-tree', mt0, env=env)[0] == 0; built = True
            for pth in conf0:
                m = L(git(repo, 'show', '%s:%s' % (mt0, pth)))
                a = [i for i, l in enumerate(m) if l.startswith('<<<<<<< ')]; b = [i for i, l in enumerate(m) if l == '=======']; c = [i for i, l in enumerate(m) if l.startswith('>>>>>>> ')]
                if not (len(a) == len(b) == len(c) == 1): built = False; break
                txt = '\n'.join(m[:a[0]] + m[a[0] + 1:b[0]] + m[c[0] + 1:])
                rc, sha, e = wgit(repo, 'hash-object', '-w', '--stdin', input_bytes=txt.encode()); assert rc == 0
                assert wgit(repo, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (sha.strip(), pth), env=env)[0] == 0
            if built:
                rc, tro, e = wgit(repo, 'write-tree', env=env); tro = tro.strip()
                q = os.path.join(out, '_quarantine'); os.makedirs(q, exist_ok=True); shutil.move(idx, os.path.join(q, os.path.basename(idx) + '.' + tro[:8]))
                so = sim_commit(repo, [spB['head'], sa], 'Merge develop (take OURS on both conflicts, SIM)\n', tro)
                tt, rr, oo = runqm(so, sa)
                rep({'M1', 'M8'} <= set(tt.fails), 'Q-M TAKE-OURS SIM (drops the first PR\'s block): FAIL M1 + M8 | got %s' % tt.fails)
            else:
                rep(False, 'TAKE-OURS SIM could not be built (conflict regions != 1)')
            wrong = sim_commit(repo, [spB['head'], sa], 'Merge develop (wrong order, SIM)\n', quiet(predict, repo, spB, sa, out, 'wrong')[0])
            tt, rr, oo = runqm(wrong, sa)
            rep({'M1', 'M8'} <= set(tt.fails) and 'M4' not in tt.fails, 'Q-M WRONG-ORDER SIM: FAIL M1 + M8 | got %s' % tt.fails)
            tr_ = sim_commit(repo, [spB['head'], sa], 'Merge develop\n\nCo-Authored-By: Someone <x@y.z>\n', pred)
            tt, rr, oo = runqm(tr_, sa); rep(tt.fails == ['M4'], 'Q-M TRAILER SIM: FAIL exactly [M4] | got %s' % tt.fails)
            sp1 = sim_commit(repo, [sa], 'squash-shaped\n', pred)
            tt, rr, oo = runqm(sp1, sa); rep('M2' in tt.fails, 'Q-M single-parent SIM: FAIL M2 | got %s' % tt.fails)
            tt, rr, oo = runqm(good, 'f' * 40)
            rep(rr == 'UNRESOLVABLE' and 'develop unresolvable' in oo and tt.n == 0, 'Q-M ABSENT DEVELOP refuses BY NAME, 0 checks: %r' % oo.strip()[:110])
            tt, rr, oo = runqm('e' * 40, sa)
            rep(rr == 'UNRESOLVABLE' and 'merge-in head unresolvable' in oo, 'Q-M absent merge-in head refuses BY NAME')
            # a SIM develop that edits one of B's code paths -> M6 RE-GATE by content
            idx = os.path.join(out, 'simdev.index.%d' % os.getpid()); env = {'GIT_INDEX_FILE': idx}
            assert wgit(repo, 'read-tree', sa, env=env)[0] == 0
            pth = spB['product_file']; txt = show(repo, sa, pth) + '// SIM develop edit\n'
            rc, sha, e = wgit(repo, 'hash-object', '-w', '--stdin', input_bytes=txt.encode()); assert rc == 0
            assert wgit(repo, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (sha.strip(), pth), env=env)[0] == 0
            rc, tsd, e = wgit(repo, 'write-tree', env=env); tsd = tsd.strip()
            q = os.path.join(out, '_quarantine'); os.makedirs(q, exist_ok=True); shutil.move(idx, os.path.join(q, os.path.basename(idx) + '.' + tsd[:8]))
            simdev = sim_commit(repo, [sa], 'SIM develop: touches %s\n' % pth, tsd)
            gx = sim_commit(repo, [spB['head'], simdev], 'Merge SIM develop\n', pred)
            tt, rr, oo = runqm(gx, simdev)
            m6 = [l for l in oo.split('\n') if l.startswith('FAIL M6')]
            rep('M6' in tt.fails and m6 and 'RE-GATE' in m6[0], 'Q-M REAL CODE-PATH CHANGE on develop: M6 RE-GATE by content: %r' % (m6 or [''])[0][:120])
            r2, o2 = quiet(predict, repo, spB, simdev, out, 'tail')
            rep(r2 is None and 'RE-GATE' in o2, 'predict REFUSES a develop that touches the PR\'s code path: %r' % o2.strip()[:100])
    elif spA:
        print('INFO selftest: PR B not supplied -> the chain / Q-M-over-squash arms are NOT RUN (A-only kit)')
    print('SELFTEST %d/%d' % (sum(res), len(res)))
    return 0 if res and all(res) else 1


def main():
    A = sys.argv[1:]
    if not A: print(__doc__); return 2
    def opt(k, d=None): return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d
    repo = opt('--repo', os.path.join(SCRATCH, 'clone'))
    which = opt('--pr', 'A')
    if which not in ('A', 'B'): print('unknown --pr (want A or B)'); return 2
    spA = spec('A', opt('--head-a') or (opt('--head') if which == 'A' else None))
    spB = None if '--a-only' in A else spec('B', opt('--head-b') or (opt('--head') if which == 'B' else None), opt('--b-pr'))
    sp = spA if which == 'A' else spB
    if sp is None: print('C4 REFUSED: --pr B with --a-only'); return 2
    for s in [x for x in (spA, spB) if x]:
        if not resolvable(repo, s['head']):
            print('C4 REFUSED: head unresolvable: PR %s head %r is not a commit in %s — fetch it BY SHA (X7)' % (s['key'], s['head'], repo)); return 2
    D = opt('--develop-after') or opt('--develop') or K['develop_at_draft']
    print('c4_docs_gate69 mode %s | PR %s %s head %s | develop %s | A head %s | B head %s%s' % (
        A[0], sp['key'], sp['ticket'], sp['head'][:12], D[:12], spA['head'][:12], spB['head'][:12] if spB else 'NOT INCLUDED',
        (' (B PR #%s)' % spB['pr']) if spB and spB.get('pr') else (' (B PR number NOT SUPPLIED)' if spB else '')))
    out = opt('--out', os.path.join(SCRATCH, 'c4'))
    if A[0] == '--selftest': return selftest(repo, D, spA, spB)
    if A[0] == 'containment':
        t = Tally(); containment(repo, sp, t); return t.end()
    if A[0] == 'h2proof':
        u = unresolved(repo, (('develop', D), ('merge-base', sp['merge_base'])))
        if u: print('H2PROOF REFUSED: ' + u); return 2
        t = Tally(); h2proof(repo, sp, D, t); return t.end()
    if A[0] == 'predict':
        r = predict(repo, sp, D, out, opt('--order', 'tail'))
        return 2 if r in ('UNRESOLVABLE', 'REFUSED') else (0 if ok_tree(r) else 1)
    if A[0] == 'chain':
        u = unresolved(repo, (('develop', D),))
        if u: print('CHAIN REFUSED: ' + u); return 2
        r = chain(repo, D, spA, spB, out)
        return 0 if all(ok_tree(v) for k, v in r.items() if '|' in k) else 1
    if A[0] == 'mergetree':
        ov = opt('--over-sim-of')
        if ov:
            first, second = (spA, spB) if ov == 'A' else (spB, spA)
            if not (first and second): print('MERGETREE REFUSED: --over-sim-of needs both PRs'); return 2
            tf = predict(repo, first, D, out, quiet=True)
            if not ok_tree(tf): print('MERGETREE REFUSED: the first PR does not predict on %s' % D[:12]); return 1
            sq = sim_commit(repo, [D], 'SIM squash of %s (gate69)\n' % first['ticket'], tf)
            print('SIM squash of PR %s on %s = commit %s tree %s' % (first['key'], D[:12], sq, tf))
            return mergetree(repo, second, sq, out, label='[PR %s over SIM squash(%s)] ' % (second['key'], first['key']))
        return mergetree(repo, sp, D, out)
    if A[0] == 'qm':
        t = Tally(); r = qm(repo, sp, opt('--merge-in-head'), D, opt('--predicted'), t, out)
        if r == 'UNRESOLVABLE': print('CHECKED 0 (refused by name)'); return 2
        return t.end()
    if A[0] == 'sim1394':
        u = unresolved(repo, (('develop', D), ('#1394 head', spec('X1394')['head'])))
        if u: print('SIM1394 REFUSED: ' + u); return 2
        sim1394(repo, D, spA, spB, out); return 0
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
