# READY — KS-1868-KS-1868-O78-P3 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o78_p3_originate_verification_v2_chain_fact_catch_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 16:12 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o78_p3_originate_verification_v2_chain_fact_catch_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o78_p3_originate_verification_v2_chain_fact_catch_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o78_p3_originate_verification_v2_chain_fact_catch_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o78_p3_originate_verification_v2_chain_fact_catch_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 16:12 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o78_p3_originate_verification_v2_chain_fact_catch_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `cd9c4a7dd3b87f4810d16b40352a63330d1d6793`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/verificationV2.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-chain-fact-catch-o78p3-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/verificationV2.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-chain-fact-catch-o78p3-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/originate/src/routes/verificationV2.ts
166	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-chain-fact-catch-o78p3-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: verificationV2.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/verificationV2.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-chain-fact-catch-o78p3-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/verificationV2.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-chain-fact-catch-o78p3-unreadable-throw.test.ts 166 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/verificationV2.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-chain-fact-catch-o78p3-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-1868 v2 chain-fact read catch reads the thrown value safely RED ks1868 R1 a revoked Proxy: answered 200 not registered and logged with the constant reason', 'KS-1868 v2 chain-fact read catch reads the thrown value safely RED ks1868 R2 an Error whose message getter throws: answered 200 not registered and logged with the constant reason', 'KS-1868 v2 chain-fact read catch reads the thrown value safely RED ks1868 R3 an Error whose message getter throws a revoked Proxy: answered 200 not registered and logged with the constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2108 failed=0 | after: total=2114 failed=0` · `NEW reds: []` [baseline_suite.json total=2108 failed=0; after_suite.json total=2114 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/verificationV2.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-chain-fact-catch-o78p3-unreadable-throw.test.ts` (+166/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/verificationV2.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `cd9c4a7dd3b87f4810d16b40352a63330d1d6793` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o78_p3_originate_verification_v2_chain_fact_catch_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o78_p3_originate_verification_v2_chain_fact_catch_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o78_p3_originate_verification_v2_chain_fact_catch_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/verificationV2.ts b/Blockchain/Dev/services/originate/src/routes/verificationV2.ts
--- a/Blockchain/Dev/services/originate/src/routes/verificationV2.ts
+++ b/Blockchain/Dev/services/originate/src/routes/verificationV2.ts
@@ -108,7 +108,13 @@
     const chain: any = await resp.json();
     return chain?.verified === true ? chain : null;
   } catch (err: any) {
-    logger.warn('v2 verify: chain-fact read failed; matches present stored state', { error: err?.message });
+    let reason: string | undefined;
+    try {
+      reason = err?.message;
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('v2 verify: chain-fact read failed; matches present stored state', { error: reason });
     return null;
   }
 }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-chain-fact-catch-o78p3-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-chain-fact-catch-o78p3-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-chain-fact-catch-o78p3-unreadable-throw.test.ts
@@ -0,0 +1,166 @@
+// KS-1868 (originate routes/verificationV2.ts, fetchChainFact, the chain-first fallback of POST /api/v2/verification/verify): the catch logged
+// `{ error: err?.message }` and returned null. When the thrown value cannot be read (a revoked Proxy makes `?.message` throw; an Error whose `message` getter throws),
+// that read threw INSIDE the catch: fetchChainFact rejected instead of returning null, the route's catch answered the constant 500, and the caller got a server error where an ordinary Error
+// (a network failure, a timeout) gets the honest 200 { count: 0, matches: [] } with the stored state presented. The catch now reads the message inside its own try and logs the constant
+// `unreadable thrown value`. The anchoring service call is replaced by a plain function that rejects with the chosen value; the database stand-in answers no registered rows, so the
+// route takes the chain-first fallback. A real loopback listener; a request that gets no answer within the window is reported as the string NO ANSWER.
+process.env.NODE_ENV = 'development';
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
+
+const mockLoggerError = jest.fn();
+const mockLoggerWarn = jest.fn();
+const mockExecuteRaw = jest.fn();
+let mockChainFetch: () => Promise<unknown> = async () => new Response(null, { status: 503 });
+
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: async () => [], $executeRaw: (...args: unknown[]) => mockExecuteRaw(...args) },
+  getTenantManager: () => null,
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+}));
+
+jest.mock('@secuura/shared', () =>
+  require('./helpers/sharedModuleMock').makeSharedMock({
+    runWithTenantId: (_t: unknown, fn: () => unknown) => fn(),
+    queryWithTenantGuc: jest.fn(),
+  }),
+);
+
+jest.mock('../repositories/documentRepo', () => ({
+  walkAncestors: jest.fn().mockResolvedValue({ lineage: [], truncated: false }),
+  walkDescendants: jest.fn().mockResolvedValue({ descendants: [], truncated: false }),
+  updateDocument: jest.fn().mockResolvedValue(undefined),
+  MAX_LINEAGE_DEPTH: 10,
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: mockLoggerWarn, error: mockLoggerError, debug: jest.fn() },
+}));
+
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { verificationV2Router } from '../routes/verificationV2';
+
+const UNREADABLE = 'unreadable thrown value';
+const HASH = 'f'.repeat(64);
+const WARN_CONTEXT = 'v2 verify: chain-fact read failed; matches present stored state';
+const NOT_REGISTERED = { hash: 'sha256:' + HASH, count: 0, matches: [] };
+
+const realFetch = globalThis.fetch;
+const app = express();
+app.use(express.json());
+app.use('/api/v2/verification', verificationV2Router);
+let server: ReturnType<typeof app.listen>;
+let baseUrl = '';
+
+beforeAll(async () => {
+  // Only the anchoring service call is replaced; every other request (the test's own, to the loopback listener) goes to the real fetch.
+  (globalThis as any).fetch = (input: any, init?: any) =>
+    String(input).includes('/api/anchors/verify/') ? mockChainFetch() : realFetch(input, init);
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+afterAll(() => {
+  (globalThis as any).fetch = realFetch;
+  server?.close();
+});
+beforeEach(() => {
+  jest.clearAllMocks();
+  mockChainFetch = async () => new Response(null, { status: 503 });
+});
+
+function chainFetchRejectsWith(thrown: unknown): void {
+  mockChainFetch = async () => {
+    throw thrown;
+  };
+}
+
+async function verifyByHash(): Promise<{ status: number | 'NO ANSWER'; body: any }> {
+  try {
+    const res = await realFetch(baseUrl + '/api/v2/verification/verify', {
+      method: 'POST',
+      headers: { 'content-type': 'application/json' },
+      body: JSON.stringify({ hash: HASH }),
+      signal: AbortSignal.timeout(1500),
+    });
+    return { status: res.status, body: await res.json() };
+  } catch {
+    return { status: 'NO ANSWER', body: null };
+  }
+}
+
+function revokedProxy(): object {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+}
+
+function throwingMessageError(): Error {
+  const e = new Error('ks1868 hidden');
+  Object.defineProperty(e, 'message', {
+    get() {
+      throw new Error('ks1868 message getter');
+    },
+  });
+  return e;
+}
+
+function getterThrowsProxyError(): Error {
+  const e = new Error('ks1868 hidden');
+  const p = revokedProxy();
+  Object.defineProperty(e, 'message', {
+    get() {
+      throw p;
+    },
+  });
+  return e;
+}
+
+const UNREADABLE_CASES: Array<{ label: string; make: () => unknown }> = [
+  { label: 'R1 a revoked Proxy', make: revokedProxy },
+  { label: 'R2 an Error whose message getter throws', make: throwingMessageError },
+  { label: 'R3 an Error whose message getter throws a revoked Proxy', make: getterThrowsProxyError },
+];
+
+describe('KS-1868 v2 chain-fact read catch reads the thrown value safely', () => {
+  it.each(UNREADABLE_CASES)('RED ks1868 $label: answered 200 not registered and logged with the constant reason', async (c) => {
+    chainFetchRejectsWith(c.make());
+    const reply = await verifyByHash();
+    expect(reply.status).toBe(200);
+    expect(reply.body).toEqual(expect.objectContaining(NOT_REGISTERED));
+    expect(mockLoggerWarn.mock.calls).toEqual([[WARN_CONTEXT, { error: UNREADABLE }]]);
+    expect(mockLoggerError).not.toHaveBeenCalled();
+    expect(mockExecuteRaw).not.toHaveBeenCalled();
+  });
+
+  it('control ks1868 C1: an ordinary Error logs its own message and is answered 200 not registered', async () => {
+    chainFetchRejectsWith(new Error('ks1868 ordinary'));
+    const reply = await verifyByHash();
+    expect(reply.status).toBe(200);
+    expect(reply.body).toEqual(expect.objectContaining(NOT_REGISTERED));
+    expect(mockLoggerWarn.mock.calls).toEqual([[WARN_CONTEXT, { error: 'ks1868 ordinary' }]]);
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+
+  it('control ks1868 C2: a thrown string is logged as before (no message) and answered 200 not registered', async () => {
+    chainFetchRejectsWith('ks1868 plain string');
+    const reply = await verifyByHash();
+    expect(reply.status).toBe(200);
+    expect(reply.body).toEqual(expect.objectContaining(NOT_REGISTERED));
+    expect(mockLoggerWarn.mock.calls).toEqual([[WARN_CONTEXT, { error: undefined }]]);
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+
+  it('control ks1868 C3: a non-2xx answer from the anchoring service is answered 200 not registered with its own warn line', async () => {
+    const reply = await verifyByHash();
+    expect(reply.status).toBe(200);
+    expect(reply.body).toEqual(expect.objectContaining(NOT_REGISTERED));
+    expect(mockLoggerWarn.mock.calls).toEqual([['v2 verify: chain-fact read returned non-2xx; matches present stored state', { status: 503 }]]);
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+});
```
