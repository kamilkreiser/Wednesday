# READY — KS-1642-READPROBE-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1642_p1/out.md.checker/patch.diff`** (from `ls` at 17:15 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1642_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1642_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1642_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1642_p1-control-r2/out.md.checker/patch.diff` rc 0, Wednesday 16:3x seat).

**Held 17:15 2026-10-19 by Wednesday 16:3x seat after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1642_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `722e07f19cee683ea037930e601e380a9491f7b5`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts , Blockchain/Dev/services/originate/src/__tests__/ks1642-the-409-mapping-helpers-never-throw-on-an-unreadable-error-shape.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1642-the-409-mapping-helpers-never-throw-on-an-unreadable-error-shape.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	0	Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts
53	0	Blockchain/Dev/services/originate/src/__tests__/ks1642-the-409-mapping-helpers-never-throw-on-an-unreadable-error-shape.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (3 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 3 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts byte-exact incl. leading whitespace (apply mode strict): OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)` [a3i_indent.out: `OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1642-the-409-mapping-helpers-never-throw-on-an-unreadable-error-shape.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1642-the-409-mapping-helpers-never-throw-on-an-unreadable-error-shape.test.ts fails at the untouched tip (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1642 - the 409 mapping helpers never throw on an unreadable error shape RED KS-1642 G1: a throwing getter on the outer code answers false instead of throwing', "KS-1642 - the 409 mapping helpers never throw on an unreadable error shape RED KS-1642 G3: a throwing getter on a cause's originalMessage answers false instead of throwing", 'KS-1642 - the 409 mapping helpers never throw on an unreadable error shape RED KS-1642 G4: a Proxy whose ownKeys throws answers false instead of throwing']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1642-the-409-mapping-helpers-never-throw-on-an-unreadable-error-shape.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1481 failed=0 | after: total=1486 failed=0` · `NEW reds: []` [baseline_suite.json total=1481 failed=0; after_suite.json total=1486 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +56/-0 test=src/__tests__/ks1642-the-409-mapping-helpers-never-throw-on-an-unreadable-error-shape.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts` (+3/-0 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1642-the-409-mapping-helpers-never-throw-on-an-unreadable-error-shape.test.ts` (+53/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `722e07f19cee683ea037930e601e380a9491f7b5` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1642_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1642_p1/KS-1642.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1642_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts b/Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts
index bb0cd29dd..d7d3670bb 100644
--- a/Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts
+++ b/Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts
@@ -67,2 +67,4 @@
     const o = node as Record<string, unknown>;
+    // KS-1642: read every field this function uses once, up front. A node that cannot be read (a throwing getter, a Proxy trap) yields no record and is skipped, so nothing below can throw.
+    try { void [o.originalCode, o.code, o.constraint, o.originalMessage, o.message, Object.keys(o)]; } catch { return; }
     const sqlstate = str(o.originalCode) ?? str(o.code);
@@ -73,2 +75,3 @@
       let child: unknown;
+      // KS-1642: an unreadable child cannot be a driver record we need; skip it, never fail the mapping.
       try { child = o[key]; } catch { continue; }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1642-the-409-mapping-helpers-never-throw-on-an-unreadable-error-shape.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1642-the-409-mapping-helpers-never-throw-on-an-unreadable-error-shape.test.ts
new file mode 100644
index 000000000..eb386cdc7
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1642-the-409-mapping-helpers-never-throw-on-an-unreadable-error-shape.test.ts
@@ -0,0 +1,53 @@
+/**
+ * KS-1642 (gate P1's MIN-2 on #1568) - idNamespaceCollision.ts promises "Nothing here throws on an unexpected shape",
+ * but a throwing getter on the outer `code` (G1), on a cause's `originalMessage` (G3), or a Proxy whose `ownKeys` throws
+ * (G4) made the helper THROW, and a throw there escapes the route's catch and becomes the outer 500. After the fix each
+ * of those answers false. The control cells keep what must not change: a record is still found when an UNRELATED child
+ * has a throwing getter (H10, the `try` around a child read), and an ordinary refusal is still recognised.
+ */
+import {
+  isIdNamespaceCollision,
+  isLiveAnchorIdClaim,
+  ID_NAMESPACE_CONSTRAINT,
+  MIGRATION_MESSAGES,
+} from '../utils/idNamespaceCollision';
+
+const boom = (): never => { throw new Error('ks1642 unreadable'); };
+const refusal = () => ({
+  code: '23505',
+  constraint: ID_NAMESPACE_CONSTRAINT,
+  message: MIGRATION_MESSAGES[ID_NAMESPACE_CONSTRAINT],
+});
+
+describe('KS-1642 - the 409 mapping helpers never throw on an unreadable error shape', () => {
+  it('RED KS-1642 G1: a throwing getter on the outer code answers false instead of throwing', () => {
+    const err = Object.defineProperty({ message: 'x' }, 'code', { get: boom, enumerable: true });
+    expect(() => isIdNamespaceCollision(err)).not.toThrow();
+    expect(isIdNamespaceCollision(err)).toBe(false);
+    expect(isLiveAnchorIdClaim(err)).toBe(false);
+  });
+
+  it('RED KS-1642 G3: a throwing getter on a cause\'s originalMessage answers false instead of throwing', () => {
+    const cause = Object.defineProperty({ originalCode: '23505' }, 'originalMessage', { get: boom, enumerable: true });
+    const err = { code: 'P2010', cause };
+    expect(() => isIdNamespaceCollision(err)).not.toThrow();
+    expect(isIdNamespaceCollision(err)).toBe(false);
+  });
+
+  it('RED KS-1642 G4: a Proxy whose ownKeys throws answers false instead of throwing', () => {
+    const err = new Proxy({ code: '23505' }, { ownKeys: boom });
+    expect(() => isIdNamespaceCollision(err)).not.toThrow();
+    expect(isIdNamespaceCollision(err)).toBe(false);
+  });
+
+  it('CONTROL KS-1642 H10: a throwing getter on an UNRELATED child does not hide the refusal record', () => {
+    const err = Object.defineProperty(refusal(), 'unrelated', { get: boom, enumerable: true });
+    expect(isIdNamespaceCollision(err)).toBe(true);
+    expect(isLiveAnchorIdClaim(err)).toBe(false);
+  });
+
+  it('CONTROL KS-1642 C1: an ordinary node-postgres refusal is still recognised as 050 and not as 051', () => {
+    expect(isIdNamespaceCollision(refusal())).toBe(true);
+    expect(isLiveAnchorIdClaim(refusal())).toBe(false);
+  });
+});
```
