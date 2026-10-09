#!/usr/bin/env python3
"""c3_cells_gate79.py — the CELLS, the TAMPER MATRIX and the PROBES for #1437 (KS-1402), run in YOUR OWN worktree (never under
!CODING: every write path is checked lexically AND by realpath and refused there). NEW in gate79.

  setup   --clone CL --head H --wt WT [--log DIR]
          `git worktree add --detach WT H` in YOUR clone, then in WT/Blockchain/Dev: `npm ci --ignore-scripts` and
          `npm run build --workspace=packages/shared` (dist/index.js ASSERTED — STANDING_LINES :380: without it every suite fails to
          LOAD and still prints a count). Refuses a WT that exists.
  cells   --wt WT --clone CL --head H --base B --route base|head --tests base|head --out DIR
          plants documents.ts (route) and the three test files (tests) FROM THE NAMED REV by content into WT (ks1402 has no base
          blob: --tests base reads it ABSENT, by name), asserts each plant LANDED (sha256 of the file == the blob's), runs jest ONCE
          per file (`--runTestsByPath --json`), RESTORES every planted file to the HEAD blob by content and asserts the sha, and
          prints per file: suites / tests / passed / failed, LOAD-FAILED (never a count), and per ks1402 cell C1..C10 its status.
          The READY's table: (route base, tests head) reds C1 C2 C9 in ks1402, ks739 0/17, ks697 16/17 is (route head, tests base).
  tamper  --wt WT --clone CL --head H --base B --out DIR [--only T1,T2]
          for each kit tamper row: start from the HEAD blob, apply every edit with its anchor asserted EXACTLY ONCE in its scope
          (block = the email-resolution block only; file = the whole file; BASE_BLOB = base's whole documents.ts), assert LANDED
          (sha changed AND each replacement text present), run the ks1402 file, read which cells RED, RESTORE (sha asserted).
          A suite that fails to LOAD is TAMPER-INVALID (never a red). Prints, per row, measured reds vs the READY's reds:
          MATCH / DIFFER, and flags an ALL-GREEN row (a tamper no cell catches). Also a HEAD row (must be all green) and a
          CONTROL row that plants a no-op comment (must be all green: a red there means the harness is noisy).
  probe   --wt WT --clone CL --head H --out DIR
          appends probe_block_gate79.ts.txt to a COPY of the head's ks1402 file as __tests__/gate79-probe.test.ts in WT, runs it with
          G79_PROBE_OUT=<DIR>/probe_facts.jsonl, then MOVES the probe file into DIR (quarantine, never rm) and asserts WT porcelain is
          clean. Prints each probe's facts: P-a1 tenantless caller (what is bound, whom it resolves), P-a2 what the request-db adapter
          binds for an undefined tenant (+ pg's prepareValue(undefined)), P-c cross-tenant vs miss bytes + headers, P-d normalisation
          variants, P-e key-absent on the email path / id path / malformed. FACTS, never a verdict.
  --selftest   the jest-json reader (passed / failed / load-failed), the anchor-once editor (0 and 2 occurrences refuse), the
               scope finder, the MATCH/DIFFER comparator, the forbidden-path refusal.
rc 0 / 1 (a FAIL: plant not landed, restore failed, HEAD row not all green, CONTROL red, an all-green tamper, LOAD failure where a
count was expected) / 2 refused."""
import hashlib, json, os, re, shutil, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate79 import K, git, git_bytes, blob, req, opt, wgit, must_be_outside, handler, block, sha256_16

HERE = os.path.dirname(os.path.abspath(__file__))
RF = K['route_file']; TF = K['test_files']; OD = K['originate_dir']; DD = K['dev_dir']
CELL_RX = re.compile(r'^(C\d+b?)\b')


def sha(b): return hashlib.sha256(b).hexdigest()


def now(): return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def write_checked(wt, rel, data):
    p = os.path.join(wt, rel); must_be_outside(p, 'write')
    open(p, 'wb').write(data)
    got = open(p, 'rb').read()
    if sha(got) != sha(data):
        raise SystemExit('PLANT NOT LANDED: %s' % rel)
    return p


def jest(wt, rel_test, json_path, env_extra=None):
    od = os.path.join(wt, OD); bin_ = os.path.join(wt, DD, 'node_modules', '.bin', 'jest')
    env = dict(os.environ); env.update(env_extra or {}); env.pop('GIT_SSH_COMMAND', None)
    p = subprocess.run(['node', bin_, '--config', os.path.join(od, 'jest.config.js'), '--ci', '--json', '--outputFile=' + json_path,
                        '--runTestsByPath', os.path.join(wt, rel_test)], cwd=od, capture_output=True, env=env, timeout=600)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def read_jest(json_path):
    """-> {'load_failed': bool, 'tests': n, 'passed': n, 'failed': n, 'cells': {title_or_cell: status}, 'message': str}"""
    if not os.path.isfile(json_path):
        return {'load_failed': True, 'tests': 0, 'passed': 0, 'failed': 0, 'cells': {}, 'message': 'NO JSON WRITTEN'}
    d = json.load(open(json_path))
    tr = d.get('testResults') or []
    ar = [a for r in tr for a in r.get('assertionResults') or []]
    msg = ' | '.join((r.get('message') or '')[:300] for r in tr if r.get('message'))
    load_failed = (not ar) or any('Test suite failed to run' in (r.get('message') or '') for r in tr)
    cells = {}
    for a in ar:
        m = CELL_RX.match(a['title'])
        cells[m.group(1) if m else a['title'][:80]] = a['status']
    return {'load_failed': load_failed, 'tests': len(ar), 'passed': sum(1 for a in ar if a['status'] == 'passed'),
            'failed': sum(1 for a in ar if a['status'] == 'failed'), 'cells': cells, 'message': msg}


def apply_edits(src, edits, scope):
    """returns the tampered text; refuses unless each anchor occurs EXACTLY ONCE in its scope."""
    if edits == 'BASE_BLOB':
        raise SystemExit('apply_edits: BASE_BLOB is handled by the caller')
    out = src
    for a, b in edits:
        if scope == 'block':
            hs, he = handler(out); bs, be = block(out, hs, he); region = out[bs:be]
            if region.count(a) != 1:
                raise SystemExit('ANCHOR %r occurs %d time(s) in the block (want 1) — the tamper is NOT applied' % (a[:60], region.count(a)))
            out = out[:bs] + region.replace(a, b) + out[be:]
        else:
            if out.count(a) != 1:
                raise SystemExit('ANCHOR %r occurs %d time(s) in the file (want 1) — the tamper is NOT applied' % (a[:60], out.count(a)))
            out = out.replace(a, b)
    return out


def compare(reds, want):
    return 'MATCH' if sorted(reds) == sorted(want) else 'DIFFER (measured %s, READY %s)' % (sorted(reds), sorted(want))


def porcelain(wt):
    return subprocess.run(['git', '-C', wt, 'status', '--porcelain', '--untracked-files=all', '--', '.', ':!Blockchain/Dev/**/node_modules',
                           ':!Blockchain/Dev/packages/shared/dist'], capture_output=True, text=True).stdout.strip()


def setup(clone, head, wt, logd):
    must_be_outside(wt, 'worktree'); must_be_outside(clone, 'clone')
    if os.path.exists(wt): print('REFUSED: %s exists (a fresh worktree each time)' % wt); return 2
    logd = logd or os.path.dirname(wt.rstrip('/')); os.makedirs(logd, exist_ok=True)
    rc, o, e = wgit(clone, 'worktree', 'add', '--detach', wt, head)
    print('%s worktree add rc %d %s' % (now(), rc, e.strip()[-120:]))
    if rc: return 1
    dev = os.path.join(wt, DD)
    for name, cmd in (('ci', ['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund']),
                      ('build_shared', ['npm', 'run', 'build', '--workspace=packages/shared'])):
        p = subprocess.run(cmd, cwd=dev, capture_output=True, timeout=1200)
        open(os.path.join(logd, 'setup_%s.out' % name), 'wb').write(p.stdout); open(os.path.join(logd, 'setup_%s.err' % name), 'wb').write(p.stderr)
        print('%s %s rc %d (%s)' % (now(), ' '.join(cmd), p.returncode, os.path.join(logd, 'setup_%s.out' % name)))
        if p.returncode: return 1
    ok = os.path.isfile(os.path.join(dev, 'packages', 'shared', 'dist', 'index.js'))
    print('ASSERT packages/shared/dist/index.js present: %s' % ok)
    print('porcelain after setup (node_modules / dist excluded): %r' % porcelain(wt)[:200])
    return 0 if ok else 1


def restore_head(wt, clone, head, rels):
    bad = []
    for rel in rels:
        if blob(clone, head, rel):
            data = git_bytes(clone, head, rel); write_checked(wt, rel, data)
            if sha(open(os.path.join(wt, rel), 'rb').read()) != sha(data): bad.append(rel)
    return bad


def cells(wt, clone, head, base, route, tests, out):
    must_be_outside(out, 'out dir'); os.makedirs(out, exist_ok=True); rc = 0
    rev = {'base': base, 'head': head}
    planted = []
    print('%s CELLS route=%s (%s) tests=%s (%s) wt %s' % (now(), route, rev[route][:12], tests, rev[tests][:12], wt))
    data = git_bytes(clone, rev[route], RF); write_checked(wt, RF, data); planted.append(RF)
    print('  PLANT %s from %s sha256/16 %s LANDED' % (RF, route, sha(data)[:16]))
    for k, rel in TF.items():
        if not blob(clone, rev[tests], rel):
            print('  %s ABSENT at %s %s — NOT RUN by name' % (k, tests, rev[tests][:12])); continue
        d = git_bytes(clone, rev[tests], rel); write_checked(wt, rel, d); planted.append(rel)
    try:
        for k, rel in TF.items():
            if not os.path.isfile(os.path.join(wt, rel)) or not blob(clone, rev[tests], rel):
                continue
            jp = os.path.join(out, 'cells_%s_route-%s_tests-%s.json' % (k, route, tests))
            jrc, so, se = jest(wt, rel, jp)
            open(jp[:-5] + '.out', 'w').write(so); open(jp[:-5] + '.err', 'w').write(se)
            r = read_jest(jp)
            print('  %-6s jest rc %d | tests %d passed %d failed %d | LOAD-FAILED %s %s' % (k, jrc, r['tests'], r['passed'], r['failed'], r['load_failed'], r['message'][:160] if r['load_failed'] else ''))
            if r['load_failed']: rc = 1
            if k == 'ks1402':
                print('  ks1402 cells: %s' % ' '.join('%s=%s' % (c, r['cells'].get(c, 'ABSENT')) for c in K['cells']))
                print('  ks1402 REDS: %s' % sorted(c for c in K['cells'] if r['cells'].get(c) != 'passed'))
            else:
                fails = [t for t, s in r['cells'].items() if s != 'passed']
                for t in fails[:20]: print('    RED %s' % t)
    finally:
        bad = restore_head(wt, clone, head, planted)
        print('  RESTORE %d planted file(s) to the HEAD blob: %s' % (len(planted), 'sha OK' if not bad else 'FAILED %s' % bad))
        if bad: rc = 1
    return rc


def tamper(wt, clone, head, base, out, only):
    must_be_outside(out, 'out dir'); os.makedirs(out, exist_ok=True); rc = 0
    hsrc = git_bytes(clone, head, RF).decode('utf-8'); bsrc = git_bytes(clone, base, RF)
    rows = [{'id': 'HEAD', 'what': 'the head, unchanged', 'ready_reds': [], 'edits': [], 'scope': 'file'},
            {'id': 'CTRL', 'what': 'CONTROL: a no-op comment planted in the block', 'ready_reds': [], 'scope': 'block',
             'edits': [['let resolvedHolderId = newHolderId;', 'let resolvedHolderId = newHolderId; // gate79 no-op control']]}] + K['tampers']
    if only: rows = [r for r in rows if r['id'] in only or r['id'] == 'HEAD']
    print('%s TAMPER over %s (head %s, base %s): %d row(s)' % (now(), RF, head[:12], base[:12], len(rows)))
    summary = []
    for row in rows:
        try:
            if row['edits'] == 'BASE_BLOB':
                data = bsrc; landed = sha(data) != sha(hsrc.encode())
            else:
                t = apply_edits(hsrc, row['edits'], row['scope']) if row['edits'] else hsrc
                data = t.encode('utf-8')
                landed = (not row['edits']) or (sha(data) != sha(hsrc.encode()) and all(b in t for a, b in row['edits']))
        except SystemExit as e:
            print('ROW %-5s %-55s REFUSED: %s' % (row['id'], row['what'][:55], e)); rc = 1; summary.append((row['id'], 'REFUSED')); continue
        if not landed:
            print('ROW %-5s TAMPER NOT LANDED — no verdict' % row['id']); rc = 1; summary.append((row['id'], 'NOT LANDED')); continue
        write_checked(wt, RF, data)
        jp = os.path.join(out, 'tamper_%s.json' % row['id'])
        try:
            jrc, so, se = jest(wt, TF['ks1402'], jp)
            open(jp[:-5] + '.err', 'w').write(se)
        finally:
            bad = restore_head(wt, clone, head, [RF])
        r = read_jest(jp)
        reds = sorted(c for c in K['cells'] if r['cells'].get(c) != 'passed')
        if r['load_failed']:
            verdict = 'TAMPER-INVALID (suite failed to LOAD: %s)' % r['message'][:120]; rc = 1
        elif row['id'] in ('HEAD', 'CTRL'):
            verdict = 'OK all green' if not reds else 'FAIL: %s red' % reds; rc |= 1 if reds else 0
        else:
            verdict = compare(reds, row['ready_reds']) + ('' if reds else '  <<< ALL-GREEN: no cell catches this tamper')
            if not reds: rc = 1
        print('ROW %-5s %-55s landed sha256/16 %s | tests %d passed %d | reds %s | %s | restore %s' % (
            row['id'], row['what'][:55], sha(data)[:16], r['tests'], r['passed'], reds, verdict, 'OK' if not bad else 'FAILED'))
        if bad: rc = 1
        summary.append((row['id'], verdict))
    nmatch = sum(1 for _, v in summary if v.startswith('MATCH')); ntamp = len([s for s in summary if s[0] not in ('HEAD', 'CTRL')])
    print('SUMMARY %d/%d tamper rows MATCH the READY; HEAD %s; CTRL %s' % (nmatch, ntamp, dict(summary).get('HEAD'), dict(summary).get('CTRL')))
    print('porcelain after (node_modules / dist excluded): %r' % porcelain(wt)[:200])
    return rc


def probe(wt, clone, head, out):
    must_be_outside(out, 'out dir'); os.makedirs(out, exist_ok=True)
    rel = os.path.join(os.path.dirname(TF['ks1402']), 'gate79-probe.test.ts')
    src = git_bytes(clone, head, TF['ks1402']).decode('utf-8') + open(os.path.join(HERE, 'probe_block_gate79.ts.txt'), encoding='utf-8').read()
    write_checked(wt, rel, src.encode('utf-8'))
    facts = os.path.join(out, 'probe_facts.jsonl')
    if os.path.exists(facts): print('REFUSED: %s exists (fresh out dir)' % facts); return 2
    jp = os.path.join(out, 'probe.json')
    try:
        jrc, so, se = jest(wt, rel, jp, {'G79_PROBE_OUT': facts})
        open(os.path.join(out, 'probe.err'), 'w').write(se)
    finally:
        shutil.move(os.path.join(wt, rel), os.path.join(out, 'gate79-probe.test.ts.QUARANTINED'))
    r = read_jest(jp)
    print('%s PROBE jest rc %d | tests %d passed %d | LOAD-FAILED %s %s' % (now(), jrc, r['tests'], r['passed'], r['load_failed'], r['message'][:200] if r['load_failed'] else ''))
    print('  original 11 cells in the probe run: %s' % ' '.join('%s=%s' % (c, r['cells'].get(c, 'ABSENT')) for c in K['cells']))
    n = 0
    if os.path.isfile(facts):
        for l in open(facts):
            n += 1; d = json.loads(l); print('FACT %s %s' % (d.pop('id'), json.dumps(d, ensure_ascii=True)[:1800]))
    pc = porcelain(wt)
    print('  probe facts %d line(s) (want 5) | probe file quarantined to %s | porcelain after %r' % (n, out, pc[:200]))
    return 0 if (not r['load_failed'] and n == 5 and not pc) else 1


def selftest():
    import tempfile
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    d = tempfile.mkdtemp(prefix='g79st_')
    jp = os.path.join(d, 'a.json')
    json.dump({'testResults': [{'message': '', 'assertionResults': [{'title': 'C1: x', 'status': 'passed'}, {'title': 'C2b: y', 'status': 'failed'},
                                                                   {'title': 'C10 (order, Q-HOIST): z', 'status': 'passed'}]}]}, open(jp, 'w'))
    r = read_jest(jp); rep(r['cells'] == {'C1': 'passed', 'C2b': 'failed', 'C10': 'passed'} and r['failed'] == 1 and not r['load_failed'], 'read_jest maps C1 / C2b / C10 titles')
    json.dump({'testResults': [{'message': '  ● Test suite failed to run\n  TS2304', 'assertionResults': []}]}, open(jp, 'w'))
    rep(read_jest(jp)['load_failed'], 'PLANTED suite-load failure reads LOAD-FAILED, never a red count')
    rep(read_jest(os.path.join(d, 'none.json'))['load_failed'], 'a missing jest json reads LOAD-FAILED (a check whose input is missing goes RED)')
    src = "x\ndocumentsRouter.post(\n  '/:id/transfer-custody',\n  a,\n      let resolvedHolderId = newHolderId;\n      AND (tenant_id IS NULL OR tenant_id = ${tenantId}::uuid)\n      if (!resolvedHolderId) {\n      AND (tenant_id IS NULL OR tenant_id = ${tenantId}::uuid)\n);\ndocumentsRouter.get(\n"
    t = apply_edits(src, [['AND (tenant_id IS NULL OR tenant_id = ${tenantId}::uuid)', 'AND (tenant_id = ${tenantId}::uuid)']], 'block')
    rep(t.count('tenant_id IS NULL') == 1 and t.index('AND (tenant_id = ') < t.index('if (!resolvedHolderId)'), 'block scope: the email read is tampered, the id-path twin is NOT')
    try: apply_edits(src, [['AND (tenant_id IS NULL OR tenant_id = ${tenantId}::uuid)', 'x']], 'file'); rep(False, 'a 2-occurrence file anchor was ACCEPTED')
    except SystemExit: rep(True, 'PLANTED 2-occurrence anchor in file scope REFUSES (a silent wrong-site edit is impossible)')
    try: apply_edits(src, [['NOT THERE', 'x']], 'block'); rep(False, 'an absent anchor was ACCEPTED')
    except SystemExit: rep(True, 'PLANTED absent anchor REFUSES (no silent no-op edit)')
    rep(compare(['C2', 'C2b'], ['C2b', 'C2']) == 'MATCH' and compare(['C2'], ['C2', 'C2b']).startswith('DIFFER'), 'comparator: MATCH ignores order; a missing red DIFFERS')
    try: must_be_outside('/Volumes/DevMASTER/!CODING/Secuura/x', 'write'); rep(False, 'a !CODING write path was ACCEPTED')
    except SystemExit: rep(True, 'a write path under !CODING REFUSES')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if not A: print(__doc__); return 2
    if A[0] == '--selftest': return selftest()
    try:
        if A[0] == 'setup':
            return setup(req(A, '--clone'), req(A, '--head', True), req(A, '--wt'), opt(A, '--log'))
        if A[0] == 'cells':
            ro, te = req(A, '--route'), req(A, '--tests')
            if ro not in ('base', 'head') or te not in ('base', 'head'): print('REFUSED: --route/--tests base|head'); return 2
            return cells(req(A, '--wt'), req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), ro, te, req(A, '--out'))
        if A[0] == 'tamper':
            o = opt(A, '--only')
            return tamper(req(A, '--wt'), req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), req(A, '--out'), o.split(',') if o else None)
        if A[0] == 'probe':
            return probe(req(A, '--wt'), req(A, '--clone'), req(A, '--head', True), req(A, '--out'))
    except SystemExit as e:
        print(e); return 2
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
