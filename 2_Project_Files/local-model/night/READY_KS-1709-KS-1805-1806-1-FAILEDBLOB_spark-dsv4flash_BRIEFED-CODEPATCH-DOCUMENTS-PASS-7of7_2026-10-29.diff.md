# READY — KS-1709-KS-1805-1806-1-FAILEDBLOB (Spark (DeepSeek V4 Flash), briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1806_1_failed_blob_unanchored-r2/out.md.checker/patch.diff`** (from `ls` at 22:04 2026-10-29; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1806_1_failed_blob_unanchored-r2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1806_1_failed_blob_unanchored-r2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 22:04 2026-10-29 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1806_1_failed_blob_unanchored-r2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `6d41673e0f79c0f02c2ec7b893cc960b6fa3ec10`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/documents.ts , Blockchain/Dev/services/originate/src/__tests__/ks1806-1-a-failed-anchor-blob-reads-unanchored-on-the-documents-surface.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/documents.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1806-1-a-failed-anchor-blob-reads-unanchored-on-the-documents-surface.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	3	Blockchain/Dev/services/originate/src/routes/documents.ts
176	0	Blockchain/Dev/services/originate/src/__tests__/ks1806-1-a-failed-anchor-blob-reads-unanchored-on-the-documents-surface.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (8 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 8 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 3.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/documents.ts byte-exact incl. leading whitespace (apply mode strict): OK 8 line(s) byte-exact incl. leading whitespace (of 8; 8 line(s) added by the apply)` [a3i_indent.out: `OK 8 line(s) byte-exact incl. leading whitespace (of 8; 8 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/documents.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1806-1-a-failed-anchor-blob-reads-unanchored-on-the-documents-surface.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1806-1-a-failed-anchor-blob-reads-unanchored-on-the-documents-surface.test.ts fails at the untouched tip (3 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=3 of total=8; red cell(s): ['KS-1709 / 1806-1: a failed anchor blob reads unanchored on the documents surface RED KS-1806-1 G1 a kept certification (KS-1709): GET /api/documents/:id says blockchain.anchored is false', 'KS-1709 / 1806-1: a failed anchor blob reads unanchored on the documents surface RED KS-1806-1 G1 the retry route dev-fallback blob: GET /api/documents/:id says blockchain.anchored is false', 'KS-1709 / 1806-1: a failed anchor blob reads unanchored on the documents surface RED KS-1806-1 G2: the POST /api/documents/:id/anchor guard consults the failed-status set, so a failed blob is retryable and is not refused as already anchored']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1806-1-a-failed-anchor-blob-reads-unanchored-on-the-documents-surface.test.ts passes with the product hunk (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1757 failed=0 | after: total=1765 failed=0` · `NEW reds: []` [baseline_suite.json total=1757 failed=0; after_suite.json total=1765 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +184/-3 test=src/__tests__/ks1806-1-a-failed-anchor-blob-reads-unanchored-on-the-documents-surface.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/documents.ts` (+8/-3 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1806-1-a-failed-anchor-blob-reads-unanchored-on-the-documents-surface.test.ts` (+176/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `6d41673e0f79c0f02c2ec7b893cc960b6fa3ec10` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1806_1_failed_blob_unanchored-r2/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1806_1_failed_blob_unanchored-r2/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/documents.ts b/Blockchain/Dev/services/originate/src/routes/documents.ts
--- a/Blockchain/Dev/services/originate/src/routes/documents.ts
+++ b/Blockchain/Dev/services/originate/src/routes/documents.ts
@@ -71,4 +71,9 @@
  *  hand the registrant that anchor's identity (the round-2 gate's MAJ-A). Still a 409: the caller
  *  must choose another documentUuid, and retrying this one can never succeed. */
 const LIVE_ANCHOR_ID_CONFLICT_BODY = { success: false, error: { code: 'CONFLICT', message: 'documentUuid is already held by an anchor record and cannot be registered' } } as const;
+/**
+ * KS-1709 / gate 15 finding 1806-1: the blockchain-blob statuses that mean nothing is anchored. `anchor_failed` is the KS-520 fail-closed state; `failed` is the KS-1124 F4
+ * value a kept certification carries (KS-1709) and that this file's own retry route writes in its dev fallback. verification.ts already treats both as failed (its FAILED_ANCHOR_STATUSES).
+ */
+const FAILED_ANCHOR_STATUSES: ReadonlySet<string> = new Set(['anchor_failed', 'failed']);
 export const documentsRouter = Router();
@@ -1196,8 +1201,8 @@
         blockchain: {
           // KS-520: `anchored` is status-derived, not presence-derived — the
           // fail-closed state records a blockchain object whose status is
-          // 'anchor_failed', and that must not read as anchored.
-          anchored: !!document.blockchain && document.blockchain.status !== 'anchor_failed',
+          // 'anchor_failed' (or 'failed', KS-1709), and that must not read as anchored.
+          anchored: !!document.blockchain && !FAILED_ANCHOR_STATUSES.has(String(document.blockchain.status)),
           // KS-587 (document-blob leg): the KS-522 rules applied at the serve
           // boundary too, so blobs written BEFORE the writer fixes (e.g. the
           // SIMULATE_ANCHORING branch's stored tx_sim_ hash) still read
@@ -1455,6 +1460,6 @@
       // KS-520: a document whose auto-anchor FAILED (fail-closed state,
       // blockchain.status === 'anchor_failed') is not anchored — it must be
       // retryable through this route rather than 400ing as "already anchored".
-      if (document.blockchain && document.blockchain.status !== 'anchor_failed') {
+      if (document.blockchain && !FAILED_ANCHOR_STATUSES.has(String(document.blockchain.status))) {
         return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Document is already anchored' } });
       }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1806-1-a-failed-anchor-blob-reads-unanchored-on-the-documents-surface.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1806-1-a-failed-anchor-blob-reads-unanchored-on-the-documents-surface.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1806-1-a-failed-anchor-blob-reads-unanchored-on-the-documents-surface.test.ts
@@ -0,0 +1,176 @@
+/**
+ * KS-1709 / gate 15 finding 1806-1: a blockchain blob whose status is 'failed' (the kept certification of KS-1709, and the retry route's own dev fallback, both KS-1124 F4) read as ANCHORED
+ * on GET /api/documents/:id, because documents.ts treated only 'anchor_failed' as unanchored; and the retry route POST /api/documents/:id/anchor refused it as "already anchored".
+ * verification.ts already treats both values as failed. These cells make the repository RETURN a document and read the route's own answer; the POST guard is pinned by a source-text cell
+ * (the POST handler calls the anchoring service, which this hermetic file does not reach).
+ *
+ * Harness: the same mocks as the retired-verify-route cells (DATABASE_URL shim, documentRepo + collaborators mocked, auth passthrough), a loopback listener.
+ */
+
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
+
+import * as fs from 'fs';
+import * as path from 'path';
+
+const DOC_ID = '22222222-3333-4444-8555-666666666666';
+
+const mockGetDocument = jest.fn();
+
+jest.mock('../repositories/documentRepo', () => ({
+  getDocument: mockGetDocument,
+  listDocuments: jest.fn(),
+  saveDocument: jest.fn(async () => ({ dbId: '99999999-9999-4999-8999-999999999999', inserted: true })),
+  updateDocument: jest.fn(async () => undefined),
+  getSigningRequest: jest.fn(),
+  saveSigningRequest: jest.fn(),
+  deleteSigningRequest: jest.fn(),
+  generateContentHash: jest.fn(() => 'a'.repeat(64)),
+  seedDemoDocuments: jest.fn(async () => undefined),
+  assertNoCycle: jest.fn(async () => undefined),
+}));
+
+jest.mock('../repositories/shareRepo', () => ({
+  createShare: jest.fn(),
+}));
+
+jest.mock('../repositories/lifecycleEventRepo', () => ({
+  createLifecycleEvent: jest.fn(),
+  setLifecycleEventAnchor: jest.fn(),
+  listLifecycleEvents: jest.fn(),
+}));
+
+jest.mock('../events', () => ({
+  publishEvent: jest.fn(async () => undefined),
+  EventTypes: {
+    DOCUMENT_CREATED: 'document.created',
+    DOCUMENT_OWNERSHIP_TRANSFERRED: 'document.ownership_transferred',
+    DOCUMENT_VERSIONED: 'document.versioned',
+  },
+}));
+
+jest.mock('../services/threadTokenClient', () => ({
+  mintAndRegisterThreadToken: jest.fn(async () => ({})),
+}));
+
+jest.mock('../routes/verification', () => ({
+  registerInPlatformRegistry: jest.fn(async () => undefined),
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (req: any, _res: unknown, next: () => void) => {
+    req.user = { userId: '11111111-2222-4333-8444-555555555555', role: 'ISSUER_ADMIN' };
+    next();
+  },
+}));
+
+jest.mock('../middleware/rbac', () => ({
+  isAllowedByRoleOrScope: () => true,
+}));
+
+jest.mock('../services/anchorStateSync', () => ({
+  pollAnchorUntilConfirmed: jest.fn(async () => undefined),
+  reconcileDocumentAnchorState: jest.fn(async (d: any) => d),
+}));
+
+jest.mock('../services/provenance', () => {
+  const actual = jest.requireActual('../services/provenance');
+  return {
+    ...actual,
+    recordActionProvenance: jest.fn(async () => undefined),
+    getCreationProvenance: jest.fn(async () => null),
+    wasCreatedByConnector: jest.fn(async () => true),
+  };
+});
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
+}));
+
+import express from 'express';
+import { documentsRouter, publicDocumentsRouter } from '../routes/documents';
+
+const app = express();
+// Same mount order as index.ts: public router first, then the auth-gated one.
+app.use('/api/documents', express.json(), publicDocumentsRouter);
+app.use('/api/documents', express.json(), documentsRouter);
+
+let baseUrl = '';
+let server: ReturnType<typeof app.listen>;
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  const address = server.address();
+  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
+});
+
+afterAll(() => {
+  server?.close();
+});
+
+// The blob KS-1124 F4 stores for a kept certification whose anchor was refused (KS-1709), and the blob this file's retry route writes in its dev fallback.
+const KEPT_CERT = { anchorId: null, txHash: null, blockHeight: null, anchoredAt: null, confidence: 'pending-onchain', anchoringStatus: 'failed', status: 'failed' };
+const RETRY_FALLBACK = { txHash: null, blockHeight: null, anchoredAt: null, confidence: 'pending-onchain', status: 'failed' };
+const CONFIRMED = { anchorId: 'anchor_1', txHash: 'f'.repeat(64), blockHeight: 4242, anchoredAt: '2026-10-29T00:00:00.000Z', status: 'confirmed' };
+const SUBMITTED = { anchorId: 'anchor_1', txHash: 'e'.repeat(64), blockHeight: 0, anchoredAt: '2026-10-29T00:00:00.000Z', status: 'submitted' };
+
+function row(blockchain: unknown) {
+  return {
+    id: DOC_ID,
+    type: 'DOCUMENT',
+    status: 'issued',
+    contentHash: 'a'.repeat(64),
+    signatures: [],
+    data: { title: 'c' },
+    blockchain,
+    owner: { id: '11111111-2222-4333-8444-555555555555' },
+    createdAt: '2026-10-29T00:00:00Z',
+    updatedAt: '2026-10-29T00:00:00Z',
+  };
+}
+
+async function readAnchored(blockchain: unknown): Promise<{ http: number; anchored: unknown }> {
+  mockGetDocument.mockResolvedValue(row(blockchain));
+  const res = await fetch(`${baseUrl}/api/documents/${DOC_ID}`);
+  const body: any = await res.json().catch(() => ({}));
+  return { http: res.status, anchored: body?.blockchain?.anchored };
+}
+
+const SRC = fs.readFileSync(path.resolve(__dirname, '..', 'routes', 'documents.ts'), 'utf8');
+const RETRY_FROM = SRC.indexOf("'/:id/anchor',");
+const RETRY_LAST = 'Document is already anchored';
+const RETRY_BLOCK = RETRY_FROM < 0 ? '' : SRC.slice(RETRY_FROM, SRC.indexOf(RETRY_LAST, RETRY_FROM) + RETRY_LAST.length);
+
+describe('KS-1709 / 1806-1: a failed anchor blob reads unanchored on the documents surface', () => {
+  it.each([
+    ['a kept certification (KS-1709)', KEPT_CERT],
+    ['the retry route dev-fallback blob', RETRY_FALLBACK],
+  ])('RED KS-1806-1 G1 %s: GET /api/documents/:id says blockchain.anchored is false', async (_label, blob) => {
+    expect(await readAnchored(blob)).toEqual({ http: 200, anchored: false });
+  });
+
+  it('RED KS-1806-1 G2: the POST /api/documents/:id/anchor guard consults the failed-status set, so a failed blob is retryable and is not refused as already anchored', () => {
+    expect(RETRY_BLOCK.includes('!FAILED_ANCHOR_STATUSES.has(String(document.blockchain.status))')).toBe(true);
+    expect(RETRY_BLOCK.includes("document.blockchain.status !== 'anchor_failed'")).toBe(false);
+  });
+
+  it('control KS-1806-1 C1: a blob with status anchor_failed (KS-520) still reads unanchored', async () => {
+    expect(await readAnchored({ ...KEPT_CERT, status: 'anchor_failed' })).toEqual({ http: 200, anchored: false });
+  });
+
+  it('control KS-1806-1 C2: a document with no blockchain blob still reads unanchored', async () => {
+    expect(await readAnchored(null)).toEqual({ http: 200, anchored: false });
+  });
+
+  it.each([
+    ['confirmed', CONFIRMED],
+    ['submitted', SUBMITTED],
+  ])('control KS-1806-1 C3 %s: a blob in a live anchor state still reads anchored', async (_label, blob) => {
+    expect(await readAnchored(blob)).toEqual({ http: 200, anchored: true });
+  });
+
+  it('control KS-1806-1 C4: the block located in documents.ts is ONE handler, the anchor-retry route (it holds the already-anchored refusal once)', () => {
+    expect([RETRY_BLOCK.length > 0, RETRY_BLOCK.split(RETRY_LAST).length, RETRY_BLOCK.includes('documentsRouter')]).toEqual([true, 2, false]);
+  });
+});
```
