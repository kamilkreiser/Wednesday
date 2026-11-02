STARTABLE: YES (after Tuesday stamps the 9 slots and the last line; the RULING slot needs the card's verbatim words and clock, which this drafter could not read; unfilled, C-277 and the texts naming it HOLD and the rest runs)

# B1134 DRAFTER REPORT (kit `2026-11-02_B1134_SEAT-R138_hpsmpoc-records-274-275.md`, 21996 bytes, 10 four-underscore lines = 9 slots + the last line)

## BLUF
One HPSM-POC records seat files the product owner's frame chip ruling (option a) as C-277 and the landing of code PR #275 (squash 5f128fb8, merged 15:02:25 AEDT) as C-278, tests HPSMPOC-420 and -421 against B1121, and handles HPSMPOC-434. PR #274 was already recorded (C-275 :5321, comments 40650 and 40651), so nothing is owed for it. Defaults: -421 comment and move (every clause MET); -420 comment only (the chip, row and tiles are built, but "N answers so far" and "Answered N of M questions shown" still print another count, so not every clause of the ruled scope is met: not called done); -434 HOLD, no Jira write (the pin row is on the unmerged branch b1095, diverged from main; comment 40645 already says kept). HPSMPOC-405 and -409 untouched. No new C-entry says the tile label is accepted: its card is OPEN and the records say held from deploy. Jira: at most 3 comments and 2 transitions, 0 creates.

## Facts re-measured (instrument; control)
- Clocks `date`: 15:43:50 first read, 15:56:14 last HPSM read, 15:59:56 last df. Records main `be670d1c` (`git/ref/heads/main`; merge of PR #170), open records PRs 0, `records/b1134` 404 (control `records/b1110` = 466e7e79). Raw `CLARIFICATIONS.md` 5346 lines, headings C-270 :5278 .. C-276 :5336 (grep -n); `grep -c -i 'pull request 275|PR #275|5f128fb8|f762cc7'` = 0 over it, control `PR #274|4b3cefae` = 8. BACKLOG 3182 lines (last section :3157, `B1110-C1` :3178), history 2685 lines. Next free: C-277, C-278.
- Code main `5f128fb8` (`git/ref/heads/main`; `pulls/99999` 404); open code PRs 0. PR #275: merged 04:02:25Z = 15:02:25 AEDT, head f762cc7a, 24 paths (+830 -46), 2 commits, squash one parent; `ci` run 41386236618 attempt 1 completed success; code-scanning open alerts 0; check-runs 19 listed with mixed status (skipped/success, some `in_progress` at 15:50): the seat reads the conclusions before writing a CI sentence. Chip `CustomerShell.tsx:89`, `:92`, row `SecurityAssessments.tsx:23`, tiles `SecurityDashboard.tsx:29`, `SecurityReports.tsx:62` (raw GET at 5f128fb8, `grep -F`; matches B1121). Squash message read whole: it names the scored count, the 500 on an unparsable stored answer, the unchanged list route, +1 command, and "Left as they are, a words decision" for the two other lines; it does not hold "14 of the 20" (so B1121-1 is fixed in the text).
- Branch `b1095/...` = 76116bc6, compare with code main: diverged (ahead 3 behind 2; reverse ahead 2 behind 3): not merged. HPSMPOC-434 pin row therefore not on main (to be re-read by the seat with `git grep`).
- Jira (helper `.tools/b1110/jira.py` GET): 436 issues (Done 290, Backlog 143, In Progress 3), highest -436; -420 and -421 Backlog 0 comments; -434 Backlog comment 40645; -405 comment 40650, -409 comment 40651; -423 Done, 5 comments. `text ~ "B1134"` 0 and `"REC-LAND275-02NOV-K421"` 0; REFUSE 3 controls fire (`key = HPSMPOC-268` 1, `"qxv9k2zzprobe"` 0, `"REC-DONE-01NOV-K402"` 1).
- B1121 pointers (grep -n): tile label :139, tickets :146-150, stays-open words :151-154, findings :197-202, FOR TUESDAY :205-211, line 1 verdict. B1107 FOR TUESDAY item 4 at :229; B1095 kit :20, :85.
- Hosted state: 48 `Briefs/2026-11-0[12]_B*_STATUS.md`; 0 start `DEPLOYED`, `PARTIAL`, `ROLLED BACK`; control `DEPLOY` prints B1031 and B1048.
- Panes: `%0 tuesday`, `%73 Datasec/HPSM-POC-H102` (builder, no records, no Jira), `%1 fleet-monitor`. R136 (B1129, removes old lane trees) is NOT live; the kit's REFUSE 7 stops if it is. Ports: none (`lsof` 9900-9999 empty).
- Disk: `df -g` 26 GiB at 15:43, 15:52 and 15:59:56 (the drafting reads cost nothing). **The analysis repository is 604 MB tracked (12905 blobs, git trees API, `truncated` false): a checkout or worktree with files is over the 0.5 GiB bound, and `sparse-checkout` writes the root `.git/config`, which R130's partition forbids.** Smallest route the rules allow, written into the kit: `worktree add --no-checkout`, `read-tree`, edited files in scratch, `hash-object -w`, `update-index --cacheinfo`, one commit, so only the three edited files (about 2.7 MB) exist on disk plus a fetch into the root `.git` (685532 KB at drafting; STOP if it grows over 400000 KB). Tools 36 files, 227109 bytes.

## D-decisions
- D1: entry order C-277 ruling, C-278 landing (records follow the order of recording; the ruling precedes the build). The seat re-scans before any Jira write because the Jira texts name both numbers.
- D2: -420 stays comment-only (see BLUF); the slot lets Tuesday move it. -421 moves.
- D3: -434 no second comment: 40645 already records kept and says the row is unlanded; the seat re-reads main and writes TX-434 and the move only if the row is on main.
- D4: Jira texts carry no finding ids, no card ids, B-numbers B1121 and B1134 only; the tile label sentence is "held from any deploy until the product owner has seen it" (card open).
- D5: the plumbing route replaces R130's full worktree (disk); push, PR and head-pinned merge commit are R130's Step 8 unchanged.

## Q-questions for Tuesday (default if unanswered)
- Q-1: should HPSMPOC-420 move to Done on #275 although "N answers so far" stays open? Default: no, comment only.
- Q-2: ruling words and clock for the RULING slot (this drafter did not read the card: the task forbids `decision_queue`). Default if blank: the seat HOLDS C-277 and the -420 and -421 comments (they name it) and writes C-278 and the rows only.
- Q-3: -434: wait for the branch to land (default) or record "kept" now with a second comment? Default: wait.

## UNMEASURED
The ruling's words and time; the review-copy and demo shas after today (the kit writes them as relayed); SQL Server leg, CodeQL of the records PR; whether the 3 In Progress Jira keys include any this kit touches (none named); the T15 row's file path (found by `git grep` by the seat).

## Outside the fences (disclosure)
No writes anywhere except the four files and scratch in the session scratchpad. I imported the project's `jira.py` helper (GET only; it keeps no heartbeat file: checked with grep, no `__pycache__` created under `-I -B`). Raw GETs of the records files and PR #275 files and code files went to the session scratchpad. `du -sk` ran once on the root `.git` of HPSM-POC (0.2 s). No decision_queue, no Jira write, no Azure, no message to anyone. I also read the MPS `.tools/b1120/j1120.py` (for the sibling kit), which did append heartbeat lines when imported (see the B1133 report).
