# READY — KS-1868-KS-1868-O79-B2 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_b2_originate_verification_verify_file_guard_coerces_message/out.md.checker/patch.diff`** (from `ls` at 17:46 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_b2_originate_verification_verify_file_guard_coerces_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_b2_originate_verification_verify_file_guard_coerces_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_b2_originate_verification_verify_file_guard_coerces_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_b2_originate_verification_verify_file_guard_coerces_message-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 17:46 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_b2_originate_verification_verify_file_guard_coerces_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `829233f1a388b943a9fd59c40e42332c27d9066b`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/verification.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-verify-file-guard-coerces-message-o79b2.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/verification.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-verify-file-guard-coerces-message-o79b2.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/originate/src/routes/verification.ts
168	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-verify-file-guard-coerces-message-o79b2.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (1 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: verification.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/verification.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-verify-file-guard-coerces-message-o79b2.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/verification.ts 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-verify-file-guard-coerces-message-o79b2.test.ts 168 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/verification.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-verify-file-guard-coerces-message-o79b2.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 POST /verify-file catch reads a hostile message safely RED ks1868 R1 POST /verify-file: an Error whose message getter returns a revoked Proxy gets the constant 500 through the real logger', 'KS-1868 POST /verify-file catch reads a hostile message safely RED ks1868 R2 POST /verify-file: an Error whose message getter returns an object with a throwing toJSON gets the constant 500 through the real logger']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2163 failed=0 | after: total=2167 failed=0` · `NEW reds: []` [baseline_suite.json total=2163 failed=0; after_suite.json total=2167 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/verification.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-verify-file-guard-coerces-message-o79b2.test.ts` (+168/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/verification.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `829233f1a388b943a9fd59c40e42332c27d9066b` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_b2_originate_verification_verify_file_guard_coerces_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o79_b2_originate_verification_verify_file_guard_coerces_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_b2_originate_verification_verify_file_guard_coerces_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/verification.ts b/Blockchain/Dev/services/originate/src/routes/verification.ts
--- a/Blockchain/Dev/services/originate/src/routes/verification.ts
+++ b/Blockchain/Dev/services/originate/src/routes/verification.ts
@@ -758,7 +758,7 @@
   } catch (error) {
     let reason: string;
     try {
-      reason = error instanceof Error ? error.message : String(error);
+      reason = String(error instanceof Error ? error.message : error);
     } catch {
       reason = 'unreadable thrown value';
     }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-verify-file-guard-coerces-message-o79b2.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-verify-file-guard-coerces-message-o79b2.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-verify-file-guard-coerces-message-o79b2.test.ts
@@ -0,0 +1,168 @@
+// KS-1868 (originate routes/verification.ts, POST /api/verification/verify-file, follow-up of the guard PR 1925 merged): the route catch reads the thrown value as `error instanceof Error ? error.message : String(error)`
+// inside its own try and falls back to the constant `unreadable thrown value` when that throws. That expression does not coerce `message`: for an Error whose `message` getter RETURNS a hostile
+// non-string (a revoked Proxy; an object whose toJSON throws) `reason` is that object, and the REAL winston logger throws on it inside logger.error, outside the try, so the request gets NO answer.
+// The guard now wraps the same expression in String(...) (the form PR 1924 merged in routes/certifications.ts). A request-side hook makes the handler throw the chosen value from inside its own try, on a real
+// loopback listener; a request that gets no answer within the window is reported as the string NO ANSWER, so a hang is a red assertion and not a stuck run.
+process.env.NODE_ENV = 'development';
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
+
+const mockLoggerError = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: jest.fn() },
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
+  MAX_LINEAGE_DEPTH: 10,
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: mockLoggerError, debug: jest.fn() },
+}));
+
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { verificationRouter } from '../routes/verification';
+
+const UNREADABLE = 'unreadable thrown value';
+
+// how: 'db' makes the handler's read of `req.db` (after it has read the uploaded bytes) throw.
+const ROUTES = [
+  { route: 'POST /verify-file', method: 'POST', path: '/verify-file', how: 'db', context: 'File verification error', constant: { success: false, error: { code: 'INTERNAL_ERROR', message: 'File verification failed' } } },
+];
+
+let armed: { how: string; thrown: unknown } | null = null;
+
+const app = express();
+app.use(express.json());
+app.use((req: express.Request, _res: express.Response, next: express.NextFunction) => {
+  const hook = armed;
+  armed = null;
+  if (hook && hook.how === 'db') {
+    Object.defineProperty(req, 'db', {
+      get() {
+        throw hook.thrown;
+      },
+    });
+  }
+  next();
+});
+app.use('/api/verification', verificationRouter);
+let server: ReturnType<typeof app.listen>;
+let baseUrl = '';
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+afterAll(() => server?.close());
+beforeEach(() => jest.clearAllMocks());
+
+async function callWithThrow(c: (typeof ROUTES)[number], thrown: unknown): Promise<{ status: number | 'NO ANSWER'; body: unknown }> {
+  armed = { how: c.how, thrown };
+  try {
+    const res = await fetch(baseUrl + '/api/verification' + c.path, {
+      method: c.method,
+      headers: { 'content-type': 'application/octet-stream' },
+      body: Buffer.from('ks1868 file bytes'),
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
+
+// G105-F1 (gate 105, found again by gate 106's reading of the six guards PR 1925 merged): an Error whose `message` getter RETURNS a hostile non-string. The merged guard
+// `reason = error instanceof Error ? error.message : String(error)` returned that object unchanged, so `reason` was the object, and the REAL winston logger (KS-1348 redaction and the dev
+// format) throws on it inside logger.error, outside the guard's try: the request got no answer. The cells below send logger.error through the real logger (its transports' output
+// swallowed, its formats still run), so that the failure is the real one; the ordinary-Error control C2 shows the same harness answers normally. The jest.fn logger of the cells above
+// cannot reproduce the failure, because it never formats its arguments.
+function messageGetterReturningRevokedProxy(): Error {
+  const e = new Error('ks1868 hidden');
+  Object.defineProperty(e, 'message', {
+    get(): unknown {
+      return revokedProxy();
+    },
+  });
+  return e;
+}
+
+function messageGetterReturningThrowingToJson(): Error {
+  const e = new Error('ks1868 hidden');
+  Object.defineProperty(e, 'message', {
+    get(): unknown {
+      return {
+        toJSON(): never {
+          throw new Error('ks1868 toJSON threw');
+        },
+      };
+    },
+  });
+  return e;
+}
+
+function useRealLogger(): void {
+  const real = jest.requireActual('../utils/logger').logger;
+  real.transports.forEach((t: { log?: (info: unknown, next: () => void) => void }) => {
+    t.log = (_info: unknown, next: () => void) => next();
+  });
+  mockLoggerError.mockImplementation((...a: unknown[]) => (real.error as (...x: unknown[]) => unknown)(...a));
+}
+
+afterEach(() => {
+  mockLoggerError.mockReset();
+});
+
+describe.each(ROUTES)('KS-1868 $route catch reads a hostile message safely', (c) => {
+  it(`control ks1868 C1 ${c.route}: an ordinary Error logs its own message and the answer is the constant 500`, async () => {
+    const reply = await callWithThrow(c, new Error('ks1868 ordinary'));
+    expect(reply).toEqual({ status: 500, body: c.constant });
+    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: 'ks1868 ordinary' }]]);
+  });
+
+  it(`control ks1868 C2 ${c.route}: an ordinary Error through the real logger gets the constant 500 and its own message is logged`, async () => {
+    useRealLogger();
+    const reply = await callWithThrow(c, new Error('ks1868 ordinary'));
+    expect(reply).toEqual({ status: 500, body: c.constant });
+    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: 'ks1868 ordinary' }]]);
+  });
+
+  it(`RED ks1868 R1 ${c.route}: an Error whose message getter returns a revoked Proxy gets the constant 500 through the real logger`, async () => {
+    useRealLogger();
+    const reply = await callWithThrow(c, messageGetterReturningRevokedProxy());
+    expect(reply).toEqual({ status: 500, body: c.constant });
+    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: UNREADABLE }]]);
+  });
+
+  it(`RED ks1868 R2 ${c.route}: an Error whose message getter returns an object with a throwing toJSON gets the constant 500 through the real logger`, async () => {
+    useRealLogger();
+    const reply = await callWithThrow(c, messageGetterReturningThrowingToJson());
+    expect(reply).toEqual({ status: 500, body: c.constant });
+    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: '[object Object]' }]]);
+  });
+});
```
