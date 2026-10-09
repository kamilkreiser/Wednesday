/**
 * KS-1004 — a document carrying a txHash could never be marked anchor-failed.
 *
 * Two independent locks in anchorStateSync.ts both keyed off "does a txHash
 * exist", so once one was written the failure writer became unreachable and the
 * document stayed `status: 'anchored'` for a transaction that failed on chain:
 *
 *   :284  const inFlight = !bc.txHash && bc.status !== 'anchor_failed' && ...
 *   :313  if (inFlight && anchor.status === 'failed') markDocumentAnchorFailed(...)
 *   :136  markDocumentAnchorFailed: if (doc.blockchain?.txHash || ...) return;
 *
 * And the poller writes the hash TOGETHER with the optimistic `anchored`
 * status as soon as the node reports one — well before confirmation — so every
 * `submitted` document was excluded. Those are precisely the rows whose anchors
 * are most likely to end `failed`.
 *
 * ⚠ THE OLD GUARD'S INTENT WAS RIGHT AND IS PRESERVED. Its comment said "never
 * downgrade recorded chain facts on a late/raced failure signal" — true, and it
 * mattered, because the write nulled `txHash` and zeroed `blockHeight`. The fix
 * is NOT to delete the protection: it is to stop the write being destructive
 * (the hash is carried forward) so the guard no longer has to refuse in order
 * to protect it. `confirmed` still refuses, and that is now its whole job.
 *
 * A failed transaction KEEPS its hash. It is real, it is on chain, and it is
 * the forensic trail for why the anchor failed. Only the status becomes honest.
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

import { markDocumentAnchorFailed, reconcileDocumentAnchorState } from '../services/anchorStateSync';
import type { DocumentRecord } from '../repositories/documentRepo';

const REAL_TX = '4f1e6a8d2c7b9e3f1a5b7c9d2e4f6a8b1c3d5e7f9a2b4c6d8e0f2a4b6c8d0e2f';

function baseDoc(overrides: Partial<DocumentRecord> = {}): DocumentRecord {
  return {
    id: 'doc-ks1004',
    type: 'general',
    status: 'anchored',
    owner: { id: 'user-1' },
    data: {},
    contentHash: 'a'.repeat(64),
    signatures: [],
    blockchain: { txHash: null, blockHeight: 0, status: 'pending', anchorId: 'anchor_1' },
    createdAt: '2026-01-01T00:00:00.000Z',
    updatedAt: '2026-01-01T00:00:00.000Z', // long stale — passes the reconcile threshold
    ...overrides,
  } as DocumentRecord;
}

/** The shape the poller leaves behind once the node reports a hash: a real
 *  txHash, `submitted` (NOT confirmed), and the optimistic doc status. */
function submittedWithHash(): DocumentRecord {
  return baseDoc({
    status: 'anchored',
    blockchain: { txHash: REAL_TX, blockHeight: 0, status: 'submitted', anchorId: 'anchor_1' },
  } as Partial<DocumentRecord>);
}

function anchorResponse(body: unknown, ok = true): Response {
  return { ok, json: async () => body } as unknown as Response;
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

describe('KS-1004 — markDocumentAnchorFailed reaches a hashed document', () => {
  it('REPRO: records the failure on a submitted document carrying a txHash (was: inert)', async () => {
    mockGetDocument.mockResolvedValue(submittedWithHash());

    await markDocumentAnchorFailed('doc-ks1004', 'tenant-1', 'anchor_1', 'ConwayMempoolFailure "All inputs are spent"');

    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
    const [, , updates, , opts] = mockUpdateDocument.mock.calls[0];
    expect(updates.blockchain.status).toBe('anchor_failed');
    expect(updates.blockchain.error).toContain('All inputs are spent');
    expect(updates.status).toBe('draft');
    expect(opts).toEqual({ preserveTerminalStatuses: true });
  });

  it('the txHash is CARRIED FORWARD, not nulled — the failed tx keeps its forensic trail', async () => {
    mockGetDocument.mockResolvedValue(baseDoc({
      blockchain: {
        txHash: REAL_TX, blockHeight: 4242, status: 'submitted',
        anchorId: 'anchor_1', network: 'preview', anchoredAt: '2026-02-02T00:00:00.000Z',
      },
    } as Partial<DocumentRecord>));

    await markDocumentAnchorFailed('doc-ks1004', 'tenant-1', 'anchor_1', 'failed on chain');

    const [, , updates] = mockUpdateDocument.mock.calls[0];
    // This is the assertion the whole non-destructive design exists for.
    expect(updates.blockchain.txHash).toBe(REAL_TX);
    expect(updates.blockchain.blockHeight).toBe(4242);
    expect(updates.blockchain.network).toBe('preview');
    expect(updates.blockchain.anchoredAt).toBe('2026-02-02T00:00:00.000Z');
  });

  it('CONTROL: a confirmed anchor is still refused — the guard kept its real job', async () => {
    mockGetDocument.mockResolvedValue(baseDoc({
      blockchain: { txHash: REAL_TX, blockHeight: 100, status: 'confirmed', anchorId: 'anchor_1' },
    }));
    await markDocumentAnchorFailed('doc-ks1004', 'tenant-1', 'anchor_1', 'late failure signal');
    expect(mockUpdateDocument).not.toHaveBeenCalled();
  });

  it('CONTROL: a document with NO txHash still writes null/0, exactly as before', async () => {
    mockGetDocument.mockResolvedValue(baseDoc());
    await markDocumentAnchorFailed('doc-ks1004', 'tenant-1', 'anchor_1', 'boom');
    const [, , updates] = mockUpdateDocument.mock.calls[0];
    expect(updates.blockchain.txHash).toBeNull();
    expect(updates.blockchain.blockHeight).toBe(0);
  });

  it('CONTRACT: a NO-txHash prior carrying anchoredAt does NOT keep it — an anchor time is retained only alongside a hash', async () => {
    // The blob type's own contract (`documentRepo.ts:60-61`): `anchoredAt` is
    // absent in the fail-closed state where nothing was anchored. The carry
    // is for a transaction that was BUILT and then failed, so it is keyed on
    // the hash — with no hash there is nothing whose anchor time could be
    // kept. (`ks1058-anchor-failed-preserves-thread-token.test.ts` pins the
    // same fact from the other side.)
    mockGetDocument.mockResolvedValue(baseDoc({
      blockchain: {
        txHash: null, blockHeight: 0, status: 'pending', anchorId: 'anchor_1',
        anchoredAt: '2026-02-02T00:00:00.000Z',
      },
    } as Partial<DocumentRecord>));
    await markDocumentAnchorFailed('doc-ks1004', 'tenant-1', 'anchor_1', 'boom');
    const [, , updates] = mockUpdateDocument.mock.calls[0];
    expect('anchoredAt' in updates.blockchain).toBe(false);
    // and the write still happened, fail-closed shape intact
    expect(updates.blockchain.status).toBe('anchor_failed');
    expect(updates.blockchain.txHash).toBeNull();
  });
});

describe('KS-1004 — reconcileDocumentAnchorState heals a hashed, failed document', () => {
  it('REPRO: a stale submitted-with-hash document whose anchor failed is healed to anchor_failed', async () => {
    mockGetDocument.mockResolvedValue(submittedWithHash());
    mockFetch.mockResolvedValue(anchorResponse({
      status: 'failed', transactionHash: REAL_TX, errorMessage: 'All inputs are spent',
    }));

    await reconcileDocumentAnchorState(submittedWithHash(), 'tenant-1', 'Bearer t');

    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
    const [, , updates] = mockUpdateDocument.mock.calls[0];
    expect(updates.blockchain.status).toBe('anchor_failed');
    expect(updates.blockchain.txHash).toBe(REAL_TX);
  });

  // ⚠ RELABELLED after the red-proof. This began as a CONTROL — "the fix must
  // not turn a forward heal into a failure" — and the tamper reddened it, which
  // a true control should not do. Reading why was the useful part: under the
  // old `inFlight` a hashed document failed BOTH `inFlight` and `failed`, so
  // `if (!inFlight && !failed) return document` fired and it reconciled in
  // NEITHER direction. So this is a SECOND REPRO, not a control: the lockout
  // also blocked healing forward to confirmed, which the ticket does not say.
  // Kept, honestly named. The genuine controls are the two below and the two
  // in the block above, and those stayed green under the tamper.
  it('REPRO 2: a hashed document could not heal FORWARD either — confirmed now lands', async () => {
    const doc = submittedWithHash();
    mockGetDocument.mockResolvedValue(doc);
    mockFetch.mockResolvedValue(anchorResponse({
      status: 'confirmed', verified: true, transactionHash: REAL_TX, blockNumber: 99,
    }));

    await reconcileDocumentAnchorState(doc, 'tenant-1', 'Bearer t');

    const [, , updates] = mockUpdateDocument.mock.calls[0];
    expect(updates.blockchain.status).toBe('confirmed');
    expect(updates.status).toBe('anchored');
    expect(JSON.stringify(mockUpdateDocument.mock.calls)).not.toContain('anchor_failed');
  });

  it('CONTROL: an already anchor_failed document is not re-written by the failure branch', async () => {
    const doc = baseDoc({
      blockchain: { txHash: REAL_TX, blockHeight: 0, status: 'anchor_failed', anchorId: 'anchor_1' },
    });
    mockGetDocument.mockResolvedValue(doc);
    mockFetch.mockResolvedValue(anchorResponse({ status: 'failed', errorMessage: 'still failed' }));

    await reconcileDocumentAnchorState(doc, 'tenant-1', 'Bearer t');

    // `failed` gets past the early return so it can heal FORWARD, but the
    // failure branch requires inFlight, which anchor_failed is not.
    expect(mockUpdateDocument).not.toHaveBeenCalled();
  });

  it('CONTROL: the KS-587 simulated-heal leg still requires NO txHash', async () => {
    // Widening `inFlight` would otherwise have exposed that branch — which
    // writes txHash: null — to a document carrying a real hash.
    const doc = submittedWithHash();
    mockGetDocument.mockResolvedValue(doc);
    mockFetch.mockResolvedValue(anchorResponse({
      status: 'submitted', simulated: true, transactionHash: `mock_tx_${'a'.repeat(8)}`,
    }));

    await reconcileDocumentAnchorState(doc, 'tenant-1', 'Bearer t');

    // No write at all: not confirmed, not failed, and the sim leg is bounded.
    expect(mockUpdateDocument).not.toHaveBeenCalled();
  });
});
