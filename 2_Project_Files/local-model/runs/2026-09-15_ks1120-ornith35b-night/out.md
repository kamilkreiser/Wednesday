```diff
--- /dev/null
+++ b/services/vc-issuer/src/__tests__/ks1120-f2-db-miss-falls-through-to-memory.test.ts
@@ -0,0 +1,152 @@
+/**
+ * KS-1120 F-2 — DB miss falls through to memory.
+ *
+ * The defect (routes/presentations.ts, getPresentation): when the DB returns
+ * no rows, the function used to fall back to `memPresentationStore.get(id)` and
+ * return that row if present in memory. That path was UNPINNED by tests — no cell
+ * constructs a row that exists ONLY in memory and not in the DB. A tamper that
+ * replaces the comment above line 128 with `return undefined;` simulates this
+ * being broken. This file pins both sides: cells go RED under the tamper because
+ * the memory fallback is skipped → 404 instead of 200.
+ */
+
+import { describe, it, expect, beforeAll, vi } from 'vitest';
+
+// Controllable stand-ins for ../db — each describe scripts its own behaviour.
+// vi.hoisted so the mock factory (hoisted above imports) can reach them.
+const dbMock = vi.hoisted(() => ({
+  isDbAvailable: vi.fn<() => boolean>(() => false),
+  query: vi.fn<(sql: string, params?: unknown[]) => Promise<{ rows: any[] }>>(),
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => dbMock.isDbAvailable(),
+  query: (sql: string, params?: unknown[]) => dbMock.query(sql, params),
+}));
+
+// Silence the winston logger the way db.retry.test.ts does.
+vi.mock('../utils/logger', () => ({
+  logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
+}));
+
+type Router = (rq: any, rs: any, nx: (e?: unknown) => void) => void;
+type Mods = { router: Router; errorHandler: any };
+
+async function freshModules(): Promise<Mods> {
+  vi.resetModules();
+  const { presentationRoutes } = await import('../routes/presentations');
+  const { errorHandler } = await import('../middleware/errorHandler');
+  return { router: presentationRoutes as unknown as Router, errorHandler };
+}
+
+function dispatch(mods: Mods, method: string, url: string, body?: unknown): Promise<{ status: number; body: any }> {
+  return new Promise((resolve, reject) => {
+    const req: any = { method, url, baseUrl: '', originalUrl: url, headers: {}, body };
+    const res: any = {
+      statusCode: 200,
+      status(code: number) {
+        this.statusCode = code;
+        return this;
+      },
+      json(payload: unknown) {
+        resolve({ status: this.statusCode, body: payload });
+        return this;
+      },
+    };
+    const next = (err?: unknown) => {
+      if (err) mods.errorHandler(err as Error, req, res, () => {});
+      else reject(new Error(`route did not match ${method} ${url}`));
+    };
+    mods.router(req, res, next);
+  });
+}
+
+function getById(mods: Mods, id: string) {
+  return dispatch(mods, 'GET', `/${encodeURIComponent(id)}`);
+}
+
+function baseCredential(): Record<string, unknown> {
+  return {
+    '@context': ['https://www.w3.org/2018/credentials/v1'],
+    id: 'urn:uuid:ks1120-test-credential',
+    type: ['VerifiableCredential'],
+    issuer: 'did:prism:secuura_test_issuer',
+    issuanceDate: '2026-01-01T00:00:00Z',
+    credentialSubject: { documentHash: 'ab'.repeat(32) },
+  };
+}
+
+describe('KS-1120 F-2 — DB path with memory fallback pinned', () => {
+  let mods: Mods;
+  let storedId: string;
+
+  beforeAll(async () => {
+    dbMock.isDbAvailable.mockReturnValue(true);
+    // Seed INSERT fails → row exists in MEMORY ONLY.
+    dbMock.query.mockReset();
+    dbMock.query.mockRejectedValue(new Error('insert refused in test'));
+    mods = await freshModules();
+    const created = await dispatch(mods, 'POST', '/', { credentials: [baseCredential()] });
+    expect(created.status).toBe(201);
+    storedId = created.body.presentation.id;
+  });
+
+  it('🔴 KS-1120 F-2 — a row present in memory and absent from the DB answers 200', async () => {
+    const r = await getById(mods, storedId);
+    expect(r.status).toBe(200);
+    expect(r.body?.presentation?.id).toBe(storedId);
+  });
+
+  it('🔴 KS-1120 F-2 — exactly one exact-id SELECT ran, then memory answered', async () => {
+    const r = await getById(mods, storedId);
+    expect(dbMock.query).toHaveBeenCalledTimes(1);
+    const calls = dbMock.query.mock.calls;
+    expect(calls.length).toBeGreaterThan(0);
+    for (const [sql, params] of calls) {
+      expect(String(sql)).toMatch(/WHERE id = \\\$1/);
+      expect(params).toEqual([storedId]);
+    }
+    expect(r.status).toBe(200);
+  });
+
+  it('KS-1120 control — an unknown id is 404 on the DB-miss path', async () => {
+    const r = await getById(mods, 'urn:uuid:not-stored');
+    expect(r.status).toBe(404);
+  });
+});
```
