# READY — KS-1868-KS-1868-O91-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p1_m365_user_erased_subscriber_loop_closed_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 06:31 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p1_m365_user_erased_subscriber_loop_closed_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p1_m365_user_erased_subscriber_loop_closed_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p1_m365_user_erased_subscriber_loop_closed_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p1_m365_user_erased_subscriber_loop_closed_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 06:31 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p1_m365_user_erased_subscriber_loop_closed_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `4d1ab2cb6574e2b221353ac3a1de56d515711aaf`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/m365-integration/src/userErasedSubscriber.ts } + { Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-user-erased-subscriber-loop-closed-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/m365-integration/src/userErasedSubscriber.ts` (product) and `Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-user-erased-subscriber-loop-closed-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	1	Blockchain/Dev/services/m365-integration/src/userErasedSubscriber.ts
112	0	Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-user-erased-subscriber-loop-closed-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: userErasedSubscriber.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/m365-integration/src/userErasedSubscriber.ts`; test(s): `Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-user-erased-subscriber-loop-closed-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/m365-integration/src/userErasedSubscriber.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-user-erased-subscriber-loop-closed-catch-unreadable-throw.test.ts 112 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/m365-integration/src/userErasedSubscriber.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-user-erased-subscriber-loop-closed-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-1868 the subscription-closed catch logs text and raises no unhandled rejection for a hostile thrown value RED ks1868 R1: a revoked Proxy closing the subscription raises no unhandled rejection and is logged as text, as for an ordinary Error', 'KS-1868 the subscription-closed catch logs text and raises no unhandled rejection for a hostile thrown value RED ks1868 R2: an Error whose message getter throws raises no unhandled rejection and is logged as text, as for an ordinary Error', 'KS-1868 the subscription-closed catch logs text and raises no unhandled rejection for a hostile thrown value RED ks1868 R3: an Error whose message is a Symbol raises no unhandled rejection and is logged as text, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=289 failed=1 | after: total=295 failed=0` · `NEW reds: []` [baseline_suite.json total=289 failed=1; after_suite.json total=295 failed=0]
- A6 [verbatim]: `PASS A6 whole services/m365-integration suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/m365-integration: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/m365-integration/src/userErasedSubscriber.ts` (+8/-1 per numstat.out) and the test file `Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-user-erased-subscriber-loop-closed-catch-unreadable-throw.test.ts` (+112/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/m365-integration/src/userErasedSubscriber.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `4d1ab2cb6574e2b221353ac3a1de56d515711aaf` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p1_m365_user_erased_subscriber_loop_closed_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o91_p1_m365_user_erased_subscriber_loop_closed_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p1_m365_user_erased_subscriber_loop_closed_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/m365-integration/src/userErasedSubscriber.ts b/Blockchain/Dev/services/m365-integration/src/userErasedSubscriber.ts
--- a/Blockchain/Dev/services/m365-integration/src/userErasedSubscriber.ts
+++ b/Blockchain/Dev/services/m365-integration/src/userErasedSubscriber.ts
@@ -41,5 +41,12 @@
       });
     })
     .catch((err) => {
-      log('[cascade] subscriber loop terminated', { error: err?.message });
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      log('[cascade] subscriber loop terminated', { error: reason });
     });
diff --git a/Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-user-erased-subscriber-loop-closed-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-user-erased-subscriber-loop-closed-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-user-erased-subscriber-loop-closed-catch-unreadable-throw.test.ts
@@ -0,0 +1,112 @@
+import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
+
+// KS-1868 (operator 91 screen, m365-integration user.erased subscriber): the `.catch` that closes the subscription of
+// startUserErasedSubscriber in services/m365-integration/src/userErasedSubscriber.ts logs `{ error: err?.message }` with the read
+// INSIDE the log call's arguments, unguarded. A thrown value whose read throws (a revoked Proxy, an Error whose message getter
+// throws) makes that catch handler itself throw, so the promise it returns rejects with nothing to handle it (an unhandled
+// rejection, which ends a Node process by default) and the line is never logged; an Error whose message is readable but not a
+// string (a Symbol) is handed to the log uncoerced. The cells make the subscription reject with such a value and assert no
+// unhandled rejection and a logged line that carries text (the constant when the value cannot be turned into text). Harness: the real
+// subscriber with the event bus replaced by a plain stand-in whose `subscribe` rejects with the value, and a plain recording
+// function for the log (no Redis).
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  logged: [] as unknown[][],
+  unhandled: 0,
+}));
+
+vi.mock('@secuura/shared', async (importOriginal) => {
+  const actual = await importOriginal<Record<string, unknown>>();
+  return {
+    ...actual,
+    initEventBus: () => undefined,
+    getEventBus: () => ({
+      subscribe: () => Promise.reject(h.toThrow),
+    }),
+  };
+});
+
+import { startUserErasedSubscriber } from '../userErasedSubscriber';
+
+const LOOP = '[cascade] subscriber loop terminated';
+const SAVED_LISTENERS = process.listeners('unhandledRejection');
+const onUnhandled = () => {
+  h.unhandled += 1;
+};
+
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.logged.length = 0;
+  h.unhandled = 0;
+  process.env.REDIS_URL = 'redis://stub.invalid:6379';
+  process.removeAllListeners('unhandledRejection');
+  process.on('unhandledRejection', onUnhandled);
+});
+afterEach(() => {
+  process.removeListener('unhandledRejection', onUnhandled);
+  for (const l of SAVED_LISTENERS) process.on('unhandledRejection', l as (...a: any[]) => void);
+});
+
+async function run(value: unknown): Promise<{ unhandled: number }> {
+  h.toThrow = value;
+  await startUserErasedSubscriber((msg: string, ctx?: Record<string, unknown>) => {
+    h.logged.push([msg, ctx]);
+  });
+  await new Promise<void>((resolve) => setTimeout(resolve, 25));
+  return { unhandled: h.unhandled };
+}
+const LINES = () => h.logged.filter((c) => c[0] === LOOP);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (c: unknown[] | undefined): string => {
+  const v = (c?.[1] as { error?: unknown } | undefined)?.error;
+  return typeof v === 'string' ? v : '<' + typeof v + '>';
+};
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
+describe('KS-1868 the subscription-closed catch logs text and raises no unhandled rejection for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error closing the subscription raises no unhandled rejection and is logged with its message', async () => {
+    expect(await run(new Error('stream closed'))).toEqual({ unhandled: 0 });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('stream closed');
+  });
+  it('control ks1868 C2: a thrown plain string raises no unhandled rejection and is logged without a message', async () => {
+    expect(await run('plain boom')).toEqual({ unhandled: 0 });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('<undefined>');
+  });
+  it('control ks1868 C3: an Error with an empty message raises no unhandled rejection and is logged with the empty text', async () => {
+    expect(await run(new Error(''))).toEqual({ unhandled: 0 });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('');
+  });
+  it('RED ks1868 R1: a revoked Proxy closing the subscription raises no unhandled rejection and is logged as text, as for an ordinary Error', async () => {
+    expect(await run(revokedProxy())).toEqual({ unhandled: 0 });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message getter throws raises no unhandled rejection and is logged as text, as for an ordinary Error', async () => {
+    expect(await run(getterThrows())).toEqual({ unhandled: 0 });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R3: an Error whose message is a Symbol raises no unhandled rejection and is logged as text, as for an ordinary Error', async () => {
+    expect(await run(withMessage(Symbol('ks1868')))).toEqual({ unhandled: 0 });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('Symbol(ks1868)');
+  });
+});
```
