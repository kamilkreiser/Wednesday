/**
 * KS-1058 — `markDocumentAnchorFailed` REPLACES the blockchain blob, so every
 * key it does not restate is destroyed.
 *
 * `updateDocument` shallow-spreads (`documentRepo.ts:540-544`, `{...doc, ...updates}`),
 * so the object this writer builds does not merge into the prior blob — it
 * becomes it. The QA gate raised this as F4 naming two lost keys, `threadToken`
 * and `confidence`. **They are not the same case, and only one of them is a
 * defect.** This file pins both, and pins the difference.
 *
 * ---------------------------------------------------------------------------
 * `threadToken` — a real erasure, and the reason it is worth fixing is NOT the
 * one the ticket gives.
 *
 * It is written at `routes/documents.ts:739` as an explicit cache over
 * `state_thread_registry` ("The canonical truth is state_thread_registry; this
 * is a cache"). The ticket says that makes it "recoverable rather than
 * destructive — worth confirming". Confirmed, and it is stronger than
 * recoverable: **the blob copy is WRITE-ONLY.**
 *
 *   `blockchain.threadToken` readers, whole repo            -> 0
 *     (control: `blockchain.txHash` readers                 -> 21)
 *   `threadToken` in any frontend                           -> 0
 *     (control: `txHash` in frontends                       -> 53)
 *
 * and anchoring serves the same fact from the canonical table independently
 * (`services/anchoring/src/index.ts:1001`, `FROM state_thread_registry`). So
 * nothing observable breaks today. It is fixed here because the erasure is
 * ACCIDENTAL — a minted thread token is not undone by a failed anchor, and the
 * write that records it was deliberate — not because a consumer is suffering.
 * Anyone citing this fix as user-visible would be overstating it.
 *
 * ---------------------------------------------------------------------------
 * `confidence` — NOT preserved, deliberately, and preserving it would be a BUG.
 *
 * Two independent reasons, either sufficient:
 *
 *  1. **It cannot reach this writer.** The only producer of
 *     `confidence: 'pending-onchain'` on a document blob is the dev-mode
 *     fallback at `routes/documents.ts:1339-1344`, and that branch sets NO
 *     `anchorId` (the success branch sets `anchorId` and no `confidence` — the
 *     two are mutually exclusive). `pollAnchorUntilConfirmed` is only started
 *     `if (blockchainData.anchorId)`, and `reconcileDocumentAnchorState`
 *     early-returns on `if (!bc?.anchorId)`. Both routes into this function
 *     therefore require an `anchorId` that a `confidence`-bearing blob never has.
 *
 *  2. **If it did reach it, carrying it forward would re-report a terminal
 *     failure as still pending.** The gateway reads `blockchain.confidence`
 *     back (`api-gateway/src/routes/verification.ts`) as its `pending-onchain`
 *     fallback. A blob that is `anchor_failed` AND carries
 *     `confidence: 'pending-onchain'` makes the public verify endpoint answer
 *     `pending-onchain` for an anchor that terminally failed — which is the
 *     same class of unearned claim KS-1057 has just removed, one field over.
 *
 * So the fix carries `threadToken` EXPLICITLY rather than spreading the prior
 * blob, which is what the ticket's suggested shape proposes. A blanket spread
 * would carry `confidence` (above) and `anchoredAt`, and `anchoredAt` is
 * documented on the blob type itself as "Absent in the KS-520 fail-closed
 * state — nothing was anchored, so there is no anchor time to record"
 * (`documentRepo.ts:60-61`). Cells 2 and 3 exist to stop a future blanket
 * spread reintroducing both.
 *
 * ---------------------------------------------------------------------------
 * BASE. This is written against `develop`, where this writer has NO carry-list
 * at all. The ticket's suggested shape describes #912's version of the function
 * ("smaller diff than the current explicit-carry list"), which is not on
 * develop. #912 edits the same object literal, so a textual conflict there is
 * expected and trivial: keep both its chain-fact carries and this threadToken
 * line.
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

import { markDocumentAnchorFailed } from '../services/anchorStateSync';
import type { DocumentRecord } from '../repositories/documentRepo';

const THREAD_TOKEN = {
  policyId: 'b'.repeat(56),
  scriptAddress: 'addr_test1wq_ks1058',
  mintTxHash: 'c'.repeat(64),
  network: 'preview',
};

function docWithBlob(blockchain: Record<string, unknown>): DocumentRecord {
  return {
    id: 'doc-ks1058',
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

/** Run the writer over a prior blob and return the blob it wrote. */
async function writtenBlobFor(prior: Record<string, unknown>): Promise<Record<string, any>> {
  mockGetDocument.mockResolvedValueOnce(docWithBlob(prior));
  mockUpdateDocument.mockResolvedValueOnce(undefined);
  await markDocumentAnchorFailed('doc-ks1058', 'tenant-1', 'anchor_1', 'boom');
  expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
  return (mockUpdateDocument.mock.calls[0][2] as any).blockchain;
}

beforeEach(() => {
  mockGetDocument.mockReset();
  mockUpdateDocument.mockReset();
});

describe('KS-1058 — the fail-closed write must not destroy an unrelated minted fact', () => {
  it('DEFECT: a prior threadToken survives the anchor_failed write', async () => {
    const blob = await writtenBlobFor({
      txHash: null, blockHeight: 0, status: 'pending', anchorId: 'anchor_1',
      threadToken: THREAD_TOKEN,
    });
    expect(blob.threadToken).toEqual(THREAD_TOKEN);
    // and the fail-closed shape is still intact around it
    expect(blob.status).toBe('anchor_failed');
    expect(blob.txHash).toBeNull();
    expect(blob.blockHeight).toBe(0);
  });

  it('CONTRACT: anchoredAt is NOT carried forward — the blob type says it is absent here', async () => {
    // documentRepo.ts:60-61 — "Absent in the KS-520 fail-closed state — nothing
    // was anchored, so there is no anchor time to record." A blanket spread of
    // the prior blob would violate that; this cell is what stops one landing.
    const blob = await writtenBlobFor({
      txHash: null, blockHeight: 0, status: 'pending', anchorId: 'anchor_1',
      anchoredAt: '2026-01-01T00:00:00.000Z',
    });
    expect(blob.anchoredAt).toBeUndefined();
  });

  it('DELIBERATE: confidence is NOT carried forward — it would report a terminal failure as pending', async () => {
    // See the header. The gateway reads blockchain.confidence back as its
    // `pending-onchain` fallback, so carrying it onto an anchor_failed blob
    // would make the public verify endpoint answer `pending-onchain` for an
    // anchor that terminally failed. This cell pins the decision, not an
    // accident — if a future change starts carrying it, this must go red.
    const blob = await writtenBlobFor({
      txHash: null, blockHeight: 0, status: 'pending', anchorId: 'anchor_1',
      confidence: 'pending-onchain',
    });
    expect(blob.confidence).toBeUndefined();
  });

  it('CONTROL: with no threadToken in the prior blob the written shape is unchanged', async () => {
    const blob = await writtenBlobFor({
      txHash: null, blockHeight: 0, status: 'pending', anchorId: 'anchor_1',
    });
    expect(Object.keys(blob).sort()).toEqual(
      ['anchorId', 'blockHeight', 'error', 'failedAt', 'status', 'txHash'].sort(),
    );
    expect('threadToken' in blob).toBe(false);
  });

  it('CONTROL (non-zero): the writer still records the failure it is for', async () => {
    // Without this, every assertion above is satisfied by a writer that has
    // stopped writing anything at all.
    const blob = await writtenBlobFor({
      txHash: null, blockHeight: 0, status: 'pending', anchorId: 'anchor_1',
      threadToken: THREAD_TOKEN,
    });
    expect(blob.status).toBe('anchor_failed');
    expect(blob.error).toBe('boom');
    expect(typeof blob.failedAt).toBe('string');
    expect(blob.anchorId).toBe('anchor_1');
  });

  it('UNION with KS-1004: a hashed prior IS written — status anchor_failed, txHash and blockHeight carried, threadToken preserved', async () => {
    // KS-1004 (#912) narrowed the guard to `confirmed` alone, so a document
    // carrying a real txHash is now written — the ks1004 suite's REPRO and
    // "confirmed is still refused" cells and the split ks535 cells pin the
    // guard itself. What THIS file pins is that the write keeps what it
    // found: the chain facts are carried and the thread token survives, for
    // the hashed population exactly as for the no-hash one above.
    const blob = await writtenBlobFor({
      txHash: 'd'.repeat(64), blockHeight: 42, status: 'submitted', threadToken: THREAD_TOKEN,
    });
    expect(blob.status).toBe('anchor_failed');
    expect(blob.txHash).toBe('d'.repeat(64));
    expect(blob.blockHeight).toBe(42);
    expect(blob.threadToken).toEqual(THREAD_TOKEN);
  });
});
