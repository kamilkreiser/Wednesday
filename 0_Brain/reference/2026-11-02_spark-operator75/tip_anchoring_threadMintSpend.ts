/**
 * =============================================================================
 * KS-1384 F0c — thread-mint through the wallet lock and the wallet view
 * (the fourth review's B1, M-1, M-2, M-3; design rev 4 §3.6 S3)
 * =============================================================================
 * Before F0 thread-mint spent the platform wallet with NO lock (KS-1819) and picked its seed from a fresh provider
 * read. Putting it behind the lock naively (rev 4) made it worse: the single-anchor path holds the lock through its
 * ~27-minute confirmation poll, originate calls thread-mint with a bare fetch and gives up long before that, and the
 * queued mint would then sign and pay after the caller had gone, leaving a paid NFT no registry row names (B1).
 *
 * So, here:
 *   - the lock is taken with a BOUNDED wait (`withWalletLockWithin`, 30 s, well under the caller's timeout); when
 *     it expires nothing is signed and the caller gets a 503 (B1a);
 *   - thread-mint NEVER waits for a coin: no candidate answers 503 at once (B1b), not the anchors' 2 h wait;
 *   - immediately before signing, a caller that has gone away stops it (B1c);
 *   - the seed and every input and collateral come from the view's pass-1 candidates (M-2; lucid's
 *     `presetWalletInputs`, never empty);
 *   - the mint enters the view AT SIGNING, from its signed body, with its collateral and collateral return (M-3:
 *     it has no row and no write-ahead), so the next anchor's build avoids its coins while it is live;
 *   - it confirms OUTSIDE the lock, and the view learns `valid_contract` (M-1: a valid mint never spent its
 *     collateral, so the collateral is offered again).
 * The OFF-by-default switch and the owner rule on these routes are KS 1819 / KS 1820's, not this file's.
 * =============================================================================
 */

import { WalletView, refKey } from './walletView';
import { WalletLockTimeout } from './anchorSubmission';
import { parseSignedBody, type BuildUtxo } from './cardano/transaction';
import { toViewUtxo } from './walletSpend';
import { isChainReachableError } from './cardano/provider';

/** B1: the bounded wait for the wallet lock (the review's example, well under originate's fetch timeout). */
export const THREAD_MINT_LOCK_WAIT_MS = 30_000;

/** B1b: nothing spendable now. Nothing was signed; thread-mint does not wait. */
export class ThreadMintNoCoin extends Error {
  constructor(readonly listed: number) {
    super(`no spendable coin in the platform wallet (${listed} listed, all claimed); nothing was signed`);
    this.name = 'ThreadMintNoCoin';
  }
}

/** B1c: the caller went away before signing. Nothing was signed. */
export class ThreadMintCallerGone extends Error {
  constructor() {
    super('the caller went away before the mint was signed; nothing was signed');
    this.name = 'ThreadMintCallerGone';
  }
}

/** The three refusals that answer 503 BEFORE anything is signed; null for anything else. */
export function threadMintUnavailable(err: unknown): { status: 503; code: 'SERVICE_UNAVAILABLE'; message: string } | null {
  if (err instanceof WalletLockTimeout) {
    return { status: 503, code: 'SERVICE_UNAVAILABLE', message: 'The platform wallet is busy; nothing was signed. Retry later.' };
  }
  if (err instanceof ThreadMintNoCoin) {
    return { status: 503, code: 'SERVICE_UNAVAILABLE', message: 'No spendable coin in the platform wallet; nothing was signed. Retry later.' };
  }
  if (err instanceof ThreadMintCallerGone) {
    return { status: 503, code: 'SERVICE_UNAVAILABLE', message: 'The request ended before signing; nothing was signed.' };
  }
  return null;
}

/** A provider UTxO in lucid's shape, at the wallet's own address. */
export function toLucidUtxo(u: BuildUtxo, address: string) {
  return {
    txHash: u.tx_hash,
    outputIndex: u.output_index,
    address,
    assets: Object.fromEntries(u.amount.map((a) => [a.unit, BigInt(a.quantity)])) as Record<string, bigint>,
    datumHash: null,
    datum: null,
    scriptRef: null,
  };
}

export interface ThreadMintSpend {
  candidates: ReturnType<typeof toLucidUtxo>[];
  beforeSign: () => void;
  onSigned: (txCborHex: string, txHash: string) => void;
}

export interface ThreadMintDeps<R extends { mintTxHash: string }> {
  view: WalletView;
  walletAddress: string;
  fetchUtxos: () => Promise<BuildUtxo[]>;
  lockWithin: <T>(fn: () => Promise<T>, maxWaitMs: number) => Promise<T>;
  callerGone: () => boolean;
  mint: (spend: ThreadMintSpend) => Promise<R>;
  confirm: (txHash: string) => Promise<{ confirmed: boolean; validContract?: boolean }>;
  now: () => number;
}

export async function mintThroughView<R extends { mintTxHash: string }>(
  deps: ThreadMintDeps<R>,
  lockWaitMs: number = THREAD_MINT_LOCK_WAIT_MS,
): Promise<R> {
  let signedHash: string | undefined;
  const result = await deps.lockWithin(async () => {
    const fetched = await deps.fetchUtxos();
    const c = deps.view.candidates(fetched.map(toViewUtxo), deps.now());
    const keys = new Set(c.pass1.map(refKey));
    const pass1 = fetched.filter((u) => keys.has(`${u.tx_hash}#${u.output_index}`));
    if (pass1.length === 0) throw new ThreadMintNoCoin(fetched.length);
    try {
      const r = await deps.mint({
        candidates: pass1.map((u) => toLucidUtxo(u, deps.walletAddress)),
        beforeSign: () => { if (deps.callerGone()) throw new ThreadMintCallerGone(); },
        onSigned: (txCborHex, txHash) => {
          signedHash = txHash;
          deps.view.admit({ txHash, kind: 'thread-mint', ...parseSignedBody(txCborHex, deps.walletAddress), anchorIds: [] });
        },
      });
      if (signedHash) deps.view.recordSubmit(signedHash, 'accepted');
      return r;
    } catch (err) {
      if (signedHash) deps.view.recordSubmit(signedHash, isChainReachableError(err) ? 'refused' : 'lost');
      throw err;
    }
  }, lockWaitMs);
  if (signedHash) {
    const h = signedHash;
    deps.confirm(h)
      .then((c) => { if (c.confirmed) deps.view.markConfirmed(h, deps.now(), c.validContract); })
      .catch(() => undefined);
  }
  return result;
}
