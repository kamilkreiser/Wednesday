#!/usr/bin/env python3
"""c6_notcovered_gate59.py — gate59 C6 NOT COVERED for #1382 (KS-1005): what the PR says it did NOT cover, SECTION-BOUNDED (an item counts
only inside the body's `## NOT COVERED` section, never anywhere in the body), plus the gate's own NOT-COVERED seed list (kit
gate_not_covered_seed) with, per item, whether the PR or the doc blocks name it.
  N1 SECTION   the body has exactly one `## NOT COVERED` heading; the section runs to the next `## ` heading.
  N2 REQUIRED  inside that section, every kit not_covered_required item: session revocation on password change, the §5f live sweep owed,
               the ks949 timeout reds, the full auth suite unmeasured at this head.
  N3 TICKET    KS-1005's own "Not verified" items are carried: the live probe ("a single authenticated POST against a real database") is owed
               (the live sweep line counts) — and the ticket's reset-token flow "unchecked here" is printed as INFO (named by neither).
  INFO the gate's seed list, each marked NAMED-BY-PR / NOT-NAMED (the gate adds what it could not reach).
--selftest  T0 the REAL body PASSES; planted bodies FAIL: the session-revocation line removed (N2), the live-sweep line moved ABOVE the
            heading (N2), the heading removed (N1), a second NOT COVERED heading (N1).
Usage: c6_notcovered_gate59.py [--pr 1382] [--body-file f] [--selftest]      rc 0 PASS / 1 FAIL / 2 usage"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate59 import K, now, Checks, opt_factory, GH, selftest_arm

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
    got = {k: bool(sec and re.search(rx, sec)) for k, rx in REQ.items()}
    C.chk('N2 required items in the section', all(got.values()), ' | '.join('%s: %s' % kv for kv in got.items()))
    C.chk('N3 ticket live probe owed', bool(sec and re.search(r'(?i)live sweep', sec)), 'KS-1005 "Not verified: a single authenticated POST against a real database settles it" carried as the live sweep owed: %s' % bool(sec and re.search(r'(?i)live sweep', sec)))
    print('INFO N3 the ticket\'s reset-token flow ("unchecked here"): named in the PR body: %s' % bool(re.search(r'(?i)reset', body)))


print('c6_notcovered_gate59 %s | %s' % (now(), 'REPLAY %s' % opt('--body-file') if opt('--body-file') else 'API pulls/%s' % PR))
if '--selftest' in A:
    st = {'ok': 0, 'n': 0}; sec, _ = section(BODY)
    rev = next(l for l in sec.split('\n') if re.search(REQ['session_revocation'], l))
    live = next(l for l in sec.split('\n') if re.search(REQ['live_sweep_5f'], l))
    hd = re.search(HEAD_RX, BODY).group(0)
    selftest_arm(st, 'T0 the REAL body (positive control)', lambda C: judge(C, BODY), None)
    selftest_arm(st, 'T1 session-revocation line removed', lambda C: judge(C, BODY.replace(rev + '\n', '', 1)), 'N2')
    selftest_arm(st, 'T2 the live-sweep line moved ABOVE the heading', lambda C: judge(C, BODY.replace(live + '\n', '', 1).replace(hd, live + '\n\n' + hd, 1)), 'N2')
    selftest_arm(st, 'T3 the heading removed', lambda C: judge(C, BODY.replace(hd, '## Leftovers', 1)), 'N1')
    selftest_arm(st, 'T4 a second NOT COVERED heading', lambda C: judge(C, BODY + '\n## NOT COVERED again\n- x\n'), 'N1')
    print('SELFTEST %s %d of %d' % ('OK' if st['ok'] == st['n'] else 'BROKEN', st['ok'], st['n'])); raise SystemExit(0 if st['ok'] == st['n'] else 1)
C = Checks(); judge(C, BODY)
docs_txt = ''
print('INFO the GATE\'s own NOT COVERED seed (kit gate_not_covered_seed), each against the PR body by a KEYWORD HEURISTIC (NAMED-BY-PR? is a hint to read, never a measurement):')
for item in K['gate_not_covered_seed']:
    key = re.split(r'[:(—]', item)[0].strip()[:40]
    hit = any(w in BODY.lower() for w in [x for x in re.findall(r'[a-z0-9§/-]{5,}', key.lower())[:3]])
    print('INFO   %s | %s' % ('NAMED-BY-PR?' if hit else 'NOT-NAMED  ', item))
n = C.nfail()
print('C6 NOT COVERED %s: %d FAIL of %d checks | #%s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), PR))
raise SystemExit(1 if n else 0)
