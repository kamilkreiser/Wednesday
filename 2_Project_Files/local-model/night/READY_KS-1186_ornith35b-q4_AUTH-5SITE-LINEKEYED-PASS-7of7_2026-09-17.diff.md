# READY — KS-1186 (auth userRepo.ts: five sibling reads now `return await fromRow` inside their try, so a DEK-read infra failure is classified 503 like KS-999's getUserById — 5 line-keyed sites :446 :512 :585 :594 :627 + a new test, 5 red cells + control) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE, 2026-09-17 12:52 — FIRST AUTH-TIER local-model fix
# Source read by Wednesday: the test file's 124 `+` lines IDENTICAL to the brief fence (a mutated copy unequal); the five product `-` lines IDENTICAL to the brief; the five `+` lines = the brief's code PLUS a trailing comment `// KS-1186: await so the catch classifies infra failures inside fromRow` (the model copied the house style of the already-fixed :410 `// KS-999: …` line — code identical, comment additive; the raiser may keep it, it matches :410). A3b graded by LINE NUMBER: REMOVED_LINES 446,512,585,594,627. Apply LENIENT (the last hunk header `-624,6 +624,6` miscounts — the model's known header dialect), A6 whole services/auth no new red, A7 tsc rc 0. Run: local-model/runs/2026-09-17_ks1186-ornith35b-night
# PR NOTES: `Refs KS-1186` (Closes only if the gate agrees all five named sites are the ticket's whole scope). TIER 1 (auth login / pre-auth / social sign-in / MFA-disable paths change 500 → 503 under a DEK-read infra failure — a behaviour change on normal production paths per the ticket; brief raise notes). §5f: runtime change → In Progress on merge, live sweep owed. :1040 listUsersInner out of scope. Brief: night/briefs/KS-1186.md; checker report: tests/A3B_LINE_NUMBER_REPORT_2026-09-17.md. Branch off develop; disjoint from seat A's six local heads (none touches userRepo.ts — Wednesday measured the KS-1194 head: users.ts + its test only).

```diff
--- a/Blockchain/Dev/services/auth/src/repositories/userRepo.ts
+++ b/Blockchain/Dev/services/auth/src/repositories/userRepo.ts
@@ -443,7 +443,7 @@ export async function getUserByIdWithPasswordHash(id: string): Promise<User | nu
       `SELECT ${USER_COLS}, password_hash FROM users WHERE id = $1 LIMIT 1`,
       [id],
     );
-    if (result.rows.length > 0) return fromRow(result.rows[0]);
+    if (result.rows.length > 0) return await fromRow(result.rows[0]); // KS-1186: await so the catch classifies infra failures inside fromRow
     return null;
   } catch (err: any) {
     logger.error('DB getUserByIdWithPasswordHash failed', { error: err?.message, code: err?.code });
@@ -509,7 +509,7 @@ export async function getUserByIdPreAuth(id: string): Promise<User | null> {
   try {
     const result = await query(`SELECT ${USER_COLS} FROM auth_find_user_by_id($1)`, [id]);
-    if (result.rows.length > 0) return fromRow(result.rows[0]);
+    if (result.rows.length > 0) return await fromRow(result.rows[0]); // KS-1186: await so the catch classifies infra failures inside fromRow
     return null;
   } catch (err: any) {
     logger.error('DB getUserByIdPreAuth failed', { error: err?.message, code: err?.code });
@@ -582,7 +582,7 @@ export async function getUserByEmail(email: string): Promise<User | null> {
       'SELECT * FROM auth_find_user_by_email_hash($1)',
       [hash],
     );
-    if (result.rows.length > 0) return fromRow(result.rows[0]);
+    if (result.rows.length > 0) return await fromRow(result.rows[0]); // KS-1186: await so the catch classifies infra failures inside fromRow
 
     // Legacy fallback: rows that pre-date the hash column still have
     // plaintext email and no hash. They're identifiable by NOT starting
@@ -591,7 +591,7 @@ export async function getUserByEmail(email: string): Promise<User | null> {
       'SELECT * FROM auth_find_user_by_email_legacy($1)',
       [normalised],
     );
-    if (legacy.rows.length > 0) return fromRow(legacy.rows[0]);
+    if (legacy.rows.length > 0) return await fromRow(legacy.rows[0]); // KS-1186: await so the catch classifies infra failures inside fromRow
     return null;
   } catch (err: any) {
     // KS-253: a DB failure is NOT "user not found". Swallowing it here made
@@ -624,6 +624,6 @@ export async function getUserBySocialId(provider: string, providerId: string): 
     // columns as SOCIAL_ID_COLUMN_MAP.
     const result = await query(`SELECT ${USER_COLS} FROM auth_find_user_by_social($1, $2)`, [provider, providerId]);
-    if (result.rows.length > 0) return fromRow(result.rows[0]);
+    if (result.rows.length > 0) return await fromRow(result.rows[0]); // KS-1186: await so the catch classifies infra failures inside fromRow
     return null;
   } catch (err: any) {

--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1186-userrepo-ts-five-sibling-reads-still.test.ts
@@ -0,0 +1,124 @@
+/**
+ * KS-1186: the five sibling reads of getUserById await fromRow, so a failure
+ * inside fromRow (the subject-DEK read) reaches the KS-253 classifier.
+ *
+ * getUserByIdWithPasswordHash, getUserByIdPreAuth, getUserByEmail (hash arm and
+ * legacy arm) and getUserBySocialId returned fromRow(...) unawaited from inside
+ * their try, so a rejected DEK read escaped the catch: a raw error instead of
+ * ServiceUnavailable, and no classifier log. KS-999 fixed getUserById only.
+ */
+import { describe, it, expect, beforeEach, vi } from 'vitest';
+
+vi.mock('@secuura/shared', async (importOriginal) => {
+  const actual = await importOriginal<Record<string, unknown>>();
+  return {
+    ...actual,
+    encryptField: async (v: string) => v,
+    decryptField: async (v: string) => v,
+    encryptFieldWithDek: async (v: string) => v,
+    decryptFieldWithDek: async (v: string) => v,
+    isSubjectDekCiphertext: (v: unknown) => typeof v === 'string' && v.startsWith('sdek:'),
+    isEncryptedPii: () => false,
+    lookupHash: (v: string) => 'hash:' + v,
+  };
+});
+
+vi.mock('../services/subjectDeks', () => ({
+  subjectDeks: {
+    getDek: vi.fn(async () => 'test-dek'),
+    getOrCreateDek: vi.fn(async () => 'test-dek'),
+  },
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
+}));
+
+vi.mock('../db', () => ({
+  query: vi.fn(async (sql: string, params: unknown[] = []) => {
+    const args = (params || []).map((p) => String(p));
+    const row = { id: 'ks1186-encrypted-row', email: 'sdek:ciphertext', status: 'active', role: 'user', created_at: '2026-01-01T00:00:00.000Z', updated_at: '2026-01-01T00:00:00.000Z' };
+    if (String(sql).includes('auth_find_user_by_email_hash') && args[0] === 'hash:legacy-arm@ks1186.test') return { rows: [], rowCount: 0 };
+    const known = ['ks1186-encrypted-row', 'hash:hash-arm@ks1186.test', 'legacy-arm@ks1186.test', 'google-ks1186'];
+    if (args.some((a) => known.includes(a))) return { rows: [row], rowCount: 1 };
+    return { rows: [], rowCount: 0 };
+  }),
+}));
+
+const EXPECTED_CELLS = 6;
+let CELLS_RUN = 0;
+const ID = 'ks1186-encrypted-row';
+const INFRA = 'connection terminated unexpectedly';
+const NOT_INFRA = 'ks1186-not-an-infrastructure-fault';
+const UNAVAILABLE = 'Authentication service temporarily unavailable, please retry';
+
+// [the rejection message, or 'resolved:' + the user id; whether the classifier logged 'DB <fn> failed']
+async function verdict(fn: string, call: (repo: any) => Promise<any>, reject: string): Promise<Array<string | boolean>> {
+  const saved = { ...process.env };
+  Object.assign(process.env, { NODE_ENV: 'development' });
+  vi.resetModules();
+  try {
+    const repo = await import('../repositories/userRepo');
+    const deks = await import('../services/subjectDeks');
+    const log = await import('../utils/logger');
+    if (reject) vi.mocked(deks.subjectDeks.getDek).mockRejectedValueOnce(new Error(reject));
+    let seen = '';
+    try {
+      const user = await call(repo);
+      seen = 'resolved:' + String(user && user.id);
+    } catch (err: any) {
+      seen = String(err && err.message);
+    }
+    const logged = vi.mocked(log.logger.error).mock.calls.some((c: any[]) => c[0] === 'DB ' + fn + ' failed');
+    return [seen, logged];
+  } finally {
+    process.env = saved;
+  }
+}
+
+const READS: Array<[string, (repo: any) => Promise<any>]> = [
+  ['getUserByIdWithPasswordHash', (repo) => repo.getUserByIdWithPasswordHash(ID)],
+  ['getUserByIdPreAuth', (repo) => repo.getUserByIdPreAuth(ID)],
+  ['getUserByEmail', (repo) => repo.getUserByEmail('hash-arm@ks1186.test')],
+  ['getUserByEmail', (repo) => repo.getUserByEmail('legacy-arm@ks1186.test')],
+  ['getUserBySocialId', (repo) => repo.getUserBySocialId('google', 'google-ks1186')],
+];
+
+describe('KS-1186 - the five sibling reads await fromRow, so a DEK-read failure is classified', () => {
+  beforeEach(() => { vi.clearAllMocks(); });
+
+  it('KS-1186 R1 - getUserByIdWithPasswordHash: an infrastructure failure inside fromRow becomes ServiceUnavailable and is logged', async () => {
+    CELLS_RUN += 1;
+    expect(await verdict(READS[0][0], READS[0][1], INFRA)).toEqual([UNAVAILABLE, true]);
+  });
+  it('KS-1186 R2 - getUserByIdPreAuth: an infrastructure failure inside fromRow becomes ServiceUnavailable and is logged', async () => {
+    CELLS_RUN += 1;
+    expect(await verdict(READS[1][0], READS[1][1], INFRA)).toEqual([UNAVAILABLE, true]);
+  });
+  it('KS-1186 R3 - getUserByEmail hash arm: an infrastructure failure inside fromRow becomes ServiceUnavailable and is logged', async () => {
+    CELLS_RUN += 1;
+    expect(await verdict(READS[2][0], READS[2][1], INFRA)).toEqual([UNAVAILABLE, true]);
+  });
+  it('KS-1186 R4 - getUserByEmail legacy arm: an infrastructure failure inside fromRow becomes ServiceUnavailable and is logged', async () => {
+    CELLS_RUN += 1;
+    expect(await verdict(READS[3][0], READS[3][1], INFRA)).toEqual([UNAVAILABLE, true]);
+  });
+  it('KS-1186 R5 - getUserBySocialId: an infrastructure failure inside fromRow becomes ServiceUnavailable and is logged', async () => {
+    CELLS_RUN += 1;
+    expect(await verdict(READS[4][0], READS[4][1], INFRA)).toEqual([UNAVAILABLE, true]);
+  });
+  it('KS-1186 CONTROL - a non-infrastructure failure inside fromRow is rethrown as-is by all five, and with nothing rejecting all five resolve', async () => {
+    CELLS_RUN += 1;
+    const rethrown: Array<string | boolean> = [];
+    const resolved: Array<string | boolean> = [];
+    for (const [fn, call] of READS) {
+      rethrown.push((await verdict(fn, call, NOT_INFRA))[0]);
+      resolved.push((await verdict(fn, call, ''))[0]);
+    }
+    expect(rethrown).toEqual([NOT_INFRA, NOT_INFRA, NOT_INFRA, NOT_INFRA, NOT_INFRA]);
+    expect(resolved).toEqual(['resolved:' + ID, 'resolved:' + ID, 'resolved:' + ID, 'resolved:' + ID, 'resolved:' + ID]);
+  });
+  it('KS-1186 COMPLETENESS - every graded cell above actually ran', () => {
+    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
+  });
+});
```

