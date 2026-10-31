STARTABLE: YES, after B1021 lands (the kit refuses while B1021's STATUS last line is not `READY FOR REVIEW: B1021 |` or its pane is up; one comment and one move on MPSCALC-255 under DONE-SLOT MOVE-TO-DONE; no C-entry)

# B1024 drafter report (SEAT-R106, MPS records: MPS #135, MPSCALC-255 engine half), 2026-11-01 07:1x AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1024_SEAT-R106_mps-records-255-fee-135.md`, 104 lines, 0 non-ASCII bytes (python byte count; a control string with one accented letter counts 2). It has the SHAPE of the B1013 kit, with the move mechanics of B1019/B1021. Stamp slots are left as four underscores: 6 lines match `/usr/bin/grep -c -E '_''_''_''_'` (control: a planted line counts 1). The `.pre-stamp` copy is byte-equal (`cmp` equal, sha256 `e0019fdd...415a` for both).

## BLUF
- Jobs: (1) one coordinator section on `records/b1024`, **0 C-entries**. That follows the template: B1013 held none, and you relayed that the product owner gave no ruling today; slot `RULING-TONIGHT` NONE, and any other value STOPS the seat. (2) **Up to 2 Jira writes on MPSCALC-255 only.** First one record comment. Then, under `DONE-SLOT` MOVE-TO-DONE, and only if the seat's own 4a table reads all four clauses MET, the comment reads back equal and no red run contradicts the move, transition id 41, re-read by the name Done. (3) BACKLOG rows for the 12 B1020 Notes, plus a landing pointer, an OPEN row for the separate work, and a STALE row for the build kit and builder STATUS claims. (4) A history entry and a `JIRA.md` section.
- The comment uses the gate's "Done on the engine half" sentence (B1020 STATUS line 141). A "Separate work" paragraph names the Api/DTO/openapi/web members, MPSCALC-264 and the purchase half of MPSCALC-256. The Status line says the move is the coordinator's reading of C-79 (`CLARIFICATIONS.md:1714` words, `:1716` test).
- The B1021 guard is REFUSE 7. The seat continues only when all of these hold: B1021's last line begins `READY FOR REVIEW: B1021 |`, no `Datasec/MPS-R105` pane is up, and no `MPS-R105` process is running. Any other last line is a STOP, including STOPPED and BLOCKED, because B1021 could resume. REFUSE 3 re-bases on root main as it stands then: the stamped head must equal the head in B1021's READY line, and the diff from `89522e10` may touch only CLARIFICATIONS.md. REFUSE 6 requires B1021's section to be the newest. REFUSE 8 takes the Done count from B1021's READY line.
- Model row: Sonnet, C8 (`model-routing.md:98`), `claude-sonnet-5-5` (`models_latest.json:22-23`). `BRIEF_SEAT_LEVEL=sonnet` sits inside the launch quotes (`brief_seat.sh:24` defaults to opus). Ports: none. Target READY in 60 minutes, HARD STOP at 120.

## Facts re-measured (instrument; control)
- **Landing** (`gh api -X GET pulls/135`; control `pulls/99999` 404): merged true; base main; head `687c6d1735c6...`; squash `5c64a44226614523031a7b2d67cb9bfb477a380e` with one parent, `edac7431...`. `merged_at` is 2026-10-31T19:57:38Z = 2026-11-01 06:57:38+11:00 (python zoneinfo). 1 commit, 5 files, +350 -5. **The squash tree `63455574...` equals the head's tree**; the base's `70553d31...` differs (control). Code main is the squash (`compare` reads identical). The squash is not in the hosted build: `compare` against `e027ebd0` reads behind. Open PRs: 121 and 120.
- **Hosted, at the head:** 9 of 9 check-runs `completed success` (control: a nonsense sha answers 422). CodeQL: 4 analyses at the head sha, `results_count` 0 each (the main ref returns rows: the filter can fire). Open alerts 0, fixed 0: this zero has no firing control. On the squash, `ci` 41236624685 and `Push on main` 41236624274 were both in_progress at 07:0x. The kit tells the seat to re-read both and never claim green.
- **Squash message:** the subject equals the gate's `squash-subject.txt`. `difflib` of the gate's `squash-body.txt` against the landed body finds exactly one changed line (`@@ -9 +9 @@`). The gate's `NOT TESTED: hosted CI and CodeQL.` became the measured hosted CI/CodeQL sentence. The body has one `Co-Authored-By` trailer. The PR body still holds `NOT TESTED` once; the kit records it and forbids editing it.
- **Jira** (read-only urllib GET; the `.env` is read in-process and no token is printed): `myself` 200.
  - MPSCALC-255: Backlog, Task, labels `lane-v4 mpscalc-b308 plan-b308-t-v4-4 tier-1`, **0 comments**, transitions 11/21/31/41.
  - Project: 356 issues, Done **65**; controls `zzqxnonexist` 0 and `key = MPSCALC-341` 1.
  - `B1024`, `mpscalc-b1024`, the full squash sha, `"MPS #135"`, `B1020`, `B1015` and `687c6d1*` all count 0. The control (the full `edac7431` sha) finds 3.
  - The acceptance sentence was read whole: four clauses split at semicolons.
  - Related, read only: MPSCALC-256 (comment 40383: its purchase half "waits behind MPSCALC-255") and MPSCALC-264 (the group editor, 0 comments).
- **Squash-tree reads** (`contents?ref=5c64a442`, raw; control string 0): `| X-38 |` appears once at `docs/ENGINE.md:164` (0 at `edac7431`; X-37 1). `PurchaseCalculator.cs:648-649` holds the `fee` gate and `feeDevices = s.FleetQuantity ?? deviceQuantity`. `ManagedServiceFeeTests.cs` has 13 test attributes. `PurchaseMapping.cs:32` builds the section from five arguments, so the fee cannot be reached through the Api.
- **Gate** (B1020 STATUS, 173 lines, read whole):
  - Line 1, line 172 and line 173 (`VERDICT: ... GO WITH FINDINGS (round 1 of 2) on main edac743`) are quoted. Round count: round 1 of 2 on the class "V4 engine: per-group managed-service fee", NO GO 0 before.
  - The Done-when table is at lines 134-140, all four clauses MET. The records sentences are at 141-142. Notes B1020-1 to -12 are at 113-124. The stale-claim judgement is at 125 ("none false with a verdict consequence").
- **Root** (`--no-optional-locks`): main `89522e10`; HEAD main; 0 remotes; 44 heads before `records/b1021`; no MERGE_HEAD or index.lock. `git status --short` 843 lines. Numstat: BACKLOG +2180, JIRA +355, history +430, all -0. CLARIFICATIONS: 1833 lines, 80 `### C-` headings, C-79 at `:1712`, no C-80, newest section at `:1778` (B1019).
  - At 07:03 `records/b1021` resolved to `89522e10` and `wt-b1021-records` existed. B1021's line 1 read "texts frozen ... Jira writes starting".
- **Seat names:** `R106` appears in 0 file names; in the 56 non-pre SEAT kits it appears word-bounded in 0 (control `R105`: 3). `B1024` appears in 0 files (control `B1021`: 3). The `b1024` names are absent.

## D-decisions
- D1: no C-entry, as the template has none and you relayed no ruling. Slot `RULING-TONIGHT` covers it.
- D2: tools are copied from `.tools/b1019/` (the run set B1021 used, with the transition branch), never from the live `.tools/b1021/`. KEYS is MPSCALC-255 only, MAX_WRITES 2. The excluded keys are named in the kit.
- D3: 4a is re-derived at the squash tree, B1019-style. Each clause has named backing. A clause that only someone's say-so supports is NOT MET, which makes the ticket comment-only with the PARTLY-DONE sentence.
- D4: the coordinator's design calls are quoted as the coordinator's, from B1015 kit stamp line 90 (Q-2 to Q-5), not as the product owner's words.
- D5: the Notes map is N1 (B1020-1, -2), N2 (-3), N3 (-4), N4 (-5), N5 (-6, -7), N6 (-8), N7 (-9) and N8 (-10, -11). B1020-12 gets a "no row" line because the landing closed it. That is 12 ids, asserted by program. Extra rows: `[B1024-135]`, `[B1024-OPEN-1]` (the Api half has no Jira ticket) and `[B1024-STALE]`.
- D6: the section raises one question for the coordinator without ruling on it: MPSCALC-252 and -259 stayed Backlog under B1013's comment-only slot, while -255 moves on the same kind of engine-half reading.

## Q-questions for Tuesday (each with a default)
- **Q-1 Consistency with B1013.** In B1013 you held MPSCALC-252 and -259 even though their engine clauses read MET, because the Api half was not built. MPSCALC-255 now moves on the same footing. Default: move -255 as you decided, record the difference in item (4) as an open question, and leave -252 and -259 alone (a later pass may re-judge them).
- **Q-2 Red-first backing (slot `RED-FIRST`).** The gate did not re-run the builder's red-at-inert test. It backs "red-first test" with its own GR1 run: with the fee ignored, 8 builder rows go red, on a head whose tree equals the squash's. Default: GATE-RUN, so this counts as a gate measurement and clause 3 is MET. BUILDER-ONLY makes clause 3 NOT MET and the ticket comment-only.
- **Q-3 The Api half has no ticket.** No Jira ticket holds the Api/DTO/openapi/web members of the fee (the `managed-service` search found only -25, -255 and -256). Default: a `[B1024-OPEN-1]` BACKLOG row only, no ticket created (the kit has no create path), and the comment names it as separate work. If you want a ticket, that is a later records kit.
- Q-4 Clock: default target 60 / hard stop 120 minutes (one key).
- Q-5 `DONE-SLOT`: default MOVE-TO-DONE. The launch-authority line must name C-79, or the seat treats the slot as COMMENT-ONLY.
- Q-6 `RULING-TONIGHT`: default NONE (relayed by you; the decision store was not queried, per the fence).
- Q-7 Stale Dependabot notice: the builder relays 4 alerts on main. Default: record it as RELAYED in `[B1024-STALE]` and don't measure it.

## UNMEASURED
- B1021's outcome: its landed head, Done count and section heading line. It was writing at drafting.
- The two runs on the squash (in progress at drafting).
- The hosted state, beyond the compare.
- Who landed the PR and with which flags.
- The builder's red-at-inert run.
- The Dependabot alerts.
- MPSCALC-25's text.
- The B1020 evidence files (only the two squash files were read).

## Outside-the-fences disclosure
- **Written:** the kit and this report with the Write/Edit tools. The `.pre-stamp` copy was made with `cp -p`, not the Write tool, to get a byte-exact copy; `cmp` confirms it. The rules say Write/Edit only, so I am stating it here.
- **Scratch** (session scratchpad only): `jr.py` (a GET-only Jira reader), `msg135.txt`, `prbody135.txt`, and `i252/255/256/264.txt`.
- **Read:**
  - `DRAFTER_RULES.md`.
  - The B1013 kit and report; the B1019, B1021 and B1015 kits.
  - STATUS files: B1020 whole; B1021 (9 lines); B1015 (headings, Decisions, Corrections, Open); B1013 and B1019 (Corrections and last lines).
  - Project files: CLARIFICATIONS lines 1712-1722 plus the heading census; BACKLOG ids; JIRA headings; the history top.
  - Fleet files: model-routing lines 97-98, models_latest, brief_seat line 24.
  - Directory listings (`ls`) of `.tools/b1019`, `.tools/b1013` and `.tools`. I opened no file under `b1020` or `b1021`.
- **GitHub:** `gh api -X GET` only, under the project `GH_CONFIG_DIR`. Jira: GET only. No HTTP to any hosted host.
- **Not touched:** `decision_queue.sh`, briefs_staged, the scoreboard, the ledger, and the WEDNESDAY and FRIDAY trees.
- **Hooks:** three of my calls were refused before they ran: one for a `cd`, one for an unquoted zsh variable, and one for a bare `===`. All three were re-issued correctly. There were advisory notices on case-sensitive greps. No `cd` ran.
