# READY — KS-1118 (F-2 pin only: {documentHash:A, hash:B} — the lookup sees A) — Ornith ornith:35b (Q4_K_M) PASS 7/7, TEST-ONLY mode, **the FIRST JEST ticket** (services/originate, ts-jest), 2026-09-15 18:30 — tip develop M55 48e65c435. Run `2026-09-15_ks1118-ornith35b-night2` (40 s, 1,775 tokens; taken by the 15-minute loop job on its own). Tamper :742 (hash read THIRD — the gate's T5): 2 🔴 red under it / control green / 3 green at the tip / originate suite 637 → 637 Δ 0 / tsc 0. The first sample (18:25) failed to COMPILE: my brief told the model to copy three constants it would not use and ts-jest's `noUnusedLocals` refused the file (TS6133) — brief + task rule fixed, and RETRY-ONCE now covers load errors with the compiler's lines. F-3 (the comment reword) is not in this diff — the raising seat may do it in the same PR.
# Source read by me (Wednesday): the three cells are the brief's exactly, through the ks1103 driver (four jest.mock blocks, the express app on a random port, verify(body, rows) reading the mocked queryRaw's parameters); no vitest idiom in the file (grep for `vi.` = 0). The product file is untouched.

```diff
--- /dev/null
+++ b/services/originate/src/__tests__/ks1118-verify-documenthash-over-hash.test.ts
@@ -0,0 +1,131 @@
+/**
+ * =============================================================================
+ * KS-1118 F-2 — documentHash over hash precedence pin
+ * =============================================================================
+ * The handler resolves `hashToVerify` through an alias chain. This task pins
+ * that `{documentHash: A, hash: B}` body answers exactly as `{documentHash: A}`
+ * alone does — i.e. the lookup sees A only and never falls through to B.
+ *
+ * Harness mirrors ks1103's shape so the same mock surface drives both tickets.
+ * =============================================================================
+ */
+
+process.env.NODE_ENV = 'development';
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
+
+const mockQueryRaw = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: mockQueryRaw },
+  getTenantManager: () => null,
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+}));
+
+jest.mock('@secuura/shared', () =>
+  require('./helpers/sharedModuleMock').makeSharedMock({
+    runWithTenantId: (_t: unknown, fn: () => unknown) => fn(),
+    queryWithTenantGuc: jest.fn(),
+  }),
+);
+
+jest.mock('../repositories/documentRepo', () => ({
+  walkAncestors: jest.fn().mockResolvedValue({ lineage: [], truncated: false }),
+  walkDescendants: jest.fn().mockResolvedValue({ descendants: [], truncated: false }),
+  MAX_LINEAGE_DEPTH: 10,
+}));
+
+import express from 'express';
+import { verificationRouter } from '../routes/verification';
+
+const HASH = 'f'.repeat(64);
+const OTHER = 'e'.repeat(64);
+const REAL_TX = '84fe214bd00257443c81e240a074763d476f9096b7e3525065bad06ec51c38c3';
+const DOC_ID = 'doc-1754000000000-original';
+
+function anchoredRow(): Record<string, unknown> {
+  return {
+    id: '11111111-1111-1111-1111-111111111111',
+    external_id: DOC_ID,
+    title: 'Grad cert',
+    document_type: 'DOCUMENT',
+    content_hash: HASH,
+    status: 'anchored',
+    certification_metadata: { blockchain: { txHash: REAL_TX, status: 'confirmed', blockHeight: 4547897 } },
+    metadata: {},
+    created_at: '2026-08-01T00:00:00.000Z',
+    certified_at: null,
+    organization_name: 'Acme Ltd',
+  };
+}
+
+const app = express();
+app.use(express.json());
+app.use('/api/verification', verificationRouter);
+
+let baseUrl = '';
+let server: ReturnType<typeof app.listen> | undefined;
+const realFetch = global.fetch;
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  const address = server?.address();
+  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
+});
+
+afterAll(() => {
+  if (server) server.close();
+  global.fetch = realFetch;
+});
+
+beforeEach(() => {
+  mockQueryRaw.mockReset();
+  global.fetch = jest.fn().mockRejectedValue(new Error('chain lookup disabled in test')) as unknown as typeof fetch;
+});
+
+interface Answer {
+  status: number;
+  json: Record<string, unknown>;
+  lookups: number;
+  sawHASH: boolean;
+  sawOTHER: boolean;
+}
+
+async function verify(body: unknown, rows: 'none' | 'anchored'): Promise<Answer> {
+  mockQueryRaw.mockReset();
+  mockQueryRaw.mockResolvedValue(rows === 'anchored' ? [anchoredRow()] : []);
+  const res = await realFetch(`${baseUrl}/api/verification/verify`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json' },
+    body: JSON.stringify(body),
+  });
+  const json = (await res.json()) as Record<string, unknown>;
+  const values = mockQueryRaw.mock.calls.flatMap((c: unknown[]) => c.slice(1)).map((v: unknown) => String(v));
+  return {
+    status: res.status,
+    json,
+    lookups: mockQueryRaw.mock.calls.length,
+    sawHASH: values.some((v) => v.includes(HASH)),
+    sawOTHER: values.some((v) => v.includes(OTHER)),
+  };
+}
+
+function compared(a: Answer) {
+  return {
+    status: a.status,
+    verified: a.json.verified,
+    checks: a.json.checks,
+    documentId: a.json.documentId,
+    error: a.json.error,
+  };
+}
+
+describe('KS-1118 F-2 — documentHash over hash precedence pin', () => {
+  it('🔴 KS-1118 F-2 {documentHash:A, hash:B} — the lookup sees A only (hash is read last)', async () => {
+    const p = await verify({ documentHash: HASH, hash: OTHER }, 'none');
+    expect(p.status).toBe(200);
+    expect(p.lookups).toBe(1);
+    expect(p.sawHASH).toBe(true);
+    expect(p.sawOTHER).toBe(false);
+  });
+
+  it('🔴 KS-1118 F-2 {documentHash:A, hash:B} answers exactly as {documentHash:A} alone', async () => {
+    const a = await verify({ documentHash: HASH, hash: OTHER }, 'none');
+    const b = await verify({ documentHash: HASH }, 'none');
+    expect(compared(a)).toEqual(compared(b));
+    expect(a.sawOTHER).toBe(false);
+  });
+
+  it('KS-1118 control — {contentHash:A, hash:B} still sees A only (P1, unchanged by the tamper)', async () => {
+    const c = await verify({ contentHash: HASH, hash: OTHER }, 'none');
+    expect(c.status).toBe(200);
+    expect(c.sawHASH).toBe(true);
+    expect(c.sawOTHER).toBe(false);
+  });
+});
```
