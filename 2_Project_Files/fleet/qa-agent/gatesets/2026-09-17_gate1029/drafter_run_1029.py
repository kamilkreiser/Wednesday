#!/usr/bin/env python3
"""drafter_run_1029.py — #1029 (KS-1180 part 1) TIER 2 drafter measurements in the drafter's OWN clone (paths from drafter_paths.json; never the checkout).
1. api-gateway suites (vitest JSON) at current develop, head, merged; project tsc -p . rc per tree.
2. The test-including tsc program (auth-style: api-gateway's tsconfig EXCLUDES src/__tests__) at develop and head: errors in the ks1072 file, with a planted control.
3. The tamper table on the head worktree, WHOLE api-gateway suite per row: the seat's 5 (forms copied from the seat's tamper.py) + the drafter's rows.
   Each row: anchored edits (count 1 each, marker 'qa1029'), tsc -p ., vitest JSON, restore by bytes + blob sha + git diff --quiet. Reds classified
   by failure message: WITNESS (the KS-1180 message), CONTROL (the KS-1180 control message), STATUS, TXHASH, OTHER; non-AssertionError and load failures separated.
Never rm, never cd (subprocess cwd= only)."""
import hashlib, json, os, subprocess, sys, time, datetime
from collections import Counter
GS = os.path.dirname(os.path.abspath(__file__)); OUT = GS + '/out'
PATHS = json.load(open(GS + '/drafter_paths.json'))
REL_GW = 'Blockchain/Dev/services/api-gateway'
KS = 'ks1072-the-latest-anchor-selector-documents-a.test.ts'
TREL = REL_GW + '/src/__tests__/' + KS
PRE_BLOB = '4ad1cdcd1e45044efdbb0b8e4e6eaf358453d780'; HEAD_BLOB = 'd9c98320ea64638c3ab5ef2f35c102aba6d1207a'
def now(f='%Y-%m-%d %H:%M:%S %Z'): return datetime.datetime.now().astimezone().strftime(f)
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def blob_sha(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
def gw(tree): return PATHS['trees'][tree] + '/' + REL_GW
def vitest(tree, tag):
    jf = f'{OUT}/vt_{tag}.json'
    with open(f'{OUT}/vt_{tag}.out', 'w') as fo:
        subprocess.run([gw(tree) + '/../../node_modules/.bin/vitest', 'run', '--reporter=json', '--outputFile=' + jf], cwd=gw(tree), stdout=fo, stderr=subprocess.STDOUT)
    return json.load(open(jf))
def tsc(tree, tag, proj='.'):
    with open(f'{OUT}/tsc_{tag}.out', 'w') as fo:
        return subprocess.run([gw(tree) + '/../../node_modules/.bin/tsc', '--noEmit', '-p', proj], cwd=gw(tree), stdout=fo, stderr=subprocess.STDOUT).returncode
def summary(d):
    files = len(d['testResults']); fail = [(os.path.basename(r['name']), a['title'], (a['failureMessages'] or [''])[0]) for r in d['testResults'] for a in r['assertionResults'] if a['status'] == 'failed']
    lf = [os.path.basename(r['name']) for r in d['testResults'] if r['status'] != 'passed' and not r['assertionResults']]
    return dict(files=files, tests=d['numTotalTests'], passed=d['numPassedTests'], failed=d['numFailedTests'], pending=d['numPendingTests'], load_fail=lf), fail
P('drafter_run_1029', now())
# ---- 1. suites + project tsc
SUITES = {}
for tree in ('curdev', 'head', 'merged'):
    t0 = time.time(); d = vitest(tree, 'suite_' + tree); s, fail = summary(d); s['tsc_rc'] = tsc(tree, 'project_' + tree); s['secs'] = round(time.time() - t0)
    ks = [a for r in d['testResults'] if r['name'].endswith(KS) for a in r['assertionResults']]
    s['ks1072_cells'] = [(a['status'], a['title']) for a in ks]
    SUITES[tree] = s; P(now('%H:%M:%S'), 'suite', tree, PATHS['sha'][tree][:9], {k: v for k, v in s.items() if k != 'ks1072_cells'}, '| failed', fail[:3])
    for st, ti in s['ks1072_cells']: P('     ks1072 cell', st, ti)
json.dump(SUITES, open(OUT + '/suites.json', 'w'), indent=1)
# ---- 2. test-including tsc program
INC = '{"extends": "./tsconfig.json", "include": ["src/**/*"], "exclude": ["node_modules", "dist"]}\n'
PLANT_ANCHOR = "const DOC_ID = 'doc-ks1072';\n"
for tree in ('curdev', 'head'):
    cfg = gw(tree) + '/tsconfig.qa1029-including.json'
    assert not os.path.exists(cfg); open(cfg, 'w').write(INC)
    lf = subprocess.run([gw(tree) + '/../../node_modules/.bin/tsc', '--noEmit', '-p', 'tsconfig.qa1029-including.json', '--listFilesOnly'], cwd=gw(tree), capture_output=True, text=True).stdout.splitlines()
    rc = tsc(tree, 'including_' + tree, 'tsconfig.qa1029-including.json'); lines = open(f'{OUT}/tsc_including_{tree}.out').read().splitlines()
    err = [l for l in lines if ': error TS' in l]; mine = [l for l in err if KS in l]
    P(now('%H:%M:%S'), 'including program', tree, '| listFilesOnly ks1072 in program', sum(1 for l in lf if l.endswith(KS)), '| __tests__ files', sum(1 for l in lf if '/src/__tests__/' in l),
      '| rc', rc, '| error lines', len(err), '| in ks1072', len(mine), mine[:3])
    if tree == 'head':
        tp = gw(tree) + '/src/__tests__/' + KS; orig = open(tp, 'rb').read(); txt = orig.decode(); assert txt.count(PLANT_ANCHOR) == 1
        open(tp, 'w').write(txt.replace(PLANT_ANCHOR, PLANT_ANCHOR + "const QA_PLANT_1029: number = 'not-a-number'; // qa1029 plant\n"))
        try:
            rc2 = tsc(tree, 'including_head_plant', 'tsconfig.qa1029-including.json')
        finally:
            open(tp, 'wb').write(orig)
        pl = [l for l in open(f'{OUT}/tsc_including_head_plant.out').read().splitlines() if ': error TS' in l and KS in l]
        P('   planted control (head ks1072 + one bad const): rc', rc2, '| errors in ks1072', len(pl), [l.split(': error ')[1][:60] for l in pl], '| restored sha', blob_sha(open(tp, 'rb').read()) == HEAD_BLOB)
    os.rename(cfg, cfg + '.quarantined-qa1029')
# ---- 3. tampers
WT = PATHS['trees']['head']; GWP = gw('head'); VER = GWP + '/src/routes/verification.ts'; TST = GWP + '/src/__tests__/' + KS
PRE_BYTES = subprocess.run(['git', '-C', PATHS['C'], 'cat-file', 'blob', PRE_BLOB], capture_output=True).stdout; assert blob_sha(PRE_BYTES) == PRE_BLOB
ORIG_STUB = "  originate = http.createServer((_req, res) => {\n    res.writeHead(404, jsonHead);\n    res.end('{}');\n  });\n"
SEAT_GT2 = "  originate = http.createServer((req, res) => {\n    if (req.url === '/api/documents/' + DOC_ID) { res.writeHead(200, jsonHead); res.end(JSON.stringify({ id: DOC_ID, contentHash: CONTENT_HASH, status: 'anchored' })); return; }\n    res.writeHead(404, jsonHead);\n    res.end('{}');\n  });\n"
GT2X = ("  originate = http.createServer((req, res) => {\n"
        "    const qaExpect = ['b', 'd', '2', '3', 'e'].map((c) => c.repeat(64)); // qa1029 GT2-X: tier 1 answers the txHash each cell expects\n"
        "    const qaHit = (anchorStoreRows || []).map((r) => String(r.transaction_hash)).find((h) => qaExpect.includes(h));\n"
        "    if (req.url === '/api/documents/' + DOC_ID && qaHit) { res.writeHead(200, jsonHead); res.end(JSON.stringify({ id: DOC_ID, contentHash: CONTENT_HASH, status: 'anchored', blockchain: { txHash: qaHit, blockHeight: 7, status: 'confirmed' } })); return; }\n"
        "    res.writeHead(404, jsonHead);\n    res.end('{}');\n  });\n")
V_T2 = "      doc = await fetchDocFromAnchorStore(id, authHeader);\n"
V_LOOKUP = "    let lookupSource: 'originate' | 'anchor_store' | 'mock' | null = doc ? 'originate' : null;\n"
T_ONMISS = "    const onMiss = (req: { url?: string }): void => { missUrls.push(String(req.url)); };\n"
T_PORT = "  const anchorPort = (anchorServer.address() as AddressInfo).port;\n"
# row: id, [(file, anchor, replacement)], use_pre_test_blob, predicted ks1072 reds, predicted other-file reds, predicted_by, note
ROWS = [
 ('T0', [], False, 0, {}, 'seat', 'no edit'),
 ('GREREAD', [(VER, V_T2, "      doc = (await fetchDocFromAnchorStore(id, authHeader)) && (await fetchDocFromAnchorStore(id, authHeader));\n")], False, 5, {}, 'seat', 'a hit reads the anchor store twice; a miss short-circuits'),
 ('GT2', [(TST, ORIG_STUB, SEAT_GT2)], False, 5, {}, 'seat', 'seat form: tier 1 answers a doc WITHOUT a blockchain block'),
 ('TTIER2', [(VER, "    if (!doc) {\n      doc = await fetchDocFromAnchorStore(id, authHeader);\n", "    if (true) {\n      doc = await fetchDocFromAnchorStore(id, authHeader);\n")], False, 0,
  {'ks1057': 4, 'ks1069': 2, 'ks1071': 3, 'ks1073': 1, 'ks1123': 2, 'ks1176': 1}, 'seat', 'tier 2 asked even when tier 1 answered'),
 ('TI', [(VER, V_T2, "      // tamper TI: inert comment\n" + V_T2)], False, 0, {}, 'seat', 'inert'),
 ('D-GT2-SEAT@PRE', [(TST, ORIG_STUB, SEAT_GT2)], True, 5, {}, 'drafter', 'the seat GT2 against the PRE-PR test blob 4ad1cdcd1 (old source guard): does the seat row discriminate new witness from old guard?'),
 ('D-GT2X', [(TST, ORIG_STUB, GT2X)], False, 5, {}, 'drafter', 'the #1016 gate GT2: tier 1 answers the txHash each cell expects (source persisted)'),
 ('D-GT2X@PRE', [(TST, ORIG_STUB, GT2X)], True, 0, {}, 'drafter', 'same on the PRE-PR test blob: P-1016-1 re-measured (the old guard stays green)'),
 ('D-GREREAD@PRE', [(VER, V_T2, "      doc = (await fetchDocFromAnchorStore(id, authHeader)) && (await fetchDocFromAnchorStore(id, authHeader));\n")], True, 0, {}, 'drafter', 'the seat GREREAD against the PRE-PR test blob'),
 ('D-T1-ALSO-READ', [(TST, ORIG_STUB, GT2X), (VER, V_LOOKUP, V_LOOKUP + "    if (doc) { await fetchDocFromAnchorStore(id, authHeader); } // qa1029 D-T1-ALSO-READ: tier 1 answered AND one discarded anchor-store read\n")], False, 0, {}, 'drafter',
  'tier 1 answers the expected hash AND the product makes exactly one discarded anchor-store read: the witness blind spot'),
 ('D-DOUBLE-ALWAYS', [(VER, V_T2, "      await fetchDocFromAnchorStore(id, authHeader); doc = await fetchDocFromAnchorStore(id, authHeader); // qa1029 D-DOUBLE-ALWAYS\n")], False, 6, {}, 'drafter', 'two reads on hits AND misses: the control count bound fires'),
 ('D-DEAF-MISS', [(TST, T_ONMISS, "    const onMiss = (req: { url?: string }): void => { void req; }; // qa1029 D-DEAF-MISS: the control listener never records\n")], False, 1, {}, 'drafter', 'the new control can fail'),
 ('D-ENV-LIVE', [(TST, T_PORT, T_PORT + "  process.env.ANCHORING_SERVICE_URL = 'http://127.0.0.1:' + String(anchorPort); // qa1029 D-ENV-LIVE: the live scan base = the stub\n")], False, 5, {}, 'drafter',
  'tier 2 still answers, but the live-scan call also lands on the stub: the witness counts every stub request (over-strict)'),
]
def committed(p): return subprocess.run(['git', '-C', WT, 'rev-parse', 'HEAD:' + os.path.relpath(p, WT)], capture_output=True, text=True).stdout.strip()
assert not subprocess.run(['git', '-C', WT, 'status', '--porcelain=v1', '--untracked-files=no'], capture_output=True, text=True).stdout.strip(), 'head worktree dirty'
res = []
for rid, edits, pre, pred, opred, by, note in ROWS:
    t0 = time.time(); origs = {p: open(p, 'rb').read() for p in (VER, TST)}
    assert all(blob_sha(b) == committed(p) for p, b in origs.items()), rid
    try:
        if pre: open(TST, 'wb').write(PRE_BYTES)
        for f, a, r in edits:
            txt = open(f, 'rb').read().decode(); n = txt.count(a)
            if n != 1: raise SystemExit(f'{rid}: anchor count {n} in {os.path.basename(f)}')
            open(f, 'wb').write(txt.replace(a, r).encode())
        marks = sum(open(p, 'rb').read().decode().count('qa1029') + open(p, 'rb').read().decode().count('tamper TI') for p in (VER, TST))
        trc = tsc('head', 'tamper_' + rid)
        d = vitest('head', 'tamper_' + rid)
    finally:
        for p, b in origs.items(): open(p, 'wb').write(b)
    restored = all(blob_sha(open(p, 'rb').read()) == committed(p) for p in (VER, TST))
    quiet = subprocess.run(['git', '-C', WT, 'diff', '--quiet', 'HEAD']).returncode == 0
    s, fail = summary(d)
    ks = [(t, m) for f, t, m in fail if f == KS]; oth = Counter(f.split('-')[0] for f, t, m in fail if f != KS)
    def cls(m):
        if 'KS-1180: tier 2 answered' in m: return 'WITNESS'
        if 'KS-1180 control' in m: return 'CONTROL'
        if 'expected 404 to be 200' in m or 'to be 200' in m: return 'STATUS'
        if "to be '" in m: return 'TXHASH'
        return 'OTHER'
    classes = Counter(cls(m) for t, m in ks)
    nonassert = [m[:80] for f, t, m in fail if not m.startswith('AssertionError')]
    row = dict(id=rid, by=by, pre_test_blob=pre, ks1072_reds=len(ks), pred=pred, classes=dict(classes), red_titles=[t for t, m in ks], first_msgs=[m.splitlines()[0][:160] for t, m in ks[:2]],
               other=dict(oth), other_pred=opred, non_assert=nonassert, denom=(s['files'], s['tests'], s['pending']), load_fail=s['load_fail'], tsc=trc, markers=marks,
               as_predicted=(len(ks) == pred and dict(oth) == opred and trc == 0 and not s['load_fail']), restored=restored, quiet=quiet, secs=round(time.time() - t0), note=note)
    res.append(row); json.dump(res, open(OUT + '/tamper_rows.json', 'w'), indent=1)
    P(now('%H:%M:%S'), json.dumps({k: row[k] for k in ('id', 'ks1072_reds', 'pred', 'classes', 'other', 'denom', 'tsc', 'markers', 'as_predicted', 'restored', 'quiet', 'secs')}))
    for t, m in ks: P('     red', repr(t[:90]), '|', m.splitlines()[0][:150])
    if not (restored and quiet): raise SystemExit('RESTORE FAILED ' + rid)
P('rows', len(res), 'as predicted', sum(r['as_predicted'] for r in res), '| slips', [r['id'] for r in res if not r['as_predicted']])
P('drafter_run_1029 end', now())
