# READY — KS-928-DEMOSEEDGATE-R15 (Ornith, briefed, test_only, new · jest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks928-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 01:15 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip — with an accommodation: --recount (miscounted header: hunk @@ -0,0 +1,97 @@ declared old=0 new=97 actual old=0 new=107 ); every line byte-exact`; the run's patch DIFFERS from the drafter's golden at `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_r15feed2-drafter-precheck/928DEMOSEEDGATE-R15/out.md.checker/patch.diff` (`cmp` rc 1) — read the diff before raising.

**Held 01:15 2026-09-22 by Wednesday 00:05 seat, drain sitting: expected_plus 107/107 in the diff; reds matched 2/2; golden DIFFERS (hunk-header form only; +/- body identical) after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks928-ornith35b-night/out.md.checker`, not typed).** Tip `581ed7fa124b85c7c2da89ac05d52f99c2502911`. Touches ONE file: `Blockchain/Dev/services/originate/src/__tests__/ks928-the-demo-seed-gate-s-predicate.test.ts` (new). `+` lines 107 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 4/4 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `DEMOSEEDGATE` → red exactly ['KS-928 R1 - with neither flag set the route refuses 403 DEMO', 'KS-928 R2 - with only ALLOW_DEFAULT_SEED_PASSWORDS set under']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks928-ornith35b-night/input.json`. Brief: `night/briefs/KS-928-DEMOSEEDGATE-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks928-ornith35b-night/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks928-the-demo-seed-gate-s-predicate.test.ts
@@ -0,0 +1,97 @@
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
