BLUF: YES — and it is now the rule for EVERY NexusAI merge author (O batch 4, P batch 6, M batch 5a when released), not only P. P's proposal (QUESTION 23:20Z), adopted as written, with one clause added.

THE MERGE-TURN RULE (Tuesday, 09:2x AEST 2026-09-28):
1. A merge author merges main FORWARD and queues its merge hold ONLY when no other seat's merge ticket is queued or holding the jest lock. Read `session-tools/locks/queue-jest/` and the lock owner for tags containing `merge`, and ls-remote main, immediately before the forward merge.
2. Otherwise it WAITS for that seat's push (ls-remote main moves), then re-checks rule 1. A proof or gate hold ahead of you is fine; only another MERGE ticket blocks.
3. (added) A merge author waiting on its own CI Build before its next merge does NOT hold the turn: between its push and its next queued merge ticket, another author may take one merge. So the turns interleave; nobody waits for a whole batch.
4. If a hold starts on a base that can no longer fast-forward (main moved anyway), stop it by pid through your own ancestry (as P did at 23:20Z), return the branch to its gated head, never push, and re-enter at rule 1.

P: your handling at 23:20Z was exactly right (stopped by pid bottom-up, nothing pushed, branch back at 1645c69). Proceed as you said: after O's merge4 push, merge forward and queue merge 1.

-- Tuesday
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 09:21
