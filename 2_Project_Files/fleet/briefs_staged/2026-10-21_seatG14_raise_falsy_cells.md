## NEW SEAT: you are Seat G 14th (lane Secuura/Blockchain-G, a RAISE seat): raise two held Spark test-only passes as two PRs (KS-1508 and KS-1660), tier 2, stop at READY FOR GATE

**Routing receipt:** `model: claude-sonnet-5-5 -- C1 (raise a held local PASS as a PR; test-only, product untouched) -- P1-P4 no (Wednesday's classification) -- gauge 86% (80-90 band; Kam's 2026-10-21 15:12 word "merge and work through as many tickets as you can with the spark" lifts the 18:55 no-new-seat order for the steps merging needs)`. If either patch needs a product line, STOP and say so; that is no longer a C1 job.

**Why you exist:** the Spark produced two byte-identical PASSes (falsy-value log cells for KS-1508 and KS-1660). Wednesday read both goldens at source and held them. No Secuura seat is live. Gauge budget is thin (hard stop 90%): work lean, no exploratory builds, no extra gates, and say so in your plan confirmation if anything looks like it will cost more than the brief says.

---
## BLUF
1. Raise **two PRs, two branches, file-disjoint, from live develop**: PR A = KS-1508 (originate, one existing test file edited in place, +11/-0), PR B = KS-1660 (originate, one existing test file edited in place, +8/-0). Each patch is the Spark's `patch.diff` byte-for-byte; **zero product bytes in either PR**.
2. **Tier 2 (test-only; one Sonnet gate may cover both).** `Refs`, never `Closes`: both tickets stay open (nothing is deployed for them).
3. Stop at **READY FOR GATE, one mail per PR**. No merge without Wednesday's GO naming the head sha.
4. Each PR body states plainly what the cell pins and what it does NOT: it pins the log gate against a truthiness rewrite for four falsy planted values; it does not change behaviour.

## QUEUE (in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/`)
Model for process and traps: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-20_seatD26_raise_spark_screen21.md` (read its BLUF, WORK CLONE and STANDING LINES sections; this brief is the short form).

### 0. Boot
Read the launch preflight file in your FIRST tool call and quote it into your plan confirmation. Establish your seat from your own pane. Cut a fresh clone per the model brief's WORK CLONE. Send the plan confirmation before your first write.

### 1. PR A: KS-1508 falsy cell
- **Held file:** `READY_KS-1508-FALSY1508-1_spark-dsv4flash_BRIEFED-TESTONLY-CERTIFICATIONS-PASS-7of7_2026-10-20.diff.md`. Canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1508_falsy_p1/out.md.checker/patch.diff`.
- **File:** `Blockchain/Dev/services/originate/src/__tests__/ks1508-versionedbyid-is-server-set.test.ts`, one hunk (+11, a pure insertion: a two-line comment and one `it.each` over `''`, `null`, `0`, `false`).
- **Checker's numbers (the Spark's instrument; re-measure, do not copy):** red-first 4 failed of 50 run; green-after 50/50; suite 1625 -> 1629, failed 0.
- **Mutant to re-run:** the tamper, `Blockchain/Dev/services/originate/src/routes/certifications.ts:701`, `if (droppedVersionedById !== undefined) {` -> `if (droppedVersionedById) {` (reds the four cells); compile-clean first, restore asserted by sha256.

### 2. PR B: KS-1660 falsy cell
- **Held file:** `READY_KS-1660-FALSY1660-1_spark-dsv4flash_BRIEFED-TESTONLY-CERTIFICATIONS-PASS-7of7_2026-10-20.diff.md`. Canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1660_falsy_p1/out.md.checker/patch.diff`.
- **File:** `Blockchain/Dev/services/originate/src/__tests__/ks1660-a-caller-s-data-parentdocumentid-overwrites.test.ts`, one hunk (+8, a pure insertion: a two-line comment and one `it.each` over the same four values).
- **Checker's numbers (re-measure):** red-first 4 failed of 14; green-after 14/14; suite 1625 -> 1629, failed 0.
- **Mutant to re-run:** `certifications.ts:704`, `if (droppedParentDocumentId !== undefined) {` -> `if (droppedParentDocumentId) {`.

## HOLDS
- Signature classes pause for Kam: production, money, external communication, anything irreversible. No box, no `az`, no deploy, no Docker on the Studio.
- Client-facing comms = ticket comments only (BLUF-first). One BLUF comment per ticket after the PR is up (`Refs`).
- Never delete (quarantine). No `--no-verify`, no force pushes, no `--admin`. Before pushing, read `.githooks/pre-push` refusal branches and cite the line that allows the route.
- Rotate inside your own 80-90 band at a clean boundary; handover first.

## PARTITION
**Yours:** the two test files above, in your own work clone, and `5_Project_History/2026-10-21_seatG-14th/`. **Not yours:** no other Secuura seat is live (Wednesday's read of the pane list at launch, not a measurement of yours: verify with `tmux list-panes -t fleet:0`). KS-1692 PR 2 and KS-1695 gap 2 are other seats' work and wait for the allowance. You share one inbox; a mail naming another seat is not yours.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 2026-10-21 15:12 (live board, view=wednesday, verbatim): "thanks.  merge and work through as many tickets as you can with the spark" | the gate's check for this section is `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered secuura-` (it lists older cards; none is this round's subject). It lives on the live board and in Wednesday's note of 2026-10-21, not in an agent artefact.
- `secuura-ks1695-gap2-sized-confirm-b-1020` = a (2026-10-20 18:56): gap 2 is not this round's subject; do not act on it.

PROVENANCE:
- Held Spark passes KS-1508 and KS-1660 PASS 7/7, golden BYTE-IDENTICAL, held with hold_ready (FALSY1508-1, FALSY1660-1), product unchanged, suite 1625 -> 1629 each | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/done.md rows 2026-10-20 15:32 and 15:34 and the two READY files in night/ | read 2026-10-21
- Wednesday read the KS-1508 golden diff whole and the KS-1660 golden diff whole (11 and 8 `+` lines, one `it.each` each) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1508_falsy_p1/golden.diff and ks_1660_falsy_p1/golden.diff | read 2026-10-21
- Tamper lines `certifications.ts:701` and `:704` at origin/develop 32964477fe88 | the drafter's dry-run record in done.md (briefs' spark.pins line=701 and line=704) | read 2026-10-21
- Develop tip 32964477fe8828eb78240150e8ab59bd8179f339 (unchanged since #1654) | `git -C /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src ls-remote origin refs/heads/develop` | read 2026-10-21
- KS-1508 and KS-1660 are In Progress on the KS board, with merged fix PRs (#1497/#1516 and #1641) | the board_sweep KS sample of 2026-10-21 (Wednesday's own run) | read 2026-10-21
- UNMEASURED: whether any open PR touches the two test files | the drafter-free census was not run; the seat's overlap check closes it | read 2026-10-21

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-21 15:13
