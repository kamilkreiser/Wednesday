# READY — KS-1540-INFOREDIS503-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1540_p1/out.md.checker/patch.diff`** (from `ls` at 03:01 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1540_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1540_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1540_p1-control-r2/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in health.ts (run 14 vs golden 17 body lines — context, since the change lines are equal) (identical in ks1540-info-reader-refuses-when-redis-is-unavailable.test.ts); hunk headers identical; APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 03:01 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1540_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `385fc288fae831f2ca15b9d091c844f33285b784`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/services/health.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1540-info-reader-refuses-when-redis-is-unavailable.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/services/health.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1540-info-reader-refuses-when-redis-is-unavailable.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
10	0	Blockchain/Dev/services/api-gateway/src/services/health.ts
93	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1540-info-reader-refuses-when-redis-is-unavailable.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (10 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 10 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/services/health.ts byte-exact incl. leading whitespace (apply mode strict): OK 10 line(s) byte-exact incl. leading whitespace (of 10; 10 line(s) added by the apply)` [a3i_indent.out: `OK 10 line(s) byte-exact incl. leading whitespace (of 10; 10 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/services/health.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1540-info-reader-refuses-when-redis-is-unavailable.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1540-info-reader-refuses-when-redis-is-unavailable.test.ts fails at the untouched tip (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ["KS-1540 - GET /api/connector/info refuses when Redis is unavailable RED KS-1540: Redis unavailable and a read that resolves null answers 503 SERVICE_UNAVAILABLE ONCE with the create path's text, never 200 and never []", 'KS-1540 - GET /api/connector/info refuses when Redis is unavailable RED KS-1540: the refusal comes BEFORE the settings read, which is never made']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1540-info-reader-refuses-when-redis-is-unavailable.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1175 failed=0 | after: total=1180 failed=0` · `NEW reds: []` [baseline_suite.json total=1175 failed=0; after_suite.json total=1180 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +103/-0 test=src/__tests__/ks1540-info-reader-refuses-when-redis-is-unavailable.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/services/health.ts` (+10/-0 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1540-info-reader-refuses-when-redis-is-unavailable.test.ts` (+93/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `385fc288fae831f2ca15b9d091c844f33285b784` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1540_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1540_p1/KS-1540.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1540_p1/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/services/health.ts
+++ b/Blockchain/Dev/services/api-gateway/src/services/health.ts
@@ -21,2 +21,4 @@ interface RedisServiceLike {
   getRedisClient(): import('ioredis').default | null;
+  // KS-1540: optional so that a double without it keeps working; only an explicit `false` refuses.
+  isRedisAvailable?(): boolean;
 }
@@ -46,2 +48,10 @@ export function createHealthRoutes(
     let connectorConfig: Record<string, unknown> = {};
+    // KS-1540: in the Redis in-memory fallback mode the settings read RESOLVES to null instead of throwing, which
+    // used to answer allowedDocumentTypes [] - "all types permitted" - for a connector whose allow-list could not be
+    // read. The create path refuses with this 503 before its read (routes/verification.ts, KS-1256): the same status,
+    // code and text here. Only an explicit false refuses; a service object without the method is read as before.
+    if (redisService.isRedisAvailable?.() === false) {
+      res.status(503).json({ success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Connector allow-list configuration is currently unreadable; refusing until it can be read' } });
+      return;
+    }
     // KS-1231 (#1035 gate N-1): the stored container is read FAIL CLOSED for the calling connector,
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1540-info-reader-refuses-when-redis-is-unavailable.test.ts
@@ -0,0 +1,93 @@
+// =============================================================================
+// KS-1540 - GET /api/connector/info answers 503 when Redis is unavailable, as the create path does
+// =============================================================================
+//
+// In the Redis in-memory fallback mode the platform-settings read RESOLVES to null instead of throwing, so the info
+// reader answered 200 with allowedDocumentTypes [] ("all types permitted") for a connector whose allow-list it could not
+// read. The create path (routes/verification.ts, KS-1256) refuses with 503 SERVICE_UNAVAILABLE 'Connector allow-list
+// configuration is currently unreadable; refusing until it can be read' through an explicit isRedisAvailable() test
+// BEFORE its read. The info reader now does the same when the service object reports Redis unavailable.
+//
+// Harness: the ks1532 pattern, the real createHealthRoutes behind the real authenticateToken(true) with the sk_ key
+// pre-seeded in the gateway's caches.
+// =============================================================================
+
+import { describe, it, expect, beforeAll } from 'vitest';
+import type { Request, Response, Router } from 'express';
+import { apiKeyCache, connectorBearerCache } from '../middleware/auth';
+
+const CONNECTOR_ID = 'ks1540-c1';
+const META = { connectorId: CONNECTOR_ID, scopes: ['documents:write'], organizationId: 'org-1', tenantId: 'ten-1', rateLimit: 100, rateLimitWindow: 60 };
+const UNREADABLE = 'Connector allow-list configuration is currently unreadable; refusing until it can be read';
+
+let redisUp = true;
+let reads = 0;
+let stored: unknown = null;
+const readSettings = async (): Promise<unknown> => { reads += 1; return stored; };
+
+let infoRouter: Router;
+let olderInfoRouter: Router;
+
+function makeInfoReq(): Request {
+  return {
+    headers: { 'x-api-key': 'sk_ks1540' }, method: 'GET', url: '/api/connector/info',
+    get: function (name: string) { return (this as any).headers[name?.toLowerCase()]; },
+  } as unknown as Request;
+}
+function makeInfoRes(): Response & { _status: number } {
+  const res: any = { _status: 0, status(code: number) { res._status = code; return res; }, json(body: unknown) { return body; }, setHeader() { return res; } };
+  return res;
+}
+/** GET /api/connector/info through a router. `calls` counts res.json calls: a refusal that forgot its `return` would send a SECOND response. */
+async function info(router: Router): Promise<{ status: number; body: any; calls: number }> {
+  const req = makeInfoReq();
+  const res = makeInfoRes();
+  let calls = 0;
+  const body = await new Promise<any>((resolve) => {
+    res.json = (b: unknown) => { calls += 1; resolve(b); return res; };
+    router(req, res, () => resolve({ fellThrough: true }));
+  });
+  return { status: res._status || 200, body, calls };
+}
+
+beforeAll(async () => {
+  apiKeyCache.set('sk_ks1540', { result: META, expiresAt: Date.now() + 60000 });
+  connectorBearerCache.set('sk_ks1540', { token: 'connector.jwt.token', expiresAt: Date.now() + 60000 });
+  const { createHealthRoutes } = await import('../services/health');
+  infoRouter = createHealthRoutes({}, { getNotificationSettings: readSettings, getRedisClient: () => null, isRedisAvailable: () => redisUp } as any);
+  olderInfoRouter = createHealthRoutes({}, { getNotificationSettings: readSettings, getRedisClient: () => null } as any);
+});
+
+describe('KS-1540 - GET /api/connector/info refuses when Redis is unavailable', () => {
+  it('RED KS-1540: Redis unavailable and a read that resolves null answers 503 SERVICE_UNAVAILABLE ONCE with the create path\'s text, never 200 and never []', async () => {
+    redisUp = false; stored = null; reads = 0;
+    const r = await info(infoRouter);
+    expect([r.status, r.body?.error?.code, r.body?.error?.message, r.body?.allowedDocumentTypes, r.calls]).toEqual([503, 'SERVICE_UNAVAILABLE', UNREADABLE, undefined, 1]);
+  });
+
+  it('RED KS-1540: the refusal comes BEFORE the settings read, which is never made', async () => {
+    redisUp = false; stored = null; reads = 0;
+    await info(infoRouter);
+    expect(reads).toBe(0);
+  });
+
+  it('CONTROL KS-1540: Redis available and a read that resolves null (a genuinely empty store) still answers 200 with []', async () => {
+    redisUp = true; stored = null; reads = 0;
+    const r = await info(infoRouter);
+    expect([r.status, r.body?.allowedDocumentTypes, r.calls, reads]).toEqual([200, [], 1, 1]);
+  });
+
+  it('CONTROL KS-1540: Redis available and a stored list is answered byte for byte', async () => {
+    redisUp = true; stored = { integrations: [{ id: CONNECTOR_ID, config: { allowedDocumentTypes: ['SSD_DOCUMENT'] } }] };
+    const r = await info(infoRouter);
+    expect([r.status, JSON.stringify(r.body), r.calls]).toEqual([
+      200, '{"id":"ks1540-c1","name":"Connector ks1540-c1","scopes":["documents:write"],"allowedDocumentTypes":["SSD_DOCUMENT"],"workflowPolicy":"enforce","rateLimit":100}', 1,
+    ]);
+  });
+
+  it('CONTROL KS-1540: a service object WITHOUT isRedisAvailable is read as before (only an explicit false refuses)', async () => {
+    stored = null; reads = 0;
+    const r = await info(olderInfoRouter);
+    expect([r.status, r.body?.allowedDocumentTypes, r.calls, reads]).toEqual([200, [], 1, 1]);
+  });
+});
```
