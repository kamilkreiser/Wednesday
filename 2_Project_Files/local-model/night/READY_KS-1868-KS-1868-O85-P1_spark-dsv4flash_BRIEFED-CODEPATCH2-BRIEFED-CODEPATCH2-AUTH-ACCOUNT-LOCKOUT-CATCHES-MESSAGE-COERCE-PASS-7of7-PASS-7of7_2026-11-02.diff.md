# READY — KS-1868-KS-1868-O85-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p1_auth_account_lockout_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 23:14 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p1_auth_account_lockout_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p1_auth_account_lockout_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p1_auth_account_lockout_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p1_auth_account_lockout_catches_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 23:14 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p1_auth_account_lockout_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `1584c0f0ff808fddf35245bee41b6b5f9231054c`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/services/accountLockout.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1868-account-lockout-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/services/accountLockout.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1868-account-lockout-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
24	3	Blockchain/Dev/services/auth/src/services/accountLockout.ts
162	0	Blockchain/Dev/services/auth/src/__tests__/ks1868-account-lockout-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (24 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: accountLockout.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/services/accountLockout.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1868-account-lockout-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/services/accountLockout.ts 24 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1868-account-lockout-catches-unreadable-throw.test.ts 162 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/services/accountLockout.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1868-account-lockout-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (8 failed / 12 run; controls green; assertion reds)` [red_first.json: failed=8 of total=12; red cell(s): ['KS-1868 the account lockout catches fail open and log text for a hostile thrown value RED ks1868 R1 isLockedOut: a rejection that is a revoked Proxy fails open (false) and is logged as text, as for an ordinary Error', 'KS-1868 the account lockout catches fail open and log text for a hostile thrown value RED ks1868 R2 isLockedOut: a rejection that is an Error whose message getter throws fails open (false) and is logged as text, as for an ordinary Error', 'KS-1868 the account lockout catches fail open and log text for a hostile thrown value RED ks1868 R3 isLockedOut: a rejection that is an Error whose message is a null-prototype object fails open (false) and is logged as text, as for an ordinary Error', 'KS-1868 the account lockout catches fail open and log text for a hostile thrown value RED ks1868 R4 isLockedOut: a rejection that is an Error whose message is a Symbol fails open (false) and is logged as text, as for an ordinary Error', 'KS-1868 the account lockout catches fail open and log text for a hostile thrown value RED ks1868 R5 recordFailure: a rejection that is a revoked Proxy continues (0) and is logged as text, as for an ordinary Error', 'KS-1868 the account lockout catches fail open and log text for a hostile thrown value RED ks1868 R6 recordFailure: a rejection that is an Error whose message is a Symbol continues (0) and is logged as text, as for an ordinary Error', 'KS-1868 the account lockout catches fail open and log text for a hostile thrown value RED ks1868 R7 recordSuccess: a rejection that is a revoked Proxy is non-fatal (resolves) and is logged as text, as for an ordinary Error', 'KS-1868 the account lockout catches fail open and log text for a hostile thrown value RED ks1868 R8 recordSuccess: a rejection that is an Error whose message is a Symbol is non-fatal (resolves) and is logged as text, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (12 passed / 12 run)` [green_after.json: failed=0 of total=12, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1492 failed=1 | after: total=1504 failed=0` · `NEW reds: []` [baseline_suite.json total=1492 failed=1; after_suite.json total=1504 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/services/accountLockout.ts` (+24/-3 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1868-account-lockout-catches-unreadable-throw.test.ts` (+162/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/services/accountLockout.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `1584c0f0ff808fddf35245bee41b6b5f9231054c` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p1_auth_account_lockout_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o85_p1_auth_account_lockout_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p1_auth_account_lockout_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/services/accountLockout.ts b/Blockchain/Dev/services/auth/src/services/accountLockout.ts
--- a/Blockchain/Dev/services/auth/src/services/accountLockout.ts
+++ b/Blockchain/Dev/services/auth/src/services/accountLockout.ts
@@ -89,7 +89,14 @@
     const v = await redis.get(lockoutKey(email, ip));
     return v !== null;
   } catch (err: any) {
-    logger.warn('lockout: redis error on isLockedOut — failing open', { error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('lockout: redis error on isLockedOut — failing open', { error: reason });
     return false;
   }
 }
@@ -119,7 +126,14 @@
     }
     return count;
   } catch (err: any) {
-    logger.warn('lockout: redis error on recordFailure — continuing', { error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('lockout: redis error on recordFailure — continuing', { error: reason });
     return 0;
   }
 }
@@ -130,6 +144,13 @@
   try {
     await redis.del(counterKey(email, ip), lockoutKey(email, ip));
   } catch (err: any) {
-    logger.warn('lockout: redis error on recordSuccess — non-fatal', { error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('lockout: redis error on recordSuccess — non-fatal', { error: reason });
   }
 }
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1868-account-lockout-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1868-account-lockout-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1868-account-lockout-catches-unreadable-throw.test.ts
@@ -0,0 +1,162 @@
+import { describe, it, expect, beforeAll, beforeEach, vi } from 'vitest';
+
+// KS-1868 (operator 85 screen, account lockout): the three catches of services/auth/src/services/accountLockout.ts
+// (isLockedOut, recordFailure, recordSuccess) log `{ error: err?.message }` with the read INSIDE the logger call's
+// arguments, unguarded. A thrown value whose read throws (a revoked Proxy, an Error whose message getter throws) makes the
+// catch itself throw, so the function REJECTS although the module documents that the lockout fails OPEN when Redis is down;
+// an Error whose message is readable but not a string is handed to the logger as is. The cells make the Redis command reject
+// with such a value and assert the function resolves with its fail-open value (the outcome an ordinary Error gets) and the
+// line is logged as text (the constant when the value cannot be turned into text). Harness: the real module with the logger
+// replaced by a plain stand-in and a plain-object Redis client (no Redis, no network).
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  logged: [] as unknown[][],
+}));
+
+const capture = vi.hoisted(() => ({
+  debug: () => undefined,
+  info: () => undefined,
+  warn: (...args: unknown[]) => {
+    h.logged.push(args);
+  },
+  error: () => undefined,
+  log: () => undefined,
+}));
+vi.mock('../utils/logger', () => ({ logger: capture, createLogger: () => capture, validateEnv: () => undefined }));
+
+type Lockout = typeof import('../services/accountLockout');
+let mod: Lockout;
+beforeAll(async () => {
+  mod = await import('../services/accountLockout');
+});
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.logged.length = 0;
+});
+
+/** A Redis client whose every command rejects with the thrown value, through plain functions (not spies). */
+const failingRedis = (): Parameters<Lockout['isLockedOut']>[0] => ({
+  get: () => Promise.reject(h.toThrow),
+  set: () => Promise.reject(h.toThrow),
+  incr: () => Promise.reject(h.toThrow),
+  expire: () => Promise.reject(h.toThrow),
+  del: () => Promise.reject(h.toThrow),
+});
+
+async function settle<T>(p: () => Promise<T>): Promise<{ ok: boolean; value: T | undefined }> {
+  try {
+    return { ok: true, value: await p() };
+  } catch {
+    return { ok: false, value: undefined };
+  }
+}
+const locked = () => settle(() => mod.isLockedOut(failingRedis(), 'user@example.com', '203.0.113.9'));
+const failure = () => settle(() => mod.recordFailure(failingRedis(), 'user@example.com', '203.0.113.9'));
+const success = () => settle(() => mod.recordSuccess(failingRedis(), 'user@example.com', '203.0.113.9'));
+
+const LOCKED = 'lockout: redis error on isLockedOut — failing open';
+const FAILURE = 'lockout: redis error on recordFailure — continuing';
+const SUCCESS = 'lockout: redis error on recordSuccess — non-fatal';
+const LINES = (msg: string) => h.logged.filter((c) => c[0] === msg);
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
+const SHAPES: Array<[string, () => unknown, string]> = [
+  ['a revoked Proxy', revokedProxy, 'unreadable thrown value'],
+  ['an Error whose message getter throws', getterThrows, 'unreadable thrown value'],
+  ['an Error whose message is a null-prototype object', () => withMessage(Object.create(null)), 'unreadable thrown value'],
+  ['an Error whose message is a Symbol', () => withMessage(Symbol('ks1868')), 'Symbol(ks1868)'],
+];
+
+describe('KS-1868 the account lockout catches fail open and log text for a hostile thrown value', () => {
+  it('control ks1868 C1 isLockedOut: an ordinary Error fails open (false) and is logged with its message', async () => {
+    h.toThrow = new Error('LOADING redis');
+    expect(await locked()).toEqual({ ok: true, value: false });
+    expect(LINES(LOCKED)).toHaveLength(1);
+    expect(reasonOf(LINES(LOCKED)[0])).toBe('LOADING redis');
+  });
+  it('control ks1868 C2 isLockedOut: a thrown plain string has no message, fails open (false) and is logged with no error, as before', async () => {
+    h.toThrow = 'plain boom';
+    expect(await locked()).toEqual({ ok: true, value: false });
+    expect(LINES(LOCKED)).toHaveLength(1);
+    expect(reasonOf(LINES(LOCKED)[0])).toBe('<undefined>');
+  });
+  it('control ks1868 C3 recordFailure: an ordinary Error continues (0) and is logged with its message', async () => {
+    h.toThrow = new Error('READONLY redis');
+    expect(await failure()).toEqual({ ok: true, value: 0 });
+    expect(LINES(FAILURE)).toHaveLength(1);
+    expect(reasonOf(LINES(FAILURE)[0])).toBe('READONLY redis');
+  });
+  it('control ks1868 C4 recordSuccess: an ordinary Error is non-fatal (resolves) and is logged with its message', async () => {
+    h.toThrow = new Error('CONNRESET redis');
+    expect(await success()).toEqual({ ok: true, value: undefined });
+    expect(LINES(SUCCESS)).toHaveLength(1);
+    expect(reasonOf(LINES(SUCCESS)[0])).toBe('CONNRESET redis');
+  });
+  it('RED ks1868 R1 isLockedOut: a rejection that is a revoked Proxy fails open (false) and is logged as text, as for an ordinary Error', async () => {
+    h.toThrow = SHAPES[0][1]();
+    expect(await locked()).toEqual({ ok: true, value: false });
+    expect(LINES(LOCKED)).toHaveLength(1);
+    expect(reasonOf(LINES(LOCKED)[0])).toBe(SHAPES[0][2]);
+  });
+  it('RED ks1868 R2 isLockedOut: a rejection that is an Error whose message getter throws fails open (false) and is logged as text, as for an ordinary Error', async () => {
+    h.toThrow = SHAPES[1][1]();
+    expect(await locked()).toEqual({ ok: true, value: false });
+    expect(LINES(LOCKED)).toHaveLength(1);
+    expect(reasonOf(LINES(LOCKED)[0])).toBe(SHAPES[1][2]);
+  });
+  it('RED ks1868 R3 isLockedOut: a rejection that is an Error whose message is a null-prototype object fails open (false) and is logged as text, as for an ordinary Error', async () => {
+    h.toThrow = SHAPES[2][1]();
+    expect(await locked()).toEqual({ ok: true, value: false });
+    expect(LINES(LOCKED)).toHaveLength(1);
+    expect(reasonOf(LINES(LOCKED)[0])).toBe(SHAPES[2][2]);
+  });
+  it('RED ks1868 R4 isLockedOut: a rejection that is an Error whose message is a Symbol fails open (false) and is logged as text, as for an ordinary Error', async () => {
+    h.toThrow = SHAPES[3][1]();
+    expect(await locked()).toEqual({ ok: true, value: false });
+    expect(LINES(LOCKED)).toHaveLength(1);
+    expect(reasonOf(LINES(LOCKED)[0])).toBe(SHAPES[3][2]);
+  });
+  it('RED ks1868 R5 recordFailure: a rejection that is a revoked Proxy continues (0) and is logged as text, as for an ordinary Error', async () => {
+    h.toThrow = SHAPES[0][1]();
+    expect(await failure()).toEqual({ ok: true, value: 0 });
+    expect(LINES(FAILURE)).toHaveLength(1);
+    expect(reasonOf(LINES(FAILURE)[0])).toBe(SHAPES[0][2]);
+  });
+  it('RED ks1868 R6 recordFailure: a rejection that is an Error whose message is a Symbol continues (0) and is logged as text, as for an ordinary Error', async () => {
+    h.toThrow = SHAPES[3][1]();
+    expect(await failure()).toEqual({ ok: true, value: 0 });
+    expect(LINES(FAILURE)).toHaveLength(1);
+    expect(reasonOf(LINES(FAILURE)[0])).toBe(SHAPES[3][2]);
+  });
+  it('RED ks1868 R7 recordSuccess: a rejection that is a revoked Proxy is non-fatal (resolves) and is logged as text, as for an ordinary Error', async () => {
+    h.toThrow = SHAPES[0][1]();
+    expect(await success()).toEqual({ ok: true, value: undefined });
+    expect(LINES(SUCCESS)).toHaveLength(1);
+    expect(reasonOf(LINES(SUCCESS)[0])).toBe(SHAPES[0][2]);
+  });
+  it('RED ks1868 R8 recordSuccess: a rejection that is an Error whose message is a Symbol is non-fatal (resolves) and is logged as text, as for an ordinary Error', async () => {
+    h.toThrow = SHAPES[3][1]();
+    expect(await success()).toEqual({ ok: true, value: undefined });
+    expect(LINES(SUCCESS)).toHaveLength(1);
+    expect(reasonOf(LINES(SUCCESS)[0])).toBe(SHAPES[3][2]);
+  });
+});
```
