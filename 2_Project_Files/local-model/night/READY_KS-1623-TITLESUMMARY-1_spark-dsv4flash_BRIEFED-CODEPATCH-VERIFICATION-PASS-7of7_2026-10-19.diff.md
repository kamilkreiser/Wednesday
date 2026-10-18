# READY — KS-1623-TITLESUMMARY-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1623_p1-r2/out.md.checker/patch.diff`** (from `ls` at 01:35 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1623_p1-r2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1623_p1-r2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1623_p1-control-r3/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in verification.ts (run 6 vs golden 9 body lines — context, since the change lines are equal) (identical in ks1623-title-lookup-summary-names-every-hidden-status.test.ts); hunk headers identical; APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 01:35 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1623_p1-r2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8a9970511f22661d92f634058fae8c08c656124f`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/verification.ts , Blockchain/Dev/services/originate/src/__tests__/ks1623-title-lookup-summary-names-every-hidden-status.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/verification.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1623-title-lookup-summary-names-every-hidden-status.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/originate/src/routes/verification.ts
44	0	Blockchain/Dev/services/originate/src/__tests__/ks1623-title-lookup-summary-names-every-hidden-status.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/verification.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/verification.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1623-title-lookup-summary-names-every-hidden-status.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1623-title-lookup-summary-names-every-hidden-status.test.ts fails at the untouched tip (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1623 N3 - the title lookup summary comment RED KS-1623 the summary comment names deleted', 'KS-1623 N3 - the title lookup summary comment RED KS-1623 the summary comment names expired']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1623-title-lookup-summary-names-every-hidden-status.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1388 failed=0 | after: total=1393 failed=0` · `NEW reds: []` [baseline_suite.json total=1388 failed=0; after_suite.json total=1393 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +45/-1 test=src/__tests__/ks1623-title-lookup-summary-names-every-hidden-status.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/verification.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1623-title-lookup-summary-names-every-hidden-status.test.ts` (+44/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8a9970511f22661d92f634058fae8c08c656124f` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1623_p1-r2/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1623_p1/KS-1623.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1623_p1-r2/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/verification.ts
+++ b/Blockchain/Dev/services/originate/src/routes/verification.ts
@@ -1443,5 +1443,5 @@ verificationRouter.post(
         //     document's title holds ERASED_MARKER (the column is NOT NULL), so a naive lookup would
         //     make an erased document discoverable through the very field that was erased.
-        // Absent, another tenant's, draft, revoked and the sentinel all answer ONE not-found body.
+        // Absent, another tenant's, draft, revoked, deleted, expired and the sentinel all answer ONE not-found body.
         if (titleToFind && !documentId && !computedHash) {
           // The title is deliberately NOT echoed: echoing it would make the sentinel's not-found
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1623-title-lookup-summary-names-every-hidden-status.test.ts
@@ -0,0 +1,44 @@
+/**
+ * =============================================================================
+ * KS-1623 N3 - the title lookup's summary comment names every status the query hides
+ * =============================================================================
+ * The comment above the title strategy in routes/verification.ts lists what answers the ONE
+ * not-found body. KS-1114's follow-up made the query hide `deleted` and `expired` as well as `draft`
+ * and `revoked` (and the bullets above the summary say so), but the one-line summary kept the old
+ * list. The artefact under test IS that comment, so these cells read the route's own source text
+ * (as the other source-reading cells in this directory do) and compare the summary with the SQL.
+ * =============================================================================
+ */
+import * as fs from 'fs';
+import * as path from 'path';
+
+const SOURCE = fs.readFileSync(path.resolve(__dirname, '..', 'routes', 'verification.ts'), 'utf8');
+const SUMMARY_LINES = SOURCE.split('\n').filter((l) => /^\s*\/\/ Absent, another tenant's,.*not-found body\./.test(l));
+const SUMMARY = SUMMARY_LINES[0] || '';
+const HIDDEN = /lower\(btrim\(d\.status\)\) NOT IN \(([^)]*)\)/.exec(SOURCE);
+
+describe('KS-1623 N3 - the title lookup summary comment', () => {
+  it('CONTROL the instrument reads the real route: one summary line and the status predicate exist', () => {
+    expect(SUMMARY_LINES.length).toBe(1);
+    expect(HIDDEN).not.toBeNull();
+  });
+
+  it('CONTROL the query hides exactly draft, revoked, deleted and expired', () => {
+    const statuses = (HIDDEN ? HIDDEN[1] : '').split(',').map((s) => s.trim().replace(/'/g, ''));
+    expect(statuses).toEqual(['draft', 'revoked', 'deleted', 'expired']);
+  });
+
+  it('CONTROL the summary names absent, another tenant, draft, revoked and the sentinel', () => {
+    for (const must of ['Absent', "another tenant's", 'draft', 'revoked', 'sentinel']) {
+      expect({ must, present: SUMMARY.includes(must) }).toEqual({ must, present: true });
+    }
+  });
+
+  it('RED KS-1623 the summary comment names deleted', () => {
+    expect(SUMMARY).toContain('deleted');
+  });
+
+  it('RED KS-1623 the summary comment names expired', () => {
+    expect(SUMMARY).toContain('expired');
+  });
+});
```
