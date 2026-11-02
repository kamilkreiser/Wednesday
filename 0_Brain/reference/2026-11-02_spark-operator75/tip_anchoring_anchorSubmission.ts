/**
 * =============================================================================
 * KS-705 — ANCHOR SUBMISSION (idempotent on the SUBMISSION, not only the row)
 * =============================================================================
 * The real-Cardano half of `processAnchor`, extracted for the same
 * bootless-unit-test reason as `reconciler.ts` and `anchorSchema.ts`
 * (index.ts calls app.listen on import, and the only honest way to assert
 * "the submit path ran once" is against a fake chain — a real assertion costs
 * a real transaction).
 *
 * WHAT WENT WRONG (measured on demo 2026-08-27T23:54–23:55Z, KS-697 probe):
 * one document produced THREE `Submitting anchor to Cardano` calls for a
 * single anchor id and TWO confirmed, fee-paying transactions —
 * 408e7208… (block 4,609,927) and df797be3… (block 4,609,929), 181,825
 * lovelace each. `anchor_store` kept only the second. The first is on chain,
 * carrying the same metadata for the same document, and no row points at it.
 *
 * Two independent producers, both closed here:
 *
 *   1. A create + a custody transfer both call `POST /api/anchors` for one
 *      document. They correctly resolve to the SAME row (KS-319 — keep that),
 *      but both then entered the submit path. The second waited on the wallet
 *      lock and submitted a SECOND transaction for a document already
 *      anchored. A pre-lock read cannot see this: on demo the two calls were
 *      389 ms apart and the row was still 'pending' for both. The re-read
 *      INSIDE the lock is what makes the submission idempotent.
 *
 *   2. That second submission was rejected with
 *      `ConwayMempoolFailure "All inputs are spent. Transaction has probably
 *      already been included…"` — the node saying the opposite of failure. The
 *      catch marked the row 'failed' (clobbering a status that was already
 *      'confirmed'), reset it to 'pending' and submitted a THIRD transaction,
 *      which also confirmed.
 *
 * THE RULE: a reply that names an already-submitted transaction whose hash we
 * know is a re-poll condition, never a resubmit.
 *
 * NOT HANDLED — enumerated deliberately (KS-705); extend this list, not the
 * retry:
 *   - Any node reply other than the two texts matched below. Blockfrost
 *     surfaces a node rejection as an HTTP 400 whose `message` carries the
 *     ledger's prose; the SDK exposes no enumerated code for "already in
 *     ledger"/"duplicate tx", so there is nothing further to match that would
 *     be a read rather than a guess. Sibling replies known to exist but NOT
 *     observed by us, and so NOT matched: `TxValidationErrorInCardanoMode`
 *     wrappers, `BadInputsUTxO`, and any node-specific "transaction already
 *     exists"/"duplicate transaction" text.
 *   - "Already included" on a row carrying NO real transaction hash. We
 *     cannot re-poll a transaction we cannot name, so that case keeps today's
 *     fail-and-retry behaviour rather than being silently swallowed. This is
 *     also the KS-535 cross-deployment shape (two deployments on one wallet),
 *     which this module does not and cannot fix.
 *   - Two PROCESSES submitting for one anchor. `withWalletLock` and the
 *     in-lock re-read are both process-local. A second replica still races;
 *     that needs a DB-level claim and is not in scope here. KS-726 does not
 *     close this one either — a write-ahead is still a single process's
 *     record — so this entry stands as written.
 *
 * The "row write lost after a successful submit" window found on the #756
 * review is NOT in this list: guard 4 below closes it, by hoisting the hash
 * out of the lock callback so the catch can re-poll rather than retry.
 *
 * KS-726 (write-ahead) is now IMPLEMENTED here rather than pending: the hash is
 * persisted from inside `deps.submit` via `onSigned`, BEFORE the node is asked
 * to accept the transaction, so a LOST submit reply leaves a row that names the
 * transaction instead of one the retry path answers with a second fee-paying
 * transaction. That is the class guard 4 structurally cannot reach — guard 4
 * needs `deps.submit()` to have RETURNED. See guard 5 in the catch, the
 * 'submitting' state, and `knownChainSubmission` above. The two are
 * complementary, not alternatives.
 *
 * Guard 5 rests ONLY a LOST reply. A DEFINITIVE node rejection — the reply
 * ARRIVED and said no (`isChainReachableError`: a `status_code` on the error;
 * BadInputsUTxO, ValueNotConservedUTxO, an expired TTL, "All inputs are spent")
 * — keeps the ordinary fail-and-retry path: nothing is on chain and nothing was
 * paid, so a retry is safe and free, and resting such a row in 'submitting'
 * would trade a ~15 s recovery for the reconciler's 24 h give-up (#805 review,
 * 2026-09-08; ruled 2026-09-14). One consequence for guard 3, below: on an
 * "inputs spent" reply the hash the node just refused is on the row (the
 * write-ahead put it there) and IS re-polled first — that reply is also what
 * a node says when our own earlier submit already landed (KS-705) — and only
 * when the bounded poll shows it ABSENT does the ordinary retry follow.
 *
 * Still NOT closed by the write-ahead, and deliberately: a crash of the whole
 * process between signing and the 'submitting' row write. The write-ahead
 * shrinks that gap to a single DB round-trip but cannot remove it, because
 * something has to be the first durable record.
 * =============================================================================
 */

// KS-726 (#805 review, ruled 2026-09-14): `isChainReachableError` is #728's
// discriminator — a `status_code` on the error means the node ANSWERED (any
// 4xx other than 402/408/429); no code, or 402/408/429/5xx, means it did not.
// Guard 5 below turns on it. KS-1384 F0 adds the wallet view (walletView.ts),
// which the confirm sites below keep current.
import { isChainReachableError } from './cardano/provider';
import { WalletView, platformWalletView, type OutRef, type ViewUtxo } from './walletView';
import { FamilyOutpointUnavailable, NoSpendableUtxo, payloadDigest } from './walletSpend';
import { BootArm, FamilyRegistry, CLOSURE_MIN_CONFIRMATIONS, encodedPayloadEquals } from './attemptFamily';

/**
 * KS-1384 F0 (design §3.7, the fourth review's M-3): the guarded write-ahead matched 0 rows. The row moved on
 * (a newer call re-armed it), so the newer call owns it: nothing is submitted, nothing is written, no retry is
 * scheduled. The catch checks for this FIRST.
 */
export class WriteAheadDeclined extends Error {
  constructor(readonly anchorId: string, readonly txHash: string) {
    super(`the write-ahead for ${anchorId} matched 0 rows; a newer call owns the row, ${txHash} was not submitted`);
    this.name = 'WriteAheadDeclined';
  }
}

/**
 * KS-1384 F0b (gate 48 F1): a family exists for this anchor and payload, it has NO family outpoint `u_F`, and one of
 * its members can still land. `u_F` is chosen from the first member's PASS-1 inputs (`recordMember`); a first
 * member built in pass 2 from add-backs alone has none, so a later member would be built without the shared coin,
 * on disjoint coins, and both could land: one payload paid twice. Nothing is built; the anchor waits outside the
 * lock, as rule 4 waits on a member holding `u_F`, until that member confirms (q9 confirms the row) or dies.
 */
export class FamilyWithoutOutpointInFlight extends Error {
  constructor(readonly anchorId: string, readonly members: string[]) {
    super(`a family for ${anchorId} has no shared coin and ${members.length} member(s) that may still land; nothing built`);
    this.name = 'FamilyWithoutOutpointInFlight';
  }
}

/**
 * KS-1384 F0 (design §3.7): the write-ahead did not run (`null`: the database was unavailable, or the statement
 * failed and was swallowed), or matched a count this spender cannot use. The transaction is NOT submitted, so no
 * fee is paid for a transaction no row names; the catch takes the ordinary failed path.
 */
export class WriteAheadUnavailable extends Error {
  constructor(readonly anchorId: string, readonly txHash: string, readonly count: number | null) {
    super(`the write-ahead for ${anchorId} did not land (count ${count}); ${txHash} was not submitted`);
    this.name = 'WriteAheadUnavailable';
  }
}

/**
 * KS-1384 F0 (the fourth review's M-3, stated per spender): the BATCH write-ahead. Every constituent anchor row
 * moves to 'submitting' with the transaction's hash, and the batch transaction may be sent (and so enters the
 * wallet view) only when ALL N writes matched their row. Anything less throws before the submit: no fee is paid
 * for a transaction some row cannot name. The single path's rule is the same with N = 1.
 */
export async function writeAheadEveryRow(
  anchorIds: string[],
  txHash: string,
  write: (anchorId: string) => Promise<number | null>,
): Promise<void> {
  let matched = 0;
  for (const anchorId of anchorIds) {
    if ((await write(anchorId)) === 1) matched += 1;
  }
  if (matched !== anchorIds.length) {
    throw new WriteAheadUnavailable(`batch of ${anchorIds.length}`, txHash, matched);
  }
}

/** Only a 64-hex ref is a real chain transaction — `mock_tx_…`/`tx_sim_…` are not (KS-587). */
const REAL_TX_64HEX = /^[0-9a-f]{64}$/i;

/**
 * The node replies we have actually observed for "your inputs are gone because
 * your own earlier transaction is already in flight or in a block".
 *   - the first is the demo measurement (KS-705, 2026-08-27T23:55:12Z);
 *   - the second is the shorter form recorded against KS-535.
 * Anything else is left to the failure path on purpose — see NOT HANDLED above.
 */
/**
 * The one node reply that names THIS transaction as in the ledger. Guard 3
 * re-polls on it even when the hash on the row is the one just written ahead
 * (KS-726) — because there the node is saying our transaction landed.
 */
const ALREADY_INCLUDED_REPLY = /already been included/i;

const ALREADY_SUBMITTED_REPLIES = [
  /all inputs are spent/i,
  ALREADY_INCLUDED_REPLY,
];

/** True when a submission error is the node telling us the tx is already in the ledger. */
export function isAlreadySubmittedError(err: unknown): boolean {
  const message = (err as { message?: unknown })?.message;
  if (typeof message !== 'string' || message.length === 0) return false;
  return ALREADY_SUBMITTED_REPLIES.some(pattern => pattern.test(message));
}

export interface AnchorSnapshot {
  id: string;
  status: 'pending' | 'submitting' | 'submitted' | 'confirmed' | 'failed';
  transactionHash?: string;
  retryCount: number;
  metadataLabel: number;
  metadataPayload: object;
}

export interface ConfirmationLike {
  confirmed: boolean;
  blockHash?: string;
  blockNumber?: number;
  slot?: number;
  confirmations?: number;
  /**
   * KS-726 (#805 gate F1): attempts that REACHED the chain / attempts that
   * THREW — `cardano/confirmation.ts` reports both. Optional so every injected
   * double stays type-compatible.
   *
   * ⚠ KS-1171 (Kam's ruling `c`, 2026-09-25) REVERSES what this comment used to
   * say. It read: "a `confirm` that reports neither keeps the pre-fix reading
   * (`confirmed: false` → 'absent')". That is no longer true and must not be
   * left standing: under the ruling a result carrying NO counters satisfies
   * neither ABSENT condition, so it now reads `'unknown'` and the row RESTS.
   * There is deliberately no carve-out for the counter-less shape — see the
   * gate in `reconfirmKnownSubmission`.
   */
  polled?: number;
  errored?: number;
  /** KS-1384 F0 (M-1): the `txs` answer's `valid_contract`, for the wallet view. */
  validContract?: boolean;
  /**
   * KS-1171: WHEN the chain last answered. `lastAnsweredElapsedMs` is measured
   * from the START OF POLLING, so a threshold on it is strictly conservative
   * against "60 s after the node's 400" — polling begins at or after that 400.
   */
  lastAnsweredAttempt?: number;
  lastAnsweredElapsedMs?: number;
}

/**
 * KS-1171, Kam's ruling (c). The two conditions a poll must BOTH meet before its verdict may be
 * read as a definitive "this transaction is not on chain". Exported so a regression cell names the
 * rule rather than repeating its numbers.
 */
export const ABSENT_MIN_ANSWERED_POLLS = 2;
export const ABSENT_MIN_LAST_ANSWER_MS = 60_000;

/** KS-1171 (c), in one place: a poll that ended without the transaction reads ABSENT only when BOTH conditions hold. */
export function definitelyAbsent(c: ConfirmationLike): boolean {
  return (c.polled ?? 0) >= ABSENT_MIN_ANSWERED_POLLS
    && typeof c.lastAnsweredElapsedMs === 'number'
    && c.lastAnsweredElapsedMs >= ABSENT_MIN_LAST_ANSWER_MS;
}

/**
 * KS-1384 F0b (design §3.5, B3/B4): an anchor with nothing to spend waits, from its FIRST wait (t0, held in memory
 * per anchor id), for at most this long. A front-door re-POST resets the row but not t0, so re-POSTs cannot extend
 * a process's wait without bound.
 */
export const WAIT_HORIZON_MS = 2 * 60 * 60_000;
/** The fourth review's m-5: a waiting anchor holds no lock; it is re-queued this often. */
export const WAIT_REQUEUE_MS = 60_000;
/** The marker written once, on the first wait (design §3.5 "The marker"); F-b's sweep reads t0 back from it. */
export const waitMarker = (t0: number): string =>
  `waiting for a spendable coin since ${new Date(t0).toISOString()} (KS-1384)`;

/** KS-1384 F0b: the chain reads rule 4, A1 and the boot arm need (provider.ts in production). */
export interface FamilyChainReads {
  /** An ANSWERED live tip (positive slot), or null. Every read also feeds the boot arm. */
  liveTip: () => Promise<{ slot: number; height: number | null } | null>;
  /** Who consumed this output; null = unknown (m-6). */
  outputSpender: (txHash: string, index: number) => Promise<string | null>;
  /** The transaction's JSON under `label`; undefined = no such label; null = unknown. */
  txLabelMetadata: (txHash: string, label: number) => Promise<unknown | null | undefined>;
  /** The transaction's block; null = not on chain. Throws when the chain did not answer. */
  txInfo: (txHash: string) => Promise<{ blockHeight: number | null; blockHash?: string; slot?: number; validContract?: boolean } | null>;
}

export interface AnchorSubmissionDeps {
  getAnchor: (anchorId: string) => Promise<AnchorSnapshot | null>;
  /**
   * KS-726: the optional third argument carries the write-ahead hook. Optional
   * so every existing injector — and #756's own two-argument call — stays
   * type-compatible; `cardano/index.ts`'s `AnchorSubmitOptions` is already
   * shaped for it.
   */
  submit: (
    metadataLabel: number,
    metadataPayload: object,
    options?: {
      onSigned?: (txHash: string) => Promise<void>;
      /** KS-1384 F0: who the spend is for (the wallet view's record) and the family outpoint; see cardano/index.ts. */
      spend?: { kind?: 'single'; anchorIds?: string[]; required?: OutRef };
      /** KS-1384 F0b: the signed body's facts, before the write-ahead. */
      onBuilt?: (facts: { txHash: string; ttlSlot: number; pass1Inputs: ViewUtxo[] }) => void;
    },
  ) => Promise<{ txHash: string; fee: number }>;
  confirm: (txHash: string, onStatusUpdate?: (attempt: number, status: string) => void) => Promise<ConfirmationLike>;
  /**
   * KS-1384 F-a: the production write (`dbUpdateAnchorStatus`) resolves to the matched row count, or null when
   * the write did not run. KS-1384 F0 is its first reader: the write-ahead submits only on exactly 1.
   */
  updateStatus: (anchorId: string, updates: Record<string, unknown>) => Promise<number | null>;
  bumpRetryCount: (anchorId: string) => Promise<void>;
  scheduleRetry: (anchorId: string, delayMs: number) => void;
  log: (level: 'info' | 'warn' | 'error', message: string, meta?: Record<string, unknown>) => void;
  /** The shared process-wide wallet mutex — see `withWalletLock` below. */
  withWalletLock?: <T>(fn: () => Promise<T>) => Promise<T>;
  /** KS-1384 F0: the process's wallet view (default: the shared one) and its clock. */
  view?: WalletView;
  now?: () => number;
  /**
   * KS-1384 F0b: the attempt families and the boot arm (default: this submitter's own), and the chain reads rule 4
   * and A1 use. Without `chain` the arm is never fed, so it stays disarmed and guard 3 keeps the pin's own rule,
   * and a blocked family rests its row.
   */
  families?: FamilyRegistry;
  arm?: BootArm;
  chain?: FamilyChainReads;
  maxRetries?: number;
  backoffMsPerAttempt?: number;
}

/**
 * Serialize Cardano submissions against the platform wallet. The UTXO model
 * means two concurrent submissions race to spend the same UTxO; the second one
 * fails with "All inputs are spent". We take a Promise chain as a process-local
 * mutex so each submission only begins once the prior one has committed. This
 * is the minimum viable solution — at scale we'd batch or use multi-UTxO coin
 * selection.
 *
 * Exported so the batch-anchor path in index.ts shares the SAME chain: two
 * independent locks on one wallet would be no lock at all.
 */
let walletSubmissionChain: Promise<unknown> = Promise.resolve();
export function withWalletLock<T>(fn: () => Promise<T>): Promise<T> {
  const next = walletSubmissionChain.catch(() => undefined).then(() => fn());
  walletSubmissionChain = next.catch(() => undefined);
  return next;
}

/**
 * KS-1384 F0, the fourth review's B1: the wallet lock's wait expired before the caller's turn came.
 * Nothing was built, signed or submitted; the caller answers 503.
 */
export class WalletLockTimeout extends Error {
  readonly waitedMs: number;
  constructor(waitedMs: number) {
    super(`the platform wallet stayed busy for ${waitedMs} ms; nothing was signed`);
    this.name = 'WalletLockTimeout';
    this.waitedMs = waitedMs;
  }
}

/**
 * KS-1384 F0 (B1): take the SAME process-wide wallet lock, but give up if the turn does not come within
 * `maxWaitMs`. Rejects with `WalletLockTimeout` and then NEVER runs `fn`, even when the lock frees later.
 *
 * Why: the single-anchor path holds the lock through its whole confirmation poll (about 27 minutes).
 * originate calls thread-mint with a bare fetch and gives up on it well before that; a mint that waited in
 * the queue would then sign and pay after the caller had gone, leaving a paid NFT that no registry row
 * names. A bounded wait, well under the caller's timeout, turns that into a 503 before signing.
 */
export function withWalletLockWithin<T>(fn: () => Promise<T>, maxWaitMs: number): Promise<T> {
  let timedOut = false;
  let timer: ReturnType<typeof setTimeout> | undefined;
  const expired = new Promise<never>((_resolve, reject) => {
    timer = setTimeout(() => { timedOut = true; reject(new WalletLockTimeout(maxWaitMs)); }, maxWaitMs);
  });
  const turn = withWalletLock(async () => {
    if (timedOut) return undefined as unknown as T; // our slot came too late: give it straight back, run nothing
    clearTimeout(timer);
    return fn();
  });
  return Promise.race([turn, expired]);
}

/**
 * The hash of an existing REAL chain submission for this anchor, if there is one.
 *
 * KS-726: 'submitting' counts. It is the write-ahead state — the row names a
 * transaction that was SIGNED, and whose submit reply we never received, so a
 * transaction bearing our name may already be on chain and fee-paying.
 *
 * Leaving it out is a reachable double-mint that the write-ahead itself opens,
 * not a hypothetical. `dbPersistAnchor` returns the EXISTING row's id on a
 * re-anchor of the same document+network (KS-281/KS-319) and `POST /api/anchors`
 * then calls `processAnchor` unconditionally (index.ts). So a second create — or
 * the custody-transfer hop that KS-705's own header describes — lands on a row
 * resting in 'submitting', both guards below see "no known submission", and the
 * path mints a SECOND transaction for a document whose first one may already be
 * in a block. That is the exact defect this module exists to prevent, reached
 * through the front door rather than the retry.
 *
 * Before KS-726 the case could not arise: a lost reply wrote 'failed' and
 * resolved to 'pending', and the retry path owned it. The write-ahead is what
 * makes the row REST in a state the guards could not read — so the guard has to
 * learn the state its own change creates.
 *
 * Re-polling such a row is safe and is the weaker-harm choice, on the same
 * asymmetry guard 5 turns on: `reconfirmKnownSubmission` is bounded, leaves a
 * confirmed row alone, and NEVER writes 'failed' — worst case it times out,
 * logs, and leaves the row for the reconciler, which owns the give-up decision
 * (KS-584). A delayed anchor is recoverable; a duplicate fee-paying transaction
 * is not.
 */
function knownChainSubmission(anchor: AnchorSnapshot | null): string | undefined {
  if (!anchor) return undefined;
  if (anchor.status !== 'submitting' && anchor.status !== 'submitted' && anchor.status !== 'confirmed') {
    return undefined;
  }
  const tx = anchor.transactionHash ?? '';
  return REAL_TX_64HEX.test(tx) ? tx : undefined;
}

export function createAnchorSubmitter(deps: AnchorSubmissionDeps) {
  const lock = deps.withWalletLock ?? withWalletLock;
  const maxRetries = deps.maxRetries ?? 3;
  const backoffMsPerAttempt = deps.backoffMsPerAttempt ?? 5000;
  const view = deps.view ?? platformWalletView;
  const now = deps.now ?? Date.now;
  const families = deps.families ?? new FamilyRegistry();
  const arm = deps.arm ?? new BootArm();
  const chain = deps.chain;
  /** t0 per waiting anchor (design §3.5, B3). Cleared when the anchor's write-ahead lands, or at the horizon. */
  const waitStarted = new Map<string, number>();

  /**
   * Design §3.5 and rule 4's wait (B4), the fourth review's m-5: the anchor waits OUTSIDE the wallet lock. Nothing
   * is signed, no retry is spent, nothing terminal is written inside the bound. The first wait writes the marker,
   * guarded on the row as this attempt read it (it also bumps updated_at); a re-queue does not rewrite it.
   */
  async function waitOutsideLock(anchorId: string, why: string): Promise<'requeued' | 'horizon'> {
    const firstWait = !waitStarted.has(anchorId);
    const t0 = waitStarted.get(anchorId) ?? now();
    waitStarted.set(anchorId, t0);
    if (now() - t0 >= WAIT_HORIZON_MS) {
      waitStarted.delete(anchorId);
      return 'horizon';
    }
    if (firstWait) {
      const row = await deps.getAnchor(anchorId);
      if (row) await deps.updateStatus(anchorId, { errorMessage: waitMarker(t0), ...rowExpectation(row) });
    }
    deps.log('info', 'Anchor waits for the platform wallet outside the lock — re-queued (KS-1384)', {
      anchorId, why, t0: new Date(t0).toISOString(), requeueMs: WAIT_REQUEUE_MS,
    });
    deps.scheduleRetry(anchorId, WAIT_REQUEUE_MS);
    return 'requeued';
  }

  /** A guarded write expects the row exactly as this attempt read it. */
  const rowExpectation = (row: AnchorSnapshot) =>
    ({ expectStatus: row.status, expectTransactionHash: row.transactionHash ?? null });

  async function observedTip() {
    if (!chain) return null;
    const tip = await chain.liveTip();
    arm.observe(tip?.slot);
    return tip;
  }

  /** Confirm the row with `txHash`, guarded; the count is the outcome (design §3.7). */
  async function confirmRowWith(
    anchorId: string,
    txHash: string,
    c: { blockNumber?: number | null; slot?: number; blockHash?: string; confirmations?: number },
    expect: Record<string, unknown>,
    why: string,
  ): Promise<number | null> {
    const count = await deps.updateStatus(anchorId, {
      status: 'confirmed', transactionHash: txHash, confirmations: c.confirmations ?? 1,
      blockNumber: c.blockNumber ?? undefined, slot: c.slot, blockHash: c.blockHash, confirmedAt: new Date(), ...expect,
    });
    deps.log(count === 1 ? 'info' : 'warn', count === 1
      ? 'Anchor confirmed with a transaction of its attempt family (KS-1384)'
      : 'Family confirm write matched no row — the row moved on; nothing written (KS-1384)', { anchorId, txHash, why, count });
    return count;
  }

  /** One member's poll, read under KS-1171; never writes. */
  async function pollMember(anchorId: string, txHash: string): Promise<{ verdict: 'confirmed' | 'absent' | 'unknown'; c?: ConfirmationLike }> {
    try {
      const c = await deps.confirm(txHash, (attempt, status) => deps.log('info', 'Anchor family re-poll', { anchorId, txHash, attempt, status }));
      if (c.confirmed) {
        view.markConfirmed(txHash, now(), c.validContract);
        return { verdict: 'confirmed', c };
      }
      return { verdict: definitelyAbsent(c) ? 'absent' : 'unknown', c };
    } catch {
      return { verdict: 'unknown' };
    }
  }

  /**
   * Design §3.4 rule 3: re-poll every member in parallel. Any found -> the row is confirmed with THAT member
   * (guarded). Any unknown -> rest. Only all absent reads absent.
   */
  async function repollFamily(anchorId: string, hashes: string[], expect: Record<string, unknown>): Promise<'confirmed' | 'absent' | 'unknown'> {
    const polls = await Promise.all(hashes.map(async (h) => ({ h, ...(await pollMember(anchorId, h)) })));
    const hit = polls.find((p) => p.verdict === 'confirmed');
    if (hit?.c) {
      await confirmRowWith(anchorId, hit.h, hit.c, expect, 'a family member is on chain');
      return 'confirmed';
    }
    return polls.some((p) => p.verdict === 'unknown') ? 'unknown' : 'absent';
  }

  /**
   * Design §3.4 rule 4, the build that could not spend the family outpoint `u_F`. Outside the lock. Returns
   * 'rebuild' only after closing the family (the next build starts a new one); 'rest' leaves the row as it is.
   */
  async function resolveBlockedFamily(anchorId: string, blocked: FamilyOutpointUnavailable): Promise<'rebuild' | 'rest' | 'confirmed' | 'wait'> {
    const row = await deps.getAnchor(anchorId);
    if (!row) return 'rest';
    const digest = payloadDigest(row.metadataLabel, row.metadataPayload);
    const fam = families.get(anchorId, digest);
    if (!fam?.uF) return 'rest';
    const expect = rowExpectation(row);
    const meta = { anchorId, uF: `${fam.uF.txHash}#${fam.uF.index}` };

    if (blocked.listed) {
      // u_F is listed but claimed by one of ours. m-1: our own CONFIRMED non-member spent it: close, never wait.
      const holder = view.spenderOf(fam.uF);
      if (holder && !fam.members.has(holder.txHash) && view.stateOf(holder.txHash) === 'confirmed') {
        families.close(fam);
        deps.log('warn', 'Family outpoint spent by our own confirmed non-member — family closed (KS-1384 m-1)', { ...meta, spender: holder.txHash });
        return 'rebuild';
      }
      // Our own in-flight transaction holds it: it confirms or dies. Wait for it (B4), outside the lock; nothing
      // is built meanwhile.
      deps.log('info', 'Family outpoint held by our own in-flight transaction — waiting, nothing built (KS-1384 rule 4)', { ...meta, holder: holder?.txHash });
      return 'wait';
    }

    // u_F is not listed: something spent it. First, is it one of ours?
    const verdict = await repollFamily(anchorId, [...fam.members.keys()], expect);
    if (verdict !== 'absent') return verdict === 'confirmed' ? 'confirmed' : 'rest';
    if (!chain) return 'rest';
    let tip: Awaited<ReturnType<FamilyChainReads['liveTip']>>;
    try { tip = await observedTip(); } catch { return 'rest'; }
    // No closure on TTL alone here: a member past its TTL may already be IN a block, and closing would build a
    // second transaction for a payload already anchored. TTL expiry is settled by the view instead (walletSpend.ts,
    // an answered tip plus one lookup), and the spender read below decides the rest.
    // Who spent u_F? m-6: null is UNKNOWN, and an unknown rests the row.
    const spender = await chain.outputSpender(fam.uF.txHash, fam.uF.index);
    if (!spender) {
      deps.log('warn', 'Family outpoint spender unknown — resting the row (KS-1384 m-6)', meta);
      return 'rest';
    }
    let info: Awaited<ReturnType<FamilyChainReads['txInfo']>>;
    try { info = await chain.txInfo(spender); } catch { return 'rest'; }
    if (!info) return 'rest';
    const own = view.record(spender);
    if (!own) {
      // A1: a spender we cannot see (foreign, or signed before this process started). Same payload on the
      // ENCODED side -> it anchored this row's event: confirm with it and build nothing.
      const onChain = await chain.txLabelMetadata(spender, row.metadataLabel);
      if (onChain === null) return 'rest';
      if (onChain !== undefined && encodedPayloadEquals(row.metadataPayload, onChain)) {
        await confirmRowWith(anchorId, spender, { blockNumber: info.blockHeight, slot: info.slot, blockHash: info.blockHash }, expect, 'A1: the spender of the family outpoint carries this payload');
        return 'confirmed';
      }
    } else if (own.payloadDigest === digest) {
      // Our own transaction for this very payload: confirm with it.
      await confirmRowWith(anchorId, spender, { blockNumber: info.blockHeight, slot: info.slot, blockHash: info.blockHash }, expect, 'our own same-payload transaction spent the family outpoint');
      return 'confirmed';
    }
    // A different payload spent u_F (a foreign spender, nft mints carry 721, or our own non-member). Closing needs
    // depth, by answered reads (M1): a shallower spend re-checks on the next attempt.
    if (!tip || tip.height == null || info.blockHeight == null || tip.height - info.blockHeight + 1 < CLOSURE_MIN_CONFIRMATIONS) {
      deps.log('warn', 'Family outpoint spent by another payload, not yet deep enough to close — resting the row (KS-1384)', { ...meta, spender });
      return 'rest';
    }
    families.close(fam);
    if (!own) view.noteSpentElsewhere(fam.uF, now());
    deps.log('warn', 'Family outpoint spent by another payload — family closed (KS-1384 rule 4)', { ...meta, spender });
    return 'rebuild';
  }

  /**
   * Bring the row into line with a transaction that is ALREADY on its way —
   * never a new submission. Leaves a confirmed row alone; never writes 'failed'
   * (a tx we have not found yet is not a tx that failed — the reconciler owns
   * the give-up decision, KS-584).
   */
  async function reconfirmKnownSubmission(
    anchorId: string,
    txHash: string,
    why: string,
  ): Promise<'confirmed' | 'absent' | 'unknown'> {
    // The return value is read by guard 3 only (KS-726): 'absent' means the
    // bounded poll ENDED without finding the transaction — the chain answered
    // and it is not there; 'unknown' means the poll itself failed — it threw,
    // or no attempt ever reached the chain — which says nothing about the
    // chain and keeps today's behaviour.
    deps.log('info', 'Anchor already submitted — re-polling the known transaction instead of submitting again (KS-705)', {
      anchorId, txHash, why,
    });
    const current = await deps.getAnchor(anchorId);
    if (current?.status === 'confirmed') return 'confirmed';
    try {
      const confirmation = await deps.confirm(txHash, (attempt, status) =>
        deps.log('info', 'Anchor confirmation poll', { anchorId, attempt, status }));
      if (confirmation.confirmed) {
        view.markConfirmed(txHash, now(), confirmation.validContract);
        await deps.updateStatus(anchorId, {
          status: 'confirmed',
          // KS-705 (#756 review): name the transaction that confirmed it.
          // Without this we confirm a row while never recording WHICH
          // transaction confirmed it — the same orphan this module exists to
          // prevent, one step later. The re-poll path is reached from rows
          // that already carry the hash AND from the catch below, where the
          // row write may never have landed.
          transactionHash: txHash,
          confirmations: confirmation.confirmations ?? 1,
          blockNumber: confirmation.blockNumber,
          slot: confirmation.slot,
          blockHash: confirmation.blockHash,
          confirmedAt: new Date(),
        });
        deps.log('info', 'Anchor confirmed on Cardano', {
          anchorId, txHash, blockNumber: confirmation.blockNumber, slot: confirmation.slot,
        });
        return 'confirmed';
      }
      // #805 tier-1 gate F1 (2026-09-14): the poll ended without ONE attempt
      // reaching the chain — every attempt threw (Blockfrost 5xx / 402 quota,
      // DNS, socket). That is not "the chain answered and it is not there"; it
      // is "we never asked". Reporting 'absent' here let guard 3 read an
      // unreachable chain as a DEFINITIVE rejection and schedule the ordinary
      // retry, which mints a SECOND fee-paying transaction for a document
      // whose first may already be in a block — the KS-705 class, reached
      // through the write-ahead path. 'unknown' rests the row in 'submitting'
      // for the reconciler (KS-584): the same weaker-harm choice guard 5 makes
      // for a lost reply. A `confirm` that reports no `polled` count (an
      // injected double) keeps the 'absent' reading.
      // KS-1171 — RULED BY KAM, option (c), live board 2026-09-25 12:49:07 AEST, card
      // `secuura-ks1171-when-is-an-anchor-absent`, verbatim: "c - Both conditions (strictest,
      // fewest double submissions)". A transaction may be called ABSENT — and so retried, which
      // mints a SECOND fee-paying transaction — only when BOTH hold:
      //
      //   1. at least 2 attempts ANSWERED (the chain replied, with the tx or with "not found"), and
      //   2. an answer arrived at least 60 s after the node's 400.
      //
      // Anything less rests the row in 'submitting' for the reconciler (KS-584) as 'unknown'. KS-726
      // closed the case where NO attempt reached the chain; this closes its neighbour, where one
      // early "not found" was read as definitive. Blockfrost answers 404 until a transaction is in a
      // block AND indexed, so an early answer is a likely FALSE negative in exactly the case that
      // matters — a same-hash duplicate submit, where TX_A entered the mempool seconds before the 400.
      //
      // The timing is measured from the START OF POLLING, which is at or after the 400. So
      // `lastAnsweredElapsedMs >= 60_000` IMPLIES at least 60 s since the 400, never less: the gate
      // is strictly conservative against the ruling, which is the side Kam chose.
      //
      // The cost, accepted with the ruling: a genuinely absent transaction whose late attempts threw
      // now rests ~24 h for the reconciler instead of retrying in ~15 s.
      //
      // A `confirm` that reports NO counters (an injected double) satisfies neither condition and so
      // reads 'unknown'. That REVERSES the KS-726 note and is deliberate — see
      // `ks726-gate-f1-unreachable-chain.test.ts`, whose control is rewritten to assert it. There is
      // no carve-out for `polled === undefined`: a branch whose only consumer is a test double later
      // reads as intended behaviour, and production always goes through `waitForConfirmation`, which
      // always reports both counters.
      const answered = confirmation.polled ?? 0;
      const lastAnsweredElapsedMs = confirmation.lastAnsweredElapsedMs;
      const answeredTwice = answered >= ABSENT_MIN_ANSWERED_POLLS;
      const answeredLateEnough =
        typeof lastAnsweredElapsedMs === 'number' && lastAnsweredElapsedMs >= ABSENT_MIN_LAST_ANSWER_MS;
      if (!definitelyAbsent(confirmation)) {
        // Two DIFFERENT operational facts, so two different messages. KS-726's case — no attempt
        // reached the chain at all — keeps its own wording, because "never reached the chain" is
        // still exactly what happened and an operator reading the log needs to tell it from "the
        // chain answered, but not definitively enough to retry on". Collapsing them into one
        // message also silently broke three shipped KS-726 cells that assert the KS-726 text while
        // asserting UNCHANGED behaviour; that was a defect in this change, not a consequence of
        // the ruling.
        const neverReached = answered === 0;
        deps.log(
          'warn',
          neverReached
            ? 'Anchor confirmation poll never reached the chain — treating the transaction as UNKNOWN, not absent (KS-726)'
            : 'Anchor confirmation answered but is not definitive — treating the transaction as UNKNOWN, not absent (KS-1171)',
          {
            anchorId, txHash,
            polled: confirmation.polled, errored: confirmation.errored,
            lastAnsweredAttempt: confirmation.lastAnsweredAttempt,
            lastAnsweredElapsedMs,
            answeredTwice, answeredLateEnough,
          },
        );
        return 'unknown';
      }
      deps.log('warn', 'Anchor confirmation timed out', { anchorId, txHash, polled: confirmation.polled, errored: confirmation.errored, lastAnsweredElapsedMs });
      return 'absent';
    } catch (err) {
      deps.log('error', 'Anchor confirmation polling failed', { anchorId, error: (err as Error)?.message });
      return 'unknown';
    }
  }

  /**
   * Submit one anchor to Cardano — at most one transaction per anchor.
   * `rebuild` (internal, KS-1384 F0b): this call follows a family closure; it never closes and rebuilds again.
   */
  return async function submitAnchorToChain(anchorId: string, rebuild = false): Promise<void> {
    const anchor = await deps.getAnchor(anchorId);
    if (!anchor) return;

    // Guard 1 (cheap, pre-lock): this anchor already has a transaction on chain.
    const alreadyKnown = knownChainSubmission(anchor);
    if (alreadyKnown) {
      await reconfirmKnownSubmission(anchorId, alreadyKnown, 'row already carries a chain submission');
      return;
    }

    // KS-705 (#756 review): the hash of a transaction we have already put on
    // chain, hoisted out of the lock callback so the catch below can see it.
    //
    // `deps.submit()` mints and pays for a transaction; the row write on the
    // NEXT line records its hash. If that write throws — a Postgres blip, pool
    // exhaustion, a restart — the hash dies with the stack frame, the catch
    // sees an ordinary error, and the retry submits a SECOND transaction for a
    // document that is already anchored. Guards 1 and 2 cannot see it: they
    // read the ROW, and the row is exactly what failed to be written.
    let submittedTxHash: string | undefined;

    // KS-726: the write-ahead hash — set from inside `deps.submit` via
    // `onSigned`, BEFORE the node is asked to accept the transaction.
    //
    // Declared OUT here for exactly the reason `submittedTxHash` is: a variable
    // the catch cannot see is precisely the defect this closes. #764 first wrote
    // it inside the try and `tsc` rejected the catch with TS2304 — the compiler
    // reproducing the ticket in miniature.
    //
    // The two are NOT the same fact and they do not have the same remedy:
    //   - `submittedTxHash` set  ⇒ `deps.submit()` RETURNED ⇒ the node
    //     acknowledged. Re-polling is safe (guard 4).
    //   - `writtenAheadTxHash` set and `submittedTxHash` NOT ⇒ the transaction
    //     was signed and named, and the reply was LOST. Acceptance is unknown.
    let writtenAheadTxHash: string | undefined;

    try {
      // Hold the wallet lock through submit + confirmation. The Cardano UTXO
      // model means a freshly-spent UTxO stays in Blockfrost's "available"
      // view until the tx is in a block (~20–60s). Concurrent submissions race
      // and the second one fails with "All inputs are spent". This design
      // serializes at the wallet level: at most one anchor tx in-flight from
      // the platform wallet. Throughput is intentionally bounded (~one cert
      // per block slot). A proper multi-UTXO coin selector is the
      // commercialisation upgrade path.
      type LockOutcome =
        | { kind: 'submitted' }
        | { kind: 'already'; txHash: string }
        | { kind: 'member-confirmed'; txHash: string; expect: Record<string, unknown> };
      const outcome = await lock(async (): Promise<LockOutcome> => {
        // Guard 2 (KS-705): re-read INSIDE the lock. Guard 1 ran before we
        // queued; by the time we hold the lock, the call ahead of us may have
        // submitted this very anchor. This is the guard that would have stopped
        // demo's second transaction.
        const current = (await deps.getAnchor(anchorId)) ?? anchor;
        const known = knownChainSubmission(current);
        if (known) return { kind: 'already', txHash: known };

        // KS-1384 F0b, rule 4 (design §3.4): a build for this anchor and payload while a family exists. A member
        // the wallet view already records as confirmed confirms the row, and nothing is built (q9: a same-payload
        // upsert during the in-lock poll nulled the hash; the queued call must not pay again).
        const digest = payloadDigest(current.metadataLabel, current.metadataPayload);
        const fam = families.get(anchorId, digest);
        const confirmedMember = fam ? [...fam.members.keys()].find((h) => view.stateOf(h) === 'confirmed') : undefined;
        if (confirmedMember) return { kind: 'member-confirmed', txHash: confirmedMember, expect: rowExpectation(current) };
        // m-8: a member that spent u_F was refused while u_F is still listed. Before spending u_F again, ask the
        // chain who consumed it: a lagging page can list a coin a foreign spender already took.
        if (fam?.uF && chain && [...fam.members.keys()].some((h) => view.stateOf(h) === 'dead')) {
          // Any spender at all (a member that landed after all, or someone else) means u_F is gone: rule 4 decides.
          const spender = await chain.outputSpender(fam.uF.txHash, fam.uF.index);
          if (spender) throw new FamilyOutpointUnavailable(fam.uF, false);
        }
        // Gate 48 F1: with no u_F nothing excludes a second member, so while any member may still land
        // (live, or not in the view at all), build nothing. A dead member cannot land and does not block.
        if (fam && !fam.uF) {
          const mayLand = [...fam.members.keys()].filter((h) => view.stateOf(h) !== 'dead');
          if (mayLand.length > 0) throw new FamilyWithoutOutpointInFlight(anchorId, mayLand);
        }
        let builtFacts: { txHash: string; ttlSlot: number; pass1Inputs: ViewUtxo[] } | undefined;

        // KS-1385 MIN-1 — the compare-and-set value. This is the payload we are
        // about to put ON CHAIN, so it is the only payload a transaction hash
        // written below may legitimately be recorded beside. Every write in
        // this callback that CLAIMS a transaction carries it as
        // `expectMetadataPayload`, and the UPDATE applies only while the row
        // still holds it (anchorStatusUpdate.ts).
        //
        // Ruled by Wednesday 2026-10-13T11:22:45Z after the gate measured the
        // window with the real lock and real Postgres: without this, a second
        // event's upsert landing mid-submit leaves the row carrying event 2's
        // identity next to event 1's transaction.
        //
        // Captured HERE, not at the top of `submitAnchorToChain`: the read
        // outside the lock can be arbitrarily stale, and the fact that matters
        // is what we signed, which is what `current` holds now.
        const signedMetadataPayload = current.metadataPayload;

        deps.log('info', 'Submitting anchor to Cardano', { anchorId });

        const submission = await deps.submit(current.metadataLabel, current.metadataPayload, {
          // KS-1384 F0b, rule 1: every later member of a family spends the family outpoint.
          spend: { kind: 'single', anchorIds: [anchorId], ...(fam?.uF ? { required: fam.uF } : {}) },
          onBuilt: (facts) => { builtFacts = facts; },
          // KS-726 — write-ahead. Runs after the transaction is built and
          // signed, before it is handed to the network. The hash is the
          // blake2b-256 of the signed body, so it is fully known here; nothing
          // the network says afterwards can teach us anything about it.
          onSigned: async (txHash) => {
            // #805 review F3: assigned AFTER the write, NOT before — the mirror
            // of `submittedTxHash` below, and the inverse case.
            //
            // `submittedTxHash` is captured before its write because by then the
            // transaction HAS been submitted: the fact must survive a failing
            // row write. Here the opposite holds — `onSigned` runs BEFORE the
            // network is asked, so if this write throws, NO transaction exists.
            // Assigning first would arm guard 5, which rests the row in
            // 'submitting' and schedules no retry, for a transaction that was
            // never sent — where an ordinary retry is correct and free.
            //
            // Assigned here, the variable means what guard 5 reads it as: the
            // hash is durable.
            //
            // KS-1384 F0 (design §3.7): the count decides. 0 = the row moved on and a newer call owns it
            // (WriteAheadDeclined); null = the write did not run (WriteAheadUnavailable). Either way the hook
            // THROWS, so nothing is submitted and nothing enters the wallet view (walletSpend.ts admits only
            // after this resolves). Before F0 the production write swallowed its error and the submit went
            // ahead against a row that might not name it.
            const count = await deps.updateStatus(anchorId, { status: 'submitting', transactionHash: txHash, expectMetadataPayload: signedMetadataPayload });
            if (count === 0) throw new WriteAheadDeclined(anchorId, txHash);
            if (count !== 1) throw new WriteAheadUnavailable(anchorId, txHash, count);
            writtenAheadTxHash = txHash;
            waitStarted.delete(anchorId);
            // KS-1384 F0b: a sent transaction joins its family; the first one fixes u_F (rule 0). Without the
            // body's facts (an injected submit) it still joins, with no TTL and no u_F.
            families.recordMember(anchorId, digest, txHash, builtFacts?.txHash === txHash ? builtFacts.ttlSlot : Number.POSITIVE_INFINITY,
              builtFacts?.txHash === txHash ? builtFacts.pass1Inputs : []);
          },
        });
        // Assign BEFORE the row write, not after: the write is the thing that
        // can fail, and this assignment is what survives it.
        submittedTxHash = submission.txHash;
        await deps.updateStatus(anchorId, { status: 'submitted', transactionHash: submission.txHash, expectMetadataPayload: signedMetadataPayload });
        deps.log('info', 'Anchor submitted to Cardano', { anchorId, txHash: submission.txHash, fee: submission.fee });

        // Block inside the lock until confirmed (or timed out). The next anchor
        // waiting on the lock will then read UTxOs that reflect this tx.
        try {
          const confirmation = await deps.confirm(submission.txHash, (attempt, status) =>
            deps.log('info', 'Anchor confirmation poll', { anchorId, attempt, status }));
          if (confirmation.confirmed) {
            view.markConfirmed(submission.txHash, now(), confirmation.validContract);
            await deps.updateStatus(anchorId, {
              status: 'confirmed',
              // KS-1384 F0b (design §3.7; the fourth review's m-4): the write NAMES its transaction and expects
              // it, in either in-flight state. A same-payload upsert during the poll nulled the hash: this then
              // matches 0, and the queued call confirms the row from the family (rule 4, q9) instead of paying
              // again. 'submitting' is expected too because the 'submitted' write can be swallowed (null).
              transactionHash: submission.txHash,
              expectStatus: ['submitting', 'submitted'],
              expectTransactionHash: submission.txHash,
              confirmations: confirmation.confirmations ?? 1,
              blockNumber: confirmation.blockNumber,
              slot: confirmation.slot,
              blockHash: confirmation.blockHash,
              confirmedAt: new Date(),
              // KS-1385 MIN-1: guarded for the same reason as the two writes
              // above, and NOT as an afterthought. Without it, a row whose
              // 'submitted' write was correctly declined would still be marked
              // `confirmed` — status confirmed, transaction_hash null — which
              // is a worse row than the one the guard refused to write.
              expectMetadataPayload: signedMetadataPayload,
            });
            deps.log('info', 'Anchor confirmed on Cardano', {
              anchorId,
              txHash: submission.txHash,
              blockNumber: confirmation.blockNumber,
              slot: confirmation.slot,
            });
          } else {
            deps.log('warn', 'Anchor confirmation timed out', { anchorId, txHash: submission.txHash });
          }
        } catch (err) {
          deps.log('error', 'Anchor confirmation polling failed', { anchorId, error: (err as Error).message });
        }
        return { kind: 'submitted' };
      });

      // Re-polling happens OUTSIDE the lock: we are not spending a UTxO, so
      // holding the wallet hostage for another anchor's confirmation window
      // would throttle the platform for no benefit.
      if (outcome.kind === 'already') {
        await reconfirmKnownSubmission(anchorId, outcome.txHash, 'another call submitted this anchor while we waited on the wallet lock');
      } else if (outcome.kind === 'member-confirmed') {
        // KS-1384 F0b (q9): the block details come from one poll of a transaction the view knows is on chain.
        const found = await pollMember(anchorId, outcome.txHash);
        if (found.verdict === 'confirmed' && found.c) {
          await confirmRowWith(anchorId, outcome.txHash, found.c, outcome.expect, 'a family member already confirmed (q9)');
        }
      }
    } catch (err: unknown) {
      const message = (err as { message?: string })?.message;

      // KS-1384 F0 (design §3.7, cell q3b): checked FIRST. The write-ahead matched 0 rows, so the row moved on
      // and the newer call owns it. Nothing was submitted; a 'failed' write here would land on the newer call's
      // row, and a retry would race it. One warn line, no write, no scheduleRetry.
      if (err instanceof WriteAheadDeclined) {
        deps.log('warn', 'Write-ahead matched 0 rows — a newer call owns this anchor; nothing submitted, nothing written (KS-1384)', {
          anchorId, txHash: err.txHash,
        });
        return;
      }

      // KS-1384 F0b, rule 4: the build could not spend the family outpoint, so nothing was signed. Resolved here,
      // outside the wallet lock. A closed family is rebuilt once, as a new family.
      if (err instanceof FamilyOutpointUnavailable) {
        const resolved = await resolveBlockedFamily(anchorId, err);
        if (resolved === 'rebuild' && !rebuild) await submitAnchorToChain(anchorId, true);
        if (resolved === 'wait' && (await waitOutsideLock(anchorId, 'the family outpoint is held by our own in-flight transaction')) === 'horizon') {
          // B4: after the horizon the row rests. It carries a real hash (R4 owns it) or none (F-b's sweep does).
          deps.log('warn', 'Rule 4 wait reached its horizon — resting the row (KS-1384)', { anchorId });
        }
        return;
      }

      // Gate 48 F1: a family with no u_F has a member that may still land. Wait like rule 4; nothing was signed.
      if (err instanceof FamilyWithoutOutpointInFlight) {
        if ((await waitOutsideLock(anchorId, 'a family with no shared coin has a member that may still land')) === 'horizon') {
          deps.log('warn', 'Wait for an in-flight member of a family with no shared coin reached its horizon — resting the row (KS-1384)', { anchorId, members: err.members });
        }
        return;
      }

      // KS-1384 F0b (design §3.5): nothing spendable. Not a failure of the anchor and no retry spent: wait outside
      // the lock, re-queued, up to WAIT_HORIZON_MS from t0. At the horizon, the ordinary failed path, guarded on
      // the row as this attempt read it, and no further wait (so "up to 2 h" holds).
      if (err instanceof NoSpendableUtxo) {
        if ((await waitOutsideLock(anchorId, 'no spendable coin')) === 'requeued') return;
        const row = await deps.getAnchor(anchorId);
        const count = await deps.updateStatus(anchorId, {
          status: 'failed',
          errorMessage: `no spendable coin in the platform wallet for ${WAIT_HORIZON_MS / 60_000} minutes; nothing was submitted (KS-1384)`,
          ...(row ? rowExpectation(row) : {}),
        });
        if (count === 1) await deps.bumpRetryCount(anchorId);
        deps.log('error', 'Anchor waited the full horizon for a spendable coin — failed, nothing submitted (KS-1384)', { anchorId, count });
        return;
      }

      // Guard 4 (KS-705, #756 review): we know we put a transaction on chain,
      // whatever this error says. Checked FIRST, before the node-reply matcher
      // and before any failure is recorded, because it is the strongest fact
      // available here: a hash in this variable means `deps.submit()` returned,
      // so the transaction is real and fee-paying. Answering that with another
      // transaction is the double-mint; marking the row terminally 'failed'
      // would propagate a permanent document failure for an anchor that
      // succeeded. Re-poll instead — the same treatment as the node's
      // "already included" reply, reached by a different route.
      if (submittedTxHash && REAL_TX_64HEX.test(submittedTxHash)) {
        deps.log('warn', 'Anchor submission threw AFTER the transaction reached the chain — re-polling the known hash instead of retrying (KS-705)', {
          anchorId, txHash: submittedTxHash, error: message,
        });
        await reconfirmKnownSubmission(anchorId, submittedTxHash, 'the row write failed after a successful submit');
        return;
      }

      // Guard 5 (KS-726) — the write-ahead branch. Sits BELOW guard 4 and
      // ABOVE guard 3 and the 'failed' write, because the catch is ordered by
      // the STRENGTH OF THE FACT each branch rests on, strongest first:
      //
      //   1. guard 4  — `deps.submit()` returned          → the node acknowledged
      //   2. guard 5  — signed and named, reply LOST      → acceptance UNKNOWN
      //   3. guard 3  — an inferred error-message shape   → weakest
      //   4. fall through — nothing
      //
      // Guard 5 covers ONE case: the reply was LOST. It does NOT cover a
      // DEFINITIVE rejection — the reply ARRIVED and said no. After the
      // write-ahead `writtenAheadTxHash` is set for EVERY real submission, so
      // without the discriminator below this branch would catch every error
      // thrown after signing and the retry path would be unreachable for the
      // whole class (#805 review, 2026-09-08). `isChainReachableError` (#728) is
      // that discriminator: a `status_code` on the error means the node
      // answered. A refused transaction is definitively NOT on chain and
      // nothing was paid, so it falls through to guard 3 and the ordinary
      // fail-and-retry write — a ~15 s recovery instead of the reconciler's
      // 24 h give-up on the most ordinary Cardano failure class. Ruled
      // 2026-09-14 (option 1 of the two the review offered).
      //
      // Why the LOST-reply case does NOT re-poll: after a lost reply we do not know the node
      // accepted it. Polling could block on a transaction that never landed;
      // writing 'failed' could permanently fail a document whose transaction is
      // on chain and fee-paying. The harms are asymmetric, so the guard resolves
      // toward the RECOVERABLE state — 'submitting', which the reconciler
      // selects (reconciler.ts) and settles either way.
      //
      // Its position is load-bearing, not cosmetic. #764's own review found the
      // 'failed' write landing FIRST, with the write-ahead check ~25 lines
      // later. Pre-KS-726 that flash resolved back to 'pending' and the row
      // re-entered the normal path — the KS-535 trade-off. WITH a write-ahead it
      // resolved to 'submitting' and STAYED, so the row spent a real window
      // claiming 'failed'. 'failed' is terminal by construction (KS-535) and
      // originate's poller acts on it, so a poller ticking inside that window
      // could propagate a PERMANENT document failure for a transaction that is
      // on chain. Ordering it here removes the window rather than documenting it.
      if (writtenAheadTxHash && REAL_TX_64HEX.test(writtenAheadTxHash) && isChainReachableError(err)) {
        // The node ANSWERED and refused the transaction we signed. Nothing is
        // on chain, nothing was paid: fall through to guard 3 and the terminal
        // 'failed' write + retry below, exactly as a pre-write-ahead failure did.
        // KS-1384 F0 (design §3.8, "Logging"): the WHOLE message, the status code and the provider's own error and
        // body. Every surviving log of the kintsugi/demo refusals cut the node's text, so the refusal text is
        // still UNMEASURED; this line settles it at the next occurrence.
        const refusal = err as { status_code?: number; error?: unknown; body?: unknown };
        deps.log('warn', 'Node REFUSED the written-ahead transaction — the reply arrived, nothing is on chain, keeping the ordinary fail-and-retry path (KS-726)', {
          anchorId, txHash: writtenAheadTxHash, statusCode: refusal?.status_code, error: message,
          providerError: refusal?.error, providerBody: refusal?.body,
        });
      } else if (writtenAheadTxHash && REAL_TX_64HEX.test(writtenAheadTxHash)) {
        await deps.updateStatus(anchorId, {
          status: 'submitting',
          // #805 review F2: carry the hash. The injected updateStatus SWALLOWS
          // its errors, so a DB blip during the write-ahead does not throw and
          // the submit proceeds anyway. If the reply is then lost, this guard
          // fires for a row that names no transaction — invisible to the
          // reconciler (`transaction_hash IS NOT NULL`), invisible to
          // knownChainSubmission (the empty fallback fails REAL_TX_64HEX), and
          // never retried, because this branch returns without scheduleRetry.
          // A stranded row with a paid transaction on chain: the exact failure
          // this ticket exists to close, surviving in a narrower window.
          // Idempotent when the write-ahead landed; the whole fix when it did not.
          transactionHash: writtenAheadTxHash,
          errorMessage: `Submit reply lost after signing; tx ${writtenAheadTxHash} may be on chain — left for the reconciler (KS-726)`,
        });
        // #805 review (2026-09-08), note 2: NO `bumpRetryCount` here. No retry is
        // coming from this branch, the reconciler's give-up is time-based
        // (`giveUpMs` against `created_at`, reconciler.ts), so a bump would only
        // spend budget that a later front-door re-anchor inherits reduced.
        deps.log('warn', 'Anchor submit failed AFTER the hash was written ahead — not retrying, reconciler will settle it', {
          anchorId, txHash: writtenAheadTxHash, error: message,
        });
        return;
      }

      // Guard 3 (KS-705): the node telling us the inputs are spent because our
      // own transaction is already in the ledger is not a failure. Re-poll the
      // hash we know; never answer it with another transaction.
      // KS-1384 F0b: the hash the retry writes below expect, when guard 3 decided the retry.
      let guardedOn: string | undefined;
      if (isAlreadySubmittedError(err)) {
        const current = await deps.getAnchor(anchorId);
        const known = knownChainSubmission(current);
        if (known) {
          // KS-1384 F0b (design §3.2.2, §3.4 rule 3): re-poll the WHOLE family, not only the row's hash: every
          // transaction this process signed for this anchor, in parallel, each under KS-1171. With no other
          // member this is the pin's own single re-poll, unchanged.
          const others = families.membersOfAnchor(anchorId).filter((h) => h !== known);
          const found = others.length === 0
            ? await reconfirmKnownSubmission(anchorId, known, 'node reported the transaction is already included')
            : await repollFamily(anchorId, [known, ...others], { expectStatus: ['submitting', 'submitted'], expectTransactionHash: known });
          // KS-726 (ruled 2026-09-14): the write-ahead put the hash of the
          // transaction we JUST signed on the row before the node answered, so
          // `known` can be that very hash. "inputs spent" is what a node says
          // BOTH when our own earlier submit already landed (KS-705 — the
          // re-poll above is the right answer, and skipping it is the
          // double-mint) AND when someone else spent our inputs (KS-535 — our
          // transaction can never land). The reply text cannot tell the two
          // apart; the chain can. So the re-poll runs first, bounded, and only
          // when it shows the hash we just wrote ahead ABSENT is the rejection
          // definitive — then the ordinary retry below follows, instead of the
          // reconciler's 24 h give-up. "already been included" names THIS
          // transaction as in the ledger and never reaches this branch's retry.
          //
          // KS-1384 F0b replaces the pin's `known === writtenAheadTxHash` and its "already been included" clause:
          //   - §3.2.5: the row's current hash must be a member of a family THIS process signed for this anchor.
          //     A hash some other process wrote is not ours to retry past (the pin's check, generalised);
          //   - §3.2.6, the boot arm: until an answered tip shows S_boot + ANCHOR_TTL_SLOTS + 600, a transaction
          //     signed before this process started may still land, and the family cannot see it. While disarmed
          //     the pin's clause stands: "already been included" rests the row. Once armed, the family re-poll is
          //     the whole answer, so the node's real text (which carries BOTH phrases, KS-1815) no longer makes
          //     Kam's 2026-09-14 retry ruling unreachable.
          if (found !== 'absent') return;
          if (!families.isMemberOfAnchor(anchorId, known)) {
            deps.log('warn', 'The row names a transaction this process did not sign — resting the row, not retrying past it (KS-1384 §3.2.5)', {
              anchorId, txHash: known, error: message,
            });
            return;
          }
          try { await observedTip(); } catch { /* an unanswered tip feeds nothing; the arm stays as it was */ }
          if (!arm.isArmed() && ALREADY_INCLUDED_REPLY.test(message ?? '')) {
            deps.log('warn', 'Inside the boot window the node said "already been included" — resting the row as the pin does (KS-1384 §3.2.6)', {
              anchorId, txHash: known, bootSlot: arm.bootSlot(), error: message,
            });
            return;
          }
          deps.log('warn', 'The transaction just written ahead is ABSENT on chain after the re-poll and the node said "inputs spent" — a definitive rejection; keeping the ordinary fail-and-retry path (KS-726)', {
            anchorId, txHash: known, error: message, armed: arm.isArmed(),
          });
          guardedOn = known;
        } else {
          // No hash of ours to re-poll — fall through. Swallowing this would
          // strand the anchor with no record and no retry (see NOT HANDLED).
          deps.log('warn', 'Node reported an already-included transaction, but this anchor has no known tx hash to re-poll (KS-705)', {
            anchorId, error: message,
          });
        }
      }

      const currentRetry = anchor.retryCount + 1;

      // KS-1384 F0b (design §3.7, cell q3): the writes report, and the retry follows only a write that matched
      // exactly its one row. After guard 3 they expect the attempt's own last write ('submitting', the refused
      // hash): a row that moved during the re-poll (a newer call re-armed it) matches 0 and is left to that call,
      // and a write that did not run (null) schedules nothing. Before F0 both were read as success.
      const failedCount = await deps.updateStatus(anchorId, {
        status: 'failed',
        errorMessage: message || 'Cardano submission failed',
        ...(guardedOn ? { expectStatus: 'submitting', expectTransactionHash: guardedOn } : {}),
      });
      if (failedCount !== 1) {
        deps.log('warn', 'The failed write did not match its row — no retry scheduled (KS-1384)', { anchorId, count: failedCount, error: message });
        return;
      }
      await deps.bumpRetryCount(anchorId);

      deps.log('error', 'Anchor submission failed', { anchorId, error: message, retryCount: currentRetry });

      // Retry up to `maxRetries` times with backoff.
      // KS-535: reset to 'pending' BEFORE the backoff timer starts, not inside
      // it — this makes `status: 'failed'` TERMINAL (no retry coming), which
      // originate's poller/reconciler relies on to propagate a failure to the
      // document. Previously the row sat as 'failed' for the 5–10s backoff
      // window, so an observer could not distinguish "retrying" from "given
      // up". (Trade-off: a crash during the backoff now leaves the row
      // 'pending' instead of 'failed' — a stuck-pending, same as any other
      // restart-lost anchor; anchoring has no restart re-queue either way.)
      if (currentRetry < maxRetries) {
        const backoff = currentRetry * backoffMsPerAttempt;
        deps.log('info', `Scheduling retry in ${backoff}ms`, { anchorId, retryCount: currentRetry });
        const pendingCount = await deps.updateStatus(anchorId, {
          status: 'pending',
          ...(guardedOn ? { expectStatus: 'failed', expectTransactionHash: guardedOn } : {}),
        });
        if (pendingCount === 1) deps.scheduleRetry(anchorId, backoff);
        else deps.log('warn', 'The pending reset did not match its row — no retry scheduled (KS-1384)', { anchorId, count: pendingCount });
      }
    }
  };
}
