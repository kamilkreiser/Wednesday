# READY — KS-1868-KS-1868-O34-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1868_p1_demo_boot_gate_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 18:53 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1868_p1_demo_boot_gate_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1868_p1_demo_boot_gate_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_p1_demo_boot_gate_unreadable_throw/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 18:53 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1868_p1_demo_boot_gate_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `e43a289c1c7bb687a550479643607b7cfd416897`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/demo-service/src/index.ts } + { Blockchain/Dev/services/demo-service/src/__tests__/ks1868-boot-gate-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/demo-service/src/index.ts` (product) and `Blockchain/Dev/services/demo-service/src/__tests__/ks1868-boot-gate-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
6	1	Blockchain/Dev/services/demo-service/src/index.ts
57	0	Blockchain/Dev/services/demo-service/src/__tests__/ks1868-boot-gate-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (6 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/demo-service/src/index.ts`; test(s): `Blockchain/Dev/services/demo-service/src/__tests__/ks1868-boot-gate-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/demo-service/src/index.ts 6 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/demo-service/src/__tests__/ks1868-boot-gate-unreadable-throw.test.ts 57 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/demo-service/src/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/demo-service/src/__tests__/ks1868-boot-gate-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (1 failed / 2 run; controls green; assertion reds)` [red_first.json: failed=1 of total=2; red cell(s): ['KS-1868 demo-service boot gate reads the thrown value safely RED ks1868 R1 a revoked Proxy thrown value logs a constant FATAL line and exits 1']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (2 passed / 2 run)` [green_after.json: failed=0 of total=2, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=86 failed=0 | after: total=88 failed=0` · `NEW reds: []` [baseline_suite.json total=86 failed=0; after_suite.json total=88 failed=0]
- A6 [verbatim]: `PASS A6 whole services/demo-service suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/demo-service: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/demo-service/src/index.ts` (+6/-1 per numstat.out) and the test file `Blockchain/Dev/services/demo-service/src/__tests__/ks1868-boot-gate-unreadable-throw.test.ts` (+57/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/demo-service/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `e43a289c1c7bb687a550479643607b7cfd416897` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1868_p1_demo_boot_gate_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_p1_demo_boot_gate_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1868_p1_demo_boot_gate_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/demo-service/src/index.ts b/Blockchain/Dev/services/demo-service/src/index.ts
--- a/Blockchain/Dev/services/demo-service/src/index.ts
+++ b/Blockchain/Dev/services/demo-service/src/index.ts
@@ -37,7 +37,12 @@
 try {
   assertDemoServiceEnabled();
 } catch (err) {
-  const message = err instanceof Error ? err.message : String(err);
+  let message: string;
+  try {
+    message = String(err instanceof Error ? err.message : err);
+  } catch {
+    message = 'unreadable thrown value';
+  }
   logger.error(`FATAL: ${message}`);
   process.exit(1);
 }
diff --git a/Blockchain/Dev/services/demo-service/src/__tests__/ks1868-boot-gate-unreadable-throw.test.ts b/Blockchain/Dev/services/demo-service/src/__tests__/ks1868-boot-gate-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/demo-service/src/__tests__/ks1868-boot-gate-unreadable-throw.test.ts
@@ -0,0 +1,57 @@
+// KS-1868: the boot gate in index.ts must still log FATAL and exit(1) when the
+// thrown value itself cannot be read (a revoked Proxy throws on `instanceof`).
+// The gate is a plain function, not a vi.fn(): a spy inspects what it throws
+// and would itself fail on a revoked Proxy before the code under test saw it.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  error: vi.fn(),
+}));
+
+vi.mock('../utils/logger', () => ({
+  createLogger: () => ({ debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: h.error }),
+}));
+
+vi.mock('../middleware/demoGuard', () => ({
+  assertDemoServiceEnabled: () => {
+    throw h.toThrow;
+  },
+}));
+
+vi.mock('../app', () => ({
+  createApp: () => ({
+    listen: vi.fn(() => ({ close: vi.fn() })),
+  }),
+}));
+
+import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
+
+describe('KS-1868 demo-service boot gate reads the thrown value safely', () => {
+  let exitSpy: ReturnType<typeof vi.spyOn>;
+
+  beforeEach(() => {
+    vi.resetModules();
+    h.toThrow = undefined;
+    h.error.mockReset();
+    exitSpy = vi.spyOn(process, 'exit').mockImplementation((() => undefined) as never);
+  });
+
+  afterEach(() => {
+    exitSpy.mockRestore();
+  });
+
+  it('control ks1868 C1 an ordinary Error still logs its message and exits 1', async () => {
+    h.toThrow = new Error('demo disabled');
+    await import('../index').catch(() => undefined);
+    expect(h.error).toHaveBeenCalledWith('FATAL: demo disabled');
+    expect(exitSpy).toHaveBeenCalledWith(1);
+  });
+
+  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant FATAL line and exits 1', async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    h.toThrow = proxy;
+    await import('../index').catch(() => undefined);
+    expect(h.error).toHaveBeenCalledWith('FATAL: unreadable thrown value');
+    expect(exitSpy).toHaveBeenCalledWith(1);
+  });
+});
```
