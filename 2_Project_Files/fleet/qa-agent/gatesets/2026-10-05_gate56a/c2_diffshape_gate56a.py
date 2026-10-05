#!/usr/bin/env python3
"""c2_diffshape_gate56a.py — gate56a C2 DIFF SHAPE for ONE of Seat B 59th's two date-only PRs (READ ONLY: git show + local files; prints only).
  --which pr3  (KS-528, Blockchain/Dev/scripts/audit/audit-baseline.json) — BOTH sides PARSED as JSON:
     J1 top-level keys and `$comment` equal.   J2 `accepted` count base == head == kit accepted_count (25), same keys IN THE SAME ORDER
        (no row added, removed or moved).   J3 every OTHER row is equal field-for-field AND in field order (json.dumps without sort).
     J4 the two react-router rows: `expires` base == kit old (2026-10-09) and head == kit new (2026-10-31), the literal Kam ruled.
     J5 the two rows: every field other than `expires` / `reason` equal and in the same order; `reason` either byte-equal or the base reason
        followed by an APPENDED note (prefix-preserving; the note is printed for the tester to read — the ONLY allowance in this file).
     J6 RAW TEXT: a line diff base -> head touches ONLY the `"expires"` line (required) and the `"reason"` line (optional, the appended note)
        of the two rows; same line count; same trailing newline. (Catches a re-indent or a key reorder that parses equal.)
  --which pr4  (KS-769, Blockchain/Dev/scripts/audit/lock-discovery.mjs) — LINE diff around the KS-769 entry:
     L1 the region opens at exactly ONE `      ticket: 'KS-769',` line on each side, at the same line number; every line BEFORE it byte-equal.
     L2 every line AFTER the entry's `expires:` line byte-equal.
     L3 head's `expires:` line == `      expires: '2027-01-01',` exactly (kit new_line); base's == kit old_line.
     L4 every line strictly between ticket and expires is a `//` comment on BOTH sides (comments may change; no code may enter).
     L5 exactly ONE `expires: '<date>'` literal in the file on each side.
     WARN L6 (never a FAIL): the head comment block still names the OLD expiry (2026-10-19 / 19 Oct / 2026-10-18) — a comment that is no
        longer true of the value is for the tester to rule (D-L6 in the README).
  Base-state run (no --head and no --head-file): prints the base facts and exits 4 "NO PR YET — base state" (never a PASS).
  --selftest: synthetic variants built IN MEMORY from the base text: the intended edit (and, pr3, the edit plus an appended reason note;
     pr4, the edit plus a rewritten comment) must PASS; each WRONG edit must FAIL its own row (pr3: wrong date, one row only, a third row
     re-dated, a row added, a row removed, a reason rewritten, rows reordered, re-indented; pr4: 2026-12-31, a code line changed, a second
     expires literal, the ticket changed, a line added after the entry).
Usage: c2_diffshape_gate56a.py --which pr3|pr4 --repo <clone or checkout> [--base sha] [--head sha | --head-file f] [--base-file f] [--selftest]
rc 0 PASS / 1 FAIL / 2 usage / 4 base state only"""
import difflib, io, contextlib, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate56a import K, now, Checks, has_commit, pr_cfg, side_text, opt_factory

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--which' not in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A)
W = opt('--which'); P = pr_cfg(W); REPO = opt('--repo'); BASE = opt('--base', K['base']); HEAD = opt('--head'); HF = opt('--head-file'); BF = opt('--base-file')
for s in [BASE] + ([HEAD] if HEAD else []):
    if not re.fullmatch(r'[0-9a-f]{40}', s or '') or not has_commit(REPO, s):
        print('REFUSING: %r is not a full sha of a commit in %s' % (s, REPO)); raise SystemExit(2)
if HEAD and HF:
    print('REFUSING: --head and --head-file are exclusive'); raise SystemExit(2)
BT = side_text(REPO, BASE, P['path'], BF)


def row_span(lines, rid):
    """[first, last] line index of a row `"<rid>": {` .. its closing `    },` / `    }` in a 2-space-indented accepted map"""
    st = [i for i, l in enumerate(lines) if l.strip().startswith('"%s": {' % rid)]
    if len(st) != 1:
        return None
    ind = len(lines[st[0]]) - len(lines[st[0]].lstrip())
    for j in range(st[0] + 1, len(lines)):
        if re.fullmatch(r' {%d}\},?' % ind, lines[j]):
            return (st[0], j)
    return None


def analyse_pr3(bt, ht):
    C = Checks()
    try:
        b = json.loads(bt); h = json.loads(ht)
    except Exception as e:
        C.chk('J0 parse', False, 'a side does not parse: %s' % e); return C
    C.chk('J1 top level', list(b) == list(h) and b.get('$comment') == h.get('$comment'), 'keys base %s head %s | $comment equal %s' % (list(b), list(h), b.get('$comment') == h.get('$comment')))
    ba, ha = b.get('accepted', {}), h.get('accepted', {})
    C.chk('J2 rows', list(ba) == list(ha) and len(ha) == P['accepted_count'],
          'accepted base %d head %d (kit %d) | same keys in the same order %s | added %s | removed %s' % (
              len(ba), len(ha), P['accepted_count'], list(ba) == list(ha), sorted(set(ha) - set(ba)) or 'NONE', sorted(set(ba) - set(ha)) or 'NONE'))
    others = [k for k in ba if k not in P['rows']]
    diff_o = [k for k in others if json.dumps(ba.get(k)) != json.dumps(ha.get(k))]
    C.chk('J3 other rows', not diff_o, '%d other rows field-for-field AND field-order equal; differing: %s' % (len(others), diff_o or 'NONE'))
    ex = {k: ((ba.get(k) or {}).get('expires'), (ha.get(k) or {}).get('expires')) for k in P['rows']}
    C.chk('J4 the two expires', all(v == (P['old'], P['new']) for v in ex.values()), 'base -> head %s (want %s -> %s, the ruled literal)' % (ex, P['old'], P['new']))
    j5 = []; notes = {}
    for k in P['rows']:
        bo, ho = ba.get(k) or {}, ha.get(k) or {}
        same_fields = [f for f in bo if f not in ('expires', 'reason')] == [f for f in ho if f not in ('expires', 'reason')] and list(bo) == list(ho)
        same_vals = all(bo.get(f) == ho.get(f) for f in bo if f not in ('expires', 'reason'))
        br, hr = bo.get('reason', ''), ho.get('reason', '')
        app = hr == br or hr.startswith(br)
        notes[k] = hr[len(br):] if app else 'NOT AN APPEND'
        j5.append(same_fields and same_vals and app)
    C.chk('J5 row fields', all(j5), 'per row (fields + order + values equal except expires/reason; reason byte-equal or APPENDED): %s' % dict(zip(P['rows'], j5)))
    for k, n in notes.items():
        print('INFO J5 %s reason appended note: %r' % (k, n[:300] if n else '(none — reason byte-equal)'))
    bl, hl = bt.split('\n'), ht.split('\n')
    allowed = set()
    for k in P['rows']:
        sp = row_span(bl, k)
        if sp:
            for i in range(sp[0], sp[1] + 1):
                if re.match(r'\s*"(expires|reason)":', bl[i]):
                    allowed.add(i)
    sm = difflib.SequenceMatcher(None, bl, hl, autojunk=False)
    touched = []; bad = []; shape_ok = True
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        if tag != 'replace' or (i2 - i1) != (j2 - j1):
            shape_ok = False; bad.append('%s base %d-%d head %d-%d' % (tag, i1 + 1, i2, j1 + 1, j2)); continue
        for i in range(i1, i2):
            touched.append(i)
            if i not in allowed:
                bad.append('base line %d %r' % (i + 1, bl[i][:80]))
            else:
                hi = j1 + (i - i1)
                kb = re.match(r'(\s*"\w+":)', bl[i]); kh = re.match(r'(\s*"\w+":)', hl[hi])
                if not kb or not kh or kb.group(1) != kh.group(1):
                    bad.append('base line %d key/indent changed' % (i + 1))
    exp_lines = [i for i in touched if '"expires"' in bl[i]]
    C.chk('J6 raw text', shape_ok and not bad and len(exp_lines) == 2 and len(bl) == len(hl) and bt.endswith('\n') == ht.endswith('\n'),
          'lines base %d head %d | changed base lines %s (allowed: the expires/reason lines of the two rows) | expires lines changed %d (want 2) | outside the allowance %s | trailing newline equal %s' % (
              len(bl), len(hl), [i + 1 for i in touched], len(exp_lines), bad or 'NONE', bt.endswith('\n') == ht.endswith('\n')))
    return C


def analyse_pr4(bt, ht):
    C = Checks()
    bl, hl = bt.split('\n'), ht.split('\n')
    tb = [i for i, l in enumerate(bl) if l == P['region_start_line']]; th = [i for i, l in enumerate(hl) if l == P['region_start_line']]
    if len(tb) != 1 or len(th) != 1:
        C.chk('L1 region', False, 'ticket line %r count base %d head %d (want 1 each)' % (P['region_start_line'], len(tb), len(th))); return C
    i, k = tb[0], th[0]
    eb = next((j for j in range(i + 1, len(bl)) if re.match(r'\s*expires:', bl[j])), None)
    eh = next((j for j in range(k + 1, len(hl)) if re.match(r'\s*expires:', hl[j])), None)
    C.chk('L1 region + prefix', i == k and bl[:i + 1] == hl[:k + 1], 'ticket line at base :%d head :%d | every line up to it byte-equal %s' % (i + 1, k + 1, bl[:i + 1] == hl[:k + 1]))
    if eb is None or eh is None:
        C.chk('L2 suffix', False, 'no expires line after the ticket (base %s head %s)' % (eb, eh)); return C
    C.chk('L2 suffix', bl[eb + 1:] == hl[eh + 1:], 'every line after expires byte-equal: %s (base :%d.. %d lines, head :%d.. %d lines)' % (bl[eb + 1:] == hl[eh + 1:], eb + 2, len(bl) - eb - 1, eh + 2, len(hl) - eh - 1))
    C.chk('L3 expires literal', bl[eb] == P['old_line'] and hl[eh] == P['new_line'], 'base :%d %r (want %r) | head :%d %r (want %r)' % (eb + 1, bl[eb].strip(), P['old_line'].strip(), eh + 1, hl[eh].strip(), P['new_line'].strip()))
    cb, ch = bl[i + 1:eb], hl[k + 1:eh]
    okc = all(re.match(r'\s*//', l) for l in cb) and all(re.match(r'\s*//', l) for l in ch)
    C.chk('L4 comments only', okc, 'between ticket and expires: base %d lines (:%d-:%d) head %d lines (:%d-:%d), all `//` comments %s' % (len(cb), i + 2, eb, len(ch), k + 2, eh, okc))
    lit = lambda L: sum(1 for l in L if re.match(r"\s*expires: '\d{4}-\d{2}-\d{2}',?\s*$", l))
    C.chk('L5 one literal', lit(bl) == 1 and lit(hl) == 1, "`expires: '<date>'` literals base %d head %d (want 1 each)" % (lit(bl), lit(hl)))
    for d in difflib.unified_diff(cb, ch, 'base comment', 'head comment', lineterm='', n=0):
        print('INFO L4 comment diff: %s' % d)
    stale = [l.strip() for l in ch if re.search(r'2026-10-19|2026-10-18|19 Oct', l)]
    print('%s L6 stale comment: head comment lines naming the OLD expiry: %s' % ('WARN' if stale else 'INFO', stale or 'NONE'))
    return C


AN = analyse_pr3 if W == 'pr3' else analyse_pr4
print('c2_diffshape_gate56a %s | %s %s %s | repo %s | base %s%s | head %s' % (now(), W, P['ticket'], P['path'], REPO, BASE[:12], ' (BASE-FILE %s)' % BF if BF else '',
      ('SYNTHETIC FILE %s' % HF) if HF else (HEAD or 'NONE')))

if '--selftest' in A:
    arms = []
    if W == 'pr3':
        b = json.loads(BT); bl = BT.split('\n')
        def edit_line(text, rid, field, fn):
            L = text.split('\n'); s = row_span(L, rid)
            for x in range(s[0], s[1] + 1):
                if re.match(r'\s*"%s":' % field, L[x]):
                    L[x] = fn(L[x])
            return '\n'.join(L)
        good = BT
        for r in P['rows']:
            good = edit_line(good, r, 'expires', lambda l: l.replace(P['old'], P['new']))
        note = good
        for r in P['rows']:
            note = edit_line(note, r, 'reason', lambda l: l[:l.rstrip().rfind('"')] + ' RE-DATED 2026-10-05: expires 2026-10-09 -> 2026-10-31 under KS-528 (card secuura-fuse-1009-measured-1001 a).' + l[l.rstrip().rfind('"'):])
        wrong = BT
        for r in P['rows']:
            wrong = edit_line(wrong, r, 'expires', lambda l: l.replace(P['old'], '2026-11-30'))
        one = edit_line(BT, P['rows'][0], 'expires', lambda l: l.replace(P['old'], P['new']))
        third = edit_line(good, 'GHSA-ggr8-5vv4-36mx', 'expires', lambda l: l.replace('2026-10-31', '2026-11-30'))
        d = json.loads(good); acc = d['accepted']; acc['GHSA-zzzz-zzzz-zzzz'] = {'package': 'react-router', 'reason': 'x', 'ticket': 'KS-528', 'expires': '2026-10-31'}
        added = json.dumps(d, indent=2, ensure_ascii=False) + '\n'
        d = json.loads(good); del d['accepted']['GHSA-ggr8-5vv4-36mx']; removed = json.dumps(d, indent=2, ensure_ascii=False) + '\n'
        rew = edit_line(good, P['rows'][1], 'reason', lambda l: '      "reason": "rewritten",')
        d = json.loads(good); items = list(d['accepted'].items()); items[0], items[1] = items[1], items[0]; d['accepted'] = dict(items)
        reorder = json.dumps(d, indent=2, ensure_ascii=False) + '\n'
        reindent = '\n'.join(('\t' + l[2:]) if l.startswith('  ') else l for l in good.split('\n'))
        arms = [('T0 intended edit', good, None), ('T0b intended edit + appended reason note', note, None), ('T1 wrong date 2026-11-30', wrong, 'J4'),
                ('T2 one row only', one, 'J4'), ('T3 a third row re-dated', third, 'J3'), ('T4 a row ADDED', added, 'J2'), ('T5 a row REMOVED', removed, 'J2'),
                ('T6 a reason REWRITTEN', rew, 'J5'), ('T7 rows reordered', reorder, 'J2'), ('T8 re-indented (parses equal)', reindent, 'J6')]
    else:
        good = BT.replace(P['old_line'], P['new_line'])
        bl = BT.split('\n'); i = bl.index(P['region_start_line'])
        cm = BT.split('\n'); e = cm.index(P['old_line']); cm[e] = P['new_line']; cm[e - 2:e] = ["      // KS-769 re-dated 2026-10-05 (card secuura-mobile-dormant-fuse-lapses-1019b a): valid through Thu 31 Dec 2026;",
                                                                                              "      // isLapsed is `expires <= utcToday()`, so '2027-01-01' lapses 00:00Z Fri 1 Jan 2027."]
        comment = '\n'.join(cm)
        wrong = BT.replace(P['old_line'], "      expires: '2026-12-31',")
        code = good.replace("      ticket: 'KS-769',", "      ticket: 'KS-769',", 1).replace("'(2 critical, 45 high) pending", "'(2 critical, 46 high) pending", 1)
        dup = good.replace(P['new_line'], P['new_line'] + "\n      // x\n      expires: '2027-01-01',", 1)
        tick = good.replace("      ticket: 'KS-769',", "      ticket: 'KS-770',", 1)
        after = good.replace(P['new_line'], P['new_line'] + "\n      scope: 'x',", 1)
        arms = [('T0 intended edit', good, None), ('T0b intended edit + rewritten comment', comment, None), ('T1 wrong value 2026-12-31', wrong, 'L3'),
                ('T2 a code line (reason text) changed', code, 'L1'), ('T3 a second expires literal', dup, 'L5'), ('T4 ticket changed', tick, 'L1'),
                ('T5 a field added after expires', after, 'L2')]
    ok = 0
    for name, ht, want in arms:
        with contextlib.redirect_stdout(io.StringIO()):
            C = AN(BT, ht)
        f = C.failed(); good_arm = (not f) if want is None else any(x.startswith(want) for x in f)
        ok += good_arm
        print('SELFTEST %s %s: want %s | failed %s' % ('OK' if good_arm else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, f or 'NONE'))
    print('SELFTEST %s %d of %d (%s)' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms), W)); raise SystemExit(0 if ok == len(arms) else 1)

if not HEAD and not HF:
    if W == 'pr3':
        b = json.loads(BT)['accepted']
        print('BASE STATE %s: accepted %d | %s' % (BASE[:12], len(b), {k: b[k].get('expires') for k in P['rows']}))
    else:
        bl = BT.split('\n'); e = bl.index(P['old_line']) if P['old_line'] in bl else -1
        print('BASE STATE %s: %s at :%d | region ticket :%d' % (BASE[:12], P['old_line'].strip(), e + 1, bl.index(P['region_start_line']) + 1 if P['region_start_line'] in bl else 0))
    print('C2 %s NO PR YET — base state only (rc 4; never a PASS)' % W); raise SystemExit(4)

HT = side_text(REPO, HEAD, P['path'], HF)
C = AN(BT, HT)
n = C.nfail(); print('C2 %s %s: %d FAIL of %d | %s%s' % (W, 'PASS' if n == 0 else 'FAIL', n, len(C.res), P['path'], ' | SYNTHETIC head (never evidence of the PR)' if HF else ''))
raise SystemExit(1 if n else 0)
