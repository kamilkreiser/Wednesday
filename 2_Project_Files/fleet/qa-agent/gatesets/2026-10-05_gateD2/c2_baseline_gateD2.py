#!/usr/bin/env python3
"""c2_baseline_gateD2.py — gateD2 C2: scripts/audit/audit-baseline.json, base blob vs head blob, PARSED and by RAW BYTES (a NEW COPY of
gate54f's c4_baseline, inverted: this PR REMOVES one row and adds none).
  B1 top level: same key set; `$comment` value-equal; base rows == kit baseline_rows_base (26).
  B2 key sets: REMOVED == exactly [kit baseline_removed_row] (GHSA-86w9-cpqp-85rv); ADDED none.
  B3 the 25 surviving rows: value-equal AND raw text block byte-identical (a re-serialisation that re-escapes a character is value-equal
     and byte-different).
  B4 text: the only hunk is ONE contiguous DELETE of exactly the removed row's block (and at most one comma-only edit on its neighbour);
     trailing newline as base; every surviving row's `expires` unchanged.
Verdict `BASELINE PASS|FAIL: <n> FAIL of <m> | rows <b> -> <h> | removed <ids>`.
--selftest (in memory, from the base blob; nothing written): T0 base vs base -> FAIL (B2) | T1 the row removed -> PASS | T2 a second row also
removed -> FAIL (B2) | T3 a surviving row's expiry changed -> FAIL (B3/B4) | T4 a surviving row re-escaped -> FAIL (B3 raw bytes, values equal)
| T5 the drafted head blob -> PASS.
Usage: c2_baseline_gateD2.py --repo <clone> --base <sha> --head <sha> | --repo <clone> --selftest   (rc 0 PASS / 1 FAIL / 2 usage)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gateD2 import K, commit, show, find_member, member_span, opcodes, now, Checks

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO = opt('--repo'); RM = K['baseline_removed_row']; BL = K['baseline']


def block(text, key):
    ls = text.split('\n'); i = find_member(ls, key)
    if i is None: return None
    sp = member_span(ls, i); return '\n'.join(ls[sp[0]:sp[1] + 1]).rstrip(',') if sp else None


def check(bt, ht):
    C = Checks(); jb, jh = json.loads(bt), json.loads(ht); ab, ah = jb['accepted'], jh['accepted']
    C.chk('B1 top level', sorted(jb) == sorted(jh) and jb.get('$comment') == jh.get('$comment') and len(ab) == K['baseline_rows_base'],
          'keys equal %s | $comment equal %s | base rows %d (kit %d)' % (sorted(jb) == sorted(jh), jb.get('$comment') == jh.get('$comment'), len(ab), K['baseline_rows_base']))
    add = sorted(set(ah) - set(ab)); rem = sorted(set(ab) - set(ah))
    C.chk('B2 key sets', rem == [RM] and not add, 'rows %d -> %d | REMOVED %s (want [%s]) | ADDED %s' % (len(ab), len(ah), rem, RM, add or 'NONE'))
    old = sorted(set(ab) & set(ah)); vd = [k for k in old if ab[k] != ah[k]]; rd = [k for k in old if block(bt, k) is None or block(bt, k) != block(ht, k)]
    C.chk('B3 surviving rows', len(old) == K['baseline_rows_base'] - 1 and not vd and not rd, '%d surviving rows | changed by value %d %s | by raw bytes %d %s' % (len(old), len(vd), vd[:3], len(rd), rd[:3]))
    ops = opcodes(bt, ht); bl = bt.split('\n'); i = find_member(bl, RM); sp = member_span(bl, i) if i is not None else None
    dels = [o for o in ops if o[0] == 'delete']; other = [o for o in ops if o[0] != 'delete']
    comma = [o for o in other if o[0] == 'replace' and o[2] - o[1] == 1 and o[4] - o[3] == 1 and bt.split('\n')[o[1]].rstrip().rstrip(',') == ht.split('\n')[o[3]].rstrip().rstrip(',')]
    # difflib may slide a deleted block by one line inside identical `}` / `},` context: accept a delete whose size equals the block's
    okdel = sp is not None and len(dels) == 1 and (dels[0][2] - dels[0][1]) == (sp[1] - sp[0] + 1) and abs(dels[0][1] - sp[0]) <= 1
    exch = sorted(k for k in old if ab[k].get('expires') != ah[k].get('expires'))
    C.chk('B4 text', okdel and len(other) == len(comma) <= 1 and ht.endswith('\n') == bt.endswith('\n') and not exch,
          'deletes %s (want ONE of %s lines at base %s) | other hunks %d (comma-only %d) | trailing newline equal %s | expiry changed on a surviving row %s' % (
              [(o[1] + 1, o[2] - o[1]) for o in dels], (sp[1] - sp[0] + 1) if sp else '?', (sp[0] + 1) if sp else '?', len(other), len(comma), ht.endswith('\n') == bt.endswith('\n'), exch or 'NONE'))
    return C, {'rows': (len(ab), len(ah)), 'removed': rem}


def remove_row(text, key):
    ls = text.split('\n'); i = find_member(ls, key); a, b = member_span(ls, i)
    if not ls[b].rstrip().endswith(','): ls[a - 1] = ls[a - 1].rstrip().rstrip(',')
    del ls[a:b + 1]; return '\n'.join(ls)


if '--selftest' in A:
    B = commit(REPO, K['base']); bt = show(REPO, B, BL); H = commit(REPO, K['drafted_first_commit']); hd = show(REPO, H, BL)
    print('c2_baseline_gateD2 SELFTEST %s | base %s | drafted head %s (plants in memory)' % (now(), B[:12], H[:12]))
    rows = list(json.loads(bt)['accepted']); other = next(k for k in rows if k != RM)
    T1 = remove_row(bt, RM); arms = []
    def arm(name, ht, want_pass, expect):
        print('\n=== ARM %s (expected %s) ===' % (name, 'PASS' if want_pass else 'FAIL'))
        C, f = check(bt, ht); got = C.nfail() == 0; ok = expect(C, f)
        print('ARM %s: verdict %s (expected %s) | rows %d -> %d | named failure as expected %s -> %s' % (name, 'PASS' if got else 'FAIL', 'PASS' if want_pass else 'FAIL', f['rows'][0], f['rows'][1], ok, 'OK' if got == want_pass and ok else 'MISMATCH'))
        arms.append(got == want_pass and ok)
    arm('T0 base-vs-base', bt, False, lambda C, f: f['removed'] == [] and C.failed('B2'))
    arm('T1 the one row removed', T1, True, lambda C, f: f['rows'] == (26, 25))
    arm('T2 a second row removed', remove_row(T1, other), False, lambda C, f: C.failed('B2'))
    AB = json.loads(bt)['accepted']; ex = next(k for k in rows if k != RM and AB[k].get('expires') and ('"expires": "%s"' % AB[k]['expires']) in (block(bt, k) or ''))
    T3 = T1.replace(block(bt, ex), block(bt, ex).replace('"expires": "%s"' % AB[ex]['expires'], '"expires": "2099-01-01"'), 1)
    print('(T3 re-dates %s %s -> 2099-01-01; plant landed: %s)' % (ex, AB[ex]['expires'], T3 != T1)); assert T3 != T1, 'T3 plant did not land'
    arm('T3 a surviving expiry changed', T3, False, lambda C, f: C.failed('B3') and C.failed('B4'))
    blk = block(bt, other); esc = blk.replace('-', '\\u002d', 1) if '"reason": "' in blk else blk
    arm('T4 a surviving row re-escaped', T1.replace(blk, esc, 1), False, lambda C, f: C.failed('B3') and not C.failed('B2'))
    arm('T5 the drafted head blob', hd, True, lambda C, f: f['rows'] == (26, 25))
    n = arms.count(False); print('\nSELFTEST %s: %d of %d arms' % ('OK' if n == 0 else 'MISMATCH', len(arms) - n, len(arms))); raise SystemExit(1 if n else 0)

B = commit(REPO, opt('--base', K['base'])); H = commit(REPO, opt('--head') or sys.exit('--head <sha> is required (or --selftest)'))
print('c2_baseline_gateD2 %s | repo %s | base %s | head %s' % (now(), REPO, B, H))
C, f = check(show(REPO, B, BL), show(REPO, H, BL)); n = C.nfail()
print('BASELINE %s: %d FAIL of %d checks | rows %d -> %d | removed %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), f['rows'][0], f['rows'][1], f['removed']))
raise SystemExit(1 if n else 0)
