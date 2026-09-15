# READY — KS-1074 PART B (the two READ-TIME reconcile writers in `anchorStateSync.ts` carry `threadToken` — heal-to-confirmed :343-353 and heal-to-declared-simulated :379-390; the prior blob is in hand as `bc`) — Ornith ornith:35b (Q4_K_M), RETRY-ONCE after an A2b placeholder (`2026-09-15_ks1074-ornith35b-night/retry`, 33 s) — checker PASS 7/7 at develop M55 `48e65c435`
# Source read by Wednesday 22:33: both product hunks are the brief's carry line (explicit, conditional — never a spread of `bc`) PLUS a trailing `// KS-1074: …` comment the model added (harmless; the PR seat keeps or drops both); the jest test copies the ks1004 driver — 2 🔴 cells red BY ASSERTION at the tip, 2 controls green both trees; suite 637 → 641 green, tsc rc 0.
# PR NOTES for the raising seat: (1) the harness auto-named the test from the ticket title (`ks1074-the-poller-reconcile-blob-writers-also.test.ts`) — rename to `ks1074-reconcile-writers-preserve-thread-token.test.ts`; the `it` titles carry `\u{1F534}` / `\u2014` escapes — normalise to the glyphs; (2) Wednesday's DECISION recorded: carry `threadToken` on BOTH reconcile writers (a mint is independent of the anchor outcome — KS-1058's reasoning); (3) PART A (the poller's confirm writer, a per-write `getDocument` read, precedent = the failure writer) is its own READY when it lands; the poller's SIMULATED writer (:263-274) is a third task; ONE PR for the ticket; (4) the ticket asked for a runtime repro before the fix — the 🔴 cells ARE that repro at the unit level (red at the tip proves the erasure); a boot repro is the PR seat's call; (5) paths in the diff lack the `Blockchain/Dev/` prefix.

```diff
--- a/services/originate/src/services/anchorStateSync.ts
+++ b/services/originate/src/services/anchorStateSync.ts
@@ -347,6 +347,7 @@ export async function reconcileDocumentAnchorState(
         network: anchor.network,
         status: 'confirmed',
         anchorId: bc.anchorId,
+        ...(bc.threadToken ? { threadToken: bc.threadToken } : {}), // KS-1074: preserve prior threadToken on heal-to-confirmed path
       },
       status: 'anchored',
     }, undefined, { preserveTerminalStatuses: true });
@@ -383,6 +384,7 @@ export async function reconcileDocumentAnchorState(
         network: anchor.network,
         status: confirmed ? 'confirmed' : (anchor.status || 'submitted'),
         anchorId: bc.anchorId,
+        ...(bc.threadToken ? { threadToken: bc.threadToken } : {}), // KS-1074: preserve prior threadToken on heal-to-declared-simulated path
         ...simFields,
       },
       status: 'anchored',
--- /dev/null
+++ b/services/originate/src/__tests__/ks1074-the-poller-reconcile-blob-writers-also.test.ts
@@ -0,0 +1,95 @@
+/**
+ * KS-1074 — The poller/reconcile blob writers also erase threadToken — on the CONFIRM/heal path, not just the failure path #936 fixes
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
+import { reconcileDocumentAnchorState } from '../services/anchorStateSync';
+import type { DocumentRecord } from '../repositories/documentRepo';
+
+const REAL_TX = '4f1e6a8d2c7b9e3f1a5b7c9d2e4f6a8b1c3d5e7f9a2b4c6d8e0f2a4b6c8d0e2f';
+const THREAD_TOKEN = { policyId: 'b'.repeat(56), scriptAddress: 'addr_test1wq_ks1074', mintTxHash: 'c'.repeat(64), network: 'preview' };
+const MOCK_TX = 'tx_sim_ks1074';
+
+function baseDoc(overrides: Partial<DocumentRecord> = {}): DocumentRecord {
+  return {
+    id: 'doc-ks1074',
+    type: 'general',
+    status: 'anchored',
+    owner: { id: 'user-1' },
+    data: {},
+    contentHash: 'a'.repeat(64),
+    signatures: [],
+    blockchain: { txHash: null, blockHeight: 0, status: 'pending', anchorId: 'anchor_1' },
+    createdAt: '2026-01-01T00:00:00.000Z',
+    updatedAt: '2026-01-01T00:00:00.000Z', // long stale — passes the reconcile threshold
+    ...overrides,
+  } as DocumentRecord;
+}
+
+function anchorResponse(body: unknown, ok = true): Response {
+  return { ok, json: async () => body } as unknown as Response;
+}
+
+function staleInFlightWithToken(): DocumentRecord {
+  return baseDoc({ blockchain: { txHash: null, blockHeight: 0, status: 'pending', anchorId: 'anchor_1', threadToken: THREAD_TOKEN } } as Partial<DocumentRecord>);
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
+describe('KS-1074 — the reconcile writers preserve threadToken', () => {
+  it('\u{1F534} KS-1074 \u2014 heal-to-confirmed keeps the prior threadToken', async () => {
+    const doc = staleInFlightWithToken();
+    mockGetDocument.mockResolvedValue(doc);
+    mockFetch.mockResolvedValue(anchorResponse({ status: 'confirmed', verified: true, transactionHash: REAL_TX, blockNumber: 99, network: 'preview' }));
+    
+    await reconcileDocumentAnchorState(doc, 'tenant-1', 'Bearer t');
+    
+    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
+    const blob = (mockUpdateDocument.mock.calls[0][2] as any).blockchain;
+    expect(blob.status).toBe('confirmed');
+    expect(blob.txHash).toBe(REAL_TX);
+    expect(blob.threadToken).toEqual(THREAD_TOKEN);
+  });
+
+  it('\u{1F534} KS-1074 \u2014 heal-to-declared-simulated keeps the prior threadToken', async () => {
+    const doc = staleInFlightWithToken();
+    mockGetDocument.mockResolvedValue(doc);
+    mockFetch.mockResolvedValue(anchorResponse({ status: 'confirmed', transactionHash: null, simulated: true, simulatedTxRef: MOCK_TX, blockNumber: 0, network: 'devnet', verified: false }));
+    
+    await reconcileDocumentAnchorState(doc, 'tenant-1', 'Bearer t');
+    
+    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
+    const blob = (mockUpdateDocument.mock.calls[0][2] as any).blockchain;
+    expect(blob.simulated).toBe(true);
+    expect(blob.txHash).toBeNull();
+    expect(blob.threadToken).toEqual(THREAD_TOKEN);
+  });
+
+  it('KS-1074 control \u2014 with no threadToken in the prior blob, the confirmed write carries no threadToken key', async () => {
+    const doc = baseDoc();
+    mockGetDocument.mockResolvedValue(doc);
+    mockFetch.mockResolvedValue(anchorResponse({ status: 'confirmed', verified: true, transactionHash: REAL_TX, blockNumber: 99, network: 'preview' }));
+    
+    await reconcileDocumentAnchorState(doc, 'tenant-1', 'Bearer t');
+    
+    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
+    const blob = (mockUpdateDocument.mock.calls[0][2] as any).blockchain;
+    expect(blob.status).toBe('confirmed');
+    expect('threadToken' in blob).toBe(false);
+  });
+
+  it('KS-1074 control \u2014 the confirmed heal still writes the chain facts', async () => {
+    const doc = staleInFlightWithToken();
+    mockGetDocument.mockResolvedValue(doc);
+    mockFetch.mockResolvedValue(anchorResponse({ status: 'confirmed', verified: true, transactionHash: REAL_TX, blockNumber: 99, network: 'preview' }));
+    
+    await reconcileDocumentAnchorState(doc, 'tenant-1', 'Bearer t');
+    
+    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
+    const blob = (mockUpdateDocument.mock.calls[0][2] as any).blockchain;
+    expect(blob.txHash).toBe(REAL_TX);
+    expect(blob.blockHeight).toBe(99);
+    expect(blob.anchorId).toBe('anchor_1');
+    expect((mockUpdateDocument.mock.calls[0][2] as any).status).toBe('anchored');
+  });
+});
```
