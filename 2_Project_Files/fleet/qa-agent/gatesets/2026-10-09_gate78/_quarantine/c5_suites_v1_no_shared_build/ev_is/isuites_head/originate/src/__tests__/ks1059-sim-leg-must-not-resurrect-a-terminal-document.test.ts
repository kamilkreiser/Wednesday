/**
 * KS-1059 — the `inFlight &&` half of the KS-587 sim leg is pinned by nothing.
 *
 * `reconcileDocumentAnchorState`'s sim leg reads:
 *
 *     if (inFlight && !bc.txHash && simFields.simulated) {   // anchorStateSync.ts:378 at 6ab9d5021e96
 *       ... updateDocument(..., { status: 'anchored' })
 *
 * **Established by RUNNING it, not by reading it** — which is the whole content
 * of this ticket. On `develop` at `d4cf7e3cf`, with `inFlight &&` deleted from
 * that line and nothing else changed:
 *
 *     baseline, whole originate suite   2 failed / 513 passed / 515 total
 *     with `inFlight &&` removed        2 failed / 513 passed / 515 total
 *
 * **Byte-identical. Zero cells redden.** (The ticket records a 516-passed
 * baseline from an earlier tree; 513 is today's develop, measured here rather
 * than inherited. The conclusion is the same and does not depend on the total.)
 *
 * A guard whose removal reddens nothing is not a guard. This file makes it one.
 *
 * ---------------------------------------------------------------------------
 * WHAT THE LINE ACTUALLY HOLDS, and why it got MORE load-bearing rather than less.
 *
 * `inFlight` used to imply `!bc.txHash`, so the two halves overlapped and the
 * line looked partly redundant. It is not redundant now — and since `d4cf7e3cf`
 * the `!bc.txHash` term has MOVED OUT of the `inFlight` definition and INTO the
 * sim leg itself, so the two no longer overlap at all. The path at `6ab9d5021e96`:
 *
 *   :329  `const inFlight = bc.status !== 'anchor_failed' && bc.status !== 'confirmed';`
 *   :331  `if (!inFlight && !failed) return document;`
 *           an `anchor_failed` document PASSES here — `failed` is true — so it
 *           reaches everything below.
 *   :342  the heal-forward branch needs `confirmed && txHash`. A simulated
 *           anchor has no authoritative txHash, so it does not fire.
 *   :358  `if (inFlight && anchor.status === 'failed')` — the failure branch.
 *           Does not fire either.
 *   :378  the sim leg. **This `inFlight &&` is the only thing standing between
 *           an `anchor_failed` document and being rewritten to
 *           `status: 'anchored'` with `blockchain.status` reset off its
 *           terminal value.**
 *
 * So without it, a read — just a read — RESURRECTS a document whose anchor
 * terminally failed, and re-presents it as anchored. That is the KS-535 class
 * the fail-closed write exists to prevent, arriving through the healer.
 *
 * `preserveTerminalStatuses` does not save it: that option protects the
 * DOCUMENT's `revoked`/`deleted` statuses, not `blockchain.status`, and the
 * document status being written here is `'anchored'`, not a terminal one.
 *
 * ---------------------------------------------------------------------------
 * WHY NO EXISTING CELL CATCHES IT. Every existing sim-leg case in
 * `ks587-anchors-honest-simulated.test.ts` and `ks535-...` drives a blob that
 * is genuinely in flight (`status: 'pending'`, no hash), where `inFlight` is
 * TRUE and removing the conjunct changes nothing. The uncovered case is the one
 * where `inFlight` is FALSE and `failed` is what let the document through — and
 * that combination existed in no test.
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

import { reconcileDocumentAnchorState } from '../services/anchorStateSync';
import type { DocumentRecord } from '../repositories/documentRepo';

function anchorResponse(body: unknown, ok = true): Response {
  return { ok, json: async () => body } as unknown as Response;
}

const realFetch = global.fetch;
let mockFetch: jest.Mock;

/** Older than RECONCILE_STALE_MS (15 min) so the staleness gate passes. */
const LONG_AGO = new Date(Date.now() - 60 * 60 * 1000).toISOString();

function terminallyFailedDoc(): DocumentRecord {
  return {
    id: 'doc-ks1059',
    type: 'general',
    status: 'draft',           // already reverted by the fail-closed write
    owner: { id: 'user-1' },
    data: {},
    contentHash: 'a'.repeat(64),
    signatures: [],
    blockchain: {
      // The KS-520 fail-closed shape: terminal, no hash, and NOT marked
      // simulated (the `bc.simulated` early-return must not be what saves us —
      // if it were, this cell would pass for the wrong reason).
      txHash: null,
      blockHeight: 0,
      status: 'anchor_failed',
      anchorId: 'anchor_1',
      error: 'ConwayMempoolFailure "All inputs are spent"',
      failedAt: LONG_AGO,
    },
    createdAt: LONG_AGO,
    updatedAt: LONG_AGO,
  } as unknown as DocumentRecord;
}

beforeEach(() => {
  jest.clearAllMocks();
  mockFetch = jest.fn();
  (global as any).fetch = mockFetch;
  mockUpdateDocument.mockImplementation(async (_id, _t, updates) => ({ ...terminallyFailedDoc(), ...updates }));
});

afterAll(() => {
  (global as any).fetch = realFetch;
});

describe('KS-1059 — the sim leg must not resurrect a terminally-failed document', () => {
  it('DEFECT CELL: an anchor_failed document is NOT rewritten to anchored by a simulated anchor', async () => {
    // The anchor reports a fabricated placeholder — simulatedFieldsFromAnchor
    // returns { simulated: true } for a `tx_sim_` prefix — and is not confirmed.
    mockFetch.mockResolvedValue(anchorResponse({
      status: 'pending',
      transactionHash: `tx_sim_${'d'.repeat(32)}`,
      blockNumber: null,
      network: 'preview',
    }));

    const doc = terminallyFailedDoc();
    const out = await reconcileDocumentAnchorState(doc, 'tenant-1', 'Bearer t');

    // Nothing may be written: the document is terminal.
    expect(mockUpdateDocument).not.toHaveBeenCalled();
    // And the returned document keeps its terminal state.
    expect(out.status).toBe('draft');
    expect((out.blockchain as any).status).toBe('anchor_failed');
  });

  it('CONTROL (non-zero): a genuinely in-flight blob with the same simulated anchor IS healed', async () => {
    // Without this, the cell above is satisfied by a reconcile that has stopped
    // writing anything at all — the sim leg has to still work for the case it
    // was written for (KS-587).
    mockFetch.mockResolvedValue(anchorResponse({
      status: 'pending',
      transactionHash: `tx_sim_${'d'.repeat(32)}`,
      blockNumber: null,
      network: 'preview',
    }));

    const doc = terminallyFailedDoc();
    (doc.blockchain as any).status = 'pending';   // in flight, not terminal
    delete (doc.blockchain as any).error;
    delete (doc.blockchain as any).failedAt;

    await reconcileDocumentAnchorState(doc, 'tenant-1', 'Bearer t');

    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
    const updates = mockUpdateDocument.mock.calls[0][2] as any;
    expect(updates.status).toBe('anchored');
    expect(updates.blockchain.simulated).toBe(true);
  });

  it('CONTROL: the terminal document is let THROUGH the early returns — it is the sim leg that stops it', async () => {
    // If an early return were what stopped the write, the defect cell would
    // pass with or without the guard and would be pinning nothing. Proof that
    // execution reaches the anchor read: the fetch is actually made.
    mockFetch.mockResolvedValue(anchorResponse({
      status: 'pending',
      transactionHash: `tx_sim_${'d'.repeat(32)}`,
      blockNumber: null,
      network: 'preview',
    }));

    await reconcileDocumentAnchorState(terminallyFailedDoc(), 'tenant-1', 'Bearer t');

    expect(mockFetch).toHaveBeenCalledTimes(1);
    expect(String(mockFetch.mock.calls[0][0])).toContain('/api/anchors/anchor_1');
  });

  it('CONTROL: a terminal document whose anchor genuinely confirmed IS still healed forward', async () => {
    // The heal-forward branch is deliberately NOT gated on `inFlight` — a
    // mis-marked failure whose retry later succeeded must still be corrected.
    // This cell stops an over-broad "never touch a terminal document" fix.
    mockFetch.mockResolvedValue(anchorResponse({
      status: 'confirmed',
      verified: true,
      transactionHash: 'e'.repeat(64),
      blockNumber: 4242,
      network: 'preview',
    }));

    await reconcileDocumentAnchorState(terminallyFailedDoc(), 'tenant-1', 'Bearer t');

    expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
    const updates = mockUpdateDocument.mock.calls[0][2] as any;
    expect(updates.blockchain.status).toBe('confirmed');
    expect(updates.blockchain.txHash).toBe('e'.repeat(64));
  });
});
