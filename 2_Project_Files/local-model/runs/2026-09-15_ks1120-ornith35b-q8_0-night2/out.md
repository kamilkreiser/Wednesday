```diff
--- /dev/null
+++ b/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1120-get-api-presentations-id-exact-or.test.ts
@@ -0,0 +1,175 @@
+/**
+ * KS-1120 F-1 — GET /api/presentations/:id on the memory path must be EXACT or 404.
+ *
+ * The defect shape (routes/presentations.ts line 128): if `memPresentationStore.get(id)` were
+ * replaced with a prefix scan (`Array.from(...entries()).find(([k]) => k.startsWith(id))?.[1]`),
+ * any PREFIX or MIDDLE fragment of a stored presentation id would answer 200 instead of 404.
+ * This task is TEST-ONLY at the tip: no product hunk. The checker reddens cells by planting that
+ * tamper into a clone and expects them GREEN when the patch is reverted to the untouched tip.
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
+/** Fresh router + errorHandler per describe, so memPresentationStore starts empty. */
+async function freshModules(): Promise<Mods> {
+  vi.resetModules();
+  const { presentationRoutes } = await import('../routes/presentations');
+  const { errorHandler } = await import('../middleware/errorHandler');
+  return { router: presentationRoutes as unknown as Router, errorHandler };
+}
+
+/**
+ * Dispatch through the real Express router with a mocked req/res pair; route
+ * errors flow into the real shared errorHandler exactly as in index.ts
+ * (same shape as ks444.requestSchema.test.ts).
+ */
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
+/** GET /:id with the id URL-encoded (Express decodes route params). */
+function getById(mods: Mods, id: string) {
+  return dispatch(mods, 'GET', `/${encodeURIComponent(id)}`);
+}
+
+/** A minimal spec-complete W3C VC item for the create-presentation payload. */
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
+const NOT_FOUND = { status: 404, code: 'NOT_FOUND', message: 'Presentation not found' };
+
+function expectNotFound(r: { status: number; body: any }) {
+  expect(r.status).toBe(NOT_FOUND.status);
+  expect(r.body?.error?.code).toBe(NOT_FOUND.code);
+  expect(r.body?.error?.message).toBe(NOT_FOUND.message);
+  expect(r.body?.presentation).toBeUndefined();
+}
+
+describe('KS-1120 F-1 — memory path (isDbAvailable() false): exact id or 404', () => {
+  // Pin the base so storedId's prefix is deterministic across runs.
+  const VC_BASE_URL = 'https://abc0.issuer1.example';
+  let mods: Mods;
+  let storedId: string;
+
+  beforeAll(async () => {
+    process.env.VC_BASE_URL = VC_BASE_URL;
+    dbMock.isDbAvailable.mockReturnValue(false);
+    dbMock.query.mockReset();
+    mods = await freshModules();
+    // Seed one real row through the real POST / (no holderDID → no signing gate).
+    const created = await dispatch(mods, 'POST', '/', { credentials: [baseCredential()] });
+    expect(created.status).toBe(201);
+    storedId = created.body.presentation.id;
+    expect(storedId).toMatch(new RegExp(`^${VC_BASE_URL.replace(/[.]/g, '\\.')}/presentations/[0-9a-f-]{36}$`));
+  });
+
+  it('🔴 KS-1120 F-1 — a PREFIX of the stored id answers 404 on the memory path', async () => {
+    // A proper prefix (not equal to the full id) must still answer 404. Under the tamper this goes RED.
+    const prefix = storedId.slice(0, storedId.length - 6);
+    expect(storedId.startsWith(prefix)).toBe(true);
+    expect(prefix).not.toBe(storedId);
+    expectNotFound(await getById(mods, prefix));
+  });
+
+  it('🔴 KS-1120 F-1 — a shorter prefix (the URL origin of the id) answers 404 too', async () => {
+    // The reference says the id shape is `${VC_BASE_URL}/presentations/<uuid>`; slice at '/presentations/'
+    // to get just `https://abc0.issuer1.example`. That origin is a true prefix and must also be 404.
+    const origin = storedId.slice(0, storedId.indexOf('/presentations/'));
+    expect(storedId.startsWith(origin)).toBe(true);
+    expect(origin).not.toBe(storedId);
+    expectNotFound(await getById(mods, origin));
+  });
+
+  it('KS-1120 control — the exact id answers 200 on the memory path', async () => {
+    // Green both at tip AND under the tamper: an exact match survives either lookup strategy.
+    const r = await getById(mods, storedId);
+    expect(r.status).toBe(200);
+    expect(r.body?.presentation?.id).toBe(storedId);
+  });
+});
```
