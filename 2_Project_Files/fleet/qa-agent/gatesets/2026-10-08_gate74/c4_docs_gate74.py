#!/usr/bin/env python3
r"""c4_docs_gate74.py — the two platform docs for gate74's ONE row (#1423, KS-1164), and the LANDING prediction.
Carried in SHAPE from c4_docs_gate73.py (D1-D6 + tag balance, chain, qm); re-written for one member by the gate74 drafter: there is
no chain (one lander), so `chain` becomes `merged` (the squash prediction onto the develop read NOW) and `qm` is not carried (no merge-in
is predicted; if one becomes necessary the kit is RE-DRAFTED, because a merge-in push carries develop's Blockchain/Dev advance and is
refused by leg 14 while KS-1450 is open — KIT_REPORT §0.3).

MODES (every PR value a REQUIRED argument; nothing defaults to the kit's pins, each is COMPARED with them):
  docs    --pr 1423 --repo <YOUR clone> --base <40-hex> --head <40-hex>
          D1 per doc: base -> head is EXACTLY ONE contiguous INSERT (difflib on lines), 0 lines replaced or deleted, inserted
             IMMEDIATELY before the one `</body>` line (`close_tag_rx`), i.e. "the ONLY difference from the base blob IS this fragment".
          D2 flow: the fragment carries exactly ONE flow number (the newline-tolerant reader from composee5_copy.py:66) == kit flow_num 26;
             cheat: exactly ONE keyed h2 (the widened reader) == kit cheat_key KS-1164; every `<h2` opening in the cheat doc is keyed.
          D3 flow numbers UNIQUE at the head; 26 ABSENT at the base.   D4 cheat keys UNIQUE at the head; KS-1164 ABSENT at the base.
          D5 TAG BALANCE (STANDING_LINES 2026-10-08: html_docs_matrix 12/0 is NOT this evidence): per tag in TAGS, the fragment's
             opens == closes, AND the whole doc's (opens - closes) is unchanged base -> head.
          D6 POSITIVE CONTROL from the DOCUMENT's shape (STANDING_LINES R 13th): a key/number KNOWN present at the base (the base's own
             LAST flow number and LAST cheat key, read from the base) reads exactly 1 with the same reader that reads 26 / KS-1164 as 0.
          D7 PLANTED ARMS on the real fragment, each asserted LANDED then refused: one `</h2>` deleted -> D5 FAILS; the fragment placed
             AFTER `</body>` -> D1 FAILS; the fragment doubled -> D1/D3 FAIL.  (A zero needs a control that prints.)
  merged  --pr 1423 --repo <YOUR clone> --base <40-hex> --head <40-hex> --develop <40-hex> [--expect-tree <40-hex>]
          M1 `git merge-tree --write-tree <develop> <head>` in YOUR clone (wgit refuses under !CODING): rc 0 and a tree.
             CONTROL: the kit's known-conflicting pair (gate73's #1407 and #1409 heads, docs-only conflict) reads rc 1 with both docs
             named, so the instrument CAN see a conflict.
          M2 diff(develop, merged) path set == the PR's own path set (3 paths): nothing else moves.
          M3 the code path(s) in merged == the head's blob; every PR path's mode == the head's.
          M4 per doc: merged blob == develop's blob with the head's EXACT fragment inserted immediately before develop's `</body>`
             (BYTES, not an inference): git's auto-merge IS the keep-both composition, so NO merge-in commit is needed.
          M5 at merged: flow numbers UNIQUE and 26 exactly once; cheat keys UNIQUE and KS-1164 exactly once; per-tag balance delta
             develop -> merged == 0.
          M6 base..develop touched the docs (reported) and touched 0 of the row's code paths.
          M7 --expect-tree given: merged tree == it (the kit's predicted_squash_tree at the draft develop).
          VERDICT line: `MERGE-IN NEEDED: no` only when M1-M5 all PASS; anything else prints `MERGE-IN NEEDED: yes/unknown — STOP`.
  --selftest --repo <clone>   planted arms through run_docs / run_merged with wrong values (each MUST fail), plus the green runs.
rc 0 all PASS / 1 any FAIL / 2 refused by name / 11 an argument != kit.json."""
import difflib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate74 import (K, ROWS, D, Tally, git, wgit, git_bytes, obj_at, mode_at, opt, row_arg, refuse_absent, code_paths,
                        flow_nums, cheat_keys, CLOSE_RX, outside_forbidden)

H2_RX = re.compile(r'<h2\b[^>]*>(.*?)</h2\s*>', re.S | re.I)
KEY_TAIL_RX = re.compile(r'(?:&mdash;|\u2014)\s*(KS-\d+)\s*$', re.S)


def cheat_split(text):
    """-> (keys, unkeyed): every <h2>...</h2> read ONE heading at a time (no lazy match can straddle two), keyed iff it ENDS in
    `— KS-n` / `&mdash; KS-n`. develop eae08a3f carries ONE heading the pinned reader cannot key ('... — KS-1445 (with KS-1367)'),
    so the merged doc is judged by: unkeyed(merged) == unkeyed(develop) (BASE-STATE, not this PR's) and the row's key exactly once."""
    keys, unkeyed = [], []
    for m in H2_RX.finditer(text):
        k = KEY_TAIL_RX.search(m.group(1))
        if k: keys.append(k.group(1))
        else: unkeyed.append(re.sub(r'\s+', ' ', m.group(1)).strip()[:90])
    return keys, unkeyed

TAGS = ('div', 'table', 'tr', 'td', 'th', 'h2', 'h3', 'h4', 'pre', 'code', 'strong', 'em', 'ul', 'ol', 'li', 'p', 'a', 'span', 'section')
DOCS = (('flow', D['flow']), ('cheat', D['cheat']))


def tag_counts(text):
    out = {}
    for t in TAGS:
        o = len(re.findall(r'<%s(?=[\s>/])' % t, text, re.I)); c = len(re.findall(r'</%s\s*>' % t, text, re.I))
        out[t] = (o, c)
    return out


def balance(text):
    return {t: o - c for t, (o, c) in tag_counts(text).items()}


def close_line(lines):
    c = [i for i, l in enumerate(lines) if CLOSE_RX.match(l)]
    if len(c) != 1: raise ValueError('close tag matched %d lines (want 1)' % len(c))
    return c[0]


def single_insert(a_lines, b_lines):
    """-> (ok, fragment_lines, msg). ok iff exactly one opcode != equal, it is an insert, and it sits immediately before a's </body>."""
    ops = [o for o in difflib.SequenceMatcher(None, a_lines, b_lines, autojunk=False).get_opcodes() if o[0] != 'equal']
    if len(ops) != 1 or ops[0][0] != 'insert':
        return False, [], 'non-equal opcodes %s (want exactly ONE insert)' % [(o[0], o[1], o[2], o[3], o[4]) for o in ops][:4]
    _, i1, i2, j1, j2 = ops[0]
    try: ci = close_line(a_lines)
    except ValueError as e: return False, [], str(e)
    frag = b_lines[j1:j2]
    # difflib may slide an insert across identical boundary lines; the bytes decide: a + frag before </body> must equal b
    composed = a_lines[:ci] + frag + a_lines[ci:]
    if composed != b_lines:
        # retry with the insert re-anchored at </body> (identical-line slide): the fragment is b's lines between a's prefix and suffix
        n = len(b_lines) - len(a_lines)
        frag2 = b_lines[ci:ci + n] if n > 0 else []
        if n > 0 and a_lines[:ci] + frag2 + a_lines[ci:] == b_lines:
            return True, frag2, 'ONE insert of %d lines immediately before </body> (line %d of the base), re-anchored across identical lines' % (n, ci + 1)
        return False, frag, 'the insert is at base line %d, NOT immediately before </body> (line %d)' % (i1 + 1, ci + 1)
    return True, frag, 'ONE insert of %d lines immediately before </body> (line %d of the base)' % (len(frag), ci + 1)


def text_of(repo, rev, path): return git_bytes(repo, rev, path).decode('utf-8')


def run_docs(repo, r, base, head, t=None, texts=None, quiet_arms=False):
    R = ROWS[r]; t = t or Tally()
    for name, path in DOCS:
        a = texts[name][0] if texts else text_of(repo, base, path)
        b = texts[name][1] if texts else text_of(repo, head, path)
        al, bl = a.split('\n'), b.split('\n')
        ok, frag, msg = single_insert(al, bl)
        t.check('D1-%s' % name, ok, '%s base -> head: %s' % (name, msg))
        ftxt = '\n'.join(frag)
        if name == 'flow':
            fn = flow_nums(ftxt); hn = flow_nums(b); bn = flow_nums(a)
            t.check('D2-flow', fn == [R['flow_num']], 'fragment flow numbers %s == [kit %d]' % (fn, R['flow_num']))
            dup = sorted(set(x for x in hn if hn.count(x) > 1))
            t.check('D3-flow', not dup and R['flow_num'] not in bn, 'head flow numbers UNIQUE (dups %s, %d numbers) | %d ABSENT at base: %s' % (
                dup or 'none', len(hn), R['flow_num'], R['flow_num'] not in bn))
            last = bn[-1] if bn else None
            t.check('D6-flow', last is not None and bn.count(last) == 1 and flow_nums(a).count(R['flow_num']) == 0,
                    'CONTROL from the DOCUMENT: the base\'s own last flow number %s reads 1 with the reader that reads %d as 0' % (last, R['flow_num']))
        else:
            try: fk = cheat_keys(ftxt); hk = cheat_keys(b); bk = cheat_keys(a)
            except ValueError as e: t.check('D2-cheat', False, str(e)); continue
            t.check('D2-cheat', fk == [R['cheat_key']], 'fragment cheat keys %s == [kit %s]; every <h2 keyed' % (fk, R['cheat_key']))
            dup = sorted(set(x for x in hk if hk.count(x) > 1))
            t.check('D4-cheat', not dup and R['cheat_key'] not in bk, 'head cheat keys UNIQUE (dups %s, %d keys) | %s ABSENT at base: %s' % (
                dup or 'none', len(hk), R['cheat_key'], R['cheat_key'] not in bk))
            last = bk[-1] if bk else None
            t.check('D6-cheat', last is not None and bk.count(last) == 1, 'CONTROL from the DOCUMENT: the base\'s own last cheat key %s reads 1' % last)
        fb = {k: v for k, v in balance(ftxt).items() if v}
        db = {k: (balance(a)[k], balance(b)[k]) for k in TAGS if balance(a)[k] != balance(b)[k]}
        t.check('D5-%s' % name, not fb and not db, '%s fragment tag balance (opens-closes != 0: %s) | whole-doc balance moved: %s | fragment counts %s' % (
            name, fb or 'none', db or 'none', {k: v for k, v in tag_counts(ftxt).items() if v != (0, 0)}))
        # D7 planted arms on THIS fragment
        if frag:
            ci = close_line(al)
            ih2 = [i for i, l in enumerate(frag) if '</h2>' in l]
            if ih2:
                bad = list(frag); bad[ih2[0]] = bad[ih2[0]].replace('</h2>', '', 1)
                landed = '\n'.join(bad).count('</h2>') == ftxt.count('</h2>') - 1
                t.check('D7a-%s' % name, landed and bool({k: v for k, v in balance('\n'.join(bad)).items() if v}),
                        'PLANTED one </h2> deleted (landed %s): the balance check REFUSES it' % landed)
            after = al[:ci + 1] + frag + al[ci + 1:]
            ok2, _, m2 = single_insert(al, after)
            t.check('D7b-%s' % name, after != bl and not ok2, 'PLANTED fragment AFTER </body>: D1 REFUSES (%s)' % m2[:80])
            dbl = al[:ci] + frag + frag + al[ci:]
            ok3, _, m3 = single_insert(al, dbl)
            if name == 'flow':
                n3 = flow_nums('\n'.join(dbl)); refused = (not ok3) or n3.count(R['flow_num']) != 1
            else:
                k3 = cheat_keys('\n'.join(dbl)); refused = (not ok3) or k3.count(R['cheat_key']) != 1
            t.check('D7c-%s' % name, refused, 'PLANTED fragment DOUBLED: refused (D1 ok=%s; own number/key count != 1)' % ok3)
    return t


def merge_tree(repo, ours, theirs):
    rc, o, e = wgit(repo, 'merge-tree', '--write-tree', '--name-only', ours, theirs)
    lines = o.split('\n')
    tree = lines[0].strip() if lines else ''
    files = []
    for l in lines[1:]:
        if not l.strip(): break
        files.append(l)
    return rc, tree, files


def run_merged(repo, r, base, head, dev, expect_tree=None, t=None):
    R = ROWS[r]; t = t or Tally()
    if not outside_forbidden(repo):
        t.check('M0', False, 'REFUSED: --repo %s is under %s; merge-tree writes objects — use YOUR OWN scratch clone' % (repo, K['forbidden_root'])); return t
    rc, tree, files = merge_tree(repo, dev, head)
    c = K['merge_tree_control']
    crc, ctree, cfiles = merge_tree(repo, c['ours'], c['theirs'])
    t.check('M1', rc == 0 and re.fullmatch(r'[0-9a-f]{40}', tree or '') is not None and crc == 1 and sorted(cfiles) == sorted(c['files']),
            'merge-tree develop %s + head %s: rc %d tree %s | CONTROL %s + %s (a known docs conflict): rc %d files %s' % (
                dev[:12], head[:12], rc, tree[:12], c['ours'][:12], c['theirs'][:12], crc, [os.path.basename(f) for f in cfiles]))
    if rc != 0:
        print('MERGE-IN NEEDED: yes/unknown — STOP (merge-tree rc %d, conflicted %s). A merge-in push carries develop\'s Blockchain/Dev advance '
              'and leg 14 refuses it while KS-1450 is open: RE-DRAFT, never --no-verify.' % (rc, files)); return t
    moved = sorted(l for l in git(repo, 'diff', '--name-only', dev, tree).split('\n') if l)
    own = sorted(R['numstat'])
    t.check('M2', moved == own, 'diff(develop, merged) paths %s == the PR\'s %d paths: %s' % ([os.path.basename(p) for p in moved], len(own), moved == own))
    bad = [p for p in code_paths(R) if obj_at(repo, tree, p) != obj_at(repo, head, p)]
    badm = [p for p in own if mode_at(repo, tree, p) != mode_at(repo, head, p)]
    t.check('M3', not bad and not badm, 'code path blobs merged == head (%d checked; differing %s) | modes == head (differing %s)' % (len(code_paths(R)), bad or 'none', badm or 'none'))
    allm = True
    for name, path in DOCS:
        dv = text_of(repo, dev, path); bs = text_of(repo, base, path); hd = text_of(repo, head, path); mg = text_of(repo, tree, path)
        ok, frag, msg = single_insert(bs.split('\n'), hd.split('\n'))
        dl = dv.split('\n'); ci = close_line(dl)
        composed = '\n'.join(dl[:ci] + frag + dl[ci:])
        eq = ok and composed.encode() == mg.encode()
        allm = allm and eq
        t.check('M4-%s' % name, eq, '%s: merged blob %s == develop %s + the head\'s %d-line fragment before </body> (BYTES): %s' % (
            name, obj_at(repo, tree, path)[:12], obj_at(repo, dev, path)[:12], len(frag), eq))
        if name == 'flow':
            mn = flow_nums(mg); dup = sorted(set(x for x in mn if mn.count(x) > 1))
            ok5 = not dup and mn.count(R['flow_num']) == 1
            t.check('M5-flow', ok5, 'merged flow numbers UNIQUE (dups %s) and %d exactly once (%d); tail %s' % (dup or 'none', R['flow_num'], mn.count(R['flow_num']), mn[-6:]))
        else:
            mk, mu = cheat_split(mg); dk, du = cheat_split(dv); dup = sorted(set(x for x in mk if mk.count(x) > 1))
            hopen = len(re.findall(r'<h2\b', mg, re.I))
            ok5 = not dup and mk.count(R['cheat_key']) == 1 and mu == du and hopen == len(mk) + len(mu)
            t.check('M5-cheat', ok5, 'merged cheat keys UNIQUE (dups %s) and %s exactly once (%d); tail %s | UNKEYED headings merged %d == develop %d (BASE-STATE, same text: %s) %s | <h2 openings %d == keyed %d + unkeyed %d' % (
                dup or 'none', R['cheat_key'], mk.count(R['cheat_key']), mk[-6:], len(mu), len(du), mu == du, mu[:2], hopen, len(mk), len(mu)))
        bd = {k: (balance(dv)[k], balance(mg)[k]) for k in TAGS if balance(dv)[k] != balance(mg)[k]}
        t.check('M5-%s-tags' % name, not bd, '%s per-tag balance develop -> merged unchanged (moved: %s)' % (name, bd or 'none'))
        allm = allm and ok5 and not bd
    anc = git(repo, 'merge-base', '--is-ancestor', base, dev, check=False)[0] == 0
    cmoved = [p for p in code_paths(R) if obj_at(repo, base, p) != obj_at(repo, dev, p)]
    dmoved = [os.path.basename(p) for _, p in DOCS if obj_at(repo, base, p) != obj_at(repo, dev, p)]
    bd_paths = [l for l in git(repo, 'diff', '--name-only', base, dev).split('\n') if l]
    bdev = [p for p in bd_paths if p.startswith('Blockchain/Dev/')]
    t.check('M6', anc and not cmoved, 'develop descends from base %s: %s | base..develop %d paths, %d under Blockchain/Dev/ %s | row code paths moved %s | docs moved %s' % (
        base[:12], anc, len(bd_paths), len(bdev), bdev[:4], cmoved or 'none', dmoved or 'none'))
    if expect_tree:
        t.check('M7', tree == expect_tree, 'merged tree %s == --expect-tree %s' % (tree[:12], expect_tree[:12]))
    if t.fails:
        print('MERGE-IN NEEDED: yes/unknown — STOP (failing %s)' % t.fails)
    else:
        print('MERGE-IN NEEDED: no — the squash is an API call that runs no local hook; predicted squash tree %s on develop %s' % (tree, dev))
        print('LEG-14 EXPOSURE: none for the squash. A merge-in push WOULD carry %d Blockchain/Dev/ path(s) of develop\'s advance (@{upstream}..HEAD) and run the full preflight.' % len(bdev))
    print('PREDICTED_TREE=%s' % tree)
    return t


def selftest(repo):
    import io, contextlib
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    def quiet(fn, *a, **k):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): tt = fn(*a, **k)
        return tt, buf.getvalue()
    R = ROWS['1423']; base = R['parents'][0]; head = R['head_expected']; dev = K['develop_at_draft']
    tt, o = quiet(run_docs, repo, '1423', base, head)
    rep(not tt.fails and tt.n == 16, 'GREEN docs at the pins: %d checked (want 16: 8 per doc), fails %s' % (tt.n, tt.fails))
    tt, o = quiet(run_merged, repo, '1423', base, head, dev, K['predicted_squash']['tree'])
    rep(not tt.fails and tt.n == 11 and 'MERGE-IN NEEDED: no' in o, 'GREEN merged at the draft develop: %d checked (want 11), fails %s' % (tt.n, tt.fails))
    # wrong head (base itself): D1 has 0 ops -> FAIL
    tt, o = quiet(run_docs, repo, '1423', base, base)
    rep('D1-flow' in tt.fails and 'D1-cheat' in tt.fails, 'PLANTED head == base: D1 FAILS on both docs')
    # a head that is NOT a docs append (gate73 #1407 vs its own base): numbers/keys != kit
    g73 = K['merge_tree_control']
    tt, o = quiet(run_docs, repo, '1423', K['merge_tree_control']['base'], g73['ours'])
    rep('D2-flow' in tt.fails and 'D2-cheat' in tt.fails, 'PLANTED another PR\'s docs (gate73 #1407 on its base): D2 FAILS (number/key != 26 / KS-1164)')
    # expect-tree wrong
    tt, o = quiet(run_merged, repo, '1423', base, head, dev, '0' * 40)
    rep('M7' in tt.fails and 'MERGE-IN NEEDED: yes' in o, 'PLANTED wrong --expect-tree: M7 FAILS and the verdict says STOP')
    # merged onto a develop that ALREADY holds the head (the head itself as develop): M2 path set != 3 / M4
    tt, o = quiet(run_merged, repo, '1423', base, head, base)
    rep(not tt.fails, '(develop == base, the PR-alone landing): GREEN — the base itself is a valid develop (%s)' % (tt.fails or 'no fails'))
    # forbidden repo
    tt, o = quiet(run_merged, '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files', '1423', base, head, dev)
    rep('M0' in tt.fails, 'PLANTED --repo = the SHARED checkout: merge-tree REFUSED (M0)')
    # in-memory doc tamper: delete a </table> in the cheat fragment -> D5
    texts = {}
    for name, path in DOCS:
        texts[name] = [text_of(repo, base, path), text_of(repo, head, path)]
    hb = texts['cheat'][1]; i = hb.rfind('</table>'); texts['cheat'][1] = hb[:i] + hb[i + 8:]
    landed = texts['cheat'][1].count('</table>') == hb.count('</table>') - 1
    tt, o = quiet(run_docs, repo, '1423', base, head, texts=texts)
    rep(landed and 'D5-cheat' in tt.fails, 'PLANTED the cheat fragment\'s last </table> deleted (landed %s): D5 REFUSES' % landed)
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]; repo = opt(A, '--repo')
    if not repo: print(__doc__); return 2
    if '--selftest' in A: return selftest(repo)
    mode = A[0] if A else ''
    r = row_arg(); R = ROWS[r]
    base, head = opt(A, '--base'), opt(A, '--head')
    if not (base and head): print('REFUSED: --base and --head are REQUIRED'); return 2
    if base != R['parents'][0]: print('REFUSED: WRONG VALUE --base %s != kit %s' % (base, R['parents'][0])); return 11
    if head != R['head_expected']: print('REFUSED: WRONG VALUE --head %s != kit %s (the kit\'s figures are for that head; re-draft)' % (head, R['head_expected'])); return 11
    if mode == 'docs':
        rc = refuse_absent(repo, [('--base', base), ('--head', head)])
        return rc or run_docs(repo, r, base, head).end()
    if mode == 'merged':
        dev = opt(A, '--develop')
        if not dev: print('REFUSED: --develop is REQUIRED'); return 2
        c = K['merge_tree_control']
        rc = refuse_absent(repo, [('--base', base), ('--head', head), ('--develop', dev), ('control ours', c['ours']), ('control theirs', c['theirs'])])
        return rc or run_merged(repo, r, base, head, dev, opt(A, '--expect-tree')).end()
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
