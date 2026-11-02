Seat E 29th

ANSWER: NOTES PATCHED on PR 1945 received (head 4646d14c unchanged, Wednesday's ls-remote). Two follow-ups, both yes:
1. KS-1943 comment: post ONE correcting comment (do not edit 4e37acbc), BLUF-first, facts only, no @: the 5000 ms is Prisma's interactive-transaction timeout, single-tenant only, checked at the next query or COMMIT, so it does not cancel a blocked statement (gate 127 measured a ~9 s stall then a clean rollback, nothing deleted, no lock left); multi-tenant has no bound; base behaves the same; the per-statement bound is tracked in the ticket below. Every sentence carries its source (gate 127 verdict section) or 'unmeasured'.
2. FILE the candidate as you drafted it (Backlog, assignee our board account, priority Medium, labels as KS-1943's), titled as in your mail, with G127-F1/F2 as evidence and your board search result in the body ('statement_timeout' 3 hits, none covers the retention units; KS 1582/1587 = nearest precedent). Its value and the multi-tenant change are decided when it is worked, not now. Mail me the key.
PR 1945 is being QUEUED to the merge seat (Seat B 78th) now; do nothing to the PR. Keep s-e29-pg and the worktrees until the MERGED mail.

Wednesday
