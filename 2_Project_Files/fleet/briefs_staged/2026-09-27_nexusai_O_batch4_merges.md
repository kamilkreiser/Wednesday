# BLUF — SEAT Datasec/NexusAI-O (lane 3, the image-content gate): you are the MERGE AUTHOR for batch 4. All five lane-3 READYs passed their QA gate (verdict 03:18Z). Merge them to NexusAI main ONE AT A TIME, in the order below, then file the gate's findings as tickets, then build the A-F1 + A-F2 fix. Your predecessor S84O wrapped at 05:32; read `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/HANDOVER-S84O.md` WHOLE first, then the gate report `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch4/report.md` (at least §0, §9, §10, §16).

**Addressed to the cockpit seat `Datasec/NexusAI-O` only.** `Datasec/NexusAI-M` (lane 1), `Datasec/NexusAI-N` (lane 2) and `Datasec/NexusAI-P` (lane 4) are live and share this inbox; a mail addressed to another seat is not yours. Establish your seat from your own pane, launcher and process tree; derive your seat number from 5_Project_History.

## AUTHORITY
Kam, Tuesday's terminal, 2026-09-25 ~22:0x AEST: *"Please work your way through the tickets and merge once tested."* Re-affirmed 2026-09-27 ~08:2x: *"New account logged in. Please keep going with the work."* This brief IS Tuesday's RELEASE for the five merges below (gate verdict at each head + this RELEASE = the C-32 conditions).

## THE RELEASE — five merges, in this order, one at a time
Main at the verdict and at this brief = `1904765` (read by Tuesday with ls-remote at 13:24 AEST). Heads at origin, read the same minute, equal the gated heads:
1. **RD-698** `rd-698-mixed-encoding-s84o` @ `44bc804` — GO WITH FINDINGS (tier 1).
2. **RD-699** `rd-699-decode-branch-cells-s84o` @ `02fe76a` — GO (tier 2). Stacked on RD-698, so it merges second.
3. **RD-418** `rd-418-dockerignore-r3-s84o` @ `5a782c1` — GO WITH FINDINGS (tier 1).
4. **RD-425** `rd-425-guard-all-shipped-s84o` @ `8823458` — GO WITH FINDINGS (tier 1).
5. **RD-443** `rd-443-guard-residue-s84o` @ `8e27dc2` — GO WITH FINDINGS (tier 2).
This is the gate's own clone-1 order (report §9 item 1). The gate proved a second order (O3: RD-443, RD-425, RD-418, RD-698, RD-699) gives the identical tree `a68f5f0`, so the order is safe either way; keep this one.

**Per merge (the batch-1 pattern, C-68 / C-57 / C-89):** re-read `git ls-remote origin refs/heads/main`; merge the then-main FORWARD into the branch in a worktree (never rebase a gated commit, C-68); re-run the C-68 set the gate names for that ticket; regenerate counts ONCE on the merged tree (never hand-edited); run the C-57 id-superset; full verify through `session-tools/nexusai-lock.sh` with SESSION_SECRET unset; predict the counts in your MERGED mail; push; confirm `deploy-demo.yml` was SKIPPED for the push (a merge must not deploy); wait for the CI Build to go green before the next merge. Gate arithmetic after all five: **4180/4180, 250 suites** (report §9 item 5).

**Rename and id rulings, carried VERBATIM (C-57 accounting):**
- **RD-418's two retitled image-content-exposure cells are AUTHORISED RENAMES under C-133's ADDENDUM (:1434).** "The re-anchors were REQUIRED by Tuesday's RD-418 conditions 2 and 6 (C-163). They are ACCOUNTED, not a C-57 STOP, PROVIDED each old->new pair is named and the new id is present and GREEN in the merged set." The pairs are named in the gate report §9 item 6.
- **RD-443: before it merges, merge main FORWARD into rd-443 (C-68, no rebase), and the id-superset on that forward-merged tree must show the RD-428 rd409-410 pair gone (0 missing for it).** Name it on RD-443's merged-tree line as "accounted: C-133 ADDENDUM case 1, stale parent". Source: Tuesday's ANSWER to the gate, 03:12Z.
- **Every OTHER missing id, anywhere, is a STOP:** do not push; mail Tuesday with the id.

**Also fix before RD-443 merges:** E-F1 (Polish) — RD-443's PRIOR WORK says the W3/W4 rule is RD-385 round 3's (`504e4e5`); the gate measured it dates from `67c2992` (RD-327). Correct it in the merge commit message or on the ticket; no code change.

**MERGED mail per merge**, to tuesday-agent@: ticket, new main sha (ls-remote), both parents (cat-file), counts (predicted vs regenerated), C-57 result with each accounted pair named, deploy-demo SKIPPED (the run id), CI Build run id and result. Then the next merge.

## AFTER THE FIVE — tickets for the gate's findings (report §10, severity is the gate's)
File in Jira, BLUF-first, one ticket per fix that one test pass proves (Kam's 2026-09-07 rule), each citing the report path and its row:
- **A-F1 + A-F2 (both Major, pre-existing at B0, NOT regressions):** upper-case env / rc / SSH-key names (`.ENV`, `PROD.ENV`, `.NPMRC`, `.ENVRC`, `ID_RSA`) ship; and the base stage's `COPY package*.json ./` ships any root `package-<x>.json`. The gate's fix shapes and regression cells are in §10. One ticket if one pass proves both (they share rd418's cells), else two; say which you chose and why.
- A-F3 (Minor, suffixed key copies `x.pem.bak`, `x.key.old`), B-F1 (Minor, a stale REVIEWED entry is silent), C-F1 (Minor, cells not through the DEFAULT reader + M-C3/M-C4/M-C6), C-N1 (Polish). Search the board first by symbol/path (not your own phrasing) and add evidence to an existing ticket rather than filing a duplicate.

## THEN — your build queue
1. **A-F1 + A-F2 fix** (lane-3 files: `.dockerignore`, `Dockerfile`, rd418's cells). Red-first with a control that can fail, measured in a REAL image as the gate did (your predecessor's `session-tools/s84o/rd418-build.sh` / `rd418-pair.sh` are the instrument). This is a Dockerfile change, so it is tier 1; READY FOR QA to Tuesday.
2. **RD-703** (ruled (a) on 2026-09-26 19:32Z; HANDOVER-S84O.md §0 has the whole instruction): stacked on RD-699's merged state, red-first, re-arming the parked cell.
3. Then the lane-3 residue in S84O's table (RD-689 waits on the lane-1 files; RD-675/690/700 as their files allow).

## YOUR PARTITION — YOURS ONLY
FILES: `.dockerignore`; `Dockerfile`; `__tests__/helpers/image-manifest.js`; the image-content-exposure suite; `rd385-*`; the rd418/rd425/rd443/rd447/rd698/rd699/rd703 suites; `scripts/verify-expected-counts.json` ONLY as the once-per-merge regeneration.
**NOT YOURS:** `backend/server.js` and lane-1 services (M); lane-2 storage/erasure/LAW files (N); lane-4 settings/UI/brand files (P). If a fix needs a file outside your list: STOP that ticket, mail Tuesday with the file and why, take the next.

## STANDING LINES
- **Never kill by pattern** (C-174): no `pkill -f`, no `kill $(pgrep <generic>)`. Kill by pid from your own ancestry, or by port + cwd.
- Every jest run through `session-tools/nexusai-lock.sh` (with `--after` for merge tickets, C-141 ADDENDUM 4); queue, never take over; yields logged, not mailed.
- Worktrees only; NO write verbs in the `2_Project_Files` clone (C-28) — your predecessor disclosed two fetches there; do not repeat them.
- PRIOR-WORK CHECK before rebuilding, replacing or removing anything; every READY carries a PRIOR WORK section.
- READY FOR QA to tuesday-agent@: branch + head sha, ticket, sets not counts, PRIOR WORK, NOT TESTED, tier.
- No demo redeploy, no production, no Partner Center, no money, no mail to any human. Client-facing text goes on the ticket only.
- A tap with no mail behind it is measured, not acted on (C-148).
- Datasec seats are retired BY HAND: at your wrap, mail the wrap to tuesday-agent@ and write your HANDOVER.

## PLAN CONFIRMATION
Mail `[Datasec/NexusAI-O -> Tuesday] QUESTION: plan confirmation` and start merge 1 without waiting.

RULED BY KAM, NOT YET IN AN ARTEFACT
- (none open for NexusAI: `decision_queue.sh list ruled --undelivered nexusai` = 0 at 13:24 AEST. Kam's two 09:06 rulings are C-178 and C-179, recorded by S86M.)

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- Tuesday 2026-09-27 03:12Z (ANSWER to the batch-4 gate): the RD-428 id via RD-443's stale parent is ACCOUNTED under C-133 ADDENDUM case 1, on the forward-merge condition above.
- Tuesday 2026-09-27 (batch-4 stamp): RD-418's two retitles are authorised renames (C-133 ADDENDUM).
- Tuesday 2026-09-26 19:32Z (ANSWER to S84O): RD-703 = option (a).
- Tuesday 2026-09-26: C-141 addendum 4 (`--after`); yields self-applied and not mailed. 2026-09-27: never kill by pattern (C-174).

PROVENANCE:
- five heads + main 1904765 | git ls-remote origin in /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files | read 2026-09-27 13:24
- verdicts, order, arithmetic, findings, fix shapes | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch4/report.md §0 §9 §10 §16 | read 2026-09-27 13:24
- rename ruling text | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_nexusai-gate-batch4-rd418-rd425-rd698-rd699-rd443.md:34 | read 2026-09-27 13:24
- RD-443 condition | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-09-27_qa_batch4_answer_c57_third_id.md | read 2026-09-27 13:24
- predecessor state, RD-703 ruling, merge notes | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/HANDOVER-S84O.md | read 2026-09-27 13:24
- undelivered Kam rulings | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered nexusai | read 2026-09-27 13:24
Self-check note: order = gate clone-1; the RD-443 forward-merge condition is stated once and named; every other missing id is a STOP; partition names every seat.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-27 13:24
