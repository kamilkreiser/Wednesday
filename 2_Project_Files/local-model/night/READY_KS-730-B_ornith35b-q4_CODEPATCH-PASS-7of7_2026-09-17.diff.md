# READY — KS-730 PART B (originate `routes/adminConfig.ts` :187/:219/:231, POST/PUT/DELETE /document-types catches → `logger.error` + constant 500 text) + NEW test ks730-adminconfig-document-types-500-body.test.ts — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE (05:55). Held by Wednesday at 06:01 AEST.
# Source read by me (Wednesday): model product +6/-3 in 2 hunks and the 131-line test IDENTICAL in sequence to the brief's fences (python compare; a mutated copy unequal). Apply STRICT. A4 4 red / 6 run by assertion, controls green; A6 NEW reds []; A7 tsc rc 0.
# A LIVE LEAK OFF PRODUCTION (read, not driven against a database): a malformed id's PostgreSQL error text reaches the 500 body; the demo runs NODE_ENV=development (KS-658).
# NOT GRADED BY THE CHECKER: the 43 identical catches elsewhere in the file (A3e by text); the product section is exactly the two named hunks (read).
# PR NOTES: "Refs KS-730 (part B)". Tier 1 at raise. Independent of part A (different files); KS-730 stays open.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
+++ b/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
@@ -184,7 +184,8 @@ adminConfigRouter.post('/document-types', async (req: Request, res: Response) =>
     if (err?.message?.includes('unique constraint')) {
       return res.status(409).json({ success: false, error: { code: 'CONFLICT', message: 'Document type code already exists' } });
     }
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message } });
+    logger.error('Document type create failed', { error: err instanceof Error ? err.message : String(err) });
+    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
   }
 });
 
@@ -216,19 +217,21 @@ adminConfigRouter.put('/document-types/:id', async (req: Request, res: Response)
     `;
     res.json({ success: result > 0, message: result > 0 ? 'Updated' : 'Not found' });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message } });
+    logger.error('Document type update failed', { error: err instanceof Error ? err.message : String(err) });
+    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
   }
 });
 
 /** Delete a document type */
 adminConfigRouter.delete('/document-types/:id', async (req: Request, res: Response) => {
   try {
     const result = await ((req as any).db || prisma).$executeRaw`
       DELETE FROM document_type_configs WHERE id = ${req.params.id}::uuid
     `;
     res.json({ success: result > 0, message: result > 0 ? 'Deleted' : 'Not found' });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message } });
+    logger.error('Document type delete failed', { error: err instanceof Error ? err.message : String(err) });
+    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
   }
 });
 
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks730-adminconfig-document-types-500-body.test.ts
@@ -0,0 +1,131 @@
+// KS-730 (part B: originate routes/adminConfig.ts, the three document-type write routes). A database error must never
+// reach the 500 body in any NODE_ENV (the KS-727 doctrine), and its message must be logged instead of being lost.
+const mockQueryRaw = jest.fn();
+const mockExecuteRaw = jest.fn();
+const mockLoggerError = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: mockQueryRaw, $executeRaw: mockExecuteRaw },
+  refreshTenantConfigs: jest.fn(),
+  withTenant: (_tenant: unknown, fn: () => unknown) => fn(),
+  getTenantManager: () => null,
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: mockLoggerError, debug: jest.fn() },
+}));
+
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { adminConfigRouter } from '../routes/adminConfig';
+
+const LEAK = 'invalid input syntax for type uuid: ks730-private-detail';
+const NODE_ENVS = ['development', 'demo', 'test', undefined];
+const CREATE_BODY = { name: 'KS-730 type', code: 'ks730-type', approvalWorkflowId: 'ks730-not-a-uuid' };
+const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
+const ORIGINAL_NODE_ENV = process.env.NODE_ENV;
+
+const app = express();
+app.use(express.json());
+app.use('/api/admin', adminConfigRouter);
+let server: ReturnType<typeof app.listen>;
+let baseUrl = '';
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  baseUrl = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
+});
+afterAll(() => server?.close());
+beforeEach(() => {
+  mockQueryRaw.mockReset();
+  mockExecuteRaw.mockReset();
+  mockLoggerError.mockReset();
+});
+afterEach(() => setNodeEnv(ORIGINAL_NODE_ENV));
+
+function setNodeEnv(value: string | undefined): void {
+  if (value === undefined) delete process.env.NODE_ENV;
+  else process.env.NODE_ENV = value;
+}
+
+async function call(method: string, path: string, body: object | undefined, nodeEnv: string | undefined): Promise<{ status: number; text: string }> {
+  setNodeEnv(nodeEnv);
+  const res = await fetch(`${baseUrl}/api/admin${path}`, {
+    method,
+    headers: { 'content-type': 'application/json' },
+    body: body === undefined ? undefined : JSON.stringify(body),
+  });
+  return { status: res.status, text: await res.text() };
+}
+
+describe('KS-730 part B — the document-type write routes never answer a 500 with err.message', () => {
+  it('🔴 KS-730 B1 — POST /document-types: the database error is not in the 500 body under development, demo, test or unset', async () => {
+    for (const nodeEnv of NODE_ENVS) {
+      mockQueryRaw.mockRejectedValueOnce(new Error(LEAK));
+      const reply = await call('POST', '/document-types', CREATE_BODY, nodeEnv);
+      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
+      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
+    }
+  });
+
+  it('🔴 KS-730 B2 — PUT /document-types/:id: the database error is not in the 500 body under development, demo, test or unset', async () => {
+    for (const nodeEnv of NODE_ENVS) {
+      mockExecuteRaw.mockRejectedValueOnce(new Error(LEAK));
+      const reply = await call('PUT', '/document-types/ks730-not-a-uuid', { name: 'renamed' }, nodeEnv);
+      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
+      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
+    }
+  });
+
+  it('🔴 KS-730 B3 — DELETE /document-types/:id: the database error is not in the 500 body under development, demo, test or unset', async () => {
+    for (const nodeEnv of NODE_ENVS) {
+      mockExecuteRaw.mockRejectedValueOnce(new Error(LEAK));
+      const reply = await call('DELETE', '/document-types/ks730-not-a-uuid', undefined, nodeEnv);
+      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
+      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
+    }
+  });
+
+  it('🔴 KS-730 B4 — each of the three routes logs the database error once, server-side, with its own message', async () => {
+    mockQueryRaw.mockRejectedValueOnce(new Error(LEAK));
+    mockExecuteRaw.mockRejectedValueOnce(new Error(LEAK)).mockRejectedValueOnce(new Error(LEAK));
+    await call('POST', '/document-types', CREATE_BODY, 'development');
+    await call('PUT', '/document-types/ks730-not-a-uuid', { name: 'renamed' }, 'development');
+    await call('DELETE', '/document-types/ks730-not-a-uuid', undefined, 'development');
+    expect(mockLoggerError.mock.calls).toEqual([
+      ['Document type create failed', { error: LEAK }],
+      ['Document type update failed', { error: LEAK }],
+      ['Document type delete failed', { error: LEAK }],
+    ]);
+  });
+
+  it('🟢 KS-730 control — under production the three routes already answer the constant text, and the database mock was reached', async () => {
+    mockQueryRaw.mockRejectedValueOnce(new Error(LEAK));
+    mockExecuteRaw.mockRejectedValueOnce(new Error(LEAK)).mockRejectedValueOnce(new Error(LEAK));
+    const created = await call('POST', '/document-types', CREATE_BODY, 'production');
+    const updated = await call('PUT', '/document-types/ks730-not-a-uuid', { name: 'renamed' }, 'production');
+    const deleted = await call('DELETE', '/document-types/ks730-not-a-uuid', undefined, 'production');
+    expect([created.status, updated.status, deleted.status]).toEqual([500, 500, 500]);
+    expect([created.text, updated.text, deleted.text].map((text) => JSON.parse(text))).toEqual([CONSTANT_BODY, CONSTANT_BODY, CONSTANT_BODY]);
+    expect([mockQueryRaw.mock.calls.length, mockExecuteRaw.mock.calls.length]).toEqual([1, 2]);
+  });
+
+  it('🟢 KS-730 control — authored 400 and 409 messages survive, a successful delete answers 200, and nothing is logged', async () => {
+    const refused = await call('POST', '/document-types', { name: 'no code' }, 'development');
+    expect([refused.status, JSON.parse(refused.text).error.message]).toEqual([400, 'name and code are required']);
+    mockQueryRaw.mockRejectedValueOnce(new Error('duplicate key value violates unique constraint document_type_configs_code_key'));
+    const conflict = await call('POST', '/document-types', CREATE_BODY, 'development');
+    expect([conflict.status, JSON.parse(conflict.text).error.message]).toEqual([409, 'Document type code already exists']);
+    mockExecuteRaw.mockResolvedValueOnce(1);
+    const deleted = await call('DELETE', '/document-types/ks730-not-a-uuid', undefined, 'development');
+    expect([deleted.status, JSON.parse(deleted.text)]).toEqual([200, { success: true, message: 'Deleted' }]);
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+});
```
