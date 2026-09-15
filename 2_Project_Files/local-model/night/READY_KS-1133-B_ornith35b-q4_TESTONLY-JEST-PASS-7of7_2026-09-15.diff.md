# READY — KS-1133 Part B (the v2 route cell: {contentHash:A, hash:B} → B — hash read FIRST; Kam's 2026-09-13 `accept-split` ruling, checklist item 3's v2 half) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE, TEST-ONLY mode (jest, services/originate), run `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-15_ks1133-ornith35b-night3`, 2026-09-15 23:46
# Source read by me (Wednesday): the four cells are the brief's byte-for-byte on the ks584 driver (four jest.mock blocks, the express app on a random port, verifyV2(body) through realFetch; mockQueryRaw → [] so the route answers 200/count 0 and ECHOES the hash it looked up as body.hash). A4 red 2/4 at the tip under the tamper (v1's chain planted at verificationV2.ts:446; controls green), A5 4/4 green, A6 no new red across services/originate, A7 tsc rc 0. No product change — the code is right at the tip; this is the PIN.
# PR NOTES for the Sunday raising seat: (1) v1's matching cell ALREADY EXISTS — ks1103-verify-hash-field.test.ts P1 ({contentHash:A, hash:B} → A) — cite it in the PR, do not duplicate it; (2) Part A (the two route DESCRIPTIONS in originate.openapi.ts + the registry-reading test) is a separate READY — bundle A+B as ONE PR for KS-1133 with the yaml regenerated (docs/openapi/secuura-api.yaml is generated from the .openapi.ts sources); (3) checklist item 4 (the VerifyRequest description at originate.openapi.ts:551 names an INCOMPLETE alias list — documentId, hash, title, contentHash) is left for the PR seat's judgement — touch it only if the sentence is touched, per the ticket.

```diff
--- /dev/null
+++ b/services/originate/src/__tests__/ks1133-v2-verify-hash-read-first.test.ts
@@ -0,0 +1,107 @@
+/**
+ * =============================================================================
+ * KS-1133 — v2 reads hash FIRST in the alias chain (the ruled split)
+ * =============================================================================
+ */
+
+process.env.NODE_ENV = 'development';
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
+
+const mockQueryRaw = jest.fn();
+const mockAuthenticateCalls: unknown[] = [];
+
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: mockQueryRaw },
+  getTenantManager: () => null,
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: (opts?: unknown) => {
+    mockAuthenticateCalls.push(opts);
+    return (_req: unknown, _res: unknown, next: () => void) => next();
+  },
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
+  updateDocument: jest.fn().mockResolvedValue(undefined),
+  MAX_LINEAGE_DEPTH: 10,
+}));
+
+import express from 'express';
+import { verificationV2Router } from '../routes/verificationV2';
+
+const HASH = 'f'.repeat(64);
+const OTHER = 'e'.repeat(64);
+
+const app = express();
+app.use(express.json());
+app.use('/api/v2/verification', verificationV2Router);
+
+let baseUrl = '';
+let server: ReturnType<typeof app.listen>;
+const realFetch = global.fetch;
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  const address = server.address();
+  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
+});
+
+afterAll(() => {
+  server?.close();
+  global.fetch = realFetch;
+});
+
+async function verifyV2(body: Record<string, unknown>, headers: Record<string, string> = {}): Promise<{ status: number; body: any }> {
+  const res = await realFetch(`${baseUrl}/api/v2/verification/verify`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json', ...headers },
+    body: JSON.stringify(body),
+  });
+  return { status: res.status, body: await res.json() };
+}
+
+beforeEach(() => {
+  jest.clearAllMocks();
+  global.fetch = jest.fn().mockRejectedValue(new Error('chain lookup disabled in test')) as unknown as typeof fetch;
+});
+
+describe('KS-1133 — v2 reads hash FIRST in the alias chain (the ruled split)', () => {
+  it('🔴 KS-1133 v2 {contentHash:A, hash:B} — the lookup sees B (hash is read first)', async () => {
+    mockQueryRaw.mockResolvedValue([]);
+    const { status, body } = await verifyV2({ contentHash: HASH, hash: OTHER });
+    expect(status).toBe(200);
+    expect(body.hash).toBe(`sha256:${OTHER}`);
+  });
+
+  it('🔴 KS-1133 v2 {providedHash:A, documentHash:A, hash:B} — hash still wins over every alias', async () => {
+    mockQueryRaw.mockResolvedValue([]);
+    const { status, body } = await verifyV2({ providedHash: HASH, documentHash: HASH, hash: OTHER });
+    expect(status).toBe(200);
+    expect(body.hash).toBe(`sha256:${OTHER}`);
+  });
+
+  it('KS-1133 control — {contentHash:A} alone is looked up as A on both chains', async () => {
+    mockQueryRaw.mockResolvedValue([]);
+    const { status, body } = await verifyV2({ contentHash: HASH });
+    expect(status).toBe(200);
+    expect(body.hash).toBe(`sha256:${HASH}`);
+  });
+
+  it('KS-1133 control — {hash:B} alone is looked up as B on both chains', async () => {
+    mockQueryRaw.mockResolvedValue([]);
+    const { status, body } = await verifyV2({ hash: OTHER });
+    expect(status).toBe(200);
+    expect(body.hash).toBe(`sha256:${OTHER}`);
+  });
+});
```
