# READY — KS-1802-KS-1802-SEEDLOG (Spark (DeepSeek V4 Flash), briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1802_p1/out.md.checker/patch.diff`** (from `ls` at 19:08 2026-10-29; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1802_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1802_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 19:08 2026-10-29 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1802_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `e4cd2e1325bacbe1fd39e549f8aaefc943485d12`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/adminConfig.ts , Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
10	1	Blockchain/Dev/services/originate/src/routes/adminConfig.ts
127	0	Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (9 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 10 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/adminConfig.ts byte-exact incl. leading whitespace (apply mode strict): OK 9 line(s) byte-exact incl. leading whitespace (of 9; 10 line(s) added by the apply)` [a3i_indent.out: `OK 9 line(s) byte-exact incl. leading whitespace (of 9; 10 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts fails at the untouched tip (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-1802: seed-demo-users keeps going when a user insert throws a hostile value RED KS-1802 R1: every insert rejecting with a revoked Proxy is reported as 14 failed, not as the constant 500', 'KS-1802: seed-demo-users keeps going when a user insert throws a hostile value RED KS-1802 R2: every insert rejecting with a throwing message getter is reported as 14 failed, not as the constant 500', 'KS-1802: seed-demo-users keeps going when a user insert throws a hostile value RED KS-1802 R3: one hostile failure on the first user does not stop the other 13 from being seeded']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1745 failed=0 | after: total=1751 failed=0` · `NEW reds: []` [baseline_suite.json total=1745 failed=0; after_suite.json total=1751 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +137/-1 test=src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (+10/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts` (+127/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `e4cd2e1325bacbe1fd39e549f8aaefc943485d12` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1802_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1802_p1/KS-1802.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1802_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/adminConfig.ts b/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
--- a/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
+++ b/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
@@ -143,5 +143,14 @@
     return err?.message?.includes('does not exist') === true || err?.code === '42P01';
   } catch {
     return false;
+  }
+}
+
+/** KS-1802: the thrown value's message for a log line; the fixed fallback when the value cannot be read (a revoked Proxy, a `message` getter that throws). */
+function readableErrorMessage(err: any): string | undefined {
+  try {
+    return err?.message;
+  } catch {
+    return 'thrown value that could not be described';
   }
 }
@@ -2109,6 +2118,6 @@
         // DO NOTHING a conflict is no longer an exception, so anything reaching
         // here is a real failure and was being swallowed silently.
         failed++;
-        logger.error('Demo user seed failed', { email: u.email, error: err?.message });
+        logger.error('Demo user seed failed', { email: u.email, error: readableErrorMessage(err) });
       }
     }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts
@@ -0,0 +1,127 @@
+// KS-1802 (originate routes/adminConfig.ts, POST /seed-demo-users): the per-user catch counted the failure (failed++) and THEN logged `err?.message`. That read touches the thrown value, so a
+// revoked Proxy, or an object whose `message` getter throws, made the read throw from inside the catch: the loop stopped at the first such user, the rest of the seed was never attempted, and the
+// route answered the constant 500 instead of its normal report. The fix reads the message through a guarded helper. The database is mocked (the same mocks as the KS-1780 cells); both seed flags
+// are set, the route is driven over a real loopback listener, and every insert is made to reject with the hostile value.
+process.env.NODE_ENV = 'development';
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
+process.env.ALLOW_DEFAULT_SEED_PASSWORDS = 'true';
+process.env.ENABLE_DEMO_SEED = 'true';
+
+const mockQueryRaw = jest.fn();
+const mockExecuteRaw = jest.fn();
+const mockLogError = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: mockQueryRaw, $executeRaw: mockExecuteRaw },
+  refreshTenantConfigs: jest.fn(),
+  withTenant: (_t: unknown, fn: (tx: unknown) => unknown) => fn({ $queryRaw: mockQueryRaw, $executeRaw: mockExecuteRaw }),
+  getTenantManager: () => null,
+}));
+
+jest.mock('../middleware/auth', () => {
+  const actual = jest.requireActual('../middleware/auth');
+  return {
+    ...actual,
+    authenticate: () => (req: any, _res: unknown, next: () => void) => {
+      const principal = { id: 'u-ks1802', role: 'SYSTEM_ADMIN', tenantId: 't-ks1802' };
+      req._secuuraUser = principal; req.user = principal; req.tenantId = principal.tenantId;
+      next();
+    },
+    requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  };
+});
+
+jest.mock('@secuura/shared', () =>
+  require('./helpers/sharedModuleMock').makeSharedMock({
+    ...(jest.requireActual('@secuura/shared') as Record<string, unknown>),
+    runWithPlatformScope: (fn: () => unknown) => fn(),
+    queryWithTenantGuc: jest.fn(),
+  }),
+);
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: mockLogError, debug: jest.fn() },
+}));
+
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { adminConfigRouter } from '../routes/adminConfig';
+
+const USERS = 14;
+const app = express();
+app.use('/api/admin', express.json(), adminConfigRouter);
+let server: ReturnType<typeof app.listen>;
+let baseUrl = '';
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+afterAll(() => {
+  (server as unknown as { closeAllConnections?: () => void })?.closeAllConnections?.();
+  server?.close();
+});
+beforeEach(() => {
+  mockQueryRaw.mockReset();
+  mockExecuteRaw.mockReset();
+  mockLogError.mockReset();
+  mockQueryRaw.mockResolvedValue([]);
+});
+
+async function seed(): Promise<{ status: number | 'NO ANSWER'; body: unknown }> {
+  try {
+    const res = await fetch(baseUrl + '/api/admin/seed-demo-users', { method: 'POST', signal: AbortSignal.timeout(3000) });
+    return { status: res.status, body: await res.json() };
+  } catch {
+    return { status: 'NO ANSWER', body: null };
+  }
+}
+
+function revokedProxy(): object {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+}
+
+function throwingMessageGetter(): object {
+  return {
+    get message(): string {
+      throw new Error('ks1802 getter');
+    },
+  };
+}
+
+describe('KS-1802: seed-demo-users keeps going when a user insert throws a hostile value', () => {
+  it('RED KS-1802 R1: every insert rejecting with a revoked Proxy is reported as 14 failed, not as the constant 500', async () => {
+    mockExecuteRaw.mockRejectedValue(revokedProxy());
+    expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 0, created: 0, alreadyPresent: 0, failed: USERS } });
+  });
+
+  it('RED KS-1802 R2: every insert rejecting with a throwing message getter is reported as 14 failed, not as the constant 500', async () => {
+    mockExecuteRaw.mockRejectedValue(throwingMessageGetter());
+    expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 0, created: 0, alreadyPresent: 0, failed: USERS } });
+  });
+
+  it('RED KS-1802 R3: one hostile failure on the first user does not stop the other 13 from being seeded', async () => {
+    mockExecuteRaw.mockRejectedValueOnce(revokedProxy()).mockResolvedValue(1);
+    expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 13, created: 13, alreadyPresent: 0, failed: 1 } });
+  });
+
+  it('control KS-1802 C1: an ordinary Error on every insert is reported as 14 failed and its message is logged', async () => {
+    mockExecuteRaw.mockRejectedValue(new Error('ks1802 ordinary'));
+    expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 0, created: 0, alreadyPresent: 0, failed: USERS } });
+    expect(mockLogError).toHaveBeenCalledWith('Demo user seed failed', { email: 'james.wilson@ox.ac.uk', error: 'ks1802 ordinary' });
+  });
+
+  it('control KS-1802 C2: every insert creating a row is reported as 14 created', async () => {
+    mockExecuteRaw.mockResolvedValue(1);
+    expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: USERS, created: USERS, alreadyPresent: 0, failed: 0 } });
+  });
+
+  it('control KS-1802 C3: every insert hitting a conflict is reported as 14 already present', async () => {
+    mockExecuteRaw.mockResolvedValue(0);
+    expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 0, created: 0, alreadyPresent: USERS, failed: 0 } });
+  });
+});
```
