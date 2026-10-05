#!/usr/bin/env python3
"""c2b_docfix_gate57.py — gate57 C2 (#1380), the DOC half: the two owed one-line corrections as CHARACTER diffs, and every other byte of
the KS 1404 / KS 1015 blocks identical. Read-only (git objects); prints only.
  F0 BLOCK BOUNDS at cut_base (both docs): each kit base_blocks span opens with its first_line_rx, holds >= 20 lines, and the ruled line
     sits INSIDE its named block (a vacuous 2-line span is not a byte-identity proof).
  F1 Q-27 (cheat :3738, D's KS 1404 block): base line == kit old, head line == kit new; SAME LENGTH, exactly TWO differing indices, and they
     are the '27' -> '36' digits; '# 27 cells' 1 -> 0 and '# 36 cells' 0 -> 1 in the cheat sheet, 0 / 0 in the flow doc (both sides).
  F1c THE CELL COUNT: the KS 1404 test file at cut_base counts 36 cells by an instrument that counts `it(` lines PLUS each `it.each([`
     table's rows; CONTROL: the `it(` count alone (32) != 36, so the instrument is not the naive one.
  F2 N-1375-1 (flow :1875, cheat :3721 — the KS 1015 block of BOTH docs): head line == base line with ONLY kit old_sentence replaced by kit
     new_sentence (common prefix and suffix byte-identical); the new sentence carries every kit n1375_required_elements; 'other 27 KS-1015'
     (case-insensitive) 1 -> 0 per doc; FIRING CONTROL: the base line vs itself with one sentence character changed reads exactly 1 index.
  F3 BYTE-IDENTITY of the rest: for each doc and each of KS 1015 / KS 1404, every base line of the block except the ruled line(s) is
     byte-equal at the SAME line number in the head (the PR's blocks are appended after them), and the count of changed lines inside
     the block == the ruled count (KS 1015 flow 1, cheat 1; KS 1404 flow 0, cheat 1).
  F4 NOTHING ELSE REPLACED: base->head line opcodes per doc are exactly {the ruled replaced lines} + ONE tail insert before `  </body>`;
     0 deleted lines (flow -1 / cheat -2 in numstat are those replacements).
  F5 PR 2 (#1381) does NOT touch the ruled lines: at its head '# 27 cells' 1 and 'other 27 KS-1015' 1 (they are PR 1's to change).
--selftest: plants into COPIES of the real texts — a 3-character Q-27 mutation, Q-27 in the flow doc instead, a trailing space on the
N-1375-1 line, '26 remain' dropped, a second sentence edited in the same line, another line of the KS 1404 block touched, the fix in one doc
only, a deleted line, Q-27 written as '# 36  cells' (length +1): each must land on its named check; the real head must PASS.
Usage: c2b_docfix_gate57.py --repo <clone> [--head <#1380 sha>] [--head2 <#1381 sha>] [--selftest]     rc 0 PASS / 1 FAIL / 2 usage"""
import os, re, sys, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate57 import K, git, now, Checks, opt_factory, show, has_commit, opcodes, char_diff

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A); REPO = opt('--repo'); CUT = K['cut_base']
H1 = opt('--head', K['prs']['pr1']['ready_head']); H2 = opt('--head2', K['prs']['pr2']['ready_head'])
for s in (CUT, H1, H2):
    if not re.fullmatch(r'[0-9a-f]{40}', s) or not has_commit(REPO, s):
        print('REFUSING: %s is not a 40-hex commit present in %s' % (s, REPO)); raise SystemExit(2)
FLOW, CHEAT = K['docs']; FX = K['doc_fixes']; BB = K['base_blocks']; MIN_LINES = 20


def ci(text, s):
    return len(re.findall(re.escape(s), text, re.I))


def cells(src):
    n_it = len(re.findall(r'(?m)^\s*it\(', src)); rows = 0
    for m in re.finditer(r'it\.each\(\[\n(.*?)\n\s*\]\)', src, re.S):
        rows += len([l for l in m.group(1).split('\n') if re.match(r'^\s*\[', l)])
    return n_it, rows


def analyse(BD, HD, HD2, ks1404_src):
    C = Checks()
    # F0
    msgs = []; ok0 = True
    for d in K['docs']:
        bl = BD[d].split('\n')
        for name, b in BB[d].items():
            first = bl[b['first'] - 1]; n = b['last'] - b['first'] + 1; good = re.match(b['first_line_rx'], first) is not None and n >= MIN_LINES
            ok0 &= good; msgs.append('%s %s %d-%d (%d lines) opens %r: %s' % (d[19:25], name, b['first'], b['last'], n, first.strip()[:30], good))
    for fk, f in FX.items():
        b = BB[f['doc']][f['block']]; inside = b['first'] <= f['line'] <= b['last']; ok0 &= inside; msgs.append('%s line %d inside %s: %s' % (fk, f['line'], f['block'], inside))
    C.chk('F0 block bounds', ok0, ' | '.join(msgs))
    # F1 Q-27
    q = FX['Q27']; bq = BD[q['doc']].split('\n')[q['line'] - 1]; hq = HD[q['doc']].split('\n')[q['line'] - 1]
    same, idx = char_diff(bq, hq)
    digits = same and idx == [i for i in range(len(bq)) if bq[i] != hq[i]] and len(idx) == 2 and bq[idx[0]:idx[-1] + 1] == '27' and hq[idx[0]:idx[-1] + 1] == '36'
    cnt = {(t, d[19:24], s): ci(T[d], t) for t in ('# 27 cells', '# 36 cells') for d in K['docs'] for s, T in (('base', BD), ('head', HD))}
    want = {('# 27 cells', 'QA_To', 'base'): 1, ('# 27 cells', 'QA_To', 'head'): 0, ('# 36 cells', 'QA_To', 'base'): 0, ('# 36 cells', 'QA_To', 'head'): 1,
            ('# 27 cells', 'API_S', 'base'): 0, ('# 27 cells', 'API_S', 'head'): 0, ('# 36 cells', 'API_S', 'base'): 0, ('# 36 cells', 'API_S', 'head'): 0}
    C.chk('F1 Q-27 character diff', bq == q['old'] and hq == q['new'] and digits and cnt == want,
          'base :%d == kit old %s | head == kit new %s | same length %s (%d) | differing indices %s (want 2, the digits 27 -> 36: %s) | counts %s%s' % (
              q['line'], bq == q['old'], hq == q['new'], same, len(hq), idx if same else 'n/a (prefix/suffix %s)' % (idx,), digits,
              {'%s %s %s' % k: v for k, v in cnt.items() if v}, '' if cnt == want else ' MISMATCH vs %s' % {'%s %s %s' % k: v for k, v in want.items() if v}))
    mut = bq[:idx[0]] + 'abc' + bq[idx[0] + 3:] if same and idx else bq
    s2, i2 = char_diff(bq, mut)
    n_it, rows = cells(ks1404_src or '')
    C.chk('F1c 36 cells counted', n_it + rows == K['ks1404_cells_expected'] and n_it != K['ks1404_cells_expected'] and s2 and len(i2) == 3,
          '%s at %s: it( %d + it.each rows %d = %d (kit %d) | CONTROL the it( count alone %d != %d: %s | firing control: a 3-character mutation of the base line reads %d differing indices' % (
              K['ks1404_test'].split('/')[-1], CUT[:12], n_it, rows, n_it + rows, K['ks1404_cells_expected'], n_it, K['ks1404_cells_expected'], n_it != K['ks1404_cells_expected'], len(i2) if s2 else -1))
    # F2 N-1375-1
    for fk in ('N1375_1_flow', 'N1375_1_cheat'):
        f = FX[fk]; d = f['doc']; bline = BD[d].split('\n')[f['line'] - 1]; hline = HD[d].split('\n')[f['line'] - 1]
        exp = bline.replace(f['old_sentence'], f['new_sentence'], 1) if bline.count(f['old_sentence']) == 1 else None
        p = bline.find(f['old_sentence']); pre_ok = p >= 0 and hline.startswith(bline[:p]) and hline.endswith(bline[p + len(f['old_sentence']):])
        elems = [e for e in K['n1375_required_elements'] if e not in hline]
        o27 = (ci(BD[d], 'other 27 KS-1015'), ci(HD[d], 'other 27 KS-1015'))
        C.chk('F2 N-1375-1 %s' % d[19:24], exp is not None and hline == exp and pre_ok and not elems and o27 == (1, 0),
              'base :%d carries the old sentence once: %s | head == base with ONLY the sentence replaced: %s | prefix (%d chars) and suffix byte-identical: %s | required elements missing %s | "other 27 KS-1015" base %d -> head %d' % (
                  f['line'], exp is not None, hline == exp, max(p, 0), pre_ok, elems or 'NONE', o27[0], o27[1]))
    # F3 + F4
    ruled = {}
    for f in FX.values():
        ruled.setdefault(f['doc'], set()).add(f['line'])
    for d in K['docs']:
        bl = BD[d].split('\n'); hl = HD[d].split('\n'); ops = opcodes(bl, hl)
        rep = sorted(i + 1 for op, i1, i2, j1, j2 in ops if op == 'replace' and i2 - i1 == j2 - j1 for i in range(i1, i2))
        other = [(op, i1 + 1, i2, j1 + 1, j2) for op, i1, i2, j1, j2 in ops if not (op == 'replace' and i2 - i1 == j2 - j1)]
        tail = [o for o in other if o[0] == 'insert' and bl[o[1] - 1] == K['doc_close_anchor']]
        C.chk('F4 only ruled lines replaced %s' % d[19:24], rep == sorted(ruled.get(d, ())) and len(other) == 1 and len(tail) == 1,
              'replaced base lines %s (ruled %s) | other hunks %s (want exactly ONE insert before %r)' % (rep, sorted(ruled.get(d, ())), other, K['doc_close_anchor'].strip()))
        for name, b in BB[d].items():
            span = range(b['first'], b['last'] + 1); diff = [n for n in span if n > len(hl) or bl[n - 1] != hl[n - 1]]
            want_n = sorted(f['line'] for f in FX.values() if f['doc'] == d and f['block'] == name)
            C.chk('F3 %s %s byte-identical but ruled' % (name, d[19:24]), diff == want_n,
                  'base %d-%d (%d lines): lines differing at the same line number in the head %s (want exactly the ruled %s)' % (b['first'], b['last'], len(span), diff, want_n))
    # F5
    f5 = {d[19:24]: (ci(HD2[d], '# 27 cells'), ci(HD2[d], 'other 27 KS-1015')) for d in K['docs']}
    C.chk('F5 PR 2 leaves the ruled lines', f5 == {'API_S': (0, 1), 'QA_To': (1, 1)}, "at #1381's head ('# 27 cells', 'other 27 KS-1015') per doc %s (want flow (0, 1), cheat (1, 1))" % f5)
    return C


def load(sha):
    T = {}
    for d in K['docs']:
        T[d] = show(REPO, sha, d)
        if T[d] is None: raise SystemExit('REFUSING: %s absent at %s' % (d, sha[:12]))
    return T


print('c2b_docfix_gate57 %s | repo %s | cut_base %s | #1380 %s | #1381 %s | mode %s' % (now(), REPO, CUT[:12], H1[:12], H2[:12], 'selftest' if '--selftest' in A else 'gate'))
BD = load(CUT); HD = load(H1); HD2 = load(H2); SRC = show(REPO, CUT, K['ks1404_test'])
if '--selftest' in A:
    q = FX['Q27']; nf = FX['N1375_1_flow']; nc = FX['N1375_1_cheat']
    def plant(d, fn, T=None):
        t = dict(T or HD); t[d] = fn(t[d]); return t
    def at(n, fn):
        def g(s):
            L = s.split('\n'); L[n - 1] = fn(L[n - 1]); return '\n'.join(L)
        return g
    arms = [
        ('T0 real #1380 head', HD, HD2, None),
        ('T1 Q-27 with a 3-character change', plant(q['doc'], at(q['line'], lambda l: l.replace('# 36 cells', '# 36 cellz'))), HD2, 'F1 '),
        ('T2 Q-27 written "# 36  cells" (length +1)', plant(q['doc'], at(q['line'], lambda l: l.replace('# 36 cells', '# 36  cells'))), HD2, 'F1 '),
        ('T3 a trailing space on the N-1375-1 flow line', plant(nf['doc'], at(nf['line'], lambda l: l + ' ')), HD2, 'F2 N-1375-1 API_S'),
        ('T4 "26 remain" dropped from the cheat sentence', plant(nc['doc'], at(nc['line'], lambda l: l.replace('so 26 remain unowned', 'the rest remain unowned'))), HD2, 'F2 N-1375-1 QA_To'),
        ('T5 a second sentence edited on the cheat N-1375-1 line', plant(nc['doc'], at(nc['line'], lambda l: l.replace('pre-existing;', 'pre-existing,', 1))), HD2, 'F2 N-1375-1 QA_To'),
        ('T6 another line of the cheat KS 1404 block touched', plant(CHEAT, at(BB[CHEAT]['KS1404']['first'] + 5, lambda l: l + 'x')), HD2, 'F3 KS1404 QA_To'),
        ('T7 N-1375-1 fixed in the cheat sheet only', plant(FLOW, at(nf['line'], lambda l: l.replace(nf['new_sentence'], nf['old_sentence']))), HD2, 'F2 N-1375-1 API_S'),
        ('T8 a deleted line in the flow KS 1015 block', plant(FLOW, lambda s: '\n'.join(l for i, l in enumerate(s.split('\n')) if i != BB[FLOW]['KS1015']['first'] + 3)), HD2, 'F4'),
        ('T9 PR 2 had changed "# 27 cells" too', HD, plant(CHEAT, lambda s: s.replace('# 27 cells', '# 36 cells'), HD2), 'F5'),
        ('T10 a line outside both blocks touched (head)', plant(FLOW, lambda s: s.replace('</head>', '</head> ', 1)), HD2, 'F4'),
    ]
    ok = 0
    for name, hd, hd2, want in arms:
        if want is not None and hd == HD and hd2 == HD2:
            print('SELFTEST MISS %s: the plant changed NOTHING (an inert plant is not an arm)' % name); continue
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): C = analyse(BD, hd, hd2, SRC)
        f = C.failed(); good = (not f) if want is None else any(x.startswith(want) for x in f)
        ok += good; print('SELFTEST %s %s: want %s | failed %s' % ('OK' if good else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, f or 'NONE'))
        for l in buf.getvalue().splitlines():
            if (l.startswith('FAIL') and want and l[5:].startswith(want)) or not good: print('    ' + l[:260])
    print('SELFTEST %s %d of %d' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms))); raise SystemExit(0 if ok == len(arms) else 1)
C = analyse(BD, HD, HD2, SRC); n = C.nfail()
print('C2b DOCFIX %s: %d FAIL of %d checks | #1380 %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), H1[:12]))
raise SystemExit(1 if n else 0)
