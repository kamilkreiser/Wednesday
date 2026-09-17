# READY — KS-1196 (api-gateway routes/admin.ts:682: document-type ids `dt-`+Date.now() collide within a millisecond and the second create overwrites the first — default U: `dt-`+crypto.randomUUID(); + a new vitest file) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE, 2026-09-17 15:59
# Source read by Wednesday (scratchpad cmp_brief.py): test 117/117 lines IDENTICAL to the brief (a mutated copy unequal); product `-` identical; the `+` line = the brief's code PLUS a trailing comment `// KS-1196: use crypto.randomUUID to avoid millisecond collisions` (code identical, comment additive, A3i byte-exact); apply LENIENT (the model's hunk-header dialect); A6 no new red; A7 tsc rc 0.
# PR NOTES: Closes KS-1196 (per DEFAULTS2 report; confirm at raise). TIER 2. Default U chosen by Wednesday's agent (no card: no status-code or caller change; ids pass through encodeURIComponent; whether any caller SORTS by id: unmeasured). Side finding for a ticket (read, not run): the handler stores `{ id, ...body }` — a body `id` diverges from its Redis key. Report local-model/night/briefs/DEFAULTS2_2026-09-17.REPORT.md.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
@@ -679,7 +679,7 @@ export function createAdminRoutes(deps: AdminRouteDeps): Router {
     try {
       const body = req.body || {};
-      const id = `dt-${Date.now()}`;
+      const id = `dt-${crypto.randomUUID()}`; // KS-1196: use crypto.randomUUID to avoid millisecond collisions
       const now = new Date().toISOString();
       const docType = {
         id,
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1196-admin-post-api-admin-document-types.test.ts
@@ -0,0 +1,117 @@
+/**
+ * KS-1196: POST /api/admin/document-types built the new id from the clock
+ * alone, so two creates in the same millisecond got the same id, both
+ * answered 201, and the second silently overwrote the first in the catalogue.
+ *
+ * The fix draws the id from crypto.randomUUID and keeps the dt- prefix. These
+ * cells freeze Date.now, so the clock alone can never tell two creates apart.
+ */
+import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
+import type { Request, Response, Router } from 'express';
+import { configureAuth, authenticateToken, parseTestToken } from '../middleware/auth';
+import { createAdminRoutes, type AdminRouteDeps } from '../routes/admin';
+
+const EXPECTED_CELLS = 3;
+let CELLS_RUN = 0;
+const FROZEN_NOW = 1758000000000;
+
+function buildTestToken(payload: Record<string, unknown>): string {
+  return 'test_token_' + Buffer.from(JSON.stringify(payload)).toString('base64');
+}
+
+const ADMIN_HEADERS = {
+  authorization: 'Bearer ' + buildTestToken({ sub: 'admin-1', role: 'SYSTEM_ADMIN', email: 'admin-1@test.io' }),
+};
+
+type CapturedRes = Response & { _status: number; _json: any };
+
+function dispatch(router: Router, body: unknown): Promise<CapturedRes> {
+  return new Promise((resolve, reject) => {
+    const res: any = {
+      _status: 200,
+      _json: null,
+      status(code: number) {
+        res._status = code;
+        return res;
+      },
+      json(payload: unknown) {
+        res._json = payload;
+        resolve(res);
+        return res;
+      },
+      setHeader() {
+        return res;
+      },
+    };
+    const req = {
+      method: 'POST',
+      url: '/api/admin/document-types',
+      headers: ADMIN_HEADERS,
+      body,
+      query: {},
+      get(name: string) {
+        return (this as any).headers[name.toLowerCase()];
+      },
+    } as unknown as Request;
+    router(req, res, (err: unknown) => (err ? reject(err) : resolve(res)));
+  });
+}
+
+let catalogue: Map<string, any>;
+let router: Router;
+
+beforeEach(() => {
+  vi.stubEnv('NODE_ENV', 'test');
+  configureAuth({ enableTestTokens: true, defaultTenantId: 'default' });
+  catalogue = new Map();
+  const redisService = {
+    getAllDocumentTypes: async () => Array.from(catalogue.values()),
+    getDocumentType: async (id: string) => catalogue.get(id) || null,
+    setDocumentType: async (id: string, data: object) => {
+      catalogue.set(id, data);
+    },
+  };
+  router = createAdminRoutes({
+    authenticateToken,
+    parseTestToken,
+    query: async () => ({ rows: [], rowCount: 0 }),
+    isDbAvailable: () => false,
+    redisService,
+    services: {},
+    log: () => undefined,
+  } as unknown as AdminRouteDeps);
+  vi.spyOn(Date, 'now').mockReturnValue(FROZEN_NOW);
+});
+
+afterEach(() => {
+  vi.restoreAllMocks();
+  vi.unstubAllEnvs();
+});
+
+describe('KS-1196 - two document-type creates in one millisecond never share an id', () => {
+  it('KS-1196 R1 - two creates in the same millisecond answer two different ids', async () => {
+    CELLS_RUN += 1;
+    const first = await dispatch(router, { name: 'Alpha Type', code: 'ALPHA' });
+    const second = await dispatch(router, { name: 'Beta Type', code: 'BETA' });
+    expect([first._status, second._status]).toEqual([201, 201]);
+    expect(first._json.id).not.toBe(second._json.id);
+  });
+  it('KS-1196 R2 - both types are still in the catalogue after the second create', async () => {
+    CELLS_RUN += 1;
+    await dispatch(router, { name: 'Alpha Type', code: 'ALPHA' });
+    await dispatch(router, { name: 'Beta Type', code: 'BETA' });
+    const names = Array.from(catalogue.values()).map((t) => t.name).sort();
+    expect(names).toEqual(['Alpha Type', 'Beta Type']);
+  });
+  it('KS-1196 CONTROL - one create answers 201 with a dt- id stored under that same key', async () => {
+    CELLS_RUN += 1;
+    const res = await dispatch(router, { name: 'Gamma Type', code: 'GAMMA' });
+    expect(res._status).toBe(201);
+    expect(res._json.id.startsWith('dt-')).toBe(true);
+    expect(res._json.name).toBe('Gamma Type');
+    expect(Array.from(catalogue.keys())).toEqual([res._json.id]);
+  });
+  it('KS-1196 COMPLETENESS - every graded cell above actually ran', () => {
+    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
+  });
+});
```
