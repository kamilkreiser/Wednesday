# READY — KS-2163-O144-P1 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2163_o144_p1_originate_id_namespace_collision_unreadable_node_follows_its_other_children/out.md.checker/patch.diff`** (from `ls` at 22:24 2026-11-11; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2163_o144_p1_originate_id_namespace_collision_unreadable_node_follows_its_other_children/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2163_o144_p1_originate_id_namespace_collision_unreadable_node_follows_its_other_children/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_2163_o144_p1_originate_id_namespace_collision_unreadable_node_follows_its_other_children/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 22:24 2026-11-11 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2163_o144_p1_originate_id_namespace_collision_unreadable_node_follows_its_other_children/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `2e998b8d9aeaeaa6e87a35d933c6f0445bb981d4`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks2163-an-unreadable-node-still-yields-a-readable-refusal-under-its-other-children.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks2163-an-unreadable-node-still-yields-a-readable-refusal-under-its-other-children.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
11	1	Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts
91	0	Blockchain/Dev/services/originate/src/__tests__/ks2163-an-unreadable-node-still-yields-a-readable-refusal-under-its-other-children.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (11 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: idNamespaceCollision.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks2163-an-unreadable-node-still-yields-a-readable-refusal-under-its-other-children.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts 11 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks2163-an-unreadable-node-still-yields-a-readable-refusal-under-its-other-children.test.ts 91 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks2163-an-unreadable-node-still-yields-a-readable-refusal-under-its-other-children.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 10 run; controls green; assertion reds)` [red_first.json: failed=4 of total=10; red cell(s): ['KS-2163 - an unreadable node still yields a readable refusal under any of its own children RED ks2163 R1: a 050 refusal at meta.driverAdapterError.cause under an unreadable wrapper is found', 'KS-2163 - an unreadable node still yields a readable refusal under any of its own children RED ks2163 R2: a 050 refusal inside an errors array on an unreadable wrapper is found', 'KS-2163 - an unreadable node still yields a readable refusal under any of its own children RED ks2163 R3: a 051 refusal under an unreadable wrapper child is found as the live-anchor claim', 'KS-2163 - an unreadable node still yields a readable refusal under any of its own children RED ks2163 R4: a sibling child whose getter throws does not hide the readable refusal beside it']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (10 passed / 10 run)` [green_after.json: failed=0 of total=10, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2592 failed=11 | after: total=2602 failed=11` · `NEW reds: []` [baseline_suite.json total=2592 failed=11; after_suite.json total=2602 failed=11]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts` (+11/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks2163-an-unreadable-node-still-yields-a-readable-refusal-under-its-other-children.test.ts` (+91/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `2e998b8d9aeaeaa6e87a35d933c6f0445bb981d4` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2163_o144_p1_originate_id_namespace_collision_unreadable_node_follows_its_other_children/input.json`. Brief (given by --brief; its `# ` heading names KS-2163): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_2163_o144_p1_originate_id_namespace_collision_unreadable_node_follows_its_other_children/KS-2163.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2163_o144_p1_originate_id_namespace_collision_unreadable_node_follows_its_other_children/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts b/Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts
--- a/Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts
+++ b/Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts
@@ -69,3 +69,13 @@
     // KS-1658: an unreadable node is skipped on its own, not with its subtree: a readable refusal in its `cause` is still found.
-    try { void [o.originalCode, o.code, o.constraint, o.originalMessage, o.message, Object.keys(o)]; } catch { try { visit(o.cause, depth + 1); } catch { /* the cause cannot be read either */ } return; }
+    try { void [o.originalCode, o.code, o.constraint, o.originalMessage, o.message, Object.keys(o)]; } catch {
+      try { visit(o.cause, depth + 1); } catch { /* the cause cannot be read either */ }
+      // KS-2163: the node's OTHER own enumerable children are followed too, each read in its own try, so a readable refusal under any of them is still found.
+      let keys: string[] = [];
+      try { keys = Object.keys(o); } catch { /* the own keys cannot be listed */ }
+      for (const key of keys) {
+        if (key === 'cause') continue;
+        try { visit(o[key], depth + 1); } catch { /* this child cannot be read */ }
+      }
+      return;
+    }
     const sqlstate = str(o.originalCode) ?? str(o.code);
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks2163-an-unreadable-node-still-yields-a-readable-refusal-under-its-other-children.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks2163-an-unreadable-node-still-yields-a-readable-refusal-under-its-other-children.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks2163-an-unreadable-node-still-yields-a-readable-refusal-under-its-other-children.test.ts
@@ -0,0 +1,91 @@
+/**
+ * KS-2163 (gate AU1's N2 on #1634, KS-1658) - when the read probe in idNamespaceCollision.ts finds a node it cannot read (a throwing
+ * getter, a Proxy trap), it follows only that node's `cause`. A readable migration 050 or 051 refusal under any OTHER child of that
+ * node (`meta.driverAdapterError.cause` under a Prisma wrapper, an `errors` array on an AggregateError) is not recognised, and the
+ * caller answers 500 where 409 is correct. After the fix an unreadable node also contributes its other own enumerable children, each
+ * read in its own try, with the same depth bound and seen-set. The control cells keep what must not change.
+ */
+import {
+  isIdNamespaceCollision,
+  isLiveAnchorIdClaim,
+  ID_NAMESPACE_CONSTRAINT,
+  LIVE_ANCHOR_ID_CONSTRAINT,
+  MIGRATION_MESSAGES,
+} from '../utils/idNamespaceCollision';
+
+const boom = (): never => { throw new Error('ks2163 unreadable'); };
+const refusal = (constraint: keyof typeof MIGRATION_MESSAGES) => ({
+  code: '23505',
+  constraint,
+  message: MIGRATION_MESSAGES[constraint],
+});
+// An outer node whose `code` getter throws (so the up-front read fails), carrying the given children as own enumerable properties.
+const unreadableWith = (children: Record<string, unknown>) => {
+  const outer: Record<string, unknown> = { message: 'wrapper' };
+  Object.defineProperty(outer, 'code', { get: boom, enumerable: true });
+  for (const [key, value] of Object.entries(children)) {
+    Object.defineProperty(outer, key, { value, enumerable: true });
+  }
+  return outer;
+};
+
+describe('KS-2163 - an unreadable node still yields a readable refusal under any of its own children', () => {
+  it('RED ks2163 R1: a 050 refusal at meta.driverAdapterError.cause under an unreadable wrapper is found', () => {
+    const err = unreadableWith({ meta: { driverAdapterError: { name: 'DriverAdapterError', cause: refusal(ID_NAMESPACE_CONSTRAINT) } } });
+    expect(isIdNamespaceCollision(err)).toBe(true);
+    expect(isLiveAnchorIdClaim(err)).toBe(false);
+  });
+
+  it('RED ks2163 R2: a 050 refusal inside an errors array on an unreadable wrapper is found', () => {
+    const err = unreadableWith({ errors: [{ message: 'other' }, refusal(ID_NAMESPACE_CONSTRAINT)] });
+    expect(isIdNamespaceCollision(err)).toBe(true);
+  });
+
+  it('RED ks2163 R3: a 051 refusal under an unreadable wrapper child is found as the live-anchor claim', () => {
+    const err = unreadableWith({ inner: refusal(LIVE_ANCHOR_ID_CONSTRAINT) });
+    expect(isLiveAnchorIdClaim(err)).toBe(true);
+    expect(isIdNamespaceCollision(err)).toBe(false);
+  });
+
+  it('RED ks2163 R4: a sibling child whose getter throws does not hide the readable refusal beside it', () => {
+    const err = unreadableWith({ inner: refusal(ID_NAMESPACE_CONSTRAINT) });
+    Object.defineProperty(err, 'broken', { get: boom, enumerable: true });
+    expect(isIdNamespaceCollision(err)).toBe(true);
+  });
+
+  it('control ks2163 C1: an unreadable wrapper whose child holds some OTHER unique violation answers false', () => {
+    const err = unreadableWith({ inner: { code: '23505', constraint: 'documents_pkey', message: 'duplicate key' } });
+    expect(isIdNamespaceCollision(err)).toBe(false);
+    expect(isLiveAnchorIdClaim(err)).toBe(false);
+  });
+
+  it('control ks2163 C2: an unreadable wrapper with an unreadable child and no refusal answers false and does not throw', () => {
+    const err = unreadableWith({});
+    Object.defineProperty(err, 'broken', { get: boom, enumerable: true });
+    expect(() => isIdNamespaceCollision(err)).not.toThrow();
+    expect(isIdNamespaceCollision(err)).toBe(false);
+  });
+
+  it('control ks2163 C3: a Proxy whose ownKeys throws and which holds no refusal answers false and does not throw', () => {
+    const err = new Proxy({ code: '23505' }, { ownKeys: boom });
+    expect(() => isIdNamespaceCollision(err)).not.toThrow();
+    expect(isIdNamespaceCollision(err)).toBe(false);
+  });
+
+  it('control ks2163 C4: an ordinary node-postgres 050 refusal is still recognised as 050 and not as 051', () => {
+    expect(isIdNamespaceCollision(refusal(ID_NAMESPACE_CONSTRAINT))).toBe(true);
+    expect(isLiveAnchorIdClaim(refusal(ID_NAMESPACE_CONSTRAINT))).toBe(false);
+  });
+
+  it('control ks2163 C5: the depth bound still applies through the child path (a refusal behind five unreadable wrappers is NOT found)', () => {
+    let node: unknown = refusal(ID_NAMESPACE_CONSTRAINT);
+    for (let i = 0; i < 5; i += 1) node = unreadableWith({ inner: node });
+    expect(isIdNamespaceCollision(node)).toBe(false);
+  });
+
+  it('control ks2163 C6: a cyclic unreadable wrapper terminates and answers false', () => {
+    const err = unreadableWith({});
+    Object.defineProperty(err, 'self', { value: err, enumerable: true });
+    expect(isIdNamespaceCollision(err)).toBe(false);
+  });
+});
```

> NOTE (operator o144, 2026-11-11): TIER 2 (a boolean helper behind the 409 mapping). The ticket's alternative outcome (accept N2 and close) is Wednesday's decision; this PASS is the candidate for the build outcome. ONE replaced line (70) becomes a multi-line catch. Wednesday: read the + lines (golden = mine, byte-identical). UNMEASURED: no real driver produces the shape; routes not exercised end to end. Load1 was 23-29 for the real round (other seats, whole-service run included); A6 originate suite 2592 -> 2602, 11 baseline reds unchanged, 0 new.
