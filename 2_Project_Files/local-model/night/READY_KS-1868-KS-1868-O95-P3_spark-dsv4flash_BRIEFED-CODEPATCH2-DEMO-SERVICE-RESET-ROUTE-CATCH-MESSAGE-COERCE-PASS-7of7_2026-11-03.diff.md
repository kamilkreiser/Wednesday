# READY — KS-1868-KS-1868-O95-P3 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p3_demo_service_reset_route_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 15:02 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p3_demo_service_reset_route_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p3_demo_service_reset_route_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p3_demo_service_reset_route_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p3_demo_service_reset_route_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 15:02 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p3_demo_service_reset_route_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `67309f28ab2132ca7b6a45b28c731aa480642a9a`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/demo-service/src/routes/reset.ts } + { Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-reset-route-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/demo-service/src/routes/reset.ts` (product) and `Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-reset-route-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
6	1	Blockchain/Dev/services/demo-service/src/routes/reset.ts
95	0	Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-reset-route-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (6 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: reset.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/demo-service/src/routes/reset.ts`; test(s): `Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-reset-route-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/demo-service/src/routes/reset.ts 6 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-reset-route-catch-unreadable-throw.test.ts 95 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/demo-service/src/routes/reset.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-reset-route-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 POST /demo-api/reset reads the thrown value safely RED ks1868 R1 a revoked Proxy is answered 500 with a constant reason', 'KS-1868 POST /demo-api/reset reads the thrown value safely RED ks1868 R2 an Error whose message getter throws is answered 500 with a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=103 failed=0 | after: total=107 failed=0` · `NEW reds: []` [baseline_suite.json total=103 failed=0; after_suite.json total=107 failed=0]
- A6 [verbatim]: `PASS A6 whole services/demo-service suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/demo-service: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/demo-service/src/routes/reset.ts` (+6/-1 per numstat.out) and the test file `Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-reset-route-catch-unreadable-throw.test.ts` (+95/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/demo-service/src/routes/reset.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `67309f28ab2132ca7b6a45b28c731aa480642a9a` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p3_demo_service_reset_route_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o95_p3_demo_service_reset_route_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p3_demo_service_reset_route_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/demo-service/src/routes/reset.ts b/Blockchain/Dev/services/demo-service/src/routes/reset.ts
--- a/Blockchain/Dev/services/demo-service/src/routes/reset.ts
+++ b/Blockchain/Dev/services/demo-service/src/routes/reset.ts
@@ -61,5 +61,10 @@
     });
   } catch (err: unknown) {
     const totalDurationMs = Date.now() - overallStart;
-    const message = err instanceof Error ? err.message : 'Unknown error';
+    let message: string;
+    try {
+      message = err instanceof Error ? err.message : 'Unknown error';
+    } catch {
+      message = 'unreadable thrown value';
+    }
     const failedStep = message.includes('pg_restore') ? 'database' : 'redis';
diff --git a/Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-reset-route-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-reset-route-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-reset-route-catch-unreadable-throw.test.ts
@@ -0,0 +1,95 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-1868: POST /demo-api/reset (src/routes/reset.ts) answers a failed reset with a 500 body that carries the failure's message and
+// the step that failed. Its catch reads `err instanceof Error ? err.message : 'Unknown error'` unguarded. When the value the reset
+// step rejected with cannot be read (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws, throws on
+// `.message`) the catch throws before it answers, so the handler REJECTS and the request gets no response at all. The cells run
+// the route handler directly with a duck-typed response (an Express 4 handler is an async function whose rejection nobody awaits).
+// The reset service and logger stand-ins are plain functions, not vi.fn(): a spy inspects what it rejects with and could itself
+// fail on a revoked Proxy before the code under test saw it.
+const state = vi.hoisted(() => ({ toThrow: undefined as unknown }));
+
+vi.mock('../utils/logger', () => ({
+  logger: {
+    debug: () => undefined,
+    info: () => undefined,
+    warn: () => undefined,
+    error: () => undefined,
+  },
+}));
+
+vi.mock('../services/resetService', () => ({
+  resetDatabase: () => Promise.reject(state.toThrow),
+  resetRedis: () => Promise.resolve({ success: true, keysCleared: 0 }),
+}));
+
+import { resetRouter } from '../routes/reset';
+
+type Reply = { status: number | undefined; body: unknown };
+type Layer = { route?: { path: string; stack: Array<{ handle: (req: unknown, res: unknown) => Promise<unknown> }> } };
+
+const handler = (resetRouter as unknown as { stack: Layer[] }).stack.find((l) => l.route?.path === '/reset')!.route!.stack[0].handle;
+
+/** The reply, or the string 'rejected' when the handler rejects (an assertion can then fail on it). */
+async function postReset(value: unknown): Promise<Reply | 'rejected'> {
+  state.toThrow = value;
+  const reply: Reply = { status: undefined, body: undefined };
+  const res = {
+    status(code: number) {
+      reply.status = code;
+      return res;
+    },
+    json(body: unknown) {
+      reply.body = body;
+      return res;
+    },
+  };
+  try {
+    await handler({ headers: { 'x-demo-reset': '1' } }, res);
+  } catch {
+    return 'rejected';
+  }
+  return reply;
+}
+
+const revokedProxy = (): unknown => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+const failed = (message: string, failedStep: string): Reply => ({
+  status: 500,
+  body: { success: false, error: { code: 'INTERNAL_ERROR', message, failedStep } },
+});
+
+describe('KS-1868 POST /demo-api/reset reads the thrown value safely', () => {
+  beforeEach(() => {
+    state.toThrow = undefined;
+  });
+
+  it('control ks1868 C1 an ordinary Error from the database step is answered 500 with its message and the database step', async () => {
+    expect(await postReset(new Error('pg_restore failed: boom'))).toEqual(failed('pg_restore failed: boom', 'database'));
+  });
+
+  it('control ks1868 C2 a thrown plain string is answered 500 with the default message', async () => {
+    expect(await postReset('plain text failure')).toEqual(failed('Unknown error', 'redis'));
+  });
+
+  it('RED ks1868 R1 a revoked Proxy is answered 500 with a constant reason', async () => {
+    expect(await postReset(revokedProxy())).toEqual(failed('unreadable thrown value', 'redis'));
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws is answered 500 with a constant reason', async () => {
+    expect(await postReset(getterThrows())).toEqual(failed('unreadable thrown value', 'redis'));
+  });
+});
```
