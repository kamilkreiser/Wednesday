# Gate 311, TIER 2 (Sonnet, routing v1.0 tier-2 row), ONE batched session: R 98th round 2 = PR 2176 (KS-1927, demo-service) and PR 2177 (KS-2163, originate). Two PRs, one verdict file with one section per PR. Commissioned 2026-11-11 ~23:3x AEDT by the Mac mini Wednesday seat. Both carry ONE product file: if either touches a security surface by your read, RAISE it to tier 1 in the verdict and say why; do not continue it as tier 2.

Common rules: the tier-2 shape of /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-10_gate306-tier2-pr2166-2169/commission.md (read whole; its common-rules pointer and Constraints apply unchanged). Calibration: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_gate307-tier2-pr2170/verdict.md.

Pins (Wednesday's ls-remote 23:3x AEDT, equal to the READY's 12:30:23Z reads; RE-READ at start and end, say whether each moved):
- develop 98d7a21cf207241847e4e317413776413db54980
- PR 2176 head 69aca3e281a40d3607a1c4b3d054e1b30df90776
- PR 2177 head f252dd2ca9c04cdda0bcd67fcaec45e115b307db
Both branches are cut on 2e998b8d9aea (one commit behind develop; the move touched only analytics). Ask your merge-tree questions onto 98d7a21cf207.

READY (read whole; reproduce, do not trust): /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_gate311-tier2-pr2176-2177/ready_r98_round2.txt. The commissioning mail: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-11_R98_addendum_o144_rows.md. The Spark operator's report behind both held passes: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_spark-operator-o144/report.md. The PRs are model-written (DeepSeek V4 Flash on the Spark), applied byte-for-byte by the seat: read the product lines as you would any author's.

Questions, per PR:
1. File set at the head: exactly the two files the READY names (PR files API + a diff read; planted difference control). Product numstat: persona.ts +5/-0, idNamespaceCollision.ts +11/-1.
2. Does the change do what its ticket asks and no more? Read KS-1927 and KS-2163 whole on Linear (read-only). KS-2163 offers two outcomes; Wednesday ruled BUILD (in the addendum); judge the build on its merits, not the choice.
3. RED-FIRST: in YOUR scratch copy, the new cells fail for the right reason with the product file put back to develop's bytes, and pass at the head (seat: 2 of 5 for 2176, 4 of 10 for 2177). Add at least one mutant of your own per PR that a correct test must catch (2176: drop the headersSent guard, or call removeHeader unconditionally; 2177: drop the `key === 'cause'` skip, or visit without a try). Whole service suites at the head against develop's counts (seat: demo-service 103 -> 108; originate 2592 -> 2602, 0 failed; the operator reported 11 baseline reds in originate and the seat read none: settle which, with the command and rc). Whole-suite legs only at load1 < 8; otherwise name what you deferred.
4. PR 2176: with the ks1868 persona test's stub res (no removeHeader), does every existing cell still pass? Is there any path where the cookie is copied, the 500 is sent, and Set-Cookie still leaves?
5. PR 2177: can the widened walk report a refusal that is NOT a migration 050/051 collision (a false 409)? Is it bounded (depth, seen-set, a Proxy whose ownKeys throws, a getter that throws on every key)? Any measurable cost on a deep or wide error object?
6. Bodies: title 'Refs KS-NNNN:'; no closing word in closing form; Wednesday's BUILD ruling present in 2177's body as hers; carried vs run named honestly.
7. Merge tree of each PR onto 98d7a21cf207: clean, with a planted conflict control; no other open PR touches either write path.
Constraints: read-only on the Secuura checkout (ls-remote, show, log, diff, ls-tree, cat-file, grep only, with GIT_OPTIONAL_LOCKS=0; fetch or clone into YOUR scratchpad only); no push, no merge, no board/Linear/GitHub writes, no mail; never print secrets; no cd; quoted heredocs; never rm.
OUTPUT: verdict.md in this folder: per PR, GO / GO WITH NOTES / NO GO at its head sha (and the tier, raised or not), findings numbered G311-<PR>-N with severity, what you ran (commands + rc + load1), what you did NOT run. Return it in full.
