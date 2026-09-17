#!/usr/bin/env python3
"""redraft_tamper_1035.py [ROW ...] — #1035 (KS-1204) tamper table in the RE-DRAFTER clone's HEAD worktree (never the seat worktree, never the checkout).
The seat's 8 rows are taken from its runner's ROWS literal by PARSING (ast; GUARD / GUARD_BLOCK / PREC / ROWS evaluated by a literal-only evaluator: Constant,
Name of those four, str +, Tuple, List) — the runner is never executed (it hard-codes the seat worktree). Then the re-drafter's rows. Per row: every anchor count
1 (else VOID), project tsc --noEmit -p . (non-zero = VOID), the WHOLE api-gateway suite on vitest 4.1.11 (node Blockchain/Dev/node_modules/vitest/vitest.mjs),
60 s ceilings unless the row says default; denominator asserted = T0; reds split AssertionError / other; restore by bytes, blob sha asserted, git diff --quiet."""
import ast, hashlib, json, os, subprocess, sys, time, datetime, re
GS = os.path.dirname(os.path.abspath(__file__)); PA = json.load(open(GS + '/out/r2/paths.json')); WT = PA['trees']['head']
OUT = GS + '/out/r2/tamper'; os.makedirs(OUT, exist_ok=True); ONLY = set(sys.argv[1:])
DEV = WT + '/Blockchain/Dev'; GW = DEV + '/services/api-gateway'
VREL = 'Blockchain/Dev/services/api-gateway/src/routes/verification.ts'; HREL = 'Blockchain/Dev/services/api-gateway/src/services/health.ts'
SEAT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-17_seatA-7th/ks1204/build/tamper_1204.py'
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def sh(*a, cwd=None): return subprocess.run(list(a), cwd=cwd, capture_output=True, text=True)
def blob(b): return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()
src = open(SEAT).read(); print('seat runner sha256', hashlib.sha256(src.encode()).hexdigest()[:16], 'bytes', len(src), '| parsed, NOT executed', flush=True)
tree = ast.parse(src); env = {}
def ev(n):
    if isinstance(n, ast.Constant): return n.value
    if isinstance(n, ast.Name): return env[n.id]
    if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add): return ev(n.left) + ev(n.right)
    if isinstance(n, ast.Tuple): return tuple(ev(x) for x in n.elts)
    if isinstance(n, ast.List): return [ev(x) for x in n.elts]
    raise ValueError('non-literal node ' + type(n).__name__)
for node in tree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ('GUARD', 'GUARD_BLOCK', 'PREC', 'ROWS', 'DEV', 'EXPECT_HEAD'):
        env[node.targets[0].id] = ev(node.value)
print('seat literals parsed:', sorted(env), '| seat EXPECT_HEAD', env['EXPECT_HEAD'][:9], '| seat develop', env['DEV'][:9], flush=True)
ROWS = [(rid, VREL, edits, pred, names, t60) for rid, edits, pred, names, t60 in env['ROWS']]
G_ = env['GUARD']; PREC = env['PREC']
MSG = "message: 'Connector document-type allow-list is not a list; refusing until it is corrected'"
ROWS += [
 ('X-NULL-REFUSED', VREL, [(G_, "        if (rawAllowedTypes !== undefined && !Array.isArray(rawAllowedTypes)) {\n")], None, 'CONTROL aimed at a CONTROL cell: a stored null is refused too (absent / null / [] unrestricted must red)', True),
 ('X-UNTYPED-OPEN', VREL, [(G_, "        if (rawAllowedTypes !== undefined && rawAllowedTypes !== null && !Array.isArray(rawAllowedTypes) && (body.documentType || body.type)) {\n")], None, 'aimed at the REFUSAL: an untyped body passes a non-array list (veto 3 reversed)', True),
 ('X-STATUS-400', VREL, [("res.status(403).json({ success: false, error: { code: 'FORBIDDEN', " + MSG, "res.status(400).json({ success: false, error: { code: 'VALIDATION_ERROR', " + MSG)], None, 'aimed at the REFUSAL: 400 VALIDATION_ERROR instead of 403 FORBIDDEN (veto 1 reversed)', True),
 ('X-MSG-MEMBER', VREL, [(MSG, "message: `Connector is not permitted to register document type \"${String(body.documentType || body.type)}\"`")], None, 'aimed at the REFUSAL: the non-array refusal reuses the member-refusal message (can a reader tell them apart?)', True),
 ('X-OBJECT-AS-LIST', VREL, [(G_, "        if (rawAllowedTypes !== undefined && rawAllowedTypes !== null && typeof rawAllowedTypes !== 'object') {\n")], None, 'aimed at the REFUSAL predicate: any object (incl. {} and array-likes) counts as a list', True),
 ('X-DT-ONLY', VREL, [(PREC, "        const requestedType = body.documentType;\n")], None, 'CONTROL aimed at the ks1176 F control: the allow-list reads documentType only (type ignored)', True),
 ('X-INFO-ALWAYS-EMPTY', HREL, [("      allowedDocumentTypes: connectorConfig.allowedDocumentTypes || [],\n", "      allowedDocumentTypes: [],\n")], None, 'the SECOND reader (GET /api/connector/info) always tells [] (= all types permitted): does any cell see what a connector is told?', True),
]
HEAD_BLOBS = {r: sh('git', '-C', WT, 'rev-parse', 'HEAD:' + r).stdout.strip() for r in (VREL, HREL)}
assert sh('git', '-C', WT, 'status', '--porcelain', '--untracked-files=no').stdout == ''
table = []; T0 = {}
print('redraft_tamper_1035 start', now(), '| head worktree', WT[-40:], flush=True)
for rid, rel, edits, pred, names, t60 in ROWS:
    if ONLY and rid not in ONLY and rid != 'T0': continue
    F = WT + '/' + rel; orig = open(F, 'rb').read(); assert blob(orig) == HEAD_BLOBS[rel]
    row = {'id': rid, 'file': rel.split('/')[-1], 'seat_predicted': pred, 'names': names, 't60': t60}
    try:
        if edits == 'WHOLEFILE':
            devb = subprocess.run(['git', '-C', WT, 'show', PA['sha']['dev'] + ':' + rel], capture_output=True).stdout
            open(F, 'wb').write(devb); row['anchors'] = 'whole-file develop %s blob %s' % (PA['sha']['dev'][:9], blob(devb)[:9])
        elif edits:
            text = orig.decode(); counts = []
            for a, b in edits:
                n = text.count(a); counts.append(n)
                if n != 1: break
                text = text.replace(a, b)
            row['anchors'] = counts
            if any(c != 1 for c in counts):
                row['VOID'] = 'anchor counts %s' % counts; table.append(row); print(json.dumps(row), flush=True); continue
            open(F, 'wb').write(text.encode())
        row['applied'] = (blob(open(F, 'rb').read()) != HEAD_BLOBS[rel]) or not edits
        row['tsc_rc'] = sh('node', DEV + '/node_modules/typescript/bin/tsc', '--noEmit', '-p', '.', cwd=GW).returncode
        jf = OUT + '/%s.vitest.json' % rid
        cmd = ['node', DEV + '/node_modules/vitest/vitest.mjs', 'run', '--reporter=json', '--outputFile=' + jf] + (['--testTimeout=60000', '--hookTimeout=60000'] if t60 else [])
        row['load'] = '%.1f/%.1f/%.1f' % os.getloadavg(); t0 = time.time()
        e2 = dict(os.environ, CI='1'); e2.pop('NODE_ENV', None)
        v = subprocess.run(cmd, cwd=GW, capture_output=True, text=True, env=e2); row['secs'] = round(time.time() - t0, 1)
        open(OUT + '/%s.vitest.out' % rid, 'w').write(v.stdout[-4000:] + '\n--- stderr ---\n' + v.stderr[-6000:])
        d = json.load(open(jf)); row['files'] = len(d['testResults']); row['tests'] = d['numTotalTests']; row['pending'] = d['numPendingTests']
        reds, other = [], []
        for f in d['testResults']:
            if f['status'] != 'passed' and not f['assertionResults']: other.append('FILE-LOAD %s: %s' % (f['name'].split('/')[-1], (f.get('message') or '')[:160]))
            for t in f['assertionResults']:
                if t['status'] == 'failed':
                    msg = (t.get('failureMessages') or [''])[0]
                    item = '%s :: %s :: %s' % (f['name'].split('/')[-1][:40], t['title'][:100], re.sub(r'\s+', ' ', msg.splitlines()[0] if msg else '')[:130])
                    (reds if msg.startswith('AssertionError') else other).append(item)
        if rid == 'T0': T0.update(files=row['files'], tests=row['tests'])
        row['denominator_equal_T0'] = (row['files'], row['tests'], row['pending']) == (T0.get('files'), T0.get('tests'), 0)
        if row['tsc_rc'] != 0: row['VOID'] = 'tsc non-zero'
        row['reds'] = len(reds); row['red_cells'] = reds; row['non_assertion'] = other
        if pred is not None: row['as_seat_predicted'] = len(reds) == pred and not other and row['denominator_equal_T0'] and 'VOID' not in row
    finally:
        open(F, 'wb').write(orig)
        row['restored_blob_equal'] = blob(open(F, 'rb').read()) == HEAD_BLOBS[rel]
        row['git_diff_quiet'] = subprocess.run(['git', '-C', WT, 'diff', '--quiet', 'HEAD']).returncode == 0
    table.append(row)
    print(now(), json.dumps({k: v for k, v in row.items() if k not in ('red_cells', 'names')}), flush=True)
    for r in row['red_cells']: print('   RED', r, flush=True)
    for r in row['non_assertion']: print('   NON-ASSERTION', r, flush=True)
    json.dump(table, open(OUT + '/tamper_table.json', 'w'), indent=1)
seat = [r for r in table if r['seat_predicted'] is not None]
print('SEAT ROWS AS PREDICTED: %d / %d | seat reds total %d' % (sum(bool(r.get('as_seat_predicted')) for r in seat), len(seat), sum(r.get('reds', 0) for r in seat)))
print('porcelain at end:', repr(sh('git', '-C', WT, 'status', '--porcelain', '--untracked-files=no').stdout), '| end', now())
