/**
 * =============================================================================
 * TRANSACTION CONFIRMATION POLLER
 * =============================================================================
 * Polls Blockfrost for transaction confirmation status with exponential backoff.
 * =============================================================================
 */

import { getTransaction } from './provider';

export interface ConfirmationResult {
  confirmed: boolean;
  blockHash?: string;
  blockNumber?: number;
  slot?: number;
  confirmations?: number;
  error?: string;
  /**
   * KS-726 (#805 tier-1 gate, F1): how many attempts REACHED the chain — the
   * provider answered, with the transaction or with "not found" — and how many
   * THREW (5xx, 402 quota, DNS, socket). `confirmed: false` with `polled: 0`
   * means the chain was never asked, which says nothing about the transaction;
   * a caller that reads it as "absent" re-submits a transaction that may
   * already be in a block. Both are counts of what ran, never a verdict.
   */
  polled?: number;
  errored?: number;
  /**
   * KS-1171 (Kam's ruling `c`, live board 2026-09-25 12:49:07 AEST, card
   * `secuura-ks1171-when-is-an-anchor-absent`): WHEN the chain last answered, not just how often.
   *
   * `polled` alone cannot tell an early "not found" from a late one, and the difference decides
   * whether "absent" is trustworthy: Blockfrost answers 404 until a transaction is in a block AND
   * indexed, so an answer seconds after the node's 400 says almost nothing, while the same answer a
   * minute later says a great deal. `lastAnsweredElapsedMs` is measured from the START OF POLLING,
   * which is at or after the 400 — so it is always <= the true elapsed-since-400, and any threshold
   * applied to it is strictly conservative: it can only ever retry LESS than the rule allows.
   */
  lastAnsweredAttempt?: number;
  lastAnsweredElapsedMs?: number;
  /**
   * KS-1384 F0 (the fourth review's M-1): the `txs` answer's `valid_contract`. False means phase 2 failed: the
   * chain spent the COLLATERAL and not the regular inputs. Absent when the answer did not carry it.
   */
  validContract?: boolean;
}

/**
 * Wait for a transaction to appear on chain.
 *
 * @param txHash               - Transaction hash to monitor
 * @param maxAttempts          - Maximum number of polling attempts (default 30)
 * @param initialDelayMs       - Initial delay between attempts in ms (default 10000)
 * @param maxDelayMs           - Maximum delay between attempts (default 60000)
 * @param onStatusUpdate       - Optional callback for status updates
 */
export async function waitForConfirmation(
  txHash: string,
  maxAttempts = 30,
  initialDelayMs = 10_000,
  maxDelayMs = 60_000,
  onStatusUpdate?: (attempt: number, status: string) => void,
): Promise<ConfirmationResult> {
  let delay = initialDelayMs;
  // KS-726 (#805 gate F1): count what each attempt DID. `getTransaction` returns
  // null when the chain answered "not found" (a 404 — provider.ts) and throws
  // when it could not answer; the two must not collapse into one `confirmed:
  // false`, because the caller's next step differs (re-submit vs rest).
  let polled = 0;
  let errored = 0;
  // KS-1171: the clock the ABSENT rule is read against. Started here, which is at or after the
  // node's 400 — see `lastAnsweredElapsedMs` on the result type for why that direction is safe.
  const startedAtMs = Date.now();
  let lastAnsweredAttempt: number | undefined;
  let lastAnsweredElapsedMs: number | undefined;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      const tx = await getTransaction(txHash);
      polled += 1;
      // The chain ANSWERED on this attempt (with the transaction or with "not found"); a throw
      // never reaches here. Recorded for KS-1171's two-condition ABSENT rule.
      lastAnsweredAttempt = attempt;
      lastAnsweredElapsedMs = Date.now() - startedAtMs;

      if (tx) {
        return {
          confirmed: true,
          blockHash: tx.block,
          blockNumber: tx.block_height,
          slot: tx.slot,
          confirmations: 1,
          polled,
          errored,
          lastAnsweredAttempt,
          lastAnsweredElapsedMs,
          ...(typeof tx.valid_contract === 'boolean' ? { validContract: tx.valid_contract } : {}),
        };
      }

      if (onStatusUpdate) {
        onStatusUpdate(attempt, `pending (attempt ${attempt}/${maxAttempts})`);
      }
    } catch (err: any) {
      errored += 1;
      if (onStatusUpdate) {
        onStatusUpdate(attempt, `error: ${err?.message}`);
      }
    }

    // Exponential backoff with jitter
    await sleep(delay + require('crypto').randomInt(0, 2000));
    delay = Math.min(delay * 1.5, maxDelayMs);
  }

  return {
    confirmed: false,
    polled,
    errored,
    lastAnsweredAttempt,
    lastAnsweredElapsedMs,
    error: polled === 0
      ? `Transaction ${txHash} could not be checked: ${errored}/${maxAttempts} attempts failed to reach the chain`
      : `Transaction ${txHash} not confirmed after ${maxAttempts} attempts (${polled} answered, ${errored} failed)`,
  };
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}
