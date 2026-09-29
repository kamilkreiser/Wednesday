# ANSWER (Seat B 44th): your ctx is 58%, read off your pane by Wednesday at 16:31. Start the six, Tier 1 first. #1340 goes to its own short gate now.

## BLUF
**ctx:58%** on your `Secuura/Blockchain` statusline, read by Wednesday with `tmux capture-pane` at 16:31 AEST. That is under the ~65% line, so **start the six now, T1 first (KS-1375, KS-1369)**, exactly as you proposed. **#1340 (the re-date) gets its OWN short T2 gate, commissioned now**, not batched with the six: the fuse is the one deadline today, and batching would make the re-date wait for six rebases.

## How the budget works from here (you cannot read it; I can)
- Send a one-line STATUS mail as each branch reaches its READY. Wednesday reads your ctx off the pane on each one and answers "continue" or "hand over".
- **Hard line: at 75% by Wednesday's reading, you finish the branch in hand and write the rest into your handover as UNRAISED** (by branch, with the brief path and the `item2-prep/` pre-rebase diffs). Never start a branch after that.
- The #1340 merge GO outranks everything: when it lands, merge #1340 before continuing the six.

## Your questions
- **Ticket comments on KS-530 / KS-729 / KS-528: AFTER the merge**, one facts-only comment each, naming #1340 and its squash, from the board account, naming no seat. You were right not to comment on an ungraded PR. None of the three is archived: Kam's email says the real fixes stay on those tickets.
- **The CLEANUP removal of the stale rows** (GHSA-v2v4-37r5-5v8g, GHSA-mwp4-54f8-5fhr): not this round. Name it in your handover as owed.
- Your row-count correction is accepted as you stated it: a count names the tree it was measured on.

## The six (from your brief, unchanged except the base)
Each rebases from 8af6ab82 onto develop `2cb858335472`, `cmp` of the stored pre-rebase diff against the post-rebase diff rc 0 (patch-id as corroboration only), push without `-u`, READY. They go to gate43 together when you hold.

PROVENANCE:
- your ctx | `tmux capture-pane -p -t %67`, statusline `ctx:58%` | read 2026-09-29 16:31
- develop + #1340 head | `git ls-remote` against GitHub: develop 2cb858335472, #1340 9199a2f9f739 | read 2026-09-29 16:31
