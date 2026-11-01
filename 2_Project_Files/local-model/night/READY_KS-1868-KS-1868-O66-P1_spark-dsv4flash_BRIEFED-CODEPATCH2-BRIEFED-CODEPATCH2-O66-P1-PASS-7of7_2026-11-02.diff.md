# READY — KS-1868-KS-1868-O66-P1 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o66_p1_originate_verification_v2_verify_verify_file_catches_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 09:06 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o66_p1_originate_verification_v2_verify_verify_file_catches_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o66_p1_originate_verification_v2_verify_verify_file_catches_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o66_p1_originate_verification_v2_verify_verify_file_catches_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o66_p1_originate_verification_v2_verify_verify_file_catches_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 09:06 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o66_p1_originate_verification_v2_verify_verify_file_catches_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `03977e89a343ad7362760e4fb0270602fb6da5ce`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/verificationV2.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-route-catches-p1-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/verificationV2.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-route-catches-p1-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
14	2	Blockchain/Dev/services/originate/src/routes/verificationV2.ts
124	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-route-catches-p1-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (14 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: verificationV2.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/verificationV2.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-route-catches-p1-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/verificationV2.ts 14 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-route-catches-p1-unreadable-throw.test.ts 124 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/verificationV2.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-route-catches-p1-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=4 of total=8; red cell(s): ['KS-1868 POST /verify catch reads the thrown value safely RED ks1868 R1 POST /verify: a revoked Proxy thrown by the database is logged as a constant reason and answered with the constant 500', 'KS-1868 POST /verify catch reads the thrown value safely RED ks1868 R2 POST /verify: an Error whose message getter throws is logged as a constant reason and answered with the constant 500', 'KS-1868 POST /verify-file catch reads the thrown value safely RED ks1868 R1 POST /verify-file: a revoked Proxy thrown by the database is logged as a constant reason and answered with the constant 500', 'KS-1868 POST /verify-file catch reads the thrown value safely RED ks1868 R2 POST /verify-file: an Error whose message getter throws is logged as a constant reason and answered with the constant 500']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1999 failed=0 | after: total=2007 failed=0` · `NEW reds: []` [baseline_suite.json total=1999 failed=0; after_suite.json total=2007 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/verificationV2.ts` (+14/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-route-catches-p1-unreadable-throw.test.ts` (+124/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/verificationV2.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `03977e89a343ad7362760e4fb0270602fb6da5ce` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o66_p1_originate_verification_v2_verify_verify_file_catches_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o66_p1_originate_verification_v2_verify_verify_file_catches_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o66_p1_originate_verification_v2_verify_verify_file_catches_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/verificationV2.ts b/Blockchain/Dev/services/originate/src/routes/verificationV2.ts
--- a/Blockchain/Dev/services/originate/src/routes/verificationV2.ts
+++ b/Blockchain/Dev/services/originate/src/routes/verificationV2.ts
@@ -438,7 +438,13 @@
       const matches = rows.map((row) => buildMatch(req, row, false, chainBlobOfRow(row), trusted));
       return res.json({ hash: null, count: matches.length, matches, verifiedAt: new Date().toISOString() });
     } catch (error) {
-      logger.error('v2 verification error', { error: error instanceof Error ? error.message : String(error) });
+      let reason: string;
+      try {
+        reason = error instanceof Error ? error.message : String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('v2 verification error', { error: reason });
       return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Verification failed' } });
     }
   },
@@ -474,7 +480,13 @@
       verifiedAt: new Date().toISOString(),
     });
   } catch (error) {
-    logger.error('v2 file verification error', { error: error instanceof Error ? error.message : String(error) });
+    let reason: string;
+    try {
+      reason = error instanceof Error ? error.message : String(error);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('v2 file verification error', { error: reason });
     return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'File verification failed' } });
   }
 });
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-route-catches-p1-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-route-catches-p1-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-verification-v2-route-catches-p1-unreadable-throw.test.ts
@@ -0,0 +1,124 @@
+// KS-1868 (originate routes/verificationV2.ts, POST /api/v2/verification/verify and POST /api/v2/verification/verify-file): both route catch blocks logged
+// `error instanceof Error ? error.message : String(error)` themselves and then answered the constant 500. When the thrown value cannot be read (a revoked Proxy makes
+// `instanceof` throw; an Error whose `message` getter throws), that read threw INSIDE the catch: the handler's promise rejected and the request got NO answer. Both catches
+// now read the value inside their own try and log the constant reason `unreadable thrown value`. The database stand-in rejects with the thrown value on a real loopback
+// listener; a request that gets no answer within the window is reported as the string NO ANSWER, so a hang is a red assertion and not a stuck run.
+process.env.NODE_ENV = 'development';
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
+
+const mockQueryRaw = jest.fn();
+const mockLoggerError = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: mockQueryRaw },
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
+  logger: { info: jest.fn(), warn: jest.fn(), error: mockLoggerError, debug: jest.fn() },
+}));
+
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { verificationV2Router } from '../routes/verificationV2';
+
+const CONSTANT_BODY_VERIFY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Verification failed' } };
+const CONSTANT_BODY_FILE = { success: false, error: { code: 'INTERNAL_ERROR', message: 'File verification failed' } };
+const UNREADABLE = 'unreadable thrown value';
+const HASH = 'f'.repeat(64);
+
+const ROUTES = [
+  { route: 'POST /verify', path: '/verify', context: 'v2 verification error', constant: CONSTANT_BODY_VERIFY, file: false },
+  { route: 'POST /verify-file', path: '/verify-file', context: 'v2 file verification error', constant: CONSTANT_BODY_FILE, file: true },
+];
+
+const app = express();
+app.use(express.json());
+app.use('/api/v2/verification', verificationV2Router);
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
+  mockQueryRaw.mockRejectedValueOnce(thrown);
+  try {
+    const res = await fetch(baseUrl + '/api/v2/verification' + c.path, {
+      method: 'POST',
+      headers: { 'content-type': c.file ? 'application/octet-stream' : 'application/json' },
+      body: c.file ? Buffer.from('ks1868 file bytes') : JSON.stringify({ hash: HASH }),
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
+describe.each(ROUTES)('KS-1868 $route catch reads the thrown value safely', (c) => {
+  it(`RED ks1868 R1 ${c.route}: a revoked Proxy thrown by the database is logged as a constant reason and answered with the constant 500`, async () => {
+    const reply = await callWithThrow(c, revokedProxy());
+    expect(reply).toEqual({ status: 500, body: c.constant });
+    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: UNREADABLE }]]);
+  });
+
+  it(`RED ks1868 R2 ${c.route}: an Error whose message getter throws is logged as a constant reason and answered with the constant 500`, async () => {
+    const reply = await callWithThrow(c, throwingMessageError());
+    expect(reply).toEqual({ status: 500, body: c.constant });
+    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: UNREADABLE }]]);
+  });
+
+  it(`control ks1868 C1 ${c.route}: an ordinary Error logs its own message and the answer is the constant 500 without it`, async () => {
+    const reply = await callWithThrow(c, new Error('ks1868 ordinary'));
+    expect(reply).toEqual({ status: 500, body: c.constant });
+    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: 'ks1868 ordinary' }]]);
+  });
+
+  it(`control ks1868 C2 ${c.route}: a thrown string is logged as itself, as before`, async () => {
+    const reply = await callWithThrow(c, 'ks1868 plain string');
+    expect(reply).toEqual({ status: 500, body: c.constant });
+    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: 'ks1868 plain string' }]]);
+  });
+});
```
