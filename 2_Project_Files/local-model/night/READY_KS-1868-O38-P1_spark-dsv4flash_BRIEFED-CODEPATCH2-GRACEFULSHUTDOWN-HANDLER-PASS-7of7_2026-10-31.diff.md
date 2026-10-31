# READY — KS-1868-O38-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o38_p1_shared_gracefulshutdown_unhandled_rejection_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 14:44 2026-10-31; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o38_p1_shared_gracefulshutdown_unhandled_rejection_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o38_p1_shared_gracefulshutdown_unhandled_rejection_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o38_p1_shared_gracefulshutdown_unhandled_rejection_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o38_p1_shared_gracefulshutdown_unhandled_rejection_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 14:44 2026-10-31 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o38_p1_shared_gracefulshutdown_unhandled_rejection_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `9e1eb55fde5338d0ad95848736cbd013d7b7f651`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/packages/shared/src/utils/gracefulShutdown.ts } + { Blockchain/Dev/packages/shared/src/__tests__/ks1868-unhandled-rejection-handler-unreadable-reason.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/packages/shared/src/utils/gracefulShutdown.ts` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks1868-unhandled-rejection-handler-unreadable-reason.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	2	Blockchain/Dev/packages/shared/src/utils/gracefulShutdown.ts
66	0	Blockchain/Dev/packages/shared/src/__tests__/ks1868-unhandled-rejection-handler-unreadable-reason.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: gracefulShutdown.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/packages/shared/src/utils/gracefulShutdown.ts`; test(s): `Blockchain/Dev/packages/shared/src/__tests__/ks1868-unhandled-rejection-handler-unreadable-reason.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/packages/shared/src/utils/gracefulShutdown.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/packages/shared/src/__tests__/ks1868-unhandled-rejection-handler-unreadable-reason.test.ts 66 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/packages/shared/src/utils/gracefulShutdown.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks1868-unhandled-rejection-handler-unreadable-reason.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 3 run; controls green; assertion reds)` [red_first.json: failed=2 of total=3; red cell(s): ['KS-1868 unhandledRejection handler reads the reason safely RED ks1868 R1 a revoked Proxy reason is logged as a constant in survive mode, without throwing', 'KS-1868 unhandledRejection handler reads the reason safely RED ks1868 R2 an Error whose message getter throws is logged as a constant and still shuts down in exit mode']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (3 passed / 3 run)` [green_after.json: failed=0 of total=3, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1081 failed=2 | after: total=1084 failed=1` · `NEW reds: []` [baseline_suite.json total=1081 failed=2; after_suite.json total=1084 failed=1]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/packages/shared/src/utils/gracefulShutdown.ts` (+8/-2 per numstat.out) and the test file `Blockchain/Dev/packages/shared/src/__tests__/ks1868-unhandled-rejection-handler-unreadable-reason.test.ts` (+66/-0); 2 files in all (code_patch2: products Blockchain/Dev/packages/shared/src/utils/gracefulShutdown.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `9e1eb55fde5338d0ad95848736cbd013d7b7f651` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o38_p1_shared_gracefulshutdown_unhandled_rejection_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o38_p1_shared_gracefulshutdown_unhandled_rejection_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o38_p1_shared_gracefulshutdown_unhandled_rejection_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/packages/shared/src/utils/gracefulShutdown.ts b/Blockchain/Dev/packages/shared/src/utils/gracefulShutdown.ts
--- a/Blockchain/Dev/packages/shared/src/utils/gracefulShutdown.ts
+++ b/Blockchain/Dev/packages/shared/src/utils/gracefulShutdown.ts
@@ -49,8 +49,14 @@
 }): (reason: unknown, promise: Promise<unknown>) => void {
   let survived = 0;
   return (reason: unknown) => {
-    const detail =
-      reason instanceof Error ? `${reason.message}\n${reason.stack ?? ''}` : String(reason);
+    let detail: string;
+    try {
+      detail = reason instanceof Error
+        ? `${reason.message}\n${reason.stack ?? ''}`
+        : String(reason);
+    } catch {
+      detail = 'unreadable thrown value';
+    }
     if (ctx.mode === 'survive') {
       survived++;
       ctx.logger(
diff --git a/Blockchain/Dev/packages/shared/src/__tests__/ks1868-unhandled-rejection-handler-unreadable-reason.test.ts b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-unhandled-rejection-handler-unreadable-reason.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-unhandled-rejection-handler-unreadable-reason.test.ts
@@ -0,0 +1,66 @@
+import { describe, it, expect } from 'vitest';
+import { createUnhandledRejectionHandler } from '../utils/gracefulShutdown';
+
+// KS-1868: the unhandledRejection handler must still log (and still shut down in 'exit' mode)
+// when the rejection reason itself cannot be read (a revoked Proxy throws on `instanceof`; an
+// Error whose `message` getter throws, throws on `.message`). Today the handler itself throws,
+// which in 'survive' mode (the api-gateway) turns one bad rejection into the outage KS-546 prevents.
+// The logger and shutdown stand-ins are plain functions, not vi.fn(): a spy could inspect a
+// revoked Proxy and fail before the code under test saw it.
+
+type Outcome = { threw: boolean; logs: string[]; shutdowns: string[] };
+
+function run(mode: 'exit' | 'survive', reason: unknown): Outcome {
+  const out: Outcome = { threw: false, logs: [], shutdowns: [] };
+  const handler = createUnhandledRejectionHandler({
+    serviceName: 'svc',
+    mode,
+    logger: (m: string) => {
+      out.logs.push(m);
+    },
+    shutdown: (s: string) => {
+      out.shutdowns.push(s);
+    },
+  });
+  try {
+    handler(reason, Promise.resolve());
+  } catch {
+    out.threw = true;
+  }
+  return out;
+}
+
+describe('KS-1868 unhandledRejection handler reads the reason safely', () => {
+  it('control ks1868 C1 an ordinary Error still logs its message and never shuts down in survive mode', () => {
+    const out = run('survive', new Error('boom'));
+    expect(out.threw).toBe(false);
+    expect(out.logs).toHaveLength(1);
+    expect(out.logs[0]).toContain('boom');
+    expect(out.shutdowns).toEqual([]);
+  });
+
+  it('RED ks1868 R1 a revoked Proxy reason is logged as a constant in survive mode, without throwing', () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    const out = run('survive', proxy);
+    expect(out.threw).toBe(false);
+    expect(out.logs).toHaveLength(1);
+    expect(out.logs[0]).toContain('unreadable thrown value');
+    expect(out.shutdowns).toEqual([]);
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws is logged as a constant and still shuts down in exit mode', () => {
+    const reason = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    const out = run('exit', reason);
+    expect(out.threw).toBe(false);
+    expect(out.logs).toHaveLength(1);
+    expect(out.logs[0]).toContain('unreadable thrown value');
+    expect(out.shutdowns).toEqual(['unhandledRejection']);
+  });
+});
```
