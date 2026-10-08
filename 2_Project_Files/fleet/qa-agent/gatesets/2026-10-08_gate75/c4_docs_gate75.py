#!/usr/bin/env python3
r"""c4_docs_gate75.py — the two platform docs and the LANDING for gate75 (#1426 KS-1450). Written new by the gate75 drafter: #1426 does
not append a keyed block before </body> (gate74's shape); it INSERTS ONE CLAUSE into ONE existing line of each doc. So the docs are
checked as bytes, not as headings.
Usage:
  c4_docs_gate75.py docs   --pr 1426 --repo <YOUR clone> --base <40-hex> --head <40-hex>
  c4_docs_gate75.py merged --pr 1426 --repo <YOUR clone> --base <40-hex> --head <40-hex> --develop <40-hex> [--expect-tree <40-hex>]
  c4_docs_gate75.py --selftest --repo <clone>
docs:
  D1  exactly ONE line differs per doc, and the line count is unchanged
  D2  that line's difference is ONE INSERTION: head line with the fragment removed == base line (SequenceMatcher: one `insert` opcode)
  D3  the fragment sha256/16 and bytes == the kit's; it occurs exactly ONCE in the head doc and 0 times in the base doc; the line no. == kit
  D4  PARITY: the clause (kit anchor start..end) is byte-identical in D1 and D2 (skill §4 :378 both files, same clause)
  D5  TAG BALANCE: per-tag open == close inside each fragment; whole-doc per-tag open/close balance unchanged base -> head; `<code` counted
      attribute-aware (CONTROL: the literal `<code>` count on D2's base reads unbalanced, so the naive instrument would lie)
  D6  planted arms, each must be REFUSED by D1-D5: a `</code>` deleted from the fragment; the fragment doubled; a second line touched; the
      clause made to differ by one byte between the docs
merged:
  M1  `merge-tree --write-tree <develop> <head>` rc 0 in YOUR clone; CONTROL pair (kit merge_tree_control) rc 1 naming BOTH docs
  M2  diff(develop, merged) == exactly the PR's paths, each merged blob == the head's blob (no keep-both composition is needed when the
      head sits on develop; if develop moved, M2 reports which PR path develop also moved)
  M3  when develop == the base: predicted tree == END_TREE (and == --expect-tree when given)
  M4  base..develop Blockchain/Dev paths (the LEG-14 exposure of any merge-in push; an API squash runs no local hook)
  prints `MERGE-IN NEEDED: no|yes` and `PREDICTED_TREE=<40-hex>`
rc 0 all PASS / 1 any FAIL / 2 refused."""
import collections, difflib, hashlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate75 import K, ROWS, Tally, git, git_bytes, wgit, obj_at, opt, row_arg, refuse_absent, outside_forbidden

D = K['docs']
TAG = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)(\s[^>]*)?>')
VOID = {'br', 'hr', 'img', 'meta', 'link', 'input', 'wbr', 'col', 'source', 'area', 'base', 'param', 'track', 'embed'}


def tags(t):
    c = collections.Counter()
    for m in TAG.finditer(t):
        n = m.group(2).lower()
        if n in VOID: continue
        c[(n, 'close' if m.group(1) else 'open')] += 1
    return c


def unbalanced(c):
    return {n: (c[(n, 'open')], c[(n, 'close')]) for n in sorted({k[0] for k in c}) if c[(n, 'open')] != c[(n, 'close')]}


def analyse(btxt, htxt):
    """PURE: returns dict for one doc (base text, head text)."""
    b, h = btxt.split('\n'), htxt.split('\n')
    out = {'lines_base': len(b), 'lines_head': len(h), 'diff_lines': [], 'insertion_only': False, 'fragment': None}
    if len(b) != len(h): return out
    out['diff_lines'] = [i + 1 for i in range(len(b)) if b[i] != h[i]]
    if len(out['diff_lines']) == 1:
        i = out['diff_lines'][0] - 1
        ops = [o for o in difflib.SequenceMatcher(None, b[i], h[i], autojunk=False).get_opcodes() if o[0] != 'equal']
        if len(ops) == 1 and ops[0][0] == 'insert':
            f = h[i][ops[0][3]:ops[0][4]]
            out['fragment'] = f
            out['insertion_only'] = h[i].replace(f, '', 1) == b[i]
    out['tags_base'] = tags(btxt); out['tags_head'] = tags(htxt)
    return out


def clause(f):
    if not f or D['clause_anchor_start'] not in f or D['clause_anchor_end'] not in f: return None
    s = f.index(D['clause_anchor_start']); e = f.index(D['clause_anchor_end'], s) + len(D['clause_anchor_end'])
    return f[s:e]


def judge(t, docs):
    """docs: {'flow': (btxt, htxt), 'cheat': (btxt, htxt)} -> checks into Tally t."""
    A = {k: analyse(*v) for k, v in docs.items()}
    for k in ('flow', 'cheat'):
        a = A[k]; base_t, head_t = docs[k]
        t.check('D1-%s' % k, a['lines_base'] == a['lines_head'] and len(a['diff_lines']) == 1,
                'lines base %d head %d | differing lines %s (want exactly ONE)' % (a['lines_base'], a['lines_head'], a['diff_lines'][:6]))
        t.check('D2-%s' % k, a['insertion_only'], 'the one differing line is ONE insertion (head line minus fragment == base line): %s' % a['insertion_only'])
        f = a['fragment'] or ''
        fh = hashlib.sha256(f.encode()).hexdigest()[:16]
        t.check('D3-%s' % k, fh == D['%s_fragment_sha256_16' % k] and len(f.encode()) == D['%s_fragment_bytes' % k]
                and head_t.count(f) == 1 and base_t.count(f) == 0 and a['diff_lines'][:1] == [D['%s_line' % k]],
                'fragment %d B sha256/16 %s (kit %s / %d B) | in head %d, in base %d | line %s (kit %d)' % (
                    len(f.encode()), fh, D['%s_fragment_sha256_16' % k], D['%s_fragment_bytes' % k], head_t.count(f) if f else -1,
                    base_t.count(f) if f else -1, a['diff_lines'][:1], D['%s_line' % k]))
        ft = tags(f); ub_f = unbalanced(ft); ub_b = unbalanced(a['tags_base']); ub_h = unbalanced(a['tags_head'])
        code_b = (a['tags_base'][('code', 'open')], a['tags_base'][('code', 'close')]); code_h = (a['tags_head'][('code', 'open')], a['tags_head'][('code', 'close')])
        t.check('D5-%s' % k, f and not ub_f and ub_b == ub_h, 'fragment tags %s unbalanced %s | whole-doc unbalanced base %s head %s | <code…> base %s head %s | literal `<code>` base %d' % (
            dict(ft), ub_f or 'none', ub_b or 'none', ub_h or 'none', code_b, code_h, base_t.count('<code>')))
    c1, c2 = clause(A['flow']['fragment']), clause(A['cheat']['fragment'])
    t.check('D4', c1 is not None and c1 == c2, 'PARITY: the clause (%r..%r) byte-identical in both docs: %s (%s chars)' % (
        D['clause_anchor_start'][:20], D['clause_anchor_end'][-20:], c1 == c2 and c1 is not None, len(c1) if c1 else None))
    return A


def docs_mode(repo, base, head):
    t = Tally()
    docs = {k: (git_bytes(repo, base, D[k]).decode('utf-8'), git_bytes(repo, head, D[k]).decode('utf-8')) for k in ('flow', 'cheat')}
    for k in ('flow', 'cheat'):
        t.info('D0-%s' % k, '%s base blob %s head blob %s (kit %s / %s)' % (os.path.basename(D[k]), obj_at(repo, base, D[k])[:12], obj_at(repo, head, D[k])[:12],
                                                                          D['%s_blob_base' % k][:12], D['%s_blob_head' % k][:12]))
    judge(t, docs)
    # D6: planted arms on COPIES in memory — each must make at least one check FAIL
    import io, contextlib
    arms = []
    fl_b, fl_h = docs['flow']; ch_b, ch_h = docs['cheat']
    fa = analyse(fl_b, fl_h)['fragment'] or ''
    arms.append(('a </code> deleted from the flow fragment', {'flow': (fl_b, fl_h.replace(fa, fa.replace('</code>', '', 1), 1)), 'cheat': (ch_b, ch_h)}))
    arms.append(('the flow fragment doubled', {'flow': (fl_b, fl_h.replace(fa, fa + fa, 1)), 'cheat': (ch_b, ch_h)}))
    hl = fl_h.split('\n'); hl[0] = hl[0] + ' '; arms.append(('a second flow line touched', {'flow': (fl_b, '\n'.join(hl)), 'cheat': (ch_b, ch_h)}))
    arms.append(('the clause differs by one byte in cheat', {'flow': (fl_b, fl_h), 'cheat': (ch_b, ch_h.replace('cannot widen silently', 'cannot widen  silently', 1))}))
    for name, dd in arms:
        tt = Tally()
        with contextlib.redirect_stdout(io.StringIO()): judge(tt, dd)
        t.check('D6', bool(tt.fails), 'PLANTED %s: REFUSED by %s' % (name, tt.fails or 'NOTHING (a blind instrument)'))
    return t


def merged_mode(repo, base, head, dev, expect):
    t = Tally(); R = ROWS[row_arg()]
    if not outside_forbidden(repo):
        print('REFUSED: merge-tree is a write verb; --repo must be YOUR clone outside %s' % K['forbidden_root']); sys.exit(2)
    rc, o, e = wgit(repo, 'merge-tree', '--write-tree', dev, head)
    tree = o.split('\n')[0].strip() if rc == 0 else ''
    mc = K['merge_tree_control']
    crc, co, ce = wgit(repo, 'merge-tree', '--write-tree', '--name-only', mc['ours'], mc['theirs'])
    named = [f for f in mc['files'] if f in co]
    t.check('M1', rc == 0 and re.fullmatch(r'[0-9a-f]{40}', tree or '') is not None and crc == 1 and len(named) == 2,
            'merge-tree develop %s + head %s rc %d tree %s | CONTROL %s x %s rc %d naming %d/2 docs' % (dev[:12], head[:12], rc, tree[:12] or '-', mc['ours'][:12], mc['theirs'][:12], crc, len(named)))
    paths = [l for l in git(repo, 'diff', '--name-only', dev, tree).split('\n') if l] if tree else []
    bad = [p for p in paths if obj_at(repo, tree, p) != obj_at(repo, head, p)]
    devmoved = [p for p in R['numstat'] if obj_at(repo, R['parents'][0], p) != obj_at(repo, dev, p)]
    t.check('M2', sorted(paths) == sorted(R['numstat']) and not bad, 'diff(develop, merged) %d paths == the PR\'s %d: %s | merged blob != head blob on %s | PR paths develop also moved: %s' % (
        len(paths), len(R['numstat']), sorted(paths) == sorted(R['numstat']), bad or 'none', devmoved or 'none'))
    if dev == base:
        t.check('M3', tree == R['end_tree'] and (not expect or tree == expect), 'develop == base: predicted tree %s == END_TREE %s%s' % (
            tree[:12], R['end_tree'][:12], (' == --expect-tree %s' % expect[:12]) if expect else ''))
    else:
        t.check('M3', not expect or tree == expect, 'develop MOVED from the base: predicted tree %s%s (re-predicted; END_TREE no longer applies)' % (
            tree[:12], (' == --expect-tree %s' % expect[:12]) if expect else ''))
    bd = [l for l in git(repo, 'diff', '--name-only', base, dev).split('\n') if l]; bdev = [p for p in bd if p.startswith('Blockchain/Dev/')]
    t.info('M4', 'LEG-14 EXPOSURE: base..develop %d path(s), %d under Blockchain/Dev/ %s (an API squash runs no local hook; a merge-in push would carry these)' % (len(bd), len(bdev), bdev[:4]))
    need = not (t.fails == [] and rc == 0)
    print('MERGE-IN NEEDED: %s' % ('yes' if need else 'no'))
    print('PREDICTED_TREE=%s' % tree)
    return t


def selftest(repo):
    import io, contextlib
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    R = ROWS['1426']; base, head = R['parents'][0], R['head_expected']
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): t = docs_mode(repo, base, head)
    o = buf.getvalue()
    rep(not t.fails and t.n >= 13, 'docs GREEN at the pins: %d checked, fails %s' % (t.n, t.fails))
    rep(o.count('PASS D6 ') == 4, 'all 4 planted D6 arms REFUSED (%d)' % o.count('PASS D6 '))
    rep('literal `<code>` base 602' in o, 'the naive literal `<code>` count reads 602 on D2\'s base (R 16th lesson 5 reproduced: the attribute-aware count is the instrument)')
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): t = docs_mode(repo, head, head)
    rep(bool(t.fails), 'PLANTED base == head (no change at all): docs REFUSES (%s)' % t.fails[:3])
    os.environ.setdefault('G75_ROW', '1426')
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): t = merged_mode(repo, base, head, base, None)
    o = buf.getvalue()
    rep(not t.fails and 'MERGE-IN NEEDED: no' in o and ('PREDICTED_TREE=%s' % R['end_tree']) in o, 'merged GREEN at develop == base: tree == END_TREE, MERGE-IN NEEDED: no')
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): t = merged_mode(repo, base, head, base, K['develop_tree_at_draft'])
    rep('M3' in t.fails and 'MERGE-IN NEEDED: yes' in buf.getvalue(), 'PLANTED a wrong --expect-tree: M3 FAILS and the verdict reads yes')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]; repo = opt(A, '--repo')
    if not repo: print(__doc__); return 2
    if '--selftest' in A: return selftest(repo)
    mode = A[0] if A else ''
    r = row_arg(); R = ROWS[r]
    base, head = opt(A, '--base'), opt(A, '--head')
    if not base or not head: print('REFUSED: --base and --head are REQUIRED'); return 2
    if base != R['parents'][0]: print('REFUSED: WRONG VALUE --base %s != kit %s' % (base, R['parents'][0])); return 11
    if mode == 'docs':
        rc = refuse_absent(repo, [('--base', base), ('--head', head)])
        return rc or docs_mode(repo, base, head).end()
    if mode == 'merged':
        dev = opt(A, '--develop')
        if not dev: print('REFUSED: --develop is REQUIRED'); return 2
        rc = refuse_absent(repo, [('--base', base), ('--head', head), ('--develop', dev), ('control ours', K['merge_tree_control']['ours']), ('control theirs', K['merge_tree_control']['theirs'])])
        return rc or merged_mode(repo, base, head, dev, opt(A, '--expect-tree')).end()
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
