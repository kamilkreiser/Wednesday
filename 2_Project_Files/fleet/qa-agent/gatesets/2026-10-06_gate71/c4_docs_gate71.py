#!/usr/bin/env python3
r"""c4_docs_gate71.py — the two platform docs for ONE ROW (`--pr 1404` KS-1436 / `--pr 1398` KS-1136) and the MERGE-IN PREDICTION.
THE HEAD IS A PARAMETER. WIDENED 2026-10-07 (the pre-widen file is in _superseded_2026-10-07/kit_pre_widen/).
READERS: composee5's newline-tolerant h2 readers, extracted at the pinned lines by lib_gate71; the CHEAT reader is WIDENED there
(`&mdash;` or U+2014, derived from the pinned pattern) because #1402 wrote U+2014 and the pinned reader reads 0 keys on develop.

THE DOC RULE (Wednesday ruling 4 + Q-06N, 2026-10-07): flow numbers are UNIQUE and each PR block is KEYED to its ticket (flow h2 carries
`(KS-n)`, cheat h2 `— KS-n`); the block goes key-anchored immediately before develop's `</body>` (ANY indentation: base `  </body>`,
develop `</body>`). ASCENDING ORDER IS NOT ASSERTED — develop will read `… 22. 27. 23. …` BY DESIGN; ascent is printed as INFO only.

MODES (all: --repo <YOUR clone> --head <40-hex> --pr <row>)
  docs      D1 BOUNDARY-FREE (head minus ONE byte span == base; CONTROL 1-byte-altered span FALSE);  D2 the line block LAST before the
            close tag;  D3 flow == base + [own] (17 a GAP), UNIQUE, own block KEYED; cheat == base + [key];  D3-ctl split-h2 HIT/MISS;
            D4 only the row's key hyphenated in the block (CONTROL KS-9999);  D5 `<h2` openings == keyed h2s, div balance kept;
            D6 INFO: the cheat block opens with `<div class="section">` and closes it (a section card) — a FINDING when it does not.
  predict   --develop-after D [--stack-on S] [--num-map OLD:NEW]   D == base: NO MERGE-IN (tree == END_TREE). Otherwise D (or the
            stacked commit S, e.g. develop + #1404's predicted squash) must descend from the base and leave the row's CODE paths alone.
            A doc unchanged since the base takes the head blob; a doc develop rewrote in the NEW matrix format takes the row's block
            RE-COMPOSED by recompose_gate71.py (text conservation asserted) and inserted before `</body>`; an OLD-format develop takes the
            block verbatim (TAIL). Read-back: own once and LAST, develop's sequence the prefix, UNIQUE numbers; ascent INFO.
  guard     --tree T --out DIR   materialise T's two docs + develop's static guard (systemTest/__tests__/html_docs_matrix.test.sh and
            its support/html_docs_check.mjs, from T) under DIR and run THE GUARD ITSELF (`bash …/html_docs_matrix.test.sh`): rc, ratio.
  targets   --develop-after D --out DIR   THE CHAIN in merge order (kit merge_order): #1404 onto D -> tree A (guard), its squash as an
            OBJECTS-ONLY SIM commit A' (parent D); #1398 onto A' with the kit's CANDIDATE num-map -> tree B (guard); #1398 AS AUTHORED
            (no renumber) -> must REFUSE on UNIQUE; POSITIVE CONTROL: the OLD-format block tail-appended to D must FAIL the guard. Plus
            git merge-tree for each step as a CROSS-CHECK that is NEVER PICKED (per doc: conflict / AGREE; outside the docs: AGREE).
  mergetree --develop-after D [--stack-on S]   git merge-tree vs predict, printed; DIVERGENCE per doc is printed, never picked.
  qm        --merge-in-head M --develop-after D [--stack-on S]  Q1 parents == [head, D|S]; Q2 tree(M) == the prediction; Q3 read-back +
            UNIQUE; Q4 M's doc minus the own block == D's doc byte for byte; Q5 code blobs == the head's; Q6 the guard passes on tree(M).
  --selftest  SIM develop (OLD format, objects only) arms as before, plus: the UNIQUE/KEYED rule accepts `22 27 23` and a planted
            ASCENDING-DEMANDING rule rejects it (G71_DOCS_DEMAND_ASCENDING=1 makes the kit's own rule demand ascent: the self-test must
            then FAIL); a duplicate number FAILS; the pinned cheat reader is blind on develop while the widened one reads its keys.
rc 0 PASS / 1 FAIL or DIVERGENCE / 2 refused by name."""
import json, os, re, subprocess, sys, tarfile, io, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate71 import (K, P, D, Tally, git, git_bytes, wgit, refuse_absent, resolvable, outside_forbidden, opt, blob_at, close_idx,
                        flow_nums, flow_num_pos, cheat_keys, cheat_keys_pinned, cheat_key_pos, old_sameline_nums, h2_open_count)
import recompose_gate71 as RC

BASE = P['parents'][0]
DOCS = {'flow': D['flow'], 'cheat': D['cheat']}
SECTION_OPEN = re.compile(r'^\s*<div class="section">\s*$')
SIM_ENV = {'GIT_AUTHOR_NAME': 'gate71 SIM', 'GIT_AUTHOR_EMAIL': 'sim@gate71.invalid', 'GIT_COMMITTER_NAME': 'gate71 SIM',
           'GIT_COMMITTER_EMAIL': 'sim@gate71.invalid', 'GIT_AUTHOR_DATE': '2026-10-07T00:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-07T00:00:00Z'}
DEMAND_ASC = os.environ.get('G71_DOCS_DEMAND_ASCENDING') == '1'     # a planted WRONG rule, for the self-test's own arm only


class Refused(Exception): pass


def code_paths(R): return [p for p in R['numstat'] if not p.startswith('Projects Documents/')]
def own(doc, R, num=None): return (num if num is not None else R['flow_num']) if doc == 'flow' else R['cheat_key']
def seq(text, doc): return flow_nums(text) if doc == 'flow' else cheat_keys(text)


def positions(text, doc):
    raw = flow_num_pos(text) if doc == 'flow' else cheat_key_pos(text)
    T = text.split('\n')
    return [(k, ln - 1 if ln > 0 and SECTION_OPEN.match(T[ln - 1]) else ln) for k, ln in raw]


def close_line(L):
    try: return close_idx(L)
    except ValueError as x: raise Refused(str(x))


def block(doc, htext, btext, o):
    H = htext.split('\n'); pos = positions(htext, doc)
    idx = [i for i, (k, _) in enumerate(pos) if k == o]
    if len(idx) != 1: raise Refused('%s: own %s found %d time(s) at the head (want 1)' % (doc, o, len(idx)))
    s = pos[idx[0]][1]; e = pos[idx[0] + 1][1] if idx[0] + 1 < len(pos) else close_line(H)
    if H[:s] + H[e:] != btext.split('\n'): raise Refused('%s: head minus the %s block != base (not ONE pure insertion)' % (doc, o))
    return H[s:e], e == close_line(H)


def boundary_free(hb, bb):
    i = 0
    while i < len(bb) and hb[i] == bb[i]: i += 1
    j = 0
    while j < len(bb) - i and hb[-1 - j] == bb[-1 - j]: j += 1
    frag = hb[i:len(hb) - j]
    return frag, hb.replace(frag, b'', 1) == bb, hb.count(frag)


def flow_rule(s):
    """THE RULE: numbers UNIQUE. Ascent is NOT part of it (ruling 4). G71_DOCS_DEMAND_ASCENDING=1 plants the WRONG rule (self-test arm)."""
    ok = len(s) == len(set(s))
    return ok and (s == sorted(s)) if DEMAND_ASC else ok


def flow_rule_ascending(s): return len(s) == len(set(s)) and s == sorted(s)      # the WRONG rule, kept as a named negative arm


def keyed(doc, blk_lines, R):
    """the own block's h2 carries the row's ticket: flow `(KS-n)` in the h2, cheat `— KS-n` as the h2's key."""
    t = '\n'.join(blk_lines)
    h2 = re.search(r'<h2[^>]*>(.*?)</h2>', t, re.S)
    if not h2: return False
    return ('(%s)' % R['ticket']) in h2.group(1) if doc == 'flow' else cheat_keys(h2.group(0)) == [R['ticket']]


def insert(doc, dtext, blk, o, order='tail'):
    Dl = dtext.split('\n'); pos = positions(dtext, doc)
    if o in [k for k, _ in pos]: raise Refused('%s: develop ALREADY carries %s — UNIQUE would break (merged twice, or a number collision: RULING NEEDED)' % (doc, o))
    at = pos[-1][1] if order == 'wrong' else close_line(Dl)
    return '\n'.join(Dl[:at] + blk + Dl[at:])


def readback(doc, text, dtext, o):
    try: s = seq(text, doc)
    except ValueError as x: return False, 'reader refused: %s' % x
    ok = s.count(o) == 1 and s[-1] == o
    pre = dtext is None or [x for x in s if x != o] == seq(dtext, doc)
    uniq = flow_rule(s) if doc == 'flow' else len(s) == len(set(s))
    asc = s == sorted(s) if doc == 'flow' else None
    return ok and pre and uniq, 'own %s x%d, LAST %s, develop prefix kept %s, UNIQUE %s, tail %s%s' % (
        o, s.count(o), s[-1:] == [o], pre, uniq, s[-4:], (', ascending %s (INFO, never asserted)' % asc) if doc == 'flow' else '')


def is_matrix_format(text): return 'class="pmatrix"' in text


# ---------------- docs ----------------
def docs(repo, head, R):
    t = Tally()
    for doc, path in DOCS.items():
        bb, hb = git_bytes(repo, BASE, path), git_bytes(repo, head, path)
        frag, ok, n = boundary_free(hb, bb)
        alt = bytearray(frag); k = len(alt) // 2; alt[k] = (alt[k] + 1) % 256; ctl = hb.replace(bytes(alt), b'', 1) == bb
        t.check('D1-%s' % doc, ok and n == 1 and not ctl, 'head minus ONE span (%d B) == base: %s; span occurs %d time(s); CONTROL 1-byte-altered span reproduces base: %s' % (len(frag), ok, n, ctl))
        bt, ht = bb.decode(), hb.decode(); o = own(doc, R)
        try:
            blk, last = block(doc, ht, bt, o)
            t.check('D2-%s' % doc, last, 'line block %d lines, head minus block == base line for line, block is LAST before the close tag: %s' % (len(blk), last))
        except Refused as x:
            t.check('D2-%s' % doc, False, str(x)); blk = []
        sb, sh = seq(bt, doc), seq(ht, doc)
        if doc == 'flow':
            t.check('D3-flow', sh == sb + [o] and 17 not in sh and flow_rule(sh) and keyed(doc, blk, R) and sb == D['flow_seq_base'],
                    'base %s.. -> head ..%s; 17 a GAP: %s; UNIQUE %s; own block KEYED (%s) %s; base == kit %s; ascending %s (INFO, never asserted)' % (
                        sb[:3], sh[-4:], 17 not in sh, flow_rule(sh), R['ticket'], keyed(doc, blk, R), sb == D['flow_seq_base'], sh == sorted(sh)))
            plant = ht.replace('</body>', '<h2>\n    99. planted split heading</h2>\n</body>', 1)
            t.check('D3-flow-ctl', 99 in flow_nums(plant) and 99 not in old_sameline_nums(plant) and o in old_sameline_nums(ht),
                    'PLANTED `<h2>\\n  99.`: tolerant reader HIT %s, same-line reader MISSED %s (the same-line reader still sees %s: %s)' % (
                        99 in flow_nums(plant), 99 not in old_sameline_nums(plant), o, o in old_sameline_nums(ht)))
        else:
            t.check('D3-cheat', sh == sb + [o] and sb == D['cheat_seq_base'] and keyed(doc, blk, R), 'base tail %s -> head tail %s; base == kit %s; KEYED %s' % (sb[-2:], sh[-3:], sb == D['cheat_seq_base'], keyed(doc, blk, R)))
        btxt = '\n'.join(blk)
        hy = sorted(set(re.findall(r'\bKS-\d+\b', btxt))); de = sorted(set(re.findall(r'\bKS \d+\b', btxt)))
        ctl = re.findall(r'\bKS-\d+\b', btxt + ' KS-9999 ')
        t.check('D4-%s' % doc, hy == [R['ticket']] and 'KS-9999' in ctl, 'hyphenated keys in the block %s (want only %s) | de-hyphenated %s | CONTROL planted KS-9999 found %s | doc-wide distinct hyphenated keys %d' % (
            hy, R['ticket'], de, 'KS-9999' in ctl, len(set(re.findall(r'\bKS-\d+\b', ht)))))
        try: nk = len(seq(ht, doc))
        except ValueError: nk = -1
        dv = lambda s: len(re.findall(r'<div\b', s)) - len(re.findall(r'</div>', s))
        t.check('D5-%s' % doc, h2_open_count(ht) == nk and dv(ht) == dv(bt), '`<h2` openings %d == numbered/keyed %d; div balance %d == base %d' % (h2_open_count(ht), nk, dv(ht), dv(bt)))
        if doc == 'cheat' and blk:
            wrapped = SECTION_OPEN.match(blk[0]) is not None and blk[-1].strip() == '</div>'
            t.info('D6-cheat', ('the block is a section card: opens `<div class="section">`, closes `</div>`' if wrapped else
                                'FINDING (polish, not a blocker): the block is NOT wrapped in `<div class="section">` (first line %r) — every other KS section is; it renders outside a section card' % blk[0].strip()[:60]))
    return t.end()


# ---------------- predict / guard / mergetree / qm ----------------
def build_tree(repo, dev, blobs):
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


def commit_sim(repo, tree, parent, msg):
    rc, o, e = wgit(repo, 'commit-tree', tree, '-p', parent, '-m', msg, env=SIM_ENV)
    if rc: raise Refused('commit-tree: %s' % e.strip()[:120])
    return o.strip()


def predict(repo, head, dev, R, num_map=None, verbatim=False):
    """(tree, {doc: text}, lines). dev: develop, or a stacked SIM commit. num_map {old: new} renumbers the flow block (a RULING)."""
    out = []; num_map = num_map or {}
    if dev == BASE:
        out.append('develop == the base %s: NO MERGE-IN NEEDED; the squash tree == END_TREE %s' % (BASE[:12], R['end_tree'][:12]))
        return git(repo, 'rev-parse', head + '^{tree}').strip(), None, out
    if git(repo, 'merge-base', '--is-ancestor', BASE, dev, check=False)[0] != 0: raise Refused('develop %s does not descend from the base' % dev[:12])
    moved = [p for p in code_paths(R) if blob_at(repo, BASE, p) != blob_at(repo, dev, p)]
    if moved: raise Refused('develop moved a CODE path of #%s since the base %s: RE-GATE' % (R['pr'], moved))
    blobs, texts = {}, {}
    for p in code_paths(R): blobs[p] = (git(repo, 'ls-tree', head, '--', p).split()[0], git(repo, 'rev-parse', '%s:%s' % (head, p)).strip())
    for doc, path in DOCS.items():
        bt, ht, dt = (git_bytes(repo, r, path).decode() for r in (BASE, head, dev))
        if dt == bt:
            texts[doc] = ht; out.append('%s: develop UNCHANGED since the base -> the head blob' % doc)
        else:
            blk, _ = block(doc, ht, bt, own(doc, R))
            o = own(doc, R, num_map.get(R['flow_num']) if doc == 'flow' else None)
            if is_matrix_format(dt) and not verbatim:
                nb = RC.recompose('\n'.join(blk), num_map if doc == 'flow' else {})
                if RC.visible_text('\n'.join(blk), num_map if doc == 'flow' else {}) != RC.visible_text(nb):
                    raise Refused('%s: RE-COMPOSITION changed the visible text (dropped or merged words)' % doc)
                how = 'RE-COMPOSED to the matrix format (%d -> %d lines, visible text conserved%s)' % (len(blk), nb.count('\n') + 1,
                      (', RENUMBERED %s' % num_map) if (doc == 'flow' and num_map) else '')
                blk = nb.split('\n')
            else:
                how = 'VERBATIM (%s)' % ('develop is OLD format' if not is_matrix_format(dt) else 'POSITIVE CONTROL: old format into a matrix develop')
            m = insert(doc, dt, blk, o); texts[doc] = m
            ok, why = readback(doc, m, dt, o)
            out.append('%s: key-anchored insert before </body>, %s -> read-back %s: %s' % (doc, how, 'OK' if ok else 'FAIL', why))
            if not ok: raise Refused('%s read-back FAILED: %s' % (doc, why))
        blobs[path] = ('100644', hash_blob(repo, texts[doc].encode()))
    return build_tree(repo, dev, blobs), texts, out


def run_guard(repo, tree, out, tag):
    """materialise the tree's docs + its static guard; run the guard ITSELF. -> (rc, (passed, failed) | None, log path)."""
    d = os.path.join(out, 'guard_' + tag); os.makedirs(d)
    paths = [D['guard_suite'], D['guard_checker'], D['flow'], D['cheat']]
    p = subprocess.run(['git', '-C', repo, 'archive', '--format=tar', tree, '--'] + paths, capture_output=True)
    if p.returncode: raise Refused('git archive %s: %s' % (tree[:12], p.stderr.decode()[:160]))
    tarfile.open(fileobj=io.BytesIO(p.stdout)).extractall(d)
    tmp = os.path.join(d, '.tmp'); os.makedirs(tmp)
    log = os.path.join(out, 'guard_%s.log' % tag)
    with open(log, 'wb') as fo:
        rc = subprocess.run(['bash', os.path.join(d, D['guard_suite'])], env=dict(os.environ, TMPDIR=tmp), stdout=fo, stderr=subprocess.STDOUT).returncode
    open(log + '.rc', 'w').write('%d\n' % rc)
    text = open(log, encoding='utf-8', errors='replace').read()
    m = re.search(r'^\s*(\d+) passed, (\d+) failed\s*$', text, re.M)
    return rc, ((int(m.group(1)), int(m.group(2))) if m else None), log, text


def mergetree(repo, head, dev):
    rc, o, e = wgit(repo, 'merge-tree', '--write-tree', '--name-only', dev, head)
    lines = o.strip().split('\n'); return rc, (lines[0] if lines else ''), [l for l in lines[1:] if l and not l.startswith('Auto-merging') and not l.startswith('CONFLICT')], e.strip()


def compare_mergetree(repo, mt, tree):
    """(docs verdict {doc: AGREE|DIVERGENCE…}, outside-docs differing paths)."""
    dv = {}
    for doc, path in DOCS.items():
        a, b = blob_at(repo, mt, path), blob_at(repo, tree, path)
        marks = git_bytes(repo, mt, path).count(b'<<<<<<<') if a else 0
        dv[doc] = 'AGREE' if a == b else 'DIVERGENCE (merge-tree blob %s, %d conflict marker(s); predicted %s)' % (a[:12], marks, b[:12])
    diff = [l for l in git(repo, 'diff', '--name-only', mt, tree).split('\n') if l and l not in DOCS.values()]
    return dv, diff


def run_predict(repo, head, dev, R, num_map, outf):
    t = Tally()
    try: tree, texts, lines = predict(repo, head, dev, R, num_map)
    except Refused as x: print('REFUSED: %s' % x); return 1
    for l in lines: print('  ' + l)
    t.check('M1', bool(re.fullmatch(r'[0-9a-f]{40}', tree)), 'PREDICTED squash tree of #%s on %s: %s' % (R['pr'], dev[:12], tree))
    if outf: open(outf, 'w').write('develop %s\nhead %s\npredicted_tree %s\n' % (dev, head, tree))
    return t.end()


def run_mergetree(repo, head, dev, R, num_map):
    t = Tally()
    try: tree, texts, _ = predict(repo, head, dev, R, num_map)
    except Refused as x: print('REFUSED: %s' % x); return 1
    rc, mt, rest, err = mergetree(repo, head, dev)
    print('  git merge-tree rc %d tree %s conflicted/paths %s' % (rc, mt[:12], rest[:6]))
    dv, diff = compare_mergetree(repo, mt, tree)
    for doc, v in dv.items(): print('  %s: %s' % (doc, v))
    print('  outside the two docs: merge-tree vs predicted differ on %d path(s) %s' % (len(diff), diff[:5]))
    agree = rc == 0 and mt == tree
    t.check('MT', agree, '%s: merge-tree %s vs predicted %s (the key-anchored prediction is the TARGET; merge-tree is printed, never picked)' % (
        'AGREE' if agree else 'DIVERGENCE', mt[:12], tree[:12]))
    return t.end()


def run_qm(repo, head, dev, m, R, num_map, out):
    t = Tally()
    rr = refuse_absent(repo, [('merge-in head', m), ('develop', dev)])
    if rr: return rr
    pr = git(repo, 'log', '-1', '--format=%P', m).split()
    t.check('Q1', pr == [head, dev], 'parents %s == [head, develop]' % [x[:12] for x in pr])
    try: tree, texts, _ = predict(repo, head, dev, R, num_map)
    except Refused as x: print('REFUSED: %s' % x); return 1
    mt = git(repo, 'rev-parse', m + '^{tree}').strip()
    t.check('Q2', mt == tree, 'tree(M) %s == predicted %s' % (mt[:12], tree[:12]))
    for doc, path in DOCS.items():
        mtext, dtext = git_bytes(repo, m, path).decode(), git_bytes(repo, dev, path).decode()
        o = own(doc, R, num_map.get(R['flow_num']) if doc == 'flow' else None)
        ok, why = readback(doc, mtext, dtext, o); t.check('Q3-%s' % doc, ok, why)
        try: block(doc, mtext, dtext, o); t.check('Q4-%s' % doc, True, 'M minus its block == develop byte for byte')
        except Refused as x: t.check('Q4-%s' % doc, False, str(x))
    cb = [p for p in code_paths(R) if blob_at(repo, m, p) != blob_at(repo, head, p)]
    t.check('Q5', not cb, 'code paths at M == the head blobs %s' % (cb or ''))
    if out:
        rc, pf, log, _ = run_guard(repo, mt, out, 'qm')
        t.check('Q6', rc == 0 and pf is not None and pf[1] == 0, 'develop\'s static guard on tree(M): rc %d %s (%s)' % (rc, pf, log))
    else: t.info('Q6', 'NOT RUN by name (no --out): the guard on tree(M)')
    return t.end()


def num_map_arg(s):
    if not s: return {}
    a, b = s.split(':'); return {int(a): int(b)}


def kit_num_map(pr):
    return {int(a): b for a, b in K['docs']['recompose'][pr]['num_map'].items()}


def run_targets(repo, dev, out):
    """the chain in merge order; trees and guard results to OUT/targets.json."""
    t = Tally(); res = {'develop': dev}
    r04, r98 = K['rows']['1404'], K['rows']['1398']
    try:
        A, ta, la = predict(repo, r04['head_expected'], dev, r04, kit_num_map('1404'))
    except Refused as x: print('REFUSED (#1404 onto develop): %s' % x); return 1
    for l in la: print('  #1404: ' + l)
    rc, pf, log, txt = run_guard(repo, A, out, 'T1_1404')
    t.check('T1', rc == 0 and pf is not None and pf[1] == 0, '#1404 onto develop %s -> TARGET TREE %s | develop\'s guard on it: rc %d %s (%s)' % (dev[:12], A, rc, pf, log))
    Asim = commit_sim(repo, A, dev, 'gate71 SIM: #1404 squash onto develop %s (objects only; the predicted target A)' % dev[:12])
    res.update(target_1404=A, sim_1404_commit=Asim, guard_1404=[rc, pf])
    nm = kit_num_map('1398')
    try:
        B, tb, lb = predict(repo, r98['head_expected'], Asim, r98, nm)
    except Refused as x: print('REFUSED (#1398 onto develop + #1404): %s' % x); return 1
    for l in lb: print('  #1398: ' + l)
    rc, pf, log, txt = run_guard(repo, B, out, 'T2_1398')
    t.check('T2', rc == 0 and pf is not None and pf[1] == 0, '#1398 onto develop + #1404 (%s), CANDIDATE num-map %s -> TARGET TREE %s | guard rc %d %s (%s)' % (Asim[:12], nm, B, rc, pf, log))
    res.update(target_1398=B, num_map_1398=nm, guard_1398=[rc, pf])
    try:
        X, _, _ = predict(repo, r98['head_expected'], Asim, r98, {}); t.check('T2x', False, '#1398 AS AUTHORED (23.) built %s — it must REFUSE on UNIQUE' % X)
    except Refused as x: t.check('T2x', 'UNIQUE' in str(x) or 'ALREADY' in str(x), '#1398 AS AUTHORED (flow 23.) onto develop + #1404 REFUSES: %s' % str(x)[:150])
    try:
        N, _, _ = predict(repo, r04['head_expected'], dev, r04, {}, verbatim=True)
        rc, pf, log, txt = run_guard(repo, N, out, 'CTL_oldformat')
        t.check('T-CTL', rc != 0 and pf is not None and pf[1] > 0 and 'prose outside a table' in txt,
                'POSITIVE CONTROL: #1404\'s OLD-format block tail-appended to develop (tree %s) FAILS develop\'s guard: rc %d %s, `prose outside a table` x%d (%s)' % (
                    N[:12], rc, pf, txt.count('prose outside a table'), log))
        res.update(control_oldformat_tree=N, guard_control=[rc, pf])
    except Refused as x: t.check('T-CTL', False, 'control could not be built: %s' % x)
    for tag, head, base_c, tree in (('1404', r04['head_expected'], dev, A), ('1398', r98['head_expected'], Asim, B)):
        mrc, mt, rest, err = mergetree(repo, head, base_c)
        dv, diff = compare_mergetree(repo, mt, tree)
        print('CROSS-CHECK merge-tree #%s onto %s: rc %d tree %s conflicted %s | %s | outside the docs: %d path(s) differ %s' % (
            tag, base_c[:12], mrc, mt[:12], rest[:4], ' / '.join('%s %s' % (d, v) for d, v in dv.items()), len(diff), diff[:4]))
        res['mergetree_%s' % tag] = {'rc': mrc, 'tree': mt, 'conflicted': rest, 'docs': dv, 'outside_docs_differ': diff}
        t.info('MT-%s' % tag, 'merge-tree is a CROSS-CHECK, never picked: %s' % ('AGREE' if mrc == 0 and mt == tree else 'DIVERGENCE — see KIT_REPORT WIDENED §DIVERGENCE'))
    json.dump(res, open(os.path.join(out, 'targets.json'), 'w'), indent=1)
    print('TARGETS written: %s' % os.path.join(out, 'targets.json'))
    return t.end()


# ---------------- selftest ----------------
def sim_develop(repo, R):
    blobs = {}
    for doc, path in DOCS.items():
        t = git_bytes(repo, BASE, path).decode()
        add = ('  <h2>24. A planted foreign block (KS 9998)</h2>\n    <p>sim</p>\n' if doc == 'flow' else
               '  <div class="section">\n      <h2>Planted foreign section &mdash; KS-9998</h2>\n      <p>sim</p>\n    </div>\n')
        blobs[path] = ('100644', hash_blob(repo, t.replace('  </body>', add.rstrip('\n') + '\n  </body>', 1).encode()))
    return commit_sim(repo, build_tree(repo, BASE, blobs), BASE, 'gate71 SIM develop: foreign block 24 / KS-9998')


def selftest(repo, head, R):
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    rr = refuse_absent(repo, [('head', head), ('base', BASE)])
    if rr: return rr
    o = own('flow', R)
    sim = sim_develop(repo, R); print('SIM develop %s (objects only, parent %s, OLD format) for row #%s' % (sim, BASE[:12], R['pr']))
    tree, texts, lines = predict(repo, head, sim, R)
    for l in lines: print('  ' + l)
    ok, why = readback('flow', texts['flow'], git_bytes(repo, sim, DOCS['flow']).decode(), o)
    rep(ok and flow_nums(texts['flow'])[-2:] == [24, o], 'TAIL on SIM: flow ...24 %d (own LAST, NOT ascending — INFO), read-back OK: %s' % (o, why))
    ok, why = readback('cheat', texts['cheat'], git_bytes(repo, sim, DOCS['cheat']).decode(), R['cheat_key'])
    rep(ok and cheat_keys(texts['cheat'])[-2:] == ['KS-9998', R['cheat_key']], 'TAIL on SIM: cheat ...KS-9998 %s, read-back OK' % R['cheat_key'])
    ht, bt, st = (git_bytes(repo, r, DOCS['flow']).decode() for r in (head, BASE, sim))
    blk, _ = block('flow', ht, bt, o)
    w = insert('flow', st, blk, o, order='wrong'); ok, why = readback('flow', w, st, o)
    rep(not ok, 'PLANTED WRONG POSITION (block before develop\'s last section) FAILS the read-back: %s' % why)
    rep(boundary_free(git_bytes(repo, head, DOCS['cheat']), git_bytes(repo, BASE, DOCS['cheat']))[1], 'boundary-free: the real cheat insertion reproduces the base')
    hb = git_bytes(repo, head, DOCS['flow']); bb = git_bytes(repo, BASE, DOCS['flow'])
    edited = hb.replace(b'<h2>1.', b'<h2>1 .', 1)
    rep(edited != hb and not boundary_free(edited, bb)[1], 'PLANTED edit of a PRE-EXISTING heading: NOT one pure insertion (boundary-free FALSE)')
    try: block('flow', edited.decode(), bb.decode(), o); rep(False, 'line-anchored block must refuse an edited pre-existing line')
    except Refused: rep(True, 'PLANTED edit of a pre-existing line: the line-anchored block REFUSES')
    plant = ht.replace('</body>', '<h2>\n    99. x</h2>\n</body>', 1)
    rep(99 in flow_nums(plant) and 99 not in old_sameline_nums(plant), 'split `<h2>\\n 99.`: tolerant HIT, same-line MISSED')
    try: insert('flow', ht, blk, o); rep(False, 'inserting into a develop that already has the own number must refuse')
    except Refused: rep(True, 'PLANTED develop already carrying %d.: insert REFUSES (UNIQUE: merged twice / a collision)' % o)
    by_design = [1, 2, 16, 18, 21, 22, 27, 23]
    rep(flow_rule(by_design), 'THE RULE accepts the BY-DESIGN order `… 22. 27. 23.` (UNIQUE, not ascending) — fails if G71_DOCS_DEMAND_ASCENDING=1 plants the wrong rule')
    rep(not flow_rule_ascending(by_design), 'the named WRONG rule (ascending) REJECTS `… 22. 27. 23.` — the arm that would wrongly demand ascent fires')
    rep(not flow_rule([21, 22, 23, 24, 23]), 'PLANTED duplicate number 23 FAILS UNIQUE')
    rep(keyed('flow', ['<h2>27. x (KS-1436)</h2>'], K['rows']['1404']) and not keyed('flow', ['<h2>27. x (KS 1436)</h2>'], K['rows']['1404']), 'KEYED: `(KS-1436)` in the h2 passes; a de-hyphenated key FAILS')
    rep(close_line(['x', '  </body>']) == 1 and close_line(['x', '</body>']) == 1, 'close tag matched at any indentation (base `  </body>`, develop `</body>`)')
    try: close_line(['</body>', '</body>']); rep(False, 'two close tags must refuse')
    except Refused: rep(True, 'PLANTED two `</body>` lines REFUSE')
    dev = K['develop_at_draft']
    if resolvable(repo, dev):
        dc = git_bytes(repo, dev, DOCS['cheat']).decode()
        rep(cheat_keys_pinned(dc) == [] and cheat_keys(dc) == D['cheat_seq_develop'], 'develop %s cheat: the PINNED reader reads %d keys (BLIND to U+2014), the WIDENED reader reads %d == kit' % (
            dev[:12], len(cheat_keys_pinned(dc)), len(cheat_keys(dc))))
        rep(flow_nums(git_bytes(repo, dev, DOCS['flow']).decode()) == D['flow_seq_develop'], 'develop flow sequence == kit (… 21 22 23 24: develop already HOLDS 23)')
    else: rep(False, 'develop %s absent from the clone: the reader arms cannot run (fetch it by sha)' % dev[:12])
    cb = {K['product']['path']: ('100755', hash_blob(repo, git_bytes(repo, BASE, K['product']['path']) + b'# sim\n')),
          K['product_1404']['path']: ('100755', hash_blob(repo, git_bytes(repo, BASE, K['product_1404']['path']) + b'# sim\n'))}
    c2 = commit_sim(repo, build_tree(repo, sim, cb), sim, 'gate71 SIM: code paths touched')
    try: predict(repo, head, c2, R); rep(False, 'a develop that touched the row\'s code path must refuse')
    except Refused as x: rep('RE-GATE' in str(x), 'PLANTED develop touching the row\'s code path: predict REFUSES (%s)' % str(x)[:70])
    rep(predict(repo, head, BASE, R)[0] == R['end_tree'], 'develop == base: predicted tree == END_TREE (positive control)')
    rep(refuse_absent(repo, [('x', 'deadbeef' * 5)]) == 2, 'an ABSENT object is refused BY NAME (rc 2)')
    if DEMAND_ASC: print('NOTE G71_DOCS_DEMAND_ASCENDING=1: the WRONG rule is planted; this self-test MUST fail')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    repo = opt(A, '--repo'); head = opt(A, '--head', P['head_expected'])
    if not A or not repo: print(__doc__); return 2
    named = [('head', head), ('base', BASE)]
    dev = opt(A, '--develop-after'); stack = opt(A, '--stack-on')
    for n, s in (('develop', dev), ('stack', stack)):
        if s: named.append((n, s))
    rr = refuse_absent(repo, named)
    if rr: return rr
    on = stack or dev
    nm = num_map_arg(opt(A, '--num-map')) if opt(A, '--num-map') else kit_num_map(P['pr'])
    print('C4 %s row #%s (%s) head %s on %s num-map %s' % (A[0], P['pr'], P['ticket'], head[:12], (on or '-')[:12], nm or '{}'))
    try:
        if '--selftest' in A: return selftest(repo, head, P)
        if A[0] == 'docs': return docs(repo, head, P)
        if A[0] == 'predict' and on: return run_predict(repo, head, on, P, nm, opt(A, '--out'))
        if A[0] == 'mergetree' and on: return run_mergetree(repo, head, on, P, nm)
        if A[0] == 'qm' and on and opt(A, '--merge-in-head'): return run_qm(repo, head, on, opt(A, '--merge-in-head'), P, nm, opt(A, '--out'))
        if A[0] in ('guard', 'targets'):
            out = opt(A, '--out')
            if not out: print('REFUSED: --out <a fresh dir> is required'); return 2
            os.makedirs(out, exist_ok=True)
            if os.listdir(out): print('REFUSED: --out %s is not empty' % out); return 2
            if A[0] == 'guard' and opt(A, '--tree'):
                rc, pf, log, txt = run_guard(repo, opt(A, '--tree'), out, 'adhoc'); print(txt); print('GUARD rc %d %s' % (rc, pf)); return 0 if rc == 0 else 1
            if A[0] == 'targets' and dev: return run_targets(repo, dev, out)
    except Refused as x:
        print('REFUSED: %s' % x); return 1
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
