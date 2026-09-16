# READY — KS-1188 F2 (NEW auth test ks1188-getuserbyid-failed-log-meta-keys.test.ts: the `DB getUserById failed` log meta key set is exactly {code, error} on the infra, pg 53300 and rethrow arms) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE (05:57). Held by Wednesday at 06:01 AEST.
# Source read by me (Wednesday): the model's 122 lines IDENTICAL to the brief's test block (python compare; a mutated copy unequal); one new file, userRepo.ts / ks999 / ks949 untouched; apply STRICT; A4 under the #1013 gate's Q-LOG-LEAK (userRepo.ts:413 adds stack + userId) 3 red / 5 run by assertion, controls green; A6 auth NEW reds [].
# PR NOTES: "Refs KS-1188 (F2)" — F1 (route-level 503 pins) and F3 (backup-code burn order, a product decision) stay open. Test-only → tier 2.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1188-getuserbyid-failed-log-meta-keys.test.ts
@@ -0,0 +1,122 @@
+// KS-1188 F2 (the #1013 gate on KS-999): the ks999 log cell matches the new 'DB getUserById failed' line with
+// objectContaining({ error }), so a catch that ALSO logged stack and userId (the gate's Q-LOG-LEAK) reddened 0 of 745
+// cells. These cells drive the REAL getUserById catch through a getDek rejection and pin the meta key set exactly.
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
+    if (String(sql).includes('SELECT') && String(sql).includes('FROM users')) {
+      const id = String((params || [])[0] ?? '');
+      if (id === 'ks1188-encrypted-row') {
+        return { rows: [{ id, email: 'sdek:ciphertext', status: 'active', role: 'user', created_at: '2026-01-01T00:00:00.000Z', updated_at: '2026-01-01T00:00:00.000Z' }], rowCount: 1 };
+      }
+      return { rows: [], rowCount: 0 };
+    }
+    return { rows: [], rowCount: 0 };
+  }),
+}));
+
+async function loadRepo() {
+  const saved = { ...process.env };
+  Object.assign(process.env, { NODE_ENV: 'development' });
+  vi.resetModules();
+  const repo = await import('../repositories/userRepo');
+  const deks = await import('../services/subjectDeks');
+  const log = await import('../utils/logger');
+  return { repo, deks, log, restore: () => { process.env = saved; } };
+}
+
+const USER_ID = 'ks1188-encrypted-row';
+const LINE = 'DB getUserById failed';
+
+/** Every meta object the logger received with the classifier line, in call order. */
+function metasOf(calls: unknown[][]): Array<Record<string, unknown>> {
+  return calls.filter((call) => call[0] === LINE).map((call) => call[1] as Record<string, unknown>);
+}
+
+describe('KS-1188 F2 — the DB getUserById failed line carries exactly error and code', () => {
+  beforeEach(() => { vi.clearAllMocks(); });
+
+  it('🔴 KS-1188 F2 — a message-form infrastructure failure logs a meta whose key set is exactly error and code', async () => {
+    const { repo, deks, log, restore } = await loadRepo();
+    try {
+      vi.mocked(deks.subjectDeks.getDek).mockRejectedValueOnce(new Error('connection terminated unexpectedly'));
+      await expect(repo.getUserById(USER_ID)).rejects.toThrow(/temporarily unavailable/);
+      const metas = metasOf(vi.mocked(log.logger.error).mock.calls);
+      expect(metas.length).toBe(1);
+      expect(Object.keys(metas[0]).sort(), 'the meta keys of the classifier line').toEqual(['code', 'error']);
+      expect(JSON.stringify(metas[0])).not.toContain(USER_ID);
+    } finally { restore(); }
+  });
+
+  it('🔴 KS-1188 F2 — a pg 53300 failure logs a meta whose key set is exactly error and code, with the code', async () => {
+    const { repo, deks, log, restore } = await loadRepo();
+    try {
+      vi.mocked(deks.subjectDeks.getDek).mockRejectedValueOnce(Object.assign(new Error('sorry, too many clients already'), { code: '53300' }));
+      await expect(repo.getUserById(USER_ID)).rejects.toThrow(/temporarily unavailable/);
+      const metas = metasOf(vi.mocked(log.logger.error).mock.calls);
+      expect(metas.length).toBe(1);
+      expect(Object.keys(metas[0]).sort(), 'the meta keys of the classifier line').toEqual(['code', 'error']);
+      expect(metas[0]).toStrictEqual({ error: 'sorry, too many clients already', code: '53300' });
+    } finally { restore(); }
+  });
+
+  it('🔴 KS-1188 F2 — a NON-infrastructure failure is rethrown as-is and its meta key set is still exactly error and code', async () => {
+    const { repo, deks, log, restore } = await loadRepo();
+    try {
+      vi.mocked(deks.subjectDeks.getDek).mockRejectedValueOnce(new Error('ks1188-not-an-infrastructure-fault'));
+      await expect(repo.getUserById(USER_ID)).rejects.toThrow(/ks1188-not-an-infrastructure-fault/);
+      const metas = metasOf(vi.mocked(log.logger.error).mock.calls);
+      expect(metas.length).toBe(1);
+      expect(Object.keys(metas[0]).sort(), 'the meta keys of the classifier line').toEqual(['code', 'error']);
+      expect(JSON.stringify(metas[0])).not.toContain(USER_ID);
+    } finally { restore(); }
+  });
+
+  it('🟢 KS-1188 control — the REAL catch ran: getDek was read for the row and the line was logged once with the rejection message', async () => {
+    const { repo, deks, log, restore } = await loadRepo();
+    try {
+      vi.mocked(deks.subjectDeks.getDek).mockRejectedValueOnce(new Error('connection terminated unexpectedly'));
+      await repo.getUserById(USER_ID).catch(() => undefined);
+      expect(deks.subjectDeks.getDek).toHaveBeenCalledWith(USER_ID);
+      const metas = metasOf(vi.mocked(log.logger.error).mock.calls);
+      expect(metas.length).toBe(1);
+      expect(metas[0].error).toBe('connection terminated unexpectedly');
+    } finally { restore(); }
+  });
+
+  it('🟢 KS-1188 control — with nothing rejecting the row resolves and the line is never logged', async () => {
+    const { repo, deks, log, restore } = await loadRepo();
+    try {
+      const user = await repo.getUserById(USER_ID);
+      expect(user?.id).toBe(USER_ID);
+      expect(deks.subjectDeks.getDek).toHaveBeenCalledWith(USER_ID);
+      expect(metasOf(vi.mocked(log.logger.error).mock.calls).length).toBe(0);
+    } finally { restore(); }
+  });
+});
```
