/**
 * =============================================================================
 * ANCHOR STATE SYNC (KS-535)
 * =============================================================================
 * Keeps a document's `blockchain` block truthful against the anchoring
 * service's `anchor_store` — the authoritative record of what actually
 * happened on chain.
 *
 * KS-520 closed the SYNCHRONOUS half of anchor honesty (the anchoring POST
 * itself failing → `blockchain.status: 'anchor_failed'`). This module closes
 * the ASYNCHRONOUS half: the POST was accepted (202) but the Cardano
 * submission later failed terminally. Before KS-535, that failure never
 * propagated — `pollAnchorUntilConfirmed` only wrote when it observed a
 * txHash, so the document kept `status: 'anchored'` forever (reproduced live
 * on demo: 2 of the 10 most recent anchors).
 *
 * Three pieces:
 *
 *  - `pollAnchorUntilConfirmed` — the confirmation poller (extracted from the
 *    create-route closure so the manual retry route POST /:id/anchor can use
 *    it too — that path previously never polled at all, so a retried anchor
 *    could neither gain its txHash nor report a failure). On a terminal
 *    `failed` anchor it now writes the KS-520 fail-closed shape.
 *
 *  - `markDocumentAnchorFailed` — the failure writer. Reverts the accept-time
 *    optimistic `status: 'anchored'` to the honest pre-anchor status and
 *    records the KS-520 `anchor_failed` blockchain block.
 *
 *  - `reconcileDocumentAnchorState` — read-time self-healing for documents
 *    whose poller died (service restart, or the failure landed after the
 *    poller's window — anchoring's retry/backoff chain can outlive it). Runs
 *    on GET /api/documents/:id for stale in-flight anchors, in BOTH
 *    directions: a terminally-failed anchor heals the doc to `anchor_failed`,
 *    and a confirmed anchor heals a stale `pending`/mis-marked
 *    `anchor_failed` doc to the truth.
 *
 * Anchoring-side invariant this relies on (changed together in KS-535):
 * `anchor_store.status = 'failed'` is TERMINAL. During a scheduled retry the
 * row is reset to 'pending' BEFORE the backoff timer starts, so an observed
 * 'failed' means no retry is coming. The poller still double-checks
 * (two consecutive observations) to be safe against the write-gap race.
 * =============================================================================
 */

import { getDocument, updateDocument, DocumentRecord } from '../repositories/documentRepo';
import { logger } from '../utils/logger';
import { simulatedFieldsFromAnchor } from './anchorHonesty';

export function anchoringBaseUrl(): string {
  return process.env.ANCHORING_SERVICE_URL || 'http://anchoring:4005';
}

/** Shape of GET /api/anchors/:id (anchoring/src/index.ts). */
export interface AnchorReadState {
  status?: string;
  transactionHash?: string | null;
  transactionId?: string | null;
  txHash?: string | null;
  blockNumber?: number | null;
  network?: string;
  anchoredAt?: string | null;
  createdAt?: string | null;
  verified?: boolean;
  errorMessage?: string | null;
  retryCount?: number;
  // KS-587: the anchor READ is honest since PR #659 — a placeholder hash is
  // nulled and re-surfaced as `simulatedTxRef` with `simulated: true`.
  simulated?: boolean;
  simulatedTxRef?: string | null;
}

/**
 * The authoritative tx hash of an anchor read, or null. Rejects the legacy
 * dev-mode placeholder prefixes (`tx_…` / `mock_tx_…`) — a placeholder is
 * not an on-chain transaction (KS-522 honest-labelling family).
 */
export function authoritativeTxHash(anchor: AnchorReadState): string | null {
  const raw = anchor.transactionHash || anchor.txHash || anchor.transactionId;
  if (typeof raw !== 'string' || raw.length === 0) return null;
  if (raw.startsWith('tx_') || raw.startsWith('mock_tx_')) return null;
  return raw;
}

/**
 * Read one anchor from the anchoring service. Returns null on any failure —
 * callers must treat "couldn't read" as "no new information", never as a
 * state change.
 */
/**
 * KS-1074: the blob keys a REBUILD must carry forward, or they are destroyed.
 *
 * `updateDocument` replaces the `blockchain` column wholesale (`documentRepo.ts` builds
 * `{ ...doc, ...updates }`, a TOP-LEVEL spread), so every writer that hands it a fresh object
 * destroys every key it does not restate. KS-1058 fixed one writer — the failure path — and four
 * more rebuild the blob with no `threadToken`, two of them on the SUCCESS path. A document that
 * mints a token at create and then anchors NORMALLY lost the cache dashboards read.
 *
 * Carried EXPLICITLY rather than by spreading `prior`: a blanket spread would also carry
 * `anchoredAt`, which the blob's own contract says is "Absent in the KS-520 fail-closed state —
 * nothing was anchored". That reasoning is KS-1058's and is preserved here.
 *
 * `!= null`, NOT truthiness (the MINOR-2 item on this ticket): `threadToken` is typed `unknown`, so
 * an empty string or 0 would be silently discarded by the very write that exists to stop a value
 * being lost. Theoretical for a real hex token, and exactly what a rewrite reintroduces.
 *
 * `simulatedTxRef` is deliberately NOT carried — the decision this ticket asks for, per writer. The
 * two simulated writers already spread `...simFields`, reconstructed from the anchor being read, so
 * nothing is inherited; and carrying a simulated marker onto a write that has just recorded a REAL
 * confirmed txHash would assert something false.
 */
function carriedForward(prior: Record<string, unknown> | null | undefined): Record<string, unknown> {
  return prior?.threadToken != null ? { threadToken: prior.threadToken } : {};
}

export async function fetchAnchorState(
  anchorId: string,
  authHeader: string,
  timeoutMs = 3_000,
): Promise<AnchorReadState | null> {
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const resp = await fetch(`${anchoringBaseUrl()}/api/anchors/${encodeURIComponent(anchorId)}`, {
        headers: authHeader ? { Authorization: authHeader } : {},
        signal: controller.signal,
      });
      if (!resp.ok) return null;
      const payload: any = await resp.json();
      return (payload.data || payload) as AnchorReadState;
    } finally {
      clearTimeout(timer);
    }
  } catch {
    return null;
  }
}

/**
 * Record a terminal on-chain anchor failure on the document (the KS-520
 * fail-closed shape), reverting the accept-time optimistic `status:
 * 'anchored'` to the honest pre-anchor status.
 *
 * Revert target: `signed` when signatures exist, else `draft`. (A
 * `pending_signature` creation status cannot be reconstructed — the
 * accept-time write already destroyed it — but both revert targets are
 * honest "not anchored" states and the signing flow keys off signing
 * requests, not this field.)
 *
 * No-ops when the anchor is already `confirmed` — never downgrade a recorded
 * success on a late/raced failure signal. `preserveTerminalStatuses` keeps
 * revoked/deleted authoritative.
 *
 * KS-1004: this used to no-op on `txHash` TOO, which made the failure writer
 * unreachable for the population most likely to need it — a transaction that
 * reached the chain and then failed. The guard's stated intent was right
 * ("never downgrade recorded chain facts"), but it was enforced by refusing to
 * WRITE rather than by not DESTROYING: the write nulled `txHash` and zeroed
 * `blockHeight`, so admitting a hashed document would have erased the very
 * facts the guard protected.
 *
 * So the write is now non-destructive — an existing `txHash`, `blockHeight`,
 * `network` and `anchoredAt` are carried forward — and the guard narrows to
 * `confirmed` alone. A failed transaction KEEPS its hash: it is real, it is on
 * chain, and it is the forensic trail for why the anchor failed. Only the
 * status becomes honest.
 *
 * KS-1058: the write REPLACES the blockchain blob (updateDocument spreads
 * shallowly), so anything not restated here is destroyed. `threadToken` is
 * carried forward; `confidence` deliberately is NOT — see the call site.
 */
export async function markDocumentAnchorFailed(
  documentId: string,
  tenantId: string,
  anchorId: string | undefined,
  errorMessage?: string | null,
): Promise<void> {
  const doc = await getDocument(documentId, tenantId);
  if (!doc) return;
  if (doc.blockchain?.status === 'confirmed') return;
  const prior = doc.blockchain as (typeof doc.blockchain & { threadToken?: unknown }) | undefined;
  const revertStatus: DocumentRecord['status'] = doc.signatures?.length ? 'signed' : 'draft';
  await updateDocument(documentId, tenantId, {
    status: revertStatus,
    blockchain: {
      status: 'anchor_failed',
      // KS-1004: carry the chain facts forward rather than nulling them. A tx
      // that failed on chain still has a hash worth keeping; `?? null` / `?? 0`
      // reproduce the previous values exactly for the no-hash case.
      txHash: prior?.txHash ?? null,
      blockHeight: prior?.blockHeight ?? 0,
      ...(prior?.network ? { network: prior.network } : {}),
      // KS-1004: an anchor time is retained only for a transaction that was
      // built and then failed — a no-hash fail-closed blob has none, which is
      // the blob type's own contract (`documentRepo.ts:60-61`).
      ...(prior?.txHash && prior?.anchoredAt ? { anchoredAt: prior.anchoredAt } : {}),
      ...(anchorId ? { anchorId } : {}),
      // KS-1058: `updateDocument` shallow-spreads (`{...doc, ...updates}`),
      // so this object REPLACES the blockchain blob wholesale and every key
      // it does not restate is destroyed. `threadToken` is the one key that
      // matters: it is written at `routes/documents.ts:739` as a cache over
      // `state_thread_registry`, it is unrelated to whether the anchor
      // succeeded, and a mint that already happened is not undone by a failed
      // anchor. Carried explicitly rather than by spreading `prior`, because
      // a blanket spread would also carry `anchoredAt`, which the blob's own
      // contract (`documentRepo.ts:60-61`) says is "Absent in the KS-520
      // fail-closed state — nothing was anchored".
      ...carriedForward(prior as Record<string, unknown> | undefined),
      error: errorMessage || 'anchor failed on chain',
      failedAt: new Date().toISOString(),
    },
  }, undefined, { preserveTerminalStatuses: true });
  logger.warn('Document anchor failed on chain — fail-closed state recorded (KS-535)', {
    documentId,
    anchorId,
    error: errorMessage || undefined,
  });
}

export interface PollAnchorOptions {
  anchorId: string;
  documentId: string;
  tenantId: string;
  authHeader: string;
  /** Test seams — production callers use the defaults. */
  maxAttempts?: number;
  intervalMs?: number;
}

/**
 * Poll the anchor resource until it is confirmed on-chain (writing the real
 * txHash + blockHeight onto the document) OR terminally failed (writing the
 * KS-520 fail-closed shape — the KS-535 fix; previously a failed anchor
 * produced no write at all and the document claimed `anchored` forever).
 */
export async function pollAnchorUntilConfirmed(opts: PollAnchorOptions): Promise<void> {
  const { anchorId, documentId, tenantId, authHeader } = opts;
  const maxAttempts = opts.maxAttempts ?? 60;
  const intervalMs = opts.intervalMs ?? 10_000;
  // KS-535: anchoring resets a retrying row to 'pending' BEFORE its backoff
  // timer starts, so 'failed' is terminal — but the two status writes are not
  // atomic, so require two consecutive observations before concluding.
  let consecutiveFailed = 0;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    await new Promise((r) => setTimeout(r, intervalMs));
    try {
      const anchor = await fetchAnchorState(anchorId, authHeader, Math.min(intervalMs, 5_000));
      if (!anchor) continue;
      const txHash = authoritativeTxHash(anchor);
      const confirmed = anchor.verified === true || anchor.status === 'confirmed';
      if (txHash) {
        // KS-1074: the prior blob is read HERE, per write, not once before the loop. The
        // thread-token mint is fire-and-forget at document create and can land mid-poll, so a
        // blob read earlier would not carry a token that exists by the time this writes.
        const priorBlob = (await getDocument(documentId, tenantId))?.blockchain as Record<string, unknown> | undefined;
        // KS-521: preserveTerminalStatuses — this poll can land minutes after
        // creation and must not stomp a `revoked` set by the owner in between.
        await updateDocument(documentId, tenantId, {
          blockchain: {
            ...carriedForward(priorBlob),
            txHash,
            blockHeight: anchor.blockNumber || 0,
            anchoredAt: anchor.anchoredAt || anchor.createdAt || new Date().toISOString(),
            network: anchor.network,
            status: confirmed ? 'confirmed' : (anchor.status || 'submitted'),
            anchorId,
          },
          status: 'anchored',
        }, undefined, { preserveTerminalStatuses: true });
        if (confirmed) {
          logger.info('Document anchor confirmed on chain', { documentId, txHash, blockHeight: anchor.blockNumber });
          return;
        }
        consecutiveFailed = 0;
        continue;
      }
      if (anchor.status === 'failed') {
        consecutiveFailed += 1;
        if (consecutiveFailed >= 2) {
          await markDocumentAnchorFailed(documentId, tenantId, anchorId, anchor.errorMessage);
          return;
        }
        continue;
      }
      // KS-587 (document-blob leg): a SIMULATED anchor never yields an
      // authoritative txHash, so before this branch the poller wrote nothing
      // for it at all — the document blob stayed `pending` with no `simulated`
      // key, a caller reading only the document could not tell the anchor is
      // not on chain (KS-589 D1), and `presentBlockchainHonestly` had neither
      // of its inputs (KS-589 D4). Write the honest declaration instead:
      // txHash stays null, the placeholder rides in `simulatedTxRef`.
      const simFields = simulatedFieldsFromAnchor(anchor);
      if (simFields.simulated) {
        const priorSimBlob = (await getDocument(documentId, tenantId))?.blockchain as Record<string, unknown> | undefined;
        await updateDocument(documentId, tenantId, {
          blockchain: {
            ...carriedForward(priorSimBlob),
            txHash: null,
            blockHeight: anchor.blockNumber || 0,
            anchoredAt: anchor.anchoredAt || anchor.createdAt || new Date().toISOString(),
            network: anchor.network,
            status: confirmed ? 'confirmed' : (anchor.status || 'submitted'),
            anchorId,
            ...simFields,
          },
          status: 'anchored',
        }, undefined, { preserveTerminalStatuses: true });
        if (confirmed) {
          logger.info('Document anchor settled as SIMULATED — declared on the document blob (KS-587)', { documentId, anchorId });
          return;
        }
        consecutiveFailed = 0;
        continue;
      }
      consecutiveFailed = 0;
    } catch (pollErr: any) {
      logger.warn('Anchor poll failed', { documentId, attempt, error: pollErr?.message });
    }
  }
  logger.warn('Anchor poll exhausted without confirmation', { documentId, anchorId });
}

/**
 * How long an in-flight anchor claim may sit untouched before a read
 * re-checks it against anchor_store. Longer than the poller's 10-minute
 * window, so the reconcile only fires where the poller is provably gone.
 */
const RECONCILE_STALE_MS = parseInt(process.env.ANCHOR_RECONCILE_STALE_MS || `${15 * 60 * 1000}`, 10);

/**
 * Read-time self-healing (KS-535): when serving a document whose anchor
 * outcome is stale/unresolved, re-check anchor_store and persist the truth.
 * Covers the poller-lifetime gap — a restart loses the in-process poller, and
 * anchoring's retry chain can land a terminal failure after the poller's
 * window — in both directions:
 *
 *  - stale in-flight (`pending`/`submitted`, no txHash) + anchor `failed`
 *    → heal to `anchor_failed` (this is the state the two stuck demo
 *    documents are in);
 *  - stale in-flight + anchor confirmed → heal forward to `confirmed`;
 *  - `anchor_failed` + anchor confirmed with a real txHash → heal forward
 *    (covers a mis-marked failure whose retry later succeeded).
 *
 * Returns the refreshed document, or the original when there is nothing to
 * do or the anchoring read fails (no new information ≠ a state change).
 */
export async function reconcileDocumentAnchorState(
  document: DocumentRecord,
  tenantId: string,
  authHeader: string,
): Promise<DocumentRecord> {
  const bc = document.blockchain;
  if (!bc?.anchorId) return document;
  if (bc.simulated) return document;
  // KS-1004: "in flight" means NOT YET TERMINAL — it must not also require the
  // absence of a txHash. The poller writes the hash together with the
  // optimistic `status: 'anchored'` as soon as the node reports one, well
  // before confirmation, so keying off the hash excluded every `submitted`
  // document from the failure branch below: exactly the rows whose anchors are
  // most likely to end `failed`. `confirmed` and `anchor_failed` are the two
  // terminal states, and they are the whole condition.
  const inFlight = bc.status !== 'anchor_failed' && bc.status !== 'confirmed';
  const failed = bc.status === 'anchor_failed';
  if (!inFlight && !failed) return document;

  const updatedAtMs = Date.parse(document.updatedAt || '');
  if (Number.isFinite(updatedAtMs) && Date.now() - updatedAtMs < RECONCILE_STALE_MS) return document;

  const anchor = await fetchAnchorState(bc.anchorId, authHeader);
  if (!anchor) return document;

  const txHash = authoritativeTxHash(anchor);
  const confirmed = anchor.verified === true || anchor.status === 'confirmed';

  if (confirmed && txHash) {
    const refreshed = await updateDocument(document.id, tenantId, {
      blockchain: {
        // KS-1074: `bc` is this document's prior blob, already in scope — no extra read needed.
        ...carriedForward(bc as unknown as Record<string, unknown>),
        txHash,
        blockHeight: anchor.blockNumber || 0,
        anchoredAt: anchor.anchoredAt || anchor.createdAt || new Date().toISOString(),
        network: anchor.network,
        status: 'confirmed',
        anchorId: bc.anchorId,
      },
      status: 'anchored',
    }, undefined, { preserveTerminalStatuses: true });
    logger.info('Stale anchor state healed to confirmed on read (KS-535)', { documentId: document.id, anchorId: bc.anchorId, txHash });
    return refreshed || document;
  }

  if (inFlight && anchor.status === 'failed') {
    await markDocumentAnchorFailed(document.id, tenantId, bc.anchorId, anchor.errorMessage);
    const refreshed = await getDocument(document.id, tenantId);
    return refreshed || document;
  }

  // KS-587 (document-blob leg): heal a stale in-flight blob whose anchor is
  // SIMULATED — the poller historically wrote nothing for those (no
  // authoritative txHash), so pre-fix documents sit `pending` forever with no
  // `simulated` key. Once healed, the `bc.simulated` early-return above stops
  // this document from re-reconciling on every read.
  //
  // KS-1004: `!bc.txHash` is stated explicitly here now. It used to be implied
  // by `inFlight`, and widening that condition would otherwise have exposed
  // this branch — which writes `txHash: null` — to documents carrying a real
  // hash. This leg is for blobs with NO authoritative txHash, exactly as the
  // comment above says, so the guard belongs in the condition rather than
  // inherited from one that no longer carries it. Behaviour is byte-identical
  // to before KS-1004 for every document this branch was ever meant to reach.
  const simFields = simulatedFieldsFromAnchor(anchor);
  if (inFlight && !bc.txHash && simFields.simulated) {
    const refreshed = await updateDocument(document.id, tenantId, {
      blockchain: {
        ...carriedForward(bc as unknown as Record<string, unknown>),
        txHash: null,
        blockHeight: anchor.blockNumber || 0,
        anchoredAt: anchor.anchoredAt || anchor.createdAt || new Date().toISOString(),
        network: anchor.network,
        status: confirmed ? 'confirmed' : (anchor.status || 'submitted'),
        anchorId: bc.anchorId,
        ...simFields,
      },
      status: 'anchored',
    }, undefined, { preserveTerminalStatuses: true });
    logger.info('Stale anchor state healed to declared-simulated on read (KS-587)', { documentId: document.id, anchorId: bc.anchorId });
    return refreshed || document;
  }

  return document;
}
