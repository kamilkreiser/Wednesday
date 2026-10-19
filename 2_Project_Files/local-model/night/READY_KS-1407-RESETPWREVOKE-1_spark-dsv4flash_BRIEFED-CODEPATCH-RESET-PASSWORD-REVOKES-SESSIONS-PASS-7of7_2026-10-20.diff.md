# READY — KS-1407-RESETPWREVOKE-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1407_p2/out.md.checker/patch.diff`** (from `ls` at 09:52 2026-10-20; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1407_p2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1407_p2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1407_p2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1407_p2-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 09:52 2026-10-20 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1407_p2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `89956fe92956a810f6821fdee09915f087feea7b`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/auth/src/routes/auth.ts , Blockchain/Dev/services/auth/src/__tests__/ks1407-reset-password-revokes-the-sessions.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/routes/auth.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1407-reset-password-revokes-the-sessions.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
4	1	Blockchain/Dev/services/auth/src/routes/auth.ts
169	0	Blockchain/Dev/services/auth/src/__tests__/ks1407-reset-password-revokes-the-sessions.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (4 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 4 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/auth/src/routes/auth.ts byte-exact incl. leading whitespace (apply mode strict): OK 4 line(s) byte-exact incl. leading whitespace (of 4; 4 line(s) added by the apply)` [a3i_indent.out: `OK 4 line(s) byte-exact incl. leading whitespace (of 4; 4 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/routes/auth.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1407-reset-password-revokes-the-sessions.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1407-reset-password-revokes-the-sessions.test.ts fails at the untouched tip (3 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=3 of total=7; red cell(s): ['KS-1407 reset-password revokes the account sessions RED KS-1407 R1: a successful reset revokes every session of that account, once', 'KS-1407 reset-password revokes the account sessions RED KS-1407 R2: the revocation runs after the new hash was written and before the reset token is burned', 'KS-1407 reset-password revokes the account sessions RED KS-1407 R3: the number of sessions revoked is logged with the account id']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1407-reset-password-revokes-the-sessions.test.ts passes with the product hunk (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1096 failed=0 | after: total=1103 failed=0` · `NEW reds: []` [baseline_suite.json total=1096 failed=0; after_suite.json total=1103 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +173/-1 test=src/__tests__/ks1407-reset-password-revokes-the-sessions.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/routes/auth.ts` (+4/-1 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1407-reset-password-revokes-the-sessions.test.ts` (+169/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `89956fe92956a810f6821fdee09915f087feea7b` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1407_p2/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1407_p2/KS-1407.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1407_p2/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/routes/auth.ts b/Blockchain/Dev/services/auth/src/routes/auth.ts
index fa7b3386a..6c3fac379 100644
--- a/Blockchain/Dev/services/auth/src/routes/auth.ts
+++ b/Blockchain/Dev/services/auth/src/routes/auth.ts
@@ -16,3 +16,3 @@
 import { sendVerificationEmail, sendPasswordResetEmail } from '../services/email';
-import { createSession, revokeSession, getSession, rotateSessionRefreshToken } from '../services/session';
+import { createSession, revokeSession, revokeAllUserSessions, getSession, rotateSessionRefreshToken } from '../services/session';
 import { denylistRefreshJti, isRefreshJtiDenylisted } from '../services/refreshDenylist';
@@ -848,2 +848,5 @@
     await userRepo.updateUserOrThrow(user.id, { passwordHash: newHash }, 'Password reset');
+    // KS-1407: the old password minted sessions; none of them may outlive it. Before the token is burned, so a failing revocation leaves it usable for a retry.
+    const sessionsRevoked = await revokeAllUserSessions(user.id);
+    logger.info('Password reset revoked the account sessions', { userId: user.id, sessionsRevoked });
     await userRepo.consumeResetToken(tokenHash);
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1407-reset-password-revokes-the-sessions.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1407-reset-password-revokes-the-sessions.test.ts
new file mode 100644
index 000000000..0dfb0241e
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1407-reset-password-revokes-the-sessions.test.ts
@@ -0,0 +1,169 @@
+// KS-1407 (N-1382-1) - a successful POST /api/auth/reset-password revokes the account's sessions.
+//
+// THE DEFECT, at develop 89956fe92956: routes/auth.ts writes the new password hash, burns the single-use reset token and answers 200,
+// and makes ZERO revokeAllUserSessions calls. A reset is exactly the flow a user runs when they think the account is compromised, and
+// every session the old password minted stays live. This file pins the call: after a reset whose write LANDED, revokeAllUserSessions
+// runs once for that account, after the password write and BEFORE the single-use token is burned (so a failing revocation leaves the
+// token usable for a retry); and it does NOT run for a reset that was refused (unknown token, expired token, weak password) or
+// whose write did not land.
+//
+// The route, the real userRepo, the real errorHandler and the real password service run; the database, the logger, the e-mail sender and
+// the events are replaced, and the session module keeps everything except revokeAllUserSessions, which records its calls.
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+import express from 'express';
+
+const USER_ID = 'b1c2d3e4-5f6a-4b7c-8d9e-0f1a2b3c4d5e';
+const EMAIL = 'ks1407-reset@example.test';
+const RESET_TOKEN = 'ks1407-reset-token';
+const NEW_PASSWORD = 'S0me-Str0ng-Passw0rd!x';
+
+const state = vi.hoisted(() => ({
+  /** false = the password UPDATE matches no row and the read-back finds nothing (the write does not land). */
+  persisted: true,
+  /** what the reset-token lookup finds */
+  token: 'valid' as 'valid' | 'unknown' | 'expired',
+  queries: [] as Array<{ sql: string }>,
+  /** one entry per revokeAllUserSessions call: the account, and what had already happened by then */
+  revokes: [] as Array<{ userId: string; passwordWrites: number; tokenBurns: number }>,
+}));
+
+const silentLogger = { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() };
+vi.mock('../utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger, validateEnv: vi.fn() }));
+vi.mock('@secuura/shared/utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger }));
+
+function userRow() {
+  return {
+    id: USER_ID, email: EMAIL, first_name: 'K', last_name: 'S', display_name: 'KS',
+    role: 'user', status: 'active', email_verified: false,
+    phone_number: null, phone_verified: false,
+    mfa_enabled: false, mfa_secret: null, mfa_backup_codes: null,
+    verification_level: 'basic', organization_id: null, tenant_id: null, tenant_slug: null,
+    wallet_address: null, auth_method: 'password', external_provider: null, external_id: null,
+    google_id: null, linkedin_id: null, facebook_id: null, apple_id: null,
+    github_id: null, microsoft_personal_id: null, metadata: null,
+    password_hash: '$argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ$aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
+    created_at: new Date(), updated_at: new Date(), last_login_at: null,
+  };
+}
+
+const passwordWrites = () => state.queries.filter((q) => /^\s*UPDATE\s+users/i.test(q.sql)).length;
+const tokenBurns = () => state.queries.filter((q) => /^\s*UPDATE\s+password_reset_tokens/i.test(q.sql)).length;
+
+vi.mock('../db', () => ({
+  query: vi.fn(async (sql: string) => {
+    state.queries.push({ sql });
+    if (/auth_find_user_by_id/i.test(sql)) return { rows: [userRow()], rowCount: 1 };
+    if (/^\s*UPDATE\s+users/i.test(sql)) return { rows: [], rowCount: state.persisted ? 1 : 0 };
+    if (/FROM\s+users\s+WHERE\s+id/i.test(sql)) {
+      return state.persisted ? { rows: [userRow()], rowCount: 1 } : { rows: [], rowCount: 0 };
+    }
+    if (/password_reset_tokens/i.test(sql)) {
+      if (/^\s*UPDATE/i.test(sql)) return { rows: [], rowCount: 1 };
+      if (state.token === 'unknown') return { rows: [], rowCount: 0 };
+      const at = state.token === 'expired' ? Date.now() - 600_000 : Date.now() + 600_000;
+      return { rows: [{ user_id: USER_ID, expires_at: new Date(at) }], rowCount: 1 };
+    }
+    return { rows: [], rowCount: 0 };
+  }),
+}));
+
+vi.mock('../services/email', () => ({
+  sendVerificationEmail: vi.fn(async () => undefined),
+  sendPasswordResetEmail: vi.fn(async () => undefined),
+}));
+vi.mock('../events', () => ({ publishEvent: vi.fn(async () => undefined), EventTypes: {} }));
+
+vi.mock('../services/session', async (importOriginal) => {
+  const actual = await importOriginal<Record<string, unknown>>();
+  return {
+    ...actual,
+    revokeAllUserSessions: vi.fn(async (userId: string) => {
+      state.revokes.push({ userId, passwordWrites: passwordWrites(), tokenBurns: tokenBurns() });
+      return 3;
+    }),
+  };
+});
+
+let server: Server;
+let base: string;
+
+beforeAll(async () => {
+  const { authRoutes } = await import('../routes/auth');
+  const { errorHandler } = await import('../middleware/errorHandler');
+  const app = express();
+  app.use(express.json());
+  app.use('/api/auth', authRoutes);
+  app.use(errorHandler);
+  server = app.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => server.once('listening', () => r()));
+  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
+});
+
+afterAll(async () => { await new Promise<void>((r) => server.close(() => r())); });
+
+beforeEach(() => {
+  state.persisted = true;
+  state.token = 'valid';
+  state.queries = [];
+  state.revokes = [];
+  vi.clearAllMocks();
+});
+
+async function resetPassword(password = NEW_PASSWORD) {
+  const res = await fetch(`${base}/api/auth/reset-password`, {
+    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ token: RESET_TOKEN, password }),
+  });
+  return { status: res.status, body: await res.text() };
+}
+
+describe('KS-1407 reset-password revokes the account sessions', () => {
+  it('RED KS-1407 R1: a successful reset revokes every session of that account, once', async () => {
+    const r = await resetPassword();
+    expect(r.status).toBe(200);
+    expect(state.revokes.map((c) => c.userId)).toEqual([USER_ID]);
+  });
+
+  it('RED KS-1407 R2: the revocation runs after the new hash was written and before the reset token is burned', async () => {
+    await resetPassword();
+    expect(state.revokes).toEqual([{ userId: USER_ID, passwordWrites: 1, tokenBurns: 0 }]);
+    expect(tokenBurns()).toBe(1);
+  });
+
+  it('RED KS-1407 R3: the number of sessions revoked is logged with the account id', async () => {
+    await resetPassword();
+    expect(silentLogger.info).toHaveBeenCalledWith('Password reset revoked the account sessions', { userId: USER_ID, sessionsRevoked: 3 });
+  });
+
+  it('CONTROL KS-1407 C1: a reset whose write did not land is not answered 200 and revokes nothing', async () => {
+    state.persisted = false;
+    const r = await resetPassword();
+    expect(r.status).not.toBe(200);
+    expect(passwordWrites()).toBeGreaterThan(0);
+    expect(state.revokes).toEqual([]);
+  });
+
+  it('CONTROL KS-1407 C2: an unknown reset token answers 404, writes nothing and revokes nothing', async () => {
+    state.token = 'unknown';
+    const r = await resetPassword();
+    expect(r.status).toBe(404);
+    expect(passwordWrites()).toBe(0);
+    expect(state.revokes).toEqual([]);
+  });
+
+  it('CONTROL KS-1407 C3: an expired reset token is refused 400, writes nothing and revokes nothing', async () => {
+    state.token = 'expired';
+    const r = await resetPassword();
+    expect(r.status).toBe(400);
+    expect(passwordWrites()).toBe(0);
+    expect(state.revokes).toEqual([]);
+  });
+
+  it('CONTROL KS-1407 C4: a weak new password is refused, writes nothing and revokes nothing', async () => {
+    const r = await resetPassword('aaaaaaaaaaaaaaaaaaaa');
+    expect([400, 422]).toContain(r.status);
+    expect(passwordWrites()).toBe(0);
+    expect(state.revokes).toEqual([]);
+  });
+});
```
