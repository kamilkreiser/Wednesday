#!/usr/bin/env python3
"""c6_notcovered_gate61.py — gate61 C6 NOT COVERED for #1383 (KS-1401): what the PR says it did NOT cover, SECTION-BOUNDED (an item counts
only inside the body's one not-covered section — heading kit not_covered_heading_rx, the PR's own is `## Not covered / owed` — never
anywhere in the body), plus the brief's ITEM 4 list and the gate's own seed list.
  N1 SECTION    exactly one not-covered heading; the section runs to the next `## ` heading and is non-empty.
  N2 REQUIRED   inside it, every kit not_covered_required item: the §5f live sweep, the live apply / apply round owed, per-tenant databases,
                expiry-checker.ts:139, kintsugi's NULL count + connecting role UNMEASURED, the suite's cost on every push.
  N3 BRIEF ITEM 4 (INFO, the gate rules each): every kit not_covered_brief_item4 item, printed IN-SECTION / ELSEWHERE-IN-BODY / ABSENT
                (the brief's ITEM 4 listed it under NOT COVERED: applied on no real database, column nullability, originate's GUC, 038a's
                header, the gateway-runner end state).
  INFO the gate's seed list (kit gate_not_covered_seed), each against the body by a KEYWORD HEURISTIC (a hint to read, never a measurement).
--selftest  T0 the REAL body PASSES; planted bodies FAIL: the live-sweep line removed (N2), the per-tenant line moved ABOVE the heading (N2),
            the heading removed (N1), a second not-covered heading (N1).
Usage: c6_notcovered_gate61.py [--pr 1383] [--body-file f] [--selftest]      rc 0 PASS / 1 FAIL / 2 usage. Prints `CHECKED <n>`."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate61 import K, now, Checks, opt_factory, GH, selftest_arm

A = sys.argv[1:]
if '--help' in A or '-h' in A:
    print(__doc__); raise SystemExit(0)
opt = opt_factory(A); PR = opt('--pr', K['pr']); REQ = K['not_covered_required']; HEAD_RX = K['not_covered_heading_rx']
BODY = open(opt('--body-file'), encoding='utf-8').read() if opt('--body-file') else (GH().get('pulls/' + PR).get('body') or '')


def section(body):
    hs = list(re.finditer(HEAD_RX, body))
    if len(hs) != 1: return None, len(hs)
    rest = body[hs[0].end():]; m = re.search(r'(?m)^## ', rest)
    return rest[:m.start()] if m else rest, 1


def judge(C, body):
    sec, nh = section(body)
    C.chk('N1 section', sec is not None and sec.strip() != '', 'not-covered headings %d (want 1) | section %s chars' % (nh, len(sec) if sec else 0))
    got = {k: bool(sec and re.search(rx, sec)) for k, rx in REQ.items()}
    C.chk('N2 required items in the section', all(got.values()), ' | '.join('%s: %s' % kv for kv in got.items()))
    for k, rx in K['not_covered_brief_item4'].items():
        ins = bool(sec and re.search(rx, sec)); anyw = re.search(rx, body) is not None
        print('INFO N3 brief ITEM 4 — %s: %s' % (k, 'IN-SECTION' if ins else ('ELSEWHERE-IN-BODY' if anyw else 'ABSENT')))


print('c6_notcovered_gate61 %s | %s' % (now(), 'REPLAY %s' % opt('--body-file') if opt('--body-file') else 'API pulls/%s' % PR))
if '--selftest' in A:
    st = {'ok': 0, 'n': 0}; sec, _ = section(BODY)
    live = next(l for l in sec.split('\n') if re.search(REQ['live_sweep_5f'], l))
    pt = next(l for l in sec.split('\n') if re.search(REQ['per_tenant_dbs'], l))
    hd = re.search(HEAD_RX, BODY).group(0)
    selftest_arm(st, 'T0 the REAL body (positive control)', lambda C: judge(C, BODY), None)
    selftest_arm(st, 'T1 the live-sweep line removed', lambda C: judge(C, BODY.replace(live + '\n', '', 1)), 'N2')
    selftest_arm(st, 'T2 the per-tenant line moved ABOVE the heading', lambda C: judge(C, BODY.replace(pt + '\n', '', 1).replace(hd, pt + '\n\n' + hd, 1)), 'N2')
    selftest_arm(st, 'T3 the heading removed', lambda C: judge(C, BODY.replace(hd, '## Leftovers', 1)), 'N1')
    selftest_arm(st, 'T4 a second not-covered heading', lambda C: judge(C, BODY + '\n## NOT COVERED again\n- x\n'), 'N1')
    print('SELFTEST %s %d of %d' % ('OK' if st['ok'] == st['n'] else 'BROKEN', st['ok'], st['n']))
    print('CHECKED %d arm(s)' % st['n']); raise SystemExit(0 if st['ok'] == st['n'] and st['n'] > 0 else 1)
C = Checks(); judge(C, BODY)
print('INFO the GATE\'s own NOT COVERED seed (kit gate_not_covered_seed), each against the PR body by a KEYWORD HEURISTIC (NAMED-BY-PR? is a hint to read, never a measurement):')
for item in K['gate_not_covered_seed']:
    words = [w for w in re.findall(r'[a-z0-9_§/-]{6,}', item.lower())][:4]
    hit = sum(w in BODY.lower() for w in words) >= 2
    print('INFO   %s | %s' % ('NAMED-BY-PR?' if hit else 'NOT-NAMED  ', item))
n = C.nfail()
print('CHECKED %d check(s)' % len(C.res))
print('C6 NOT COVERED %s: %d FAIL of %d checks | #%s' % ('PASS' if n == 0 and C.res else 'FAIL', n, len(C.res), PR))
raise SystemExit(1 if n or not C.res else 0)
