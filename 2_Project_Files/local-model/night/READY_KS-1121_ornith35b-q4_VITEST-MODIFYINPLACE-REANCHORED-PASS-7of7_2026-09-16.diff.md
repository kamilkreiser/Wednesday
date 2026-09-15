# READY — KS-1121 (Security: `credentialRepo.getById` resolved a credential by SUBSTRING — a DB `LIKE '%id%'` fallback and a memory `includes()` scan — under BOTH `GET /api/credentials/:id` and `POST /api/credentials/:id/revoke`; now EXACT-or-undefined, the KS-1020/#966 rule; the pinned partial-match test flipped) — **KAM RULED 2026-09-16 07:01 (card `secuura-ornith-decision-class-tickets-1121-629-975`, option a: "delete the substring branch exactly as #966 did for presentations (exact-or-404) and flip the one pinned test")** — Ornith ornith:35b (Q4_K_M) PASS 7/7 on the r2 RETRY (r1: three separate edits, one deletion drifted each sample; r2 first sample: the one-hunk rewrite right, the test hunk dropped the `finally`'s closing brace; r2 retry: both right), VITEST, MODIFY-IN-PLACE test (`test_file=` pin), tip develop M55 48e65c435, run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks1121-ornith35b-night2 (retry/)
# Source read by me (Wednesday): the applied `getById` is the brief's block byte-for-byte (the `+` side of the reanchored section: the JSDoc, ONE exact `SELECT … WHERE id = $1`, the catch unchanged, `return memoryStore.get(id)`); the LIKE query, the `%${id}%` pattern, the `includes()` loop and the `// Partial match` comment are all `-` lines; `revoke()` (:231-247) untouched and inherits the exact lookup. tsc after: 0 lines. The modified test: the pin cell `getById supports partial-match substring lookup` REPLACED by three 🔴 cells — every fragment (`abcdef`, `urn:vc:abc`, `1234`, `bcde`, `urn:vc:abcdef-123`, `%`, `_`) → undefined; `revoke('revoke-target')` → undefined and the stored credential's `revoked` stays false; DB path (`isDbAvailable` mocked true) → exactly ONE `SELECT credential` query and never a LIKE — plus the `import { isDbAvailable, query } from '../db'` line. At the tip: 3 failed / 11 run, controls green, assertion reds; after: 11/11; A6 the whole vc-issuer suite (108 at baseline) shows no NEW red.
# PR NOTES for the Sunday raising seat: (1) TWO files: `Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts` (:72–:108 — the JSDoc + `getById` body) + `src/__tests__/credentialRepo.test.ts` (an import; the pin cell → three cells); KS-1121 → Done, and the PR body cites Kam's 07:01 ruling. (2) Behaviour change to state in the PR body: `GET /api/credentials/:id` answers 404 for any id that is not an exact stored id (it used to return an arbitrary credential for a fragment); `POST /api/credentials/:id/revoke` refuses (undefined → the route's not-found path) on a fragment instead of revoking an arbitrary row. (3) NOT in this change (KS-1116): ownership/tenant checks on both routes — the ticket's item 2; sequence KS-1121 with KS-1116 in the PR note as the card said. (4) Route-level cells (the KS-1020 test's shape on `routes/credentials.ts`) were NOT written — the repo-level cells prove the lookup; a route-level pin is a follow-up if Peter wants the wire proven. (5) Apply the REANCHORED sections as held in this READY (the model's context lines did not match at the file; every hunk was rebuilt from its -/+ lines).

```diff
--- a/Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts
+++ b/Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts
@@ -70,41 +70,26 @@
 }
 
 /**
- * Retrieve a credential by its full ID, or by a partial-match substring.
+ * Retrieve a credential by its EXACT id — a fragment resolves nothing (KS-1121, the KS-1020 rule; #966
+ * did the same for presentations). The LIKE fallback and the includes() scan are deleted.
  */
 export async function getById(id: string): Promise<SecuuraCredential | undefined> {
   // Try DB first
   if (isDbAvailable()) {
     try {
       await ensureTable();
-      // Exact match
-      let result = await query<{ credential: SecuuraCredential }>(
-        'SELECT credential FROM vc_credentials_store WHERE id = $1',
-        [id],
-      );
-      if (result.rows.length > 0) return result.rows[0].credential;
-
-      // Partial match
-      result = await query<{ credential: SecuuraCredential }>(
-        'SELECT credential FROM vc_credentials_store WHERE id LIKE $1 LIMIT 1',
-        [`%${id}%`],
-      );
-      if (result.rows.length > 0) return result.rows[0].credential;
+      const result = await query<{ credential: SecuuraCredential }>(
+        'SELECT credential FROM vc_credentials_store WHERE id = $1',
+        [id],
+      );
+      if (result.rows.length > 0) return result.rows[0].credential;
     } catch (err: any) {
       logger.warn('DB read failed — falling back to memory', { error: err?.message });
     }
   }
 
-  // Fall back to memory
-  const exact = memoryStore.get(id);
-  if (exact) return exact;
-
-  for (const [key, value] of memoryStore.entries()) {
-    if (key.includes(id) || value.id.includes(id)) {
-      return value;
-    }
-  }
-  return undefined;
+  // Fall back to memory
+  return memoryStore.get(id);
 }
 
 /**
--- a/Blockchain/Dev/services/vc-issuer/src/__tests__/credentialRepo.test.ts
+++ b/Blockchain/Dev/services/vc-issuer/src/__tests__/credentialRepo.test.ts
@@ -17,6 +17,7 @@ vi.mock('../utils/logger', () => ({
 }));
 
 import * as repo from '../repositories/credentialRepo';
+import { isDbAvailable, query } from '../db';
 
 function makeCredential(overrides: Record<string, unknown> = {}) {
   return {
@@ -55,12 +56,34 @@ describe('credentialRepo (memory-only mode)', () => {
     expect(got!.id).toBe(c.id);
   });
 
-  it('getById supports partial-match substring lookup', async () => {
+  it('\ud83d\udd34 KS-1121 \u2014 getById resolves a credential by its EXACT id only: every fragment is undefined', async () => {
     const c = makeCredential({ id: 'urn:vc:abcdef-1234' });
     await repo.store(c);
-    const got = await repo.getById('abcdef');
-    expect(got?.id).toBe('urn:vc:abcdef-1234');
+    expect((await repo.getById(c.id))?.id).toBe('urn:vc:abcdef-1234');
+    for (const fragment of ['abcdef', 'urn:vc:abc', '1234', 'bcde', 'urn:vc:abcdef-123', '%', '_']) {
+      expect(await repo.getById(fragment), `fragment ${fragment}`).toBeUndefined();
+    }
+  });
+
+  it('\ud83d\udd34 KS-1121 \u2014 revoke on a fragment returns undefined and mutates nothing', async () => {
+    const c = makeCredential({ id: 'urn:vc:revoke-target-5678' });
+    await repo.store(c);
+    expect(await repo.revoke('revoke-target', 'fragment')).toBeUndefined();
+    expect((await repo.getById(c.id))?.credentialStatus?.revoked).toBe(false);
+  });
+
+  it('\ud83d\udd34 KS-1121 \u2014 DB path: an unknown id costs exactly ONE lookup query, and it is never a LIKE', async () => {
+    vi.mocked(isDbAvailable).mockReturnValue(true);
+    vi.mocked(query).mockResolvedValue({ rows: [] } as any);
+    try {
+      expect(await repo.getById('abcdef')).toBeUndefined();
+      const lookups = vi.mocked(query).mock.calls.map((call) => String(call[0])).filter((sql) => /SELECT credential/i.test(sql));
+      expect(lookups).toHaveLength(1);
+      expect(lookups[0]).not.toMatch(/ LIKE /i);
+    } finally {
+      vi.mocked(isDbAvailable).mockReturnValue(false);
+      vi.mocked(query).mockReset();
+    }
   }
 
   it('getById returns undefined for a totally absent id', async () => {
```
