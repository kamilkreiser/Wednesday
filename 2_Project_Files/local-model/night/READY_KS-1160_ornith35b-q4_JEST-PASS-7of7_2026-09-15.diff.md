# READY — KS-1160 (originate POST /api/webhooks persists and echoes the SSRF guard's NORMALISED url, as PATCH already did) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE, **jest** (services/originate), 2026-09-15 18:37 — tip develop M55 48e65c435. Run `2026-09-15_ks1160-ornith35b-night` (30 s, 1,594 tokens). 2 🔴 red at the tip (the INSERT bound the raw url; the 201 body echoed it) / control green (the guard consulted once with the raw input) / 3 green after / originate suite Δ 0 / tsc 0.
# Source read by me (Wednesday): two one-token edits exactly as briefed — :257 `${url}` → `${urlValidation.url}`, :262 `url` → `url: urlValidation.url`; :219 and the PATCH path untouched. The test is the ks444 driver with the shared mock's guard made to trim (the original returned the raw string, which is why the defect was invisible); it reads the 4th interpolated value of the tagged `$executeRaw` call. Peter's §6 finding on #720 — cite comment 5479494525 in the PR body.

```diff
--- a/services/originate/src/routes/webhooks.ts
+++ b/services/originate/src/routes/webhooks.ts
@@ -254,12 +254,12 @@ webhooksRouter.post('/', async (req: Request, res: Response) => {
     const tenantId = reqTenant && UUID_RE.test(reqTenant) ? reqTenant : DEFAULT_TENANT_ID;
     await runWithTenantId(tenantId, () => db.$executeRaw`
       INSERT INTO svc_webhooks (id, organization_id, tenant_id, url, secret_v2, events, description, is_active)
-      VALUES (${id}::uuid, ${userId}::uuid, ${tenantId}::uuid, ${url}, ${encrypted}, ${events}, ${description || null}, true)
+      VALUES (${id}::uuid, ${userId}::uuid, ${tenantId}::uuid, ${urlValidation.url}, ${encrypted}, ${events}, ${description || null}, true)
     `);
 
     res.status(201).json({
       success: true,
-      webhook: { id, url, events, description, isActive: true },
+      webhook: { id, url: urlValidation.url, events, description, isActive: true },
       secret,
       warning: 'Store the webhook secret securely — it is used to verify payload signatures and cannot be retrieved later.',
     });
--- /dev/null
+++ b/services/originate/src/__tests__/ks1160-webhooks-post-persists-normalised-url.test.ts
@@ -0,0 +1,109 @@
+/**
+ * KS-1160 — POST /api/webhooks persists the RAW url where PATCH persists the normalised one.
+ *
+ * The create handler consults validateWebhookUrl but then DISCARDS its .url: line 257 binds
+ * `${url}` into the INSERT and line 262 echoes raw `url`. Fix shape: persist and echo
+ * urlValidation.url on the POST path exactly as PATCH does. Harness mirrors ks444-webhooks-create-description-guard.test.ts with ONE change inside the @secuura/shared mock so assertSafeOutboundUrl NORMALISES.
+ */
+
+const mockExecuteRaw = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: {
+    $queryRaw: jest.fn(),
+    $executeRaw: mockExecuteRaw,
+    $executeRawUnsafe: jest.fn(),
+  },
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (req: any, _res: unknown, next: () => void) => {
+    req.user = { userId: '11111111-2222-4333-8444-555555555555' };
+    next();
+  },
+}));
+
+jest.mock('@secuura/shared', () =>
+  require('./helpers/sharedModuleMock').makeSharedMock({
+    encryptField: jest.fn(() => 'v1:mock-ciphertext'),
+    decryptField: jest.fn(() => ''),
+    runWithTenantId: jest.fn(async (_tenantId: unknown, fn: () => unknown) => fn()),
+    assertSafeOutboundUrl: jest.fn(async (raw: unknown) => ({ ok: true as const, url: String(raw).trim() })),
+  }),
+);
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
+}));
+
+import express from 'express';
+import { webhooksRouter } from '../routes/webhooks';
+
+const shared = jest.requireMock('@secuura/shared') as { assertSafeOutboundUrl: jest.Mock };
+
+const app = express();
+app.use('/api/webhooks', express.json(), webhooksRouter);
+
+let baseUrl = '';
+let server: ReturnType<typeof app.listen>;
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  const address = server.address();
+  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
+});
+
+afterAll(() => server?.close());
+beforeEach(() => {
+  mockExecuteRaw.mockReset();
+  shared.assertSafeOutboundUrl.mockClear();
+});
+
+function createWebhook(body: unknown): Promise<Response> {
+  return fetch(`${baseUrl}/api/webhooks`, {
+    method: 'POST',
+    headers: { 'content-type': 'application/json' },
+    body: JSON.stringify(body),
+  });
+}
+
+describe('KS-1160 POST /api/webhooks — URL normalisation persistence', () => {
+  it('🔴 KS-1160 — POST persists the guard\'s NORMALISED url, not the raw request string', async () => {
+    const RAW = '  https://partner.example.com/hooks  ';
+    const NORMALISED = 'https://partner.example.com/hooks';
+    mockExecuteRaw.mockResolvedValueOnce(1);
+    const res = await createWebhook({ url: RAW, events: ['certification.issued'] });
+    expect(res.status).toBe(201);
+    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
+    const boundUrl = mockExecuteRaw.mock.calls[0][4];
+    expect(boundUrl).toBe(NORMALISED);
+  });
+
+  it('🔴 KS-1160 — the 201 body echoes the normalised url', async () => {
+    const RAW = '  https://partner.example.com/hooks  ';
+    const NORMALISED = 'https://partner.example.com/hooks';
+    mockExecuteRaw.mockResolvedValueOnce(1);
+    const res = await createWebhook({ url: RAW, events: ['certification.issued'] });
+    expect(res.status).toBe(201);
+    const body = (await res.json()) as { webhook?: { url?: string } };
+    expect(body.webhook?.url).toBe(NORMALISED);
+  });
+
+  it('KS-1160 control — the guard is consulted once with the raw request url, before and after', async () => {
+    const RAW = '  https://partner.example.com/hooks  ';
+    mockExecuteRaw.mockResolvedValueOnce(1);
+    await createWebhook({ url: RAW, events: ['certification.issued'] });
+    expect(shared.assertSafeOutboundUrl).toHaveBeenCalledTimes(1);
+    expect(shared.assertSafeOutboundUrl).toHaveBeenCalledWith(RAW);
+  });
+});
```
