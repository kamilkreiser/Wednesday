STARTABLE: YES (batch 3b, 38 keys; B1019 landed and is finished, no records seat is live, B1020 has no pane and touches neither Jira nor the root records)

# B1021 drafter report (SEAT-R105, MPS records: batch 3b of the merged MPSCALC tickets under C-79), 2026-11-01

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1021_SEAT-R105_mps-records-done-batch3b.md` (152 lines; B1019 shape). Its `.md.pre-stamp` is a byte copy: `cmp` equal, sha256 `610ba02c...2a609be9` for both. Unstamped it has 6 lines with the four-underscore pattern (5 slot lines and the last line). Non-ASCII bytes 0 (control 2).

## BLUF
- **One kit for all 38 keys.** These are MPS #99 to #125. Every squash reads `behind` `e027ebd0`, so none is in the hosted build (control: the #73 squash reads `ahead`). Every squash reads `ahead` of code main `edac7431`. The Hosted sentence on all 38 is: "The squash is not in the build the project records as hosted; it is merged to main only (relayed, not probed by this pass)."
- **First pass: 31 MOVE-likely (5 of them only by reading (i)), 1 conditional (MPSCALC-197), 6 HOLD (MPSCALC-189, -198, -215, -217, -316, -325).** Write cap 76 (38 comments plus at most 38 transitions).
- **Q-7 from B1019 is answered in the kit as reading (i).** It is the coordinator's reading, not the product owner's, and rests on reading (d) as worded at `CLARIFICATIONS.md:1727`. A NO GO at the round cap does not contradict a move under condition (3) when two things hold: each of its open findings is filed as ANOTHER ticket, and this ticket's own clauses read MET with an acceptance that names none of those residuals. A residual held as a comment on the ticket itself does not count as filed, and holds the ticket. It is gated by a new slot, `CAP-READING` [YES]. It covers MPSCALC-190 to -193 (gate B547; findings filed as MPSCALC-318, -319, -320) and MPSCALC-176 (gate B766; findings filed as -350 and -351). MPSCALC-189 is held, because B547-3 sits on it as comment 39958 and its acceptance names the twin class.
- **What 3a taught, built in:**
  - copy only the 14 tools 3a ran, plus `scan610.py` and the driver; the 5 stale copies are named and not copied;
  - set `BASE` by hand;
  - the driver prints its last 12 lines and the return code on failure;
  - move the heartbeat out of a `logs/` folder;
  - the git-status baseline is 837 before the Step-0 copy and 838 after it;
  - pre-scan quoted fragments for banned words (MPSCALC-211 says "live path");
  - BACKLOG rows claim only what was grepped.
- Model: Sonnet, C8 `model-routing.md:98` (C7 `:97`), `claude-sonnet-5-5` (`models_latest.json:22-23`). `BRIEF_SEAT_LEVEL=sonnet` is inside the launch quotes (`brief_seat.sh:24` defaults to opus). Ports: none. Load1 was 9.41 at drafting, so `launch_when_cool` will wait.

## First-pass per-key table (from Jira text, the gates' first lines and their Done-when rows; the seat re-derives every clause)
| key | PR(s) | last gate | lead | reason |
|---|---|---|---|---|
| 104 | #99 | B545 GWF r2 | MOVE | "-104 3 of 3" |
| 176 | #125 | B766 NO GO r2 cap (C-77 landing) | MOVE (i) | 3 clauses MET (40195); B766-1/-2 -> MPSCALC-350, B766-3 -> -351 |
| 189 | #100 | B547 NO GO r2 cap | HOLD | B547-3 is ON this ticket (39958); acceptance names NFC twins |
| 190 | #100 | B547 | MOVE (i) | 1 of 1; B547-2 -> MPSCALC-319 |
| 191 | #100 | B547 | MOVE (i) | 2 of 2 |
| 192 | #100 | B547 | MOVE (i) | 1 of 1 |
| 193 | #100 | B547 | MOVE (i) | 2 of 2 |
| 196 | #102 | B575 GWF r3 of 3 | MOVE | 4 of 4 |
| 197 | #99 | B545 GWF r2 | COND | clause 2: a hosted count must come before any save refusal; C-54 says that refusal is unbuilt |
| 198 | #103 | B553 GWF r2 | HOLD | the e2e spec was written but no gate ran it (B546-7, B553 "E2E: NO"); same as 3a's -297 |
| 199 | #103 | B553 | MOVE | MET |
| 204 | #107 | B604 GWF r2 | MOVE | 6 of 6; ruling C-62; B604-1 -> MPSCALC-333 |
| 208 | #103 | B553 | MOVE | MET; check the widened Care pack/Staging labels (39565) |
| 210 | #102 | B575 | MOVE | (e) was PARTLY at B552 and is MET at B575 |
| 211 | #99 | B545 | MOVE | 1 of 1 |
| 215 | #102 | B575 | HOLD | (c) inventory PATCH NOT MET (B552 row 140) |
| 216 | #102 | B575 | MOVE | 4 of 4 |
| 217 | #102 | B575 | HOLD | (b) repeated supply row PARTLY, narrowed (reading g) |
| 219 | #105 | B581 GWF r2 | MOVE | 6 of 6 "already fixed": name the squash |
| 220 | #103 | B553 | MOVE | MET |
| 228 | #105 | B581 | MOVE | 9 of 9; C-49 rule 1, C-57 words |
| 230 | #102 | B575 | MOVE | 1 of 1; C-49 rule 3; check no new words |
| 291 | #106 | B576 GWF r2 | MOVE | MET; B576-1 -> MPSCALC-328 |
| 292 | #106 | B576 | MOVE | MET |
| 293 | #106 | B576 | MOVE | MET; "user-facing literal changes 0" |
| 294 | #106 | B576 | MOVE | MET |
| 301 | #103 | B553 | MOVE | MET |
| 303 | #104 | B580 GWF r2 | MOVE | 1 of 1; B562-1 and -2 closed at B580 |
| 316 | #107 | B604 | HOLD | ruled sentence built, but `maxLength 100` (:849, :897) and `QuoteEndpoints.cs:1424` are open and on no other ticket |
| 318 | #104 | B580 | MOVE | 3 of 3 |
| 319 | #104 | B580 | MOVE | 2 of 2 |
| 320 | #104 | B580 | MOVE | 2 of 2 |
| 322 | #102 | B575 | MOVE | "B552-1 closed" |
| 323 | #102, #108 | B594 GWF r1 | MOVE | B594-1/-2 -> MPSCALC-332 |
| 324 | #102, #108 | B594 | MOVE | 4 survivors killed |
| 325 | #102, #112 | B678 NO GO r2 cap (C-78 landing) | HOLD | B678-2 "touches the acceptance itself" (40186), though it is filed as MPSCALC-355; #112 red push run |
| 326 | #102, #108 | B594 | MOVE | answer 2 |
| 327 | #102, #108 | B594 | MOVE | answer 2; count the member-group rows |
Totals: MOVE 31 (176, 190 to 193 by reading (i)), COND 1, HOLD 6.

## Facts re-measured (instrument; control)
- **Root** (`git --no-optional-locks`):
  - main `89522e10` = HEAD; 44 branches; remote count 0; no MERGE_HEAD or index.lock.
  - Status lines 837. Numstat: BACKLOG +2180, JIRA +355, history +430.
  - CLARIFICATIONS: 1833 lines, 80 `### C-` headings, C-79 once at :1712 (control C-78 once at :1620). C-80 appears 0 times across all 44 branches (control: C-79 on `records/b1019` 1). Newest section at :1778.
  - `.tools/b1021`, `wt-b1021-records` and `.git-lock` are absent. `records/b1021` rc 1.
- **Jira** (own GET reader):
  - 356 issues: Backlog 291, Done 65.
  - The 38 keys: all Backlog, Task, 49 comments, total by field = total by endpoint on each.
  - `text ~ "B1021"` 0 and `labels = mpscalc-b1021` 0. Controls: `zzqxnonexist` 0, `key = MPSCALC-341` 1, `text ~ "B1019"` 39.
  - Transitions on MPSCALC-104 and -327: 11/21/31/41 Done.
- **PRs** (`gh api -X GET`):
  - 11 read; all merged into main. Figures are in the kit table.
  - Check-runs 8/8/0 on all but #112, which reads 8/6/1 (dotnet failure, package skipped; push run 40237171081 failure).
  - Carve-out facts: #112 has 4 files and none is a publish path; the B160 test name is in `PublishOutputTests.cs` on main once (control 0); #125 and main push runs are success. The job log itself is RELAYED (40186, C-78).
  - Controls: `pulls/99999` 404, `compare/nonsense...main` 404.
- **Residual census** (`text ~ "<finding>"`; control 0):
  - filed elsewhere: B553-1 -> 321, B576-1 -> 328, B581-1 -> 330, B594-1 -> 332 (+323), B604-1 -> 333 (+204), B766-1 -> 350 (+176), B678-2 -> 355 (+325);
  - on the ticket itself: B547-3 -> 189 only, B591-9 -> 316 only;
  - `B562-1` 0 (closed at B580, never ticketed).
- **Partition:**
  - tmux shows only tuesday, fleet-monitor, NexusAI-M60 and HPSM-POC-H89. No MPS seat.
  - B1015's STATUS reads READY FOR QA; B1020 has no STATUS.
  - B1020 kit line 14: it uses its own clone and touches no Jira, root records or `records/*`. It takes `.git-lock` for seconds around its clone and fetch.

## D-decisions
- **D1 One kit, not a split.** The commission names all 38 keys. 3a ran 39 keys and 67 writes and finished in 31 minutes of a 210-minute window.
- **D2 Reading (i) is written as the coordinator's, gated by a slot**, and kept narrow:
  - it changes only condition (3), never a clause;
  - a residual sitting on the ticket itself still holds the ticket.
- **D3 Slots:**
  - `DONE-SLOT` [MOVE-TO-DONE];
  - `CAP-READING` [YES];
  - `CARVE-OUT` [YES] for MPS #112. It only clears the red-run condition; MPSCALC-325 is held anyway by default.
  - No TIER2-ATTEST slot: every 3b PR had a QA gate.
- **D4 Target READY 150 and HARD STOP 210 minutes**, as 3a.
- **D5 Excluded keys = 50:** MPSCALC-153, -252 to -259, -261, -295, and the 39 3a keys. The residual tickets are read-only by name.
- **D6 Template sources:**
  - The launch line follows the B1019 template (`launch_when_cool.sh`), not the bare `cockpit.sh add` of DRAFTER_RULES.
  - I quoted the Done transition from B1019 STATUS:192, because B987's quote is older.

## Q-questions for Tuesday (each with a default)
- **Q-1 Size.** The batch has 31 MOVE-likely leads plus 1 conditional, over the ~30-move split line. Default: one kit (D1).
- **Q-2 Reading (i) / slot `CAP-READING`** (B1019's Q-7). Default: YES. MPSCALC-176 and -190 to -193 move where 4a reads every clause MET; MPSCALC-189 is held.
- **Q-3 PR #100 landed on the coordinator's round-cap ruling** (the section after C-54, `:1076-1078`), not a product-owner ruling. #112 (C-78) and #125 (C-77) landed on product-owner rulings. Default: the authority behind a landing does not enter the Done test. C-79 asks "merged", and condition (3) is about gate lines.
- **Q-4 MPSCALC-325.** Default: HOLD. The gate's words are "touches the acceptance itself", though B678-2 is filed as MPSCALC-355 and reading (c) would clear the #112 red. The alternative is MOVE under (d) + (c), if the seat reads the acceptance as met by the committed rows.
- **Q-5 MPSCALC-197 clause 2.** Default: MOVE only if the seat does both of these; else HOLD:
  - quotes the gate's MET reading of clause 2;
  - shows that no save-time refusal of repeated BOM numbers exists at the squash or at main.
- **Q-6 MPSCALC-198.** Default: HOLD. The e2e was never run, and CI has no Playwright; this is the same as 3a's -297.
- **Q-7 MPSCALC-316.** Default: HOLD. The open words are on the ticket itself, and its acceptance names "so a reader is not told 100 characters".
- **Q-8 MPSCALC-215 and -217.** Default: HOLD, unless the seat finds a later merged change that closes clause (c) or (b) (reading a).

## UNMEASURED
I made no write. These were not measured:
- the clauses against the squash diffs;
- gate STATUS bodies beyond their first lines and the Done-when rows of B538, B546, B552, B553 and B575;
- the #112 job log;
- whether MPS #127/#128 rows pin B678-2 (C-78 says UNMEASURED);
- the MPSCALC-327 member-group rows;
- which squash fixed MPSCALC-219;
- whether 230's block reuses an existing sentence;
- the hosted state (relayed);
- whether B1020 starts during the pass.

## Outside-the-fences disclosure
- **Files written:** the kit, the report, and the `.pre-stamp`. I made the `.pre-stamp` with `cp` (a shell write), not the Write tool, so the copy is byte-exact (`cmp` equal). I also patched the kit's line citations with a short `python3` in-place replace, which is a shell edit of my own file. After that I re-read every cited line.
- **Scratch went only to the session scratchpad:** `tools/ro.py` (a GET-only Jira reader that reads `JIRA_*` in-process), `tools/gh1.sh`, `d/b3b.json`/`.txt`, and `gh/pr*.json`.
- **I wrote my own reader** instead of running the project helper. I read the env loader and fence of `.tools/b1019/j1019.py` (lines 1-60 and the `call` lines), not by running it.
- **One GitHub code-search GET** (`search/code`) located the B160 test file.
- **Not read or run:** no card was read and `decision_queue.sh` was not run. No `fleet/briefs_staged`, scoreboard, ledger, WEDNESDAY or FRIDAY tree. Nothing under `.tools/b1020`, `b1015` or `wt-b1019-records` was read. I read the B1020 kit in `tuesday/briefs/` for the partition.
- **Hook output:**
  - A case-sensitivity advisory fired on three early `^### C-` greps. Their counts were re-done with `-i` and controls.
  - One zsh word-split refusal was re-run under `bash`.
  - An early zsh call passed 38 keys as one word and failed before any network call; it was re-run correctly.
- **My own mistakes, fixed before this report:** the first draft cited B1019 item 1 at `:1780`, C-54 `Not settled` at `:1043`, C-78's B160 line at `:1622` and item 3 at `:1824-1825`. They are now `:1782`, `:1042`, `:1623` and `:1825`.
