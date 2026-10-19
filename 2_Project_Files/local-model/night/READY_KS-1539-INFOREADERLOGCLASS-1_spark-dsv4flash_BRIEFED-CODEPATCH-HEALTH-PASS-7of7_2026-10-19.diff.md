# READY — KS-1539-INFOREADERLOGCLASS-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1539_p1/out.md.checker/patch.diff`** (from `ls` at 14:04 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1539_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1539_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 14:04 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1539_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `37834600a543cb0276f427d969ac034d9df74fbd`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/services/health.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1539-info-reader-logs-a-thrown-allow-list-read.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/services/health.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1539-info-reader-logs-a-thrown-allow-list-read.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
5	1	Blockchain/Dev/services/api-gateway/src/services/health.ts
102	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1539-info-reader-logs-a-thrown-allow-list-read.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (5 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 5 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/services/health.ts byte-exact incl. leading whitespace (apply mode strict): OK 5 line(s) byte-exact incl. leading whitespace (of 5; 5 line(s) added by the apply)` [a3i_indent.out: `OK 5 line(s) byte-exact incl. leading whitespace (of 5; 5 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/services/health.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1539-info-reader-logs-a-thrown-allow-list-read.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1539-info-reader-logs-a-thrown-allow-list-read.test.ts fails at the untouched tip (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1539 - a thrown allow-list read on GET /api/connector/info leaves a server-side trace RED KS-1539 L1: a rejected Error logs ONE warn that names the route and the class Error', 'KS-1539 - a thrown allow-list read on GET /api/connector/info leaves a server-side trace RED KS-1539 L2: a rejected SyntaxError logs the class SyntaxError and none of the stored text its message quotes', 'KS-1539 - a thrown allow-list read on GET /api/connector/info leaves a server-side trace RED KS-1539 L3: a rejected string and a synchronous throw each log one warn, the class being the typeof or the Error class']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1539-info-reader-logs-a-thrown-allow-list-read.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1117 failed=0 | after: total=1122 failed=0` · `NEW reds: []` [baseline_suite.json total=1117 failed=0; after_suite.json total=1122 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +107/-1 test=src/__tests__/ks1539-info-reader-logs-a-thrown-allow-list-read.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/services/health.ts` (+5/-1 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1539-info-reader-logs-a-thrown-allow-list-read.test.ts` (+102/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `37834600a543cb0276f427d969ac034d9df74fbd` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1539_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1539_p1/KS-1539.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1539_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/services/health.ts b/Blockchain/Dev/services/api-gateway/src/services/health.ts
index 48aaf4dd3..8cbc352a8 100644
--- a/Blockchain/Dev/services/api-gateway/src/services/health.ts
+++ b/Blockchain/Dev/services/api-gateway/src/services/health.ts
@@ -14,2 +14,3 @@ import { authenticateToken } from '../middleware/auth';
 import { query } from '../db';
+import { logger } from '../utils/logger';
 import { getStartupMigrations } from './startupMigrationStatus';
@@ -76,3 +77,3 @@ export function createHealthRoutes(
       }
-    } catch {
+    } catch (err) {
       // KS-1532: a THROWN read refuses, as the create path does (routes/verification.ts, KS-1256): the same
@@ -80,2 +81,5 @@ export function createHealthRoutes(
       // allowedDocumentTypes [] - "all types permitted" - at the moment the allow-list could not be read.
+      // KS-1539: leave a server-side trace of WHICH fault this was. The error's CLASS only: a JSON.parse SyntaxError's message
+      // quotes the stored bytes, and the stored bytes are the allow-list itself.
+      logger.warn('Connector allow-list settings read threw; answering 503 (GET /api/connector/info)', { route: 'GET /api/connector/info', errorClass: err instanceof Error ? err.constructor.name : typeof err });
       res.status(503).json({ success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Connector allow-list configuration could not be read; refusing until it can be read' } });
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1539-info-reader-logs-a-thrown-allow-list-read.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1539-info-reader-logs-a-thrown-allow-list-read.test.ts
new file mode 100644
index 000000000..d8c83fb02
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1539-info-reader-logs-a-thrown-allow-list-read.test.ts
@@ -0,0 +1,102 @@
+/**
+ * KS-1539 (the info-reader half) - GET /api/connector/info answers 503 when the platform-settings read THROWS
+ * (KS-1532) but logged nothing, so an operator who sees connector 503s has no server-side line saying which fault
+ * it was (the Redis client's MaxRetriesPerRequestError, or the SyntaxError from JSON.parse on malformed stored bytes).
+ * The catch now logs ONE warn naming the route and the error's CLASS. It deliberately does not log the error's
+ * message: a JSON.parse SyntaxError quotes the stored bytes, and the stored bytes are the allow-list itself.
+ * The 503 answer is unchanged. Harness: the ks1532 pattern - the real createHealthRoutes behind the real
+ * authenticateToken(true), one settings read the cell controls, `logger.warn` spied.
+ */
+import { describe, it, expect, beforeAll, afterAll, afterEach, vi } from 'vitest';
+import type { Request, Router } from 'express';
+import { apiKeyCache, connectorBearerCache } from '../middleware/auth';
+import { logger } from '../utils/logger';
+
+const CONNECTOR_ID = 'ks1539-c1';
+const META = { connectorId: CONNECTOR_ID, scopes: ['documents:write'], organizationId: 'org-1', tenantId: 'ten-1', rateLimit: 100, rateLimitWindow: 60 };
+const QUOTED = 'ks1539-quoted-allow-list-type';
+
+type ReadMode = 'ok' | 'rejects-error' | 'rejects-syntax' | 'rejects-string' | 'throws-sync';
+let readMode: ReadMode = 'ok';
+function readSettings(): Promise<unknown> {
+  switch (readMode) {
+    case 'ok': return Promise.resolve({ integrations: [{ id: CONNECTOR_ID, config: { allowedDocumentTypes: ['SSD_DOCUMENT'] } }] });
+    case 'rejects-error': return Promise.reject(new Error('redis down'));
+    case 'rejects-syntax': return Promise.reject(new SyntaxError(`Unexpected token 'x', ..."[x-${QUOTED}]"... is not valid JSON`));
+    case 'rejects-string': return Promise.reject('redis down');
+    case 'throws-sync': throw new Error('redis client is closed');
+  }
+}
+
+let infoRouter: Router;
+const warns: unknown[][] = [];
+function makeReq(): Request {
+  return {
+    headers: { 'x-api-key': 'sk_ks1539' }, method: 'GET', url: '/api/connector/info',
+    get: function (name: string) { return (this as any).headers[name?.toLowerCase()]; },
+  } as unknown as Request;
+}
+async function info(): Promise<{ status: number; body: any; calls: number }> {
+  const req = makeReq();
+  const res: any = { _status: 0, status(code: number) { res._status = code; return res; }, json(body: unknown) { return body; }, setHeader() { return res; } };
+  let calls = 0;
+  const body = await new Promise<any>((resolve) => {
+    res.json = (b: unknown) => { calls += 1; resolve(b); return res; };
+    infoRouter(req, res, () => resolve({ fellThrough: true }));
+  });
+  return { status: res._status || 200, body, calls };
+}
+/** The structured metadata of every warn that names the info route. */
+const infoWarns = (): Array<Record<string, unknown>> =>
+  warns.filter((w) => JSON.stringify(w).includes('/api/connector/info')).map((w) => w[1] as Record<string, unknown>);
+
+beforeAll(async () => {
+  apiKeyCache.set('sk_ks1539', { result: META, expiresAt: Date.now() + 60000 });
+  connectorBearerCache.set('sk_ks1539', { token: 'connector.jwt.token', expiresAt: Date.now() + 60000 });
+  vi.spyOn(logger, 'warn').mockImplementation(((...a: unknown[]) => { warns.push(a); return logger; }) as never);
+  const { createHealthRoutes } = await import('../services/health');
+  infoRouter = createHealthRoutes({}, { getNotificationSettings: () => readSettings(), getRedisClient: () => null } as any);
+});
+afterEach(() => { warns.length = 0; readMode = 'ok'; });
+afterAll(() => { vi.restoreAllMocks(); });
+
+describe('KS-1539 - a thrown allow-list read on GET /api/connector/info leaves a server-side trace', () => {
+  it('RED KS-1539 L1: a rejected Error logs ONE warn that names the route and the class Error', async () => {
+    readMode = 'rejects-error';
+    const r = await info();
+    expect(r.status).toBe(503);
+    expect(infoWarns().map((m) => [m.route, m.errorClass])).toEqual([['GET /api/connector/info', 'Error']]);
+  });
+
+  it('RED KS-1539 L2: a rejected SyntaxError logs the class SyntaxError and none of the stored text its message quotes', async () => {
+    readMode = 'rejects-syntax';
+    await info();
+    expect(infoWarns().map((m) => m.errorClass)).toEqual(['SyntaxError']);
+    expect(JSON.stringify(warns)).not.toContain(QUOTED);
+  });
+
+  it('RED KS-1539 L3: a rejected string and a synchronous throw each log one warn, the class being the typeof or the Error class', async () => {
+    readMode = 'rejects-string';
+    await info();
+    const afterString = infoWarns().map((m) => m.errorClass);
+    warns.length = 0;
+    readMode = 'throws-sync';
+    await info();
+    expect([afterString, infoWarns().map((m) => m.errorClass)]).toEqual([['string'], ['Error']]);
+  });
+
+  it('CONTROL KS-1539 L4: a healthy read answers 200 and logs nothing', async () => {
+    readMode = 'ok';
+    const r = await info();
+    expect([r.status, r.body?.allowedDocumentTypes]).toEqual([200, ['SSD_DOCUMENT']]);
+    expect(infoWarns()).toHaveLength(0);
+  });
+
+  it('CONTROL KS-1539 L5: the 503 answer for a thrown read is unchanged - same status, code and text, sent once', async () => {
+    readMode = 'rejects-error';
+    const r = await info();
+    expect([r.status, r.body?.error?.code, r.body?.error?.message, r.calls]).toEqual([
+      503, 'SERVICE_UNAVAILABLE', 'Connector allow-list configuration could not be read; refusing until it can be read', 1,
+    ]);
+  });
+});
```
