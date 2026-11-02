/**
 * =============================================================================
 * CARDANO INTEGRATION — ORCHESTRATION
 * =============================================================================
 * Top-level module that initialises the Blockfrost provider and platform wallet,
 * then exposes high-level functions for anchoring documents on Cardano.
 *
 * Behaviour:
 *   - When DEMO_MODE=true → uses MockAnchoringProvider (no API keys required)
 *   - When BLOCKFROST_API_KEY + PLATFORM_WALLET_MNEMONIC are set → real Cardano
 *   - When either is missing → gracefully disabled (caller falls back to mock)
 * =============================================================================
 */

import {
  initProvider, fetchProtocolParams, fetchUtxosAll, fetchLiveTip, getTransaction, submitTransaction, ProtocolParams,
} from './provider';
import { initWallet, PlatformWallet } from './wallet';
import { buildAnchorTransaction } from './transaction';
import { waitForConfirmation, ConfirmationResult } from './confirmation';
import { MockAnchoringProvider } from '../mocks/mockProvider';
import { logger } from '../utils/logger';
import { platformWalletView, type OutRef, type ViewUtxo } from '../walletView';
import { spendFromView, payloadDigest } from '../walletSpend';
import { platformBootArm } from '../attemptFamily';

/**
 * KS-1384 F0b: every live tip read in this process goes through here, so each one feeds the boot arm
 * (attemptFamily.ts). The first answered read after start fixes S_boot.
 */
export async function observedLiveTip() {
  const tip = await fetchLiveTip();
  platformBootArm.observe(tip?.slot);
  return tip;
}

let cardanoReady = false;
let cardanoConfigured = false;
let demoMode = false;
let mockProvider: MockAnchoringProvider | null = null;
let wallet: PlatformWallet | null = null;
let cachedParams: ProtocolParams | null = null;
let paramsRefreshedAt = 0;

const PARAMS_CACHE_TTL_MS = 5 * 60 * 1000; // 5 minutes

/**
 * Check whether the service is running in demo mode.
 */
export function isDemoMode(): boolean {
  return demoMode;
}

/**
 * Initialise the Cardano integration.
 * Returns true if blockchain operations are available (real or mock).
 */
export async function initCardano(network: string): Promise<boolean> {
  // Check for demo mode — forbidden in production
  if (process.env.DEMO_MODE === 'true') {
    if (process.env.NODE_ENV === 'production') {
      logger.error('[Cardano] FATAL: DEMO_MODE=true is not allowed in production. Configure BLOCKFROST_API_KEY and PLATFORM_WALLET_MNEMONIC for real Cardano integration.');
      process.exit(1);
    }
    demoMode = true;
    mockProvider = new MockAnchoringProvider();
    cardanoReady = true;
    logger.warn('[Cardano] ⚠ DEMO_MODE active — using MockAnchoringProvider. DO NOT USE IN PRODUCTION.');
    return true;
  }

  const apiKey = process.env.BLOCKFROST_API_KEY;
  const mnemonic = process.env.PLATFORM_WALLET_MNEMONIC;

  if (!apiKey || !mnemonic) {
    logger.info('[Cardano] BLOCKFROST_API_KEY or PLATFORM_WALLET_MNEMONIC not set — mock mode');
    return false;
  }

  // KS-671 (#728 review): CONFIGURED is not READY, and /health could not tell
  // them apart. If the quota is already exhausted at container start,
  // fetchProtocolParams() fails and this function returns false — so
  // isCardanoReady() is false and the endpoint reported `mode: 'mock'`,
  // `status: 'healthy'`, exactly as if no credentials had ever been supplied,
  // with `reachability: 'failing'` sitting in the body unused. That is the
  // state after ANY restart during an outage. Recording configuration
  // separately from readiness is what lets /health say "we meant to be on
  // chain and we are not" instead of "we were never trying".
  cardanoConfigured = true;

  try {
    // Initialise Blockfrost provider
    const provider = initProvider(apiKey, network);
    if (!provider) {
      logger.warn('[Cardano] Failed to initialise Blockfrost provider');
      return false;
    }

    // Initialise platform wallet from mnemonic
    wallet = initWallet(mnemonic, network);
    logger.info(`[Cardano] Platform wallet: ${wallet.address}`);

    // Fetch and cache protocol parameters
    cachedParams = await fetchProtocolParams();
    if (!cachedParams) {
      logger.warn('[Cardano] Failed to fetch protocol parameters');
      return false;
    }
    paramsRefreshedAt = Date.now();

    cardanoReady = true;
    logger.info(`[Cardano] Integration ready — network: ${network}`);
    return true;
  } catch (err: any) {
    logger.error(`[Cardano] Initialisation failed: ${err?.message}`);
    return false;
  }
}

/**
 * Check whether real Cardano operations are available.
 */
export function isCardanoReady(): boolean {
  return cardanoReady;
}

/**
 * Were real-chain credentials SUPPLIED? True even when initialisation then
 * failed — that distinction is the whole point (see initCardano).
 */
export function isCardanoConfigured(): boolean {
  return cardanoConfigured;
}

/** Test seam — resets the configured flag. Not used at runtime. */
export function __resetCardanoConfigured(): void {
  cardanoConfigured = false;
}

/**
 * Get the platform wallet address.
 */
export function getWalletAddress(): string | null {
  return wallet?.address ?? null;
}

/**
 * Ensure protocol parameters are fresh (refresh if stale).
 */
async function ensureFreshParams(): Promise<ProtocolParams> {
  if (!cachedParams || Date.now() - paramsRefreshedAt > PARAMS_CACHE_TTL_MS) {
    const fresh = await fetchProtocolParams();
    if (fresh) {
      cachedParams = fresh;
      paramsRefreshedAt = Date.now();
    }
  }
  if (!cachedParams) throw new Error('Protocol parameters unavailable');
  return cachedParams;
}

// ---------------------------------------------------------------------------
// PUBLIC API
// ---------------------------------------------------------------------------

export interface AnchorSubmitResult {
  txHash: string;
  fee: number;
  /** KS-1384 F0: the signed body's inputs, and those that came from pass 1 with their lovelace (rule 0's u_F). */
  inputs?: OutRef[];
  pass1Inputs?: ViewUtxo[];
}

/**
 * Options for {@link submitAnchor}.
 */
export interface AnchorSubmitOptions {
  /**
   * KS-726 — write-ahead hook. Called with the deterministic transaction hash
   * AFTER the transaction is built and signed but BEFORE it is submitted.
   *
   * A Cardano transaction hash is the blake2b-256 of the serialised transaction
   * body (`transaction.ts:126`), so it is fully known locally before the network
   * ever sees the transaction. Persisting it here — rather than learning it from
   * the submit reply — is what makes a LOST reply survivable: if `submit` throws
   * after the node already accepted the transaction, the row still names it, and
   * the reconciler can settle it instead of the retry path minting a second
   * fee-paying transaction for one document.
   *
   * Ordering is the contract, and it is load-bearing in both directions:
   *   - it runs before submit, so a lost reply cannot orphan a paid transaction;
   *   - if it THROWS, the submit does not happen at all, so we never spend a fee
   *     for a transaction no row can name.
   *
   * ⚠ THE SECOND HALF IS INERT IN THE PRODUCTION WIRING, and saying so is the
   * point (#805 review F3). The only production hook calls
   * `dbUpdateAnchorStatus`, which swallows every error
   * (`catch (err) { log('warn', …) }`), so it CANNOT throw. A DB failure during
   * the write-ahead therefore does not stop the submit — the transaction is
   * sent and paid for against a row that may not name it.
   *
   * So the guarantee this callback offers is BEST-EFFORT, not absolute, and the
   * PR body's "any failure at any point leaves a row that names the
   * transaction" should be read that way. The residual window is closed on the
   * other side instead: both write-ahead guards now re-write the hash
   * themselves (#805 F2), so a swallowed write still ends with a
   * reconciler-visible row. Changing the swallow is a much larger decision than
   * this ticket and is deliberately not taken here.
   *
   * Optional. Omitting it leaves the pre-KS-726 behaviour exactly as it was,
   * which is what keeps the two-argument call sites — including the `deps.submit`
   * that #756 extracted into `anchorSubmission.ts` — type-compatible.
   *
   * KS-1384 F0: the second half is now LIVE. Both production hooks throw unless their write matched the rows
   * the spender needs (`WriteAheadDeclined` / `WriteAheadUnavailable`, anchorSubmission.ts), so a write-ahead
   * that did not land stops the submit, and the transaction is admitted to the wallet view only after it
   * resolves (the fourth review's M-3).
   */
  onSigned?: (txHash: string) => Promise<void>;
  /** KS-1384 F0: who this spend is for, as the wallet view records it, and the family outpoint if any. */
  spend?: {
    kind?: 'single' | 'batch';
    anchorIds?: string[];
    required?: OutRef;
    extraClaims?: Iterable<string>;
  };
  /** KS-1384 F0b: the signed body's facts, before the write-ahead (the family records its member from them). */
  onBuilt?: (facts: { txHash: string; ttlSlot: number; pass1Inputs: ViewUtxo[] }) => void;
}

/** KS-1384 F0 (design §3.3): "a bounded refetch (for example 6 x 5 s)" before `NoSpendableUtxo`. */
const REFETCH_ATTEMPTS = 6;
const REFETCH_DELAY_MS = 5_000;

/**
 * Submit a single document anchor transaction to Cardano.
 * In demo mode, delegates to MockAnchoringProvider for instant results.
 *
 * @param metadataLabel   - CIP metadata label (674 for single anchors)
 * @param metadataPayload - The metadata object to embed in the transaction
 */
export async function submitAnchor(
  metadataLabel: number,
  metadataPayload: object,
  options: AnchorSubmitOptions = {},
): Promise<AnchorSubmitResult> {
  // Demo mode: delegate to mock provider.
  //
  // KS-726 — `onSigned` is deliberately NOT called here, and this carve-out is
  // a control property rather than an omission: name what it prevents, or the
  // next reader simplifies it away.
  //
  // MockAnchoringProvider returns a BARE 64-hex sha256 (`mocks/mockProvider.ts`),
  // which does NOT match `FABRICATED_TX_PREFIX` (/^(tx_sim_|mock_tx_|mock_batch_tx_|tx_)/) and
  // DOES match the /^[0-9a-f]{64}$/i test that both write-ahead guards use to
  // decide "this row names a real transaction" (`REAL_TX_64HEX` in
  // anchorSubmission.ts, `REAL_TX_64HEX_RETRY` on the batch path in index.ts).
  // Measured in #764, not assumed.
  //
  // So writing ahead in demo mode would make a mock hash indistinguishable from
  // a real one to the failure path, with two consequences neither this change
  // nor KS-726 ever intended: demo anchors would stop retrying, and the
  // reconciler would poll the chain for a transaction that was never submitted
  // and then fail it after `giveUpMs`.
  //
  // The mislabelling predates KS-726; what is new is that KS-726 is the first
  // thing to make BEHAVIOUR depend on it. Skipping the write-ahead here keeps
  // the defect where it was rather than building on it. The label itself is
  // KS-587's to fix.
  if (demoMode && mockProvider) {
    const contentHash = JSON.stringify(metadataPayload);
    const result = await mockProvider.submitAnchor(contentHash);
    return { txHash: result.transactionHash, fee: Number(result.fee) };
  }

  if (!cardanoReady || !wallet) {
    throw new Error('Cardano integration not ready');
  }

  const params = await ensureFreshParams();
  const w = wallet;

  // KS-1384 F0: build from the wallet view's candidates, not a bare fetched page (walletSpend.ts). The
  // KS-726 write-ahead runs inside, after signing and before the network is involved: the hash is derived
  // locally from the signed body, so every failure from there on leaves a row that names the transaction. If
  // the hook throws we deliberately do not submit — see AnchorSubmitOptions.onSigned.
  const spent = await spendFromView(
    {
      view: platformWalletView,
      fetchUtxos: () => fetchUtxosAll(w.address),
      build: (selection) => buildAnchorTransaction(w, params, metadataLabel, metadataPayload, selection),
      submit: submitTransaction,
      liveTip: observedLiveTip,
      lookup: async (h) => {
        const tx = await getTransaction(h);
        return tx ? { validContract: tx.valid_contract } : null;
      },
      now: Date.now,
      sleep: (ms) => new Promise((resolve) => setTimeout(resolve, ms)),
      refetchAttempts: REFETCH_ATTEMPTS,
      refetchDelayMs: REFETCH_DELAY_MS,
    },
    {
      kind: options.spend?.kind ?? 'single',
      anchorIds: options.spend?.anchorIds ?? [],
      payloadDigest: payloadDigest(metadataLabel, metadataPayload),
      ...(options.spend?.required ? { required: options.spend.required } : {}),
      ...(options.spend?.extraClaims ? { extraClaims: options.spend.extraClaims } : {}),
      ...(options.onSigned ? { onSigned: options.onSigned } : {}),
      ...(options.onBuilt ? { onBuilt: options.onBuilt } : {}),
    },
  );

  if (spent.txHash !== spent.built.txHash) {
    logger.warn('[Cardano] Hash mismatch', { expected: spent.built.txHash, got: spent.txHash });
  }

  return { txHash: spent.txHash, fee: spent.fee, inputs: spent.built.inputs, pass1Inputs: spent.pass1Inputs };
}

/**
 * Submit an anchor and wait for on-chain confirmation.
 * Returns both submission details and confirmation data.
 * In demo mode, confirmation is instant via MockAnchoringProvider.
 */
export async function submitAndConfirmAnchor(
  metadataLabel: number,
  metadataPayload: object,
  onStatusUpdate?: (attempt: number, status: string) => void,
  options: AnchorSubmitOptions = {},
): Promise<AnchorSubmitResult & ConfirmationResult> {
  const submission = await submitAnchor(metadataLabel, metadataPayload, options);

  // Demo mode: instant confirmation via mock
  if (demoMode && mockProvider) {
    const confirmation = await mockProvider.waitForConfirmation(submission.txHash);
    return { ...submission, ...confirmation };
  }

  const confirmation = await waitForConfirmation(
    submission.txHash,
    30,      // max attempts
    10_000,  // initial delay 10s
    60_000,  // max delay 60s
    onStatusUpdate,
  );

  return { ...submission, ...confirmation };
}

// Re-exports
export { ConfirmationResult } from './confirmation';
export { waitForConfirmation } from './confirmation';
export { getChainHealth, CHAIN_DEGRADED_AFTER_FAILURES, CHAIN_HEALTH_STALE_MS } from './provider';
export type { ChainHealth, ChainReachability } from './provider';
