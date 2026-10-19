# READY — KS-1660-PARENTDOCDROP-1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1660_p1c/out.md.checker/patch.diff`** (from `ls` at 01:02 2026-10-20; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1660_p1c/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1660_p1c/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1660_p1c/out.md.checker/section_3.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1660_p1c/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1660_p1c-control-r3/out.md.checker/patch.diff` rc 0, Wednesday (overnight 10-20)).

**Held 01:02 2026-10-20 by Wednesday (overnight 10-20) after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1660_p1c/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `a66cd6a4d1726794c816fd4fefec58c728d410e5`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/certifications.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts , Blockchain/Dev/services/originate/src/__tests__/ks1660-a-caller-s-data-parentdocumentid-overwrites.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts` (test) — equal to numstat.out's set (3 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
5	1	Blockchain/Dev/services/originate/src/routes/certifications.ts
1	0	Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts
148	0	Blockchain/Dev/services/originate/src/__tests__/ks1660-a-caller-s-data-parentdocumentid-overwrites.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (5 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: certifications.ts`
- CODE_PATCH2 (rung 3, 1 product files + 2 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/certifications.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts`, `Blockchain/Dev/services/originate/src/__tests__/ks1660-a-caller-s-data-parentdocumentid-overwrites.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/certifications.ts 5 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1660-a-caller-s-data-parentdocumentid-overwrites.test.ts 148 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=3 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/certifications.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- section 3 `section_3.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1660-a-caller-s-data-parentdocumentid-overwrites.test.ts` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (5 failed / 20 run; controls green; assertion reds)` [red_first.json: failed=5 of total=20; red cell(s): ["KS-1660 POST /api/certifications/issue with parentDocumentId as ISSUER_ADMIN RED KS-1660 R1: a supplied data.parentDocumentId does not overwrite the stored one: data and column both name the route's parent", 'KS-1660 POST /api/certifications/issue with parentDocumentId as ISSUER_ADMIN RED KS-1660 R2: a non-string data.parentDocumentId is dropped too', "KS-1660 POST /api/certifications/issue with parentDocumentId as SYSTEM_ADMIN RED KS-1660 R1: a supplied data.parentDocumentId does not overwrite the stored one: data and column both name the route's parent", 'KS-1660 POST /api/certifications/issue with parentDocumentId as SYSTEM_ADMIN RED KS-1660 R2: a non-string data.parentDocumentId is dropped too', 'KS-1660 the drop is logged without the value RED KS-1660 R3: a derived row that carried the key logs that it did, with the tenant, and never the planted value']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (20 passed / 20 run)` [green_after.json: failed=0 of total=20, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1510 failed=0 | after: total=1520 failed=0` · `NEW reds: []` [baseline_suite.json total=1510 failed=0; after_suite.json total=1520 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=3 products=1 tests=2 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (+5/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts` (+1/-0); 3 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/certifications.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict) — at the tip `a66cd6a4d1726794c816fd4fefec58c728d410e5` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1660_p1c/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1660_p1/KS-1660.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1660_p1c/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/certifications.ts b/Blockchain/Dev/services/originate/src/routes/certifications.ts
index 66791e844..15f3b2bdc 100644
--- a/Blockchain/Dev/services/originate/src/routes/certifications.ts
+++ b/Blockchain/Dev/services/originate/src/routes/certifications.ts
@@ -644,3 +644,4 @@
         // and logged (tenant and actor ids only, never the value). The certification's own `data` is not touched.
-        const { versionedById: droppedVersionedById, ...dataWithoutVersionedById } = (data ?? {}) as Record<string, unknown>;
+        // KS-1660: `parentDocumentId` is server-set the same way: the route's own value is written first and the spread below would overwrite it.
+        const { versionedById: droppedVersionedById, parentDocumentId: droppedParentDocumentId, ...dataWithoutVersionedById } = (data ?? {}) as Record<string, unknown>;
         if (droppedVersionedById !== undefined) {
@@ -648,2 +649,5 @@
         }
+        if (droppedParentDocumentId !== undefined) {
+          logger.info('KS-1660: a caller-supplied data.parentDocumentId was dropped from the derived certification document', { tenantId: getReqTenantId(req), userId: issuer.id });
+        }
         const derivedDoc: DocumentRecord = {
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts
index 1907f387c..c3197faa1 100644
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts
@@ -65,2 +65,3 @@
   'ks1508-versionedbyid-is-server-set.test.ts',
+  'ks1660-a-caller-s-data-parentdocumentid-overwrites.test.ts',
   'ks444-certifications-issue-body-types.test.ts',
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1660-a-caller-s-data-parentdocumentid-overwrites.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1660-a-caller-s-data-parentdocumentid-overwrites.test.ts
new file mode 100644
index 000000000..ef90c4826
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1660-a-caller-s-data-parentdocumentid-overwrites.test.ts
@@ -0,0 +1,148 @@
+/**
+ * KS-1660 - a caller's `data.parentDocumentId` no longer overwrites the server's on the derived certification document.
+ *
+ * POST /api/certifications/issue with a `parentDocumentId` writes a derived document whose stored `data` is the server's keys and
+ * then the caller's `data` spread after them. The route's own `parentDocumentId` (the `parent_document_id` column) is right, but the
+ * stored metadata blob, which a read shows, carried the CALLER's value, so a read showed another organisation's document as the
+ * parent. After this change the derived row's `data.parentDocumentId` is always the route's own value, as KS-1508 did for `versionedById`.
+ *
+ * Harness: the KS-1508 suite's pattern (the real certificationsRouter over an in-memory store that keeps the rows the handler saved).
+ */
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@127.0.0.1:1/test';
+process.env.SIMULATE_ANCHORING = 'true';
+process.env.ANCHORING_SERVICE_URL = 'http://127.0.0.1:2';
+
+const store = new Map<string, any>();
+const saved: any[] = [];
+
+jest.mock('../repositories/documentRepo', () => ({
+  getDocument: jest.fn(async (id: string) => store.get(id) ?? null),
+  listDocuments: jest.fn(async () => ({ items: [...store.values()], total: store.size })),
+  saveDocument: jest.fn(async (record: any) => {
+    const copy = JSON.parse(JSON.stringify(record));
+    if (!Array.isArray(copy.signatures)) copy.signatures = [];
+    store.set(copy.id, copy);
+    saved.push(copy);
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
+  saveCertification: jest.fn(async () => undefined),
+  listCertifications: jest.fn(),
+  saveShare: jest.fn(),
+  getSharesByCertification: jest.fn(),
+  getLineageEvents: jest.fn(),
+}));
+jest.mock('../db', () => ({ prisma: { $queryRaw: jest.fn(), $executeRaw: jest.fn(), $executeRawUnsafe: jest.fn() } }));
+jest.mock('../services/chargeEvents', () => ({ createChargeEvent: jest.fn(async () => ({ id: 'charge-1' })), getChargeEventsByCertification: jest.fn() }));
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
+jest.mock('../utils/logger', () => ({ logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() } }));
+
+import express from 'express';
+import { certificationsRouter } from '../routes/certifications';
+
+const TENANT = 'a0000000-0000-4000-8000-000000000001';
+const ISSUER = { userId: '11111111-2222-4333-8444-555555551660', role: 'ISSUER_ADMIN', verificationLevel: 'none', tenantId: TENANT };
+const SYSADMIN = { userId: '11111111-2222-4333-8444-555555551661', role: 'SYSTEM_ADMIN', tenantId: TENANT };
+const SOURCE_ID = 'doc-src-1660';
+const FOREIGN_ID = 'doc-another-organisations-document';
+
+const app = express();
+app.use((req: any, _res, next) => { req.tenantId = TENANT; next(); });
+app.use('/api/certifications', express.json(), certificationsRouter);
+const certStub = express();
+certStub.use(express.json());
+certStub.post('/api/issuer-certs/sign', (req, res) => {
+  res.json({ success: true, signature: 'ab', signatureAlgorithm: 'RSASSA-PSS-SHA256', signedContentHash: req.body.contentHash, signedAt: new Date().toISOString(),
+    cert: { id: 'c1', fingerprintSha256: 'f'.repeat(64), subject: 'CN=probe', issuer: 'CN=probe', certPem: 'PEM', validFrom: '2026-01-01', validUntil: '2027-01-01', trustLevel: 'self-signed' } });
+});
+let base = '';
+let server: ReturnType<typeof app.listen>;
+let stub: ReturnType<typeof certStub.listen>;
+beforeAll(async () => {
+  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => r()); });
+  await new Promise<void>((r) => { stub = certStub.listen(0, '127.0.0.1', () => r()); });
+  const a = server.address(); base = 'http://127.0.0.1:' + String(typeof a === 'object' && a ? a.port : 0);
+  const s = stub.address(); process.env.AUTH_SERVICE_URL = 'http://127.0.0.1:' + String(typeof s === 'object' && s ? s.port : 0);
+});
+afterAll(() => { server?.close(); stub?.close(); });
+beforeEach(() => {
+  store.clear(); saved.length = 0;
+  store.set(SOURCE_ID, { id: SOURCE_ID, type: 'DOCUMENT', status: 'draft', owner: { id: ISSUER.userId }, data: { title: 'src' }, contentHash: 'sha256:' + 'a'.repeat(64), signatures: [], createdAt: '2026-10-01T00:00:00Z', updatedAt: '2026-10-01T00:00:00Z' });
+});
+async function issue(principal: Record<string, unknown>, data: Record<string, unknown>) {
+  const res = await fetch(base + '/api/certifications/issue', { method: 'POST', headers: { 'content-type': 'application/json', 'x-probe-user': JSON.stringify(principal) }, body: JSON.stringify({ type: 'DOCUMENT', parentDocumentId: SOURCE_ID, data: { title: 'c', ...data } }) });
+  const written = saved.filter((r) => r.id !== SOURCE_ID);
+  return { status: res.status, written: written.length, rec: written.length > 0 ? written[written.length - 1] : null };
+}
+
+describe.each([['ISSUER_ADMIN', ISSUER], ['SYSTEM_ADMIN', SYSADMIN]])('KS-1660 POST /api/certifications/issue with parentDocumentId as %s', (_who, principal) => {
+  it('RED KS-1660 R1: a supplied data.parentDocumentId does not overwrite the stored one: data and column both name the route\'s parent', async () => {
+    const r = await issue(principal, { parentDocumentId: FOREIGN_ID });
+    expect([r.status, r.written]).toEqual([201, 1]);
+    expect(r.rec.data.parentDocumentId).toBe(SOURCE_ID);
+    expect(r.rec.parentDocumentId).toBe(SOURCE_ID);
+  });
+  it('RED KS-1660 R2: a non-string data.parentDocumentId is dropped too', async () => {
+    const r = await issue(principal, { parentDocumentId: { id: FOREIGN_ID } });
+    expect([r.status, r.rec.data.parentDocumentId]).toEqual([201, SOURCE_ID]);
+  });
+  it('CONTROL KS-1660 C1: without the key the stored parent is the route\'s, and the caller\'s OTHER data is kept', async () => {
+    const r = await issue(principal, { customNote: 'kept' });
+    expect([r.status, r.rec.data.parentDocumentId, r.rec.parentDocumentId, r.rec.data.customNote, r.rec.data.title]).toEqual([201, SOURCE_ID, SOURCE_ID, 'kept', 'c']);
+  });
+  it('CONTROL KS-1660 C2: the other caller keys still pass beside a planted parent', async () => {
+    const r = await issue(principal, { parentDocumentId: FOREIGN_ID, customNote: 'kept' });
+    expect([r.status, r.rec.data.customNote]).toEqual([201, 'kept']);
+  });
+});
+
+describe('KS-1660 the drop is logged without the value', () => {
+  const { logger } = jest.requireMock('../utils/logger') as { logger: { info: jest.Mock; warn: jest.Mock } };
+  const logged = () => [...logger.info.mock.calls, ...logger.warn.mock.calls].filter((c) => /KS-1660/.test(String(c[0])));
+  it('RED KS-1660 R3: a derived row that carried the key logs that it did, with the tenant, and never the planted value', async () => {
+    logger.info.mockClear(); logger.warn.mockClear();
+    const r = await issue(ISSUER, { parentDocumentId: FOREIGN_ID });
+    expect(r.status).toBe(201);
+    expect(logged().length).toBe(1);
+    expect(JSON.stringify(logged())).not.toContain(FOREIGN_ID);
+    expect(JSON.stringify(logged()[0][1])).toContain(TENANT);
+  });
+  it('CONTROL KS-1660 C3: a derived row that did not carry the key logs nothing about it', async () => {
+    logger.info.mockClear(); logger.warn.mockClear();
+    const r = await issue(ISSUER, {});
+    expect([r.status, logged().length]).toEqual([201, 0]);
+  });
+});
```
