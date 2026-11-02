# READY — KS-1868-KS-1868-O90-P2 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p2_demo_service_state_redis_listener_and_presenter_mode_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 05:17 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p2_demo_service_state_redis_listener_and_presenter_mode_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p2_demo_service_state_redis_listener_and_presenter_mode_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p2_demo_service_state_redis_listener_and_presenter_mode_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p2_demo_service_state_redis_listener_and_presenter_mode_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 05:17 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p2_demo_service_state_redis_listener_and_presenter_mode_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `4307ac876caea7d1835b17d6360760b7ec6e6bbe`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/demo-service/src/routes/state.ts } + { Blockchain/Dev/services/demo-service/src/__tests__/ks1868-state-redis-listener-and-presenter-mode-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/demo-service/src/routes/state.ts` (product) and `Blockchain/Dev/services/demo-service/src/__tests__/ks1868-state-redis-listener-and-presenter-mode-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
13	2	Blockchain/Dev/services/demo-service/src/routes/state.ts
153	0	Blockchain/Dev/services/demo-service/src/__tests__/ks1868-state-redis-listener-and-presenter-mode-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (13 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: state.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/demo-service/src/routes/state.ts`; test(s): `Blockchain/Dev/services/demo-service/src/__tests__/ks1868-state-redis-listener-and-presenter-mode-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/demo-service/src/routes/state.ts 13 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/demo-service/src/__tests__/ks1868-state-redis-listener-and-presenter-mode-unreadable-throw.test.ts 153 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/demo-service/src/routes/state.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/demo-service/src/__tests__/ks1868-state-redis-listener-and-presenter-mode-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1868 demo-service state: the Redis error listener and the presenter-mode catch read the thrown value safely RED ks1868 R1 a revoked Proxy reaching the Redis listener does not throw and is logged as text', 'KS-1868 demo-service state: the Redis error listener and the presenter-mode catch read the thrown value safely RED ks1868 R2 an Error whose message getter throws reaching the Redis listener does not throw and is logged as text', 'KS-1868 demo-service state: the Redis error listener and the presenter-mode catch read the thrown value safely RED ks1868 R3 a revoked Proxy from the presenter-mode write is logged as text and answered with the 500 body', 'KS-1868 demo-service state: the Redis error listener and the presenter-mode catch read the thrown value safely RED ks1868 R4 an Error whose message getter throws from the presenter-mode write is logged as text and answered with the 500 body']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=97 failed=0 | after: total=103 failed=0` · `NEW reds: []` [baseline_suite.json total=97 failed=0; after_suite.json total=103 failed=0]
- A6 [verbatim]: `PASS A6 whole services/demo-service suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/demo-service: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/demo-service/src/routes/state.ts` (+13/-2 per numstat.out) and the test file `Blockchain/Dev/services/demo-service/src/__tests__/ks1868-state-redis-listener-and-presenter-mode-unreadable-throw.test.ts` (+153/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/demo-service/src/routes/state.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `4307ac876caea7d1835b17d6360760b7ec6e6bbe` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p2_demo_service_state_redis_listener_and_presenter_mode_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o90_p2_demo_service_state_redis_listener_and_presenter_mode_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p2_demo_service_state_redis_listener_and_presenter_mode_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/demo-service/src/routes/state.ts b/Blockchain/Dev/services/demo-service/src/routes/state.ts
--- a/Blockchain/Dev/services/demo-service/src/routes/state.ts
+++ b/Blockchain/Dev/services/demo-service/src/routes/state.ts
@@ -43,4 +43,10 @@
     redis.on('error', (err) => {
-      logger.warn('Redis unavailable, using in-memory state', { error: err.message });
+      let message: string;
+      try {
+        message = err instanceof Error ? err.message : 'Unknown error';
+      } catch {
+        message = 'unreadable thrown value';
+      }
+      logger.warn('Redis unavailable, using in-memory state', { error: message });
       redis = null;
     });
@@ -112,7 +118,12 @@
     logger.info('Presenter mode toggled', { enabled: value });
     return res.json({ success: true, presenterMode: value });
   } catch (err) {
-    const message = err instanceof Error ? err.message : 'Unknown error';
+    let message: string;
+    try {
+      message = err instanceof Error ? err.message : 'Unknown error';
+    } catch {
+      message = 'unreadable thrown value';
+    }
     logger.error('Failed to toggle presenter mode', { error: message });
     return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
   }
diff --git a/Blockchain/Dev/services/demo-service/src/__tests__/ks1868-state-redis-listener-and-presenter-mode-unreadable-throw.test.ts b/Blockchain/Dev/services/demo-service/src/__tests__/ks1868-state-redis-listener-and-presenter-mode-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/demo-service/src/__tests__/ks1868-state-redis-listener-and-presenter-mode-unreadable-throw.test.ts
@@ -0,0 +1,153 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-1868 (operator 90 screen, demo-service state routes): two places of services/demo-service/src/routes/state.ts read a
+// thrown value unguarded. (1) The Redis client 'error' listener in getRedis (line 44) passes `err.message` into logger.warn
+// BEFORE it sets `redis = null`: a value whose read throws (a revoked Proxy, an Error whose message getter throws) makes the
+// listener throw (an uncaught exception from the client's EventEmitter) and leaves the dead client in place. (2) The catch
+// of POST /presenter-mode (line 112) reads `err instanceof Error ? err.message : ...` outside any guard: the catch throws,
+// so the handler rejects and the request never gets its 500. The fix is the guard the GET /state catch of this same file
+// already uses (the read inside a try, the constant 'unreadable thrown value' when the read throws).
+// The Redis stand-in is a plain class, not a vi.fn(): a spy could inspect a revoked Proxy and fail before the code under
+// test saw it. The logger is a recording stand-in; no Redis, no network.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  listener: undefined as undefined | ((e: unknown) => void),
+  warn: vi.fn(),
+  error: vi.fn(),
+}));
+
+vi.mock('ioredis', () => ({
+  default: class {
+    on(event: string, fn: (e: unknown) => void) {
+      if (event === 'error') h.listener = fn;
+      return this;
+    }
+    get() {
+      return Promise.resolve(null);
+    }
+    set() {
+      return Promise.reject(h.toThrow);
+    }
+  },
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: { debug: vi.fn(), info: vi.fn(), warn: h.warn, error: h.error },
+  createLogger: () => ({ debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn() }),
+}));
+
+import { stateRouter } from '../routes/state';
+
+type Handler = (req: unknown, res: unknown) => unknown;
+type Layer = { route?: { path: string; stack: Array<{ handle: Handler }> } };
+type Outcome = { threw: boolean; status?: number; body?: unknown };
+
+function handlerFor(path: string): Handler {
+  const layer = (stateRouter as unknown as { stack: Layer[] }).stack.find((l) => l.route?.path === path);
+  return layer!.route!.stack[0].handle;
+}
+
+async function run(path: string, req: unknown): Promise<Outcome> {
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
+  try {
+    await handlerFor(path)(req, res);
+  } catch {
+    out.threw = true;
+  }
+  return out;
+}
+
+/** Make getRedis create the client (so the 'error' listener is attached), then emit the value to the listener. */
+async function emit(value: unknown): Promise<{ threw: boolean }> {
+  await run('/state', {});
+  try {
+    (h.listener as (e: unknown) => void)(value);
+    return { threw: false };
+  } catch {
+    return { threw: true };
+  }
+}
+
+const WARNS = () => h.warn.mock.calls.filter((c) => String(c[0]).includes('Redis unavailable'));
+const ERRORS = () => h.error.mock.calls.filter((c) => String(c[0]).includes('Failed to toggle presenter mode'));
+
+const revokedProxy = (): unknown => {
+  const rp = Proxy.revocable({}, {});
+  rp.revoke();
+  return rp.proxy;
+};
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+describe('KS-1868 demo-service state: the Redis error listener and the presenter-mode catch read the thrown value safely', () => {
+  beforeEach(() => {
+    process.env.REDIS_URL = 'redis://127.0.0.1:1';
+    h.toThrow = undefined;
+    h.warn.mockReset();
+    h.error.mockReset();
+  });
+
+  it('control ks1868 C1 an ordinary Error reaching the Redis listener does not throw and is logged with its message', async () => {
+    expect(await emit(new Error('redis boom'))).toEqual({ threw: false });
+    expect(WARNS()).toHaveLength(1);
+    expect(WARNS()[0][1]).toEqual({ error: 'redis boom' });
+  });
+
+  it('control ks1868 C2 an ordinary Error from the presenter-mode write is logged and answered with the 500 body', async () => {
+    h.toThrow = new Error('redis boom');
+    const out = await run('/presenter-mode', { body: { enabled: true } });
+    expect(out.threw).toBe(false);
+    expect(out.status).toBe(500);
+    expect(out.body).toEqual({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
+    expect(ERRORS()).toHaveLength(1);
+    expect(ERRORS()[0][1]).toEqual({ error: 'redis boom' });
+  });
+
+  it('RED ks1868 R1 a revoked Proxy reaching the Redis listener does not throw and is logged as text', async () => {
+    expect(await emit(revokedProxy())).toEqual({ threw: false });
+    expect(WARNS()).toHaveLength(1);
+    expect(WARNS()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws reaching the Redis listener does not throw and is logged as text', async () => {
+    expect(await emit(getterThrows())).toEqual({ threw: false });
+    expect(WARNS()).toHaveLength(1);
+    expect(WARNS()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R3 a revoked Proxy from the presenter-mode write is logged as text and answered with the 500 body', async () => {
+    h.toThrow = revokedProxy();
+    const out = await run('/presenter-mode', { body: { enabled: true } });
+    expect(out.threw).toBe(false);
+    expect(out.status).toBe(500);
+    expect(out.body).toEqual({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
+    expect(ERRORS()).toHaveLength(1);
+    expect(ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R4 an Error whose message getter throws from the presenter-mode write is logged as text and answered with the 500 body', async () => {
+    h.toThrow = getterThrows();
+    const out = await run('/presenter-mode', { body: { enabled: true } });
+    expect(out.threw).toBe(false);
+    expect(out.status).toBe(500);
+    expect(out.body).toEqual({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
+    expect(ERRORS()).toHaveLength(1);
+    expect(ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+});
```
