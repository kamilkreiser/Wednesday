#!/usr/bin/env python3
"""drafter_tamper.py ROW... — #1017 ROUND 2 tampers on the HEAD tree (a067d4e3e) of the drafter clone: the seat's 7 rows in the SEAT'S OWN FORMS (read from its
tamper1195r2.py) + the gate rows G-BUCKET-HASH / G-BUCKET-CONNECTOR (commissioned) and G-BUCKET-RAW (drafter's). Each row: anchor count asserted = 1, marker
asserted = 1 where the form allows a marker (a seat form that is a pure deletion carries none: its sha change is asserted instead), project tsc --noEmit -p .
rc (non-compiling = VOID), WHOLE api-gateway suite with the denominator asserted 53/436 pending 0, optional probes under the row (PROBE env
'ROW=harness|label|stages|fake;...'), restore from saved bytes with sha256 == git HEAD blob and git diff --quiet. Never rm; stderr kept per run."""
import os, sys, json, hashlib, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import drafter_run as R
TREE = 'head'; WT = R.T[TREE]; GWP = WT + '/' + R.GW
AUTH = 'src/middleware/auth.ts'; RLE = 'src/middleware/rateLimitEnforce.ts'
DEN = (53, 436)
CONT = "      runWithTenantId(meta.tenantId, () => clientRateLimit(req, res, next));\n"
GUARD = "    if (countedRequests.has(req)) {\n      next();\n      return;\n    }\n"
FILTER = "    if (!user || !MACHINE_AUTH_METHODS.has(user.authMethod)) {\n"
BUCKET = "    const clientId = user.rateLimitBucket || user.connectorId || user.userId || 'unknown';\n"
ADD = "    countedRequests.add(req);\n"
HASHL = "        rateLimitBucket: `api_key:${createHash('sha256').update('secuura-rate-limit-bucket\\0').update(apiKey).digest('hex')}`,\n"
ROWS = {
 'T0': (None, None, None, 'seat 0'),
 'TA': (AUTH, CONT, "      runWithTenantId(meta.tenantId, next);\n", 'seat 8: R1/A3, A1, R2, R3, (a), (b), (c), F-2'),
 'G-ERASE': (RLE, GUARD, "", 'seat 2: R3, F-2 (seat form: the guard block deleted, the add kept)'),
 'TW': (RLE, FILTER, "    if (!user || (!MACHINE_AUTH_METHODS.has(user.authMethod) && false)) {\n", 'seat 6: JWT control + 5 interactive-method cells'),
 'TT': (AUTH, CONT, "      clientRateLimit(req, res, next);\n", 'seat 1: A2 context'),
 'G-BUCKET': (RLE, BUCKET, "    const clientId = user.connectorId || user.userId || 'unknown';\n", 'seat 3: (a), (b), (c)'),
 'TI': (RLE, ADD, "    countedRequests.add(req); // inert tamper\n", 'seat 0'),
 'G-BUCKET-HASH': (AUTH, HASHL, "        rateLimitBucket: `api_key:${createHash('sha256').update(apiKey).digest('hex')}`, // QA-TAMPER-GBUCKETHASH undomained = security key_hash\n", 'Wednesday-commissioned; drafter predicts 0 reds (no cell reads the bucket name)'),
 'G-BUCKET-CONNECTOR': (RLE, BUCKET, "    const clientId = user.connectorId || user.rateLimitBucket || user.userId || 'unknown'; // QA-TAMPER-GBUCKETCONNECTOR connector first\n", 'Wednesday-commissioned; drafter predicts 1 red: (b)'),
 'G-BUCKET-RAW': (AUTH, HASHL, "        rateLimitBucket: `api_key:${apiKey}`, // QA-TAMPER-GBUCKETRAW the raw key as the bucket\n", 'drafter: 0 reds predicted (no cell reads the bucket name)'),
 'G-BUCKET-RAW2': (AUTH, HASHL, "        rateLimitBucket: `api_key:${apiKey}${typeof createHash === 'function' ? '' : ''}`, // QA-TAMPER-GBUCKETRAW2 the raw key as the bucket (form 2 keeps a read of createHash: compiles)\n", 'drafter: 0 reds predicted (no cell reads the bucket name); form 1 was VOID (TS6133)'),
}
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def blob_ok(rel):
    b = subprocess.run(['git', '-C', WT, 'rev-parse', 'HEAD:' + R.GW + '/' + rel], capture_output=True, text=True).stdout.strip()
    h = subprocess.run(['git', 'hash-object', GWP + '/' + rel], capture_output=True, text=True).stdout.strip()
    return b == h, b[:9], h[:9]
PROBE = {}
for x in os.environ.get('PROBE', '').split(';'):
    if '=' in x:
        row, spec = x.split('=', 1); PROBE.setdefault(row, []).append(spec.split('|'))
results = []
outname = os.environ.get('TAMPER_OUT', 'tamper_rows')
for row in sys.argv[1:]:
    key = row.split('#')[0]
    rel, old, new, pred = ROWS[key]
    R.P('ROW-START', row, TREE, R.ts(), 'predicted-by', pred)
    dq0 = subprocess.run(['git', '-C', WT, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True); R.P('tracked porcelain before', len(dq0.stdout.splitlines()), dq0.stderr.strip()[:200]); assert not dq0.stdout.strip()
    if rel:
        p = GWP + '/' + rel; s = open(p).read(); saved = open(p, 'rb').read(); before = sha(p)
        c = s.count(old); R.P('anchor count', c); assert c == 1
        open(p, 'w').write(s.replace(old, new)); assert sha(p) != before
        mk = [w for w in new.split() if w.startswith('QA-TAMPER-')]
        if mk: mc = open(p).read().count(mk[0]); R.P('marker', mk[0], 'count', mc); assert mc == 1
        else: R.P('seat form (no marker): file sha changed', sha(p)[:12], '!=', before[:12])
    trc = R.tsc(TREE)
    r = R.vitest(TREE, [], 'tamper_%s' % row)
    for harness, label, stages, fake in PROBE.get(row, []):
        env = {'QA_STAGES': stages} if stages else {}
        if fake == '1': env['QA_FAKE_REDIS'] = '1'
        R.probe(TREE, 'tamper_%s_%s' % (row, label), env, harness)
    if rel:
        open(p, 'wb').write(saved); ok, b, h = blob_ok(rel); R.P('restore sha256 identical', sha(p) == before, 'HEAD blob', b, 'worktree', h, ok); assert ok and sha(p) == before
    dq = subprocess.run(['git', '-C', WT, 'diff', '--quiet'], capture_output=True, text=True); R.P('git diff --quiet rc', dq.returncode); assert dq.returncode == 0
    den_ok = bool(r) and (r['files'], r['tests']) == DEN and r['pending'] == 0
    R.P('DENOMINATOR', (r['files'], r['tests']) if r else None, 'expected', DEN, 'pending', r and r['pending'], 'OK' if den_ok else 'DENOMINATOR-MISMATCH')
    results.append(dict(row=row, tsc_rc=trc, void=trc != 0, files=r and r['files'], tests=r and r['tests'], failed=r and r['failed'], pending=r and r['pending'], failed_suites=r and r['failed_suites'],
                        reds=[x[0].split('/')[-1] + ' :: ' + x[1] for x in (r['notpassed'] if r else [])], decisive=[x[3].split('\n')[0][:200] for x in (r['notpassed'] if r else [])], predicted_by=pred, denominator_ok=den_ok))
    json.dump(results, open(R.GS + '/%s.json' % outname, 'w'), indent=1)
R.P('tamper end', R.ts())
