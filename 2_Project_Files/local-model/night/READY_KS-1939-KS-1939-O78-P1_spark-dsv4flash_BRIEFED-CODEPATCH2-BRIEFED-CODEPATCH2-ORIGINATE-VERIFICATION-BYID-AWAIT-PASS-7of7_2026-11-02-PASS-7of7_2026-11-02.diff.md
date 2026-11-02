# READY — KS-1939-KS-1939-O78-P1 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1939_o78_p1_originate_verification_by_id_existence_answer_is_awaited/out.md.checker/patch.diff`** (from `ls` at 16:03 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1939_o78_p1_originate_verification_by_id_existence_answer_is_awaited/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1939_o78_p1_originate_verification_by_id_existence_answer_is_awaited/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1939_o78_p1_originate_verification_by_id_existence_answer_is_awaited/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1939_o78_p1_originate_verification_by_id_existence_answer_is_awaited-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 16:03 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1939_o78_p1_originate_verification_by_id_existence_answer_is_awaited/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `cd9c4a7dd3b87f4810d16b40352a63330d1d6793`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/verification.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1939-verification-by-id-existence-answer-throw-is-answered.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/verification.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1939-verification-by-id-existence-answer-throw-is-answered.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/originate/src/routes/verification.ts
195	0	Blockchain/Dev/services/originate/src/__tests__/ks1939-verification-by-id-existence-answer-throw-is-answered.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (1 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: verification.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/verification.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1939-verification-by-id-existence-answer-throw-is-answered.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/verification.ts 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1939-verification-by-id-existence-answer-throw-is-answered.test.ts 195 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/verification.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1939-verification-by-id-existence-answer-throw-is-answered.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1939 POST /verify by documentId: a throw while building the existence answer is answered by the lookup catch RED ks1939 R1: an ordinary Error thrown by the first res.json of the by-id answer is answered 200 lookup failed and logged', 'KS-1939 POST /verify by documentId: a throw while building the existence answer is answered by the lookup catch RED ks1939 R2: a thrown string from the by-id answer is answered 200 lookup failed', 'KS-1939 POST /verify by documentId: a throw while building the existence answer is answered by the lookup catch RED ks1939 R3: an ordinary Error thrown while reading the found row is answered 200 lookup failed']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2108 failed=0 | after: total=2113 failed=0` · `NEW reds: []` [baseline_suite.json total=2108 failed=0; after_suite.json total=2113 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/verification.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1939-verification-by-id-existence-answer-throw-is-answered.test.ts` (+195/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/verification.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `cd9c4a7dd3b87f4810d16b40352a63330d1d6793` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1939_o78_p1_originate_verification_by_id_existence_answer_is_awaited/input.json`. Brief (given by --brief; its `# ` heading names KS-1939): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1939_o78_p1_originate_verification_by_id_existence_answer_is_awaited/KS-1939.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1939_o78_p1_originate_verification_by_id_existence_answer_is_awaited/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/verification.ts b/Blockchain/Dev/services/originate/src/routes/verification.ts
--- a/Blockchain/Dev/services/originate/src/routes/verification.ts
+++ b/Blockchain/Dev/services/originate/src/routes/verification.ts
@@ -1354,5 +1354,5 @@
           if (rows.length > 0) {
-            return respondExistenceOnly(
+            return await respondExistenceOnly(
               rows[0],
               'Document found by ID but no hash was provided. To verify integrity, provide the document file or its SHA-256 hash.',
             );
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1939-verification-by-id-existence-answer-throw-is-answered.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1939-verification-by-id-existence-answer-throw-is-answered.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1939-verification-by-id-existence-answer-throw-is-answered.test.ts
@@ -0,0 +1,195 @@
+// KS-1939 (originate routes/verification.ts, POST /api/verification/verify, strategy 2 by documentId): the handler answered a found document with
+// `return respondExistenceOnly(...)` INSIDE its lookup try, without `await`. respondExistenceOnly is async, so a throw inside it (a
+// field read, the response write) became a rejected promise that left the try and its catch, and the request got NO answer. With `return await` the
+// catch of the lookup block answers it, exactly as it answers an ordinary Error from the lookup query itself: HTTP 200 { verified: false, error: 'Verification lookup failed' }.
+// These cells use ORDINARY errors only (an unreadable thrown value in that catch is a separate pass). A real loopback listener; a request that gets no answer within the window
+// is reported as the string NO ANSWER, so a hang is a red assertion and not a stuck run.
+process.env.NODE_ENV = 'development';
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
+
+const mockLoggerError = jest.fn();
+const mockLoggerWarn = jest.fn();
+const mockExecuteRaw = jest.fn();
+let mockQueryRaw: () => Promise<unknown[]> = async () => [];
+
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: (..._args: unknown[]) => mockQueryRaw(), $executeRaw: (...args: unknown[]) => mockExecuteRaw(...args) },
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
+  logger: { info: jest.fn(), warn: mockLoggerWarn, error: mockLoggerError, debug: jest.fn() },
+}));
+
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { verificationRouter } from '../routes/verification';
+
+const DOC = 'ks1939-doc';
+const HASH = 'f'.repeat(64);
+const LOOKUP_FAILED = { verified: false, error: 'Verification lookup failed' };
+
+function docRow(): Record<string, unknown> {
+  return {
+    id: '11111111-1111-4111-8111-111111111111',
+    external_id: DOC,
+    title: 'ks1939 title',
+    document_type: 'certificate',
+    content_hash: HASH,
+    status: 'certified',
+    certification_metadata: {},
+    metadata: {},
+    created_at: new Date(0),
+    certified_at: new Date(0),
+    organization_name: 'ks1939 org',
+  };
+}
+
+// The first query of the by-id strategy answers `first`; every later query answers no rows.
+function answerFirstQueryWith(first: unknown[]): void {
+  let n = 0;
+  mockQueryRaw = async () => (n++ === 0 ? first : []);
+}
+
+// The first query of the by-id strategy rejects with `thrown` (a plain function, not jest.fn(): a spy may inspect a revoked Proxy before the code under test sees it).
+function rejectFirstQueryWith(thrown: unknown): void {
+  mockQueryRaw = async () => {
+    throw thrown;
+  };
+}
+
+let armedJsonThrow: { thrown: unknown } | null = null;
+
+const app = express();
+app.use(express.json());
+app.use((_req: express.Request, res: express.Response, next: express.NextFunction) => {
+  const hook = armedJsonThrow;
+  armedJsonThrow = null;
+  if (hook) {
+    const realJson = res.json.bind(res);
+    let first = true;
+    res.json = ((body: unknown) => {
+      if (first) {
+        first = false;
+        throw hook.thrown;
+      }
+      return realJson(body);
+    }) as typeof res.json;
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
+beforeEach(() => {
+  jest.clearAllMocks();
+  mockQueryRaw = async () => [];
+  armedJsonThrow = null;
+});
+
+// POST /api/verification/verify with a body carrying ONLY a documentId (strategy 2, by id). No answer within the window is reported as the string NO ANSWER.
+async function verifyById(): Promise<{ status: number | 'NO ANSWER'; body: any }> {
+  try {
+    const res = await fetch(baseUrl + '/api/verification/verify', {
+      method: 'POST',
+      headers: { 'content-type': 'application/json' },
+      body: JSON.stringify({ documentId: DOC }),
+      signal: AbortSignal.timeout(1500),
+    });
+    return { status: res.status, body: await res.json() };
+  } catch {
+    return { status: 'NO ANSWER', body: null };
+  }
+}
+
+describe('KS-1939 POST /verify by documentId: a throw while building the existence answer is answered by the lookup catch', () => {
+  it('RED ks1939 R1: an ordinary Error thrown by the first res.json of the by-id answer is answered 200 lookup failed and logged', async () => {
+    answerFirstQueryWith([docRow()]);
+    armedJsonThrow = { thrown: new Error('ks1939 ordinary') };
+    const reply = await verifyById();
+    expect(reply).toEqual({ status: 200, body: LOOKUP_FAILED });
+    expect(mockLoggerWarn.mock.calls).toEqual([['Verification lookup failed', { documentId: DOC, error: 'ks1939 ordinary' }]]);
+    expect(mockLoggerError).not.toHaveBeenCalled();
+    expect(mockExecuteRaw).not.toHaveBeenCalled();
+  });
+
+  it('RED ks1939 R2: a thrown string from the by-id answer is answered 200 lookup failed', async () => {
+    answerFirstQueryWith([docRow()]);
+    armedJsonThrow = { thrown: 'ks1939 plain string' };
+    const reply = await verifyById();
+    expect(reply).toEqual({ status: 200, body: LOOKUP_FAILED });
+    expect(mockLoggerWarn.mock.calls).toEqual([['Verification lookup failed', { documentId: DOC, error: undefined }]]);
+    expect(mockLoggerError).not.toHaveBeenCalled();
+    expect(mockExecuteRaw).not.toHaveBeenCalled();
+  });
+
+  it('RED ks1939 R3: an ordinary Error thrown while reading the found row is answered 200 lookup failed', async () => {
+    const bad = docRow();
+    Object.defineProperty(bad, 'status', {
+      get() {
+        throw new Error('ks1939 status getter');
+      },
+    });
+    answerFirstQueryWith([bad]);
+    const reply = await verifyById();
+    expect(reply).toEqual({ status: 200, body: LOOKUP_FAILED });
+    expect(mockLoggerWarn.mock.calls).toEqual([['Verification lookup failed', { documentId: DOC, error: 'ks1939 status getter' }]]);
+    expect(mockLoggerError).not.toHaveBeenCalled();
+    expect(mockExecuteRaw).not.toHaveBeenCalled();
+  });
+
+  it('control ks1939 C1: an ordinary Error from the lookup query itself is answered 200 lookup failed, as before', async () => {
+    rejectFirstQueryWith(new Error('ks1939 query'));
+    const reply = await verifyById();
+    expect(reply).toEqual({ status: 200, body: LOOKUP_FAILED });
+    expect(mockLoggerWarn.mock.calls).toEqual([['Verification lookup failed', { documentId: DOC, error: 'ks1939 query' }]]);
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+
+  it('control ks1939 C2: a found document still gets the existence-only answer, never a verdict', async () => {
+    answerFirstQueryWith([docRow()]);
+    const reply = await verifyById();
+    expect(reply.status).toBe(200);
+    expect(reply.body).toEqual(
+      expect.objectContaining({
+        verified: false,
+        documentId: DOC,
+        title: 'ks1939 title',
+        status: 'certified',
+        contentHash: HASH,
+        checks: expect.objectContaining({ documentExists: true, hashValid: false, integrityVerified: false }),
+      }),
+    );
+    expect(reply.body.error).toBeUndefined();
+    expect(String(reply.body.warning)).toContain('Document found by ID');
+    expect(mockLoggerWarn).not.toHaveBeenCalled();
+    expect(mockLoggerError).not.toHaveBeenCalled();
+    expect(mockExecuteRaw).not.toHaveBeenCalled();
+  });
+});
```
