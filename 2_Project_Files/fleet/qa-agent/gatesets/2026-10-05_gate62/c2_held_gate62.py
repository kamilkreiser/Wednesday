#!/usr/bin/env python3
"""c2_held_gate62.py — C2 APPLIED == HELD for #1387: apply the two HELD Spark carves (envexample, then alerting) to develop with a TEMP
index in YOUR OWN scratch clone (write verbs refused inside /Volumes/DevMASTER/!CODING), and compare each of the three non-doc files
with the head's blob, by LINES.

  H1  each held patch's sha256 prefix == the brief's P9 (envexample e50bdc17f06010fe, alerting e89345ec73eeef75)
  H2  `git apply --cached --check` then `--cached` of BOTH, in order, rc 0 (STRICT, no fuzz)
  H3  the TEST file: independent apply == head blob (byte-equal)
  H4  each ENV EXAMPLE: independent apply vs head = EXACTLY one added line, the `# KS-1388:` why+ticket comment directly above the
      URI line, and nothing else (the body's claim); CONTROL: each applied file differs from its develop blob (the apply landed)
  INFO the docs' sentence "all three resulting files are cmp-equal" (flow 14.3 / cheat `applied == held` row) is printed beside H4:
       if H4 measures one added line per env file, the docs' "all three cmp-equal" is FALSE as written (README doubt D3).

Usage: c2_held_gate62.py --repo <OWN scratch clone> [--out <dir>] [--envexample <patch>] [--alerting <patch>]  |  --selftest --repo <clone>
rc 0 all PASS / rc 1 any FAIL or 0 checked / rc 2 refused."""
import difflib, hashlib, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate62 import K, git, wgit, Tally, outside_forbidden, HERE, SCRATCH

RUNS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs'
HELD = {'envexample': (RUNS + '/spark_secuura_2026-10-05_KS-1388-envexample/out.md.checker/patch.diff', 'e50bdc17f06010fe'),
        'alerting': (RUNS + '/spark_secuura_2026-10-05_KS-1388-alerting/out.md.checker/patch.diff', 'e89345ec73eeef75')}


def apply_held(repo, out, patches):
    if not outside_forbidden(repo):
        print('REFUSED: %s is inside %s — use your OWN scratch clone' % (repo, K['forbidden_root'])); raise SystemExit(2)
    os.makedirs(out, exist_ok=True)
    idx = os.path.join(out, 'held.index.%d' % os.getpid()); env = {'GIT_INDEX_FILE': idx}
    assert wgit(repo, 'read-tree', K['develop'], env=env)[0] == 0
    rcs = []
    for p in patches:
        rc1, _, e1 = _apply(repo, p, env, True)
        rc2, _, e2 = _apply(repo, p, env, False)
        rcs.append((os.path.basename(os.path.dirname(os.path.dirname(p))), rc1, rc2, (e1 + e2).strip()[:200]))
    rc, tree, e = wgit(repo, 'write-tree', env=env); assert rc == 0, e
    shutil.move(idx, os.path.join(out, '_quarantine_held_index_%s' % tree.strip()[:8]))
    return rcs, tree.strip()


def _apply(repo, patch, env, check):
    import subprocess
    if not outside_forbidden(repo): raise SystemExit(2)
    e = dict(os.environ); e.update(env)
    args = ['git', '-C', repo, 'apply', '--cached'] + (['--check'] if check else []) + [patch]
    p = subprocess.run(args, capture_output=True, env=e)
    return p.returncode, p.stdout.decode(), p.stderr.decode()


def judge(repo, patches, shas, t, out):
    got = {k: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16] for k, p in patches.items()}
    t.check('H1', all(got[k] == shas[k] for k in shas), 'held patch sha256 prefixes %s (want %s)' % (got, shas))
    rcs, tree = apply_held(repo, out, [patches['envexample'], patches['alerting']])
    t.check('H2', all(r[1] == 0 and r[2] == 0 for r in rcs), 'apply --check / apply rc per carve %s; independent tree %s' % ([r[:3] for r in rcs], tree[:12]))
    b = lambda rev, p: git(repo, 'show', '%s:%s' % (rev, p))
    t.check('H3', b(tree, K['test']) == b(K['head'], K['test']), 'test file: independent apply %s head blob' % (
        '==' if b(tree, K['test']) == b(K['head'], K['test']) else '!='))
    for p in K['env_examples']:
        ap, hd, dv = b(tree, p).split('\n'), b(K['head'], p).split('\n'), b(K['develop'], p).split('\n')
        ops = [o for o in difflib.SequenceMatcher(None, ap, hd, autojunk=False).get_opcodes() if o[0] != 'equal']
        added = [hd[o[3]:o[4]] for o in ops]
        one = (len(ops) == 1 and ops[0][0] == 'insert' and len(added[0]) == 1 and added[0][0].startswith('# KS-1388:')
               and 'SECUURA_NGINX_STATUS_URI=' not in added[0][0] and hd[ops[0][3] + 1].startswith('# SECUURA_NGINX_STATUS_URI=http://secuura-nginx-gateway:80/'))
        landed = ap != dv
        t.check('H4 ' + p, one and landed, 'apply vs head: %d op(s) %s; added %s; CONTROL apply differs from develop blob: %s' % (
            len(ops), [o[0] for o in ops], added, landed))
    t.info('DOCS', 'flow 14.3 / cheat say "all three resulting files are cmp-equal"; the PR body says each env example differs by exactly one added comment line')


def selftest(repo):
    import io, contextlib
    fx = os.path.join(SCRATCH, 'fixtures'); os.makedirs(fx, exist_ok=True)
    out = os.path.join(SCRATCH, 'sim'); ok = total = 0
    def run(patches, shas):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): judge(repo, patches, shas, t, out)
        return t
    real = {k: v[0] for k, v in HELD.items()}; shas = {k: v[1] for k, v in HELD.items()}
    t0 = run(real, shas); total += 1; ok += not t0.fails
    print('SELFTEST %s T0 the REAL held patches: %d checked, fails %s' % ('OK' if not t0.fails else 'MISS', t0.n, t0.fails))
    src = open(real['envexample']).read()
    a = '+# SECUURA_NGINX_STATUS_URI=http://secuura-nginx-gateway:80/stub_status'
    assert src.count(a) == 1, 'anchor count %d' % src.count(a)
    bad = src.replace(a, '+# SECUURA_NGINX_STATUS_URI=http://secuura-nginx-gateway:8080/stub_status')
    p = os.path.join(fx, 'held_envexample_port8080.diff'); open(p, 'w').write(bad)
    t = run({'envexample': p, 'alerting': real['alerting']}, {'envexample': hashlib.sha256(bad.encode()).hexdigest()[:16], 'alerting': shas['alerting']})
    total += 1; g = 'H4 observability/.env.example' in t.fails; ok += g
    print('SELFTEST %s a held carve with a DIFFERENT port (fixture %s): want FAIL H4 .env.example | got %s' % ('OK' if g else 'MISS', os.path.basename(p), t.fails))
    t = run(real, {'envexample': '0' * 16, 'alerting': shas['alerting']}); total += 1; g = 'H1' in t.fails; ok += g
    print('SELFTEST %s a held-patch hash mismatch: want FAIL H1 | got %s' % ('OK' if g else 'MISS', t.fails))
    rc = None
    try:
        with contextlib.redirect_stdout(io.StringIO()): apply_held(K['checkout'], out, [real['envexample']])
    except SystemExit as e: rc = e.code
    total += 1; g = rc == 2; ok += g
    print('SELFTEST %s refusal: apply into the SHARED checkout refused before any write (rc %s)' % ('OK' if g else 'MISS', rc))
    print('SELFTEST %s %d of %d' % ('OK' if ok == total else 'BROKEN', ok, total)); print('CHECKED %d arm(s)' % total)
    return 0 if ok == total else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if not A or '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    repo = opt('--repo')
    if not repo: raise SystemExit('need --repo <OWN scratch clone>')
    if '--selftest' in A: raise SystemExit(selftest(repo))
    patches = {'envexample': opt('--envexample', HELD['envexample'][0]), 'alerting': opt('--alerting', HELD['alerting'][0])}
    t = Tally(); judge(repo, patches, {k: v[1] for k, v in HELD.items()}, t, opt('--out', os.path.join(SCRATCH, 'sim'))); raise SystemExit(t.end())
