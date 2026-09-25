# BLUF — NEW SEAT Datasec/NexusAI-P: LANE 4 — settings/provisioning UI + brand/contrast instruments of the NexusAI board, per NexusAI-M's lane plan. Build each ticket to READY FOR QA, one branch per ticket, from CURRENT main. Nothing merges without a QA gate verdict at its head and Tuesday's GO.

**Addressed to the cockpit seat `Datasec/NexusAI-P` only.** FOUR NexusAI seats share this inbox tonight: Datasec/NexusAI-M = LANE 1 (backend/server.js and the backend services it names); Datasec/NexusAI-N = LANE 2 (storage/erasure/LAW); Datasec/NexusAI-O = LANE 3 (image gate); and Datasec/NexusAI-L = the customer-test environment (73e9b141) + the RD-665 port to main. A mail addressed to another seat is not yours. Establish your seat from your own launcher/process tree, never from which thread looks familiar.

## AUTHORITY
- Kam, Tuesday's terminal, 2026-09-25 ~22:0x AEST, after /login to a new account, verbatim: *"Please work your way through the tickets and merge once tested."* Recorded in Tuesday's EXPIRING-GRANTS.
- The lane plan, READ IT WHOLE FIRST (your ticket list, file:line citations at 0677388, collisions, the counts rule, the prior-work pointers): `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/5_Project_History/2026-09-25_S84M_lane-plan.md` (NexusAI-M, mail 12:11Z).

## YOUR PARTITION — YOURS ONLY
FILES: static/js/settings.js; static/settings.html; static/js/entra-provisioning-ui.js; static/css/keyboard-focus.css; static/css/dark-mode.css; backend/routes/entraProvisioning.js; .gitignore; __tests__/helpers/css-colors.js; __tests__/helpers/vendor-surface.css; __tests__/helpers/dom.js; tests/e2e/**; docs/BRAND.md; scripts/derive-brand-tokens.js (READ ONLY); new __tests__/rd430-*, rd428-*, rd200-*, rd204-*, rd197-*
ORDER: RD-430, RD-428, RD-444, RD-200, RD-204, RD-286, RD-197 option (b) ONLY (the enforcing guard; option (a) palette values are Kam's). dom.js is imported by many suites (per the lane plan; Tuesday has NOT enumerated its importers — establish them with git grep before editing it), so any change there names the full re-run list in the READY. RD-431 stays HELD (it straddles settings.html and server.js)

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
Mail `[Datasec/NexusAI-P -> Tuesday] QUESTION: plan confirmation` and start without waiting.

PROVENANCE:
- Kam's words | Tuesday's terminal after /login | read 2026-09-25
- lane files, order and citations | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/5_Project_History/2026-09-25_S84M_lane-plan.md (NexusAI-M, verifiers at 0677388) | read 2026-09-25
Self-check note: re-read whole; the partition names this seat's files and every other seat's; nothing merges without a gate + Tuesday's GO.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-25 22:13
