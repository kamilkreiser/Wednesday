#!/usr/bin/env python3
"""c6_notcovered_gate60.py — gate60 C6 NOT COVERED for #1384 (KS-1210): what the PR says it did NOT cover, SECTION-BOUNDED (an item counts only
inside the body's `## NOT COVERED` section, never anywhere in the body), plus the gate's own seed list (kit gate_not_covered_seed) with, per
item, a keyword hint of whether the PR names it.
  N1 SECTION   exactly one `## NOT COVERED` heading; the section runs to the next `## ` heading (or the end).
  N2 REQUIRED  inside that section, every kit not_covered_required item: the §5f live sweep owed, the gateway edge has no role gate for
               /api/oauth/apps, existing apps carrying a now-refused scope NOT migrated, the tenant bound SOURCE-READ not live.
  N3 TENANT    the section's "tenant bound" sentence is about the TENANT boundary, not only the role lists: it names RLS, a tenant GUC, or
               cross-tenant access. The drafter's read FAILS it — the PR's sentence says "Both role lists were verified by reading users.ts",
               which is the Q-ROLES drift, not the cross-tenant bound of the six-role bypass (README doubt D1).
  INFO         the gate's seed list, each NAMED-BY-PR? / NOT-NAMED by a KEYWORD HEURISTIC (a hint to read, never a measurement).
--selftest  BASELINE-AWARE (N3 fails at the real body): T0 the REAL body; planted bodies FAIL: the live-sweep line removed (N2), the gateway
            line moved ABOVE the heading (N2), the heading removed (N1), a second NOT COVERED heading (N1); and a planted RLS sentence makes
            N3 PASS (its control).
Usage: c6_notcovered_gate60.py [--pr 1384] [--body-file f] [--selftest]      rc 0 PASS / 1 FAIL / 2 usage"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate60 import K, now, Checks, opt_factory, GH, selftest_arm

A = sys.argv[1:]
if '--help' in A or '-h' in A:
    print(__doc__); raise SystemExit(0)
opt = opt_factory(A); PR = opt('--pr', K['pr']); REQ = K['not_covered_required']
BODY = open(opt('--body-file'), encoding='utf-8').read() if opt('--body-file') else (GH().get('pulls/' + PR).get('body') or '')
HEAD_RX = r'(?mi)^##\s+NOT COVERED\b.*$'


def section(body):
    hs = list(re.finditer(HEAD_RX, body))
    if len(hs) != 1: return None, len(hs)
    rest = body[hs[0].end():]; m = re.search(r'(?m)^## ', rest)
    return rest[:m.start()] if m else rest, 1


def judge(C, body):
    sec, nh = section(body)
    C.chk('N1 section', sec is not None and sec.strip() != '', '`## NOT COVERED` headings %d (want 1) | section %s chars' % (nh, len(sec) if sec else 0))
    got = {k: bool(sec and re.search(rx, sec, re.S)) for k, rx in REQ.items()}
    C.chk('N2 required items in the section', all(got.values()), 'CHECKED %d item(s): %s' % (len(got), ' | '.join('%s: %s' % kv for kv in got.items())))
    items = re.split(r'(?m)^- ', sec or '')   # one bullet item each (the section is a markdown list)
    tl = next((l for l in items if re.search(r'(?i)tenant bound', l)), '')
    n3 = bool(re.search(r'(?i)\bRLS\b|row.level security|tenant GUC|seedTenantGuc|cross-tenant|another tenant|other tenant', tl))
    C.chk('N3 tenant bound is about the tenant', n3, 'the "tenant bound" item names RLS / the tenant GUC / cross-tenant access: %s | its text: %r' % (n3, ' '.join(tl.split())[:220]))


print('c6_notcovered_gate60 %s | %s' % (now(), 'REPLAY %s' % opt('--body-file') if opt('--body-file') else 'API pulls/%s' % PR))
if '--selftest' in A:
    st = {'ok': 0, 'n': 0}; sec, _ = section(BODY)
    Cb = Checks(True); judge(Cb, BODY); BASE = set(Cb.failed())
    print('SELFTEST BASELINE: the real body fails %s — an arm counts only a NEW failure of its named check' % (sorted(BASE) or 'NOTHING'))
    paras = sec.split('\n- ')
    live = '- ' + next(p for p in paras if re.search(REQ['live_sweep_5f'], p)).rstrip('\n')
    gw = '- ' + next(p for p in paras if re.search(REQ['gateway_no_role_gate'], p, re.S)).rstrip('\n')
    hd = re.search(HEAD_RX, BODY).group(0)
    def narm(name, fn, want):
        def wrapped(C):
            C2 = Checks(True); fn(C2)
            for tag, ok in C2.tags: C.chk(tag, ok or tag in BASE, '(baseline-aware)')
        return selftest_arm(st, name, wrapped, want)
    def strip(p): assert p in BODY, 'plant anchor absent: %r' % p[:60]; return BODY.replace(p + '\n', '', 1)
    narm('T0 the REAL body, baseline-aware (positive control)', lambda C: judge(C, BODY), None)
    narm('T1 the live-sweep item removed', lambda C: judge(C, strip(live)), 'N2')
    narm('T2 the gateway item moved ABOVE the heading', lambda C: judge(C, strip(gw).replace(hd, gw + '\n\n' + hd, 1)), 'N2')
    narm('T3 the heading removed', lambda C: judge(C, BODY.replace(hd, '## Leftovers', 1)), 'N1')
    narm('T4 a second NOT COVERED heading', lambda C: judge(C, BODY + '\n## NOT COVERED again\n- x\n'), 'N1')
    def t5(C):
        b = BODY.replace('- **The tenant bound is SOURCE-READ, not live.**', '- **The tenant bound is SOURCE-READ, not live** (an ORG_ADMIN of another tenant is held off only by RLS and the tenant GUC).', 1)
        assert b != BODY, 'plant anchor absent'
        Cx = Checks(True); judge(Cx, b)
        for t, ok in Cx.tags:
            if t.startswith('N3'): C.chk(t, ok, '(N3 only: the planted RLS sentence must make it pass)')
    selftest_arm(st, 'T5c CONTROL a planted RLS sentence makes N3 pass', t5, None)
    print('SELFTEST %s %d of %d' % ('OK' if st['ok'] == st['n'] else 'BROKEN', st['ok'], st['n'])); raise SystemExit(0 if st['ok'] == st['n'] else 1)
C = Checks(); judge(C, BODY)
print('INFO the GATE\'s own NOT COVERED seed (kit gate_not_covered_seed), each against the PR body by a KEYWORD HEURISTIC (NAMED-BY-PR? is a hint to read, never a measurement):')
for item in K['gate_not_covered_seed']:
    key = re.split(r'[:(—]', item)[0].strip()[:48]
    hit = any(w in BODY.lower() for w in [x for x in re.findall(r'[a-z0-9§/_-]{5,}', key.lower())[:3]])
    print('INFO   %s | %s' % ('NAMED-BY-PR?' if hit else 'NOT-NAMED  ', item))
n = C.nfail()
print('C6 NOT COVERED %s: %d FAIL of %d checks | #%s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), PR))
raise SystemExit(1 if n else 0)
