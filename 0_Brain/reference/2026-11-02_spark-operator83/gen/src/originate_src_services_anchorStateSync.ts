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

import { getDocument, writeAnchorBlobIf, DocumentRecord } from '../repositories/documentRepo';
import { logger } from '../utils/logger';
import { simulatedFieldsFromAnchor } from './anchorHonesty';
import { toBlockHeight } from '../utils/blockHeight';
import { authoritativeTxHash, type AnchorReadState } from './anchorRead';
import { resolveAnchorState, createAttemptsOf, type AnchorRowRead, type OwnCreateAnswer } from './anchorResolution';
import { askOwnCreate } from './ownCreateClient';

export function anchoringBaseUrl(): string {
  return process.env.ANCHORING_SERVICE_URL || 'http://anchoring:4005';
}

// KS-1384 R2b: AnchorReadState and authoritativeTxHash live in ./anchorRead (moved verbatim); re-exported here for existing importers.
export { authoritativeTxHash, type AnchorReadState } from './anchorRead';

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
  return {
    ...(prior?.threadToken != null ? { threadToken: prior.threadToken } : {}),
    // KS-1384 R2b (D6): the create attempts are what the resolver binds a row to the create by (anchorResolution.ts
    // isBoundToCreate) and what own-create scans for. Every rebuild writer, the fail-closed one included, must keep them, or
    // the first anchor_failed write would leave the document unbindable for good (no anchoredAt in that state, by KS-1004's
    // contract, and no attempts).
    ...(Array.isArray(prior?.createAttempts) ? { createAttempts: prior.createAttempts } : {}),
  };
}

// =============================================================================
// KS-1384 R2b part 3 (Wednesday's GO on D1-D3, 2026-10-31 13:20:11Z): the three readers below become CALLERS of the one
// resolver (anchorResolution.ts) and write through the conditional blob write (documentRepo writeAnchorBlobIf), where
// `confirmed` is terminal in SQL. Before R2b each decided by its own rule and wrote through updateDocument, which tests no
// blob state: the poller wrote on every poll, markDocumentAnchorFailed relied on a JavaScript `confirmed` check, and the GET
// reconcile failed a document on one `failed` observation of its row, without asking whether its create was on chain.
// =============================================================================

/** The ids an anchor row of THIS document may carry: its external id, and its documentUuid (the primary key when S sent none). */
export function documentIdsOf(doc: DocumentRecord): string[] {
  return [doc.id, doc.documentUuid].filter((x): x is string => typeof x === 'string' && x.length > 0);
}

/**
 * The create attempts own-create binds to (D4, D6): the blob's createAttempts when it records them; for a legacy blob that
 * records none, its anchoredAt and the instants within +-2 ms of it (the resolver's legacy binding rule, anchorResolution.ts
 * isBoundToCreate); none when it has neither, in which case own-create is not asked (askOwnCreate answers not-answered).
 */
export function ownCreateTimestampsOf(blob: Record<string, unknown> | null | undefined): string[] {
  const attempts = createAttemptsOf(blob);
  if (Array.isArray(blob?.createAttempts)) return attempts.map((ms) => new Date(ms).toISOString());
  const at = typeof blob?.anchoredAt === 'string' ? Date.parse(blob.anchoredAt) : NaN;
  if (!Number.isFinite(at)) return [];
  return [-2, -1, 0, 1, 2].map((d) => new Date(at + d).toISOString());
}

/** The lazy own-create question for this document, asked ONLY when the resolver's table needs it. */
function ownCreateFor(doc: DocumentRecord, authHeader: string): () => Promise<OwnCreateAnswer> {
  return () => askOwnCreate(fetch, anchoringBaseUrl(), authHeader, {
    documentId: doc.id,
    contentHash: String(doc.contentHash || '').replace(/^sha256:/i, '').toLowerCase(),
    timestamps: ownCreateTimestampsOf(doc.blockchain as Record<string, unknown> | undefined),
  });
}

/** The blob a resolver `confirmed` decision writes (and the verify heals present): the same shape for every reader. */
function confirmedBlobOf(
  prior: Record<string, unknown> | null | undefined,
  row: AnchorRowRead,
  decision: { tx: string; blockNumber: number | null },
  anchorId: string,
): Record<string, unknown> {
  return {
    ...carriedForward(prior),
    txHash: decision.tx,
    // KS-1509 / KS-1333: an unknown height stays null, never a fabricated 0.
    blockHeight: toBlockHeight(decision.blockNumber ?? row.blockNumber),
    anchoredAt: row.anchoredAt || row.createdAt || new Date().toISOString(),
    network: row.network,
    status: 'confirmed',
    anchorId,
  };
}

/** Write a resolver `confirmed` decision through D2. Returns the matched row count (0: the blob was already confirmed). */
async function writeConfirmed(
  documentId: string,
  tenantId: string,
  prior: Record<string, unknown> | undefined,
  row: AnchorRowRead,
  decision: { tx: string; blockNumber: number | null },
  anchorId: string,
): Promise<number> {
  return writeAnchorBlobIf(documentId, tenantId, 'confirmed', confirmedBlobOf(prior, row, decision, anchorId), { rowStatus: 'anchored' });
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
  // KS-1384 R2b part 3 (D2): through the conditional blob write, not updateDocument. The SQL refuses a `confirmed` blob (the
  // JavaScript check above is only the fast path), and with an anchorId it writes only while the blob still names THAT anchor,
  // so a late failure signal for an older attempt cannot fail a blob a newer one owns. The row status is reverted under the
  // preserveTerminalStatuses CASE inside the write (a revoked or deleted row keeps its status), as before.
  const written = await writeAnchorBlobIf(documentId, tenantId, 'anchor_failed', {
    status: 'anchor_failed',
    // KS-1004: carry the chain facts forward rather than nulling them. A tx
    // that failed on chain still has a hash worth keeping; `?? null` keeps the
    // no-hash case's null. KS-1509: an unknown height stays null as well (the
    // KS-1333 direction), never a fabricated 0; a real prior height is kept.
    txHash: prior?.txHash ?? null,
    blockHeight: prior?.blockHeight ?? null,
    ...(prior?.network ? { network: prior.network } : {}),
    // KS-1004: an anchor time is retained only for a transaction that was
    // built and then failed — a no-hash fail-closed blob has none, which is
    // the blob type's own contract (`documentRepo.ts:60-61`).
    // KS-1158 R1: "has a hash" means an AUTHORITATIVE hash. A dev-mode
    // placeholder (`tx_sim_…`, `mock_tx_…`) is not a transaction
    // (`authoritativeTxHash`, KS-522), so it must not keep a time that
    // implies one was anchored.
    ...(authoritativeTxHash({ txHash: prior?.txHash }) && prior?.anchoredAt ? { anchoredAt: prior.anchoredAt } : {}),
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
  }, { rowStatus: revertStatus, ...(anchorId ? { expectAnchorId: anchorId } : {}) });
  if (written !== 1) {
    logger.warn('Document anchor failure NOT recorded: the blob was confirmed, already failed, or names another anchor (KS-1384 R2b)', { documentId, anchorId, written });
    return;
  }
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
      const anchor = await fetchAnchorState(anchorId, authHeader, Math.min(intervalMs, 5_000)) as AnchorRowRead | null;
      if (!anchor) continue;
      const txHash = authoritativeTxHash(anchor);
      const confirmed = anchor.verified === true || anchor.status === 'confirmed';
      // KS-1384 R2b part 3 (D1, D3): a confirmed row, or a failed one seen twice, is DECIDED by the one resolver, and its
      // decision is written through D2. Before R2b the poller wrote `confirmed` from any row that carried a tx, whatever
      // document or attempt the row's payload was (an event's payload, a reset row's new hash), and failed the document on two
      // `failed` reads without asking whether its create had landed (kintsugi's document, 2026-10-31).
      if ((confirmed && txHash) || anchor.status === 'failed') {
        if (anchor.status === 'failed') {
          consecutiveFailed += 1;
          if (consecutiveFailed < 2) continue;
        }
        const doc = await getDocument(documentId, tenantId);
        if (!doc) return;
        const prior = doc.blockchain as unknown as Record<string, unknown> | undefined;
        const d = await resolveAnchorState({
          blob: prior,
          documentIds: documentIdsOf(doc),
          row: anchor,
          inFlightStale: false, // the poller is the live holder of this attempt: an in-flight row is never stale to it
          ownCreate: ownCreateFor(doc, authHeader),
        });
        if (d.write === 'confirmed') {
          const written = await writeConfirmed(documentId, tenantId, prior, anchor, d, anchorId);
          logger.info('Document anchor confirmed on chain', { documentId, txHash: d.tx, via: d.via, written, blockHeight: anchor.blockNumber });
          return;
        }
        if (d.write === 'anchor_failed') {
          await markDocumentAnchorFailed(documentId, tenantId, anchorId, anchor.errorMessage ?? d.reason);
          return;
        }
        // none: the blob is confirmed already, the row is another document's, or own-create could not answer. Only the
        // last can change on a later poll (own-create caches a not-answered for 60 s, so this is not a scan per poll).
        logger.info('Anchor poll: the resolver wrote nothing (KS-1384 R2b)', { documentId, anchorId, reason: d.reason });
        if (prior?.status === 'confirmed') return;
        continue;
      }
      if (txHash) {
        // KS-1074: the prior blob is read HERE, per write, not once before the loop. The
        // thread-token mint is fire-and-forget at document create and can land mid-poll, so a
        // blob read earlier would not carry a token that exists by the time this writes.
        const priorBlob = (await getDocument(documentId, tenantId))?.blockchain as Record<string, unknown> | undefined;
        // KS-521: preserveTerminalStatuses — this poll can land minutes after
        // creation and must not stomp a `revoked` set by the owner in between (the CASE inside the write keeps it).
        // KS-1384 R2b part 3 (D2 `progress`): the row is in flight WITH a tx (a confirmed row went to the resolver above). The
        // write lands only while the blob is neither confirmed nor failed AND still names THIS anchor, so a slow poll can no
        // longer write a submitted state over a confirmed blob, or over a newer attempt's.
        await writeAnchorBlobIf(documentId, tenantId, 'progress', {
          ...carriedForward(priorBlob),
          txHash,
          blockHeight: toBlockHeight(anchor.blockNumber),
          anchoredAt: anchor.anchoredAt || anchor.createdAt || new Date().toISOString(),
          network: anchor.network,
          status: anchor.status || 'submitted',
          anchorId,
        }, { expectAnchorId: anchorId, rowStatus: 'anchored' });
        consecutiveFailed = 0;
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
        // KS-1384 R2b part 3 (D2): the declared-simulated blob goes through the conditional write too: `confirmed` never over
        // a confirmed blob; an in-flight declaration only while the blob still names this anchor.
        await writeAnchorBlobIf(documentId, tenantId, confirmed ? 'confirmed' : 'progress', {
          ...carriedForward(priorSimBlob),
          txHash: null,
          blockHeight: toBlockHeight(anchor.blockNumber),
          anchoredAt: anchor.anchoredAt || anchor.createdAt || new Date().toISOString(),
          network: anchor.network,
          status: confirmed ? 'confirmed' : (anchor.status || 'submitted'),
          anchorId,
          ...simFields,
        }, { rowStatus: 'anchored', ...(confirmed ? {} : { expectAnchorId: anchorId }) });
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

  const anchor = await fetchAnchorState(bc.anchorId, authHeader) as AnchorRowRead | null;
  if (!anchor) return document;

  const confirmed = anchor.verified === true || anchor.status === 'confirmed';
  const simFields = simulatedFieldsFromAnchor(anchor);

  // KS-1384 R2b part 3 (D1, D3): a real (not simulated) row is DECIDED by the one resolver, with an in-flight row counted as
  // STALE (this read runs only after RECONCILE_STALE_MS of silence). Before R2b this reconcile healed to `confirmed` from any
  // confirmed row with a tx (an event's payload included), and failed the document on ONE `failed` read without asking
  // whether its create was on chain: so whether kintsugi's document ended confirmed or failed depended on which reader ran
  // first. Now: a confirmed row bound to the create confirms; otherwise own-create decides (found confirms, none fails,
  // not answered changes nothing), and every write goes through D2. A SIMULATED row runs through the resolver too: a failed
  // one still takes the fail-closed path (as it did before R2b, ahead of the KS-587 leg), and one the table cannot decide (a
  // simulated confirmation has no authoritative tx) falls through to the KS-587 declaration below.
  const prior = bc as unknown as Record<string, unknown>;
  const d = await resolveAnchorState({
    blob: prior,
    documentIds: documentIdsOf(document),
    row: anchor,
    inFlightStale: true,
    ownCreate: ownCreateFor(document, authHeader),
  });
  if (d.write === 'confirmed') {
    const written = await writeConfirmed(document.id, tenantId, prior, anchor, d, bc.anchorId);
    logger.info('Stale anchor state healed to confirmed on read (KS-535, KS-1384 R2b)', { documentId: document.id, anchorId: bc.anchorId, txHash: d.tx, via: d.via, written });
    const refreshed = await getDocument(document.id, tenantId);
    return refreshed || document;
  }
  if (d.write === 'anchor_failed' && inFlight) {
    await markDocumentAnchorFailed(document.id, tenantId, bc.anchorId, anchor.errorMessage ?? d.reason);
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
  if (inFlight && !bc.txHash && simFields.simulated) {
    // KS-1384 R2b part 3 (D2): written through the conditional blob write (never over a confirmed blob; an in-flight
    // declaration only while the blob still names this anchor), then re-read, since the write returns a row count.
    await writeAnchorBlobIf(document.id, tenantId, confirmed ? 'confirmed' : 'progress', {
      ...carriedForward(bc as unknown as Record<string, unknown>),
      txHash: null,
      blockHeight: toBlockHeight(anchor.blockNumber),
      anchoredAt: anchor.anchoredAt || anchor.createdAt || new Date().toISOString(),
      network: anchor.network,
      status: confirmed ? 'confirmed' : (anchor.status || 'submitted'),
      anchorId: bc.anchorId,
      ...simFields,
    }, { rowStatus: 'anchored', ...(confirmed ? {} : { expectAnchorId: bc.anchorId }) });
    logger.info('Stale anchor state healed to declared-simulated on read (KS-587)', { documentId: document.id, anchorId: bc.anchorId });
    const refreshed = await getDocument(document.id, tenantId);
    return refreshed || document;
  }

  return document;
}

// =============================================================================
// KS-1384 R2b part 5 (D3; Wednesday's GO on R2b, 2026-10-31 13:20:11Z): the verify heals' ONE shared path.
// =============================================================================

/** A real Cardano transaction hash (verification.ts REAL_TXHASH_RE; not imported, to keep this service free of route modules). */
const REAL_TX_RE = /^[0-9a-f]{64}$/i;

/** What a verify heal knows about the row it is presenting. */
export interface VerifyHealInput {
  /** The document's external id (what anchoring's rows carry as documentId when S sent one). */
  documentId: string;
  /** The primary key, which anchoring's rows carry when S sent no documentUuid. */
  documentPk?: string | null;
  /** The row's tenant; null or a cross-tenant row means present only, never write. */
  tenantId: string | null;
  blob: Record<string, unknown> | null;
  contentHash: string;
  updatedAt?: string | Date | null;
  /** The caller's bearer. Anchoring's anchor read and own-create are behind its JWT gate, so no bearer means no heal. */
  authHeader: string;
  /** False for a row from another tenant's pool: the default client here would write the wrong database. */
  write: boolean;
}

/**
 * The verify heals (v1 verification.ts, v2 verificationV2.ts) as CALLERS of the one resolver. Before R2b both healed a stale
 * in-flight blob to `confirmed` from verify-by-hash's chain answer when it was the same transaction OR the chain index named
 * this document (sameDoc), and wrote it through updateDocument. A confirmed transaction for this document's id is not
 * necessarily its CREATE (a share or lifecycle event carries the documentId too), so a verify could confirm a document with
 * another transaction's hash, and which reader ran first decided what the document said (kintsugi, 31 Oct).
 *
 * Now the heal reads the blob's OWN anchor row (its anchorId) and the resolver decides, exactly as the GET reconcile does: a
 * confirmed row bound to the create confirms; otherwise own-create decides. Only a `confirmed` decision is presented and
 * written, through D2 (`confirmed` is terminal in SQL). A verify never FAILS a document: an `anchor_failed` decision changes
 * nothing here (the reconcile and the poller write it). Returns the blob to PRESENT: the confirmed blob, or the blob unchanged.
 *
 * No bearer, no heal (Wednesday's ruling on part 5, 2026-10-31 19:55:30Z, D3 as written): anchoring's anchor read and
 * own-create are behind its JWT gate, so a v2 verify (caller-independent by design: it forwards no bearer) and an anonymous
 * v1 verify present the STORED state, fail closed, until the GET reconcile or the poller heals it. Before R2b both healed a
 * stale-pending blob from verify-by-hash's pre-auth chain answer; a bound, bearer-less variant is a separate follow-up.
 */
export async function healAnchorForVerify(input: VerifyHealInput): Promise<Record<string, unknown> | null> {
  const blob = input.blob;
  // Which blobs a verify may heal is UNCHANGED from before R2b, as KS-1661 and KS-1676 pinned it: a real (not simulated) blob
  // with a real 64-hex txHash that is neither settled (`confirmed`, `anchored: true`) nor failed (`failed`, `anchor_failed`).
  // R2b changes only what DECIDES the heal. A failed blob is healed forward by the GET reconcile, never by a verify.
  if (!blob || blob.simulated === true) return blob;
  if (typeof blob.txHash !== 'string' || !REAL_TX_RE.test(blob.txHash)) return blob;
  if (blob.status === 'confirmed' || blob.anchored === true) return blob;
  if (blob.status === 'failed' || blob.status === 'anchor_failed') return blob;
  const anchorId = typeof blob.anchorId === 'string' && blob.anchorId.length > 0 ? blob.anchorId : null;
  if (!anchorId || !input.authHeader) return blob;
  const row = await fetchAnchorState(anchorId, input.authHeader) as AnchorRowRead | null;
  // KS-1661's rule, kept for the row: a simulated anchor never heals a document (a TRUTHY test, not === true).
  if (!row || (row as { simulated?: unknown }).simulated) return blob;
  const updatedAtMs = Date.parse(input.updatedAt instanceof Date ? input.updatedAt.toISOString() : String(input.updatedAt ?? ''));
  const d = await resolveAnchorState({
    blob,
    documentIds: [input.documentId, input.documentPk].filter((x): x is string => typeof x === 'string' && x.length > 0),
    row,
    // The reconcile's staleness rule: an in-flight row is asked about only after RECONCILE_STALE_MS of silence. An unknown
    // updatedAt is NOT stale, so a verify never spends a chain scan on a guess.
    inFlightStale: Number.isFinite(updatedAtMs) && Date.now() - updatedAtMs >= RECONCILE_STALE_MS,
    ownCreate: () => askOwnCreate(fetch, anchoringBaseUrl(), input.authHeader, {
      documentId: input.documentId,
      contentHash: String(input.contentHash || '').replace(/^sha256:/i, '').toLowerCase(),
      timestamps: ownCreateTimestampsOf(blob),
    }),
  });
  if (d.write !== 'confirmed') return blob;
  const healed = confirmedBlobOf(blob, row, d, anchorId);
  // KS-1129 (FALLTHROUGH): an unusable height falls through to the STORED height, never a fabricated 0; unknown stays null.
  if (healed.blockHeight == null) {
    const stored = toBlockHeight(blob.blockHeight as number | string | null | undefined);
    if (stored != null && stored > 0) healed.blockHeight = stored;
  }
  if (input.write && input.tenantId) {
    try {
      const written = await writeAnchorBlobIf(input.documentId, input.tenantId, 'confirmed', healed, { rowStatus: 'anchored' });
      logger.info('Verify heal: anchor state confirmed through the resolver (KS-584, KS-1384 R2b)', { documentId: input.documentId, anchorId, txHash: d.tx, via: d.via, written });
    } catch (err: unknown) {
      // Presentation already has the decision; the write is convergence, and the reconcile and the poller are the catch-all.
      logger.warn('Verify heal: the confirmed write failed (presentation unaffected)', { documentId: input.documentId, error: err instanceof Error ? err.message : String(err) });
    }
  }
  return healed;
}
