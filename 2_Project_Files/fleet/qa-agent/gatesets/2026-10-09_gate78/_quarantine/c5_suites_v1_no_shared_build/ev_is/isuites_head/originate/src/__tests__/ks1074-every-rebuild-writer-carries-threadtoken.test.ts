/**
 * =============================================================================
 * KS-1074 — every blob-rebuild writer must carry threadToken forward
 * =============================================================================
 * `updateDocument` replaces the `blockchain` column WHOLESALE. Measured at source rather than taken
 * from a comment: `documentRepo.ts` builds `const updated = { ...doc, ...updates }` — a TOP-LEVEL
 * spread — so `updates.blockchain` replaces `doc.blockchain` entirely and every key not restated is
 * destroyed.
 *
 * KS-1058 fixed exactly one writer, `markDocumentAnchorFailed` (the FAILURE path). Four more rebuild
 * the blob as a literal with no `threadToken`, and two of them are on the SUCCESS path — so a
 * document that mints a thread token at create and then anchors NORMALLY loses the cache that
 * dashboards read. `state_thread_registry` stays the canonical truth; the blob field exists to avoid
 * that lookup, which is the whole point of KS-1058.
 *
 * WHY EACH CELL IS PER WRITER: the five writers are five separate object literals, and a cell on one
 * says nothing about the others. That is how four of them survived KS-1058.
 *
 * `simulatedTxRef` is deliberately NOT carried forward — a decision per writer, which is what this
 * ticket asks for. The two simulated writers already spread `...simFields`, derived from the anchor
 * being read, so the value is reconstructed rather than inherited; and carrying a simulated marker
 * onto a write that has just recorded a REAL confirmed txHash would assert something false.
 * =============================================================================
 */

const mockGetDocument = jest.fn();
const mockUpdateDocument = jest.fn();

jest.mock('../repositories/documentRepo', () => ({
  getDocument: mockGetDocument,
  updateDocument: mockUpdateDocument,
}));

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

import {
  markDocumentAnchorFailed,
  pollAnchorUntilConfirmed,
  reconcileDocumentAnchorState,
} from '../services/anchorStateSync';
import type { DocumentRecord } from '../repositories/documentRepo';

const REAL_TX = 'd'.repeat(64);
const THREAD_TOKEN = {
  policyId: 'b'.repeat(56),
  scriptAddress: 'addr_test1wq_ks1074',
  mintTxHash: 'c'.repeat(64),
  network: 'preview',
};

function docWithBlob(blockchain: Record<string, unknown>): DocumentRecord {
  return {
    id: 'doc-ks1074',
    type: 'general',
    status: 'anchored',
    owner: { id: 'user-1' },
    data: {},
    contentHash: 'a'.repeat(64),
    signatures: [],
    blockchain,
    createdAt: '2026-01-01T00:00:00.000Z',
    updatedAt: '2026-01-01T00:00:00.000Z',
  } as unknown as DocumentRecord;
}

const realFetch = global.fetch;

/** One anchor read, then the poller stops. */
function stubAnchor(anchor: Record<string, unknown>) {
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ data: anchor }),
  }) as unknown as typeof fetch;
}

/** The blob handed to updateDocument on its single call. */
function writtenBlob(): Record<string, any> {
  expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
  return (mockUpdateDocument.mock.calls[0][2] as any).blockchain;
}

beforeEach(() => {
  mockGetDocument.mockReset();
  mockUpdateDocument.mockReset().mockResolvedValue(undefined);
  global.fetch = jest.fn().mockRejectedValue(new Error('anchor read disabled in test')) as unknown as typeof fetch;
});

afterAll(() => {
  global.fetch = realFetch;
});

describe('KS-1074 — every rebuild writer carries threadToken forward', () => {
  it('KS-1074 W1 FAILCLOSED: markDocumentAnchorFailed carries it (KS-1058, re-pinned here so the set is complete)', async () => {
    mockGetDocument.mockResolvedValueOnce(
      docWithBlob({ txHash: null, blockHeight: 0, status: 'pending', anchorId: 'anchor_1', threadToken: THREAD_TOKEN }),
    );
    await markDocumentAnchorFailed('doc-ks1074', 'tenant-1', 'anchor_1', 'boom');
    const blob = writtenBlob();
    expect([blob.status, blob.threadToken]).toEqual(['anchor_failed', THREAD_TOKEN]);
  });

  it('KS-1074 W2 POLLERCONFIRM: the poller SUCCESS writer carries it — a real txHash, the path a normal anchor takes', async () => {
    mockGetDocument.mockResolvedValue(
      docWithBlob({ txHash: null, blockHeight: 0, status: 'submitted', anchorId: 'anchor_1', threadToken: THREAD_TOKEN }),
    );
    stubAnchor({ status: 'confirmed', transactionHash: REAL_TX, blockNumber: 4242, verified: true, network: 'preview' });
    await pollAnchorUntilConfirmed({ anchorId: 'anchor_1', documentId: 'doc-ks1074', tenantId: 'tenant-1', authHeader: '', maxAttempts: 1, intervalMs: 1 });
    const blob = writtenBlob();
    // the write really is the SUCCESS shape, not a failure write that happens to carry the token
    expect([blob.txHash, blob.status, blob.threadToken]).toEqual([REAL_TX, 'confirmed', THREAD_TOKEN]);
  });

  it('KS-1074 W3 POLLERSIMULATED: the poller SIMULATED writer carries it, and still declares the simulation', async () => {
    mockGetDocument.mockResolvedValue(
      docWithBlob({ txHash: null, blockHeight: 0, status: 'submitted', anchorId: 'anchor_1', threadToken: THREAD_TOKEN }),
    );
    stubAnchor({ status: 'confirmed', transactionHash: `tx_sim_${'e'.repeat(64)}`, simulated: true, simulatedTxRef: `tx_sim_${'e'.repeat(64)}`, blockNumber: 1, verified: true });
    await pollAnchorUntilConfirmed({ anchorId: 'anchor_1', documentId: 'doc-ks1074', tenantId: 'tenant-1', authHeader: '', maxAttempts: 1, intervalMs: 1 });
    const blob = writtenBlob();
    expect([blob.txHash, blob.simulated, blob.threadToken]).toEqual([null, true, THREAD_TOKEN]);
  });

  it('KS-1074 W4 RECONCILECONFIRM: the read-time heal-to-confirmed writer carries it', async () => {
    const doc = docWithBlob({ txHash: null, blockHeight: 0, status: 'submitted', anchorId: 'anchor_1', threadToken: THREAD_TOKEN });
    (doc as any).updatedAt = '2020-01-01T00:00:00.000Z';   // older than RECONCILE_STALE_MS
    mockGetDocument.mockResolvedValue(doc);
    mockUpdateDocument.mockResolvedValue(doc);
    stubAnchor({ status: 'confirmed', transactionHash: REAL_TX, blockNumber: 4242, verified: true, network: 'preview' });
    await reconcileDocumentAnchorState(doc, 'tenant-1', '');
    const blob = writtenBlob();
    expect([blob.txHash, blob.status, blob.threadToken]).toEqual([REAL_TX, 'confirmed', THREAD_TOKEN]);
  });

  it('KS-1074 W5 RECONCILESIMULATED: the read-time heal-to-simulated writer carries it', async () => {
    const doc = docWithBlob({ txHash: null, blockHeight: 0, status: 'submitted', anchorId: 'anchor_1', threadToken: THREAD_TOKEN });
    (doc as any).updatedAt = '2020-01-01T00:00:00.000Z';
    mockGetDocument.mockResolvedValue(doc);
    mockUpdateDocument.mockResolvedValue(doc);
    stubAnchor({ status: 'submitted', transactionHash: `tx_sim_${'e'.repeat(64)}`, simulated: true, simulatedTxRef: `tx_sim_${'e'.repeat(64)}`, blockNumber: 1 });
    await reconcileDocumentAnchorState(doc, 'tenant-1', '');
    const blob = writtenBlob();
    expect([blob.txHash, blob.simulated, blob.threadToken]).toEqual([null, true, THREAD_TOKEN]);
  });

  it('KS-1074 FALSYTOKEN: a present-but-falsy token is carried, because the guard is != null and not truthiness', async () => {
    // The MINOR-2 item from #936's gate: `prior?.threadToken ? ... : {}` drops an empty string or 0 —
    // discarded by the very write that exists to stop a value being lost. Theoretical for a real hex
    // token, and exactly the kind of thing a rewrite reintroduces, so it is pinned.
    mockGetDocument.mockResolvedValueOnce(
      docWithBlob({ txHash: null, blockHeight: 0, status: 'pending', anchorId: 'anchor_1', threadToken: '' }),
    );
    await markDocumentAnchorFailed('doc-ks1074', 'tenant-1', 'anchor_1', 'boom');
    const blob = writtenBlob();
    expect(['threadToken' in blob, blob.threadToken]).toEqual([true, '']);
  });

  it('KS-1074 ABSENTSTAYSABSENT: with no prior token the key is not invented', async () => {
    mockGetDocument.mockResolvedValueOnce(
      docWithBlob({ txHash: null, blockHeight: 0, status: 'pending', anchorId: 'anchor_1' }),
    );
    await markDocumentAnchorFailed('doc-ks1074', 'tenant-1', 'anchor_1', 'boom');
    const blob = writtenBlob();
    expect(['threadToken' in blob, blob.status]).toEqual([false, 'anchor_failed']);
  });

  it('KS-1074 NOSIMULATEDTXREFONREAL: a real confirmed write does NOT inherit a prior simulatedTxRef', async () => {
    // The decision this ticket asks for, asserted rather than left to a reader: carrying a simulated
    // marker onto a write that has just recorded a REAL confirmed txHash would assert something false.
    mockGetDocument.mockResolvedValue(
      docWithBlob({ txHash: null, status: 'submitted', anchorId: 'anchor_1', threadToken: THREAD_TOKEN, simulatedTxRef: `tx_sim_${'e'.repeat(64)}`, simulated: true }),
    );
    stubAnchor({ status: 'confirmed', transactionHash: REAL_TX, blockNumber: 4242, verified: true });
    await pollAnchorUntilConfirmed({ anchorId: 'anchor_1', documentId: 'doc-ks1074', tenantId: 'tenant-1', authHeader: '', maxAttempts: 1, intervalMs: 1 });
    const blob = writtenBlob();
    expect([blob.txHash, 'simulatedTxRef' in blob, blob.simulated, blob.threadToken])
      .toEqual([REAL_TX, false, undefined, THREAD_TOKEN]);
  });
});
