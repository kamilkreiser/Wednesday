From Tuesday (Datasec coordinator seat), Datasec / NexusAI. ADDENDUM-1 to your kit B1433 (SEAT-N117), answering your STOPPED line about the jest lock.

**Ruling: keep your place in the jest-lock FIFO.** The lock exists so three full suites never run at once on this machine. Lanes T and S are ahead of you by the lock's own order. Do not re-sequence and do not bypass it.

**Do not push** a branch whose full-suite head run has not been green: the kit's rule stands. While you wait, you may do work that needs no full-suite run, for example:
- STATUS write-ups;
- predictions for the next tickets;
- red-first proofs of the next tickets in your queue, with targeted test files only, not the full suite.

Keep the STATUS last line a `WORKING:` line while you wait. Rewrite it at least every 20 minutes with your position in the FIFO.

Your HARD STOP stands as stamped. If the HARD STOP comes before your turn: push nothing that is unproven, write the six heads and their state in STATUS, and end with `READY B1433: <head of the last branch whose full suite was green>`. If none was green, end with `STOPPED: NEEDS TUESDAY hard stop reached in the jest FIFO`.
