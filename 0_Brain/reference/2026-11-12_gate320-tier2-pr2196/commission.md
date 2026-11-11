# Gate 320, TIER 2 (Sonnet, routing v1.0 tier-2 row: tests + a guard baseline, no product source), ONE session: Seat A 21st row C = PR 2196 (KS-2125: the KS-1536 role-list guard's baseline lowered oauth.ts 2 -> 1 and users.ts 11 -> 9, plus a NEW packages/shared vitest asserting each of the two EQUALS the guard's own count, plus a flow + cheat fragment pair). Commissioned 2026-11-12 ~06:5x AEDT by the Mac mini Wednesday seat. The seat read it as tier 1; Wednesday tiers it 2 (no service source, no behaviour change). RAISE to tier 1 if any changed line is outside the four files the READY names.

Method: copy-and-change of /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate318-tier2-pr2194/commission.md (read it whole, and through it gates 316/314/313: common rules, Constraints, output shape and controls apply unchanged). Calibration: gate 318's verdict.md.

Pins (Wednesday's ls-remote 06:5x AEDT; RE-READ at start and end): develop c78c80bd537015674fa5e22701d745946f94d4fb; PR 2196 head fed1d35ce95c4983952a8a780b92dc4e2c522e16 (one commit, parent 2c86b074da97; develop is one test-only commit past it). Merge-tree onto the newest develop you read.

READY (read whole; reproduce, do not trust): ready_a21_ks2125_mail.txt in THIS folder. Questions:
1. Scope: `git diff --numstat` of the PR = the four files only (baseline json +2 -2, new test +59, two fragment files); no service source.
2. The counts: re-take oauth.ts and users.ts counts AT THE MERGE TREE with the guard's OWN rule (read the guard test, run it or its counting logic in a scratch copy): 1 and 9? A different number is a NO GO finding.
3. The new test DUPLICATES the guard's counting rule (the guard exports nothing). Is the copy faithful (regexes, filter, length cap, exclusions) to the guard's text at develop? A divergence = a finding. Reproduce red-first (baseline reverted -> R1, R2 red) and one mutant of your own that the seat did not run.
4. Is a tight EQUALS pin the right ratchet, or does it make every future PR that removes a role list from those files fail until it lowers the baseline in the same PR (state that consequence plainly as a Note: it is the point, per the READY, but the builder of the next such PR needs to know).
5. The guard (99) and the whole packages/shared suite at the merge tree: the two known reds only (ks1725-zod3-compat 114 vs 113 = KS-2170; wallet-signature, the Node class)? Any third red is a finding.
6. Census (GraphQL, control PR 2125 api-gateway/src/index.ts must fire) on the four paths and on oauth.ts / users.ts (PR 2075 is the known count-neutral one: confirm by its patch).
7. Fragment pair: docs-fragments check passes at the head.

Spark shadow (after your verdict): spark_gate.sh / spark_review.py WITH --pr-body-file on PR 2196 (work dir in your session scratchpad, not under WEDNESDAY); record verdict, recall, false claims.

OUTPUT: verdict.md in THIS folder (first line 'PR 2196: GO / GO WITH NOTES / NO GO (at head ...; tier ...)'; findings G320-2196-N graded Minor / Note / Info with evidence; NOT TESTED; Spark shadow). If your Write is refused, return the verdict text in full. Constraints as gates 313-318: write only in this folder (scratch under scratch/), read-only git verbs in the shared Secuura checkout with GIT_OPTIONAL_LOCKS=0, no push, no PR comment, no Linear write, no mail, no rm, no cd, never print .env values, GitHub reads GET only, GraphQL preferred, never a per-PR or per-file REST loop. Load: whole-suite legs at load1 < 8.
