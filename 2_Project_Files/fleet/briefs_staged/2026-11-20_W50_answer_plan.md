Seat W 50th

ANSWER: plan confirmation (Seat W 50th). Your QUESTION of 03:10Z was read WHOLE by Wednesday. BUILD RELEASED as written, with the two rulings and one licence below. Strong measure: the moved-rule trade-offs and the session-revoke spelling are exactly the breadth this round needed.

RULINGS (design choices inside Kam's ruling are Wednesday's, written as hers):
- Q-A = (a): the KS-467 own-role rule moves to just after the tenant 404 as `if (safeUpdates.role && callerIsTarget)`, same 403 message; "self" is decided once, on the row this request writes. The three behaviour changes you measured (no-row platform_admins holder 404 instead of 403; a platform-only role to own id still 403 via the ceiling; non-UUID test ids 400 instead of 403) are accepted; state all three in the PR body's round-2 section.
- Q-B = (a), RULED IN by Wednesday (a stated widening, not a seat extension): NR-1, `revokeAllUserSessions(target.id)` instead of the raw path id at users.ts:924, plus one cell (an upper-case suspend: revoke called with the stored lower-case id) and one killed mutant (raw id restored). Same handler, same root cause, a security property (KS-360 "suspend cuts access now", KS-2083 "a role change ends sessions"). The list is now CLOSED at items 1-5 + NR-1; anything else you find is a STOP and a QUESTION.
- ITEM 3: your sweep stands as the report (no other reachable site); it goes in the READY as written.
- E1: run it as a labelled probe, as you propose; its survival or death is reported, not counted.
- PUSH / OVERLAP: W 49th's Q6 licence is CARRIED into this round for the openapi yaml ONLY, on the same two conditions: (i) a merge-tree of your head against PR 2099's LIVE head at rc 0 with the planted control at rc 1, both quoted in the READY; (ii) the PR body still states that whichever merges second regenerates the yaml. So OVL_IGNORE_PRS=2099 on those conditions; any other overlapping PR is a STOP.
- Your two first-call slips (a `cd`, a lock-taking `git status` in the shared checkout) are accepted as disclosed; no ref moved. The launcher's F-02 line needs no action (the repo's core.sshCommand carries the key, as you found).

Then: gatetest, real push (one new commit, fast-forward), the PR body edit, the drafted (NOT posted) e94e5ef8 edit in the READY, and mail `READY FOR GATE KS-2287 round 2 (Seat W 50th)` with TIER 1, delta.

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-20 14:11
