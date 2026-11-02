# READY — KS-1868-KS-1868-O88-P9 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o88_p9_api_gateway_redis_listener_and_connect_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 03:17 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o88_p9_api_gateway_redis_listener_and_connect_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o88_p9_api_gateway_redis_listener_and_connect_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o88_p9_api_gateway_redis_listener_and_connect_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o88_p9_api_gateway_redis_listener_and_connect_catch_guard_message-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 03:17 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o88_p9_api_gateway_redis_listener_and_connect_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `9d7e871fb771395772a3383eeea0833828fd5ba4`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/src/services/redis.ts } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-gateway-redis-listener-and-connect-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/services/redis.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-gateway-redis-listener-and-connect-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
18	4	Blockchain/Dev/services/api-gateway/src/services/redis.ts
154	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-gateway-redis-listener-and-connect-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (18 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: redis.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/api-gateway/src/services/redis.ts`; test(s): `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-gateway-redis-listener-and-connect-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/api-gateway/src/services/redis.ts 18 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-gateway-redis-listener-and-connect-catch-unreadable-throw.test.ts 154 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/services/redis.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-gateway-redis-listener-and-connect-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=6 of total=9; red cell(s): ['KS-1868 the gateway Redis listener and connect catch survive and log text for a hostile thrown value RED ks1868 R1: a revoked Proxy from connect in dev/test makes initRedis answer false and is logged as text, as for an ordinary Error', 'KS-1868 the gateway Redis listener and connect catch survive and log text for a hostile thrown value RED ks1868 R2: a revoked Proxy from connect in production rejects with the named production error and is logged as text, as for an ordinary Error', 'KS-1868 the gateway Redis listener and connect catch survive and log text for a hostile thrown value RED ks1868 R3: an Error whose message is a Symbol from connect in dev/test makes initRedis answer false and is logged as text, as for an ordinary Error', 'KS-1868 the gateway Redis listener and connect catch survive and log text for a hostile thrown value RED ks1868 R4: a revoked Proxy reaching the listener does not throw, is logged as text and clears the connected flag, as for an ordinary Error', 'KS-1868 the gateway Redis listener and connect catch survive and log text for a hostile thrown value RED ks1868 R5: an Error whose message getter throws reaching the listener does not throw, is logged as text and clears the connected flag, as for an ordinary Error', 'KS-1868 the gateway Redis listener and connect catch survive and log text for a hostile thrown value RED ks1868 R6: an Error whose message is a Symbol reaching the listener does not throw, is logged as text and clears the connected flag, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1412 failed=0 | after: total=1421 failed=0` · `NEW reds: []` [baseline_suite.json total=1412 failed=0; after_suite.json total=1421 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/services/redis.ts` (+18/-4 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-gateway-redis-listener-and-connect-catch-unreadable-throw.test.ts` (+154/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/api-gateway/src/services/redis.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `9d7e871fb771395772a3383eeea0833828fd5ba4` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o88_p9_api_gateway_redis_listener_and_connect_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o88_p9_api_gateway_redis_listener_and_connect_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o88_p9_api_gateway_redis_listener_and_connect_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/services/redis.ts b/Blockchain/Dev/services/api-gateway/src/services/redis.ts
--- a/Blockchain/Dev/services/api-gateway/src/services/redis.ts
+++ b/Blockchain/Dev/services/api-gateway/src/services/redis.ts
@@ -91,4 +91,11 @@
     redisClient.on('error', (err) => {
-      logger.error('[Redis] Connection error', { error: err.message });
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('[Redis] Connection error', { error: reason });
       isConnected = false;
     });
@@ -106,6 +113,13 @@
     logger.info('[Redis] Connection test successful');
     return true;
   } catch (error) {
+    let reason: string | null | undefined;
+    try {
+      const m = (error as Error)?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
     // Pen-test M4 fix: production REFUSES to start without Redis. Rate limit
     // + sessions are both Redis-backed; falling back to per-pod in-memory
     // means each replica has its own counter (effectively no rate limit
@@ -114,11 +128,11 @@
     // flowing.
     if (process.env.NODE_ENV === 'production') {
       logger.error('[Redis] FATAL: connection failed in production — refusing to start', {
-        error: (error as Error).message,
+        error: reason,
       });
-      throw new Error('REDIS_REQUIRED_IN_PRODUCTION: ' + (error as Error).message);
+      throw new Error('REDIS_REQUIRED_IN_PRODUCTION: ' + reason);
     }
-    logger.warn('[Redis] Failed to connect, using in-memory fallback (dev/test only)', { error: (error as Error).message });
+    logger.warn('[Redis] Failed to connect, using in-memory fallback (dev/test only)', { error: reason });
     fallbackMode = true;
     return false;
   }
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-gateway-redis-listener-and-connect-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-gateway-redis-listener-and-connect-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-gateway-redis-listener-and-connect-catch-unreadable-throw.test.ts
@@ -0,0 +1,154 @@
+import { describe, it, expect, beforeEach, afterAll, vi } from 'vitest';
+
+// KS-1868 (operator 88 screen, api-gateway redis service): the Redis client 'error' listener (line 92) and the connect catch
+// (lines 117-125) of services/api-gateway/src/services/redis.ts read the thrown value's message unguarded. A thrown value whose
+// read throws (a revoked Proxy, an Error whose message getter throws) makes the listener throw BEFORE it clears the
+// connected flag (so isRedisAvailable() keeps answering true while Redis is down) and makes the catch throw a TypeError from
+// inside the catch (initRedis rejects with it, instead of falling back in dev/test or refusing with the named production
+// error); an Error whose message is a Symbol is passed to the logger uncoerced. The cells make the client emit / fail with
+// such a value and assert the outcome an ordinary Error gets, with text in the log. Harness: the real module with ioredis
+// replaced by a plain stand-in class (it hands over its listeners; connect rejects with the value when asked) and the logger
+// by a plain recording object.
+const h = vi.hoisted(() => ({
+  listeners: {} as Record<string, (e: unknown) => void>,
+  connectFailure: undefined as undefined | { value: unknown },
+  logs: [] as { level: string; message: string; meta: Record<string, unknown> | undefined }[],
+}));
+
+vi.mock('ioredis', () => ({
+  default: function RedisMock() {
+    return {
+      on: (event: string, fn: (e: unknown) => void) => {
+        h.listeners[event] = fn;
+      },
+      connect: async () => {
+        if (h.connectFailure) throw h.connectFailure.value;
+      },
+      ping: async () => 'PONG',
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
+type Rs = typeof import('../services/redis');
+const realEnv = process.env.NODE_ENV;
+afterAll(() => {
+  process.env.NODE_ENV = realEnv;
+});
+beforeEach(() => {
+  h.listeners = {};
+  h.connectFailure = undefined;
+  h.logs.length = 0;
+  process.env.NODE_ENV = 'test';
+});
+
+async function freshRedis(): Promise<Rs> {
+  vi.resetModules();
+  return import('../services/redis');
+}
+async function emit(value: unknown): Promise<{ threw: boolean; available: boolean }> {
+  const rs = await freshRedis();
+  await rs.initRedis();
+  let threw = false;
+  try {
+    h.listeners.error(value);
+  } catch {
+    threw = true;
+  }
+  return { threw, available: rs.isRedisAvailable() };
+}
+async function connectFails(value: unknown, env: string): Promise<{ resolved: boolean; value: boolean | undefined; message: string }> {
+  process.env.NODE_ENV = env;
+  h.connectFailure = { value };
+  const rs = await freshRedis();
+  try {
+    return { resolved: true, value: await rs.initRedis(), message: '' };
+  } catch (e) {
+    return { resolved: false, value: undefined, message: (e as Error).message };
+  }
+}
+const LINE = (prefix: string): { level: string; message: string; meta: Record<string, unknown> | undefined }[] =>
+  h.logs.filter((l) => l.message.startsWith(prefix));
+const LISTENER = '[Redis] Connection error';
+const FALLBACK = '[Redis] Failed to connect, using in-memory fallback';
+const FATAL = '[Redis] FATAL';
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
+describe('KS-1868 the gateway Redis listener and connect catch survive and log text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error from connect in dev/test makes initRedis answer false and is logged with its message', async () => {
+    expect(await connectFails(new Error('connect boom'), 'test')).toEqual({ resolved: true, value: false, message: '' });
+    expect(LINE(FALLBACK)).toHaveLength(1);
+    expect(reasonOf(LINE(FALLBACK)[0])).toBe('connect boom');
+  });
+  it('control ks1868 C2: an ordinary Error from connect in production rejects with the named production error carrying its message', async () => {
+    expect(await connectFails(new Error('connect boom'), 'production')).toEqual({
+      resolved: false,
+      value: undefined,
+      message: 'REDIS_REQUIRED_IN_PRODUCTION: connect boom',
+    });
+    expect(LINE(FATAL)).toHaveLength(1);
+    expect(reasonOf(LINE(FATAL)[0])).toBe('connect boom');
+  });
+  it('control ks1868 C3: an ordinary Error reaching the listener does not throw, is logged with its message and clears the connected flag', async () => {
+    expect(await emit(new Error('listener boom'))).toEqual({ threw: false, available: false });
+    expect(LINE(LISTENER)).toHaveLength(1);
+    expect(reasonOf(LINE(LISTENER)[0])).toBe('listener boom');
+  });
+  it('RED ks1868 R1: a revoked Proxy from connect in dev/test makes initRedis answer false and is logged as text, as for an ordinary Error', async () => {
+    expect(await connectFails(revokedProxy(), 'test')).toEqual({ resolved: true, value: false, message: '' });
+    expect(LINE(FALLBACK)).toHaveLength(1);
+    expect(reasonOf(LINE(FALLBACK)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: a revoked Proxy from connect in production rejects with the named production error and is logged as text, as for an ordinary Error', async () => {
+    expect(await connectFails(revokedProxy(), 'production')).toEqual({
+      resolved: false,
+      value: undefined,
+      message: 'REDIS_REQUIRED_IN_PRODUCTION: unreadable thrown value',
+    });
+    expect(LINE(FATAL)).toHaveLength(1);
+    expect(reasonOf(LINE(FATAL)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R3: an Error whose message is a Symbol from connect in dev/test makes initRedis answer false and is logged as text, as for an ordinary Error', async () => {
+    expect(await connectFails(withMessage(Symbol('ks1868')), 'test')).toEqual({ resolved: true, value: false, message: '' });
+    expect(LINE(FALLBACK)).toHaveLength(1);
+    expect(reasonOf(LINE(FALLBACK)[0])).toBe('Symbol(ks1868)');
+  });
+  it('RED ks1868 R4: a revoked Proxy reaching the listener does not throw, is logged as text and clears the connected flag, as for an ordinary Error', async () => {
+    expect(await emit(revokedProxy())).toEqual({ threw: false, available: false });
+    expect(LINE(LISTENER)).toHaveLength(1);
+    expect(reasonOf(LINE(LISTENER)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R5: an Error whose message getter throws reaching the listener does not throw, is logged as text and clears the connected flag, as for an ordinary Error', async () => {
+    expect(await emit(getterThrows())).toEqual({ threw: false, available: false });
+    expect(LINE(LISTENER)).toHaveLength(1);
+    expect(reasonOf(LINE(LISTENER)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R6: an Error whose message is a Symbol reaching the listener does not throw, is logged as text and clears the connected flag, as for an ordinary Error', async () => {
+    expect(await emit(withMessage(Symbol('ks1868')))).toEqual({ threw: false, available: false });
+    expect(LINE(LISTENER)).toHaveLength(1);
+    expect(reasonOf(LINE(LISTENER)[0])).toBe('Symbol(ks1868)');
+  });
+});
```
