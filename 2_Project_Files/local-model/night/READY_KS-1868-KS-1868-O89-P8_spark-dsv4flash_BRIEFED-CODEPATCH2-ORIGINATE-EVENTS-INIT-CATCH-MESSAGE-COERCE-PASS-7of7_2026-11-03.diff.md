# READY — KS-1868-KS-1868-O89-P8 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_p8_originate_events_init_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 04:26 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_p8_originate_events_init_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_p8_originate_events_init_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_p8_originate_events_init_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_p8_originate_events_init_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 04:26 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_p8_originate_events_init_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `2d3b3bb3d3865689e3cad843f9ebb90a2f606960`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/events.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-events-init-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/events.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-events-init-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	1	Blockchain/Dev/services/originate/src/events.ts
104	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-events-init-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: events.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/events.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-events-init-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/events.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-events-init-catch-unreadable-throw.test.ts 104 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/events.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-events-init-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1868 the event bus init catch survives and logs text for a hostile thrown value RED ks1868 R1: a revoked Proxy from the Redis constructor makes initEventBus answer false and is logged as text, as for an ordinary Error', 'KS-1868 the event bus init catch survives and logs text for a hostile thrown value RED ks1868 R2: an Error whose message getter throws from the Redis constructor makes initEventBus answer false and is logged as text, as for an ordinary Error', 'KS-1868 the event bus init catch survives and logs text for a hostile thrown value RED ks1868 R3: an Error whose message is a Symbol from the Redis constructor makes initEventBus answer false and is logged as text, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2334 failed=0 | after: total=2339 failed=0` · `NEW reds: []` [baseline_suite.json total=2334 failed=0; after_suite.json total=2339 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/events.ts` (+8/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-events-init-catch-unreadable-throw.test.ts` (+104/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/events.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `2d3b3bb3d3865689e3cad843f9ebb90a2f606960` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_p8_originate_events_init_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o89_p8_originate_events_init_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_p8_originate_events_init_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/events.ts b/Blockchain/Dev/services/originate/src/events.ts
--- a/Blockchain/Dev/services/originate/src/events.ts
+++ b/Blockchain/Dev/services/originate/src/events.ts
@@ -92,7 +92,14 @@
     logger.info('EventBus initialised for originate service');
     return true;
   } catch (err: any) {
-    logger.warn('Failed to initialise EventBus', { error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('Failed to initialise EventBus', { error: reason });
     return false;
   }
 }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-events-init-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-events-init-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-events-init-catch-unreadable-throw.test.ts
@@ -0,0 +1,104 @@
+// KS-1868 (operator 89 screen, originate event bus): the catch of initEventBus (line 95) of services/originate/src/events.ts
+// passes `err?.message` straight into the logger's meta object, unguarded. A thrown value whose read throws (a revoked Proxy, an
+// Error whose message getter throws) makes the catch itself throw, so initEventBus THROWS instead of answering false (its
+// contract: "Returns true if Redis connection was established"; on failure the service carries on without events); an Error
+// whose message is not a string (a Symbol) is passed to the logger uncoerced. The cells make the Redis constructor throw
+// such a value and assert initEventBus answers false and the logged value is text (the constant when the value cannot be
+// turned into text). Harness: the real module with ioredis replaced by a plain stand-in class and the logger by a plain
+// recording object (no Redis, no network).
+const mockH: {
+  ctorFailure: undefined | { value: unknown };
+  logs: { level: string; message: string; meta: Record<string, unknown> | undefined }[];
+} = { ctorFailure: undefined, logs: [] };
+
+jest.mock('ioredis', () => ({
+  __esModule: true,
+  default: function RedisMock() {
+    if (mockH.ctorFailure) throw mockH.ctorFailure.value;
+    return {
+      status: 'wait',
+      on: () => undefined,
+      connect: async () => undefined,
+      disconnect: () => undefined,
+      xadd: async () => '1-0',
+    };
+  },
+}));
+jest.mock('../utils/logger', () => {
+  const rec = (level: string) => (message: string, meta?: Record<string, unknown>) => {
+    mockH.logs.push({ level, message, meta });
+  };
+  return { logger: { debug: rec('debug'), info: rec('info'), warn: rec('warn'), error: rec('error') } };
+});
+
+type Ev = typeof import('../events');
+beforeEach(() => {
+  mockH.ctorFailure = undefined;
+  mockH.logs.length = 0;
+});
+
+function freshEvents(): Ev {
+  jest.resetModules();
+  // eslint-disable-next-line @typescript-eslint/no-require-imports
+  return require('../events') as Ev;
+}
+function init(value: unknown): { ok: boolean; value: boolean | undefined } {
+  mockH.ctorFailure = { value };
+  const ev = freshEvents();
+  try {
+    return { ok: true, value: ev.initEventBus('redis://localhost:6379') };
+  } catch {
+    return { ok: false, value: undefined };
+  }
+}
+const LINE = (message: string): { level: string; message: string; meta: Record<string, unknown> | undefined }[] =>
+  mockH.logs.filter((l) => l.message === message);
+const INIT = 'Failed to initialise EventBus';
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (l: { meta: Record<string, unknown> | undefined } | undefined): string =>
+  typeof l?.meta?.error === 'string' ? (l.meta.error as string) : '<' + typeof l?.meta?.error + '>';
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
+
+describe('KS-1868 the event bus init catch survives and logs text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error from the Redis constructor makes initEventBus answer false and is logged with its message', () => {
+    expect(init(new Error('init boom'))).toEqual({ ok: true, value: false });
+    expect(LINE(INIT)).toHaveLength(1);
+    expect(reasonOf(LINE(INIT)[0])).toBe('init boom');
+  });
+  it('control ks1868 C2: a thrown number from the Redis constructor makes initEventBus answer false and is logged without a message', () => {
+    expect(init(42)).toEqual({ ok: true, value: false });
+    expect(LINE(INIT)).toHaveLength(1);
+    expect(reasonOf(LINE(INIT)[0])).toBe('<undefined>');
+  });
+  it('RED ks1868 R1: a revoked Proxy from the Redis constructor makes initEventBus answer false and is logged as text, as for an ordinary Error', () => {
+    expect(init(revokedProxy())).toEqual({ ok: true, value: false });
+    expect(LINE(INIT)).toHaveLength(1);
+    expect(reasonOf(LINE(INIT)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message getter throws from the Redis constructor makes initEventBus answer false and is logged as text, as for an ordinary Error', () => {
+    expect(init(getterThrows())).toEqual({ ok: true, value: false });
+    expect(LINE(INIT)).toHaveLength(1);
+    expect(reasonOf(LINE(INIT)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R3: an Error whose message is a Symbol from the Redis constructor makes initEventBus answer false and is logged as text, as for an ordinary Error', () => {
+    expect(init(withMessage(Symbol('ks1868')))).toEqual({ ok: true, value: false });
+    expect(LINE(INIT)).toHaveLength(1);
+    expect(reasonOf(LINE(INIT)[0])).toBe('Symbol(ks1868)');
+  });
+});
```
