#!/usr/bin/env python3
"""c6_notcovered_gate54a.py — gate54a C6 NOT COVERED, stated WITH measurements (READ ONLY on git objects + the PR body file).
  N1 §5f APPLIES: the skill's §5f at BASE reads "A runtime-behaviour change is not done ... on offline quality-gate green alone"; the diff carries
     runtime source (non-test .ts under services/*/src: users.ts, authenticate.ts) -> a live sweep is owed and NOT done: NOT COVERED.
     CONTROLS of the same classifier: it reads >= 1 on this diff AND 0 on PR 0's diff (kit base_parent..pr0_commit: lockfiles + a baseline).
  N2 the PR body says §5f was NOT done and claims no Done (`§5f` + `no live sweep`).
  N3 S-SIDE: the body says Platform S's connector key carrying `users:read` is NOT measurable from K (UNMEASURED; without it S moves 401 -> 403).
  N4 NO DEPLOY: the body says no deploy; the gate deploys nothing.
  N5 tsc BLIND TO THE TEST: tsconfig at head excludes src/__tests__ (read), and the body says so.
  N6 no live S+K pair run, no Schemathesis / Akto: the body says so.
Each N2-N6 is a regex over the body, printed with the matching sentence (the gate reads the sentence, not the regex).
--body-file <f> (default gh_body_<expected_pr>.md). --selftest: the real body must PASS; each statement removed must FAIL its row.
Usage: c6_notcovered_gate54a.py --repo <clone> [--base sha] [--head sha] [--body-file f] [--selftest]   rc 0 PASS / 1 FAIL / 2 usage"""
import json, os, re, sys, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate54a import K, G, git, now, Checks, has_commit, show

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO = opt('--repo'); BASE = opt('--base', K['base']); HEAD = opt('--head', K['expected_head'])
BODYF = opt('--body-file', os.path.join(G, 'gh_body_%s.md' % K['expected_pr']))
for s in (BASE, HEAD):
    if not re.fullmatch(r'[0-9a-f]{40}', s) or not has_commit(REPO, s): print('REFUSING: %s not a commit in %s' % (s, REPO)); raise SystemExit(2)
TEST_RX = re.compile(r'(^|/)(__tests__|tests?|e2e|spec)/|\.(test|spec)\.[cm]?[jt]sx?$')
def runtime(paths): return [p for p in paths if p.startswith(K['services_root'] + '/') and '/src/' in p and re.search(r'\.[cm]?[jt]sx?$', p) and not TEST_RX.search(p)]
STMTS = [
    ('N2 §5f stated', r'§5f[^\n]*no live sweep|no live sweep[^\n]*§5f|Skill §5f: no live sweep'),
    ('N3 S-side users:read UNMEASURED', r'connector key carries `?users:read`?[^\n]*not measurable|not measurable from K'),
    ('N4 no deploy', r'(?m)^\s*-\s*No deploy\b|\bno deploy\b'),
    ('N5 tsc excludes the test', r'excludes `?src/__tests__`?'),
    ('N6 no S+K pair / no Schemathesis-Akto', r'No live S\+K pair run[\s\S]{0,400}No Schemathesis, no Akto|No Schemathesis, no Akto[\s\S]{0,400}No live S\+K pair'),
]
def analyse(body, label):
    C = Checks()
    sk = show(REPO, BASE, K['skill']) or ''
    f5 = 'A runtime-behaviour change is not done' in sk and 'live sweep' in sk
    names = git(REPO, 'diff', '--name-only', BASE, HEAD).splitlines(); rt = runtime(names)
    ctl = runtime(git(REPO, 'diff', '--name-only', K['base_parent'], K['pr0_commit']).splitlines())
    C.chk('N1 §5f applies', f5 and len(rt) >= 1 and ctl == [], '[%s] §5f clause at %s present %s | runtime source paths in base..head %d %s | CONTROL PR 0 diff: %d (want 0) | VERDICT LINE: §5f NOT COVERED — a runtime-behaviour change with no live sweep; no ticket moves to Done on this gate' % (
        label, BASE[:12], f5, len(rt), [p.split('/src/')[-1] for p in rt], len(ctl)))
    for tag, rx in STMTS:
        m = re.search(rx, body or '', re.I)
        if tag.startswith('N5'):
            ts = show(REPO, HEAD, K['tsconfig']) or '{}'
            try: ex = json.loads(re.sub(r'//.*', '', ts)).get('exclude') or []
            except Exception: ex = ['UNPARSEABLE']
            C.chk(tag, m is not None and 'src/__tests__' in ex, 'tsconfig exclude at head %s | body: %r' % (ex, (body[max(0, m.start() - 60):m.end() + 20].replace('\n', ' ') if m else 'ABSENT')))
        else:
            C.chk(tag, m is not None, 'body: %r' % ((body[max(0, m.start() - 40):m.end() + 40].replace('\n', ' ')[:200]) if m else 'ABSENT'))
    return C
print('c6_notcovered_gate54a %s | repo %s | base %s | head %s | body %s' % (now(), REPO, BASE[:12], HEAD[:12], os.path.basename(BODYF)))
BODY = open(BODYF, encoding='utf-8').read() if os.path.isfile(BODYF) else ''
if '--selftest' in A:
    arms = [('T0 real body', BODY, None)]
    for tag, rx in STMTS:
        arms.append(('T-%s removed' % tag.split()[0], re.sub(rx, '[removed by selftest]', BODY, flags=re.I), tag.split()[0]))
    ok = 0
    for name, body, want in arms:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): C = analyse(body, name)
        f = C.failed(); good = (not f) if want is None else any(x.startswith(want) for x in f)
        ok += good; print('SELFTEST %s %s: want %s | failed %s' % ('OK' if good else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, f or 'NONE'))
    print('SELFTEST %s %d of %d' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms))); raise SystemExit(0 if ok == len(arms) else 1)
C = analyse(BODY, 'HEAD')
print('NOT COVERED (for the verdict, each with its reason): §5f live sweep (runtime change, none run) | S-side connector key users:read (unmeasurable from K) | no deploy | no live S+K pair, no Schemathesis / Akto | tsc never type-checks the new test (tsconfig exclude)')
n = C.nfail(); print('C6 NOT-COVERED %s: %d FAIL of %d' % ('PASS' if n == 0 else 'FAIL', n, len(C.res))); raise SystemExit(1 if n else 0)
