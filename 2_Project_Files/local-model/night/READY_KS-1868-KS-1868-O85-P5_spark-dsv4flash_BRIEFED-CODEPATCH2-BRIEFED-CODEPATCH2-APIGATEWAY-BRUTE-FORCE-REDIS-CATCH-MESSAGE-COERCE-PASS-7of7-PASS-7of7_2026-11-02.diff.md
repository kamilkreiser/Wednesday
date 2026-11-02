# READY — KS-1868-KS-1868-O85-P5 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p5_api_gateway_brute_force_redis_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 23:48 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p5_api_gateway_brute_force_redis_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p5_api_gateway_brute_force_redis_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p5_api_gateway_brute_force_redis_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p5_api_gateway_brute_force_redis_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 23:48 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p5_api_gateway_brute_force_redis_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `1584c0f0ff808fddf35245bee41b6b5f9231054c`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/src/middleware/security.ts } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-brute-force-redis-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/middleware/security.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-brute-force-redis-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/api-gateway/src/middleware/security.ts
160	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-brute-force-redis-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: security.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/api-gateway/src/middleware/security.ts`; test(s): `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-brute-force-redis-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/api-gateway/src/middleware/security.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-brute-force-redis-catch-unreadable-throw.test.ts 160 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/middleware/security.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-brute-force-redis-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=4 of total=8; red cell(s): ['KS-1868 the brute-force Redis-error catch lets the request through and logs text for a hostile thrown value RED ks1868 R1: a Redis rejection that is a revoked Proxy lets the login request through (200) and is logged as text, as for an ordinary Error', 'KS-1868 the brute-force Redis-error catch lets the request through and logs text for a hostile thrown value RED ks1868 R2: a Redis rejection that is an Error whose message getter throws lets the login request through (200) and is logged as text, as for an ordinary Error', 'KS-1868 the brute-force Redis-error catch lets the request through and logs text for a hostile thrown value RED ks1868 R3: a Redis rejection that is an Error whose message is a null-prototype object lets the login request through (200) and is logged as text, as for an ordinary Error', 'KS-1868 the brute-force Redis-error catch lets the request through and logs text for a hostile thrown value RED ks1868 R4: a Redis rejection that is an Error whose message is a Symbol lets the login request through (200) and is logged as text, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1412 failed=0 | after: total=1420 failed=0` · `NEW reds: []` [baseline_suite.json total=1412 failed=0; after_suite.json total=1420 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/middleware/security.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-brute-force-redis-catch-unreadable-throw.test.ts` (+160/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/api-gateway/src/middleware/security.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `1584c0f0ff808fddf35245bee41b6b5f9231054c` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p5_api_gateway_brute_force_redis_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o85_p5_api_gateway_brute_force_redis_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p5_api_gateway_brute_force_redis_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/middleware/security.ts b/Blockchain/Dev/services/api-gateway/src/middleware/security.ts
--- a/Blockchain/Dev/services/api-gateway/src/middleware/security.ts
+++ b/Blockchain/Dev/services/api-gateway/src/middleware/security.ts
@@ -194,8 +194,14 @@
       next();
     } catch (error) {
       // On Redis error, allow the request through (fail open for availability)
+      let reason: string;
+      try {
+        reason = String(error instanceof Error ? error.message : error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
       winstonLogger.error('[BruteForce] Redis error, allowing request', {
-        error: error instanceof Error ? error.message : String(error),
+        error: reason,
       });
       next();
     }
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-brute-force-redis-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-brute-force-redis-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-brute-force-redis-catch-unreadable-throw.test.ts
@@ -0,0 +1,160 @@
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import express from 'express';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+
+// KS-1868 (operator 85 screen, gateway brute force): the Redis-error catch of createBruteForceProtection in
+// services/api-gateway/src/middleware/security.ts logs `{ error: error instanceof Error ? error.message : String(error) }` with
+// the read INSIDE the logger call's arguments, unguarded, in a catch that exists to let the request through (fail open). A thrown
+// value whose read throws (a revoked Proxy: `instanceof` throws; an Error whose message getter throws) makes the catch itself
+// throw, so next() is never called and the async middleware rejects with no handler: the login request HANGS; an Error whose
+// message is readable but not a string is handed to the logger as is. The cells make the Redis read reject with such a value and
+// assert the request is let through (200) and the error line is logged as text (the constant when the value cannot be turned into
+// text). Harness: the real middleware on a real express app on loopback, with the logger and the redis service replaced by plain
+// stand-ins (no Redis).
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  fault: true,
+  reads: 0,
+  logged: [] as unknown[][],
+}));
+
+const capture = vi.hoisted(() => ({
+  debug: () => undefined,
+  info: () => undefined,
+  warn: () => undefined,
+  error: (...args: unknown[]) => {
+    h.logged.push(args);
+  },
+  log: () => undefined,
+}));
+vi.mock('../utils/logger', () => ({ logger: capture, createLogger: () => capture, validateEnv: () => undefined }));
+vi.mock('../services/redis', async (importOriginal) => {
+  const real = (await importOriginal()) as Record<string, unknown>;
+  return {
+    ...real,
+    getBruteForceData: () => {
+      h.reads += 1;
+      return h.fault ? Promise.reject(h.toThrow) : Promise.resolve(null);
+    },
+    setBruteForceData: async () => undefined,
+    deleteBruteForceData: async () => undefined,
+  };
+});
+
+import { createBruteForceProtection } from '../middleware/security';
+
+const CONFIG = { bruteForce: { freeRetries: 2, minWait: 1000, maxWait: 60_000, lifetime: 900_000 }, suspiciousPatterns: [] };
+
+let srv: Server;
+let base = '';
+beforeAll(async () => {
+  const app = express();
+  app.use(createBruteForceProtection(CONFIG as never));
+  app.use((req, res) => {
+    res.status(200).json({ helperAttached: Boolean((req as unknown as { bruteForce?: unknown }).bruteForce) });
+  });
+  srv = app.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => srv.once('listening', () => r()));
+  base = 'http://127.0.0.1:' + (srv.address() as AddressInfo).port;
+});
+afterAll(async () => {
+  srv.closeAllConnections();
+  await new Promise<void>((r) => srv.close(() => r()));
+});
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.fault = true;
+  h.reads = 0;
+  h.logged.length = 0;
+});
+
+/** POST to a path; status 0 when no answer arrives within 1.5 s (the request hangs). */
+async function hit(path: string): Promise<{ status: number; helper: boolean | null }> {
+  try {
+    const r = await fetch(base + path, { method: 'POST', signal: AbortSignal.timeout(1500) });
+    const j = (await r.json().catch(() => ({}))) as { helperAttached?: boolean };
+    return { status: r.status, helper: j.helperAttached ?? null };
+  } catch {
+    return { status: 0, helper: null };
+  }
+}
+const FAILED = '[BruteForce] Redis error, allowing request';
+const LINES = () => h.logged.filter((c) => c[0] === FAILED);
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
+describe('KS-1868 the brute-force Redis-error catch lets the request through and logs text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error lets the login request through (200, no helper) and is logged with its message', async () => {
+    h.toThrow = new Error('redis down');
+    expect(await hit('/api/auth/login')).toEqual({ status: 200, helper: false });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('redis down');
+  });
+  it('control ks1868 C2: a thrown plain string lets the request through (200) and is logged as its own text', async () => {
+    h.toThrow = 'plain boom';
+    expect(await hit('/api/auth/login')).toEqual({ status: 200, helper: false });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('plain boom');
+  });
+  it('control ks1868 C3: with no Redis fault the helper is attached (200) and nothing is logged', async () => {
+    h.fault = false;
+    expect(await hit('/api/auth/login')).toEqual({ status: 200, helper: true });
+    expect(LINES()).toHaveLength(0);
+  });
+  it('control ks1868 C4: a path that is not the login path never reads Redis', async () => {
+    h.toThrow = new Error('redis down');
+    expect(await hit('/api/documents')).toEqual({ status: 200, helper: false });
+    expect(h.reads).toBe(0);
+    expect(LINES()).toHaveLength(0);
+  });
+  it('RED ks1868 R1: a Redis rejection that is a revoked Proxy lets the login request through (200) and is logged as text, as for an ordinary Error', async () => {
+    h.toThrow = SHAPES[0][1]();
+    expect(await hit('/api/auth/login')).toEqual({ status: 200, helper: false });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe(SHAPES[0][2]);
+  });
+  it('RED ks1868 R2: a Redis rejection that is an Error whose message getter throws lets the login request through (200) and is logged as text, as for an ordinary Error', async () => {
+    h.toThrow = SHAPES[1][1]();
+    expect(await hit('/api/auth/login')).toEqual({ status: 200, helper: false });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe(SHAPES[1][2]);
+  });
+  it('RED ks1868 R3: a Redis rejection that is an Error whose message is a null-prototype object lets the login request through (200) and is logged as text, as for an ordinary Error', async () => {
+    h.toThrow = SHAPES[2][1]();
+    expect(await hit('/api/auth/login')).toEqual({ status: 200, helper: false });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe(SHAPES[2][2]);
+  });
+  it('RED ks1868 R4: a Redis rejection that is an Error whose message is a Symbol lets the login request through (200) and is logged as text, as for an ordinary Error', async () => {
+    h.toThrow = SHAPES[3][1]();
+    expect(await hit('/api/auth/login')).toEqual({ status: 200, helper: false });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe(SHAPES[3][2]);
+  });
+});
```
