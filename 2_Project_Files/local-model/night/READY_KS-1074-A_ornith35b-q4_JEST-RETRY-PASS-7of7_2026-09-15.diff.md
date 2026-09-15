# READY — KS-1074 PART A (the POLLER's CONFIRM writer in `anchorStateSync.ts` :228-238 reads the document with `getDocument` immediately before its write and carries `threadToken` explicitly — the failure writer's precedent) — Ornith ornith:35b (Q4_K_M), RETRY-ONCE (`2026-09-15_ks1074-ornith35b-night2/retry`, 35 s) — checker PASS 7/7 at develop M55 `48e65c435`
# Source read by Wednesday 22:38: see the hunks below against the brief `briefs/split_1074A/KS-1074.md` — the read line and the conditional carry; 2 🔴 cells red BY ASSERTION at the tip (one proves the writer now READS before it writes), 2 controls green both trees; suite no new reds, tsc rc 0. Wednesday's DECISION recorded: one `getDocument` read per confirm-write (≤ 60 per poll) rather than one read before the loop, because a single early read races the create-time mint.
# PR NOTES for the raising seat: (1) the harness auto-named the test from the ticket title — rename to `ks1074-poller-confirm-writer-preserves-thread-token.test.ts`; normalise any `\u{1F534}` / `\u2014` escapes in the titles; (2) Parts A + B + C (the poller's simulated writer) → ONE PR with the KS-1058 reasoning quoted; (3) paths lack the `Blockchain/Dev/` prefix.

```diff
--- a/services/originate/src/services/anchorStateSync.ts
+++ b/services/originate/src/services/anchorStateSync.ts
@@ -225,6 +225,7 @@ export async function pollAnchorUntilConfirmed(opts: PollAnchorOptions): Promise<
       if (txHash) {
         // KS-521: preserveTerminalStatuses — this poll can land minutes after
         // creation and must not stomp a `revoked` set by the owner in between.
+        const prior = (await getDocument(documentId, tenantId))?.blockchain;
         await updateDocument(documentId, tenantId, {
           blockchain: {
             txHash,
@@ -233,6 +234,7 @@ export async function pollAnchorUntilConfirmed(opts: PollAnchorOptions): Promise<
             network: anchor.network,
             status: confirmed ? 'confirmed' : (anchor.status || 'submitted'),
             anchorId,
+            ...(prior?.threadToken ? { threadToken: prior.threadToken } : {}),
           },
           status: 'anchored',
         }, undefined, { preserveTerminalStatuses: true });
--- /dev/null
+++ b/services/originate/src/__tests__/ks1074-the-poller-reconcile-blob-writers-also.test.ts
@@ -0,0 +1,108 @@
+/**
+ * =============================================================================
+ * KS-1074 — The poller/reconcile blob writers also erase threadToken
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
+const REAL_TX = '4f1e6a8d2c7b9e3f1a5b7c9d2e4f6a8b1c3d5e7f9a2b4c6d8e0f2a4b6c8d0e2f';
+const THREAD_TOKEN = { policyId: 'b'.repeat(56), scriptAddress: 'addr_test1wq_ks1074', mintTxHash: 'c'.repeat(64), network: 'preview' };
+
+function baseDoc(overrides: Partial<DocumentRecord> = {}): DocumentRecord {
+  return {
+    id: 'doc-ks1074-d1',
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
+describe('KS-1074 — the poller confirm writer preserves threadToken', () => {
+  it('\u{1F534} KS-1074 \u2014 a confirmed anchor keeps the prior threadToken on the document blob', async () => {
+    mockGetDocument.mockResolvedValue(docWithToken());
+    mockFetch.mockResolvedValue(anchorResponse({ status: 'confirmed', transactionHash: REAL_TX, blockNumber: 123, network: 'preview', verified: true }));
+
+    await pollAnchorUntilConfirmed({ anchorId: 'anchor_1', documentId: 'doc-ks1074', tenantId: 'tenant-1', authHeader: 'Bearer t', intervalMs: 1, maxAttempts: 10 });
+
+    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
+    const [, , updates] = mockUpdateDocument.mock.calls[0];
+    const blob = updates.blockchain as any;
+    expect(blob.status).toBe('confirmed');
+    expect(blob.txHash).toBe(REAL_TX);
+    expect(blob.threadToken).toEqual(THREAD_TOKEN);
+  });
+
+  it('\u{1F534} KS-1074 \u2014 the writer READS the document before it writes', async () => {
+    mockGetDocument.mockResolvedValue(docWithToken());
+    mockFetch.mockResolvedValue(anchorResponse({ status: 'confirmed', transactionHash: REAL_TX, blockNumber: 123, network: 'preview', verified: true }));
+
+    await pollAnchorUntilConfirmed({ anchorId: 'anchor_1', documentId: 'doc-ks1074', tenantId: 'tenant-1', authHeader: 'Bearer t', intervalMs: 1, maxAttempts: 10 });
+
+    expect(mockGetDocument).toHaveBeenCalledWith('doc-ks1074', 'tenant-1');
+  });
+
+  it('KS-1074 control \u2014 with no threadToken in the prior blob the write carries no threadToken key', async () => {
+    mockGetDocument.mockResolvedValue(baseDoc());
+    mockFetch.mockResolvedValue(anchorResponse({ status: 'confirmed', transactionHash: REAL_TX, blockNumber: 123, network: 'preview', verified: true }));
+
+    await pollAnchorUntilConfirmed({ anchorId: 'anchor_1', documentId: 'doc-ks1074', tenantId: 'tenant-1', authHeader: 'Bearer t', intervalMs: 1, maxAttempts: 10 });
+
+    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
+    const [, , updates] = mockUpdateDocument.mock.calls[0];
+    const blob = updates.blockchain as any;
+    expect(blob.status).toBe('confirmed');
+    expect('threadToken' in blob).toBe(false);
+  });
+
+  it('KS-1074 control \u2014 the confirm write still carries the chain facts and the KS-521 option', async () => {
+    mockGetDocument.mockResolvedValue(docWithToken());
+    mockFetch.mockResolvedValue(anchorResponse({ status: 'confirmed', transactionHash: REAL_TX, blockNumber: 123, network: 'preview', verified: true }));
+
+    await pollAnchorUntilConfirmed({ anchorId: 'anchor_1', documentId: 'doc-ks1074', tenantId: 'tenant-1', authHeader: 'Bearer t', intervalMs: 1, maxAttempts: 10 });
+
+    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
+    const [, , updates, , opts] = mockUpdateDocument.mock.calls[0];
+    const blob = updates.blockchain as any;
+    expect(blob.txHash).toBe(REAL_TX);
+    expect(blob.blockHeight).toBe(123);
+    expect(blob.network).toBe('preview');
+    expect(blob.anchorId).toBe('anchor_1');
+    expect(opts).toEqual({ preserveTerminalStatuses: true });
+  });
+});
```
