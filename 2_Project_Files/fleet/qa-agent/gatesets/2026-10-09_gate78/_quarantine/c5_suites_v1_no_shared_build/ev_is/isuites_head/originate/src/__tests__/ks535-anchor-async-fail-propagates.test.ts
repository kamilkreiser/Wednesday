/**
 * KS-535 — a terminally-failed on-chain anchor must propagate to the
 * document instead of leaving it claiming `status: 'anchored'` forever.
 *
 * KS-520 pinned the SYNCHRONOUS half (the anchoring POST failing). This file
 * pins the ASYNCHRONOUS half in services/anchorStateSync.ts:
 *
 *  1. `pollAnchorUntilConfirmed` — on a terminal `failed` anchor (two
 *     consecutive observations; anchoring resets retrying rows to 'pending'
 *     before their backoff, so 'failed' is terminal) it writes the KS-520
 *     fail-closed shape and reverts the accept-time optimistic status.
 *  2. `markDocumentAnchorFailed` — never downgrades a CONFIRMED anchor.
 *     (KS-1004 narrowed this: it used to refuse on a txHash too, which made
 *     the failure writer unreachable for a transaction that reached the chain
 *     and then failed. The write is now non-destructive — the hash is carried
 *     forward — so the guard no longer has to refuse in order to protect it.)
 *  3. `reconcileDocumentAnchorState` — read-time self-healing for documents
 *     whose poller died (restart / failure landed after the poll window),
 *     in both directions (stale-pending → anchor_failed, and
 *     anchor_failed/stale-pending → confirmed).
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
  authoritativeTxHash,
  markDocumentAnchorFailed,
  pollAnchorUntilConfirmed,
  reconcileDocumentAnchorState,
} from '../services/anchorStateSync';
import type { DocumentRecord } from '../repositories/documentRepo';

const REAL_TX = '4f1e6a8d2c7b9e3f1a5b7c9d2e4f6a8b1c3d5e7f9a2b4c6d8e0f2a4b6c8d0e2f';

function baseDoc(overrides: Partial<DocumentRecord> = {}): DocumentRecord {
  return {
    id: 'doc-ks535',
    type: 'general',
    status: 'anchored',
    owner: { id: 'user-1' },
    data: {},
    contentHash: 'a'.repeat(64),
    signatures: [],
    blockchain: { txHash: null, blockHeight: 0, status: 'pending', anchorId: 'anchor_1' },
    createdAt: '2026-01-01T00:00:00.000Z',
    updatedAt: '2026-01-01T00:00:00.000Z', // long stale — reconcile threshold passes
    ...overrides,
  } as DocumentRecord;
}

function anchorResponse(body: unknown, ok = true): Response {
  return {
    ok,
    json: async () => body,
  } as unknown as Response;
}

const realFetch = global.fetch;
let mockFetch: jest.Mock;

beforeEach(() => {
  jest.clearAllMocks();
  mockFetch = jest.fn();
  (global as any).fetch = mockFetch;
  mockUpdateDocument.mockImplementation(async (_id, _tenant, updates) => ({ ...baseDoc(), ...updates }));
});

afterAll(() => {
  (global as any).fetch = realFetch;
});

describe('authoritativeTxHash', () => {
  it('rejects placeholder prefixes and empties, accepts a real hash', () => {
    expect(authoritativeTxHash({ transactionHash: `tx_${'a'.repeat(8)}` })).toBeNull();
    expect(authoritativeTxHash({ transactionHash: `mock_tx_${'a'.repeat(8)}` })).toBeNull();
    expect(authoritativeTxHash({ transactionHash: null })).toBeNull();
    expect(authoritativeTxHash({})).toBeNull();
    expect(authoritativeTxHash({ transactionHash: REAL_TX })).toBe(REAL_TX);
    expect(authoritativeTxHash({ transactionId: REAL_TX })).toBe(REAL_TX);
  });
});

describe('pollAnchorUntilConfirmed — terminal failure propagates (the KS-535 defect)', () => {
  it('writes the KS-520 fail-closed shape after two consecutive failed observations', async () => {
    mockGetDocument.mockResolvedValue(baseDoc());
    mockFetch.mockResolvedValue(anchorResponse({
      status: 'failed',
      transactionHash: null,
      errorMessage: 'ConwayMempoolFailure "All inputs are spent"',
    }));

    await pollAnchorUntilConfirmed({
      anchorId: 'anchor_1', documentId: 'doc-ks535', tenantId: 'tenant-1',
      authHeader: 'Bearer t', intervalMs: 1, maxAttempts: 10,
    });

    // Exactly one write: the fail-closed state, terminal-status-guarded.
    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
    const [, , updates, , opts] = mockUpdateDocument.mock.calls[0];
    expect(updates.blockchain.status).toBe('anchor_failed');
    expect(updates.blockchain.txHash).toBeNull();
    expect(updates.blockchain.error).toContain('All inputs are spent');
    expect(updates.blockchain.anchorId).toBe('anchor_1');
    // The accept-time optimistic 'anchored' is reverted (no signatures → draft).
    expect(updates.status).toBe('draft');
    expect(opts).toEqual({ preserveTerminalStatuses: true });
    // Two observations were required before concluding.
    expect(mockFetch.mock.calls.length).toBeGreaterThanOrEqual(2);
  });

  it('reverts to signed when the document carries signatures', async () => {
    mockGetDocument.mockResolvedValue(baseDoc({
      signatures: [{ signerId: 's', walletAddress: 'addr', signature: 'sig', signedAt: 'now' }],
    }));
    mockFetch.mockResolvedValue(anchorResponse({ status: 'failed', errorMessage: 'boom' }));

    await pollAnchorUntilConfirmed({
      anchorId: 'anchor_1', documentId: 'doc-ks535', tenantId: 'tenant-1',
      authHeader: 'Bearer t', intervalMs: 1, maxAttempts: 10,
    });

    expect(mockUpdateDocument.mock.calls[0][2].status).toBe('signed');
  });

  it('does NOT conclude failure from a single observation followed by recovery', async () => {
    mockFetch
      .mockResolvedValueOnce(anchorResponse({ status: 'failed', errorMessage: 'transient' }))
      .mockResolvedValue(anchorResponse({ status: 'confirmed', verified: true, transactionHash: REAL_TX, blockNumber: 123 }));

    await pollAnchorUntilConfirmed({
      anchorId: 'anchor_1', documentId: 'doc-ks535', tenantId: 'tenant-1',
      authHeader: 'Bearer t', intervalMs: 1, maxAttempts: 10,
    });

    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
    const [, , updates] = mockUpdateDocument.mock.calls[0];
    expect(updates.blockchain.status).toBe('confirmed');
    expect(updates.blockchain.txHash).toBe(REAL_TX);
    expect(updates.status).toBe('anchored');
    expect(JSON.stringify(mockUpdateDocument.mock.calls)).not.toContain('anchor_failed');
  });

  it('still exits quietly when the poll window closes without resolution', async () => {
    mockFetch.mockResolvedValue(anchorResponse({ status: 'pending', transactionHash: null }));
    await pollAnchorUntilConfirmed({
      anchorId: 'anchor_1', documentId: 'doc-ks535', tenantId: 'tenant-1',
      authHeader: 'Bearer t', intervalMs: 1, maxAttempts: 3,
    });
    expect(mockUpdateDocument).not.toHaveBeenCalled();
  });
});

describe('markDocumentAnchorFailed — never downgrades recorded chain facts', () => {
  // KS-1004: this cell used to be named "no-ops when the document already
  // carries a real txHash" and its fixture set txHash AND status:'confirmed'
  // TOGETHER — so the `confirmed` arm alone satisfied it and the cell could
  // never detect a change to the txHash arm. It was green over the guard it
  // was named for. The two conditions are now exercised separately.
  it('no-ops when the anchor is confirmed — WITHOUT a txHash, so this isolates the confirmed arm', async () => {
    mockGetDocument.mockResolvedValue(baseDoc({
      blockchain: { txHash: null, blockHeight: 100, status: 'confirmed', anchorId: 'anchor_1' },
    }));
    await markDocumentAnchorFailed('doc-ks535', 'tenant-1', 'anchor_1', 'late failure signal');
    expect(mockUpdateDocument).not.toHaveBeenCalled();
  });

  it('no-ops on a confirmed anchor even when it also carries a txHash (the original fixture)', async () => {
    mockGetDocument.mockResolvedValue(baseDoc({
      blockchain: { txHash: REAL_TX, blockHeight: 100, status: 'confirmed', anchorId: 'anchor_1' },
    }));
    await markDocumentAnchorFailed('doc-ks535', 'tenant-1', 'anchor_1', 'late failure signal');
    expect(mockUpdateDocument).not.toHaveBeenCalled();
  });

  it('no-ops when the document no longer exists', async () => {
    mockGetDocument.mockResolvedValue(null);
    await markDocumentAnchorFailed('doc-ks535', 'tenant-1', 'anchor_1', 'x');
    expect(mockUpdateDocument).not.toHaveBeenCalled();
  });
});

describe('reconcileDocumentAnchorState — read-time self-healing', () => {
  it('heals a stale in-flight document whose anchor terminally failed (the stuck demo shape)', async () => {
    const doc = baseDoc();
    const healed = baseDoc({ status: 'draft', blockchain: { txHash: null, blockHeight: 0, status: 'anchor_failed', anchorId: 'anchor_1' } });
    mockGetDocument.mockResolvedValue(healed);
    mockFetch.mockResolvedValue(anchorResponse({ status: 'failed', errorMessage: 'All inputs are spent', retryCount: 3 }));

    const result = await reconcileDocumentAnchorState(doc, 'tenant-1', 'Bearer t');

    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
    expect(mockUpdateDocument.mock.calls[0][2].blockchain.status).toBe('anchor_failed');
    expect(result.blockchain?.status).toBe('anchor_failed');
  });

  it('heals a stale in-flight document forward to confirmed', async () => {
    mockFetch.mockResolvedValue(anchorResponse({ status: 'confirmed', verified: true, transactionHash: REAL_TX, blockNumber: 42, network: 'preview' }));

    const result = await reconcileDocumentAnchorState(baseDoc(), 'tenant-1', 'Bearer t');

    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
    const [, , updates] = mockUpdateDocument.mock.calls[0];
    expect(updates.blockchain.status).toBe('confirmed');
    expect(updates.blockchain.txHash).toBe(REAL_TX);
    expect(updates.status).toBe('anchored');
    expect(result.blockchain?.txHash).toBe(REAL_TX);
  });

  it('heals a mis-marked anchor_failed document forward when the anchor confirmed', async () => {
    const doc = baseDoc({ status: 'draft', blockchain: { txHash: null, blockHeight: 0, status: 'anchor_failed', anchorId: 'anchor_1' } });
    mockFetch.mockResolvedValue(anchorResponse({ status: 'confirmed', verified: true, transactionHash: REAL_TX, blockNumber: 42 }));

    const result = await reconcileDocumentAnchorState(doc, 'tenant-1', 'Bearer t');

    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
    expect(mockUpdateDocument.mock.calls[0][2].blockchain.status).toBe('confirmed');
    expect(result.blockchain?.status).toBe('confirmed');
  });

  it('leaves a FRESH in-flight document alone (no anchoring call)', async () => {
    const doc = baseDoc({ updatedAt: new Date().toISOString() });
    const result = await reconcileDocumentAnchorState(doc, 'tenant-1', 'Bearer t');
    expect(mockFetch).not.toHaveBeenCalled();
    expect(mockUpdateDocument).not.toHaveBeenCalled();
    expect(result).toBe(doc);
  });

  it('treats an unreadable anchor as no-new-information, never a state change', async () => {
    mockFetch.mockRejectedValue(new Error('anchoring down'));
    const doc = baseDoc();
    const result = await reconcileDocumentAnchorState(doc, 'tenant-1', 'Bearer t');
    expect(mockUpdateDocument).not.toHaveBeenCalled();
    expect(result).toBe(doc);
  });

  it('skips documents with no anchorId, simulated anchors, and resolved states', async () => {
    const noAnchor = baseDoc({ blockchain: { txHash: null, blockHeight: 0, status: 'pending' } });
    const simulated = baseDoc({ blockchain: { txHash: 'tx_sim_abc', blockHeight: 0, simulated: true, anchorId: 'anchor_1' } });
    const confirmed = baseDoc({ blockchain: { txHash: REAL_TX, blockHeight: 1, status: 'confirmed', anchorId: 'anchor_1' } });
    for (const doc of [noAnchor, simulated, confirmed]) {
      const result = await reconcileDocumentAnchorState(doc, 'tenant-1', 'Bearer t');
      expect(result).toBe(doc);
    }
    expect(mockFetch).not.toHaveBeenCalled();
    expect(mockUpdateDocument).not.toHaveBeenCalled();
  });
});
