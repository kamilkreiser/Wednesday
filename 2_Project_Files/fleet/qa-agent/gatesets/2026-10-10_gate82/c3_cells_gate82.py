#!/usr/bin/env python3
"""c3_cells_gate82.py — the RUN instruments for gate82: #1448's vitest cells / whole security suite / tsc / spec regeneration / rotate probe / tamper rows (in YOUR
worktree), #1447's and #1449's shell suites (arms, siblings, the runner's failed-run output, tamper rows) in trees extracted OUTSIDE every git repo, #1449's
core.hooksPath HAZARD arms (scratch repos), and the COMPOSITION of all three (code paths disjoint in a temp index, the two platform-k HTML docs keep-both in
several orders with html_docs_matrix on each composed tree and a count-based drop-a-block control). Every write path is checked lexically AND by realpath and
refused under !CODING. Carried in shape from c3_cells_gate81.py; [g82] rebuilt. EACH PR has its OWN base (#1447/#1448 76b683c7dcd0, #1449 f247ff85b612).

  setup    --clone CL --head H --wt WT [--log DIR]      `git worktree add --detach` in YOUR clone; in WT/Blockchain/Dev `npm ci --ignore-scripts` and
           `npm run build --workspace=packages/shared` (dist/index.js ASSERTED). Refuses a WT that exists. (X1)
  sec      --state head|base|srchead_yamlbase|srcbase_yamlhead [--whole] --wt WT --clone CL --base1448 B --head1448 H --out DIR
           materialises a STATE of #1448 in WT (spec source / committed yaml / the new test), each plant ASSERTED LANDED (sha), runs vitest ONCE (the new test, or --whole
           the security package), reads the per-cell JSON, RESTORES every touched path by sha (an originally-absent path is MOVED to the quarantine, never deleted).
  tsc      --wt WT --clone CL --base1448 B --head1448 H --out DIR     package tsc rc, the program's test files, and a scratch config that NAMES the new test (non-empty
           proof by --listFilesOnly + a planted TS2322 control)
  specregen --wt WT ...    `tsx scripts/generate-openapi.ts --check` at the head (rc, "CHECK PASS") and a CONTROL: the BASE yaml planted must make it exit non-zero
  probe    --wt WT ...     appends probe_rotate_gate82.ts.txt to a COPY of the security package's own ks577 test, runs it with G82_PROBE_OUT, MOVES the copy out
  tamper   --pr 1447|1448|1449 ... --out DIR [--only T1,T2]   HEAD row (all green), CONTROL no-op row, then the tamper rows of that PR: anchor EXACTLY ONCE, LANDED,
           run the PR's suite, read which cells RED, RESTORE (sha). LOAD failure = TAMPER-INVALID. ALL-GREEN = a tamper no cell catches (a finding to rule).
           1447/1449 need --clone/--head/--base/--scratch (an extracted tree, no installs); 1448 needs --wt/--clone/--base1448/--head1448.
  shells   --pr 1447|1449 --clone CL --head H --base B --scratch S --out DIR   the new suite with the head product / the BASE product planted / the payload state;
           the siblings at base and head with their FULL outputs byte-compared; `run-shell-suites.sh --list` base vs head; html_docs_matrix; (1447) the runner's
           failed-run output bytes. All in a tree extracted with `git archive` into a directory that is NOT inside any git repo (asserted, with a control).
  hooks    --clone CL --head H --base B --scratch S --out DIR   (#1449) the core.hooksPath HAZARD: scratch repos H1..H9 (unset / `.githooks` / other value / a
           worktree / TMPDIR inside a repo), the test AS RECEIVED (the payload: head minus the cd line) and as COMMITTED, the caller's .git/config hashed around each run
           with a positive control and an empty-hash guard. Arm H9 measures the case the seat left UNMEASURED.
  compose  --clone CL --head1447.. --base1447.. --develop D --scratch S --out DIR   the three PRs in a TEMP INDEX over D in orders A / B / C (full and code-only
           trees recorded; the code-only tree must be identical in all orders and equal D + each PR's own paths), `git merge-tree --write-tree` per pair and per PR onto D.
  docs     (same args)  the two docs: each fragment extracted against its PR's OWN parent, textual merge-file step by step per order (a conflict at the shared
           line is the expected finding), KEEP-BOTH onto D, a count-wanted table per fragment, html_docs_matrix on every composed tree, and a DROP-A-BLOCK control that
           the counts must catch (html_docs_matrix does not: gate81 G81-2).
  --selftest   (refuses unless TMPDIR is a canonical directory outside every repo)
rc 0 / 1 (a FAIL: plant not landed, restore failed, HEAD row not green, CONTROL red, a LOAD failure where a count was expected, a composition that does not compose)
/ 2 refused. NOT RUN is reported by name and is never a pass."""
import difflib, hashlib, json, os, re, shutil, signal, subprocess, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate82 import K, PR, git, git_bytes, blob, req, opt, wgit, must_be_outside, extract, resolvable

HERE = os.path.dirname(os.path.abspath(__file__))
P47, P48, P49 = PR(1447), PR(1448), PR(1449)
DD = K['dev_dir']; SECD = 'Blockchain/Dev/services/security'
DOCS = list(K['known_develop_overlap'])
SRC, YAML, TEST48, RT = P48['spec_source'], P48['spec_yaml'], P48['test_file'], P48['runtime_source']
HOST = P48['probe_host_test']
EMPTY_SHA = 'e3b0c44298fc1c14'
PRED48 = {
    'base': '3 passed / 4 failed of 7 (RED KS-1434 A1 A2 A3 A4 red; control C1 C2 C3 green)  [PR body: rc 1, 3 passed / 4 failed]',
    'head': '7/7 green  [PR body: 7 passed, 0 failed]',
    'srchead_yamlbase': 'A4 red only (source declares rotate, the committed yaml does not)  [PR body: yaml reverted, source kept: A4 fails and A1-A3 pass]',
    'srcbase_yamlhead': 'A1 A2 A3 red, A4 green (yaml declares rotate, the source does not)  [PR body: source reverted, yaml kept: A1-A3 fail and A4 passes]',
}
WHOLE48 = {'base': 'security: 27 files / 284 tests (PR body: 284 passed, 27 files; the new file absent)', 'head': 'security: 28 files / 291 tests (PR body: 291 passed, 28 files)'}


def sha(b): return hashlib.sha256(b).hexdigest()
def now(): return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


# ---------------- paths / repos ----------------
def in_repo(path):
    """True when `path` lies inside ANY git work tree (git rev-parse --show-toplevel succeeds there)."""
    d = path if os.path.isdir(path) else os.path.dirname(path)
    while d and not os.path.isdir(d): d = os.path.dirname(d)
    e = dict(os.environ); e.pop('GIT_DIR', None); e.pop('GIT_WORK_TREE', None)
    return subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True, env=e).returncode == 0


def assert_not_in_repo(path, what):
    """[g82] the bootstrap-env.sh hazard: a scratch tree inside a repo that has .githooks makes the suites WRITE that repo's core.hooksPath."""
    if in_repo(path): raise SystemExit('REFUSED: %s %s is inside a git repository (bootstrap-env.sh would act on THAT repo\'s core.hooksPath) — use a scratch under /private/tmp outside every repo' % (what, path))


def canon_tmp(scratch):
    """a realpath-canonical TMPDIR under `scratch`, outside every repo and under !CODING never."""
    must_be_outside(scratch, 'scratch'); real = os.path.realpath(scratch)
    if real != os.path.abspath(scratch): raise SystemExit('REFUSED: scratch %s is not canonical (realpath %s): pass the realpath' % (scratch, real))
    assert_not_in_repo(real, 'scratch'); t = os.path.join(real, 'tmp'); os.makedirs(t, exist_ok=True); return t


def w(path, data):
    must_be_outside(path, 'write'); os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'wb').write(data if isinstance(data, bytes) else data.encode('utf-8'))


def write_checked(wt, rel, data):
    p = os.path.join(wt, rel); must_be_outside(p, 'write'); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'wb').write(data)
    if sha(open(p, 'rb').read()) != sha(data): raise SystemExit('PLANT NOT LANDED: %s' % rel)
    return p


def run(cmd, cwd=None, env=None, timeout=900, stdin=None):
    """-> (rc, out, err, timed_out). The child runs in its OWN process group; a timeout kills the group."""
    e = dict(os.environ); e.update(env or {}); e.pop('GIT_SSH_COMMAND', None)
    p = subprocess.Popen(cmd, cwd=cwd, env=e, stdin=(subprocess.PIPE if stdin is not None else subprocess.DEVNULL), stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    try:
        o, er = p.communicate(input=(stdin.encode() if stdin is not None else None), timeout=timeout); to = False
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL); o, er = p.communicate(); to = True
    return p.returncode, o.decode('utf-8', 'replace'), er.decode('utf-8', 'replace'), to


def cgit(clone, args, env=None, inp=None):
    """plumbing in the KIT CLONE only (refuses a clone under !CODING); never the shared checkout."""
    must_be_outside(clone, 'git %s' % args[0])
    e = dict(os.environ); e.update(env or {}); e.pop('GIT_SSH_COMMAND', None)
    p = subprocess.run(['git', '-C', clone] + list(args), capture_output=True, env=e, input=inp)
    return p.returncode, p.stdout, p.stderr.decode('utf-8', 'replace')


# ---------------- vitest ----------------
def cell_key(title, seen):
    k = title.split(': ', 1)[0].replace("'", '')[:70]
    n = seen.get(k, 0); seen[k] = n + 1
    return k if n == 0 else '%s #%d' % (k, n + 1)


def read_vitest(json_path):
    if not os.path.isfile(json_path): return {'load_failed': True, 'tests': 0, 'passed': 0, 'failed': 0, 'skipped': 0, 'suites': 0, 'failed_suites': 0, 'cells': {}, 'message': 'NO JSON WRITTEN', 'fail_msgs': {}, 'load_failed_suites': []}
    d = json.load(open(json_path)); tr = d.get('testResults') or []
    ar = [(r, a) for r in tr for a in r.get('assertionResults') or []]
    lf = [r.get('name', '?') for r in tr if 'Test suite failed to run' in (r.get('message') or '') or (not r.get('assertionResults') and r.get('status') == 'failed')]
    seen = {}; cells = {}; msgs = {}
    for r, a in ar:
        k = cell_key(a['title'], seen); cells[k] = a['status']
        if a['status'] == 'failed': msgs[k] = ' '.join((a.get('failureMessages') or [''])[0].split())[:260]
    return {'load_failed': bool(lf) or not ar, 'load_failed_suites': lf, 'tests': len(ar), 'passed': sum(1 for _, a in ar if a['status'] == 'passed'),
            'failed': sum(1 for _, a in ar if a['status'] == 'failed'), 'skipped': sum(1 for _, a in ar if a['status'] in ('pending', 'todo', 'skipped')),
            'suites': len(tr), 'failed_suites': sum(1 for r in tr if r.get('status') == 'failed'), 'cells': cells, 'fail_msgs': msgs,
            'message': ' | '.join((r.get('message') or '')[:200] for r in tr if r.get('message'))}


def vitest(wt, rels, json_path, env_extra=None, timeout=1500):
    pd = os.path.join(wt, SECD); vt = os.path.join(wt, DD, 'node_modules', 'vitest', 'vitest.mjs')
    cmd = ['node', vt, 'run', '--reporter=json', '--outputFile=' + json_path] + [os.path.relpath(os.path.join(wt, r), pd) for r in rels]
    e = dict(env_extra or {}); e.setdefault('SECURITY_DISABLE_BOOT', '1')
    return run(cmd, cwd=pd, env=e, timeout=timeout)


def porcelain(wt):
    return subprocess.run(['git', '-C', wt, 'status', '--porcelain', '--untracked-files=all', '--', '.', ':!Blockchain/Dev/**/node_modules', ':!Blockchain/Dev/packages/shared/dist'], capture_output=True, text=True).stdout.strip()


def apply_edits(src, edits):
    """returns the tampered text; refuses unless each anchor occurs EXACTLY ONCE in the (progressively edited) file."""
    out = src
    for a, b in edits:
        n = out.count(a)
        if n != 1: raise SystemExit('ANCHOR %r occurs %d time(s) (want 1) — the tamper is NOT applied' % (a[:70], n))
        out = out.replace(a, b)
    return out


def landed(before, after, edits):
    return sha(before.encode()) != sha(after.encode()) and all(b in after for _, b in edits if b)


# ---------------- setup ----------------
def setup(clone, head, wt, logd):
    must_be_outside(wt, 'worktree'); must_be_outside(clone, 'clone')
    if os.path.exists(wt): print('REFUSED: %s exists (a fresh worktree each time)' % wt); return 2
    logd = logd or os.path.dirname(wt.rstrip('/')); os.makedirs(logd, exist_ok=True)
    rc, o, e = wgit(clone, 'worktree', 'add', '--detach', wt, head)
    print('%s worktree add rc %d %s' % (now(), rc, e.strip()[-120:]))
    if rc: return 1
    dev = os.path.join(wt, DD)
    for name, cmd in (('ci', ['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund']), ('build_shared', ['npm', 'run', 'build', '--workspace=packages/shared'])):
        rc, o, e, to = run(cmd, cwd=dev, timeout=1500)
        w(os.path.join(logd, 'setup_%s.out' % name), o); w(os.path.join(logd, 'setup_%s.err' % name), e)
        print('%s %s rc %d%s (%s)' % (now(), ' '.join(cmd), rc, ' TIMEOUT' if to else '', os.path.join(logd, 'setup_%s.out' % name)))
        if rc: return 1
    ok = os.path.isfile(os.path.join(dev, 'packages', 'shared', 'dist', 'index.js'))
    print('ASSERT packages/shared/dist/index.js present: %s | porcelain after setup %r' % (ok, porcelain(wt)[:160]))
    return 0 if ok else 1


# ---------------- #1448 states ----------------
def state48(state, clone, base, head):
    """-> {relpath: bytes|None}: the variable paths of #1448 (None = must be ABSENT)."""
    if state not in PRED48: raise SystemExit('REFUSED: --state %r (head|base|srchead_yamlbase|srcbase_yamlhead)' % state)
    src_rev = head if state in ('head', 'srchead_yamlbase') else base
    yaml_rev = head if state in ('head', 'srcbase_yamlhead') else base
    return {SRC: git_bytes(clone, src_rev, SRC), YAML: git_bytes(clone, yaml_rev, YAML), TEST48: git_bytes(clone, head, TEST48)}


def apply_state(wt, wr, qdir):
    rec = {}
    for rel, data in wr.items():
        p = os.path.join(wt, rel); must_be_outside(p, 'write')
        rec[rel] = open(p, 'rb').read() if os.path.isfile(p) else None
        if data is None:
            if os.path.isfile(p):
                os.makedirs(qdir, exist_ok=True); shutil.move(p, os.path.join(qdir, 'removed_%s_%d' % (os.path.basename(rel), int(time.time() * 1000))))
            if os.path.isfile(p): raise SystemExit('REMOVE NOT LANDED: %s' % rel)
        else:
            write_checked(wt, rel, data)
    return rec


def restore_state(wt, rec, qdir):
    bad = []
    for rel, data in rec.items():
        p = os.path.join(wt, rel)
        if data is None:
            if os.path.isfile(p):
                os.makedirs(qdir, exist_ok=True); shutil.move(p, os.path.join(qdir, 'planted_%s_%d' % (os.path.basename(rel), int(time.time() * 1000))))
            if os.path.isfile(p): bad.append(rel)
        else:
            write_checked(wt, rel, data)
            if sha(open(p, 'rb').read()) != sha(data): bad.append(rel)
    return bad


def sec_cmd(state, whole, wt, clone, base, head, out):
    must_be_outside(out, 'out dir'); os.makedirs(out, exist_ok=True); qd = os.path.join(out, 'quarantine')
    wr = state48(state, clone, base, head)
    if whole and state == 'base': wr[TEST48] = None          # the base suite has no new test
    rec = apply_state(wt, wr, qd)
    for rel, data in wr.items(): print('PLANT LANDED %-48s %s' % (rel.split('/')[-1], ('sha256/16 ' + sha(data)[:16]) if data is not None else 'ABSENT (moved to quarantine)'))
    jp = os.path.join(out, 'sec_state%s_%s.json' % (state, 'whole' if whole else 'file'))
    rels = [] if whole else [TEST48]
    rc, o, e, to = vitest(wt, rels, jp, timeout=1800 if whole else 900); w(jp.replace('.json', '.out'), o); w(jp.replace('.json', '.err'), e)
    r = read_vitest(jp); bad = restore_state(wt, rec, qd)
    print('%s vitest %s state=%s rc %d%s | LOAD-FAILED %s | suites %d | tests %d passed %d failed %d skipped %d | restored by sha: %s | porcelain %r' % (
        now(), 'WHOLE security' if whole else 'on the new test', state, rc, ' TIMEOUT' if to else '', r['load_failed'], r['suites'], r['tests'], r['passed'], r['failed'], r['skipped'], not bad, porcelain(wt)[:100]))
    for k, v in sorted(r['cells'].items()) if not whole else [(k, v) for k, v in r['cells'].items() if v == 'failed']:
        print('  %-8s %s%s' % (v.upper(), k, ('  :: ' + r['fail_msgs'][k][:200]) if k in r['fail_msgs'] else ''))
    print('PREDICTION %s%s: %s -- measured passed %d of %d tests across %d file(s), reds %s' % (state, ' WHOLE' if whole else '', (WHOLE48.get(state) if whole else PRED48[state]) or 'none recorded', r['passed'], r['tests'], r['suites'], sorted(k for k, v in r['cells'].items() if v == 'failed')))
    return 1 if (r['load_failed'] or bad) else 0


def tsc_cmd(wt, clone, base, head, out):
    must_be_outside(out, 'out dir'); os.makedirs(out, exist_ok=True)
    tsc = os.path.join(wt, DD, 'node_modules', '.bin', 'tsc'); pd = os.path.join(wt, SECD); tc = os.path.join(pd, 'tsconfig.json')
    rc, o, e, to = run(['node', tsc, '--noEmit', '-p', tc], cwd=pd, timeout=900); w(os.path.join(out, 'tsc_pkg.out'), o); w(os.path.join(out, 'tsc_pkg.err'), e)
    ex = run(['node', tsc, '--noEmit', '-p', tc, '--listFilesOnly'], cwd=pd, timeout=300)[1]
    n_test = len([l for l in ex.split('\n') if '/__tests__/' in l])
    print('%s tsc --noEmit -p services/security/tsconfig.json: rc %d%s | files of the program under src/__tests__: %d (the program %s the new test)' % (now(), rc, ' TIMEOUT' if to else '', n_test, 'EXCLUDES' if n_test == 0 else 'INCLUDES'))
    # scratch config that NAMES the new test (the seat's method): extends the package config
    sc = os.path.join(pd, 'tsconfig.gate82-scratch.json'); must_be_outside(sc, 'write')
    open(sc, 'w').write(json.dumps({'extends': './tsconfig.json', 'compilerOptions': {'noEmit': True, 'types': ['node']}, 'files': ['src/__tests__/ks1434-api-key-create-spec-declares-rotate.test.ts'], 'include': [], 'exclude': []}))
    try:
        rc2, o2, e2, _ = run(['node', tsc, '-p', sc], cwd=pd, timeout=900); lst = run(['node', tsc, '-p', sc, '--listFilesOnly'], cwd=pd, timeout=300)[1].split('\n')
        named = any(l.endswith('ks1434-api-key-create-spec-declares-rotate.test.ts') for l in lst); reach = any(l.endswith('src/security.openapi.ts') for l in lst)
        print('%s tsc with a SCRATCH config naming the new test: rc %d | program files %d | names the new test %s | reaches security.openapi.ts %s' % (now(), rc2, len([x for x in lst if x.strip()]), named, reach))
        plant = os.path.join(pd, 'src', 'gate82_ts2322_plant.ts'); open(plant, 'w').write("export const gate82Plant: number = 'not a number';\n")
        open(sc, 'w').write(json.dumps({'extends': './tsconfig.json', 'compilerOptions': {'noEmit': True, 'types': ['node']}, 'files': ['src/__tests__/ks1434-api-key-create-spec-declares-rotate.test.ts', 'src/gate82_ts2322_plant.ts'], 'include': [], 'exclude': []}))
        rc3, o3, e3, _ = run(['node', tsc, '-p', sc], cwd=pd, timeout=900)
        shutil.move(plant, os.path.join(out, 'gate82_ts2322_plant.ts.quarantined'))
        print('%s tsc CONTROL (a planted TS2322 in the same program): rc %d (must be non-zero; TS2322 in output: %s)' % (now(), rc3, 'TS2322' in o3 + e3))
    finally:
        if os.path.exists(sc): shutil.move(sc, os.path.join(out, 'tsconfig.gate82-scratch.json.quarantined'))
    ok = rc == 0 and rc2 == 0 and named and reach and rc3 != 0 and 'TS2322' in o3 + e3
    print('porcelain after: %r' % porcelain(wt)[:100]); return 0 if ok else 1


def specregen_cmd(wt, clone, base, head, out):
    must_be_outside(out, 'out dir'); os.makedirs(out, exist_ok=True); qd = os.path.join(out, 'quarantine')
    gen = os.path.join(wt, DD, 'scripts', 'generate-openapi.ts')   # `node --import tsx` (NOT the tsx CLI: its IPC socket path under a long TMPDIR exceeds the unix-socket limit and it dies)
    rc, o, e, to = run(['node', '--import', 'tsx', gen, '--check'], cwd=os.path.join(wt, DD), timeout=600); w(os.path.join(out, 'specregen_head.out'), o); w(os.path.join(out, 'specregen_head.err'), e)
    mods = [l.strip() for l in (o + e).split('\n') if re.match(r'^\s+- [a-z][a-z0-9-]*$', l)]
    print('%s generate-openapi.ts --check at the head: rc %d%s | "CHECK PASS" %s | modules listed by the generator: %d (the #1448 body says 19 at the base) incl. security: %s' % (now(), rc, ' TIMEOUT' if to else '', 'CHECK PASS' in o + e, len(mods), '- security' in mods))
    rec = apply_state(wt, {YAML: git_bytes(clone, base, YAML)}, qd)
    rc2, o2, e2, _ = run(['node', '--import', 'tsx', gen, '--check'], cwd=os.path.join(wt, DD), timeout=600); w(os.path.join(out, 'specregen_baseyaml.out'), o2); w(os.path.join(out, 'specregen_baseyaml.err'), e2)
    bad = restore_state(wt, rec, qd)
    print('%s CONTROL: the BASE yaml planted, --check: rc %d (must be non-zero) | "CHECK PASS" %s | drift message: %s | restored by sha %s' % (
        now(), rc2, 'CHECK PASS' in o2 + e2, [l.strip()[:120] for l in (o2 + e2).split('\n') if 'drift' in l.lower() or 'differ' in l.lower() or 'FAIL' in l][:2], not bad))
    pg = subprocess.run(['git', '-C', wt, 'status', '--porcelain'], capture_output=True, text=True).stdout.strip()
    print('porcelain after: %r' % pg[:100]); return 0 if (rc == 0 and 'CHECK PASS' in o + e and rc2 != 0 and not bad and not pg) else 1


def probe_cmd(wt, clone, base, head, out):
    must_be_outside(out, 'out dir'); os.makedirs(out, exist_ok=True); qd = os.path.join(out, 'quarantine')
    wr = state48('head', clone, base, head); rec = apply_state(wt, wr, qd)
    blk = open(os.path.join(HERE, 'probe_rotate_gate82.ts.txt'), encoding='utf-8').read()
    src = open(os.path.join(wt, HOST), encoding='utf-8').read()
    prel = os.path.join(os.path.dirname(HOST), 'gate82-probe-rotate.test.ts'); facts = os.path.join(out, 'probe_facts_rotate.jsonl')
    if os.path.exists(facts): os.rename(facts, facts + '.prev.%d' % int(time.time()))
    write_checked(wt, prel, (src + '\n' + blk).encode('utf-8'))
    jp = os.path.join(out, 'probe_rotate.json')
    rc, o, e, to = vitest(wt, [prel], jp, env_extra={'G82_PROBE_OUT': facts}); w(jp.replace('.json', '.out'), o); w(jp.replace('.json', '.err'), e)
    r = read_vitest(jp); qdir = os.path.join(out, 'quarantine_probe'); os.makedirs(qdir, exist_ok=True)
    shutil.move(os.path.join(wt, prel), os.path.join(qdir, 'gate82-probe-rotate.test.ts')); bad = restore_state(wt, rec, qd); pc = porcelain(wt)
    print('%s probe vitest rc %d%s | LOAD-FAILED %s | tests %d passed %d failed %d | the probe copy moved to %s | restored %s | porcelain clean: %s' % (now(), rc, ' TIMEOUT' if to else '', r['load_failed'], r['tests'], r['passed'], r['failed'], qdir, not bad, pc == ''))
    ran = 0
    for l in open(facts) if os.path.isfile(facts) else []:
        d = json.loads(l); ran += 1; print('  %s' % json.dumps(d, sort_keys=True)[:420])
    print('PROBE facts recorded: %d record(s) in %s (FACTS; the gate rules). NOT covered by this probe: the DB path, the null result, the HTTP handler and the 201 body.' % (ran, facts))
    return 0 if (not r['load_failed'] and ran >= 12 and not bad and pc == '') else 1


# ---------------- TAMPER tables ----------------
H48_DESC_ANCHOR = "'When true and a connectorId is supplied, the other active API keys for that connector in the same tenant are retired after the new key is minted: ' +"
TAMPER = {
 '1448': dict(kind='vitest', rows=[
    ('S1', 'remove the rotate property from the zod source (the yaml keeps it)', SRC, 'CUT_ROTATE', ['RED KS-1434 A1', 'RED KS-1434 A2', 'RED KS-1434 A3']),
    ('S2', 'the committed yaml loses rotate (the source keeps it)', YAML, 'YAML_CUT', ['RED KS-1434 A4']),
    ('S3', 'rotate default flips to true', SRC, [('rotate: z.boolean().optional().default(false).openapi({', 'rotate: z.boolean().optional().default(true).openapi({')], ['RED KS-1434 A2']),
    ('S4', 'rotate becomes a string', SRC, [('rotate: z.boolean().optional().default(false).openapi({', 'rotate: z.string().optional().default("false").openapi({')], ['RED KS-1434 A1', 'RED KS-1434 A2']),
    ('S5', 'the description drops the priorKeysRevoked sentence', SRC, [("'In that case the 201 response reports priorKeysRevoked, where null means the retirement was attempted and failed and the prior key is still valid. ' +\n", "'' +\n")], ['RED KS-1434 A3']),
    ('S6', 'WORDING: the description says the caller\'s keys instead of the other active keys for that connector (all four tokens kept)', SRC, [("the other active API keys for that connector in the same tenant are retired", "the caller\\'s own API keys are retired (connectorId, API_KEY_ROTATION_GRACE_SECONDS, priorKeysRevoked)")], []),
    ('S7', 'WORDING: the description claims EVERY key of the tenant is retired when no connectorId is sent (retire + connectorId + both tokens kept)', SRC, [("'Without a connectorId no prior key is retired.',", "'Without a connectorId every prior key in the tenant is retired (connectorId).',")], []),
    ('S8', 'WORDING: the grace sentence says positive means DEACTIVATED (the opposite of the runtime)', SRC, [("and with a positive value they are given an expiry that many seconds from now if that is earlier than their current one", "and with a positive value they are deactivated at once")], []),
    ('S9', 'a SECOND property is added to the yaml block (C1 pins "rotate is the only key that may be added")', YAML, 'YAML_EXTRA', ['control KS-1434 C1']),
    ('S10', 'the YAML description drifts from the generator (one word changed in the committed yaml only)', YAML, [("API_KEY_ROTATION_GRACE_SECONDS unset or 0 they are deactivated", "API_KEY_ROTATION_GRACE_SECONDS unset or 0 they are paused")], []),
    ('S11', 'WORDING, REGENERATED: the S8 wrong sentence in the source AND the committed yaml REGENERATED by the generator (cells, drift check and check:openapi all consistent)', SRC, [("and with a positive value they are given an expiry that many seconds from now if that is earlier than their current one", "and with a positive value they are deactivated at once")], []),
 ]),
 '1447': dict(kind='shell', gate='gate_script', rows=[
    ('M1', 'the old sentence returns (both echo lines as at the base)', 'RESTORE_BASE', [], ['cell 1']),
    ('M2', 'only the words `the remaining` return on the first echo', None, [('were changed under KS-1031. Exit 3 - the code this"', 'were changed under KS-1031; the remaining Exit 3 - the code this"')], ['cell 1']),
    ('M3', 'the runner exits 1 instead of 3 on a failed run', None, [('  exit 3\nfi', '  exit 1\nfi')], ['cell 2']),
    ('M4', 'the Summary line text changes', None, [('echo "Summary: applied=$applied_count failed=$failed_count skipped=$skipped_count"', 'echo "Totals: applied=$applied_count failed=$failed_count skipped=$skipped_count"')], ['cell 3', 'cell 4']),
    ('M5', 'the KS-1031 (KS-754 gate F-4) explanation is dropped', None, [('echo "KS-1031 (KS-754 gate F-4): this runner used to exit 0 here, so the"\n', '')], ['cell 2']),
    ('M6', 'WORDING: the message names a DIFFERENT open defect ("KS-808 still has an open defect") — no `counts-skips`, no `the remaining`', None, [('were changed under KS-1031. Exit 3 - the code this"', 'were changed under KS-1031; KS-808 still has an open defect. Exit 3 - the code this"')], []),
    ('M7', 'the clean run prints a failure line', None, [('echo "Migration runner finished (applied=$applied_count, failed=$failed_count)."', 'echo "ERROR: 0 migration(s) failed"; echo "Migration runner finished (applied=$applied_count, failed=$failed_count)."')], ['cell 4']),
 ]),
 '1449': dict(kind='shell', gate='template', rows=[
    ('E1', 'the key returns as `API_GATEWAY_PORT=6882`', None, 'APPEND:API_GATEWAY_PORT=6882\n', ['cell 1', 'cell 2']),
    ('E2', 'the key returns with leading spaces', None, 'APPEND:  API_GATEWAY_PORT=6882\n', ['cell 1', 'cell 2']),
    ('E3', 'the key returns as `export API_GATEWAY_PORT=6882` (the detector anchors on the key at the start of the line)', None, 'APPEND:export API_GATEWAY_PORT=6882\n', []),
    ('E4', 'the key returns with spaces around the equals sign', None, 'APPEND:API_GATEWAY_PORT = 6882\n', []),
    ('E5', 'the `# API GATEWAY` heading is removed', None, [('# API GATEWAY\n', '# GATEWAY\n')], ['cell 4']),
    ('E6', 'POSTGRES_EXTERNAL_PORT is removed from the template', None, [('POSTGRES_EXTERNAL_PORT=6432\n', '')], ['cell 4']),
    ('E7', 'WRONG FILE: the key returns in the LEGACY template .env.example (the suite scans only env.example and the generated .env)', 'LEGACY', 'APPEND:API_GATEWAY_PORT=6882\n', []),
    ('E8', 'a different dead gateway key is added (`API_GATEWAY_URL_PORT=6882`)', None, 'APPEND:API_GATEWAY_URL_PORT=6882\n', []),
 ]),
}
CELLRX = {'1447': [('cell 1', r'^FAIL: the failed-run output still names'), ('cell 2', r'^FAIL: CONTROL failed run'), ('cell 3', r'^FAIL: CONTROL summary'), ('cell 4', r'^FAIL: CONTROL clean run')],
          '1449': [('cell 1', r'^FAIL: env\.example still sets'), ('cell 2', r'^FAIL: the generated slot-2 \.env carries'), ('cell 3', r'^FAIL: CONTROL the detector'), ('cell 4', r'^FAIL: CONTROL bootstrap')]}


def pcounts(text):
    m = re.search(r'(\d+) passed, (\d+) failed', text); return (int(m.group(1)), int(m.group(2))) if m else None


def red_cells(pr, out):
    return sorted(c for c, rx in CELLRX[pr] if re.search(rx, out, re.M))


def tamper48(wt, clone, base, head, out, only):
    must_be_outside(out, 'out dir'); os.makedirs(out, exist_ok=True); qd = os.path.join(out, 'quarantine'); rc_all = 0
    wr = state48('head', clone, base, head); rec = apply_state(wt, wr, qd)
    rows = [('HEAD', 'no change (all green)', None, None, []), ('CONTROL', 'a no-op comment appended to the source (all green)', SRC, 'NOOP', [])] + [(a, b, c, d, e) for a, b, c, d, e in TAMPER['1448']['rows']]
    for tid, name, f, edits, pred in rows:
        if only and tid not in only and tid not in ('HEAD', 'CONTROL'): continue
        try:
            orig = git_bytes(clone, head, f).decode('utf-8') if f else None
            if edits is None: new = orig
            elif edits == 'NOOP': new = orig + '\n// gate82-noop\n'
            elif edits == 'CUT_ROTATE':
                a = orig.index('    // KS-1434: the runtime create schema'); b = orig.index('  }).openapi({', a)
                if orig.count('    // KS-1434: the runtime create schema') != 1: raise SystemExit('ANCHOR KS-1434 comment != 1')
                new = orig[:a] + orig[b:]
            elif edits in ('YAML_CUT', 'YAML_EXTRA'):
                lo = orig.index('\n    ApiKeyCreateRequest:\n'); hi = orig.index('\n    ApiKeyCreateResponse:\n', lo)
                inside = list(re.finditer(r'\n {8}rotate:\n(?: {10}.*\n)+', orig[lo:hi]))
                if len(inside) != 1: raise SystemExit('ANCHOR yaml rotate block inside ApiKeyCreateRequest occurs %d times (want 1)' % len(inside))
                m = inside[0]
                if edits == 'YAML_CUT': new = orig[:lo + m.start() + 1] + orig[lo + m.end():]
                else: new = orig[:lo + m.start() + 1] + '        gate82Extra:\n          type: boolean\n' + orig[lo + m.start() + 1:]
            else: new = apply_edits(orig, edits)
        except SystemExit as e:
            print('%s %-8s TAMPER-INVALID: %s' % (now(), tid, e)); rc_all = 1; continue
        ok_land = (new == orig) if edits is None else (new != orig)
        if f: write_checked(wt, f, new.encode('utf-8'))
        yaml_orig = git_bytes(clone, head, YAML)
        if tid == 'S11':   # regenerate the committed yaml from the tampered source (write mode), so every consistency check sees a CONSISTENT wrong description
            gen = os.path.join(wt, DD, 'scripts', 'generate-openapi.ts')
            gr0, go0, ge0, _ = run(['node', '--import', 'tsx', gen], cwd=os.path.join(wt, DD), timeout=600)
            print('      (S11) generator in WRITE mode rc %d; yaml changed vs head: %s' % (gr0, sha(open(os.path.join(wt, YAML), 'rb').read()) != sha(yaml_orig)))
        jp = os.path.join(out, 'tamper_1448_%s.json' % tid); r_rc, o, e, to = vitest(wt, [TEST48], jp); w(jp.replace('.json', '.out'), o); w(jp.replace('.json', '.err'), e)
        r = read_vitest(jp); reds = sorted(k for k, v in r['cells'].items() if v == 'failed')
        extra = ''
        if f and tid in ('S1', 'S2', 'S3', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11'):
            gen = os.path.join(wt, DD, 'scripts', 'generate-openapi.ts')
            gr, go, ge, _ = run(['node', '--import', 'tsx', gen, '--check'], cwd=os.path.join(wt, DD), timeout=600)
            extra = ' | generate-openapi --check rc %d (%s)' % (gr, 'CAUGHT by the committed-yaml drift check' if gr else 'NOT caught by it')
        if f: write_checked(wt, f, orig.encode('utf-8'))
        if tid == 'S11': write_checked(wt, YAML, yaml_orig)
        back = (sha(open(os.path.join(wt, f), 'rb').read()) == sha(orig.encode())) and (sha(open(os.path.join(wt, YAML), 'rb').read()) == sha(yaml_orig)) if f else True
        if r['load_failed']: verdict = 'TAMPER-INVALID (suite failed to LOAD: %s)' % r['message'][:120]; rc_all = 1
        elif tid == 'HEAD': verdict = 'OK all green' if not reds else 'FAIL: HEAD row has reds %s' % reds; rc_all |= 0 if not reds else 1
        elif tid == 'CONTROL': verdict = 'OK all green (harness quiet)' if not reds else 'FAIL: the no-op reds %s: the harness is noisy' % reds; rc_all |= 0 if not reds else 1
        else: verdict = ('ALL-GREEN: NO CELL CATCHES THIS TAMPER (a finding to rule)' if not reds else 'caught by %d cell(s)' % len(reds)) + ' | kit-builder prediction %s: %s' % (pred or 'ALL-GREEN', 'MATCH' if sorted(pred) == reds else 'DIFFER')
        print('%s %-8s %-92s landed %s restored %s | tests %d failed %d | %s%s' % (now(), tid, name[:92], ok_land, back, r['tests'], r['failed'], verdict, extra))
        for k in reds: print('      %s :: %s' % (k, r['fail_msgs'].get(k, '')[:160]))
        if not ok_land or not back: rc_all = 1
    bad = restore_state(wt, rec, qd)
    print('porcelain after the tamper rows: %r | state restored: %s' % (porcelain(wt)[:120], not bad)); return rc_all | (1 if bad else 0)


# ---------------- shell legs (#1447 / #1449) ----------------
def existing(clone, rev, cands):
    out = []
    for c in cands:
        if git(clone, 'ls-tree', rev, '--', c).strip(): out.append(c)
    return out


def tree_for(clone, rev, dest, pr):
    """extract the paths a PR's shell legs need into `dest` (NOT inside a repo)."""
    assert_not_in_repo(os.path.dirname(dest.rstrip('/')) or dest, 'tree parent')
    if os.path.exists(dest): raise SystemExit('REFUSED: %s exists (a fresh tree each time)' % dest)
    c = ['Blockchain/Dev/scripts', 'systemTest', '.githooks', 'Blockchain/Dev/docker-compose.yml', 'Blockchain/Dev/env.example', 'Blockchain/Dev/.env.example', 'Blockchain/Dev/env.local.example', 'Blockchain/Dev/observability', 'Blockchain/Dev/docker', 'observability'] + DOCS
    n = extract(clone, rev, existing(clone, rev, c), dest)
    assert_not_in_repo(dest, 'extracted tree')
    return dest


def cfg_hash(path):
    b = open(path, 'rb').read() if os.path.isfile(path) else b''
    h = hashlib.sha256(b).hexdigest()[:16]
    if h == EMPTY_SHA or not b: raise SystemExit('REFUSED: the config at %s is empty or absent (hash %s is the EMPTY-string hash: a check on it could not fail)' % (path, h))
    return h


def wed_config():
    gd = subprocess.run(['git', '-C', HERE, 'rev-parse', '--git-common-dir'], capture_output=True, text=True).stdout.strip()
    gd = gd if os.path.isabs(gd) else os.path.join(HERE, gd)
    return os.path.join(os.path.realpath(gd), 'config')


def run_suite(tree, rel, tmp, cwd, extra_env=None, timeout=300):
    env = {'TMPDIR': tmp}; env.update(extra_env or {})
    rc, o, e, to = run(['/bin/bash', os.path.join(tree, rel)], cwd=cwd, env=env, timeout=timeout)
    return rc, o, e, to, pcounts(o + e)


def failed_run_output(script_text, tmp):
    """the runner's own output on a failed run, with the suite's stubs: -> (rc, bytes, text)."""
    wk = os.path.join(tmp, 'frun_%d' % int(time.time() * 1000)); os.makedirs(os.path.join(wk, 'bin')); os.makedirs(os.path.join(wk, 'x', 'scripts')); os.makedirs(os.path.join(wk, 'x', 'migrations'))
    open(os.path.join(wk, 'bin', 'pg_isready'), 'w').write('#!/bin/sh\nexit 0\n')
    open(os.path.join(wk, 'bin', 'psql'), 'w').write('#!/bin/sh\nfor a in "$@"; do\n  case "$a" in\n    *.sql) case " $PSQL_FAIL " in *" ${a##*/} "*) echo "ERROR: 22P02 (stub)" >&2; exit 1 ;; esac ;;\n  esac\ndone\nexit 0\n')
    for f in ('pg_isready', 'psql'): os.chmod(os.path.join(wk, 'bin', f), 0o755)
    open(os.path.join(wk, 'x', 'scripts', 'run-migrations.sh'), 'w').write(script_text)
    open(os.path.join(wk, 'x', 'migrations', '047_ok.sql'), 'w').write('SELECT 1;\n'); open(os.path.join(wk, 'x', 'migrations', '048_ok.sql'), 'w').write('SELECT 1;\n')
    rc, o, e, to = run(['sh', 'scripts/run-migrations.sh'], cwd=os.path.join(wk, 'x'), env={'PATH': os.path.join(wk, 'bin') + ':/usr/bin:/bin', 'PSQL_FAIL': '048_ok.sql', 'DATABASE_URL': 'postgresql://secuura:pw@localhost:5432/secuura'}, timeout=60)
    txt = o + e
    return rc, len(txt.encode()), txt


def shells_cmd(pr, clone, head, base, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    tmp = canon_tmp(scratch); P = PR(pr)
    ctl = in_repo(HERE)
    print('%s scratch %s is canonical and NOT inside a repo (asserted); CONTROL: the kit dir %s IS inside a repo: %s' % (now(), scratch, HERE, ctl))
    if not ctl: print('FAIL the in-repo control did not fire'); return 1
    wed = wed_config(); h0 = cfg_hash(wed); print('hashed around every run: the config of the repo that CONTAINS this kit, %s sha256/16 %s' % (wed, h0))
    kc = os.path.join(clone, '.git', 'config') if os.path.isdir(os.path.join(clone, '.git')) else os.path.join(clone, 'config')
    k0 = cfg_hash(kc)
    stamp = '%d' % int(time.time()); th = tree_for(clone, head, os.path.join(scratch, 'tree_head_' + stamp), pr); tb = tree_for(clone, base, os.path.join(scratch, 'tree_base_' + stamp), pr)
    suite = P['suite']; gs = P['gate_script'] if pr == '1447' else None
    def cnt(c): return c
    if pr == '1447':
        runner = P['gate_script']
        g_head, g_base = git_bytes(clone, head, runner), git_bytes(clone, base, runner)
        pay = g_head.decode().split('\n'); pi = [i for i, l in enumerate(pay) if re.match(r'\s*# KS-1456:', l)]
        if len(pi) != 1: print('FAIL the Q-5D1456 comment line occurs %d times' % len(pi)); return 1
        g_pay = '\n'.join(pay[:pi[0]] + pay[pi[0] + 1:]).encode()
        arms = [('A', 'head runner, head suite', g_head, (4, 0), 0), ('B', 'BASE runner planted, head suite', g_base, (3, 1), 1), ('C', 'payload (head minus the comment line), head suite', g_pay, (4, 0), 0)]
        mode = os.stat(os.path.join(th, runner)).st_mode
        for aid, lab, data, want, wrc in arms:
            write_checked(th, runner, data); os.chmod(os.path.join(th, runner), mode)
            rc, o, e, to, c = run_suite(th, suite, tmp, scratch)
            w(os.path.join(out, 'shell1447_%s.out' % aid), o); w(os.path.join(out, 'shell1447_%s.err' % aid), e)
            print('%s ARM %s (%s): rc %d%s counts %s (the PR body says %s, rc %s) | red cells %s | plant sha256/16 %s' % (now(), aid, lab, rc, ' TIMEOUT' if to else '', c, want, wrc, red_cells('1447', o + e), sha(data)[:16]))
            if aid in ('A', 'C') and (c != want or rc != 0): rc_all = 1
            if aid == 'B' and (c != want or rc != 1): rc_all = 1
        write_checked(th, runner, g_head); os.chmod(os.path.join(th, runner), mode)
        # the runner's own failed-run output bytes: the body says 897 B, rc 3, byte-identical with and without the comment line
        res = {}
        for lab, data in (('head', g_head), ('payload', g_pay), ('base', g_base)):
            rc, nb, txt = failed_run_output(data.decode(), tmp); res[lab] = (rc, nb, txt); w(os.path.join(out, 'failedrun_%s.txt' % lab), txt)
        print('%s failed-run output of the runner (psql stub fails 048_ok.sql): head rc %d %d B | payload rc %d %d B | base rc %d %d B | head == payload byte for byte: %s (the PR body: 897 bytes, rc 3 each) | base vs head: %s' % (
            now(), res['head'][0], res['head'][1], res['payload'][0], res['payload'][1], res['base'][0], res['base'][1], res['head'][2] == res['payload'][2],
            [l for l in difflib.unified_diff(res['base'][2].split('\n'), res['head'][2].split('\n'), lineterm='', n=0) if not l.startswith(('---', '+++', '@@'))]))
        if not (res['head'][0] == 3 == res['payload'][0] and res['head'][2] == res['payload'][2] and res['head'][1] == 897): rc_all = 1
        sibs = P['siblings'][:2]; run_sibs = [(s, True) for s in sibs] + [(P['siblings'][2], False)]
        for s, can in run_sibs:
            if not can:
                print('%s SIBLING %s: NOT RUN by the kit (it needs services/api-gateway/src, node_modules, tsx and a DB shape; the seat claims 27/0 after and no base comparison): the gate may run it in its worktree' % (now(), s.split('/')[-1])); continue
            for lab, tr, data in (('base', th, g_base), ('head', th, g_head)):
                write_checked(th, runner, data); os.chmod(os.path.join(th, runner), mode)
                rc, o, e, to, c = run_suite(th, s, tmp, scratch); w(os.path.join(out, 'sibling_%s_%s.out' % (lab, os.path.basename(s))), o); w(os.path.join(out, 'sibling_%s_%s.err' % (lab, os.path.basename(s))), e)
                print('%s SIBLING %-4s %-60s rc %d%s counts %s output sha256/16 %s' % (now(), lab, os.path.basename(s), rc, ' TIMEOUT' if to else '', c, sha((o + e).encode())[:16]))
        write_checked(th, runner, g_head); os.chmod(os.path.join(th, runner), mode)
    else:
        tpl = P['template']; t_head, t_base = git_bytes(clone, head, tpl), git_bytes(clone, base, tpl)
        td = t_head.decode().split('\n'); wi = [i for i, l in enumerate(td) if l.startswith('# KS-1417: this block used to set')]
        if len(wi) != 1: print('FAIL the WHY line occurs %d times' % len(wi)); return 1
        t_pay = '\n'.join(td[:wi[0]] + td[wi[0] + 1:]).encode()
        ts_head = git_bytes(clone, head, suite).decode(); cdl = [i for i, l in enumerate(ts_head.split('\n')) if re.match(r'\s*cd "\$TREE"', l)]
        if len(cdl) != 1: print('FAIL the cd line occurs %d times' % len(cdl)); return 1
        ts_pay = '\n'.join(ts_head.split('\n')[:cdl[0]] + ts_head.split('\n')[cdl[0] + 1:])
        arms = [('A', 'head template, head test', t_head, ts_head, (4, 0), 0), ('B', 'BASE template planted, head test', t_base, ts_head, (2, 2), 1), ('C', 'payload template (no WHY line) + payload test (no cd line)', t_pay, ts_pay, (4, 0), 0)]
        for aid, lab, data, tdata, want, wrc in arms:
            write_checked(th, tpl, data)
            payname = suite.replace('.test.sh', '_payload.test.sh') if aid == 'C' else suite
            if aid == 'C': write_checked(th, payname, tdata.encode())
            rc, o, e, to, c = run_suite(th, payname, tmp, scratch)
            w(os.path.join(out, 'shell1449_%s.out' % aid), o); w(os.path.join(out, 'shell1449_%s.err' % aid), e)
            print('%s ARM %s (%s): rc %d%s counts %s (the PR body says %s, rc %s) | red cells %s | template sha256/16 %s' % (now(), aid, lab, rc, ' TIMEOUT' if to else '', c, want, wrc, red_cells('1449', o + e), sha(data)[:16]))
            if c != want or rc != wrc: rc_all = 1
            if aid == 'C' and os.path.exists(os.path.join(th, payname)): shutil.move(os.path.join(th, payname), os.path.join(out, 'quarantine_payload_test.sh'))
        write_checked(th, tpl, t_head)
        outs = {}
        for s in P['siblings']:
            for lab, data in (('base', t_base), ('head', t_head)):
                write_checked(th, tpl, data)
                rc, o, e, to, c = run_suite(th, s, tmp, scratch, timeout=600); outs[(s, lab)] = (rc, o + e, c)
                w(os.path.join(out, 'sibling_%s_%s.out' % (lab, os.path.basename(s))), o); w(os.path.join(out, 'sibling_%s_%s.err' % (lab, os.path.basename(s))), e)
            b_, h_ = outs[(s, 'base')], outs[(s, 'head')]
            dl = [l for l in difflib.unified_diff(b_[1].split('\n'), h_[1].split('\n'), lineterm='', n=0) if not l.startswith(('---', '+++', '@@'))]
            print('%s SIBLING %-44s base rc %d %s | head rc %d %s | counts equal %s | FULL outputs byte-identical %s (%d differing line(s): %s)' % (
                now(), os.path.basename(s), b_[0], b_[2], h_[0], h_[2], b_[2] == h_[2], b_[1] == h_[1], len(dl), [x[:110] for x in dl[:4]]))
            if b_[2] != h_[2] or h_[0] != b_[0]: rc_all = 1          # a base/head DIFFERENCE is a kit FAIL
            if h_[0] != 0 and h_[0] == b_[0] and b_[2] == h_[2]:    # equal and not green: an environment limit of the kit's tree, REPORTED, never a pass
                fl = [l.strip()[:150] for l in h_[1].split('\n') if l.startswith('FAIL')][:3]
                print('      -> NOT GREEN IN THE KIT\'S TREE, IDENTICAL at base and head (rc %d, %s): %s ; the READY claims green; the likely cause is a dependency the extracted tree does not have (e.g. `npx tsx` in systemTest/playwright: no npm ci there; npm ci in systemTest is NOT a named exception) — the cells it affects are NOT RUN here' % (h_[0], h_[2], fl))
        write_checked(th, tpl, t_head)
    # shell-suite discovery and the docs matrix
    for lab, tr in (('base', tb), ('head', th)):
        rc, o, e, to = run(['/bin/bash', os.path.join(tr, 'Blockchain/Dev/scripts/run-shell-suites.sh'), '--list'], cwd=scratch, env={'TMPDIR': tmp})
        n = len([l for l in o.split('\n') if l.strip()])
        print('%s run-shell-suites.sh --list at the %s tree: rc %d, %d line(s) (PR body: 74 -> 75; the new suite listed at head: %s)' % (now(), lab, rc, n, os.path.basename(suite) in o))
        w(os.path.join(out, 'list_%s.txt' % lab), o)
    rc, o, e, to, c = run_suite(th, K['docs_composition']['matrix_suite'], tmp, scratch)
    inval = 'is missing' in (o + e)
    print('%s html_docs_matrix at the head tree: rc %d counts %s (PR body: 12/0)%s' % (now(), rc, c, '  TREE-INVALID (a doc is missing: not a measurement)' if inval else ''))
    w(os.path.join(out, 'matrix_head.out'), o); w(os.path.join(out, 'matrix_head.err'), e)
    if inval or c is None or c[1] != 0: rc_all = 1
    wed1, k1 = cfg_hash(wed), cfg_hash(kc)
    print('CONFIG HASHES after: the repo containing this kit %s -> %s (%s) | the kit clone %s -> %s (%s)' % (h0, wed1, 'UNCHANGED' if h0 == wed1 else 'CHANGED', k0, k1, 'UNCHANGED' if k0 == k1 else 'CHANGED'))
    if h0 != wed1 or k0 != k1: rc_all = 1
    return rc_all


# ---------------- #1449 hooks hazard ----------------
GENV = {'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_AUTHOR_NAME': 'gate82', 'GIT_AUTHOR_EMAIL': 'x@x', 'GIT_COMMITTER_NAME': 'gate82', 'GIT_COMMITTER_EMAIL': 'x@x'}


def sh_git(args, cwd=None):
    e = dict(os.environ); e.update(GENV); e.pop('GIT_DIR', None); e.pop('GIT_WORK_TREE', None); e.pop('GIT_SSH_COMMAND', None)
    p = subprocess.run(['git'] + list(args), capture_output=True, text=True, cwd=cwd, env=e); return p.returncode, p.stdout.strip(), p.stderr.strip()


def make_repo(path, hooks):
    """a scratch repo with a .githooks dir (so the script's condition holds) and core.hooksPath = hooks (None = unset). Outside !CODING by construction."""
    must_be_outside(path, 'repo'); os.makedirs(path)
    assert sh_git(['init', '-q', path])[0] == 0
    os.makedirs(os.path.join(path, '.githooks')); open(os.path.join(path, '.githooks', '.keep'), 'w').write('x\n')
    open(os.path.join(path, 'f'), 'w').write('x\n')
    assert sh_git(['-C', path, 'add', '-A'])[0] == 0 and sh_git(['-C', path, 'commit', '-q', '-m', 'init'])[0] == 0
    if hooks is not None: assert sh_git(['-C', path, 'config', 'core.hooksPath', hooks])[0] == 0
    return path


def hooks_cmd(clone, head, base, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    tmp = canon_tmp(scratch); P = PR(1449); suite = P['suite']; stamp = '%d' % int(time.time())
    th = tree_for(clone, head, os.path.join(scratch, 'hk_tree_' + stamp), '1449')
    ts_head = git_bytes(clone, head, suite).decode(); ls = ts_head.split('\n'); cdl = [i for i, l in enumerate(ls) if re.match(r'\s*cd "\$TREE"', l)]
    if len(cdl) != 1: print('FAIL the cd line occurs %d times' % len(cdl)); return 1
    payname = suite.replace('.test.sh', '_payload.test.sh'); write_checked(th, payname, '\n'.join(ls[:cdl[0]] + ls[cdl[0] + 1:]).encode())
    print('%s the test AS RECEIVED = the committed test minus its one `cd "$TREE"` line (re-derived blob prefix %s; the seat\'s payload blob ebfa7933d1ab)' % (now(), hashlib.sha1(b'blob %d\0' % len('\n'.join(ls[:cdl[0]] + ls[cdl[0] + 1:]).encode()) + '\n'.join(ls[:cdl[0]] + ls[cdl[0] + 1:]).encode()).hexdigest()[:12]))
    # positive controls for the instrument
    rctl = make_repo(os.path.join(scratch, 'hk_ctl_' + stamp), None); cfg = os.path.join(rctl, '.git', 'config'); c0 = cfg_hash(cfg)
    sh_git(['-C', rctl, 'config', 'core.hooksPath', 'zz']); c1 = cfg_hash(cfg)
    print('%s INSTRUMENT CONTROL: a direct `git config core.hooksPath zz` changes the hash %s -> %s (reads CHANGED: %s); the empty-string hash %s is refused (a missing file raises)' % (now(), c0, c1, c0 != c1, EMPTY_SHA))
    if c0 == c1: return 1
    try: cfg_hash(os.path.join(scratch, 'no-such-config')); print('FAIL the empty-hash guard did not fire'); return 1
    except SystemExit: print('  the empty-hash guard fired on an absent config (OK)')
    def arm(aid, label, test, hooks, mode, want_changed, tmpdir=None, note=''):
        rp = make_repo(os.path.join(scratch, 'hk_%s_%s' % (aid, stamp)), hooks); cwd = rp
        if mode == 'worktree':
            wtp = os.path.join(scratch, 'hk_%s_wt_%s' % (aid, stamp)); assert sh_git(['-C', rp, 'worktree', 'add', '-q', '--detach', wtp])[0] == 0; cwd = wtp
        td = tmpdir(rp) if tmpdir else tmp
        if tmpdir: os.makedirs(td, exist_ok=True)
        cfg = os.path.join(rp, '.git', 'config'); before = cfg_hash(cfg); val0 = sh_git(['-C', rp, 'config', 'core.hooksPath'])[1] or '(unset)'
        rc, o, e, to, c = run_suite(th, test, td, cwd, extra_env=GENV)
        after = cfg_hash(cfg); val1 = sh_git(['-C', rp, 'config', 'core.hooksPath'])[1] or '(unset)'
        wt_cfg = os.path.join(rp, '.git', 'worktrees'); wtpriv = os.path.isdir(wt_cfg) and any(f == 'config.worktree' for _, _, fs in os.walk(wt_cfg) for f in fs)
        changed = before != after
        ok = (changed == want_changed) and c is not None
        w(os.path.join(out, 'hooks_%s.out' % aid), o + e)
        print('%s ARM %-3s %-86s test rc %d counts %s | hooksPath %s -> %s | caller .git/config hash %s -> %s : %s (predicted %s) %s%s' % (
            now(), aid, label, rc, c, val0, val1, before, after, 'CHANGED' if changed else 'UNCHANGED', 'CHANGED' if want_changed else 'UNCHANGED', 'MATCH' if ok else 'DIFFER', (' | worktree-private config.worktree: %s' % wtpriv) if mode == 'worktree' else '') + (' | ' + note if note else ''))
        return ok
    A = [('H1', 'repo with core.hooksPath UNSET; cwd = the repo; test AS RECEIVED (no cd)', payname, None, 'repo', True),
         ('H2', 'the same, test AS COMMITTED (with the cd)', suite, None, 'repo', False),
         ('H3', 'core.hooksPath already `.githooks`; AS RECEIVED', payname, '.githooks', 'repo', False),
         ('H4', 'core.hooksPath already `.githooks`; AS COMMITTED', suite, '.githooks', 'repo', False),
         ('H5', 'core.hooksPath = `custom/hooks` (some OTHER value); AS RECEIVED', payname, 'custom/hooks', 'repo', True),
         ('H6', 'core.hooksPath = `custom/hooks`; AS COMMITTED', suite, 'custom/hooks', 'repo', False),
         ('H7', 'cwd = a git WORKTREE of a repo with it unset; AS RECEIVED (the MAIN repo\'s config is hashed)', payname, None, 'worktree', True),
         ('H8', 'the same worktree caller; AS COMMITTED', suite, None, 'worktree', False)]
    for aid, label, test, hooks, mode, want in A:
        try:
            if not arm(aid, label, test, hooks, mode, want): rc_all = 1
        except SystemExit as e:
            print('%s ARM %s INVALID: %s' % (now(), aid, e)); rc_all = 1
    # H9: the case the seat left UNMEASURED: TMPDIR inside a repo that has .githooks (core.hooksPath unset), test AS COMMITTED (the cd lands inside that repo)
    try:
        ok = arm('H9', 'TMPDIR INSIDE the unset repo (the seat\'s UNMEASURED case); test AS COMMITTED (cd into a scratch tree that lies inside the repo)', suite, None, 'repo', True, tmpdir=lambda rp: os.path.join(rp, 'tmp'),
                 note='kit-builder PREDICTION from reading bootstrap-env.sh:315-324: CHANGED (git rev-parse --show-toplevel then resolves to the enclosing repo); the arm MEASURES it')
        if not ok: rc_all = 1
    except SystemExit as e:
        print('%s ARM H9 INVALID: %s' % (now(), e)); rc_all = 1
    print('NOTE: every arm runs with GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 (a GLOBAL core.hooksPath on a real machine changes what the script reads); scratch repos live under %s, outside every other repo.' % scratch)
    return rc_all


# ---------------- docs / compose ----------------
def insertion(basetxt, headtxt):
    la, lb = basetxt.split('\n'), headtxt.split('\n')
    ops = [x for x in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes() if x[0] != 'equal']
    if len(ops) != 1 or ops[0][0] != 'insert': raise SystemExit('not a pure insertion: %s' % ops[:3])
    _, i1, _, j1, j2 = ops[0]; return i1, lb[j1:j2]


def compose_keep_both(devtxt, frags):
    """[g82] frags: [fragment_lines] IN THE ORDER TO PLACE THEM; all are inserted immediately before the LAST `</body>` of `devtxt` (the develop the gate reads):
    each PR's fragment was extracted against its OWN parent, and every parent's insertion point is the line before </body>."""
    la = devtxt.split('\n'); idx = [i for i, l in enumerate(la) if l.strip() == '</body>']
    if not idx: raise SystemExit('no </body> line in the develop doc')
    i = idx[-1]; return '\n'.join(la[:i] + [l for f in frags for l in f] + la[i:])


def flow_numbers(txt): return [int(x) for x in re.findall(r'<h2>(\d+)\.', txt)]


def merge_file(cur, basef, other):
    rc, o, e, to = run(['git', 'merge-file', '-p', '-L', 'ours', '-L', 'base', '-L', 'theirs', cur, basef, other], timeout=60)
    return rc, o


def heads_of(A): return dict((n, req(A, '--head' + n, True)) for n in K['go_prs'])
def bases_of(A): return dict((n, req(A, '--base' + n, True)) for n in K['go_prs'])


def compose_tree(clone, develop, heads, bases, order, scratch, tag):
    """a TEMP INDEX tree of the whole composition in `order` over DEVELOP: every PR's exclusive (non-doc) paths from its head (each asserted UNCHANGED between the PR's base and
    develop, else the head's blob would silently revert develop), the docs keep-both in `order`. -> dict(full, nodocs, docs). Writes objects into the KIT CLONE only."""
    idx = os.path.join(scratch, 'idx_%s_%d' % (tag, int(time.time() * 1000))); env = {'GIT_INDEX_FILE': idx}; must_be_outside(idx, 'temp index')
    rc, o, e = cgit(clone, ['read-tree', develop], env=env)
    if rc: raise SystemExit('read-tree: ' + e)
    def put(path, data, mode='100644'):
        rc, o, e = cgit(clone, ['hash-object', '-w', '--stdin'], inp=data)
        if rc: raise SystemExit('hash-object: ' + e)
        bid = o.decode().strip(); rc, o, e = cgit(clone, ['update-index', '--add', '--cacheinfo', '%s,%s,%s' % (mode, bid, path)], env=env)
        if rc: raise SystemExit('update-index: ' + e)
        return bid
    moved = []
    for n in order:
        for path in PR(n)['numstat']:
            if path in DOCS: continue
            if path not in PR(n)['added_paths'] and blob(clone, bases[n], path) != blob(clone, develop, path): moved.append((n, path))
            put(path, git_bytes(clone, heads[n], path), PR(n)['modes'][path])
    if moved: raise SystemExit('develop MOVED a path of a PR since its base: %s (the head blob would revert it)' % moved)
    docs_texts = {}
    for d in DOCS:
        dv = git_bytes(clone, develop, d).decode('utf-8')
        fr = [insertion(git_bytes(clone, bases[n], d).decode('utf-8'), git_bytes(clone, heads[n], d).decode('utf-8'))[1] for n in order]
        docs_texts[d] = compose_keep_both(dv, fr); put(d, docs_texts[d].encode('utf-8'))
    rc, o, e = cgit(clone, ['write-tree'], env=env)
    if rc: raise SystemExit('write-tree: ' + e)
    full = o.decode().strip()
    for d in DOCS:
        bid = cgit(clone, ['rev-parse', '%s:%s' % (develop, d)])[1].decode().strip(); cgit(clone, ['update-index', '--cacheinfo', '100644,%s,%s' % (bid, d)], env=env)
    rc, o, e = cgit(clone, ['write-tree'], env=env); nodocs = o.decode().strip()
    return dict(full=full, nodocs=nodocs, docs=docs_texts)


def compose_cmd(clone, develop, heads, bases, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); os.makedirs(scratch, exist_ok=True); rc_all = 0
    print('%s COMPOSITION over develop %s: the code paths are DISJOINT (c1 P13), so there is no audit-export.ts-style same-file merge; the proof is: a temp-index tree per order, the code-only tree identical across orders and equal to develop + each PR\'s own paths' % (now(), develop[:12]))
    trees = {}
    for tag, order in (('A', K['compose_orders']['A']), ('B', K['compose_orders']['B']), ('C', K['compose_orders']['C'])):
        try:
            t = compose_tree(clone, develop, heads, bases, order, scratch, tag); trees[tag] = t
            print('  TEMP-INDEX TREE order %s (%s): FULL %s | CODE-ONLY (docs reset to develop) %s' % (tag, ' -> '.join('#' + n for n in order), t['full'], t['nodocs']))
        except SystemExit as e:
            print('  TEMP-INDEX TREE order %s: %s' % (tag, e)); rc_all = 1
    if len(trees) == 3:
        same = len({t['nodocs'] for t in trees.values()}) == 1; nfull = len({t['full'] for t in trees.values()})
        print('  CODE-ONLY tree IDENTICAL across orders A / B / C: %s (%s) | FULL trees differ only by the docs order: %d distinct of 3' % (same, trees['A']['nodocs'][:12], nfull)); rc_all |= 0 if same else 1
        want = sorted(set(p for n in K['go_prs'] for p in PR(n)['numstat'] if p not in DOCS))
        rc, o, e = cgit(clone, ['diff', '--name-only', develop, trees['A']['nodocs']])
        got = sorted(x for x in o.decode().split('\n') if x)
        print('  develop..CODE-ONLY-tree paths == the union of the three PRs\' own non-doc paths: %s (%d paths) %s' % (got == want, len(got), '' if got == want else (sorted(set(got) ^ set(want)))))
        rc_all |= 0 if got == want else 1
        for n in K['go_prs']:
            for p in PR(n)['code_paths']:
                a = cgit(clone, ['rev-parse', '%s:%s' % (trees['A']['nodocs'], p)])[1].decode().strip(); b = cgit(clone, ['rev-parse', '%s:%s' % (heads[n], p)])[1].decode().strip()
                if a != b: print('  FAIL composed blob of %s != #%s head blob' % (p, n)); rc_all = 1
        print('  every PR path of the CODE-ONLY tree == that PR\'s head blob (checked for %d paths)' % sum(len(PR(n)['code_paths']) for n in K['go_prs']))
        json.dump(dict((k, dict(full=v['full'], nodocs=v['nodocs'])) for k, v in trees.items()), open(os.path.join(out, 'compose_trees.json'), 'w'), indent=1)
    pairs = [('1447', '1448'), ('1447', '1449'), ('1448', '1449')]
    for a, b in pairs:
        rc, o, e = cgit(clone, ['merge-tree', '--write-tree', '--name-only', heads[a], heads[b]])
        lines = o.decode('utf-8', 'replace').strip().split('\n'); tree = lines[0] if lines else ''
        conf = [l for l in lines[1:] if l.strip() and not l.startswith('Auto-merging') and not l.startswith('CONFLICT')]
        print('  merge-tree --write-tree #%s + #%s (merge base computed by git): rc %d (1 = conflicts; anything else is an ERROR) tree %s | conflicted paths %s' % (a, b, rc, tree[:12], sorted(set(conf)) or 'none'))
        if rc not in (0, 1): rc_all = 1
    for n in K['go_prs']:
        rc, o, e = cgit(clone, ['merge-tree', '--write-tree', '--name-only', develop, heads[n]])
        lines = o.decode('utf-8', 'replace').strip().split('\n'); conf = [l for l in lines[1:] if l.strip() and not l.startswith('Auto-merging') and not l.startswith('CONFLICT')]
        print('  merge-tree --write-tree develop %s + #%s: rc %d tree %s | conflicted paths %s' % (develop[:12], n, rc, (lines[0] if lines else '')[:12], sorted(set(conf)) or 'none'))
        if rc not in (0, 1): rc_all = 1
    return rc_all


def docs_cmd(clone, develop, heads, bases, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    assert_not_in_repo(scratch, 'scratch'); tmp = canon_tmp(scratch)
    orders = [(t, K['compose_orders'][t]) for t in ('A', 'B', 'C')]; texts = {}; wants = {}
    for d in DOCS:
        dv = git_bytes(clone, develop, d).decode('utf-8'); nm = os.path.basename(d)
        ins = dict((n, insertion(git_bytes(clone, bases[n], d).decode('utf-8'), git_bytes(clone, heads[n], d).decode('utf-8'))) for n in heads)
        print('%s %s: insertion position per PR against ITS OWN parent (line) %s | each directly before </body> | develop tail flow numbers %s (document order) | next free by max+1 %s' % (
            now(), nm, dict((n, v[0] + 1) for n, v in ins.items()), flow_numbers(dv)[-4:], (max(flow_numbers(dv)) + 1) if flow_numbers(dv) else 'n/a'))
        sd = os.path.join(scratch, 'docs_' + nm[:12]); os.makedirs(sd, exist_ok=True); w(os.path.join(sd, 'develop.html'), dv)
        for n in heads:
            w(os.path.join(sd, 'parent_%s.html' % n), git_bytes(clone, bases[n], d)); w(os.path.join(sd, 'head_%s.html' % n), git_bytes(clone, heads[n], d))
        for n in heads:   # each PR ALONE onto develop (a textual merge of its change onto the develop the gate reads)
            rc, o = merge_file(os.path.join(sd, 'develop.html'), os.path.join(sd, 'parent_%s.html' % n), os.path.join(sd, 'head_%s.html' % n)); w(os.path.join(out, 'merge_alone_%s_%s.txt' % (nm[:10], n)), o)
            print('  #%s alone onto develop, textual merge-file: %s hunk(s) (a conflict means develop has a block at the SAME insertion line; #%s\'s parent is %s)' % (n, rc if rc >= 0 else 'ERR', n, bases[n][:12]))
        for tag, order in orders:
            frs = [ins[n][1] for n in order]; res = compose_keep_both(dv, frs); texts[(tag, d)] = res
            w(os.path.join(sd, 'composed_%s.html' % tag), res)
            counts = dict((n, res.count('\n'.join(ins[n][1]))) for n in order)
            h2 = {}
            for n in order:
                h2[n] = len([l for l in ins[n][1] if '<h2' in l])
            rebuilt = '\n'.join([l for l in res.split('\n')])
            # composed minus the fragments == develop, byte for byte
            minus = res
            for n in order: minus = minus.replace('\n'.join(ins[n][1]) + '\n', '', 1)
            fn = flow_numbers(res) if d == DOCS[0] else None
            once = all(c == 1 for c in counts.values()); equal_dev = (minus == dv)
            print('     KEEP-BOTH %s (%s): fragment counts WANT 1 each %s -> %s | composed minus the 3 fragments == develop byte for byte: %s | h2 per fragment %s%s' % (
                tag, ' -> '.join('#' + n for n in order), counts, once, equal_dev, h2, (' | flow numbers in file order (tail) %s' % fn[-6:]) if fn else ''))
            if not once or not equal_dev: rc_all = 1
            if d == DOCS[0]:
                wantf = [K['docs_composition']['flow_numbers'][n] for n in order]; tail = [x for x in fn if x in wantf]
                print('     placement order %s -> file order of the three flow numbers %s : %s' % (wantf, tail, 'MATCH' if tail == wantf else 'DIFFER')); rc_all |= 0 if tail == wantf else 1
    SHELL_PATHS = ['systemTest', 'Blockchain/Dev/scripts', '.githooks'] + DOCS
    def tree(rev, dest):
        if not os.path.exists(dest): extract(clone, rev, existing(clone, rev, SHELL_PATHS), dest)
        assert_not_in_repo(dest, 'matrix tree'); return dest
    mx = K['docs_composition']['matrix_suite']; results = {}
    drop = {}
    for d in DOCS:
        dv = git_bytes(clone, develop, d).decode('utf-8'); ins = dict((n, insertion(git_bytes(clone, bases[n], d).decode('utf-8'), git_bytes(clone, heads[n], d).decode('utf-8'))) for n in heads)
        drop[d] = compose_keep_both(dv, [ins[n][1] for n in ('1447', '1449')]); wants[d] = ins
    for lab, rev, comp in [('develop tree (control)', develop, None)] + [('COMPOSED order %s' % t, develop, t) for t, _ in orders] + [('DROP-A-BLOCK control (no #1448)', develop, 'DROP')]:
        td = os.path.join(scratch, 'mx_' + re.sub(r'\W+', '_', lab)[:22]); tree(rev, td)
        if comp:
            for d in DOCS: w(os.path.join(td, d), drop[d] if comp == 'DROP' else texts[(comp, d)])
        rc, o, e, to = run(['/bin/bash', os.path.join(td, mx)], cwd=td, env={'TMPDIR': tmp}, timeout=300); m = re.search(r'(\d+) passed, (\d+) failed', o + e); c = (int(m.group(1)), int(m.group(2))) if m else None
        inval = 'is missing' in (o + e)
        w(os.path.join(out, 'matrix_%s.out' % re.sub(r'\W+', '_', lab)[:22]), o); w(os.path.join(out, 'matrix_%s.err' % re.sub(r'\W+', '_', lab)[:22]), e)
        print('%s html_docs_matrix on %-34s rc %d%s counts %s%s' % (now(), lab, rc, ' TIMEOUT' if to else '', c, '  TREE-INVALID (a doc is missing: not a measurement)' if inval else ''))
        results[lab] = (rc, c, inval)
        if inval: rc_all = 1
    ok_orders = [lab for lab, (rc, c, inv) in results.items() if lab.startswith('COMPOSED') and rc == 0 and c and c[1] == 0 and not inv]
    print('COMPOSED orders with html_docs_matrix 0 failed: %s (PASS condition: order A + at least ONE other)' % ok_orders)
    if 'COMPOSED order A' not in ok_orders or len(ok_orders) < 2: rc_all = 1
    dk = results['DROP-A-BLOCK control (no #1448)']
    cnt = all(drop[DOCS[0]].count('\n'.join(wants[DOCS[0]][n][1])) == 1 for n in ('1447', '1449', '1448')) if False else (drop[DOCS[0]].count('\n'.join(wants[DOCS[0]]['1448'][1])) == 1)
    print('CONTROL: a composition WITHOUT #1448: html_docs_matrix rc %d counts %s (gate81 G81-2: the matrix does NOT detect a dropped block) | the COUNT check (fragment of #1448 present once) reads %s and the flow number 54 is present: %s -> the count check %s' % (
        dk[0], dk[1], cnt, 54 in flow_numbers(drop[DOCS[0]]), 'CATCHES the drop' if not cnt and 54 not in flow_numbers(drop[DOCS[0]]) else 'DOES NOT CATCH THE DROP'))
    rc_all |= 0 if (not cnt and 54 not in flow_numbers(drop[DOCS[0]])) else 1
    return rc_all


# ---------------- shell tamper (#1447 / #1449) ----------------
def tamper_shell(pr, clone, head, base, scratch, out, only):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    tmp = canon_tmp(scratch); P = PR(pr); T = TAMPER[pr]; stamp = '%d' % int(time.time())
    th = tree_for(clone, head, os.path.join(scratch, 'tm_tree_%s_%s' % (pr, stamp)), pr); suite = P['suite']
    rel = P['gate_script'] if pr == '1447' else P['template']; legacy = 'Blockchain/Dev/.env.example'
    head_src = git_bytes(clone, head, rel).decode('utf-8'); base_src = git_bytes(clone, base, rel).decode('utf-8'); leg_src = git_bytes(clone, head, legacy).decode('utf-8')
    mode = os.stat(os.path.join(th, rel)).st_mode
    rows = [('HEAD', 'no change (all green)', None, None, []), ('CONTROL', 'a no-op comment appended (all green)', None, 'NOOP', [])] + [(a, b, c, d, e) for a, b, c, d, e in T['rows']]
    for tid, name, special, edits, pred in rows:
        if only and tid not in only and tid not in ('HEAD', 'CONTROL'): continue
        target, src = rel, head_src
        try:
            if edits is None and special is None: new = src
            elif edits == 'NOOP': new = src + ('\n# gate82-noop\n')
            elif special == 'RESTORE_BASE': new = base_src
            elif special == 'LEGACY':
                target, src = legacy, leg_src; new = leg_src + edits[len('APPEND:'):]
            elif isinstance(edits, str) and edits.startswith('APPEND:'): new = src.rstrip('\n') + '\n' + edits[len('APPEND:'):]
            else: new = apply_edits(src, edits)
        except SystemExit as e:
            print('%s %-6s TAMPER-INVALID: %s' % (now(), tid, e)); rc_all = 1; continue
        ok_land = (new == src) if (edits is None and special is None) else (new != src)
        write_checked(th, target, new.encode('utf-8')); os.chmod(os.path.join(th, target), mode if target == rel else os.stat(os.path.join(th, target)).st_mode)
        rc, o, e, to, c = run_suite(th, suite, tmp, scratch)
        reds = red_cells(pr, o + e)
        write_checked(th, target, src.encode('utf-8')); back = sha(open(os.path.join(th, target), 'rb').read()) == sha(src.encode())
        w(os.path.join(out, 'tamper_%s_%s.out' % (pr, tid)), o + e)
        if c is None: verdict = 'TAMPER-INVALID (no count: the suite did not run)'; rc_all = 1
        elif tid in ('HEAD', 'CONTROL'): verdict = 'OK' if c == (4, 0) and rc == 0 else 'FAIL: %s rc %d' % (c, rc); rc_all |= 0 if c == (4, 0) and rc == 0 else 1
        else: verdict = ('ALL-GREEN: NO CELL CATCHES THIS TAMPER (a finding to rule)' if c[1] == 0 else 'caught: %d failed (%s)' % (c[1], reds)) + ' | kit-builder prediction %s: %s' % (pred or 'ALL-GREEN', 'MATCH' if sorted(pred) == reds else 'DIFFER')
        print('%s %-8s %-100s landed %s restored %s | rc %d counts %s | %s' % (now(), tid, name[:100], ok_land, back, rc, c, verdict))
        if not ok_land or not back: rc_all = 1
    return rc_all


# ---------------- selftest ----------------
def selftest():
    tmpd = os.environ.get('TMPDIR', '')
    if not tmpd or os.path.realpath(tmpd) != tmpd.rstrip('/') or in_repo(tmpd):
        print('REFUSED: the selftest runs only with TMPDIR set to a CANONICAL (realpath) directory outside every git repo; TMPDIR=%r (realpath %r, inside a repo: %s)' % (tmpd, os.path.realpath(tmpd) if tmpd else None, in_repo(tmpd) if tmpd and os.path.isdir(tmpd) else 'n/a')); return 2
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    rep(os.path.realpath(tmpd) == tmpd.rstrip('/') and not in_repo(tmpd), 'TMPDIR %s is canonical (realpath equal) and NOT inside a repo' % tmpd)
    tmpd = tempfile.mkdtemp(prefix='g82st_', dir=tmpd)   # a fresh work dir per run (nothing is deleted; the TMPDIR keeps the residue)
    rep(in_repo(HERE), 'CONTROL: the kit directory IS inside a repo (in_repo fires)')
    try: assert_not_in_repo(HERE, 'x'); rep(False, 'assert_not_in_repo accepted the kit dir')
    except SystemExit: rep(True, 'ARM: assert_not_in_repo refuses a path inside a repo')
    try: canon_tmp('/Volumes/DevMASTER/!CODING/zz'); rep(False, 'canon_tmp accepted a !CODING path')
    except SystemExit: rep(True, 'ARM: canon_tmp refuses a scratch under !CODING')
    try: apply_edits('a b a', [('a', 'x')]); rep(False, 'a 2-occurrence anchor was ACCEPTED')
    except SystemExit: rep(True, 'ARM: anchor occurring twice -> refused (tamper not applied)')
    try: apply_edits('a b', [('zz', 'x')]); rep(False, 'an absent anchor was ACCEPTED')
    except SystemExit: rep(True, 'ARM: anchor absent -> refused')
    t = apply_edits('one two', [('two', 'TWO')]); rep(t == 'one TWO' and landed('one two', t, [('two', 'TWO')]), 'a single-occurrence edit applies and reads LANDED')
    rep(not landed('x', 'x', [('a', 'b')]), 'PLANTED no-change reads NOT LANDED')
    j = {'testResults': [{'name': 'a', 'status': 'passed', 'assertionResults': [{'title': 'RED KS-1434 A1: x', 'status': 'passed'}, {'title': 'control KS-1434 C1: y', 'status': 'failed', 'failureMessages': ['boom\n at x']}]}, {'name': 'b', 'status': 'failed', 'assertionResults': [], 'message': 'Test suite failed to run'}]}
    p = os.path.join(tmpd, 'selftest_vitest.json'); open(p, 'w').write(json.dumps(j)); r = read_vitest(p)
    rep(r['load_failed'] and r['tests'] == 2 and r['failed'] == 1 and r['cells'].get('control KS-1434 C1') == 'failed' and 'RED KS-1434 A1' in r['cells'], 'vitest reader: a suite that failed to LOAD is load_failed (never a count); cell keys read')
    open(p, 'w').write(json.dumps({'testResults': [{'name': 'a', 'status': 'passed', 'assertionResults': [{'title': 'ok', 'status': 'passed'}]}]})); rep(not read_vitest(p)['load_failed'], 'vitest reader: a clean file is not load_failed')
    rep(read_vitest(os.path.join(tmpd, 'does-not-exist.json'))['load_failed'], 'vitest reader: NO JSON WRITTEN reads load_failed (never a green)')
    seen = {}; k1 = cell_key('RED KS-1 X1: a', seen); k2 = cell_key('RED KS-1 X1: b', seen); rep(k1 != k2, 'cell keys: two titles with the same prefix get distinct keys')
    rep(pcounts('x\n  4 passed, 0 failed\n') == (4, 0) and pcounts('nothing') is None, 'pcounts reads "N passed, M failed" and nothing else')
    rep(red_cells('1449', 'PASS: a\nFAIL: env.example still sets API_GATEWAY_PORT (nothing reads it)\nFAIL: CONTROL bootstrap rc=1') == ['cell 1', 'cell 4'] and red_cells('1447', 'PASS: x\n') == [], 'red_cells maps FAIL lines to cells and reads nothing from PASS lines')
    dev = 'x\n</body>\n'
    r1 = compose_keep_both(dev, [['H51'], ['H52'], ['H54']]); rep(r1 == 'x\nH51\nH52\nH54\n</body>\n', 'compose_keep_both: three fragments go before </body> in the given order, each present once')
    rep(compose_keep_both(dev, [['H54'], ['H52'], ['H51']]) == 'x\nH54\nH52\nH51\n</body>\n', 'compose_keep_both: the REVERSE placement is a different, equally complete text')
    rep(compose_keep_both(dev, [['H51']]).count('H54') == 0, 'CONTROL: a composition keeping one block reads the others ABSENT (the count check can fail)')
    try: compose_keep_both('no body', [['a']]); rep(False, 'a doc with no </body> was ACCEPTED')
    except SystemExit: rep(True, 'ARM: a develop doc with no </body> -> refused')
    ia, fa = insertion('x\n</body>\n', 'x\nH51\n</body>\n'); rep(ia == 1 and fa == ['H51'], 'insertion reads the block and its base position')
    try: insertion('x\n</body>\n', 'y\n</body>\n'); rep(False, 'a non-insertion was ACCEPTED')
    except SystemExit: rep(True, 'ARM: a replaced base line is not a pure insertion -> refused')
    rep(flow_numbers('<h2>51. a</h2><h2>52. b</h2><h2>54. c</h2>') == [51, 52, 54], 'flow_numbers reads <h2>NN.</h2> headings')
    d = os.path.join(tmpd, 'selftest_a'); os.makedirs(d, exist_ok=True)
    for n, tx in (('x', 'one\ntwo\nthree\n'), ('y', 'one\ntwo\nthree\nfour\n'), ('z', 'zero\ntwo\nthree\n'), ('q', 'one\nTWO\nthree\n'), ('r', 'one\ntwo!\nthree\n')): open(os.path.join(d, n), 'w').write(tx)
    rc, o = merge_file(os.path.join(d, 'y'), os.path.join(d, 'x'), os.path.join(d, 'z')); rep(rc == 0 and o.startswith('zero') and o.rstrip().endswith('four'), 'merge_file: a clean 3-way merge reads rc 0')
    rc, o = merge_file(os.path.join(d, 'q'), os.path.join(d, 'x'), os.path.join(d, 'r')); rep(rc == 1 and ('<' * 7 + ' ours') in o, 'merge_file: PLANTED same-line edits read rc 1 with a conflict marker (the instrument can see a conflict)')
    rc, o, e, to = run(['sh', '-c', 'cat >/dev/null'], timeout=2, stdin=None); rep(rc == 0 and not to, 'run(): a child with stdin /dev/null returns')
    pre = time.time(); rc, o, e, to = run(['sh', '-c', 'sleep 30'], timeout=1); rep(to and time.time() - pre < 6, 'run(): a hanging child is killed by process group at the timeout (TIMEOUT reported)')
    try: must_be_outside('/Volumes/DevMASTER/!CODING/x/y', 'write'); rep(False, 'a write under !CODING was ACCEPTED')
    except SystemExit: rep(True, 'ARM: a write path under !CODING -> refused (lexical)')
    try: extract('/nonexistent-repo', 'abc', ['x'], '/Volumes/DevMASTER/!CODING/zz'); rep(False, 'extract into !CODING was ACCEPTED')
    except SystemExit: rep(True, 'ARM: extract into a !CODING dest -> refused before any write')
    try: cgit('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files', ['write-tree']); rep(False, 'plumbing in the shared checkout was ACCEPTED')
    except SystemExit: rep(True, 'ARM: a plumbing write verb against a clone under !CODING (the shared checkout) -> refused before it runs')
    try: state48('main', 'x', 'y', 'z'); rep(False, '--state main was ACCEPTED')
    except SystemExit: rep(True, 'ARM: --state main -> refused')
    try: cfg_hash(os.path.join(tmpd, 'absent-config')); rep(False, 'cfg_hash accepted an absent config')
    except SystemExit: rep(True, 'ARM: cfg_hash refuses an absent / empty config (the EMPTY-string hash e3b0c44298fc1c14 can never be a measurement)')
    # a real scratch repo: make_repo creates a repo whose .githooks exists and whose hooksPath state is as asked; the hash instrument sees a direct change
    r0 = make_repo(os.path.join(tmpd, 'selftest_repo_unset'), None); r1 = make_repo(os.path.join(tmpd, 'selftest_repo_set'), '.githooks')
    rep(sh_git(['-C', r0, 'config', 'core.hooksPath'])[1] == '' and sh_git(['-C', r1, 'config', 'core.hooksPath'])[1] == '.githooks' and os.path.isdir(os.path.join(r0, '.githooks')), 'make_repo: an UNSET repo and an already-`.githooks` repo, both with a .githooks directory')
    h0 = cfg_hash(os.path.join(r0, '.git', 'config')); sh_git(['-C', r0, 'config', 'core.hooksPath', 'zz']); rep(cfg_hash(os.path.join(r0, '.git', 'config')) != h0, 'cfg_hash: a direct config change reads CHANGED (the positive control of the hooks arms)')
    rep(in_repo(r0) and not in_repo(tmpd), 'in_repo: a scratch repo reads inside, the canonical TMPDIR reads outside')
    rc, nb, txt = failed_run_output('#!/bin/sh\necho hello\nexit 3\n', tmpd); rep(rc == 3 and txt.strip() == 'hello' and nb == 6, 'failed_run_output: runs a script under the stub PATH and reads rc and bytes')
    for pr_, T in TAMPER.items():
        ok = all(len(rw) == 5 for rw in T['rows']); rep(ok, '#%s tamper table: %d rows, each (id, name, file/special, edits, predicted reds)' % (pr_, len(T['rows'])))
    rep(len(TAMPER['1448']['rows']) == 11 and len(TAMPER['1447']['rows']) == 7 and len(TAMPER['1449']['rows']) == 8, 'tamper tables are the declared sizes (11 / 7 / 8)')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A: print(__doc__); return 2
    try:
        cmd = A[0]
        if cmd == 'setup': return setup(req(A, '--clone'), req(A, '--head', True), req(A, '--wt'), opt(A, '--log'))
        if cmd in ('sec', 'tsc', 'specregen', 'probe'):
            wt, cl, out = req(A, '--wt'), req(A, '--clone'), req(A, '--out'); bs, hd = req(A, '--base1448', True), req(A, '--head1448', True)
            if cmd == 'sec': return sec_cmd(req(A, '--state'), '--whole' in A, wt, cl, bs, hd, out)
            if cmd == 'tsc': return tsc_cmd(wt, cl, bs, hd, out)
            if cmd == 'specregen': return specregen_cmd(wt, cl, bs, hd, out)
            return probe_cmd(wt, cl, bs, hd, out)
        if cmd == 'tamper':
            pr = req(A, '--pr'); only = (opt(A, '--only') or '').split(',') if opt(A, '--only') else None
            if pr not in TAMPER: raise SystemExit('REFUSED: --pr %r has no tamper table (1447|1448|1449)' % pr)
            if pr == '1448': return tamper48(req(A, '--wt'), req(A, '--clone'), req(A, '--base1448', True), req(A, '--head1448', True), req(A, '--out'), only)
            return tamper_shell(pr, req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), req(A, '--scratch'), req(A, '--out'), only)
        if cmd == 'shells':
            pr = req(A, '--pr')
            if pr not in ('1447', '1449'): raise SystemExit('REFUSED: --pr %r has no shell legs (1447|1449)' % pr)
            return shells_cmd(pr, req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), req(A, '--scratch'), req(A, '--out'))
        if cmd == 'hooks': return hooks_cmd(req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), req(A, '--scratch'), req(A, '--out'))
        if cmd == 'compose': return compose_cmd(req(A, '--clone'), req(A, '--develop', True), heads_of(A), bases_of(A), req(A, '--scratch'), req(A, '--out'))
        if cmd == 'docs': return docs_cmd(req(A, '--clone'), req(A, '--develop', True), heads_of(A), bases_of(A), req(A, '--scratch'), req(A, '--out'))
    except SystemExit as e:
        print(e); return 2
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
