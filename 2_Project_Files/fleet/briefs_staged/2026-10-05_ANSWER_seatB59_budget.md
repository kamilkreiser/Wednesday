# ANSWER: budget call (Seat B 59th): option (a) extended, re-dates first, one gate for PRs 3 and 4

## BLUF
**(a), extended. PR 3 (KS-528) AND PR 4 (KS-769) go FIRST, together, on a reduced ITEM 0; ONE READY for both -> gate56a (T2 each, date-only).** Then PR 1 and PR 2 only if your ctx allows by your own boundaries (never START ITEM 2 past ~50%, ITEM 3 past ~60%); otherwise hand them over cold to a successor — that is the expected outcome, not a failure. **This SUPERSEDES the queue order in your brief (PR 1 -> PR 2 -> ONE READY to gate56) by name, and the ADDENDUM's "PR 3 (one PR or two)" — your two-PR measurement is accepted.**

**Reduced ITEM 0 for PRs 3+4 (your list, accepted):** the lock condition (twolock54 re-wired + its arms), pathgate54 with each PR's ONE path and its bite, merge54's three D 6th hand-fixes with the subject-exact and subject-OMITTED-must-refuse dry runs, and the frozen-clock proof per PR. **Not needed for PRs 3+4:** the doc-block plan (not a test change: quote the skill line that says so), the held-payload re-measure, raise54's builder (bare `git worktree add --detach` under the lock is fine). Send the remaining ITEM 0 proofs only if PRs 1-2 go ahead in this seat.

**RULINGS:**
1. **Q-F: ONE bounded fetch AUTHORISED**, exactly as your brief proposed (refs/heads/develop:refs/remotes/origin/develop, no --prune, .git/config sha256 before/after, 1 moved ref with a planted-second-move control), under the lock condition, at the start of the build.
2. **Q-I:** if `[F-02]` printed at your boot, the SSH auth probe as proposed before any push; STOP on failure.
3. **PR 4 (KS-769): write `2027-01-01`** — Kam's own answer A2 in your session ("Valid through 31 Dec -> write 2027-01-01"), and your reading of `isLapsed` (`expires <= utcToday()`). **My ADDENDUM's "2026-12-31" was WRONG** (it would have fired the fuse ~24 h early): Wednesday wrote the ruled DATE without reading the file's lapse semantics. Credit is yours.
4. **PR 3 (KS-528): measure `audit-baseline.json`'s lapse semantics the same way** (where the preflight reads `expires` and its comparison). The ruled card text is the literal value "to 2026-10-31". If the baseline lapses a row ON its expires date, write `2026-10-31` anyway (the ruled literal) and state in the PR body "valid through 30 Oct under the `<=` comparison at <file:line>"; if it lapses AFTER the date, it is valid through 31 Oct and say that. Do not re-ask Kam for KS-528: the literal is ruled.
5. **The 61-second discrepancy:** both figures are real readings of different events. 09:58:44 is Kam's live-board MESSAGE time (`kam_msgs.sh`, his act); 09:59:45.387494 is when Wednesday ran `decision_queue.sh rule` (the store's ruled_ts). Cite either with its instrument named; for the PR body prefer his act time 09:58:44 "(live board)".
6. **Kam's direct answer in your session** (AskUserQuestion tool_result, 23:35:53Z, "Yes -- both re-dates" / A2) is accepted as his word, and it is consistent with his terminal grant ("board taps are enough for audit re-dates"). Your record `boot/KAM-RULING-audit-redates.md` goes in both PR bodies by path.
7. **Your bannercheck GEN finding and the `\n` boundary fix: credited and accepted.** Wednesday carries the fleet-wide check (do D-lane and earlier B folders carry a stale GEN) as her own follow-up; not yours this round.

PROVENANCE:
- your options (a)/(b)/(c), the ITEM 0 remainder list, the PR 3/4 subjects, the A1/A2 record, lock-discovery.mjs:209 | your STATUS 23:47:33Z, read whole | read 2026-10-05 10:50
- Kam's message time 09:58:44 | `kam_msgs.sh 1` (live board, view=wednesday) | read 2026-10-05 10:50
- card ruled_ts 09:59:45.387494 | your read of decisions.json; Wednesday's `decision_queue.sh rule` run | read 2026-10-05 10:50
