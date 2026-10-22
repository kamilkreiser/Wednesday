## NEW SEAT: you are Seat G 17th (lane Secuura/Blockchain-G, SONNET): post Kam's two ruled notes (Peter now, Stuart on Wednesday's mail), and raise ONE small PR re-dating two audit rows; end the PR at READY FOR GATE

**Routing receipt:** `model: claude-sonnet-5-5 -- C1 (ticket comments + a one-file data change) -- P1-P4: posting needs the board identity -- gauge 97% (Kam's taps 10:05 today; lean)`. The project launcher pins claude-opus-5; Wednesday switches this pane to Sonnet at your plan prompt.

## BLUF
1. **Post to Peter NOW (after your plan confirmation):** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-23_seatD-30th/evidence/draft_KS485_combined.txt` VERBATIM as ONE comment on KS-485. Pre-send hash gate: 3,563 B, sha256/16 `b191d7ff8151de24` (refuse on any difference). Absent-id control first; then assert `suggestion_userMentions` names Peter; report the comment id and read the body back by id.
2. **Post to Stuart ONLY on Wednesday's mail "POST STUART"**: `.../2026-10-23_seatD-30th/evidence/draft_KS772_combined.txt` (2,339 B, `290a3dd57f4a27a9`) as ONE comment on KS-772, same gates, mention `stuart.jamieson=8f5b499d-2d28-4887-ad06-f5b9051ed5ae`. Wednesday is confirming one detail with Kam first. Post NOTHING else to Stuart, and never K1, K1b, K1c or any single draft.
3. **PR (tier 2):** in `Blockchain/Dev/scripts/audit/audit-baseline.json`, set `expires` to `2026-11-30` for exactly `GHSA-ggr8-5vv4-36mx` (deepmerge-ts, KS-664) and `GHSA-rj75-hqrm-r3gf` (postcss-selector-parser, KS-1425), with a dated note naming Kam's tap. Nothing else changes. One PR from develop, `Refs KS-1707`. End at READY FOR GATE.

## QUEUE
### 0. Boot
Read the launch preflight file first and quote it in your plan confirmation. Establish your seat from your pane (if `@cockpit_name` reads empty, this mail is your identity). A fresh work clone from GitHub under `deploy-clones/seatG17-<sha12>`, never `2_Project_Files` (the project's read-only rule for a second live session). Pin develop at your boot (Wednesday's read: `2bd32cbd6ed6`). Send the plan confirmation before your first write or post.
### 1. The Peter post (item 1 above)
### 2. The PR (item 3 above)
Proof: `audit:gate` and `audit:locks` rc 0 at the head; a lapsed-copy control (one of the two rows set to 2026-10-01 in a scratch copy) makes both legs exit non-zero naming it; restore by sha256; `audit:contract` 59/59. Push per the repo's `.githooks/pre-push`: cite the lines that allow a new branch; no `--no-verify`, no force.
### 3. The Stuart post (item 2), when Wednesday mails it

## HOLDS
- Signature classes pause for Kam. Client-facing comms = these two ticket comments only, as ruled; nothing on the extranet; nothing else to any human.
- No box, no `az`, no deploy, no Docker. Never delete (quarantine). An exit code on its own line. A waiter is a background job whose exit wakes you, written with a quoted heredoc.
- Rotate inside your 80-90 band at a clean boundary, handover first.

## PARTITION
**Yours:** `audit-baseline.json` in your own clone; the two comments; `5_Project_History/2026-10-23_seatG-17th/`. **Not yours:** no other Secuura seat is live (Wednesday's pane read at launch). KS-1709's "mark it unanchored" build (Kam's tap b today) is a LATER seat's, not yours.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Gate check: `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered secuura-`.
- `secuura-ks485-answer-peter-vouch-secret-1023` = a (2026-10-23 10:05:11, "Post the draft to Peter on KS-485 as written") -> delivered by item 1.
- `secuura-ks1707-fifth-row-postcss-no-fix-1023` = a (2026-10-23 10:05:24, "Re-date it to 30 Nov with the other four"); the card's amended option detail names BOTH rows (postcss and deepmerge-ts): Wednesday's reading, stated to Kam with a correction offer -> delivered by item 3's merged PR.
- `secuura-kintsugi-deploy-notice-1022` = b (2026-10-23 10:05:38, "Post both notices as drafted") -> item 2, on Wednesday's mail only (the corrected combined note; Wednesday confirms with Kam).
- `secuura-ks1709-keep-unanchored-certification-1023` = b (10:05:06, "Keep it, but mark it unanchored") -> NOT this seat.

PROVENANCE:
- Develop tip `2bd32cbd6ed60cb1ebf7929b9460910aea19a3b4` (#1682) | `git -C /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src ls-remote origin refs/heads/develop` | read 2026-10-23
- At that tip the two rows expire 2026-10-31; braces and both react-router rows already 2026-11-30 | `git show origin/develop:Blockchain/Dev/scripts/audit/audit-baseline.json` parsed by Wednesday | read 2026-10-23
- Combined drafts' sizes and hashes; every line traced to its two source drafts except one declared joining heading each | Wednesday's independent line-level check 2026-10-23 09:2x | read 2026-10-23
- Kam's four taps, verbatim | `2_Project_Files/tools/kam_msgs.sh 5` (live board, view=wednesday) | read 2026-10-23
- KS-485 state UNMEASURED today: Peter's deploy ticket; his question 8b8bcfc3 (2026-10-22T13:38:22Z) | the seat reads it newest first with a control | read 2026-10-23
- KS-772 state UNMEASURED today: Stuart's deploy-notice ticket | the seat reads it | read 2026-10-23
- KS-1707 state UNMEASURED today: Backlog/open after #1682 | the seat reads it | read 2026-10-23
- KS-664 state (In Progress, last comment 2026-09-13T21:59:52Z) | Wednesday's GraphQL read 06:1x | read 2026-10-23
- KS-1425 state (In Progress, last comment 2026-10-06T05:05:51Z) | same read | read 2026-10-23

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-23 10:07
