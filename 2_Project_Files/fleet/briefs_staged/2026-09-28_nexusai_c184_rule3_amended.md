BLUF: RULED YES, as P proposed. This SUPERSEDES rule 3 of the 09:21 merge-turn rule (C-184). Once a merge author has pushed, it queues its NEXT merge ticket only after that push's CI Build has finished with a failing set that fits C-185 (a subset of {rd638 E2}). While another author's Build is running, the turn is open to the others. This applies to O, N, P and M.

THE AMENDED RULE 3 (Tuesday, 2026-09-28, after P's QUESTION 06:14Z and O's STATUS 06:14Z):
3. After a push, the author does NOT queue its next merge ticket until the CI Build on its own push has completed and its failing set fits C-185, named in its MERGED mail. During that wait, any other author may take ONE merge under rule 1.
3a. Order when more than one author is waiting for the same open turn: O first (RD-443 is batch 4's last merge, and it releases M's batch 5a), then P (batch 6), then M (5a, once released), then N. After each push the turn passes to the next author in that order who is ready, and a seat with nothing ready is skipped.
3b. A ticket already queued stands. N's s86n-merge2-rd684 (queued 06:14Z) is NOT withdrawn. It runs, N pushes, and from then on N follows 3. The next merge ticket queued after N's merge-2 push is O's merge 5, then P's batch-6 merge 1.

Rules 1, 2 and 4 are unchanged. The CI known set is unchanged (C-185). "A red Build outside the known set" is still a STOP.

Why: as applied, the window in the old rule 3 ("between its push and its next queued merge ticket") had zero width, so batch 4 and batch 6 waited behind every batch-3 merge. That is the whole-batch wait the rule existed to prevent. Queueing before green gains nothing anyway: a hold on an un-green main cannot push.

O: your handling was right (you stopped before merging forward; rd-443 is back at 8e27dc2). Your one `git fetch origin main` in your own worktree is noted and allowed. Take the turn after N's merge-2 push, with your prediction 4184/251 re-based on whatever main is then.
P: right to ask instead of improvising. You go after O.
N: finish merge 2, push, then wait for its Build before queueing merge 3.
Whoever records it: one C-entry amending C-184, with this mail's timestamp.

-- Tuesday
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 16:15
