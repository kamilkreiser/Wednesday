STARTABLE: YES

# B1230 drafter report (Security Composer records seat R160, PR #115 / the DEPLOY.md line 255 sentence)

Drafted by an Agent-tool drafter. Clocks are the `date` lines printed in each action (19:22 to 19:29 AEDT 2026-11-03); the kit types none of its own beyond the measured merge time (converted by program).

## BLUF
- Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1230_SEAT-R160_composer-records-115.md`, 77 lines (`wc -l`), 6 stamp-slot lines (5 slots + last line; control `grep -c -E '_''_''_''_'` = 6). Sonnet, C8, `BRIEF_SEAT_LEVEL=sonnet` in the launch line, no ports. Slots file `2026-11-03_B1230_slots.json` (`@NOW@`, `@WINDOW_END@`, `@HARD_END@` for you to fill).
- Writes: at most 2 Jira writes (NEW-A create, default NONE; one facts-only comment on PCOMP-127, default FILE), BACKLOG rows #463 (landing) and #464 (follow-ups), State append on #462 (and #461 only if it meets the stated property), entry C-124, history entry, one JIRA.md bullet.
- Ticket vs row, decided: the three Minors of the round-2 review are a ROW (#464), not a ticket, by the project's convention. Tickets here are created "on the product owner's ruling to ... ticket" (`BACKLOG.md:446-449`, `:454-457`); gate Minors/Notes with no such ruling are "row only, NOT RULED ... no ticket" (`BACKLOG.md:451` #455, `:452` #456, `:458` #462; C-122 (5) `CLARIFICATIONS.md:2302`). None of the three rulings on this sentence says ticket. The ticket text (T1) is ready if you stamp FILE.
- Which ticket owns the sentence: none asks for it. PCOMP-127 is the only one naming it ("a separate change in the code repo"); PCOMP-113 only locates line 255. So the comment goes on PCOMP-127 (Q-2).
- Mechanics are the B1209 kit's; the facts moved since it: root main is `1ec760d0`, highest BACKLOG #462, highest C-123, Jira 127.

## Facts re-measured (instrument, control)
- PR #115: `gh api -X GET .../pulls/115` under the project `GH_CONFIG_DIR`: merged true, `merged_at` 2026-11-03T07:32:00Z = 18:32:00 AEDT (`TZ=Australia/Sydney date -r 1793691120` printed `Tue 3 Nov 2026 18:32:00 AEDT`), squash `d424af7f503f1abe8ae24fe3acbc54aa963e6c25`, base `2f63b2f6`, head `78b0d75f`, 3 commits, 1 file +1 -1. Control `pulls/9999` 404. `commits/d424af7f`: one parent `2f63b2f6`, tree `dd2c4f4654c21557361acb6da9dfc19eb8bc6a05` (= the tree `B1222_STATUS.md:23` records for the head), verified true, DEPLOY.md blob `89c35502` (equal to the card's delivered text). `git/ref/heads/main` = `d424af7f`.
- DEPLOY.md at `2f63b2f6` vs `d424af7f` (contents API, both 652 lines): `diff` prints `255c255` only; `awk NR==255` at the squash is the approved sentence with all three additions; `:203`, `:259`, `:263`, `:265` as PCOMP-127 quotes them. b778 file blob `2348719a` at the squash, 1,786 lines; `grep -n` printed `:445`, `:666`, `:1385`, `:1398`, `:1405`, `:1661`.
- Squash message vs `2026-11-03_B1222_evidence/squash-body.txt`: `diff` rc 0 (BODY_EQUAL); subject = `squash-subject.txt` + " (#115)"; `Co-Authored-By` 1, `localdomain` 0 (control: the three builder commits carry `localdomain` per `B1222_STATUS.md:155`).
- Check-runs head: CodeQL, Analyze (csharp), Analyze (javascript-typescript) success 07:29:40Z to 07:30:44Z (before merge); squash: both Analyze success 07:33:41Z, 07:36:21Z. Alerts open: main 0, `refs/pull/115/head` 0, control `state=fixed` 20. Open PRs [91, 86, 85].
- Reviews: `B1217_STATUS.md:1`/`:134` NO GO round 1 of 2, Majors `:112`, `:113`; `B1222_STATUS.md:1`/`:174` GO WITH FINDINGS round 2 of 2; Minors `:147`-`:149`, Notes `:150`-`:155`; checklist `:158`, `:163`, `:164`. Builders READY at `B1214_STATUS.md:101`, `B1220_STATUS.md:67`, `B1224_STATUS.md:73`.
- Root records: main `1ec760d0`, porcelain over the four paths 0 (control: whole repo 1,389), staged 0, no MERGE_HEAD/index.lock (the `ls` printed both errors), no remote; BACKLOG 458 lines (#462 at `:458`, `| 463 |` count 0), CLARIFICATIONS 2337 lines (C-123 `:2316`), JIRA.md 45 lines, `PR #115` in the four paths 0,0,0,0 (control `PR #114` in JIRA.md 1). `.tools/b1230`, `wt-b1230-rec`, `records/b1230` absent (control `records/b1209` resolves). 21 scripts in `.tools/b1209/scripts`, `/transitions` 0 in `jira1209.py`.
- Jira (project's own `jira1209` module in-process, GET only, no token printed; `myself` 200): total 127, held 19, seed 94, Done 26, highest PCOMP-127; `plan-comp-463` to `-466` 0, controls `-446`, `-458` 1; `zzqxvbw` 0, `composer` 62; PCOMP-127 Task Backlog [plan-comp-461] 0 comments; PCOMP-116 1 comment. Duplicate searches in the kit.
- Seat name: `R160` 0 files (control `R155`: 3 files); `ls | grep -c B1230` 0 before my files. Live panes: %0 tuesday, %1 fleet-monitor, HPSM-POC-G325, HPSM-POC-G324, NexusAI-G323; no Composer pane; `ps` printed only its own line.
- Model row: `model-routing.md:97` C7, `:98` C8; `models_latest.json:23` claude-sonnet-5-5; `brief_seat.sh:24` default opus.
- Text scan of the posted (`> `) lines (8 of them): backtick/backslash 0, non-ASCII 0 (python byte count on the whole kit), B-number 0, banned words 0 other than inside "NOT DEPLOYED" (3 lines), "Composer" only as "Composer PR" (5). Control: a planted `> x B1230 gate` line fires the pattern (1).

## D-decisions (mine)
- D-1: ticket slot NEW-A defaults to NONE, row #464 holds the three Minors and Notes -4 to -8 plus B1217-6. Reason above.
- D-2: comment on PCOMP-127 (not -113). PCOMP-127 quotes the sentence as a pending separate change; the comment closes that pointer without moving anything. PCOMP-116's own comment (B1209) is not re-commented.
- D-3: no Done-when table and no MOVE slot: PCOMP-127 is an open three-item ticket, only commented.
- D-4: Jira text says "the squash text states each precisely; the file does not", because the squash message equals the review's corrected body but line 255 still carries the three looser words. The records must not imply the file was corrected.
- D-5: the kit cites rulings by date and count (three), no card ids and no clock. Card times (06:40:34, 16:56:22, 17:28:42) are in the report only.
- D-6: State appends: #462 required; #461 only by the stated property; #416 locates line 255 only and is left, to be listed by the seat.

## Q-questions for Tuesday (each with a default)
- Q-1: Ticket the three Minors (stamp NEW-A FILE) or row only? Default NONE (row #464): the project ticketed only on a ruling to ticket, and none was given on this sentence. If FILE: label `plan-comp-464`, MAX_WRITES 2 already set.
- Q-2: Comment key PCOMP-127 (default, the only ticket naming the sentence) or PCOMP-113 (pin paragraph, row #416)? If -113 the comment text and KEYS need re-drafting; I did not.
- Q-3: Baseline root main `1ec760d0` (REFUSE 3 pins it). Default yes.
- Q-4: The fix of the three wordings is a code change under a review whose class is at two of two (`B1222_STATUS.md:164`: a third round on the product owner's word). Default: not commissioned; the kit only records.
- Q-5: Ruling times differ from the commission: the cards read 06:40:34, 16:56:22 and 17:28:42 (commission said 06:39, 16:56, 17:27; one card text itself says "your 06:39"). The kit uses dates only. Default: leave as is.
- Q-6: The squash has no `CodeQL` check-run (only both `Analyze`), as the B1209 report said for #114. Default: treat as the repo's pattern; the head CodeQL success and 0 alerts on both refs are what the kit records.

## UNMEASURED
Hosted site; review cells (RELAYED); whether main or Jira moved after 19:29 AEDT; who merged #115; whether the coordinator re-read CodeQL beyond the check-run times; gawk; the demo VM; the 06:39 vs 06:40:34 discrepancy cause.

## Outside the fences
None. Reads only: DRAFTER_RULES, the B1209 kit/.pre-stamp/slots/report, the B1217/B1220/B1222/B1224 kits and STATUS files, the Composer root records (BACKLOG, CLARIFICATIONS, JIRA.md, history), Jira GETs via the project's `jira1209` module (no token printed; no bytecode written), `gh api -X GET`, git read verbs, tmux/ps/stat, and `decision_queue.sh show <exact id>` for the three named ids into scratch files (no `list`). Scratch copies of DEPLOY.md, the b778 file and a Jira read script are only in the session scratchpad.
