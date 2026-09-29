#!/usr/bin/env python3
"""baseline_gate48a.py — the drafter's READ of #1354's audit-baseline change (a PREDICTION for BASELINE-ROW-FIELDS and FUSE-COUNT; the gate
re-derives both). From the SCRATCH clone, `git show` of Blockchain/Dev/scripts/audit/audit-baseline.json at the BASE (pins develop) and at the
HEAD (pins head, or --head <sha> for a control plant); scripts/audit/baseline-contract.mjs at base / head / END:
  B1 both parse; top-level keys equal and `$comment` byte-equal.
  B2 `accepted`: ADDED == exactly {GHSA-r53p-7pc4-xj5r}; REMOVED none; every other row JSON-equal base vs head (CHANGED none).
  B3 the raw text diff is a PURE INSERT: `git diff --numstat` == 7 0, every changed line a `+` line, the rest byte-equal (a -U0 diff has no `-`).
  B4 the new row's fields: EXACTLY {package, reason, ticket, decidedAt, expires}; package `undici`; ticket `KS-470`; decidedAt `2026-09-30`;
     expires EXACTLY `2026-10-09` (an ISO date, the fuse date); reason non-empty.
  B5 baseline-contract.mjs blob at head == at base (ROUTE B reverted the ROUTE A edit), and GRANDFATHERED_NO_EXPIRY (parsed from the .mjs:
     the GHSA ids between `new Set([` and `]);`) == the set of rows with NO `expires` at the head (the contract's own equality assertion).
  B6 FUSE-COUNT: the rows whose `expires` == 2026-10-09 at base and at head (count, ids, package, ticket, whether its reason names Kam);
     every distinct `expires` value with its count at the head. The seat: 4 -> 5.
  B7 INFO: which files at END read the baseline (`git grep -l audit-baseline.json` over Blockchain/Dev, with a control spelling that fires).
Writes row_reason_gate48a.md beside this script (only on the REAL head): the new row's `reason` split into numbered sentences, VERBATIM, for
REASON-TEXT-TRUE (the gate checks each sentence against the tree / the image; the drafter checks none of them).
rc 0 BASELINE PASS / rc 1 FAIL. Usage: baseline_gate48a.py <scratchpad> [--head <sha>]"""
import json, os, re, subprocess, sys, hashlib, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate48a.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]; CL = os.path.join(SP, 'g48a_sp', 'clone')
N = K['order'][0]; BASE = P['develop']; REAL = P['prs'][N]['head']; HEAD = A[A.index('--head') + 1] if '--head' in A else REAL
BL = 'Blockchain/Dev/scripts/audit/audit-baseline.json'; CT = 'Blockchain/Dev/scripts/audit/baseline-contract.mjs'
NEW = 'GHSA-r53p-7pc4-xj5r'; FUSE = K['fuse_date']
def git(*a, ok=(0,)):
    r = subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=True)
    if r.returncode not in ok: raise SystemExit('REFUSING: git %s rc %d %s' % (' '.join(a), r.returncode, r.stderr[:200]))
    return r.stdout
bad = []
def chk(tag, ok, msg):
    print('%s %s: %s' % ('PASS' if ok else 'FAIL', tag, msg))
    if not ok: bad.append(tag)
print('baseline_gate48a | %s at base %s and head %s' % (BL, BASE[:12], HEAD[:12]))
tb, th = git('show', '%s:%s' % (BASE, BL)), git('show', '%s:%s' % (HEAD, BL))
b, h = json.loads(tb), json.loads(th)
chk('B1', sorted(b) == sorted(h) and b.get('$comment') == h.get('$comment'), 'top-level keys %s == %s; $comment byte-equal: %s' % (sorted(b), sorted(h), b.get('$comment') == h.get('$comment')))
ba, ha = b['accepted'], h['accepted']
added = sorted(set(ha) - set(ba)); removed = sorted(set(ba) - set(ha)); changed = sorted(k for k in set(ba) & set(ha) if ba[k] != ha[k])
print('    rows %d -> %d | ADDED %s | REMOVED %s | CHANGED %s' % (len(ba), len(ha), added, removed or 'none', changed or 'none'))
chk('B2', added == [NEW] and not removed and not changed, 'exactly one row added (%s), none removed, none changed' % NEW)
ns = git('diff', '--numstat', BASE, HEAD, '--', BL).split()
u0 = git('diff', '-U0', BASE, HEAD, '--', BL)
minus = [l for l in u0.splitlines() if l.startswith('-') and not l.startswith('---')]
plus = [l for l in u0.splitlines() if l.startswith('+') and not l.startswith('+++')]
chk('B3', ns[:2] == ['7', '0'] and not minus and len(plus) == 7, 'git diff --numstat %s | -U0: %d `+` line(s), %d `-` line(s) (a pure insert)' % (' '.join(ns[:2]), len(plus), len(minus)))
r = ha.get(NEW) or {}
chk('B4', sorted(r) == sorted(['package', 'reason', 'ticket', 'decidedAt', 'expires']) and r.get('package') == 'undici' and r.get('ticket') == 'KS-470'
    and r.get('decidedAt') == '2026-09-30' and r.get('expires') == FUSE and bool((r.get('reason') or '').strip()),
    'fields %s | package %r | ticket %r | decidedAt %r | expires %r (want %r) | reason %d chars' % (sorted(r), r.get('package'), r.get('ticket'), r.get('decidedAt'), r.get('expires'), FUSE, len(r.get('reason') or '')))
cb, ch = git('rev-parse', '%s:%s' % (BASE, CT)).strip(), git('rev-parse', '%s:%s' % (HEAD, CT)).strip()
mjs = git('show', '%s:%s' % (HEAD, CT)); m = re.search(r'GRANDFATHERED_NO_EXPIRY\s*=\s*new Set\(\[(.*?)\]\);', mjs, re.S)
gf = set(re.findall(r"'(GHSA-[a-z0-9-]+)'", m.group(1))) if m else set()
noexp = set(k for k, v in ha.items() if 'expires' not in v)
chk('B5', cb == ch and bool(gf) and gf == noexp, 'contract blob base %s == head %s: %s | GRANDFATHERED_NO_EXPIRY %d ids == the %d head rows with NO expires: %s (only-in-set %s, only-in-rows %s)' % (
    cb[:12], ch[:12], cb == ch, len(gf), len(noexp), gf == noexp, sorted(gf - noexp) or 'none', sorted(noexp - gf) or 'none'))
def fuse(acc):
    return sorted((k, v.get('package'), v.get('ticket'), 'Kam' in (v.get('reason') or '')) for k, v in acc.items() if v.get('expires') == FUSE)
fb, fh = fuse(ba), fuse(ha)
dist = {}
for v in ha.values(): dist[v.get('expires', '(none)')] = dist.get(v.get('expires', '(none)'), 0) + 1
print('    base rows expiring %s: %d %s' % (FUSE, len(fb), fb))
print('    head rows expiring %s: %d %s' % (FUSE, len(fh), fh))
print('    head expires values: %s' % ' | '.join('%s x%d' % (k, v) for k, v in sorted(dist.items())))
chk('B6', len(fh) == len(fb) + 1 and NEW in [x[0] for x in fh], 'FUSE-COUNT at the head: %d row(s) expire %s (base %d; this PR adds exactly its own row)' % (len(fh), FUSE, len(fb)))
cons = git('grep', '-l', '-F', 'audit-baseline.json', P['end_tree'], '--', 'Blockchain/Dev', ':(exclude)**/node_modules/**', ok=(0, 1)).split()
ctl = git('grep', '-l', '-F', 'GRANDFATHERED_NO_EXPIRY', P['end_tree'], '--', 'Blockchain/Dev', ok=(0, 1)).split()
print('INFO B7 files at END naming audit-baseline.json: %d %s | CONTROL GRANDFATHERED_NO_EXPIRY: %d file(s)' % (len(cons), [c.split(':', 1)[1] for c in cons][:12], len(ctl)))
if HEAD == REAL and r.get('reason'):
    ss = [s.strip() for s in re.split(r'(?<=[.;])\s+(?=[A-Za-z(])', r['reason']) if s.strip()]
    out = ['# gate48a — the NEW baseline row\'s `reason`, VERBATIM, split into sentences for REASON-TEXT-TRUE', '',
           'Read %s by baseline_gate48a.py: `git show %s:%s`, row `%s`. reason sha256 %s, %d chars, %d sentence(s). The split is at `. ` / `; ` before a letter; the gate checks EVERY sentence as a row (claim · instrument + tree/image · TRUE / FALSE / UNMEASURED / TRUE-BUT-CONDITIONAL). The drafter checked NONE of them. It is a PUBLISHED record: it lands in develop and every later reader of the baseline reads it.' % (
               datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), HEAD, BL, NEW, hashlib.sha256(r['reason'].encode()).hexdigest(), len(r['reason']), len(ss)), '']
    out += ['%d. %s' % (i + 1, s) for i, s in enumerate(ss)]
    open(os.path.join(G, 'row_reason_gate48a.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print('INFO reason: %d sentence(s) -> row_reason_gate48a.md (sha256 %s)' % (len(ss), hashlib.sha256(r['reason'].encode()).hexdigest()[:16]))
print('BASELINE %s: %d FAIL | FUSE-COUNT %d row(s) expire %s at the head (base %d) | GRANDFATHERED %d == no-expiry %d' % ('PASS' if not bad else 'FAIL', len(bad), len(fh), FUSE, len(fb), len(gf), len(noexp)))
raise SystemExit(1 if bad else 0)
