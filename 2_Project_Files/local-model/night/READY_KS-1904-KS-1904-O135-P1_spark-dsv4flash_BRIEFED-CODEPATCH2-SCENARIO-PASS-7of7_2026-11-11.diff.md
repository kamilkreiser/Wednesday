# READY — KS-1904-KS-1904-O135-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1904_o135_p1_demo_service_scenario_context_logs_only_a_string_message/out.md.checker/patch.diff`** (from `ls` at 14:39 2026-11-11; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1904_o135_p1_demo_service_scenario_context_logs_only_a_string_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1904_o135_p1_demo_service_scenario_context_logs_only_a_string_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1904_o135_p1_demo_service_scenario_context_logs_only_a_string_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1904_o135_p1_demo_service_scenario_context_logs_only_a_string_message-control/out.md.checker/patch.diff` rc 0, Spark operator o135 (Wednesday)).

**Held 14:39 2026-11-11 by Spark operator o135 (Wednesday) after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1904_o135_p1_demo_service_scenario_context_logs_only_a_string_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `4a91ff3e1c56326da501f352ae2e9b2e3308fa4e`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/demo-service/src/routes/scenario.ts } + { Blockchain/Dev/services/demo-service/src/__tests__/ks1904-scenario-context-logs-only-a-string-message.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/demo-service/src/routes/scenario.ts` (product) and `Blockchain/Dev/services/demo-service/src/__tests__/ks1904-scenario-context-logs-only-a-string-message.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	1	Blockchain/Dev/services/demo-service/src/routes/scenario.ts
100	0	Blockchain/Dev/services/demo-service/src/__tests__/ks1904-scenario-context-logs-only-a-string-message.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (3 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: scenario.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/demo-service/src/routes/scenario.ts`; test(s): `Blockchain/Dev/services/demo-service/src/__tests__/ks1904-scenario-context-logs-only-a-string-message.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/demo-service/src/routes/scenario.ts 3 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/demo-service/src/__tests__/ks1904-scenario-context-logs-only-a-string-message.test.ts 100 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/demo-service/src/routes/scenario.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/demo-service/src/__tests__/ks1904-scenario-context-logs-only-a-string-message.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 3 run; controls green; assertion reds)` [red_first.json: failed=2 of total=3; red cell(s): ['KS-1904 scenario context handler logs only a string message RED ks1904 R1 an Error whose message getter returns an object with a throwing toJSON logs a constant string reason', 'KS-1904 scenario context handler logs only a string message RED ks1904 R2 an Error whose message getter returns a number logs a constant string reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (3 passed / 3 run)` [green_after.json: failed=0 of total=3, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=103 failed=0 | after: total=106 failed=0` · `NEW reds: []` [baseline_suite.json total=103 failed=0; after_suite.json total=106 failed=0]
- A6 [verbatim]: `PASS A6 whole services/demo-service suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/demo-service: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/demo-service/src/routes/scenario.ts` (+3/-1 per numstat.out) and the test file `Blockchain/Dev/services/demo-service/src/__tests__/ks1904-scenario-context-logs-only-a-string-message.test.ts` (+100/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/demo-service/src/routes/scenario.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `4a91ff3e1c56326da501f352ae2e9b2e3308fa4e` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1904_o135_p1_demo_service_scenario_context_logs_only_a_string_message/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1904_o135_p1_demo_service_scenario_context_logs_only_a_string_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/demo-service/src/routes/scenario.ts b/Blockchain/Dev/services/demo-service/src/routes/scenario.ts
--- a/Blockchain/Dev/services/demo-service/src/routes/scenario.ts
+++ b/Blockchain/Dev/services/demo-service/src/routes/scenario.ts
@@ -112,7 +112,9 @@
   } catch (err) {
     let message: string;
     try {
-      message = err instanceof Error ? err.message : 'Unknown error';
+      const read = err instanceof Error ? err.message : 'Unknown error';
+      // KS-1904: a message getter can RETURN a non-string (an object with a throwing toJSON): the logger would be handed it and its serialiser would throw.
+      message = typeof read === 'string' ? read : 'unreadable thrown value';
     } catch {
       message = 'unreadable thrown value';
     }
diff --git a/Blockchain/Dev/services/demo-service/src/__tests__/ks1904-scenario-context-logs-only-a-string-message.test.ts b/Blockchain/Dev/services/demo-service/src/__tests__/ks1904-scenario-context-logs-only-a-string-message.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/demo-service/src/__tests__/ks1904-scenario-context-logs-only-a-string-message.test.ts
@@ -0,0 +1,100 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-1904: the GET /scenario/context handler guards a message read that THROWS (KS-1868) but not one that RETURNS a non-string: an Error
+// whose `message` getter returns an object with a throwing toJSON was handed to the logger as { error: <object> }, and JSON.stringify of
+// that meta throws. The handler now logs the constant reason for any message that is not a string. Harness: the KS-1868 one (the real
+// route handler, a request whose `query` getter raises the value under test, the logger replaced).
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  error: vi.fn(),
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: h.error },
+  createLogger: () => ({ debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn() }),
+}));
+
+import { scenarioRouter } from '../routes/scenario';
+
+type Layer = { route?: { path: string; stack: Array<{ handle: (req: unknown, res: unknown) => unknown }> } };
+type Outcome = { threw: boolean; status?: number; body?: unknown };
+
+/** Run the real route handler with a request whose `query` getter throws the value under test. */
+async function runHandler(): Promise<Outcome> {
+  const layer = (scenarioRouter as unknown as { stack: Layer[] }).stack.find(
+    (l) => l.route?.path === '/scenario/context',
+  );
+  const handle = layer!.route!.stack[0].handle;
+  const out: Outcome = { threw: false };
+  const res = {
+    status(code: number) {
+      out.status = code;
+      return res;
+    },
+    json(body: unknown) {
+      out.body = body;
+      return res;
+    },
+  };
+  const req = {
+    get query(): never {
+      throw h.toThrow;
+    },
+  };
+  try {
+    await handle(req, res);
+  } catch {
+    out.threw = true;
+  }
+  return out;
+}
+
+const ERRORS = () => h.error.mock.calls.filter((c) => String(c[0]).includes('Failed to get scenario context'));
+const GENERIC = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
+const errorWithMessage = (value: unknown) =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        return value;
+      },
+    },
+  });
+
+describe('KS-1904 scenario context handler logs only a string message', () => {
+  beforeEach(() => {
+    h.toThrow = undefined;
+    h.error.mockReset();
+  });
+
+  it('control ks1904 C1 an ordinary Error still logs its message and answers 500', async () => {
+    h.toThrow = new Error('query boom');
+    const out = await runHandler();
+    expect(out.status).toBe(500);
+    expect(out.body).toEqual(GENERIC);
+    expect(ERRORS()).toHaveLength(1);
+    expect(ERRORS()[0][1]).toEqual({ error: 'query boom' });
+  });
+
+  it('RED ks1904 R1 an Error whose message getter returns an object with a throwing toJSON logs a constant string reason', async () => {
+    h.toThrow = errorWithMessage({
+      toJSON() {
+        throw new Error('toJSON boom');
+      },
+    });
+    const out = await runHandler();
+    expect(out.threw).toBe(false);
+    expect(out.status).toBe(500);
+    expect(out.body).toEqual(GENERIC);
+    expect(ERRORS()).toHaveLength(1);
+    expect(ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1904 R2 an Error whose message getter returns a number logs a constant string reason', async () => {
+    h.toThrow = errorWithMessage(42);
+    const out = await runHandler();
+    expect(out.threw).toBe(false);
+    expect(out.status).toBe(500);
+    expect(ERRORS()).toHaveLength(1);
+    expect(ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+});
```
