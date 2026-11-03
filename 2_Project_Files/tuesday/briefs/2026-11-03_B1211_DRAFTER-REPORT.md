STARTABLE: YES (after the stamp; one soft caution Q-3)

# B1211 drafter report -- SEAT-R157 (MPS records for MPSCALC-373 / MPS #154)

Clocks (`date`): rules and gates read 13:27:13 AEDT; PR/Jira reads 13:27:24 to 13:29:20 AEDT (Tue 3 Nov 2026). Kit: `briefs/2026-11-03_B1211_SEAT-R157_mps-records-373.md`, 70 lines, ASCII 0 non-ASCII (python regex), 9 lines holding four underscores (8 slot lines + last line) -- control: `grep -c -F` over the same file.

## BLUF
One Jira comment on MPSCALC-373 plus an optional Done move (C-79: merged to main, not deployed, is enough; MPSCALC-361 precedent), one C-entry (C-90), BACKLOG rows (word-pack row, not a ticket), no creates. Writes 2 max.

## Facts re-measured (command + control)
- Code main = `5a483a908a1766591adc77279d657dbd59d5dd7b` (`gh api -X GET .../git/ref/heads/main`). `pulls/154`: merged true, merged_at 2026-11-03T02:25:51Z = 13:25:51 AEDT, 3 commits, +146 -2, 3 files; control `pulls/99999` -> 404. Squash has 1 parent `9bdf4548`; 3 paths as the task says.
- Blob equality head `76aa9599` vs squash: ENGINE.md `961c1d38`, RentalRecomputation.cs `77f03938`, VolumeBasisTests.cs `bad01e02` (same on both `commits/<sha>` file lists). Squash tree `b15cbb5aff...` equals the second review's merge write-tree `b15cbb5a...` (review STATUS Step 1) -- so the review tested the exact landed tree.
- Squash CI: 7 check-runs listed, conclusions `success`; `ci` push run and `Push on main` run `in_progress` at 13:27. Kit has the 40-minute poll and the move rule.
- Root: `rev-parse HEAD main` both `c9365c17...` (R152's ff). CLARIFICATIONS 2515 lines, 90 `### C-` headings, highest C-89 at :2506; `^### C-9` 0 hits on the working tree (control C-89 present); 62 local branches, C-90 on 0, C-89 control on 2. BACKLOG 4884 lines (last `[B1196-BATCHES]` :4879), JIRA.md 575, history 1353.
- Jira (project helper `j1184.call`, GET only): myself 200; 381 issues, Backlog 238, Done 143, highest -381 (paged all keys; sum = highest). MPSCALC-373 Backlog, label `mpscalc-b1159`, 0 comments, transitions 11/21/31/41. `text ~ "RentalRecomputation"` -> only -373; `zzqxnonexist` 0; `B1211` 0; `B1196` 6 keys (control).
- Rules text pointers at squash (`contents?ref=` raw, awk NR): RentalRecomputation.cs :22 and :23 are the MonthlyRevenue / MonthlyCost "quantity x (...)" strings; RECONCILIATION.md :48 the "Sum quantity x (base + pages x click + software)" row; ENGINE.md R-29 at :40; VolumeBasisTests.cs :206 and :226 are the two new rows (grep -n).
- Gates: round 1 `B1199_STATUS.md` NO GO (B1199-1 Major; N1-N7 at :143-149); round 2 `B1208_STATUS.md` GO WITH FINDINGS at the cap (B1199-1 closed, N2 killed, B1208-N1..N4). Read in full for round 2; round 1 Notes via grep.
- MPS convention for a landed ticket: C-79 (`CLARIFICATIONS.md:1712-1727`): Done = merged to main; conditions: slot, all clauses MET, no review line or red against it. `B1196_STATUS` moved nothing for -374 (comment only by slot) -- the kit's own precedent for the move is MPSCALC-361 (`[B1159-DONE-1]`, comment 40678). Hosted deploy: card-per-deploy (`CLARIFICATIONS.md:593`), does not keep a ticket open.
- Word-pack convention: BACKLOG `[B1111-WORDS-1]` chain, latest `[B1171-WORDS-1]` (:4788); no ticket.
- Partition: panes `Datasec/HPSM-POC-G313`, `Datasec/MPS-G316`, `fleet-monitor`, `tuesday`; no `MPS-R` pane (so REFUSE 3 passes only with the seat's own pane); ports 9900-9999 listeners 0; word-boundary scan of 134 non-`.pre-` SEAT kits of 11-02/11-03 for R157, MPS-R157, b1211, B1211: 0 each (control R152: 4). `.tools/b1211`, `.tools/wt-b1211-records`, `.tools/.git-lock` absent. `df -g` 351.
- Model: `model-routing.md:98` C8 Sonnet first; `models_latest.json:23` `claude-sonnet-5-5`; `brief_seat.sh:24` defaults to opus (level written inside the quotes).
- Scan rules read from `.tools/b1196/lib1196.py:24-50` and `scan610.py`: bans digit-dot-digit, dollar, percent, backtick, names (incl. the company name), "deployed", "live", "complet", Tuesday etc. Kit's fixed texts avoid them; R152's three narrowings (LIT1, LIT2, CHANNEL) are deleted in the kit.

## D-decisions
- D-1: No create/ticket at all (the task: word-pack items are a BACKLOG row if the convention says so; it does). Writes capped at 2.
- D-2: Per the new fixed-text rule (no B-number, no gate/lane/seat/brief words), Jira comment and C-entry say "independent review" with round and verdict and carry no finding ids or B-numbers; B-numbers stay only in the kit body, BACKLOG row ids, history and the JIRA.md section header (convention). R152's "[B1196]" tail became "Source: records pass, <<DAY>>."
- D-3: One C-entry (C-90) covers both the ruling and the landing (like C-88); heading quotes the ruling label "Build it, strict review (tier 1, as MPSCALC-361)". No card id in the kit; CARD-REF is a stamp slot (the id for `--delivered` is in the task text).
- D-4: Round-1 Notes mapping to rows: N3 and B1208-N3 and N5 -> `[B1211-WORDS-1]`; N1, N2, N4, N6 and B1199-1 -> DONE-1; N7, B1208-N1/N2/N4 -> G1208-NOTES. Each id once.
- D-5: The Api 3359 vs 3353 difference is a Note in the comment (tree differs, not a defect), per task.

## Q-questions for Tuesday
- Q-1: MOVE-373 -- MOVE-TO-DONE or COMMENT-ONLY? Default COMMENT-ONLY (kit safe value); recommended MOVE-TO-DONE if the squash CI reads 8 of 8 success and the seat's table is all MET: round 1 NO GO is closed by round 2 GO WITH FINDINGS, no regrade, Rules text is a word item not a Done-when clause.
- Q-2: Should the ruling's relay (live board 06:39 AEDT, option a) get its exact time and channel in slot RULING-REF? Default: the seat writes "the board, <time from the slot>"; UNMEASURED by me (I did not read the decision store).
- Q-3: The squash `ci` run was still in progress at drafting; if it finishes red the move is blocked and the comment says so. Default: launch anyway, the seat polls 40 minutes.

## UNMEASURED
CodeQL check names and code-scanning count on the squash; `ci` result after 13:27; whether the ruling changed after 06:39; the hosted state; search-index counts after the seat's write; whether G316's reads (MPSCALC-359) would see the changed Done/comment totals (information only).

## Outside-the-fences disclosure
None breached. Reads: both gate STATUS files, CLARIFICATIONS lines, `.tools/b1184`/`.tools/b1196` helper headers and the `j1184.call` helper (GET only, three throwaway scripts in the session scratchpad, no write), `gh api -X GET` under the MPS `GH_CONFIG_DIR` (raw copies of 4 squash files into the scratchpad). No `decision_queue.sh` call. Did not open `.tools/b1207`/`.tools/b1208`. The first `grep -n '^### C-'` was case-sensitive (hook advisory); re-run with `-i` and controls.
