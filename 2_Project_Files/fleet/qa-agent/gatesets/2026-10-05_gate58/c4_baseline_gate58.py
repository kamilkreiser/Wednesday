#!/usr/bin/env python3
"""c4_baseline_gate58.py — gate58 C4: scripts/audit/audit-baseline.json, base blob vs head blob, PARSED (never grep) and by RAW BYTES.
  B1 top level: head parses; same top-level keys IN THE SAME ORDER; `$comment` value-equal AND byte-equal; base rows == kit (25).
  B2 key sets (STANDING_LINES :380, keyed on parsed KEY SETS): `accepted` REMOVED == exactly the kit removed_rows (c83g, 73wf, w9m9);
     ADDED none; head rows == kit (22); each removed row at the base carried the kit package / ticket / expires (2026-10-15) — so the
     removal is of the rows the fuse named, not look-alikes.
  B3 the 22 remaining rows: value-equal AND raw text block byte-identical to base (a re-serialisation that turns `→` into `\\u2192` is
     value-equal and byte-different), and in the SAME ORDER.
  B4 text: the diff is DELETIONS ONLY — every deleted line lies inside one of the three removed rows' base blocks, plus at most ONE
     comma-only edit (the previous row's trailing comma, only if a removed row was last); 0 inserted lines; trailing newline as base.
  B5 fuses: every remaining row's `expires` unchanged; the 2026-10-15 cohort base 3 -> head 0; other cohorts printed base -> head.
Verdict: `BASELINE PASS|FAIL: <n> FAIL of <m> checks | rows <b> -> <h> | removed <ids>`.
--selftest (in memory, from the base blob; nothing written):
  T0 base vs base -> FAIL (B2: removed 0) | T1 the three rows deleted as text -> PASS | T2 only two deleted (w9m9 kept) -> FAIL B2
  T3 T1 + an extra row (vfj7) deleted -> FAIL B2 | T4 T1 + a remaining row's `→` re-escaped as \\u2192 -> FAIL B3 by bytes, values equal
  T5 the three re-dated to 2026-10-31 instead of removed -> FAIL B2 (and B5) | T6 T1 + a planted new row -> FAIL B2 (added 1)
  T7 T1 via json.dump of the whole file (value-equal remainder) -> FAIL B3/B4 (the re-serialisation)
Usage: c4_baseline_gate58.py --repo <clone> --base <sha> --head <sha>  |  --repo <clone> --selftest.  rc 0 PASS / 1 FAIL / 2 usage."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate58 import K, commit, show, block, find_member, member_span, opcodes, now, Checks, opt_factory

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A)
REPO = opt('--repo'); RM = K['removed_rows']; BL = K['baseline']


def check(bt, ht, quiet=False):
    C = Checks(quiet=quiet); jb = json.loads(bt)
    try:
        jh = json.loads(ht)
    except ValueError as e:
        C.chk('B1 top level', False, 'head does NOT parse: %s' % e); return C, {'rows': (len(jb['accepted']), -1), 'removed': []}
    ab, ah = jb['accepted'], jh['accepted']
    C.chk('B1 top level', list(jb) == list(jh) and jb.get('$comment') == jh.get('$comment') and json.dumps(jb.get('$comment'), ensure_ascii=False) in ht and len(ab) == K['baseline_rows_base'],
          'keys (ordered) %s == %s | $comment value-equal %s, byte-present %s | base rows %d (kit %d)' % (list(jb), list(jh), jb.get('$comment') == jh.get('$comment'), json.dumps(jb.get('$comment'), ensure_ascii=False) in ht, len(ab), K['baseline_rows_base']))
    add = sorted(set(ah) - set(ab)); rem = sorted(set(ab) - set(ah))
    shape = [(g, {f: ab.get(g, {}).get(f) for f in ('package', 'ticket', 'expires')}) for g in sorted(RM)]
    shape_ok = all(s == {f: RM[g][f] for f in ('package', 'ticket', 'expires')} for g, s in shape)
    C.chk('B2 key sets', rem == sorted(RM) and not add and len(ah) == K['baseline_rows_head'] and shape_ok,
          'rows %d -> %d (kit %d) | REMOVED %s (want %s) | ADDED %s | the removed rows at base == kit package/ticket/expires: %s %s' % (
              len(ab), len(ah), K['baseline_rows_head'], rem or 'NONE', sorted(RM), add or 'NONE', shape_ok, '' if shape_ok else shape))
    keep = [k for k in ab if k in ah]; vd = [k for k in keep if ab[k] != ah[k]]; rd = [k for k in keep if block(bt, k) is None or block(bt, k) != block(ht, k)]
    order = [k for k in ah if k in ab] == keep
    C.chk('B3 remaining rows', len(keep) == K['baseline_rows_head'] and not vd and not rd and order,
          '%d remaining rows | changed by value %d %s | by raw bytes %d %s | order preserved %s' % (len(keep), len(vd), vd[:3], len(rd), rd[:3], order))
    bl = bt.split('\n'); hl = ht.split('\n'); spans = []
    for g in RM:
        i = find_member(bl, g)
        if i is not None: spans.append(member_span(bl, i))
    ops = opcodes(bt, ht); bad = []; comma = 0; deleted = 0
    for o in ops:
        if o[0] == 'delete' and all(any(s[0] <= j <= s[1] for s in spans) for j in range(o[1], o[2])):
            deleted += o[2] - o[1]; continue
        if o[0] == 'replace' and o[2] - o[1] == 1 and o[4] - o[3] == 1 and comma == 0 and bl[o[1]].rstrip() + ',' == hl[o[3]].rstrip():
            comma += 1; continue
        bad.append(o[:5])
    ins = sum(o[4] - o[3] for o in ops if o[0] in ('insert', 'replace'))
    C.chk('B4 text', not bad and ht.endswith('\n') == bt.endswith('\n') and deleted == sum(s[1] - s[0] + 1 for s in spans),
          '%d hunk(s): %d deleted line(s) inside the 3 removed rows (their blocks span %d lines) | %d comma-only edit(s) | other edits %d %s | inserted/replaced lines %d | trailing newline %s == base %s' % (
              len(ops), deleted, sum(s[1] - s[0] + 1 for s in spans), comma, len(bad), bad[:2], ins, ht.endswith('\n'), bt.endswith('\n')))
    eb = {k: v.get('expires') for k, v in ab.items()}; eh = {k: v.get('expires') for k, v in ah.items()}
    exch = sorted(k for k in keep if eb[k] != eh[k])
    coh = sorted(set(v for v in eb.values() if v) | set(v for v in eh.values() if v))
    cs = ' | '.join('%s %d -> %d' % (d, list(eb.values()).count(d), list(eh.values()).count(d)) for d in coh)
    C.chk('B5 fuses', not exch and list(eh.values()).count(K['freeze_day']) == 0 and list(eb.values()).count(K['freeze_day']) == 3,
          'expiry changed on a remaining row: %s | cohorts %s' % (exch or 'NONE', cs))
    return C, {'rows': (len(ab), len(ah)), 'removed': rem}


def delete_rows(text, ids):
    ls = text.split('\n')
    for g in ids:
        i = find_member(ls, g); a, b = member_span(ls, i)
        if not ls[b].rstrip().endswith(','): ls[a - 1] = ls[a - 1].rstrip().rstrip(',')
        del ls[a:b + 1]
    return '\n'.join(ls)


if '--selftest' in A:
    B = commit(REPO, K['base']); bt = show(REPO, B, BL)
    print('c4_baseline_gate58 SELFTEST %s | repo %s | base %s (plants in memory)' % (now(), REPO, B[:12]))
    arms = []

    def arm(name, ht, want_pass, expect):
        print('\n=== ARM %s (expected %s) ===' % (name, 'PASS' if want_pass else 'FAIL'))
        C, f = check(bt, ht); got = C.nfail() == 0; ok = expect(C, f)
        print('ARM %s: verdict %s (expected %s) | rows %d -> %d | failed %s | named as expected %s -> %s' % (name, 'PASS' if got else 'FAIL', 'PASS' if want_pass else 'FAIL',
              f['rows'][0], f['rows'][1], C.failed() or 'NONE', ok, 'OK' if (got == want_pass and ok) else 'MISMATCH'))
        arms.append(got == want_pass and ok)
    ids = sorted(RM); T1 = delete_rows(bt, ids)
    arm('T0 base-vs-base', bt, False, lambda C, f: f['rows'] == (25, 25) and 'B2 key sets' in C.failed() and 'B1 top level' not in C.failed())
    arm('T1 the three rows deleted', T1, True, lambda C, f: f['rows'] == (25, 22))
    arm('T2 only two deleted (w9m9 kept)', delete_rows(bt, ['GHSA-c83g-rgw3-j3cx', 'GHSA-73wf-gq98-2v4g']), False, lambda C, f: f['rows'] == (25, 23) and 'B2 key sets' in C.failed())
    arm('T3 an extra row (vfj7) deleted', delete_rows(bt, ids + ['GHSA-vfj7-8cjw-p6xm']), False, lambda C, f: f['rows'] == (25, 21) and 'B2 key sets' in C.failed() and 'B4 text' in C.failed())
    keep = [k for k in json.loads(T1)['accepted'] if '→' in (block(T1, k) or '')]
    if keep:
        T4 = T1.replace(block(T1, keep[0]), block(T1, keep[0]).replace('→', '\\u2192'), 1)
        print('(T4 re-escapes the arrows of %s; values equal: %s)' % (keep[0], json.loads(T4)['accepted'][keep[0]] == json.loads(T1)['accepted'][keep[0]]))
        arm('T4 a remaining row re-escaped', T4, False, lambda C, f: 'B3 remaining rows' in C.failed() and 'B2 key sets' not in C.failed())
    else:
        print('T4 SKIPPED: no remaining row carries a non-ASCII arrow'); arms.append(False)
    T5 = bt
    for g in ids: T5 = T5.replace(block(bt, g), block(bt, g).replace('"expires": "2026-10-15"', '"expires": "2026-10-31"'), 1)
    arm('T5 re-dated instead of removed', T5, False, lambda C, f: 'B2 key sets' in C.failed() and 'B5 fuses' in C.failed())
    ls = T1.split('\n'); i = find_member(ls, 'GHSA-vfj7-8cjw-p6xm'); ls[i:i] = ['    "GHSA-zzzz-gate-58pl": {', '      "package": "x",', '      "reason": "plant",', '      "ticket": "KS-749"', '    },']
    arm('T6 T1 + a planted new row', '\n'.join(ls), False, lambda C, f: f['rows'] == (25, 23) and 'B2 key sets' in C.failed())
    j = json.loads(bt)
    for g in ids: del j['accepted'][g]
    T7 = json.dumps(j, indent=2) + '\n'
    print('(T7 json.dump of the whole file: remainder value-equal %s, bytes equal to T1 %s)' % (json.loads(T7) == json.loads(T1), T7 == T1))
    arm('T7 json.dump re-serialisation', T7, False, lambda C, f: f['rows'] == (25, 22) and ('B3 remaining rows' in C.failed() or 'B4 text' in C.failed()))
    n = arms.count(False)
    print('\nSELFTEST %s: %d of %d arms returned their expected verdict' % ('OK' if n == 0 else 'MISMATCH', len(arms) - n, len(arms)))
    raise SystemExit(1 if n else 0)

B = commit(REPO, opt('--base', K['base'])); H = commit(REPO, opt('--head') or sys.exit('--head <sha> is required (or --selftest)'))
print('c4_baseline_gate58 %s | repo %s | base %s | head %s' % (now(), REPO, B, H))
C, f = check(show(REPO, B, BL), show(REPO, H, BL)); n = C.nfail()
print('BASELINE %s: %d FAIL of %d checks | rows %d -> %d | removed %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), f['rows'][0], f['rows'][1], f['removed']))
raise SystemExit(1 if n else 0)
