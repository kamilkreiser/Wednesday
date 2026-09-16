#!/usr/bin/env python3
"""drafter_tamper.py ROW... — the seat's 6 rows + the gate's own tampers on the HEAD tree (cbe29597d; api-gateway tree c133f38f6 = 973eb49ef's, where the seat ran)
of the drafter clone. Each row: text anchor count asserted = 1, marker asserted = 1, project tsc --noEmit -p . rc (a non-compiling tamper is VOID), whole
api-gateway suite with the denominator asserted 53/432 pending 0, optional probe stages under the tamper (PROBE=<row>:<stages>;...), restore from saved bytes
with sha256 == git HEAD blob and `git diff --quiet` asserted. Never rm; stderr kept per run."""
import os, sys, json, hashlib, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import drafter_run as R
TREE = 'head'; WT = R.T[TREE]; GWP = WT + '/' + R.GW
AUTH = 'src/middleware/auth.ts'; RLE = 'src/middleware/rateLimitEnforce.ts'
DEN = (53, 432)
KEYB = "      runWithTenantId(meta.tenantId, () => clientRateLimit(req, res, next));\n"
GUARD = "    if (countedRequests.has(req)) {\n      next();\n      return;\n    }\n    countedRequests.add(req);\n"
FILTER = "    if (!user || !MACHINE_AUTH_METHODS.has(user.authMethod)) {\n"
MSET = "const MACHINE_AUTH_METHODS = new Set(['api_key', 'oauth_app']);\n"
CLIENT = "    const clientId = user.connectorId || user.userId || 'unknown';\n"
ROWS = {
 'T0': (None, None, None, 'READY 0'),
 'TA': (AUTH, KEYB, "      runWithTenantId(meta.tenantId, next); // QA-TAMPER-TA key branch continues with next\n", 'READY 4 (R1/A3, A1, R2, R3)'),
 'TG': (RLE, "    if (countedRequests.has(req)) {\n", "    if (countedRequests.has(req) && false) { // QA-TAMPER-TG once-per-request guard disabled (form 2: compiles)\n", 'READY 1 (R3); = G-ERASE on the whole suite'),
 'TW': (RLE, FILTER, "    if (!user || (false && !MACHINE_AUTH_METHODS.has(user.authMethod))) { // QA-TAMPER-TW machine filter widened to every user (form 2: compiles)\n", 'READY 6 (JWT control + 5 rateLimitEnforce interactive-method cells; seat predicted 1)'),
 'TT': (AUTH, KEYB, "      clientRateLimit(req, res, next); // QA-TAMPER-TT limiter and continuation outside runWithTenantId\n", 'READY 1 (A2-context)'),
 'TI': (RLE, MSET, "// QA-TAMPER-TI inert comment\n" + MSET, 'READY 0'),
 'G-CTRL': (RLE, MSET, "const MACHINE_AUTH_METHODS = new Set(['api_key', 'oauth_app', 'email']); // QA-TAMPER-GCTRL aimed at the JWT control\n", 'drafter: aimed at the JWT control (authMethod email)'),
 'G-OAUTH': (RLE, MSET, "const MACHINE_AUTH_METHODS = new Set(['api_key', 'oauth_app', 'oauth']); // QA-TAMPER-GOAUTH the real OAuth producer limited\n", "drafter: auth signs authMethod 'oauth' (READ); no cell pins it"),
 'G-KEYSCOPE': (RLE, CLIENT, "    const clientId = (req as any).ip || 'unknown'; // QA-TAMPER-GKEYSCOPE counter keyed per IP\n", 'drafter: counter keyed per IP instead of per key'),
 'G-AFTER': (AUTH, KEYB, "      runWithTenantId(meta.tenantId, () => { next(); void clientRateLimit(req, res, () => {}); }); // QA-TAMPER-GAFTER limiter after next\n", 'drafter: limiter moved after next() (item 8)'),
}
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def blob_ok(rel):
    b = subprocess.run(['git', '-C', WT, 'rev-parse', 'HEAD:' + R.GW + '/' + rel], capture_output=True, text=True).stdout.strip()
    h = subprocess.run(['git', 'hash-object', GWP + '/' + rel], capture_output=True, text=True).stdout.strip()
    return b == h, b[:9], h[:9]
PROBE = dict(x.split(':', 1) for x in os.environ.get('PROBE', '').split(';') if ':' in x)
results = []
for row in sys.argv[1:]:
    rel, old, new, pred = ROWS[row]
    R.P('ROW-START', row, TREE, R.ts(), 'predicted-by', pred)
    dq0 = subprocess.run(['git', '-C', WT, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True); R.P('tracked porcelain before', len(dq0.stdout.splitlines())); assert not dq0.stdout.strip()
    if rel:
        p = GWP + '/' + rel; s = open(p).read(); saved = open(p, 'rb').read(); before = sha(p)
        c = s.count(old); R.P('anchor count', c); assert c == 1
        open(p, 'w').write(s.replace(old, new))
        mk = 'QA-TAMPER-' + row.replace('-', '').replace('G', 'G', 1) if False else [w for w in new.split() if w.startswith('QA-TAMPER-')][0]
        mc = open(p).read().count(mk); R.P('marker', mk, 'count', mc); assert mc == 1
    trc = R.tsc(TREE)
    r = R.vitest(TREE, [], 'tamper_%s' % row)
    if row in PROBE:
        R.probe(TREE, 'qa1017-drafter-probe.test.ts', 'probe_tamper_%s' % row, 'rows_probe_tamper_%s.json' % row, {'QA_STAGES': PROBE[row], **({'QA_AUDIT': '1'} if 'order' in PROBE[row] else {})})
    if rel:
        open(p, 'wb').write(saved); ok, b, h = blob_ok(rel); R.P('restore sha256 identical', sha(p) == before, 'HEAD blob', b, 'worktree', h, ok); assert ok and sha(p) == before
    dq = subprocess.run(['git', '-C', WT, 'diff', '--quiet'], capture_output=True, text=True); R.P('git diff --quiet rc', dq.returncode); assert dq.returncode == 0
    den_ok = bool(r) and (r['files'], r['tests']) == DEN and r['pending'] == 0
    R.P('DENOMINATOR', (r['files'], r['tests']) if r else None, 'expected', DEN, 'pending', r and r['pending'], 'OK' if den_ok else 'DENOMINATOR-MISMATCH')
    results.append(dict(row=row, tsc_rc=trc, void=trc != 0, files=r and r['files'], tests=r and r['tests'], failed=r and r['failed'], pending=r and r['pending'], failed_suites=r and r['failed_suites'],
                        reds=[x[0].split('/')[-1] + ' :: ' + x[1] for x in (r['notpassed'] if r else [])], decisive=[x[3].split('\n')[0][:200] for x in (r['notpassed'] if r else [])], predicted_by=pred, denominator_ok=den_ok))
    json.dump(results, open(R.GS + '/tamper_head_%s.json' % '_'.join(sys.argv[1:])[:90], 'w'), indent=1)
R.P('tamper end', R.ts())
