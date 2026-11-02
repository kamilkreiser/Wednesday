/**
 * =============================================================================
 * KS-1384 F-b — the driving set (design rev 2 §9 row R5; rev 4 §4.3)
 * =============================================================================
 * The anchor ids THIS process is still working on: waiting in the wallet lock's
 * queue, holding the lock, on a retry or wait timer (`scheduleRetry`), or inside
 * a batch submission. The reconciler's sweep (R6) never touches a row whose id is
 * in here, because the process that holds it will write it.
 *
 * It is in memory on purpose. After a restart it is empty, and that is exactly
 * when a `(pending, NULL)` row has nobody left to drive it — the case R6 exists
 * for. A second process on the same database has its own set and cannot see
 * this one; that is why R6 also waits out a boot grace and the wait marker
 * (reconciler.ts), and why the deploy rule is one anchoring process per wallet
 * with no container overlap at recreate.
 *
 * Counted, not a plain Set: one id can be driven by several holders at once
 * (a front-door re-POST calls processAnchor while that id's wait timer is still
 * pending), and the first holder to finish must not make the id look free.
 * =============================================================================
 */

export class DrivingSet {
  private readonly holders = new Map<string, number>();

  enter(anchorId: string): void {
    this.holders.set(anchorId, (this.holders.get(anchorId) ?? 0) + 1);
  }

  leave(anchorId: string): void {
    const n = (this.holders.get(anchorId) ?? 0) - 1;
    if (n > 0) this.holders.set(anchorId, n);
    else this.holders.delete(anchorId);
  }

  has(anchorId: string): boolean {
    return this.holders.has(anchorId);
  }

  get size(): number {
    return this.holders.size;
  }
}

/** Hold `anchorIds` while `fn` runs, whatever it resolves or throws. */
export async function driveWhile<T>(set: DrivingSet, anchorIds: string[], fn: () => Promise<T>): Promise<T> {
  for (const id of anchorIds) set.enter(id);
  try {
    return await fn();
  } finally {
    for (const id of anchorIds) set.leave(id);
  }
}

/**
 * `scheduleRetry`'s timer: the id counts as driven from the moment the retry is
 * scheduled until the retried run has finished. A wait re-queue is a timer too,
 * so an anchor waiting for a spendable coin stays driven between its turns.
 */
export function driveTimer(
  set: DrivingSet,
  anchorId: string,
  delayMs: number,
  run: (anchorId: string) => Promise<unknown>,
  schedule: (fn: () => void, ms: number) => unknown = setTimeout,
): void {
  set.enter(anchorId);
  schedule(() => {
    let done: Promise<unknown>;
    try {
      done = Promise.resolve(run(anchorId));
    } catch (err) {
      done = Promise.reject(err);
    }
    done.finally(() => set.leave(anchorId)).catch(() => undefined);
  }, delayMs);
}

/** The process's ONE driving set, beside `platformWalletView` and `platformFamilies`. */
export const platformDriving = new DrivingSet();
