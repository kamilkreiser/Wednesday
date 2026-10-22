# READY — KS-1709-KS-1709-RECERTLOG1709-2 (Spark (DeepSeek V4 Flash), briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-22_ks_1709_p2/out.md.checker/patch.diff`** (from `ls` at 15:36 2026-10-22; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-22_ks_1709_p2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-22_ks_1709_p2/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-22_ks_1709_p2/out.md.checker/section_3.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1709_p2/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 15:36 2026-10-22 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-22_ks_1709_p2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `bcc51903d89329932532058cbd58fd1ced7d3a0c`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/certifications.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts , Blockchain/Dev/services/originate/src/__tests__/ks1709-a-refused-recertification-anchor-is-logged.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts` (test) — equal to numstat.out's set (3 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
5	0	Blockchain/Dev/services/originate/src/routes/certifications.ts
1	0	Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts
176	0	Blockchain/Dev/services/originate/src/__tests__/ks1709-a-refused-recertification-anchor-is-logged.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (5 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: certifications.ts`
- CODE_PATCH2 (rung 3, 1 product files + 2 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/certifications.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts`, `Blockchain/Dev/services/originate/src/__tests__/ks1709-a-refused-recertification-anchor-is-logged.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/certifications.ts 5 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1709-a-refused-recertification-anchor-is-logged.test.ts 176 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=3 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/certifications.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- section 3 `section_3.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1709-a-refused-recertification-anchor-is-logged.test.ts` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 15 run; controls green; assertion reds)` [red_first.json: failed=3 of total=15; red cell(s): ['KS-1709 a non-ok answer from anchoring on POST /api/certifications/:id/recertify is logged RED KS-1709 V1: a 400 with a reason logs one warn naming both certificates, the status and the reason', 'KS-1709 a non-ok answer from anchoring on POST /api/certifications/:id/recertify is logged RED KS-1709 V2: a 503 with an empty body logs the status and an empty body, not nothing', 'KS-1709 a non-ok answer from anchoring on POST /api/certifications/:id/recertify is logged RED KS-1709 V3: a long body is cut to its first 200 characters']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (15 passed / 15 run)` [green_after.json: failed=0 of total=15, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1633 failed=0 | after: total=1638 failed=0` · `NEW reds: []` [baseline_suite.json total=1633 failed=0; after_suite.json total=1638 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=3 products=1 tests=2 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (+5/-0 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts` (+1/-0); 3 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/certifications.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict) — at the tip `bcc51903d89329932532058cbd58fd1ced7d3a0c` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-22_ks_1709_p2/input.json`. Brief (given by --brief; its `# ` heading names KS-1709): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1709_p2/KS-1709.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-22_ks_1709_p2/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/certifications.ts
+++ b/Blockchain/Dev/services/originate/src/routes/certifications.ts
@@ -1384,6 +1384,11 @@
           const j = await upstream.json() as any;
           upstreamAnchorId = j?.data?.id || null;
           anchoringStatus = 'submitted';
+        } else {
+          // KS-1709: the same gap as the issue route: a refusal is an answer, not an exception, so the catch below never sees it.
+          // Without this line a non-ok answer left the verification certificate with no anchor and no log line anywhere.
+          const errText = await upstream.text().catch(() => '');
+          logger.warn('KS-1709: the anchoring service refused the recertification anchor', { certId: newCertId, originalCertificationId: id, status: upstream.status, body: errText.slice(0, 200) });
         }
       } catch (err: any) {
         logger.warn('Anchoring service unreachable for verification cert', { error: err?.message });
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts
@@ -65,6 +65,7 @@
   'ks1508-versionedbyid-is-server-set.test.ts',
   'ks1660-a-caller-s-data-parentdocumentid-overwrites.test.ts',
   'ks1679-the-same-caller-spread-still-overwrites.test.ts',
+  'ks1709-a-refused-recertification-anchor-is-logged.test.ts',
   'ks444-certifications-issue-body-types.test.ts',
   'ks444-documents-create-title-guard.test.ts',
   'ks445-certifications-issue-unstorable-payload.test.ts',
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1709-a-refused-recertification-anchor-is-logged.test.ts
@@ -0,0 +1,176 @@
+/**
+ * KS-1709 (second site) - a non-ok answer from the anchoring service on POST /api/certifications/:id/recertify is logged.
+ *
+ * The recertify route posts the verification certificate's anchor to anchoring's POST /api/anchors and checked only
+ * `if (upstream.ok)`, exactly like the issue route. A refusal (a 4xx or 5xx) is an answer, not an exception, so the `catch`
+ * never saw it, and outside production the verification certificate was saved with no anchor and no log line anywhere.
+ * After this change one warn line names the new certificate id, the original certification id, the status and the first
+ * 200 characters of the body. The response and the saved certificate are NOT changed here.
+ *
+ * Harness: the KS-1385 site-7 suite's (the real certificationsRouter, a real local HTTP server standing in for anchoring),
+ * with the anchoring answer set per cell.
+ */
+
+delete process.env.SIMULATE_ANCHORING;
+process.env.ANCHORING_SERVICE_URL = 'http://127.0.0.1:2';
+
+const CERT_ID = '55555555-5555-4555-8555-555555551709';
+const EXISTING_CERT = {
+  id: CERT_ID,
+  type: 'verification_certificate',
+  issuerId: '11111111-2222-4333-8444-555555551709',
+  issuerName: 'ks1709 issuer',
+  holderId: '66666666-6666-4666-8666-666666661709',
+  status: 'active',
+  contentHash: 'e'.repeat(64),
+  data: { note: 'original' },
+  timestamp: '2026-10-13T00:00:00.000Z',
+  tenantId: 'a0000000-0000-4000-8000-000000000001',
+};
+
+jest.mock('../repositories/certificationRepo', () => ({
+  getCertification: jest.fn(async () => EXISTING_CERT),
+  saveCertification: jest.fn(async () => undefined),
+  listCertifications: jest.fn(async () => []),
+  saveShare: jest.fn(async () => undefined),
+  getSharesByCertification: jest.fn(async () => []),
+  getLineageEvents: jest.fn(async () => []),
+  initRepo: jest.fn(async () => undefined),
+}));
+jest.mock('../repositories/documentRepo', () => ({
+  getDocument: jest.fn(async () => undefined),
+  saveDocument: jest.fn(async () => ({ dbId: '77777777-7777-4777-8777-777777771709', inserted: true })),
+  assertNoCycle: jest.fn(async () => undefined),
+  generateContentHash: jest.fn(() => 'f'.repeat(64)),
+}));
+jest.mock('../services/provenance', () => ({
+  extractOnBehalfOf: jest.fn(() => undefined),
+  resolveOnBehalfOf: jest.fn(async () => undefined),
+  recordActionProvenance: jest.fn(async () => undefined),
+  wasCreatedByConnector: jest.fn(async () => false),
+  OnBehalfOfError: class extends Error {},
+}));
+jest.mock('../services/chargeEvents', () => ({
+  createChargeEvent: jest.fn(async () => ({ id: 'chg-ks1709', feeStatus: 'free' })),
+  getChargeEventsByCertification: jest.fn(async () => []),
+  getUsageSummary: jest.fn(async () => ({})),
+}));
+jest.mock('../utils/notificationClient', () => ({
+  notifyDocumentCertified: jest.fn(async () => undefined),
+  notifyDocumentRevoked: jest.fn(async () => undefined),
+  notifyDocumentShared: jest.fn(async () => undefined),
+}));
+jest.mock('../events', () => ({
+  publishEvent: jest.fn(async () => undefined),
+  EventTypes: { DOCUMENT_CREATED: 'document.created', CERTIFICATION_ISSUED: 'certification.issued' },
+}));
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (req: any, _res: unknown, next: () => void) => {
+    req.user = { userId: '11111111-2222-4333-8444-555555551709', role: 'ISSUER_ADMIN' };
+    next();
+  },
+}));
+jest.mock('../middleware/rbac', () => ({ isAllowedByRoleOrScope: () => true }));
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
+}));
+jest.mock('../db', () => ({
+  prisma: {
+    $queryRaw: jest.fn(async () => [{ id: '66666666-6666-4666-8666-666666661709' }]),
+    $executeRaw: jest.fn(async () => 0),
+  },
+  getTenantManager: jest.fn(() => null),
+}));
+
+import * as http from 'http';
+import express from 'express';
+import { certificationsRouter } from '../routes/certifications';
+
+const UNREACHABLE = 'http://127.0.0.1:2';
+let anchorReply: { status: number; body: string } = { status: 202, body: '{}' };
+let anchoringServer: http.Server;
+let appServer: ReturnType<express.Express['listen']>;
+let baseUrl = '';
+let anchoringUrl = '';
+
+beforeAll(async () => {
+  anchoringServer = http.createServer((req, res) => {
+    req.on('data', () => undefined);
+    req.on('end', () => {
+      res.writeHead(anchorReply.status, { 'content-type': 'application/json' });
+      res.end(anchorReply.body);
+    });
+  });
+  await new Promise<void>((r) => anchoringServer.listen(0, '127.0.0.1', () => r()));
+  const a = anchoringServer.address();
+  anchoringUrl = `http://127.0.0.1:${typeof a === 'object' && a ? a.port : 0}`;
+
+  const app = express();
+  app.use('/api/certifications', express.json(), certificationsRouter);
+  await new Promise<void>((r) => { appServer = app.listen(0, '127.0.0.1', () => r()); });
+  const addr = appServer.address();
+  baseUrl = `http://127.0.0.1:${typeof addr === 'object' && addr ? addr.port : 0}`;
+});
+
+afterAll(async () => {
+  for (const srv of [appServer, anchoringServer]) {
+    if (!srv) continue;
+    (srv as any).closeAllConnections?.();
+    await new Promise<void>((r) => srv.close(() => r()));
+  }
+});
+
+const { logger } = jest.requireMock('../utils/logger') as { logger: { info: jest.Mock; warn: jest.Mock; error: jest.Mock } };
+const refused = () => logger.warn.mock.calls.filter((c) => /KS-1709/.test(String(c[0])));
+const unreachable = () => logger.warn.mock.calls.filter((c) => String(c[0]) === 'Anchoring service unreachable for verification cert');
+
+beforeEach(() => {
+  logger.info.mockClear(); logger.warn.mockClear(); logger.error.mockClear();
+  process.env.ANCHORING_SERVICE_URL = anchoringUrl;
+});
+afterEach(() => { process.env.ANCHORING_SERVICE_URL = UNREACHABLE; });
+
+async function recertify() {
+  const r = await fetch(`${baseUrl}/api/certifications/${CERT_ID}/recertify`, {
+    method: 'POST',
+    headers: { 'content-type': 'application/json', authorization: 'Bearer ks1709-recert' },
+    body: JSON.stringify({ note: 'again' }),
+  });
+  const out: any = await r.json().catch(() => ({}));
+  return { status: r.status, body: out };
+}
+
+describe('KS-1709 a non-ok answer from anchoring on POST /api/certifications/:id/recertify is logged', () => {
+  it('RED KS-1709 V1: a 400 with a reason logs one warn naming both certificates, the status and the reason', async () => {
+    anchorReply = { status: 400, body: JSON.stringify({ success: false, error: { message: 'Invalid DID' } }) };
+    const r = await recertify();
+    expect(r.status).toBe(201);
+    expect(refused().length).toBe(1);
+    const fields = refused()[0][1];
+    expect([fields.originalCertificationId, fields.status]).toEqual([CERT_ID, 400]);
+    expect(String(fields.certId)).not.toBe(CERT_ID);
+    expect(String(fields.body)).toContain('Invalid DID');
+  });
+  it('RED KS-1709 V2: a 503 with an empty body logs the status and an empty body, not nothing', async () => {
+    anchorReply = { status: 503, body: '' };
+    const r = await recertify();
+    expect(r.status).toBe(201);
+    expect(refused().map((c) => [c[1].originalCertificationId, c[1].status, c[1].body])).toEqual([[CERT_ID, 503, '']]);
+  });
+  it('RED KS-1709 V3: a long body is cut to its first 200 characters', async () => {
+    anchorReply = { status: 422, body: 'x'.repeat(1000) };
+    const r = await recertify();
+    expect(r.status).toBe(201);
+    expect(refused().map((c) => [c[1].status, String(c[1].body).length])).toEqual([[422, 200]]);
+  });
+  it('CONTROL KS-1709 D1: an accepted anchor logs no refusal', async () => {
+    anchorReply = { status: 202, body: JSON.stringify({ success: true, data: { id: 'anchor-1709-v' } }) };
+    const r = await recertify();
+    expect([r.status, refused().length]).toEqual([201, 0]);
+  });
+  it('CONTROL KS-1709 D2: an unreachable anchoring service keeps its own warn and logs no refusal', async () => {
+    process.env.ANCHORING_SERVICE_URL = UNREACHABLE;
+    const r = await recertify();
+    expect([r.status, refused().length, unreachable().length]).toEqual([201, 0, 1]);
+  });
+});
```
