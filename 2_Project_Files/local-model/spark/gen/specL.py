import importlib.util,sys,os
_s=importlib.util.spec_from_file_location('si','/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/47e67e09-3cbe-4324-a237-cb248e143809/scratchpad/gen/specI.py'); _m=importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
P1='Blockchain/Dev/services/api-gateway/src/routes/batch.ts'
P2='Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts'
TP='Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-the-batch-and-audit-export-upstream-fetches-are-bounded.test.ts'
B1=("const TRANSFER_SERVICE_URL = process.env.TRANSFER_SERVICE_URL || 'http://localhost:4004';\n",
"""const TRANSFER_SERVICE_URL = process.env.TRANSFER_SERVICE_URL || 'http://localhost:4004';

// KS-1240: the batch fan-out fetch carries a timeout signal. Without one an originate or transfer service that never answers holds the whole batch request open. On expiry the fetch rejects and the existing
// catch in proxyRequest returns `{ ok: false, error }` for that item, as it already does for an unreachable service.
const UPSTREAM_BATCH_FETCH_TIMEOUT_MS = 30_000;
""")
B2=("    const response = await fetch(`${baseUrl}${path}`, {\n","    const response = await fetch(`${baseUrl}${path}`, {\n      signal: AbortSignal.timeout(UPSTREAM_BATCH_FETCH_TIMEOUT_MS),\n")
A1=("const SECURITY_SERVICE_URL = process.env.SECURITY_SERVICE_URL || 'http://localhost:4005';\n",
"""const SECURITY_SERVICE_URL = process.env.SECURITY_SERVICE_URL || 'http://localhost:4005';

// KS-1240: the audit-log fetch carries a timeout signal. Without one a security service that never answers holds the export request open. On expiry the fetch rejects and the existing catch answers the
// constant 502 BAD_GATEWAY, as it already does for an unreachable service.
const UPSTREAM_AUDIT_FETCH_TIMEOUT_MS = 30_000;
""")
A2=("        { method: 'GET', headers },\n","        { method: 'GET', headers, signal: AbortSignal.timeout(UPSTREAM_AUDIT_FETCH_TIMEOUT_MS) },\n")
T=_m.TEST
T=T.replace("api-gateway routes/proxy.ts and routes/admin.ts","api-gateway routes/batch.ts and routes/audit-export.ts")
T=T.replace("the hand-built upstream fetches in these two files carried no timeout","the upstream fetch in each of these two files carried no timeout")
T=T.replace("(the key-exchange half of the same ticket is in middleware/auth.ts)","(the key-exchange half of the same ticket is in middleware/auth.ts, the proxy.ts and admin.ts half is another file)")
T=T.replace("const PROXY_SRC = readFileSync(join(__dirname, '..', 'routes', 'proxy.ts'), 'utf8');","const BATCH_SRC = readFileSync(join(__dirname, '..', 'routes', 'batch.ts'), 'utf8');")
T=T.replace("const ADMIN_SRC = readFileSync(join(__dirname, '..', 'routes', 'admin.ts'), 'utf8');","const AUDIT_SRC = readFileSync(join(__dirname, '..', 'routes', 'audit-export.ts'), 'utf8');")
i=T.index("describe('KS-1240")
T=T[:i]+'''describe('KS-1240: the batch and audit-export upstream fetches are bounded', () => {
  it('RED KS-1240 R1 every fetch call in batch.ts carries an AbortSignal.timeout', () => {
    expect(unbounded(BATCH_SRC)).toEqual([]);
  });

  it('RED KS-1240 R2 every fetch call in audit-export.ts carries an AbortSignal.timeout', () => {
    expect(unbounded(AUDIT_SRC)).toEqual([]);
  });

  it('RED KS-1240 R3 batch.ts declares its timeout constant, positive and at most 120000 ms', () => {
    const ms = constantMs(BATCH_SRC, 'UPSTREAM_BATCH_FETCH_TIMEOUT_MS');
    expect(ms).toBeGreaterThan(0);
    expect(ms).toBeLessThanOrEqual(120000);
  });

  it('RED KS-1240 R4 audit-export.ts declares its timeout constant, positive and at most 120000 ms', () => {
    const ms = constantMs(AUDIT_SRC, 'UPSTREAM_AUDIT_FETCH_TIMEOUT_MS');
    expect(ms).toBeGreaterThan(0);
    expect(ms).toBeLessThanOrEqual(120000);
  });

  it('control KS-1240 C1 batch.ts has exactly one fetch call', () => {
    expect(fetchCalls(BATCH_SRC)).toHaveLength(1);
  });

  it('control KS-1240 C2 audit-export.ts has exactly one fetch call', () => {
    expect(fetchCalls(AUDIT_SRC)).toHaveLength(1);
  });

  it('control KS-1240 C3 the extractor reads a call whose init object holds a signal as bounded', () => {
    const synthetic = "const r = await fetch(url, { method: 'GET', signal: AbortSignal.timeout(5000) });\\n";
    expect(unbounded(synthetic)).toEqual([]);
  });

  it('control KS-1240 C4 the extractor reads a synthetic call with no signal as unbounded', () => {
    const synthetic = "const r = await fetch('http://x', { method: 'POST', body: JSON.stringify({ a: (1) }) });\\n";
    expect(unbounded(synthetic)).toEqual(["fetch('http://x', { method: 'POST', body: JSON.stringify({ a: (1) }) })"]);
  });
});
'''
S=dict(_m.S)
S.update(dict(dir='ks_1240_p3_batch_audit',
 title='api-gateway: the upstream fetches in routes/batch.ts (1) and routes/audit-export.ts (1) carry no timeout; add AbortSignal.timeout to each (RUNG 3, code_patch2: TWO product files, 4 hunks + one NEW source-text vitest)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 3 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Third slice of KS-1240 (middleware/auth.ts is `ks_1240_p1`; routes/proxy.ts + routes/admin.ts is `ks_1240_p2_proxy_admin`). The 30 s bound is the drafter's value; the raise seat confirms it with the owner. tokenisation.ts is still left out on purpose (its catch degrades to an empty map, so a timeout there changes what PII reaches storage). The Spark may fail this one (capability data).",
 products=[(P1,[B1,B2]),(P2,[A1,A2])],
 prodnote=['product 1 of 2, modified in place: TWO hunks - an added constant block, then one added `signal:` line in the fetch','product 2 of 2, modified in place: TWO hunks - an added constant block, then the fetch init object gains a `signal` property on its existing line'],
 tests=[dict(path=TP,content=T)],
 testnote=['NEW file, vitest, given in full below; 8 cells (source-text pins, balanced-parenthesis extractor)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1240-the-batch-and-audit-export-upstream-fetches-are-bounded.test.ts` from `Blockchain/Dev/services/api-gateway',
 pins='''# code_patch2: 2 products in services/api-gateway (batch.ts two hunks; audit-export.ts two hunks) + 1 NEW source-text vitest file; ref = ks689 (shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/api-gateway/src/__tests__/ks689-users-admin-create-auth-mount.test.ts
line=117
ctx=65536
''',
 wrong="`proxyRequest` in `routes/batch.ts` (`:132`, the fan-out fetch to originate and transfer) and the audit-log fetch in `routes/audit-export.ts` (`:172`, to the security service) pass no `signal`. An upstream that accepts the connection and never answers holds the caller's request open for as long as the socket lives. Each fetch sits inside a `try` whose `catch` already answers for an unreachable service (`batch.ts`: `{ ok: false, error }` for that item; `audit-export.ts`: the constant 502 BAD_GATEWAY). The change adds, per file, a module constant for the bound and a `signal: AbortSignal.timeout(<constant>)` in the one fetch. When the signal fires the fetch rejects and the existing catch answers as it does for an unreachable service. Nothing else changes for a healthy upstream.",
 where="- `routes/batch.ts:117` - **must change** (insertion): after `const TRANSFER_SERVICE_URL = process.env.TRANSFER_SERVICE_URL || 'http://localhost:4004';` a blank line, two comment lines and `const UPSTREAM_BATCH_FETCH_TIMEOUT_MS = 30_000;` (hunk 1 of batch.ts).\n- `routes/batch.ts:132` - **must change** (insertion): one added line `      signal: AbortSignal.timeout(UPSTREAM_BATCH_FETCH_TIMEOUT_MS),` right after the line `    const response = await fetch(`${baseUrl}${path}`, {` (hunk 2). Line numbers are at the tip before the constant block is added.\n- `routes/audit-export.ts:71` - **must change** (insertion): after `const SECURITY_SERVICE_URL = ...;` a blank line, two comment lines and `const UPSTREAM_AUDIT_FETCH_TIMEOUT_MS = 30_000;` (hunk 1 of audit-export.ts).\n- `routes/audit-export.ts:175` - **must change**: the line `        { method: 'GET', headers },` becomes `        { method: 'GET', headers, signal: AbortSignal.timeout(UPSTREAM_AUDIT_FETCH_TIMEOUT_MS) },` (hunk 2).\n- Every `catch` block and every other line of both files are NOT touched.",
 exactnote="Four hunks (two in batch.ts, two in audit-export.ts): three pure insertions with context and one single-line replacement.\n",
 donot="**Do NOT touch** any other line of `batch.ts` or `audit-export.ts`, the `catch` blocks, `proxy.ts`, `admin.ts`, `middleware/auth.ts`, `services/tokenisation.ts`, or any other file.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Pure ASCII, vitest imports, no top-level await. It reads `routes/batch.ts` and `routes/audit-export.ts` with `readFileSync` (the technique of ks689).",
 red=['RED KS-1240 R1','RED KS-1240 R2','RED KS-1240 R3','RED KS-1240 R4'],
 cells="- RED `R1`, `R2`: at the tip the one fetch call in each file carries no `AbortSignal.timeout`, so `unbounded(...)` returns its first line and `toEqual([])` fails; after the edit both lists are empty.\n- RED `R3`, `R4`: at the tip the constants do not exist, so `constantMs` is NaN and `toBeGreaterThan(0)` fails; after the edit both read 30000.\n- CONTROL `C1` to `C4`: green at the tip AND after (one fetch call per file; the extractor reads a call holding a signal as bounded and a synthetic unsignalled call as unbounded).",
 premises="- The two unbounded fetches are `batch.ts:132` (`await fetch(`${baseUrl}${path}`, {`) and `audit-export.ts:172-175` (`await fetch(` with the URL on `:174` and the init object `{ method: 'GET', headers },` on `:175`); no other `fetch(` occurs in either file.\n- `proxyRequest`'s catch returns `{ ok: false, error: err.message || 'Service request failed' }`; the audit-export catch answers the constant 502 BAD_GATEWAY (read at the tip).\n- `ks689-users-admin-create-auth-mount.test.ts` reads `routes/proxy.ts` with `readFileSync` from `__dirname/..`, so the same read works here.\n- The service's test runner is vitest. The golden is generated by script, not typed.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- Whether 30 s is the right bound for a bulk audit export: not established (the drafter's value; the raise seat confirms with the owner).\n- The cells are source-text pins; no request is sent, so the catch answers on expiry are read from the existing catch blocks, not driven.\n- Open PRs touching these files: none by the file lists of every open PR read on 2026-10-28.",
 scope="**Closes the batch.ts and audit-export.ts fetch slice of KS-1240.** `services/tokenisation.ts` and the health fetches stay open. Link the PR as Refs KS-1240, never a close-word.",
))
