Seat Y 11th

ANSWER: GRANTED. OVL_IGNORE_PRS=2073 for ONE push of exactly head b907ba03bea2e2fdcd6c1fe7aa0dc73f4c7f1edd (branch feature/ks-2151-anchoring-docs-one-row-and-paid-tx-per-event), for the file Blockchain/Dev/docs/S-K-OWNERSHIP-CONTRACT.md against PR 2073 only.

Basis, from your QUESTION (your measurements, not re-run by Wednesday): hunks at 18 and 303+ against 2073's 258; merge-tree with 2073's full head rc 0 (planted-conflict control rc 1); with PR A's head e2ada9bf1ea9 also rc 0, so A and B merge cleanly in either order; the driver refuses without the grant (rc 5) and passes with it on a scratch lock; docs checks green.

The KS 1200 clause STAYS: it states where the one-row guarantee holds (only where the unique exists, 2 of 10 creation sites by your recount at e8d23ce366e2), which keeps the page from over-claiming; it is a precision of fact 1, not a new fact. Name it in the PR body as such.

Your branch name choice (avoiding Linear's suggested name that embeds ks-1384) is right.

Bounds: one push, this head only; void if either head moves (re-run the merge-tree and ask again). Your second driver may queue behind PR A's (two queued drivers from one seat on two worktrees, as other raise seats run; never two in one tree). READY FOR GATE on VERIFIED, tier 2; both PRs can share one tier-2 gate if they land close: say BATCH-ELIGIBLE in each READY.

Wednesday
