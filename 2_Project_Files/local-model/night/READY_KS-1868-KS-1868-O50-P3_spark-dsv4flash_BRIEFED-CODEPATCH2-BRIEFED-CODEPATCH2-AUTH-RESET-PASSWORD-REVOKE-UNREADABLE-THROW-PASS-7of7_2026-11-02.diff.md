# READY — KS-1868-KS-1868-O50-P3 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p3_auth_reset_password_revoke_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 01:26 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p3_auth_reset_password_revoke_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p3_auth_reset_password_revoke_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p3_auth_reset_password_revoke_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p3_auth_reset_password_revoke_unreadable_throw-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 01:26 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p3_auth_reset_password_revoke_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8afcf256ed5fb38d05f7273e08e1b912446bac5c`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/routes/auth.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-reset-password-revoke-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/routes/auth.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-reset-password-revoke-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/auth/src/routes/auth.ts
160	0	Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-reset-password-revoke-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: auth.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/routes/auth.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-reset-password-revoke-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/routes/auth.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-reset-password-revoke-unreadable-throw.test.ts 160 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/routes/auth.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-reset-password-revoke-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 the reset-password revocation catch block reads the thrown value safely RED ks1868 R1 a revoked Proxy thrown value logs a constant reason and the route still answers the 503', 'KS-1868 the reset-password revocation catch block reads the thrown value safely RED ks1868 R2 an Error whose message getter throws logs a constant reason and the route still answers the 503']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1459 failed=3 | after: total=1463 failed=2` · `NEW reds: []` [baseline_suite.json total=1459 failed=3; after_suite.json total=1463 failed=2]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/routes/auth.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-reset-password-revoke-unreadable-throw.test.ts` (+160/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/routes/auth.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8afcf256ed5fb38d05f7273e08e1b912446bac5c` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p3_auth_reset_password_revoke_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o50_p3_auth_reset_password_revoke_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p3_auth_reset_password_revoke_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/routes/auth.ts b/Blockchain/Dev/services/auth/src/routes/auth.ts
--- a/Blockchain/Dev/services/auth/src/routes/auth.ts
+++ b/Blockchain/Dev/services/auth/src/routes/auth.ts
@@ -876,8 +876,14 @@
     try {
       sessionsRevoked = await revokeAllUserSessions(user.id);
     } catch (err: unknown) {
+      let reason: string;
+      try {
+        reason = err instanceof Error ? err.message : String(err);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
       logger.error('Password reset: the session revocation THREW after the password write', {
-        userId: user.id, error: err instanceof Error ? err.message : String(err),
+        userId: user.id, error: reason,
       });
       throw new ServiceUnavailableError(
         'Your password WAS reset, but your other sessions could not be ended because the session store became unreachable. Your reset link has NOT been used — please use it again shortly to end those sessions.',
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-reset-password-revoke-unreadable-throw.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-reset-password-revoke-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-reset-password-revoke-unreadable-throw.test.ts
@@ -0,0 +1,160 @@
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { AddressInfo } from 'node:net';
+import type { Server } from 'node:http';
+import express from 'express';
+
+// KS-1868: POST /reset-password revokes the account's sessions after the password write; when that revocation
+// THROWS, the catch block must still log its line and map the failure onto the KS-1692 503 (`Your password WAS
+// reset, but your other sessions could not be ended ...`, reset link NOT burned) even if the thrown value cannot
+// be read (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws, throws on `.message`).
+// Today the unreadable value makes the catch block itself throw a TypeError before the 503 is built, so the
+// caller gets a generic 500 INTERNAL_ERROR. Harness: the ks1407 reset-password test (real router and error
+// handler; repository, session store, mail and event bus mocked). The revocation stand-in rejects with a plain
+// function, not a vi.fn(): a spy inspects what it rejects with and could itself fail on a revoked Proxy before
+// the code under test saw it.
+const USER_ID = 'c1d2e3f4-5a6b-4c7d-8e9f-0a1b2c3d4e5f';
+const NEW_PASSWORD = 'S0me-Str0ng-Passw0rd!x';
+const LINE = 'Password reset: the session revocation THREW after the password write';
+
+const h = vi.hoisted(() => ({
+  revokeRejects: false,
+  toThrow: undefined as unknown,
+  logged: [] as unknown[][],
+  pwUpdates: 0,
+  linkBurns: 0,
+}));
+
+const capture = vi.hoisted(() => ({
+  debug: () => undefined,
+  info: () => undefined,
+  warn: () => undefined,
+  error: (...args: unknown[]) => {
+    h.logged.push(args);
+  },
+  log: () => undefined,
+}));
+vi.mock('../utils/logger', () => ({ logger: capture, createLogger: () => capture, validateEnv: () => undefined }));
+vi.mock('@secuura/shared/utils/logger', () => ({ logger: capture, createLogger: () => capture }));
+
+vi.mock('../repositories/userRepo', () => {
+  const repoMock = {
+    getResetToken: vi.fn(async () => ({ userId: 'c1d2e3f4-5a6b-4c7d-8e9f-0a1b2c3d4e5f', expiresAt: new Date(Date.now() + 600_000) })),
+    getUserByIdPreAuth: vi.fn(async () => ({ id: 'c1d2e3f4-5a6b-4c7d-8e9f-0a1b2c3d4e5f', email: 'ks1868-reset@example.test', status: 'ACTIVE' })),
+    updateUserOrThrow: vi.fn(async () => {
+      h.pwUpdates += 1;
+      return { id: 'c1d2e3f4-5a6b-4c7d-8e9f-0a1b2c3d4e5f' };
+    }),
+    consumeResetToken: vi.fn(async () => {
+      h.linkBurns += 1;
+    }),
+  };
+  return { default: repoMock, __esModule: true, ...repoMock };
+});
+vi.mock('../services/password', async (importOriginal) => ({
+  ...(await importOriginal<Record<string, unknown>>()),
+  hashPassword: vi.fn(async () => 'hashed'),
+}));
+vi.mock('../services/session', () => ({
+  isRedisAvailable: () => true,
+  revokeAllUserSessions: () => (h.revokeRejects ? Promise.reject(h.toThrow) : Promise.resolve(0)),
+}));
+vi.mock('../services/email', () => ({
+  sendVerificationEmail: vi.fn(async () => undefined),
+  sendPasswordResetEmail: vi.fn(async () => undefined),
+}));
+vi.mock('../events', () => ({ publishEvent: vi.fn(async () => undefined), EventTypes: {} }));
+vi.mock('../db', () => ({ isDbAvailable: () => false, query: vi.fn(async () => ({ rows: [], rowCount: 0 })) }));
+
+let server: Server;
+let baseUrl = '';
+beforeAll(async () => {
+  const { authRoutes } = await import('../routes/auth');
+  const { errorHandler } = await import('../middleware/errorHandler');
+  const app = express();
+  app.use(express.json());
+  app.use('/api/auth', authRoutes);
+  app.use(errorHandler);
+  server = app.listen(0, '127.0.0.1');
+  await new Promise<void>((resolve) => server.once('listening', () => resolve()));
+  baseUrl = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
+});
+afterAll(async () => {
+  await new Promise<void>((resolve) => server.close(() => resolve()));
+});
+beforeEach(() => {
+  h.revokeRejects = false;
+  h.toThrow = undefined;
+  h.logged.length = 0;
+  h.pwUpdates = 0;
+  h.linkBurns = 0;
+});
+
+const LINES = () => h.logged.filter((c) => c[0] === LINE);
+
+async function resetPassword() {
+  const res = await fetch(baseUrl + '/api/auth/reset-password', {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json' },
+    body: JSON.stringify({ token: 'ks1868-reset-token', password: NEW_PASSWORD }),
+  });
+  const body = (await res.json().catch(() => ({}))) as Record<string, unknown>;
+  const err = (body.error ?? {}) as Record<string, unknown>;
+  return { status: res.status, code: String(err.code ?? ''), message: String(err.message ?? '') };
+}
+
+describe('KS-1868 the reset-password revocation catch block reads the thrown value safely', () => {
+  it('control ks1868 C1 an ordinary Error still logs its message and the route answers the 503 with the token unburned', async () => {
+    h.revokeRejects = true;
+    h.toThrow = new Error('redis down');
+    const r = await resetPassword();
+    expect(r.status).toBe(503);
+    expect(r.code).toBe('SERVICE_UNAVAILABLE');
+    expect(r.message).toMatch(/password WAS reset/i);
+    expect(h.pwUpdates).toBe(1);
+    expect(h.linkBurns).toBe(0);
+    expect(LINES()).toHaveLength(1);
+    expect(LINES()[0][1]).toEqual({ userId: USER_ID, error: 'redis down' });
+  });
+
+  it('control ks1868 C2 a revocation that succeeds reaches 200, burns the token once and logs no failure line', async () => {
+    const r = await resetPassword();
+    expect(r.status).toBe(200);
+    expect(h.pwUpdates).toBe(1);
+    expect(h.linkBurns).toBe(1);
+    expect(LINES()).toHaveLength(0);
+  });
+
+  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason and the route still answers the 503', async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    h.revokeRejects = true;
+    h.toThrow = proxy;
+    const r = await resetPassword();
+    expect(r.status).toBe(503);
+    expect(r.code).toBe('SERVICE_UNAVAILABLE');
+    expect(r.message).toMatch(/password WAS reset/i);
+    expect(h.pwUpdates).toBe(1);
+    expect(h.linkBurns).toBe(0);
+    expect(LINES()).toHaveLength(1);
+    expect(LINES()[0][1]).toEqual({ userId: USER_ID, error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason and the route still answers the 503', async () => {
+    h.revokeRejects = true;
+    h.toThrow = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    const r = await resetPassword();
+    expect(r.status).toBe(503);
+    expect(r.code).toBe('SERVICE_UNAVAILABLE');
+    expect(r.message).toMatch(/password WAS reset/i);
+    expect(h.pwUpdates).toBe(1);
+    expect(h.linkBurns).toBe(0);
+    expect(LINES()).toHaveLength(1);
+    expect(LINES()[0][1]).toEqual({ userId: USER_ID, error: 'unreadable thrown value' });
+  });
+});
```

## OPERATOR 50 NOTES (appended by the operator, not by hold_ready)
- SECURITY SURFACE: services/auth/src/routes/auth.ts. The raise of this pass will be gated tier 1.
- Behaviour change the raise PR must state: a reset-password whose session revocation throws an unreadable value today answers 500 INTERNAL_ERROR (password written, other sessions NOT revoked, token not burned, caller told only 'unexpected'); after the fix it answers the 503 SERVICE_UNAVAILABLE every ordinary revocation failure already gets ('Your password WAS reset, but your other sessions could not be ended...'). Writes and burns are identical. Same read exists at routes/users.ts change-password (not touched).
- Apply with: git apply -C1 <patch.diff> (the plain strict apply and plain patch both refuse the product hunk: the hunk has 3 leading and 0 trailing context lines because the next line is blank and build_input refuses blank context; git treats that as anchored to end of file). This pass applies strictly (it has trailing context).
- Combined with the other two passes (applied in order P3, P1, P2 to a scratch clone at the tip): the 3 new test files 12/12 green together; tsc -p tsconfig.test.json 42 errors = the 42 baseline errors, 0 in the new files. Whole-suite combined run UNMEASURED.
- The checker's whole-suite step A6 can go red on ks949-platform-admin-seed-identity.test.ts ('enumeration actually finds seed sites' / 'no executable seed site ... real address'): those two cells run 3.4-4.1 s at baseline against a 5 s timeout and timed out under load in 4 of 10 whole-suite runs of this session (see report). It is a pre-existing timing flake, not caused by the patch; re-run before reading it as a red.
