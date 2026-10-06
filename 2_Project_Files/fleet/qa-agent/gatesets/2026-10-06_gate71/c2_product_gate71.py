#!/usr/bin/env python3
r"""c2_product_gate71.py — the PRODUCT checks for #1398 (KS-1136): Blockchain/Testing/jobs/09-aggregate-report.sh. THE HEAD IS A PARAMETER.
Every aggregator run is a REAL `bash jobs/09-aggregate-report.sh` from a fresh fixture `Testing/` tree, exactly as run-internal-audit.sh:119-121
and both suites call it (TARGET_BASE RUN_DIR SELF FAIL_ON=high AUDIT_RUNS_DIR exported, cwd $SELF). Nothing is written outside --out.

MODES (all: --repo <YOUR clone> --head <40-hex> --out <a FRESH dir of yours>)
  guard     G1 head minus ONE contiguous 14-line span == the base blob line for line (a pure insertion);  G2 the span sits after
            `is_baselined() {`'s block and before `ALL_FINDINGS=$(jq '.' "$TMP")`;  G3 the loop's 7 names == kit == every
            `[ -f "$RUN_DIR/<x>.json" ]` block in the file minus 04, and each job id == the FIRST `emit "<id>"` of that block;
            G4 the guard line exactly once, TWO conjuncts;  G5 04's block byte-identical base vs head (KS-878's guard untouched).
  suite     --wt <a worktree AT THE HEAD>  S1 the new suite at the head: rc 0, 6 passed;  S2 RED-FIRST: AGG_SH = the BASE blob
            (extracted, git-blob-hash asserted == 739ebab) -> rc 1, EXACTLY cells 1-3 FAIL, controls 4-6 ok;  S3 ONE RED ARM PER
            CONJUNCT, each a mutated COPY of the head blob (anchor count 1 asserted, tamper LANDED asserted, `bash -n` rc 0 first):
            A drops `[ -f "$_f" ] && ` -> 2 passed / 4 failed;  B drops ` && ! jq -e . "$_f" >/dev/null 2>&1` -> 4 passed / 2 failed;
            S4 extra discriminating arms: C 08 dropped from the loop -> cells 2+3 red;  D the loop MOVED below ALL_FINDINGS -> cells 1-3
            red (red-proves the placement sentence "it runs before ALL_FINDINGS reads $TMP");  S5 the suite's own AGG_SH="" refusal rc 2;
            S6 a second run of S1 agrees (determinism).
  shapes    THE LEGITIMATE-SHAPES MATRIX (BRIEF_TEMPLATE §2a): for each of the 7 loop jobs x every shape, BASE blob vs HEAD blob, fresh fixture
            each. CLEAN shapes (absent, valid-zero, the job's own SKIP/error JSON, two concatenated valid values) must read the SAME at head
            as at base: 0 findings, rc 0. FINDINGS (valid with findings) must emit the job's own finding(s) at head == base and NO
            unreadable id. UNREADABLE shapes (0-byte, whitespace, truncated, valid+trailing garbage, JSON null, JSON false, mode 000; for 06
            also the runner's stderr merged into the artefact, clean and carrying a leak) must emit EXACTLY ONE `<job>/unreadable-artefact`
            HIGH at head, plus whatever the base already emitted, rc 1 — and the BASE column says what it did BEFORE (a 0-finding rc 0 there
            is the clean-scan silence). Also: 04 truncated (exactly once, base == head), all-7 truncated, all-7 with findings, and the
            REPEAT shape (the same truncated artefact on two consecutive runs: run 2's NEW set, rc, totals.high, REPORT.md). CONTROL: the
            head rules applied to the BASE column must report violations (else the matrix cannot discriminate).
  callers   --wt <head worktree> [optional]  every tracked file naming a consumer token (git grep, at the head), classified EXECUTES-09 /
            CALLS-RUNNER / READS-REPORT / DOC; the set of EXECUTING callers == kit consumers_expected; positive control (09 names itself)
            and a fabricated-token control (0). With --wt: the trivy suite run against the head blob AND the base blob (head minus the loop):
            equal results = it never reaches the new loop (its negatives are untouched, and it is not coverage for this change).
  --selftest  the shape-rule evaluator, the guard parser and the arm builders on synthetic input. Planted arms must FAIL.
rc 0 pass / 1 FAIL / 2 refused (absent object, bad args)."""
import hashlib, json, os, re, shutil, stat, subprocess, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate71 import K, P, Tally, git, git_bytes, refuse_absent, opt

PR = K['product']; PATH = PR['path']; JOBS = PR['loop_jobs']
TS = 'runs/2026-10-05_fixture'


def blob_sha(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()


# ---------------- guard ----------------
def insertion_span(base_lines, head_lines):
    """(start, length) of the ONE contiguous span whose removal makes head == base, else None."""
    n = len(head_lines) - len(base_lines)
    if n <= 0: return None
    i = 0
    while i < len(base_lines) and base_lines[i] == head_lines[i]: i += 1
    return (i, n) if head_lines[:i] + head_lines[i + n:] == base_lines else None


def blocks_by_artefact(text):
    """{artefact: first emit job id} for every `if [ -f "$RUN_DIR/<x>.json" ]` block."""
    L = text.split('\n'); out = {}
    for i, l in enumerate(L):
        m = re.match(r'^if \[ -f "\$RUN_DIR/([0-9a-z-]+)\.json" \]; then$', l)
        if not m: continue
        for j in range(i + 1, min(i + 80, len(L))):
            e = re.search(r'\bemit "([0-9A-Za-z_-]+)"', L[j])
            if e: out[m.group(1)] = e.group(1); break
            if L[j] == 'fi': out[m.group(1)] = None; break
    return out


def loop_names(span_text):
    m = re.search(r'for _art in (.*?); do', span_text, re.S)
    if not m: return None
    return dict(tok.split(':', 1) for tok in m.group(1).replace('\\\n', ' ').split())


def block_text(text, art):
    L = text.split('\n'); s = [i for i, l in enumerate(L) if l == 'if [ -f "$RUN_DIR/%s.json" ]; then' % art]
    if len(s) != 1: return None
    e = s[0]
    while e < len(L) and L[e] != 'fi': e += 1
    return '\n'.join(L[s[0]:e + 1])


def guard(repo, head):
    t = Tally(); base = P['parents'][0]
    bb, hb = git_bytes(repo, base, PATH), git_bytes(repo, head, PATH)
    t.check('G0', blob_sha(bb) == PR['base_blob'], 'base blob %s == kit %s | head blob %s (kit %s)' % (blob_sha(bb)[:12], PR['base_blob'][:12], blob_sha(hb)[:12], PR['head_blob'][:12]))
    BL, HL = bb.decode().split('\n'), hb.decode().split('\n')
    sp = insertion_span(BL, HL)
    t.check('G1', sp is not None and sp[1] == 14, 'head minus ONE contiguous span == base: %s (want 14 lines)' % (('lines %d-%d (%d lines)' % (sp[0] + 1, sp[0] + sp[1], sp[1])) if sp else 'NOT a pure insertion'))
    if not sp: return t.end()
    span = '\n'.join(HL[sp[0]:sp[0] + sp[1]])
    ib = [i for i, l in enumerate(HL) if l.startswith(PR['anchor_before'])]; ia = [i for i, l in enumerate(HL) if l.startswith(PR['anchor_after'])]
    t.check('G2', len(ib) == 1 and len(ia) == 1 and ib[0] < sp[0] and sp[0] + sp[1] <= ia[0],
            '`%s` at :%s, span :%d-:%d, `ALL_FINDINGS=` at :%s — after the baseline helper, BEFORE ALL_FINDINGS reads $TMP' % (
                PR['anchor_before'], [x + 1 for x in ib], sp[0] + 1, sp[0] + sp[1], [x + 1 for x in ia]))
    names = loop_names(span); blocks = blocks_by_artefact(hb.decode())
    expect_from_file = {a: j for a, j in blocks.items() if a not in PR['guarded_elsewhere']}
    t.check('G3', names == JOBS == expect_from_file, 'loop %s | kit %s | file blocks minus 04 %s' % (
        sorted((names or {}).items()) == sorted(JOBS.items()), sorted(JOBS.items()) == sorted(expect_from_file.items()), sorted(expect_from_file.items())))
    gl = [l for l in HL if l == PR['guard_line']]
    t.check('G4', len(gl) == 1 and gl[0].count('&&') == 1 and PR['conjunct_A'] in gl[0] and PR['conjunct_B'] in gl[0],
            'guard line present %d time(s); conjuncts `[ -f "$_f" ]` and `! jq -e . "$_f"` (two, joined by one &&)' % len(gl))
    t.check('G5', block_text(bb.decode(), '04-container-trivy') == block_text(hb.decode(), '04-container-trivy') is not None,
            "04's block (KS-676 + KS-878) byte-identical base vs head")
    t.info('G6', 'the emitted description is %r — note it asserts a CAUSE ("aborted mid-write") the aggregator does not observe (06 stderr, 000 mode, JSON null are other causes)'
           % re.search(r'"\$\{_art%%:\*\}\.json ([^"]+)"', span).group(1))
    return t.end()


# ---------------- running the real aggregator ----------------
def write_art(run, name, spec):
    p = os.path.join(run, name + '.json')
    if spec is None: return
    if isinstance(spec, tuple) and spec[0] == 'mode000':
        open(p, 'wb').write(spec[1]); os.chmod(p, 0); return
    open(p, 'wb').write(spec)


def run_agg(agg_bytes, arts, root, reuse=False):
    """arts: {artefact basename: bytes | None | ('mode000', bytes)}. Returns dict(rc, findings, ids, high_total, new, md_new_none)."""
    run = os.path.join(root, TS)
    if not reuse:
        os.makedirs(os.path.join(root, 'Testing', 'jobs')); os.makedirs(run)
        open(os.path.join(root, 'Testing', 'jobs', '09-aggregate-report.sh'), 'wb').write(agg_bytes)
    for n, s in arts.items(): write_art(run, n, s)
    env = dict(os.environ, TARGET_BASE='fixture', RUN_DIR=run, SELF=os.path.join(root, 'Testing'), FAIL_ON='high', AUDIT_RUNS_DIR=os.path.join(root, 'runs'))
    with open(os.path.join(root, 'out.txt'), 'wb') as fo:
        rc = subprocess.run(['bash', 'jobs/09-aggregate-report.sh'], cwd=os.path.join(root, 'Testing'), env=env, stdout=fo, stderr=subprocess.STDOUT).returncode
    for n, s in arts.items():
        if isinstance(s, tuple): os.chmod(os.path.join(run, n + '.json'), stat.S_IRUSR | stat.S_IWUSR)
    try:
        rep = json.load(open(os.path.join(run, 'REPORT.json')))
    except (OSError, ValueError):
        return {'rc': rc, 'ids': None, 'findings': None, 'high_total': None, 'new': None, 'md_new_none': None}
    md = open(os.path.join(run, 'REPORT.md'), encoding='utf-8').read()
    return {'rc': rc, 'findings': [(f['job'], f['severity'], f['id']) for f in rep['findings']], 'ids': sorted(f['id'] for f in rep['findings']),
            'high_total': rep['totals']['high'], 'new': sorted(f['id'] for f in rep['new_since_prev']),
            'md_new_none': '## NEW findings since last run\n\n_None._' in md}


VALID_ZERO = {'01-dependency-audit': b'{"runs":[]}\n', '07-license-compliance': b'{"runs":[]}\n', '05-dast-zap': b'{"alerts":[]}\n',
              '08-aiken-tests': b'{"tests":{"passed":10,"failed":0}}\n', '02-secret-scan': b'{"findings":[]}\n', '03-sast-semgrep': b'{"findings":[]}\n',
              '06-tenant-isolation': b'{"findings":[]}\n'}
# the job's OWN skip / error shape, copied from each job script at the head (a SKIP reads clean today — KS-676 class, not this PR)
SKIP = {'01-dependency-audit': b'{"error":"repo not found at /x"}\n', '02-secret-scan': b'{"error":"gitleaks not installed","findings":[]}\n',
        '03-sast-semgrep': b'{"error":"semgrep not installed","findings":[]}\n', '05-dast-zap': b'{"error":"docker daemon not reachable","alerts":[]}\n',
        '06-tenant-isolation': b'{"error":"runner missing","findings":[]}\n', '07-license-compliance': b'{"error":"install: npm i -g license-checker-rseidelsohn","blocking":[]}\n',
        '08-aiken-tests': b'{"error":"aiken not installed","tests":{}}\n'}
WITH = {'01-dependency-audit': (b'{"runs":[{"service":"svc","counts":{},"advisories":[{"package":"pkg","severity":"high","title":"t"}]}]}\n', ['svc/pkg']),
        '02-secret-scan': (b'{"findings":[{"RuleID":"r1","File":"a.ts","StartLine":3}],"total":1}\n', ['r1@a.ts:3']),
        '03-sast-semgrep': (b'{"findings":[{"check_id":"c1","severity":"ERROR","path":"a.ts","line":3,"message":"m"}],"total":1}\n', ['c1@a.ts:3']),
        '05-dast-zap': (b'{"target":"t","alerts":[{"name":"n1","risk":"High (Medium)","first_url":"http://x/"}]}\n', ['n1@http://x/']),
        '06-tenant-isolation': (b'{"tested":[],"findings":[{"endpoint":"/api/x","observed_tenant":"a","expected_tenant":"b"}]}\n', ['/api/x:saw=a:want=b']),
        '07-license-compliance': (b'{"runs":[{"service":"s","total":1,"blocking":[{"package":"p","license":"GPL-3.0"}]}]}\n', ['s/p']),
        '08-aiken-tests': (b'{"tests":{"total":12,"passed":10,"failed":2},"aiken_exit":1}\n', ['tests-failed:2'])}
STDERR = b'login failed for verifier@secuura.com: 401 {"success":false}\n'   # runner.ts:74 console.error, merged by 06-tenant-isolation.sh:71 `2>&1`


def shapes_for(art):
    s = [('absent', None, 'CLEAN'), ('valid-zero', VALID_ZERO[art], 'CLEAN'), ('skip-error', SKIP[art], 'CLEAN'),
         ('two-values', VALID_ZERO[art] + VALID_ZERO[art], 'CLEAN'), ('valid-findings', WITH[art][0], 'FINDINGS'),
         ('empty-0B', b'', 'UNREADABLE'), ('whitespace', b'  \n', 'UNREADABLE'), ('truncated', b'{"x":[\n', 'UNREADABLE'),
         ('trailing-garbage', WITH[art][0] + b'{"x":[\n', 'UNREADABLE'), ('json-null', b'null\n', 'UNREADABLE'),
         ('json-false', b'false\n', 'UNREADABLE'), ('mode-000', ('mode000', VALID_ZERO[art]), 'UNREADABLE')]
    if art == '06-tenant-isolation':
        s += [('stderr-merged-clean', STDERR + VALID_ZERO[art], 'UNREADABLE'), ('stderr-merged-LEAK', STDERR + WITH[art][0], 'UNREADABLE')]
    return s


def rule(cls, job, b, h):
    """(ok, why) for one shape: the HEAD rule given the BASE result."""
    un = '%s/unreadable-artefact' % job
    if h['ids'] is None: return False, 'head wrote no REPORT.json'
    if cls == 'CLEAN':
        return (h['ids'] == [] and h['rc'] == 0 and h['ids'] == b['ids'] and h['rc'] == b['rc']), 'clean must stay clean (0 findings, rc 0, == base)'
    if cls == 'FINDINGS':
        return (un not in h['ids'] and h['ids'] == b['ids'] and h['rc'] == b['rc'] and h['ids'] != []), 'own findings only, == base, no unreadable id'
    want = sorted((b['ids'] or []) + [un])
    sev = [s for (j, s, i) in h['findings'] if i == un]
    return (h['ids'] == want and sev == ['high'] and h['rc'] == 1), 'base ids + exactly one %s HIGH, rc 1' % un


def shapes(out, hb, bb):
    t = Tally(); rows = []; base_viol = 0
    for art, job in sorted(JOBS.items()):
        for name, spec, cls in shapes_for(art):
            r = {}
            for side, blob in (('base', bb), ('head', hb)):
                root = tempfile.mkdtemp(prefix='%s.%s.%s.' % (art[:2], name, side), dir=out)
                r[side] = run_agg(blob, {art: spec}, root)
            ok, why = rule(cls, job, r['base'], r['head'])
            bok, _ = rule(cls, job, r['base'], r['base']) if r['base']['ids'] is not None else (False, '')
            base_viol += 0 if bok else 1
            before = 'CLEAN-SCAN SILENCE' if cls == 'UNREADABLE' and r['base']['ids'] == [] and r['base']['rc'] == 0 else ''
            rows.append((art, name, cls, r['base'], r['head'], before))
            t.check('SH-%s-%s' % (art[:2], name), ok, '%-10s BEFORE rc %s ids %s %s | NOW rc %s ids %s | %s' % (
                cls, r['base']['rc'], r['base']['ids'], before, r['head']['rc'], r['head']['ids'], why))
    # 04: KS-878's own guard, exactly once, base == head
    r = {s: run_agg(b, {'04-container-trivy': b'{"images":[\n'}, tempfile.mkdtemp(prefix='04.trunc.%s.' % s, dir=out)) for s, b in (('base', bb), ('head', hb))}
    t.check('SH-04-truncated', r['head']['ids'] == r['base']['ids'] == ['04-trivy/unreadable-artefact'] and r['head']['rc'] == 1,
            '04 truncated: base %s head %s (exactly once, not doubled)' % (r['base']['ids'], r['head']['ids']))
    allt = {a: b'{"x":[\n' for a in JOBS}
    r = {s: run_agg(b, allt, tempfile.mkdtemp(prefix='all7.trunc.%s.' % s, dir=out)) for s, b in (('base', bb), ('head', hb))}
    t.check('SH-all7-truncated', r['head']['ids'] == sorted('%s/unreadable-artefact' % j for j in JOBS.values()) and r['head']['rc'] == 1 and r['base']['ids'] == [] and r['base']['rc'] == 0,
            'all 7 truncated: BEFORE rc %s ids %s | NOW rc %s, %d unreadable ids' % (r['base']['rc'], r['base']['ids'], r['head']['rc'], len(r['head']['ids'] or [])))
    allw = {a: WITH[a][0] for a in JOBS}; want = sorted(i for a in JOBS for i in WITH[a][1])
    r = {s: run_agg(b, allw, tempfile.mkdtemp(prefix='all7.with.%s.' % s, dir=out)) for s, b in (('base', bb), ('head', hb))}
    t.check('SH-all7-findings', r['head']['ids'] == r['base']['ids'] == want, 'all 7 valid with findings: base == head == the 7 own ids: %s' % (r['head']['ids'] == want))
    # REPEAT: the same truncated 01 artefact on two consecutive runs in ONE runs/ dir (09 diffs against the previous REPORT.json)
    for side, blob in (('base', bb), ('head', hb)):
        root = tempfile.mkdtemp(prefix='repeat.%s.' % side, dir=out)
        r1 = run_agg(blob, {'01-dependency-audit': b'{"x":[\n'}, root)
        run2 = os.path.join(root, 'runs', '2026-10-06_fixture'); os.makedirs(run2)
        open(os.path.join(run2, '01-dependency-audit.json'), 'wb').write(b'{"x":[\n')
        env = dict(os.environ, TARGET_BASE='fixture', RUN_DIR=run2, SELF=os.path.join(root, 'Testing'), FAIL_ON='high', AUDIT_RUNS_DIR=os.path.join(root, 'runs'))
        rc2 = subprocess.run(['bash', 'jobs/09-aggregate-report.sh'], cwd=os.path.join(root, 'Testing'), env=env, capture_output=True).returncode
        rep2 = json.load(open(os.path.join(run2, 'REPORT.json')))
        t.info('SH-REPEAT-%s' % side, 'run 1 rc %s ids %s | run 2 rc %s, totals.high %s, NEW %s, prev_run %r — a persisting unreadable artefact is NOT new on run 2 (R-1 semantics, as for 04)' % (
            r1['rc'], r1['ids'], rc2, rep2['totals']['high'], [f['id'] for f in rep2['new_since_prev']], rep2['prev_run']))
    t.check('SH-CONTROL', base_viol > 0, 'the head rules applied to the BASE column report %d violation(s) (> 0: the matrix discriminates)' % base_viol)
    json.dump([{'artefact': a, 'shape': n, 'class': c, 'before': b, 'now': h, 'note': x} for a, n, c, b, h, x in rows], open(os.path.join(out, 'shapes.json'), 'w'), indent=1)
    print('MATRIX written: %s (%d rows)' % (os.path.join(out, 'shapes.json'), len(rows)))
    return t.end()


# ---------------- the suite, red-first, per-conjunct arms ----------------
def mutate(src, old, new, label):
    s = src.decode()
    n = s.count(old)
    if n != 1: raise SystemExit('ARM %s: anchor %r found %d time(s) (want 1) — refusing to tamper' % (label, old, n))
    m = s.replace(old, new, 1).encode()
    if m == src or blob_sha(m) == blob_sha(src): raise SystemExit('ARM %s: tamper did NOT land' % label)
    return m


def move_loop_below(src):
    L = src.decode().split('\n'); sp = [i for i, l in enumerate(L) if l.startswith('# KS-1136 R-3:')]
    e = [i for i, l in enumerate(L) if l == 'done' and i > sp[0]][0] + 1
    blk = L[sp[0]:e + 1]; rest = L[:sp[0]] + L[e + 1:]
    ia = [i for i, l in enumerate(rest) if l.startswith(PR['anchor_after'])]
    if len(blk) != 14 or len(ia) != 1: raise SystemExit('ARM D: loop %d lines / anchor %d (want 14 / 1)' % (len(blk), len(ia)))
    return '\n'.join(rest[:ia[0] + 1] + blk + rest[ia[0] + 1:]).encode()


def run_suite(suite, agg, out, tag):
    tmp = os.path.join(out, 'tmp'); os.makedirs(tmp, exist_ok=True)
    env = dict(os.environ, TMPDIR=tmp)                 # the suite's mktemp lands under --out, never the system temp
    if agg is not None: env['AGG_SH'] = agg
    t0 = time.time()
    p = subprocess.run(['bash', suite], env=env, capture_output=True)
    o = p.stdout.decode('utf-8', 'replace') + p.stderr.decode('utf-8', 'replace')
    open(os.path.join(out, 'suite_%s.out' % tag), 'w').write(o); open(os.path.join(out, 'suite_%s.rc' % tag), 'w').write('%d\n' % p.returncode)
    m = re.search(r'^\s*(\d+) passed, (\d+) failed\s*$', o, re.M)
    cells = re.findall(r'^  (ok|FAIL) ', o, re.M)
    return p.returncode, (int(m.group(1)), int(m.group(2))) if m else None, [i + 1 for i, c in enumerate(cells) if c == 'FAIL'], time.time() - t0


def suite(repo, head, wt, out):
    t = Tally()
    st = os.path.join(wt, PR['suite']); agg_wt = os.path.join(wt, PATH)
    if git(wt, 'rev-parse', 'HEAD').strip() != head:
        print('REFUSED: --wt %s is not AT the head %s' % (wt, head[:12])); return 2
    hb = open(agg_wt, 'rb').read()
    t.check('S0', blob_sha(hb) == blob_sha(git_bytes(repo, head, PATH)) and os.access(agg_wt, os.X_OK),
            'the worktree aggregator == the head blob (%s) and is EXECUTABLE on disk (git apply drops the bit — STANDING 2026-09-30)' % blob_sha(hb)[:12])
    rc, pf, red, dt = run_suite(st, None, out, 'head')
    t.check('S1', rc == 0 and pf == (6, 0), 'new suite at the head: rc %d, %s passed/failed, %.2f s (author: 6/0 rc 0, 1.332 s)' % (rc, pf, dt))
    bb = git_bytes(repo, P['parents'][0], PATH); bp = os.path.join(out, 'agg_BASE_739ebab.sh'); open(bp, 'wb').write(bb)
    rc, pf, red, dt = run_suite(st, bp, out, 'redfirst')
    t.check('S2', blob_sha(bb) == PR['base_blob'] and rc == 1 and pf == (3, 3) and red == [1, 2, 3],
            'RED-FIRST on the base blob %s: rc %d, %s, red cells %s (want rc 1, 3/3, cells [1, 2, 3]; controls 4-6 ok)' % (blob_sha(bb)[:12], rc, pf, red))
    arms = [('A', PR['conjunct_A'], '', (2, 4), 'drops `[ -f "$_f" ] &&` (EXISTS)'),
            ('B', PR['conjunct_B'], '', (4, 2), 'drops `! jq -e .` (PARSES)'),
            ('C', '08-aiken-tests:08-aiken; do', 'GATE71-REMOVED-08:08-aiken; do', (4, 2), 'removes 08 from the loop (an absent name in its place)')]
    for lab, old, new, want, what in arms:
        m = mutate(hb, old, new, lab); mp = os.path.join(out, 'agg_ARM_%s.sh' % lab); open(mp, 'wb').write(m)
        n = subprocess.run(['bash', '-n', mp], capture_output=True).returncode
        rc, pf, red, dt = run_suite(st, mp, out, 'arm%s' % lab)
        t.check('S3-%s' % lab if lab in 'AB' else 'S4-%s' % lab, n == 0 and rc == 1 and pf == want,
                'ARM %s %s: anchor x1, landed (sha %s != head), bash -n rc %d, suite rc %d %s red cells %s (want %s)' % (lab, what, blob_sha(m)[:12], n, rc, pf, red, want))
    m = move_loop_below(hb); mp = os.path.join(out, 'agg_ARM_D.sh'); open(mp, 'wb').write(m)
    n = subprocess.run(['bash', '-n', mp], capture_output=True).returncode
    rc, pf, red, dt = run_suite(st, mp, out, 'armD')
    t.check('S4-D', n == 0 and rc == 1 and red == [1, 2, 3], 'ARM D the loop MOVED below ALL_FINDINGS (sha %s): bash -n %d, suite rc %d %s red %s (want cells [1, 2, 3])' % (blob_sha(m)[:12], n, rc, pf, red))
    rc, pf, red, dt = run_suite(st, '', out, 'emptyAGG')
    t.check('S5', rc == 2 and pf is None, "the suite's own refusal: AGG_SH='' -> rc %d, no verdict line (want rc 2)" % rc)
    rc, pf, red, dt = run_suite(st, None, out, 'head2')
    t.check('S6', rc == 0 and pf == (6, 0), 'second run at the head agrees: rc %d %s' % (rc, pf))
    return t.end()


# ---------------- callers ----------------
def callers(repo, head, wt, out):
    t = Tally(); hits = {}
    for tok in K['consumer_tokens']:
        rc, o, e = git(repo, 'grep', '-l', '-F', tok, head, '--', '.', check=False)
        for l in o.split('\n'):
            if l: hits.setdefault(l.split(':', 1)[1], set()).add(tok)
    fab = git(repo, 'grep', '-l', '-F', 'GATE71-FABRICATED-TOKEN-x9q', head, '--', '.', check=False)[1].strip()
    t.check('K0', PATH in hits and fab == '', 'positive control: 09 names itself (%s) | fabricated token files: %d' % (PATH in hits, len(fab.split('\n')) if fab else 0))
    execs = {}
    for f in sorted(hits):
        txt = git(repo, 'show', '%s:%s' % (head, f), check=False)[1]
        live = '\n'.join(l for l in txt.split('\n') if not re.match(r'^\s*#', l))      # comments never count as an invocation
        if f.startswith('Projects Documents/') or f.endswith('.md') or f.endswith('.html'): cls = 'DOC'
        elif re.search(r'\bbash\s+\S*09-aggregate-report\.sh', live): cls = 'EXECUTES-09'
        elif re.search(r'(\./\S*run-internal-audit\.sh|\bbash\s+\S*run-internal-audit\.sh)', live) and f.endswith(('.yml', '.yaml', '.sh')): cls = 'CALLS-RUNNER'
        elif 'REPORT.json' in txt or 'REPORT.md' in txt: cls = 'READS-REPORT'
        else: cls = 'MENTIONS'
        if cls != 'DOC': execs[f] = cls
        print('CALLER %-13s %s  [%s]' % (cls, f, ','.join(sorted(hits[f]))))
    exp = set(K['consumers_expected']) - {'Blockchain/Testing/baselines/*.txt'}
    got = {f for f, c in execs.items() if c in ('EXECUTES-09', 'CALLS-RUNNER')}
    t.check('K1', exp - {PATH} <= set(execs) | {PATH}, 'every kit-expected consumer found: missing %s' % sorted(exp - set(execs) - {PATH}))
    t.info('K2', 'EXECUTING callers at the head: %s | NOT in the kit list: %s' % (sorted(got), sorted(got - exp) or 'none'))
    bl = [l for l in git(repo, 'ls-tree', '-r', '--name-only', head, '--', 'Blockchain/Testing/baselines').split('\n') if l]
    fps = [(f, l) for f in bl for l in git(repo, 'show', '%s:%s' % (head, f)).split('\n') if l.strip() and not re.match(r'^\s*#', l)]
    masked = [(f, l.split()[0]) for f, l in fps if 'unreadable-artefact' in l]
    t.check('K4', not masked and len(fps) > 0, 'baseline fingerprints at the head: %d over %d file(s) (CONTROL > 0); carrying `unreadable-artefact` (would mask the new HIGH): %s' % (
        len(fps), len(bl), masked or 0))
    if wt:
        ts = os.path.join(wt, 'Blockchain/Dev/scripts/__tests__/aggregate_report_trivy_artefact.test.sh')
        hp = os.path.join(out, 'agg_HEAD.sh'); open(hp, 'wb').write(git_bytes(repo, head, PATH))
        bp = os.path.join(out, 'agg_BASE.sh'); open(bp, 'wb').write(git_bytes(repo, P['parents'][0], PATH))
        a = run_suite(ts, hp, out, 'trivy_head'); b = run_suite(ts, bp, out, 'trivy_base')
        t.check('K3', a[0] == 0 and b[0] == 0 and a[1] == b[1] == (5, 0),
                'the trivy suite against HEAD %s and against BASE (= head minus the loop) %s: identical -> it never reaches the loop; its negatives are untouched' % (a[1], b[1]))
    else:
        t.info('K3', 'NOT RUN by name (no --wt): the trivy-suite blindness arm')
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    rep(insertion_span(['a', 'b', 'c'], ['a', 'x', 'y', 'b', 'c']) == (1, 2), 'insertion_span finds a pure 2-line insertion')
    rep(insertion_span(['a', 'b', 'c'], ['a', 'x', 'b', 'C']) is None, 'PLANTED edit of an existing line: NOT a pure insertion')
    rep(loop_names('for _art in a:x b:y \\\n   c:z; do') == {'a': 'x', 'b': 'y', 'c': 'z'}, 'loop_names reads a continued list')
    blk = 'if [ -f "$RUN_DIR/01-dependency-audit.json" ]; then\n  emit "01-deps" x\nfi\nif [ -f "$RUN_DIR/02-secret-scan.json" ]; then\n  emit "02-WRONG" x\nfi'
    rep(blocks_by_artefact(blk) == {'01-dependency-audit': '01-deps', '02-secret-scan': '02-WRONG'}, 'blocks_by_artefact maps artefact -> first emit id (a PLANTED wrong id is visible)')
    z = {'rc': 0, 'ids': [], 'findings': []}; u = {'rc': 1, 'ids': ['01-deps/unreadable-artefact'], 'findings': [('01-deps', 'high', '01-deps/unreadable-artefact')]}
    rep(rule('UNREADABLE', '01-deps', z, u)[0], 'rule: base silent + head one HIGH unreadable passes')
    rep(not rule('UNREADABLE', '01-deps', z, z)[0], 'PLANTED head still silent on an unreadable shape FAILS')
    rep(not rule('CLEAN', '01-deps', z, u)[0], 'PLANTED head flagging a CLEAN shape FAILS (false alarm)')
    uu = dict(u, ids=['01-deps/unreadable-artefact'] * 2, findings=[('01-deps', 'high', '01-deps/unreadable-artefact')] * 2)
    rep(not rule('UNREADABLE', '01-deps', z, uu)[0], 'PLANTED doubled unreadable finding FAILS')
    f = {'rc': 1, 'ids': ['svc/pkg'], 'findings': [('01-deps', 'high', 'svc/pkg')]}
    rep(rule('FINDINGS', '01-deps', f, f)[0] and not rule('FINDINGS', '01-deps', f, {'rc': 1, 'ids': ['01-deps/unreadable-artefact', 'svc/pkg'], 'findings': []})[0],
        'rule FINDINGS: own ids pass; an extra unreadable id on valid JSON FAILS')
    try: mutate(b'x && y && z', ' && ', '', 'T'); rep(False, 'PLANTED non-unique anchor must refuse')
    except SystemExit: rep(True, 'PLANTED non-unique anchor (count 2) REFUSES the tamper')
    try: mutate(b'abc', 'q', 'q', 'T'); rep(False, 'absent anchor must refuse')
    except SystemExit: rep(True, 'PLANTED absent anchor REFUSES')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A or A[0] not in ('guard', 'suite', 'shapes', 'callers') or not opt(A, '--repo'): print(__doc__); return 2
    repo = opt(A, '--repo'); head = opt(A, '--head', P['head_expected'])
    rr = refuse_absent(repo, [('head', head), ('base', P['parents'][0])])
    if rr: return rr
    out = opt(A, '--out')
    if A[0] != 'guard':
        if not out: print('REFUSED: --out <a fresh dir of yours> is required'); return 2
        os.makedirs(out, exist_ok=True)
        if os.listdir(out): print('REFUSED: --out %s is not empty (use a FRESH dir; never clean one)' % out); return 2
    print('C2 %s #%s head %s repo %s out %s' % (A[0], P['pr'], head, repo, out))
    if A[0] == 'guard': return guard(repo, head)
    if A[0] == 'suite':
        if not opt(A, '--wt'): print('REFUSED: suite needs --wt <worktree at the head>'); return 2
        return suite(repo, head, opt(A, '--wt'), out)
    if A[0] == 'shapes':
        return shapes(out, git_bytes(repo, head, PATH), git_bytes(repo, P['parents'][0], PATH))
    return callers(repo, head, opt(A, '--wt'), out)


if __name__ == '__main__':
    sys.exit(main())
