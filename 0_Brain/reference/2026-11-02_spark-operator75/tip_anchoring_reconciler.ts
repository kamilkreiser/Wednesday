/**
 * =============================================================================
 * KS-584 (P3) — stuck-anchor reconciler
 * =============================================================================
 * The in-process confirmation poll dies with the service (KS-535) and its
 * 30-attempt window is shorter than a congested chain, so anchor_store rows
 * can sit 'pending'/'submitted' forever while their tx is settled on-chain —
 * the stale state behind the QA-High false negative (an anonymous verifier
 * told a settled anchor is not anchored, 2026-08-11). Kam's ruling: fix the
 * CAUSE — make the stored status honest — rather than preferring-confirmed
 * over wrong data at read time.
 *
 * Properties:
 *   - idempotent; survives restarts by construction (reads the DB, not
 *     process state) — except the answered-pass count below, which is in
 *     memory and so starts again from zero after a restart (safe: it can
 *     only delay a `failed` write);
 *   - only ever moves a row TOWARD chain truth: real-tx rows to 'confirmed'
 *     when the chain has the tx in a block, or to terminal 'failed' when the
 *     tx has not appeared within the give-up window (its inputs were spent by
 *     something else — the KS-535 `All inputs are spent` class);
 *   - fabricated refs (`tx_sim_`/`mock_tx_`) are never chain-checked — KS-587
 *     owns those rows;
 *   - KS-1384 F-a (KS-1808): the give-up window is measured from the row's
 *     LAST WRITE (`updated_at`), not from `created_at`. A row re-armed by a
 *     later anchor request starts its window again; on `created_at` an old
 *     row was given up at its first pass after a re-anchor;
 *   - KS-1384 F-a (KS-1810): a row is marked failed only after TWO
 *     CONSECUTIVE passes past the window in which the chain ANSWERED "not
 *     found". A pass in which the provider could not answer (an outage, a
 *     quota error) never fails a row and resets the count, because "could not
 *     ask" says nothing about the transaction;
 *   - KS-1384 F-a: each write expects the status set and the hash this pass
 *     read, so a row that moved between the SELECT and the write (a new hash
 *     from a re-anchor, or a terminal state written by the submitter) is left
 *     as it is. Only a write that matched its row is counted.
 *
 * KS-1384 F-b adds the rows with NO hash, and one step before every give-up
 * (design rev 2 §9 rows R4-R8, rev 4 §4.3):
 *   - R4, adopt before giving up: before a real-hash row is failed, the
 *     platform wallet is searched for a transaction carrying this row's
 *     payload under ANOTHER hash (the restart shape: the row rests on Y while
 *     an encode-equal X landed). Found and confirmed: the row is confirmed
 *     with X. A search that could not finish defers the give-up; it never
 *     forces it;
 *   - R5: a `(non-final, NULL)` row this process still drives (drivingSet.ts:
 *     the lock queue, the lock, a retry or wait timer, a batch) is never
 *     touched;
 *   - R6, the sweep: a `(non-final, NULL)` row nobody here drives, untouched
 *     for MIN_AGE, is searched for in the same way. Found: confirmed with that
 *     transaction. A COMPLETE search that finds nothing: `failed`, "no
 *     transaction found for this event; nothing was submitted". Anything less
 *     than complete: left for the next pass. It never builds or submits;
 *   - R6 honours the wait marker the submitter writes on an anchor's first
 *     wait: a marked row is not swept before t0 + the wait horizon + 15 min,
 *     so a waiter in another process finishes its own horizon first;
 *   - R6 does not run until the boot arm's window has passed since this
 *     process's first pass (the fourth review's m-3, as Wednesday ruled after
 *     gate 48): the TTL plus its margin, about 2 h 10 min, the same window in
 *     which guard 3 treats a transaction signed before the restart as still
 *     able to land. Inside it a re-POST-nulled row may yet be anchored by such
 *     a transaction, and the driving set, being in memory, cannot see rows an
 *     overlapping old process still holds. The deploy rule is still no
 *     container overlap at recreate;
 *   - R6's writes also expect the row's updated_at as read, so a front-door
 *     re-POST landing during the search makes the write match 0 rows;
 *   - R7 is NOT built: a non-final row carrying a placeholder hash is still
 *     never chain-checked and never written here (KS-587; KS-1870). R8, a
 *     re-drive, is a Kam card and is not built either.
 *   The search and A1 share ONE comparison, on the encoded side
 *   (`encodedPayloadEquals`, attemptFamily.ts).
 *
 * Dependency-injected so it is unit-testable without booting the service
 * (index.ts starts the HTTP listener on import).
 * =============================================================================
 */

import { encodedPayloadEquals, BOOT_ARM_MARGIN_SLOTS } from './attemptFamily';
import { ANCHOR_TTL_SLOTS } from './cardano/transaction';
import type { ScanWalletLabel } from './walletLabelScan';

export interface ReconcilerCheck {
  confirmed: boolean;
  blockHash?: string;
  blockNumber?: number;
  slot?: number;
  confirmations?: number;
  /** KS-726: attempts in which the chain answered (found or "not found"). */
  polled?: number;
  /** KS-726: attempts that threw before the chain answered. */
  errored?: number;
}

export interface ReconcilerDeps {
  isDbAvailable: () => boolean;
  isCardanoReady: () => boolean;
  query: (sql: string, params?: unknown[]) => Promise<{ rows: any[] }>;
  /** Single-shot chain check for a tx — waitForConfirmation(tx, 1, 0, 0). */
  checkTx: (txHash: string) => Promise<ReconcilerCheck>;
  /**
   * KS-1384 F-a: resolves to the matched row count, or null when the write did not run
   * (`runAnchorStatusUpdate`'s contract). Only a 1 is counted as a write that happened.
   */
  updateStatus: (anchorId: string, updates: Record<string, unknown>) => Promise<number | null>;
  log: (level: string, message: string, meta?: Record<string, unknown>) => void;
  now?: () => number;
  /** KS-1384 F-b (R5): true while THIS process drives the anchor (drivingSet.ts). R6 never touches a driven row. */
  isDriven: (anchorId: string) => boolean;
  /** KS-1384 F-b: the shared scan core over the platform wallet (walletLabelScan.ts). */
  scanWallet: ScanWalletLabel;
}

export interface ReconcilerConfig {
  minAgeMs: number;
  giveUpMs: number;
  batch: number;
  /** KS-1384 F-b: the submitter's wait horizon (anchorSubmission.ts `WAIT_HORIZON_MS`); default 2 h. */
  waitHorizonMs?: number;
}

export interface ReconcilerResult {
  scanned: number;
  confirmed: number;
  failed: number;
}

const REAL_TX_64HEX = /^[0-9a-f]{64}$/i;
/** The statuses this reconciler selects; every write it makes expects the row to still be in one of them. */
const NON_FINAL = ['pending', 'submitted', 'submitting'];
/** KS-1810: answered "not found" passes past the window needed before a row is failed. */
export const ANSWERED_MISSES_TO_FAIL = 2;
/** Bound on the in-memory count map; entries are removed on confirm, fail and reset, so this is a backstop. */
const MAX_TRACKED = 10_000;

/** Cardano's slot length: 1 s on mainnet and on preview since the Shelley era. */
export const CARDANO_SLOT_MS = 1_000;
/**
 * KS-1384 F-b (m-3; ruled after gate 48): R6 does not run until this long after this process's first pass (index.ts runs it
 * at listen time). It is the boot arm's window (attemptFamily.ts `BootArm`): ANCHOR_TTL_SLOTS + BOOT_ARM_MARGIN_SLOTS, read
 * from the same two constants so one restart rule governs both. The arm counts chain slots from its first answered tip, the
 * sweep counts milliseconds from its first pass; at one slot a second they are the same length, and the arm can only start later.
 */
export const SWEEP_BOOT_GRACE_MS = (ANCHOR_TTL_SLOTS + BOOT_ARM_MARGIN_SLOTS) * CARDANO_SLOT_MS;
/** KS-1384 F-b: a row carrying the wait marker is not swept before t0 + the wait horizon + this. */
export const SWEEP_AFTER_HORIZON_MS = 15 * 60_000;
/**
 * KS-1384 F-b (cells r4 and l2): the search starts this long before the row's CREATION, rev 2's rule, restored after gate 49
 * N1/L2. Rev 3's minor 9 had moved it to the last write, for consistency with the give-up window. But F0b's no-shared-coin
 * wait rests a row whose member was signed BEFORE its last write (the wait marker), and that member may have landed long
 * before it. From the last write, a complete search missed it and failed the row "nothing was submitted".
 */
export const ADOPT_SCAN_LOOKBACK_MS = 10 * 60_000;
export const DEFAULT_WAIT_HORIZON_MS = 2 * 60 * 60_000;
export const SWEEP_FAILED_MESSAGE = 'no transaction found for this event; nothing was submitted (KS-1384 R6)';

const WAIT_MARKER = /waiting for a spendable coin since (\S+) \(KS-1384\)/;

/**
 * KS-1384 F-b: t0 from the marker anchorSubmission.ts writes on an anchor's first wait (`waitMarker`).
 * Returns t0 in epoch ms; `undefined` when the text carries no marker; `null` when it carries one that cannot be
 * read, which the sweep treats as "leave the row" (it cannot tell how long the waiter may still run).
 */
export function waitMarkerT0(errorMessage: unknown): number | null | undefined {
  if (typeof errorMessage !== 'string' || !errorMessage.includes('waiting for a spendable coin')) return undefined;
  const m = WAIT_MARKER.exec(errorMessage);
  const t0 = m ? Date.parse(m[1]) : NaN;
  return Number.isFinite(t0) ? t0 : null;
}

/** The row's stored payload as an object, or null when there is nothing to compare against. */
function storedPayload(raw: unknown): object | null {
  let v: unknown = raw;
  if (typeof raw === 'string') {
    try { v = JSON.parse(raw); } catch { return null; }
  }
  return v !== null && typeof v === 'object' && !Array.isArray(v) && Object.keys(v as object).length > 0 ? (v as object) : null;
}

type AdoptOutcome =
  | { kind: 'adopted'; txHash: string; check: ReconcilerCheck }
  | { kind: 'none' }
  | { kind: 'no-payload' }
  | { kind: 'undecided'; why: string };

export function createStuckAnchorReconciler(deps: ReconcilerDeps, config: ReconcilerConfig) {
  let running = false;
  /** KS-1810: `${anchorId}:${txHash}` -> consecutive answered not-found passes past the window. */
  const answeredMisses = new Map<string, number>();
  const now = deps.now ?? Date.now;
  const waitHorizonMs = config.waitHorizonMs ?? DEFAULT_WAIT_HORIZON_MS;
  /** KS-1384 F-b (m-3): when this process ran its first pass; R6 waits SWEEP_BOOT_GRACE_MS from here. */
  let firstPassAt: number | undefined;

  /**
   * KS-1384 F-b: look for a transaction carrying this row's payload (encoded side, the label the row was
   * anchored under) from ADOPT_SCAN_LOOKBACK_MS before the row's creation, not its last write (gate 49 N1/L2: a member
   * signed before the last write may have landed before it). `ownHash` is the row's current hash
   * (R4) or null (R6). Only a COMPLETE search, and a match the single-shot check confirms, decide anything.
   */
  async function adoptScan(row: any, ownHash: string | null): Promise<AdoptOutcome> {
    const payload = storedPayload(row.metadata_payload);
    if (!payload) return { kind: 'no-payload' };
    const label = Number(row.metadata_label ?? 674);
    const fromMs = new Date(row.created_at).getTime() - ADOPT_SCAN_LOOKBACK_MS;
    const scan = await deps.scanWallet({ label, fromMs, toMs: now(), match: (json) => encodedPayloadEquals(payload, json) });
    if (scan.outcome !== 'complete') return { kind: 'undecided', why: `the search was ${scan.outcome}` };
    // The row's own transaction listed on chain while the single-shot check said "not found": the reads
    // disagree, so decide nothing.
    if (ownHash && scan.matches.some((m) => m.txHash === ownHash)) return { kind: 'undecided', why: "the row's own transaction is listed on chain" };
    const x = scan.matches.find((m) => m.txHash !== ownHash);
    if (!x) return { kind: 'none' };
    const check = await deps.checkTx(x.txHash);
    if (!check.confirmed) return { kind: 'undecided', why: 'the matching transaction did not confirm on the single-shot check' };
    return { kind: 'adopted', txHash: x.txHash, check };
  }

  const confirmedWith = (txHash: string, c: ReconcilerCheck) => ({
    status: 'confirmed',
    transactionHash: txHash,
    confirmations: c.confirmations ?? 1,
    blockNumber: c.blockNumber,
    slot: c.slot,
    blockHash: c.blockHash,
    confirmedAt: new Date(),
  });

  /** KS-1384 F-b, R5 and R6: the `(non-final, NULL)` rows. */
  async function sweepNullHashRows(out: ReconcilerResult): Promise<void> {
    const rows = await deps.query(
      `SELECT id, status, transaction_hash, metadata_label, metadata_payload, error_message, created_at, updated_at,
              updated_at::text AS updated_at_token
         FROM anchor_store
        WHERE status IN ('pending', 'submitted', 'submitting')
          AND transaction_hash IS NULL
          AND simulated = FALSE
          AND updated_at < NOW() - ($1 || ' milliseconds')::interval
        ORDER BY updated_at ASC
        LIMIT $2`,
      [String(config.minAgeMs), config.batch],
    );
    for (const row of rows.rows) {
      if (row.transaction_hash !== null && row.transaction_hash !== undefined) continue; // R4 owns rows with a hash
      if (!NON_FINAL.includes(row.status) || typeof row.updated_at_token !== 'string') continue;
      if (deps.isDriven(row.id)) continue; // R5
      const t0 = waitMarkerT0(row.error_message);
      if (t0 === null) {
        deps.log('warn', 'Reconciler: wait marker unreadable; row left as it is (KS-1384 R6)', { anchorId: row.id });
        continue;
      }
      if (t0 !== undefined && now() < t0 + waitHorizonMs + SWEEP_AFTER_HORIZON_MS) continue;
      out.scanned++;
      try {
        const adopt = await adoptScan(row, null);
        if (adopt.kind === 'no-payload' || adopt.kind === 'undecided') {
          deps.log('info', 'Reconciler: no-hash row left for the next pass (KS-1384 R6)', {
            anchorId: row.id, why: adopt.kind === 'undecided' ? adopt.why : 'no stored payload to search for',
          });
          continue;
        }
        if (deps.isDriven(row.id)) continue; // picked up by this process during the search
        // The row exactly as read: same status, still no hash, and nobody wrote it since (a re-POST moves updated_at).
        const guard = { expectStatus: row.status, expectTransactionHash: null, expectUpdatedAt: row.updated_at_token };
        const write = adopt.kind === 'adopted'
          ? { ...confirmedWith(adopt.txHash, adopt.check), ...guard }
          : { status: 'failed', errorMessage: SWEEP_FAILED_MESSAGE, ...guard };
        const n = await deps.updateStatus(row.id, write);
        if (n === 1) {
          if (adopt.kind === 'adopted') {
            out.confirmed++;
            deps.log('info', 'Reconciler: no-hash row adopted its transaction found on chain (KS-1384 R6)', { anchorId: row.id, txHash: adopt.txHash });
          } else {
            out.failed++;
            deps.log('warn', 'Reconciler: no-hash row failed — no transaction carries its payload (KS-1384 R6)', { anchorId: row.id });
          }
        } else {
          deps.log('warn', n === 0
            ? 'Reconciler: the no-hash row moved after it was read; left as it is (KS-1384 R6)'
            : 'Reconciler: the no-hash row write did not run; left for the next pass (KS-1384 R6)', { anchorId: row.id, matched: n });
        }
      } catch (err: any) {
        deps.log('warn', 'Reconciler: no-hash row search errored; left as it is (KS-1384 R6)', { anchorId: row.id, error: err?.message });
      }
    }
  }

  return async function reconcileStuckAnchors(): Promise<ReconcilerResult> {
    const out: ReconcilerResult = { scanned: 0, confirmed: 0, failed: 0 };
    const startedAt = firstPassAt ?? (firstPassAt = now());
    if (running || !deps.isDbAvailable() || !deps.isCardanoReady()) return out;
    running = true;
    try {
      // MIN_AGE keeps the reconciler off rows that were written recently. The age is
      // read from updated_at, which each status write moves, but the confirmation poll
      // writes nothing between submitted and confirmed, so a row the live loop is still
      // polling can pass MIN_AGE (KS-1816).
      const rows = await deps.query(
        `SELECT id, transaction_hash, metadata_label, metadata_payload, created_at, updated_at FROM anchor_store
          -- KS-726: 'submitting' is the write-ahead state — the row NAMES a
          -- signed transaction whose submit reply we never received. Those are
          -- precisely the rows this reconciler exists for: the transaction may
          -- be on chain and fee-paying, and nothing else will ever settle it.
          -- Omitting the state here would make write-ahead pointless, since the
          -- hash would be stored and then never looked at.
          WHERE status IN ('pending', 'submitted', 'submitting')
            AND transaction_hash IS NOT NULL
            AND simulated = FALSE
            AND updated_at < NOW() - ($1 || ' milliseconds')::interval
          ORDER BY updated_at ASC
          LIMIT $2`,
        [String(config.minAgeMs), config.batch],
      );
      for (const row of rows.rows) {
        const tx = String(row.transaction_hash || '');
        if (!REAL_TX_64HEX.test(tx)) continue;
        out.scanned++;
        const key = `${row.id}:${tx}`;
        // KS-1384 F-a: the write must find the row as this pass read it: still non-final, still naming this hash.
        const guard = { expectStatus: NON_FINAL, expectTransactionHash: tx };
        try {
          const confirmation = await deps.checkTx(tx);
          if (confirmation.confirmed) {
            answeredMisses.delete(key);
            const n = await deps.updateStatus(row.id, {
              status: 'confirmed',
              confirmations: confirmation.confirmations ?? 1,
              blockNumber: confirmation.blockNumber,
              slot: confirmation.slot,
              blockHash: confirmation.blockHash,
              confirmedAt: new Date(),
              ...guard,
            });
            if (n === 1) {
              out.confirmed++;
              deps.log('info', 'Reconciler: stale anchor confirmed against chain (KS-584)', { anchorId: row.id, txHash: tx, blockNumber: confirmation.blockNumber });
            } else {
              deps.log('warn', n === 0
                ? 'Reconciler: the row moved after it was read (new hash or final status); left as it is (KS-1384)'
                : 'Reconciler: the confirmed write did not run; the row is left for the next pass (KS-1384)', { anchorId: row.id, txHash: tx, matched: n });
            }
            continue;
          }

          const answered = (confirmation.polled ?? 0) > 0;
          const pastWindow = now() - new Date(row.updated_at).getTime() > config.giveUpMs;
          if (!answered) {
            // KS-1810: the provider never answered. That says nothing about the transaction: never fail on it,
            // and start the consecutive count again.
            answeredMisses.delete(key);
            if (pastWindow) {
              deps.log('warn', 'Reconciler: chain could not be asked (provider error); not counted towards give-up (KS-1810)', { anchorId: row.id, txHash: tx, errored: confirmation.errored ?? null });
            }
            continue;
          }
          if (!pastWindow) {
            answeredMisses.delete(key);
            continue;
          }
          const misses = (answeredMisses.get(key) ?? 0) + 1;
          if (misses < ANSWERED_MISSES_TO_FAIL) {
            if (answeredMisses.size >= MAX_TRACKED) answeredMisses.clear();
            answeredMisses.set(key, misses);
            deps.log('info', 'Reconciler: not on chain past the give-up window; waiting for a second answered pass (KS-1810)', { anchorId: row.id, txHash: tx, misses });
            continue;
          }
          answeredMisses.delete(key);
          // KS-1384 F-b (R4, cell r5): before giving up, look for this row's payload on chain under ANOTHER hash.
          const adopt = await adoptScan(row, tx);
          if (adopt.kind === 'undecided') {
            // Never give up on missing information: the next answered miss searches again.
            answeredMisses.set(key, ANSWERED_MISSES_TO_FAIL - 1);
            deps.log('info', 'Reconciler: give-up deferred, the search for the payload could not decide (KS-1384 R4)', { anchorId: row.id, txHash: tx, why: adopt.why });
            continue;
          }
          if (adopt.kind === 'adopted') {
            const m = await deps.updateStatus(row.id, { ...confirmedWith(adopt.txHash, adopt.check), ...guard });
            if (m === 1) {
              out.confirmed++;
              deps.log('info', 'Reconciler: adopted the transaction carrying this row\'s payload under another hash (KS-1384 R4)', { anchorId: row.id, restedOn: tx, adopted: adopt.txHash });
            } else {
              deps.log('warn', m === 0
                ? 'Reconciler: the row moved after it was read (new hash or final status); left as it is (KS-1384)'
                : 'Reconciler: the confirmed write did not run; the row is left for the next pass (KS-1384)', { anchorId: row.id, txHash: tx, matched: m });
            }
            continue;
          }
          const n = await deps.updateStatus(row.id, {
            status: 'failed',
            errorMessage: `transaction never appeared on chain within ${Math.round(config.giveUpMs / 3_600_000)}h (reconciler)`,
            ...guard,
          });
          if (n === 1) {
            out.failed++;
            deps.log('warn', 'Reconciler: stale anchor marked failed — tx never appeared (KS-584)', { anchorId: row.id, txHash: tx });
          } else {
            deps.log('warn', n === 0
              ? 'Reconciler: the row moved after it was read (new hash or final status); left as it is (KS-1384)'
              : 'Reconciler: the failed write did not run; the row is left for the next pass (KS-1384)', { anchorId: row.id, txHash: tx, matched: n });
          }
        } catch (err: any) {
          // Reached when checkTx or updateStatus rejects. The production checkTx
          // (waitForConfirmation(tx, 1, 0, 0) in index.ts) catches a provider error itself
          // and answers confirmed:false with polled 0, so a provider outage never lands here:
          // the "could not ask" branch above decides it (never failed, KS-1810). A rejection
          // here leaves the row for the next pass and is not counted. Never guess.
          answeredMisses.delete(key);
          deps.log('warn', 'Reconciler: chain check errored; leaving row as-is', { anchorId: row.id, error: err?.message });
        }
      }
      if (now() - startedAt >= SWEEP_BOOT_GRACE_MS) await sweepNullHashRows(out);
      if (out.scanned > 0) {
        deps.log('info', 'Reconciler pass complete (KS-584)', { ...out });
      }
    } catch (err: any) {
      deps.log('warn', 'Reconciler pass failed', { error: err?.message });
    } finally {
      running = false;
    }
    return out;
  };
}
