STARTABLE: YES (after the stamp; one timing point below)

# B1371 drafter report (seat Datasec/MPS-R193, Sonnet records)

## BLUF
Kit written, 62 lines (long paragraphs, B1366 form). R193 and b1371 are unused (word-boundary scan of the 9 non-`.pre-` SEAT kits of 7 and 8 Nov: 0 each; control `R191` found 8 in the B1366 kit). Both PRs verified at source: merged, one parent, files and per-path blobs as the commission says. **Two findings change the work: (1) #166's main CI was still in_progress at 23:29, so -386's move may need a wait; (2) #166's squash tree is not its head's tree, so the kit tells the seat to compare blobs per path.** Slots in the file are the safe values; recommendations below.

## Facts re-measured (instrument; clock 23:29 AEDT, `date`)
- Code main = `31234f5f0e17dadcd5d6955055d477e660d204b7` (`gh api -X GET git/ref/heads/main`); open PRs 0, control `pulls/99999` 404; `compare 31234f5f...main` identical 0/0.
- #165: merged, head `b525cd8c...`, squash `dc1b3f0c...`, one parent `bb9bac9b`, merged_at 12:15:02Z (23:15:02 AEDT by my arithmetic, UTC+11), paths ProposalPage.tsx and .test.tsx, tree `b51d111b` = head tree; blobs squash = head 2 of 2 (`f350b33d`, `414c4271`). Runs: 8 of 8 check-runs success, ci and Push on main success attempt 1.
- #166: merged, head `737b2635...`, squash `31234f5f...`, one parent `dc1b3f0c` (the #165 squash), merged_at 12:28:11Z (23:28:11 AEDT), paths noBrowserPricing.ts and .test.ts. Blobs squash = head 2 of 2 (`3e177636`, `25c661fb`; parent's `38f2fdf3`, `9be029b0` differ). The commission's phrase "blobs equal to heads" holds per path; the TREES differ (squash `f4dde937` vs head `fccb246f`) because the head sits on bb9bac9b; `f4dde937` equals the gate's combined-pair tree (`B1370_STATUS.md:15`). **Runs: ci and Push on main in_progress, check-runs total 7, success 2.**
- Jira (own GET via `j1366.issue/comments`): -385 Backlog label mpscalc-b1355, 0 comments; -386 Backlog label mpscalc-b1366, 0 comments; -106 Backlog, comments 39426 and 40814; all have transition 41 named Done; project `search` length 386.
- C-79 at `:1712`, `:1714`, `:1716`, `:1727` (awk NR==n); highest C heading C-98 at :2605 (`/usr/bin/grep -n -i`, printed :2571 :2583 :2594 :2605); next C-99. Root HEAD = main = `ee320c64` (B1366's commit); dirty files history.md, BACKLOG.md, JIRA.md. BACKLOG.md 5196 lines (last row `[B1366-BATCHES]` :5191, Batch 21), JIRA.md 675, history.md 1406, CLARIFICATIONS.md 2615 (wc -l). Note BACKLOG.md and JIRA.md sit at the project root, CLARIFICATIONS.md under `1_Project_Definition/`.
- Gate STATUS: 123 lines, verdict `:1` GO WITH FINDINGS both, combined GO; findings B1370-1..10 at `:90-:99` (1-5 Minor, 6-10 Note), clauses at `:64`, `:73`, `:115`. Landing sentences in `landing.txt` last two lines.
- model-routing.md `:98` C8, `:109` G2, `:110` G3, `:111` cap (awk NR==n); `models_latest.json:23` claude-sonnet-5-5; `brief_seat.sh:24` defaults opus. Ports: `lsof 9500-9529` 0 listeners. Panes: tuesday, fleet-monitor.

## D-decisions
- D-1 Findings B1370-1..10 become ten rows `[B1371-M-1..10]`, no ticket (convention: model-routing.md:111 tickets Majors and the cap residue; this is GO round 1 with Major 0). B1370-2 (four shapes outside the 18) is flagged in its row as a ticket CANDIDATE for the coordinator.
- D-2 Fixed-text word list, exemptions and the "no finding id in a comment" rule carried over from B1366; comments name no B-number, so the ten finding ids appear only in BACKLOG and JIRA.md accounting.
- D-3 The Done-when for -385 is read from the TICKET text (C-79 says "the ticket's"); the gate itself says the builder kit's wider property is the thing B1370-1 breaches, the ticket's scope being flushSync. The kit tells the seat to quote the words it used.
- D-4 -106 is the same case as -375 in R180 (a gate GO that the coordinator read as NO GO 2 of 2 with the residue ticketed): the kit makes it depend on slot CAP-READING, as R180 did. Without it the seat posts the comment only.
- D-5 ROW-RESIDUAL slot added: -385 and -386 carry Minors held as rows (reading (k)); R180 used the same slot.
- D-6 The fence allows 3 plan keys, 6 writes, no create; the transition only after that key's comment reads back.
- D-7 Slots in the JSON are safe defaults (HOLD / NONE / NO / NO / HOLD), as the commission asked.

## Q-questions for Tuesday (each with a default)
- Q-1 Move keys. Recommend `MPSCALC-106, MPSCALC-385, MPSCALC-386` with COMMENTS FILE, CAP-READING YES, ROW-RESIDUAL YES, REC-CLAR-99 FILE (the commission names all three moves and the C-entry). Default if you decline: COMMENTS FILE, MOVE-KEYS NONE. Each move is conditional in the kit on its own table, so naming a key cannot force a wrong move.
- Q-2 CAP-READING YES is your reading (the coordinator's), not the product owner's; C-98 records that the residue is ticketed as MPSCALC-386, which is the shape reading (i) names. Default YES if Q-1 is taken; if NO, -106 is comment-only.
- Q-3 Is a +6/-1 diff against the ticket's "one line pair" (gate Note B1370-8) a failed clause on -385? Default: the kit leaves it to the seat, which must quote the ticket's words; my own reading is that "Product byte: one line pair" is a size estimate, not an acceptance clause, so MET with a Note. Say so in the stamp if you want it fixed either way.
- Q-4 Timing: -386's runs were unfinished. Default: the seat polls up to 20 minutes and holds the move if red/unfinished. If the runs are already green when you stamp, nothing changes.
- Q-5 CARD-REF is NONE in the slots (no card was named in the commission).

## UNMEASURED
No Done-when verdict was drafted (the tables are the seat's). Hosted runs of `31234f5f` after 23:29. Code-scanning alert lists (count only). Whether either PR is in a hosted build (never probed). The 40814 comment text beyond what I printed. The `launch_when_cool.sh` line itself was not run. Tuesday's own reads: the STAMP slot carries only my reads; add yours.
Not read: C-97's scan paragraph (the seat copies it), R180's STATUS and B1366's tool sources beyond `j1366.py` lines 1-40 and 193-240 and the function list.

## Outside-the-fences disclosure
I wrote one scratch Python reader at `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/1f2a0f1e-7ce2-452e-bd48-e061d7356fdf/scratchpad/rd.py` that imports the project's `j1366` (GET only; ran `issue`, `comments`, `call GET transitions`, `search`; nothing printed from `.env`). It was not in my two files but is scratch. One Bash call carried a stray `cd` and was refused by the hook (no effect). I did not run `decision_queue.sh` and read no card. I wrote nothing in any project folder, Jira or GitHub. `__pycache__` was suppressed by the module's `sys.dont_write_bytecode`.
