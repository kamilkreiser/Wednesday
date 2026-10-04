#!/usr/bin/env python3
"""c4_baseline_gate54f.py — gate54f C4: scripts/audit/audit-baseline.json, base blob vs head blob, PARSED (never grep) and by RAW BYTES.
  B1 top level: same key set; `$comment` value-equal; rows base == kit baseline_rows_base (24).
  B2 key sets: `accepted` ADDED == exactly the kit new_rows ids (+2); REMOVED none; kit forbidden_row (GHSA-ch52-4w7c-c8xp) absent at head.
  B3 each new row: package / ticket / expires == kit (braces KS-1403, node-forge KS-1404, both 2026-10-31); `reason` a non-empty string;
     its key set is ONE OF THE KEY SETS the base rows already use AND contains package/reason/ticket/expires; R2's exact shape
     {expires, package, reason, ticket} reported separately (INFO R2-SHAPE exact | deviates).
  B4 the 24 old rows: value-equal AND raw text block byte-identical (a re-serialisation that turns `→` into `\\u2192` is value-equal and byte-different).
  B5 text: only insertions, plus at most ONE replaced line whose only change is a trailing comma added (appending after the last row);
     trailing newline as base. Fuse census: rows expiring 2026-10-31 base -> head; every dated row's expiry unchanged.
Verdict: `BASELINE PASS|FAIL: <n> FAIL of <m> checks | rows <b> -> <h> | added <ids>`.
--selftest (in memory, from the base blob; nothing written):
  T0 base vs base -> FAIL with +0 rows | T1 the two legitimate rows appended -> PASS | T2 T1 + a ch52 row -> FAIL (B2)
  T3 T1 + an old row's `→` re-escaped as \\u2192 -> FAIL on B4 by raw bytes while values stay equal | T4 expiry 2026-11-01 -> FAIL (B3)
  T5 tickets swapped -> FAIL (B3) | T6 T1 inserted MID-file (no comma edit) -> PASS (the second legitimate shape)
Usage: c4_baseline_gate54f.py --repo <clone> --base <sha> --head <sha>  |  --repo <clone> --selftest.  rc 0 PASS / 1 FAIL / 2 usage."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate54f import K, commit, show, block, opcodes, now, Checks

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO = opt('--repo'); NEW = K['new_rows']; FORB = K['forbidden_row']; BL = K['baseline']


def check(bt, ht):
    C = Checks(); jb, jh = json.loads(bt), json.loads(ht); ab, ah = jb['accepted'], jh['accepted']
    C.chk('B1 top level', sorted(jb) == sorted(jh) and jb.get('$comment') == jh.get('$comment') and len(ab) == K['baseline_rows_base'],
          'keys %s == %s | $comment equal %s | base rows %d (kit %d)' % (sorted(jb), sorted(jh), jb.get('$comment') == jh.get('$comment'), len(ab), K['baseline_rows_base']))
    add = sorted(set(ah) - set(ab)); rem = sorted(set(ab) - set(ah))
    C.chk('B2 key sets', add == sorted(NEW) and not rem and FORB not in ah,
          'rows %d -> %d | ADDED %s (want %s) | REMOVED %s | %s at head: %s' % (len(ab), len(ah), add, sorted(NEW), rem or 'NONE', FORB, 'PRESENT' if FORB in ah else 'absent'))
    shapes = set(tuple(sorted(v)) for v in ab.values())
    for gid, want in sorted(NEW.items()):
        r = ah.get(gid)
        if r is None:
            C.chk('B3 %s' % gid, False, 'row ABSENT at head'); continue
        ks = tuple(sorted(r)); exact = ks == tuple(K['new_row_keys'])
        C.chk('B3 %s' % gid, all(r.get(f) == want[f] for f in want) and isinstance(r.get('reason'), str) and r['reason'].strip() != '' and ks in shapes and set(K['new_row_keys']) <= set(ks),
              'package %r ticket %r expires %r (want %s) | reason %d chars | keys %s, an existing base shape: %s' % (
                  r.get('package'), r.get('ticket'), r.get('expires'), json.dumps(want), len(r.get('reason') or ''), list(ks), ks in shapes))
        print('INFO R2-SHAPE %s %s (R2: %s)' % (gid, 'exact' if exact else 'DEVIATES', K['new_row_keys']))
    old = sorted(set(ab) & set(ah)); vd = [k for k in old if ab[k] != ah[k]]; rd = [k for k in old if block(bt, k) is None or block(bt, k) != block(ht, k)]
    C.chk('B4 old rows', len(old) == K['baseline_rows_base'] and not vd and not rd,
          '%d old rows | changed by value %d %s | by raw bytes %d %s' % (len(old), len(vd), vd[:3], len(rd), rd[:3]))
    ops = opcodes(bt, ht); bl, hl = bt.split('\n'), ht.split('\n'); bad = []; comma = 0
    for o in ops:
        if o[0] == 'insert': continue
        if o[0] == 'replace' and o[2] - o[1] == 1 and comma == 0 and hl[o[3]] == bl[o[1]] + ',' :
            comma += 1; continue
        if o[0] == 'replace' and o[2] - o[1] == 1 and comma == 0 and hl[o[3]].rstrip() == bl[o[1]].rstrip() + ',':
            comma += 1; continue
        bad.append(o[:5])
    ins = sum(o[4] - o[3] for o in ops) - comma
    eb = {k: v.get('expires') for k, v in ab.items()}; eh = {k: v.get('expires') for k, v in ah.items()}
    exch = sorted(k for k in old if eb[k] != eh[k]); co = (sum(1 for v in eb.values() if v == '2026-10-31'), sum(1 for v in eh.values() if v == '2026-10-31'))
    C.chk('B5 text + fuses', not bad and ht.endswith('\n') == bt.endswith('\n') and not exch,
          '%d hunk(s): +%d inserted line(s), %d comma-only line edit(s), other edits %d %s | trailing newline %s == base %s | expiry changed on an old row: %s | 2026-10-31 cohort %d -> %d' % (
              len(ops), ins, comma, len(bad), bad[:2], ht.endswith('\n'), bt.endswith('\n'), exch or 'NONE', co[0], co[1]))
    return C, {'rows': (len(ab), len(ah)), 'added': add}


def row_lines(gid, r, ind='    '):
    out = ['%s"%s": {' % (ind, gid)]; items = list(r.items())
    for i, (k, v) in enumerate(items): out.append('%s  "%s": %s%s' % (ind, k, json.dumps(v, ensure_ascii=False), ',' if i < len(items) - 1 else ''))
    return out + ['%s}' % ind]


def append_rows(text, rows):
    ls = text.split('\n'); end = max(i for i, l in enumerate(ls) if l == '  }')   # the close of `accepted`
    ls[end - 1] = ls[end - 1] + ','; new = []
    for n, (g, r) in enumerate(rows):
        rl = row_lines(g, r)
        if n < len(rows) - 1: rl[-1] += ','
        new += rl
    ls[end:end] = new; return '\n'.join(ls)


def insert_mid(text, rows):
    ls = text.split('\n'); i = next(j for j, l in enumerate(ls) if l.startswith('    "GHSA-'))   # before the FIRST row: no comma edit
    new = []
    for g, r in rows: rl = row_lines(g, r); rl[-1] += ','; new += rl
    ls[i:i] = new; return '\n'.join(ls)


def legit(t=None, e=None):
    rows = []
    for g, w in sorted(NEW.items()):
        rows.append((g, {'package': w['package'], 'reason': 'gate54f selftest plant: reason text', 'ticket': (t or {}).get(g, w['ticket']), 'expires': e or w['expires']}))
    return rows


if '--selftest' in A:
    B = commit(REPO, K['base']); bt = show(REPO, B, BL)
    print('c4_baseline_gate54f SELFTEST %s | repo %s | base %s (plants in memory)' % (now(), REPO, B[:12]))
    arms = []
    def arm(name, ht, want_pass, expect):
        print('\n=== ARM %s (expected %s) ===' % (name, 'PASS' if want_pass else 'FAIL'))
        C, f = check(bt, ht); got = C.nfail() == 0; ok = expect(C, f)
        print('ARM %s: verdict %s (expected %s) | rows %d -> %d | named failure as expected %s -> %s' % (name, 'PASS' if got else 'FAIL', 'PASS' if want_pass else 'FAIL', f['rows'][0], f['rows'][1], ok, 'OK' if (got == want_pass and ok) else 'MISMATCH'))
        arms.append(got == want_pass and ok)
    arm('T0 base-vs-base', bt, False, lambda C, f: f['rows'] == (24, 24) and f['added'] == [] and C.failed('B2') and not C.failed('B4'))
    T1 = append_rows(bt, legit()); arm('T1 two legitimate rows appended', T1, True, lambda C, f: f['rows'] == (24, 26))
    arm('T2 T1 + a ch52 row', append_rows(bt, legit() + [(FORB, {'package': 'http-cache-semantics', 'reason': 'x', 'ticket': 'KS-1403', 'expires': '2026-10-31'})]), False, lambda C, f: FORB in f['added'] and C.failed('B2') and not C.failed('B4'))
    arrow = next(k for k in json.loads(bt)['accepted'] if '→' in (block(bt, k) or ''))
    T3 = T1.replace(block(bt, arrow), block(bt, arrow).replace('→', '\\u2192'), 1)
    print('(T3 re-escapes the arrows of %s; values stay equal: %s)' % (arrow, json.loads(T3)['accepted'][arrow] == json.loads(bt)['accepted'][arrow]))
    arm('T3 T1 + an old row re-escaped', T3, False, lambda C, f: f['rows'] == (24, 26) and C.failed('B4') and not C.failed('B3') and not C.failed('B2'))
    arm('T4 expiry 2026-11-01', append_rows(bt, legit(e='2026-11-01')), False, lambda C, f: f['rows'] == (24, 26) and len(C.failed('B3')) == 2 and not C.failed('B4'))
    arm('T5 tickets swapped', append_rows(bt, legit(t={'GHSA-vfj7-8cjw-p6xm': 'KS-1404', 'GHSA-86w9-cpqp-85rv': 'KS-1403'})), False, lambda C, f: f['rows'] == (24, 26) and len(C.failed('B3')) == 2 and not C.failed('B4'))
    arm('T6 rows inserted mid-file', insert_mid(bt, legit()), True, lambda C, f: f['rows'] == (24, 26))
    n = arms.count(False)
    print('\nSELFTEST %s: %d of %d arms returned their expected verdict' % ('OK' if n == 0 else 'MISMATCH', len(arms) - n, len(arms)))
    raise SystemExit(1 if n else 0)

B = commit(REPO, opt('--base', K['base'])); H = commit(REPO, opt('--head') or sys.exit('--head <sha> is required (or --selftest)'))
print('c4_baseline_gate54f %s | repo %s | base %s | head %s' % (now(), REPO, B, H))
C, f = check(show(REPO, B, BL), show(REPO, H, BL)); n = C.nfail()
print('BASELINE %s: %d FAIL of %d checks | rows %d -> %d | added %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), f['rows'][0], f['rows'][1], f['added']))
raise SystemExit(1 if n else 0)
