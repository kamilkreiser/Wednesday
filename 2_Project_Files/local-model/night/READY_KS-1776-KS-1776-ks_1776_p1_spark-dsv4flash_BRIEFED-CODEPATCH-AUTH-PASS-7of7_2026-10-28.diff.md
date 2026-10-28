# READY — KS-1776-KS-1776-ks_1776_p1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1776_p1/out.md.checker/patch.diff`** (from `ls` at 13:50 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1776_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1776_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1776_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1776_p1-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 13:50 2026-10-28 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1776_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8894c7486f82f6eb682fecb879791f53312537b1`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/auth/src/routes/auth.ts , Blockchain/Dev/services/auth/src/__tests__/ks1776-demo-user-seed-timer-cannot-escape-as-an-uncaught-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/routes/auth.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1776-demo-user-seed-timer-cannot-escape-as-an-uncaught-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
10	3	Blockchain/Dev/services/auth/src/routes/auth.ts
102	0	Blockchain/Dev/services/auth/src/__tests__/ks1776-demo-user-seed-timer-cannot-escape-as-an-uncaught-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (10 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 10 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 3.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/auth/src/routes/auth.ts byte-exact incl. leading whitespace (apply mode strict): OK 10 line(s) byte-exact incl. leading whitespace (of 10; 10 line(s) added by the apply)` [a3i_indent.out: `OK 10 line(s) byte-exact incl. leading whitespace (of 10; 10 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/routes/auth.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1776-demo-user-seed-timer-cannot-escape-as-an-uncaught-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1776-demo-user-seed-timer-cannot-escape-as-an-uncaught-throw.test.ts fails at the untouched tip (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1776: the demo-user seed timer cannot escape as an uncaught throw RED KS-1776 D1 firing the seed timer does not throw when the repository has no seedDemoUsers', 'KS-1776: the demo-user seed timer cannot escape as an uncaught throw RED KS-1776 D2 the missing seedDemoUsers is logged as Failed to seed demo users instead']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1776-demo-user-seed-timer-cannot-escape-as-an-uncaught-throw.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1200 failed=2 | after: total=1204 failed=1` · `NEW reds: []` [baseline_suite.json total=1200 failed=2; after_suite.json total=1204 failed=1]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +112/-3 test=src/__tests__/ks1776-demo-user-seed-timer-cannot-escape-as-an-uncaught-throw.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/routes/auth.ts` (+10/-3 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1776-demo-user-seed-timer-cannot-escape-as-an-uncaught-throw.test.ts` (+102/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8894c7486f82f6eb682fecb879791f53312537b1` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1776_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1776_p1/KS-1776.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1776_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/routes/auth.ts b/Blockchain/Dev/services/auth/src/routes/auth.ts
--- a/Blockchain/Dev/services/auth/src/routes/auth.ts
+++ b/Blockchain/Dev/services/auth/src/routes/auth.ts
@@ -59,8 +59,15 @@
 // =============================================================================
 // SEED DEMO USERS — runs once at startup via the repository
 // =============================================================================
+// KS-1776: seedDemoUsers is started from a timer, outside any request. A synchronous throw from it (a repository mock that lacks the export, a repository that is not ready) never reached the
+// .catch below, so it escaped the timer as an uncaught exception that the test runner pinned on whichever test was running. Both the throw and the rejection now go to the same log line.
+const logSeedFailure = (err: unknown): void => {
+  logger.error('Failed to seed demo users', { error: err });
+};
 setTimeout(() => {
-  userRepo.seedDemoUsers(hashPassword).catch((err) =>
-    logger.error('Failed to seed demo users', { error: err }),
-  );
+  try {
+    userRepo.seedDemoUsers(hashPassword).catch(logSeedFailure);
+  } catch (err) {
+    logSeedFailure(err);
+  }
 }, 2000);
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1776-demo-user-seed-timer-cannot-escape-as-an-uncaught-throw.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1776-demo-user-seed-timer-cannot-escape-as-an-uncaught-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1776-demo-user-seed-timer-cannot-escape-as-an-uncaught-throw.test.ts
@@ -0,0 +1,102 @@
+// KS-1776 (services/auth routes/auth.ts): importing the routes module arms a module-scope `setTimeout(..., 2000)` that calls `userRepo.seedDemoUsers(hashPassword).catch(...)`. When the
+// repository mock of a test has no `seedDemoUsers` export, vitest's mock THROWS on that property read, synchronously, inside the timer callback: the `.catch` is never reached and the
+// error escapes as an uncaught exception that vitest pins on whichever test is running (seen once, in ks781-login-authorize-agree, in a loaded run). Here the timer is driven with FAKE
+// timers so the escape is an assertion: D1 reads whether firing the timer throws, D2 reads whether the failure is logged instead. C1 and C2 pin what must not change.
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+
+const silent = { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() };
+vi.mock('../utils/logger', () => ({ logger: silent, createLogger: () => silent, validateEnv: vi.fn() }));
+vi.mock('@secuura/shared/utils/logger', () => ({ logger: silent, createLogger: () => silent }));
+
+const USER_REPO_BASE = {
+  getUserById: vi.fn(async () => null),
+  getUserByIdPreAuth: vi.fn(async () => null),
+  getUserByEmail: vi.fn(async () => null),
+  updateUser: vi.fn(async () => undefined),
+  getPlatformAdmin: vi.fn(async () => null),
+  updatePlatformAdminPassword: vi.fn(async () => undefined),
+  reencryptMfaSecretIfLegacy: vi.fn(async () => undefined),
+  reencryptPlatformAdminMfaSecretIfLegacy: vi.fn(async () => undefined),
+};
+
+vi.mock('../db', () => ({ query: vi.fn(async () => ({ rows: [], rowCount: 0 })) }));
+vi.mock('../repositories/userRepo', () => ({ ...USER_REPO_BASE }));
+vi.mock('../services/session', () => ({
+  createSession: vi.fn(async () => ({ id: 'sess-new' })),
+  getSession: vi.fn(async () => null),
+  rotateSessionRefreshToken: vi.fn(async () => undefined),
+  revokeSession: vi.fn(async () => undefined),
+  getRedisClient: vi.fn(() => null),
+  validateSession: vi.fn(async () => true),
+  updateSessionActivity: vi.fn(async () => undefined),
+}));
+vi.mock('../services/refreshDenylist', () => ({
+  isRefreshJtiDenylisted: vi.fn(async () => false),
+  denylistRefreshJti: vi.fn(async () => undefined),
+}));
+vi.mock('../services/accountLockout', () => ({
+  isLockedOut: vi.fn(async () => false), recordFailure: vi.fn(async () => 1),
+  recordSuccess: vi.fn(async () => undefined), clearFailures: vi.fn(async () => undefined),
+}));
+vi.mock('../services/password', () => ({
+  verifyPassword: vi.fn(async () => false), hashPassword: vi.fn(async () => '$argon2id$stub'),
+  checkPasswordStrength: vi.fn(() => ({ ok: true })), generateResetToken: vi.fn(() => 'tok'), shouldRehashAfterVerify: vi.fn(() => false),
+}));
+vi.mock('../services/email', () => ({ sendVerificationEmail: vi.fn(async () => undefined), sendPasswordResetEmail: vi.fn(async () => undefined) }));
+vi.mock('../events', () => ({ publishEvent: vi.fn(async () => undefined), EventTypes: {} }));
+
+function advance(ms: number): string {
+  try {
+    vi.advanceTimersByTime(ms);
+    return 'ok';
+  } catch (err) {
+    return 'THREW ' + (err instanceof Error ? err.message : String(err));
+  }
+}
+
+beforeAll(() => {
+  vi.useFakeTimers();
+});
+afterAll(() => {
+  vi.useRealTimers();
+});
+
+describe('KS-1776: the demo-user seed timer cannot escape as an uncaught throw', () => {
+  it('RED KS-1776 D1 firing the seed timer does not throw when the repository has no seedDemoUsers', async () => {
+    vi.resetModules();
+    silent.error.mockClear();
+    await import('../routes/auth');
+    expect(advance(2500)).toBe('ok');
+  });
+
+  it('RED KS-1776 D2 the missing seedDemoUsers is logged as Failed to seed demo users instead', async () => {
+    vi.resetModules();
+    silent.error.mockClear();
+    await import('../routes/auth');
+    advance(2500);
+    expect(silent.error.mock.calls.map((call) => call[0])).toEqual(['Failed to seed demo users']);
+  });
+
+  it('control KS-1776 C1 with seedDemoUsers present it is called once, with the password hasher, after 2000 ms and not before', async () => {
+    vi.resetModules();
+    const seed = vi.fn(async () => undefined);
+    vi.doMock('../repositories/userRepo', () => ({ ...USER_REPO_BASE, seedDemoUsers: seed }));
+    await import('../routes/auth');
+    advance(1999);
+    expect(seed).not.toHaveBeenCalled();
+    advance(1);
+    expect(seed).toHaveBeenCalledTimes(1);
+    expect(typeof (seed.mock.calls[0] as unknown[])[0]).toBe('function');
+  });
+
+  it('control KS-1776 C2 a seedDemoUsers that rejects is logged as Failed to seed demo users', async () => {
+    vi.resetModules();
+    silent.error.mockClear();
+    vi.doMock('../repositories/userRepo', () => ({ ...USER_REPO_BASE, seedDemoUsers: vi.fn(async () => { throw new Error('ks1776 rejection'); }) }));
+    await import('../routes/auth');
+    advance(2500);
+    await Promise.resolve();
+    await Promise.resolve();
+    expect(silent.error.mock.calls.map((call) => call[0])).toEqual(['Failed to seed demo users']);
+  });
+});
```

## DECISION NOTE (source-read, Spark operator for Wednesday, 2026-10-28 PM) - HOLD-WITH-DECISION: the fix SHAPE was chosen by the drafter, not the ticket
- KS-1776 is facts-only ("no fix proposed"): a module-scope `setTimeout(() => userRepo.seedDemoUsers(hashPassword).catch(...), 2000)` in `services/auth/src/routes/auth.ts` throws SYNCHRONOUSLY when a test's `userRepo` mock lacks the export, which escapes the timer as an uncaught vitest error pinned on whichever test is running. The drafter chose to make the PRODUCT timer callback tolerant: `try { userRepo.seedDemoUsers(hashPassword).catch(logSeedFailure) } catch (err) { logSeedFailure(err) }`, with both paths logging the same `Failed to seed demo users` line and the existing `{ error: err }` payload.
- Alternatives the owner may prefer: (a) fix only the offending test's mock (add `seedDemoUsers` to the `userRepo` mock in ks781-login-authorize-agree), leaving product code alone; (b) move the seed out of module scope (KS-1737 says the type-check ratchet forbids top-level await in service tests, which is why this shape avoided it). The chosen shape does change product code for a test-isolation symptom.
- Behaviour for production: unchanged when `seedDemoUsers` exists and resolves or rejects (same log line, same payload); a synchronous throw there is now logged instead of crashing the process as an uncaught exception (arguably a robustness gain, but a change; the repository module always exports it in production, so this branch is test-only in practice).
- Source-read of the patch: 5 lines -> 12, nothing outside `routes/auth.ts:62-73` changed; the new test uses fake timers and a 9-module mock set (D1/D2 red, C1/C2 control). Not exercised against the original flake (seen once in a loaded run).
- Verdict: HOLD-WITH-DECISION; the raise seat confirms the shape with the owner (Refs KS-1776, no close-word).
