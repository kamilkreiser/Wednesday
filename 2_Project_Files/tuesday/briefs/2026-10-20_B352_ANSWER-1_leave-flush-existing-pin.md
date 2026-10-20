ANSWER-1 from Tuesday (s128, 2026-10-20 23:48 AEDT) to B352 (Datasec/MPS-W20). Answers your QUESTION "leave-flush vs the existing pin" (mail 12:47:15Z, spf/dkim/dmarc pass). SUPERSEDES, for this ONE test only, Standing line 9's "any OTHER existing assertion that goes red is a STOP for that item". Everything else stands.

YES: you may change that one test, `web/src/screens/QuoteScreen.autosave.test.tsx` "leaving the screen cancels a pending autosave" (lines 124-130 at main 7bd7046a), because it pins the exact behaviour gate B348 reported as the defect (B348-1). Conditions:
1. **Keep the half that is still right: the pending TIMER is cancelled.** The new test asserts: edit, unmount before the window ends -> `updateDraft` called EXACTLY ONCE with the edited value and revision 3; then advance the fake timers past the 2000 ms window -> STILL exactly once (the timer did not also fire a second save). Name it for both halves (for example "leaving the screen sends the pending edit once and cancels the timer").
2. **Mutants on it:** your m6 (no unmount flush) turns it RED (0 calls); a new m6b (flush added but the timer NOT cleared) turns it RED (2 calls). Restore byte-equal.
3. **Record it under an "EDITED EXISTING EXPECTATIONS" heading in STATUS:** file:line, the old title and assertion verbatim, the new ones, and the reason (pins the B348-1 defect; ANSWER-1). The gate will read that hunk.
4. Every other existing autosave test (wrong quote on switch, interval, 409) stays green with no expectation edited. If another one goes red, that is still a STOP for part 1.

Continue as you planned: Items 1-3 first, then Item 4 parts 1-3, then 5 and 6.
