STARTABLE: YES

# B1010 drafter report (SEAT-G249, HPSM-POC round-2 tier-2 gate)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1010_SEAT-G249_hpsmpoc-keep-awake-round2-gate-tier2.md` (37 lines; 8 stamp lines read by `grep -c -E '_''_''_''_'`, 0 non-ASCII by `LC_ALL=C grep -c '[^ -~]'`, 0 `@X@` tokens). Shape copied from B1003; cut to six checks.

## BLUF
Startable now. Gate row G2 (routing line 109), cap row G-cap (line 111), Sonnet `claude-sonnet-5-5` (models_latest.json line 23), `BRIEF_SEAT_LEVEL=sonnet` inside the quotes. Round 2 of 2: a NO GO goes to the product owner.

## Facts re-measured (instrument, control, frame)
- `git ls-remote origin` branch `refs/heads/b999/hpsmpoc-uat-db-keep-awake-template` = `2b8829468e90cf2990c0d165a1176bbb7a2d1016`; main = `e0b939571ca969933ad80b6579da4948f5d59948`; `refs/heads/b1010*` printed nothing (control: the `b999*` pattern printed the branch line).
- `gh api -X GET compare 930cb5b5...2b882946`: ahead 1, behind 0, `infra/env/uat.bicepparam +1 -1`, `infra/tests/test_security_baseline.py +18 -0`; `grep -c -E '^infra/|ci\.yml'` on its file list = 2 (control: the pattern matches both paths). `compare 930cb5b5...main`: diverged, 2 ahead, 1 behind, 12 files, 0 matching `^infra/|ci\.yml`.
- PRs for the branch (state all) 0; open PRs: none printed.
- Commit message via the API: true to B1008's STATUS, ASCII, no B-number or person; author fields 0 non-ASCII. `git grep -c -i B1003` in the test file at head = 0, control `B175` = 11.
- Head test file by `git grep -n`: `pause_delay` anchor line 1057, `rule_env_params` anchor line 2289, the 2542 row, the new row at 2713. `AUTO_PAUSE_EXPRESSION` 7 hits at 930cb5b5, 9 at head; `not one literal number` 3 at 930cb5b5, 5 at head (`git grep -c -F`; no zero-control needed, counts are non-zero).
- uat.bicepparam head lines 17-26 read: line 21 carries the new measured words; `sqlUseFreeLimit = false` and `sqlAutoPauseDelay = -1` still present; line 24 says "about A$323 a month" (322.84 rounded; Note).
- B991 STATUS lines (grep -n -i family, positive hits): 23 (12 web 5xx, 10 s), 57 (`UPSTREAM_TIMEOUT_MS = 10_000`), 139 (resume 30.0 s or 60.0 s).
- Absent before launch: `.tools/b1010` and `.tools/wt-b1010*` (`ls -d`, no such file); no file in `briefs/` names G249 or B1010 (count 0 before writing). Panes (tmux `@cockpit_name`): `tuesday`, `Datasec/MPS-G248`, `Datasec/HPSM-POC-R101`; no G249. Ports: the gate binds none (no lsof run needed; none claimed).
- Present: `.tools/bicep/bicep`, `.tools/b198/lock.sh`, `.tools/b267/waitload.sh`, `launch_when_cool.sh`, the B1003 evidence folder with `pr-title.txt` and `pr-body.txt` (shape source).

## D-decisions
- D1: kit CARRIES round 1's cost figures, Learn quotes, 12-plant table and compile result by line citation (no network at all this round), per the commission; only "no infra/ci.yml path moved on main" is re-measured.
- D2: plants are exactly P0, M11a, M11b, M13 (the builder's four, run by the gate itself) plus at most ONE extra the gate may devise for a delay shape the new row misses (the commission's "second loosening").
- D3: the pass predicate is "begins `== validate: OK`" because the real last line carries `(artefacts in <tmp dir>)` (B1008 STATUS line 35; B1003 line 24).
- D4: squash text replaces the B1003-3/-4 sentences; "A$" mixing removed (AUD throughout). The gate verifies each "the others are red under plants" claim against the table before writing it.
- D5: ORIGINAL STAMP SLOTS are all four underscores; no typed clock anywhere.
- D6: expected net numstat for the squash (round 1 +160 -11 plus this commit) is left for the gate to PRINT from `compare <merge-base>...2b882946`; I did not state a number, because line 21 was changed in commit 1 and again in commit 2, so net is not a simple sum.

## Q-questions for Tuesday
- Q-1: Should the extra plant (D2) stay at "at most 1"? Default: yes, 1.
- Q-2: Should the gate also run `validate.sh` at the pin (930cb5b5), not only at head? Default: no; round 1 already has Ran 320 rc 0 at that head, and the names diff uses -v whole-file runs at pin and head.
- Q-3: The squash/PR texts omit the attribution line (Tuesday appends). Default: as written.

## UNMEASURED
Test results of the new row and every plant (nobody on the gate side has run them; the builder's are claims). The compiled byte-equality (builder's claim). shellcheck (absent locally). Hosted CI and CodeQL (no PR). Azure acceptance in place.

## Outside the fences
None. Read only: DRAFTER_RULES, B1003 kit and STATUS, B1008 brief and STATUS, B991 STATUS (three grep lines), routing and models files, B1003 evidence pr-title/pr-body, git read verbs (`ls-remote`, `grep`, `log`, `show`, `cat-file`) on `2_Project_Files`, `gh api -X GET` under the project config dir. No decision queue, no staged briefs, no scoreboard, no ledger, no HP Reporting and Docs/, SOW, Source_Documents/ or inbound/. No fetch, no az, no HTTP to any site.
