# READY — KS-1230 (Ornith, briefed, vitest code_patch) — PASS 7/7 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-18_ks1230-ornith35b-night/out.md.checker/section_N.diff`, each applied with its `section_N.opts`.** Raise from those, not from the fence below.

**Held 2026-09-18 15:20 by the 14:4x Wednesday seat after a source read.** Run `runs/2026-09-18_ks1230-ornith35b-night`. Tip `8b9c3f022` (builder's ls-remote pin). Product `services/api-gateway/src/routes/admin.ts`. Brief `night/briefs/KS-1230.md` (search subagent, 14:5x-15:0x).

## Source read
- PUT /api/admin/settings refuses (400 VALIDATION_ERROR, stores nothing) any present, non-null integrations[i].config.allowedDocumentTypes that is not an array of strings; absent/null stays allowed (the readers treat it as no restriction - verification.ts:1216-1218 read by Wednesday). Red 4/6 at tip, 6/6 after. BEHAVIOUR CHANGE on an admin write path: say so in the PR body.
- The product hunk's '+' and '-' lines are IDENTICAL to the brief's edit block (Wednesday's line compare; crossed control KS-1258 brief vs KS-1230 diff = 17 of 17 missing, so the compare can fail).
- Checker: A1-A7 PASS incl. A6 (whole api-gateway suite, no NEW red) and A7 strict tsc.
**HELD. Not raised.** Refs KS-1230, linkKind contributes, no closing phrase.

---
## The model's output, verbatim

```diff
--- a/services/api-gateway/src/routes/admin.ts
+++ b/services/api-gateway/src/routes/admin.ts
@@ -1123,4 +1123,18 @@
   router.put('/api/admin/settings', requireAdmin, mockBodyParser, async (req: Request, res: Response) => {
     const body = req.body || {};
+    // KS-1230: validate every integrations[].config.allowedDocumentTypes BEFORE the merge and the write. A string, an
+    // object or an empty string was stored as given and, after KS-1204, locked that connector out of every create.
+    // Absent (undefined or null) stays allowed: the readers treat it as no restriction.
+    const ints = body.integrations;
+    if (Array.isArray(ints)) {
+      for (let i = 0; i < ints.length; i++) {
+        const types = ints[i]?.config?.allowedDocumentTypes;
+        if (types === undefined || types === null) continue;
+        if (!Array.isArray(types) || !types.every((t: unknown) => typeof t === 'string')) {
+          res.status(400).json({ success: false, error: { code: 'VALIDATION_ERROR', message: 'integrations[' + i + '].config.allowedDocumentTypes must be an array of strings' } });
+          return;
+        }
+      }
+    }
     const existing = (await redisService.getNotificationSettings('platform-settings') || {}) as Record<string, unknown>;
     const merged = { ...existing, ...body };
--- /dev/null
+++ b/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts
@@ -0,0 +1,129 @@
+/**
+ * =============================================================================
+ * KS-1230 - PUT /api/admin/settings must refuse a malformed allowedDocumentTypes
+ * =============================================================================
+ * routes/admin.ts PUT /api/admin/settings merged the body over the stored
+ * platform-settings and wrote it with no validation, so a string, an object or
+ * an empty string was stored as a connector's allow-list. After KS-1204 the read
+ * side refuses every create for a non-array allow-list, so one malformed admin
+ * save locked the connector out and nobody learned it until the 403s.
+ *
+ * These cells call the REAL admin router in-process with a recording
+ * redisService stub (the dispatch shape of ks719-settings-write-auth.test.ts).
+ * No gateway boot, no network, no Redis.
+ * =============================================================================
+ */
+import { describe, it, expect, beforeEach } from 'vitest';
+import type { Request, Response, Router, RequestHandler } from 'express';
+import { createAdminRoutes, type AdminRouteDeps } from '../routes/admin';
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
+    send(body: unknown) {
+      res._json = body;
+      onFinish();
+      return res;
+    },
+  };
+  return res;
+}
+
+function dispatch(router: Router, body: unknown): Promise<CapturedRes> {
+  return new Promise((resolve, reject) => {
+    const res = makeRes(() => resolve(res));
+    const req = {
+      method: 'PUT',
+      url: '/api/admin/settings',
+      headers: { authorization: 'Bearer ks1230-admin' },
+      body,
+      query: {},
+      get(name: string) {
+        return (this as any).headers[name?.toLowerCase()];
+      },
+    } as unknown as Request;
+    router(req, res as any, (err: unknown) => (err ? reject(err) : resolve(res)));
+  });
+}
+
+const ADMIN = { userId: 'ks1230-admin', email: 'ks1230@test.io', role: 'SYSTEM_ADMIN', verificationLevel: 'BASIC' };
+
+function build() {
+  const writes: Array<{ key: string; value: unknown }> = [];
+  const passThrough: RequestHandler = (_req, _res, next) => next();
+  const router = createAdminRoutes({
+    authenticateToken: () => passThrough,
+    parseTestToken: () => ADMIN,
+    query: async () => ({ rows: [], rowCount: 0 }),
+    isDbAvailable: () => false,
+    redisService: {
+      getNotificationSettings: async () => null,
+      setNotificationSettings: async (key: string, value: unknown) => {
+        writes.push({ key, value });
+      },
+    },
+    services: {},
+    log: () => undefined,
+  } as unknown as AdminRouteDeps);
+  return { router, writes };
+}
+
+const withTypes = (allowedDocumentTypes: unknown) => ({
+  integrations: [{ id: 'ks1230-c1', config: { allowedDocumentTypes } }],
+});
+
+describe('KS-1230: PUT /api/admin/settings validates allowedDocumentTypes at write time', () => {
+  let h: ReturnType<typeof build>;
+
+  beforeEach(() => {
+    h = build();
+  });
+
+  it('🔴 a STRING allow-list is refused with 400 VALIDATION_ERROR and nothing is stored', async () => {
+    const res = await dispatch(h.router, withTypes('SSD_DOCUMENT'));
+    expect([res._status, (res._json as any)?.error?.code, h.writes.length]).toEqual([400, 'VALIDATION_ERROR', 0]);
+  });
+
+  it('🔴 an OBJECT allow-list is refused with 400 VALIDATION_ERROR and nothing is stored', async () => {
+    const res = await dispatch(h.router, withTypes({ a: 'SSD_DOCUMENT' }));
+    expect([res._status, (res._json as any)?.error?.code, h.writes.length]).toEqual([400, 'VALIDATION_ERROR', 0]);
+  });
+
+  it('🔴 an EMPTY STRING allow-list is refused with 400 VALIDATION_ERROR and nothing is stored', async () => {
+    const res = await dispatch(h.router, withTypes(''));
+    expect([res._status, (res._json as any)?.error?.code, h.writes.length]).toEqual([400, 'VALIDATION_ERROR', 0]);
+  });
+
+  it('🔴 an array holding a NON-STRING is refused with 400 VALIDATION_ERROR and nothing is stored', async () => {
+    const res = await dispatch(h.router, withTypes(['SSD_DOCUMENT', 5]));
+    expect([res._status, (res._json as any)?.error?.code, h.writes.length]).toEqual([400, 'VALIDATION_ERROR', 0]);
+  });
+
+  it('control: an array of strings and an empty array are stored with 200', async () => {
+    const a = await dispatch(h.router, withTypes(['SSD_DOCUMENT']));
+    const b = await dispatch(h.router, withTypes([]));
+    expect([a._status, b._status, h.writes.length]).toEqual([200, 200, 2]);
+    expect(h.writes[0]).toEqual({ key: 'platform-settings', value: withTypes(['SSD_DOCUMENT']) });
+  });
+
+  it('control: an ABSENT allow-list and a body with no integrations are stored with 200', async () => {
+    const a = await dispatch(h.router, { integrations: [{ id: 'ks1230-c2', config: { workflowPolicy: 'enforce' } }] });
+    const b = await dispatch(h.router, { general: { platformName: 'Secuura' } });
+    expect([a._status, b._status, h.writes.length]).toEqual([200, 200, 2]);
+  });
+});
```
