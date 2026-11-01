# READY — KS-1868-KS-1868-O69-P3 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o69_p3_originate_certifications_recertify_route_catch_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 10:16 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o69_p3_originate_certifications_recertify_route_catch_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o69_p3_originate_certifications_recertify_route_catch_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o69_p3_originate_certifications_recertify_route_catch_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o69_p3_originate_certifications_recertify_route_catch_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 10:16 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o69_p3_originate_certifications_recertify_route_catch_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `b887480394cc67764922b0aa123027c344241ed7`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/certifications.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-route-catch-p3-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-route-catch-p3-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/originate/src/routes/certifications.ts
127	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-route-catch-p3-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: certifications.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/certifications.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-route-catch-p3-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/certifications.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-route-catch-p3-unreadable-throw.test.ts 127 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/certifications.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-route-catch-p3-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 POST /:id/recertify catch reads the thrown value safely RED ks1868 R1 POST /:id/recertify: a revoked Proxy from getCertification is logged as a constant reason and answered with the constant 500', 'KS-1868 POST /:id/recertify catch reads the thrown value safely RED ks1868 R2 POST /:id/recertify: an Error whose message getter throws is logged as a constant reason and answered with the constant 500']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1999 failed=0 | after: total=2003 failed=0` · `NEW reds: []` [baseline_suite.json total=1999 failed=0; after_suite.json total=2003 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-route-catch-p3-unreadable-throw.test.ts` (+127/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/certifications.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `b887480394cc67764922b0aa123027c344241ed7` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o69_p3_originate_certifications_recertify_route_catch_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o69_p3_originate_certifications_recertify_route_catch_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o69_p3_originate_certifications_recertify_route_catch_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/certifications.ts b/Blockchain/Dev/services/originate/src/routes/certifications.ts
--- a/Blockchain/Dev/services/originate/src/routes/certifications.ts
+++ b/Blockchain/Dev/services/originate/src/routes/certifications.ts
@@ -1492,7 +1492,13 @@
         chargeEventId: recertCharge.id,
       });
     } catch (error) {
-      logger.error('Failed to issue verification certificate', { error: error instanceof Error ? error.message : String(error) });
+      let reason: string;
+      try {
+        reason = error instanceof Error ? error.message : String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('Failed to issue verification certificate', { error: reason });
       res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to issue verification certificate' } });
     }
   }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-route-catch-p3-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-route-catch-p3-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-route-catch-p3-unreadable-throw.test.ts
@@ -0,0 +1,127 @@
+// KS-1868 (originate routes/certifications.ts, POST /api/certifications/:id/recertify): each route catch logged
+// `error instanceof Error ? error.message : String(error)` itself and then answered a constant 500. When the thrown value cannot be read (a revoked Proxy makes
+// `instanceof` throw; an Error whose `message` getter throws), that read threw INSIDE the catch: the handler's promise rejected and the request got NO answer. Each catch
+// now reads the value inside its own try and logs the constant reason `unreadable thrown value`. getCertification rejects with the thrown value on a real loopback
+// listener, before the route has written or anchored anything; a request that gets no answer within the window is reported as the string NO ANSWER, so a hang is a red assertion and not a stuck run.
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
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (req: any, _res: unknown, next: () => void) => { req.user = { userId: '11111111-2222-4333-8444-555555555555', email: 'ks1868@example.test' }; next(); },
+}));
+jest.mock('../utils/logger', () => ({ logger: mockLog }));
+
+import express from 'express';
+import { certificationsRouter } from '../routes/certifications';
+
+const TENANT = 'a0000000-0000-4000-8000-0000000000aa';
+const CERT_ID = 'aaaaaaaa-1111-4111-8111-111111111111';
+const UNREADABLE = 'unreadable thrown value';
+
+const ROUTES = [
+  { route: 'POST /:id/recertify', path: `/${CERT_ID}/recertify`, context: 'Failed to issue verification certificate', constant: { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to issue verification certificate' } }, payload: { note: 'ks1868' } },
+];
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
+});
+
+async function callWithThrow(c: (typeof ROUTES)[number], thrown: unknown): Promise<{ status: number | string; body?: unknown }> {
+  mockGetCertification.mockRejectedValueOnce(thrown);
+  try {
+    const res = await fetch(`${baseUrl}/api/certifications${c.path}`, {
+      method: 'POST',
+      headers: { 'content-type': 'application/json' },
+      body: JSON.stringify(c.payload),
+      signal: AbortSignal.timeout(1500),
+    });
+    return { status: res.status, body: await res.json() };
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
+const throwingMessageError = (): Error =>
+  Object.defineProperty(new Error('ks1868 hidden'), 'message', {
+    get(): string {
+      throw new Error('ks1868 message getter threw');
+    },
+  });
+
+describe.each(ROUTES)('KS-1868 $route catch reads the thrown value safely', (c) => {
+  it(`RED ks1868 R1 ${c.route}: a revoked Proxy from getCertification is logged as a constant reason and answered with the constant 500`, async () => {
+    expect(await callWithThrow(c, revokedProxy())).toEqual({ status: 500, body: c.constant });
+    expect(mockLog.error.mock.calls).toEqual([[c.context, { error: UNREADABLE }]]);
+  });
+
+  it(`RED ks1868 R2 ${c.route}: an Error whose message getter throws is logged as a constant reason and answered with the constant 500`, async () => {
+    expect(await callWithThrow(c, throwingMessageError())).toEqual({ status: 500, body: c.constant });
+    expect(mockLog.error.mock.calls).toEqual([[c.context, { error: UNREADABLE }]]);
+  });
+
+  it(`control ks1868 C1 ${c.route}: an ordinary Error logs its own message and the answer is the constant 500`, async () => {
+    expect(await callWithThrow(c, new Error('ks1868 ordinary'))).toEqual({ status: 500, body: c.constant });
+    expect(mockLog.error.mock.calls).toEqual([[c.context, { error: 'ks1868 ordinary' }]]);
+  });
+
+  it(`control ks1868 C2 ${c.route}: a thrown string is logged as itself, as before`, async () => {
+    expect(await callWithThrow(c, 'ks1868 plain string')).toEqual({ status: 500, body: c.constant });
+    expect(mockLog.error.mock.calls).toEqual([[c.context, { error: 'ks1868 plain string' }]]);
+  });
+});
```
