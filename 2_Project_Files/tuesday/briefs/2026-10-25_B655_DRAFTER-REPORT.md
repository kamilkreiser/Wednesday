STARTABLE: YES (after the stamp; launch only at load1 below 7: load1 was 15.21 at 10:57)
Topic: mps-records-111-and-rulings-1025. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B655_SEAT-R38_mps-records-111-and-rulings-1025.md` (134 lines). Pane `Datasec/MPS-R38`, Sonnet, launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.

BLUF
- One records seat for lane R-MPS: PR #111 (squash `dd0ce36d`) as a landing record, gate B643 as ONE ticket (B643-1,-2,-3 Minor + -4,-5 Note, 12 survivors), 7 comments (-334, -329, -332, -290, -169, -288, -325), six C-entries C-66..C-71, one Tuesday section, 8 BACKLOG rows, 2 history entries, 1 JIRA.md section, the stray 63-byte file moved by the sixth ruling's grant (PART 5), root `main` fast-forwarded by the seat itself (B610's pattern, MEASURED: root HEAD `823480a7` = B610's commit).
- The walk-cap ruling is recorded as ruling only (C-70, "Delivered: none on main; the build is with B654"); PR #110 / MPS-G107 / MPS-M21 paths are fenced from both sides.

Facts re-measured (instrument; control)
- Name: `MPS-R38` unused: `grep -l -E 'MPS-R38([^0-9]|$)'` over non-.pre- SEAT kits of 24-25 Oct rc 1; `tmux list-panes` count 0 (control `MPS-G107` count 1). R35/R36/R37 are HPSM-POC; MPS-R34 is B610 (finished).
- PR #111: `gh api -X GET pulls/111`: closed, merged, squash `dd0ce36dc1083266bf89c55d9ddab4aa9efb4c85`, parent `93e1cab5`, merged 2026-10-24T22:10:58Z (09:10:58 AEDT), head `0c275f48`, 3 files +193 -3, 2 commits; `git/ref/heads/main` = `dd0ce36d`; open PRs: #110 only (head `650ddfb7`); squash check-runs 8 of 8 success; `compare e027ebd0...dd0ce36d` ahead 13 behind 0.
- Root: HEAD `823480a7`, branch main; `merge-base --is-ancestor` true; CLARIFICATIONS `numstat` empty (control BACKLOG prints `1261 0`); highest `### C-65` (count 1), no `### C-66` on any local branch; CLARIFICATIONS 1325 lines, last coordinator heading `:1277`; BACKLOG 2790 (last row `[B610-LANDED]` `:2785`); JIRA.md 262 (last `## B610` `:249`); history 1126; `records/b655`, `.tools/b655`, `.tools/.git-lock` absent (control `records/b610` lists).
- Jira (through `.tools/b610/j610.py` GET path, every JQL `project = MPSCALC AND ( ... )`): highest key MPSCALC-334 (`key > MPSCALC-334` 0; `created >= "2026-10-25"` lists 331-334); `labels = mpscalc-b655` 0 (control `mpscalc-b610` 4); `zzqxvbw` 0; `QA gate B354` 6; all 7 comment targets Backlog; counts -334 0, -329 1, -332 0, -290 1, -169 0, -288 0, -325 1; `stubApi.test.ts` 3 (-334, -313, -118), `figuresOmit` 0, `seenQuotes` 0, `B643` 0, `dd0ce36d` 0.
- Gate B643 read WHOLE (392 lines, sha256 `5dd4e9fe...4972`): line 1 `GO WITH FOLLOW-UPS round 1 of 2 @ 0c275f4`; findings `:331-340`; ROUND-CAP `:354-357`; survivors L5-L10, K2-K6, P2.
- Stray file: 63 bytes, sha256 `db16a0c38d07e96f5c0b40a9820bd989eddf0d5e5e6377523116923343c0874a`, content one `ALLDONE ...` line; destination `.tools/_quarantine/Datasec` absent (`ls` rc 1); `.tools/_quarantine` exists.
- Six cards read by exact `show` of six ids into scratch files (each file contained "Datasec", status ruled). Verification program: all 46 italic-quoted strings in the RULINGS block occur in the card text (one first name replaced by a role before comparing); control mutant not found. Card ids appear only in this report (kit scan: 0). Kit has 9 lines with the four-underscore pattern (8 slots + last line), 0 non-ASCII.

D-decisions (override at the stamp)
- D1. B643-8 (unpinned stub operations, part B parked with its load failure) goes into the MPSCALC-334 comment, not into the new ticket (334's BLUF already lists those operations); the new ticket carries B643-1..5 only. The sweep text put "-4 -5 -8" in the one ticket.
- D2. New ticket tier label `tier-2` (gate B643 is routing row G2, tests only). Lane label `lane-v1` copied from -334.
- D3. R6 becomes C-71 (a ruling of the product owner on this project's card), heading as a plain question; "Delivered" records the move. The B643 STATUS and evidence folder stay untracked (slot B643-COMMIT = no).
- D4. The move uses `mv -n` of exactly that path to `.tools/_quarantine/Datasec` (the path the sweep names, no rename); any mismatch of size/sha/content means move nothing, list under NOT DONE, do the rest.
- D5. The RULINGS block carries verbatim card text (no ids, no defaults) so the seat need not and may not query the store; stamp slot RULINGS-RELAY confirms it. R4's choice (a) differs from the card's recommendation (b); said in the kit.
- D6. No Jira text pastes the R2 sentence or the number 503 (B351 scan list); C-entries (files) do.

Questions for Tuesday (each with a default)
- Q-1. `model-routing.md` has no "records seat" row (grep of table rows found C7 line 97 "Sonnet drafts, posts only a body the coordinator approved byte for byte" as nearest). Default: Sonnet posts its own comments as B610 did (instruction given to me: Sonnet records). If you want C7 applied literally, the seat would draft and Tuesday approve each of 8 Jira bodies.
- Q-2. The gate's own FOR TUESDAY line (`:346`) says "tier 1" for the follow-up ticket; the sweep lane row and routing say G2 tier 2. Default `tier-2`.
- Q-3. Hard stop: kit suggests target 75 min, hard stop 2 h 30 min, 8 Jira writes.
- Q-4. Save a `.pre-stamp` copy beside the kit before stamping (REFUSE control reads it; I may write only two files). It should read 9 lines with the pattern.

UNMEASURED
- Jira descriptions/Acceptance of the 7 targets and neighbours (twin check is the seat's job); line numbers of the Where symbols at `dd0ce36d` (gate's are at `0c275f48`; the files are byte-equal to base per gate `:66`); whether `openapi.json:218` and `docs/API.md:274` read as the cards say at `dd0ce36d`; any MPS ruling after 09:57 (six exact ids only); whether any `b654*` ref exists yet (printed nothing at 10:5x); the helper contents of `.tools/b610/`; the squash message body beyond its subject.

Outside-the-fences disclosure
- I typed one `cd` in a Bash call; the hook refused it before running; nothing ran. I invoked `.tools/b610/j610.py` (the project's own read path, read-only, GET verbs enforced by its own assert) via importlib from a scratch script; token never printed. `decision_queue.sh show` was run six times (exact ids only, never `list`). I read B654's brief head (a Tuesday-owned file) for the fence paths. I read the sweep sections 0, 1, 3-MPS, 4 and 6. No git ref write, no Jira/GitHub write, no HTTP to any app host, no file written other than the kit, this report, and scratch files in the session scratchpad (card copies, a Jira GET script, a verification script).
