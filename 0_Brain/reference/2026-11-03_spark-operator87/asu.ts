/**
 * =============================================================================
 * KS-1385 MIN-1 — the anchor status UPDATE, built in one place
 * =============================================================================
 * WHY THIS MODULE EXISTS AT ALL. The invariant "the identity stored beside a
 * transaction hash is the identity of the event that produced that hash" does
 * not hold under concurrency once `metadata_payload` is writable. The pull
 * request 1549 gate measured it with the real `createAnchorSubmitter`, the real
 * wallet lock and real Postgres: with event 2's upsert landing while event 1 is
 * between "read the payload inside the lock" and "write submitted + tx1", the
 * row ends as `storedActor: did:key:zSHARER` beside
 * `actorInTheTxOnChain: did:key:zUPLOADER`, and `invariantHolds: false`.
 *
 * Wednesday ruled a compare-and-set in the submitter (2026-10-13T11:22:45Z).
 * The comparison has to be ATOMIC with the write, so it belongs in the
 * statement — and the statement was a template literal inlined in
 * `dbUpdateAnchorStatus`, where no cell can reach it.
 *
 * ⚠ AND THAT IS THE POINT OF THE EXTRACTION, not tidiness. The gate's race
 * cell — the one Wednesday told me to ADOPT as the red-first proof — hand-rolls
 * its own `updateStatus`, "mirroring index.ts dbUpdateAnchorStatus". A fix left
 * inside `dbUpdateAnchorStatus` would be proven by a cell that re-implements
 * `dbUpdateAnchorStatus`: the cell would pass against a product that still had
 * the defect. Extracted here, the cell imports the product's own builder and a
 * mutant on the compare-and-set reddens it.
 *
 * Pure: no database, no clock passed in by surprise, no environment. It returns
 * SQL text and bind values, so a cell can assert the shape AND execute it.
 * =============================================================================
 */

import { FABRICATED_TX_PREFIX } from './honestAnchor';

export interface AnchorStatusUpdate {
  status?: string;
  transactionHash?: string | null;
  blockHash?: string | null;
  blockNumber?: number | null;
  slot?: number | null;
  confirmations?: number | null;
  confirmedAt?: Date | null;
  errorMessage?: string | null;
  simulated?: boolean;
  /**
   * KS-1385 MIN-1 — the compare-and-set. When present, the UPDATE applies ONLY
   * if the row's `metadata_payload` is still this value: the payload the caller
   * read, signed and submitted. `metadata_payload` is `jsonb`, so the
   * comparison is semantic rather than textual and key order cannot make a
   * matching payload look different.
   *
   * A miss is not an error. It means a later event has already replaced the
   * payload, so this write would have recorded "event 2's identity, anchored by
   * event 1's transaction" — the falsification itself. Declining to write
   * leaves the row `pending` with no hash, which is exactly the state event 2's
   * own submission then resolves: it mints its own transaction and stores a
   * self-consistent row. Two genuinely different events produce two
   * transactions, which is honest; the double-mint guards (KS-705 / KS-726)
   * exist to stop the SAME payload being minted twice, and this is not that.
   */
  expectMetadataPayload?: object;
  /**
   * KS-1384 F-a — the row-count builder. When present, the UPDATE applies only
   * if the row's `status` is still this value (or one of these values). A
   * caller that read the row, did slow work (a chain check, a re-poll), and
   * then writes must not overwrite a row that moved meanwhile: the write
   * matches 0 rows instead, and the caller reads the 0 from
   * `runAnchorStatusUpdate`.
   */
  expectStatus?: string | string[];
  /**
   * KS-1384 F-a — the same, for `transaction_hash`. NULL-safe: `null` expects
   * a row with no hash (`IS NULL`), never `= NULL`, which matches nothing.
   */
  expectTransactionHash?: string | null;
  /**
   * KS-1384 F-b — the same, for `updated_at`, given as the row's own text form
   * (`updated_at::text` as read). Every status write and every front-door
   * upsert moves `updated_at`, so a caller that read a row, did slow work (the
   * sweep's chain scan) and then writes can require "nobody wrote this row
   * since I read it". Compared as `timestamptz`, so the server time zone
   * cannot make an equal instant look different.
   */
  expectUpdatedAt?: string;
}

export interface BuiltStatusUpdate {
  sql: string;
  params: unknown[];
  /** True when `expectMetadataPayload` was supplied, so a caller can tell a guarded write from an ordinary one. */
  guarded: boolean;
  /** KS-1384 F-a: true when any expectation (payload, status, hash or, since F-b, updated_at) narrows the WHERE beyond the id. */
  conditional: boolean;
}

/**
 * Build the UPDATE for one anchor row. Returns null when there is nothing to
 * write — the caller must not issue a statement with an empty SET list.
 */
export function buildAnchorStatusUpdate(anchorId: string, updates: AnchorStatusUpdate, now: Date = new Date()): BuiltStatusUpdate | null {
  const setClauses: string[] = [];
  const params: unknown[] = [];
  let idx = 1;

  if (updates.status !== undefined) { setClauses.push(`status = $${idx++}`); params.push(updates.status); }
  if (updates.transactionHash !== undefined) {
    setClauses.push(`transaction_hash = $${idx++}`); params.push(updates.transactionHash);
    // KS-587: this UPDATE is how a processed anchor gains its hash — the row
    // was inserted pending (simulated=false, no hash) and this path is what
    // let mock_tx_ hashes land as simulated=false + confirmed. Recompute the
    // flag whenever the hash changes.
    setClauses.push(`simulated = $${idx++}`);
    params.push(
      updates.simulated === true ||
        FABRICATED_TX_PREFIX.test(updates.transactionHash || ''),
    );
  }
  if (updates.blockHash !== undefined) { setClauses.push(`block_hash = $${idx++}`); params.push(updates.blockHash); }
  if (updates.blockNumber !== undefined) { setClauses.push(`block_number = $${idx++}`); params.push(updates.blockNumber); }
  if (updates.slot !== undefined) { setClauses.push(`slot = $${idx++}`); params.push(updates.slot); }
  if (updates.confirmations !== undefined) { setClauses.push(`confirmations = $${idx++}`); params.push(updates.confirmations); }
  if (updates.confirmedAt !== undefined) { setClauses.push(`confirmed_at = $${idx++}`); params.push(updates.confirmedAt); }
  if (updates.errorMessage !== undefined) { setClauses.push(`error_message = $${idx++}`); params.push(updates.errorMessage); }

  if (setClauses.length === 0) return null;

  setClauses.push(`updated_at = $${idx++}`);
  params.push(now);

  const where: string[] = [`id = $${idx++}`];
  params.push(anchorId);

  const guarded = updates.expectMetadataPayload !== undefined;
  if (guarded) {
    where.push(`metadata_payload = $${idx++}::jsonb`);
    params.push(JSON.stringify(updates.expectMetadataPayload));
  }

  if (updates.expectStatus !== undefined) {
    if (Array.isArray(updates.expectStatus)) {
      where.push(`status = ANY($${idx++}::text[])`);
      params.push(updates.expectStatus);
    } else {
      where.push(`status = $${idx++}`);
      params.push(updates.expectStatus);
    }
  }

  if (updates.expectTransactionHash !== undefined) {
    if (updates.expectTransactionHash === null) {
      where.push('transaction_hash IS NULL');
    } else {
      where.push(`transaction_hash = $${idx++}`);
      params.push(updates.expectTransactionHash);
    }
  }

  if (updates.expectUpdatedAt !== undefined) {
    where.push(`updated_at = $${idx++}::timestamptz`);
    params.push(updates.expectUpdatedAt);
  }

  return {
    sql: `UPDATE anchor_store SET ${setClauses.join(', ')} WHERE ${where.join(' AND ')}`,
    params,
    guarded,
    conditional: where.length > 1,
  };
}

export interface RunStatusUpdateDeps {
  isDbAvailable: () => boolean;
  ensureTables: () => Promise<unknown>;
  query: (sql: string, params?: unknown[]) => Promise<unknown>;
  log: (level: 'info' | 'warn' | 'error', message: string, meta?: Record<string, unknown>) => void;
}

/**
 * KS-1384 F-a — execute one status UPDATE and say how many rows it matched.
 *
 * This is the body `dbUpdateAnchorStatus` (index.ts) used to inline, moved here
 * so a cell can reach it without booting the service. The pin's version
 * returned nothing and swallowed every error, so a caller could not tell "the
 * row moved under me" (0 rows) from "the write never ran" (a database fault).
 *
 * Returns:
 *   - the matched row count (0 or 1 for an id-keyed UPDATE);
 *   - `null` when the write did not run or its result is unknown: the database
 *     is unavailable, there was nothing to write, the statement threw, or the
 *     driver reported no numeric `rowCount`.
 * A caller must treat `null` as "unknown", never as success. The errors are
 * still logged at warn and still not rethrown: every caller at this pin ignores
 * the result, and KS-1384 F0 is the first that reads it.
 */
export async function runAnchorStatusUpdate(
  deps: RunStatusUpdateDeps,
  anchorId: string,
  updates: AnchorStatusUpdate,
  now: Date = new Date(),
): Promise<number | null> {
  try {
    if (!deps.isDbAvailable()) return null;
    await deps.ensureTables();

    const built = buildAnchorStatusUpdate(anchorId, updates, now);
    if (!built) return null;

    const result: any = await deps.query(built.sql, built.params);
    const affected = typeof result?.rowCount === 'number' ? result.rowCount : null;

    // KS-1385 MIN-1: a guarded write that matched NO row is not an error — it
    // is the race being caught. Say so once, at warn, because an operator
    // seeing a paid transaction with no row to show for it needs this line to
    // explain it. The transaction is on chain and honest; it just is not the
    // one this row indexes any more (KS-1384 is the structural ticket for a
    // row that can only index one).
    if (built.guarded && affected === 0) {
      deps.log('warn', 'KS-1385: declined to record a transaction against an anchor whose metadata changed under it — a later event had already replaced the payload', {
        anchorId,
        status: updates.status,
        transactionHash: updates.transactionHash,
      });
    }
    return affected;
  } catch (err: any) {
    deps.log('warn', 'Failed to update anchor status in DB', { anchorId, error: err?.message });
    return null;
  }
}
