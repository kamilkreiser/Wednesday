# READY — KS-999 ITEM 1 (`getUserById` awaits `fromRow`, so a fromRow-side infrastructure failure reaches the KS-253 classifier — 503, never a raw 500) — Ornith ornith:35b (Q4_K_M) FIRST SAMPLE (`2026-09-15_ks999-ornith35b-night`; the run's A3c FAIL was a harness false negative on a trailing comment, IMPROVEMENTS row 89; RE-CHECKED PASS 7/7 in the same scratch clone under the fixed A3c) — at develop M55 `48e65c435`
# Source read by Wednesday 22:58: the product hunk is the one-word `await` at :406 plus a trailing `// KS-999:` comment (harmless — the PR seat keeps or drops it); the vitest test uses the ks949 dynamic-import driver with self-contained mocks and an `sdek:` row so fromRow takes its getDek read — 2 🔴 cells red BY ASSERTION at the tip (raw message escapes; the classifier's log never fires), 3 controls green both trees; auth suite no new reds, tsc rc 0.
# PR NOTES for the raising seat: (1) AUTH SERVICE, not auth logic — Wednesday's reading of Kam's 16:40, stated in the brief header; a 500→503 change on the normal production path, so the ticket's item 2 (gate against the four calling route families) is the QA gate's job on Sunday; (2) item 3 (rename the ks949 'UNAWAITED fromRow' characterisation cell) and item 4 (the logger mock) are test-file edits for the PR seat; (3) the four sibling `return fromRow(` sites (:442/:508/:581/:623) are OUT of scope — file a follow-up; (4) rename the auto-named test to `ks999-getuserbyid-awaits-fromrow.test.ts`; (5) paths lack the `Blockchain/Dev/` prefix.

```diff
--- a/services/auth/src/repositories/userRepo.ts
+++ b/services/auth/src/repositories/userRepo.ts
@@ -403,7 +403,7 @@ export async function getUserById(id: string, tenantId?: string): Promise<User | null> {
   try {
     const result = await query(`SELECT ${USER_COLS} FROM users WHERE id = $1 LIMIT 1`, [id], tenantId);
-    if (result.rows.length > 0) return fromRow(result.rows[0]);
+    if (result.rows.length > 0) return await fromRow(result.rows[0]); // KS-999: await so the catch classifies infra failures inside fromRow
     return null;
   } catch (err: any) {
     logger.error('DB getUserById failed', { error: err?.message, code: err?.code });
--- /dev/null
+++ b/services/auth/src/__tests__/ks999-getuserbyid-s-decrypt-path-escapes-the.test.ts
@@ -0,0 +1,75 @@
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
+    lookupHash: (v: string) => `hash:${v}`,
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
+    if (/select/i.test(String(sql)) && /from\s+users/i.test(String(sql))) {
+      const id = String((params || [])[0] ?? '');
+      if (id === 'ks999-encrypted-row') {
+        return { rows: [{ id, email: 'sdek:ciphertext', status: 'active', role: 'user', created_at: '2026-01-01T00:00:00.000Z', updated_at: '2026-01-01T00:00:00.000Z' }], rowCount: 1 };
+      }
+      return { rows: [], rowCount: 0 };
+    }
+    return { rows: [], rowCount: 0 };
+  }),
+}));
+
+async function loadRepo(env: Record<string, string | undefined>) {
+  const saved = { ...process.env };
+  Object.assign(process.env, { NODE_ENV: 'development', ...env });
+  vi.resetModules();
+  const repo = await import('../repositories/userRepo');
+  const db = await import('../db');
+  const deks = await import('../services/subjectDeks');
+  const log = await import('../utils/logger');
+  return { repo, db, deks, log, restore: () => { process.env = saved; } };
+}
+const ID = 'ks999-encrypted-row';
+
+describe('KS-999 — getUserById awaits fromRow, so a fromRow-side DB failure is classified', () => {
+  beforeEach(() => { vi.clearAllMocks(); });
+
+  it('🔴 KS-999 — an INFRASTRUCTURE failure inside fromRow (the getDek read) becomes ServiceUnavailable, not a raw error', async () => {
+    const { repo, deks, restore } = await loadRepo({});
+    try {
+      vi.mocked(deks.subjectDeks.getDek).mockRejectedValueOnce(new Error('connection terminated unexpectedly'));
+      await expect(repo.getUserById(ID)).rejects.toThrow(/temporarily unavailable/);
+    } finally { restore(); }
+  });
+
+  it('🔴 KS-999 — the fromRow-side failure is LOGGED by the classifier (the catch now runs)', async () => {
+    const { repo, deks, log, restore } = await loadRepo({});
+    try {
+      vi.mocked(deks.subjectDeks.getDek).mockRejectedValueOnce(new Error('connection terminated unexpectedly'));
+      await repo.getUserById(ID).catch(() => undefined);
+      expect(log.logger.error).toHaveBeenCalledWith('DB getUserById failed', expect.objectContaining({ error: 'connection terminated unexpectedly' }));
+    } finally { restore(); }
+  });
+
+  it('KS-999 control — a NON-infrastructure failure inside fromRow is rethrown as-is, before and after', async () => {
+    const { repo, deks, restore } = await loadRepo({});
+    try {
+      vi.mocked(deks.subjectDeks.getDek).mockRejectedValueOnce(new Error('ks999-not-an-infrastructure-fault'));
+      await expect(repo.getUserById(ID)).rejects.toThrow(/ks999-not-an-infrastructure-fault/);
+    } finally { restore(); }
+  });
+
+  it('KS-999 control — a query()-side infrastructure failure was already classified (KS-963)', async () => {
+    const { repo, db, restore } = await loadRepo({});
+    try {
+      vi.mocked(db.query).mockRejectedValueOnce(new Error('connection terminated unexpectedly'));
+      await expect(repo.getUserById(ID)).rejects.toThrow(/temporarily unavailable/);
+    } finally { restore(); }
+  });
+
+  it('KS-999 control — with nothing rejecting the encrypted row resolves, so the reds above fail on the rejection and not on the fixture', async () => {
+    const { repo, deks, restore } = await loadRepo({});
+    try {
+      const user = await repo.getUserById(ID);
+      expect(user?.id).toBe(ID);
+      expect(deks.subjectDeks.getDek).toHaveBeenCalledWith(ID);
+    } finally { restore(); }
+  });
+});
```
