#!/usr/bin/env python3
"""c3_cells_gate85.py — the RUN instruments for gate85: ONE PR, #1453 (KS-1432). Everything runs in ONE scratch tree OUTSIDE every git repo (`git archive` of the head + a COPY of an installed
node_modules), never in the builder's worktree and never in the shared checkout. NO npm, NO npx, NO install of anything, NO network: every tool is a binary already inside the copied
node_modules/.bin (`vitest`, `tsc`, `eslint`) or `node`/`bash`. Plants are file swaps ASSERTED LANDED and RESTORED by git blob id. Every figure printed is the DRAFTER'S PREDICTION (predictions/);
the gate re-measures on its own tree.

  prep       --repo R --head H --base B --tree T --deps-from DIR     T must not exist (canonical /private/tmp/claude-501/... path, under no repo). Extracts the head (Blockchain/Dev, Projects Documents,
                                                                      systemTest/__tests__, .githooks), copies DIR/node_modules + DIR/packages/shared/dist + DIR/services/api-gateway/node_modules
                                                                      (DIR = a `Blockchain/Dev` directory somebody else installed: a READ of it; Q-NM85), then `nmcheck`.
  nmcheck    --tree T                      the copied node_modules vs the HEAD's package-lock.json: the hidden lockfile's every package == the lock's version; 0 non-optional lock packages missing
  cells      --tree T --out O --repo R --head H --base B       RED/GREEN: (G) head product + head test; (R) BASE product + head test = "the test section alone"; (B) base + base test; (P) head product + base test
  suite      --tree T --out O --repo R --head H --base B       the whole api-gateway vitest suite at the head and at the base (files, tests, failures), JSON totals AND summed rows
  mutations  --tree T --out O --repo R --head H --base B       M0 / M1 / M2 (the builder's table) + gate-owned G1..G6, each: guard test + whole suite, the failing cells named, restore asserted
  route      --tree T --out O --repo R --head H --base B       THE UNMEASURED CLAIM: the real POST /api/documents route (the ks815 harness shape: real router, raw socket) driven with null / array / number /
                                                                string / boolean / object bodies at HEAD, with the call site deleted (M2) and at BASE with the inline check deleted (M0)
  static     --tree T --out O --repo R --head H --base B       tsc --noEmit (package), a program NAMING the changed test (+ planted TS2322 control), eslint src (warnings located against the diff hunks)
  docs       --tree T --out O --repo R --head H --base B --develop D     html_docs_matrix on the head tree; per-fragment COUNT; drop / duplicate controls (the matrix is blind to both); keep-both onto develop
  compose    --clone C --head H --base B --develop D [--other 1451=<sha> --other 1452=<sha>]     merge-tree --write-tree --name-only in YOUR clone (outside the forbidden root): develop + head, and head vs each other open PR (INFO)
  --selftest
rc 0 all pass / 1 a FAIL (a finding, a blind control) / 2 refused."""
import hashlib, json, os, re, shutil, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate85 import K, PR, Tally, git, wgit, show, blob, req, opt, resolvable, blob_of_bytes, canonical_tmp, must_be_outside, extract, run as lrun, docs_base, exact_tail_insert, TAIL, HEX40

DEV = 'Blockchain/Dev'
SVC = 'Blockchain/Dev/services/api-gateway'


# ---------------------------------------------------------------- helpers
def need_canonical(path, what):
    if not canonical_tmp(os.path.dirname(os.path.abspath(path)) if not os.path.exists(path) else path):
        raise SystemExit('REFUSED: %s %s is not a canonical /private/tmp/claude-501/ path under no git repository' % (what, path))
    must_be_outside(path, what)


def hid(tree, rel): return blob_of_bytes(open(os.path.join(tree, rel), 'rb').read()) if os.path.isfile(os.path.join(tree, rel)) else ''


def vt(tree, out, name, args, env_extra=None, reporter_text=False, timeout=900):
    """run the tree's own vitest binary (no npx) in the api-gateway dir; -> dict with rc, totals (JSON AND summed rows), failing cell ids, files."""
    svc = os.path.join(tree, SVC); js = os.path.join(out, name + '.json'); os.makedirs(out, exist_ok=True)
    tmp = os.path.join(out, '_tmp'); os.makedirs(tmp, exist_ok=True)
    cmd = [os.path.join(tree, DEV, 'node_modules', '.bin', 'vitest'), 'run'] + list(args)
    cmd += (['--reporter=default', '--reporter=json', '--outputFile.json=' + js] if reporter_text else ['--reporter=json', '--outputFile=' + js])
    if os.path.exists(js): os.remove(js)
    t0 = time.time(); rc, so, se = lrun(cmd, svc, env=dict(env_extra or {}, TMPDIR=tmp), timeout=timeout)
    open(os.path.join(out, name + '.stdout'), 'w').write(so); open(os.path.join(out, name + '.stderr'), 'w').write(se)
    res = {'name': name, 'rc': rc, 'secs': round(time.time() - t0, 1), 'json': os.path.isfile(js), 'stdout': so, 'stderr': se}
    if res['json']:
        j = json.load(open(js)); rows = [(r['name'], ((a.get('ancestorTitles') or [''])[-1][:28] + ' :: ' if a.get('ancestorTitles') else '') + (a.get('title') or ''), a['status']) for r in j['testResults'] for a in r['assertionResults']]
        res.update({'total': j['numTotalTests'], 'passed': j['numPassedTests'], 'failed': j['numFailedTests'], 'files': len(j['testResults']), 'failed_files': sum(1 for r in j['testResults'] if r['status'] != 'passed'),
                    'rows': len(rows), 'rows_passed': sum(1 for x in rows if x[2] == 'passed'), 'rows_failed': sum(1 for x in rows if x[2] == 'failed'),
                    'failing': [(os.path.basename(x[0]), x[1]) for x in rows if x[2] == 'failed'], 'suites_failed_to_load': [os.path.basename(r['name']) for r in j['testResults'] if r['status'] == 'failed' and not r['assertionResults']]})
        res['consistent'] = res['total'] == res['rows'] and res['passed'] == res['rows_passed'] and res['failed'] == res['rows_failed']
    return res


def line(r):
    if not r.get('json'): return '%s rc=%s NO JSON (a run that wrote no report is NOT RUN, never a pass) stderr: %s' % (r['name'], r['rc'], r['stderr'][-200:].strip())
    return '%s rc=%d %d passed / %d failed of %d tests in %d file(s) (%d failed file(s)); summed rows %d/%d/%d %s; %.1fs' % (
        r['name'], r['rc'], r['passed'], r['failed'], r['total'], r['files'], r['failed_files'], r['rows_passed'], r['rows_failed'], r['rows'], 'AGREE' if r['consistent'] else 'DISAGREE <<<', r['secs'])


class Plant:
    """swap files in the tree for given bytes; assert LANDED (blob id == expected, != before) and restore by blob id."""
    def __init__(self, tree): self.tree = tree; self.orig = {}
    def put(self, rel, data):
        fp = os.path.join(self.tree, rel)
        if rel not in self.orig: self.orig[rel] = open(fp, 'rb').read()
        before = blob_of_bytes(open(fp, 'rb').read()); open(fp, 'wb').write(data if isinstance(data, bytes) else data.encode('utf-8'))
        after = hid(self.tree, rel)
        return before, after, after == blob_of_bytes(data), before != after
    def restore(self):
        bad = []
        for rel, data in self.orig.items():
            fp = os.path.join(self.tree, rel); open(fp, 'wb').write(data)
            if hid(self.tree, rel) != blob_of_bytes(data): bad.append(rel)
        self.orig = {}
        return bad


def block_after(text, anchor_line):
    """the block `if (...) {` ... matching `}` that starts at the (unique) line containing anchor_line: -> (start, end) char offsets (end exclusive, includes the trailing newline)."""
    lines = text.split('\n'); idx = [i for i, l in enumerate(lines) if anchor_line in l]
    if len(idx) != 1: raise SystemExit('block_after: anchor %r found %d times, want exactly 1' % (anchor_line, len(idx)))
    i = idx[0]; ind = re.match(r'\s*', lines[i]).group(0)
    j = next((k for k in range(i + 1, len(lines)) if lines[k] == ind + '}'), None)
    if j is None: raise SystemExit('block_after: no closing brace at indent %d after the anchor' % len(ind))
    start = sum(len(l) + 1 for l in lines[:i]); end = sum(len(l) + 1 for l in lines[:j + 1])
    return start, end


def mutate(kind, text):
    """-> (new_text, description). The anchors are asserted to appear exactly once."""
    OLDC = "parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)"
    if kind == 'M0':       # at BASE bytes: delete the route's inline check block
        s, e = block_after(text, "if (%s) {" % OLDC); return text[:s] + text[e:], 'base bytes: the inline `if (...)` 400 block deleted'
    if kind == 'M2':       # at HEAD: delete the call-site block
        s, e = block_after(text, 'if (!isAcceptableDocumentBody(parsed)) {'); return text[:s] + text[e:], 'head: the call-site `if (!isAcceptableDocumentBody(parsed))` 400 block deleted'
    rets = {'M1': ("  return !(%s);\n" % OLDC, "  return true;\n", 'head: the exported predicate returns true (accepts everything)'),
            'G1': ("  return !(%s);\n" % OLDC, "  return (%s);\n" % OLDC, 'head: the predicate returns the UN-negated condition (accepts exactly what the route should refuse)'),
            'G2': ("  return !(%s);\n" % OLDC, "  return !(parsed === null || typeof parsed !== 'object');\n", 'head: the predicate drops the Array.isArray term (arrays accepted)'),
            'G3': ("  return !(%s);\n" % OLDC, "  return !(typeof parsed !== 'object' || Array.isArray(parsed));\n", 'head: the predicate drops the `parsed === null` term (null accepted)'),
            'G6': ("export function isAcceptableDocumentBody(", "function isAcceptableDocumentBody(", 'head: the `export` keyword removed (the route still calls it; the test cannot reach it)')}
    if kind in rets:
        old, new, d = rets[kind]
        if text.count(old) != 1: raise SystemExit('mutate %s: anchor found %d times, want exactly 1' % (kind, text.count(old)))
        return text.replace(old, new), d
    calls = {'G4': ("if (!isAcceptableDocumentBody(parsed)) {", "if (parsed === null) {", 'head: the call site weakened to `if (parsed === null)` (the route accepts arrays, numbers, strings, booleans; the predicate stays correct)'),
             'G5': ("if (!isAcceptableDocumentBody(parsed)) {", "if (isAcceptableDocumentBody(parsed)) {", 'head: the call site INVERTED (the route refuses what it should accept)')}
    if kind in calls:
        old, new, d = calls[kind]
        if text.count(old) != 1: raise SystemExit('mutate %s: anchor found %d times, want exactly 1' % (kind, text.count(old)))
        return text.replace(old, new), d
    raise SystemExit('mutate: unknown kind %r' % kind)


def get_files(repo, P, head, base):
    prod, test = P['product'], P['test_file']
    return {'hp': show(repo, head, prod), 'bp': show(repo, base, prod), 'ht': show(repo, head, test), 'bt': show(repo, base, test)}


def settle(t, tree, F, P):
    """put the tree into a known state: head product + head test, asserted by blob id vs the kit."""
    pl = Plant(tree); pl.put(P['product'], F['hp']); pl.put(P['test_file'], F['ht']); pl.orig = {}
    ok = hid(tree, P['product']) == P['blobs_full']['product_head'] and hid(tree, P['test_file']) == P['blobs_full']['test_head']
    return ok


# ---------------------------------------------------------------- prep / nmcheck
def nmcheck(tree):
    t = Tally(); lockp = os.path.join(tree, DEV, 'package-lock.json'); hp = os.path.join(tree, DEV, 'node_modules', '.package-lock.json')
    if not (os.path.isfile(lockp) and os.path.isfile(hp)):
        t.check('NM0', False, 'package-lock.json or node_modules/.package-lock.json missing in %s' % tree); return t.end()
    lock = json.load(open(lockp))['packages']; hidl = json.load(open(hp))['packages']
    mism = [k for k, v in hidl.items() if k in lock and lock[k].get('version') != v.get('version')]; extra = [k for k in hidl if k not in lock]
    miss = [k for k, v in lock.items() if k.startswith('node_modules/') and k not in hidl and not v.get('optional') and not v.get('link')]
    t.check('NM1', len(hidl) > 1000 and not mism and not extra and not miss, 'hidden lockfile %d packages vs the HEAD package-lock.json %d packages: version mismatches %d %s, installed-but-not-in-lock %d, non-optional-in-lock-but-not-installed %d %s' % (
        len(hidl), len(lock), len(mism), mism[:3], len(extra), len(miss), miss[:3]))
    t.check('NM1-CONTROL', bool(hidl) and any(True for _ in [0]) and (lambda l, h: [k for k, v in {**h, 'node_modules/zz-planted': {'version': '9.9.9'}}.items() if k in {**l, 'node_modules/zz-planted': {'version': '0.0.1'}} and {**l, 'node_modules/zz-planted': {'version': '0.0.1'}}[k].get('version') != v.get('version')] == ['node_modules/zz-planted'])(lock, hidl), 'CONTROL: a planted package at a different version reads as a mismatch (the comparison can fail)')
    for b in ('vitest', 'tsc', 'eslint'):
        fp = os.path.join(tree, DEV, 'node_modules', '.bin', b); t.check('NM2', os.path.exists(fp), 'node_modules/.bin/%s present: %s' % (b, os.path.exists(fp)))
    rc, so, se = lrun([os.path.join(tree, DEV, 'node_modules', '.bin', 'vitest'), '--version'], os.path.join(tree, SVC)); rc2, so2, _ = lrun([os.path.join(tree, DEV, 'node_modules', '.bin', 'tsc'), '--version'], os.path.join(tree, SVC))
    rc3, so3, _ = lrun(['node', '--version'], os.path.join(tree, SVC))
    t.info('NM3', 'versions: vitest %s | tsc %s | node %s (the builder\'s: vitest 4.1.11, TypeScript 5.9.3, node v24.7.0)' % (so.strip(), so2.strip(), so3.strip()))
    sh = os.path.join(tree, DEV, 'packages', 'shared', 'dist'); t.check('NM4', os.path.isdir(sh) and any(True for _ in os.scandir(sh)), 'packages/shared/dist present and non-empty (the built workspace package the api-gateway imports): %s' % os.path.isdir(sh))
    return t.end()


def prep(repo, P, head, base, tree, deps):
    need_canonical(tree, 'tree')
    if os.path.exists(tree): print('REFUSED: %s exists (build each attempt in its own new directory; never reuse or delete)' % tree); return 2
    os.makedirs(tree)
    n = extract(repo, head, [DEV, 'Projects Documents', 'systemTest/__tests__', '.githooks'], tree)
    print('extracted %d files of %s into %s' % (n, head[:12], tree))
    for rel in ('node_modules', 'packages/shared/dist', 'services/api-gateway/node_modules'):
        src = os.path.join(deps, rel)
        if not os.path.isdir(src): print('REFUSED: %s is not a directory' % src); return 2
        dst = os.path.join(tree, DEV, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
        cp = subprocess.run(['cp', '-R', src, dst], capture_output=True, text=True)      # cp -R keeps symlinks as symlinks and is ~10x faster than a Python tree walk on this volume pair
        if cp.returncode != 0: print('REFUSED: cp -R %s failed: %s' % (src, cp.stderr[:200])); return 2
    print('copied node_modules (%d KiB), packages/shared/dist, services/api-gateway/node_modules from %s' % (int(subprocess.run(['du', '-sk', os.path.join(tree, DEV, 'node_modules')], capture_output=True, text=True).stdout.split()[0]), deps))
    t = Tally()
    for k in ('product_head', 'test_head'):
        rel = P['product'] if k == 'product_head' else P['test_file']; t.check('PREP-' + k, hid(tree, rel) == P['blobs_full'][k], '%s blob in the tree %s == git %s' % (rel.split('/')[-1], hid(tree, rel)[:12], P['blobs_full'][k][:12]))
    t.check('PREP-NOREPO', canonical_tmp(tree) and not os.path.exists(os.path.join(tree, '.git')), 'the tree is outside every git repository (no .git on any parent): %s' % canonical_tmp(tree))
    rc = nmcheck(tree)
    return 0 if (rc == 0 and not t.fails and t.end() == 0) else 1


# ---------------------------------------------------------------- cells / suite / mutations
def cells(tree, out, repo, P, head, base):
    t = Tally(); F = get_files(repo, P, head, base); pl = Plant(tree); T = P['test_name']; tp = 'src/__tests__/' + T
    print('settle:', settle(t, tree, F, P))
    combos = [('G', 'head product + head test (the PR)', F['hp'], F['ht']), ('R', 'BASE product + head test = "the test section alone"', F['bp'], F['ht']),
              ('B', 'BASE product + BASE test (the 8 existing cells at the base)', F['bp'], F['bt']), ('P', 'head product + BASE test (the product section alone)', F['hp'], F['bt'])]
    want = {'G': (10, 0), 'R': (1, 9), 'B': (8, 0), 'P': (8, 0)}
    for tag, desc, prod, tst in combos:
        b1 = pl.put(P['product'], prod); b2 = pl.put(P['test_file'], tst)
        landed = b1[2] and b2[2] and (hid(tree, P['product']) == blob_of_bytes(prod.encode()))
        r = vt(tree, out, 'cells_' + tag, [tp], reporter_text=True)
        text_sum = re.findall(r'Tests\s+(?:(\d+) failed \| )?(\d+) passed', r['stdout'])
        ok = r.get('json') and r['consistent'] and (r['passed'], r['failed']) == want[tag] and (r['rc'] == (0 if want[tag][1] == 0 else 1)) and landed
        t.check('CELLS-' + tag, ok, '%s | plant LANDED (blob ids asserted; product changed: %s test changed: %s) | %s | want %d passed / %d failed | text summary %s' % (desc, b1[3], b2[3], line(r), want[tag][0], want[tag][1], text_sum[-1:] or 'n/a'))
        if tag == 'R' and r.get('json'):
            t.info('CELLS-R-NAMES', 'failing cells (%d): %s' % (len(r['failing']), [x[1][:70] for x in r['failing']]))
            msgs = re.findall(r'(?:AssertionError: )(expected [^\n]{0,60}?to (?:be|equal) [^\n/]{0,20})', r['stdout'] + r['stderr']); t.info('CELLS-R-MSG', 'assertion messages seen in the text report: %s' % sorted(set(msgs))[:6])
        bad = pl.restore(); t.check('CELLS-RESTORE-' + tag, not bad and hid(tree, P['product']) == P['blobs_full']['product_head'] and hid(tree, P['test_file']) == P['blobs_full']['test_head'], 'restored: product %s test %s == the head blobs' % (hid(tree, P['product'])[:12], hid(tree, P['test_file'])[:12]))
    return t.end()


def suite(tree, out, repo, P, head, base):
    t = Tally(); F = get_files(repo, P, head, base); pl = Plant(tree); settle(t, tree, F, P)
    r = vt(tree, out, 'suite_head', [], reporter_text=True)
    t.check('SUITE-HEAD', r.get('json') and r['consistent'] and (r['passed'], r['failed'], r['files']) == (871, 0, 96) and r['rc'] == 0 and not r['suites_failed_to_load'], line(r) + ' | want 871 passed / 0 failed in 96 files, rc 0, no suite failed to load %s' % r.get('suites_failed_to_load'))
    pl.put(P['product'], F['bp']); pl.put(P['test_file'], F['bt'])
    rb = vt(tree, out, 'suite_base', [], reporter_text=True)
    t.check('SUITE-BASE', rb.get('json') and rb['consistent'] and (rb['passed'], rb['failed'], rb['files']) == (869, 0, 96) and rb['rc'] == 0, line(rb) + ' | want 869 passed / 0 failed in 96 files (the base bytes of both files)')
    bad = pl.restore(); t.check('SUITE-RESTORE', not bad and hid(tree, P['product']) == P['blobs_full']['product_head'], 'restored to the head blobs: %s' % (not bad))
    if r.get('json') and rb.get('json'): t.info('SUITE-DELTA', 'tests %d -> %d (+%d), files %d -> %d; the test file is CHANGED, not added' % (rb['total'], r['total'], r['total'] - rb['total'], rb['files'], r['files']))
    return t.end()


MUTS = [('M0', 'base', "builder's M0: at BASE bytes delete the route's inline check (the ticket's premise)", (8, 0, 868, 1)),
        ('M1', 'head', "builder's M1: the exported predicate accepts everything", (4, 6, 864, 7)),
        ('M2', 'head', "builder's M2: delete the call-site block", (10, 0, 870, 1)),
        ('G1', 'head', 'gate: predicate UN-negated', None), ('G2', 'head', 'gate: predicate drops the Array.isArray term', None), ('G3', 'head', 'gate: predicate drops the null term', None),
        ('G4', 'head', 'gate: call site weakened to `if (parsed === null)`', None), ('G5', 'head', 'gate: call site INVERTED', None), ('G6', 'head', 'gate: `export` removed from the predicate', None)]


def mutations(tree, out, repo, P, head, base, only=None):
    t = Tally(); F = get_files(repo, P, head, base); T = P['test_name']; tp = 'src/__tests__/' + T; settle(t, tree, F, P)
    rows = []
    for mid, at, desc, claim in MUTS:
        if only and mid not in only: continue
        pl = Plant(tree); src = F['bp'] if at == 'base' else F['hp']; tst = F['bt'] if at == 'base' else F['ht']
        new, d = mutate(mid, src)
        landed1 = pl.put(P['test_file'], tst); landed2 = pl.put(P['product'], new)
        anchor = (new != src) and landed2[2] and landed2[3]
        rt = vt(tree, out, 'mut_%s_test' % mid, [tp]); rs = vt(tree, out, 'mut_%s_suite' % mid, [])
        bad = pl.restore(); restored = (not bad) and hid(tree, P['product']) == P['blobs_full']['product_head'] and hid(tree, P['test_file']) == P['blobs_full']['test_head']
        outside = [x for x in rs.get('failing', []) if not x[0].startswith(('ks529', 'ks815'))]
        ok_claim = True if claim is None else (rt.get('json') and rs.get('json') and (rt['passed'], rt['failed']) == (claim[0], claim[1]) and rs['passed'] == claim[2] and rs['failed'] == claim[3])
        t.check('MUT-' + mid, bool(anchor and restored and rt.get('json') and rs.get('json') and rt['consistent'] and rs['consistent'] and ok_claim),
                '%s [%s] plant LANDED (blob changed, anchor found once): %s | guard test: %d passed / %d failed | suite: %d passed / %d failed of %d | failing outside the two guard files: %s | restored by blob id: %s%s' % (
                    mid, d, anchor, rt.get('passed', -1), rt.get('failed', -1), rs.get('passed', -1), rs.get('failed', -1), rs.get('total', -1), [x[0] + '::' + x[1][:40] for x in outside][:4] or 'none', restored,
                    (' | builder\'s claim: guard %d passed / %d failed, suite %d passed / %d failed' % claim) if claim else ' | (gate-owned: no builder claim; the figures are the finding)'))
        if rs.get('json'): t.info('MUT-%s-NAMES' % mid, 'failing cells in the suite (%d): %s' % (len(rs['failing']), [x[0].replace('.test.ts', '') + '::' + x[1][:55] for x in rs['failing']][:10]))
        rows.append((mid, rt.get('passed'), rt.get('failed'), rs.get('passed'), rs.get('failed')))
    t.check('MUT-CONTROL-NOOP', True, 'a no-op control is `cells G` / `suite` (head bytes, all green) run by the other commands in the same tree; a mutation whose anchor is not found aborts before running (block_after / mutate assert exactly one match)')
    return t.end()


# ---------------------------------------------------------------- route (the unmeasured claim)
ROUTE_TEST = r"""// gate85's OWN scratch test (written into the gate's scratch tree, never into a repo). It mounts the REAL verification router exactly the way
// ks815-verification-router-guards-its-own-body.test.ts does and POSTs raw bodies to POST /api/documents over a socket; it records, it asserts nothing.
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import express from 'express';
import net from 'node:net';
import fs from 'node:fs';
import type { Server } from 'node:http';
import type { AddressInfo } from 'node:net';
import type { RequestHandler } from 'express';

let server: Server; let port: number; const realFetch = globalThis.fetch; const results: Record<string, unknown> = {};
const unhandled: string[] = []; process.on('unhandledRejection', (e) => { unhandled.push(String((e as Error)?.message ?? e)); });

beforeAll(async () => {
  globalThis.fetch = (async () => ({ ok: false, status: 404, json: async () => ({}), text: async () => '' })) as never;
  const { createVerificationRoutes } = await import('../routes/verification');
  const mockBodyParser: RequestHandler = express.json({ limit: '1mb' });
  const app = express();
  app.use(createVerificationRoutes({
    authenticateToken: () => (req, _res, next) => { (req as { user?: unknown }).user = { userId: 'u1', email: 'u@secuura.local', role: 'ADMIN', organizationId: 'o1', tenantId: 't1', verificationLevel: 'FULL' }; next(); },
    mockBodyParser, query: vi.fn(async () => ({ rows: [] })) as never, isDbAvailable: () => false,
    redisService: { getPendingDocument: vi.fn(async () => null), deletePendingDocument: vi.fn(async () => undefined), getAllDocumentTypes: vi.fn(async () => []), getAllWorkflowInstances: vi.fn(async () => []),
      getNotificationSettings: vi.fn(async () => ({})), getRejectedDocument: vi.fn(async () => null), setRejectedDocument: vi.fn(async () => undefined), getWorkflowDocumentMapping: vi.fn(async () => null),
      getWorkflowInstance: vi.fn(async () => null), setWorkflowInstance: vi.fn(async () => undefined) } as never,
    services: {} as never, log: () => undefined, memWorkflowToDocumentMap: new Map(), memRejectedDocuments: new Map(), dbSaveRejection: vi.fn(async () => undefined), ADMIN_ROLES: ['ADMIN', 'admin'],
    enforceDocumentTypeRules: vi.fn(async () => ({ ok: true, docType: {} })) as never, createWorkflowInstanceIfRequired: vi.fn(async () => ({ gated: false })) as never, meetsVerificationLevel: () => true,
  }));
  server = app.listen(0, '127.0.0.1'); await new Promise<void>((r) => server.once('listening', () => r())); port = (server.address() as AddressInfo).port;
});
afterAll(async () => {
  globalThis.fetch = realFetch; await new Promise<void>((r) => server.close(() => r()));
  fs.writeFileSync(process.env.G85_ROUTE_OUT as string, JSON.stringify({ results, unhandled }, null, 1));
});

function raw(path: string, body: string): Promise<{ status: number; code?: string; message?: string; text: string }> {
  return new Promise((resolve, reject) => {
    const head = ['POST ' + path + ' HTTP/1.1', 'Host: 127.0.0.1', 'Connection: close', 'Content-Type: application/json', 'Content-Length: ' + Buffer.byteLength(body), '', ''].join('\r\n');
    const sock = net.connect(port, '127.0.0.1', () => sock.write(head + body)); const chunks: Buffer[] = [];
    sock.setTimeout(4000, () => { sock.destroy(); resolve({ status: -1, text: 'TIMEOUT (no response in 4 s)' }); });
    sock.on('data', (d) => chunks.push(d)); sock.on('error', reject);
    sock.on('end', () => {
      const text = Buffer.concat(chunks).toString('utf8'); const status = Number(text.slice(9, 12)); const b = text.slice(text.indexOf('\r\n\r\n') + 4);
      let code: string | undefined; let message: string | undefined;
      try { const j = JSON.parse(b.replace(/^[0-9a-f]+\r\n/i, '').trim()); code = j?.error?.code; message = j?.error?.message; } catch { /* not json */ }
      resolve({ status, code, message, text: text.slice(0, 160) });
    });
  });
}
const SHAPES: Array<[string, string]> = [['null', 'null'], ['array', '[]'], ['array1', '[1]'], ['number', '42'], ['string', '"str"'], ['boolean', 'true'], ['false', 'false'],
  ['emptyobject', '{}'], ['object', '{"title":"x","documentType":"CERTIFICATE"}'], ['badjson', '{bad']];
describe('gate85 route shapes', () => {
  for (const [label, body] of SHAPES) {
    it('records ' + label, async () => { const r = await raw('/api/documents', body); results[label] = { body, status: r.status, code: r.code, message: r.message, head: r.text }; expect(true).toBe(true); });
  }
});
"""


def route(tree, out, repo, P, head, base):
    t = Tally(); F = get_files(repo, P, head, base); settle(t, tree, F, P)
    rel = SVC + '/src/__tests__/zz_gate85_route_shapes.test.ts'; fp = os.path.join(tree, rel); os.makedirs(out, exist_ok=True)
    open(fp, 'w').write(ROUTE_TEST)
    t.check('ROUTE0', canonical_tmp(tree) and not os.path.exists(os.path.join(tree, '.git')), 'the gate\'s own scratch test %s was written into the scratch tree (outside every repo)' % rel)
    variants = [('HEAD', 'head', None), ('M2', 'head', 'M2'), ('M0', 'base', 'M0'), ('G4', 'head', 'G4')]
    res = {}
    for name, at, mut in variants:
        pl = Plant(tree); src = F['bp'] if at == 'base' else F['hp']
        new = src
        if mut: new, d = mutate(mut, src)
        pl.put(P['product'], new); landed = hid(tree, P['product']) == blob_of_bytes(new.encode()) and (mut is None or new != src)
        outp = os.path.join(out, 'route_%s_shapes.json' % name)
        if os.path.exists(outp): os.remove(outp)
        r = vt(tree, out, 'route_%s' % name, ['src/__tests__/zz_gate85_route_shapes.test.ts'], env_extra={'G85_ROUTE_OUT': outp})
        bad = pl.restore()
        data = json.load(open(outp)) if os.path.isfile(outp) else None
        res[name] = data
        t.check('ROUTE-' + name, bool(landed and not bad and data and r.get('json') and r['rc'] == 0 and len(data['results']) == 10),
                '%s (%s) plant LANDED: %s | %s | recorded shapes %s | unhandledRejections seen by the harness: %s' % (name, 'head bytes' if not mut else mutate(mut, src)[1], landed, line(r), len(data['results']) if data else 'NONE', data['unhandled'] if data else 'n/a'))
        if data: t.info('ROUTE-%s-TABLE' % name, ' | '.join('%s=%s%s' % (k, v['status'], ('/' + v['code']) if v.get('code') else '') for k, v in data['results'].items()))
    if res.get('HEAD'):
        h = res['HEAD']['results']; refused = {k: v['status'] for k, v in h.items() if k in ('null', 'array', 'array1', 'number', 'string', 'boolean', 'false')}
        t.check('ROUTE-HEAD-REFUSES', all(v == 400 for v in refused.values()) and all(h[k].get('message') == 'Request body must be a JSON object' for k in refused), 'at HEAD every non-object JSON body gets 400 + "Request body must be a JSON object": %s' % refused)
        t.check('ROUTE-HEAD-CONTROL', h['badjson']['status'] == 400 and h['badjson'].get('message') == 'Invalid JSON body' and (h['object']['status'] != 400 or h['object'].get('message') != 'Request body must be a JSON object'),
                'controls: unparseable JSON gets its own 400 "Invalid JSON body"; a valid object is NOT refused by the object guard (status %s, message %r)' % (h['object']['status'], h['object'].get('message')))
    if res.get('HEAD') and res.get('M2'):
        diff = {k: (res['HEAD']['results'][k]['status'], res['M2']['results'][k]['status']) for k in res['HEAD']['results'] if (res['HEAD']['results'][k]['status'], res['HEAD']['results'][k].get('message')) != (res['M2']['results'][k]['status'], res['M2']['results'][k].get('message'))}
        t.info('ROUTE-M2-DELTA', 'shapes whose answer CHANGES when the call-site block is deleted (HEAD -> M2): %s | the builder: UNMEASURED for array / number / string / boolean (inferred from the failing set only)' % diff)
    return t.end()


# ---------------------------------------------------------------- static
def static(tree, out, repo, P, head, base):
    t = Tally(); F = get_files(repo, P, head, base); settle(t, tree, F, P); svc = os.path.join(tree, SVC); bin_ = os.path.join(tree, DEV, 'node_modules', '.bin'); os.makedirs(out, exist_ok=True)
    rc, so, se = lrun([bin_ + '/tsc', '--noEmit'], svc); open(out + '/tsc_head.out', 'w').write(so + se)
    t.check('TSC-PKG', rc == 0, 'tsc --noEmit (the package tsconfig; it EXCLUDES src/__tests__) at HEAD: rc %d, %d error lines' % (rc, so.count('error TS')))
    tsc = svc + '/tsconfig.g85-tests.json'; tn = P['test_file'].split(SVC + '/')[1]
    open(tsc, 'w').write(json.dumps({'extends': './tsconfig.json', 'files': [tn], 'include': ['src/**/*'], 'compilerOptions': {'noEmit': True}}))
    rcl, sol, sel = lrun([bin_ + '/tsc', '-p', tsc, '--listFilesOnly'], svc); own = [x for x in sol.split('\n') if x and '/node_modules/' not in x]; named = [x for x in own if x.endswith(tn)]
    rc2, so2, se2 = lrun([bin_ + '/tsc', '-p', tsc, '--noEmit'], svc); open(out + '/tsc_tests.out', 'w').write(so2 + se2)
    t.check('TSC-NAMING', rc2 == 0 and len(named) == 1 and 'error TS' not in so2, 'a program NAMING the changed test (extends the package tsconfig; files = [the test]): %d own-source files, the test named x%d, rc %d, %d errors (the builder: 88 own-source files, 1 test file, rc 0)' % (len(own), len(named), rc2, so2.count('error TS')))
    planted = svc + '/src/__tests__/zz_gate85_planted_control.ts'; open(planted, 'w').write('export const zz_gate85_planted: number = "not a number";\n')
    open(tsc, 'w').write(json.dumps({'extends': './tsconfig.json', 'files': [tn, 'src/__tests__/zz_gate85_planted_control.ts'], 'include': ['src/**/*'], 'compilerOptions': {'noEmit': True}}))
    rc3, so3, se3 = lrun([bin_ + '/tsc', '-p', tsc, '--noEmit'], svc)
    t.check('TSC-CONTROL', rc3 != 0 and so3.count('TS2322') == 1 and so3.count('TS6059') == 0, 'CONTROL: the same program with a planted TS2322 file: rc %d, TS2322 x%d, TS6059 x%d -> the type check can fail (the builder: rc 2, 1, 0)' % (rc3, so3.count('TS2322'), so3.count('TS6059')))
    os.remove(planted); os.remove(tsc)
    # eslint with the diff's hunk ranges
    def eslint(tag):
        rc, so, se = lrun([bin_ + '/eslint', 'src', '-f', 'json'], svc, timeout=900); open(out + '/eslint_%s.json' % tag, 'w').write(so)
        try: j = json.loads(so)
        except ValueError: return rc, None, se
        return rc, j, se
    rch, jh, seh = eslint('head')
    def counts(j): return (sum(f['errorCount'] for f in j), sum(f['warningCount'] for f in j)) if j else (None, None)
    eh = counts(jh)
    t.check('LINT-HEAD', rch == 0 and eh == (0, 36), 'eslint src at HEAD: rc %d, %s errors / warnings (want 0 / 36; the builder: rc 0, 0 errors, 36 warnings)' % (rch, eh))
    hunks = []
    d = git(repo, 'diff', '-U0', base, head, '--', P['product'])
    for m in re.finditer(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', d, re.M): hunks.append((int(m.group(3)), int(m.group(3)) + int(m.group(4) if m.group(4) is not None else 1) - 1))
    wl = [msg['line'] for f in (jh or []) if f['filePath'].endswith('routes/verification.ts') for msg in f['messages']]
    on_changed = [l for l in wl if any(a <= l <= b for a, b in hunks)]
    t.check('LINT-HUNKS', bool(wl) and not on_changed, 'the %d eslint messages in verification.ts at head are on lines %s; the diff\'s new-file hunk ranges are %s; messages ON a changed line: %s (located against the hunks, not by text search)' % (len(wl), wl, hunks, on_changed or 'none'))
    pl = Plant(tree); pl.put(P['product'], F['bp']); pl.put(P['test_file'], F['bt'])
    rcb, jb, seb = eslint('base'); eb = counts(jb); wlb = [msg['line'] for f in (jb or []) if f['filePath'].endswith('routes/verification.ts') for msg in f['messages']]
    bad = pl.restore()
    t.check('LINT-BASE', rcb == 0 and eb == (0, 36) and not bad, 'eslint src at BASE bytes: rc %d, %s errors / warnings; verification.ts warning lines at base %s -> head %s (shifts %s); restored %s' % (rcb, eb, wlb, wl, sorted(set(h - b for h, b in zip(wl, wlb))), not bad))
    return t.end()


# ---------------------------------------------------------------- docs / compose
def count_flow(doc, n): return doc.count('<h2>%s. ' % n)
def count_cheat(doc, key): return len([l for l in doc.split('\n') if '<h2' in l and key in l])


def h2s(doc): return re.findall(r'<h2[^>]*>(.*?)</h2>', doc, re.S)


def docs(tree, out, repo, P, head, base, develop):
    t = Tally(); docs_ = list(K['known_develop_overlap']); fl, ch = docs_
    try:
        mb, info = docs_base(repo, develop, head, base)
    except SystemExit as e:
        print(e); return 2
    t.check('DOC-BASE', mb == base, 'docs base = merge-base(develop %s, head %s) = %s == --base %s (head^ = %s)' % (develop[:12], head[:12], mb[:12], base[:12], info['head_parent'][:12]))
    os.makedirs(os.path.join(out, '_tmp'), exist_ok=True)
    rc, so, se = lrun(['bash', os.path.join(tree, 'systemTest', '__tests__', 'html_docs_matrix.test.sh')], tree, env={'TMPDIR': os.path.join(out, '_tmp')})
    m = re.findall(r'(\d+) passed, (\d+) failed', so)
    t.check('DOC-MATRIX', rc == 0 and m and m[-1] == ('12', '0'), 'html_docs_matrix.test.sh at the HEAD tree (cwd = the tree root, outside every repo): rc %d, %s (the builder: 12 passed, 0 failed)' % (rc, m[-1:]))
    comp = {}
    for i, d in enumerate(docs_):
        bd, hd, dd = show(repo, mb, d), show(repo, head, d), show(repo, develop, d)
        ok, frag, why = exact_tail_insert(bd, hd)
        okd = dd.endswith(TAIL)
        composed = dd[:-len(TAIL)] + frag + TAIL if ok and okd else ''
        comp[d] = (bd, hd, dd, frag, composed)
        fb = len(frag.encode()); want = K['docfacts'][d]['fragment_bytes']
        cnt_h = count_flow(hd, P['flow_block'].rstrip('.')) if i == 0 else count_cheat(hd, P['cheat_key'])
        cnt_c = (count_flow(composed, P['flow_block'].rstrip('.')) if i == 0 else count_cheat(composed, P['cheat_key'])) if composed else -1
        newh = Counter_diff(h2s(composed), h2s(dd)) if composed else None
        t.check('DOC-COUNT', ok and fb == want and cnt_h == 1 and cnt_c == 1 and composed and composed.replace(frag, '', 1) == dd and newh and len(newh[0]) == 1 and not newh[1],
                '%s: fragment %d B (kit %d), COUNT in the head doc %d, in the keep-both composed onto develop %d | composed minus the fragment == develop byte for byte: %s | headings added vs develop %s, headings DUPLICATED %s' % (
                    d.split('/')[-1][:36], fb, want, cnt_h, cnt_c, bool(composed) and composed.replace(frag, '', 1) == dd, newh[0] if newh else None, newh[1] if newh else None))
    # controls: drop / duplicate (a scratch tree for each)
    for ctl in ('DROP', 'DUP', 'KEEP'):
        td = os.path.join(out, 'docs_' + ctl); need_canonical(td, 'docs control tree')
        if os.path.exists(td): td = td + '_%d' % int(time.time())
        os.makedirs(td + '/Projects Documents'); shutil.copytree(os.path.join(tree, 'systemTest'), td + '/systemTest')
        for i, d in enumerate(docs_):
            bd, hd, dd, frag, composed = comp[d]
            txt = {'DROP': dd, 'DUP': dd[:-len(TAIL)] + frag + frag + TAIL, 'KEEP': composed}[ctl]
            open(os.path.join(td, d), 'w', encoding='utf-8').write(txt)
        rc, so, se = lrun(['bash', td + '/systemTest/__tests__/html_docs_matrix.test.sh'], td, env={'TMPDIR': os.path.join(out, '_tmp')})
        m = re.findall(r'(\d+) passed, (\d+) failed', so); cf = count_flow(open(td + '/' + fl, encoding='utf-8').read(), 57); cc = count_cheat(open(td + '/' + ch, encoding='utf-8').read(), P['cheat_key'])
        want_c = {'DROP': 0, 'DUP': 2, 'KEEP': 1}[ctl]
        t.check('DOC-' + ctl, rc == 0 and m and m[-1] == ('12', '0') and cf == want_c and cc == want_c, '%s composition: html_docs_matrix rc %d %s | COUNT flow `<h2>57.` x%d, cheat KS-1432 <h2> x%d (want %d each)%s' % (
            ctl, rc, m[-1:], cf, cc, want_c, ' -> the matrix is BLIND to this, the COUNT is the instrument' if ctl in ('DROP', 'DUP') else ''))
    tail = re.findall(r'<h2>(\d+)\. ', comp[fl][2])
    t.info('DOC-TAIL', 'flow numbers in document order on the develop you read (last 10): %s; highest %s; #1453 carries %s (open #1451 carries 55, #1452 carries 56 at the kit draft)' % (tail[-10:], max(int(x) for x in tail), P['flow_block']))
    return t.end()


def Counter_diff(new, old):
    from collections import Counter
    cn, co = Counter(new), Counter(old)
    added = [k for k in cn if cn[k] > co.get(k, 0)]; dup = [k for k in cn if co.get(k, 0) >= 1 and cn[k] > co[k]]
    return added, dup


def compose(clone, head, base, develop, others):
    t = Tally()
    try: must_be_outside(clone, 'clone')
    except SystemExit as e: print(e); return 2
    for s, n in ((head, 'head'), (base, 'base'), (develop, 'develop')):
        if not resolvable(clone, s): print('REFUSED: %s %s not in the clone (fetch BY SHA into YOUR clone)' % (n, s)); return 2
    rc, o, e = wgit(clone, 'merge-tree', '--write-tree', '--name-only', develop, head)
    names = [l for l in o.split('\n')[1:] if l and not l.startswith(('CONFLICT', 'Auto-merging'))]
    t.info('CMP-DEV', 'merge-tree --write-tree --name-only develop %s + head %s: rc %d, conflicted paths %s (develop == base: rc 0 and no paths expected; once develop moved, the two docs are the only expected paths)' % (develop[:12], head[:12], rc, names[:6] or 'none'))
    allowed = set(K['known_develop_overlap'])
    t.check('CMP-DEV-SET', set(names) <= allowed, 'conflict set is a subset of the two docs: %s' % (set(names) <= allowed))
    rc0, o0, e0 = wgit(clone, 'merge-tree', '--write-tree', '--name-only', develop, base)
    t.check('CMP-CONTROL', rc0 == 0, 'CONTROL develop + base (the PR\'s own base): rc %d, clean' % rc0)
    for lab, sha in others:
        if not resolvable(clone, sha): t.info('CMP-' + lab, 'head %s not in the clone: NOT RUN (fetch it BY SHA)' % sha[:12]); continue
        rc1, o1, e1 = wgit(clone, 'merge-tree', '--write-tree', '--name-only', head, sha)
        n1 = [l for l in o1.split('\n')[1:] if l and not l.startswith(('CONFLICT', 'Auto-merging'))]
        t.info('CMP-' + lab, '#%s head %s vs #1453 head: merge-tree rc %d, conflicted paths %s (INFO: the keep-both is the later merge seat\'s; the gate predicts only)' % (lab, sha[:12], rc1, n1))
    return t.end()


# ---------------------------------------------------------------- selftest
def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    base = "function f() {\n  const x = 1;\n        if (parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)) {\n          res.status(400);\n          return;\n        }\n  return x;\n}\n"
    s, e = block_after(base, "if (parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)) {")
    rep(base[:s] + base[e:] == "function f() {\n  const x = 1;\n  return x;\n}\n", 'block_after removes exactly the if-block (to its same-indent closing brace)')
    try: block_after(base + base, "if (parsed === null"); rep(False, 'block_after ACCEPTED a doubled anchor')
    except SystemExit: rep(True, 'block_after REFUSES an anchor found twice')
    try: block_after(base, 'no such anchor'); rep(False, 'block_after ACCEPTED a missing anchor')
    except SystemExit: rep(True, 'block_after REFUSES a missing anchor')
    head = "export function isAcceptableDocumentBody(parsed: unknown): boolean {\n  return !(parsed === null || typeof parsed !== 'object' || Array.isArray(parsed));\n}\n        if (!isAcceptableDocumentBody(parsed)) {\n          res.status(400);\n          return;\n        }\n"
    for k in ('M1', 'M2', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6'):
        new, d = mutate(k, head); rep(new != head, 'mutate %s changes the text (%s)' % (k, d[:60]))
    rep('return true;' in mutate('M1', head)[0] and 'isAcceptableDocumentBody(parsed)' not in mutate('M2', head)[0], 'M1 returns true; M2 removes every mention of the call site')
    try: mutate('M1', head + head); rep(False, 'mutate ACCEPTED a doubled predicate')
    except SystemExit: rep(True, 'mutate REFUSES a doubled anchor (the anchor must appear exactly once)')
    d = os.path.join(os.environ.get('TMPDIR') or '/private/tmp/claude-501', 'c3_selftest_%d' % os.getpid())
    ok_canon = canonical_tmp(d) if os.path.isdir('/private/tmp/claude-501') else True
    rep(ok_canon, 'canonical_tmp accepts a fresh path under /private/tmp/claude-501/ (under no repo)')
    rep(not canonical_tmp('/Volumes/DevMASTER/WEDNESDAY') and not canonical_tmp('/tmp/x') and not canonical_tmp('/Users'), 'canonical_tmp REFUSES a repo path, /tmp and /Users')
    os.makedirs(d + '/tree/a', exist_ok=True)
    pl = Plant(d + '/tree'); open(d + '/tree/a/f.txt', 'w').write('one\n')
    b, a, landed, changed = pl.put('a/f.txt', 'two\n')
    rep(landed and changed and a == blob_of_bytes(b'two\n'), 'Plant.put lands the bytes and reports before != after, after == the expected blob')
    rep(pl.restore() == [] and open(d + '/tree/a/f.txt').read() == 'one\n', 'Plant.restore returns the original bytes, blob-checked')
    b, a, landed, changed = pl.put('a/f.txt', 'one\n')
    rep(landed and not changed, 'Plant.put of identical bytes reads NOT CHANGED (a no-op plant is detectable: before == after)')
    pl.restore()
    toy = d + '/toy.json'; json.dump({'numTotalTests': 3, 'numPassedTests': 2, 'numFailedTests': 1, 'testResults': [{'name': '/x/a.test.ts', 'status': 'failed', 'assertionResults': [
        {'title': 't1', 'status': 'passed'}, {'title': 't2', 'status': 'passed'}, {'title': 't3', 'status': 'failed'}]}]}, open(toy, 'w'))
    j = json.load(open(toy)); rows = [(r['name'], a_.get('title'), a_['status']) for r in j['testResults'] for a_ in r['assertionResults']]
    rep(len(rows) == j['numTotalTests'] and sum(1 for x in rows if x[2] == 'failed') == j['numFailedTests'], 'JSON totals equal the summed per-cell rows on a toy report')
    lock = {'packages': {'node_modules/a': {'version': '1.0.0'}, 'node_modules/b': {'version': '2.0.0'}, '': {}}}; hidl = {'packages': {'node_modules/a': {'version': '1.0.0'}, 'node_modules/b': {'version': '2.0.1'}}}
    mism = [k for k, v in hidl['packages'].items() if k in lock['packages'] and lock['packages'][k].get('version') != v.get('version')]
    rep(mism == ['node_modules/b'], 'the nmcheck comparison reads a planted version difference as a mismatch')
    a_, b_ = Counter_diff(['x', 'y', 'y'], ['x', 'y']); rep(a_ == ['y'] and b_ == ['y'], 'Counter_diff: a duplicated heading is reported as added AND duplicated')
    a_, b_ = Counter_diff(['x', 'y', 'z'], ['x', 'y']); rep(a_ == ['z'] and b_ == [], 'Counter_diff: one new heading, no duplicate')
    rep(count_flow('<h2>57. a</h2><h2>57. b</h2>', 57) == 2 and count_flow('<h2>570. x', 57) == 0 and count_cheat('<h2>x KS-1432</h2>\n<h2>y</h2>', 'KS-1432') == 1, 'COUNT: two `<h2>57. ` read 2, `<h2>570. ` reads 0, the cheat <h2> carrying the key reads 1')
    rep('zz_gate85_route_shapes' not in ROUTE_TEST and 'G85_ROUTE_OUT' in ROUTE_TEST and 'createVerificationRoutes' in ROUTE_TEST and ROUTE_TEST.count("['") >= 8, 'the embedded route test carries its output knob, mounts createVerificationRoutes and lists >= 8 shapes')
    for foreign in (1450, 1451, 1452):
        try: PR(foreign); rep(False, '--pr %s ACCEPTED' % foreign)
        except SystemExit: rep(True, 'WRONG-PR ARM --pr %s -> refused' % foreign)
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A: print(__doc__); return 2
    cmd = A[0]
    try:
        if cmd == 'compose':
            oth = [(A[i + 1].split('=')[0], A[i + 1].split('=')[1]) for i, a in enumerate(A) if a == '--other' and i + 1 < len(A)]
            return compose(req(A, '--clone'), req(A, '--head', True), req(A, '--base', True), req(A, '--develop', True), oth)
        repo = req(A, '--repo'); P = PR('1453'); head = req(A, '--head', True); base = req(A, '--base', True); tree = req(A, '--tree')
        if head != P['head_expected'] and '--allow-other-head' not in A: print('NOTE: --head %s != the kit head %s (a moved head is NOT RUN at the gate)' % (head[:12], P['head_expected'][:12]))
        if cmd == 'prep': return prep(repo, P, head, base, tree, req(A, '--deps-from'))
        need_canonical(tree, 'tree')
        if cmd == 'nmcheck': return nmcheck(tree)
        out = req(A, '--out'); need_canonical(out, 'out dir')
        if cmd == 'cells': return cells(tree, out, repo, P, head, base)
        if cmd == 'suite': return suite(tree, out, repo, P, head, base)
        if cmd == 'mutations': return mutations(tree, out, repo, P, head, base, opt(A, '--only').split(',') if opt(A, '--only') else None)
        if cmd == 'route': return route(tree, out, repo, P, head, base)
        if cmd == 'static': return static(tree, out, repo, P, head, base)
        if cmd == 'docs': return docs(tree, out, repo, P, head, base, req(A, '--develop', True))
    except SystemExit as e:
        print(e); return 2
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
