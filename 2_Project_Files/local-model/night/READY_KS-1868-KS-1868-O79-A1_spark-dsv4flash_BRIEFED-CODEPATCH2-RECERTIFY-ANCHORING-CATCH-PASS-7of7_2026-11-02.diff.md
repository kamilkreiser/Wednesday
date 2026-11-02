# READY — KS-1868-KS-1868-O79-A1 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a1_originate_certifications_recertify_anchoring_catch_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 16:34 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a1_originate_certifications_recertify_anchoring_catch_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a1_originate_certifications_recertify_anchoring_catch_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a1_originate_certifications_recertify_anchoring_catch_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a1_originate_certifications_recertify_anchoring_catch_unreadable_throw-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 16:34 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a1_originate_certifications_recertify_anchoring_catch_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8f313815f415c65849210f5d3e30cae44d15a516`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/certifications.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-anchoring-catch-o79p1-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-anchoring-catch-o79p1-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/originate/src/routes/certifications.ts
173	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-anchoring-catch-o79p1-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: certifications.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/certifications.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-anchoring-catch-o79p1-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/certifications.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-anchoring-catch-o79p1-unreadable-throw.test.ts 173 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/certifications.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-anchoring-catch-o79p1-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (5 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=5 of total=7; red cell(s): ['KS-1868 G105-F2 POST /:id/recertify: the anchoring inner catch reads the thrown value safely RED ks1868 R1: a revoked Proxy as the anchoring rejection gets the ordinary outcome (certificate issued and charged) and logs the constant reason', 'KS-1868 G105-F2 POST /:id/recertify: the anchoring inner catch reads the thrown value safely RED ks1868 R2: an Error whose message getter throws gets the ordinary outcome and logs the constant reason', 'KS-1868 G105-F2 POST /:id/recertify: the anchoring inner catch reads the thrown value safely RED ks1868 R3: an Error whose message getter returns a revoked Proxy gets the ordinary outcome through the real logger', 'KS-1868 G105-F2 POST /:id/recertify: the anchoring inner catch reads the thrown value safely RED ks1868 R4: an Error whose message getter returns an object with a throwing toJSON gets the ordinary outcome through the real logger', 'KS-1868 G105-F2 POST /:id/recertify: the anchoring inner catch reads the thrown value safely RED ks1868 R5: a thrown string gets the ordinary outcome and is logged as itself']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2163 failed=0 | after: total=2170 failed=0` · `NEW reds: []` [baseline_suite.json total=2163 failed=0; after_suite.json total=2170 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-anchoring-catch-o79p1-unreadable-throw.test.ts` (+173/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/certifications.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8f313815f415c65849210f5d3e30cae44d15a516` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a1_originate_certifications_recertify_anchoring_catch_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o79_a1_originate_certifications_recertify_anchoring_catch_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a1_originate_certifications_recertify_anchoring_catch_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/certifications.ts b/Blockchain/Dev/services/originate/src/routes/certifications.ts
--- a/Blockchain/Dev/services/originate/src/routes/certifications.ts
+++ b/Blockchain/Dev/services/originate/src/routes/certifications.ts
@@ -1443,7 +1443,13 @@
           logger.warn('KS-1709: the anchoring service refused the recertification anchor', { certId: newCertId, originalCertificationId: id, status: upstream.status, body: errText.slice(0, 200) });
         }
       } catch (err: any) {
-        logger.warn('Anchoring service unreachable for verification cert', { error: err?.message });
+        let reason: string;
+        try {
+          reason = String(err instanceof Error ? err.message : err);
+        } catch {
+          reason = 'unreadable thrown value';
+        }
+        logger.warn('Anchoring service unreachable for verification cert', { error: reason });
       }
       if (anchoringStatus === 'failed' && process.env.NODE_ENV === 'production') {
         return res.status(503).json({
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-anchoring-catch-o79p1-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-anchoring-catch-o79p1-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-recertify-anchoring-catch-o79p1-unreadable-throw.test.ts
@@ -0,0 +1,173 @@
+// KS-1868 (originate routes/certifications.ts, POST /api/certifications/:id/recertify, gate 105 G105-F2): the inner catch around the anchoring-service call logged `{ error: err?.message }`
+// unguarded. An ORDINARY rejection of that call (a network failure) is swallowed: the route continues, saves the verification certificate with anchoringStatus failed, records the charge and
+// answers 201 (outside production). When the thrown value cannot be read (a revoked Proxy; an Error whose `message` getter throws or returns a hostile non-string) the read threw INSIDE the
+// catch, the route's outer catch answered 500, and NO certificate was issued and NO charge was recorded. The catch now reads the value inside its own try and logs the constant reason
+// `unreadable thrown value`, so an unreadable rejection gets exactly the ordinary outcome: the certificate IS issued and the charge IS recorded. The anchoring call is replaced by a plain
+// function on the global fetch (the cell's own client passes through), and the cells that name the real logger run through the real winston logger, whose formats still run.
+const mockGetCertification = jest.fn();
+const mockSaveCertification = jest.fn(async (..._a: unknown[]) => undefined);
+const mockCreateChargeEvent = jest.fn(async (..._a: unknown[]) => ({ id: 'charge-new', eventType: 'verification_certificate' }));
+const mockLog = { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() };
+
+jest.mock('../repositories/certificationRepo', () => ({
+  initRepo: jest.fn(async () => undefined),
+  getCertification: (...a: unknown[]) => mockGetCertification(...a),
+  saveCertification: (...a: unknown[]) => mockSaveCertification(...a),
+  listCertifications: jest.fn(),
+  saveShare: jest.fn(),
+  getSharesByCertification: jest.fn(async () => [] as unknown[]),
+  getLineageEvents: jest.fn(async () => [] as unknown[]),
+  deleteCertification: jest.fn(),
+  reserveCertificationRow: jest.fn(),
+}));
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: jest.fn(async () => []), $executeRaw: jest.fn(async () => 1), $executeRawUnsafe: jest.fn() },
+}));
+jest.mock('../services/chargeEvents', () => ({
+  createChargeEvent: (...a: unknown[]) => mockCreateChargeEvent(...a),
+  getChargeEventsByCertification: jest.fn(async () => [] as unknown[]),
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
+const ISSUER_ID = '11111111-2222-4333-8444-555555555555';
+const UNREADABLE = 'unreadable thrown value';
+const CONTEXT = 'Anchoring service unreachable for verification cert';
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
+beforeEach(() => { jest.clearAllMocks(); });
+afterEach(() => { mockLog.error.mockReset(); mockLog.warn.mockReset(); });
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
+const messageGetterReturningRevokedProxy = (): Error =>
+  Object.defineProperty(new Error('ks1868 hidden'), 'message', {
+    get(): unknown {
+      return revokedProxy();
+    },
+  });
+const messageGetterReturningThrowingToJson = (): Error =>
+  Object.defineProperty(new Error('ks1868 hidden'), 'message', {
+    get(): unknown {
+      return { toJSON(): never { throw new Error('ks1868 toJSON threw'); } };
+    },
+  });
+function useRealLogger(): void {
+  const real = jest.requireActual('../utils/logger').logger;
+  real.transports.forEach((t: { log?: (info: unknown, next: () => void) => void }) => {
+    t.log = (_info: unknown, next: () => void) => next();
+  });
+  mockLog.error.mockImplementation((...a: unknown[]) => (real.error as (...x: unknown[]) => unknown)(...a));
+  mockLog.warn.mockImplementation((...a: unknown[]) => (real.warn as (...x: unknown[]) => unknown)(...a));
+}
+
+// The anchoring call (the only fetch to a URL that does not start with the cell's own listener) is a PLAIN function that rejects with the chosen value.
+async function recertifyWithAnchoringRejecting(thrown: unknown): Promise<{ status: number | string; body?: any; savedTypes: unknown[]; charges: unknown[] }> {
+  const clientFetch = globalThis.fetch;
+  (globalThis as any).fetch = (url: unknown, init?: unknown) =>
+    String(url).startsWith(baseUrl) ? clientFetch(url as string, init as RequestInit) : Promise.reject(thrown);
+  mockGetCertification.mockResolvedValueOnce({ id: CERT_ID, type: 'professional_certification', status: 'certified', issuer: { id: ISSUER_ID }, holder: { id: 'ks1868-holder' }, data: { title: 'ks1868' } });
+  const state = () => ({
+    savedTypes: mockSaveCertification.mock.calls.map((c) => (c[0] as { type?: unknown }).type),
+    charges: mockCreateChargeEvent.mock.calls.map((c) => c[0]),
+  });
+  try {
+    const res = await clientFetch(`${baseUrl}/api/certifications/${CERT_ID}/recertify`, {
+      method: 'POST',
+      headers: { 'content-type': 'application/json' },
+      body: JSON.stringify({ note: 'ks1868' }),
+      signal: AbortSignal.timeout(2500),
+    });
+    return { status: res.status, body: await res.json(), ...state() };
+  } catch {
+    return { status: 'NO ANSWER', ...state() };
+  } finally {
+    (globalThis as any).fetch = clientFetch;
+  }
+}
+const warnLines = (): unknown[][] => mockLog.warn.mock.calls.filter((c) => c[0] === CONTEXT);
+
+// The ordinary outcome, and so the outcome every unreadable value must get: 201, a verification certificate saved with anchoringStatus failed, and the charge recorded.
+async function expectIssued(thrown: unknown, logged: unknown): Promise<void> {
+  const r = await recertifyWithAnchoringRejecting(thrown);
+  expect(r.status).toBe(201);
+  expect(r.body).toMatchObject({ type: 'verification_certificate', status: 'issued', anchoringStatus: 'failed' });
+  expect(r.savedTypes).toEqual(['verification_certificate']);
+  expect(r.charges).toEqual(['verification_certificate']);
+  expect(warnLines()).toEqual([[CONTEXT, { error: logged }]]);
+}
+
+describe('KS-1868 G105-F2 POST /:id/recertify: the anchoring inner catch reads the thrown value safely', () => {
+  it('control ks1868 C1: an ordinary anchoring rejection is swallowed, the certificate is issued and charged, and its own message is logged', async () => {
+    await expectIssued(new Error('ks1868 anchoring down'), 'ks1868 anchoring down');
+  });
+
+  it('control ks1868 C2: an ordinary Error through the real logger gets the same outcome', async () => {
+    useRealLogger();
+    await expectIssued(new Error('ks1868 anchoring down'), 'ks1868 anchoring down');
+  });
+
+  it('RED ks1868 R1: a revoked Proxy as the anchoring rejection gets the ordinary outcome (certificate issued and charged) and logs the constant reason', async () => {
+    await expectIssued(revokedProxy(), UNREADABLE);
+  });
+
+  it('RED ks1868 R2: an Error whose message getter throws gets the ordinary outcome and logs the constant reason', async () => {
+    await expectIssued(throwingMessageError(), UNREADABLE);
+  });
+
+  it('RED ks1868 R3: an Error whose message getter returns a revoked Proxy gets the ordinary outcome through the real logger', async () => {
+    useRealLogger();
+    await expectIssued(messageGetterReturningRevokedProxy(), UNREADABLE);
+  });
+
+  it('RED ks1868 R4: an Error whose message getter returns an object with a throwing toJSON gets the ordinary outcome through the real logger', async () => {
+    useRealLogger();
+    await expectIssued(messageGetterReturningThrowingToJson(), '[object Object]');
+  });
+
+  it('RED ks1868 R5: a thrown string gets the ordinary outcome and is logged as itself', async () => {
+    await expectIssued('ks1868 plain string', 'ks1868 plain string');
+  });
+});
```
