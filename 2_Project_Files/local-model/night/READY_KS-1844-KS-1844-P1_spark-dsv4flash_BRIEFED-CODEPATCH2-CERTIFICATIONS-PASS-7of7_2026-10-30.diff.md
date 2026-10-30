# READY — KS-1844-KS-1844-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1844_p1_get_cert_hostile_throw/out.md.checker/patch.diff`** (from `ls` at 11:57 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1844_p1_get_cert_hostile_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1844_p1_get_cert_hostile_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1844_p1_get_cert_hostile_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1844_p1_get_cert_hostile_throw-control-r3/out.md.checker/patch.diff` rc 0, Wednesday coordinator: Spark operator 19).

**Held 11:57 2026-10-30 by Wednesday coordinator: Spark operator 19 after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1844_p1_get_cert_hostile_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `530f091120d5da749edf972e8e0089e44cfc5589`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/certifications.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1844-get-certification-by-id-answers-a-hostile-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1844-get-certification-by-id-answers-a-hostile-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
17	3	Blockchain/Dev/services/originate/src/routes/certifications.ts
136	0	Blockchain/Dev/services/originate/src/__tests__/ks1844-get-certification-by-id-answers-a-hostile-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (17 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: certifications.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/certifications.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1844-get-certification-by-id-answers-a-hostile-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/certifications.ts 17 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1844-get-certification-by-id-answers-a-hostile-throw.test.ts 136 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/certifications.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1844-get-certification-by-id-answers-a-hostile-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=3 of total=7; red cell(s): ['KS-1844 GET /api/certifications/:id survives a thrown value it cannot read RED KS-1844 D1 a revoked Proxy from getCertification is answered with the constant 500', 'KS-1844 GET /api/certifications/:id survives a thrown value it cannot read RED KS-1844 D2 an Error whose code getter throws is answered with the constant 500', 'KS-1844 GET /api/certifications/:id survives a thrown value it cannot read RED KS-1844 D3 an Error whose message getter throws is answered with the constant 500']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1854 failed=0 | after: total=1861 failed=0` · `NEW reds: []` [baseline_suite.json total=1854 failed=0; after_suite.json total=1861 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (+17/-3 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1844-get-certification-by-id-answers-a-hostile-throw.test.ts` (+136/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/certifications.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `530f091120d5da749edf972e8e0089e44cfc5589` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1844_p1_get_cert_hostile_throw/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1844_p1_get_cert_hostile_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/certifications.ts b/Blockchain/Dev/services/originate/src/routes/certifications.ts
--- a/Blockchain/Dev/services/originate/src/routes/certifications.ts
+++ b/Blockchain/Dev/services/originate/src/routes/certifications.ts
@@ -1070,11 +1070,25 @@
       // KS-255: originate queries run through Prisma, which wraps the pg error
       // (code P2010, pg code only in meta/message) — so also match the wrapped
       // shape, not just the bare `code` the pg driver would set.
-      const pgCode = (error as { code?: string })?.code ?? (error as { meta?: { code?: string } })?.meta?.code;
-      if (pgCode === '22P02' || (error instanceof Error && error.message.includes('22P02'))) {
+      // KS-1844: the reads below touch the thrown value itself (`code`, `meta.code`, `instanceof`, `message`). A revoked Proxy, or an Error whose getter throws, made one of them throw out of this catch,
+      // and on an async Express 4 handler that left the request with no answer. A value that cannot be read is not a 22P02 and falls through to the constant 500 below.
+      let invalidId = false;
+      try {
+        const thrownCode = (error as { code?: string })?.code ?? (error as { meta?: { code?: string } })?.meta?.code;
+        invalidId = thrownCode === '22P02' || (error instanceof Error && error.message.includes('22P02'));
+      } catch {
+        invalidId = false;
+      }
+      if (invalidId) {
         return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Certification not found' } });
       }
-      logger.error('Failed to get certification', { error: error instanceof Error ? error.message : String(error) });
+      let reason: string;
+      try {
+        reason = error instanceof Error ? error.message : String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('Failed to get certification', { error: reason });
       res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get certification' } });
     }
   }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1844-get-certification-by-id-answers-a-hostile-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1844-get-certification-by-id-answers-a-hostile-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1844-get-certification-by-id-answers-a-hostile-throw.test.ts
@@ -0,0 +1,136 @@
+/**
+ * KS-1844 - GET /api/certifications/:id: the catch must survive a thrown value it cannot read.
+ *
+ * The handler's catch read `code`, `meta.code`, `error instanceof Error` and `error.message` straight off the thrown value with no
+ * try of its own. A revoked Proxy (every property read and `instanceof` throw), or an Error whose `code` or `message` getter throws,
+ * therefore threw inside the catch of an async Express 4 handler, and the request got NO answer. A request with no answer in 1500 ms
+ * is reported here as the string NO ANSWER, so a hang is a red assertion and not a stuck run. The controls pin what must not change:
+ * the three readable 22P02 shapes still answer 404, and an ordinary Error still answers the constant 500 and is logged by message.
+ */
+const mockGetCertification = jest.fn();
+const mockSaveCertification = jest.fn(async (..._a: unknown[]) => undefined);
+const mockGetShares = jest.fn(async (..._a: unknown[]) => [] as unknown[]);
+const mockGetLineageEvents = jest.fn(async (..._a: unknown[]) => [] as unknown[]);
+const mockCreateChargeEvent = jest.fn(async (..._a: unknown[]) => ({ id: 'charge-new', eventType: 'evidence_export' }));
+const mockGetChargeEvents = jest.fn(async (..._a: unknown[]) => [] as unknown[]);
+const mockLog = { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() };
+
+jest.mock('../repositories/certificationRepo', () => ({
+  initRepo: jest.fn(async () => undefined),
+  getCertification: (...a: unknown[]) => mockGetCertification(...a),
+  saveCertification: (...a: unknown[]) => mockSaveCertification(...a),
+  listCertifications: jest.fn(),
+  saveShare: jest.fn(),
+  getSharesByCertification: (...a: unknown[]) => mockGetShares(...a),
+  getLineageEvents: (...a: unknown[]) => mockGetLineageEvents(...a),
+  deleteCertification: jest.fn(),
+  reserveCertificationRow: jest.fn(),
+}));
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: jest.fn(async () => []), $executeRaw: jest.fn(async () => 1), $executeRawUnsafe: jest.fn() },
+}));
+jest.mock('../services/chargeEvents', () => ({
+  createChargeEvent: (...a: unknown[]) => mockCreateChargeEvent(...a),
+  getChargeEventsByCertification: (...a: unknown[]) => mockGetChargeEvents(...a),
+}));
+jest.mock('../utils/notificationClient', () => ({
+  notifyDocumentCertified: jest.fn(async () => undefined),
+  notifyDocumentRevoked: jest.fn(async () => undefined),
+  notifyDocumentShared: jest.fn(async () => undefined),
+}));
+jest.mock('../events', () => ({
+  publishEvent: jest.fn(async () => undefined),
+  EventTypes: { CERTIFICATION_ISSUED: 'certification.issued' },
+}));
+jest.mock('../repositories/documentRepo', () => ({
+  getDocument: jest.fn(),
+  saveDocument: jest.fn(async () => undefined),
+  assertNoCycle: jest.fn(async () => undefined),
+  generateContentHash: jest.fn(() => 'hash'),
+}));
+let testUser: Record<string, unknown> | null = null;
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (req: any, _res: unknown, next: () => void) => { req.user = testUser; next(); },
+}));
+jest.mock('../utils/logger', () => ({ logger: mockLog }));
+
+import express from 'express';
+import { certificationsRouter } from '../routes/certifications';
+
+const TENANT = 'a0000000-0000-4000-8000-0000000000aa';
+const CERT_ID = 'aaaaaaaa-1111-4111-8111-111111111111';
+
+const app = express();
+app.use((req: any, _res: unknown, next: () => void) => { req.tenantId = TENANT; next(); });
+app.use('/api/certifications', express.json(), certificationsRouter);
+
+let baseUrl = '';
+let server: ReturnType<typeof app.listen>;
+beforeAll(async () => {
+  await new Promise<void>((resolve) => { server = app.listen(0, '127.0.0.1', () => resolve()); });
+  const address = server.address();
+  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
+});
+afterAll(() => { server?.close(); });
+
+beforeEach(() => {
+  jest.clearAllMocks();
+  testUser = null;
+});
+
+type Answer = { status: number | string; code?: string };
+
+// What GET /api/certifications/:id answers when getCertification rejects with `thrown`: the status and the error code of the envelope, or NO ANSWER after 1500 ms.
+async function answerFor(thrown: unknown): Promise<Answer> {
+  mockGetCertification.mockRejectedValueOnce(thrown);
+  try {
+    const res = await fetch(`${baseUrl}/api/certifications/${CERT_ID}`, { signal: AbortSignal.timeout(1500) });
+    const body = (await res.json()) as { error?: { code?: string } };
+    return { status: res.status, code: body.error?.code };
+  } catch {
+    return { status: 'NO ANSWER' };
+  }
+}
+
+const revokedProxy = (): object => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+const throwingGetter = (name: 'code' | 'message'): object =>
+  Object.defineProperty(new Error('ks1844 getter'), name, {
+    get(): string {
+      throw new Error(`ks1844 ${name} getter threw`);
+    },
+  });
+
+describe('KS-1844 GET /api/certifications/:id survives a thrown value it cannot read', () => {
+  it('RED KS-1844 D1 a revoked Proxy from getCertification is answered with the constant 500', async () => {
+    expect(await answerFor(revokedProxy())).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
+  });
+
+  it('RED KS-1844 D2 an Error whose code getter throws is answered with the constant 500', async () => {
+    expect(await answerFor(throwingGetter('code'))).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
+  });
+
+  it('RED KS-1844 D3 an Error whose message getter throws is answered with the constant 500', async () => {
+    expect(await answerFor(throwingGetter('message'))).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
+  });
+
+  it('CONTROL KS-1844 C1 a bare pg code 22P02 on the thrown value is still answered 404 NOT_FOUND', async () => {
+    expect(await answerFor(Object.assign(new Error('invalid input syntax for type uuid'), { code: '22P02' }))).toEqual({ status: 404, code: 'NOT_FOUND' });
+  });
+
+  it('CONTROL KS-1844 C2 a 22P02 only in meta.code (no own code) is still answered 404 NOT_FOUND', async () => {
+    expect(await answerFor(Object.assign(new Error('Raw query failed'), { meta: { code: '22P02' } }))).toEqual({ status: 404, code: 'NOT_FOUND' });
+  });
+
+  it('CONTROL KS-1844 C3 a 22P02 only inside the message text is still answered 404 NOT_FOUND', async () => {
+    expect(await answerFor(new Error('Raw query failed. Code: `22P02`. Message: invalid input syntax for type uuid'))).toEqual({ status: 404, code: 'NOT_FOUND' });
+  });
+
+  it('CONTROL KS-1844 C4 an ordinary Error is still answered with the constant 500 and logged by its message', async () => {
+    expect(await answerFor(new Error('ks1844 ordinary'))).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
+    expect(mockLog.error).toHaveBeenCalledWith('Failed to get certification', { error: 'ks1844 ordinary' });
+  });
+});
```
