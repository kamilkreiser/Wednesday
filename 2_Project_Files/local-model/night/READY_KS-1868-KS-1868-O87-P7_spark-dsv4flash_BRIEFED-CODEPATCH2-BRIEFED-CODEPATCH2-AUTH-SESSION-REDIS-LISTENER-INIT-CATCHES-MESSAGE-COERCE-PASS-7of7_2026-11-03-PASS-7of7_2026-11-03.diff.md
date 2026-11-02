# READY — KS-1868-KS-1868-O87-P7 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p7_auth_session_redis_listener_and_init_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 01:44 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p7_auth_session_redis_listener_and_init_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p7_auth_session_redis_listener_and_init_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p7_auth_session_redis_listener_and_init_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p7_auth_session_redis_listener_and_init_catches_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 01:44 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p7_auth_session_redis_listener_and_init_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8150eeb3802bd9cfe5242ffbc49278c1a3739a84`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/services/session.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-session-listener-and-init-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/services/session.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-session-listener-and-init-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
16	2	Blockchain/Dev/services/auth/src/services/session.ts
148	0	Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-session-listener-and-init-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (16 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: session.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/services/session.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-session-listener-and-init-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/services/session.ts 16 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-session-listener-and-init-catch-unreadable-throw.test.ts 148 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/services/session.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-session-listener-and-init-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (5 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=5 of total=9; red cell(s): ['KS-1868 the session store Redis listener and init catch survive and log text for a hostile thrown value RED ks1868 R1: a revoked Proxy reaching the Redis listener does not throw, marks Redis unavailable and is logged as text, as for an ordinary Error', 'KS-1868 the session store Redis listener and init catch survive and log text for a hostile thrown value RED ks1868 R2: an Error whose message is a Symbol reaching the Redis listener does not throw, marks Redis unavailable and is logged as text, as for an ordinary Error', 'KS-1868 the session store Redis listener and init catch survive and log text for a hostile thrown value RED ks1868 R3: a revoked Proxy from connect leaves initRedisSession resolving with Redis unavailable and is logged as text, as for an ordinary Error', 'KS-1868 the session store Redis listener and init catch survive and log text for a hostile thrown value RED ks1868 R4: an Error whose message getter throws from connect leaves initRedisSession resolving with Redis unavailable and is logged as text, as for an ordinary Error', 'KS-1868 the session store Redis listener and init catch survive and log text for a hostile thrown value RED ks1868 R5: an Error whose message is a Symbol from connect leaves initRedisSession resolving with Redis unavailable and is logged as text, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1536 failed=1 | after: total=1545 failed=0` · `NEW reds: []` [baseline_suite.json total=1536 failed=1; after_suite.json total=1545 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/services/session.ts` (+16/-2 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-session-listener-and-init-catch-unreadable-throw.test.ts` (+148/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/services/session.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8150eeb3802bd9cfe5242ffbc49278c1a3739a84` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p7_auth_session_redis_listener_and_init_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o87_p7_auth_session_redis_listener_and_init_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p7_auth_session_redis_listener_and_init_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/services/session.ts b/Blockchain/Dev/services/auth/src/services/session.ts
--- a/Blockchain/Dev/services/auth/src/services/session.ts
+++ b/Blockchain/Dev/services/auth/src/services/session.ts
@@ -58,4 +58,11 @@
     redis.on('error', (err: Error) => {
-      logger.error('Redis error', { error: err.message });
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('Redis error', { error: reason });
       redisAvailable = false;
     });
@@ -69,7 +76,14 @@
       logger.info('Redis ready');
     });
   } catch (err: any) {
-    logger.warn('Redis unavailable — using in-memory session fallback', { error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('Redis unavailable — using in-memory session fallback', { error: reason });
     redisAvailable = false;
   }
 }
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-session-listener-and-init-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-session-listener-and-init-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-session-listener-and-init-catch-unreadable-throw.test.ts
@@ -0,0 +1,148 @@
+import { describe, it, expect, beforeEach, afterAll, vi } from 'vitest';
+
+// KS-1868 (operator 87 screen, auth session store): the Redis 'error' listener (line 59) and the init catch (line 72) of
+// services/auth/src/services/session.ts pass `err.message` / `err?.message` straight into the logger's meta object,
+// unguarded. A thrown value whose read throws (a revoked Proxy, an Error whose message getter throws) makes the listener /
+// the catch itself throw: an exception thrown by a listener of the client's 'error' event escapes the EventEmitter as an
+// uncaught exception BEFORE the line `redisAvailable = false` runs (the flag stays true while the client is down), and a
+// throwing init catch makes initRedisSession REJECT instead of falling back to the in-memory sessions with the flag false;
+// an Error whose message is not a string (a Symbol) is passed to the logger uncoerced. The cells emit such a value to the
+// captured listener / make the client's connect reject with it and assert the listener returns, the availability flag is
+// false, initRedisSession resolves and the logged value is text (the constant when the value cannot be turned into text).
+// Harness: the real module with ioredis replaced by a plain stand-in class and the logger by a plain recording object.
+const h = vi.hoisted(() => ({
+  listener: undefined as undefined | ((e: unknown) => void),
+  connectFailure: undefined as undefined | { value: unknown },
+  logs: [] as { level: string; message: string; meta: Record<string, unknown> | undefined }[],
+}));
+
+vi.mock('ioredis', () => ({
+  default: function RedisMock() {
+    return {
+      status: 'wait',
+      on: (event: string, fn: (e: unknown) => void) => {
+        if (event === 'error') h.listener = fn;
+      },
+      connect: async () => {
+        if (h.connectFailure) throw h.connectFailure.value;
+      },
+      ping: async () => 'PONG',
+      disconnect: () => undefined,
+    };
+  },
+}));
+vi.mock('../utils/logger', () => {
+  const rec = (level: string) => (message: string, meta?: Record<string, unknown>) => {
+    h.logs.push({ level, message, meta });
+  };
+  return { logger: { debug: rec('debug'), info: rec('info'), warn: rec('warn'), error: rec('error') } };
+});
+
+type Sess = typeof import('../services/session');
+const realUrl = process.env.REDIS_URL;
+afterAll(() => {
+  if (realUrl === undefined) delete process.env.REDIS_URL;
+  else process.env.REDIS_URL = realUrl;
+});
+beforeEach(() => {
+  h.listener = undefined;
+  h.connectFailure = undefined;
+  h.logs.length = 0;
+  process.env.REDIS_URL = 'redis://localhost:6379';
+});
+
+async function freshSession(): Promise<Sess> {
+  vi.resetModules();
+  return import('../services/session');
+}
+async function emit(value: unknown): Promise<{ threw: boolean; available: boolean }> {
+  const sess = await freshSession();
+  await sess.initRedisSession();
+  try {
+    (h.listener as (e: unknown) => void)(value);
+    return { threw: false, available: sess.isRedisAvailable() };
+  } catch {
+    return { threw: true, available: sess.isRedisAvailable() };
+  }
+}
+async function init(value: unknown): Promise<{ ok: boolean; available: boolean | undefined }> {
+  h.connectFailure = { value };
+  const sess = await freshSession();
+  try {
+    await sess.initRedisSession();
+    return { ok: true, available: sess.isRedisAvailable() };
+  } catch {
+    return { ok: false, available: undefined };
+  }
+}
+const LINE = (message: string): { level: string; message: string; meta: Record<string, unknown> | undefined }[] =>
+  h.logs.filter((l) => l.message === message);
+const LISTENER = 'Redis error';
+const INIT = 'Redis unavailable — using in-memory session fallback';
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
+describe('KS-1868 the session store Redis listener and init catch survive and log text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error reaching the Redis listener does not throw, marks Redis unavailable and is logged with its message', async () => {
+    expect(await emit(new Error('redis boom'))).toEqual({ threw: false, available: false });
+    expect(LINE(LISTENER)).toHaveLength(1);
+    expect(reasonOf(LINE(LISTENER)[0])).toBe('redis boom');
+  });
+  it('control ks1868 C2: a plain string reaching the Redis listener does not throw, marks Redis unavailable and is logged without a message', async () => {
+    expect(await emit('plain boom')).toEqual({ threw: false, available: false });
+    expect(LINE(LISTENER)).toHaveLength(1);
+    expect(reasonOf(LINE(LISTENER)[0])).toBe('<undefined>');
+  });
+  it('control ks1868 C3: an ordinary Error from connect leaves initRedisSession resolving with Redis unavailable and is logged with its message', async () => {
+    expect(await init(new Error('connect boom'))).toEqual({ ok: true, available: false });
+    expect(LINE(INIT)).toHaveLength(1);
+    expect(reasonOf(LINE(INIT)[0])).toBe('connect boom');
+  });
+  it('control ks1868 C4: a thrown number from connect leaves initRedisSession resolving with Redis unavailable and is logged without a message', async () => {
+    expect(await init(42)).toEqual({ ok: true, available: false });
+    expect(LINE(INIT)).toHaveLength(1);
+    expect(reasonOf(LINE(INIT)[0])).toBe('<undefined>');
+  });
+  it('RED ks1868 R1: a revoked Proxy reaching the Redis listener does not throw, marks Redis unavailable and is logged as text, as for an ordinary Error', async () => {
+    expect(await emit(revokedProxy())).toEqual({ threw: false, available: false });
+    expect(LINE(LISTENER)).toHaveLength(1);
+    expect(reasonOf(LINE(LISTENER)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message is a Symbol reaching the Redis listener does not throw, marks Redis unavailable and is logged as text, as for an ordinary Error', async () => {
+    expect(await emit(withMessage(Symbol('ks1868')))).toEqual({ threw: false, available: false });
+    expect(LINE(LISTENER)).toHaveLength(1);
+    expect(reasonOf(LINE(LISTENER)[0])).toBe('Symbol(ks1868)');
+  });
+  it('RED ks1868 R3: a revoked Proxy from connect leaves initRedisSession resolving with Redis unavailable and is logged as text, as for an ordinary Error', async () => {
+    expect(await init(revokedProxy())).toEqual({ ok: true, available: false });
+    expect(LINE(INIT)).toHaveLength(1);
+    expect(reasonOf(LINE(INIT)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R4: an Error whose message getter throws from connect leaves initRedisSession resolving with Redis unavailable and is logged as text, as for an ordinary Error', async () => {
+    expect(await init(getterThrows())).toEqual({ ok: true, available: false });
+    expect(LINE(INIT)).toHaveLength(1);
+    expect(reasonOf(LINE(INIT)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R5: an Error whose message is a Symbol from connect leaves initRedisSession resolving with Redis unavailable and is logged as text, as for an ordinary Error', async () => {
+    expect(await init(withMessage(Symbol('ks1868')))).toEqual({ ok: true, available: false });
+    expect(LINE(INIT)).toHaveLength(1);
+    expect(reasonOf(LINE(INIT)[0])).toBe('Symbol(ks1868)');
+  });
+});
```
