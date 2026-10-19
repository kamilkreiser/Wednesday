# READY — KS-1506-AUDITEXPORTAUTH-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1506_p1/out.md.checker/patch.diff`** (from `ls` at 14:04 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1506_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1506_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 14:04 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1506_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `37834600a543cb0276f427d969ac034d9df74fbd`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/index.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1506-audit-export-requires-authentication.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/index.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1506-audit-export-requires-authentication.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	2	Blockchain/Dev/services/api-gateway/src/index.ts
138	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1506-audit-export-requires-authentication.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/index.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1506-audit-export-requires-authentication.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1506-audit-export-requires-authentication.test.ts fails at the untouched tip (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1506 - the platform audit export runs behind authenticateToken RED KS-1506 A1: a platform admin gets the export as JSON, and the security service is asked with the admin Authorization', 'KS-1506 - the platform audit export runs behind authenticateToken RED KS-1506 A2: a platform admin gets the export as CSV with the entry row', 'KS-1506 - the platform audit export runs behind authenticateToken RED KS-1506 A3: an authenticated caller who is not an admin is answered 403 FORBIDDEN, not 401']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1506-audit-export-requires-authentication.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1117 failed=0 | after: total=1122 failed=0` · `NEW reds: []` [baseline_suite.json total=1117 failed=0; after_suite.json total=1122 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +140/-2 test=src/__tests__/ks1506-audit-export-requires-authentication.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/index.ts` (+2/-2 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1506-audit-export-requires-authentication.test.ts` (+138/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `37834600a543cb0276f427d969ac034d9df74fbd` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1506_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1506_p1/KS-1506.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1506_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/index.ts b/Blockchain/Dev/services/api-gateway/src/index.ts
index 4817a72ac..94d34512e 100644
--- a/Blockchain/Dev/services/api-gateway/src/index.ts
+++ b/Blockchain/Dev/services/api-gateway/src/index.ts
@@ -810,4 +810,4 @@ app.use('/api/batch', batchRouter);
 app.use('/api/notifications', notificationsRouter);
-app.use('/api/admin/audit', auditExportRouter);
-
+app.use('/api/admin/audit', authenticateToken(true), auditExportRouter);
+
 app.get(['/api', '/api/v1'], (_req: Request, res: Response) => {
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1506-audit-export-requires-authentication.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1506-audit-export-requires-authentication.test.ts
new file mode 100644
index 000000000..365ff7623
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1506-audit-export-requires-authentication.test.ts
@@ -0,0 +1,138 @@
+/**
+ * KS-1506 - the platform audit export (GET /api/admin/audit/export) is mounted WITHOUT authenticateToken, and its
+ * handler reads `req.user`, which only that middleware sets. So the route answered 401 to every caller, an admin
+ * included, and KS-745's goal (an exportable audit trail) was unreachable. The mount now runs authenticateToken(true)
+ * first. Measured on the real gateway app over HTTP against one stub upstream: the export's own fetch of the security
+ * service's /api/audit is answered by the stub, and the stub records the Authorization header it was sent.
+ */
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import http from 'http';
+import jwt from 'jsonwebtoken';
+import type { AddressInfo } from 'node:net';
+
+// The real app boots over HTTP below. Its DB is a stub: the audit middleware reads it, and it is not under test here.
+vi.mock('../db', async (orig) => {
+  const real = (await orig()) as Record<string, unknown>;
+  return { ...real, isDbAvailable: () => true, query: async () => ({ rows: [], rowCount: 0 }) };
+});
+
+const PRIV = process.env.__TEST_JWT_PRIVATE_PEM as string;
+const TENANT = 'a0000000-0000-4000-8000-000000001506';
+const SERVICES = ['ANALYTICS', 'ANCHORING', 'AUTH', 'BILLING', 'GOVERNANCE', 'KYC', 'NFT', 'NOTIFICATION', 'ORIGINATE', 'PRISM',
+  'REFERRAL', 'SECURITY', 'STAKING', 'TIMESTAMPING', 'TRANSFER', 'VC_ISSUER', 'WALLET'];
+
+type Hit = { url: string; authorization: string | null };
+const hits: Hit[] = [];
+const ENTRY = { id: 'ks1506-entry-1', timestamp: '2026-10-01T00:00:00.000Z', type: 'admin', action: 'ks1506.test', userId: 'u-admin', outcome: 'success' };
+
+function sign(claims: Record<string, unknown>): string {
+  return jwt.sign(
+    { userId: 'u-ks1506', email: 'u@ks1506.test', role: 'ISSUER', tenantId: TENANT, verificationLevel: 'BASIC', ...claims },
+    PRIV,
+    { algorithm: 'RS256', expiresIn: '10m' },
+  );
+}
+const adminBearer = (): string => 'Bearer ' + sign({ role: 'SUPER_ADMIN' });
+const issuerBearer = (): string => 'Bearer ' + sign({ role: 'ISSUER' });
+const connectorBearer = (): string =>
+  'Bearer ' + sign({ userId: 'connector:ks1506', email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector', scopes: ['documents:read'] });
+
+async function listen(server: http.Server): Promise<string> {
+  await new Promise<void>((r) => server.listen(0, '127.0.0.1', () => r()));
+  return `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
+}
+async function closeServer(server: http.Server | undefined): Promise<void> {
+  if (!server) return;
+  server.closeAllConnections();
+  await new Promise<void>((r) => server.close(() => r()));
+}
+
+/** One upstream for every service: it answers the export's audit fetch and records everything else. */
+function createUpstream(): http.Server {
+  return http.createServer((req, res) => {
+    const json = (status: number, payload: unknown) => { res.writeHead(status, { 'content-type': 'application/json' }); res.end(JSON.stringify(payload)); };
+    const url = req.url || '';
+    if (url.startsWith('/.well-known/')) return json(404, {});
+    hits.push({ url, authorization: (req.headers.authorization as string | undefined) ?? null });
+    if (url.startsWith('/api/audit?')) return json(200, { success: true, data: { logs: [ENTRY], total: 1, limit: 50, offset: 0 } });
+    return json(200, { success: true, data: { recorder: true } });
+  });
+}
+
+type Res = { status: number; contentType: string; text: string; json: any };
+function get(base: string, path: string, headers: Record<string, string> = {}): Promise<Res> {
+  return new Promise((resolveGet, reject) => {
+    const target = new URL(base);
+    const req = http.request({ hostname: target.hostname, port: target.port, path, method: 'GET', agent: false, headers }, (res) => {
+      const c: Buffer[] = [];
+      res.on('data', (d: Buffer) => c.push(d));
+      res.on('end', () => {
+        const text = Buffer.concat(c).toString();
+        let json: any = null;
+        try { json = JSON.parse(text); } catch { /* non-JSON body */ }
+        resolveGet({ status: res.statusCode ?? 0, contentType: String(res.headers['content-type'] ?? ''), text, json });
+      });
+    });
+    req.setTimeout(20000, () => req.destroy(new Error(`no response from GET ${path} within 20 s`)));
+    req.on('error', reject);
+    req.end();
+  });
+}
+
+const EXPORT = '/api/admin/audit/export?from=2026-10-01&to=2026-10-02&type=all';
+let upstream: http.Server | undefined;
+let gateway: http.Server | undefined;
+let base = '';
+
+beforeAll(async () => {
+  expect(PRIV, 'vitest.setup.ts provisioned a throwaway RS256 private key').toBeTruthy();
+  upstream = createUpstream();
+  const upstreamUrl = await listen(upstream);
+  vi.stubEnv('NODE_ENV', 'test');
+  for (const name of SERVICES) vi.stubEnv(`${name}_SERVICE_URL`, upstreamUrl);
+  vi.stubEnv('TENANT_PROVISIONING_URL', upstreamUrl);
+  vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
+  delete process.env.JWT_JWKS_URL;
+  vi.resetModules();
+  vi.spyOn(console, 'warn').mockImplementation(() => undefined);
+  vi.spyOn(console, 'error').mockImplementation(() => undefined);
+  const app = (await import('../index')).default;
+  gateway = http.createServer(app as http.RequestListener);
+  base = await listen(gateway);
+}, 60000);
+afterAll(async () => { await closeServer(gateway); await closeServer(upstream); vi.restoreAllMocks(); vi.unstubAllEnvs(); });
+
+describe('KS-1506 - the platform audit export runs behind authenticateToken', () => {
+  it('RED KS-1506 A1: a platform admin gets the export as JSON, and the security service is asked with the admin Authorization', async () => {
+    hits.length = 0;
+    const bearer = adminBearer();
+    const r = await get(base, EXPORT, { authorization: bearer });
+    expect([r.status, r.json?.success, r.json?.meta?.totalEntries, r.json?.data?.[0]?.id]).toEqual([200, true, 1, 'ks1506-entry-1']);
+    expect(hits.filter((h) => h.url.startsWith('/api/audit?')).map((h) => h.authorization)).toEqual([bearer]);
+  });
+
+  it('RED KS-1506 A2: a platform admin gets the export as CSV with the entry row', async () => {
+    const r = await get(base, EXPORT + '&format=csv', { authorization: adminBearer() });
+    expect([r.status, r.contentType.startsWith('text/csv')]).toEqual([200, true]);
+    expect(r.text.split('\n')[1]).toContain('ks1506-entry-1');
+  });
+
+  it('RED KS-1506 A3: an authenticated caller who is not an admin is answered 403 FORBIDDEN, not 401', async () => {
+    const r = await get(base, EXPORT, { authorization: issuerBearer() });
+    expect([r.status, r.json?.error?.code]).toEqual([403, 'FORBIDDEN']);
+  });
+
+  it('CONTROL KS-1506 A4: an anonymous caller is answered 401 UNAUTHORIZED and the security service is never asked', async () => {
+    hits.length = 0;
+    const r = await get(base, EXPORT);
+    expect([r.status, r.json?.error?.code]).toEqual([401, 'UNAUTHORIZED']);
+    expect(hits.filter((h) => h.url.startsWith('/api/audit?'))).toHaveLength(0);
+  });
+
+  it('CONTROL KS-1506 A5: a connector JWT presented as a Bearer is refused 401 and the security service is never asked', async () => {
+    hits.length = 0;
+    const r = await get(base, EXPORT, { authorization: connectorBearer() });
+    expect(r.status).toBe(401);
+    expect(hits.filter((h) => h.url.startsWith('/api/audit?'))).toHaveLength(0);
+  });
+});
```
