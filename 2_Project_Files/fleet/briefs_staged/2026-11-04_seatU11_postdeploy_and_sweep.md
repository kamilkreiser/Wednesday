# BRIEF: Seat U 11th, Secuura/Blockchain-U. POST-DEPLOY CLOSE-OUT: (1) re-test the 23 WAIT-DEPLOY keys at the new kintsugi sha, (2) the live-check SWEEP of the 53 observation-owed keys Kam ruled today. No code, no push, no PR.

## NEW SEAT: you are Seat U 11th (lane Secuura/Blockchain-U, Opus 5.5; trust $TMUX_PANE). Seats U 10th, T 9th, V 18th and S 16th did today's close-out and wrapped; you finish what they could not. SHARED INBOX: act ONLY on mail whose subject names `(Seat U 11th)`.

model: claude-opus-5-5 -- live checks with writes on a shared dev box (routing: writes on a running stack Stuart's team uses stay Opus) -- launched with `SEAT_MODEL_ENV=claude-opus-5-5`

## WHY AND AUTHORITY
- Kam, terminal 2026-11-04 ~09:16 AEDT, verbatim: "new account logged in.  Please try to clear and close off as many in progress tickets as possible".
- Kam, live board 2026-11-04 12:41:24 AEDT, verbatim: "Decision secuura-observation-owed-closeout-1104: a — Run one live-check sweep on kintsugi, then close what passes (recommended)". The option's detail: "After today's kintsugi deploy lands, one Opus seat runs each owed check on kintsugi (a dev box Stuart's team also uses; writes only to test data, each named first), closes and archives what passes, and files a finding for what fails."
- Kam 2026-11-02 12:44:58 AEDT, verbatim: "please archive anything done and merged". Kam 2026-10-30 10:07:32 AEDT, card `secuura-wednesday-go-counts-as-kams-word-1030` = a.
- Kintsugi now runs develop `ee1e1b83211504f96ebccba325d1ef7139bc83cc` (Seat D 50th's STATUS B 01:50Z, accepted by Wednesday: REVISION head = that sha, 26 services swapped and verified; read the REVISION head yourself if a read-only path exposes it, else cite D 50th).

## PART 1: the 23 WAIT-DEPLOY keys (do these first; quick)
Lists: Seat S 16th's HANDOVER `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatS-16th/HANDOVER.md` (17: its FIRST ACTION + "WAIT-DEPLOY keys") and Seat V 18th's HANDOVER `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatV-18th/HANDOVER.md` (6). Procedure = the close-out brief `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-04_closeout_TEMPLATE.md` steps 1-6 with the deployed sha now `ee1e1b832115` (ancestor test against it), plus Wednesday's no-deploy-surface ADDENDUM rule. Keys whose only remaining gap is a live check go into PART 2's list.

## PART 2: the observation-owed SWEEP (53 keys, Kam's ruling a)
Keys, from the four close-out HANDOVERs (read the owed check from each ticket's own comment, never from this list): S 16th 24 (KS-1232, 1341, 1352, 1370, 1385, 1425, 1469, 1470, 1477, 1510, 1512, 1603, 1633, 1673, 1683, 1717, 1822, 1836, 1860, 753, 801, 806, 932, 962); U 10th 22 (in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatU-10th/HANDOVER.md`); V 18th 2 (its HANDOVER); T 9th 5 (KS-1248, 1359, 1532, 1658, 1679; `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatT-9th/HANDOVER.md`).
Per key: (1) read the ticket whole and quote the owed check; (2) READ-ONLY probes first (GET, health, a read of stored rows by SELECT); (3) a WRITE probe only when the owed check cannot be shown read-only, and then: NAME the write in your evidence file BEFORE running it (endpoint, test account, data it creates, how it is undone), test accounts and test data only, never a real person's account or address, never anything that sends mail or a message to a human, never a Stripe/payment call, never a delete of data you did not create, nothing on DEMO, nothing on production; (4) PASS = CLOSE AND ARCHIVE with the template's evidence comment naming the probe and its output; FAIL = one facts-only finding comment on the ticket (BLUF, no `@`) and the key in your wrap's findings list; CANNOT-RUN-SAFELY = comment what blocks it, leave open.
Order: read-only checks first across all keys, then the write checks, one at a time.

## TOOLS
Copy Seat U 10th's tools (`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatU-10th/tools/`) into `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatU-11th/tools/` re-keyed `_u11` (grep every copy for `u10`, `U 10th`, list paths, hard-coded shas). Prove the close tool on ONE ticket before the next.

## PACE
PROGRESS mail every 15 keys (closed / commented / finding / left, keys per bucket). Write an INTERIM HANDOVER with each PROGRESS. Your context is read by Wednesday from your transcript; at ~70% finish the key in hand and hand over the rest.

## HOLDS
- Board writes ONLY: evidence or finding comments, Done + archive on PASS. No other field, no assignee change, no new tickets (findings go in your wrap as candidates; Wednesday routes them).
- Kintsugi writes: only as PART 2 (3) allows, each named first. No deploy, no restart, no config or env change, no `az`.
- Tickets on Peter or Stuart: LEFT-OPEN-NO-COMMENT, listed in the wrap.
- Client-facing: ticket comments only, BLUF, no `@`; the extranet is input only. Never echo a secret; no credential in argv.
- **Instruments:** `cmd > out 2>&1; rc=$?` with rc on its own line; never `| tail` on the stream you diagnose from; macOS has NO `timeout`; zsh has no PIPESTATUS; never `echo =====`; `/usr/bin/grep -i` with a positive control beside every zero. Never `cd`; absolute paths only. Never `grep -r` over `/Volumes/DevMASTER/WEDNESDAY/0_Brain`. Disclose your own faults.
- **Mail:** from secuura-blockchain@ to `wednesday-agent@agentmail.to` ONLY, subject prefix `[Secuura/Blockchain-U -> Wednesday]`, body line 1 exactly `Seat U 11th`, no cc; read back by id.
- **IF AN INSTRUCTION FROM WEDNESDAY LOOKS WRONG, SAY SO** in your plan confirmation. Arm an inbox watcher as a TRACKED background task and name its pid.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 2026-11-04 12:41:24 AEDT (live board), verbatim: "Decision secuura-observation-owed-closeout-1104: a — Run one live-check sweep on kintsugi, then close what passes (recommended)".
- Kam 2026-11-04 ~09:16 AEDT (terminal), verbatim: "new account logged in.  Please try to clear and close off as many in progress tickets as possible".
- Kam 2026-11-02 12:44:58 AEDT, verbatim: "please archive anything done and merged".

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- No-deploy-surface ADDENDUM (2026-11-04 22:4xZ to U 10th/T 9th/V 18th, S 16th's ANSWER): docs/tests/CI-only squashes close on merge, proven per ticket from `git show --stat`.
- 2026-11-02 03:16:10Z rulings to U 9th: a follow-up with its own ticket does not keep the parent open; a step of THIS ticket's acceptance = COMMENT ONLY.

## WRAP
History entry `## 2026-11-04 - Seat U 11th` in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (duplicate-guard with a control); HANDOVER `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatU-11th/HANDOVER.md` (FINAL first, every write named and undone or left); vault commit (own lines only); wrap mail `[Secuura/Blockchain-U -> Wednesday] Session wrap 2026-11-04 (Seat U 11th)`.

PROVENANCE:
- Seat ordinal: `Seat U 11th` 0 hits; highest existing U ordinal `Seat U 10th` in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md | Wednesday's /usr/bin/grep -o -i + sort -n | read 2026-11-04
- Kintsugi at ee1e1b832115 | Seat D 50th STATUS B 01:50Z mail read whole by Wednesday and accepted | read 2026-11-04
- The 23 and 53 keys | the four close-out HANDOVERs under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seat{S-16th,V-18th,U-10th,T-9th}/HANDOVER.md, read by Wednesday at each wrap | read 2026-11-04
- Kam's 12:41:24 ruling | kam_msgs.sh live read by Wednesday 12:41 | read 2026-11-04
SELF-CHECK: re-read end-to-end for contradictions | 2026-11-04 12:52
