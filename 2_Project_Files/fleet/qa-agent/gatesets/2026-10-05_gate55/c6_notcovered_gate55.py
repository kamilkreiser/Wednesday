#!/usr/bin/env python3
"""c6_notcovered_gate55.py — gate55 C6 NOT COVERED, named and measured (READ ONLY on git objects + the PR body file; prints only).
  N1 §5f AND THIS DIFF: the skill's §5f at BASE ("A runtime-behaviour change is not done ...", "live sweep"); the classifier counts RUNTIME
     source in base..head (non-test .ts under services/*/src, EXCLUDING *.openapi.ts spec-registration modules, which no runtime file
     imports — c2 plan R3). This diff reads 0. CONTROLS of the same classifier: #1374's diff (kit base_parent..base) reads >= 1 (users.ts,
     authenticate.ts), and PR 0's diff (kit pr0_range) reads 0. VERDICT LINE either way: no live call proves the handler still answers the
     declared shape (C5 is READ ONLY) — §5f's live sweep is NOT COVERED by name, and no ticket moves on this gate.
  N2 the body names §5f / no live sweep.     N3 the body says no live call to the delegation GET was made.
  N4 the body says no S+K pair and no Schemathesis / Akto.      N5 the body says no deploy.
  N6 tsc BLIND TO THE TEST: tsconfig at head excludes src/__tests__ (parsed, with its line number) AND the body says so.
Each N2-N6 prints the matching sentence (the gate reads the sentence, not the regex). --body-file is REQUIRED (the launch action saves it).
--selftest: the given body must PASS; each statement removed must FAIL its own row; the classifier controls must hold.
Usage: c6_notcovered_gate55.py --repo <clone or checkout> --body-file f [--base sha] [--head sha] [--selftest]   rc 0 PASS / 1 FAIL / 2 usage"""
import io, contextlib, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate55 import K, git, now, Checks, has_commit, show

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A or '--body-file' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO = opt('--repo'); BASE = opt('--base', K['base']); HEAD = opt('--head', K['expected_head']); BODYF = opt('--body-file')
for s in (BASE, HEAD):
    if not re.fullmatch(r'[0-9a-f]{40}', s) or not has_commit(REPO, s): print('REFUSING: %s not a commit in %s' % (s, REPO)); raise SystemExit(2)
if not os.path.isfile(BODYF): print('REFUSING: body file %s absent' % BODYF); raise SystemExit(2)
TEST_RX = re.compile(r'(^|/)(__tests__|tests?|e2e|spec)/|\.(test|spec)\.[cm]?[jt]sx?$')
SPEC_RX = re.compile(K['openapi_ts_rx'])
def runtime(paths): return [p for p in paths if p.startswith('Blockchain/Dev/services/') and '/src/' in p and re.search(r'\.[cm]?[jt]sx?$', p) and not TEST_RX.search(p) and not SPEC_RX.search(p)]
STMTS = [
    ('N2 §5f named', r'§5f[^\n]{0,80}no live sweep|no live sweep[^\n]{0,80}§5f'),
    ('N3 no live call to the delegation GET', r'no live call to the delegation GET'),
    ('N4 no S+K pair, no Schemathesis/Akto', r'No live S\+K pair[\s\S]{0,120}No Schemathesis, no Akto|No Schemathesis, no Akto[\s\S]{0,120}No live S\+K pair'),
    ('N5 no deploy', r'(?im)^\s*-\s*No deploy\b|\bno deploy\b'),
    ('N6 tsc excludes the test', r'excludes `?src/__tests__`?'),
]
def analyse(body, label):
    C = Checks()
    sk = show(REPO, BASE, K['skill']) or ''
    f5 = 'A runtime-behaviour change is not done' in sk and 'live sweep' in sk
    rt = runtime(git(REPO, 'diff', '--name-only', BASE, HEAD).splitlines())
    c1374 = runtime(git(REPO, 'diff', '--name-only', K['base_parent'], K['base']).splitlines())
    c0 = runtime(git(REPO, 'diff', '--name-only', K['pr0_range'][0], K['pr0_range'][1]).splitlines())
    C.chk('N1 §5f and this diff', f5 and len(c1374) >= 1 and c0 == [],
          '[%s] §5f clause at %s present %s | runtime source paths in base..head: %d %s | CONTROLS: #1374 diff %d %s (want >= 1), PR 0 diff %d (want 0) | VERDICT LINE: §5f live sweep NOT COVERED — no live call proves the handler still answers the declared shape; no ticket moves on this gate' % (
              label, BASE[:12], f5, len(rt), [p.split('/src/')[-1] for p in rt], len(c1374), [p.split('/src/')[-1] for p in c1374], len(c0)))
    for tag, rx in STMTS:
        m = re.search(rx, body or '', re.I)
        snip = (body[max(0, m.start() - 50):m.end() + 30].replace('\n', ' ')[:220]) if m else 'ABSENT'
        if tag.startswith('N6'):
            ts = show(REPO, HEAD, K['tsconfig']) or '{}'; ln = [i + 1 for i, l in enumerate(ts.split('\n')) if '"src/__tests__"' in l]
            try: ex = json.loads(re.sub(r'//.*', '', ts)).get('exclude') or []
            except Exception: ex = ['UNPARSEABLE']
            C.chk(tag, m is not None and 'src/__tests__' in ex, 'tsconfig exclude at head %s (line %s) | body: %r' % (ex, ln, snip))
        else:
            C.chk(tag, m is not None, 'body: %r' % snip)
    return C
print('c6_notcovered_gate55 %s | repo %s | base %s | head %s | body %s' % (now(), REPO, BASE[:12], HEAD[:12], BODYF))
BODY = open(BODYF, encoding='utf-8').read()
if '--selftest' in A:
    arms = [('T0 the given body', BODY, None)] + [('T-%s removed' % t.split()[0], re.sub(rx, '[removed by selftest]', BODY, flags=re.I), t.split()[0]) for t, rx in STMTS]
    ok = 0
    for name, body, want in arms:
        with contextlib.redirect_stdout(io.StringIO()): C = analyse(body, name)
        f = C.failed(); good = (not f) if want is None else any(x.startswith(want) for x in f)
        ok += good; print('SELFTEST %s %s: want %s | failed %s' % ('OK' if good else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, f or 'NONE'))
    print('SELFTEST %s %d of %d' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms))); raise SystemExit(0 if ok == len(arms) else 1)
C = analyse(BODY, 'HEAD')
print('NOT COVERED (each with its reason): §5f live sweep (no live call to GET /api/delegations/{id}; C5 is a source read) | no S+K pair, no Schemathesis / Akto re-run of response_schema_conformance | no deploy | tsc never type-checks the new test (tsconfig exclude) | the other KS-1015 pairs')
n = C.nfail(); print('C6 NOT-COVERED %s: %d FAIL of %d' % ('PASS' if n == 0 else 'FAIL', n, len(C.res))); raise SystemExit(1 if n else 0)
