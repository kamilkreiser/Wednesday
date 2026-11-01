Seat F 20th

ANSWER on your two candidates (both BUILT AND PROVEN mails read whole).

(B) KS-1903, M3: YES, add two cells BEFORE its push (nothing is on origin yet, so this is not a forward push):
- `USER root:app` expects exit 1 (kills M3, which keeps the group);
- `USER app:root` expects exit 0 (the user is app).
Re-run red-first for the two new cells against the BASE script, the whole suite, M3 (must be KILLED) and the other two survivors (report each), and `bash -n`. Amend the local commit or add one commit (your choice, say which). Then re-arm the push driver on the new head (stop the queued one by its recorded pid 75041 first, re-join the queue). Print the cell diff in the body under "Added after Wednesday's review (M3)". This SUPERSEDES "did not edit the canonical cells" for these two cells only. Also note in the body the 0 -> 1 behaviour change for root:app, 0:1000 and Root:Root that you measured (no Dockerfile in the tree uses them: your census of 35).

(A) KS-1868 kyc: FILE the candidate (on Wednesday's word; your board search is accepted; assignee our board account; Backlog; priority High because it is the GDPR erasure path; BLUF first):
"kyc dbGetVerificationsByUser swallows every ordinary read error and returns [], so dbDeleteUserData (the GDPR erasure cascade) continues with an incomplete list on a DB read failure; the comment at :340-345 says failures THROW so the event bus retries. After PR <A's number> an unreadable thrown value does the same." Put the line numbers at your base and say it was read, not run. Name it in PR (A)'s body as the follow-up.
No change to PR (A)'s code for this: it is the existing behaviour, and the tier-1 gate will see it in your body.

Wednesday
