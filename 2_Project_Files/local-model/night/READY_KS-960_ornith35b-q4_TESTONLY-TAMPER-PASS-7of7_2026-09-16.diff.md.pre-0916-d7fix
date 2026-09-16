# READY — KS-960 (two schema sources disagree on whether `users.email` is unique; the runtime side is already right and the PIN was owed) — Ornith ornith:35b (Q4_K_M) PASS 7/7 on its FIRST sample, TEST-ONLY / TAMPER-GRADED, tip develop M55 48e65c435, run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks960-ornith35b-night
# ⭐ THE FIRST DELIBERATE TAMPER-GRADED BRIEF, and it matters beyond this ticket. The queue's own header said coverage-only tickets "cannot pass RED-FIRST" and that the backlog is dominated by them. That stopped being true on 2026-09-15 when `build_input.sh` grew the `## Tamper` block (test-only: A3 test file only, A4 red UNDER THE TAMPER, A5 green at the tip). Nineteen held fixes already used the shape; nobody had pointed the candidate list at it. **This is that class, briefed on purpose, passing first sample.**
# SCOPE — read this before raising: KS-960's MAIN ask is a RULING ("⛔ DO NOT RECONCILE THESE TWO FILES YET") and this is NOT that. The ticket states as settled fact that the runtime is already correct — `createUser` conflicts on `email_lookup_hash` and says why. **This closes the owed PIN only; the schema-reconciliation decision stays open and is Kam's/Peter's.** Say so in the PR body or it reads as closing the ticket.
# Source read by me (Wednesday), the artefacts and not the verdict: ONE file touched, the new suite `services/auth/src/__tests__/ks960-two-schema-sources-disagree-on-whether.test.ts`, +106/-0. The product file is UNTOUCHED (A3 test-only asserts exactly that). Six cells: three reds by ASSERTION on the recorded SQL, two controls, a completeness arm (`CELLS_RUN === EXPECTED_CELLS`). Under the tamper 3 fail / 6 run with both controls green; at the untouched tip 6/6. Whole `services/auth` suite: no NEW red against a baseline that is itself red (734 total, 3 pre-existing failures, attributed not counted). `tsc --noEmit` rc 0 against a green baseline.
# THE CELL WORTH KEEPING, because it is the one a human would have got wrong: cell 2 asserts the statement does NOT contain `ON CONFLICT (email)`. At the tip the text is `ON CONFLICT (email_lookup_hash)` — the byte after `(email` is `_`, not `)`, so the assertion is GREEN at the tip and RED the moment the tamper narrows the conflict target. That is the 42P10 shape pinned precisely: KS-949 F1 was an `ON CONFLICT (email)` statement raising 42P10 on every boot while its suite stayed green.
# THE TAMPER (verified by the builder against the tip before the run, and re-verified by me): `services/auth/src/repositories/userRepo.ts:688` — `ON CONFLICT (email_lookup_hash) WHERE email_lookup_hash IS NOT NULL DO UPDATE SET` → `ON CONFLICT (email) DO UPDATE SET`. I measured that line independently: byte-for-byte as quoted and occurring EXACTLY ONCE in a 1875-line file. It carries a `statement_ok:` clause because the line sits mid-template-literal — the gate fired and the clause states that :681-694 hold no executable TypeScript.
# THE COVERAGE GAP THIS CLOSES, measured: `git grep -in "ON CONFLICT"` over `services/auth/src/__tests__` at the tip returns 4 hits and ALL FOUR ARE COMMENTS. No auth cell asserted any conflict target before this one.
# PR NOTES: (1) ONE new file, no product change — this cannot regress runtime behaviour. (2) The controls are the load-bearing half of a tamper-graded pin: they prove the harness reaches `createUser` and records its real SQL, so a red under the tamper means something. (3) Do NOT let this close KS-960. The ticket's own ⛔ stands.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks960-two-schema-sources-disagree-on-whether.test.ts
@@ -0,0 +1,101 @@
+/**
+ * KS-960 — the auth runtime conflicts on `email_lookup_hash`, never on `email`.
+ *
+ * The two schema sources disagree about whether `users.email` is unique, so
+ * `ON CONFLICT (email)` is valid against one and 42P10 against the other. This
+ * file settles nothing about which source is authoritative: it pins the one
+ * thing that IS settled — the statement `createUser` actually issues — so that
+ * the KS-949 F1 shape (a seed that raised 42P10 on every boot while its suite
+ * stayed green) cannot reappear here unseen.
+ */
+import { describe, it, expect, vi, beforeAll } from 'vitest';
+import type { User } from '../types';
+
+const mockQuery = vi.hoisted(() => vi.fn());
+vi.mock('../db', () => ({
+  query: mockQuery,
+  isDbAvailable: () => true,
+  getPool: () => ({}),
+}));
+vi.mock('../utils/logger', () => ({
+  logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
+}));
+vi.mock('../services/subjectDeks', () => ({
+  subjectDeks: {
+    getDek: async () => 'test-dek',
+    getOrCreateDek: async () => 'test-dek',
+  },
+}));
+vi.mock('@secuura/shared', async (importOriginal) => {
+  const actual = await importOriginal<Record<string, unknown>>();
+  return {
+    ...actual,
+    encryptField: async (v: string) => 'enc:' + v,
+    decryptField: async (v: string) => v,
+    encryptFieldWithDek: async (v: string) => 'enc:' + v,
+    decryptFieldWithDek: async (v: string) => v,
+    isSubjectDekCiphertext: () => false,
+    isEncryptedPii: () => false,
+    lookupHash: (v: string) => 'hash:' + v,
+  };
+});
+
+import { createUser } from '../repositories/userRepo';
+
+const EXPECTED_CELLS = 5;
+let CELLS_RUN = 0;
+const EMAIL = 'Someone.New@Example.COM';
+const NORMALISED = 'someone.new@example.com';
+const NEW_USER: User = {
+  id: 'a0000000-0000-4000-8000-000000000960',
+  email: EMAIL,
+  emailVerified: false,
+  phoneVerified: false,
+  mfaEnabled: false,
+  role: 'ISSUER_ADMIN',
+  verificationLevel: 'BASIC',
+  status: 'ACTIVE',
+  createdAt: new Date('2026-09-16T00:00:00.000Z'),
+  updatedAt: new Date('2026-09-16T00:00:00.000Z'),
+};
+let insertSql = '';
+let insertParams: unknown[] = [];
+
+beforeAll(async () => {
+  mockQuery.mockReset();
+  mockQuery.mockResolvedValue({ rows: [], rowCount: 1 });
+  await createUser({ ...NEW_USER });
+  const call = mockQuery.mock.calls.find((c) => String(c[0]).includes('INSERT INTO users'));
+  insertSql = call ? String(call[0]) : '';
+  insertParams = call ? (call[1] as unknown[]) : [];
+});
+
+describe('KS-960 — createUser conflicts on the deterministic column', () => {
+  it('🔴 KS-960 1 — the INSERT conflicts on email_lookup_hash', () => {
+    CELLS_RUN += 1;
+    expect(insertSql).toContain('ON CONFLICT (email_lookup_hash)');
+  });
+
+  it('🔴 KS-960 2 — the statement carries no ON CONFLICT (email) — the 42P10 shape', () => {
+    CELLS_RUN += 1;
+    expect(insertSql).not.toContain('ON CONFLICT (email)');
+  });
+
+  it('🔴 KS-960 3 — the conflict target keeps the partial-index predicate', () => {
+    CELLS_RUN += 1;
+    expect(insertSql).toContain('WHERE email_lookup_hash IS NOT NULL DO UPDATE SET');
+  });
+
+  it('🟢 KS-960 4 CONTROL — createUser issued the 22-parameter INSERT INTO users', () => {
+    CELLS_RUN += 1;
+    expect(insertSql).toContain('INSERT INTO users');
+    expect(insertSql).toContain('$22');
+    expect(insertParams.length).toBe(22);
+  });
+
+  it('🟢 KS-960 5 CONTROL — email is bound as ciphertext, email_lookup_hash as the deterministic hash', () => {
+    CELLS_RUN += 1;
+    expect(insertParams[1]).toBe('enc:' + NORMALISED);
+    expect(insertParams[2]).toBe('hash:' + NORMALISED);
+    expect(insertParams[1]).not.toBe(NORMALISED);
+  });
+
+  it('COMPLETENESS: every graded cell above actually ran', () => {
+    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
+  });
+});
```
