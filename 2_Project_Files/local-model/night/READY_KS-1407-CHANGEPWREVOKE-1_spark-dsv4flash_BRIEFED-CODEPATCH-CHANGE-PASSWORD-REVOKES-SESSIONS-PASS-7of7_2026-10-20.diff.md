# READY — KS-1407-CHANGEPWREVOKE-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1407_p1/out.md.checker/patch.diff`** (from `ls` at 09:52 2026-10-20; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1407_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1407_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1407_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1407_p1-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 09:52 2026-10-20 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1407_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `89956fe92956a810f6821fdee09915f087feea7b`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/auth/src/routes/users.ts , Blockchain/Dev/services/auth/src/__tests__/ks1407-change-password-revokes-the-sessions.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/routes/users.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1407-change-password-revokes-the-sessions.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	0	Blockchain/Dev/services/auth/src/routes/users.ts
185	0	Blockchain/Dev/services/auth/src/__tests__/ks1407-change-password-revokes-the-sessions.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (3 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 3 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/auth/src/routes/users.ts byte-exact incl. leading whitespace (apply mode strict): OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)` [a3i_indent.out: `OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/routes/users.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1407-change-password-revokes-the-sessions.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1407-change-password-revokes-the-sessions.test.ts fails at the untouched tip (3 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=3 of total=7; red cell(s): ['KS-1407 change-password revokes the account sessions RED KS-1407 R1: a successful change revokes every session of that account, once', 'KS-1407 change-password revokes the account sessions RED KS-1407 R2: the revocation runs AFTER the new hash was written, never before it', 'KS-1407 change-password revokes the account sessions RED KS-1407 R3: the number of sessions revoked is logged with the account id']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1407-change-password-revokes-the-sessions.test.ts passes with the product hunk (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1096 failed=0 | after: total=1103 failed=0` · `NEW reds: []` [baseline_suite.json total=1096 failed=0; after_suite.json total=1103 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +188/-0 test=src/__tests__/ks1407-change-password-revokes-the-sessions.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/routes/users.ts` (+3/-0 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1407-change-password-revokes-the-sessions.test.ts` (+185/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `89956fe92956a810f6821fdee09915f087feea7b` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1407_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1407_p1/KS-1407.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1407_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/routes/users.ts b/Blockchain/Dev/services/auth/src/routes/users.ts
index 10fab906c..bcdd27018 100644
--- a/Blockchain/Dev/services/auth/src/routes/users.ts
+++ b/Blockchain/Dev/services/auth/src/routes/users.ts
@@ -1001,2 +1001,5 @@
     logger.info('Password changed', { userId: user.id });
+    // KS-1407: the old password minted sessions; none of them may outlive it. Runs only after the write above landed (it throws otherwise).
+    const sessionsRevoked = await revokeAllUserSessions(user.id);
+    logger.info('Password change revoked the account sessions', { userId: user.id, sessionsRevoked });
     res.json({ success: true, message: 'Password changed successfully' });
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1407-change-password-revokes-the-sessions.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1407-change-password-revokes-the-sessions.test.ts
new file mode 100644
index 000000000..06d3e779f
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1407-change-password-revokes-the-sessions.test.ts
@@ -0,0 +1,185 @@
+// KS-1407 (N-1382-1) - a successful POST /api/users/me/change-password revokes the account's sessions.
+//
+// THE DEFECT, at develop 89956fe92956: routes/users.ts writes the new password hash and answers 200, and makes ZERO
+// revokeAllUserSessions calls. Every other session the old password minted (including one an attacker holds after a
+// compromise) stays live. This file pins the call: after a change that LANDED, revokeAllUserSessions runs once for that account,
+// AFTER the write; and it does NOT run for a change that was refused or did not land.
+//
+// The route, the real userRepo, the real errorHandler and the real password service run; only the database, the logger and the
+// session service are replaced. The database stand-in is the KS-1005 one (a SELECT carries password_hash only when it asks for it).
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { AddressInfo } from 'node:net';
+import type { Server } from 'node:http';
+import express from 'express';
+
+const USER_ID = 'ks1407-change-password-user';
+const CURRENT_PASSWORD = 'ks1407-Current-Passw0rd!';
+const NEW_PASSWORD = 'ks1407-Replacement-Passw0rd!';
+
+type Call = { sql: string; values: unknown[] };
+const updates: Call[] = [];
+let storedHash: string | null = null;
+/** false = the UPDATE matches no row (the write does not land). */
+let writeLands = true;
+/** how many UPDATEs had been issued at the moment revokeAllUserSessions ran, one entry per call */
+const updatesSeenAtRevoke: number[] = [];
+
+vi.mock('@secuura/shared', async (importOriginal) => {
+  const actual = await importOriginal<Record<string, unknown>>();
+  return {
+    ...actual,
+    encryptField: (v: string) => v,
+    decryptField: (v: string) => v,
+    encryptFieldWithDek: (v: string) => v,
+    decryptFieldWithDek: (v: string) => v,
+    isSubjectDekCiphertext: () => false,
+    isEncryptedPii: () => false,
+    lookupHash: (v: string) => 'hash:' + v,
+  };
+});
+
+vi.mock('../services/subjectDeks', () => ({
+  subjectDeks: {
+    getDek: vi.fn(async () => Buffer.from('ks1407-throwaway-dek')),
+    getOrCreateDek: vi.fn(async () => Buffer.from('ks1407-throwaway-dek')),
+  },
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  query: vi.fn(async (sql: string, values: unknown[] = []) => {
+    const text = String(sql);
+    if (text.includes('UPDATE users')) {
+      updates.push({ sql: text, values });
+      if (!writeLands) return { rows: [], rowCount: 0 };
+      return { rows: [{ id: USER_ID, email: 'ks1407@example.test', status: 'active', role: 'user' }], rowCount: 1 };
+    }
+    if (text.includes('SELECT') && text.includes('users')) {
+      const row: Record<string, unknown> = {
+        id: USER_ID,
+        email: 'ks1407@example.test',
+        status: 'active',
+        role: 'user',
+        auth_method: 'password',
+        created_at: '2026-01-01T00:00:00.000Z',
+        updated_at: '2026-01-01T00:00:00.000Z',
+      };
+      if (text.includes('password_hash')) row.password_hash = storedHash;
+      return { rows: [row], rowCount: 1 };
+    }
+    return { rows: [], rowCount: 0 };
+  }),
+}));
+
+vi.mock('../middleware/authenticate', () => {
+  const inject = () => (req: any, _res: any, next: () => void) => {
+    req.user = { userId: USER_ID, role: 'user' };
+    next();
+  };
+  return { authenticate: inject, authenticateAccessOrConnector: inject };
+});
+
+const revokeAllUserSessions = vi.fn(async (_userId: string) => 3);
+vi.mock('../services/session', () => ({
+  revokeAllUserSessions: (userId: string) => {
+    updatesSeenAtRevoke.push(updates.length);
+    return revokeAllUserSessions(userId);
+  },
+}));
+
+let server: Server;
+let base = '';
+let hashPassword: (p: string) => Promise<string>;
+let logger: { info: ReturnType<typeof vi.fn> };
+
+beforeAll(async () => {
+  const pw = await import('../services/password');
+  hashPassword = pw.hashPassword;
+  logger = (await import('../utils/logger')).logger as unknown as { info: ReturnType<typeof vi.fn> };
+  const { userRoutes } = await import('../routes/users');
+  const { errorHandler } = await import('../middleware/errorHandler');
+  const app = express();
+  app.use(express.json());
+  app.use('/api/users', userRoutes);
+  app.use(errorHandler);
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => {
+      base = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
+      resolve();
+    });
+  });
+});
+
+afterAll(async () => {
+  await new Promise<void>((resolve) => server.close(() => resolve()));
+});
+
+beforeEach(async () => {
+  updates.length = 0;
+  updatesSeenAtRevoke.length = 0;
+  writeLands = true;
+  vi.clearAllMocks();
+  storedHash = await hashPassword(CURRENT_PASSWORD);
+});
+
+async function changePassword(currentPassword: string, newPassword = NEW_PASSWORD) {
+  const res = await fetch(base + '/api/users/me/change-password', {
+    method: 'POST',
+    headers: { 'content-type': 'application/json' },
+    body: JSON.stringify({ currentPassword, newPassword }),
+  });
+  return { status: res.status, body: await res.json().catch(() => ({})) };
+}
+
+describe('KS-1407 change-password revokes the account sessions', () => {
+  it('RED KS-1407 R1: a successful change revokes every session of that account, once', async () => {
+    const r = await changePassword(CURRENT_PASSWORD);
+    expect(r.status).toBe(200);
+    expect(revokeAllUserSessions).toHaveBeenCalledTimes(1);
+    expect(revokeAllUserSessions).toHaveBeenCalledWith(USER_ID);
+  });
+
+  it('RED KS-1407 R2: the revocation runs AFTER the new hash was written, never before it', async () => {
+    await changePassword(CURRENT_PASSWORD);
+    expect(updates.filter((c) => c.sql.includes('password_hash')).length).toBe(1);
+    expect(updatesSeenAtRevoke).toEqual([1]);
+  });
+
+  it('RED KS-1407 R3: the number of sessions revoked is logged with the account id', async () => {
+    await changePassword(CURRENT_PASSWORD);
+    expect(logger.info).toHaveBeenCalledWith('Password change revoked the account sessions', { userId: USER_ID, sessionsRevoked: 3 });
+  });
+
+  it('CONTROL KS-1407 C1: a WRONG current password answers 400, writes nothing and revokes nothing', async () => {
+    const r = await changePassword('ks1407-not-the-current-password');
+    expect(r.status).toBe(400);
+    expect(updates.length).toBe(0);
+    expect(revokeAllUserSessions).not.toHaveBeenCalled();
+  });
+
+  it('CONTROL KS-1407 C2: a too-weak new password is refused and revokes nothing', async () => {
+    const r = await changePassword(CURRENT_PASSWORD, 'aaaaaaaaaaaaaaaaaaaa');
+    expect([400, 422]).toContain(r.status);
+    expect(updates.length).toBe(0);
+    expect(revokeAllUserSessions).not.toHaveBeenCalled();
+  });
+
+  it('CONTROL KS-1407 C3: a change whose write did not land is not answered 200 and revokes nothing', async () => {
+    writeLands = false;
+    const r = await changePassword(CURRENT_PASSWORD);
+    expect(r.status).not.toBe(200);
+    expect(updates.length).toBeGreaterThan(0);
+    expect(revokeAllUserSessions).not.toHaveBeenCalled();
+  });
+
+  it('CONTROL KS-1407 C4: a passwordless account still answers 404 and revokes nothing', async () => {
+    storedHash = null;
+    const r = await changePassword(CURRENT_PASSWORD);
+    expect(r.status).toBe(404);
+    expect(revokeAllUserSessions).not.toHaveBeenCalled();
+  });
+});
```
