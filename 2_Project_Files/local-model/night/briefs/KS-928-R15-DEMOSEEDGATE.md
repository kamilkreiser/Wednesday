# KS-928 R15-DEMOSEEDGATE - re-brief of the held READY at develop 9f0265eb0 (written 20:35 on 2026-09-21 by Wednesday's census15 drafter from the file at the tip - 0 lines read whole)
File: `Blockchain/Dev/services/originate/src/__tests__/ks928-the-demo-seed-gate-s-predicate.test.ts`
Tip: `9f0265eb06ecf24d4de18149ce862ad2330a61ee`
Runner: `jest`

## Premises (measured by the census15 drafter at 20:35:38 AEST, in a `--shared` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-928_ornith35b-q4_TESTONLY-JEST-DEMOSEEDGATE-PASS-7of7_2026-09-17.diff.md` (its checker PASS was at an OLDER tip; run dir GONE/unnamed - the READY fence is the patch); canonical patch 4170 B sha256[:16] `23e6bf038cdd84c0`, +107/-0.
- The old patch at the tip: strict rc 0 / --recount rc 0 / --directory=Blockchain/Dev rc 0 / -R rc 1 -> effective mode **strict**; the old READY's + lines PRESENT at the tip: NO (content absent - un-merged).
- The test file `Blockchain/Dev/services/originate/src/__tests__/ks928-the-demo-seed-gate-s-predicate.test.ts` at the tip: ABSENT - ONE NEW FILE. Mode: **NEW**.
- Tamper source: the old brief `night/briefs/KS-928.md` (its `## Tamper` line/from/to, converted to the current `### ID` shape). Each From located at the tip by exact whole-line match (count in the Tampers section).
- Ticket KS-928: Backlog, assignee kamil.kreiser@secuura.ai, PR attachments #874 (all merged); briefs already on disk: KS-928.md.
- Generator notes: reds INFERRED as every non-CONTROL/COMPLETENESS cell (2) - no RED-prefixed title in the old patch; Wednesday confirms the set against the old READY header.

## What is wrong (one paragraph)
The held READY's own summary, verbatim from its header (the model wrote these cells once and the checker passed them on the date in the file name; the run is re-done at the CURRENT tip so the checker verdicts it fresh):
> # READY — KS-928 (TEST-ONLY, jest, originate: a new test pins that POST seed-demo-users refuses 403 DEMO_SEED_DISABLED when isDemoSeedEnabled() is false — red under the tamper at routes/adminConfig.ts:1893, controls green) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE, strict, 2026-09-17 15:18
> # Source read by Wednesday (scratchpad cmp_brief.py): the test file's 107 `+` lines IDENTICAL to the brief fence (a mutated copy unequal); one new file, no product change; A6 originate 637 -> 641 no new red; A7 tsc rc 0.
> # PR NOTES: Closes/Refs per the gate (the ticket's ask is exactly this pin + red-proof; its attached PR #874 is merged). TIER 2 (test-only). Peter's comment on KS-928 asks to keep the 403 status + DEMO_SEED_DISABLED code — the test pins both. After READY_KS-730-B merges (+3 lines above the gate) the tamper line becomes :1896 — irrelevant to the raise, relevant to a rebuild. Not tested: the KS-502 system test on a live stack. Brief night/briefs/KS-928.md; report night/briefs/BRIEFS_2026-09-17k.REPORT.md.
This task asks for the SAME cells, re-derived at develop `9f0265eb0`. Nothing in the product changes. The old diff still applies at the tip in mode strict - emit the same cells, anchored on the lines quoted below.

## THE MODE - read this twice
TEST-ONLY, ONE NEW FILE: your diff contains EXACTLY ONE file, the NEW test file above: `--- /dev/null` then `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks928-the-demo-seed-gate-s-predicate.test.ts` then ONE `@@ -0,0 +1,N @@` hunk, every line `+`, no context, no `-`. No product hunk. This service runs JEST (ts-jest): `jest` names only, never `vi`.

## The exact change
```
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

## Cells (every cell RED or CONTROL; the names below are the EXACT it() titles)
- `KS-928 R1 - with neither flag set the route refuses 403 DEMO_SEED_DISABLED and touches no table`
- `KS-928 R2 - with only ALLOW_DEFAULT_SEED_PASSWORDS set under NODE_ENV development the route still refuses`
- `KS-928 CONTROL - with both flags true the route runs and counts all 14 accounts as already present`  (CONTROL - green on both trees)

## Tampers
### DEMOSEEDGATE
File: `Blockchain/Dev/services/originate/src/routes/adminConfig.ts`
Line: 1897
From:
```
    if (!isDemoSeedEnabled()) {
```
To:
```
    if (false && !isDemoSeedEnabled()) { // TAMPER: KS-928 red-proof, the route no longer consults the gate
```
Reds: `KS-928 R1 - with neither flag set the route refuses 403 DEMO_SEED_DISABLED and touches no table`, `KS-928 R2 - with only ALLOW_DEFAULT_SEED_PASSWORDS set under NODE_ENV development the route still refuses`
(From located at the tip: 1 match(es); the old brief/input said line 1893)

## Controls
- `KS-928 CONTROL - with both flags true the route runs and counts all 14 accounts as already present`

## Output
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/originate/src/__tests__/ks928-the-demo-seed-gate-s-predicate.test.ts`); correct hunk counts; no `\$` / `\u` / backslash escapes in a `+` line; the cell titles EXACTLY as listed (the checker matches the full title).
