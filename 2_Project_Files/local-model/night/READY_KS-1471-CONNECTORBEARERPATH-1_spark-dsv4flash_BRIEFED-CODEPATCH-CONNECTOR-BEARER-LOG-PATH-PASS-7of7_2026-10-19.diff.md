# READY — KS-1471-CONNECTORBEARERPATH-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1471_p1/out.md.checker/patch.diff`** (from `ls` at 09:58 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1471_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1471_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1471_p1-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in auth.ts (run 6 vs golden 7 body lines — context, since the change lines are equal) (identical in ks1471-connector-bearer-refusal-logs-the-full-path.test.ts); hunk headers identical; APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 09:58 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1471_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `78cb3c3939e319332e387ffecb075a169edd4a39`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/middleware/auth.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1471-connector-bearer-refusal-logs-the-full-path.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1471-connector-bearer-refusal-logs-the-full-path.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/api-gateway/src/middleware/auth.ts
100	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1471-connector-bearer-refusal-logs-the-full-path.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/middleware/auth.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1471-connector-bearer-refusal-logs-the-full-path.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1471-connector-bearer-refusal-logs-the-full-path.test.ts fails at the untouched tip (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1471 - the refused-connector-Bearer warning names the full path, mount prefix included RED KS-1471 L1: a refusal inside a router mounted at /api/credentials logs the path /api/credentials/abc', 'KS-1471 - the refused-connector-Bearer warning names the full path, mount prefix included RED KS-1471 L2: the logged path carries no query string, so a token in the query never reaches the log']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1471-connector-bearer-refusal-logs-the-full-path.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1106 failed=0 | after: total=1111 failed=0` · `NEW reds: []` [baseline_suite.json total=1106 failed=0; after_suite.json total=1111 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +101/-1 test=src/__tests__/ks1471-connector-bearer-refusal-logs-the-full-path.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1471-connector-bearer-refusal-logs-the-full-path.test.ts` (+100/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `78cb3c3939e319332e387ffecb075a169edd4a39` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1471_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1471_p1/KS-1471.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1471_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/middleware/auth.ts b/Blockchain/Dev/services/api-gateway/src/middleware/auth.ts
--- a/Blockchain/Dev/services/api-gateway/src/middleware/auth.ts
+++ b/Blockchain/Dev/services/api-gateway/src/middleware/auth.ts
@@ -274,3 +274,3 @@ function refuseConnectorBearer(req: Request, res: Response, decoded: Pick<UserPa
     method: req.method,
-    path: req.path,
+    path: req.baseUrl + req.path,
     requestId: req.requestId,
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1471-connector-bearer-refusal-logs-the-full-path.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1471-connector-bearer-refusal-logs-the-full-path.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1471-connector-bearer-refusal-logs-the-full-path.test.ts
@@ -0,0 +1,100 @@
+/**
+ * KS-1471 - the CONNECTOR_JWT_AS_BEARER_REFUSED warning logged `req.path`, which inside a mounted router is the
+ * mount-relative remainder: a refused `GET /api/credentials/abc` logged "/abc". The warning exists to show WHICH
+ * call presented a connector Bearer, and the mount prefix is what says which route it was. It now logs
+ * `req.baseUrl + req.path` (the full path, no query string: `req.originalUrl` would carry a query token).
+ * Real `authenticateToken` on a bare express app, one router mounted under /api/credentials and one route at the root.
+ */
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import express from 'express';
+import http from 'http';
+import jwt from 'jsonwebtoken';
+import type { AddressInfo } from 'node:net';
+import { configureAuth, authenticateToken } from '../middleware/auth';
+import { logger } from '../utils/logger';
+
+const PRIV = process.env.__TEST_JWT_PRIVATE_PEM || '';
+const realFetch = globalThis.fetch;
+let baseUrl = '';
+let server: http.Server;
+const warns: unknown[][] = [];
+
+function sign(claims: Record<string, unknown>): string {
+  return jwt.sign(
+    { userId: 'u-ks1471', email: 'u@ks1471.test', role: 'ISSUER', tenantId: 't-ks1471', verificationLevel: 'BASIC', ...claims },
+    PRIV,
+    { algorithm: 'RS256', expiresIn: '10m' },
+  );
+}
+const connectorJwt = () =>
+  sign({ userId: 'connector:ks1471-conn', email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector', scopes: ['documents:write'], organizationId: 'org-ks1471' });
+
+async function call(path: string, bearer: string): Promise<{ status: number; body: any }> {
+  const r = await realFetch(baseUrl + path, { headers: { authorization: 'Bearer ' + bearer } });
+  return { status: r.status, body: await r.json().catch(() => ({})) };
+}
+
+/** The structured metadata of every refusal warning logged since `warns` was last cleared. */
+const refusals = (): Array<Record<string, unknown>> =>
+  warns.map((w) => w[1] as Record<string, unknown>).filter((m) => m && m.event === 'CONNECTOR_JWT_AS_BEARER_REFUSED');
+
+beforeAll(async () => {
+  expect(PRIV.length, 'vitest.setup.ts provisioned a throwaway RS256 private key').toBeGreaterThan(100);
+  delete process.env.JWT_JWKS_URL;
+  configureAuth({ securityServiceUrl: 'http://127.0.0.1:9', authServiceUrl: 'http://127.0.0.1:9' });
+  vi.spyOn(console, 'error').mockImplementation(() => undefined);
+  vi.spyOn(console, 'warn').mockImplementation(() => undefined);
+  vi.spyOn(logger, 'warn').mockImplementation(((...a: unknown[]) => { warns.push(a); return logger; }) as never);
+  const app = express();
+  const router = express.Router();
+  router.use(authenticateToken(true));
+  router.get('/:id', (_req, res) => { res.status(200).json({ ok: true }); });
+  app.use('/api/credentials', router);
+  app.get('/required', authenticateToken(true), (_req, res) => { res.status(200).json({ ok: true }); });
+  server = app.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => server.once('listening', () => r()));
+  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+afterAll(async () => {
+  globalThis.fetch = realFetch;
+  vi.restoreAllMocks();
+  await new Promise<void>((r) => server.close(() => r()));
+});
+
+describe('KS-1471 - the refused-connector-Bearer warning names the full path, mount prefix included', () => {
+  it('RED KS-1471 L1: a refusal inside a router mounted at /api/credentials logs the path /api/credentials/abc', async () => {
+    warns.length = 0;
+    const r = await call('/api/credentials/abc', connectorJwt());
+    expect(r.status).toBe(401);
+    expect(refusals().map((m) => m.path)).toEqual(['/api/credentials/abc']);
+  });
+
+  it('RED KS-1471 L2: the logged path carries no query string, so a token in the query never reaches the log', async () => {
+    warns.length = 0;
+    await call('/api/credentials/abc?access_token=ks1471-query-secret', connectorJwt());
+    expect(refusals().map((m) => m.path)).toEqual(['/api/credentials/abc']);
+    expect(JSON.stringify(warns)).not.toContain('ks1471-query-secret');
+  });
+
+  it('CONTROL KS-1471 L3: a refusal on a route mounted at the root still logs its own path', async () => {
+    warns.length = 0;
+    const r = await call('/required', connectorJwt());
+    expect(r.status).toBe(401);
+    expect(refusals().map((m) => m.path)).toEqual(['/required']);
+  });
+
+  it('CONTROL KS-1471 L4: the refusal is still a 401 UNAUTHORIZED that names x-api-key, and logs the connector id', async () => {
+    warns.length = 0;
+    const r = await call('/api/credentials/abc', connectorJwt());
+    expect([r.status, r.body?.error?.code]).toEqual([401, 'UNAUTHORIZED']);
+    expect(String(r.body?.error?.message)).toContain('x-api-key');
+    expect(refusals().map((m) => m.connector)).toEqual(['connector:ks1471-conn']);
+  });
+
+  it('CONTROL KS-1471 L5: an ordinary human Bearer passes the router mount and logs no refusal', async () => {
+    warns.length = 0;
+    const r = await call('/api/credentials/abc', sign({}));
+    expect(r.status).toBe(200);
+    expect(refusals()).toHaveLength(0);
+  });
+});
```
