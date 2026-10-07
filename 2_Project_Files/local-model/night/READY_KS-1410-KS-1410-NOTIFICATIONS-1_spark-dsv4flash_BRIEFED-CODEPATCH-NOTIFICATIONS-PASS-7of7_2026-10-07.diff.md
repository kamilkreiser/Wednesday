# READY — KS-1410-KS-1410-NOTIFICATIONS-1 (Spark DeepSeek V4 Flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1410-apigw-notifications-500/out.md.checker/patch.diff`** (from `ls` at 15:41 2026-10-07; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1410-apigw-notifications-500/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1410-apigw-notifications-500/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1410-apigw-notifications-500/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1410-apigw-notifications-500-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 15:41 2026-10-07 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1410-apigw-notifications-500/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `147ae442074c7f3b5be9ce7ccc4452c8dae34b4f`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/routes/notifications.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1410-notifications-500-never-answers-err-message.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/notifications.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1410-notifications-500-never-answers-err-message.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
20	8	Blockchain/Dev/services/api-gateway/src/routes/notifications.ts
138	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1410-notifications-500-never-answers-err-message.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (17 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 20 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 8.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/routes/notifications.ts byte-exact incl. leading whitespace (apply mode strict): OK 17 line(s) byte-exact incl. leading whitespace (of 17; 18 line(s) added by the apply)` [a3i_indent.out: `OK 17 line(s) byte-exact incl. leading whitespace (of 17; 18 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/notifications.ts` (hunks=7, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1410-notifications-500-never-answers-err-message.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1410-notifications-500-never-answers-err-message.test.ts fails at the untouched tip (12 failed / 15 run; controls green; assertion reds)` [red_first.json: failed=12 of total=15; red cell(s): ["KS-1410 api-gateway notifications: a 500 never answers the thrown text RED KS-1410 N1 'GET /': the thrown message is not in the 500 body under production, development or test", "KS-1410 api-gateway notifications: a 500 never answers the thrown text RED KS-1410 N1 'GET /unread/count': the thrown message is not in the 500 body under production, development or test", "KS-1410 api-gateway notifications: a 500 never answers the thrown text RED KS-1410 N1 'PATCH /:id/read': the thrown message is not in the 500 body under production, development or test", "KS-1410 api-gateway notifications: a 500 never answers the thrown text RED KS-1410 N1 'PATCH /read-all': the thrown message is not in the 500 body under production, development or test", "KS-1410 api-gateway notifications: a 500 never answers the thrown text RED KS-1410 N1 'DELETE /:id': the thrown message is not in the 500 body under production, development or test", "KS-1410 api-gateway notifications: a 500 never answers the thrown text RED KS-1410 N1 'POST /': the thrown message is not in the 500 body under production, development or test", "KS-1410 api-gateway notifications: a 500 never answers the thrown text RED KS-1410 N2 'GET /': the thrown message is logged once, server-side, with this route named", "KS-1410 api-gateway notifications: a 500 never answers the thrown text RED KS-1410 N2 'GET /unread/count': the thrown message is logged once, server-side, with this route named", "KS-1410 api-gateway notifications: a 500 never answers the thrown text RED KS-1410 N2 'PATCH /:id/read': the thrown message is logged once, server-side, with this route named", "KS-1410 api-gateway notifications: a 500 never answers the thrown text RED KS-1410 N2 'PATCH /read-all': the thrown message is logged once, server-side, with this route named", "KS-1410 api-gateway notifications: a 500 never answers the thrown text RED KS-1410 N2 'DELETE /:id': the thrown message is logged once, server-side, with this route named", "KS-1410 api-gateway notifications: a 500 never answers the thrown text RED KS-1410 N2 'POST /': the thrown message is logged once, server-side, with this route named"]]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1410-notifications-500-never-answers-err-message.test.ts passes with the product hunk (15 passed / 15 run)` [green_after.json: failed=0 of total=15, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=818 failed=0 | after: total=833 failed=0` · `NEW reds: []` [baseline_suite.json total=818 failed=0; after_suite.json total=833 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +158/-8 test=src/__tests__/ks1410-notifications-500-never-answers-err-message.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/notifications.ts` (+20/-8 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1410-notifications-500-never-answers-err-message.test.ts` (+138/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `147ae442074c7f3b5be9ce7ccc4452c8dae34b4f` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1410-apigw-notifications-500/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1410-apigw-notifications-500/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/routes/notifications.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/notifications.ts
@@ -13,7 +13,19 @@
 import { Router, Request, Response } from 'express';
 import crypto from 'crypto';
 import { authenticateToken } from '../middleware/auth';
+import { logger } from '../utils/logger';
-
+
 const router = Router();
-
+
+/**
+ * KS-1410: the only place in this router that turns a caught error into a 500. The six route catch blocks below put
+ * the thrown error's own text in the 500 body with NO NODE_ENV guard, so it reached the client in every environment,
+ * production included. Same shape as originate's fail500 (KS-1334, KS-730): log the thrown text server-side with
+ * the route named, answer the constant body.
+ */
+function fail500(res: Response, context: string, err: unknown): void {
+  logger.error(context, { error: err instanceof Error ? err.message : String(err) });
+  res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
+}
+
 // KS-375: every notifications operation is documented as bearer-authed
@@ -123,6 +135,6 @@
       },
     });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message || 'Internal server error' } });
+    fail500(res, 'Notification list failed (GET /api/notifications)', err);
   }
 });
@@ -145,5 +157,5 @@
     res.json({ success: true, data: { unreadCount } });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message || 'Internal server error' } });
+    fail500(res, 'Unread count failed (GET /api/notifications/unread/count)', err);
   }
 });
@@ -174,5 +186,5 @@
     res.json({ success: true, data: notification });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message || 'Internal server error' } });
+    fail500(res, 'Mark read failed (PATCH /api/notifications/:id/read)', err);
   }
 });
@@ -202,5 +214,5 @@
     res.json({ success: true, data: { updatedCount } });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message || 'Internal server error' } });
+    fail500(res, 'Mark all read failed (PATCH /api/notifications/read-all)', err);
   }
 });
@@ -232,5 +244,5 @@
     res.json({ success: true, message: 'Notification deleted' });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message || 'Internal server error' } });
+    fail500(res, 'Notification delete failed (DELETE /api/notifications/:id)', err);
   }
 });
@@ -288,5 +300,5 @@
     res.status(201).json({ success: true, data: notification });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message || 'Internal server error' } });
+    fail500(res, 'Notification create failed (POST /api/notifications)', err);
   }
 });
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1410-notifications-500-never-answers-err-message.test.ts
@@ -0,0 +1,138 @@
+/**
+ * KS-1410 (api-gateway routes/notifications.ts): six catch blocks answered a 500 whose body carried the thrown
+ * error's own text (`err.message || 'Internal server error'`) with NO NODE_ENV guard, so it reached the client in
+ * every environment, production included (:126 :147 :176 :204 :234 :290 at develop 147ae442074c). The fix gives the
+ * file a fail500 helper, the shape of originate's (KS-1334, KS-730): log the thrown text server-side with the route
+ * named, answer the constant body.
+ *
+ * Harness: the fake req/res dispatch of notifications.test.ts (the real router, no server, no network), with the
+ * router-wide authenticateToken replaced by a pass-through, so req.user is exactly what the cell sets.
+ * HOW EACH CATCH IS REACHED: five routes read req.user FIRST, inside their try, and the fake request's user carries
+ * a userId getter that throws LEAK; POST / destructures req.body first, and its body carries the throwing getter.
+ */
+import { describe, it, expect, vi, afterEach, beforeEach } from 'vitest';
+import type { Request, Response, Router } from 'express';
+
+const mockLoggerError = vi.hoisted(() => vi.fn());
+vi.mock('../utils/logger', () => ({
+  logger: { error: mockLoggerError, warn: vi.fn(), info: vi.fn(), debug: vi.fn() },
+}));
+vi.mock('../middleware/auth', () => ({
+  authenticateToken: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+}));
+
+import notificationsRouter from '../routes/notifications';
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
+/** An object whose `field` throws LEAK when the route reads it. */
+function throwing(field: string): Record<string, unknown> {
+  return Object.defineProperty({}, field, {
+    enumerable: true,
+    get() {
+      throw new Error(LEAK);
+    },
+  });
+}
+
+const ROUTES = [
+  { label: 'GET /', method: 'GET', url: '/', via: 'user', context: 'Notification list failed (GET /api/notifications)' },
+  { label: 'GET /unread/count', method: 'GET', url: '/unread/count', via: 'user', context: 'Unread count failed (GET /api/notifications/unread/count)' },
+  { label: 'PATCH /:id/read', method: 'PATCH', url: '/n-ks1410/read', via: 'user', context: 'Mark read failed (PATCH /api/notifications/:id/read)' },
+  { label: 'PATCH /read-all', method: 'PATCH', url: '/read-all', via: 'user', context: 'Mark all read failed (PATCH /api/notifications/read-all)' },
+  { label: 'DELETE /:id', method: 'DELETE', url: '/n-ks1410', via: 'user', context: 'Notification delete failed (DELETE /api/notifications/:id)' },
+  { label: 'POST /', method: 'POST', url: '/', via: 'body', context: 'Notification create failed (POST /api/notifications)' },
+];
+
+function arm(route: (typeof ROUTES)[number]) {
+  return route.via === 'user'
+    ? { method: route.method, url: route.url, user: throwing('userId'), body: {} }
+    : { method: route.method, url: route.url, user: { userId: 'u-ks1410' }, body: throwing('userId') };
+}
+
+beforeEach(() => mockLoggerError.mockClear());
+afterEach(() => vi.unstubAllEnvs());
+
+describe('KS-1410 api-gateway notifications: a 500 never answers the thrown text', () => {
+  it.each(ROUTES)('RED KS-1410 N1 $label: the thrown message is not in the 500 body under production, development or test', async (route) => {
+    for (const nodeEnv of NODE_ENVS) {
+      vi.stubEnv('NODE_ENV', nodeEnv);
+      mockLoggerError.mockClear();
+      const res = await dispatch(notificationsRouter, arm(route));
+      expect({ nodeEnv, status: res._status, leaked: JSON.stringify(res._json).includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
+      expect(res._json).toEqual(CONSTANT_BODY);
+      // REACHED, not merely clean: only fail500 logs this route's context with the thrown text.
+      expect(mockLoggerError.mock.calls.at(-1)).toEqual([route.context, { error: LEAK }]);
+    }
+  });
+
+  it.each(ROUTES)('RED KS-1410 N2 $label: the thrown message is logged once, server-side, with this route named', async (route) => {
+    vi.stubEnv('NODE_ENV', 'production');
+    const res = await dispatch(notificationsRouter, arm(route));
+    expect(res._status).toBe(500);
+    expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
+  });
+
+  it('control KS-1410 NC1: no req.user still answers 401 UNAUTHORIZED on GET /', async () => {
+    const res = await dispatch(notificationsRouter, { method: 'GET', url: '/' });
+    expect(res._status).toBe(401);
+    expect((res._json as any).error.code).toBe('UNAUTHORIZED');
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+
+  it('control KS-1410 NC2: a POST / missing its fields still answers 400 BAD_REQUEST', async () => {
+    const res = await dispatch(notificationsRouter, { method: 'POST', url: '/', user: { userId: 'u-ks1410' }, body: { userId: 'r-ks1410' } });
+    expect(res._status).toBe(400);
+    expect((res._json as any).error.code).toBe('BAD_REQUEST');
+  });
+
+  it('control KS-1410 NC3: create then list still answers 201 then 200 with the created row', async () => {
+    const created = await dispatch(notificationsRouter, { method: 'POST', url: '/', user: { userId: 'u-ks1410' }, body: { userId: 'reader-ks1410', type: 'system', title: 'T', message: 'M' } });
+    const listed = await dispatch(notificationsRouter, { method: 'GET', url: '/', user: { userId: 'reader-ks1410' } });
+    expect([created._status, listed._status, (listed._json as any).data.map((n: any) => n.title)]).toEqual([201, 200, ['T']]);
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+});
```

**Raise note (Wednesday, 15:41):** the golden carries two whitespace-only blank-line changes near the `logger` import in notifications.ts (`-`/`+` of an empty line); harmless, but name them in the PR body or let the raise seat normalise them only if the gate agrees. Wednesday read the product hunks at source before queueing (information-leak surface).
