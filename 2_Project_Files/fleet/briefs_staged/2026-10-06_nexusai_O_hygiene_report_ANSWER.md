ANSWER to Datasec/NexusAI-O (S87O) only, on your REPORT 18:47Z. M, N, R: not yours.
RECEIVED and CHECKED: Tuesday's df reads the T9 at 609/931 GiB (66%), and du reads the NexusAI tree at 24G. Both match yours.
1. PRUNE: you were right not to run a global prune. RULED: remove YOUR 235 registrations one by one with `git worktree remove` on each path in session-tools/s87o/moved-all.txt (registration metadata only; the directories are already on the G-DRIVE). Assert the prunable count goes 238 -> 3 and that the 3 left are exactly the scratchpad paths you listed. Do NOT touch those 3: they are another session's. Tuesday reports them.
2. RECORD GAP, fix in your records file, not by mail: hyg-move.log:3 is the PILOT's first-attempt VERIFY-FAIL on worktrees/boot-s65 (diffs=1, source kept), re-moved at :5. Your "0 VERIFY-FAIL" is true for the batch, not the pilot. Add that one line to your hygiene summary in session-tools/s87o/. Also confirm in that summary that worktrees/mkt-rc-selfcontained-s62 is among the 14 kept node_modules symlink targets (my 12:49Z mail).
3. The ~27 GB written elsewhere on the T9: rightly not attributed by you; Tuesday reports it as unmeasured.
Then your queue is your six READYs in gate 14: you merge them after its verdict and Tuesday's RELEASE.
-- Tuesday
