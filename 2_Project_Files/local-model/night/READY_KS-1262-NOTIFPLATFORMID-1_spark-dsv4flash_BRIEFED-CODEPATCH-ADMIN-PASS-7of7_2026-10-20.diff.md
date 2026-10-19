# READY — KS-1262-NOTIFPLATFORMID-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1262_p1/out.md.checker/patch.diff`** (from `ls` at 01:02 2026-10-20; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1262_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1262_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1262_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1262_p1-control/out.md.checker/patch.diff` rc 0, Wednesday (overnight 10-20)).

**Held 01:02 2026-10-20 by Wednesday (overnight 10-20) after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1262_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `a66cd6a4d1726794c816fd4fefec58c728d410e5`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/routes/admin.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1262-notification-put-cannot-write-platform-settings.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1262-notification-put-cannot-write-platform-settings.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
5	0	Blockchain/Dev/services/api-gateway/src/routes/admin.ts
138	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1262-notification-put-cannot-write-platform-settings.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (5 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 5 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/routes/admin.ts byte-exact incl. leading whitespace (apply mode strict): OK 5 line(s) byte-exact incl. leading whitespace (of 5; 5 line(s) added by the apply)` [a3i_indent.out: `OK 5 line(s) byte-exact incl. leading whitespace (of 5; 5 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1262-notification-put-cannot-write-platform-settings.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1262-notification-put-cannot-write-platform-settings.test.ts fails at the untouched tip (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-1262 - the per-user notification PUT cannot reach the platform-settings record RED KS-1262 R1: a role-user caller whose userId is platform-settings is refused 403 FORBIDDEN and nothing is written', 'KS-1262 - the per-user notification PUT cannot reach the platform-settings record RED KS-1262 R2: the refusal is by id, not by role: an admin-role caller with that userId is refused too', 'KS-1262 - the per-user notification PUT cannot reach the platform-settings record RED KS-1262 R3: the platform-wide record is untouched after the refused PUT']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1262-notification-put-cannot-write-platform-settings.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1158 failed=0 | after: total=1164 failed=0` · `NEW reds: []` [baseline_suite.json total=1158 failed=0; after_suite.json total=1164 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +143/-0 test=src/__tests__/ks1262-notification-put-cannot-write-platform-settings.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (+5/-0 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1262-notification-put-cannot-write-platform-settings.test.ts` (+138/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `a66cd6a4d1726794c816fd4fefec58c728d410e5` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1262_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1262_p1/KS-1262.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1262_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
index 046a17226..15b37033f 100644
--- a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
@@ -1492,2 +1492,7 @@
     const userId = req.user!.userId;
+    // KS-1262: the platform-wide record is stored under the same namespace; this per-user writer must never address it.
+    if (userId === 'platform-settings') {
+      res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'This identity cannot write per-user notification settings' } });
+      return;
+    }
     const body = req.body || {};
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1262-notification-put-cannot-write-platform-settings.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1262-notification-put-cannot-write-platform-settings.test.ts
new file mode 100644
index 000000000..1010b8d67
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1262-notification-put-cannot-write-platform-settings.test.ts
@@ -0,0 +1,138 @@
+/**
+ * KS-1262 - PUT /api/settings/notifications must not write the platform-wide `platform-settings` record.
+ *
+ * Both PUT /api/admin/settings (requireAdmin) and PUT /api/settings/notifications (any authenticated caller) store through
+ * setNotificationSettings(key, data), under the same `notif:<key>` namespace. The per-user route used the caller's own userId as the
+ * key, so a caller whose userId was exactly `platform-settings` replaced the platform-wide record without the admin door.
+ * After this change that one id is refused with 403 FORBIDDEN and nothing is written; every other id behaves as before.
+ *
+ * These tests dispatch through the real admin router with the real authentication middleware and a recording Redis stand-in.
+ */
+
+import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
+import type { Request, Response, Router, RequestHandler } from 'express';
+import { configureAuth, authenticateToken, parseTestToken } from '../middleware/auth';
+import { createAdminRoutes, type AdminRouteDeps } from '../routes/admin';
+
+function buildTestToken(payload: Record<string, unknown>): string {
+  return `test_token_${Buffer.from(JSON.stringify(payload)).toString('base64')}`;
+}
+
+type CapturedRes = Response & { _status: number; _json: unknown };
+
+function makeRes(onFinish: () => void): CapturedRes {
+  const res: any = {
+    _status: 200,
+    _json: null,
+    status(code: number) { res._status = code; return res; },
+    json(body: unknown) { res._json = body; onFinish(); return res; },
+    setHeader() { return res; },
+    send(body: unknown) { res._json = body; onFinish(); return res; },
+  };
+  return res;
+}
+
+function dispatch(router: Router, opts: { method: string; url: string; headers?: Record<string, string>; body?: unknown }): Promise<CapturedRes> {
+  return new Promise((resolve, reject) => {
+    const res = makeRes(() => resolve(res));
+    const req = {
+      method: opts.method,
+      url: opts.url,
+      headers: opts.headers || {},
+      body: opts.body,
+      query: {},
+      get(name: string) { return (this as any).headers[name?.toLowerCase()]; },
+    } as unknown as Request;
+    router(req, res as any, (err: unknown) => (err ? reject(err) : resolve(res)));
+  });
+}
+
+const SEED = { general: { platformName: 'Seeded Platform' }, integrations: [{ config: { allowedDocumentTypes: ['DOCUMENT'] } }] };
+
+function makeRecordingRedis() {
+  const notif = new Map<string, unknown>([['platform-settings', SEED]]);
+  const writes: string[] = [];
+  return {
+    writes,
+    notif,
+    service: {
+      getNotificationSettings: async (key: string) => (notif.has(key) ? notif.get(key) : null),
+      setNotificationSettings: async (key: string, value: unknown) => { writes.push(key); notif.set(key, value); },
+    },
+  };
+}
+
+function buildRouter(redisService: object): Router {
+  const passThroughBodyParser: RequestHandler = (_req, _res, next) => next();
+  return createAdminRoutes({
+    authenticateToken,
+    parseTestToken,
+    mockBodyParser: passThroughBodyParser,
+    query: async () => ({ rows: [], rowCount: 0 }),
+    isDbAvailable: () => false,
+    redisService,
+    services: {},
+    log: () => undefined,
+  } as unknown as AdminRouteDeps);
+}
+
+describe('KS-1262 - the per-user notification PUT cannot reach the platform-settings record', () => {
+  let redis: ReturnType<typeof makeRecordingRedis>;
+  let router: Router;
+
+  beforeEach(() => {
+    vi.stubEnv('NODE_ENV', 'test');
+    configureAuth({ enableTestTokens: true, defaultTenantId: 'default' });
+    redis = makeRecordingRedis();
+    router = buildRouter(redis.service);
+  });
+
+  afterEach(() => {
+    vi.unstubAllEnvs();
+  });
+
+  const put = (sub: string, role: string) => dispatch(router, {
+    method: 'PUT',
+    url: '/api/settings/notifications',
+    headers: { authorization: `Bearer ${buildTestToken({ sub, role, email: `${sub}@test.io` })}` },
+    body: { integrations: [{ config: { allowedDocumentTypes: 'planted' } }] },
+  });
+
+  it('RED KS-1262 R1: a role-user caller whose userId is platform-settings is refused 403 FORBIDDEN and nothing is written', async () => {
+    const res = await put('platform-settings', 'user');
+    expect(res._status).toBe(403);
+    expect((res._json as any).error.code).toBe('FORBIDDEN');
+    expect(redis.writes).toEqual([]);
+  });
+
+  it('RED KS-1262 R2: the refusal is by id, not by role: an admin-role caller with that userId is refused too', async () => {
+    const res = await put('platform-settings', 'admin');
+    expect(res._status).toBe(403);
+    expect(redis.writes).toEqual([]);
+  });
+
+  it('RED KS-1262 R3: the platform-wide record is untouched after the refused PUT', async () => {
+    await put('platform-settings', 'user');
+    expect(redis.notif.get('platform-settings')).toEqual(SEED);
+  });
+
+  it('CONTROL KS-1262 C1: another userId still writes its own key and leaves the platform record alone', async () => {
+    const res = await put('someone-else', 'user');
+    expect(res._status).toBe(200);
+    expect(redis.writes).toEqual(['someone-else']);
+    expect(redis.notif.get('platform-settings')).toEqual(SEED);
+  });
+
+  it('CONTROL KS-1262 C2: only the exact id is refused: look-alike ids still write their own key', async () => {
+    const a = await put('platform-settings-2', 'user');
+    const b = await put('Platform-Settings', 'user');
+    expect([a._status, b._status]).toEqual([200, 200]);
+    expect(redis.writes).toEqual(['platform-settings-2', 'Platform-Settings']);
+  });
+
+  it('CONTROL KS-1262 C3: the anonymous PUT is still 401 and writes nothing', async () => {
+    const res = await dispatch(router, { method: 'PUT', url: '/api/settings/notifications', body: { x: 1 } });
+    expect(res._status).toBe(401);
+    expect(redis.writes).toEqual([]);
+  });
+});
```
