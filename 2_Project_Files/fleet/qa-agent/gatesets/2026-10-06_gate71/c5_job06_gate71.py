#!/usr/bin/env python3
r"""c5_job06_gate71.py — the PRODUCT checks for #1404 (KS-1436, T2): Blockchain/Testing/jobs/06-tenant-isolation.sh, and THE CHAIN
job 06 -> 09 that makes #1404 #1398's MERGE CONDITION (Wednesday ruling Q2). THE HEADS ARE PARAMETERS. Added 2026-10-07 (widening).

Every job-06 run is a REAL `bash jobs/06-tenant-isolation.sh` in a fresh fixture: node, curl and tsx are STUBS on a private PATH (no
stack, no network); the tsx stub REPLAYS the runner's own output shapes (runner.ts:74 `console.error("login failed for <email>: <status>
<body>")`, :150-151 the verifier@ -> holder@ fallback, :262 `console.log(JSON.stringify({tested, findings}, null, 2))`, :155-159 the
both-logins-failed warning, :271 the caught-error JSON). Every 09 run is a REAL `bash jobs/09-aggregate-report.sh` over THAT job's
RUN_DIR (the `.json.stderr` sidecar included). Nothing is written outside --out.

MODES (all: --repo <YOUR clone> --out <a FRESH dir>; `--pr 1404` is implied — this script measures the 1404 row and the chain)
  guard06   G0 base / head blobs == kit;  G1 base -> head is ONE contiguous replacement: the removed line == kit `2>&1` line, the added
            lines == 3 comment lines + the kit `2> "$OUT.stderr"` line;  G2 the comment carries KS-1436 and the prior `2>&1` (skill §5d);
            G3 0 non-comment `2>&1` at the head (CONTROL: base has 1);  G4 the `Writes:` header and both `jq … || echo "?"` swallow
            lines byte-identical (the PR says it deliberately leaves them);  G5 mode 100755 at base and head;  G6 INFO: every tracked
            line that globs or uploads RUN_DIR / audit-runs (the sidecar's consumers).
  suite06   the author's suite run from a MATERIALISED COPY (suite + job blobs written under --out, REPO_ROOT resolves there; no worktree,
            nothing of the author's touched): S1 head 5/0 rc 0;  S2 RED-FIRST with the BASE job blob: rc 1, 1 passed / 4 failed, the
            CONTROL cell 1 green, cells 2-5 red;  S3 ONE RED ARM PER PROPERTY, each a mutated COPY of the head job (anchor x1, tamper
            landed, bash -n rc 0): DEVNULL `2>/dev/null` -> 4/1, only cell 4 ("stderr is kept") red;  WRONGNAME `2> "$OUT.err"` ->
            4/1, only cell 4 red (cell 4 pins the sidecar's NAME);  S4 determinism re-run.
  chain     THE COMPOSED MATRIX: job 06 {BASE 4d077ab, HEAD 6bd87f1} x 09 {BASE 739ebab, #1398 HEAD 22a2479} x 8 runner shapes
            (quiet-clean, fallback-clean, both-logins-fail, runner-error-caught, quiet-leak, fallback-leak, truncated, crash-no-stdout).
            RULES (the ruling's shapes): with BOTH applied a designed fallback run reads CLEAN, a real leak reads the leak finding at
            CRITICAL (>= HIGH), rc 1, and a truncated artefact reads `06-tenant/unreadable-artefact` HIGH, rc 1;  #1398 ALONE turns the
            fallback run into `unreadable-artefact` (the FALSE ALARM Q2 named) — measured, and BOTH must read it CLEAN;  #1404 ALONE
            makes a fallback LEAK visible where BEFORE it read clean;  the sidecar holds exactly the stderr and 09's ids are unchanged
            with it removed (CONTROL);  the job's own summary reads `tested=3 cross-tenant_findings=0` at HEAD, `tested=?` at BASE.
            CONTROL: the BOTH rules applied to the BEFORE column must report violations.  --stack-tree <tree-ish> takes the HEAD 06 and
            the #1398 09 from that tree after asserting both blobs equal the heads' (develop + #1404 + #1398 stacked target).
  reach06   --rev <commit>  Q2's STATIC measurement: every .github/workflows file, its triggers, and whether it reaches job 06 (directly,
            via run-internal-audit.sh, via ci/orchestrate.sh); per-PR = a trigger in kit per_pr_triggers. CONTROLS: >= 1 workflow
            reaches 06 (positive), a fabricated token reaches 0. The by-LOG-LINE half is gh_gate71.py `job06` (it needs GitHub).
  --selftest  the trigger parser, the result classifier, the rules and the arm builders on synthetic input; planted arms must FAIL.
rc 0 pass / 1 FAIL / 2 refused (absent object, bad args)."""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile, time
if '--pr' not in sys.argv: sys.argv += ['--pr', '1404']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate71 import K, P, ROW, Tally, git, git_bytes, refuse_absent, opt

P6 = K['product_1404']; J6 = P6['path']; AGG = K['product']['path']
R1398 = K['rows']['1398']; BASE = P['parents'][0]
UN = '06-tenant/unreadable-artefact'
LEAK_ID = '/api/documents:saw=tenant-b:want=tenant-a'   # 09:171 emits "$endpoint:saw=$observed:want=$expected"; runner.ts sets endpoint = m.path


def blob_sha(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()


# ---------------- guard06 ----------------
def replacement(base_lines, head_lines):
    """(i, removed, added) for ONE contiguous replacement turning base into head, else None."""
    i = 0
    while i < min(len(base_lines), len(head_lines)) and base_lines[i] == head_lines[i]: i += 1
    j = 0
    while j < min(len(base_lines), len(head_lines)) - i and base_lines[-1 - j] == head_lines[-1 - j]: j += 1
    return i, base_lines[i:len(base_lines) - j], head_lines[i:len(head_lines) - j]


def live_2to1(lines):
    """non-comment lines that run the RUNNER with `2>&1` (the file's other `2>&1`, `command -v node >/dev/null 2>&1` at :41, is not one)."""
    return [l for l in lines if '2>&1' in l and '"$RUNNER"' in l and not l.lstrip().startswith('#')]


def guard06(repo, head):
    t = Tally()
    bb, hb = git_bytes(repo, BASE, J6), git_bytes(repo, head, J6)
    t.check('G0', blob_sha(bb) == P6['base_blob'] and blob_sha(hb) == P6['head_blob'], 'base blob %s (kit %s) | head blob %s (kit %s)' % (
        blob_sha(bb)[:12], P6['base_blob'][:12], blob_sha(hb)[:12], P6['head_blob'][:12]))
    BL, HL = bb.decode().split('\n'), hb.decode().split('\n')
    i, rem, add = replacement(BL, HL)
    com = [l for l in add if l.lstrip().startswith('#')]; prod = [l for l in add if not l.lstrip().startswith('#')]
    t.check('G1', rem == [P6['removed_line']] and prod == [P6['added_line']] and len(com) == P6['comment_lines'] and add[-1] == P6['added_line'],
            'ONE contiguous replacement at :%d: removed %r | added %d comment line(s) + %r' % (i + 1, rem, len(com), prod))
    t.check('G2', bool(com) and 'KS-1436' in com[0] and '2>&1' in ' '.join(com), 'the WHY comment carries KS-1436 and names the prior `2>&1` (skill §5d): %r' % (com[:1],))
    t.check('G3', live_2to1(HL) == [] and len(live_2to1(BL)) == 1, 'non-comment runner invocations with `2>&1`: head %d (want 0) | CONTROL base %d (want 1) | every `2>&1` at the head (INFO): %d' % (
        len(live_2to1(HL)), len(live_2to1(BL)), sum(1 for l in HL if '2>&1' in l and not l.lstrip().startswith('#'))))
    keep = [P6['writes_header']] + P6['swallow_lines']
    t.check('G4', all(BL.count(k) == 1 and HL.count(k) == 1 for k in keep), 'the `Writes:` header and both `jq … || echo "?"` swallow lines present once at base AND head (left in place by design)')
    mb = git(repo, 'ls-tree', BASE, '--', J6).split()[0]; mh = git(repo, 'ls-tree', head, '--', J6).split()[0]
    t.check('G5', mb == mh == '100755', 'mode base %s head %s (want 100755 both)' % (mb, mh))
    rc, o, e = git(repo, 'grep', '-n', '-E', r'RUN_DIR/\*|RUN_DIR"/\*|audit-runs/latest|\*\.json\b', head, '--', 'Blockchain/Testing', '.github', check=False)
    hits = [l for l in o.split('\n') if l]
    t.info('G6', 'lines that glob / upload the run dir (the sidecar `%s` is a NEW file there): %d %s' % (P6['sidecar'], len(hits), [h.split(':', 2)[1] + ':' + h.split(':', 2)[2][:40] for h in hits][:6]))
    return t.end()


# ---------------- fixtures ----------------
def runner_out(shape):
    """(stdout, stderr) the tsx stub replays, per runner.ts."""
    t3 = [{'endpoint': '/api/documents', 'method': 'GET', 'expected_status': 403, 'actual_status': 403, 'outcome': 'pass'},
          {'endpoint': '/api/anchors', 'method': 'GET', 'expected_status': 403, 'actual_status': 403, 'outcome': 'pass'},
          {'endpoint': '/api/webhooks', 'method': 'GET', 'expected_status': 403, 'actual_status': 403, 'outcome': 'pass'}]
    leak = [{'endpoint': '/api/documents', 'method': 'GET', 'observed_tenant': 'tenant-b', 'expected_tenant': 'tenant-a',
             'detail': "Principal-B successfully GET'd on principal-A's document"}]
    v = P6['runner_stderr_line'] + '\n'; h = v.replace('verifier@', 'holder@')
    pretty = lambda f: json.dumps({'tested': t3, 'findings': f}, indent=2) + '\n'
    return {'quiet-clean': (pretty([]), ''), 'fallback-clean': (pretty([]), v), 'quiet-leak': (pretty(leak), ''), 'fallback-leak': (pretty(leak), v),
            'both-logins-fail': (json.dumps({'warning': 'second principal login failed — only role-isolation could not be tested', 'tested': t3, 'findings': []}) + '\n', v + h),
            'runner-error-caught': (json.dumps({'error': 'TypeError: fetch failed', 'tested': [], 'findings': []}) + '\n', ''),
            'truncated': ('{\n  "tested": [\n    {\n      "endpoint": "/api/doc', 'Killed: 9\n'),
            'crash-no-stdout': ('', 'node:internal/modules/run_main:123\n  triggerUncaughtException(\n')}[shape]


SHAPES = ['quiet-clean', 'fallback-clean', 'both-logins-fail', 'runner-error-caught', 'quiet-leak', 'fallback-leak', 'truncated', 'crash-no-stdout']


def run_job06(job_bytes, shape, root):
    os.makedirs(os.path.join(root, 'Testing', 'jobs')); os.makedirs(os.path.join(root, 'Testing', 'tests', 'tenant-isolation'))
    os.makedirs(os.path.join(root, 'bin')); run = os.path.join(root, 'runs', '2026-10-07_fixture'); os.makedirs(run)
    jp = os.path.join(root, 'Testing', 'jobs', '06-tenant-isolation.sh'); open(jp, 'wb').write(job_bytes); os.chmod(jp, 0o755)
    open(os.path.join(root, 'Testing', 'tests', 'tenant-isolation', 'runner.ts'), 'w').write('// fixture: the tsx stub replays runner.ts output\n')
    so, se = runner_out(shape)
    open(os.path.join(root, 'stub_stdout'), 'w').write(so); open(os.path.join(root, 'stub_stderr'), 'w').write(se)
    for n in ('node', 'curl'):
        open(os.path.join(root, 'bin', n), 'w').write('#!/bin/bash\nexit 0\n')
    # ORDER IS THE RUNNER'S: login() runs (and console.error fires, :74) BEFORE the final console.log (:262), so stderr is written FIRST;
    # a mid-write abort / crash writes its stderr AFTER whatever stdout got out. (Drafter's ex1 wrote stdout first for every shape: wrong
    # for the fallback shapes, and it made BASE read the leak through jq's first value — superseded, KIT_REPORT WIDENED §defects.)
    first_err = shape not in ('truncated', 'crash-no-stdout')
    body = ('cat "%s/stub_stderr" >&2\ncat "%s/stub_stdout"\n' if first_err else 'cat "%s/stub_stdout"\ncat "%s/stub_stderr" >&2\n') % (root, root)
    open(os.path.join(root, 'bin', 'tsx'), 'w').write('#!/bin/bash\n' + body + 'exit 0\n')
    for n in ('node', 'curl', 'tsx'): os.chmod(os.path.join(root, 'bin', n), 0o755)
    env = dict(os.environ, PATH=os.path.join(root, 'bin') + ':/usr/bin:/bin', SELF=os.path.join(root, 'Testing'), RUN_DIR=run, TARGET_BASE='http://fixture.invalid')
    p = subprocess.run(['bash', 'jobs/06-tenant-isolation.sh'], cwd=os.path.join(root, 'Testing'), env=env, capture_output=True)
    out = p.stdout.decode('utf-8', 'replace') + p.stderr.decode('utf-8', 'replace')
    open(os.path.join(root, 'job06.out'), 'w').write(out); open(os.path.join(root, 'job06.rc'), 'w').write('%d\n' % p.returncode)
    return p.returncode, out, run


def run_09(agg_bytes, root, run):
    jp = os.path.join(root, 'Testing', 'jobs', '09-aggregate-report.sh'); open(jp, 'wb').write(agg_bytes); os.chmod(jp, 0o755)
    env = dict(os.environ, TARGET_BASE='fixture', RUN_DIR=run, SELF=os.path.join(root, 'Testing'), FAIL_ON='high', AUDIT_RUNS_DIR=os.path.join(root, 'runs'))
    with open(os.path.join(root, 'agg09.out'), 'wb') as fo:
        rc = subprocess.run(['bash', 'jobs/09-aggregate-report.sh'], cwd=os.path.join(root, 'Testing'), env=env, stdout=fo, stderr=subprocess.STDOUT).returncode
    open(os.path.join(root, 'agg09.rc'), 'w').write('%d\n' % rc)
    try: rep = json.load(open(os.path.join(run, 'REPORT.json')))
    except (OSError, ValueError): return {'rc': rc, 'ids': None, 'sev': None}
    return {'rc': rc, 'ids': sorted(f['id'] for f in rep['findings']), 'sev': sorted((f['id'], f['severity']) for f in rep['findings'])}


def classify(r):
    if r['ids'] is None: return 'NO-REPORT'
    if r['ids'] == [] and r['rc'] == 0: return 'CLEAN'
    if r['ids'] == [LEAK_ID] and r['sev'] == [(LEAK_ID, P6['agg_06_severity'])] and r['rc'] == 1: return 'LEAK'
    if r['ids'] == [UN] and r['sev'] == [(UN, 'high')] and r['rc'] == 1: return 'UNREADABLE'
    return 'OTHER %s rc %s' % (r['sev'], r['rc'])


# the expected class per (06 side, 09 side) — BOTH is the ruling; the others are what each PR alone does, MEASURED and stated
EXPECT = {('head', '1398'): {'quiet-clean': 'CLEAN', 'fallback-clean': 'CLEAN', 'both-logins-fail': 'CLEAN', 'runner-error-caught': 'CLEAN',
                             'quiet-leak': 'LEAK', 'fallback-leak': 'LEAK', 'truncated': 'UNREADABLE', 'crash-no-stdout': 'UNREADABLE'},
          ('head', 'base'): {'quiet-clean': 'CLEAN', 'fallback-clean': 'CLEAN', 'both-logins-fail': 'CLEAN', 'runner-error-caught': 'CLEAN',
                             'quiet-leak': 'LEAK', 'fallback-leak': 'LEAK', 'truncated': 'CLEAN', 'crash-no-stdout': 'CLEAN'},
          ('base', '1398'): {'quiet-clean': 'CLEAN', 'fallback-clean': 'UNREADABLE', 'both-logins-fail': 'UNREADABLE', 'runner-error-caught': 'CLEAN',
                             'quiet-leak': 'LEAK', 'fallback-leak': 'UNREADABLE', 'truncated': 'UNREADABLE', 'crash-no-stdout': 'UNREADABLE'},
          ('base', 'base'): {'quiet-clean': 'CLEAN', 'fallback-clean': 'CLEAN', 'both-logins-fail': 'CLEAN', 'runner-error-caught': 'CLEAN',
                             'quiet-leak': 'LEAK', 'fallback-leak': 'CLEAN', 'truncated': 'CLEAN', 'crash-no-stdout': 'CLEAN'}}
NOTE = {('base', 'base', 'fallback-leak'): 'BEFORE: a REAL LEAK READ CLEAN (the original silence)',
        ('base', '1398', 'fallback-clean'): '#1398 ALONE: the FALSE ALARM Q2 named (a legitimate run reds, cause text false)',
        ('base', '1398', 'fallback-leak'): '#1398 ALONE: a true alarm, but the leak id is NOT emitted (cause text false)',
        ('head', 'base', 'truncated'): '#1404 ALONE: a truncated artefact still reads clean (that is #1398\'s fix, not this one)',
        ('head', '1398', 'fallback-clean'): 'BOTH: the fallback run reads CLEAN (the false alarm is gone)'}


def chain(repo, h04, h98, out, stack):
    t = Tally()
    j = {'base': git_bytes(repo, BASE, J6), 'head': git_bytes(repo, h04, J6)}
    a = {'base': git_bytes(repo, BASE, AGG), '1398': git_bytes(repo, h98, AGG)}
    t.check('CH0', blob_sha(j['base']) == P6['base_blob'] and blob_sha(j['head']) == P6['head_blob'] and blob_sha(a['base']) == K['product']['base_blob']
            and blob_sha(a['1398']) == K['product']['head_blob'], 'blobs: 06 base %s head %s | 09 base %s #1398 %s (== kit)' % (
                blob_sha(j['base'])[:12], blob_sha(j['head'])[:12], blob_sha(a['base'])[:12], blob_sha(a['1398'])[:12]))
    if stack:
        s6, s9 = git_bytes(repo, stack, J6), git_bytes(repo, stack, AGG)
        ok = s6 == j['head'] and s9 == a['1398']
        t.check('CH0s', ok, 'STACKED TREE %s: its 06 == #1404 06 %s, its 09 == #1398 09 %s -> the BOTH column runs the stacked tree\'s blobs' % (stack[:12], s6 == j['head'], s9 == a['1398']))
        if not ok: return t.end()
        j['head'], a['1398'] = s6, s9
    grid = {}; viol_before = 0
    for shape in SHAPES:
        for js in ('base', 'head'):
            root = tempfile.mkdtemp(prefix='06%s.%s.' % (js, shape), dir=out)
            jrc, jout, run = run_job06(j[js], shape, root)
            snap = {f: open(os.path.join(run, f), 'rb').read() for f in sorted(os.listdir(run))}
            for asd in ('base', '1398'):
                r2 = os.path.join(root, 'agg_' + asd); shutil.copytree(os.path.join(root, 'Testing'), os.path.join(r2, 'Testing'))
                run2 = os.path.join(r2, 'runs', '2026-10-07_fixture'); os.makedirs(run2)
                for f, b in snap.items(): open(os.path.join(run2, f), 'wb').write(b)
                res = run_09(a[asd], r2, run2); cls = classify(res)
                grid[(js, asd, shape)] = (cls, res, jrc, jout, sorted(snap))
                want = EXPECT[(js, asd)][shape]
                t.check('CH-%s-%s-%s' % (js, asd, shape), cls == want and jrc == 0, '06 %-4s x 09 %-4s %-19s -> %-10s (want %-10s) job rc %d | artefact files %s%s' % (
                    js, asd, shape, cls, want, jrc, sorted(snap), (' | ' + NOTE[(js, asd, shape)]) if (js, asd, shape) in NOTE else ''))
            if js == 'base' and EXPECT[('head', '1398')][shape] != grid[('base', 'base', shape)][0]: viol_before += 1
    # the sidecar: holds exactly the stderr, and 09 ignores it
    root = tempfile.mkdtemp(prefix='sidecar.', dir=out); jrc, jout, run = run_job06(j['head'], 'fallback-leak', root)
    sc = os.path.join(run, P6['sidecar']); side = open(sc).read() if os.path.exists(sc) else None
    with_sc = run_09(a['1398'], root, run)
    root2 = tempfile.mkdtemp(prefix='sidecar_removed.', dir=out); shutil.copytree(os.path.join(root, 'Testing'), os.path.join(root2, 'Testing'))
    run2 = os.path.join(root2, 'runs', '2026-10-07_fixture'); os.makedirs(run2)
    shutil.copy(os.path.join(run, '06-tenant-isolation.json'), run2)
    without = run_09(a['1398'], root2, run2)
    t.check('CH-SIDECAR', side == runner_out('fallback-leak')[1] and with_sc['ids'] == without['ids'] == [LEAK_ID],
            'sidecar %s holds exactly the runner stderr: %s | 09 ids WITH the sidecar %s == WITHOUT it %s (CONTROL: removing it changes nothing)' % (
                P6['sidecar'], side == runner_out('fallback-leak')[1], with_sc['ids'], without['ids']))
    hs = grid[('head', 'base', 'fallback-clean')][3]; bs = grid[('base', 'base', 'fallback-clean')][3]
    t.check('CH-SUMMARY', 'tested=3 cross-tenant_findings=0' in hs and 'tested=? cross-tenant_findings=?' in bs,
            'job 06 summary on a fallback run: HEAD %r | BASE %r' % (hs.strip()[-40:], bs.strip()[-40:]))
    t.check('CH-CONTROL', viol_before > 0, 'the BOTH rules applied to the BEFORE column (06 base x 09 base) report %d violation(s) (> 0: the matrix discriminates)' % viol_before)
    json.dump([{'job06': js, 'agg09': asd, 'shape': sh, 'class': v[0], 'agg': v[1], 'job_rc': v[2], 'files': v[4]} for (js, asd, sh), v in sorted(grid.items())],
              open(os.path.join(out, 'chain.json'), 'w'), indent=1)
    print('CHAIN MATRIX written: %s (%d cells)' % (os.path.join(out, 'chain.json'), len(grid)))
    return t.end()


# ---------------- suite06 ----------------
def mutate(src, old, new, label):
    s = src.decode(); n = s.count(old)
    if n != 1: raise SystemExit('ARM %s: anchor %r found %d time(s) (want 1) — refusing to tamper' % (label, old, n))
    m = s.replace(old, new, 1).encode()
    if blob_sha(m) == blob_sha(src): raise SystemExit('ARM %s: tamper did NOT land' % label)
    return m


def run_suite06(suite_bytes, job_bytes, out, tag):
    root = os.path.join(out, 'mini_' + tag)
    sp = os.path.join(root, P6['suite']); jp = os.path.join(root, J6)
    os.makedirs(os.path.dirname(sp)); os.makedirs(os.path.dirname(jp))
    open(sp, 'wb').write(suite_bytes); open(jp, 'wb').write(job_bytes); os.chmod(jp, 0o755)
    n = subprocess.run(['bash', '-n', jp], capture_output=True).returncode
    tmp = os.path.join(out, 'tmp'); os.makedirs(tmp, exist_ok=True)
    t0 = time.time(); p = subprocess.run(['bash', sp], env=dict(os.environ, TMPDIR=tmp), capture_output=True)
    o = p.stdout.decode('utf-8', 'replace') + p.stderr.decode('utf-8', 'replace')
    open(os.path.join(out, 'suite06_%s.out' % tag), 'w').write(o); open(os.path.join(out, 'suite06_%s.rc' % tag), 'w').write('%d\n' % p.returncode)
    m = re.search(r'^\s*(\d+) passed, (\d+) failed\s*$', o, re.M)
    cells = re.findall(r'^  (ok|FAIL) ', o, re.M)
    return n, p.returncode, (int(m.group(1)), int(m.group(2))) if m else None, [i + 1 for i, c in enumerate(cells) if c == 'FAIL'], time.time() - t0


def suite06(repo, head, out):
    t = Tally()
    sb = git_bytes(repo, head, P6['suite']); hb = git_bytes(repo, head, J6); bb = git_bytes(repo, BASE, J6)
    t.check('S0', blob_sha(sb) == P6['suite_blob'], 'suite blob %s == kit %s' % (blob_sha(sb)[:12], P6['suite_blob'][:12]))
    n, rc, pf, red, dt = run_suite06(sb, hb, out, 'head')
    t.check('S1', n == 0 and rc == 0 and pf == (5, 0), 'suite at the head (materialised copy): bash -n %d, rc %d, %s, %.2f s (author: 5/0 rc 0)' % (n, rc, pf, dt))
    n, rc, pf, red, dt = run_suite06(sb, bb, out, 'redfirst')
    t.check('S2', rc == 1 and pf == (1, 4) and red == [2, 3, 4, 5], 'RED-FIRST on the BASE job blob %s: rc %d, %s, red cells %s (want rc 1, 1/4, CONTROL cell 1 green, cells [2, 3, 4, 5])' % (blob_sha(bb)[:12], rc, pf, red))
    for lab, new, what in (('DEVNULL', '2>/dev/null', 'stderr DISCARDED'), ('WRONGNAME', '2> "$OUT.err"', 'stderr kept under ANOTHER name')):
        m = mutate(hb, '2> "$OUT.stderr"', new, lab)
        n, rc, pf, red, dt = run_suite06(sb, m, out, 'arm' + lab)
        t.check('S3-%s' % lab, n == 0 and rc == 1 and pf == (4, 1) and red == [4], 'ARM %s (%s): anchor x1, landed (sha %s), bash -n %d, rc %d %s red cells %s (want 4/1, only cell 4)' % (lab, what, blob_sha(m)[:12], n, rc, pf, red))
    n, rc, pf, red, dt = run_suite06(sb, hb, out, 'head2')
    t.check('S4', rc == 0 and pf == (5, 0), 'second run at the head agrees: rc %d %s' % (rc, pf))
    return t.end()


# ---------------- reach06 ----------------
def triggers(text):
    """the workflow's `on:` trigger names (block form, list form or scalar form)."""
    L = text.split('\n')
    for i, l in enumerate(L):
        m = re.match(r'^(on|"on"|\'on\'):\s*(.*)$', l)
        if not m: continue
        rest = re.sub(r'\s+#.*$', '', m.group(2)).strip()
        if rest.startswith('['): return [x.strip().strip('"\'') for x in rest.strip('[]').split(',') if x.strip()]
        if rest: return [rest.strip('"\'')]
        out = []
        for l2 in L[i + 1:]:
            if l2.strip() == '' or l2.lstrip().startswith('#'): continue
            if not l2.startswith(' '): break
            mm = re.match(r'^  ([A-Za-z_]+):', l2)
            if mm: out.append(mm.group(1))
        return out
    return []


def reach06(repo, rev):
    t = Tally(); pr_trig = set(P6['per_pr_triggers'])
    files = [l for l in git(repo, 'ls-tree', '-r', '--name-only', rev, '--', '.github/workflows').split('\n') if l.endswith(('.yml', '.yaml'))]
    reach = {}
    for f in files:
        txt = git(repo, 'show', '%s:%s' % (rev, f))
        live = '\n'.join(l for l in txt.split('\n') if not l.lstrip().startswith('#'))
        how = [tok for tok in P6['reach_tokens'] if tok in live]
        tr = triggers(txt)
        if how: reach[f] = (how, tr)
        print('WORKFLOW %-48s triggers %-40s reaches-06-via %s' % (f, ','.join(tr), how or '-'))
    fab = [f for f in files if 'GATE71-FABRICATED-REACH-q7' in git(repo, 'show', '%s:%s' % (rev, f))]
    t.check('R0', len(files) > 0 and fab == [], '%d workflow files read at %s | fabricated token in %d (CONTROL 0)' % (len(files), rev[:12], len(fab)))
    t.check('R1', len(reach) >= 1, 'POSITIVE CONTROL: %d workflow(s) reach job 06 (%s)' % (len(reach), sorted(reach)))
    perpr = {f: sorted(set(tr) & pr_trig) for f, (h, tr) in reach.items() if set(tr) & pr_trig}
    t.check('R2', not perpr, 'workflows that reach job 06 AND carry a per-PR trigger %s: %s (want none)' % (sorted(pr_trig), perpr or 'none'))
    ria = git(repo, 'show', '%s:Blockchain/Testing/run-internal-audit.sh' % rev); orc = git(repo, 'show', '%s:Blockchain/Testing/ci/orchestrate.sh' % rev)
    t.info('R3', 'run-internal-audit.sh globs jobs/[0-9][0-9]-*.sh (06 included): %s | ci/orchestrate.sh names 06-tenant-isolation: %s — both are reached only from the workflows above' % (
        'jobs/[0-9][0-9]-*.sh' in ria, '06-tenant-isolation' in orc))
    return t.end()


# ---------------- selftest ----------------
def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    rep(triggers('name: x\non:\n  workflow_dispatch:\n    inputs: {}\njobs: {}\n') == ['workflow_dispatch'], 'triggers: block form')
    rep(triggers('on: [push, pull_request]\n') == ['push', 'pull_request'] and triggers('on: pull_request\n') == ['pull_request'], 'triggers: list and scalar forms')
    rep(triggers('on:\n  # schedule:\n  #   - cron: x\n  workflow_dispatch:\n') == ['workflow_dispatch'], 'triggers: a commented-out schedule is NOT a trigger')
    rep(set(triggers('on:\n  pull_request:\n    branches: [develop]\n  workflow_dispatch:\n')) & set(P6['per_pr_triggers']) == {'pull_request'}, 'PLANTED pull_request trigger is seen as per-PR')
    z = {'rc': 0, 'ids': [], 'sev': []}; u = {'rc': 1, 'ids': [UN], 'sev': [(UN, 'high')]}; lk = {'rc': 1, 'ids': [LEAK_ID], 'sev': [(LEAK_ID, 'critical')]}
    rep(classify(z) == 'CLEAN' and classify(u) == 'UNREADABLE' and classify(lk) == 'LEAK', 'classify: CLEAN / UNREADABLE / LEAK')
    rep(classify({'rc': 0, 'ids': [UN], 'sev': [(UN, 'high')]}).startswith('OTHER'), 'PLANTED unreadable id with rc 0: OTHER (never CLEAN, never UNREADABLE)')
    rep(classify({'rc': 1, 'ids': [LEAK_ID, UN], 'sev': [(LEAK_ID, 'critical'), (UN, 'high')]}).startswith('OTHER'), 'PLANTED leak + unreadable together: OTHER')
    rep(EXPECT[('head', '1398')]['fallback-clean'] == 'CLEAN' and EXPECT[('base', '1398')]['fallback-clean'] == 'UNREADABLE', 'the rules encode Q2: fallback CLEAN with BOTH, the false alarm with #1398 alone')
    rep(sorted(s for s in SHAPES if EXPECT[('head', '1398')][s] != EXPECT[('base', 'base')][s]) == ['crash-no-stdout', 'fallback-leak', 'truncated'], 'the BOTH rules differ from BEFORE on exactly 3 shapes (fallback-leak, truncated, crash-no-stdout): the CH-CONTROL can fire')
    rep(replacement(['a', 'x', 'b'], ['a', 'c1', 'y', 'b']) == (1, ['x'], ['c1', 'y']), 'replacement: one contiguous span')
    rep(live_2to1(['# "$RUNNER" was 2>&1', '"$RUNNER" > o 2>&1', 'command -v node >/dev/null 2>&1']) == ['"$RUNNER" > o 2>&1'], 'a `2>&1` in a COMMENT, or on a non-runner line, is not a runner `2>&1`')
    try: mutate(b'a 2> "$OUT.stderr" b 2> "$OUT.stderr"', '2> "$OUT.stderr"', 'x', 'T'); rep(False, 'non-unique anchor must refuse')
    except SystemExit: rep(True, 'PLANTED non-unique anchor REFUSES the tamper')
    so, se = runner_out('fallback-clean')
    rep(json.loads(so)['findings'] == [] and se.startswith('login failed for verifier@'), 'the stub replays runner.ts:262 JSON on stdout and :74 on stderr')
    try: json.loads(runner_out('truncated')[0]); rep(False, 'truncated must not parse')
    except ValueError: rep(True, 'the truncated shape does not parse (control for UNREADABLE)')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A or A[0] not in ('guard06', 'suite06', 'chain', 'reach06') or not opt(A, '--repo'): print(__doc__); return 2
    if ROW != '1404': print('REFUSED: c5 measures the 1404 row (and the chain); got --pr %s' % ROW); return 2
    repo = opt(A, '--repo'); h04 = opt(A, '--head', P['head_expected']); h98 = opt(A, '--head-1398', R1398['head_expected'])
    named = [('head 1404', h04), ('base', BASE), ('head 1398', h98)]
    if opt(A, '--rev'): named.append(('rev', opt(A, '--rev')))
    rr = refuse_absent(repo, named)
    if rr: return rr
    print('C5 %s row #1404 head %s | #1398 head %s | repo %s' % (A[0], h04, h98, repo))
    if A[0] == 'guard06': return guard06(repo, h04)
    if A[0] == 'reach06':
        if not opt(A, '--rev'): print('REFUSED: reach06 needs --rev <commit>'); return 2
        return reach06(repo, opt(A, '--rev'))
    out = opt(A, '--out')
    if not out: print('REFUSED: --out <a fresh dir of yours> is required'); return 2
    os.makedirs(out, exist_ok=True)
    if os.listdir(out): print('REFUSED: --out %s is not empty (use a FRESH dir; never clean one)' % out); return 2
    if A[0] == 'suite06': return suite06(repo, h04, out)
    return chain(repo, h04, h98, out, opt(A, '--stack-tree'))


if __name__ == '__main__':
    sys.exit(main())
