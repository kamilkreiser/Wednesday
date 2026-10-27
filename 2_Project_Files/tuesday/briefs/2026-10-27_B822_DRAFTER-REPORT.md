STARTABLE: YES

# B822 drafter report (Datasec / Security Composer, lane C-DATE, PCOMP-103, seat J26)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B822_SEAT-J26_composer-103-date-rule-closing-rows.md` (112 lines). Drafted 2026-10-27 13:0x AEDT.

## BLUF
One new branch `b822/composer-date-rule-closing-rows`, one commit on main `8df52332e52bf520633317120c563a16387d1a13` (the squash of #97), ONE path `apps/api/test/b626-date-rule-rows.db.test.ts`, additions only: four rows (`"-01-01"`, `"20272027-01-01"`, `"2027-0101-01"`, `"2027-01-0101"`) through the file's `expectDueDateRefused`. Sonnet (C2 line 92, L6 line 85), gate tier 2 (G2 line 109), "round 1 of 2" on the new PR per your 13:0x ruling CC1/CC2, a further NO GO on the class goes to you as a STOP. A 15-mutant battery (the 13 survivors plus the two equivalents QMq and QDq), old file against new file, plus regression (FLg, FLy, IX2full), controls c0-c3 and the whole apps/api db group before/after (+4 tests). Template shape: B806 kit. Launch line carries `BRIEF_SEAT_LEVEL=sonnet`.

## Facts re-measured (instrument; control)
- Main `8df52332e52bf520633317120c563a16387d1a13` by `git ls-remote` and `gh api commits/main` (message "Deploy guide: name every pin ..."), not the `422ecf37` the B806 kit used: #97 landed. `b822*` absent; control `b806*` prints `6f75c2d1...`.
- Blobs by `gh api contents --jq .sha` at main: the b626 test `9bc0a71e57c16fef365f00b8ce537736cc802007` (raw copy `git hash-object` equals it; 233 lines, 10815 bytes, 0 non-ASCII, 0 CR, 13 `it(` lines expanding to 30 rows by loops); `app.ts` `2c5d5ad12510091e285887dea263dd85fcbe8f7c`; `package.json` / `package-lock.json` the same as in the B806 kit. `DATE` pattern text count 1 in `app.ts` (control `zzz-no-such-string-7f3a` 0). Only commit on the test path: `8347f91b` (PR #92).
- PCOMP-103 read by `jira791.py` `get` (in-process credentials): Backlog, label `plan-comp-389`, 0 comments, description as the sweep quotes; control `PCOMP-999999` HTTP 404. Evidence files exist at `1_Project_Definition/Briefs/2026-10-25_B682_evidence/runs/` (`fix4-closing-rows.txt` 21 lines, `c3d-table.txt` 24, `raw-route-answers-group-quantifiers.txt` 15); `fix4` table copied into the kit as RELAYED (QMq/QDq 0 red; QDst oddity: `c3d-table.txt` marks it `killed-by-whole` FILE-LEVEL rc1 at the 1522-test level though 0 red/30 here; the kit makes the seat re-measure it).
- Open PRs #95, #91, #86, #85: 0 shared paths each with the test path or `app.ts`; control (#95's `apps/api/test/b712-setup-target-locked.db.test.ts`) 1. Branches b6*/b7*/b8* not compared at branch level (the seat does it, STEP "PRIOR-WORK CHECK").
- Ports 7630-7639: `lsof` printed nothing (rc 1); control: a `python3 -I` listener on 7639 counted 1, then freed. Word-scan `763[0-9]` over non-`.pre-` 26/27 Oct SEAT kits: 0 hits; control `892[0-9]` printed 2. Seat name `J26`: 0 kits; control `J25` 9. Panes at 13:04: `%0 tuesday`, `%65 Datasec/Security-Composer-R62`, `%63 Datasec/HPSM-POC-D38`, `%62 Datasec/NexusAI-M21`, `%1 fleet-monitor` (no J26). `.tools/b822` and `wt-b822-base` absent; control `.tools/b781` lists. `core.sshCommand` is the Composer deploy key (path elided). Load1 8.39 at 13:04 (so the seat will wait).
- Runner: `.tools/b781/scripts/dbone.sh` runs the packages/db config; the API-db shape is `.tools/b615/scripts/dbone.sh` (config `apps/api/vitest.db.config.ts`, mounts packages and apps). The kit has the seat write `apione.sh` from that. `b781/scripts/names.py` is already the apps/api names program with `NEW = 'api/test/b626-date-rule-rows.db.test.ts'` (earlier date-rule lane), read by the kit as a copy source. `scripts/test-db.sh` and `ci.sh:117-118` at main read: the db step passes only if both vitest runs exit 0.
- Model row text of C2/L6/G1/G2/G-cap printed by `sed -n` of `model-routing.md`; `claude-sonnet-5-5` at `models_latest.json` lines 23 and 38; `brief_seat.sh:24` defaults to Opus. Stamp slots: 9 lines with the four-underscore pattern; 0 non-ASCII bytes; 0 hits for the owner's name.

## D-decisions (mine, for you to accept or strike)
- D1: One file, additions only, as the ticket's first fix shape ("append the four rows"), not a new file. Reason: the helper `expectDueDateRefused` is file-local (not exported), so a new file would copy it.
- D2: A 15-mutant battery with the 2 equivalents (QMq, QDq) as expected-green controls, plus FLg/FLy/IX2full regression, run old file against new file in ONE vitest invocation per mutant (the new file is copied into the mutation tree under a scratch name, never committed), so "the new rows alone kill them" is measured. Property (6): the new red set is a superset of the old.
- D3: The whole `apps/api` db group runs before and after (names lost 0, added 4) because the CI db step requires every file of the group to pass; `packages/db` is not re-run (no byte there).
- D4: The mutation loop may run inside one container's own `/repo` layer so the host trees stay clean; the kit states the property (no host file of the fix tree is mutated) rather than the mechanism.
- D5: Hard-stop suggestion 2 h target / 3.5 h hard stop (smaller than B806's 2.5/4 h).
- D6: Commit message and added lines carry no Jira key, no B-number, no name (same rule as B806).

## Q-questions for Tuesday (each with a default)
- Q1: Accept one file, additions only (D1)? Default: yes.
- Q2: Accept the whole apps/api group run (before and after) given load1 8.39 now? Default: yes; the seat's heavy gate waits for load1 < 7, with a 5400 s give-up in `heavy.sh`.
- Q3: Should the seat also re-run the 82-row neighbour file and the 164-row contract file against the 13 (the ticket relays them as survivors there)? Default: no; the whole-group run covers their green at main, and the kit lists them under NOT TESTED for the mutants.
- Q4: The ticket's note on separator and digit-class variants (`[-_]`, `([\d_]{4})`) is out of lane and listed under FOR TUESDAY. Default: leave it for a card or a later ticket.
- Q5: Stamp clocks and gauge: yours.

## UNMEASURED
No vitest, container, image build or mutant: whether the four rows pass at main's product and kill the 13 on the named rows at `8df52332` (RELAYED from the PR #92 head measurement); whether `apps` mounted read-only over `/repo` runs the apps/api suite at this base (b615 did, earlier); the group count at main; the QDst oddity; battery wall time; the 82/164-row files against the 13; branch-level compares of b6*/b7*/b8*.

## Outside the fences
None known. Writes: the kit and this report only (scratch files only in the session scratchpad: a Jira reader script, raw copies of the test, `app.ts`, `harness.ts`, `ci.sh`, `test-db.sh`, the vitest config, the Dockerfile). Reads: drafter rules, wave-1 commission, 1300 sweep, B806 kit and report, `model-routing.md`, `models_latest.json`, `brief_seat.sh:24`, `.tools/b781/scripts/*` and `.tools/b615/scripts/dbone.sh`, the three evidence files, `jira791.py` imported by a scratchpad script for two issue GETs (PCOMP-103 and the 404 control), no write call. `gh api -X GET` only (contents, pulls, pulls/files, commits, branches). `tmux list-panes`, `lsof` (a transient local listener on 7639, freed), `uptime`, `date`. A listing of `.tools/` for existing b8xx trees (read). One shell command was refused by the no-`cd` hook (my first call contained a `cd`); one by the zsh `=` hook (a separator line); both re-issued fixed; no effect on state.

READ-WHOLE-BY-TUESDAY: ____
