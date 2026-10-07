# READY — KS-1410-BATCH-AUDITEXPORT-1 (Spark DeepSeek V4 Flash, briefed, code_patch2 multi-file) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1410-apigw-batch-audit-export-500/out.md.checker/patch.diff`**. BYTE-IDENTICAL to the drafter's golden `2_Project_Files/local-model/night/briefs/KS-1410-apigw-batch-audit-export-500/golden.diff` (`cmp -s` rc 0, Wednesday afternoon seat; cross-control vs the notifications golden rc 1).

**Held BY HAND 15:41 2026-10-07 by Wednesday afternoon seat** (`hold_ready.py` has no code_patch2 path yet: OWED). Clauses below COPIED from `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1410-apigw-batch-audit-export-500/checker.out`. Tip `147ae442074c7f3b5be9ce7ccc4452c8dae34b4f`. Round 1 of 2. Wednesday read the product hunks at source before queueing (information-leak surface): each of the four catch blocks (`batch.ts` certify/verify/delegate, `audit-export.ts` export) now calls a per-file `fail500` that logs the thrown text server-side and answers the constant `Internal server error` body (the KS-1334 / KS-730 originate precedent).

## Checker verdict lines (verbatim)
- PASS A1 output is exactly one fenced ```diff block, nothing outside it
- PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)
- PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/src/routes/batch.ts , Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks1410-batch-and-audit-export-500-never-answer-err-message.test.ts }
- PASS A3b every must_change site the brief names is changed by a product section (3 site(s), 2 product file(s))
- PASS A3c every '+' line the brief adds is in the declared sections (26 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)
- PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)
- PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (9 failed / 12 run; controls green; assertion reds)
- PASS A5 GREEN-AFTER: every declared test passes with all 2 product section(s) (12 passed / 12 run)
- PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip
- PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)
- SUMMARY files=3 products=2 tests=1 red_first=yes apply_mode=strict
- PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=6 ok=6 bad=0 skipped_newfile=1)

## PR NOTES for the raise seat
- CODE_PATCH2 — products `Blockchain/Dev/services/api-gateway/src/routes/batch.ts` and `…/routes/audit-export.ts`, plus ONE new test (the fake req/res dispatch of notifications.test.ts). `Refs KS-1410` — closes 4 of the ticket's 28 sites; with the notifications carve, 10 of 28. Name the other 18 as open (E-lane file `transfer/delegations.ts`; tenant-provisioning has no harness; mcp-server listens at import).
- Real reachable path, measured by the drafter: `{"documents":[null]}` to `POST /api/batch/certifications` leaks the TypeError text in the 500 body today.
- Harness note (screen finding): code_patch2's A3b grades only the FIRST product's sites; `audit-export.ts:196` is covered by A3x byte identity and the audit test cells, not by A3b. Say so in Test Evidence.
- Stacks with the notifications carve (both goldens apply together; api-gateway 818 → 845, tsc rc 0, drafter). Raise them in ONE PR or two adjacent PRs, the raise seat's call; tier: the gate decides (information disclosure in error bodies → recommend TIER 1).
- Disjoint from Seat E 10th's `routes/verification.ts` and its ks529 test (same service, different files).

```diff
--- a/Blockchain/Dev/services/api-gateway/src/routes/batch.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/batch.ts
@@ -13,7 +13,19 @@
 import { Router, Request, Response } from 'express';
+import { logger } from '../utils/logger';
-
+
 const router = Router();
-
+
+/**
+ * KS-1410: the only place in this router that turns a caught error into a 500. The three route catch blocks below put the
+ * thrown error's own text in the 500 body with NO NODE_ENV guard, so it reached the client in every environment,
+ * production included. Same shape as originate's fail500 (KS-1334, KS-730): log the thrown text server-side with
+ * the route named, answer the constant body.
+ */
+function fail500(res: Response, context: string, err: unknown): void {
+  logger.error(context, { error: err instanceof Error ? err.message : String(err) });
+  res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
+}
+
 // ---------------------------------------------------------------------------
 // Inline validators (api-gateway does not depend on zod)
 // ---------------------------------------------------------------------------
@@ -164,5 +176,5 @@
     res.json(buildBatchResponse(results));
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message || 'Internal server error' } });
+    fail500(res, 'Batch certify failed (POST /api/batch/certifications)', err);
   }
 });
@@ -212,5 +224,5 @@
     res.json(buildBatchResponse(results));
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message || 'Internal server error' } });
+    fail500(res, 'Batch verify failed (POST /api/batch/verify)', err);
   }
 });
@@ -260,5 +272,5 @@
     res.json(buildBatchResponse(results));
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message || 'Internal server error' } });
+    fail500(res, 'Batch delegate failed (POST /api/batch/delegations)', err);
   }
 });
--- a/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
@@ -13,7 +13,19 @@
 import { Router, Request, Response } from 'express';
+import { logger } from '../utils/logger';
-
+
 const router = Router();
-
+
+/**
+ * KS-1410: the only place in this router that turns a caught error into a 500. The route's catch block below put the
+ * thrown error's own text in the 500 body with NO NODE_ENV guard, so it reached the client in every environment,
+ * production included. Same shape as originate's fail500 (KS-1334, KS-730): log the thrown text server-side with
+ * the route named, answer the constant body.
+ */
+function fail500(res: Response, context: string, err: unknown): void {
+  logger.error(context, { error: err instanceof Error ? err.message : String(err) });
+  res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
+}
+
 // ---------------------------------------------------------------------------
 // Types
 // ---------------------------------------------------------------------------
@@ -193,6 +205,6 @@
       data: entries,
     });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message || 'Internal server error' } });
+    fail500(res, 'Audit export failed (GET /api/admin/audit/export)', err);
   }
 });
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1410-batch-and-audit-export-500-never-answer-err-message.test.ts
@@ -0,0 +1,136 @@
+/**
+ * KS-1410 (api-gateway routes/batch.ts + routes/audit-export.ts): four catch blocks answered a 500 whose body
+ * carried the thrown error's own text (`err.message || 'Internal server error'`) with NO NODE_ENV guard, so it
+ * reached the client in every environment, production included (batch.ts :166 :214 :262, audit-export.ts :196 at
+ * develop 147ae442074c). The fix gives each file a fail500 helper, the shape of originate's (KS-1334, KS-730): log
+ * the thrown text server-side with the route named, answer the constant body.
+ *
+ * Harness: the fake req/res dispatch of notifications.test.ts (the real routers, no server, no network).
+ * HOW EACH CATCH IS REACHED: every route reads req.user FIRST, inside its try. The fake request's user carries a
+ * getter that throws LEAK on the field the route reads (batch: userId; audit export: role), so the throw lands in
+ * the catch under test and no upstream is called. R3 reaches the certify catch the real way: a null entry in
+ * `documents` makes validateBatchCertify throw a TypeError.
+ */
+import { describe, it, expect, vi, afterEach, beforeEach } from 'vitest';
+import type { Request, Response, Router } from 'express';
+
+const mockLoggerError = vi.hoisted(() => vi.fn());
+vi.mock('../utils/logger', () => ({
+  logger: { error: mockLoggerError, warn: vi.fn(), info: vi.fn(), debug: vi.fn() },
+}));
+
+import batchRouter from '../routes/batch';
+import auditExportRouter from '../routes/audit-export';
+
+// THE FIXTURE IS LOAD-BEARING: a private host:port and a marker no other code path could produce.
+const LEAK = 'connect ECONNREFUSED 10.0.4.17:5432 ks1410-private-detail';
+const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
+const NODE_ENVS = ['production', 'development', 'test'];
+
+type CapturedRes = Response & { _status: number; _json: unknown };
+
+function makeRes(onFinish: () => void): CapturedRes {
+  const res: any = {
+    _status: 200,
+    _json: null,
+    status(code: number) {
+      res._status = code;
+      return res;
+    },
+    json(body: unknown) {
+      res._json = body;
+      onFinish();
+      return res;
+    },
+    setHeader() {
+      return res;
+    },
+  };
+  return res;
+}
+
+function dispatch(router: Router, opts: { method: string; url: string; user?: unknown; body?: unknown }): Promise<CapturedRes> {
+  return new Promise((resolve, reject) => {
+    const res = makeRes(() => resolve(res));
+    const req = {
+      method: opts.method,
+      url: opts.url,
+      headers: {},
+      body: opts.body,
+      query: {},
+      user: opts.user,
+      get(name: string) {
+        return (this as any).headers[name?.toLowerCase()];
+      },
+    } as unknown as Request;
+    router(req, res as any, (err: unknown) => (err ? reject(err) : resolve(res)));
+  });
+}
+
+/** A req.user whose `field` throws LEAK when the route reads it. */
+function throwingUser(field: string): Record<string, unknown> {
+  return Object.defineProperty({}, field, {
+    enumerable: true,
+    get() {
+      throw new Error(LEAK);
+    },
+  });
+}
+
+const ROUTES = [
+  { label: 'batch POST /certifications', router: batchRouter, method: 'POST', url: '/certifications', field: 'userId', context: 'Batch certify failed (POST /api/batch/certifications)' },
+  { label: 'batch POST /verify', router: batchRouter, method: 'POST', url: '/verify', field: 'userId', context: 'Batch verify failed (POST /api/batch/verify)' },
+  { label: 'batch POST /delegations', router: batchRouter, method: 'POST', url: '/delegations', field: 'userId', context: 'Batch delegate failed (POST /api/batch/delegations)' },
+  { label: 'audit GET /export', router: auditExportRouter, method: 'GET', url: '/export', field: 'role', context: 'Audit export failed (GET /api/admin/audit/export)' },
+];
+
+beforeEach(() => mockLoggerError.mockClear());
+afterEach(() => vi.unstubAllEnvs());
+
+describe('KS-1410 api-gateway batch + audit export: a 500 never answers the thrown text', () => {
+  it.each(ROUTES)('RED KS-1410 R1 $label: the thrown message is not in the 500 body under production, development or test', async (route) => {
+    for (const nodeEnv of NODE_ENVS) {
+      vi.stubEnv('NODE_ENV', nodeEnv);
+      mockLoggerError.mockClear();
+      const res = await dispatch(route.router, { method: route.method, url: route.url, user: throwingUser(route.field), body: {} });
+      expect({ nodeEnv, status: res._status, leaked: JSON.stringify(res._json).includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
+      expect(res._json).toEqual(CONSTANT_BODY);
+      // REACHED, not merely clean: only fail500 logs this route's context with the thrown text.
+      expect(mockLoggerError.mock.calls.at(-1)).toEqual([route.context, { error: LEAK }]);
+    }
+  });
+
+  it.each(ROUTES)('RED KS-1410 R2 $label: the thrown message is logged once, server-side, with this route named', async (route) => {
+    vi.stubEnv('NODE_ENV', 'production');
+    const res = await dispatch(route.router, { method: route.method, url: route.url, user: throwingUser(route.field), body: {} });
+    expect(res._status).toBe(500);
+    expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
+  });
+
+  it('RED KS-1410 R3 batch POST /certifications: a null document entry (a real TypeError) answers the constant 500 body', async () => {
+    vi.stubEnv('NODE_ENV', 'production');
+    const res = await dispatch(batchRouter, { method: 'POST', url: '/certifications', user: { userId: 'u-ks1410' }, body: { documents: [null] } });
+    expect(res._status).toBe(500);
+    expect(res._json).toEqual(CONSTANT_BODY);
+    expect(mockLoggerError.mock.calls).toEqual([['Batch certify failed (POST /api/batch/certifications)', { error: expect.stringContaining('documentHash') }]]);
+  });
+
+  it('control KS-1410 C1: no req.user still answers 401 UNAUTHORIZED on batch and on the audit export', async () => {
+    const batch = await dispatch(batchRouter, { method: 'POST', url: '/certifications', body: {} });
+    const audit = await dispatch(auditExportRouter, { method: 'GET', url: '/export' });
+    expect([batch._status, (batch._json as any).error.code, audit._status, (audit._json as any).error.code]).toEqual([401, 'UNAUTHORIZED', 401, 'UNAUTHORIZED']);
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+
+  it('control KS-1410 C2: a malformed batch body still answers 400 BAD_REQUEST with its validator message', async () => {
+    const res = await dispatch(batchRouter, { method: 'POST', url: '/delegations', user: { userId: 'u-ks1410' }, body: {} });
+    expect(res._status).toBe(400);
+    expect(res._json).toEqual({ success: false, error: { code: 'BAD_REQUEST', message: 'delegations array required' } });
+  });
+
+  it('control KS-1410 C3: a non-admin role still answers 403 FORBIDDEN on the audit export', async () => {
+    const res = await dispatch(auditExportRouter, { method: 'GET', url: '/export', user: { role: 'user' } });
+    expect(res._status).toBe(403);
+    expect((res._json as any).error.code).toBe('FORBIDDEN');
+  });
+});
```
