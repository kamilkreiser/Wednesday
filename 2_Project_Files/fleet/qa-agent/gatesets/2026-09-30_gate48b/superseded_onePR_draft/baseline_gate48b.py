#!/usr/bin/env python3
"""baseline_gate48b.py — the drafter's READ of the audit baseline around #1355 (a PREDICTION for NO-BASELINE-ROW, FUSE-COUNT and FOLLOW-ONS;
the gate re-derives each). From the SCRATCH clone, `git show` of Blockchain/Dev/scripts/audit/audit-baseline.json and baseline-contract.mjs:
  B1 NO BASELINE ROW: audit-baseline.json's blob at develop == at the head (or --head <sha>) == at END; `git diff --numstat` empty.
  B2 the contract's own equality at END: GRANDFATHERED_NO_EXPIRY (parsed from the .mjs: the GHSA ids between `new Set([` and `]);`) == the
     set of rows with NO `expires`; the contract blob at develop == head.
  B3 FUSE-COUNT at END: the rows whose `expires` == 2026-10-09 (count, ids, package, ticket), every distinct `expires` value with its count,
     and the hours left to 2026-10-09T00:00:00Z computed NOW (UTC). The seat: 4 at develop and at END (#1355 adds no row; only #1354 would).
  B4 THE 14-ROW CLEANUP (the seat's leg-6 line at config iii, VERBATIM in the capture — the drafter runs no leg): the rows the seat names
     exist at END with the package and ticket the line prints (12 undici: 9 KS-470 + 3 KS-559; 2 ip-address: KS-470, KS-729); which are
     GRANDFATHERED (no expires); which sit on the fuse date; the severity of each undici row is read in lockdelta_1.out (D5). If the
     cleanup lands, the fuse count becomes (B3 count − the cleanup rows on the fuse date).
rc 0 BASELINE PASS / rc 1 FAIL. Usage: baseline_gate48b.py <scratchpad> [--head <sha>]"""
import json, os, re, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate48b.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]; CL = os.path.join(SP, 'g48b_sp', 'clone')
N = K['order'][0]; BASE = P['develop']; HEAD = A[A.index('--head') + 1] if '--head' in A else P['prs'][N]['head']; END = P['end_tree']
BL = 'Blockchain/Dev/scripts/audit/audit-baseline.json'; CT = 'Blockchain/Dev/scripts/audit/baseline-contract.mjs'; FUSE = K['fuse_date']
CLEANUP = [('GHSA-2mjp-6q6p-2qxm', 'undici', 'KS-470'), ('GHSA-35p6-xmwp-9g52', 'undici', 'KS-470'), ('GHSA-4992-7rv2-5pvq', 'undici', 'KS-470'),
           ('GHSA-g8m3-5g58-fq7m', 'undici', 'KS-470'), ('GHSA-g9mf-h72j-4rw9', 'undici', 'KS-470'), ('GHSA-p88m-4jfj-68fv', 'undici', 'KS-470'),
           ('GHSA-v9p9-hfj2-hcw8', 'undici', 'KS-470'), ('GHSA-vrm6-8vpv-qv8q', 'undici', 'KS-470'), ('GHSA-vxpw-j846-p89q', 'undici', 'KS-470'),
           ('GHSA-v2v4-37r5-5v8g', 'ip-address', 'KS-470'), ('GHSA-mwp4-54f8-5fhr', 'ip-address', 'KS-729'),
           ('GHSA-8xcm-r25x-g524', 'undici', 'KS-559'), ('GHSA-m8rv-5g2x-5cg5', 'undici', 'KS-559'), ('GHSA-v3r7-h72x-cjcm', 'undici', 'KS-559')]
def git(*a):
    r = subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=True)
    if r.returncode: raise SystemExit('REFUSING: git %s rc %d %s' % (' '.join(a[:3]), r.returncode, r.stderr[:200]))
    return r.stdout
bad = []
def chk(tag, ok, msg):
    print('%s %s: %s' % ('PASS' if ok else 'FAIL', tag, msg))
    if not ok: bad.append(tag)
now = datetime.datetime.now(datetime.timezone.utc)
print('baseline_gate48b %s | %s at base %s, head %s, END %s' % (now.strftime('%Y-%m-%dT%H:%M:%SZ'), BL, BASE[:12], HEAD[:12], END[:12]))
bb, hb, eb = (git('rev-parse', '%s:%s' % (t, BL)).strip() for t in (BASE, HEAD, END))
ns = git('diff', '--numstat', BASE, HEAD, '--', BL).strip()
chk('B1', bb == hb == eb and not ns, 'NO BASELINE ROW: blob develop %s | head %s | END %s | numstat %r' % (bb[:12], hb[:12], eb[:12], ns or 'empty'))
acc = json.loads(git('show', '%s:%s' % (HEAD, BL)))['accepted']
mjs = git('show', '%s:%s' % (HEAD, CT)); m = re.search(r'GRANDFATHERED_NO_EXPIRY\s*=\s*new Set\(\[(.*?)\]\);', mjs, re.S)
gf = set(re.findall(r"'(GHSA-[a-z0-9-]+)'", m.group(1))) if m else set(); noexp = set(k for k, v in acc.items() if 'expires' not in v)
cb, ch = git('rev-parse', '%s:%s' % (BASE, CT)).strip(), git('rev-parse', '%s:%s' % (HEAD, CT)).strip()
chk('B2', cb == ch and bool(gf) and gf == noexp, 'contract blob develop %s == head %s: %s | GRANDFATHERED_NO_EXPIRY %d == the %d rows with NO expires: %s' % (cb[:12], ch[:12], cb == ch, len(gf), len(noexp), gf == noexp))
fz = sorted((k, v.get('package'), v.get('ticket')) for k, v in acc.items() if v.get('expires') == FUSE)
dist = {}
for v in acc.values(): dist[v.get('expires', '(none)')] = dist.get(v.get('expires', '(none)'), 0) + 1
hrs = (datetime.datetime(2026, 10, 9, tzinfo=datetime.timezone.utc) - now).total_seconds() / 3600
print('    rows %d | expires values: %s' % (len(acc), ' | '.join('%s x%d' % (k, v) for k, v in sorted(dist.items()))))
print('    FUSE rows (%s) at the head == END: %d %s' % (FUSE, len(fz), fz))
print('    %.1f h to %sT00:00:00Z, computed at %s (UTC; the contract lapses a row ON the named day)' % (hrs, FUSE, now.strftime('%Y-%m-%dT%H:%M:%SZ')))
chk('B3', len(fz) == 4, 'FUSE-COUNT at END: %d row(s) expire %s (#1355 adds none; #1354 would make it 5)' % (len(fz), FUSE))
rows = []; okc = True
for g, pk, tk in CLEANUP:
    r = acc.get(g) or {}; ok = r.get('package') == pk and r.get('ticket') == tk; okc &= ok
    rows.append((g, pk, tk, r.get('expires', '(none)'), g in gf, ok))
    print('    CLEANUP row %s %-10s %-7s | at END: package %r ticket %r expires %s | GRANDFATHERED %s | as the line prints: %s' % (g, pk, tk, r.get('package'), r.get('ticket'), r.get('expires', '(none)'), g in gf, ok))
onfuse = [x[0] for x in rows if x[3] == FUSE]
chk('B4', okc and len(rows) == 14 and sum(x[1] == 'undici' for x in rows) == 12, 'the 14 CLEANUP rows exist as the seat\'s line prints them: 12 undici (%d KS-470 + %d KS-559) + 2 ip-address; GRANDFATHERED %d of 14; on the fuse date %s -> fuse count after the cleanup %d' % (
    sum(x[1] == 'undici' and x[2] == 'KS-470' for x in rows), sum(x[2] == 'KS-559' for x in rows), sum(x[4] for x in rows), onfuse, len(fz) - len(onfuse)))
print('BASELINE %s: %d FAIL | NO ROW (blob %s at develop/head/END) | FUSE-COUNT %d row(s) on %s at END, %.1f h left | CLEANUP 14 rows, %d on the fuse' % ('PASS' if not bad else 'FAIL', len(bad), eb[:12], len(fz), FUSE, hrs, len(onfuse)))
raise SystemExit(1 if bad else 0)
