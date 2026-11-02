/**
 * =============================================================================
 * KS-1384 F0 — spending the platform wallet through the wallet view
 * (design rev 4 §3.3, §3.5; the fourth review's M-3, m-6)
 * =============================================================================
 * One build, from candidates the view allows, in the order the design fixes:
 *   1. settle any LIVE spender whose encoded TTL an ANSWERED live tip has passed: one lookup each; found ->
 *      confirmed (with `valid_contract`, M-1), not found -> dead. An unanswered tip or lookup settles nothing.
 *   2. fetch every UTxO (all pages), take the view's candidates;
 *   3. build from pass 1; only when pass 1 cannot pay, build from pass 2 (pass 1 plus the add-backs);
 *   4. nothing can pay: refetch a bounded number of times, then `NoSpendableUtxo` (the caller waits, §3.5);
 *   5. the write-ahead hook runs; it THROWS unless its write matched the rows this spender needs (M-3: one for a
 *      single anchor, all N for a batch). A transaction is admitted to the view only after it resolves, so a
 *      signed transaction that was never sent can never hold a coin;
 *   6. submit, and record what came back: accepted, refused (the node answered no: dead at once, its add-backs
 *      dropped) or lost (no answer: it stays live).
 *
 * Pure of process state: the view, the provider calls and the clock are injected (bootless unit tests, the
 * same reason as anchorSubmission.ts). `cardano/index.ts` wires the production instances.
 * =============================================================================
 */

import { createHash } from 'crypto';
import { WalletView, refKey, type OutRef, type SpenderKind, type ViewUtxo } from './walletView';
import {
  isInsufficientInputError,
  type AnchorBuildSelection,
  type BuildUtxo,
  type BuiltAnchorTransaction,
} from './cardano/transaction';
import { isChainReachableError } from './cardano/provider';
import { toCardanoMetadatum } from './cardano/cardanoMetadatum';

/**
 * Every coin is claimed, or nothing fetched can pay, after the bounded refetch. Nothing was signed. This is
 * not a failure of the anchor and spends no retry (design §3.5): the caller waits and re-queues.
 */
export class NoSpendableUtxo extends Error {
  constructor(readonly fetched: number, readonly claimed: number) {
    super(`no spendable coin in the platform wallet (${fetched} listed, ${claimed} claimed); nothing was signed`);
    this.name = 'NoSpendableUtxo';
  }
}

/**
 * The family outpoint is not among this build's candidates: rule 4 decides, the build does not run. `listed`
 * says whether the fetched page still lists it (then something of ours claims it) or not (then something spent it).
 */
export class FamilyOutpointUnavailable extends Error {
  constructor(readonly outpoint: OutRef, readonly listed: boolean) {
    super(`the family outpoint ${refKey(outpoint)} is not spendable now (${listed ? 'claimed' : 'not listed'}); nothing was signed`);
    this.name = 'FamilyOutpointUnavailable';
  }
}

/**
 * The family and A1 key (design §3.4): label plus the ENCODED payload, the exact JSON the builder attaches
 * (`transaction.ts`, `toCardanoMetadatum`). Two payloads that decode alike but encode differently are different.
 */
export function payloadDigest(metadataLabel: number, metadataPayload: object): string {
  return createHash('sha256')
    .update(`${metadataLabel}:${JSON.stringify(toCardanoMetadatum(metadataPayload))}`)
    .digest('hex');
}

const lovelaceOf = (u: BuildUtxo): bigint =>
  BigInt(u.amount.find((a) => a.unit === 'lovelace')?.quantity ?? '0');

export const toViewUtxo = (u: BuildUtxo): ViewUtxo =>
  ({ txHash: u.tx_hash, index: u.output_index, lovelace: lovelaceOf(u) });

const toBuildUtxo = (v: ViewUtxo): BuildUtxo =>
  ({ tx_hash: v.txHash, output_index: v.index, amount: [{ unit: 'lovelace', quantity: v.lovelace.toString() }] });

export interface SpendDeps {
  view: WalletView;
  fetchUtxos: () => Promise<BuildUtxo[]>;
  build: (selection: AnchorBuildSelection) => Promise<BuiltAnchorTransaction>;
  submit: (txCborHex: string) => Promise<string>;
  /** An ANSWERED live tip, or null (provider.ts `fetchLiveTip`). */
  liveTip: () => Promise<{ slot: number } | null>;
  /** A transaction's on-chain record: null = the chain answered "not found"; throws when it could not answer. */
  lookup: (txHash: string) => Promise<{ validContract?: boolean } | null>;
  now: () => number;
  sleep: (ms: number) => Promise<void>;
  /** Design §3.3: "a bounded refetch (for example 6 x 5 s)". */
  refetchAttempts: number;
  refetchDelayMs: number;
}

export interface SpendRequest {
  kind: Exclude<SpenderKind, 'thread-mint'>;
  anchorIds: string[];
  payloadDigest: string;
  /** The family outpoint: must be a candidate, else FamilyOutpointUnavailable (rule 4 owns that case). */
  required?: OutRef;
  /** Outpoints held against this build on top of the view's own claims (rule 2: another family's u_F). */
  extraClaims?: Iterable<string>;
  /** The write-ahead. Resolves only when its write matched the rows this spender needs; throws otherwise. */
  onSigned?: (txHash: string) => Promise<void>;
  /** KS-1384 F0b: the signed body's facts, before the write-ahead (the family records its member from them). */
  onBuilt?: (facts: { txHash: string; ttlSlot: number; pass1Inputs: ViewUtxo[] }) => void;
}

export interface SpendResult {
  txHash: string;
  fee: number;
  built: BuiltAnchorTransaction;
  /** 1 or 2: which pass paid (design C). */
  pass: 1 | 2;
  /** The built transaction's inputs that came from pass 1, with their lovelace (the u_F choice, rule 0). */
  pass1Inputs: ViewUtxo[];
}

/**
 * Step 1: a live spender past its encoded TTL by an answered tip is settled by one lookup. Never on the local
 * clock (the review's M1), and never on an unanswered read.
 */
export async function settleExpiredSpenders(deps: Pick<SpendDeps, 'view' | 'liveTip' | 'lookup' | 'now'>): Promise<void> {
  const live = deps.view.liveTxHashes();
  if (live.length === 0) return;
  const tip = await deps.liveTip();
  if (!tip) return;
  for (const h of live) {
    const rec = deps.view.record(h);
    if (!rec || tip.slot <= rec.ttlSlot) continue;
    try {
      const onChain = await deps.lookup(h);
      if (onChain) deps.view.markConfirmed(h, deps.now(), onChain.validContract);
      else deps.view.markDead(h);
    } catch {
      // the chain did not answer: settle nothing
    }
  }
}

export async function spendFromView(deps: SpendDeps, req: SpendRequest): Promise<SpendResult> {
  await settleExpiredSpenders(deps);
  for (let attempt = 0; ; attempt++) {
    const fetched = await deps.fetchUtxos();
    const now = deps.now();
    const c = deps.view.candidates(fetched.map(toViewUtxo), now, req.extraClaims ?? []);
    const pass1Keys = new Set(c.pass1.map(refKey));
    const pass1 = fetched.filter((u) => pass1Keys.has(`${u.tx_hash}#${u.output_index}`));

    if (req.required && !pass1Keys.has(refKey(req.required))) {
      const k = refKey(req.required);
      throw new FamilyOutpointUnavailable(req.required, fetched.some((u) => `${u.tx_hash}#${u.output_index}` === k));
    }

    let built: BuiltAnchorTransaction | undefined;
    let pass: 1 | 2 = 1;
    if (pass1.length > 0) {
      try {
        built = await deps.build({ candidates: pass1, required: req.required });
      } catch (err) {
        if (!isInsufficientInputError(err)) throw err;
      }
    }
    if (!built && c.addBacks.length > 0) {
      try {
        built = await deps.build({ candidates: [...pass1, ...c.addBacks.map(toBuildUtxo)], required: req.required });
        pass = 2;
      } catch (err) {
        if (!isInsufficientInputError(err)) throw err;
      }
    }

    if (built) {
      const inputKeys = new Set(built.inputs.map(refKey));
      const usedAddBacks = pass === 2 ? c.addBacks.filter((a) => inputKeys.has(refKey(a))) : [];
      const pass1Inputs = c.pass1.filter((u) => inputKeys.has(refKey(u)));
      req.onBuilt?.({ txHash: built.txHash, ttlSlot: built.ttlSlot, pass1Inputs });
      // M-3: admitted only after the write-ahead resolves (it throws unless its write matched the rows needed).
      if (req.onSigned) await req.onSigned(built.txHash);
      deps.view.admit({
        txHash: built.txHash,
        kind: req.kind,
        inputs: built.inputs,
        collateral: built.collateral,
        ...(built.collateralReturn ? { collateralReturn: built.collateralReturn } : {}),
        ownOutputs: built.ownOutputs,
        ttlSlot: built.ttlSlot,
        anchorIds: req.anchorIds,
        payloadDigest: req.payloadDigest,
        ...(usedAddBacks.length ? { usedAddBacks } : {}),
      });
      try {
        const submitted = await deps.submit(built.txCborHex);
        deps.view.recordSubmit(built.txHash, 'accepted');
        return { txHash: submitted || built.txHash, fee: built.fee, built, pass, pass1Inputs };
      } catch (err) {
        // The node answered no (a status code) -> refused: dead at once. No answer -> lost: it may be in a mempool.
        deps.view.recordSubmit(built.txHash, isChainReachableError(err) ? 'refused' : 'lost');
        throw err;
      }
    }

    if (attempt >= deps.refetchAttempts) {
      throw new NoSpendableUtxo(fetched.length, fetched.length - pass1.length);
    }
    await deps.sleep(deps.refetchDelayMs);
  }
}
