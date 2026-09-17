# READY — KS-928 (TEST-ONLY, jest, originate: a new test pins that POST seed-demo-users refuses 403 DEMO_SEED_DISABLED when isDemoSeedEnabled() is false — red under the tamper at routes/adminConfig.ts:1893, controls green) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE, strict, 2026-09-17 15:18
# Source read by Wednesday (scratchpad cmp_brief.py): the test file's 107 `+` lines IDENTICAL to the brief fence (a mutated copy unequal); one new file, no product change; A6 originate 637 -> 641 no new red; A7 tsc rc 0.
# PR NOTES: Closes/Refs per the gate (the ticket's ask is exactly this pin + red-proof; its attached PR #874 is merged). TIER 2 (test-only). Peter's comment on KS-928 asks to keep the 403 status + DEMO_SEED_DISABLED code — the test pins both. After READY_KS-730-B merges (+3 lines above the gate) the tamper line becomes :1896 — irrelevant to the raise, relevant to a rebuild. Not tested: the KS-502 system test on a live stack. Brief night/briefs/KS-928.md; report night/briefs/BRIEFS_2026-09-17k.REPORT.md.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks928-the-demo-seed-gate-s-predicate.test.ts
@@ -0,0 +1,107 @@
+/**
+ * KS-928: POST /api/admin/seed-demo-users must consult the demo-seed gate.
+ *
+ * The gate predicate has its own tests, but nothing observed that the route
+ * calls it, so removing the check left every originate suite green. This file
+ * mounts the real router and asserts the refusal, and the run when both flags
+ * are set.
+ */
+process.env.NODE_ENV = 'development';
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
+
+const mockQueryRaw = jest.fn();
+const mockExecuteRaw = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: mockQueryRaw, $executeRaw: mockExecuteRaw },
+  refreshTenantConfigs: jest.fn(),
+  withTenant: (_t: unknown, fn: () => unknown) => fn(),
+  getTenantManager: () => null,
+}));
+
+// authenticate is replaced by an ORG_ADMIN principal; requireRole stays real.
+jest.mock('../middleware/auth', () => {
+  const actual = jest.requireActual('../middleware/auth');
+  return {
+    ...actual,
+    authenticate: () => (req: any, _res: unknown, next: () => void) => {
+      const principal = { userId: 'u1', role: 'ORG_ADMIN', tenantId: 'a0000000-0000-4000-8000-0000000000aa' };
+      req._secuuraUser = principal;
+      req.user = principal;
+      next();
+    },
+  };
+});
+
+jest.mock('@secuura/shared', () =>
+  require('./helpers/sharedModuleMock').makeSharedMock({
+    runWithPlatformScope: (fn: () => unknown) => fn(),
+  }),
+);
+
+import express from 'express';
+import { adminConfigRouter } from '../routes/adminConfig';
+
+const FLAGS = ['ALLOW_DEFAULT_SEED_PASSWORDS', 'ENABLE_DEMO_SEED'];
+const EXPECTED_CELLS = 3;
+let CELLS_RUN = 0;
+
+const app = express();
+app.use(express.json());
+app.use('/api/admin', adminConfigRouter);
+
+let baseUrl = '';
+let server: ReturnType<typeof app.listen>;
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  const address = server.address();
+  baseUrl = 'http://127.0.0.1:' + (typeof address === 'object' && address ? address.port : 0);
+});
+
+afterAll(() => {
+  server?.close();
+});
+
+beforeEach(() => {
+  mockQueryRaw.mockReset();
+  mockExecuteRaw.mockReset();
+  mockQueryRaw.mockResolvedValue([]);
+  mockExecuteRaw.mockResolvedValue(0);
+  for (const flag of FLAGS) delete process.env[flag];
+});
+
+afterEach(() => {
+  for (const flag of FLAGS) delete process.env[flag];
+});
+
+async function seed(): Promise<{ status: number; body: any }> {
+  const res = await fetch(baseUrl + '/api/admin/seed-demo-users', { method: 'POST' });
+  return { status: res.status, body: await res.json() };
+}
+
+describe('KS-928 - POST /api/admin/seed-demo-users consults the demo-seed gate', () => {
+  it('KS-928 R1 - with neither flag set the route refuses 403 DEMO_SEED_DISABLED and touches no table', async () => {
+    CELLS_RUN += 1;
+    const { status, body } = await seed();
+    expect([status, body.error?.code, mockExecuteRaw.mock.calls.length, mockQueryRaw.mock.calls.length]).toEqual([403, 'DEMO_SEED_DISABLED', 0, 0]);
+  });
+  it('KS-928 R2 - with only ALLOW_DEFAULT_SEED_PASSWORDS set under NODE_ENV development the route still refuses', async () => {
+    CELLS_RUN += 1;
+    process.env.ALLOW_DEFAULT_SEED_PASSWORDS = 'true';
+    const { status, body } = await seed();
+    expect([status, body.error?.code, mockExecuteRaw.mock.calls.length]).toEqual([403, 'DEMO_SEED_DISABLED', 0]);
+  });
+  it('KS-928 CONTROL - with both flags true the route runs and counts all 14 accounts as already present', async () => {
+    CELLS_RUN += 1;
+    process.env.ALLOW_DEFAULT_SEED_PASSWORDS = 'true';
+    process.env.ENABLE_DEMO_SEED = 'true';
+    const { status, body } = await seed();
+    expect([status, body.success, body.created, body.alreadyPresent, body.failed, mockExecuteRaw.mock.calls.length]).toEqual([200, true, 0, 14, 0, 14]);
+  });
+  it('KS-928 COMPLETENESS - every graded cell above actually ran', () => {
+    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
+  });
+});
```
