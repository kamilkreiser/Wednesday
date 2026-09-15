# READY — KS-1074 PART C (the POLLER's SIMULATED writer in `anchorStateSync.ts` :263-274 reads the document with `getDocument` immediately before its write and carries `threadToken` explicitly) — Ornith ornith:35b (Q4_K_M), r2 FIRST SAMPLE on the corrected brief (`2026-09-15_ks1074-ornith35b-night4`; r1 + its retry were Wednesday's copy-list defect, IMPROVEMENTS row 88) — checker PASS 7/7 at develop M55 `48e65c435`
# Source read by Wednesday 22:45: the read line inside `if (simFields.simulated) {` and the conditional carry before `...simFields,` — the brief's lines; 2 🔴 cells red BY ASSERTION at the tip, 2 controls green both trees; no new suite reds, tsc rc 0. **KS-1074 COMPLETE in Ornith's hands: Parts A (poller confirm) + B (two reconcile writers) + C (poller simulated) → ONE PR, bundle 28 in the raising brief.**
# PR NOTES for the raising seat: (1) rename the auto-named test to `ks1074-poller-simulated-writer-preserves-thread-token.test.ts`; normalise any `\u{1F534}` / `\u2014` escapes; (2) three test files + one product file in the PR; (3) paths lack the `Blockchain/Dev/` prefix.

```diff
--- a/services/originate/src/services/anchorStateSync.ts
+++ b/services/originate/src/services/anchorStateSync.ts
@@ -259,6 +259,7 @@ export async function pollAnchorUntilConfirmed(opts: PollAnchorOptions): Promise<
       // KS-587 (document-blob leg): a SIMULATED anchor never yields an
       // authoritative txHash, so before this branch the poller wrote nothing
       // for it at all — the document blob stayed `pending` with no `simulated`
       // key, a caller reading only the document could not tell the anchor is
       // not on chain (KS-589 D1), and `presentBlockchainHonestly` had neither
       // of its inputs (KS-589 D4). Write the honest declaration instead:
       // txHash stays null, the placeholder rides in `simulatedTxRef`.
       const simFields = simulatedFieldsFromAnchor(anchor);
       if (simFields.simulated) {
+        const prior = (await getDocument(documentId, tenantId))?.blockchain;
         await updateDocument(documentId, tenantId, {
           blockchain: {
             txHash: null,
@@ -267,6 +268,7 @@ export async function pollAnchorUntilConfirmed(opts: PollAnchorOptions): Promise<
             network: anchor.network,
             status: confirmed ? 'confirmed' : (anchor.status || 'submitted'),
             anchorId,
+            ...(prior?.threadToken ? { threadToken: prior.threadToken } : {}),
             ...simFields,
           },
           status: 'anchored',
--- /dev/null
+++ b/services/originate/src/__tests__/ks1074-the-poller-reconcile-blob-writers-also.test.ts
@@ -0,0 +1,101 @@
+/**
+ * =============================================================================
+ * KS-1074 — The poller's SIMULATED writer preserves threadToken.
+ * =============================================================================
+ */
+
+const mockGetDocument = jest.fn();
+const mockUpdateDocument = jest.fn();
+
+jest.mock('../repositories/documentRepo', () => ({
+  getDocument: mockGetDocument,
+  updateDocument: mockUpdateDocument,
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
+}));
+
+import { pollAnchorUntilConfirmed } from '../services/anchorStateSync';
+import type { DocumentRecord } from '../repositories/documentRepo';
+
+const MOCK_TX = `mock_tx_${'a'.repeat(64)}`;
+const THREAD_TOKEN = { policyId: 'b'.repeat(56), scriptAddress: 'addr_test1wq_ks1074', mintTxHash: 'c'.repeat(64), network: 'preview' };
+
+function baseDoc(overrides: Partial<DocumentRecord> = {}): DocumentRecord {
+  return {
+    id: 'doc-ks587-d1',
+    type: 'general',
+    status: 'anchored',
+    owner: { id: 'user-1' },
+    data: {},
+    contentHash: 'a'.repeat(64),
+    signatures: [],
+    blockchain: { txHash: null, blockHeight: 0, status: 'pending', anchorId: 'anchor_1' },
+    createdAt: '2026-01-01T00:00:00.000Z',
+    updatedAt: '2026-01-01T00:00:00.000Z',
+    ...overrides,
+  } as DocumentRecord;
+}
+
+function docWithToken(): DocumentRecord {
+  return baseDoc({ blockchain: { txHash: null, blockHeight: 0, status: 'pending', anchorId: 'anchor_1', threadToken: THREAD_TOKEN } } as Partial<DocumentRecord>);
+}
+
+function anchorResponse(body: unknown, ok = true): Response {
+  return { ok, json: async () => body } as unknown as Response;
+}
+
+function simulatedAnchorRead(over: Record<string, unknown> = {}) {
+  return {
+    status: 'confirmed',
+    transactionHash: null,
+    simulated: true,
+    simulatedTxRef: MOCK_TX,
+    blockNumber: 0,
+    network: 'devnet',
+    verified: false,
+    ...over,
+  };
+}
+
+const realFetch = global.fetch;
+let mockFetch: jest.Mock;
+
+beforeEach(() => {
+  jest.clearAllMocks();
+  mockFetch = jest.fn();
+  (global as any).fetch = mockFetch;
+  mockUpdateDocument.mockImplementation(async (_id, _tenant, updates) => ({ ...baseDoc(), ...updates }));
+});
+
+afterAll(() => {
+  (global as any).fetch = realFetch;
+});
+
+describe('KS-1074 — the poller simulated writer preserves threadToken', () => {
+  it('🔴 KS-1074 — a declared-simulated anchor keeps the prior threadToken on the document blob', async () => {
+    mockGetDocument.mockResolvedValue(docWithToken());
+    mockFetch.mockResolvedValue(anchorResponse(simulatedAnchorRead()));
+
+    await pollAnchorUntilConfirmed({ anchorId: 'anchor_1', documentId: 'doc-ks1074', tenantId: 'tenant-1', authHeader: 'Bearer t', intervalMs: 1, maxAttempts: 10 });
+
+    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
+    const blob = (mockUpdateDocument.mock.calls[0][2] as any).blockchain;
+    expect(blob.simulated).toBe(true);
+    expect(blob.txHash).toBeNull();
+    expect(blob.threadToken).toEqual(THREAD_TOKEN);
+  });
+
+  it('🔴 KS-1074 — the writer READS the document before it writes', async () => {
+    mockGetDocument.mockResolvedValue(docWithToken());
+    mockFetch.mockResolvedValue(anchorResponse(simulatedAnchorRead()));
+
+    await pollAnchorUntilConfirmed({ anchorId: 'anchor_1', documentId: 'doc-ks1074', tenantId: 'tenant-1', authHeader: 'Bearer t', intervalMs: 1, maxAttempts: 10 });
+
+    expect(mockGetDocument).toHaveBeenCalledWith('doc-ks1074', 'tenant-1');
+  });
+
+  it('KS-1074 control — with no threadToken in the prior blob the write carries no threadToken key', async () => {
+    mockGetDocument.mockResolvedValue(baseDoc());
+    mockFetch.mockResolvedValue(anchorResponse(simulatedAnchorRead()));
+
+    await pollAnchorUntilConfirmed({ anchorId: 'anchor_1', documentId: 'doc-ks1074', tenantId: 'tenant-1', authHeader: 'Bearer t', intervalMs: 1, maxAttempts: 10 });
+
+    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
+    const blob = (mockUpdateDocument.mock.calls[0][2] as any).blockchain;
+    expect(blob.simulated).toBe(true);
+    expect('threadToken' in blob).toBe(false);
+  });
+
+  it('KS-1074 control — the simulated write still carries its declaration and the KS-521 option', async () => {
+    mockGetDocument.mockResolvedValue(docWithToken());
+    mockFetch.mockResolvedValue(anchorResponse(simulatedAnchorRead()));
+
+    await pollAnchorUntilConfirmed({ anchorId: 'anchor_1', documentId: 'doc-ks1074', tenantId: 'tenant-1', authHeader: 'Bearer t', intervalMs: 1, maxAttempts: 10 });
+
+    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
+    const blob = (mockUpdateDocument.mock.calls[0][2] as any).blockchain;
+    expect(blob.simulatedTxRef).toBe(MOCK_TX);
+    expect(blob.status).toBe('confirmed');
+    expect(blob.anchorId).toBe('anchor_1');
+    expect(mockUpdateDocument.mock.calls[0][4]).toEqual({ preserveTerminalStatuses: true });
+  });
+});
```
