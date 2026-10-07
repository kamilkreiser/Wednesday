#!/usr/bin/env python3
r"""c4_docs_gate73.py — the two platform docs for the FOUR gate73 rows, and the STACKED KEEP-BOTH MERGE-IN PREDICTION for any landing order.

THE COMPOSER (gate71's pattern, carried): a row's doc change is ONE pure line-block insertion immediately before `</body>`; its docs merge-in
onto a develop that already holds earlier landers is that SAME block, byte-identical, inserted immediately before develop's `</body>` — i.e.
AFTER every earlier lander's block (keep-both, earlier first). No re-composition is needed this round: all four rows were written on the
SAME base in the SAME matrix format (gate71's recompose_gate71.py is therefore NOT used; `calibrate` proves the identity composer reproduces
each row's own END_TREE byte for byte, and that base's two doc blobs ARE gate71's predicted #1398 targets, i.e. that composer's last
prediction landed byte for byte).

MODES (every mode: --repo <YOUR clone>; every PR-specific value is an ARGUMENT, never a default)
  docs      --pr R --head H        D1 BOUNDARY-FREE (head minus ONE byte span == base; CONTROL a 1-byte-altered span FALSE);
                                   D2 the line block is LAST before `</body>` and head minus block == base line for line;
                                   D3 flow == base + [own num], UNIQUE, own block KEYED `(KS-n)`; cheat == base + [own key]; split-h2 CONTROL;
                                   D4 only the row's key hyphenated inside the block (CONTROL planted KS-9999 found);
                                   D5 `<h2` openings == keyed h2s, div balance kept;  D6 INFO the cheat block's `<div class="section">` wrapper.
  calibrate --heads 1407=H,1409=H,1408=H,1410=H     each row composed ALONE onto the base == its head tree == its END_TREE (byte for byte);
                                   base's doc blobs == gate71's recomposed_2026-10-07/MANIFEST.txt #1398 targets (INFO + check).
  chain     --order a,b,c,d --develop D --heads ... --out DIR [--no-guard]
                                   step i: develop_i = D (i=0) or SIM_{i-1} (objects-only commit-tree in YOUR clone); predicted tree_i;
                                   read-back (own once, LAST, develop_i's sequence the prefix, UNIQUE); THE GUARD ITSELF on tree_i
                                   (`bash systemTest/__tests__/html_docs_matrix.test.sh` materialised from tree_i); git merge-tree as a
                                   CROSS-CHECK that is printed and NEVER PICKED. INDEPENDENT FINAL CHECK: the last tree's docs rebuilt in ONE
                                   pass (base + every fragment in order) and its code paths == each head's blobs. Writes DIR/chain.json, the
                                   composed docs per step (merge seat takes them VERBATIM) and DIR/MANIFEST.txt.
  orders    --develop D --heads ... --out DIR       every one of the 24 orders: the tree at each step (no guard), to DIR/orders.json.
  qm        --pr R --head H --merge-in-head M --develop-after D --predicted-tree T --out DIR
                                   Q1 M's parents == [H, D] exactly (count AND order); Q2 tree(M) == T; Q3 read-back + UNIQUE; Q4 M's docs minus
                                   the row's block == D's docs byte for byte; Q5 code blobs == H's; Q6 the guard on tree(M).
  --selftest                       planted arms that MUST fail (see selftest()).
rc 0 PASS / 1 FAIL / 2 refused by name."""
import io, itertools, json, os, re, subprocess, sys, tarfile, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate73 import (K, D, ROWS, BASE, Tally, git, git_bytes, wgit, refuse_absent, outside_forbidden, opt, obj_at, mode_at, close_idx,
                        flow_nums, flow_num_pos, cheat_keys, cheat_key_pos, old_sameline_nums, h2_open_count, code_paths, row_arg)

DOCS = {'flow': D['flow'], 'cheat': D['cheat']}
SECTION_OPEN = re.compile(r'^\s*<div class="section">\s*$')
SIM_ENV = {'GIT_AUTHOR_NAME': 'gate73 SIM', 'GIT_AUTHOR_EMAIL': 'sim@gate73.invalid', 'GIT_COMMITTER_NAME': 'gate73 SIM',
           'GIT_COMMITTER_EMAIL': 'sim@gate73.invalid', 'GIT_AUTHOR_DATE': '2026-10-07T00:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-07T00:00:00Z'}


DEMAND_ASC = os.environ.get('G73_DOCS_DEMAND_ASCENDING') == '1'     # a planted WRONG rule: the self-test MUST then fail


class Refused(Exception): pass


def own(doc, R): return R['flow_num'] if doc == 'flow' else R['cheat_key']
def seq(text, doc): return flow_nums(text) if doc == 'flow' else cheat_keys(text)


def boundary_free(hb, bb):
    """bytes: the ONE span whose removal from head gives base, whether that holds, and how often the span occurs in head."""
    i = 0
    while i < len(bb) and hb[i] == bb[i]: i += 1
    j = 0
    while j < len(bb) - i and hb[-1 - j] == bb[-1 - j]: j += 1
    frag = hb[i:len(hb) - j]
    return frag, hb.replace(frag, b'', 1) == bb, hb.count(frag)


def line_block(htext, btext):
    """the inserted LINE block: H = B[:s] + blk + B[s:]. Refuses unless head is base plus exactly one contiguous line insertion."""
    H, B = htext.split('\n'), btext.split('\n')
    if len(H) <= len(B): raise Refused('head has %d lines, base %d: not an insertion' % (len(H), len(B)))
    s = 0
    while s < len(B) and H[s] == B[s]: s += 1
    n = len(H) - len(B)
    if H[:s] + H[s + n:] != B:
        # the common-prefix split can land inside a run of identical lines; anchor the block's end on the close tag instead
        c = close_idx(H); s2 = c - n
        if s2 < 0 or H[:s2] + H[c:] != B: raise Refused('head minus ONE contiguous line block != base (not ONE pure insertion)')
        s = s2
    blk = H[s:s + n]
    return blk, s, (s + n == close_idx(H))


def keyed(doc, blk_lines, R):
    t = '\n'.join(blk_lines)
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', t, re.S)
    if len(h2s) != 1: return False
    return ('(%s)' % R['ticket']) in h2s[0] if doc == 'flow' else cheat_keys('<h2>%s</h2>' % h2s[0]) == [R['cheat_key']]


def insert_before_close(dtext, blk):
    L = dtext.split('\n'); at = close_idx(L)
    return '\n'.join(L[:at] + blk + L[at:])


def balance(text):
    """(<table opens - </table> closes, <div opens - </div> closes). The html_docs_matrix guard does NOT check tag balance (measured
    2026-10-07: a keep-both resolution that dropped one `</table>` read 12 passed / 0 failed), so the kit checks it itself."""
    return (len(re.findall(r'<table\b', text)) - len(re.findall(r'</table>', text)), len(re.findall(r'<div\b', text)) - len(re.findall(r'</div>', text)))


def readback(doc, text, dtext, o):
    try: s = seq(text, doc); sd = seq(dtext, doc)
    except ValueError as x: return False, 'reader refused: %s' % x
    bal_ok = balance(text) == balance(dtext)
    ok = s.count(o) == 1 and s[-1] == o and s[:-1] == sd and len(s) == len(set(s)) and bal_ok
    if DEMAND_ASC and doc == 'flow': ok = ok and s == sorted(s)          # the planted WRONG rule (self-test arm only)
    return ok, 'own %s x%d, LAST %s, develop prefix kept %s, UNIQUE %s, table/div balance %s == develop %s, tail %s%s' % (
        o, s.count(o), s[-1:] == [o], s[:-1] == sd, len(s) == len(set(s)), balance(text), balance(dtext), s[-6:],
        (', ascending %s (INFO, never asserted)' % (s == sorted(s))) if doc == 'flow' else '')


def heads_arg(A, need=None):
    h = {}
    for kv in (opt(A, '--heads') or '').split(','):
        if '=' in kv: k, v = kv.split('=', 1); h[k.strip()] = v.strip()
    bad = [r for r in (need or ROWS) if r not in h or not re.fullmatch(r'[0-9a-f]{40}', h[r])]
    if bad: raise SystemExit('c4: REFUSED — --heads must name every row in FULL 40-hex (missing/malformed: %s)' % bad)
    return h


# ---------------- docs (per row) ----------------
def docs(repo, head, R):
    t = Tally()
    for doc, path in DOCS.items():
        bb, hb = git_bytes(repo, BASE, path), git_bytes(repo, head, path)
        frag, ok, n = boundary_free(hb, bb)
        alt = bytearray(frag); k = len(alt) // 2
        if alt: alt[k] = (alt[k] + 1) % 256
        ctl = bool(alt) and hb.replace(bytes(alt), b'', 1) == bb
        t.check('D1-%s' % doc, ok and n == 1 and not ctl and len(frag) > 0,
                'head minus ONE span (%d B) == base: %s; span occurs %d time(s); CONTROL 1-byte-altered span reproduces base: %s' % (len(frag), ok, n, ctl))
        bt, ht = bb.decode(), hb.decode(); o = own(doc, R)
        try:
            blk, at, last = line_block(ht, bt)
            t.check('D2-%s' % doc, last, 'line block %d lines at line %d, head minus block == base, block is LAST before </body>: %s' % (len(blk), at + 1, last))
        except (Refused, ValueError) as x:
            t.check('D2-%s' % doc, False, str(x)); blk = []
        sb, sh = seq(bt, doc), seq(ht, doc)
        if doc == 'flow':
            t.check('D3-flow', sh == sb + [o] and len(sh) == len(set(sh)) and keyed(doc, blk, R) and sb == D['flow_seq_base'],
                    'base ..%s -> head ..%s; UNIQUE %s; own block KEYED (%s) %s; base == kit %s; ascending %s (INFO)' % (
                        sb[-3:], sh[-4:], len(sh) == len(set(sh)), R['ticket'], keyed(doc, blk, R), sb == D['flow_seq_base'], sh == sorted(sh)))
            plant = ht.replace('</body>', '<h2>\n    99. planted split heading</h2>\n</body>', 1)
            t.check('D3-flow-ctl', 99 in flow_nums(plant) and 99 not in old_sameline_nums(plant),
                    'PLANTED `<h2>\\n  99.`: tolerant reader HIT %s, same-line reader MISSED %s' % (99 in flow_nums(plant), 99 not in old_sameline_nums(plant)))
        else:
            t.check('D3-cheat', sh == sb + [o] and sb == D['cheat_seq_base'] and keyed(doc, blk, R),
                    'base tail %s -> head tail %s; base == kit %s; KEYED %s' % (sb[-2:], sh[-3:], sb == D['cheat_seq_base'], keyed(doc, blk, R)))
        btxt = '\n'.join(blk)
        hy = sorted(set(re.findall(r'\bKS-\d+\b', btxt))); de = sorted(set(re.findall(r'\bKS \d+\b', btxt)))
        ctl2 = 'KS-9999' in re.findall(r'\bKS-\d+\b', btxt + ' KS-9999 ')
        t.check('D4-%s' % doc, hy == R['keys_hyphenated_allowed'] and ctl2,
                'hyphenated keys in the block %s (want only %s) | de-hyphenated %s | CONTROL planted KS-9999 found %s' % (hy, R['keys_hyphenated_allowed'], de, ctl2))
        try: nk = len(seq(ht, doc))
        except ValueError: nk = -1
        dv = lambda s: len(re.findall(r'<div\b', s)) - len(re.findall(r'</div>', s))
        t.check('D5-%s' % doc, h2_open_count(ht) == nk and balance(ht) == balance(bt) and balance('\n'.join(blk)) == (0, 0),
                '`<h2` openings %d == keyed %d; table/div balance head %s == base %s; the block alone balanced %s' % (h2_open_count(ht), nk, balance(ht), balance(bt), balance('\n'.join(blk))))
        if doc == 'cheat' and blk:
            wrapped = SECTION_OPEN.match(blk[0]) is not None and blk[-1].strip() == '</div>'
            t.info('D6-cheat', 'the block is a section card (`<div class="section">` … `</div>`)' if wrapped else
                   'FINDING (polish, not a blocker by the drafter): the block is NOT wrapped in `<div class="section">` (first line %r); the base tail section (KS-1136) is a section card' % blk[0].strip()[:70])
    return t.end()


# ---------------- trees ----------------
def build_tree(repo, dev, blobs):
    if not outside_forbidden(repo): raise Refused('clone inside the forbidden root')
    fd, idx = tempfile.mkstemp(prefix='g73idx.'); os.close(fd); os.unlink(idx); env = {'GIT_INDEX_FILE': idx}
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


def blocks_of(repo, head):
    out = {}
    for doc, path in DOCS.items():
        blk, _, last = line_block(git_bytes(repo, head, path).decode(), git_bytes(repo, BASE, path).decode())
        if not last: raise Refused('%s: the row block is not LAST before </body> at %s' % (doc, head[:12]))
        out[doc] = blk
    return out


def predict(repo, head, dev, R):
    """(tree, {doc: text}, notes). dev: develop or a stacked SIM commit."""
    notes = []
    if dev == BASE:
        notes.append('develop == the base %s: NO MERGE-IN; the squash tree == END_TREE' % BASE[:12])
        t = git(repo, 'rev-parse', head + '^{tree}').strip()
        return t, {d: git_bytes(repo, head, p).decode() for d, p in DOCS.items()}, notes
    if git(repo, 'merge-base', '--is-ancestor', BASE, dev, check=False)[0] != 0: raise Refused('develop %s does not descend from the base %s' % (dev[:12], BASE[:12]))
    moved = [p for p in code_paths(R) if obj_at(repo, BASE, p) != obj_at(repo, dev, p)]
    if moved: raise Refused('develop %s moved a CODE path of #%s since the base: %s — RE-GATE, the docs-only merge-in no longer holds' % (dev[:12], R['pr'], moved))
    blobs, texts = {}, {}
    for p in code_paths(R):
        blobs[p] = (mode_at(repo, head, p), obj_at(repo, head, p))
    blk = blocks_of(repo, head)
    for doc, path in DOCS.items():
        bt, dt = git_bytes(repo, BASE, path).decode(), git_bytes(repo, dev, path).decode()
        if dt == bt:
            texts[doc] = git_bytes(repo, head, path).decode(); notes.append('%s: develop UNCHANGED since the base -> the head blob' % doc)
        else:
            m = insert_before_close(dt, blk[doc]); texts[doc] = m
            ok, why = readback(doc, m, dt, own(doc, R))
            notes.append('%s: KEEP-BOTH, the head block (%d lines, byte-identical) before develop\'s </body> -> read-back %s: %s' % (doc, len(blk[doc]), 'OK' if ok else 'FAIL', why))
            if not ok: raise Refused('%s read-back FAILED: %s' % (doc, why))
        blobs[path] = ('100644', hash_blob(repo, texts[doc].encode()))
    return build_tree(repo, dev, blobs), texts, notes


def run_guard(repo, tree, out, tag):
    d = os.path.join(out, 'guard_' + tag); os.makedirs(d)
    paths = [D['guard_suite'], D['guard_checker'], D['flow'], D['cheat']]
    p = subprocess.run(['git', '-C', repo, 'archive', '--format=tar', tree, '--'] + paths, capture_output=True)
    if p.returncode: raise Refused('git archive %s: %s' % (tree[:12], p.stderr.decode()[:160]))
    tarfile.open(fileobj=io.BytesIO(p.stdout)).extractall(d)
    tmp = os.path.join(d, '.tmp'); os.makedirs(tmp)
    log = os.path.join(out, 'guard_%s.log' % tag)
    with open(log, 'wb') as fo:
        rc = subprocess.run(['bash', os.path.join(d, D['guard_suite'])], env=dict(os.environ, TMPDIR=tmp), stdout=fo, stderr=subprocess.STDOUT).returncode
    text = open(log, encoding='utf-8', errors='replace').read()
    m = re.search(r'^\s*(\d+) passed, (\d+) failed\s*$', text, re.M)
    return rc, ((int(m.group(1)), int(m.group(2))) if m else None), log


def mergetree(repo, dev, head, tree):
    rc, o, e = wgit(repo, 'merge-tree', '--write-tree', '--name-only', dev, head)
    lines = o.strip().split('\n'); mt = lines[0] if lines else ''
    if not re.fullmatch(r'[0-9a-f]{40}', mt): return rc, {'error': (e or o).strip()[:200]}, []
    dv = {}
    for doc, path in DOCS.items():
        a, b = obj_at(repo, mt, path), obj_at(repo, tree, path)
        marks = git_bytes(repo, mt, path).count(b'<<<<<<<') if a else 0
        dv[doc] = 'AGREE' if a == b else 'DIVERGENCE (merge-tree conflicts: %d marker(s); never picked)' % marks
    diff = [l for l in git(repo, 'diff', '--name-only', mt, tree).split('\n') if l and l not in DOCS.values()]
    return rc, dv, diff


def union_check(repo, dev, head, texts, out, tag):
    """AN INDEPENDENT INSTRUMENT: git's own 3-way file merger with --union (keeps both sides, OURS = develop FIRST) on (develop, base, head)
    for each doc, compared byte for byte with the composer's text. Files only, under OUT: no repository is written."""
    res = {}
    for doc, path in DOCS.items():
        d = os.path.join(out, 'union_%s_%s' % (tag, doc)); os.makedirs(d, exist_ok=True)
        fs = []
        for nm, rev in (('ours_develop', dev), ('base', BASE), ('theirs_head', head)):
            fn = os.path.join(d, nm + '.html'); open(fn, 'wb').write(git_bytes(repo, rev, path)); fs.append(fn)
        p = subprocess.run(['git', 'merge-file', '-p', '--union'] + fs, capture_output=True)
        if p.stdout == texts[doc].encode(): res[doc] = 'AGREE'
        else:
            u = p.stdout.decode('utf-8', 'replace')
            res[doc] = 'DIFFERS: union %d lines vs composer %d, union table/div balance %s vs composer %s — a HAZARD (diff3 trims the lines the two blocks END with alike, so `--union` DROPS the earlier lander\'s closing tag(s)); the composer is the target, never the union' % (
                u.count('\n'), texts[doc].count('\n'), balance(u), balance(texts[doc]))
    return res


def chain(repo, order, dev0, heads, out, guard=True, quiet=False):
    os.makedirs(out, exist_ok=True)
    res = {'develop': dev0, 'order': order, 'steps': []}; dev = dev0; ok_all = True
    for i, r in enumerate(order):
        R = ROWS[r]; h = heads[r]
        tree, texts, notes = predict(repo, h, dev, R)
        st = {'step': i + 1, 'pr': r, 'head': h, 'onto': dev, 'tree': tree, 'notes': notes,
              'merge_in_needed': dev != BASE, 'tree_equals_end_tree': tree == R['end_tree']}
        if guard:
            rc, ratio, log = run_guard(repo, tree, out, '%d_%s' % (i + 1, r))
            st['guard'] = {'rc': rc, 'ratio': ratio, 'log': log}
            ok_all &= rc == 0 and ratio is not None and ratio[1] == 0
        mrc, dv, outside = mergetree(repo, dev, h, tree)
        st['merge_tree'] = {'rc': mrc, 'docs': dv, 'outside_docs_differing': outside}
        ok_all &= outside == []
        un = union_check(repo, dev, h, texts, out, '%d_%s' % (i + 1, r)); st['union'] = un
        for doc in DOCS:
            fn = os.path.join(out, '%d_%s_composed_%s_doc.html' % (i + 1, r, doc))
            open(fn, 'wb').write(texts[doc].encode()); st['%s_doc' % doc] = fn
            st['%s_blob' % doc] = obj_at(repo, tree, DOCS[doc])
        sim = commit_sim(repo, tree, dev, 'gate73 SIM: develop + #%s squash (objects only, never pushed)' % r)
        st['sim_commit'] = sim; res['steps'].append(st); dev = sim
        if not quiet:
            print('STEP %d #%s head %s onto %s -> tree %s%s' % (i + 1, r, h[:12], st['onto'][:12], tree, '  (== END_TREE, no merge-in)' if st['tree_equals_end_tree'] else '  (docs-only keep-both merge-in)'))
            for n in notes: print('   ' + n)
            if guard: print('   guard: rc %d, %s passed / %s failed' % (st['guard']['rc'], *(st['guard']['ratio'] or ('?', '?'))))
            print('   merge-tree cross-check (NEVER PICKED): rc %d, %s, outside the docs differing: %s' % (mrc, dv, outside))
            print('   INDEPENDENT: `git merge-file -p --union` (develop, base, head) == the composer, per doc: %s' % un)
    # INDEPENDENT final check: one-pass composition from the base, and each code path == its head's blob
    last = res['steps'][-1]['tree']; t = Tally() if not quiet else None
    fin_ok = True
    for doc, path in DOCS.items():
        d0 = git_bytes(repo, dev0, path).decode()
        bl = d0.split('\n'); c = close_idx(bl); blks = []
        for r in order: blks += blocks_of(repo, heads[r])[doc]
        one = '\n'.join(bl[:c] + blks + bl[c:])
        same = one.encode() == git_bytes(repo, last, path); fin_ok &= same
        s = seq(one, doc); want = seq(d0, doc) + [own(doc, ROWS[r]) for r in order]
        fin_ok &= s == want
        if not quiet: print('FINAL-%s one-pass composition (develop %s + every block in landing order) == the chain\'s last blob: %s; sequence == develop + landing order: %s (tail %s)' % (
            doc, dev0[:12], same, s == want, s[-5:]))
    for r in order:
        for p in code_paths(ROWS[r]):
            eq = obj_at(repo, last, p) == obj_at(repo, heads[r], p); fin_ok &= eq
            if not eq and not quiet: print('FINAL-CODE FAIL %s at the last tree != #%s head' % (p, r))
    if not quiet: print('FINAL-CODE every row\'s code paths in the last tree == that row\'s head blob: %s' % fin_ok)
    res['final_ok'] = fin_ok; ok_all &= fin_ok
    json.dump(res, open(os.path.join(out, 'chain.json'), 'w'), indent=1)
    with open(os.path.join(out, 'MANIFEST.txt'), 'w') as f:
        f.write('gate73 stacked keep-both docs merge-in prediction. develop %s, order %s.\n' % (dev0, ' -> '.join('#' + r for r in order)))
        f.write('The merge seat takes each step\'s composed docs VERBATIM; then tree(M) == the predicted tree exactly (qm Q2 strict).\n')
        for st in res['steps']:
            f.write('step %d #%s head %s onto %s: tree %s | flow blob %s | cheat blob %s | merge-in %s | guard %s\n' % (
                st['step'], st['pr'], st['head'][:12], st['onto'][:12], st['tree'], st['flow_blob'], st['cheat_blob'],
                'needed' if st['merge_in_needed'] else 'NONE (== END_TREE)', st.get('guard', {}).get('ratio')))
    if not quiet: print('CHAIN written: %s (chain.json, MANIFEST.txt, composed docs per step) — %s' % (out, 'ALL OK' if ok_all else 'NOT ALL OK'))
    return 0 if ok_all else 1


def orders(repo, dev0, heads, out):
    os.makedirs(out, exist_ok=True); table = {}
    for perm in itertools.permutations(list(ROWS)):
        d = os.path.join(out, '_'.join(perm))
        rc = chain(repo, list(perm), dev0, heads, d, guard=False, quiet=True)
        c = json.load(open(os.path.join(d, 'chain.json')))
        table['>'.join(perm)] = {'rc': rc, 'trees': [s['tree'] for s in c['steps']]}
        print('ORDER %s rc %d trees %s' % (' -> '.join(perm), rc, ' '.join(s['tree'][:12] for s in c['steps'])))
    json.dump(table, open(os.path.join(out, 'orders.json'), 'w'), indent=1)
    finals = set(v['trees'][-1] for v in table.values())
    print('ORDERS %d, all rc 0: %s; distinct FINAL trees %d (each order\'s final docs differ only in block order)' % (
        len(table), all(v['rc'] == 0 for v in table.values()), len(finals)))
    return 0 if all(v['rc'] == 0 for v in table.values()) else 1


def calibrate(repo, heads):
    t = Tally()
    for r, R in ROWS.items():
        tree, texts, _ = predict(repo, heads[r], BASE, R)
        # compose ALONE through the keep-both path too (not the dev==base shortcut): base doc + block before </body>
        same = True
        for doc, path in DOCS.items():
            m = insert_before_close(git_bytes(repo, BASE, path).decode(), blocks_of(repo, heads[r])[doc])
            same &= m.encode() == git_bytes(repo, heads[r], path)
        t.check('CAL-%s' % r, same and tree == R['end_tree'], 'composer(base, [#%s]) == the head doc blobs BYTE FOR BYTE: %s; tree %s == END_TREE %s: %s' % (
            r, same, tree[:12], R['end_tree'][:12], tree == R['end_tree']))
    man = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-10-06_gate71', 'recomposed_2026-10-07', 'MANIFEST.txt')
    try:
        mt = open(man).read()
        f1 = re.search(r'1398 flow: .*?after ([0-9a-f]{40})', mt).group(1); c1 = re.search(r'1398 cheat: .*?after ([0-9a-f]{40})', mt).group(1)
        t.check('CAL-gate71', obj_at(repo, BASE, D['flow']) == f1 and obj_at(repo, BASE, D['cheat']) == c1,
                'base %s doc blobs == gate71\'s predicted #1398 targets (flow %s, cheat %s): the composer lineage\'s last prediction LANDED byte for byte' % (BASE[:12], f1[:12], c1[:12]))
    except (OSError, AttributeError) as x:
        t.info('CAL-gate71', 'gate71 MANIFEST unreadable here (%s): lineage check NOT RUN' % x)
    return t.end()


def qm(repo, R, head, M, dev, T, out):
    t = Tally(); os.makedirs(out, exist_ok=True)
    par = git(repo, 'log', '-1', '--format=%P', M).split()
    t.check('Q1', par == [head, dev], 'M %s parents %s (want EXACTLY [head %s, develop %s], count %d)' % (M[:12], [p[:12] for p in par], head[:12], dev[:12], len(par)))
    tm = git(repo, 'rev-parse', M + '^{tree}').strip()
    t.check('Q2', tm == T, 'tree(M) %s == predicted %s' % (tm[:12], T[:12]))
    blk = blocks_of(repo, head)
    for doc, path in DOCS.items():
        mt, dt = git_bytes(repo, M, path).decode(), git_bytes(repo, dev, path).decode()
        ok, why = readback(doc, mt, dt, own(doc, R)); t.check('Q3-%s' % doc, ok, why)
        L = mt.split('\n'); b = blk[doc]; n = len(b)
        hits = [i for i in range(len(L) - n + 1) if L[i:i + n] == b]
        t.check('Q4-%s' % doc, len(hits) == 1 and L[:hits[0]] + L[hits[0] + n:] == dt.split('\n'),
                'the head block occurs %d time(s) in M; M minus it == develop byte for byte: %s' % (len(hits), len(hits) == 1 and L[:hits[0]] + L[hits[0] + n:] == dt.split('\n')))
    bad = [p for p in code_paths(R) if obj_at(repo, M, p) != obj_at(repo, head, p)]
    t.check('Q5', not bad, 'code blobs in M == the head\'s: %s %s' % (not bad, bad))
    rc, ratio, log = run_guard(repo, tm, out, 'qm_%s' % R['pr'])
    t.check('Q6', rc == 0 and ratio is not None and ratio[1] == 0, 'the guard on tree(M): rc %d, %s (log %s)' % (rc, ratio, log))
    return t.end()


# ---------------- self-test ----------------
def selftest(repo, heads):
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    out = tempfile.mkdtemp(prefix='g73c4st.', dir=os.environ.get('G73_SCRATCH') or None)
    R0 = ROWS['1407']; h0 = heads['1407']
    # 1 boundary-free control
    bb, hb = git_bytes(repo, BASE, D['flow']), git_bytes(repo, h0, D['flow'])
    frag, ok, n = boundary_free(hb, bb); alt = bytearray(frag); alt[len(alt) // 2] ^= 1
    rep(ok and n == 1 and hb.replace(bytes(alt), b'', 1) != bb, 'D1: the real fragment reproduces base, a 1-byte-altered one does NOT')
    # 2 a head that ALSO edits a pre-existing block is not ONE pure insertion
    bt = bb.decode(); ht = hb.decode().replace('<h2', '<h2 ', 1)
    try: line_block(ht, bt); rep(False, 'PLANTED edit of a pre-existing heading: line_block should REFUSE')
    except (Refused, ValueError): rep(True, 'PLANTED edit of a pre-existing heading: line_block REFUSES (not ONE pure insertion)')
    # 3 calibration identity: each row alone onto base == END_TREE
    for r in ROWS:
        tr, _, _ = predict(repo, heads[r], BASE, ROWS[r]); rep(tr == ROWS[r]['end_tree'], 'calibration #%s alone on base == END_TREE %s' % (r, ROWS[r]['end_tree'][:12]))
    # 4 keep-both read-back: the second lander lands AFTER the first; a WRONG-side insert (before the first lander) fails read-back
    sim1 = commit_sim(repo, ROWS['1407']['end_tree'], BASE, 'selftest SIM #1407')
    try:
        tr2, tx2, _ = predict(repo, heads['1409'], sim1, ROWS['1409'])
        s = flow_nums(tx2['flow']); rep(s[-2:] == [29, 25], 'keep-both: #1409 onto develop+#1407 -> flow tail %s (29 then 25, NOT ascending, BY DESIGN)' % s[-2:])
    except Refused as x:
        rep(False, 'keep-both: #1409 onto develop+#1407 REFUSED: %s' % x)
    dt = git_bytes(repo, sim1, D['flow']).decode(); L = dt.split('\n'); fp = [ln for k, ln in flow_num_pos(dt) if k == 29][0]
    wrong = '\n'.join(L[:fp] + blocks_of(repo, heads['1409'])['flow'] + L[fp:])
    rep(not readback('flow', wrong, dt, 25)[0], 'PLANTED wrong-side insert (#1409 BEFORE #1407\'s block): read-back FAILS')
    # 5 duplicate number: #1407 onto a develop that already holds #1407 -> read-back fails (own twice)
    docs_only = build_tree(repo, BASE, {p: ('100644', obj_at(repo, h0, p)) for p in DOCS.values()})
    sim_d = commit_sim(repo, docs_only, BASE, 'selftest SIM: base + #1407 docs only')
    try:
        predict(repo, h0, sim_d, R0); rep(False, 'PLANTED double landing of #1407: should REFUSE')
    except Refused as x: rep('read-back FAILED' in str(x), 'PLANTED double landing of #1407: REFUSED (%s)' % str(x)[:80])
    # 6 develop that moved a row code path refuses
    blob = hash_blob(repo, b'planted\n')
    t6 = build_tree(repo, BASE, {'systemTest/scripts/check-package-format.sh': ('100755', blob)}); sim6 = commit_sim(repo, t6, BASE, 'selftest SIM touching 1407 code')
    try: predict(repo, h0, sim6, R0); rep(False, 'PLANTED develop touching #1407 code: should REFUSE')
    except Refused as x: rep('moved a CODE path' in str(x), 'PLANTED develop touching #1407 code: REFUSED')
    # 7 a develop that does not descend from the base refuses
    parent = git(repo, 'rev-parse', BASE + '^1').strip()
    try: predict(repo, h0, parent, R0); rep(False, 'PLANTED ancestor develop: should REFUSE')
    except Refused as x: rep('does not descend' in str(x), 'PLANTED ancestor develop (%s): REFUSED' % parent[:12])
    # 8 the guard fires on a planted prose-outside-a-table block (POSITIVE CONTROL of the guard itself)
    bad = insert_before_close(git_bytes(repo, BASE, D['flow']).decode(), ['<h2>99. planted (KS-9999)</h2>', '<p>Planted prose outside any table.</p>'])
    tb = build_tree(repo, BASE, {D['flow']: ('100644', hash_blob(repo, bad.encode()))})
    rc, ratio, _ = run_guard(repo, tb, out, 'ctl_bad'); rc0, ratio0, _ = run_guard(repo, ROWS['1407']['end_tree'], out, 'ctl_good')
    rep(rc != 0 and rc0 == 0 and ratio0 is not None and ratio0[1] == 0, 'guard POSITIVE CONTROL: planted prose block rc %d %s vs #1407 END_TREE rc %d %s' % (rc, ratio, rc0, ratio0))
    # 9 cheat reader widened: base carries &mdash; AND U+2014 keyed h2s; the pinned reader alone misses some
    from lib_gate73 import cheat_keys_pinned
    ct = git_bytes(repo, heads['1408'], D['cheat']).decode()
    rep('KS-1435' in cheat_keys(ct) and 'KS-1435' not in cheat_keys_pinned(ct), 'cheat: widened reader reads KS-1435 (U+2014); the pinned &mdash;-only reader is BLIND to it')
    # 10 keyed(): a flow block whose h2 lacks its ticket is NOT keyed
    rep(not keyed('flow', ['<h2>29. no key here</h2>'], R0) and keyed('flow', blocks_of(repo, h0)['flow'], R0), 'KEYED: an unkeyed h2 FAILS, the real #1407 block PASSES')
    # 11 THE UNION HAZARD: `git merge-file --union` of (develop+#1407, base, #1409) on the CHEAT drops a closing `</table>`; the kit's
    #    read-back REFUSES it on tag balance while the repo's own guard PASSES it (the guard is blind to tag balance: named, not fixed)
    fs = []
    for nm, rev in (('o', sim1), ('b', BASE), ('t', heads['1409'])):
        fn = os.path.join(out, 'u11_%s.html' % nm); open(fn, 'wb').write(git_bytes(repo, rev, D['cheat'])); fs.append(fn)
    u = subprocess.run(['git', 'merge-file', '-p', '--union'] + fs, capture_output=True).stdout.decode()
    rb = readback('cheat', u, git_bytes(repo, sim1, D['cheat']).decode(), 'KS-1313')
    tu = build_tree(repo, sim1, {D['cheat']: ('100644', hash_blob(repo, u.encode()))})
    rcu, ratu, _ = run_guard(repo, tu, out, 'union_hazard')
    rep(not rb[0] and 'balance' in rb[1] and rcu == 0, 'UNION HAZARD: union-resolved cheat read-back REFUSES (%s) while the repo guard reads rc %d %s (BLIND to tag balance)' % (
        rb[1][rb[1].find('table/div'):rb[1].find(', tail')], rcu, ratu))
    print('SELFTEST %d/%d (scratch %s)' % (sum(res), len(res), out)); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    repo = opt(A, '--repo')
    if not repo: print(__doc__); return 2
    if '--selftest' in A:
        h = heads_arg(A); return refuse_absent(repo, [('head ' + r, s) for r, s in h.items()]) or selftest(repo, h)
    mode = A[0] if A else ''
    if mode == 'docs':
        r = row_arg(); h = opt(A, '--head')
        return refuse_absent(repo, [('--head', h)]) or docs(repo, h, ROWS[r])
    if mode == 'calibrate':
        h = heads_arg(A); return refuse_absent(repo, [('head ' + r, s) for r, s in h.items()]) or calibrate(repo, h)
    if mode in ('chain', 'orders'):
        need = [x for x in (opt(A, '--order') or '').split(',') if x in ROWS] if mode == 'chain' else None
        h = heads_arg(A, need or None); dev = opt(A, '--develop'); out = opt(A, '--out')
        if not out: raise SystemExit('c4: --out DIR is required')
        rc = refuse_absent(repo, [('--develop', dev)] + [('head ' + r, s) for r, s in h.items()])
        if rc: return rc
        try:
            if mode == 'orders': return orders(repo, dev, h, out)
            order = [x for x in (opt(A, '--order') or '').split(',') if x]
            if not order or len(set(order)) != len(order) or any(x not in ROWS for x in order):
                raise SystemExit('c4: REFUSED — --order must name 1-4 distinct rows of %s (the rows still to land, in landing order)' % sorted(ROWS))
            return chain(repo, order, dev, h, out, guard='--no-guard' not in A)
        except Refused as x:
            print('REFUSED: %s' % x); return 1
    if mode == 'qm':
        r = row_arg(); h, M, dev, T, out = (opt(A, k) for k in ('--head', '--merge-in-head', '--develop-after', '--predicted-tree', '--out'))
        if not (out and T): raise SystemExit('c4 qm: --predicted-tree and --out are required')
        return refuse_absent(repo, [('--head', h), ('--merge-in-head', M), ('--develop-after', dev)]) or qm(repo, ROWS[r], h, M, dev, T, out)
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
