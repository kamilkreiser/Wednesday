# READY — KS-1840-KS-1840-STALECITATION (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1840_p1_stale_citation/out.md.checker/patch.diff`** (from `ls` at 05:06 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1840_p1_stale_citation/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1840_p1_stale_citation/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1840_p1_stale_citation/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 05:06 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1840_p1_stale_citation/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `429ba4824915f02bb4f7e80c4704921cbdde2a08`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/anchoring/src/index.ts } + { Blockchain/Dev/services/anchoring/src/__tests__/ks1840-stale-gateway-citation-is-gone.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/anchoring/src/index.ts` (product) and `Blockchain/Dev/services/anchoring/src/__tests__/ks1840-stale-gateway-citation-is-gone.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	3	Blockchain/Dev/services/anchoring/src/index.ts
32	0	Blockchain/Dev/services/anchoring/src/__tests__/ks1840-stale-gateway-citation-is-gone.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (3 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/anchoring/src/index.ts`; test(s): `Blockchain/Dev/services/anchoring/src/__tests__/ks1840-stale-gateway-citation-is-gone.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/anchoring/src/index.ts 3 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/anchoring/src/__tests__/ks1840-stale-gateway-citation-is-gone.test.ts 32 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1840-stale-gateway-citation-is-gone.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1840: no comment or doc row cites the retired gateway function RED KS-1840 R1 index.ts no longer cites the retired gateway function', 'KS-1840: no comment or doc row cites the retired gateway function RED KS-1840 R2 index.ts says the cited function was retired in KS-1628 and the caller question is not measured']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=537 failed=1 | after: total=542 failed=1` · `NEW reds: []` [baseline_suite.json total=537 failed=1; after_suite.json total=542 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/anchoring/src/index.ts` (+3/-3 per numstat.out) and the test file `Blockchain/Dev/services/anchoring/src/__tests__/ks1840-stale-gateway-citation-is-gone.test.ts` (+32/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/anchoring/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `429ba4824915f02bb4f7e80c4704921cbdde2a08` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1840_p1_stale_citation/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1840_p1_stale_citation/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/anchoring/src/index.ts b/Blockchain/Dev/services/anchoring/src/index.ts
--- a/Blockchain/Dev/services/anchoring/src/index.ts
+++ b/Blockchain/Dev/services/anchoring/src/index.ts
@@ -980,9 +980,9 @@
  * That's id-reflection — enabling enumeration ("did this id exist or not?")
  * and giving an attacker confirmation that their guess landed on a syntactic
  * shape the API will accept. Now: 404 with no echoed id when no anchors
- * match. Gateway callers already handle non-200 by resolving null
- * (see makeFetchDocFromAnchorStore in api-gateway/src/routes/verification.ts),
- * so the verifier-portal flow is unaffected.
+ * match. The gateway function once cited here as the caller that handles a
+ * non-200 was retired in KS-1628. Whether a current caller treats a 404 from
+ * this route as no anchor is not measured (KS-1840).
  */
 app.get('/api/anchors/document/:documentId', async (req: Request, res: Response) => {
   const dbResults = await dbGetAnchorsByDocument(req.params.documentId);
diff --git a/Blockchain/Dev/services/anchoring/src/__tests__/ks1840-stale-gateway-citation-is-gone.test.ts b/Blockchain/Dev/services/anchoring/src/__tests__/ks1840-stale-gateway-citation-is-gone.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1840-stale-gateway-citation-is-gone.test.ts
@@ -0,0 +1,32 @@
+// KS-1840 (anchoring): the block comment above GET /api/anchors/document/:documentId in index.ts, and the struck-through H2 row of DEVELOPMENT.md, cited a gateway function
+// (the one that "already handles non-200 by resolving null") that was retired in KS-1628. These cells read index.ts as text (the DEVELOPMENT.md row is a separate, doc-only follow-up: the Spark builder measures one service per brief).
+// R1 and R2 are red until the stale citation is replaced; C1 to C3 pin what must not move.
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'fs';
+import { resolve } from 'path';
+
+const INDEX_SRC = readFileSync(resolve(__dirname, '..', 'index.ts'), 'utf8');
+
+describe('KS-1840: no comment or doc row cites the retired gateway function', () => {
+  it('RED KS-1840 R1 index.ts no longer cites the retired gateway function', () => {
+    expect(INDEX_SRC).not.toContain('makeFetchDocFromAnchorStore');
+  });
+
+  it('RED KS-1840 R2 index.ts says the cited function was retired in KS-1628 and the caller question is not measured', () => {
+    expect(INDEX_SRC).toContain('was retired in KS-1628');
+    expect(INDEX_SRC).toContain('is not measured (KS-1840)');
+  });
+
+  it('control KS-1840 C1 the route comment still explains the 404 with no echoed id', () => {
+    expect(INDEX_SRC).toContain('BACKLOG H2 (was F-API-01 part 2)');
+    expect(INDEX_SRC).toContain('* GET /api/anchors/document/:documentId');
+  });
+
+  it('control KS-1840 C2 the route handler line is untouched', () => {
+    expect(INDEX_SRC).toContain("app.get('/api/anchors/document/:documentId', async (req: Request, res: Response) => {");
+  });
+
+  it('control KS-1840 C3 the file was read (the instrument is not reading an empty string)', () => {
+    expect(INDEX_SRC.length).toBeGreaterThan(5000);
+  });
+});
```
