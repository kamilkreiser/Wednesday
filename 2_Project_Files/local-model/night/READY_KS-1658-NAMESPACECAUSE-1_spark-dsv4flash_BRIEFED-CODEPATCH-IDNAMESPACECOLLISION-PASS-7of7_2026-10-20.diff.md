# READY — KS-1658-NAMESPACECAUSE-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1658_p1/out.md.checker/patch.diff`** (from `ls` at 00:18 2026-10-20; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1658_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1658_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1658_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1658_p1-control/out.md.checker/patch.diff` rc 0, Wednesday (overnight 10-20)).

**Held 00:18 2026-10-20 by Wednesday (overnight 10-20) after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1658_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `bc3e2e2460fff5e961cd26b70da3ab0050fccbcc`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts , Blockchain/Dev/services/originate/src/__tests__/ks1658-an-unreadable-wrapper-does-not-hide-a-readable-refusal-in-its-cause.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1658-an-unreadable-wrapper-does-not-hide-a-readable-refusal-in-its-cause.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	1	Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts
62	0	Blockchain/Dev/services/originate/src/__tests__/ks1658-an-unreadable-wrapper-does-not-hide-a-readable-refusal-in-its-cause.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1658-an-unreadable-wrapper-does-not-hide-a-readable-refusal-in-its-cause.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1658-an-unreadable-wrapper-does-not-hide-a-readable-refusal-in-its-cause.test.ts fails at the untouched tip (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-1658 - an unreadable wrapper does not hide a readable refusal in its cause RED KS-1658 R1: an unreadable outer node around a real 050 refusal still reads as the 050 collision', 'KS-1658 - an unreadable wrapper does not hide a readable refusal in its cause RED KS-1658 R2: an unreadable outer node around a real 051 refusal still reads as the live-anchor claim', 'KS-1658 - an unreadable wrapper does not hide a readable refusal in its cause RED KS-1658 R3: a Proxy whose ownKeys throws, with a readable 050 refusal as its cause, still reads as the 050 collision']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1658-an-unreadable-wrapper-does-not-hide-a-readable-refusal-in-its-cause.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1510 failed=0 | after: total=1516 failed=0` · `NEW reds: []` [baseline_suite.json total=1510 failed=0; after_suite.json total=1516 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +64/-1 test=src/__tests__/ks1658-an-unreadable-wrapper-does-not-hide-a-readable-refusal-in-its-cause.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts` (+2/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1658-an-unreadable-wrapper-does-not-hide-a-readable-refusal-in-its-cause.test.ts` (+62/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `bc3e2e2460fff5e961cd26b70da3ab0050fccbcc` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1658_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1658_p1/KS-1658.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1658_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts b/Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts
index d7d3670bb..2d989b1e2 100644
--- a/Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts
+++ b/Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts
@@ -68,3 +68,4 @@
     // KS-1642: read every field this function uses once, up front. A node that cannot be read (a throwing getter, a Proxy trap) yields no record and is skipped, so nothing below can throw.
-    try { void [o.originalCode, o.code, o.constraint, o.originalMessage, o.message, Object.keys(o)]; } catch { return; }
+    // KS-1658: an unreadable node is skipped on its own, not with its subtree: a readable refusal in its `cause` is still found.
+    try { void [o.originalCode, o.code, o.constraint, o.originalMessage, o.message, Object.keys(o)]; } catch { try { visit(o.cause, depth + 1); } catch { /* the cause cannot be read either */ } return; }
     const sqlstate = str(o.originalCode) ?? str(o.code);
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1658-an-unreadable-wrapper-does-not-hide-a-readable-refusal-in-its-cause.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1658-an-unreadable-wrapper-does-not-hide-a-readable-refusal-in-its-cause.test.ts
new file mode 100644
index 000000000..de80ef606
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1658-an-unreadable-wrapper-does-not-hide-a-readable-refusal-in-its-cause.test.ts
@@ -0,0 +1,62 @@
+/**
+ * KS-1658 (gate AD1's N2 on #1618) - the read probe in idNamespaceCollision.ts skipped an unreadable node WITH its
+ * `cause` subtree, so a readable migration refusal nested inside an unreadable wrapper was no longer recognised
+ * and the caller answered 500 where 409 is correct. After the fix an unreadable node is skipped on its own and
+ * the walk still goes into its `cause`. The control cells keep what must not change: an unreadable wrapper around
+ * a non-refusal, or around a cause that cannot itself be read, answers false and never throws.
+ */
+import {
+  isIdNamespaceCollision,
+  isLiveAnchorIdClaim,
+  ID_NAMESPACE_CONSTRAINT,
+  LIVE_ANCHOR_ID_CONSTRAINT,
+  MIGRATION_MESSAGES,
+} from '../utils/idNamespaceCollision';
+
+const boom = (): never => { throw new Error('ks1658 unreadable'); };
+const refusal = (constraint: keyof typeof MIGRATION_MESSAGES) => ({
+  code: '23505',
+  constraint,
+  message: MIGRATION_MESSAGES[constraint],
+});
+const unreadableAround = (cause: unknown) => {
+  const outer = Object.defineProperty({ message: 'wrapper' }, 'code', { get: boom, enumerable: true });
+  return Object.defineProperty(outer, 'cause', { value: cause, enumerable: false });
+};
+
+describe('KS-1658 - an unreadable wrapper does not hide a readable refusal in its cause', () => {
+  it('RED KS-1658 R1: an unreadable outer node around a real 050 refusal still reads as the 050 collision', () => {
+    const err = unreadableAround(refusal(ID_NAMESPACE_CONSTRAINT));
+    expect(isIdNamespaceCollision(err)).toBe(true);
+    expect(isLiveAnchorIdClaim(err)).toBe(false);
+  });
+
+  it('RED KS-1658 R2: an unreadable outer node around a real 051 refusal still reads as the live-anchor claim', () => {
+    const err = unreadableAround(refusal(LIVE_ANCHOR_ID_CONSTRAINT));
+    expect(isLiveAnchorIdClaim(err)).toBe(true);
+    expect(isIdNamespaceCollision(err)).toBe(false);
+  });
+
+  it('RED KS-1658 R3: a Proxy whose ownKeys throws, with a readable 050 refusal as its cause, still reads as the 050 collision', () => {
+    const err = new Proxy({ code: '23505', cause: refusal(ID_NAMESPACE_CONSTRAINT) }, { ownKeys: boom });
+    expect(isIdNamespaceCollision(err)).toBe(true);
+  });
+
+  it('CONTROL KS-1658 C1: an unreadable outer node around some OTHER unique violation answers false', () => {
+    const err = unreadableAround({ code: '23505', constraint: 'documents_pkey', message: 'duplicate key' });
+    expect(isIdNamespaceCollision(err)).toBe(false);
+    expect(isLiveAnchorIdClaim(err)).toBe(false);
+  });
+
+  it('CONTROL KS-1658 C2: an unreadable outer node whose cause cannot be read either answers false and does not throw', () => {
+    const outer = Object.defineProperty({ message: 'wrapper' }, 'code', { get: boom, enumerable: true });
+    const err = Object.defineProperty(outer, 'cause', { get: boom, enumerable: false });
+    expect(() => isIdNamespaceCollision(err)).not.toThrow();
+    expect(isIdNamespaceCollision(err)).toBe(false);
+  });
+
+  it('CONTROL KS-1658 C3: an ordinary node-postgres 050 refusal is still recognised as 050 and not as 051', () => {
+    expect(isIdNamespaceCollision(refusal(ID_NAMESPACE_CONSTRAINT))).toBe(true);
+    expect(isLiveAnchorIdClaim(refusal(ID_NAMESPACE_CONSTRAINT))).toBe(false);
+  });
+});
```
