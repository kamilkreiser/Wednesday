# READY — KS-1642-H9PIN-2 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1642_p2/out.md.checker/patch.diff`** (from `ls` at 17:15 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1642_p2/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1642_p2-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) identical in every file; hunk headers identical; APPLIED RESULT IDENTICAL: both patches applied strictly (`git apply -p1`, scratch tempdir) to the tip content carried in input.json['files'] yield byte-identical files (ks1612-409-mapping-survives-the-prisma-error-shape.test.ts, sha256 equal).

**Held 17:15 2026-10-19 by Wednesday 16:3x seat after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1642_p2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `722e07f19cee683ea037930e601e380a9491f7b5`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/originate/src/__tests__/ks1612-409-mapping-survives-the-prisma-error-shape.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/originate/src/__tests__/ks1612-409-mapping-survives-the-prisma-error-shape.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
14	0	Blockchain/Dev/services/originate/src/__tests__/ks1612-409-mapping-survives-the-prisma-error-shape.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (12 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 14 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/__tests__/ks1612-409-mapping-survives-the-prisma-error-shape.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 12 line(s) byte-exact incl. leading whitespace (of 12; 14 line(s) added by the apply)` [a3i_indent.out: `OK 12 line(s) byte-exact incl. leading whitespace (of 12; 14 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `7be1f1dd35d52062` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts:84)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-19_ks_1642_p2_170802/clone/Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts:84: '    && (r.constraint === constraint || (r.constraint === null && r.message === MIGRATION_MESSAGES[constraint])));' -> '    && (r.constraint === constraint || (r.message === MIGRATION_MESSAGES[constraint])));'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 84. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1612-409-mapping-survives-the-prisma-error-shape.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1612-409-mapping-survives-the-prisma-error-shape.test.ts fails at the untouched tip (1 failed / 15 run; controls green; assertion reds)` [red_first.json: failed=1 of total=15; red cell(s): ["KS-1612 MIN-A — 050 and 051 map to 409 through BOTH driver shapes RED KS-1642 H9: a 23505 that names ANOTHER constraint is not a migration refusal, even with a migration's exact message"]]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1612-409-mapping-survives-the-prisma-error-shape.test.ts passes with the product hunk (15 passed / 15 run)` [green_after.json: failed=0 of total=15, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1481 failed=0 | after: total=1483 failed=0` · `NEW reds: []` [baseline_suite.json total=1481 failed=0; after_suite.json total=1483 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +14/-0 test=src/__tests__/ks1612-409-mapping-survives-the-prisma-error-shape.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/originate/src/__tests__/ks1612-409-mapping-survives-the-prisma-error-shape.test.ts` (+14/-0 per numstat.out); the product `Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts` is the tamper target and is byte-unchanged (sha256 7be1f1dd35d52062, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `722e07f19cee683ea037930e601e380a9491f7b5` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1642_p2/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1642_p2/KS-1642.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1642_p2/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1612-409-mapping-survives-the-prisma-error-shape.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1612-409-mapping-survives-the-prisma-error-shape.test.ts
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1612-409-mapping-survives-the-prisma-error-shape.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1612-409-mapping-survives-the-prisma-error-shape.test.ts
@@ -115,2 +115,16 @@
   });
+
+  // KS-1642 (gate P1 mutant H9): the `r.constraint === null` guard in isMigrationRefusal. A node-postgres 23505 that names
+  // ANOTHER constraint must not be taken for a migration's refusal just because its message equals that migration's RAISE text.
+  it('RED KS-1642 H9: a 23505 that names ANOTHER constraint is not a migration refusal, even with a migration\'s exact message', () => {
+    for (const constraint of [ID_NAMESPACE_CONSTRAINT, LIVE_ANCHOR_ID_CONSTRAINT] as const) {
+      const other = { code: '23505', constraint: 'documents_external_id_key', message: MIGRATION_MESSAGES[constraint] };
+      expect([isIdNamespaceCollision(other), isLiveAnchorIdClaim(other)]).toEqual([false, false]);
+    }
+  });
+
+  it('CONTROL KS-1642 H9c: the same exact message with NO constraint field (the Prisma shape) is still that migration\'s refusal', () => {
+    const noConstraint = { code: '23505', message: MIGRATION_MESSAGES[ID_NAMESPACE_CONSTRAINT] };
+    expect([isIdNamespaceCollision(noConstraint), isLiveAnchorIdClaim(noConstraint)]).toEqual([true, false]);
+  });
 });
```
