# READY — KS-1188-F2-R15 (Ornith, briefed, test_only, new · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1188-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 21:43 2026-09-21). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip — with an accommodation: --recount (miscounted header: hunk @@ -0,0 +1,97 @@ declared old=0 new=97 actual old=0 new=122 ); every line byte-exact`; golden not located — no byte-identity claim is made.

**Held 21:43 2026-09-21 by Wednesday (the 20:1x seat) after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1188-ornith35b-night/out.md.checker`, not typed).** Tip `9f0265eb06ecf24d4de18149ce862ad2330a61ee`. Touches ONE file: `Blockchain/Dev/services/auth/src/__tests__/ks1188-getuserbyid-failed-log-meta-keys.test.ts` (new). `+` lines 122 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 5/5 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `F2` → red exactly ['RED KS-1188 F2 - a NON-infrastructure failure is rethrown as', 'RED KS-1188 F2 - a message-form infrastructure failure logs ', 'RED KS-1188 F2 - a pg 53300 failure logs a meta whose key se']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1188-ornith35b-night/input.json`. Brief: `night/briefs/KS-1188-F2-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1188-ornith35b-night/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1188-getuserbyid-failed-log-meta-keys.test.ts
@@ -0,0 +1,97 @@
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
+describe('KS-1188 F2 - the DB getUserById failed line carries exactly error and code', () => {
+  beforeEach(() => { vi.clearAllMocks(); });
+
+  it('RED KS-1188 F2 - a message-form infrastructure failure logs a meta whose key set is exactly error and code', async () => {
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
+  it('RED KS-1188 F2 - a pg 53300 failure logs a meta whose key set is exactly error and code, with the code', async () => {
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
+  it('RED KS-1188 F2 - a NON-infrastructure failure is rethrown as-is and its meta key set is still exactly error and code', async () => {
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
+  it('GREEN KS-1188 control - the REAL catch ran: getDek was read for the row and the line was logged once with the rejection message', async () => {
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
+  it('GREEN KS-1188 control - with nothing rejecting the row resolves and the line is never logged', async () => {
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
