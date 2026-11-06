STARTABLE: YES (after Tuesday's stamp; defaults make it comment-only and file nothing; the recommended slots are in the slots file)

# B1355 DRAFTER REPORT (SEAT-R189, MPS records, evening pass)

Files: kit `2026-11-06_B1355_SEAT-R189_mps-records-evening-pass.md` (93 lines, ASCII, 13 four-underscore lines: 12 Stamp slots plus the last line), `2026-11-06_B1355_slots.json` (13 keys, valid JSON, no `@SEAT@`, no angle-bracket placeholder), this report. Template: R180's kit (B1316) as asked, with R183's (B1331) refinements; R183 is the newest records pass and carries the create branch and the right-way-round `compare`.

## BLUF
- **MPS's Done rule is C-79** (`CLARIFICATIONS.md:1712`, `:1714`, `:1716`, `:1727`, re-printed with `awk NR==n` at drafting). The kit quotes it and the readings (a)-(v) by line; no reading adds a real-browser leg.
- **MPSCALC-108, real browser NOT RUN: C-79 permits Done and does not compel it.** The ticket asks two things (ignore `printAs` while pending; recorder + double-click gives 1 call); the review marks both MET in jsdom and says a real browser/dialog/logo load was NOT TESTED (`B1346_STATUS.md:89`). The comment must say NOT RUN in those words. The move is the stamp's call (Q-1).
- **The OPEN is already recorded**: `BACKLOG.md` `[B483-E2E]` (:2413) and `[B704-B696-2]` (:2977) state the same `bom-v5.css` SyntaxError and the "0 tests in 0 files" whole-list result, and MPSCALC-334 comment 40155 (part B) holds it. A new ticket would duplicate. Default: one row; recommended: row plus ONE comment on MPSCALC-334; TICKET is a slot value if Tuesday overrides (Q-3).
- **MPSCALC-127 is measured met**: the change is MPS #98 (squash `4c593517`, merged 2026-10-23T03:53:18Z; "rounds nothing" 1 line before, 0 after and at `c55eb874`; the three fix-shape clauses read MET at `ENGINE.md:62`, `:64-68`, `:71`). One caveat: the gate of #98 left a Minor on that paragraph (the list omits whole-unit round-up) with no ticket and no row; reading (p) says record it as a row, not hold the move. The sweep's "unidentified earlier change" is #98.
- **Unfinished CI at drafting** (20:49-20:50): `ci` push run of `e7038ad0` (#162, MPSCALC-108) and `330a1c83` (#161, MPSCALC-94) `in_progress`; `c55eb874` is 8 of 8 success. The kit makes the seat poll before freezing a MOVE for 94 and 108.
- **Live-seat REFUSE**: R180's pane test does not fire on M99 (below); two other shapes in R180's kit could fire on a builder or a sibling pass, and are rewritten. M99's own kit refuses on a word scan for its paths in a live pane's kit, so R189's kit does not spell M99's paths, branch or folder names (0 hits by program).

## Facts re-measured (instrument; control)
- Clocks, `date`: 20:42:44 AEDT (PR reads), 20:49:35 (blob reads), 20:54:56 (pane list).
- **Code main** `c55eb874856fc34b5c13f190301c75f2e33e1869` (`gh api -X GET .../git/ref/heads/main`, project `GH_CONFIG_DIR`); open PRs 0, control `pulls/99999` 404. #162 `e7038ad0` (parent `aa7fd175`, 20:41:07 AEDT, 2 paths), #161 `330a1c83` (parent `e7038ad0`, 20:41:28, 1 path), #163 `c55eb874` (parent `330a1c83`, 20:41:45, 5 paths); merged_at by `date -r` under AEDT; each `merged true`, base main.
- **Blob equality squash vs head, 8 of 8 paths True** (`contents/<path>?ref=<sha>` `.sha`; control `ProposalPage.tsx` at `aa7fd175` vs the #162 head reads False). Reading (u) holds.
- **Hosted runs**: `e7038ad0` 7 check-runs, dotnet in_progress; `330a1c83` 8, package in_progress at the read; `c55eb874` 8 of 8 success, `ci` push `completed success` attempt 1; `Push on main` `completed success` on all three. Code-scanning open 0 and fixed 0: a zero with no control that fires (the kit says so).
- **Root**: `HEAD`=`main`=`847600008084b05c23e8affc609dddfe570b5501` (R183's commit); dirty = `history.md`, `BACKLOG.md`, `JIRA.md` only; CLARIFICATIONS 2592 lines, highest C-96 at :2583 (anchored `grep -i -c -E '^### C-96( |$)'` 1, `C-97` 0); next number C-97. BACKLOG 5064, JIRA.md 635, history 1394. `git remote` prints nothing. `.tools/b1355` absent.
- **Jira** (own GET, scratch reader, `.env` read in-process, never printed): 384 issues = highest key MPSCALC-384; Backlog 230, Done 154. MPSCALC-94, -108, -134, -127: Backlog, 0 comments; -106: Backlog, 1 comment (39426); -334: Backlog, 3 comments (40122, 40155, 40539). Transitions 11/21/31/41 read on -94. MPSCALC-108 priority Medium, assignee none. `text ~ "B1346"` 0, `"B1355"` 0, `labels = "mpscalc-b1355"` 0; control `text ~ "B1196"` 6; nonsense token 0.
- **Dedupe queries** (project JQL `text ~`, which stems; the control `Ancestors` returns 207 keys, so only symbol hits count): `CatalogueOverlayStore` 8, `RefuseSameDirectory` 2 (-94, -97), `printAs` 1 (-108), `flushSync` 0, `printPending` 0, `pdftotextTimeout` 0, `calleeName` 0, `killSignal` 1 (-134), `execFileSync` 1 (-134), `pdftotext` 1 (-134), `bom-v5` 2 (-334, -263), `SyntaxError` 1 (-334). BACKLOG `grep -c -i -F`: `flushSync` 0, `printPending` 0, `pdftotextTimeout` 0, `killSignal` 0, `B1346` 0 (control `B1316-` 7), `bom-v5` 5, `SyntaxError` 2. So findings 8-13 have no earlier row or ticket; the OPEN has three.
- **Pointers at `c55eb874`** (printed by `grep -n` / `awk NR==n` over raw files): `CatalogueOverlayStore.cs:243`, `:260`; `ProposalPage.tsx:215`, `:223`, `:234` (`finally` at :227 sits inside `printNow`, so a throw from `flushSync` at :234 leaves :223's flag set); `pdftotextTimeout.test.ts:32`, `:60`, `:93`; `ENGINE.md:62-71`; `PurchaseCalculator.cs:850`, `:985` (`Math.Ceiling`, 2 lines; the gate's :637/:780 moved); `bom.spec.ts:5,:8`, `smoke.spec.ts:2` imports; `ci.yml` playwright 0 lines (control `dotnet` 9).
- **MPSCALC-106 branch**: `compare c55eb874...cc2e0960` `diverged`, ahead 1 behind 3; round-2 branch `matching-refs/heads/b1352` 0 (the existing round-1 branch is the one M99 pushes to).
- **Ports**: `lsof -nP -iTCP:9500-9509 -sTCP:LISTEN | wc -l` 0, `9430-9439` 0, `9400-9409` 0; word-boundary scan of the 62 non-`.pre-` SEAT kits of 5-6 Nov: `R189` 0, `MPS-R189` 0, `B1355` 0, `b1355` 0, `950[0-9]` 0 lines (control `9400|9430` 12 lines, control `R183` 5 files). M99's block is 9470-9479 (from its kit): no overlap. Panes at 20:54:56: `tuesday`, `fleet-monitor`, `Datasec/NexusAI-G360`, `Datasec/MPS-M99`, `Datasec/NexusAI-G359`, `Datasec/NexusAI-N104`.
- **Model**: `model-routing.md:98` C8 (Sonnet 1st), `:97` C7 (not applicable, reasoned as in R183), `:110` G3 (no gate), `:111` cap rule; `models_latest.json:23` `claude-sonnet-5-5`; `brief_seat.sh:24` defaults to opus, so the launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.

## Fixed Jira text lengths (asserted by `python3 -I`; summary limit 255; ASCII; banned-word/char list clean; a planted control fired 7 kinds)
| text | length |
|---|---|
| TICKET-11 summary | 198 (OK) |
| OPEN-ticket summary (only under OPEN-AS = TICKET) | 194 (OK) |
| H (merged-only sentence) | 100 |
| H (no change made) | 64 |
| C (source line, with the day placeholder) | 30 |
| Done-rule line | 274 |
| 106 BLUF skeleton | 201 |
| 127 BLUF skeleton | 252 |
| 108 NOT RUN sentence | 164 |
| 106 coordinator-origin sentence | 211 |
Descriptions and comment bodies are built by the seat from the tables; there is no field limit on them besides Jira's body cap, which the seat checks at the freeze.

## Live-seat REFUSE (asked: would R180's shape fire on M99, and rewrite)
- R180's REFUSE 3 pipeline `... | grep -E '^Datasec/MPS-R[0-9]+$' | grep -v -x -F 'Datasec/MPS-R189' | wc -l`, run over planted lists: `Datasec/MPS-M99` -> 0; `M99` + `R189` -> 0; `R172` + `R189` -> 1; `R1890` + `R189` -> 1; `M94` + `R189` -> 0. **It does not fire on M99.**
- R180's REFUSE 4 (project-wide Jira totals, "a changed total is another pass's write: STOP") would stop a pass on a sibling records pass's writes; rewritten per key (that key HELD, the pass goes on). M99's kit says Jira read only, so it cannot trip it.
- R180's REFUSE 6 (stop if `.tools/.git-lock` exists after 15 minutes) would stop on a builder that took the lock for a fetch; the lock wraps ref writes only (DRAFTER_RULES), so it is no longer a Step-0 refuse: the seat waits at the ref write, up to hard stop minus 25.
- M99's own kit (line 112): refuse on a live `Datasec/MPS-*` pane whose kit GRANTS a path of its own, tested by `grep -l -w` over that kit. R189's kit has 0 hits for the two guard paths, the round-2 branch name, the round-2 tools folder and its brief id (`grep -c -w` 0 each; control: the same grep over M99's kit prints 10). Rewritten to refer to "the round-2 builder's paths".

## D-decisions the kit takes
D-1 C-79 as the rule. D-2 Defaults comment-only (MOVE-KEYS NONE, QUALIFIED-OK NO, ROW-RESIDUAL NO, TICKET-11 HOLD, OPEN-AS ROWS). D-3 Minors are rows (`[B1331-M-*]` precedent); B1346-11 is a ticket (the instruction). D-4 No duplicate ticket for the OPEN. D-5 MPSCALC-106 and -334 never move. D-6 One comment per key with the table. D-7 C-97 is a landing entry (copy of C-96's shape). D-8 Finding ids B1346-1/-2/-3 are allowed in the 106 comment and `[B1346-11]` in the new ticket's summary, by exact string (the instruction names them; the earlier kits banned finding ids in comments). D-9 Max writes 12: creates 2 (second only under OPEN-AS = TICKET), comments 6, moves 4 (94, 108, 127, 134).

## Q-questions for Tuesday (each with a default)
- **Q-1** MPSCALC-108: move to Done with the comment saying NOT RUN? Default: not moved (empty slot). Recommended: move, because C-79's words and every reading are silent on a real-browser leg and Done means merged to main (`:1714`); the move waits for the unfinished `ci` run to read success.
- **Q-2** MPSCALC-94 (review marks Y-3 "MET, on a Mac"; the hosted arm cannot run the refusal and the new rows are 0 red under the inside-walk mutant there): accept as MET (QUALIFIED-OK YES)? Default NO (comment "met on the review's machine, not shown on the hosted arm", stays). Recommended YES: the ticket's text names no runner.
- **Q-3** OPEN-AS: ROWS (default), COMMENT-334 (recommended), TICKET (duplicates two rows and MPSCALC-334 part B). Your commissioning words were "file it"; the dedupe says it is filed.
- **Q-4** Grade of B1346-11 (review: Minor, "Tuesday may read it stricter"): default Minor, ticketed as instructed with a one-line fix and a throw-once mock row.
- **Q-5** MPSCALC-127: include in MOVE-KEYS? Default NONE. Recommended: yes, with the Minor of the #98 review rowed (`[B1355-M-7]`).
- **Q-6** B1346-4 to -7 (class B Minors): not rowed here (M99's side; a fix may close some). Default: not rowed; say if you want rows anyway.
- **Q-7** The C-97 heading's question: default is the landing phrase "Did MPS #161 ... #162 ... #163 ... land on main?" with "no product-owner ruling is known to rest on it" (RULING-REF unfilled).
- **Q-8** CARD-REF default NONE.

## UNMEASURED
No Jira write; no test; no Playwright run (the `--list` exit and the 37-test parse are the review's, RELAYED); whether `ci` of `e7038ad0` and `330a1c83` finishes green; whether M99 keeps to its fences; whether a real `playwright test` hits the CSS import and which loader the earlier real runs used; whether any card or ruling stands behind these landings (decision store not read); Jira comment bodies after drafting; the hosted state.

## Outside-the-fences disclosure
Read-only throughout. Scratch Python reader `jr.py`/`jq.py` and small shell scripts in the session scratchpad (Jira GET only, `.env` read in-process, never printed; `gh api -X GET` only, under the MPS `GH_CONFIG_DIR`). I read: the MPS root records files (CLARIFICATIONS, BACKLOG, JIRA.md, history, CLAUDE.md line counts), the B1346, B517, B524, B1316, B1331 STATUS files, the R180/R183 kits and drafter report, M99's kit (for its partition and REFUSE), the sweep-1510 line 93, the daily note's lines mentioning 127 (no hit about it). Two hook refusals: a `git worktree list` in the project repo (a write verb; I did not retry it, I used `for-each-ref` and `ls` instead) and an unquoted `set -- $p` in zsh (rerun as a bash script). No `decision_queue.sh`, no card store, no `fleet/briefs_staged`, no scoreboard, no `_ledger.md`, no WEDNESDAY/FRIDAY tree. Files written: the three B1355 files in the briefs folder, plus scratch in the scratchpad.
