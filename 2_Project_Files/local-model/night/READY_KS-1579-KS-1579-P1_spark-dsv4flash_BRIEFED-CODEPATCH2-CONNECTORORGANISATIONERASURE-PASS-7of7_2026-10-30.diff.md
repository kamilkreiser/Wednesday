# READY — KS-1579-KS-1579-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1579_p1_erase_connector_text/out.md.checker/patch.diff`** (from `ls` at 12:16 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1579_p1_erase_connector_text/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1579_p1_erase_connector_text/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1579_p1_erase_connector_text/out.md.checker/section_3.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1579_p1_erase_connector_text/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1579_p1_erase_connector_text-control/out.md.checker/patch.diff` rc 0, Spark operator 20).

**Held 12:16 2026-10-30 by Spark operator 20 after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1579_p1_erase_connector_text/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `530f091120d5da749edf972e8e0089e44cfc5589`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/services/connectorOrganisationErasure.ts , Blockchain/Dev/services/originate/src/__tests__/ks695-ask3-erase-connector-refusals.test.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1579-erase-connector-comment-and-title-state-the-truth.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/services/connectorOrganisationErasure.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1579-erase-connector-comment-and-title-state-the-truth.test.ts` (test) — equal to numstat.out's set (3 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	2	Blockchain/Dev/services/originate/src/services/connectorOrganisationErasure.ts
1	1	Blockchain/Dev/services/originate/src/__tests__/ks695-ask3-erase-connector-refusals.test.ts
43	0	Blockchain/Dev/services/originate/src/__tests__/ks1579-erase-connector-comment-and-title-state-the-truth.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (4 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: connectorOrganisationErasure.ts ks695-ask3-erase-connector-refusals.test.ts`
- CODE_PATCH2 (rung 3, 2 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/services/connectorOrganisationErasure.ts`, `Blockchain/Dev/services/originate/src/__tests__/ks695-ask3-erase-connector-refusals.test.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1579-erase-connector-comment-and-title-state-the-truth.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/services/connectorOrganisationErasure.ts 3 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks695-ask3-erase-connector-refusals.test.ts 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1579-erase-connector-comment-and-title-state-the-truth.test.ts 43 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=3 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/services/connectorOrganisationErasure.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks695-ask3-erase-connector-refusals.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- section 3 `section_3.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1579-erase-connector-comment-and-title-state-the-truth.test.ts` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1579 items 3 and 4: the header comment and the cell title state what the code does RED KS-1579 T1 the erasure header no longer says a key was "rotated away"', 'KS-1579 items 3 and 4: the header comment and the cell title state what the code does RED KS-1579 T2 the erasure header says only a DELETED key escapes the guard and that a rotation leaves the old key readable', 'KS-1579 items 3 and 4: the header comment and the cell title state what the code does RED KS-1579 T3 the unit cell title no longer claims the 403 "already" came from the ownership comparison', 'KS-1579 items 3 and 4: the header comment and the cell title state what the code does RED KS-1579 T4 the unit cell title says it pins the status, not which refusal produces it']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 2 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1854 failed=0 | after: total=1860 failed=0` · `NEW reds: []` [baseline_suite.json total=1854 failed=0; after_suite.json total=1860 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=3 products=2 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/services/connectorOrganisationErasure.ts` (+3/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1579-erase-connector-comment-and-title-state-the-truth.test.ts` (+43/-0); 3 files in all (code_patch2: products Blockchain/Dev/services/originate/src/services/connectorOrganisationErasure.ts, Blockchain/Dev/services/originate/src/__tests__/ks695-ask3-erase-connector-refusals.test.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict) — at the tip `530f091120d5da749edf972e8e0089e44cfc5589` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1579_p1_erase_connector_text/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1579_p1_erase_connector_text/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/services/connectorOrganisationErasure.ts b/Blockchain/Dev/services/originate/src/services/connectorOrganisationErasure.ts
--- a/Blockchain/Dev/services/originate/src/services/connectorOrganisationErasure.ts
+++ b/Blockchain/Dev/services/originate/src/services/connectorOrganisationErasure.ts
@@ -216,8 +216,9 @@
 //           key committed before that UPDATE's snapshot is always seen and rolls the whole transaction back (m-1);
 //       (2) a key with NO connector id (NULL or blank) authenticates as the principal `connector:api-key`, which is also the literal
 //           label, so that principal is shared by every such key and by legacy rows from before ticket KS-869. It cannot identify
-//           one connector, and no key table can make an erasure by it safe (a guard that reads live keys cannot see a key that was
-//           deleted or rotated away). The erasure REFUSES it (403, nothing written) before it reads any key. A key without an id
+//           one connector, and no key table can make an erasure by it safe (a guard that reads the key table, inactive keys included,
+//           cannot see a key that was DELETED: a rotation only deactivates or shortens the old key). The erasure REFUSES it (403, nothing
+//           written) before it reads any key. A key without an id
 //           could never erase (its stored id is not the label); this closes the key that stores the label itself.
 //   - NOT closed here (M-1 path 1): the security service lets an organisation-scoped admin mint a key for ANOTHER
 //     organisation with any connector id, and this erasure trusts the key row, so that key can erase that organisation.
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks695-ask3-erase-connector-refusals.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks695-ask3-erase-connector-refusals.test.ts
--- a/Blockchain/Dev/services/originate/src/__tests__/ks695-ask3-erase-connector-refusals.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks695-ask3-erase-connector-refusals.test.ts
@@ -279,4 +279,4 @@
-  it('CONTROL - M-2 liveness is UNCHANGED: a key with a NULL, and one with an empty, connector id already got 403 from the ownership comparison and still does', async () => {
+  it('CONTROL - M-2 liveness is UNCHANGED: a key with a NULL, and one with an empty, connector id is still refused 403 (this cell pins the status, not which refusal produces it)', async () => {
     keyRows['key-null-695'] = { organization_id: ORG, connector_id: null };
     keyRows['key-empty-695'] = { organization_id: ORG, connector_id: '' };
     for (const keyId of ['key-null-695', 'key-empty-695']) {
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1579-erase-connector-comment-and-title-state-the-truth.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1579-erase-connector-comment-and-title-state-the-truth.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1579-erase-connector-comment-and-title-state-the-truth.test.ts
@@ -0,0 +1,43 @@
+/**
+ * KS-1579 items 3 and 4 - two pieces of text in the KS-695 erase-connector files must say what the code does.
+ *
+ * Item 4: the header comment of connectorOrganisationErasure.ts said the key-table guard cannot see a key "that was deleted or
+ * rotated away". A rotation only deactivates the old key or shortens its expiry (security's retirePriorStatement is an UPDATE), and the
+ * guard reads inactive keys, so a rotated key IS seen; only a DELETED key escapes it.
+ * Item 3: the unit cell titled "... already got 403 from the ownership comparison and still does" kept a reason that stopped being
+ * true when the fallback refusal was added in round 6. The cell pins the status, not the reason, and its title now says so.
+ * These are source-text cells: they read the two files as text, so no server is started.
+ */
+import * as fs from 'fs';
+import * as path from 'path';
+
+const erasureSource = fs.readFileSync(path.join(__dirname, '..', 'services', 'connectorOrganisationErasure.ts'), 'utf8');
+const refusalsSource = fs.readFileSync(path.join(__dirname, 'ks695-ask3-erase-connector-refusals.test.ts'), 'utf8');
+
+describe('KS-1579 items 3 and 4: the header comment and the cell title state what the code does', () => {
+  it('RED KS-1579 T1 the erasure header no longer says a key was "rotated away"', () => {
+    expect(erasureSource).not.toContain('deleted or rotated away');
+  });
+
+  it('RED KS-1579 T2 the erasure header says only a DELETED key escapes the guard and that a rotation leaves the old key readable', () => {
+    expect(erasureSource).toContain('cannot see a key that was DELETED: a rotation only deactivates or shortens the old key');
+  });
+
+  it('RED KS-1579 T3 the unit cell title no longer claims the 403 "already" came from the ownership comparison', () => {
+    expect(refusalsSource).not.toContain('already got 403 from the ownership comparison and still does');
+  });
+
+  it('RED KS-1579 T4 the unit cell title says it pins the status, not which refusal produces it', () => {
+    expect(refusalsSource).toContain('is still refused 403 (this cell pins the status, not which refusal produces it)');
+  });
+
+  it('CONTROL KS-1579 T5 the retitled cell still exists once and still checks the two keys', () => {
+    expect(refusalsSource.split('M-2 liveness is UNCHANGED').length - 1).toBe(1);
+    expect(refusalsSource).toContain("for (const keyId of ['key-null-695', 'key-empty-695'])");
+  });
+
+  it('CONTROL KS-1579 T6 the erasure file still declares the fallback predicate and still names the principal label', () => {
+    expect(erasureSource).toContain('export function isFallbackConnectorId(');
+    expect(erasureSource).toContain('connector:api-key');
+  });
+});
```
