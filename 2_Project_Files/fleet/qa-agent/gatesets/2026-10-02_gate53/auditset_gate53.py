#!/usr/bin/env python3
"""auditset_gate53.py — the drafter's PREDICTION for requirement 5 (leg 6), by mirroring audit-gate.mjs's own classification (read at the head:
`reported` = distinct GHSA ids from every `vulnerabilities[*].via[*].url`; `fresh` = reported and not in the baseline's `accepted`; `lapsed` =
reported, baselined and `expires <= today` UTC; `stale` (CLEANUP) = baselined, not reported, `scope !== 'standalone-locks'`).
The advisory report is `npm audit --json --package-lock-only --ignore-scripts` run in a SCRATCH directory holding ONLY the root manifest, the root lock
and the workspace members' package.json files extracted from the clone at that sha (a registry READ, no install, no script). The gate's leg 6 runs
`npm audit --json` over an INSTALLED root, with its own npm: this is a prediction, and the advisory database moves, so the gate re-runs it.
Three readings, each printed as leg 6 would print it (the summary line, the CLEANUP line + ids, OK / FAIL):
  BASE  = develop's tree + develop's baseline          (expect rc 0, reported/baselined/stale = kit leg6_reported_base / 25 / leg6_stale_base)
  HEAD  = the head's tree + the head's baseline         (expect rc 0, kit leg6_reported_head / 24 / leg6_stale_head; the removed row neither
                                                          reported nor baselined; the CLEANUP list now names kit cleanup_named_row)
  RED   = develop's tree + the HEAD's baseline          (= the row removed, NO override: expect rc 1, fresh == {removed_row} exactly)
  WHY   = reported(BASE) - reported(HEAD), each with its package, vulnerable range and the lock node(s) npm attributes it to, + reported(HEAD) - reported(BASE).
Overrides (controls): --audit-base F --audit-head F (saved npm audit JSON instead of a live read; the live reads are saved as
<scratchpad>/g53_sp/npm_audit_{base,head}_<HHMMSS>.json), --today YYYY-MM-DD (the lapse clock), --base <sha> --head <sha>.
rc 0 PASS / rc 1 FAIL. Usage: auditset_gate53.py <scratchpad> [overrides]"""
import json, os, subprocess, sys, datetime, tarfile, io
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate53.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
CL = os.path.join(SP, 'g53_sp', 'clone'); N = K['order'][0]; E = K['expect_counts']; RID = K['removed_row']; T = datetime.datetime.now(datetime.timezone.utc)
def git(*a, raw=False):
    r = subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=not raw)
    if r.returncode: raise SystemExit('REFUSING: git %s rc %d' % (' '.join(a)[:80], r.returncode))
    return r.stdout
B = git('rev-parse', opt('--base', P['develop']) + '^{commit}').strip(); H = git('rev-parse', opt('--head', P['pr_pins'][N]['head']) + '^{commit}').strip()
TODAY = opt('--today', T.strftime('%Y-%m-%d'))
print('auditset_gate53 %s | base %s | head %s | today (UTC, the lapse clock) %s%s' % (T.strftime('%Y-%m-%dT%H:%M:%SZ'), B[:12], H[:12], TODAY, ' (OVERRIDDEN)' if opt('--today') else ''))
def audit(sha, lab):
    f = opt('--audit-' + lab)
    if f: print('INFO %s advisory report: SAVED %s' % (lab.upper(), f)); return json.load(open(f, encoding='utf-8'))
    d = os.path.join(SP, 'g53_sp', 'audit_%s_%s_%s' % (lab, sha[:12], T.strftime('%H%M%S'))); os.makedirs(d)
    tb = git('archive', sha, '--', ':(glob)Blockchain/Dev/package-lock.json', ':(glob)Blockchain/Dev/package.json', ':(glob)Blockchain/Dev/packages/*/package.json',
             ':(glob)Blockchain/Dev/services/*/package.json', ':(glob)Blockchain/Dev/frontend/*/package.json', raw=True)
    tarfile.open(fileobj=io.BytesIO(tb)).extractall(d, filter='data')
    out = os.path.join(SP, 'g53_sp', 'npm_audit_%s_%s.json' % (lab, T.strftime('%H%M%S')))
    with open(out, 'w') as fo, open(out + '.err', 'w') as fe:
        r = subprocess.run(['npm', 'audit', '--json', '--package-lock-only', '--ignore-scripts'], cwd=os.path.join(d, 'Blockchain', 'Dev'), stdout=fo, stderr=fe)
    nv = subprocess.run(['npm', '-v'], capture_output=True, text=True).stdout.strip()
    print('INFO %s advisory report: LIVE `npm audit --json --package-lock-only` (npm %s) at %s rc %d (non-zero means advisories exist) -> %s' % (lab.upper(), nv, sha[:12], r.returncode, out))
    return json.load(open(out, encoding='utf-8'))
def rep(j):
    m = {}
    for name, v in (j.get('vulnerabilities') or {}).items():
        for via in v.get('via') or []:
            if isinstance(via, dict) and via.get('url'):
                i = str(via['url']).split('/')[-1]
                if i not in m: m[i] = {'package': via.get('name'), 'severity': via.get('severity'), 'range': via.get('range'), 'nodes': v.get('nodes')}
    return m
def baseline(sha): return json.loads(git('show', '%s:%s' % (sha, K['baseline']))).get('accepted', {})
def lapsed(e): x = e.get('expires'); return bool(x) and x <= TODAY
def leg6(lab, r, bl):
    fresh = sorted(i for i in r if i not in bl); lap = sorted(i for i in r if i in bl and lapsed(bl[i]))
    stale = [i for i in bl if i not in r and bl[i].get('scope') != 'standalone-locks']
    print('%s audit-gate: %d distinct advisories reported, %d baselined.' % (lab, len(r), len(bl)))
    if stale: print('%s CLEANUP (advisory): %d baseline entr%s no longer reported — remove: %s' % (lab, len(stale), 'y is' if len(stale) == 1 else 'ies are', ' '.join(stale)))
    print('%s %s' % (lab, 'OK — no advisories outside the triaged baseline. (rc 0)' if not fresh and not lap else 'FAIL — new %s | lapsed %s (rc 1)' % (fresh, lap)))
    return fresh, lap, stale
res = []
def chk(tag, ok, msg): res.append(ok); print('%s %s: %s' % ('PASS' if ok else 'FAIL', tag, msg))
JB, JH = audit(B, 'base'), audit(H, 'head'); RB, RH = rep(JB), rep(JH); BB, BH = baseline(B), baseline(H)
fb, lb, sb = leg6('BASE', RB, BB); fh, lh, sh = leg6('HEAD', RH, BH); fr, lr, sr = leg6('RED ', RB, BH)
chk('A1 BASE', not fb and not lb and len(RB) == E['leg6_reported_base'] and len(BB) == E['baseline_rows_base'] and len(sb) == E['leg6_stale_base'] and RID in RB and RID in BB,
    'rc 0 %s | reported %d (want %d), baselined %d (want %d), CLEANUP %d (want %d) | %s reported AND baselined: %s' % (
        not fb and not lb, len(RB), E['leg6_reported_base'], len(BB), E['baseline_rows_base'], len(sb), E['leg6_stale_base'], RID, RID in RB and RID in BB))
chk('A2 HEAD', not fh and not lh and len(RH) == E['leg6_reported_head'] and len(BH) == E['baseline_rows_head'] and len(sh) == E['leg6_stale_head'] and RID not in RH and RID not in BH and K['cleanup_named_row'] in sh,
    'rc 0 %s | reported %d (want %d), baselined %d (want %d), CLEANUP %d (want %d) | %s in neither set: %s | CLEANUP names %s: %s' % (
        not fh and not lh, len(RH), E['leg6_reported_head'], len(BH), E['baseline_rows_head'], len(sh), E['leg6_stale_head'], RID, RID not in RH and RID not in BH,
        K['cleanup_named_row'], K['cleanup_named_row'] in sh))
chk('A3 RED-FIRST', fr == [RID] and not lr, 'develop\'s tree + the head\'s baseline (row out, NO override) -> rc 1 with fresh == %s (want [%s]) and lapsed %s' % (fr, RID, lr))
gone = sorted(set(RB) - set(RH)); new = sorted(set(RH) - set(RB))
for i in gone: print('WHY  no longer reported at head: %s %s %s range %s via node(s) %s | baselined at base: %s | in GRANDFATHERED-style no-expiry: %s' % (
    i, RB[i]['package'], RB[i]['severity'], RB[i]['range'], RB[i]['nodes'], i in BB, i in BB and not BB[i].get('expires')))
for i in new: print('WHY  NEWLY reported at head: %s %s %s range %s via %s' % (i, RH[i]['package'], RH[i]['severity'], RH[i]['range'], RH[i]['nodes']))
nested = K['nested_key']
chk('A4 WHY 11 -> 9', not new and RID in gone and all(RB[i]['nodes'] == [nested] for i in gone),
    'gone %s, new %s | every gone advisory was carried ONLY by %s (the pruned copy): %s | so the "two" are %s itself and %s; no third advisory moved' % (
        gone, new or 'NONE', nested, all(RB[i]['nodes'] == [nested] for i in gone), RID, [i for i in gone if i != RID]))
for name in (K['override_child'], K['override_parent'], 'prisma'):
    vb, vh = (JB.get('vulnerabilities') or {}).get(name), (JH.get('vulnerabilities') or {}).get(name)
    f = lambda v: 'absent' if not v else '%s via %s fixAvailable %s' % (v.get('severity'), [x if isinstance(x, str) else str(x.get('url', '')).split('/')[-1] for x in v.get('via', [])], json.dumps(v.get('fixAvailable')))
    print('INFO package %s | base: %s | head: %s' % (name, f(vb), f(vh)))
nf = res.count(False)
print('AUDITSET %s: %d FAIL of %d checks | base %s head %s | reported %d -> %d, baselined %d -> %d, CLEANUP %d -> %d, red-first fresh %s' % (
    'PASS' if nf == 0 else 'FAIL', nf, len(res), B[:12], H[:12], len(RB), len(RH), len(BB), len(BH), len(sb), len(sh), fr))
raise SystemExit(1 if nf else 0)
