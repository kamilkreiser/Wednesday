# READY — KS-1868-KS-1868-O69-P1 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o69_p1_originate_certifications_list_lineage_evidence_route_catches_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 10:04 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o69_p1_originate_certifications_list_lineage_evidence_route_catches_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o69_p1_originate_certifications_list_lineage_evidence_route_catches_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o69_p1_originate_certifications_list_lineage_evidence_route_catches_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o69_p1_originate_certifications_list_lineage_evidence_route_catches_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 10:04 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o69_p1_originate_certifications_list_lineage_evidence_route_catches_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `c8d77dce07dc502164de3325b1430e1f68016eb2`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/certifications.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-read-route-catches-p1-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-read-route-catches-p1-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
21	3	Blockchain/Dev/services/originate/src/routes/certifications.ts
125	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-read-route-catches-p1-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (21 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: certifications.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/certifications.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-read-route-catches-p1-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/certifications.ts 21 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-read-route-catches-p1-unreadable-throw.test.ts 125 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/certifications.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-read-route-catches-p1-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 12 run; controls green; assertion reds)` [red_first.json: failed=6 of total=12; red cell(s): ['KS-1868 GET / catch reads the thrown value safely RED ks1868 R1 GET /: a revoked Proxy from the repository is logged as a constant reason and answered with the constant 500', 'KS-1868 GET / catch reads the thrown value safely RED ks1868 R2 GET /: an Error whose message getter throws is logged as a constant reason and answered with the constant 500', 'KS-1868 GET /:id/lineage catch reads the thrown value safely RED ks1868 R1 GET /:id/lineage: a revoked Proxy from the repository is logged as a constant reason and answered with the constant 500', 'KS-1868 GET /:id/lineage catch reads the thrown value safely RED ks1868 R2 GET /:id/lineage: an Error whose message getter throws is logged as a constant reason and answered with the constant 500', 'KS-1868 GET /:id/evidence-bundle catch reads the thrown value safely RED ks1868 R1 GET /:id/evidence-bundle: a revoked Proxy from the repository is logged as a constant reason and answered with the constant 500', 'KS-1868 GET /:id/evidence-bundle catch reads the thrown value safely RED ks1868 R2 GET /:id/evidence-bundle: an Error whose message getter throws is logged as a constant reason and answered with the constant 500']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (12 passed / 12 run)` [green_after.json: failed=0 of total=12, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1999 failed=0 | after: total=2011 failed=0` · `NEW reds: []` [baseline_suite.json total=1999 failed=0; after_suite.json total=2011 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (+21/-3 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-read-route-catches-p1-unreadable-throw.test.ts` (+125/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/certifications.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `c8d77dce07dc502164de3325b1430e1f68016eb2` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o69_p1_originate_certifications_list_lineage_evidence_route_catches_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o69_p1_originate_certifications_list_lineage_evidence_route_catches_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o69_p1_originate_certifications_list_lineage_evidence_route_catches_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/certifications.ts b/Blockchain/Dev/services/originate/src/routes/certifications.ts
--- a/Blockchain/Dev/services/originate/src/routes/certifications.ts
+++ b/Blockchain/Dev/services/originate/src/routes/certifications.ts
@@ -1007,7 +1007,13 @@
         },
       });
     } catch (error) {
-      logger.error('Failed to list certifications', { error: error instanceof Error ? error.message : String(error) });
+      let reason: string;
+      try {
+        reason = error instanceof Error ? error.message : String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('Failed to list certifications', { error: reason });
       res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to list certifications' } });
     }
   }
@@ -1580,7 +1586,13 @@
         })),
       });
     } catch (error) {
-      logger.error('Failed to get lineage', { error: error instanceof Error ? error.message : String(error) });
+      let reason: string;
+      try {
+        reason = error instanceof Error ? error.message : String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('Failed to get lineage', { error: reason });
       res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get lineage data' } });
     }
   }
@@ -1688,7 +1700,13 @@
       );
       res.json(bundle);
     } catch (error) {
-      logger.error('Failed to generate evidence bundle', { error: error instanceof Error ? error.message : String(error) });
+      let reason: string;
+      try {
+        reason = error instanceof Error ? error.message : String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('Failed to generate evidence bundle', { error: reason });
       res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to generate evidence bundle' } });
     }
   }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-read-route-catches-p1-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-read-route-catches-p1-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-read-route-catches-p1-unreadable-throw.test.ts
@@ -0,0 +1,125 @@
+// KS-1868 (originate routes/certifications.ts, GET /api/certifications, GET /:id/lineage, GET /:id/evidence-bundle): each route catch logged
+// `error instanceof Error ? error.message : String(error)` itself and then answered a constant 500. When the thrown value cannot be read (a revoked Proxy makes
+// `instanceof` throw; an Error whose `message` getter throws), that read threw INSIDE the catch: the handler's promise rejected and the request got NO answer. Each catch
+// now reads the value inside its own try and logs the constant reason `unreadable thrown value`. The repository stand-in rejects with the thrown value on a real loopback
+// listener; a request that gets no answer within the window is reported as the string NO ANSWER, so a hang is a red assertion and not a stuck run.
+const mockGetCertification = jest.fn();
+const mockListCertifications = jest.fn();
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
+  listCertifications: (...a: unknown[]) => mockListCertifications(...a),
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
+  authenticate: () => (req: any, _res: unknown, next: () => void) => { req.user = null; next(); },
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
+  { route: 'GET /', path: '', context: 'Failed to list certifications', constant: { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to list certifications' } }, rejecter: mockListCertifications },
+  { route: 'GET /:id/lineage', path: `/${CERT_ID}/lineage`, context: 'Failed to get lineage', constant: { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get lineage data' } }, rejecter: mockGetCertification },
+  { route: 'GET /:id/evidence-bundle', path: `/${CERT_ID}/evidence-bundle`, context: 'Failed to generate evidence bundle', constant: { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to generate evidence bundle' } }, rejecter: mockGetCertification },
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
+  c.rejecter.mockRejectedValueOnce(thrown);
+  try {
+    const res = await fetch(`${baseUrl}/api/certifications${c.path}`, { signal: AbortSignal.timeout(1500) });
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
+  it(`RED ks1868 R1 ${c.route}: a revoked Proxy from the repository is logged as a constant reason and answered with the constant 500`, async () => {
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
