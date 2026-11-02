# READY — KS-1868-KS-1868-O83-P4 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p4_apigateway_rate_limit_enforce_catches_coerce_message/out.md.checker/patch.diff`** (from `ls` at 22:09 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p4_apigateway_rate_limit_enforce_catches_coerce_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p4_apigateway_rate_limit_enforce_catches_coerce_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p4_apigateway_rate_limit_enforce_catches_coerce_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p4_apigateway_rate_limit_enforce_catches_coerce_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 22:09 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p4_apigateway_rate_limit_enforce_catches_coerce_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `58b5042ccdb5a06a213ba53f5d4f7644f5f52549`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-rate-limit-enforce-message-coercion-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-rate-limit-enforce-message-coercion-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
14	2	Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts
164	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-rate-limit-enforce-message-coercion-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (14 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: rateLimitEnforce.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts`; test(s): `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-rate-limit-enforce-message-coercion-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts 14 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-rate-limit-enforce-message-coercion-unreadable-throw.test.ts 164 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-rate-limit-enforce-message-coercion-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 10 run; controls green; assertion reds)` [red_first.json: failed=6 of total=10; red cell(s): ['KS-1868 the per-client rate limiter logs text for a hostile thrown value RED ks1868 R1 a Redis rejection that is a revoked Proxy logs the constant reason and the degraded ceiling applies', 'KS-1868 the per-client rate limiter logs text for a hostile thrown value RED ks1868 R2 a Redis error whose message is a null-prototype object logs the constant reason and the degraded ceiling applies', 'KS-1868 the per-client rate limiter logs text for a hostile thrown value RED ks1868 R3 a Redis error whose message is a Symbol logs the Symbol text and the degraded ceiling applies', 'KS-1868 the per-client rate limiter logs text for a hostile thrown value RED ks1868 R4 a header write that throws a revoked Proxy logs the constant reason and the request is let through', 'KS-1868 the per-client rate limiter logs text for a hostile thrown value RED ks1868 R5 a header write that throws an Error whose message is a null-prototype object logs the constant reason and the request is let through', 'KS-1868 the per-client rate limiter logs text for a hostile thrown value RED ks1868 R6 a header write that throws an Error whose message is a Symbol logs the Symbol text and the request is let through']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (10 passed / 10 run)` [green_after.json: failed=0 of total=10, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1412 failed=0 | after: total=1422 failed=0` · `NEW reds: []` [baseline_suite.json total=1412 failed=0; after_suite.json total=1422 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts` (+14/-2 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-rate-limit-enforce-message-coercion-unreadable-throw.test.ts` (+164/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `58b5042ccdb5a06a213ba53f5d4f7644f5f52549` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p4_apigateway_rate_limit_enforce_catches_coerce_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o83_p4_apigateway_rate_limit_enforce_catches_coerce_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p4_apigateway_rate_limit_enforce_catches_coerce_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts b/Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts
--- a/Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts
+++ b/Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts
@@ -44,11 +44,17 @@
   const now = Date.now();
   if (now - lastDegradeLogAt < DEGRADE_LOG_INTERVAL_MS) return;
   lastDegradeLogAt = now;
+  let errorText: string | undefined;
+  try {
+    errorText = err instanceof Error ? String(err.message) : err ? String(err) : undefined;
+  } catch {
+    errorText = 'unreadable thrown value';
+  }
   logger.warn('[rateLimit] DEGRADED — per-client ceiling is no longer distributed', {
     reason,
     clientId,
     effect: 'counting per-replica in memory; the effective ceiling inflates to limit × replicas',
-    error: err instanceof Error ? err.message : err ? String(err) : undefined,
+    error: errorText,
     throttledFor: `${DEGRADE_LOG_INTERVAL_MS / 1000}s`,
   });
 }
@@ -297,9 +303,15 @@
       } catch (writeErr) {
         // e.g. the response is already committed. Same rule as above: a bookkeeping
         // failure does not 500 the caller, and it is not silent.
+        let reason: string;
+        try {
+          reason = String(writeErr instanceof Error ? writeErr.message : writeErr);
+        } catch {
+          reason = 'unreadable thrown value';
+        }
         logger.error('[rateLimit] could not write the rate-limit headers or the 429 — request allowed unlimited', {
           clientId,
-          error: writeErr instanceof Error ? writeErr.message : String(writeErr),
+          error: reason,
         });
         refused = false;
       }
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-rate-limit-enforce-message-coercion-unreadable-throw.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-rate-limit-enforce-message-coercion-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-rate-limit-enforce-message-coercion-unreadable-throw.test.ts
@@ -0,0 +1,164 @@
+import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
+
+// KS-1868: two catches of the api-gateway per-client rate limiter read a caught value unguarded. (1) `logDegraded` reads the Redis error as
+// `err instanceof Error ? err.message : err ? String(err) : undefined` INSIDE the try whose catch is the in-memory fallback: a revoked Proxy (or
+// an Error whose message getter throws) makes that read throw, the catch reports "in-memory fallback ALSO failed" and the request is let through
+// UNCOUNTED; an Error whose message is a non-string is handed to the logger as is. (2) The `writeErr` catch reads `writeErr instanceof Error ? ... :
+// String(writeErr)` inline: a hostile value makes the middleware itself reject. The cells assert the ordinary-Error rows for hostile values: the
+// degraded in-memory ceiling still applies (the second request over a limit of 1 is refused 429), the line carries text (the constant when the value
+// cannot be turned into text), and a failed header write lets the request through. Controls pin an ordinary Error and a thrown plain string.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  warned: [] as unknown[][],
+  errored: [] as unknown[][],
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: {
+    info: () => undefined,
+    debug: () => undefined,
+    warn: (...args: unknown[]) => {
+      h.warned.push(args);
+    },
+    error: (...args: unknown[]) => {
+      h.errored.push(args);
+    },
+  },
+}));
+
+import { enforceClientRateLimit } from '../middleware/rateLimitEnforce';
+
+const CONSTANT = 'unreadable thrown value';
+let when = Date.parse('2030-01-01T00:00:00Z');
+let n = 0;
+
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.warned.length = 0;
+  h.errored.length = 0;
+  // logDegraded throttles to one line per 30 s on a module-level clock: move the clock on for every cell.
+  when += 120_000;
+  vi.useFakeTimers({ toFake: ['Date'] });
+  vi.setSystemTime(when);
+});
+
+afterEach(() => {
+  vi.useRealTimers();
+});
+
+const revokedProxy = (): unknown => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+/** An Error whose `message` getter succeeds and returns the (non-string) value m. */
+const withMessage = (m: unknown): unknown => Object.create(Error.prototype, { message: { get() { return m; } } });
+/** The logged `error` field of a logger call as a string; the type name when it is not one. */
+const reasonOf = (c: unknown[] | undefined): string => {
+  const v = (c?.[1] as { error?: unknown } | undefined)?.error;
+  return typeof v === 'string' ? v : '<' + typeof v + '>';
+};
+
+function makeRes(setHeaderThrows: boolean) {
+  const res: any = {
+    statusCode: undefined as number | undefined,
+    setHeader: (..._args: unknown[]) => {
+      if (setHeaderThrows) throw h.toThrow;
+    },
+    status: (code: number) => {
+      res.statusCode = code;
+      return res;
+    },
+    json: () => res,
+  };
+  return res;
+}
+
+async function hit(connectorId: string, redis: unknown, setHeaderThrows: boolean) {
+  const mw = enforceClientRateLimit(redis as any);
+  const req = { user: { authMethod: 'api_key', connectorId, rateLimit: 1, rateLimitWindow: 60 } } as any;
+  const res = makeRes(setHeaderThrows);
+  let nextCalls = 0;
+  let rejected = false;
+  try {
+    await mw(req, res, () => {
+      nextCalls += 1;
+    });
+  } catch {
+    rejected = true;
+  }
+  return { rejected, nextCalls, status: res.statusCode as number | undefined };
+}
+
+const redisFailing = () => ({
+  status: 'ready',
+  incr: (..._args: unknown[]) => Promise.reject(h.toThrow),
+  pexpire: async () => 1,
+  pttl: async () => 60_000,
+});
+
+/** Two requests of one client over a limit of 1 while Redis rejects with `thrown`: the degraded ceiling must apply. */
+async function degraded(thrown: unknown, reason: string): Promise<void> {
+  h.toThrow = thrown;
+  const id = `ks1868-degraded-${(n += 1)}`;
+  const redis = redisFailing();
+  const first = await hit(id, redis, false);
+  const second = await hit(id, redis, false);
+  expect(first).toEqual({ rejected: false, nextCalls: 1, status: undefined });
+  expect(second).toEqual({ rejected: false, nextCalls: 0, status: 429 });
+  expect(h.warned).toHaveLength(1);
+  expect(reasonOf(h.warned[0])).toBe(reason);
+  expect(h.errored).toHaveLength(0);
+}
+
+/** One request whose header write throws `thrown`: the request is let through and the line carries text. */
+async function headerWrite(thrown: unknown, reason: string): Promise<void> {
+  h.toThrow = thrown;
+  const out = await hit(`ks1868-headers-${(n += 1)}`, null, true);
+  expect(out).toEqual({ rejected: false, nextCalls: 1, status: undefined });
+  expect(h.errored).toHaveLength(1);
+  expect(h.errored[0][0]).toBe('[rateLimit] could not write the rate-limit headers or the 429 — request allowed unlimited');
+  expect(reasonOf(h.errored[0])).toBe(reason);
+}
+
+describe('KS-1868 the per-client rate limiter logs text for a hostile thrown value', () => {
+  it('control ks1868 C1 a Redis error that is an ordinary Error is logged with its message and the degraded ceiling applies', async () => {
+    await degraded(new Error('redis down'), 'redis down');
+  });
+
+  it('control ks1868 C2 a Redis rejection that is a plain string is logged as its own text and the degraded ceiling applies', async () => {
+    await degraded('plain boom', 'plain boom');
+  });
+
+  it('control ks1868 C3 a header write that throws an ordinary Error is logged with its message and the request is let through', async () => {
+    await headerWrite(new Error('headers boom'), 'headers boom');
+  });
+
+  it('control ks1868 C4 a header write that throws a plain string is logged as its own text and the request is let through', async () => {
+    await headerWrite('plain boom', 'plain boom');
+  });
+
+  it('RED ks1868 R1 a Redis rejection that is a revoked Proxy logs the constant reason and the degraded ceiling applies', async () => {
+    await degraded(revokedProxy(), CONSTANT);
+  });
+
+  it('RED ks1868 R2 a Redis error whose message is a null-prototype object logs the constant reason and the degraded ceiling applies', async () => {
+    await degraded(withMessage(Object.create(null)), CONSTANT);
+  });
+
+  it('RED ks1868 R3 a Redis error whose message is a Symbol logs the Symbol text and the degraded ceiling applies', async () => {
+    await degraded(withMessage(Symbol('ks1868')), 'Symbol(ks1868)');
+  });
+
+  it('RED ks1868 R4 a header write that throws a revoked Proxy logs the constant reason and the request is let through', async () => {
+    await headerWrite(revokedProxy(), CONSTANT);
+  });
+
+  it('RED ks1868 R5 a header write that throws an Error whose message is a null-prototype object logs the constant reason and the request is let through', async () => {
+    await headerWrite(withMessage(Object.create(null)), CONSTANT);
+  });
+
+  it('RED ks1868 R6 a header write that throws an Error whose message is a Symbol logs the Symbol text and the request is let through', async () => {
+    await headerWrite(withMessage(Symbol('ks1868')), 'Symbol(ks1868)');
+  });
+});
```
