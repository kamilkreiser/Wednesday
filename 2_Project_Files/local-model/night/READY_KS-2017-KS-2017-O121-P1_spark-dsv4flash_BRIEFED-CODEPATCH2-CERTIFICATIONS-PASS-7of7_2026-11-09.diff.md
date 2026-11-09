# READY — KS-2017-KS-2017-O121-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2017_o121_p1_issue_certification_outer_catch_reads_an_unstringifiable_thrown_value/out.md.checker/patch.diff`** (from `ls` at 23:17 2026-11-09; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2017_o121_p1_issue_certification_outer_catch_reads_an_unstringifiable_thrown_value/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2017_o121_p1_issue_certification_outer_catch_reads_an_unstringifiable_thrown_value/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2017_o121_p1_issue_certification_outer_catch_reads_an_unstringifiable_thrown_value/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2017_o121_p1_issue_certification_outer_catch_reads_an_unstringifiable_thrown_value-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 23:17 2026-11-09 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2017_o121_p1_issue_certification_outer_catch_reads_an_unstringifiable_thrown_value/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d0b4825cc24493213f82b609670a4a0fa521a4b9`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/certifications.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks2017-issue-outer-catch-reads-an-unstringifiable-thrown-value.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks2017-issue-outer-catch-reads-an-unstringifiable-thrown-value.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/originate/src/routes/certifications.ts
173	0	Blockchain/Dev/services/originate/src/__tests__/ks2017-issue-outer-catch-reads-an-unstringifiable-thrown-value.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: certifications.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/certifications.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks2017-issue-outer-catch-reads-an-unstringifiable-thrown-value.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/certifications.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks2017-issue-outer-catch-reads-an-unstringifiable-thrown-value.test.ts 173 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/certifications.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks2017-issue-outer-catch-reads-an-unstringifiable-thrown-value.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-2017 POST /issue: the outer catch reads the thrown value safely RED ks2017 R1: an object with no prototype answers 500 and is logged with the constant reason', 'KS-2017 POST /issue: the outer catch reads the thrown value safely RED ks2017 R2: an object whose toString throws answers 500 and is logged with the constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2592 failed=11 | after: total=2596 failed=11` · `NEW reds: []` [baseline_suite.json total=2592 failed=11; after_suite.json total=2596 failed=11]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks2017-issue-outer-catch-reads-an-unstringifiable-thrown-value.test.ts` (+173/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/certifications.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `d0b4825cc24493213f82b609670a4a0fa521a4b9` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2017_o121_p1_issue_certification_outer_catch_reads_an_unstringifiable_thrown_value/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2017_o121_p1_issue_certification_outer_catch_reads_an_unstringifiable_thrown_value/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/certifications.ts b/Blockchain/Dev/services/originate/src/routes/certifications.ts
--- a/Blockchain/Dev/services/originate/src/routes/certifications.ts
+++ b/Blockchain/Dev/services/originate/src/routes/certifications.ts
@@ -933,5 +933,11 @@
       });
     } catch (error: any) {
-      const msg = error instanceof Error ? error.message : String(error);
+      let msg: string;
+      try {
+        // KS-2017: String() coerces here, inside the try; a value it cannot read (no prototype, a throwing toString) lands in the fallback below.
+        msg = String(error instanceof Error ? error.message : error);
+      } catch {
+        msg = 'unreadable thrown value';
+      }
       // KS-203: log name + code + stack so the next concurrent-load failure is
       // diagnosable (the previous blanket 500 logged only the message).
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks2017-issue-outer-catch-reads-an-unstringifiable-thrown-value.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks2017-issue-outer-catch-reads-an-unstringifiable-thrown-value.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks2017-issue-outer-catch-reads-an-unstringifiable-thrown-value.test.ts
@@ -0,0 +1,173 @@
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@127.0.0.1:1/test';
+process.env.SIMULATE_ANCHORING = 'true';
+
+// KS-2017: mockInject names the ONE failure a cell arms. Here only `getDoc` is used: the parent-document read at the top of the issue handler throws the chosen value into the handler's OUTER catch.
+let mockInject: Record<string, unknown> = {};
+const mockStore = new Map<string, any>();
+const mockLog = { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() };
+const mockSaveCertification = jest.fn(async (..._a: unknown[]) => undefined);
+const mockCharge = jest.fn(async (..._a: unknown[]) => {
+  if ('charge' in mockInject) throw mockInject.charge;
+  return { id: 'charge-1' };
+});
+const mockDeleteCertification = jest.fn(async (..._a: unknown[]) => {
+  if ('del' in mockInject) throw mockInject.del;
+  return 1;
+});
+const mockReserve = jest.fn(async (..._a: unknown[]) => {
+  if ('reserve' in mockInject) throw mockInject.reserve;
+  return undefined;
+});
+const mockExecuteRaw = jest.fn(async (..._a: unknown[]) => {
+  if ('update' in mockInject) throw mockInject.update;
+  return 1;
+});
+const mockQueryRaw = jest.fn(async (..._a: unknown[]) => {
+  if ('holder' in mockInject) throw mockInject.holder;
+  return [{ id: 'holder-row' }];
+});
+
+jest.mock('../repositories/documentRepo', () => ({
+  getDocument: jest.fn(async (id: string) => {
+    if ('getDoc' in mockInject) throw mockInject.getDoc;
+    return mockStore.get(id) ?? null;
+  }),
+  listDocuments: jest.fn(async () => ({ items: [...mockStore.values()], total: mockStore.size })),
+  saveDocument: jest.fn(async (record: any) => {
+    if ('saveDoc' in mockInject) throw mockInject.saveDoc;
+    const copy = JSON.parse(JSON.stringify(record));
+    if (!Array.isArray(copy.signatures)) copy.signatures = [];
+    mockStore.set(copy.id, copy);
+    return { dbId: '99999999-9999-4999-8999-999999999999', inserted: true };
+  }),
+  updateDocument: jest.fn(async () => undefined),
+  generateContentHash: jest.fn(() => 'a'.repeat(64)),
+  assertNoCycle: jest.fn(async () => undefined),
+  getOrganizationExternalRef: jest.fn(async () => null),
+}));
+jest.mock('../repositories/certificationRepo', () => ({
+  initRepo: jest.fn(async () => undefined),
+  getCertification: jest.fn(),
+  saveCertification: (...a: unknown[]) => mockSaveCertification(...a),
+  listCertifications: jest.fn(),
+  saveShare: jest.fn(),
+  getSharesByCertification: jest.fn(),
+  getLineageEvents: jest.fn(),
+  deleteCertification: (...a: unknown[]) => mockDeleteCertification(...a),
+  reserveCertificationRow: (...a: unknown[]) => mockReserve(...a),
+}));
+jest.mock('../db', () => ({ prisma: { $queryRaw: (...a: unknown[]) => mockQueryRaw(...a), $executeRaw: (...a: unknown[]) => mockExecuteRaw(...a), $executeRawUnsafe: jest.fn() } }));
+jest.mock('../services/chargeEvents', () => ({ createChargeEvent: (...a: unknown[]) => mockCharge(...a), getChargeEventsByCertification: jest.fn() }));
+jest.mock('../utils/notificationClient', () => ({ notifyDocumentCertified: jest.fn(async () => undefined), notifyDocumentRevoked: jest.fn(async () => undefined), notifyDocumentShared: jest.fn(async () => undefined) }));
+jest.mock('../repositories/shareRepo', () => ({ createShare: jest.fn() }));
+jest.mock('../repositories/lifecycleEventRepo', () => ({ createLifecycleEvent: jest.fn(), setLifecycleEventAnchor: jest.fn(), listLifecycleEvents: jest.fn() }));
+jest.mock('../events', () => ({ publishEvent: jest.fn(async () => undefined), EventTypes: { DOCUMENT_CREATED: 'document.created', DOCUMENT_OWNERSHIP_TRANSFERRED: 'document.ownership_transferred', DOCUMENT_VERSIONED: 'document.versioned', CERTIFICATION_ISSUED: 'certification.issued' } }));
+jest.mock('../services/threadTokenClient', () => ({ mintAndRegisterThreadToken: jest.fn(async () => ({})) }));
+jest.mock('../routes/verification', () => ({ registerInPlatformRegistry: jest.fn(async () => undefined) }));
+jest.mock('../services/anchorStateSync', () => ({ pollAnchorUntilConfirmed: jest.fn(async () => undefined), reconcileDocumentAnchorState: jest.fn(async (d: any) => d) }));
+jest.mock('../services/provenance', () => {
+  const actual = jest.requireActual('../services/provenance');
+  return { ...actual, recordActionProvenance: jest.fn(async () => undefined), getCreationProvenance: jest.fn(async () => null), wasCreatedByConnector: jest.fn(async () => true) };
+});
+jest.mock('@secuura/shared', () =>
+  require('./helpers/sharedModuleMock').makeSharedMock({
+    hasNulByte: jest.requireActual('@secuura/shared').hasNulByte,
+    runWithTenantId: jest.requireActual('@secuura/shared').runWithTenantId,
+    encryptField: jest.requireActual('@secuura/shared').encryptField,
+    decryptField: jest.requireActual('@secuura/shared').decryptField,
+    lookupHash: jest.requireActual('@secuura/shared').lookupHash,
+    verifyMessageSignature: jest.fn(() => true),
+  }),
+);
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (req: any, _res: unknown, next: () => void) => {
+    req.user = JSON.parse(String(req.headers['x-probe-user'] || '{}'));
+    next();
+  },
+}));
+jest.mock('../utils/logger', () => ({ logger: mockLog }));
+
+import express from 'express';
+import { certificationsRouter } from '../routes/certifications';
+
+const TENANT = 'a0000000-0000-4000-8000-000000000001';
+const ISSUER = { userId: '11111111-2222-4333-8444-555555552017', role: 'ISSUER_ADMIN', verificationLevel: 'none', tenantId: TENANT };
+const SOURCE_ID = 'doc-src-2017';
+const UNREADABLE = 'unreadable thrown value';
+
+const app = express();
+app.use((req: any, _res, next) => { req.tenantId = TENANT; next(); });
+app.use('/api/certifications', express.json(), certificationsRouter);
+let base = '';
+let server: ReturnType<typeof app.listen>;
+beforeAll(async () => {
+  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => r()); });
+  const a = server.address(); base = 'http://127.0.0.1:' + String(typeof a === 'object' && a ? a.port : 0);
+});
+afterAll(() => { server?.close(); });
+
+beforeEach(() => {
+  mockInject = {};
+  mockStore.clear();
+  mockStore.set(SOURCE_ID, { id: SOURCE_ID, type: 'DOCUMENT', status: 'draft', owner: { id: ISSUER.userId }, data: { title: 'src' }, contentHash: 'sha256:' + 'a'.repeat(64), signatures: [], createdAt: '2026-10-01T00:00:00Z', updatedAt: '2026-10-01T00:00:00Z' });
+  mockSaveCertification.mockClear(); mockCharge.mockClear(); mockDeleteCertification.mockClear(); mockReserve.mockClear(); mockExecuteRaw.mockClear(); mockQueryRaw.mockClear();
+  mockLog.info.mockReset(); mockLog.warn.mockReset(); mockLog.error.mockReset();
+});
+
+// KS-2017 (gate 203 G203-N4): the OUTER catch of POST /api/certifications/issue computed `error instanceof Error ? error.message : String(error)`
+// outside any try. A thrown value that String() cannot convert (an object with no prototype, or one whose toString throws) made the catch itself
+// throw, so the request got no answer. The cells arm the parent-document read to throw such a value and read what the client gets and what is logged.
+// NOT covered here (still open): a revoked Proxy, which makes `instanceof` and the later `error?.name` / `error?.code` reads throw.
+const noPrototype = (): unknown => Object.create(null);
+const toStringThrows = (): unknown => ({ toString() { throw new Error('ks2017 toString threw'); } });
+
+async function issue(): Promise<{ status: number | string; body: any }> {
+  try {
+    const res = await fetch(base + '/api/certifications/issue', {
+      method: 'POST',
+      headers: { 'content-type': 'application/json', 'x-probe-user': JSON.stringify(ISSUER) },
+      body: JSON.stringify({ type: 'DOCUMENT', parentDocumentId: SOURCE_ID, data: { title: 'c' } }),
+      signal: AbortSignal.timeout(3000),
+    });
+    return { status: res.status, body: await res.json().catch(() => ({})) };
+  } catch {
+    return { status: 'NO ANSWER', body: {} };
+  }
+}
+const lines = () => mockLog.error.mock.calls.filter((c) => c[0] === 'Failed to issue certification');
+
+describe('KS-2017 POST /issue: the outer catch reads the thrown value safely', () => {
+  it('control ks2017 C1: an ordinary Error answers 500 and is logged with its own message', async () => {
+    mockInject = { getDoc: new Error('ks2017 ordinary') };
+    const r = await issue();
+    expect(r.status).toBe(500);
+    expect(r.body).toMatchObject({ success: false, error: { code: 'INTERNAL_ERROR' } });
+    expect(lines()).toHaveLength(1);
+    expect(lines()[0][1]).toMatchObject({ error: 'ks2017 ordinary' });
+  });
+
+  it('control ks2017 C2: a thrown string answers 500 and is logged as itself', async () => {
+    mockInject = { getDoc: 'ks2017 plain string' };
+    const r = await issue();
+    expect(r.status).toBe(500);
+    expect(lines()).toHaveLength(1);
+    expect(lines()[0][1]).toMatchObject({ error: 'ks2017 plain string' });
+  });
+
+  it('RED ks2017 R1: an object with no prototype answers 500 and is logged with the constant reason', async () => {
+    mockInject = { getDoc: noPrototype() };
+    const r = await issue();
+    expect(r.status).toBe(500);
+    expect(r.body).toMatchObject({ success: false, error: { code: 'INTERNAL_ERROR' } });
+    expect(lines()).toHaveLength(1);
+    expect(lines()[0][1]).toMatchObject({ error: UNREADABLE });
+  });
+
+  it('RED ks2017 R2: an object whose toString throws answers 500 and is logged with the constant reason', async () => {
+    mockInject = { getDoc: toStringThrows() };
+    const r = await issue();
+    expect(r.status).toBe(500);
+    expect(lines()).toHaveLength(1);
+    expect(lines()[0][1]).toMatchObject({ error: UNREADABLE });
+  });
+});
```
