# READY — KS-1663-1663-OP7 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1663_p1/out.md.checker/patch.diff`** (from `ls` at 03:48 2026-10-29; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1663_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1663_p1/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1663_p1/out.md.checker/section_3.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 03:48 2026-10-29 by Spark operator 7 after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1663_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `7d4c4745d75cb73605462540af256f400e059062`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/anchoring/src/anchorOverwriteGuard.ts } + { Blockchain/Dev/services/anchoring/src/__tests__/ks1663-the-custody-join-comments-name-the-role-restricted-policy.test.ts , Blockchain/Dev/services/anchoring/src/__tests__/ks1385-anchor-store-keeps-the-latest-events-metadata.integration.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/anchoring/src/anchorOverwriteGuard.ts` (product) and `Blockchain/Dev/services/anchoring/src/__tests__/ks1663-the-custody-join-comments-name-the-role-restricted-policy.test.ts` (test) — equal to numstat.out's set (3 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	7	Blockchain/Dev/services/anchoring/src/anchorOverwriteGuard.ts
41	0	Blockchain/Dev/services/anchoring/src/__tests__/ks1663-the-custody-join-comments-name-the-role-restricted-policy.test.ts
5	4	Blockchain/Dev/services/anchoring/src/__tests__/ks1385-anchor-store-keeps-the-latest-events-metadata.integration.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: anchorOverwriteGuard.ts`
- CODE_PATCH2 (rung 3, 1 product files + 2 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/anchoring/src/anchorOverwriteGuard.ts`; test(s): `Blockchain/Dev/services/anchoring/src/__tests__/ks1663-the-custody-join-comments-name-the-role-restricted-policy.test.ts`, `Blockchain/Dev/services/anchoring/src/__tests__/ks1385-anchor-store-keeps-the-latest-events-metadata.integration.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/anchoring/src/anchorOverwriteGuard.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/anchoring/src/__tests__/ks1663-the-custody-join-comments-name-the-role-restricted-policy.test.ts 41 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/anchoring/src/__tests__/ks1385-anchor-store-keeps-the-latest-events-metadata.integration.test.ts 5 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=3 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/anchorOverwriteGuard.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1663-the-custody-join-comments-name-the-role-restricted-policy.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- section 3 `section_3.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1385-anchor-store-keeps-the-latest-events-metadata.integration.test.ts` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=2 of total=7; red cell(s): ['KS-1663: the custody-join comments say what the policy does RED KS-1663 R1 the guard comment no longer says users is open for SELECT by construction', 'KS-1663: the custody-join comments say what the policy does RED KS-1663 R2 the guard comment names the role the permissive policy is granted to']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=391 failed=1 | after: total=398 failed=1` · `NEW reds: []` [baseline_suite.json total=391 failed=1; after_suite.json total=398 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=3 products=1 tests=2 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/anchoring/src/anchorOverwriteGuard.ts` (+8/-7 per numstat.out) and the test file `Blockchain/Dev/services/anchoring/src/__tests__/ks1663-the-custody-join-comments-name-the-role-restricted-policy.test.ts` (+41/-0); 3 files in all (code_patch2: products Blockchain/Dev/services/anchoring/src/anchorOverwriteGuard.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict) — at the tip `7d4c4745d75cb73605462540af256f400e059062` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1663_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1663_p1/KS-1663.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1663_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/anchoring/src/anchorOverwriteGuard.ts b/Blockchain/Dev/services/anchoring/src/anchorOverwriteGuard.ts
--- a/Blockchain/Dev/services/anchoring/src/anchorOverwriteGuard.ts
+++ b/Blockchain/Dev/services/anchoring/src/anchorOverwriteGuard.ts
@@ -252,13 +252,14 @@
   const asPrimaryKey = isUuidShaped(documentId) ? documentId.trim() : null;
   return transaction(async (client) => {
     await client.query("SELECT set_config('app.current_tenant_id', $1, true)", [tenantId.trim()]);
-    // The LEFT JOIN carries its OWN `u.tenant_id = $2::uuid`, and that is not
-    // belt-and-braces duplication of the one on `documents`. `users` has a
-    // SECOND, permissive policy — `users_auth_lookup`, whose qual is literally
-    // `true` — and Postgres ORs permissive policies together, so tenant
-    // isolation on `users` is open for SELECT by construction. Measured on the
-    // repo schema. A join without its own bound would read a custodian row
-    // from ANY tenant.
+    // The LEFT JOIN carries its OWN `u.tenant_id = $2::uuid` bound. `users` has
+    // a SECOND, permissive policy, `users_auth_lookup`, whose qual is literally
+    // `true`, but it is granted to the dedicated role `secuura_auth_lookup`,
+    // not to `public`, so it does not apply to `secuura_app`, the role
+    // anchoring connects as: there `tenant_isolation` is live. The bound stays
+    // so the join does not depend on which role the connection holds: a
+    // connection that held `secuura_auth_lookup` would read a custodian row
+    // from ANY tenant. (Measured on the repo schema, KS-1663.)
     //
     // LEFT, not INNER: a document whose custodian user has been deleted must
     // still yield the document row, with a null custodian organisation, rather
diff --git a/Blockchain/Dev/services/anchoring/src/__tests__/ks1663-the-custody-join-comments-name-the-role-restricted-policy.test.ts b/Blockchain/Dev/services/anchoring/src/__tests__/ks1663-the-custody-join-comments-name-the-role-restricted-policy.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1663-the-custody-join-comments-name-the-role-restricted-policy.test.ts
@@ -0,0 +1,41 @@
+// KS-1663 (anchoring, readOwningDocument): the comment above the custody LEFT JOIN, and the same inference in the ks1385 integration test's C-e cell, said `users` is "open for SELECT by construction"
+// because the permissive policy `users_auth_lookup` has a qual of `true`. That omitted the policy's roles: it is granted to the dedicated role `secuura_auth_lookup`, not to `public`, so it does not apply to
+// `secuura_app`, the role anchoring connects as. The tenant bound on the join is right and stays; only the stated reason was false.
+// These cells read the two files as text. R1 and R2 are the product-comment cells (red until the comment is corrected); T1 and T2 pin the corrected test comment; C1 to C3 pin what must not move.
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'fs';
+import { resolve } from 'path';
+
+const GUARD_SRC = readFileSync(resolve(__dirname, '..', 'anchorOverwriteGuard.ts'), 'utf8');
+const C_E_SRC = readFileSync(resolve(__dirname, 'ks1385-anchor-store-keeps-the-latest-events-metadata.integration.test.ts'), 'utf8');
+
+describe('KS-1663: the custody-join comments say what the policy does', () => {
+  it('RED KS-1663 R1 the guard comment no longer says users is open for SELECT by construction', () => {
+    expect(GUARD_SRC).not.toContain('open for SELECT by construction');
+  });
+
+  it('RED KS-1663 R2 the guard comment names the role the permissive policy is granted to', () => {
+    expect(GUARD_SRC).toContain('granted to the dedicated role `secuura_auth_lookup`');
+  });
+
+  it('control KS-1663 T1 the C-e cell comment no longer says users is open for SELECT by construction', () => {
+    expect(C_E_SRC).not.toContain('open for SELECT by construction');
+  });
+
+  it('control KS-1663 T2 the C-e cell comment names the role the permissive policy is granted to', () => {
+    expect(C_E_SRC).toContain('granted to the dedicated role');
+  });
+
+  it('control KS-1663 C1 the custody join still carries its own tenant bound', () => {
+    expect(GUARD_SRC).toContain('AND u.tenant_id = $2::uuid');
+  });
+
+  it('control KS-1663 C2 the LEFT-not-INNER comment is still there', () => {
+    expect(GUARD_SRC).toContain('LEFT, not INNER');
+  });
+
+  it('control KS-1663 C3 both files were read (the instrument is not reading an empty string)', () => {
+    expect(GUARD_SRC.length).toBeGreaterThan(1000);
+    expect(C_E_SRC.length).toBeGreaterThan(1000);
+  });
+});
diff --git a/Blockchain/Dev/services/anchoring/src/__tests__/ks1385-anchor-store-keeps-the-latest-events-metadata.integration.test.ts b/Blockchain/Dev/services/anchoring/src/__tests__/ks1385-anchor-store-keeps-the-latest-events-metadata.integration.test.ts
--- a/Blockchain/Dev/services/anchoring/src/__tests__/ks1385-anchor-store-keeps-the-latest-events-metadata.integration.test.ts
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1385-anchor-store-keeps-the-latest-events-metadata.integration.test.ts
@@ -532,10 +532,11 @@
   it('C-e a custodian user in ANOTHER tenant resolves NO organisation — the custody JOIN is tenant-bound too', async () => {
     // ⚠ ADDED because a mutant survived. Dropping `AND u.tenant_id = $2::uuid` from the custody
     // LEFT JOIN killed no cell, and it is not cosmetic: `users` carries a SECOND, permissive
-    // policy — `users_auth_lookup`, whose qual is literally `true` — and Postgres ORs permissive
-    // policies, so tenant isolation on `users` is open for SELECT by construction. Without the
-    // explicit bound, option (c) would resolve a custodian organisation from ANY tenant the
-    // moment Kam rules it, and nothing would have objected.
+    // policy, `users_auth_lookup` (qual literally `true`), but it is granted to the dedicated role
+    // `secuura_auth_lookup`, not to `public`, so it does not apply to `secuura_app`. The explicit
+    // bound keeps the join tenant-scoped whatever role the connection holds: without it, option (c)
+    // would resolve a custodian organisation from ANY tenant for a connection that held that role,
+    // and nothing would have objected.
     const doc = await makeDocument({ tenantId: TENANT_A, issuerOrgId: ORG_ISSUER, ownerUserId: USER_FOREIGN });
     const owning = await readOwningDocument(doc, TENANT_A);
     expect(owning).not.toBeNull();
```
