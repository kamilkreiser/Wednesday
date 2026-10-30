# READY — KS-1585-KS-1585-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1585_p1_admin_docstring_ruled/out.md.checker/patch.diff`** (from `ls` at 11:57 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1585_p1_admin_docstring_ruled/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1585_p1_admin_docstring_ruled/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1585_p1_admin_docstring_ruled/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1585_p1_admin_docstring_ruled-control/out.md.checker/patch.diff` rc 0, Wednesday coordinator: Spark operator 19).

**Held 11:57 2026-10-30 by Wednesday coordinator: Spark operator 19 after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1585_p1_admin_docstring_ruled/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `530f091120d5da749edf972e8e0089e44cfc5589`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/security/src/__tests__/ks1533-key-mint-organisation-arm.test.ts } + { Blockchain/Dev/services/security/src/__tests__/ks1585-ks1533-admin-docstring-states-the-ruling.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/security/src/__tests__/ks1533-key-mint-organisation-arm.test.ts` (product) and `Blockchain/Dev/services/security/src/__tests__/ks1585-ks1533-admin-docstring-states-the-ruling.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/security/src/__tests__/ks1533-key-mint-organisation-arm.test.ts
34	0	Blockchain/Dev/services/security/src/__tests__/ks1585-ks1533-admin-docstring-states-the-ruling.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (1 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: ks1533-key-mint-organisation-arm.test.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/security/src/__tests__/ks1533-key-mint-organisation-arm.test.ts`; test(s): `Blockchain/Dev/services/security/src/__tests__/ks1585-ks1533-admin-docstring-states-the-ruling.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/security/src/__tests__/ks1533-key-mint-organisation-arm.test.ts 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/security/src/__tests__/ks1585-ks1533-admin-docstring-states-the-ruling.test.ts 34 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/security/src/__tests__/ks1533-key-mint-organisation-arm.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/security/src/__tests__/ks1585-ks1533-admin-docstring-states-the-ruling.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1585 n1: the PLAIN_ADMIN_A docstring states the KS-1570 ruling RED KS-1585 L1 the docstring no longer calls the ADMIN policy UNDECIDED', 'KS-1585 n1: the PLAIN_ADMIN_A docstring states the KS-1570 ruling RED KS-1585 L2 the docstring names the ruling (RULED, KS-1570)']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=368 failed=0 | after: total=372 failed=0` · `NEW reds: []` [baseline_suite.json total=368 failed=0; after_suite.json total=372 failed=0]
- A6 [verbatim]: `PASS A6 whole services/security suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/security: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/security/src/__tests__/ks1533-key-mint-organisation-arm.test.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/security/src/__tests__/ks1585-ks1533-admin-docstring-states-the-ruling.test.ts` (+34/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/security/src/__tests__/ks1533-key-mint-organisation-arm.test.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `530f091120d5da749edf972e8e0089e44cfc5589` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1585_p1_admin_docstring_ruled/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1585_p1_admin_docstring_ruled/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/security/src/__tests__/ks1533-key-mint-organisation-arm.test.ts b/Blockchain/Dev/services/security/src/__tests__/ks1533-key-mint-organisation-arm.test.ts
--- a/Blockchain/Dev/services/security/src/__tests__/ks1533-key-mint-organisation-arm.test.ts
+++ b/Blockchain/Dev/services/security/src/__tests__/ks1533-key-mint-organisation-arm.test.ts
@@ -77,7 +77,7 @@
 const ADMIN_A3 = () => token({ role: 'ISSUER_ADMIN', tenantId: TENANT_A, organizationId: ORG_A3 });
 /** Org-bounded, carrying NO organisation claim — the shape KS-779 recorded as intentional. */
 const ORGLESS_A = () => token({ role: 'org_admin', tenantId: TENANT_A });
-/** `ADMIN`: a KEY_ADMIN_ROLE the arm never engages for. UNDECIDED POLICY, KS-1535. */
+/** `ADMIN`: a KEY_ADMIN_ROLE bounded by its admin organisation scope. RULED, KS-1570 (shape b). */
 const PLAIN_ADMIN_A = () => token({ role: 'ADMIN', tenantId: TENANT_A, organizationId: ORG_A1 });
 /** `platform_admin`: a super-role to the gateway, not a PLATFORM_ROLE here. UNDECIDED, KS-1535. */
 const PLATFORM_ADMIN_A = () => token({ role: 'platform_admin', tenantId: TENANT_A, organizationId: ORG_A1 });
diff --git a/Blockchain/Dev/services/security/src/__tests__/ks1585-ks1533-admin-docstring-states-the-ruling.test.ts b/Blockchain/Dev/services/security/src/__tests__/ks1585-ks1533-admin-docstring-states-the-ruling.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/security/src/__tests__/ks1585-ks1533-admin-docstring-states-the-ruling.test.ts
@@ -0,0 +1,34 @@
+/**
+ * KS-1585 n1 - the `PLAIN_ADMIN_A` docstring in ks1533-key-mint-organisation-arm.test.ts must state the ruling.
+ *
+ * That docstring said `ADMIN` is a key-admin role "the arm never engages for. UNDECIDED POLICY, KS-1535." Kam ruled the policy
+ * in KS-1570 (shape b: each ADMIN acts only for the organisations in its admin organisation scope) and the cell that uses
+ * `PLAIN_ADMIN_A` was rewritten to RULED, but the docstring on the fixture was left stating the old, wrong position. These are
+ * source-text cells: they read the sibling file as text, so no server is started.
+ */
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { join } from 'node:path';
+
+const lines = readFileSync(join(__dirname, 'ks1533-key-mint-organisation-arm.test.ts'), 'utf8').split('\n');
+const docstring = lines.find((l) => l.startsWith('/** `ADMIN`:')) ?? 'NO ADMIN DOCSTRING';
+const fixtureIndex = lines.findIndex((l) => l.startsWith('const PLAIN_ADMIN_A ='));
+
+describe('KS-1585 n1: the PLAIN_ADMIN_A docstring states the KS-1570 ruling', () => {
+  it('RED KS-1585 L1 the docstring no longer calls the ADMIN policy UNDECIDED', () => {
+    expect(docstring).not.toMatch(/UNDECIDED/);
+  });
+
+  it('RED KS-1585 L2 the docstring names the ruling (RULED, KS-1570)', () => {
+    expect(docstring).toMatch(/RULED, KS-1570/);
+  });
+
+  it('CONTROL KS-1585 L3 the docstring sits directly above the PLAIN_ADMIN_A fixture', () => {
+    expect(fixtureIndex).toBeGreaterThan(0);
+    expect(lines[fixtureIndex - 1]).toBe(docstring);
+  });
+
+  it('CONTROL KS-1585 L4 the RULED cell the docstring points to still exists in the file', () => {
+    expect(lines.some((l) => l.includes("it('RULED (KS-1570, shape b): role `ADMIN` is bounded by its admin organisation scope"))).toBe(true);
+  });
+});
```
