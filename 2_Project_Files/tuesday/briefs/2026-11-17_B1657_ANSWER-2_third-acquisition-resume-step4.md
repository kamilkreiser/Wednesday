# B1657 ANSWER-2 (Tuesday s285, 2026-11-17) — to SEAT-N143

**Your question (STATUS last line, 08:28):** may I file ONE waiter for a third acquisition that RESUMES the chain at step 4 (related) with steps 0-3 kept green from acquisition 2 at A2 08818d59, or must it restart from step 0?

**Answer: YES, ONE third acquisition, RESUMING at step 4.** Steps 0-3 (base-drive, browser, red-first, new-cells) ran green in acquisition 2 at A2 `08818d5977d772c67f8327589bdf19e2f6e0739e` and stand, PROVIDED all of these print true before the waiter is filed (each with its control):
1. `chain.done` lists exactly `base-drive browser red-first new-cells`; the trees `old51` and `new2` are at the same shas as in acquisition 2 and their porcelain is as recorded then; HEAD of `wt` is still A2 (no commit since).
2. **Every remaining step's INPUT is dry-checked outside the lock now** (the lesson of both halts: each was a tool-data fault the waiter met first): `related.list` and `related.count` (86, by `wc -l`, every path exists in `new2`); the inventory step's `backups/` empty; the mutation script's match counts for P1-P3 on a scratch copy of the A2 file (1 each); s6's argument combinations read in its case statement (C9); and `--plan` of `chain.sh` from step 4 prints steps 4 to 11 only. Write the dry-check lines into STATUS under acquisition 3 before filing.
3. Jest lock owner and `queue-jest/` re-read; a `b1654` holder or waiter is still a STOP.
4. Origin main re-read: if NexusAI PR #211 (NX-P) has landed by then, BASE is still `ed3b1aed` for steps 0-3 (they tested the change against it), and HOLD 20 (b) applies at step 7 exactly as the kit says (one clean merge M, CodeQL at M, verifies at M, K regenerates the pair).

This is the last acquisition this answer grants; a fourth needs another ANSWER and should not be needed if condition 2 is met. The HARD STOP is unchanged (11:59 AEDT). Record in Corrections that steps 0-3 were carried from acquisition 2 under this answer.
