STARTABLE: YES (with one condition for Tuesday: the Build workflow's `build` of main `04a6b89d` was still `in_progress` at 14:11:20; the kit's EVIDENCE WAIT absorbs it, see Q-1)

# B2043 DRAFTER REPORT (Sonnet, in-session, read-only) -- NexusAI records kit for seat R315: pull requests 245, 246 and 247

Clocks from `date`: first read 13:55:02 AEDT 2026-11-24, last read 14:11:20. Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2043_SEAT-R315_nexusai-records-245-247.md` (107727 bytes, 216 lines), sidecar `...md.measured` (148 claim lines), this report. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s322/d2043/` (texts, builder, scanner copy, pointer program, raw reads, `facts.json`, `jira.json`, `searches.json`). The commission's header correction ("Tuesday's count between 13:54:02 and this commission; that count printed no clock") was re-read from line 8 of the commission file and the kit says exactly that; the old "13:5x" wording is not in the kit.

## BLUF
1. A records kit, form of B2004's kit: Step 0 to 8, 4 Jira comments (RD-1031, RD-1021, RD-1034 each with a move to Testing; RD-1022 evidence only, no move), up to 3 creates (NEW-A plain data-source list routes, NEW-B test-harness sentinel, NEW-C dark High Risk label), one new section 110 with three entries C-317 (PR 245), C-318 (PR 246) and C-319 (PR 247 with the open Q-5 paragraph), and one optional history branch `records/b2043-history`. Seat id R315, Sonnet, launch line in the cockpit form with `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.
2. Pull request 245 is the previous pass's history branch (B2004 / R306; merge `0e33bb8e`, 21:42:23 AEDT on 2026-11-23, HISTORY.md +22/-0, tree equal, 6 check-runs success, no Deploy demo run). No FOR-RECORDS or gate folder exists for it; drafted from the PR, its checks and the B2004 STATUS.
3. Pull request 246 (RD-1031; merge `d96a83d3`, 01:06:29 AEDT on 2026-11-24; the commission says 01:07) and 247 (RD-1021 + RD-1034; merge `04a6b89d`, 13:52:56; the commission says 13:53): the kit uses the measured clocks.
4. The Q-5 card stays unread (I read no card; "open" is RELAYED by the commission). The entries record it open, no ruling, and HOLDS 2 forbids answering it.

## Facts re-measured (instrument; control)
- Pulls 245, 246, 247: `gh api -X GET pulls/<n>` (GH_CONFIG_DIR of NexusAI; `pulls/99999` -> 404 control): merged true; merge shas `0e33bb8e4846b4d829a60e3ba7299cdb60a38da5`, `d96a83d3ee6df25f74bcfe2f9ec0d0b42714e029`, `04a6b89dcd142eebdb99f441c3840e32d7e0701f`; parents (`21a07e3c`+`3fbe07a8`; `0e33bb8e`+`6e803935`; `d96a83d3`+`5c98e04d`); merge tree = head tree for all three (`fb7f8f42`, `f09ddd08`, `d882ab64`); files 1 (22/0), 2 (25/156), 10 (305/27).
- Check-runs: 245 and 246: 6 each, all success, 4 workflow runs, no Deploy demo run. 247 at 14:09:07: 8 check-runs; Analyze x3, scan, audit success; Deploy demo `build` and `deploy` skipped (run 45315569382); only `build` of the Build run 45315569282 `in_progress` (re-read at 14:11:20: still `in_progress`).
- Build job logs (`--allow-escape-sequences` needed; the plain call refused, printed in the kit): 245 job 137637639689 and 246 job 137747771351 each `VERDICT: PASS`, 6245/6245, 395 suites. Counts file at the three merges: 6245/395, 6245/395, 6280/396.
- Code scanning on main (paged): 22 open (same 22 numbers as B2004), 222 fixed, 7 dismissed; none fixed since 2026-11-22T13:00Z; main still `04a6b89d`, 0 open pulls, compare identical.
- Jira (read helper, in-process credentials, never printed): RD-1031, RD-1021, RD-1034, RD-1022 To Do, 0 comments, transition id 31 -> Testing on each; 1031 issues, highest RD-1035; `RD-99999999` -> 404; the 7 markers read 0, three controls read 1 each; label `records-pass-1124` 0 issues.
- Existing tickets found by search (named and held, not duplicated): RD-1025 (open window after a first-run reset, To Do), RD-285 (`reproduces itself`, To Do), RD-280 (state baselines drift, To Do, nearest family of the 982-vs-80 coupling); RD-404/RD-408 (product alarm, Release Ready) read: related, not the harness.
- Pointers: `pointers2043.py` -> `pointer rows 29 fail 0`, two controls False; `requireAdminFor(` 40 lines; `qa-surface-up.sh` holds `persistence-sentinel` 0 and `printer_logs.db` 4.
- Records files: CLARIFICATIONS.md 914067 bytes, 3200 lines, sha256 prefix dcbcc1262fb03bf6, section 109 at 3170, C-316 at 3194, 1361 non-ASCII bytes; HISTORY.md at 04a6b89d 10384 lines, 1134872 bytes, sha 66bd3b637b1d7665, 7563 non-ASCII bytes, last heading 10364. Computed layout: section heading at line 3202, entries at 3204 / 3208 / 3214 (file ends at 3220); HISTORY heading at 10386, file 10406 lines.
- Model: both earlier NexusAI records kits carry `MODEL SONNET (records)` on line 6 (B1947, B2004): consistent. Rows C7 97, C8 98, G3 110; model id line 23 of models_latest.json `claude-sonnet-5-5`.
- Seat id R315 free: ls count 0, `-w R315` over 11-23/11-24 SEAT kits 0 files; control R314 count 3. Ports: none. Panes at 14:11:20: `%0 tuesday`, two unnamed; none `Datasec/NexusAI-*`.
- Scanner: the project's `.tools/b2004/scan1947.py` sha256 prefix 3707dc37c4795fbf, 6267 bytes (read by shasum/wc only), equal to my copy; `--selftest` 67 ok, 0 FAIL. Over all 55 texts (26 Jira, 16 entry, 13 history) alone and with sample fills: 0 hits after re-wording; the first run read 12 hits (substring `coordinator` in four texts, `2.48`, `4.5`), which proves the scanner fires on these texts. Every kit text line carries its sha256 prefix and I verified the 55 kit lines equal the frozen source (0 mismatches).
- `stamp_check.py <kit>` exit 0 (148 claims, 148 measured). The sidecar mixes REAL measurements (pointer rows, counts, Jira reads, panes, df) with INSTRUCTION literals (commands and slot words the seat runs): those lines say "instruction ... UNMEASURED as output". Tuesday should spot-measure at least five from the real ones.
- Steps table (inputs each from an earlier step or present at BASE): Step 0 (kit stamped; df; panes) makes `.tools/b2043`, scanner copy; Step 1 (git config, deploy key `3_Access_Keys/github_deploy_rw` exists, .env exists, repo exists) makes identity.log; Step 2 (scanner copy from Step 0, Jira names) makes helpers and the selftest log; Step 3 (CLARIFICATIONS.md, Jira, GitHub, Step 1's fetch) makes snap_before.json, facts.json, the EVIDENCE WAIT result; Step 4 (helpers, facts, kit texts) makes dry/ payloads; Step 5 (dry payloads, snap_before) makes comment ids, created keys, snap_after; Step 6 (Step 5 results, before-copy) makes entry-numbers.txt; Step 7 (entry-numbers.txt from Step 6, identity from Step 1, origin/main from Step 1) makes the branch.

## D-decisions (drafter's, each for Tuesday to accept)
- D-1 Three entries (one per landing) in ONE section 110, not one entry: the landings are different tickets and lanes; C-319 carries the open question paragraph.
- D-2 Three creates: F-1 (the plain list routes) as NEW-A; the sentinel noise of both reviews folded into NEW-B (one root cause); the dark High Risk label as NEW-C. RD-1022's F-3 is a comment, never a ticket (commission). The 982-vs-80 dataset coupling is a record line (RD-280 nearest, not written).
- D-3 RD-1025 (open window) and RD-285 (`reproduces itself`) are named and held, no comment, under the B2004 closed-list rule "a found duplicate is named and held". The commission only licensed an RD-1022 comment.
- D-4 Moves to Testing for RD-1031, RD-1021, RD-1034 (project `CLAUDE.md` line 302; `CLAUDE.md` line 273 gives Tuesday ticket status authority), each only after the move check; RD-1022 gets no move.
- D-5 The 247 hosted facts (checks, Build log, Deploy demo, scan) are FILL-INS by program from the seat's own read after an EVIDENCE WAIT (3-minute polls, at most 25 minutes); a pending or red run HOLDS the 247 texts and ends in `STOPPED: NEEDS TUESDAY`. 245 and 246 hosted facts are embedded (re-measured by the seat).
- D-6 Entry texts name no card id and no seat id; the Q-5 paragraph quotes the options from the review's `CARD-Q5.md` (a file, not the store).

## Questions for Tuesday (each with a default)
- Q-1 Launch while the Build of `04a6b89d` is still running? Default: yes, the seat waits inside Step 3 (the Jira time budget is 60 minutes with it).
- Q-2 Fold the first-boot banner (RD-1031 candidate 3) into NEW-B with the harness alarm noise? Default: folded.
- Q-3 The dataset coupling (982 vs 80; RD-1031 candidate 2): record line only? Default: yes; alternative is a comment on RD-280.
- Q-4 Comment on RD-285 (the SSL-panel flake, 1 in 5) and RD-1025 (the open window)? Default: none; named and held.
- Q-5 NEW-A priority Low (the review graded F-1 "medium, informational")? Default: Low; Medium is a one-word change before the stamp.
- Q-6 Slot COMMENT-1022: default recommended `1022` (evidence only, no move).
- Q-7 Launch form: the cockpit `add` line as B2041 ran (written in the kit), or the B2004 waiter form. Default: cockpit line.
- Q-8 PR 246 and 247 clocks: the commission's 01:07 and 13:53 are rounded; the kit uses 01:06:29 and 13:52:56 (GitHub's `merged_at`, AEDT = UTC+11). Default: measured.
- Q-9 A concurrent build kit (B2042, seat N170, RD-1026) is being drafted: it writes no records file and creates no ticket, so REFUSE 6 does not stop on it; sequence is yours. Default: launch independently.

## UNMEASURED / never run on a real output
- The local git identity prefix `be76c2c1baf03ec1` (RELAYED from the B2004 STATUS; `git config` is not a drafter verb). Only the author-address CLASS of the B2004 history commit (noreply) was read on GitHub.
- The Build log, the analysis and the code scanning effect of the merge of 247 (pending at my reads).
- The source and file:line of the High Risk label colour (NEW-C says so); the product location of the "Persistence sentinel MISSING" alarm and the 127 count (relayed from the gate's FOR-RECORDS); how a viewer sees the Data Sources tab (read from `admin.js` lines 182 and 183 only).
- The seat's helpers (ADF builder, posting path, append helper, the entry-line check beyond the project scanner, the Step 7 helper, the EVIDENCE WAIT poll, the FOR TUESDAY lister) have never run: marked in HOLDS 3. The one STOP-severity check I could run, the text scan, ran PASS on my prototype output with its control fired (the 12-hit first run; the 67 selftest controls); the extra entry checks (no card id, no seat id, no B-number, no URL) were NOT run by a program of mine beyond the scanner's own `entry` classes.
- The Q-5 card state itself (no card read; "open" relayed by the commission).

## Outside the fences (disclosure)
- Two Bash calls at the start contained `cd`; the hook refused both, nothing ran; no `cd` after.
- I imported Tuesday's s317 drafter tools read-only (`j2004.py` Jira GET helper, `scan1947.py` copy) and stat/shasum'd `.tools/b2004/scan1947.py`; stat'd one path `.tools/b2043` (absent). I did not list `.tools/`.
- I read NexusAI `CLAUDE.md` lines 267 to 310, the B2004 and B2013 and B2032 STATUS files (parts), both gates' files, the review folders' CARD-Q5.md (a file), `CLARIFICATIONS.md` and the B2004 kit whole.
- No Jira write, no GitHub write, no card read, no `decision_queue.sh`, no az/ssh/docker, no request to the demo or any app host, no listener started (one `lsof` count read, 14 listeners, none mine). Files written: the kit, its sidecar, this report, and scratch under `fleet/state/s322/d2043/`.
