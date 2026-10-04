#!/usr/bin/env python3
"""c6_notcovered_gateD2.py — gateD2 C6 NOT COVERED, stated WITH measurements (READ ONLY: git objects + the PR body file). A NEW COPY of
c6_notcovered_gate54a.py, re-keyed to the commission's nine KS 1404 items. Each row = a measurement where one exists + the sentence the PR
body states (the regex finds it; the GATE reads the sentence, not the regex).
  N1 §5f live sweep: the skill's §5f clause at BASE; runtime source in base..head (non-test .ts under services/timestamping/src) >= 1;
     CONTROL the same classifier reads 0 on PR 0's diff. VERDICT LINE: NOT COVERED, KS-1404 stays In Progress.
  N2 root-to-TSA binding unverified (no real token obtained, by rule)        N3 the D-Trust root's second source (EU Trusted List not fetched)
  N4 the box TSA_URL values (production / kintsugi / demo) unmeasured        N5 compose wiring of TSA_TRUST_ANCHORS_PEM: MEASURED count of
     docker-compose*.yml files at head that set it (0 expected — the variable is wired nowhere, so every environment fails closed)
  N6 the negative-nonce encoding preserved (der.ts quirk; C3's request-bytes differential proves it is forge's)
  N7 the mobile tree still carries node-forge: MEASURED tracked lockfiles at head with node_modules/node-forge (outside the gate's scope)
  N8 create-side verify-on-receipt (and the nonce comparison) out          N9 the opentimestamps / blockchain JSON proof paths out
--body-file <f> (the PR body the launch action saved; without one the HEAD commit messages stand in and the row says so).
--selftest: the real text must PASS each row it passes; each statement removed must FAIL its row.
Usage: c6_notcovered_gateD2.py --repo <clone> --head <sha> [--base sha] [--body-file f] [--selftest]   rc 0 PASS / 1 FAIL / 2 usage"""
import os, re, sys, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gateD2 import K, git, now, Checks, has_commit, show

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A or '--head' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO = opt('--repo'); BASE = opt('--base', K['base']); HEAD = opt('--head'); BODYF = opt('--body-file')
for s_ in (BASE, HEAD):
    if not re.fullmatch(r'[0-9a-f]{40}', s_ or '') or not has_commit(REPO, s_): print('REFUSING: %s not a commit in %s' % (s_, REPO)); raise SystemExit(2)
TEST_RX = re.compile(r'(^|/)(__tests__|tests?|e2e|spec)/|\.(test|spec)\.[cm]?[jt]sx?$')
def runtime(paths): return [p for p in paths if p.startswith(K['service'] + '/src/') and re.search(r'\.[cm]?[jt]sx?$', p) and not TEST_RX.search(p)]
STMTS = [
    ('N2 root-to-TSA binding', r'root[- ]to[- ]TSA|binding[^\n]{0,80}unverified|unverified[^\n]{0,80}binding'),
    ('N3 D-Trust second source', r'second source|EU Trusted List|Trusted List'),
    ('N4 box TSA_URL values', r'TSA_URL[^\n]{0,160}(unmeasured|not measured|production|kintsugi|demo)|(unmeasured|not measured)[^\n]{0,160}TSA_URL'),
    ('N5 compose wiring', r'compose'),
    ('N6 negative nonce', r'negative[- ]nonce|negative INTEGER|high-bit nonce|nonce[^\n]{0,60}negative'),
    ('N7 mobile node-forge', r'mobile[^\n]{0,120}node-forge|node-forge[^\n]{0,120}mobile'),
    ('N8 create-side verify', r'create-side|verify-on-receipt'),
    ('N9 opentimestamps / blockchain proofs', r'opentimestamps'),
]


def analyse(body, label):
    C = Checks(); sk = show(REPO, BASE, K['skill']) or ''
    f5 = 'A runtime-behaviour change is not done' in sk and 'live sweep' in sk
    rt = runtime(git(REPO, 'diff', '--name-only', BASE, HEAD).splitlines()); ctl = runtime(git(REPO, 'diff', '--name-only', K['pr0_parent'], K['pr0_commit']).splitlines())
    m = re.search(r'5f[^\n]{0,160}live sweep|live sweep[^\n]{0,160}5f', body or '', re.I)
    C.chk('N1 §5f', f5 and len(rt) >= 1 and ctl == [] and m is not None, '[%s] §5f clause at %s %s | runtime source paths %d %s | CONTROL PR 0 diff %d | body: %r | VERDICT LINE: NOT COVERED, KS-1404 stays In Progress' % (
        label, BASE[:12], f5, len(rt), [p.split('/src/')[-1] for p in rt], len(ctl), (body[max(0, m.start() - 30):m.end() + 30].replace('\n', ' ') if m else 'ABSENT')))
    names = git(REPO, 'ls-tree', '-r', '--name-only', HEAD).splitlines()
    comp = [n for n in names if re.search(r'docker-compose[^/]*\.ya?ml$', n) and 'TSA_TRUST_ANCHORS_PEM' in (show(REPO, HEAD, n) or '')]
    compc = [n for n in names if re.search(r'docker-compose[^/]*\.ya?ml$', n) and 'TSA_URL' in (show(REPO, HEAD, n) or '')]
    forge = [n for n in names if n.endswith('package-lock.json') and '"node_modules/node-forge"' in (show(REPO, HEAD, n) or '')]
    print('INFO N5 MEASURED compose files setting TSA_TRUST_ANCHORS_PEM: %d %s | MUST-HIT compose files naming TSA_URL: %d %s' % (len(comp), comp, len(compc), compc[:3]))
    print('INFO N7 MEASURED tracked lockfiles still carrying node_modules/node-forge at head: %d %s' % (len(forge), forge))
    for tag, rx in STMTS:
        mm = re.search(rx, body or '', re.I)
        C.chk(tag, mm is not None, 'body: %r' % ((body[max(0, mm.start() - 50):mm.end() + 50].replace('\n', ' ')[:220]) if mm else 'ABSENT'))
    return C


src = 'PR body %s' % BODYF if BODYF and os.path.isfile(BODYF) else 'HEAD commit messages (NO PR body given)'
BODY = open(BODYF, encoding='utf-8').read() if BODYF and os.path.isfile(BODYF) else '\n'.join(git(REPO, 'log', '-1', '--format=%B', c) for c in git(REPO, 'log', '--format=%H', '%s..%s' % (BASE, HEAD)).split())
print('c6_notcovered_gateD2 %s | repo %s | base %s | head %s | text: %s (%d chars)' % (now(), REPO, BASE[:12], HEAD[:12], src, len(BODY)))
if '--selftest' in A:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): ref = analyse(BODY, 'REF').failed()
    print('SELFTEST REF: rows failing on the real text %s (the prediction; each removal below must ADD its row)' % (ref or 'NONE'))
    ok = 0; n = 0
    full = BODY + '\n' + '\n'.join(['NOT COVERED (selftest synthetic): root-to-TSA binding unverified; D-Trust second source (EU Trusted List) unverified;',
        'box TSA_URL values unmeasured (production, kintsugi, demo); compose wiring out; the negative-nonce encoding preserved;',
        'the mobile tree still carries node-forge; create-side verify-on-receipt out; opentimestamps and blockchain proofs out; skill 5f: no live sweep.'])
    for tag, rx in [('N1', r'5f[^\n]{0,160}live sweep|live sweep[^\n]{0,160}5f')] + [(t.split()[0], r) for t, r in STMTS]:
        cut = re.sub(rx, '[removed]', full, flags=re.I)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): f = analyse(cut, tag).failed()
        with contextlib.redirect_stdout(io.StringIO()): f0 = analyse(full, 'FULL').failed()
        good = any(x.startswith(tag + ' ') for x in f) and not any(x.startswith(tag + ' ') for x in f0); ok += good; n += 1
        print('SELFTEST %s %s removed from a COMPLETE text: want a FAIL on %s | failed %s' % ('OK' if good else 'MISS', tag, tag, f or 'NONE'))
    print('SELFTEST %s %d of %d' % ('OK' if ok == n else 'BROKEN', ok, n)); raise SystemExit(0 if ok == n else 1)
C = analyse(BODY, 'HEAD')
print('NOT COVERED (for the verdict, each with its reason): §5f live sweep | root-to-TSA binding | D-Trust second source | box TSA_URL values | compose wiring | negative-nonce encoding | mobile node-forge | create-side verify | opentimestamps / blockchain proofs')
n = C.nfail(); print('C6 NOT-COVERED %s: %d FAIL of %d (a FAIL = the PR text does not STATE that item; the gate rules whether the omission blocks)' % ('PASS' if n == 0 else 'FAIL', n, len(C.res))); raise SystemExit(1 if n else 0)
