# READY — KS-1868-KS-1868-O87-P3 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p3_anchoring_status_update_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 01:31 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p3_anchoring_status_update_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p3_anchoring_status_update_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p3_anchoring_status_update_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p3_anchoring_status_update_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 01:31 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p3_anchoring_status_update_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8150eeb3802bd9cfe5242ffbc49278c1a3739a84`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/anchoring/src/anchorStatusUpdate.ts } + { Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchor-status-update-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/anchoring/src/anchorStatusUpdate.ts` (product) and `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchor-status-update-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	1	Blockchain/Dev/services/anchoring/src/anchorStatusUpdate.ts
106	0	Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchor-status-update-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: anchorStatusUpdate.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/anchoring/src/anchorStatusUpdate.ts`; test(s): `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchor-status-update-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/anchoring/src/anchorStatusUpdate.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchor-status-update-catch-unreadable-throw.test.ts 106 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/anchorStatusUpdate.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchor-status-update-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=3 of total=7; red cell(s): ['KS-1868 runAnchorStatusUpdate answers null and logs text for a hostile thrown value RED ks1868 R1: a revoked Proxy from the query resolves null and is logged as text, as for an ordinary Error', 'KS-1868 runAnchorStatusUpdate answers null and logs text for a hostile thrown value RED ks1868 R2: an Error whose message getter throws resolves null and is logged as text, as for an ordinary Error', 'KS-1868 runAnchorStatusUpdate answers null and logs text for a hostile thrown value RED ks1868 R3: an Error whose message is a Symbol resolves null and is logged as text, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=760 failed=1 | after: total=767 failed=1` · `NEW reds: []` [baseline_suite.json total=760 failed=1; after_suite.json total=767 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/anchoring/src/anchorStatusUpdate.ts` (+8/-1 per numstat.out) and the test file `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchor-status-update-catch-unreadable-throw.test.ts` (+106/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/anchoring/src/anchorStatusUpdate.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8150eeb3802bd9cfe5242ffbc49278c1a3739a84` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p3_anchoring_status_update_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o87_p3_anchoring_status_update_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p3_anchoring_status_update_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/anchoring/src/anchorStatusUpdate.ts b/Blockchain/Dev/services/anchoring/src/anchorStatusUpdate.ts
--- a/Blockchain/Dev/services/anchoring/src/anchorStatusUpdate.ts
+++ b/Blockchain/Dev/services/anchoring/src/anchorStatusUpdate.ts
@@ -222,7 +222,14 @@
     }
     return affected;
   } catch (err: any) {
-    deps.log('warn', 'Failed to update anchor status in DB', { anchorId, error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    deps.log('warn', 'Failed to update anchor status in DB', { anchorId, error: reason });
     return null;
   }
 }
diff --git a/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchor-status-update-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchor-status-update-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchor-status-update-catch-unreadable-throw.test.ts
@@ -0,0 +1,106 @@
+import { describe, it, expect } from 'vitest';
+import { runAnchorStatusUpdate, type RunStatusUpdateDeps } from '../anchorStatusUpdate';
+
+// KS-1868 (operator 87 screen, anchoring anchorStatusUpdate module): the catch of runAnchorStatusUpdate (line 225) passes
+// `err?.message` straight into the injected log call's meta object, unguarded. A thrown value whose read throws (a revoked
+// Proxy, an Error whose message getter throws) makes the catch itself throw, so runAnchorStatusUpdate REJECTS instead of
+// answering null as its contract says ("the statement threw" is null, logged at warn, never rethrown); an Error whose message
+// is not a string (a Symbol) is passed to the log uncoerced. The cells make the injected query reject with such a value and
+// assert the call resolves null and the warn line carries text (the constant when the value cannot be turned into text).
+// Harness: the real module; the four dependencies are plain functions (no database, no network).
+type Line = { level: string; message: string; meta: Record<string, unknown> | undefined };
+
+function deps(query: () => Promise<unknown>, lines: Line[]): RunStatusUpdateDeps {
+  return {
+    isDbAvailable: () => true,
+    ensureTables: async () => undefined,
+    query,
+    log: (level, message, meta) => {
+      lines.push({ level, message, meta });
+    },
+  };
+}
+async function run(failure: { value: unknown } | undefined): Promise<{ ok: boolean; value: number | null | undefined; lines: Line[] }> {
+  const lines: Line[] = [];
+  const query = async (): Promise<unknown> => {
+    if (failure) throw failure.value;
+    return { rowCount: 1 };
+  };
+  try {
+    return { ok: true, value: await runAnchorStatusUpdate(deps(query, lines), 'anchor-1', { status: 'failed' }), lines };
+  } catch {
+    return { ok: false, value: undefined, lines };
+  }
+}
+const FAILED = 'Failed to update anchor status in DB';
+const failedLines = (lines: Line[]): Line[] => lines.filter((l) => l.message === FAILED);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (l: Line | undefined): string => (typeof l?.meta?.error === 'string' ? (l.meta.error as string) : '<' + typeof l?.meta?.error + '>');
+
+const revokedProxy = (): unknown => {
+  const rp = Proxy.revocable({}, {});
+  rp.revoke();
+  return rp.proxy;
+};
+/** An Error whose `message` getter succeeds and returns the value m. */
+const withMessage = (m: unknown): unknown => Object.create(Error.prototype, { message: { get() { return m; } } });
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+describe('KS-1868 runAnchorStatusUpdate answers null and logs text for a hostile thrown value', () => {
+  it('control ks1868 C1: an update that matches a row resolves its row count and logs no failure', async () => {
+    const r = await run(undefined);
+    expect(r.ok).toBe(true);
+    expect(r.value).toBe(1);
+    expect(failedLines(r.lines)).toHaveLength(0);
+  });
+  it('control ks1868 C2: an ordinary Error from the query resolves null and is logged at warn with its message', async () => {
+    const r = await run({ value: new Error('update boom') });
+    expect(r.ok).toBe(true);
+    expect(r.value).toBeNull();
+    expect(failedLines(r.lines)).toHaveLength(1);
+    expect(failedLines(r.lines)[0].level).toBe('warn');
+    expect(reasonOf(failedLines(r.lines)[0])).toBe('update boom');
+  });
+  it('control ks1868 C3: a thrown plain string resolves null and is logged without a message', async () => {
+    const r = await run({ value: 'plain boom' });
+    expect(r.ok).toBe(true);
+    expect(r.value).toBeNull();
+    expect(failedLines(r.lines)).toHaveLength(1);
+    expect(reasonOf(failedLines(r.lines)[0])).toBe('<undefined>');
+  });
+  it('control ks1868 C4: a thrown number resolves null and is logged without a message', async () => {
+    const r = await run({ value: 42 });
+    expect(r.ok).toBe(true);
+    expect(r.value).toBeNull();
+    expect(failedLines(r.lines)).toHaveLength(1);
+    expect(reasonOf(failedLines(r.lines)[0])).toBe('<undefined>');
+  });
+  it('RED ks1868 R1: a revoked Proxy from the query resolves null and is logged as text, as for an ordinary Error', async () => {
+    const r = await run({ value: revokedProxy() });
+    expect(r.ok).toBe(true);
+    expect(r.value).toBeNull();
+    expect(failedLines(r.lines)).toHaveLength(1);
+    expect(reasonOf(failedLines(r.lines)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message getter throws resolves null and is logged as text, as for an ordinary Error', async () => {
+    const r = await run({ value: getterThrows() });
+    expect(r.ok).toBe(true);
+    expect(r.value).toBeNull();
+    expect(failedLines(r.lines)).toHaveLength(1);
+    expect(reasonOf(failedLines(r.lines)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R3: an Error whose message is a Symbol resolves null and is logged as text, as for an ordinary Error', async () => {
+    const r = await run({ value: withMessage(Symbol('ks1868')) });
+    expect(r.ok).toBe(true);
+    expect(r.value).toBeNull();
+    expect(failedLines(r.lines)).toHaveLength(1);
+    expect(reasonOf(failedLines(r.lines)[0])).toBe('Symbol(ks1868)');
+  });
+});
```
