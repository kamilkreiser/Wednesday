STARTABLE: YES (batch 3a, 39 keys; B1013 is finished and nothing else holds the root records or these keys)

# B1019 drafter report (SEAT-R104, MPS records: batch 3 of the merged MPSCALC tickets under C-79), 2026-11-01

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1019_SEAT-R104_mps-records-done-batch3.md` (157 lines; B1004 shape without the C-entry job). Its `.md.pre-stamp` is a byte copy (`cmp` equal, sha256 `5b0a6f29...702e8a` both). Unstamped it has 6 lines with the four-underscore pattern (5 slot lines and the last line).

## BLUF
- **Batch 3 is too big for one pass, so I split it by the hosted build.** The sweep's lane 5 count reproduces: 80 open MPSCALC tickets carry `[B583]`. Three are excluded: MPSCALC-153 (B1004 held it), -261 and -295 (ruling relays with nothing merged; C-79 is silent on these and says they "stay as they are"). That leaves 77. My first pass reads about 63 MOVE and 14 HOLD, which is over the ~30 limit.
- **3a (this kit) has 39 keys.** These are the tickets whose PRs (MPS #73 to #97) are in `e027ebd0`, the build the project records as hosted. First pass: **29 MOVE (some conditional), 10 HOLD**. Write cap 78 (39 comments plus at most 39 transitions).
- **3b has 38 keys** (PRs #99 to #125, none in the hosted build). It is listed by name in the kit as not yours and is not drafted. First pass: **34 MOVE (some conditional), 4 HOLD**.
- **The C-79 test, quoted in the kit:** the product owner's words at `CLARIFICATIONS.md:1714`, *"Done means merged to main, the same as Composer"*. The test is at `:1716` (`Settles:`), recorded there as the coordinator's reading: "a ticket moves to Done when its change is merged to main AND each Done-when clause of the ticket is MET; a clause that needs a deploy, a words approval or a further ruling is still not met by a merge ...; a merge alone never moves a ticket; the rule is silent on tickets whose work is done by a ruling or a measurement with no merged change ..., which stay as they are". The kit also points to B1004's three conditions and readings (a) to (d) at `:1727`.
- **Transition id 41**, quoted from B987's STATUS ("11 Backlog, 21 Selected for Development, 31 In Progress, 41 Done (Done re-read by name at each transition)"). Re-read today on MPSCALC-232 and -341: the same four, HTTP 200.
- Model: Sonnet, C8 `model-routing.md:98` (C7 `:97`), `claude-sonnet-5-5` (`models_latest.json:22-23`), `BRIEF_SEAT_LEVEL=sonnet` inside the launch quotes (`brief_seat.sh:24` defaults to opus). Ports: none (records seat; no listener).

## Per-key first pass (from Jira text and gate first lines only, not diffs; the seat re-derives every clause)
### Batch 3a (this kit, 39)
| key | PR(s) | first pass | reason |
|---|---|---|---|
| 27 | #90 | HOLD | spec-seed; B348 "Done-when partly ... Offline not built" |
| 28 | #89 | HOLD | B347 "the Duplicate row action is not built" |
| 34 | #88, #90 | HOLD | B348: debounce, stale discard, line states, grouped totals not built; #88 red |
| 137 | #95 | MOVE (conditional) | needs-ruling label: moves only if the seat quotes the ruling (K-01) line |
| 150 | #73, #97 | HOLD | PARTLY-DONE scope; K-11 inputs left for later |
| 160 | #97 | HOLD | PARTLY-DONE; server half for callers without rights not built |
| 172 | #95 | MOVE | B455 GWF round 2 |
| 209 | #85 | MOVE | B318 GWF |
| 213 | #80 | MOVE (conditional) | "approved at the words gate" must be closed by a quoted line (C-34) |
| 214 | #82 | MOVE (conditional) | "words go to the product owner before any deploy" (C-40) |
| 231 | #83 | MOVE (conditional) | words-gate listing must exist |
| 232, 233, 234, 235 | #85 | MOVE | B318 GWF, clauses met |
| 236 | #85 | HOLD | B318 "3 of 5 acceptance clauses met" (issued, accepted: a coordinator divergence) |
| 238, 240 | #88, #90 | MOVE | B348 GO; #88 red needs the carve-out |
| 239, 242 | #90 | MOVE (reading a) | e2e clause closed by #91 / MPSCALC-309 |
| 241 | #88 | MOVE | B325 GWF; #88 carve-out |
| 244 | #89 | HOLD | "carried as ruled (purchase 3 of 4, rental 1 of 4 ...)" |
| 245 | #89 | HOLD | Home-figure CSV not built (39833) |
| 249 | #87, #90 | MOVE | B324 GWF, B348 GO |
| 262, 263, 266 | #86 | MOVE | B332 GWF round 2; -266's clause allows an absent filter |
| 289 | #93 | MOVE | B388 GWF round 2; #93 carve-out |
| 296, 298, 299 | #90 | MOVE | B348 GO |
| 297 | #90 | HOLD | smoke.spec edited, not run |
| 304, 305 | #92 | MOVE | B365 GO / GWF (different mechanism on -305) |
| 306 | #91 | HOLD | Action off-screen; owner question B354-5 |
| 307, 308, 309, 311 | #91 | MOVE | B354 GO / GWF |

### Batch 3b (not drafted, 38) and excluded (3)
MOVE (first pass): 104, 190, 191, 192, 193 (B547 NO GO at the cap, findings filed as -318/-319/-320: reading), 196, 197 (clause names a hosted count: check), 198 (the e2e is written but not run), 199, 204, 208, 210 (B575 "-210(e) MET"), 211, 216, 219, 220, 228, 230, 291, 292, 293, 294, 301, 303, 316 (open words not ruled: reading), 318, 319, 320, 322, 323, 324, 326, 327, 176 (B766 NO GO at the cap but all 3 clauses MET; landed on C-77). HOLD: 189 (residual B547-3 commented on the ticket itself), 215 (clause c on inventory PATCH NOT MET, B552), 217 (repeated supply row PARTLY, B552), 325 (B678-2 touches the acceptance; the #112 squash has a red dotnet job, B160 row). EXCLUDED: 153, 261, 295.

## Facts re-measured (instrument; control)
- Census: 83 comments hold `[B583]`, on 83 tickets; 80 of them are Backlog (control `zzqxnone` 0). By first words: 68 "merged work names this ticket", 6 ruling relays (153, 176, 204, 261, 295, 316), 6 "PR #102" forms (322-327). Status 319 Backlog + 37 Done; 500 comments = the sum of comment totals.
- PRs (`gh api -X GET`, project `GH_CONFIG_DIR`): 26 read, all merged into `main`. The 3a squashes all read `ahead` of code main `edac7431` and of `e027ebd0`, and #97 is `identical` to `e027ebd0`. The 3b squashes read `behind` `e027ebd0`. Controls: `pulls/99999` 404, `compare/nonsense...main` 404.
- Red check-runs (8/6/1, the dotnet job) on #88, #93 and #112. The job logs (they need `--allow-escape-sequences`) name the two FeedbackTicketTests from B987 item 4. #88 (run 39366766666, job 118445270333) fails "Enabled_a_201...". #93 (run 39514401396, job 118942969581) fails "A_timeout...". Neither PR touches a FeedbackTicket path (0 of 19, 0 of 4; control 19 and 3). #112 (3b, MPSCALC-325) fails the B160 publish row, as relayed in comment 40186.
- Root: main `aa5f8b9c` = HEAD, 43 branches, remote 0, status lines 834, numstat BACKLOG +2096, JIRA +346, history +424, CLARIFICATIONS 1776 lines, highest C-79 at :1712, C-80 0, newest section at :1758. `.tools/b1019`, `wt-b1019-records` and `.git-lock` are absent; `records/b1019` gives rc 1 (control `records/b1013` rc 0).
- Partition: `tmux` shows `Datasec/MPS-M55` (B1015, the MPSCALC-255 engine build on code repo branch `b1015/...`, no Jira, no root records: kit lines 5 and 21), plus HPSM-POC-R103 and NexusAI-M60 (other projects). B1013's STATUS last line is READY FOR REVIEW and it has no pane.

## D-decisions
- D1 Split by the hosted build, not by key order. Every 3a squash is in `e027ebd0`, so the Hosted sentence is the same on every comment. No PR named on a 3a ticket is named on a 3b ticket (measured: shared 0), so the two passes never re-read each other's squashes.
- D2 No C-entry in this pass (C-79 exists). One coordinator section, 0 C-entries; the C-scan asserts that C-79 stays the highest heading.
- D3 Slots: `DONE-SLOT` [MOVE-TO-DONE]; `TIER2-ATTEST` [YES] for MPSCALC-213 and -231 (the at-source review is recorded in the PR bodies; the other tier-2 keys had QA gates); `CARVE-OUT` [YES] for the #88 and #93 reds (B1004 reading (c)).
- D4 Target READY 150 / HARD STOP 210 minutes (B1004 used 120/180 for 17 keys). The "no new key after HARD STOP minus 20" rule still applies.
- D5 The seat copies the scripts from `.tools/b1004/` and must diff every sed change, because B1004 Correction 3 shows a blind sed of the batch number goes wrong.

## Q-questions for Tuesday (each with a default)
- Q-1 The split: 3a = 39 (hosted group), 3b = 38. Default: launch 3a now and draft 3b after 3a lands.
- Q-2 Hard stop 150/210 instead of 120/180. Default: accept 150/210.
- Q-3 `CARVE-OUT` for the #88/#93 reds (MPSCALC-34, -238, -240, -241, -289). Default: YES (same tests and same reading as B1004 item 4).
- Q-4 `TIER2-ATTEST` for MPSCALC-213/-231. Default: YES.
- Q-5 MPSCALC-236 and -244: a coordinator scope ruling or a "ruled" narrowing appears to replace clauses of the ticket's own text. Default: HOLD unless the seat quotes a product-owner ruling.
- Q-6 MPSCALC-306 (owner question B354-5) and MPSCALC-245 (R-V2-3 reading): default HOLD.
- Q-7 For 3b: do findings ticketed elsewhere after a NO GO at the cap (190-193, 176) count as "a gate line contradicts"? Default: no, where the ticket's own clauses read MET (B1004 reading d). To be settled in the 3b kit.

## UNMEASURED
No write of any kind. Not measured: the Done-when clauses against the diffs (the first pass reads Jira text and gate first lines only); gate STATUS bodies beyond their first lines; the ruling lines for 137/213/214/244; whether R-V2-3 is a product-owner ruling; the hosted state (relayed); the stability of the two FeedbackTicketTests; whether M55's PR lands during the pass.

## Outside-the-fences disclosure
- I wrote three files: the kit, its `.pre-stamp` copy (named in the commission) and this report. Scratch went only to the session scratchpad (`tools/ro.py` GET-only Jira reader, `a1-a3.py`, `gh1.sh`, the `d/all.json` dump, `gh/` PR jsons and two job logs).
- I wrote my own read-only Jira reader instead of invoking the project helper, as the B1004 drafter did. I read the env loader and `call()` of `.tools/b1004/j1004.py` (lines 42-120), not by running it.
- No card was read and `decision_queue.sh` was not run. No `fleet/briefs_staged`, scoreboard, ledger, WEDNESDAY or FRIDAY tree.
- My own mistakes, all fixed in the kit before this report:
  - The first draft said "75 of the 80" were the merged-work form; measured, it is 68 + 6 + 6.
  - It cited `:1745` for MPSCALC-153's hold (that line is -182); now `:1737` and `:1754`.
  - It left out MPS #87 (MPSCALC-249's unmounted panel); added with its facts.
- One `ls | grep -w R102` control printed 0, a broken control, because `_` is a word character. I redid it with a non-digit boundary (2).
