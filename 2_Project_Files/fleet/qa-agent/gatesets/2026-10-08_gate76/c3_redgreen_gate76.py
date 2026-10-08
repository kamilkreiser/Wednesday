#!/usr/bin/env python3
r"""c3_redgreen_gate76.py — the gate RE-RUNS each seat's red/green itself, at the head, in ITS OWN worktree (STANDING lesson: the gate never
takes a seat's red/green on its word), plus arms the seats did not run. NEW at gate76 (gate75's c3_guard was a leg-14 guard instrument; the
shape is carried: bind the worktree to its tree, tamper ONLY by SAVED BYTES, restore to the HEAD state and PROVE it, read every run with ONE
parser, a red counts only on its DECLARED cell).

EVERY worktree is YOURS, outside !CODING (refused otherwise), and BOUND: `--expect-tree <40-hex>` must equal HEAD^{tree} and the start must be
porcelain-clean (untracked included, `node_modules` and build output excepted by the repo's own .gitignore) — rc 11.

MODES
  trivy     --wt W --expect-tree T --base B --scratch S --out J        (#1427 KS-1274)
            G  the three container_trivy_* suites at the head: rc + `N passed, M failed` each (R 18th: 5/0, 6/0, 5/0).
            R  THE SEAT'S RED-PROOF, re-driven: the job's bytes SAVED (asserted == its HEAD blob), the BASE blob's bytes written (asserted
               landed: hash-object == the base blob), the failed-scan suite run -> want rc 1, `4 passed, 1 failed`, the ONE failing cell == the
               KS-1274 RED cell, the `ArtifactName and no Results` CONTROL cell `ok` in BOTH states (R 18th's claim). The other two suites
               under the revert are REPORTED. Then the saved bytes restored, hash-object == the HEAD blob, porcelain clean.
            A  ARMS the seat did not run, on a STANDALONE stub harness (a copy of the job in S, never the worktree's file), each run against
               the HEAD job AND the BASE job with ONE parser: `{"Results":[]}` (clean), `{}` (THE defect), `{"SchemaVersion":2,"ArtifactName":
               "x"}` (trivy 0.71's clean shape), `null`, `[]`, `{"Results":null}`, a non-JSON line, and trivy exit 1 with no output.
               Each arm has a declared WANT at the head; a GREEN where the want is GREEN-GAP is a NAMED edge, never a pass.
  originate --wt W --expect-tree T --base B --out J [--full]          (#1428 KS-593)
            S-1 must be done (Blockchain/Dev node_modules + packages/shared/dist/index.js) — rc 12 naming what is missing.
            G  the four touched jest files at the head (`npx jest <files>` in services/originate): the `Tests:` line per file.
            R  THE SEAT'S RED: the three ROUTE files' bytes SAVED (asserted == HEAD blobs), the BASE blobs written (asserted landed), the three
               ks593-* files run -> R 18th-style ratios (G 4th: adminconfig 2f/3p, share 2f/13p, signatories 3f/3p), each FAILING test read
               by NAME; then restored and PROVED (hash-object == HEAD, porcelain clean).
            F  --full: the whole originate suite at the head (`npx jest`): `Test Suites:` + `Tests:` lines (G 4th: 96 / 1093 / 0).
  --selftest                             the parsers on CAPTURED lines + the harness's own controls.
rc 0 PASS / 1 FAIL / 2 refused / 11 not the pinned tree or not clean / 12 S-1 not done."""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile

FORBIDDEN = '/Volumes/DevMASTER/!CODING'
ENV = dict(os.environ); ENV.pop('GIT_SSH_COMMAND', None); ENV['TMPDIR'] = '/tmp'
JOB = 'Blockchain/Testing/jobs/04-container-trivy.sh'
SUITES = ['Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh',
          'Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh',
          'Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh']
RED_CELL = '🔴 KS-1274 a trivy that exits 0 with a bare {} is recorded as scan-failed and the job exits 1'
CTL_CELL = 'CONTROL KS-1274 a clean report with ArtifactName and no Results stays clean: rc 0, no error'
ORIG = 'Blockchain/Dev/services/originate'
ROUTES = ['src/routes/adminConfig.ts', 'src/routes/documents.ts', 'src/routes/signatories.ts']
TESTS = {'adminconfig': 'src/__tests__/ks593-adminconfig-list-refuses-negative-offset.test.ts',
         'share': 'src/__tests__/ks593-share-refuses-non-object-recipient.test.ts',
         'signatories': 'src/__tests__/ks593-signatories-refuses-a-non-uuid-id.test.ts',
         'hermetic': 'src/__tests__/ks1293-originate-suite-is-hermetic.test.ts'}
SEAT_RED = {'adminconfig': (2, 3), 'share': (2, 13), 'signatories': (3, 3)}      # (failed, passed) at base, G 4th's READY; share = share + hermetic files


def opt(A, k, d=None):
    return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d


class Tally:
    def __init__(self): self.n = 0; self.fails = []
    def check(self, cid, ok, msg):
        self.n += 1; print('%s %s %s' % ('PASS' if ok else 'FAIL', cid, msg))
        if not ok: self.fails.append(cid)
        return ok
    def info(self, cid, msg): print('INFO %s %s' % (cid, msg))
    def end(self):
        print('CHECKED %d' % self.n); print('%d FAIL%s' % (len(self.fails), (' (' + ' '.join(self.fails) + ')') if self.fails else ''))
        if self.n == 0: print('FAIL: 0 checked'); return 1
        return 1 if self.fails else 0


def under_forbidden(p):
    return any(q == FORBIDDEN or q.startswith(FORBIDDEN + '/') for q in (os.path.abspath(p), os.path.realpath(p)))


def g(wt, *a, inp=None):
    p = subprocess.run(['git', '-C', wt] + list(a), capture_output=True, input=inp, env=ENV)
    return p.returncode, p.stdout.decode('utf-8', 'replace').strip(), p.stderr.decode('utf-8', 'replace').strip()


def porcelain(wt):
    return g(wt, 'status', '--porcelain', '--untracked-files=all')[1]


def bind(wt, tree):
    if not (wt and tree): raise SystemExit('REFUSED: --wt and --expect-tree are REQUIRED')
    if under_forbidden(wt): print('REFUSED: --wt %s is under %s — use YOUR worktree in YOUR clone' % (wt, FORBIDDEN)); sys.exit(2)
    rc, t, _ = g(wt, 'rev-parse', 'HEAD^{tree}')
    if rc != 0 or t != tree: print('REFUSED (rc 11): worktree %s HEAD^{tree} %r != --expect-tree %s' % (wt, t[:12], tree[:12])); sys.exit(11)
    st = porcelain(wt)
    if st: print('REFUSED (rc 11): worktree %s is not clean at the start:\n%s' % (wt, st[:400])); sys.exit(11)
    print('BOUND: %s HEAD^{tree} == %s, porcelain clean (untracked included)' % (wt, tree[:12]))


def blob_at(wt, rev, path):
    rc, o, _ = g(wt, 'ls-tree', rev, '--', path)
    f = o.split(); return f[2] if rc == 0 and len(f) >= 3 else ''


def bytes_at(wt, rev, path):
    p = subprocess.run(['git', '-C', wt, 'show', '%s:%s' % (rev, path)], capture_output=True)
    if p.returncode: raise SystemExit('REFUSED: git show %s:%s rc %d' % (rev[:12], path, p.returncode))
    return p.stdout


def hash_file(wt, path):
    return g(wt, 'hash-object', '--', os.path.join(wt, path))[1]


class Tamper:
    """Write BASE bytes over a set of paths, proving the save, the landing and the restore. Never checkout/restore/reset/clean."""
    def __init__(self, wt, base, paths):
        self.wt, self.base, self.paths, self.saved = wt, base, paths, {}
    def __enter__(self):
        for p in self.paths:
            fp = os.path.join(self.wt, p); hb = blob_at(self.wt, 'HEAD', p)
            self.saved[p] = (open(fp, 'rb').read(), os.stat(fp).st_mode)
            if hash_file(self.wt, p) != hb: raise SystemExit('REFUSED: %s on disk != its HEAD blob before the tamper' % p)
            open(fp, 'wb').write(bytes_at(self.wt, self.base, p)); os.chmod(fp, self.saved[p][1])
            landed = hash_file(self.wt, p) == blob_at(self.wt, self.base, p)
            print('TAMPER %s: saved %d B (== HEAD blob %s), wrote the BASE blob %s, landed %s' % (p, len(self.saved[p][0]), hb[:12], blob_at(self.wt, self.base, p)[:12], landed))
            if not landed: raise SystemExit('REFUSED: the tamper did not land on %s' % p)
        return self
    def __exit__(self, *a):
        for p, (b, m) in self.saved.items():
            fp = os.path.join(self.wt, p); open(fp, 'wb').write(b); os.chmod(fp, m)
        bad = [p for p in self.saved if hash_file(self.wt, p) != blob_at(self.wt, 'HEAD', p)]
        st = porcelain(self.wt)
        print('RESTORE %d path(s) from SAVED BYTES: hash-object == HEAD blob for all %s | porcelain %r' % (len(self.saved), not bad, st[:200]))
        if bad or st: raise SystemExit('RESTORE FAILED: %s / %r — STOP, the worktree is not at the head' % (bad, st[:200]))


# ---------------- parsers (ONE per instrument, used before AND after) ----------------
SH_TALLY = re.compile(r'^\s*(\d+) passed, (\d+) failed\s*$', re.M)
SH_CELL = re.compile(r'^\s{2}(ok|FAIL) {1,3}(.+?)\s*$', re.M)
JEST_TESTS = re.compile(r'^Tests:\s+(?:(\d+) failed, )?(?:(\d+) skipped, )?(\d+) passed, (\d+) total', re.M)
JEST_FAILED_ONLY = re.compile(r'^Tests:\s+(\d+) failed, (\d+) total', re.M)
JEST_SUITES = re.compile(r'^Test Suites:\s+(?:(\d+) failed, )?(?:(\d+) skipped, )?(\d+) passed, (\d+) total', re.M)
JEST_FAIL_NAME = re.compile(r'^\s+✕ (.+?)(?: \(\d+ ms\))?$', re.M)


def parse_sh(text):
    m = SH_TALLY.findall(text)
    return {'tally': [int(x) for x in m[-1]] if m else None, 'cells': [(s, n) for s, n in SH_CELL.findall(text)]}


def parse_jest(text):
    m = JEST_TESTS.findall(text)
    if m:
        f, s, p, t = m[-1]; tests = [int(f or 0), int(p), int(t)]
    else:
        m2 = JEST_FAILED_ONLY.findall(text); tests = [int(m2[-1][0]), 0, int(m2[-1][1])] if m2 else None
    su = JEST_SUITES.findall(text)
    suites = [int(su[-1][0] or 0), int(su[-1][2]), int(su[-1][3])] if su else None
    return {'tests': tests, 'suites': suites, 'failed_names': JEST_FAIL_NAME.findall(text)}


def run_sh(wt, suite):
    p = subprocess.run(['bash', os.path.join(wt, suite)], capture_output=True, env=ENV, cwd=wt)
    out = p.stdout.decode('utf-8', 'replace') + p.stderr.decode('utf-8', 'replace')
    d = parse_sh(out); d['rc'] = p.returncode; d['text'] = out
    return d


# ---------------- trivy ----------------
HARNESS = r'''#!/bin/bash
# gate76 standalone stub harness: ONE image, trivy prints $TRIVY_OUT (or nothing) and exits $TRIVY_RC. Mirrors the suites' fixture shape.
set -u
root="$1"; job="$2"
rm -rf "$root"; mkdir -p "$root/Testing/jobs" "$root/bin" "$root/run"
cp "$job" "$root/Testing/jobs/04-container-trivy.sh"
printf '#!/bin/bash\ncase "${1:-}" in\n  info) exit 0 ;;\n  images) echo dev-auth:latest ;;\nesac\nexit 0\n' > "$root/bin/docker"
{ printf '#!/bin/bash\n'; printf 'cat "%s/trivy_out.txt"\n' "$root"; printf 'exit "$(cat "%s/trivy_rc.txt")"\n' "$root"; } > "$root/bin/trivy"
printf '%s' "$TRIVY_OUT" > "$root/trivy_out.txt"; printf '%s' "$TRIVY_RC" > "$root/trivy_rc.txt"
chmod +x "$root/bin/docker" "$root/bin/trivy"
( export PATH="$root/bin:/usr/bin:/bin" SELF="$root/Testing" RUN_DIR="$root/run"; cd "$root/Testing" && bash jobs/04-container-trivy.sh ) > "$root/out.txt" 2>&1
rc=$?
err="$(jq -r '.images[0].error // "none"' "$root/run/04-container-trivy.json" 2>/dev/null || echo unparseable)"
echo "RESULT rc=$rc error=$err"
'''
ARMS = [  # (id, trivy stdout, trivy rc, WANT at the head, what it is)
    ('T0', '{"Results":[]}\n', 0, 'CLEAN', 'a clean report with an empty Results array (CONTROL)'),
    ('T1', '{}\n', 0, 'FAILED', 'THE DEFECT: a bare {} exit 0'),
    ('T2', '{"SchemaVersion":2,"ArtifactName":"dev-auth:latest"}\n', 0, 'CLEAN', 'trivy 0.71 clean shape: ArtifactName, no Results (CONTROL)'),
    ('T3', 'null\n', 0, 'FAILED', 'JSON null exit 0 (has() on null errors -> scan-failed)'),
    ('T4', '[]\n', 0, 'FAILED', 'a JSON array exit 0 (has() on an array errors -> scan-failed)'),
    ('T5', '{"Results":null}\n', 0, 'CLEAN-GAP', 'Results present but null: has("Results") is TRUE -> reads CLEAN (a NAMED edge, not the ticket\'s shape)'),
    ('T6', 'not json\n', 0, 'FAILED', 'a non-JSON line exit 0 (KS-1136 path: jq cannot read it)'),
    ('T7', '', 1, 'FAILED', 'trivy exit 1 with no output (KS-1136 CONTROL)'),
]


def trivy_arms(job_head, job_base, scratch):
    hp = os.path.join(scratch, 'harness.sh'); open(hp, 'w').write(HARNESS)
    res = []
    for aid, out, rc, want, what in ARMS:
        row = {'id': aid, 'want': want, 'what': what}
        for side, job in (('head', job_head), ('base', job_base)):
            p = subprocess.run(['bash', hp, os.path.join(scratch, 'arm_%s_%s' % (aid, side)), job], capture_output=True,
                               env=dict(ENV, TRIVY_OUT=out, TRIVY_RC=str(rc)))
            m = re.search(r'RESULT rc=(\d+) error=(\S+)', p.stdout.decode())
            row[side] = (int(m.group(1)), m.group(2)) if m else ('LOADFAIL', p.stderr.decode()[:120])
        res.append(row)
    return res


def classify(r):
    rc, err = r
    if rc == 0 and err == 'none': return 'CLEAN'
    if rc == 1 and err == 'scan-failed': return 'FAILED'
    return 'OTHER(%s,%s)' % (rc, err)


def trivy(wt, tree, base, scratch, out):
    t = Tally(); bind(wt, tree); J = {'green': {}, 'red': {}, 'arms': []}
    for s in SUITES:
        d = run_sh(wt, s); J['green'][s] = {'rc': d['rc'], 'tally': d['tally']}
        t.check('G-%s' % os.path.basename(s).split('.')[0], d['rc'] == 0 and d['tally'] is not None and d['tally'][1] == 0 and d['tally'][0] > 0,
                'at the head: rc %d, %s passed / %s failed' % (d['rc'], *(d['tally'] or ('?', '?'))))
    with Tamper(wt, base, [JOB]):
        d = run_sh(wt, SUITES[1]); fails = [n for s_, n in d['cells'] if s_ == 'FAIL']; ctl = [s_ for s_, n in d['cells'] if n == CTL_CELL]
        J['red']['failed_scan'] = {'rc': d['rc'], 'tally': d['tally'], 'failing': fails, 'control': ctl}
        t.check('R1', d['rc'] == 1 and d['tally'] == [4, 1] and fails == [RED_CELL] and ctl == ['ok'],
                'job REVERTED to the base blob, suites kept patched: rc %d, %s passed / %s failed; failing cell(s) %s; CONTROL cell %s (want rc 1, 4/1, ONLY the KS-1274 RED cell, CONTROL ok)' % (
                    d['rc'], *(d['tally'] or ('?', '?')), fails, ctl))
        for s in (SUITES[0], SUITES[2]):
            d2 = run_sh(wt, s); J['red'][s] = {'rc': d2['rc'], 'tally': d2['tally']}
            t.info('R2-%s' % os.path.basename(s).split('.')[0], 'under the revert: rc %d, %s passed / %s failed (REPORTED; the clean stub reads clean under either job)' % (d2['rc'], *(d2['tally'] or ('?', '?'))))
    jh, jb = os.path.join(scratch, 'job_head.sh'), os.path.join(scratch, 'job_base.sh')
    open(jh, 'wb').write(bytes_at(wt, 'HEAD', JOB)); open(jb, 'wb').write(bytes_at(wt, base, JOB))
    arms = trivy_arms(jh, jb, scratch); J['arms'] = arms
    for a in arms:
        h, b = classify(a['head']), classify(a['base'])
        want_h = 'CLEAN' if a['want'] == 'CLEAN-GAP' else a['want']
        t.check('A-%s' % a['id'], h == want_h, '%s | head %s %s (want %s) | base %s %s%s' % (
            a['what'], h, a['head'], a['want'], b, a['base'], ' | THE FIX CHANGES THIS ARM' if h != b else ''))
    t.check('A-CTL', classify(arms[1]['base']) == 'CLEAN' and classify(arms[1]['head']) == 'FAILED',
            'NON-VACUITY: the harness reproduces the DEFECT at the base (bare {} reads CLEAN) and the fix at the head (FAILED)')
    json.dump(J, open(out, 'w'), indent=1)
    return t


# ---------------- originate ----------------
def s1_missing(wt):
    miss = []; dev = os.path.join(wt, 'Blockchain/Dev')
    if not os.path.isdir(os.path.join(dev, 'node_modules')): miss.append('Blockchain/Dev node_modules (npm ci --ignore-scripts)')
    if not os.path.isfile(os.path.join(dev, 'packages/shared/dist/index.js')): miss.append('packages/shared/dist/index.js (npm run build --workspace=packages/shared)')
    return miss


def jest(wt, files):
    cwd = os.path.join(wt, ORIG)
    p = subprocess.run(['npx', '--no-install', 'jest', '--ci', '--colors=false', '--verbose'] + list(files), capture_output=True, env=dict(ENV, CI='1', FORCE_COLOR='0'), cwd=cwd)
    out = p.stdout.decode('utf-8', 'replace') + p.stderr.decode('utf-8', 'replace')
    d = parse_jest(out); d['rc'] = p.returncode; d['text'] = out
    return d


def originate(wt, tree, base, out, full):
    t = Tally(); bind(wt, tree)
    miss = s1_missing(wt)
    if miss: print('REFUSED (rc 12): S-1 not done in %s: %s' % (wt, miss)); sys.exit(12)
    J = {'green': {}, 'red': {}}
    for k, f in TESTS.items():
        d = jest(wt, [f]); J['green'][k] = {'rc': d['rc'], 'tests': d['tests']}
        t.check('G-%s' % k, d['rc'] == 0 and d['tests'] is not None and d['tests'][0] == 0 and d['tests'][1] > 0,
                'at the head %s: rc %d, Tests [failed, passed, total] %s' % (f, d['rc'], d['tests']))
    with Tamper(wt, base, [os.path.join(ORIG, r) for r in ROUTES]):
        for k in ('adminconfig', 'share', 'signatories'):
            files = [TESTS[k]] + ([TESTS['hermetic']] if k == 'share' else [])   # G 4th's share ratio spans TWO files (share 5 + hermetic 10)
            d = jest(wt, files); J['red'][k] = {'rc': d['rc'], 'tests': d['tests'], 'failed_names': d['failed_names'], 'files': files}
            f_, p_ = (d['tests'][0], d['tests'][1]) if d['tests'] else (None, None)
            t.check('R-%s' % k, d['rc'] != 0 and (f_, p_) == SEAT_RED[k] and len(d['failed_names']) == f_,
                    'the three ROUTES reverted to base, tests kept, %s: rc %d, %s failed / %s passed (G 4th: %d / %d); failing by NAME %s' % (
                        '+'.join(os.path.basename(f) for f in files), d['rc'], f_, p_, SEAT_RED[k][0], SEAT_RED[k][1], d['failed_names']))
    if full:
        d = jest(wt, []); J['full'] = {'rc': d['rc'], 'tests': d['tests'], 'suites': d['suites']}
        t.check('F1', d['rc'] == 0 and d['tests'] is not None and d['tests'][0] == 0, 'whole originate suite at the head: rc %d, Test Suites [failed, passed, total] %s, Tests %s (G 4th: 96 / 1093 / 0)' % (
            d['rc'], d['suites'], d['tests']))
    json.dump(J, open(out, 'w'), indent=1)
    return t


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    cap = ('  ok   CONTROL - two clean scans: rc 0, 2 images, 0 errors\n  FAIL ' + RED_CELL + '\n     want 1 scan-failed, got 0 none\n  ok   ' + CTL_CELL + '\n\n  4 passed, 1 failed\n')
    d = parse_sh(cap)
    rep(d['tally'] == [4, 1] and [n for s, n in d['cells'] if s == 'FAIL'] == [RED_CELL] and ('ok', CTL_CELL) in d['cells'], 'parse_sh on the R 18th-shaped red: %s' % d['tally'])
    rep(parse_sh('FATAL: jq is not on PATH')['tally'] is None, 'parse_sh on a LOADFAIL reads None (never a red)')
    j1 = 'Tests:       2 failed, 13 passed, 15 total\n  ✕ refuses a null recipient with 400 (12 ms)\n  ✕ refuses a string recipient (3 ms)\nTest Suites: 1 failed, 1 total\n'
    d = parse_jest(j1)
    rep(d['tests'] == [2, 13, 15] and len(d['failed_names']) == 2, 'parse_jest on a 2f/13p capture: %s %s' % (d['tests'], d['failed_names']))
    d = parse_jest('Test Suites: 96 passed, 96 total\nTests:       1093 passed, 1093 total\n')
    rep(d['tests'] == [0, 1093, 1093] and d['suites'] == [0, 96, 96], 'parse_jest on the G 4th full-suite shape: %s %s' % (d['suites'], d['tests']))
    rep(parse_jest('no jest here')['tests'] is None, 'parse_jest on a foreign console reads None')
    rep(classify((0, 'none')) == 'CLEAN' and classify((1, 'scan-failed')) == 'FAILED' and classify(('LOADFAIL', 'x')).startswith('OTHER'), 'classify: CLEAN / FAILED / a LOADFAIL is OTHER, never a red')
    rep(under_forbidden('/Volumes/DevMASTER/!CODING/x') and not under_forbidden('/private/tmp/x'), 'the !CODING refusal')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    mode = A[0] if A else ''
    wt, tree, base, out = opt(A, '--wt'), opt(A, '--expect-tree'), opt(A, '--base'), opt(A, '--out')
    if mode not in ('trivy', 'originate'): print(__doc__); return 2
    if not (base and re.fullmatch(r'[0-9a-f]{40}', base) and out): print('REFUSED: --base <40-hex> and --out are REQUIRED'); return 2
    if mode == 'trivy':
        sc = opt(A, '--scratch')
        if not sc or under_forbidden(sc): print('REFUSED: --scratch <dir outside !CODING> is REQUIRED'); return 2
        os.makedirs(sc, exist_ok=True)
        return trivy(wt, tree, base, sc, out).end()
    return originate(wt, tree, base, out, '--full' in A).end()


if __name__ == '__main__':
    sys.exit(main())
