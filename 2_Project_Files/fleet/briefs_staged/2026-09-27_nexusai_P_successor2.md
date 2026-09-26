# BLUF — SUCCESSOR SEAT Datasec/NexusAI-P (lane 4: settings UI + brand). S85P wrapped at 22:53Z for rotation. Read /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/HANDOVER-S85P.md WHOLE first. Your queue: (1) finish RD-430 under the re-pin GRANT below; (2) RD-694 item 4; (3) after rd-430 merges, RD-705's settings.html half. You are ALSO the merge author for lane 4's six READYs once their gate (batch 6) returns. Nothing merges without a gate verdict plus Tuesday's RELEASE.

**Addressed to the cockpit seat `Datasec/NexusAI-P` only.** `Datasec/NexusAI-M` (S86M, lane 1) and `Datasec/NexusAI-N` (lane 2, test harness) are live and share this inbox. Establish your seat from your own pane, launcher and process tree. Derive your seat number from 5_Project_History.

## AUTHORITY
Kam, Tuesday's terminal, 2026-09-25 ~22:0x AEST: *"Please work your way through the tickets and merge once tested."* Re-affirmed 2026-09-27 ~08:2x: *"New account logged in. Please keep going with the work."*

## RULINGS (Tuesday, 2026-09-27; record them in CLARIFICATIONS, one C-number)
1. **RD-286 READY @ 1645c69: the one deviation is ACCEPTED.** The base `th` comment became the LOAD-BEARING marker, with the declaration unchanged. Tuesday's own condition 3 requires it. RD-286 joins the batch-6 gate. Do not move that head.
2. **RD-430 re-pin GRANT:** S85P's branch 9ba6f1d is red on exactly 3 pins, settings.html's node count (172 -> 157), in __tests__/dom-harness.test.js and __tests__/jsdom-instrument-limits.test.js. You may re-pin those three to the MEASURED value, for RD-430 only (C-57 widening: a measured quantity is regenerated, never guessed).
   - Conditions:
     - a red-proof that the re-pinned cell still catches a change (plant a node, see it red, restore);
     - the READY names each pin, old -> new, and why (the removed form);
     - both files are on the C-68 re-run list at merge.
   - Neither file is in any other lane's claimed list (S86M's lane plan v2, claimed-files).
3. **RD-694 item 4 (the fixture `_about` text):** read S85P's open question in its handover. If it is still undecided, mail Tuesday that one question with your recommendation, and carry on meanwhile.
4. **RD-705's settings.html half** (the dead no-store meta at settings.html:6, C-171) is yours AFTER rd-430 merges. S86M builds the server.js half (the no-store header).

## STANDING LINE, NEW TODAY
**Never kill by pattern.** No `pkill -f`, and no `kill $(pgrep ...)` on a generic pattern such as 'sleep 60'. `pkill -f` matches every process on the machine whose command line contains the text. On 2026-09-26 at 20:28 AEST a cleanup `pkill -f 'sleep 60'` killed Tuesday's wake runner (its command line contains 'sleep 600'), and that cost the fleet a night. Kill by pid, taken from your own process ancestry, or by port + cwd (C-110's rule).

## BOUNDARIES
No demo redeploy, production, Partner Center, money, or mail to any human. C-68 (never rebase a gated commit). Every jest run goes through session-tools/nexusai-lock.sh (with --after for merge tickets). SESSION_SECRET is unset for verify. Never touch a worktree whose hold is queued or running (S85P's own rule). Datasec seats are retired BY HAND: mail the wrap to tuesday-agent@.

## PLAN CONFIRMATION
Mail `[Datasec/NexusAI-P -> Tuesday] QUESTION: plan confirmation` and start RD-430 without waiting.

RULED BY KAM, NOT YET IN AN ARTEFACT
- (none open for NexusAI. Checked by Tuesday 2026-09-27 08:35; C-157, C-159, C-170 delivered. Two NEW cards are open on Kam's board and unruled: the setup-window admin-gate scope and the Redis re-raise. Neither is lane 4's.)

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- Tuesday 2026-09-27 08:33: RD-286 redundant pairs = (a) (C-172, recorded by S85P).
- Tuesday 2026-09-27: the RD-430 grant and the RD-286 deviation acceptance above.
- Tuesday 2026-09-26: C-141 addendum 4 (--after); yields self-applied and not mailed.

PROVENANCE:
- S85P's queue, asks and C-68 duties | S85P wrap mail 2026-09-26T22:53Z + READY 22:53Z in tuesday-agent@, read whole by Tuesday; your own HANDOVER-S85P.md | read 2026-09-27
- rd-286 head 1645c69 at origin | git ls-remote origin in /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files | read 2026-09-27 08:5x
- the pkill cause | your own session-tools/s85p/yield-log.md "Instrument defects" + Tuesday's pgrep -f 'sleep 60' listing the runner pid | read 2026-09-27 08:5x
Self-check note: the RD-430 grant is limited to three measured pins in two files; the RD-705 half waits for rd-430 to merge.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-27 08:55
