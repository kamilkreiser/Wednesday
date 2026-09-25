# BLUF — NEW SEAT Datasec/NexusAI-N: LANE 2 — storage, erasure, LAW query of the NexusAI board, per NexusAI-M's lane plan. Build each ticket to READY FOR QA, one branch per ticket, from CURRENT main. Nothing merges without a QA gate verdict at its head and Tuesday's GO.

**Addressed to the cockpit seat `Datasec/NexusAI-N` only.** FOUR NexusAI seats share this inbox tonight: Datasec/NexusAI-M = LANE 1 (backend/server.js and the backend services it names); Datasec/NexusAI-O = LANE 3 (image gate); Datasec/NexusAI-P = LANE 4 (settings UI + brand instruments); and Datasec/NexusAI-L = the customer-test environment (73e9b141) + the RD-665 port to main. A mail addressed to another seat is not yours. Establish your seat from your own launcher/process tree, never from which thread looks familiar.

## AUTHORITY
- Kam, Tuesday's terminal, 2026-09-25 ~22:0x AEST, after /login to a new account, verbatim: *"Please work your way through the tickets and merge once tested."* Recorded in Tuesday's EXPIRING-GRANTS.
- The lane plan, READ IT WHOLE FIRST (your ticket list, file:line citations at 0677388, collisions, the counts rule, the prior-work pointers): `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/5_Project_History/2026-09-25_S84M_lane-plan.md` (NexusAI-M, mail 12:11Z).

## YOUR PARTITION — YOURS ONLY
FILES: backend/jsonStorage.js; backend/recoveryLocations.js; backend/dataErasure.js; backend/customerDataFiles.js; backend/azureLogAnalytics.js; __tests__/helpers/erasure-write-guard.js; new __tests__/rd639-*, rd324-*, rd627a-*, rd424-*, rd314-*
ORDER: RD-639, RD-627a (the .tmp half only), RD-324, RD-424, RD-314 (server.js callers READ only; a fix needing server.js stops and mails)
ITEM 0, BEFORE the lane (board only, no code): the CLOSE-OUT list from the lane plan — RD-508 (1f27b4d), RD-592 + RD-593 (4230d23), RD-624 (ed6f3fc), RD-448 (e70d949/d364514), RD-443 docs half (4b8c418/5700df5). For each: re-verify the fix is on CURRENT main at source (the commit is an ancestor of origin/main and the cited lines hold), post ONE facts-only evidence comment, transition to the done state. RD-555 (the O-1 split question), RD-262 (children still open) and RD-606 (retire the s76d copy) are NOT closed: comment what remains. Also append the lane plan's 'NEEDS KAM OR A RULING' list to RD-536 (Kam's own list) as ONE comment, one line per ticket with the reason.
**NOT YOURS — another seat is in them right now:** backend/server.js and the lane 1 services (NexusAI-M); every file listed under the other lanes in the lane plan. If a fix needs a file outside your list: STOP that ticket, mail Tuesday with the file and why, take the next ticket.

## STANDING LINES
- Branch from CURRENT main; re-read `git ls-remote origin refs/heads/main` before branching and before every push (main moves tonight).
- Each branch commits its own `--update-counts`; at merge the counts are REGENERATED ONCE on the merged tree (C-68 amendment / C-57 / C-89). Never hand-edit.
- Red-first: a new cell red at current main, green after the fix, plus a control that can fail. Full verify through `session-tools/nexusai-lock.sh` with SESSION_SECRET unset. The lock is shared by FOUR seats: queue, never take over.
- Worktrees only. No write verbs in the stale 2_Project_Files clone (C-28): no fetch/pull/checkout there.
- PRIOR-WORK CHECK before rebuilding, replacing or removing anything (git log -S/--follow, CLARIFICATIONS, history, the s59 WIP branches the plan names). WIP branches are INTENT, not code to rebase (C-68).
- READY FOR QA to tuesday-agent@: branch + head sha, the ticket, sets not counts, a PRIOR WORK section, NOT TESTED, the QA tier the plan gives.
- No merge, no deploy, no demo, no production, no Partner Center, no mail to any human. Client-facing text goes on the ticket only.

## PLAN CONFIRMATION
Mail `[Datasec/NexusAI-N -> Tuesday] QUESTION: plan confirmation` and start without waiting.

PROVENANCE:
- Kam's words | Tuesday's terminal after /login | read 2026-09-25
- lane files, order and citations | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/5_Project_History/2026-09-25_S84M_lane-plan.md (NexusAI-M, verifiers at 0677388) | read 2026-09-25
Self-check note: re-read whole; the partition names this seat's files and every other seat's; nothing merges without a gate + Tuesday's GO.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-25 22:13
