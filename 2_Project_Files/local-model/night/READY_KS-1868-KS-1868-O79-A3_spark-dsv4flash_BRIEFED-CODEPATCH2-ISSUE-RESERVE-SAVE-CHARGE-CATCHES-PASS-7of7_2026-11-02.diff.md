# READY — KS-1868-KS-1868-O79-A3 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a3_originate_certifications_issue_reserve_save_charge_catches_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 17:39 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a3_originate_certifications_issue_reserve_save_charge_catches_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a3_originate_certifications_issue_reserve_save_charge_catches_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a3_originate_certifications_issue_reserve_save_charge_catches_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a3_originate_certifications_issue_reserve_save_charge_catches_unreadable_throw-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 17:39 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a3_originate_certifications_issue_reserve_save_charge_catches_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `829233f1a388b943a9fd59c40e42332c27d9066b`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/certifications.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-issue-reserve-save-charge-catches-o79p3-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-issue-reserve-save-charge-catches-o79p3-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
21	3	Blockchain/Dev/services/originate/src/routes/certifications.ts
227	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-issue-reserve-save-charge-catches-o79p3-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (21 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: certifications.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/certifications.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-issue-reserve-save-charge-catches-o79p3-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/certifications.ts 21 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-issue-reserve-save-charge-catches-o79p3-unreadable-throw.test.ts 227 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/certifications.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-issue-reserve-save-charge-catches-o79p3-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (9 failed / 15 run; controls green; assertion reds)` [red_first.json: failed=9 of total=15; red cell(s): ['KS-1868 G105-F5 POST /issue reserveErr (pre-anchor reservation): the inner catch reads the thrown value safely RED ks1868 R1 reserve: a revoked Proxy gets the ordinary outcome and logs the constant reason', 'KS-1868 G105-F5 POST /issue reserveErr (pre-anchor reservation): the inner catch reads the thrown value safely RED ks1868 R2 reserve: an Error whose message getter throws gets the ordinary outcome and logs the constant reason', 'KS-1868 G105-F5 POST /issue reserveErr (pre-anchor reservation): the inner catch reads the thrown value safely RED ks1868 R3 reserve: an Error whose message getter returns a revoked Proxy gets the ordinary outcome through the real logger', 'KS-1868 G105-F5 POST /issue saveErr (derived document write): the inner catch reads the thrown value safely RED ks1868 R1 saveDoc: a revoked Proxy gets the ordinary outcome and logs the constant reason', 'KS-1868 G105-F5 POST /issue saveErr (derived document write): the inner catch reads the thrown value safely RED ks1868 R2 saveDoc: an Error whose message getter throws gets the ordinary outcome and logs the constant reason', 'KS-1868 G105-F5 POST /issue saveErr (derived document write): the inner catch reads the thrown value safely RED ks1868 R3 saveDoc: an Error whose message getter returns a revoked Proxy gets the ordinary outcome through the real logger', 'KS-1868 G105-F5 POST /issue chargeErr (charge event write): the inner catch reads the thrown value safely RED ks1868 R1 charge: a revoked Proxy gets the ordinary outcome and logs the constant reason', 'KS-1868 G105-F5 POST /issue chargeErr (charge event write): the inner catch reads the thrown value safely RED ks1868 R2 charge: an Error whose message getter throws gets the ordinary outcome and logs the constant reason', 'KS-1868 G105-F5 POST /issue chargeErr (charge event write): the inner catch reads the thrown value safely RED ks1868 R3 charge: an Error whose message getter returns a revoked Proxy gets the ordinary outcome through the real logger']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (15 passed / 15 run)` [green_after.json: failed=0 of total=15, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2163 failed=0 | after: total=2178 failed=0` · `NEW reds: []` [baseline_suite.json total=2163 failed=0; after_suite.json total=2178 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (+21/-3 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-issue-reserve-save-charge-catches-o79p3-unreadable-throw.test.ts` (+227/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/certifications.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `829233f1a388b943a9fd59c40e42332c27d9066b` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a3_originate_certifications_issue_reserve_save_charge_catches_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o79_a3_originate_certifications_issue_reserve_save_charge_catches_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a3_originate_certifications_issue_reserve_save_charge_catches_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/certifications.ts b/Blockchain/Dev/services/originate/src/routes/certifications.ts
--- a/Blockchain/Dev/services/originate/src/routes/certifications.ts
+++ b/Blockchain/Dev/services/originate/src/routes/certifications.ts
@@ -579,9 +579,15 @@
         await reserveCertificationRow(buildCertification(null, 'failed'), tenantId, (req as any).db);
         provisionalWritten = true;
       } catch (reserveErr: any) {
+        let reason: string;
+        try {
+          reason = String(reserveErr instanceof Error ? reserveErr.message : reserveErr);
+        } catch {
+          reason = 'unreadable thrown value';
+        }
         logger.warn('KS-1633: the pre-anchor reservation failed; the request continues and the authoritative save decides the response', {
           certId: id,
           tenantId,
-          error: reserveErr instanceof Error ? reserveErr.message : String(reserveErr),
+          error: reason,
         });
       }
@@ -745,10 +751,16 @@
           await saveLineageDocument(derivedDoc, tenantId, (req as any).db);
           derivedDocumentExternalId = derivedExternalId;
         } catch (saveErr: any) {
+          let reason: string;
+          try {
+            reason = String(saveErr instanceof Error ? saveErr.message : saveErr);
+          } catch {
+            reason = 'unreadable thrown value';
+          }
           logger.error('KS-70: failed to write derived document for cert lineage', {
             certId: id,
             parentDocumentId,
-            error: saveErr instanceof Error ? saveErr.message : String(saveErr),
+            error: reason,
           });
           // Fall through — the certification row already landed; the
           // derived doc can be back-filled later. We don't 500 the cert.
@@ -814,9 +826,15 @@
           metadata: { txHash: certification.blockchain?.txHash },
         });
       } catch (chargeErr: any) {
+        let reason: string;
+        try {
+          reason = String(chargeErr instanceof Error ? chargeErr.message : chargeErr);
+        } catch {
+          reason = 'unreadable thrown value';
+        }
         logger.error('KS-216: failed to persist charge event(s) — continuing, certification already issued', {
           certId: id,
           tenantId,
-          error: chargeErr instanceof Error ? chargeErr.message : String(chargeErr),
+          error: reason,
         });
       }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-issue-reserve-save-charge-catches-o79p3-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-issue-reserve-save-charge-catches-o79p3-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-issue-reserve-save-charge-catches-o79p3-unreadable-throw.test.ts
@@ -0,0 +1,227 @@
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@127.0.0.1:1/test';
+process.env.SIMULATE_ANCHORING = 'true';
+
+// mockInject names the ONE failure a cell arms: the key says which stand-in throws the chosen value (reserve, anchor, saveDoc, update, charge, del, holder).
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
+  getDocument: jest.fn(async (id: string) => mockStore.get(id) ?? null),
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
+const ISSUER = { userId: '11111111-2222-4333-8444-555555551868', role: 'ISSUER_ADMIN', verificationLevel: 'none', tenantId: TENANT };
+const SOURCE_ID = 'doc-src-1868';
+const UNREADABLE = 'unreadable thrown value';
+
+const app = express();
+app.use((req: any, _res, next) => { req.tenantId = TENANT; next(); });
+app.use('/api/certifications', express.json(), certificationsRouter);
+// One loopback stub plays auth (the issuer signature). The anchoring call never leaves the process: issue() answers it from a plain function.
+const stubApp = express();
+stubApp.use(express.json());
+stubApp.post('/api/issuer-certs/sign', (req, res) => {
+  res.json({ success: true, signature: 'ab', signatureAlgorithm: 'RSASSA-PSS-SHA256', signedContentHash: req.body.contentHash, signedAt: new Date().toISOString(),
+    cert: { id: 'c1', fingerprintSha256: 'f'.repeat(64), subject: 'CN=probe', issuer: 'CN=probe', certPem: 'PEM', validFrom: '2026-01-01', validUntil: '2027-01-01', trustLevel: 'self-signed' } });
+});
+let base = '';
+let stubBase = '';
+let server: ReturnType<typeof app.listen>;
+let stub: ReturnType<typeof stubApp.listen>;
+beforeAll(async () => {
+  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => r()); });
+  await new Promise<void>((r) => { stub = stubApp.listen(0, '127.0.0.1', () => r()); });
+  const a = server.address(); base = 'http://127.0.0.1:' + String(typeof a === 'object' && a ? a.port : 0);
+  const s = stub.address(); stubBase = 'http://127.0.0.1:' + String(typeof s === 'object' && s ? s.port : 0);
+  process.env.AUTH_SERVICE_URL = stubBase;
+});
+afterAll(() => { server?.close(); stub?.close(); });
+
+beforeEach(() => {
+  mockInject = {};
+  mockStore.clear();
+  mockStore.set(SOURCE_ID, { id: SOURCE_ID, type: 'DOCUMENT', status: 'draft', owner: { id: ISSUER.userId }, data: { title: 'src' }, contentHash: 'sha256:' + 'a'.repeat(64), signatures: [], createdAt: '2026-10-01T00:00:00Z', updatedAt: '2026-10-01T00:00:00Z' });
+  mockSaveCertification.mockClear(); mockCharge.mockClear(); mockDeleteCertification.mockClear(); mockReserve.mockClear(); mockExecuteRaw.mockClear(); mockQueryRaw.mockClear();
+  mockLog.info.mockReset(); mockLog.warn.mockReset(); mockLog.error.mockReset();
+});
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
+function useRealLogger(): void {
+  const real = jest.requireActual('../utils/logger').logger;
+  real.transports.forEach((t: { log?: (info: unknown, next: () => void) => void }) => {
+    t.log = (_info: unknown, next: () => void) => next();
+  });
+  mockLog.error.mockImplementation((...a: unknown[]) => (real.error as (...x: unknown[]) => unknown)(...a));
+  mockLog.warn.mockImplementation((...a: unknown[]) => (real.warn as (...x: unknown[]) => unknown)(...a));
+}
+
+// Issues one certification (parentDocumentId path). The anchoring call (the only fetch whose URL contains /api/anchors) is a PLAIN function: it accepts, or rejects with the value when the armed failure is `anchor`.
+async function issue(extra: Record<string, unknown> = {}): Promise<{ status: number | string; body: any; saved: number; charges: unknown[]; derived: number; deleted: number }> {
+  const clientFetch = globalThis.fetch;
+  (globalThis as any).fetch = (url: unknown, init?: unknown) => {
+    if (!String(url).includes('/api/anchors')) return clientFetch(url as string, init as RequestInit);
+    if ('anchor' in mockInject) return Promise.reject(mockInject.anchor);
+    return Promise.resolve(new Response(JSON.stringify({ success: true, data: { id: 'anchor-1868' } }), { status: 202, headers: { 'content-type': 'application/json' } }));
+  };
+  const state = () => ({
+    saved: mockSaveCertification.mock.calls.length,
+    charges: mockCharge.mock.calls.map((c) => c[0]),
+    derived: mockStore.size - 1,
+    deleted: mockDeleteCertification.mock.calls.length,
+  });
+  try {
+    const res = await clientFetch(base + '/api/certifications/issue', {
+      method: 'POST',
+      headers: { 'content-type': 'application/json', 'x-probe-user': JSON.stringify(ISSUER) },
+      body: JSON.stringify({ type: 'DOCUMENT', parentDocumentId: SOURCE_ID, data: { title: 'c' }, ...extra }),
+      signal: AbortSignal.timeout(3000),
+    });
+    return { status: res.status, body: await res.json().catch(() => ({})), ...state() };
+  } catch {
+    return { status: 'NO ANSWER', body: {}, ...state() };
+  } finally {
+    (globalThis as any).fetch = clientFetch;
+  }
+}
+
+// POST /api/certifications/issue, gate 105 G105-F5: three inner catches of the issue route read the thrown value unguarded (`error: X instanceof Error ? X.message : String(X)`): the pre-anchor
+// reservation (reserveErr), the derived-document write (saveErr) and the charge write (chargeErr). Each is a best-effort step: an ORDINARY failure is logged and the route continues to the 201.
+// An unreadable value (a revoked Proxy makes `instanceof` throw; a message getter that throws; a message getter that returns a hostile non-string, which the real logger cannot print) threw INSIDE
+// the catch, so the outer catch answered 500 even though the certification was already saved. After the fix each unreadable value gets the ordinary outcome and the catch logs the constant reason.
+type Site = { name: string; key: string; level: 'warn' | 'error'; prefix: string; extraFields: Record<string, unknown>; state: { saved: number; charges: unknown[]; derived: number; deleted: number }; chargeEvents: number };
+const SITES: Site[] = [
+  { name: 'reserveErr (pre-anchor reservation)', key: 'reserve', level: 'warn', prefix: 'KS-1633: the pre-anchor reservation failed', extraFields: { tenantId: expect.any(String) },
+    state: { saved: 1, charges: ['certification_sign', 'blockchain_anchor'], derived: 1, deleted: 0 }, chargeEvents: 2 },
+  { name: 'saveErr (derived document write)', key: 'saveDoc', level: 'error', prefix: 'KS-70: failed to write derived document', extraFields: { parentDocumentId: SOURCE_ID },
+    state: { saved: 1, charges: ['certification_sign', 'blockchain_anchor'], derived: 0, deleted: 0 }, chargeEvents: 2 },
+  { name: 'chargeErr (charge event write)', key: 'charge', level: 'error', prefix: 'KS-216: failed to persist charge event', extraFields: { tenantId: expect.any(String) },
+    state: { saved: 1, charges: ['certification_sign'], derived: 1, deleted: 0 }, chargeEvents: 0 },
+];
+
+async function expectOrdinaryOutcome(s: Site, thrown: unknown, logged: unknown, real = false): Promise<void> {
+  if (real) useRealLogger();
+  mockInject = { [s.key]: thrown };
+  const r = await issue();
+  expect(r.status).toBe(201);
+  expect(r.body).toMatchObject({ type: 'DOCUMENT' });
+  expect(r.body.chargeEvents).toHaveLength(s.chargeEvents);
+  expect({ saved: r.saved, charges: r.charges, derived: r.derived, deleted: r.deleted }).toEqual(s.state);
+  const lines = mockLog[s.level].mock.calls.filter((c) => String(c[0]).startsWith(s.prefix));
+  expect(lines).toEqual([[expect.any(String), { certId: r.body.id, ...s.extraFields, error: logged }]]);
+}
+
+describe.each(SITES)('KS-1868 G105-F5 POST /issue $name: the inner catch reads the thrown value safely', (s) => {
+  it(`control ks1868 C1 ${s.key}: an ordinary Error is logged with its own message and the certification is issued as before`, async () => {
+    await expectOrdinaryOutcome(s, new Error('ks1868 ordinary'), 'ks1868 ordinary');
+  });
+
+  it(`control ks1868 C2 ${s.key}: a thrown string is logged as itself, as before`, async () => {
+    await expectOrdinaryOutcome(s, 'ks1868 plain string', 'ks1868 plain string');
+  });
+
+  it(`RED ks1868 R1 ${s.key}: a revoked Proxy gets the ordinary outcome and logs the constant reason`, async () => {
+    await expectOrdinaryOutcome(s, revokedProxy(), UNREADABLE);
+  });
+
+  it(`RED ks1868 R2 ${s.key}: an Error whose message getter throws gets the ordinary outcome and logs the constant reason`, async () => {
+    await expectOrdinaryOutcome(s, throwingMessageError(), UNREADABLE);
+  });
+
+  it(`RED ks1868 R3 ${s.key}: an Error whose message getter returns a revoked Proxy gets the ordinary outcome through the real logger`, async () => {
+    await expectOrdinaryOutcome(s, messageGetterReturningRevokedProxy(), UNREADABLE, true);
+  });
+});
```
