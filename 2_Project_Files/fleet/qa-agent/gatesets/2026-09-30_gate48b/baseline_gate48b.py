#!/usr/bin/env python3
"""baseline_gate48b.py — the drafter's READ of the audit baseline and its contract across the two PRs (a PREDICTION for ROW-PERMANENT-FIELDS,
CONTRACT-LINE-ONLY, NO-BASELINE-ROW (#1355), FUSE-COUNT and FOLLOW-ONS; the gate re-derives each). From the SCRATCH clone, `git show` at develop,
at #1354's head (pins, or --head1354 <sha> for a control), at #1355's head and at END:
  R1 ROW-PERMANENT-FIELDS (#1354 vs develop): `accepted` gains EXACTLY {GHSA-r53p-7pc4-xj5r}; none removed; every other row JSON-equal; `$comment`
     and the top-level keys byte-equal; the new row's fields EXACTLY {package, reason, ticket, decidedAt} — NO `expires` (Kam's ruling (c):
     permanent, like the twelve siblings); package `undici`; ticket `KS-470`; decidedAt `2026-09-30`; `git diff -U0` has no `-` line.
  R2 CONTRACT-LINE-ONLY (#1354 vs develop): baseline-contract.mjs `git diff --numstat` == 1 0; the one `+` line is `'GHSA-r53p-7pc4-xj5r',` (with
     its trailing comment, if any) INSIDE the GRANDFATHERED_NO_EXPIRY Set literal, and ALPHABETICAL: its neighbours sort below and above it.
  R3 the contract's own equality at #1354's head AND at END: GRANDFATHERED_NO_EXPIRY == the set of rows with NO `expires` (develop 17 == 17;
     #1354 / END 18 == 18).
  R4 THE REASON: the new row's `reason` split into numbered sentences VERBATIM -> row_reason_gate48b.md (only for the REAL head); INFO: it names
     Kam's card id `secuura-undici-ghsa-r53p-exception-1354` and `2026-09-30`; FLAG any sentence carrying `build-tree only` / `build tree only` /
     `only in the build` (gate48a's finding: undici is installed in the issuer image's BUILDER stage — "build-tree only" is not sufficient on its
     own; whether each sentence is TRUE is the gate's).
  R5 NO-BASELINE-ROW for #1355: audit-baseline.json and baseline-contract.mjs at #1355's head == develop's; at END == #1354's head's.
  R6 FUSE-COUNT at END: the rows whose `expires` == 2026-10-09, every distinct `expires` value with its count, the hours left (UTC, NOW).
  R7 THE CLEANUP AT END (the seat's leg-6 line at #1355-alone was 14 rows; with #1354's permanent r53p row also no longer reported under the
     override, the prediction at END is 15: 13 undici + 2 ip-address): which exist at END, which are GRANDFATHERED (so the cleanup must edit the
     contract too), which sit on the fuse.
rc 0 BASELINE PASS / rc 1 FAIL. Usage: baseline_gate48b.py <scratchpad> [--head1354 <sha>] [--pins <pins json> (controls: a SIM pin set)]"""
import json, os, re, subprocess, sys, datetime, hashlib
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]
P = json.load(open(A[A.index('--pins') + 1] if '--pins' in A else os.path.join(G, 'pins_gate48b.json'), encoding='utf-8'))   # --pins: controls / a simulated pin set only
SP = A[0]; CL = os.path.join(SP, 'g48b_sp', 'clone')
DEV = P['develop']; REAL = P['prs']['1354']['head']; H4 = A[A.index('--head1354') + 1] if '--head1354' in A else REAL; H5 = P['prs']['1355']['head']; END = P['end_tree']
BL = 'Blockchain/Dev/scripts/audit/audit-baseline.json'; CT = 'Blockchain/Dev/scripts/audit/baseline-contract.mjs'; FUSE = K['fuse_date']; NEW = 'GHSA-r53p-7pc4-xj5r'
CARD = K['kam_ruling']['card']
CLEANUP = [('GHSA-2mjp-6q6p-2qxm', 'undici', 'KS-470'), ('GHSA-35p6-xmwp-9g52', 'undici', 'KS-470'), ('GHSA-4992-7rv2-5pvq', 'undici', 'KS-470'),
           ('GHSA-g8m3-5g58-fq7m', 'undici', 'KS-470'), ('GHSA-g9mf-h72j-4rw9', 'undici', 'KS-470'), ('GHSA-p88m-4jfj-68fv', 'undici', 'KS-470'),
           ('GHSA-v9p9-hfj2-hcw8', 'undici', 'KS-470'), ('GHSA-vrm6-8vpv-qv8q', 'undici', 'KS-470'), ('GHSA-vxpw-j846-p89q', 'undici', 'KS-470'),
           ('GHSA-v2v4-37r5-5v8g', 'ip-address', 'KS-470'), ('GHSA-mwp4-54f8-5fhr', 'ip-address', 'KS-729'),
           ('GHSA-8xcm-r25x-g524', 'undici', 'KS-559'), ('GHSA-m8rv-5g2x-5cg5', 'undici', 'KS-559'), ('GHSA-v3r7-h72x-cjcm', 'undici', 'KS-559'),
           (NEW, 'undici', 'KS-470')]
def git(*a):
    r = subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=True)
    if r.returncode: raise SystemExit('REFUSING: git %s rc %d %s' % (' '.join(a[:3]), r.returncode, r.stderr[:200]))
    return r.stdout
bad = []
def chk(tag, ok, msg):
    print('%s %s: %s' % ('PASS' if ok else 'FAIL', tag, msg))
    if not ok: bad.append(tag)
now = datetime.datetime.now(datetime.timezone.utc)
print('baseline_gate48b %s | develop %s | #1354 head %s%s | #1355 head %s | END %s' % (now.strftime('%Y-%m-%dT%H:%M:%SZ'), DEV[:12], H4[:12], ' (CONTROL SUBJECT)' if H4 != REAL else '', H5[:12], END[:12]))
tb, th = git('show', '%s:%s' % (DEV, BL)), git('show', '%s:%s' % (H4, BL)); b, h = json.loads(tb), json.loads(th); ba, ha = b['accepted'], h['accepted']
added = sorted(set(ha) - set(ba)); removed = sorted(set(ba) - set(ha)); changed = sorted(k for k in set(ba) & set(ha) if ba[k] != ha[k])
minus = [l for l in git('diff', '-U0', DEV, H4, '--', BL).splitlines() if l.startswith('-') and not l.startswith('---')]
r = ha.get(NEW) or {}
print('    rows %d -> %d | ADDED %s | REMOVED %s | CHANGED %s | numstat %s' % (len(ba), len(ha), added, removed or 'none', changed or 'none', ' '.join(git('diff', '--numstat', DEV, H4, '--', BL).split()[:2]) or 'empty'))
chk('R1', added == [NEW] and not removed and not changed and sorted(b) == sorted(h) and b.get('$comment') == h.get('$comment') and not minus
    and sorted(r) == sorted(['package', 'reason', 'ticket', 'decidedAt']) and r.get('package') == 'undici' and r.get('ticket') == 'KS-470' and r.get('decidedAt') == '2026-09-30' and bool((r.get('reason') or '').strip()),
    'ROW-PERMANENT-FIELDS: one row added (%s), none removed / changed, $comment equal, -U0 `-` lines %d | fields %s | package %r ticket %r decidedAt %r | expires %s | reason %d chars' % (
        NEW, len(minus), sorted(r), r.get('package'), r.get('ticket'), r.get('decidedAt'), repr(r['expires']) + ' PRESENT' if 'expires' in r else 'ABSENT', len(r.get('reason') or '')))
cd, ch = git('show', '%s:%s' % (DEV, CT)), git('show', '%s:%s' % (H4, CT))
ns = git('diff', '--numstat', DEV, H4, '--', CT).split()[:2]
u0 = git('diff', '-U0', DEV, H4, '--', CT).splitlines(); plus = [l[1:] for l in u0 if l.startswith('+') and not l.startswith('+++')]; mn = [l for l in u0 if l.startswith('-') and not l.startswith('---')]
def gset(t):
    m = re.search(r'GRANDFATHERED_NO_EXPIRY\s*=\s*new Set\(\[(.*?)\]\);', t, re.S)
    return re.findall(r"'(GHSA-[a-z0-9-]+)'", m.group(1)) if m else []
lh = gset(ch); pos = lh.index(NEW) if NEW in lh else -1
alpha = pos > 0 and (pos == len(lh) - 1 or lh[pos - 1] < NEW < lh[pos + 1]) and lh[pos - 1] < NEW
chk('R2', ns == ['1', '0'] and not mn and len(plus) == 1 and re.match(r"\s*'%s',(\s*//.*)?$" % NEW, plus[0] or '') is not None and pos >= 0 and alpha and [x for x in lh if x != NEW] == gset(cd),
    'CONTRACT-LINE-ONLY: numstat %s | + line %r | inside the Set at position %d of %d | neighbours %s < %s < %s: %s | the other entries unchanged and in order: %s' % (
        ' '.join(ns) or 'empty', plus[0] if plus else None, pos, len(lh), lh[pos - 1] if pos > 0 else '-', NEW, lh[pos + 1] if 0 <= pos < len(lh) - 1 else '-', alpha, [x for x in lh if x != NEW] == gset(cd)))
def eqset(t, lab):
    acc = json.loads(git('show', '%s:%s' % (t, BL)))['accepted']; gf = set(gset(git('show', '%s:%s' % (t, CT)))); ne = set(k for k, v in acc.items() if 'expires' not in v)
    print('    %s: GRANDFATHERED_NO_EXPIRY %d == the %d rows with NO expires: %s (only-in-set %s, only-in-rows %s)' % (lab, len(gf), len(ne), gf == ne, sorted(gf - ne) or 'none', sorted(ne - gf) or 'none'))
    return gf == ne, len(gf)
e0, n0 = eqset(DEV, 'develop'); e4, n4 = eqset(H4, '#1354 head'); eE, nE = eqset(END, 'END')
chk('R3', e0 and e4 and eE and n4 == n0 + 1 and nE == n4, 'the contract\'s equality holds at develop (%d), #1354 (%d) and END (%d)' % (n0, n4, nE))
rs = (r.get('reason') or '')
ss = [s.strip() for s in re.split(r'(?<=[.;])\s+(?=[A-Za-z(])', rs) if s.strip()]
bto = [i + 1 for i, s in enumerate(ss) if re.search(r'build[- ]tree only|only in the build|build[- ]only', s, re.I)]
print('INFO R4 reason: %d sentence(s), sha256 %s | names the card id %s: %s | names 2026-09-30: %s | sentence(s) carrying a build-tree-only phrase: %s' % (
    len(ss), hashlib.sha256(rs.encode()).hexdigest()[:16], CARD, CARD in rs, '2026-09-30' in rs, bto or 'none'))
if bto: print('FLAG R4: sentence(s) %s carry a build-tree-only phrase — gate48a found undici installed in the issuer BUILDER stage: the gate rules each TRUE / FALSE' % bto)
if H4 == REAL and rs and '--pins' not in A:
    out = ['# gate48b — #1354\'s PERMANENT GHSA-r53p row: its `reason`, VERBATIM, split into sentences for ROW-PERMANENT-FIELDS', '',
           'Read %s by baseline_gate48b.py: `git show %s:%s`, row `%s`. reason sha256 %s, %d chars, %d sentence(s). The split is at `. ` / `; ` before a letter; the gate checks EVERY factual sentence as a row (claim · instrument + tree/image · TRUE / FALSE / UNMEASURED / TRUE-BUT-CONDITIONAL). The drafter checked NONE. It is a PUBLISHED record and it is now PERMANENT: every later triage reads it.' % (
               now.strftime('%Y-%m-%dT%H:%M:%SZ'), H4, BL, NEW, hashlib.sha256(rs.encode()).hexdigest(), len(rs), len(ss)), '']
    out += ['%d. %s' % (i + 1, s) for i, s in enumerate(ss)]
    open(os.path.join(G, 'row_reason_gate48b.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print('INFO R4 -> row_reason_gate48b.md')
b5 = [git('rev-parse', '%s:%s' % (t, p)).strip() for t in (DEV, H5) for p in (BL, CT)]; bE = [git('rev-parse', '%s:%s' % (t, p)).strip() for t in (H4, END) for p in (BL, CT)]
chk('R5', b5[0] == b5[2] and b5[1] == b5[3] and bE[0] == bE[2] and bE[1] == bE[3], 'NO-BASELINE-ROW (#1355): baseline %s / contract %s at develop == at #1355 (%s / %s) | END == #1354\'s head (baseline %s, contract %s): %s' % (
    b5[0][:12], b5[1][:12], b5[2][:12], b5[3][:12], bE[2][:12], bE[3][:12], bE[0] == bE[2] and bE[1] == bE[3]))
acc = json.loads(git('show', '%s:%s' % (END, BL)))['accepted']; gfE = set(gset(git('show', '%s:%s' % (END, CT))))
fz = sorted((k, v.get('package'), v.get('ticket')) for k, v in acc.items() if v.get('expires') == FUSE)
dist = {}
for v in acc.values(): dist[v.get('expires', '(none)')] = dist.get(v.get('expires', '(none)'), 0) + 1
hrs = (datetime.datetime(2026, 10, 9, tzinfo=datetime.timezone.utc) - now).total_seconds() / 3600
print('    END rows %d | expires values: %s' % (len(acc), ' | '.join('%s x%d' % (k, v) for k, v in sorted(dist.items()))))
print('    FUSE rows (%s) at END: %d %s | %.1f h to %sT00:00:00Z, computed at %s (UTC; the contract lapses a row ON the named day)' % (FUSE, len(fz), fz, hrs, FUSE, now.strftime('%Y-%m-%dT%H:%M:%SZ')))
chk('R6', len(fz) == 4 and NEW not in [x[0] for x in fz], 'FUSE-COUNT at END: %d row(s) on %s; the r53p row is NOT on it (permanent)' % (len(fz), FUSE))
rows = []; okc = True
for g_, pk, tk in CLEANUP:
    x = acc.get(g_) or {}; ok = x.get('package') == pk and x.get('ticket') == tk; okc &= ok
    rows.append((g_, pk, tk, x.get('expires', '(none)'), g_ in gfE, ok))
    print('    CLEANUP(pred.) %s %-10s %-7s | at END: expires %-10s | GRANDFATHERED %-5s | present as named: %s' % (g_, pk, tk, x.get('expires', '(none)'), g_ in gfE, ok))
onf = [x[0] for x in rows if x[3] == FUSE]
chk('R7', okc and len(rows) == 15, 'the predicted END CLEANUP: 15 rows (%d undici + %d ip-address) all present; GRANDFATHERED %d of 15 (the cleanup edits the contract too); on the fuse %s -> fuse after the cleanup %d' % (
    sum(x[1] == 'undici' for x in rows), sum(x[1] == 'ip-address' for x in rows), sum(x[4] for x in rows), onf, len(fz) - len(onf)))
print('BASELINE %s: %d FAIL | #1354 row PERMANENT (no expires), contract +1 | #1355 NO ROW | FUSE-COUNT %d on %s at END, %.1f h | CLEANUP(pred.) 15, %d GRANDFATHERED, %d on the fuse' % (
    'PASS' if not bad else 'FAIL', len(bad), len(fz), FUSE, hrs, sum(x[4] for x in rows), len(onf)))
raise SystemExit(1 if bad else 0)
