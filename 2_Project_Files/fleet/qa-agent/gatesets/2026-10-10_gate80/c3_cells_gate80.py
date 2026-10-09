#!/usr/bin/env python3
"""c3_cells_gate80.py — the RUN instruments for gate80: #1441's cells / probe / tamper / whole suite / tsc (jest, in YOUR worktree) and #1442's
suite / siblings / real packages / hook path / tamper / the docs COMPOSITION (shell + git plumbing, in YOUR scratch). Every write path is checked
lexically AND by realpath and refused under !CODING. Carried in shape from c3_cells_gate79.py; [g80] rebuilt.

  setup1441  --clone CL --head H --wt WT [--log DIR]      `git worktree add --detach` in YOUR clone; in WT/Blockchain/Dev `npm ci --ignore-scripts`
             and `npm run build --workspace=packages/shared` (dist/index.js ASSERTED). Refuses a WT that exists. (X1)
  cells1441  --wt WT --clone CL --head H --base B --route base|head --tests base|head --out DIR
             plants webhooks.ts (route) and ks1341c (tests) FROM THE NAMED REV by content, asserts each plant LANDED (sha), runs jest ONCE on the
             file, RESTORES by sha, prints per test status (LOAD-FAILED is never a count). PREDICTIONS (never evidence): (base,head) reds
             D0 D4 D3 (3 of 11); (head,head) 11/11; (base,base) 8/8 green; (head,base): the draft says 8/8 — MEASURE it.
  suite1441  --wt WT --clone CL --head H --base B --route base|head --out DIR     the WHOLE originate jest suite (`--ci --json`): suites / load
             failures / tests / passed / failed / skipped. Plants only the two files that differ (route + tests) for the base run.
  tsc1441    --wt WT --out DIR                              `tsc --noEmit -p services/originate/tsconfig.json` rc.
  probe32    --wt WT --clone CL --head H --base B --route base|head --out DIR   appends probe_block_gate80.ts.txt to a COPY of ks1341c, runs it
             with G80_PROBE_OUT, MOVES the probe out (quarantine, never rm), asserts WT porcelain clean. FACTS, never a verdict.
  tamper1441 --wt WT --clone CL --head H --base B --out DIR [--only T1,T2]   the guard-removal tamper (T1) + 5 more; anchor EXACTLY ONCE,
             LANDED (sha changed + replacement present), run ks1341c, read which tests RED, RESTORE (sha). A suite that fails to LOAD is
             TAMPER-INVALID. An ALL-GREEN row is a tamper no cell catches. Also a HEAD row (all green) and a CONTROL no-op-comment row.
  suite1442  --clone CL --head H --base B --scratch S --out DIR    extracts base/head trees (git archive) and runs the new suite four ways via
             PACKAGE_FORMAT_GATE_SH (script head / script base / script head WITHOUT the redirect / suite is the thing that fails), then the
             sibling suites at base and head, `html_docs_matrix`, `run-shell-suites.sh --list` counts. Uses /bin/bash and Homebrew bash if present.
  realpkg    --clone CL --head H --base B --scratch S --out DIR [--install]   (F) `npm ci --ignore-scripts` in the 4 systemTest packages of the HEAD
             tree (X9; a failure => NOT RUN with the reason), prettier asserted executable, `--list` / `--all` at BASE script and HEAD script (stdout /
             stderr separate), a stdin-reader census of the 4 format:check scripts, and the honest control: a 5th FIXTURE package that drains stdin
             in the SAME run as the real ones (base misses what follows it, head does not).
  hookpath   --clone CL --head H --base B --scratch S --out DIR    which pushed paths select a package: the PR's own 4 paths (predict 0, silent)
             vs `systemTest/performance/package.json` (predict 1 selected). Feeds the hook's selection input on stdin; never pushes.
  tamper1442 --clone CL --head H --base B --scratch S --out DIR    U1 /dev/zero (a hang: 20 s timeout, process group killed) U2 drop `2>&1` U3 redirect
             on `cd` only U4 redirect on the assignment U5 no redirect (== base). Each anchor once, LANDED, run the suite, reds read.
  docs       --clone CL --head1441 H --head1442 H --base B --develop D --scratch S --out DIR   the COMPOSITION in both orders (git merge-file -p on
             extracted blobs, KEEP-BOTH resolution in numeric order), flow numbering, next free flow number on develop, html_docs_matrix on the
             composed tree. Records clean/conflict, the hunks, the resolution diff.
  --selftest
rc 0 / 1 (a FAIL: plant not landed, restore failed, HEAD row not green, CONTROL red, an all-green tamper, LOAD failure where a count was
expected, a base/head output DIFFERENCE) / 2 refused. NOT RUN is reported by name and is never a pass."""
import difflib, hashlib, json, os, re, shutil, signal, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate80 import K, PR, git, git_bytes, blob, req, opt, wgit, must_be_outside, extract, resolvable

HERE = os.path.dirname(os.path.abspath(__file__))
P41 = PR(1441); P42 = PR(1442)
RF = P41['route_file']; TF = P41['test_file']; OD = K['originate_dir']; DD = K['dev_dir']


def sha(b): return hashlib.sha256(b).hexdigest()
def now(): return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
def w(path, data):
    must_be_outside(path, 'write'); os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'wb').write(data if isinstance(data, bytes) else data.encode('utf-8'))


def write_checked(wt, rel, data):
    p = os.path.join(wt, rel); must_be_outside(p, 'write'); open(p, 'wb').write(data)
    if sha(open(p, 'rb').read()) != sha(data): raise SystemExit('PLANT NOT LANDED: %s' % rel)
    return p


def run(cmd, cwd=None, env=None, timeout=900, stdin=None):
    """-> (rc, out, err, timed_out). The child runs in its OWN process group; a timeout kills the group (a /dev/zero hang leaves no stray cat)."""
    e = dict(os.environ); e.update(env or {}); e.pop('GIT_SSH_COMMAND', None)
    p = subprocess.Popen(cmd, cwd=cwd, env=e, stdin=(subprocess.PIPE if stdin is not None else subprocess.DEVNULL), stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    try:
        o, er = p.communicate(input=(stdin.encode() if stdin is not None else None), timeout=timeout); to = False
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL); o, er = p.communicate(); to = True
    return p.returncode, o.decode('utf-8', 'replace'), er.decode('utf-8', 'replace'), to


# ---------------- jest (#1441) ----------------
TITLE_RX = re.compile(r'^(RED|control) (KS-\d+) ([A-Z]\d?)\b[: ]*(.*)$')


def cell_key(title, seen):
    m = TITLE_RX.match(title)
    if not m: k = title[:60]
    else:
        lab = re.match(r'^((?:GET|POST) \S+):', m.group(4))
        k = '%s %s %s%s' % (m.group(1), m.group(2), m.group(3), (' ' + lab.group(1)) if lab else '')
    n = seen.get(k, 0); seen[k] = n + 1
    return k if n == 0 else '%s #%d' % (k, n + 1)


def read_jest(json_path):
    if not os.path.isfile(json_path): return {'load_failed': True, 'tests': 0, 'passed': 0, 'failed': 0, 'skipped': 0, 'suites': 0, 'failed_suites': 0, 'cells': {}, 'message': 'NO JSON WRITTEN', 'fail_msgs': {}}
    d = json.load(open(json_path)); tr = d.get('testResults') or []
    ar = [(r, a) for r in tr for a in r.get('assertionResults') or []]
    load_failed_suites = [r.get('name', '?') for r in tr if 'Test suite failed to run' in (r.get('message') or '') or (not r.get('assertionResults') and r.get('status') == 'failed')]
    seen = {}; cells = {}; msgs = {}
    for r, a in ar:
        k = cell_key(a['title'], seen); cells[k] = a['status']
        if a['status'] == 'failed': msgs[k] = ' '.join((a.get('failureMessages') or [''])[0].split())[:260]
    return {'load_failed': bool(load_failed_suites) or not ar, 'load_failed_suites': load_failed_suites, 'tests': len(ar),
            'passed': sum(1 for _, a in ar if a['status'] == 'passed'), 'failed': sum(1 for _, a in ar if a['status'] == 'failed'),
            'skipped': sum(1 for _, a in ar if a['status'] in ('pending', 'todo', 'skipped')), 'suites': len(tr),
            'failed_suites': sum(1 for r in tr if r.get('status') == 'failed'), 'cells': cells, 'fail_msgs': msgs,
            'message': ' | '.join((r.get('message') or '')[:200] for r in tr if r.get('message'))}


def jest(wt, rels, json_path, env_extra=None, timeout=1200):
    od = os.path.join(wt, OD); bin_ = os.path.join(wt, DD, 'node_modules', '.bin', 'jest')
    cmd = ['node', bin_, '--config', os.path.join(od, 'jest.config.js'), '--ci', '--json', '--outputFile=' + json_path]
    if rels: cmd += ['--runTestsByPath'] + [os.path.join(wt, r) for r in rels]
    return run(cmd, cwd=od, env=env_extra, timeout=timeout)


def porcelain(wt):
    return subprocess.run(['git', '-C', wt, 'status', '--porcelain', '--untracked-files=all', '--', '.', ':!Blockchain/Dev/**/node_modules', ':!Blockchain/Dev/packages/shared/dist'],
                          capture_output=True, text=True).stdout.strip()


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


def setup1441(clone, head, wt, logd):
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


PRED_CELLS = {('base', 'head'): 'reds D0 D4 D3 (3 of 11), 8 green', ('head', 'head'): '11/11 green', ('base', 'base'): '8/8 green (6 definitions; the two it.each expand per route)',
              ('head', 'base'): 'DRAFT says 8/8 where C0 is replaced; the drafter\'s own reading: base tests include control C0 (pins the swallow), which a head route should RED — MEASURE'}


def plant(wt, clone, rev_of, route, tests):
    planted = []
    for rel, which in ((RF, route), (TF, tests)):
        data = git_bytes(clone, rev_of[which], rel); write_checked(wt, rel, data); planted.append((rel, which, sha(data)))
    return planted


def restore(wt, clone, head):
    bad = []
    for rel in (RF, TF):
        data = git_bytes(clone, head, rel); write_checked(wt, rel, data)
        if sha(open(os.path.join(wt, rel), 'rb').read()) != sha(data): bad.append(rel)
    return bad


def cells1441(wt, clone, head, base, route, tests, out):
    must_be_outside(out, 'out dir'); os.makedirs(out, exist_ok=True); rev_of = {'base': base, 'head': head}
    pl = plant(wt, clone, rev_of, route, tests)
    for rel, which, s in pl: print('PLANT LANDED %s from %s sha256/16 %s' % (rel.split('/')[-1], which, s[:16]))
    jp = os.path.join(out, 'cells_route%s_tests%s.json' % (route, tests))
    rc, o, e, to = jest(wt, [TF], jp); w(jp.replace('.json', '.out'), o); w(jp.replace('.json', '.err'), e)
    r = read_jest(jp); bad = restore(wt, clone, head)
    print('%s jest rc %d%s | LOAD-FAILED %s | tests %d passed %d failed %d | restored by sha: %s | porcelain %r' % (now(), rc, ' TIMEOUT' if to else '', r['load_failed'], r['tests'], r['passed'], r['failed'], not bad, porcelain(wt)[:100]))
    for k, v in sorted(r['cells'].items()): print('  %-8s %s%s' % (v.upper(), k, ('  :: ' + r['fail_msgs'][k][:200]) if k in r['fail_msgs'] else ''))
    print('PREDICTION (route %s, tests %s): %s -- measured reds %s' % (route, tests, PRED_CELLS[(route, tests)], sorted(k for k, v in r['cells'].items() if v == 'failed')))
    return 1 if (r['load_failed'] or bad) else 0


def suite1441(wt, clone, head, base, route, out):
    must_be_outside(out, 'out dir'); os.makedirs(out, exist_ok=True); rev_of = {'base': base, 'head': head}
    if route == 'base': pl = plant(wt, clone, rev_of, 'base', 'base'); [print('PLANT LANDED %s from base sha256/16 %s' % (r.split('/')[-1], s[:16])) for r, _, s in pl]
    jp = os.path.join(out, 'suite_whole_%s.json' % route)
    rc, o, e, to = jest(wt, [], jp, timeout=1800); w(jp.replace('.json', '.out'), o); w(jp.replace('.json', '.err'), e)
    r = read_jest(jp); bad = restore(wt, clone, head)
    print('%s WHOLE originate suite at %s: jest rc %d%s | suites %d (failed %d, LOAD-FAILED %s) | tests %d passed %d failed %d skipped %d | restored: %s' % (
        now(), route, rc, ' TIMEOUT' if to else '', r['suites'], r['failed_suites'], r.get('load_failed_suites') or 0, r['tests'], r['passed'], r['failed'], r['skipped'], not bad))
    for k, v in r['cells'].items():
        if v == 'failed': print('  RED %s' % k)
    print('PREDICTION (the READY): base 1096/1096, head 1099/1099 (tests passed / total). Measured here: %d/%d' % (r['passed'], r['tests']))
    return 0 if (rc == 0 and not r['load_failed'] and not bad) else 1


def tsc1441(wt, out):
    must_be_outside(out, 'out dir'); os.makedirs(out, exist_ok=True)
    tsc = os.path.join(wt, DD, 'node_modules', '.bin', 'tsc')
    rc, o, e, to = run(['node', tsc, '--noEmit', '-p', os.path.join(wt, OD, 'tsconfig.json')], cwd=os.path.join(wt, OD), timeout=900)
    w(os.path.join(out, 'tsc.out'), o); w(os.path.join(out, 'tsc.err'), e)
    print('%s tsc --noEmit -p %s/tsconfig.json rc %d%s (stdout %d B, stderr %d B)' % (now(), OD, rc, ' TIMEOUT' if to else '', len(o), len(e)))
    return 0 if rc == 0 else 1


def probe32(wt, clone, head, base, route, out):
    must_be_outside(out, 'out dir'); os.makedirs(out, exist_ok=True); rev_of = {'base': base, 'head': head}
    pl = plant(wt, clone, rev_of, route, 'head'); [print('PLANT LANDED %s from %s' % (r.split('/')[-1], wch)) for r, wch, _ in pl]
    src = git_bytes(clone, head, TF).decode('utf-8'); blk = open(os.path.join(HERE, 'probe_block_gate80.ts.txt'), encoding='utf-8').read()
    rel = os.path.join(os.path.dirname(TF), 'gate80-probe.test.ts'); facts = os.path.join(out, 'probe_facts_route%s.jsonl' % route)
    if os.path.exists(facts): os.rename(facts, facts + '.prev.%s' % int(time.time()))
    write_checked(wt, rel, (src + blk).encode('utf-8'))
    jp = os.path.join(out, 'probe_route%s.json' % route)
    rc, o, e, to = jest(wt, [rel], jp, env_extra={'G80_PROBE_OUT': facts}); w(jp.replace('.json', '.out'), o); w(jp.replace('.json', '.err'), e)
    r = read_jest(jp)
    qdir = os.path.join(out, 'quarantine_probe'); os.makedirs(qdir, exist_ok=True); shutil.move(os.path.join(wt, rel), os.path.join(qdir, 'gate80-probe_route%s.test.ts' % route))
    bad = restore(wt, clone, head); pc = porcelain(wt)
    print('%s probe jest rc %d%s | LOAD-FAILED %s | tests %d passed %d failed %d | probe moved to %s | restored %s | porcelain clean: %s' % (now(), rc, ' TIMEOUT' if to else '', r['load_failed'], r['tests'], r['passed'], r['failed'], qdir, not bad, pc == ''))
    ran = 0
    for l in open(facts) if os.path.isfile(facts) else []:
        d = json.loads(l); ran += 1
        if d['id'] == 'P-32HEX':
            for lab, v in d['results'].items(): print('  P-32HEX route %-4s %-32s status %s dbCalls %s bound %s body %s' % (route, lab, v['status'], v['dbCalls'], v['boundValues'], v['body'][:70]))
        else: print('  %s route %s %s' % (d['id'], route, json.dumps({k: v for k, v in d.items() if k != 'id'})[:420]))
    print('PROBE facts recorded: %d record(s) in %s (FACTS; the gate rules)' % (ran, facts))
    return 0 if (not r['load_failed'] and ran >= 3 and not bad and pc == '') else 1


GUARD = "    if (!UUID_PATTERN.test(req.params.id)) {\n      return res.json({ success: true, deliveries: [] });\n    }\n"
IDFMT = "    if (!/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(req.params.id)) {\n"
RET = "return res.json({ success: true, deliveries: [] });"
TAMPERS41 = [
    ('T1', 'remove ONLY the UUID_PATTERN early return', [(GUARD, '')], ['RED KS-1345 D4']),
    ('T2', 'the early return answers 200 with the rows key MISSING', [(RET, 'return res.json({ success: true });')], ['RED KS-1345 D4']),
    ('T3', 'the guard placed BEFORE the id-format regex (a malformed id would answer 200 [] instead of 400)', [(GUARD, ''), (IDFMT, GUARD + IDFMT)], []),
    ('T4', 'the early return answers 404', [(RET, 'return res.status(404).json({ success: true, deliveries: [] });')], ['RED KS-1345 D4']),
    ('T5', 'the swallow put back on the query', [("      LIMIT 50\n    `;\n\n    res.json({ success: true, deliveries: rows });", "      LIMIT 50\n    `.catch(() => []);\n\n    res.json({ success: true, deliveries: rows });")], ['RED KS-1345 D0', 'RED KS-1345 D3']),
    ('T6', 'the route answers err.message in the 500 body instead of fail500', [("    fail500(res, 'Webhook delivery history read failed (GET /api/webhooks/:id/deliveries)', err);", "    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });")], ['RED KS-1345 D0']),
]


def tamper1441(wt, clone, head, base, out, only):
    must_be_outside(out, 'out dir'); os.makedirs(out, exist_ok=True); rc = 0
    head_src = git_bytes(clone, head, RF).decode('utf-8'); rows = [('HEAD', 'no change (all green)', None, []), ('CONTROL', 'a no-op comment appended (all green)', 'NOOP', [])] + [(a, b, c, d) for a, b, c, d in TAMPERS41]
    t_src = git_bytes(clone, head, TF); write_checked(wt, TF, t_src)
    for tid, name, edits, pred in rows:
        if only and tid not in only and tid not in ('HEAD', 'CONTROL'): continue
        try:
            if edits is None: new = head_src
            elif edits == 'NOOP': new = head_src + '\n// gate80-noop\n'
            else: new = apply_edits(head_src, edits)
        except SystemExit as e:
            print('%s %-8s TAMPER-INVALID: %s' % (now(), tid, e)); rc = 1; continue
        ok_land = True if edits is None else landed(head_src, new, [] if edits == 'NOOP' else edits)
        if edits == 'NOOP': ok_land = new != head_src and '// gate80-noop' in new
        write_checked(wt, RF, new.encode('utf-8'))
        jp = os.path.join(out, 'tamper_%s.json' % tid); r_rc, o, e, to = jest(wt, [TF], jp); w(jp.replace('.json', '.out'), o); w(jp.replace('.json', '.err'), e)
        r = read_jest(jp); reds = sorted(k for k, v in r['cells'].items() if v == 'failed')
        write_checked(wt, RF, head_src.encode('utf-8')); back = sha(open(os.path.join(wt, RF), 'rb').read()) == sha(head_src.encode())
        if r['load_failed']: verdict = 'TAMPER-INVALID (suite failed to LOAD: %s)' % r['message'][:120]; rc = 1
        elif tid == 'HEAD': verdict = 'OK all green' if not reds else 'FAIL: HEAD row has reds %s' % reds; rc |= 0 if not reds else 1
        elif tid == 'CONTROL': verdict = 'OK all green (harness quiet)' if not reds else 'FAIL: the no-op reds %s: the harness is noisy' % reds; rc |= 0 if not reds else 1
        else:
            verdict = ('ALL-GREEN: NO CELL CATCHES THIS TAMPER (a finding to rule)' if not reds else 'caught by %s' % reds) + ' | drafter prediction %s: %s' % (pred or 'none', 'MATCH' if sorted(pred) == reds else 'DIFFER')
        print('%s %-8s %-70s landed %s restored %s | tests %d failed %d | %s' % (now(), tid, name[:70], ok_land, back, r['tests'], r['failed'], verdict))
        for k in reds: print('      RED %s :: %s' % (k, r['fail_msgs'].get(k, '')[:200]))
        if not ok_land or not back: rc = 1
    print('porcelain after the tamper rows: %r' % porcelain(wt)[:120]); return rc


# ---------------- #1442 shell legs ----------------
SHELL_PATHS = ['systemTest', 'Blockchain/Dev/scripts', '.githooks'] + list(K['known_develop_overlap'][:2])   # the two docs: html_docs_matrix reads them
GATE = P42['gate_script']; SUITE = P42['suite']
BASHES = [('/bin/bash', '3.2 macOS'), ('/opt/homebrew/bin/bash', 'Homebrew')]


def tree(clone, rev, dest):
    if os.path.exists(dest): return dest
    n = extract(clone, rev, SHELL_PATHS, dest); return dest


def pcounts(text):
    m = re.search(r'(\d+) passed, (\d+) failed', text); return (int(m.group(1)), int(m.group(2))) if m else None


def run_suite(bash, tree_dir, suite_rel, gate_override=None, timeout=120):
    env = {'PACKAGE_FORMAT_GATE_SH': gate_override} if gate_override else {}
    rc, o, e, to = run([bash, os.path.join(tree_dir, suite_rel)], cwd=tree_dir, env=env, timeout=timeout)
    return rc, o, e, to, pcounts(o + e)


def suite1442(clone, head, base, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    th, tb = tree(clone, head, os.path.join(scratch, 'tree_head')), tree(clone, base, os.path.join(scratch, 'tree_base'))
    hs = git_bytes(clone, head, GATE); bs = git_bytes(clone, base, GATE)
    gh_ = os.path.join(scratch, 'gate_head.sh'); gb = os.path.join(scratch, 'gate_base.sh'); gn = os.path.join(scratch, 'gate_head_noredirect.sh')
    w(gh_, hs); w(gb, bs)
    txt = hs.decode(); a = 'npm run --silent format:check < /dev/null 2>&1'
    try: nr = apply_edits(txt, [(a, 'npm run --silent format:check 2>&1')])
    except SystemExit as e: print('TAMPER-INVALID', e); return 1
    w(gn, nr)
    for lab, p, want in (('gate_head.sh', gh_, hs), ('gate_base.sh', gb, bs), ('gate_head_noredirect.sh', gn, nr.encode())):
        print('PLANT LANDED %s sha256/16 %s (== %s)' % (lab, sha(open(p, 'rb').read())[:16], 'the blob' if lab != 'gate_head_noredirect.sh' else 'head with ONLY the redirect removed: != head %s, `< /dev/null` count %d' % (sha(open(gn, 'rb').read()) != sha(hs), nr.count('< /dev/null'))))
    print('assert: noredirect differs from head and base-script differs from head: %s %s' % (sha(nr.encode()) != sha(hs), sha(bs) != sha(hs)))
    ways = [('A (script HEAD, suite HEAD)', gh_, (9, 0), 0), ('B (script BASE, suite HEAD)', gb, 'READY: 6 passed / 3 failed rc 1', 1), ('C (script HEAD with the redirect REMOVED, suite HEAD)', gn, 'must fail like B (the suite is what fails)', 1)]
    for bash, bl in BASHES:
        if not os.path.isfile(bash): print('NOT RUN: %s (%s) is not present on this machine' % (bash, bl)); continue
        ver = run([bash, '--version'])[1].split('\n')[0]
        for lab, g, want, wrc in ways:
            rc, o, e, to, c = run_suite(bash, th, SUITE, g)
            w(os.path.join(out, 'suite1442_%s_%s.out' % (bl.split()[0], lab[0])), o); w(os.path.join(out, 'suite1442_%s_%s.err' % (bl.split()[0], lab[0])), e)
            reds = [l for l in o.split('\n') if l.startswith('FAIL')]
            print('%s [%s | %s] %-52s rc %d%s counts %s (want %s, rc %s)' % (now(), bash, ver[:40], lab, rc, ' TIMEOUT' if to else '', c, want, wrc))
            if lab[0] in 'BC':
                for l in reds: print('      RED %s' % l[:150])
            if lab[0] == 'A' and (c != (9, 0) or rc != 0): rc_all = 1
            if lab[0] in 'BC' and rc == 0: rc_all = 1
    print('(script head, suite ABSENT) n/a by the READY: the new suite exists only in the head tree')
    sibs = sorted(p for p in os.listdir(os.path.join(th, 'systemTest', '__tests__')) if p.endswith('.test.sh') and p != os.path.basename(SUITE))
    for rev, td in (('base', tb), ('head', th)):
        for s in sibs:
            body = open(os.path.join(td, 'systemTest', '__tests__', s), encoding='utf-8', errors='replace').read()
            touches = 'check-package-format' in body or 'PACKAGE_FORMAT_GATE_SH' in body
            if not touches and s != 'html_docs_matrix.test.sh': continue
            rc, o, e, to, c = run_suite('/bin/bash', td, 'systemTest/__tests__/' + s, None, timeout=300)
            w(os.path.join(out, 'sibling_%s_%s.out' % (rev, s)), o); w(os.path.join(out, 'sibling_%s_%s.err' % (rev, s)), e)
            print('%s SIBLING %-4s %-52s sources-gate %-5s rc %d%s counts %s' % (now(), rev, s, touches, rc, ' TIMEOUT' if to else '', c))
    for rev, td in (('base', tb), ('head', th)):
        rc, o, e, to = run(['/bin/bash', os.path.join(td, 'Blockchain/Dev/scripts/run-shell-suites.sh'), '--list'], cwd=td)
        n = len([l for l in o.split('\n') if l.strip()])
        print('%s run-shell-suites.sh --list at %s: rc %d, %d suite line(s) (READY: 73 -> 74); the new suite listed: %s' % (now(), rev, rc, n, 'ks998_format_gate_stdin_isolated' in o))
    return rc_all


PKGS = K['real_packages']


def realpkg(clone, head, base, scratch, out, install):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True)
    th = tree(clone, head, os.path.join(scratch, 'tree_head'))
    gb = os.path.join(scratch, 'gate_base.sh'); w(gb, git_bytes(clone, base, GATE))
    inst = {}
    if install:
        for p in PKGS:
            rc, o, e, to = run(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=os.path.join(th, 'systemTest', p), timeout=900)
            w(os.path.join(out, 'npm_ci_%s.out' % p), o); w(os.path.join(out, 'npm_ci_%s.err' % p), e); inst[p] = rc
            print('%s npm ci --ignore-scripts systemTest/%s rc %d%s%s' % (now(), p, rc, ' TIMEOUT' if to else '', ('' if rc == 0 else ' :: ' + e.strip().split('\n')[-1][:160])))
    ok_pk = []
    for p in PKGS:
        b = os.path.join(th, 'systemTest', p, 'node_modules', '.bin', 'prettier'); ex = os.path.isfile(b) and os.access(b, os.X_OK)
        print('ASSERT systemTest/%s/node_modules/.bin/prettier executable: %s' % (p, ex)); ok_pk.append(ex)
    if not all(ok_pk):
        print('REAL PACKAGES: NOT RUN (F) — %d of %d packages lack an executable prettier%s. The gate would SKIP them and a skip is not a check.' % (ok_pk.count(False), len(PKGS), '' if install else ' (run with --install, X9)'))
        return 1
    for lab in ('--list', '--all'):
        res = {}
        for sl, sp in (('base', gb), ('head', os.path.join(th, GATE))):
            # the script locates REPO_ROOT from its own path: copy it into the head tree's scripts dir under a distinct name
            cp = os.path.join(th, 'systemTest', 'scripts', 'check-package-format.%s.sh' % sl); w(cp, open(sp, 'rb').read())
            rc, o, e, to = run(['/bin/bash', cp, lab], cwd=th, timeout=600)
            w(os.path.join(out, 'gate_%s_%s.out' % (sl, lab.strip('-'))), o); w(os.path.join(out, 'gate_%s_%s.err' % (sl, lab.strip('-'))), e)
            res[sl] = (rc, o, e); print('%s gate %s %s: rc %d%s | stdout %d lines | stderr %d lines | last stdout/stderr: %r %r' % (now(), sl, lab, rc, ' TIMEOUT' if to else '', len(o.split('\n')) - 1, len(e.split('\n')) - 1, o.strip().split('\n')[-1][:80] if o.strip() else '', e.strip().split('\n')[-1][:80] if e.strip() else ''))
        same = res['base'] == res['head']
        print('REAL PACKAGES %s: base-script output == head-script output (rc, stdout, stderr): %s%s' % (lab, same, '' if same else '  <- A DIFFERENCE IS A FINDING'))
    for p in PKGS:
        pj = json.load(open(os.path.join(th, 'systemTest', p, 'package.json'))); fc = (pj.get('scripts') or {}).get('format:check', '')
        reads = bool(re.search(r'(^|\s)-(\s|$)|--stdin|\bcat\b|\bread\b|<<', fc))
        print('STDIN-READER CENSUS systemTest/%s format:check = %r -> could read stdin: %s' % (p, fc, reads))
    # the honest control: a fixture package that drains stdin, sorted BEFORE the real ones, in the SAME tree
    fx = os.path.join(th, 'systemTest', '0drain'); os.makedirs(os.path.join(fx, 'node_modules', '.bin'), exist_ok=True)
    w(os.path.join(fx, 'package.json'), '{ "name": "fixture-0drain", "version": "0.0.0", "scripts": { "format:check": "cat >/dev/null; exit 0" } }\n')
    w(os.path.join(fx, 'node_modules', '.bin', 'prettier'), '#!/bin/sh\nexit 0\n'); os.chmod(os.path.join(fx, 'node_modules', '.bin', 'prettier'), 0o755)
    paths = '\n'.join(['systemTest/0drain/x.ts'] + ['systemTest/%s/package.json' % p for p in PKGS]) + '\n'
    out2 = {}
    for sl in ('base', 'head'):
        cp = os.path.join(th, 'systemTest', 'scripts', 'check-package-format.%s.sh' % sl)
        rc, o, e, to = run(['/bin/bash', cp], cwd=th, stdin=paths, timeout=600)
        w(os.path.join(out, 'control_%s.out' % sl), o); w(os.path.join(out, 'control_%s.err' % sl), e)
        m = re.search(r'(\d+) package\(s\) checked, (\d+) skipped, (\d+) failed', o + e)
        out2[sl] = (rc, m.groups() if m else None); print('%s CONTROL (fixture drainer + %d real packages, ONE run) script %s: rc %d%s, %s' % (now(), len(PKGS), sl, rc, ' TIMEOUT' if to else '', m.group(0) if m else 'NO SUMMARY LINE'))
    miss = out2['base'][1] is not None and out2['head'][1] is not None and int(out2['head'][1][0]) > int(out2['base'][1][0])
    print('CONTROL RESULT: head checked MORE packages than base in the same run: %s (base %s, head %s) — the redirect is what keeps the list' % (miss, out2['base'][1], out2['head'][1]))
    return 0 if miss else 1


def hookpath(clone, head, base, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True)
    th = tree(clone, head, os.path.join(scratch, 'tree_head')); sc = os.path.join(th, GATE); rc_all = 0
    own = sorted(P42['numstat']); ctl = ['systemTest/performance/package.json']
    ho = open(os.path.join(th, '.githooks', 'pre-push'), encoding='utf-8').read()
    sel = [l.strip() for l in ho.split('\n') if 'check-package-format' in l or "^Blockchain/Dev/" in l][:6]
    print('HOOK READ (.githooks/pre-push at the head): the lines that decide: %s' % sel)
    for lab, paths, want in (('the PR\'s OWN four paths', own, 'NONE selected, silent, rc 0'), ('CONTROL one path under a real package', ctl, 'one package selected (SKIP if deps are not installed, else format:check OK/FAILED)')):
        rc, o, e, to = run(['/bin/bash', sc], cwd=th, stdin='\n'.join(paths) + '\n', timeout=300)
        w(os.path.join(out, 'hook_%s.out' % ('own' if paths is own else 'ctl')), o); w(os.path.join(out, 'hook_%s.err' % ('own' if paths is own else 'ctl')), e)
        pk = [p for p in PKGS if ('systemTest/%s' % p) in (o + e)]
        print('%s %-40s rc %d | stdout %r | stderr %r | packages named: %s | predicted: %s' % (now(), lab, rc, o.strip()[:100], e.strip()[:160], pk, want))
        if paths is own and (o.strip() or e.strip() or rc): rc_all = 1
        if paths is ctl and not pk: rc_all = 1
    print('the live hook adds what this did not run: the real `git push` path (upstream diff, fetch of the base), which the gate may not trigger')
    return rc_all


TAMPERS42 = [
    ('U1', '`< /dev/null` -> `< /dev/zero` (an endless stdin: a draining package hangs)', [('format:check < /dev/null 2>&1', 'format:check < /dev/zero 2>&1')], 'hang/TIMEOUT or red'),
    ('U2', 'drop `2>&1` (stderr no longer lands in $out)', [('format:check < /dev/null 2>&1)"', 'format:check < /dev/null)"')], 'unknown: the fixture prints its [warn] on STDOUT'),
    ('U3', 'the redirect on `cd` only (npm still inherits the loop stdin)', [('cd "$dir" && npm run --silent format:check < /dev/null 2>&1', 'cd "$dir" < /dev/null && npm run --silent format:check 2>&1')], 'reds like base (6/3)'),
    ('U4', 'the redirect on the assignment, outside $( ... )', [('npm run --silent format:check < /dev/null 2>&1)"', 'npm run --silent format:check 2>&1)" < /dev/null')], 'reds like base (6/3)'),
    ('U5', 'no redirect at all (== the base line)', [('npm run --silent format:check < /dev/null 2>&1', 'npm run --silent format:check 2>&1')], 'reds like base (6/3)'),
]


def tamper1442(clone, head, base, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    th = tree(clone, head, os.path.join(scratch, 'tree_head')); hs = git_bytes(clone, head, GATE).decode()
    r, o, e, to, c = run_suite('/bin/bash', th, SUITE, os.path.join(th, GATE)); print('%s HEAD row (the real head script): rc %d counts %s (must be 9,0)' % (now(), r, c)); rc_all |= 0 if c == (9, 0) else 1
    for tid, name, edits, pred in TAMPERS42:
        try: new = apply_edits(hs, edits)
        except SystemExit as e: print('%s %s TAMPER-INVALID: %s' % (now(), tid, e)); rc_all = 1; continue
        ok = landed(hs, new, edits); p = os.path.join(scratch, 'tamper_%s.sh' % tid); w(p, new)
        r, o, e, to, c = run_suite('/bin/bash', th, SUITE, p, timeout=20 if tid == 'U1' else 120)
        w(os.path.join(out, 'tamper1442_%s.out' % tid), o); w(os.path.join(out, 'tamper1442_%s.err' % tid), e)
        reds = [l[:120] for l in o.split('\n') if l.startswith('FAIL')]
        v = 'TIMEOUT (a hang, process group killed)' if to else ('ALL-GREEN: NO CELL CATCHES IT (a finding to rule)' if r == 0 and c == (9, 0) else 'caught: rc %d counts %s' % (r, c))
        print('%s %-3s %-72s landed %s | %s | drafter prediction: %s' % (now(), tid, name[:72], ok, v, pred))
        for l in reds[:4]: print('      RED %s' % l)
        if not ok: rc_all = 1
    return rc_all


# ---------------- docs composition ----------------
def merge_file(cur, basef, other):
    rc, o, e, to = run(['git', 'merge-file', '-p', '-L', 'ours', '-L', 'base', '-L', 'theirs', cur, basef, other], timeout=60)
    return rc, o   # rc = number of conflicts (>0), 0 clean, <0 error


def insertion(basetxt, headtxt):
    la, lb = basetxt.split('\n'), headtxt.split('\n')
    ops = [x for x in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes() if x[0] != 'equal']
    if len(ops) != 1 or ops[0][0] != 'insert': raise SystemExit('not a pure insertion: %s' % ops[:3])
    _, i1, _, j1, j2 = ops[0]; return i1, lb[j1:j2]


def compose_keep_both(basetxt, frags):
    """frags: [(first_pr_fragment_lines, second...)] in NUMERIC order, all inserted at the same base position; refuses differing positions."""
    la = basetxt.split('\n'); pos = {p for p, _ in frags}
    if len(pos) != 1: raise SystemExit('fragments insert at different base positions %s: not a tail keep-both' % sorted(pos))
    i = pos.pop(); ins = [l for _, f in frags for l in f]
    return '\n'.join(la[:i] + ins + la[i:])


def flow_numbers(txt): return [int(x) for x in re.findall(r'<h2>(\d+)\.', txt)]


def docs(clone, h1, h2, base, develop, scratch, out):
    must_be_outside(scratch, 'scratch'); must_be_outside(out, 'out'); os.makedirs(out, exist_ok=True); rc_all = 0
    composed = {}; composed_rev = {}; DOC = K['known_develop_overlap'][:2]
    for d in DOC:
        b = git_bytes(clone, base, d).decode('utf-8'); a = git_bytes(clone, h1, d).decode('utf-8'); c = git_bytes(clone, h2, d).decode('utf-8'); dv = git_bytes(clone, develop, d).decode('utf-8')
        (ia, fa), (ic, fc) = insertion(b, a), insertion(b, c)
        nm = os.path.basename(d); sd = os.path.join(scratch, 'docs_' + nm[:12]); os.makedirs(sd, exist_ok=True)
        for k, v in (('base', b), ('1441', a), ('1442', c)): w(os.path.join(sd, k + '.html'), v)
        print('%s %s: #1441 inserts %d line(s) at base line %d; #1442 inserts %d line(s) at base line %d; same position: %s' % (now(), nm, len(fa), ia + 1, len(fc), ic + 1, ia == ic))
        for order, (x, y, xl, yl) in (('A (1441 then 1442)', ('1441', '1442', a, c)), ('B (1442 then 1441)', ('1442', '1441', c, a))):
            rc, o = merge_file(os.path.join(sd, x + '.html'), os.path.join(sd, 'base.html'), os.path.join(sd, y + '.html'))
            hunks = o.count('<<<<<<< ours'); w(os.path.join(out, 'merge_%s_%s.txt' % (order[0], nm)), o)
            print('  ORDER %s textual merge (git merge-file): %s, %d conflict hunk(s)' % (order, 'CLEAN' if rc == 0 else ('CONFLICT' if rc > 0 else 'ERROR rc %d' % rc), hunks))
        res = compose_keep_both(b, [(ia, fa), (ic, fc)])   # numeric order: 48. then 49.
        res_rev = compose_keep_both(b, [(ic, fc), (ia, fa)])
        w(os.path.join(sd, 'composed.html'), res); w(os.path.join(sd, 'composed_reverse_numeric.html'), res_rev)
        both = all(res.count('\n'.join(f)) == 1 for f in (fa, fc))
        fn = flow_numbers(res); fb, fd = flow_numbers(b), flow_numbers(dv)
        print('  KEEP-BOTH resolution (numeric order 48. then 49.): both fragments present once: %s | flow numbers tail %s (base tail %s, develop tail %s) | the resolution diff vs base = %d inserted line(s), 0 removed' % (both, fn[-4:], fb[-3:], fd[-3:], len(fa) + len(fc)))
        print('  NEXT FREE FLOW NUMBER on develop %s: %s' % (develop[:12], (max(fd) + 1) if fd else 'n/a'))
        if not both: rc_all = 1
        composed[d] = res; composed_rev[d] = res_rev
        if d == DOC[0]:
            nums = flow_numbers(res); ok = nums.count(48) == 1 and nums.count(49) == 1 and nums.index(48) < nums.index(49)
            print('  FLOW NUMBERING: 48. once, 49. once, 48. before 49.: %s' % ok); rc_all |= 0 if ok else 1
    # html_docs_matrix on the composed tree (base tree + both composed docs) and, as the control, on each single-PR head tree and the base tree
    for lab, rev, comp in (('base tree (control)', base, False), ('#1441 head tree', h1, False), ('#1442 head tree', h2, False), ('COMPOSED (base + both docs, keep-both)', base, True), ('COMPOSED-REVERSE (49. block before 48.)', base, 'rev')):
        td = os.path.join(scratch, 'mx_' + re.sub(r'\W+', '_', lab)[:14]); tree(clone, rev, td)
        if comp:
            for d, txt in (composed_rev if comp == 'rev' else composed).items(): w(os.path.join(td, d), txt)
        rc, o, e, to, c = run_suite('/bin/bash', td, K['docs_composition']['matrix_suite'], None, timeout=300)
        w(os.path.join(out, 'matrix_%s.out' % re.sub(r'\W+', '_', lab)[:14]), o); w(os.path.join(out, 'matrix_%s.err' % re.sub(r'\W+', '_', lab)[:14]), e)
        inval = 'is missing' in (o + e)
        print('%s html_docs_matrix on %-42s rc %d%s counts %s%s' % (now(), lab, rc, ' TIMEOUT' if to else '', c, '  TREE-INVALID (a doc is missing from the extracted tree: not a measurement)' if inval else ''))
        if inval: rc_all = 1
        if comp == True and (rc != 0 or not c or c[1] != 0): rc_all = 1
        if comp == 'rev': print('   (the reverse-placement result is REPORTED: a red here means the merge seat must keep the numeric order 48. then 49.)')
    # CONTROL: a composition that DROPS a block must be caught by the instrument that checks for both blocks
    a_only = compose_keep_both(git_bytes(clone, base, DOC[0]).decode(), [insertion(git_bytes(clone, base, DOC[0]).decode(), git_bytes(clone, h1, DOC[0]).decode())])
    print('CONTROL: a composition keeping ONLY #1441\'s block reads 49. present = %s (must be False: the both-blocks check can fail)' % (49 in flow_numbers(a_only)))
    rc_all |= 1 if 49 in flow_numbers(a_only) else 0
    return rc_all


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    try: apply_edits('a b a', [('a', 'x')]); rep(False, 'a 2-occurrence anchor was ACCEPTED')
    except SystemExit: rep(True, 'ARM: anchor occurring twice -> refused (tamper not applied)')
    try: apply_edits('a b', [('zz', 'x')]); rep(False, 'an absent anchor was ACCEPTED')
    except SystemExit: rep(True, 'ARM: anchor absent -> refused')
    t = apply_edits('one two', [('two', 'TWO')]); rep(t == 'one TWO' and landed('one two', t, [('two', 'TWO')]), 'a single-occurrence edit applies and reads LANDED')
    rep(not landed('x', 'x', [('a', 'b')]), 'PLANTED no-change reads NOT LANDED')
    for e in (GUARD, IDFMT, RET):
        pass
    sample = "    if (!/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(req.params.id)) {\n      return 1;\n    }\n" + GUARD + "    const db = 1;\n"
    for tid, name, edits, pred in TAMPERS41:
        if tid in ('T1', 'T2', 'T3', 'T4'):
            try: n = apply_edits(sample, edits); rep(n != sample, '%s edit applies exactly once on a head-shaped sample' % tid)
            except SystemExit as e: rep(False, '%s edit REFUSED on the sample: %s' % (tid, e))
    j = {'testResults': [{'name': 'a', 'status': 'passed', 'assertionResults': [{'title': 'RED KS-1345 D0: x', 'status': 'passed'}, {'title': 'RED KS-1345 D4: y', 'status': 'failed', 'failureMessages': ['boom\n at x']}]},
                         {'name': 'b', 'status': 'failed', 'assertionResults': [], 'message': 'Test suite failed to run'}]}
    p = os.path.join(HERE, '_scratch', 'selftest_jest.json'); w(p, json.dumps(j)); r = read_jest(p)
    rep(r['load_failed'] and r['tests'] == 2 and r['failed'] == 1 and r['cells'].get('RED KS-1345 D4') == 'failed', 'jest reader: a suite that failed to LOAD is load_failed (never a count); cell keys read')
    w(p, json.dumps({'testResults': [{'name': 'a', 'status': 'passed', 'assertionResults': [{'title': 'ok', 'status': 'passed'}]}]})); rep(not read_jest(p)['load_failed'], 'jest reader: a clean file is not load_failed')
    rep(read_jest(os.path.join(HERE, '_scratch', 'does-not-exist.json'))['load_failed'], 'jest reader: NO JSON WRITTEN reads load_failed (never a green)')
    seen = {}; rep(cell_key('control KS-1341 C: a', seen) != cell_key('control KS-1341 C: b', seen), 'cell keys: two titles with the same prefix get distinct keys')
    rep(pcounts('x\nks998: 9 passed, 0 failed\n') == (9, 0) and pcounts('nothing') is None, 'pcounts reads "N passed, M failed" and nothing else')
    base = 'x\n</body>\n'
    ia, fa = insertion(base, 'x\nH48\n</body>\n'); ic, fc = insertion(base, 'x\nH49\n</body>\n')
    comp = compose_keep_both(base, [(ia, fa), (ic, fc)])
    rep(ia == ic == 1 and comp == 'x\nH48\nH49\n</body>\n', 'compose_keep_both: two tail insertions compose in numeric order, both present once')
    rep(comp.count('H48') == 1 and compose_keep_both(base, [(ia, fa)]).count('H49') == 0, 'CONTROL: a composition keeping one block reads the other ABSENT (the both-blocks check can fail)')
    try: compose_keep_both(base, [(1, ['a']), (2, ['b'])]); rep(False, 'fragments at different positions were ACCEPTED')
    except SystemExit: rep(True, 'ARM: fragments at different base positions -> refused (not a tail keep-both)')
    try: insertion(base, 'y\n</body>\n'); rep(False, 'a non-insertion was ACCEPTED')
    except SystemExit: rep(True, 'ARM: a replaced base line is not a pure insertion -> refused')
    rep(flow_numbers('<h2>47. a</h2><h2>48. b</h2><h2>49. c</h2>') == [47, 48, 49], 'flow_numbers reads <h2>NN.</h2> headings')
    d = os.path.join(HERE, '_scratch', 'selftest_a'); w(os.path.join(d, 'x'), 'one\ntwo\nthree\n'); w(os.path.join(d, 'y'), 'one\ntwo\nthree\nfour\n'); w(os.path.join(d, 'z'), 'zero\ntwo\nthree\n')
    rc, o = merge_file(os.path.join(d, 'y'), os.path.join(d, 'x'), os.path.join(d, 'z'))
    rep(rc == 0 and o.startswith('zero') and o.rstrip().endswith('four'), 'merge_file: a clean 3-way merge reads rc 0 (the reader of the conflict count works)')
    w(os.path.join(d, 'q'), 'one\nTWO\nthree\n'); w(os.path.join(d, 'r'), 'one\ntwo!\nthree\n')
    rc, o = merge_file(os.path.join(d, 'q'), os.path.join(d, 'x'), os.path.join(d, 'r'))
    rep(rc == 1 and '<<<<<<< ours' in o, 'merge_file: PLANTED same-line edits read rc 1 with a conflict marker (the instrument can see a conflict)')
    rc, o, e, to = run(['sh', '-c', 'cat >/dev/null'], timeout=2, stdin=None); rep(rc == 0 and not to, 'run(): a child with stdin /dev/null returns')
    pre = time.time(); rc, o, e, to = run(['sh', '-c', 'sleep 30'], timeout=1); rep(to and time.time() - pre < 6, 'run(): a hanging child is killed by process group at the timeout (TIMEOUT reported)')
    try: must_be_outside('/Volumes/DevMASTER/!CODING/x/y', 'write'); rep(False, 'a write under !CODING was ACCEPTED')
    except SystemExit: rep(True, 'ARM: a write path under !CODING -> refused (lexical)')
    try: extract('/nonexistent-repo', 'abc', ['x'], '/Volumes/DevMASTER/!CODING/zz'); rep(False, 'extract into !CODING was ACCEPTED')
    except SystemExit: rep(True, 'ARM: extract into a !CODING dest -> refused before any write')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A: print(__doc__); return 2
    try:
        cmd = A[0]
        if cmd == 'setup1441': return setup1441(req(A, '--clone'), req(A, '--head', True), req(A, '--wt'), opt(A, '--log'))
        if cmd in ('cells1441', 'suite1441', 'probe32', 'tamper1441'):
            wt, cl, hd, bs, out = req(A, '--wt'), req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), req(A, '--out')
            if cmd == 'tamper1441': return tamper1441(wt, cl, hd, bs, out, (opt(A, '--only') or '').split(',') if opt(A, '--only') else None)
            route = req(A, '--route')
            if route not in ('base', 'head'): raise SystemExit('REFUSED: --route must be base|head')
            if cmd == 'suite1441': return suite1441(wt, cl, hd, bs, route, out)
            if cmd == 'probe32': return probe32(wt, cl, hd, bs, route, out)
            tests = req(A, '--tests')
            if tests not in ('base', 'head'): raise SystemExit('REFUSED: --tests must be base|head')
            return cells1441(wt, cl, hd, bs, route, tests, out)
        if cmd == 'tsc1441': return tsc1441(req(A, '--wt'), req(A, '--out'))
        if cmd in ('suite1442', 'realpkg', 'hookpath', 'tamper1442'):
            cl, hd, bs, sc, out = req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), req(A, '--scratch'), req(A, '--out')
            if cmd == 'suite1442': return suite1442(cl, hd, bs, sc, out)
            if cmd == 'realpkg': return realpkg(cl, hd, bs, sc, out, '--install' in A)
            if cmd == 'hookpath': return hookpath(cl, hd, bs, sc, out)
            return tamper1442(cl, hd, bs, sc, out)
        if cmd == 'docs':
            return docs(req(A, '--clone'), req(A, '--head1441', True), req(A, '--head1442', True), req(A, '--base', True), req(A, '--develop', True), req(A, '--scratch'), req(A, '--out'))
    except SystemExit as e:
        print(e); return 2
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
