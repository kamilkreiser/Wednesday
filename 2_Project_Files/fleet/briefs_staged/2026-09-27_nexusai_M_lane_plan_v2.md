# BLUF — NEW SEAT Datasec/NexusAI-M. The 09-25 lane plan is DRAINED: every lane built its list, and the results are merged or waiting on gates. Your FIRST deliverable is LANE PLAN v2: which open RD tickets agents can do now, split into lanes that touch no file any open branch or live seat holds. THEN you take lane 1 (the server.js family) and build it. You are ALSO the merge author for the six lane-1 READYs S84M left FROZEN, once their gate returns. Nothing merges without a QA gate verdict at its head plus Tuesday's GO.

**Addressed to the cockpit seat `Datasec/NexusAI-M` only.** `Datasec/NexusAI-P` (S85P, lane 4) is live and shares this inbox. A mail addressed to NexusAI-P is not yours. Establish which seat you are from your own pane, launcher and process tree, never from which thread looks familiar. Derive your seat number from the project's own history (5_Project_History), not from this mail.

## AUTHORITY
- Kam, Tuesday's terminal, 2026-09-25 ~22:0x AEST, after `/login` (new account), verbatim: *"New account logged in, so you should have plenty of Azure credits. Please work your way through the tickets and merge once tested."*
- Re-affirmed 2026-09-27 ~08:2x AEST, after a second `/login`, verbatim: *"New account logged in. Please keep going with the work."* The usage gauge reads 1% on the new account.
- Recorded in Tuesday's EXPIRING-GRANTS: merges to main only on Tuesday's GO, after a QA gate at the head and a full verify, one at a time.

## STATE AT LAUNCH (measured by Tuesday)
- main = 1904765 (Tuesday's `git ls-remote origin refs/heads/main`, 2026-09-27 08:3x AEST). All of batch 1 and batch 2 is merged.
- **Open READY branches. FROZEN: do not move these heads. Their FILES are claimed until they merge:**
  - Lane 2 (author S84N, wrapped). Batch-3 gate being drafted: RD-324 168d850 · RD-684 7085ee7 · RD-685 9d7076b · RD-424 2ce26eb · RD-314 ce148d5. Files: backend/dataErasure.js, jsonStorage.js, azureLogAnalytics.js, customerDataFiles.js, recoveryLocations.js, and their tests.
  - Lane 3 (author S84O, wrapped). Batch-4 gate being drafted: RD-418 5a782c1 · RD-425 8823458 · RD-698 44bc804 · RD-699 02fe76a · RD-443 8e27dc2. Files: .dockerignore, Dockerfile, __tests__/helpers/image-manifest.js, image-content-exposure, rd385.
  - **Lane 1 (author S84M, wrapped; now YOURS to merge when gated):** RD-413 f70594a · RD-695 ad97d12 · C-170 package-into-main be0fe37 · RD-681 4209299 then RD-682 f15fed6 (stacked) · RD-627b c82aa92 · RD-696 2c221fa. Files: backend/server.js, aiConfigProvenance.js, emailService.js, first-run-setup.*, azure-marketplace/**. Tuesday drafts their gate next. Read HANDOVER-S84M.md at the project root WHOLE before anything else.
  - Lane 4 (S85P, LIVE): static/js/settings.js, settings.html, entra-provisioning-ui.js, css/dark-mode.css, keyboard-focus.css, backend/routes/entraProvisioning.js, test helpers css-colors/dom/vendor-surface, tests/e2e, docs/BRAND.md.
- The board: RD In Progress = 12 (board_count.sh, a real count). To Do, Testing and Release Ready each exceed one 250-row page (board_count refused a total). You measure the totals, paginated, with the predicate stated.

## HARD BOUNDARIES
- **No demo redeploy, no production, no Partner Center, no money, no mail to any human.** A merge must not deploy: check the deploy-demo.yml guard each time.
- The customer-test environment (73e9b141) and Friday's HPSM-POC are not touched.
- Tickets that need Kam or a client human are NOT lane work: list them separately, one line each with the reason. Tuesday cards them.
- Your repo rules stand: C-68 (never rebase a gated commit; merge forward), C-57/C-89 (counts regenerated once, never hand-edited), every jest run through `session-tools/nexusai-lock.sh` (C-141 addendum 4: `--after <ticket>` for merge tickets), SESSION_SECRET unset for verify, C-110 (record the foreign-server count; a zero is reportable only if a control fired in the same window).
- Datasec seats are retired BY HAND. When you wrap, mail the wrap to tuesday-agent@ and say so. Do not trust `cockpit.sh rotate`: it is wired to the other coordinator.

## DELIVERABLE 1 — LANE PLAN v2 (mail within your first hour, ~1 page, written as a file in 5_Project_History like the 2026-09-25 plan)
1. **Sweep the RD board** (To Do + In Progress + Testing, paginated, count + predicate stated). For each candidate: is it agent-actionable now? (no human input, no Kam ruling, not blocked). Board-search before listing anything as new.
2. **Exclude** every ticket already READY or in a gate (listed above), and the S84 lanes' carried items. Include the tickets filed during the S84 run (e.g. RD-686 to RD-705 range, RD-674, RD-697, RD-689, RD-690, RD-700, RD-701, RD-702, RD-703) if agent-actionable.
3. **Lanes:** 2 to 4, each an ordered list plus its FILES. No lane may share a file with another lane, with an open READY branch above, or with S85P's lane 4. Where a ticket needs a claimed file, it queues behind that branch's merge; say which.
4. **Per ticket:** tier (tier 1 security/auth/data/deploy/what ships; tier 2 tests/docs/config), size, and the file:line where the defect lives, read at source on 1904765.
5. **Close-outs:** tickets already fixed on main whose Jira is stale. You may post the evidence comment (commit + file:line) and transition them yourself, under this project's own board rules. List what you did.
6. **NEEDS KAM:** refresh the 09-25 list (RD-536, RD-594, RD-646/647 whose C-145 trigger is met, RD-633, RD-634, RD-386, RD-197(a), RD-193, RD-664, RD-425 PRIVACY half, RD-476, RD-591, RD-368/13/18/20/21/28, RD-50, RD-437's RD-683/RD-594 dependency). Give each one line: the decision in one sentence, and your recommendation. Tuesday turns them into cards.
7. PRIOR-WORK CHECK standing line: before rebuilding, replacing or removing anything, look first (git log -S/--follow, CLARIFICATIONS, HISTORY, handovers, tickets), write down what existed and why, and keep what works (C-49/C-50). Every READY carries a PRIOR WORK section.

## THEN — LANE 1 IS YOURS
Take lane 1's first ticket that does NOT collide with the six frozen lane-1 READYs (or measure the merge-tree in a scratch object dir and state it). Branch from current main, build, red-proof (red before the fix, green after, plus a control), full verify, push the branch, and send READY FOR QA to tuesday-agent@ (branch + head sha, sets not counts, PRIOR WORK, NOT TESTED). Continue down lane 1 while gates run. When the lane-1 gate verdict lands, merges take priority over building, one at a time, each on Tuesday's RELEASE.

## PLAN CONFIRMATION
Mail `[Datasec/NexusAI-M -> Tuesday] QUESTION: plan confirmation` and start the read-only sweep without waiting.

RULED BY KAM, NOT YET IN AN ARTEFACT
- (none open for NexusAI. Checked by Tuesday 2026-09-27 08:35 with `decision_queue.sh list ruled --undelivered`: nexusai-package-files-scope = C-170, which-subscription = C-157, store-wizard-clickthrough = C-159, all read at source in CLARIFICATIONS and marked delivered.)

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- Tuesday 2026-09-26: C-141 addendum 4 (`--after` yields place a ticket directly behind the named gate/merge ticket).
- Tuesday 2026-09-26 ~19:1x: C-141 yields are self-applied and NOT mailed.
- Tuesday 2026-09-26 09:23: nexusai-lock.sh is never edited in place (new file, arms on a scratch lock dir, atomic mv).

PROVENANCE:
- Kam's words | Tuesday's terminal after /login | read 2026-09-25 ~22:0x and 2026-09-27 ~08:2x
- main 1904765 | git ls-remote origin refs/heads/main in /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files | read 2026-09-27 08:3x
- lane-1 frozen READYs and their heads | S84M wrap mail 2026-09-26T19:31Z + each READY mail in tuesday-agent@ | read 2026-09-27
- lane-2/3 READY heads | S84N wrap 19:33Z, S84O wrap 19:32Z, their READY mails | read 2026-09-27
- RD In Progress = 12; other states over 250 | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/board_count.sh jira, project = RD - Tuesday's tool, not yours | read 2026-09-27 08:3x
- NEEDS-KAM list | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/5_Project_History/2026-09-25_S84M_lane-plan.md | read 2026-09-27
Self-check note: frozen heads never move; lanes never share a file; merges only on a gate verdict plus Tuesday's GO; nothing deploys.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-27 08:36
