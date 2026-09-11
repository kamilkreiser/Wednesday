## BLUF
- **Plan CONFIRMED as written, including all four points marked BEYOND THE RULING.** Start on this mail.
- One condition on BEYOND 3, one correction to a reason in item 0 (d), and nothing else changes.

## Rulings
1. **Item 0 — confirmed.** Search shape with `run-shell-suites.sh` as the positive control and the literal client-side match on `reached[@]`: exactly right.
2. **Item 0 (d), QA-7 inside the QA-8 ticket: CONFIRMED on your reasons 1 and 2** (same file, same severity, same later-touch route; and QA-7 waits on #953 merging while QA-8 does not — say that in the ticket, as you planned).
   **CORRECTION to your reason 3:** the "ticket creation aggregates" line is NOT a live rule. Kam gave it on 2026-09-06 at 09:42 and withdrew the aggregation half three minutes later; only the assignment half stands (new or unassigned tickets go to our board account). **Do not cite aggregation as a reason in the ticket.** In your handover, name the FILE where you read that standing line, so its owner can correct it at the source. This is Wednesday's record of Kam's withdrawal, not a new ruling.
3. **Item 1 — the Q1 shape table is ACCEPTED whole:** U, FF and N CLEAN; the refused-push row CLEAN on integrity with the verdict line naming the shape matched, and "did the push land" left to the push rc plus the origin read. That split is right.
4. **BEYOND 1 (A: added at a non-origin SHA → DIFF), BEYOND 2 (F: a non-fast-forward move → DIFF), BEYOND 4 (docstring and DIFF line say STOP and mail Wednesday; a restore is a separate, ruled action): ACCEPTED.** All three make a false CLEAN harder and remove the destructive default. With DIFF no longer meaning restore, a false DIFF now costs a mail, not a write into the shared repo.
5. **BEYOND 3 (X: `PROTOCOL-INCOMPLETE`, exit 4): ACCEPTED, with one condition.** Before you assign exit 4, read every exit the file already uses and put the full exit-code table in the docstring (0 CLEAN · 3 DIFF · 4 INCOMPLETE · anything else). An arm must show that a verify with origin unreadable does not print CLEAN under the OLD verify either way; state what OLD does.
6. **Preflight F-02 and KS-78: not blockers this round.** No push is commissioned and no stack is exercised. Record both in the handover as seen. F-02 describes a keychain identity; git uses the repo's `core.sshCommand`.
7. **Your paged-search failure, voided rather than diagnosed:** correct handling. The direct GET is the reading that stands.
8. **Kam's queue items you surfaced (KS-597, the extranet decisions, `feature/y`/`feature/w`, the `/api/seen` hook line): all already with Kam.** No action from this seat.

## Unchanged
Round ends at READY FOR REVIEW on item 1, then handover and wrap. The 50% checkpoint rule stands. Every HOLD in the brief stands.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- The brief's list (squash · Done-with-assignee · the leg-14 HOLD · #953's PROTOCOL-DIFF expected, no restore · KS-1087 High) plus rulings 2–5 above.
