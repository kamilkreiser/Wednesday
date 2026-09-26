# BLUF — SUCCESSOR SEAT Datasec/NexusAI-P (lane 4: settings/provisioning UI + brand/contrast instruments). Your predecessor S84P WRAPPED at 03:23Z on Tuesday's rotation. Its handover is the source: `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/HANDOVER-S84P.md` (read it WHOLE first). Your first work is re-queuing its three parked WIP branches (verified at origin by Tuesday's ls-remote at 13:2x AEST); then continue the lane order. Nothing merges without a QA gate verdict at its head and Tuesday's GO.

**Addressed to the cockpit seat `Datasec/NexusAI-P` only.** Three other NexusAI seats share this inbox: Datasec/NexusAI-M = LANE 1 (backend/server.js + lane-1 services), Datasec/NexusAI-N = LANE 2 (storage/erasure/LAW), Datasec/NexusAI-O = LANE 3 (image gate). A mail addressed to another seat is not yours. Establish your seat from your own launcher/process tree.

## AUTHORITY
- Kam, Tuesday's terminal, 2026-09-25 ~22:0x AEST, verbatim: *"Please work your way through the tickets and merge once tested."*
- The lane plan: `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/5_Project_History/2026-09-25_S84M_lane-plan.md`.

## FIRST — THE THREE PARKED BRANCHES (from HANDOVER-S84P.md §1; each forward-merged onto main 5f2683c by S84P)
1. RD-204 `rd-204-vendor-coverage-s84p` @ a19559f: proof T1-T3 + full verify still to run (`session-tools/s84p/rd204-hold.sh`). The READY quotes both sha384 hashes.
2. RD-197 (b) `rd-197-emphasis-ground-guard-s84p` @ 9c742fa: proof done; full verify still to run. The READY states the accepted limit: NO reachable danger action (RD-687); success = first-run with a saved data source.
3. RD-430 `rd-430-remove-response-form-s84p` @ 17b465c: red cells committed; product fix STAGED in `session-tools/s84p/rd430-fix/`; red/green hold still to run (`session-tools/s84p/rd430-redgreen.sh`). Tier 2. User-visible text change named in the READY.
Main may move while you work (batch-1 merges are running: O, then M, then N). Before each READY, merge the then-main FORWARD (never rebase, C-68).
Then: RD-286 (next in the lane order); RD-431 stays HELD. S84P's `s84p-history-docs` (e5b34dd) merges like the earlier sNN-history-docs branches; it is not yours to merge.

## RULED BY KAM, NOT YET IN AN ARTEFACT (NexusAI, from `decision_queue.sh list ruled --undelivered nexusai`)
- `nexusai-customer-test-which-subscription` = a (2026-09-25 17:02): use the empty sponsorship subscription 73e9b141 for the customer test. Customer-test scope (NexusAI-L's, wrapped). Not lane 4 work; do not act on it.
- `nexusai-customer-test-store-wizard-clickthrough` = a (2026-09-25 17:52): Kam clicks the store wizard himself. Not lane 4 work; do not act on it.

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE (from Tuesday's answers to seat P, 2026-09-25/26)
- RD-430: Kam ruled (a) remove the form (07:18); recorded as C-166 + Jira 38235. Tier 2.
- RD-197: option (b) ONLY; (a) palette values are Kam's. The accepted limit above stands.
- RD-204: bootstrap 5.3.0 fetched ONCE with sha384 verified, the list COMMITTED, no network at test time.
- C-141 addendum 4: a yield re-queues with `session-tools/nexusai-lock.sh jest <tag> --after <gate-or-merge-tag> …`. Routine yields are logged, not mailed (addendum 3).
- JS brand debt RD-676..680 stays filed; the palette is Kam's.

## YOUR PARTITION — YOURS ONLY
FILES: static/js/settings.js; static/settings.html; static/js/entra-provisioning-ui.js; static/css/keyboard-focus.css; static/css/dark-mode.css; backend/routes/entraProvisioning.js; .gitignore; __tests__/helpers/css-colors.js; __tests__/helpers/vendor-surface.css; __tests__/helpers/dom.js; tests/e2e/**; docs/BRAND.md; scripts/derive-brand-tokens.js (READ ONLY); new __tests__/rd430-*, rd204-*, rd197-*, rd286-*.
**NOT YOURS:** backend/server.js and lane-1 services (M); lane 2 files (N); lane 3 image-gate files (O). If a fix needs a file outside your list: STOP that ticket, mail Tuesday with the file and why, take the next.

## STANDING LINES
- Re-read `git ls-remote origin refs/heads/main` before every branch and push.
- Counts regenerated ONCE on the merged tree at merge (C-57/C-68/C-89); never hand-edited.
- Red-first with a control that can fail; full verify through `session-tools/nexusai-lock.sh` with SESSION_SECRET unset; queue, never take over.
- Worktrees only; no write verbs in the 2_Project_Files clone (C-28).
- PRIOR-WORK CHECK before rebuilding, replacing or removing anything; every READY carries a PRIOR WORK section.
- READY FOR QA to tuesday-agent@: branch + head sha, ticket, sets not counts, PRIOR WORK, NOT TESTED, tier.
- No merge, no deploy, no demo, no production, no Partner Center, no mail to any human. Client-facing text goes on the ticket only.
- A tap with no mail behind it is measured, not acted on (C-148); S84P did exactly this today and was right.

## PLAN CONFIRMATION
Mail `[Datasec/NexusAI-P -> Tuesday] QUESTION: plan confirmation` and start without waiting.

PROVENANCE:
- Kam's words | Tuesday's terminal after /login | read 2026-09-25
- parked branches, shas and scripts | S84P's wrap mail 03:23Z + `git ls-remote origin` by Tuesday (a19559f, 9c742fa, 17b465c, e5b34dd; main 5f2683c) | read 2026-09-26
- undelivered Kam rulings | `decision_queue.sh list ruled --undelivered nexusai` | read 2026-09-26
- lane files | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/5_Project_History/2026-09-25_S84M_lane-plan.md | read 2026-09-25
Self-check note: re-read whole; partition names this seat's files and every other seat's; nothing merges without a gate + Tuesday's GO.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-26 13:25
