# B1466 ADDENDUM-3 (SEAT-D59): the caller bookkeeping write is accepted as outside ADDENDUM-2 condition 1; continue to M2 under S16 = A

From Tuesday, 2026-11-10, answering your `STOPPED: NEEDS TUESDAY` of 21:37:58.

**Answer: yes, accepted.** Your measured reading is that submit and review each save ALL their rows in ONE `SaveChangesAsync` (`FollowUpEndpoints.cs:325`, EF's own transaction), so the action's data fails as a whole. The only earlier committed write in the same request is `CallerFilter`'s (`AssessmentModule.cs:193`) caller bookkeeping: an `app_user` `last_seen` refresh at most every 5 minutes (`Caller.cs:129-135`), or a first-seen user row plus ONE audit row (`:91-111`). That write is outside condition 1. Here is why:
- it is not part of the action: it would be written by ANY signed-in request in that window, a plain GET included;
- a single-row audit insert is what the append-only ledger accepts (Msg 37359 is about a save adding two or more rows: that is B1442 M1's own finding). Your rehearsal should show the single-row insert succeeding beside the two-row refusal. If it does not, STOP before M2;
- if the action then fails, the user is left with a fresh `last_seen` or a first-seen row: true facts, not a half-done action.

**Condition 1 now reads:** the ACTION's rows are written by one transaction with no earlier committed write OF THE ACTION in the same request; `CallerFilter`'s caller bookkeeping (as you cited it, and nothing else) is excluded. Conditions 2 to 4 of ADDENDUM-2 stand. Also put this exclusion in STATUS under PART M and in FOR TUESDAY 2, in plain words.

Continue to M2 under S16 = `A: START PREV THEN DEPLOY`, after re-reading the addenda (now three) as the kit says. Nothing else changes.
