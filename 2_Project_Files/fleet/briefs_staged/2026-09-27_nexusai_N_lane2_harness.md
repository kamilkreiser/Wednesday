# BLUF — NEW SEAT Datasec/NexusAI-N: LANE 2 of lane plan v2, the TEST-HARNESS AND INSTRUMENT lane. Build its ten items to READY FOR QA, one branch per ticket, starting with RD-591 (the port-band collision that contaminated three seats' measurements on 2026-09-21). Nothing merges without a QA gate verdict at its head plus Tuesday's GO.

**Addressed to the cockpit seat `Datasec/NexusAI-N` only.** `Datasec/NexusAI-M` (S86M, lane 1, server.js family) and `Datasec/NexusAI-P` (S85P, lane 4, settings UI + brand) are live and share this inbox. A mail addressed to them is not yours. Establish your seat from your own pane, launcher and process tree. Derive your seat number from 5_Project_History.

## AUTHORITY
- Kam, Tuesday's terminal, 2026-09-25 ~22:0x AEST, verbatim: *"Please work your way through the tickets and merge once tested."* Re-affirmed 2026-09-27 ~08:2x, verbatim: *"New account logged in. Please keep going with the work."*

## YOUR QUEUE — lane plan v2, "LANE 2"
The plan is written at /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/5_Project_History/2026-09-27_S86M_lane-plan-v2.md (your project, by S86M). Read it whole. Its LANE 2 section is your ordered list, with FILES and file:line at main 1904765. In order: RD-591 · RD-648 · RD-649 · RD-608 · RD-697* · RD-640 partial* · RD-609 · RD-653 · RD-671 · RD-700; then RD-614, and RD-629 measured first.
- \* **RD-697 and RD-640's erasure parts go AFTER the batch-3 gate's merges** (the lane-2-of-09-25 frozen branches RD-324/684/685/424/314 on dataErasure.js). Their C-68 re-run set is every erasure-* suite, and editing those files mid-gate moves the gate's ground. RD-640 F-A7's export half (backend/dataExport.js) is free now.
- **Then, Tuesday's session-tools items:** RD-606 (retire s76d/floorcheck.py by QUARANTINE into a dated _quarantine folder, never delete), RD-658, RD-670. **RD-656 (the launcher's step 1 fetching in the stale clone):** a PROPOSED DIFF mailed to Tuesday first. The launcher boots every seat, so it does not change without Tuesday's read.

## RULINGS FOR YOUR ITEMS (Tuesday, 2026-09-27; S86M records them as one C-number)
- RD-591: band by WORKTREE (a stable hash of the worktree path, not JEST_WORKER_ID alone), PLUS a stand-in that REJECTS and LOGS traffic that cannot prove it belongs to this suite (C-115). Red-proof with two seats' worth of parallel runs, and a control proving the reject fires.
- RD-653: the release-time "not now" is LIFTED (2.2.1 is live).

## FILES — yours vs NOT yours
- **Yours:** the LANE 2 FILES list in the plan.
- **NOT yours**, with the other seat working them right now:
  - backend/server.js and the lane-1 family (S86M);
  - settings.*, dark-mode.css, css-colors.js, dom.js, vendor-surface.css, tests/e2e/** (S85P);
  - dataErasure.js, jsonStorage.js, azureLogAnalytics.js (frozen, batch-3 gate);
  - .dockerignore, Dockerfile, image-manifest.js, image-content-exposure, rd385 (frozen, batch-4 gate).
- test-server.js is imported by many suites: every READY that touches it names its C-68 re-run list.
- The counts file is regenerated once at each merge (C-57/C-68), never hand-edited.

## HARD BOUNDARIES
No demo redeploy, production, Partner Center, money, or mail to any human. The customer-test environment and HPSM-POC are not touched. C-68 (never rebase a gated commit). Every jest run goes through session-tools/nexusai-lock.sh (with --after for merge tickets). SESSION_SECRET is unset for verify. C-110: record the foreign-server count, and a zero is reportable only if a control fired in the same window. Two gates (batch 3, batch 4) may be running and share the lock: yield per C-141. Datasec seats are retired BY HAND: mail your wrap to tuesday-agent@. Do not rely on cockpit.sh rotate.

## EVERY READY carries
Branch + head sha, sets not counts, red before / green after / a control, full verify, PRIOR WORK (C-49/C-50: look first, keep what works), NOT TESTED, and the tier (the plan gives it per item).

## PLAN CONFIRMATION
Mail `[Datasec/NexusAI-N -> Tuesday] QUESTION: plan confirmation` and start RD-591's read-only prior-work check without waiting.

RULED BY KAM, NOT YET IN AN ARTEFACT
- (none open for NexusAI. Checked by Tuesday 2026-09-27 08:35 with decision_queue.sh list ruled --undelivered; C-157, C-159, C-170 delivered.)

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- Tuesday 2026-09-27 08:5x: the NEEDS-TUESDAY rulings in the ANSWER to S86M ("lane plan v2 accepted"), incl. RD-591 and RD-653 above.
- Tuesday 2026-09-26: C-141 addendum 4 (--after); yields self-applied and not mailed.
- Tuesday 2026-09-26 09:23: nexusai-lock.sh is never edited in place.

PROVENANCE:
- lane 2 list, files, file:line | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/5_Project_History/2026-09-27_S86M_lane-plan-v2.md (S86M's mail 22:51Z, read whole by Tuesday) | read 2026-09-27
- frozen batch-3 and batch-4 heads | the S84N and S84O wrap mails 2026-09-26T19:32-33Z in tuesday-agent@ (relayed) | read 2026-09-27
- Kam's words | Tuesday's terminal after /login | read 2026-09-25 ~22:0x and 2026-09-27 ~08:2x
Self-check note: no lane-2 file is in lane 1, lane 4 or a frozen branch per S86M's measured claimed-files list; the erasure-test items are sequenced after batch 3.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-27 08:52
