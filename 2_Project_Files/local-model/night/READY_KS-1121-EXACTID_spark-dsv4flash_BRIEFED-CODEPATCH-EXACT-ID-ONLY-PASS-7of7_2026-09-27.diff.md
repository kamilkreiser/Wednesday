# CORRECTION by Wednesday 14:09 AEST 2026-09-27: this run is the SPARK (deepseek-v4-flash-0731, LM_BACKEND=spark), NOT Ornith. hold_ready.py wrote `ornith35b-q4` into the filename and any model line below from its Ornith-only template; the file was renamed by Wednesday (mv, same content). Model identity: runs/spark_secuura_2026-09-27_KS-1121-r2/out.md.meta.json + run.log `backend=spark`.
# BYTE PROOF (Wednesday, same action): the model's 52 +/- lines are IDENTICAL, in order, to the rev-2 brief's two fences (night/briefs/KS-1121-r2/KS-1121.md; python sequence compare, empty lines excluded). No golden dir exists; the brief's fences are the golden. The brief's product fence alone applies strict -F0 at 94c9c7aa9be7 (control). PR NOTES: `Refs KS-1121`, NO closing keyword at raise (the GO moves it). Behaviour change: GET /api/credentials/:id answers 404 for any id that is not an exact stored id, per Kam's ruling 2026-09-16 07:01 (card secuura-ornith-decision-class-tickets-1121-629-975, option a). TIER 1 (credential lookup behaviour).
# READY — KS-1121-KS-1121-EXACTID (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-27_KS-1121-r2/out.md.checker/patch.diff`** (from `ls` at 14:09 2026-09-27; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-27_KS-1121-r2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-27_KS-1121-r2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 14:09 2026-09-27 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-27_KS-1121-r2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts , Blockchain/Dev/services/vc-issuer/src/__tests__/credentialRepo.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts` (product) and `Blockchain/Dev/services/vc-issuer/src/__tests__/credentialRepo.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	14	Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts
30	6	Blockchain/Dev/services/vc-issuer/src/__tests__/credentialRepo.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 14.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/vc-issuer/src/__tests__/credentialRepo.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/credentialRepo.test.ts fails at the untouched tip (3 failed / 11 run; controls green; assertion reds)` [red_first.json: failed=3 of total=11; red cell(s): ['credentialRepo (memory-only mode) RED KS-1121 A: getById resolves a credential by its EXACT id only - every fragment is undefined', 'credentialRepo (memory-only mode) RED KS-1121 B: revoke on a fragment returns undefined and mutates nothing', 'credentialRepo (memory-only mode) RED KS-1121 C: DB path - an unknown id costs exactly ONE lookup query, and it is never a LIKE']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/credentialRepo.test.ts passes with the product hunk (11 passed / 11 run)` [green_after.json: failed=0 of total=11, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=134 failed=0 | after: total=136 failed=0` · `NEW reds: []` [baseline_suite.json total=134 failed=0; after_suite.json total=136 failed=0]
- A6 [verbatim]: `PASS A6 whole services/vc-issuer suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/vc-issuer: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +32/-20 test=src/__tests__/credentialRepo.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts` (+2/-14 per numstat.out) and the test file `Blockchain/Dev/services/vc-issuer/src/__tests__/credentialRepo.test.ts` (+30/-6); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-27_KS-1121-r2/input.json`. Brief (located by ticket + ROWID tokens under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1121-R16B-EXACTID.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-27_KS-1121-r2/checker.out`.

```diff
--- a/Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts
+++ b/Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts
@@ -85,4 +85,5 @@
 /**
- * Retrieve a credential by its full ID, or by a partial-match substring.
+ * Retrieve a credential by its EXACT id only (KS-1121; the KS-1020 / #966 rule): a fragment resolves
+ * nothing. The LIKE fallback and the includes() scan are deleted.
  */
 export async function getById(id: string): Promise<SecuuraCredential | undefined> {
@@ -96,11 +97,4 @@
         [id],
       );
       if (result.rows.length > 0) return result.rows[0].credential;
-
-      // Partial match
-      result = await query<{ credential: SecuuraCredential }>(
-        'SELECT credential FROM vc_credentials_store WHERE id LIKE $1 LIMIT 1',
-        [`%${id}%`],
-      );
-      if (result.rows.length > 0) return result.rows[0].credential;
     } catch (err: any) {
@@ -111,11 +105,5 @@
   // Fall back to memory
   const exact = memoryStore.get(id);
   if (exact) return exact;
-
-  for (const [key, value] of memoryStore.entries()) {
-    if (key.includes(id) || value.id.includes(id)) {
-      return value;
-    }
-  }
   return undefined;
 }
--- a/Blockchain/Dev/services/vc-issuer/src/__tests__/credentialRepo.test.ts
+++ b/Blockchain/Dev/services/vc-issuer/src/__tests__/credentialRepo.test.ts
@@ -55,10 +55,34 @@
     expect(got).toBeDefined();
     expect(got!.id).toBe(c.id);
   });
-
-  it('getById supports partial-match substring lookup', async () => {
-    const c = makeCredential({ id: 'urn:vc:abcdef-1234' });
-    await repo.store(c);
-    const got = await repo.getById('abcdef');
-    expect(got?.id).toBe('urn:vc:abcdef-1234');
+
+  it('RED KS-1121 A: getById resolves a credential by its EXACT id only - every fragment is undefined', async () => {
+    const stored = makeCredential({ id: 'urn:vc:abcdef-1234' });
+    await repo.store(stored);
+    expect((await repo.getById(stored.id))?.id).toBe('urn:vc:abcdef-1234');
+    for (const fragment of ['abcdef', 'urn:vc:abc', '1234', 'bcde', 'urn:vc:abcdef-123', '%', '_']) {
+      expect(await repo.getById(fragment), 'fragment ' + fragment).toBeUndefined();
+    }
+  });
+
+  it('RED KS-1121 B: revoke on a fragment returns undefined and mutates nothing', async () => {
+    const target = makeCredential({ id: 'urn:vc:revoke-target-5678' });
+    await repo.store(target);
+    expect(await repo.revoke('revoke-target', 'fragment')).toBeUndefined();
+    expect((await repo.getById(target.id))?.credentialStatus?.revoked).toBe(false);
+  });
+
+  it('RED KS-1121 C: DB path - an unknown id costs exactly ONE lookup query, and it is never a LIKE', async () => {
+    const db = await import('../db');
+    vi.mocked(db.isDbAvailable).mockReturnValue(true);
+    vi.mocked(db.query).mockResolvedValue({ rows: [] } as any);
+    try {
+      expect(await repo.getById('abcdef')).toBeUndefined();
+      const lookups = vi.mocked(db.query).mock.calls.map((call) => String(call[0])).filter((sql) => /SELECT credential/i.test(sql));
+      expect(lookups).toHaveLength(1);
+      expect(lookups[0]).not.toMatch(/ LIKE /i);
+    } finally {
+      vi.mocked(db.isDbAvailable).mockReturnValue(false);
+      vi.mocked(db.query).mockReset();
+    }
   });
```
