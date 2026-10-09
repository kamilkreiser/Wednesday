/**
 * =============================================================================
 * KS-587 (document-blob leg) — the document's `blockchain` blob must DECLARE
 * a simulated anchor, on every writer and at the serve boundary.
 * =============================================================================
 * Peter's KS-589 D1/D4 findings: originate never wrote `simulated` onto the
 * document blob outside the explicit SIMULATE_ANCHORING branch, so
 *   - a caller reading only the document could not tell a mock anchor is not
 *     on chain (D1 — the blob for a settled mock anchor read
 *     `{'anchored': True, 'status': 'pending', 'txHash': None, …}`), and
 *   - `presentBlockchainHonestly` (verification.ts) had neither of its two
 *     inputs (`simulated` absent = D1; txHash null since KS-522), so the
 *     verifier-side protection never fired (D4).
 *
 * Fix mapped on the ticket (Kam, KS-587 comment 2026-08-12): propagate the
 * anchor's `simulated` through the three document-blob writers (create-path
 * `initial`, manual-anchor `blockchainData`, the anchorStateSync poll — which
 * previously never wrote for placeholder-tx anchors at all) + present the
 * composed blob honestly at the GET read.
 *
 * This file pins:
 *   1. the pure derivation/composition helpers (services/anchorHonesty.ts);
 *   2. `pollAnchorUntilConfirmed` writing the declared-simulated blob for a
 *      simulated anchor read (RED before the fix: no write at all);
 *   3. `reconcileDocumentAnchorState` healing a stale pre-fix document to the
 *      declared-simulated shape (RED before the fix: returned unchanged).
 * The GET-read composition itself is exercised live (local stack) and pinned
 * continuously by systemTest's KS-589 D1/D4 tests once their xfail markers
 * come off.
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
  FABRICATED_TX_PREFIX,
  composeHonestBlockchainBlob,
  isSimulatedAnchor,
  simulatedFieldsFromAnchor,
} from '../services/anchorHonesty';
import { pollAnchorUntilConfirmed, reconcileDocumentAnchorState } from '../services/anchorStateSync';
import type { DocumentRecord } from '../repositories/documentRepo';

const REAL_TX = '4f1e6a8d2c7b9e3f1a5b7c9d2e4f6a8b1c3d5e7f9a2b4c6d8e0f2a4b6c8d0e2f';
const MOCK_TX = `mock_tx_${'a'.repeat(64)}`;

function baseDoc(overrides: Partial<DocumentRecord> = {}): DocumentRecord {
  return {
    id: 'doc-ks587-d1',
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
  return { ok, json: async () => body } as unknown as Response;
}

/** The honest anchor READ shape for a settled mock anchor (post-KS-587 #659). */
function simulatedAnchorRead(over: Record<string, unknown> = {}) {
  return {
    status: 'confirmed',
    transactionHash: null,
    simulated: true,
    simulatedTxRef: MOCK_TX,
    blockNumber: 0,
    network: 'devnet',
    verified: false,
    ...over,
  };
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

describe('simulatedFieldsFromAnchor — deriving the declaration from an anchoring payload', () => {
  it('carries an honest post-KS-587 payload through (flag + ref)', () => {
    expect(simulatedFieldsFromAnchor(simulatedAnchorRead())).toEqual({ simulated: true, simulatedTxRef: MOCK_TX });
  });

  it('derives from a raw placeholder hash when the flag is absent (older anchoring image / SIMULATE_ANCHORING synthesis)', () => {
    expect(simulatedFieldsFromAnchor({ txHash: MOCK_TX })).toEqual({ simulated: true, simulatedTxRef: MOCK_TX });
    expect(simulatedFieldsFromAnchor({ transactionId: `tx_sim_${'b'.repeat(8)}` })).toEqual({
      simulated: true,
      simulatedTxRef: `tx_sim_${'b'.repeat(8)}`,
    });
  });

  it('returns empty for a real anchor and for empty input — spreadable unconditionally', () => {
    expect(simulatedFieldsFromAnchor({ transactionHash: REAL_TX })).toEqual({});
    expect(simulatedFieldsFromAnchor({ txHash: null })).toEqual({});
    expect(simulatedFieldsFromAnchor(null)).toEqual({});
    expect(simulatedFieldsFromAnchor(undefined)).toEqual({});
  });

  it('declares simulated even when only the flag is present (no ref available)', () => {
    expect(simulatedFieldsFromAnchor({ simulated: true, transactionHash: null })).toEqual({ simulated: true });
  });
});

describe('composeHonestBlockchainBlob — the KS-522 rules at the serve boundary', () => {
  it('nulls a stored placeholder txHash and declares it (the SIMULATE_ANCHORING stored shape)', () => {
    const stored = { txHash: `tx_sim_${'c'.repeat(64)}`, blockHeight: 0, anchoredAt: 'x', simulated: true };
    const out = composeHonestBlockchainBlob(stored)!;
    expect(out.txHash).toBeNull();
    expect(out.simulated).toBe(true);
    expect(out.simulatedTxRef).toBe(`tx_sim_${'c'.repeat(64)}`);
  });

  it('declares a placeholder even when the stored flag lies (the KS-587 incident shape)', () => {
    const out = composeHonestBlockchainBlob({ txHash: MOCK_TX, status: 'confirmed' })!;
    expect(out.txHash).toBeNull();
    expect(out.simulated).toBe(true);
    expect(out.simulatedTxRef).toBe(MOCK_TX);
  });

  it('returns real anchors, fail-closed states and absent blobs untouched (same reference)', () => {
    const real = { txHash: REAL_TX, status: 'confirmed' };
    expect(composeHonestBlockchainBlob(real)).toBe(real);
    const failed = { txHash: null, status: 'anchor_failed', error: 'x' };
    expect(composeHonestBlockchainBlob(failed)).toBe(failed);
    expect(composeHonestBlockchainBlob(null)).toBeNull();
    expect(composeHonestBlockchainBlob(undefined)).toBeUndefined();
  });

  it('preserves an already-declared blob without inventing a ref', () => {
    const declared = { txHash: null, simulated: true, status: 'confirmed' };
    const out = composeHonestBlockchainBlob(declared)!;
    expect(out.simulated).toBe(true);
    expect(out.txHash).toBeNull();
    expect(out.simulatedTxRef).toBeUndefined();
  });

  it('shares one prefix rule with isSimulatedAnchor', () => {
    for (const p of ['tx_sim_x', 'mock_tx_x', 'tx_x']) {
      expect(FABRICATED_TX_PREFIX.test(p)).toBe(true);
      expect(isSimulatedAnchor(p)).toBe(true);
    }
    expect(isSimulatedAnchor(REAL_TX)).toBe(false);
  });
});

describe('pollAnchorUntilConfirmed — a simulated anchor SETTLES with a declared blob (KS-589 D1)', () => {
  it('writes simulated:true + simulatedTxRef + status confirmed, then stops polling', async () => {
    mockGetDocument.mockResolvedValue(baseDoc());
    mockFetch.mockResolvedValue(anchorResponse(simulatedAnchorRead()));

    await pollAnchorUntilConfirmed({
      anchorId: 'anchor_1', documentId: 'doc-ks587-d1', tenantId: 'tenant-1',
      authHeader: 'Bearer t', intervalMs: 1, maxAttempts: 10,
    });

    // RED before the fix: authoritativeTxHash rejects the placeholder, no
    // branch matched, and the poller wrote NOTHING for the anchor's entire
    // life — the blob stayed `pending` with no `simulated` key.
    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
    const [, , updates, , opts] = mockUpdateDocument.mock.calls[0];
    expect(updates.blockchain.simulated).toBe(true);
    expect(updates.blockchain.simulatedTxRef).toBe(MOCK_TX);
    expect(updates.blockchain.txHash).toBeNull();
    expect(updates.blockchain.status).toBe('confirmed');
    expect(updates.blockchain.anchorId).toBe('anchor_1');
    expect(opts).toEqual({ preserveTerminalStatuses: true });
    // Settled — exactly one observation needed.
    expect(mockFetch).toHaveBeenCalledTimes(1);
  });

  it('keeps polling a simulated anchor that has not settled yet (still declares on each write)', async () => {
    mockGetDocument.mockResolvedValue(baseDoc());
    mockFetch
      .mockResolvedValueOnce(anchorResponse(simulatedAnchorRead({ status: 'pending', verified: false })))
      .mockResolvedValueOnce(anchorResponse(simulatedAnchorRead()));

    await pollAnchorUntilConfirmed({
      anchorId: 'anchor_1', documentId: 'doc-ks587-d1', tenantId: 'tenant-1',
      authHeader: 'Bearer t', intervalMs: 1, maxAttempts: 10,
    });

    expect(mockFetch).toHaveBeenCalledTimes(2);
    const writes = mockUpdateDocument.mock.calls.map((c) => c[2].blockchain);
    expect(writes).toHaveLength(2);
    expect(writes.every((b) => b.simulated === true && b.txHash === null)).toBe(true);
    expect(writes[1].status).toBe('confirmed');
  });

  it('a REAL confirmed anchor still writes its txHash with no simulated declaration (regression)', async () => {
    mockGetDocument.mockResolvedValue(baseDoc());
    mockFetch.mockResolvedValue(anchorResponse({
      status: 'confirmed', transactionHash: REAL_TX, blockNumber: 123, network: 'preview', verified: true,
    }));

    await pollAnchorUntilConfirmed({
      anchorId: 'anchor_1', documentId: 'doc-ks587-d1', tenantId: 'tenant-1',
      authHeader: 'Bearer t', intervalMs: 1, maxAttempts: 10,
    });

    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
    const [, , updates] = mockUpdateDocument.mock.calls[0];
    expect(updates.blockchain.txHash).toBe(REAL_TX);
    expect(updates.blockchain.simulated).toBeUndefined();
    expect(updates.blockchain.simulatedTxRef).toBeUndefined();
  });

  it('a FAILED simulated anchor still takes the fail-closed path, not the declared-simulated one', async () => {
    mockGetDocument.mockResolvedValue(baseDoc());
    mockFetch.mockResolvedValue(anchorResponse(simulatedAnchorRead({ status: 'failed', errorMessage: 'boom' })));

    await pollAnchorUntilConfirmed({
      anchorId: 'anchor_1', documentId: 'doc-ks587-d1', tenantId: 'tenant-1',
      authHeader: 'Bearer t', intervalMs: 1, maxAttempts: 10,
    });

    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
    const [, , updates] = mockUpdateDocument.mock.calls[0];
    expect(updates.blockchain.status).toBe('anchor_failed');
  });
});

describe('reconcileDocumentAnchorState — pre-fix documents heal to declared-simulated on read', () => {
  it('heals a stale in-flight blob whose anchor is simulated (RED before the fix: returned unchanged)', async () => {
    const doc = baseDoc();
    mockFetch.mockResolvedValue(anchorResponse(simulatedAnchorRead()));

    const result = await reconcileDocumentAnchorState(doc, 'tenant-1', 'Bearer t');

    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
    const [, , updates, , opts] = mockUpdateDocument.mock.calls[0];
    expect(updates.blockchain.simulated).toBe(true);
    expect(updates.blockchain.simulatedTxRef).toBe(MOCK_TX);
    expect(updates.blockchain.txHash).toBeNull();
    expect(updates.blockchain.status).toBe('confirmed');
    expect(updates.blockchain.anchorId).toBe('anchor_1');
    expect(opts).toEqual({ preserveTerminalStatuses: true });
    expect((result.blockchain as any).simulated).toBe(true);
  });

  it('an already-declared blob does not re-reconcile (no anchoring read at all)', async () => {
    const doc = baseDoc({
      blockchain: { txHash: null, blockHeight: 0, status: 'confirmed', anchorId: 'anchor_1', simulated: true } as any,
    });

    const result = await reconcileDocumentAnchorState(doc, 'tenant-1', 'Bearer t');

    expect(result).toBe(doc);
    expect(mockFetch).not.toHaveBeenCalled();
    expect(mockUpdateDocument).not.toHaveBeenCalled();
  });

  it('a failed simulated anchor still heals to the fail-closed shape, not declared-simulated', async () => {
    mockGetDocument.mockResolvedValue(baseDoc());
    mockFetch.mockResolvedValue(anchorResponse(simulatedAnchorRead({ status: 'failed', errorMessage: 'boom' })));

    await reconcileDocumentAnchorState(baseDoc(), 'tenant-1', 'Bearer t');

    // markDocumentAnchorFailed's write, not the simulated heal.
    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
    const [, , updates] = mockUpdateDocument.mock.calls[0];
    expect(updates.blockchain.status).toBe('anchor_failed');
    expect(updates.blockchain.simulated).toBeUndefined();
  });
});
