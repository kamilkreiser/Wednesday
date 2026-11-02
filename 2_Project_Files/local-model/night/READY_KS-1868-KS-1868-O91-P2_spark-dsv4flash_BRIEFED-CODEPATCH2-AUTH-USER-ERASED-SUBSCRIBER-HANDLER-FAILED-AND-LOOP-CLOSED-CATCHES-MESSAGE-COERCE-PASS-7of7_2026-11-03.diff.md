# READY — KS-1868-KS-1868-O91-P2 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p2_auth_user_erased_subscriber_handler_failed_and_loop_closed_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 08:02 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p2_auth_user_erased_subscriber_handler_failed_and_loop_closed_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p2_auth_user_erased_subscriber_handler_failed_and_loop_closed_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p2_auth_user_erased_subscriber_handler_failed_and_loop_closed_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p2_auth_user_erased_subscriber_handler_failed_and_loop_closed_catches_guard_message-control-r3/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 08:02 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p2_auth_user_erased_subscriber_handler_failed_and_loop_closed_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `b85b7b6786fa6329b6f781cebf2475147738004e`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/services/userErasedSubscriber.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-erased-subscriber-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/services/userErasedSubscriber.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-erased-subscriber-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
16	2	Blockchain/Dev/services/auth/src/services/userErasedSubscriber.ts
167	0	Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-erased-subscriber-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (16 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: userErasedSubscriber.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/services/userErasedSubscriber.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-erased-subscriber-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/services/userErasedSubscriber.ts 16 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-erased-subscriber-catches-unreadable-throw.test.ts 167 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/services/userErasedSubscriber.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-erased-subscriber-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (5 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=5 of total=8; red cell(s): ['KS-1868 the user.erased subscriber rethrows the original value and logs text for a hostile thrown value RED ks1868 R1: a revoke failure that is a revoked Proxy is rethrown as is and logged as text, as for an ordinary Error', 'KS-1868 the user.erased subscriber rethrows the original value and logs text for a hostile thrown value RED ks1868 R2: a revoke failure that is an Error whose message getter throws is rethrown as is and logged as text, as for an ordinary Error', 'KS-1868 the user.erased subscriber rethrows the original value and logs text for a hostile thrown value RED ks1868 R3: a revoke failure that is an Error whose message is a Symbol is rethrown as is and logged as text, as for an ordinary Error', 'KS-1868 the user.erased subscriber rethrows the original value and logs text for a hostile thrown value RED ks1868 R4: a revoked Proxy closing the subscription raises no unhandled rejection and is logged as text, as for an ordinary Error', 'KS-1868 the user.erased subscriber rethrows the original value and logs text for a hostile thrown value RED ks1868 R5: an Error whose message getter throws closing the subscription raises no unhandled rejection and is logged as text, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1561 failed=3 | after: total=1569 failed=2` · `NEW reds: []` [baseline_suite.json total=1561 failed=3; after_suite.json total=1569 failed=2]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/services/userErasedSubscriber.ts` (+16/-2 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-erased-subscriber-catches-unreadable-throw.test.ts` (+167/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/services/userErasedSubscriber.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `b85b7b6786fa6329b6f781cebf2475147738004e` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p2_auth_user_erased_subscriber_handler_failed_and_loop_closed_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o91_p2_auth_user_erased_subscriber_handler_failed_and_loop_closed_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p2_auth_user_erased_subscriber_handler_failed_and_loop_closed_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/services/userErasedSubscriber.ts b/Blockchain/Dev/services/auth/src/services/userErasedSubscriber.ts
--- a/Blockchain/Dev/services/auth/src/services/userErasedSubscriber.ts
+++ b/Blockchain/Dev/services/auth/src/services/userErasedSubscriber.ts
@@ -94,15 +94,29 @@
           userAnonymised,
         });
       } catch (err: any) {
+        let reason: string | null | undefined;
+        try {
+          const m = err?.message;
+          reason = m === undefined || m === null ? m : String(m);
+        } catch {
+          reason = 'unreadable thrown value';
+        }
         logger.error('[cascade] user.erased handler failed', {
           userId,
           dsrId,
-          error: err?.message,
+          error: reason,
         });
         // Re-throw so the bus retries up to its max attempts and dead-letters
         throw err;
       }
     })
     .catch((err) => {
-      logger.error('[cascade] subscriber loop terminated', { error: err?.message });
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('[cascade] subscriber loop terminated', { error: reason });
     });
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-erased-subscriber-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-erased-subscriber-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-erased-subscriber-catches-unreadable-throw.test.ts
@@ -0,0 +1,167 @@
+import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
+
+// KS-1868 (operator 91 screen, auth user.erased subscriber): the handler-failed catch and the subscription-closed `.catch` of
+// startUserErasedSubscriber in services/auth/src/services/userErasedSubscriber.ts log `{ error: err?.message }` with the read INSIDE the
+// logger call's arguments, unguarded. A thrown value whose read throws (a revoked Proxy, an Error whose message getter throws) makes
+// the handler-failed catch throw BEFORE its line is logged and before the original value is rethrown (the bus then receives a
+// different error), and makes the subscription-closed catch handler throw (an unhandled rejection, which ends a Node process by
+// default); an Error whose message is readable but not a string (a Symbol) is handed to the logger uncoerced. The cells make the
+// session revoke step throw such a value and call the subscribed handler / make the subscription reject with such a value, and
+// assert the ORIGINAL value is rethrown, no unhandled rejection is raised, and the logged value is text (the constant when the
+// value cannot be turned into text). Harness: the real subscriber with the event bus replaced by a plain stand-in that hands over
+// the handler (or rejects), plain functions for the session revoke, the db query and the DEK cache, and a plain recording
+// logger (no Redis, no database).
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  mode: 'handler' as 'handler' | 'loop',
+  handler: undefined as undefined | ((event: unknown) => Promise<void>),
+  logged: [] as { message: string; meta: Record<string, unknown> | undefined }[],
+  unhandled: 0,
+}));
+
+vi.mock('@secuura/shared', async (importOriginal) => {
+  const actual = await importOriginal<Record<string, unknown>>();
+  return {
+    ...actual,
+    initEventBus: () => undefined,
+    getEventBus: () => ({
+      subscribe: (_types: unknown, _group: unknown, handler: (event: unknown) => Promise<void>) => {
+        h.handler = handler;
+        return h.mode === 'loop' ? Promise.reject(h.toThrow) : new Promise<void>(() => undefined);
+      },
+    }),
+  };
+});
+
+vi.mock('../db', () => ({
+  query: async () => ({ rows: [{ count: 1 }] }),
+}));
+
+vi.mock('../services/session', () => ({
+  revokeAllUserSessions: async () => {
+    throw h.toThrow;
+  },
+}));
+
+vi.mock('../services/subjectDeks', () => ({
+  subjectDeks: { evict: () => undefined },
+}));
+
+vi.mock('../utils/logger', () => {
+  const rec = (message: string, meta?: Record<string, unknown>) => {
+    h.logged.push({ message, meta });
+  };
+  return { logger: { info: () => undefined, warn: () => undefined, debug: () => undefined, error: rec } };
+});
+
+import { startUserErasedSubscriber } from '../services/userErasedSubscriber';
+
+const FAILED = '[cascade] user.erased handler failed';
+const LOOP = '[cascade] subscriber loop terminated';
+const SAVED_LISTENERS = process.listeners('unhandledRejection');
+const onUnhandled = () => {
+  h.unhandled += 1;
+};
+
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.mode = 'handler';
+  h.handler = undefined;
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
+async function runHandler(value: unknown): Promise<{ rejected: boolean; same: boolean }> {
+  h.toThrow = value;
+  h.mode = 'handler';
+  await startUserErasedSubscriber();
+  try {
+    await (h.handler as (event: unknown) => Promise<void>)({ payload: { userId: 'u1', dsrId: 'd1' } });
+    return { rejected: false, same: false };
+  } catch (e) {
+    return { rejected: true, same: Object.is(e, value) };
+  }
+}
+async function runLoop(value: unknown): Promise<{ unhandled: number }> {
+  h.toThrow = value;
+  h.mode = 'loop';
+  await startUserErasedSubscriber();
+  await new Promise<void>((resolve) => setTimeout(resolve, 25));
+  return { unhandled: h.unhandled };
+}
+const LINES = (message: string) => h.logged.filter((c) => c.message === message);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (c: { meta: Record<string, unknown> | undefined } | undefined): string => {
+  const v = c?.meta?.error;
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
+describe('KS-1868 the user.erased subscriber rethrows the original value and logs text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error from the session revoke is rethrown as is and logged with its message', async () => {
+    const err = new Error('revoke failed');
+    expect(await runHandler(err)).toEqual({ rejected: true, same: true });
+    expect(LINES(FAILED)).toHaveLength(1);
+    expect(reasonOf(LINES(FAILED)[0])).toBe('revoke failed');
+  });
+  it('control ks1868 C2: a thrown plain string is rethrown as is and logged without a message', async () => {
+    expect(await runHandler('plain boom')).toEqual({ rejected: true, same: true });
+    expect(LINES(FAILED)).toHaveLength(1);
+    expect(reasonOf(LINES(FAILED)[0])).toBe('<undefined>');
+  });
+  it('control ks1868 C3: an ordinary Error closing the subscription raises no unhandled rejection and is logged with its message', async () => {
+    expect(await runLoop(new Error('stream closed'))).toEqual({ unhandled: 0 });
+    expect(LINES(LOOP)).toHaveLength(1);
+    expect(reasonOf(LINES(LOOP)[0])).toBe('stream closed');
+  });
+  it('RED ks1868 R1: a revoke failure that is a revoked Proxy is rethrown as is and logged as text, as for an ordinary Error', async () => {
+    const v = revokedProxy();
+    expect(await runHandler(v)).toEqual({ rejected: true, same: true });
+    expect(LINES(FAILED)).toHaveLength(1);
+    expect(reasonOf(LINES(FAILED)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: a revoke failure that is an Error whose message getter throws is rethrown as is and logged as text, as for an ordinary Error', async () => {
+    const v = getterThrows();
+    expect(await runHandler(v)).toEqual({ rejected: true, same: true });
+    expect(LINES(FAILED)).toHaveLength(1);
+    expect(reasonOf(LINES(FAILED)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R3: a revoke failure that is an Error whose message is a Symbol is rethrown as is and logged as text, as for an ordinary Error', async () => {
+    const v = withMessage(Symbol('ks1868'));
+    expect(await runHandler(v)).toEqual({ rejected: true, same: true });
+    expect(LINES(FAILED)).toHaveLength(1);
+    expect(reasonOf(LINES(FAILED)[0])).toBe('Symbol(ks1868)');
+  });
+  it('RED ks1868 R4: a revoked Proxy closing the subscription raises no unhandled rejection and is logged as text, as for an ordinary Error', async () => {
+    expect(await runLoop(revokedProxy())).toEqual({ unhandled: 0 });
+    expect(LINES(LOOP)).toHaveLength(1);
+    expect(reasonOf(LINES(LOOP)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R5: an Error whose message getter throws closing the subscription raises no unhandled rejection and is logged as text, as for an ordinary Error', async () => {
+    expect(await runLoop(getterThrows())).toEqual({ unhandled: 0 });
+    expect(LINES(LOOP)).toHaveLength(1);
+    expect(reasonOf(LINES(LOOP)[0])).toBe('unreadable thrown value');
+  });
+});
```
