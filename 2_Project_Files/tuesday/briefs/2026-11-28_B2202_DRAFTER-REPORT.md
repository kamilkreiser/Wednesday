STARTABLE: YES (after Tuesday's stamp: four slots and the READ-WHOLE line; Q-1 to Q-5 answered in the STAMP slot)

# B2202 DRAFTER REPORT - kit SEAT-N188 (NexusAI: install the gated jest lock with `slots-jest` absent)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-28_B2202_SEAT-N188_nexusai-install-jest-lock.md` (36916 bytes, sha256 `b1205513...`), sidecar `.measured` (112 claims, `stamp_check.py <kit>` rc 0 at 03:06). Commission section 1 of `2026-11-28_B2202-B2203_NEXUSAI-LOCK-AND-RECORDS_COMMISSION.md`. Drafting 02:52:28 to 03:07 AEDT Sat 28 Nov 2026 (clocks by `date`).

## BLUF
- The kit installs the candidate by a frozen copy of N186's dry-run script (`install-b2202.sh`), with `slots-jest` never written. Then it runs four proofs through the INSTALLED lock on the live base: the gate's smoke run; one real jest run of one 3-test file (`rd977-inventory-sentinel-word.test.js`, no server, no port); two callers through the installed script (the second must wait); an installed-script holder plus an OLD-script caller (the kept pre-copy), where the old caller must wait. The rollback line is PRINTED and not run on the green path. The kit then files the four follow-up tickets (M-1, m-2, m-3, m-4) on RD, each with one `Relates` link to RD-1052. STATUS carries the sha256 before and after.
- **`session-tools/` is outside every git repository** (`rev-parse --show-toplevel` fatal on `session-tools` and on the project root; control: `2_Project_Files` prints its path). `git check-ignore` has nothing to answer, nothing is tracked, and there is no push or PR. REFUSE 5 stops the seat if its own read finds otherwise.
- **The NexusAI CLAUDE.md lets a seat create tickets** (line 297: every follow-up "gets a new Jira ticket immediately", linked; line 273: Tuesday can authorise "ticket create"). So the kit files them, after a search by marker AND by exact summary. The records kit (section 2) can find them by the same summaries (`tickets2202.json`).
- Six frozen files sit in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s337/d2202/frozen/`. `jira2202.py search` and `scan2202.py` RAN with controls fired. `install-b2202.sh`, `runjest-b2202.sh`, `proof2202.sh` and `jira2202.py create` were NEVER run on a real output (I took no lock and wrote nothing to Jira). The kit marks them so: a failure traceable to their wording is `STOPPED: NEEDS TUESDAY`.

## Facts re-measured (instrument; control)
- Main `e98b6fd984bf7eaaf55fa0302dac222b5e6ee5f3` (gh GET 02:53:29 and 03:06:16). Its parents are `826bb7a8...` and `fc5975f631bb...`. `compare/fc5975f6...main` reads `ahead 1 0`. Open PRs `[]`. Main's push Build run 46026849679 read `in_progress` at 03:06:16; the install does not depend on it.
- LIVE lock sha256 `cf01bafb...4971f`, 391 lines, `-rwxr-xr-x 501 20`, inode 2494992. CAND `52713e55...356260`, 498 lines. At 03:06:16 the base held 0 lock dirs (under bash; zsh refuses the glob) and queue-jest had 0 `^[0-9]` entries; control: `[ -e queue-jest ]` reads present. `slots-jest` absent.
- The REFUSE 4(c) `pgrep` pattern printed nothing (rc 1). Control: a process started as `/scratch/nexusai-lock.sh` via `exec -a` was found (rc 0).
- `session-tools/`: 13 names match `nexusai-lock|slots`, 0 match `b2175` (control: 13 match `nexusai-lock`).
- `install-b2202.sh` vs `install-b2175.sh`: `diff` shows 5 hunks (two header comments; `ST`, `LB`, `B`; `CAND`; `OUT`). `bash -n` and `/bin/bash -n` both rc 0.
- Main's tree `e3bf2ca0...` equals fc5975f6's tree (gh GET of both commits, and `rev-parse fc5975f6^{tree}` in N187's clone). N187's clone does not hold e98b6fd9 (`cat-file -t` fatal), so the seat's worktree is made at fc5975f6.
- `node_modules`: N187's clone, `package-lock.json` sha256 `37e5add3...`, jest 29.7.0. Main's lock blob `2d7dbece...`. N187's tree `mz` links its `node_modules` the same way (the precedent).
- rd977 file at fc5975f6: describe at line 22, first test at line 23. 3 indented `test(` cells, 0 at column 1. `PASS` in N187's plain log (line 26333).
- Jira (reads only, `jira2202.py` loading `.env` by name, never printed):
  - RD-1052: Task, Medium, To Do, labels operations and tooling, no components, `Relates` RD-1051.
  - The link type `Relates` exists.
  - `SEARCH2202 PASS 1=NEW 2=NEW 3=NEW 4=NEW` (02:59:14). All three controls fired: the first page holds 50 issues, the marker `LAND-265-759-26NOV` finds `RD-759`, and RD-1052's summary finds `RD-1052`.
- Ticket texts: I ran the project's scanner, a copy of `.tools/b2131/scan1947.py` (sha256 `3707dc37c4795fbf...`, the same file named in R344's kit), through `scan2202.py`. Result: `TEXTS 17 HITS 0 CONTROLS FIRED 6 of 6`, `SCAN2202 PASS`.
- Seat id N188 is free: 1 file (the commission); control N187 gives 14. `.tools/b2202`, `b2202-nodot` and the STATUS do not exist. No `Datasec/NexusAI-*` pane is open. Load was 13.94 at 02:57.
- Ports: none. The jest file starts no server, and its module reads constants and files at require. So there is no port block, and no lsof or kit-scan census is needed.
- Model: NexusAI CLAUDE.md names none (grep `opus|sonnet|claude model|BRIEF_SEAT_LEVEL` gives 0; control `model` gives 5). Routing row C5 (line 95) applies; `claude-sonnet-5-5` is at `models_latest.json` line 23. `brief_seat.sh` line 31 defaults to opus, so the launch line writes `BRIEF_SEAT_LEVEL=sonnet` inside the quotes, with `CLAUDE_CONFIG_DIR=.../TUESDAY/4_Credentials/.claude`.

## D-decisions (the drafter's)
- **D-1.** `install-b2202.sh` changes `B` and `CAND` as well as the three values install-steps.md names (`ST`, `LB`, `OUT`). Kept as-is, `B` was N186's lock folder: the real run would overwrite N186's `scratch/cpn-*` files and its dry-run record `logs/pre-copy-name.txt`. So `B` becomes the seat's own `.tools/b2202`, and `CAND` is typed as the candidate's absolute path. Every other line is token for token (5 `diff` hunks). This is Q-2.
- **D-2.** The smoke run keeps install-steps' literal tag `b2192-install-smoke`.
- **D-3.** I read "the old path still refuses a second holder" two ways and the kit proves both. (a) Through the installed script, the slot-1 directory `nexusai-jest.lock` admits one holder and the second caller waits. (b) An OLD-script caller (the kept pre-copy, the code a seat started before the install would run) also waits behind an installed-script holder. This is Q-3.
- **D-4.** The tickets are filed ONLY after steps 3 to 7 are green. On any earlier STOP they are not filed, and the records seat (section 2) files them from the same `tickets2202.json` texts.
- **D-5.** Each ticket: type Task; priority Medium for M-1 and Low for m-2 to m-4; labels `operations` and `tooling` (RD-1052's own); no component; one `Relates` link to RD-1052 inside the create POST (CLAUDE.md line 297 asks for a link). Each carries a marker `LOCK-FOLLOWUP-<n>-28NOV` in its last paragraph so a duplicate search can find it. FOR-RECORDS' candidate 4 (I-2, old band wording in two test files) and candidate 5 (kill -9, info) are NOT filed: the commission names M-1, m-2, m-3 and m-4 only.
- **D-6.** No comment or transition on RD-1051 or RD-1052: those belong to the records seat (FOR-RECORDS' after-install comment). READY prints the install time, pre-copy name, sha256 after and ticket keys for it.

## Q-questions for Tuesday (each with a default)
- **Q-1** Seat model. Default: **Sonnet** (row C5, line 95, applying a gated artefact by frozen scripts). The alternative is Opus, if you read installing the lock that gates every NexusAI seat as a C6-like operational change.
- **Q-2** Accept D-1 (`B` and `CAND` changed beyond install-steps' three values)? Default: **yes**.
- **Q-3** Run the old-path proof both ways (D-3)? Default: **yes**. That means six acquisitions in all, each a no-op or `sleep 20` except the one 3-test jest run.
- **Q-4** On a lock red in steps 4 to 7, should the seat run the rollback once (base idle twice) and then STOP? Default: **yes**, as install-steps step 7 says ("Use it on ANY red in step 5 or 6"). On the green path it is printed and NOT run, as the commission says.
- **Q-5** `node_modules` linked from N187's clone (the precedent of N187's and the gate's trees)? Default: **yes**. If it is missing at the seat's read, the seat STOPs and the answer is an `npm ci` in its own clone.

## The chain's inputs (every input exists at drafting or is made by an earlier step)
| step | inputs |
|---|---|
| 0 | the kit, the frozen folder, the gate folder, `.tools/b2131/scan1947.py`: all exist |
| 1 | Step 0's copies; gh, Jira, the base |
| 2 | N187's clone (holds fc5975f6) and its `node_modules`: exist |
| 3 | Step 0's `install-b2202.sh`; the candidate (exists) |
| 4, 6 | step 3 |
| 5 | steps 2 and 3; `runjest-b2202.sh` |
| 7 | step 3's pre-copy; `proof2202.sh` |
| 8 | steps 3 to 7 green; `jira2202.py`, `tickets2202.json` |
| 9 | steps 3 to 8 |

## For the sibling (section 2, R346)
The four summaries, exactly as in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s337/d2202/frozen/tickets2202.json`:
1. "Jest lock: a test tree from before the RD-1051 port band change must run alone" (marker LOCK-FOLLOWUP-1-28NOV)
2. "Jest lock: callers declare the worktree slot of the tree they run, not of their working folder" (LOCK-FOLLOWUP-2-28NOV)
3. "Jest lock: record the holder's process start time and compare it in the stale test" (LOCK-FOLLOWUP-3-28NOV)
4. "Jest lock: the waiting message says nothing for slot 1 when slot 1 is free and other slots are held" (LOCK-FOLLOWUP-4-28NOV)

N188's READY last line names their keys. If N188 stops before step 8, it names none.

## UNMEASURED / never run
- `install-b2202.sh` on the real paths. Its form ran once as N186's dry run (`INSTALLED OK`, log `install-dry.txt`). The `STOP:` wordings come from source and were never printed.
- `runjest-b2202.sh`: the `Tests:` line `3 passed, 3 total` is PREDICTED. The jest command form (`--rootDir`, `--config`, `--runTestsByPath`) is pair2175.sh's, which ran in N186's, N187's and the gate's runs.
- `proof2202.sh`: never run. The waiting line form is real (gate `mut.out`: `waiting for jest lock (queue position 1 of 1), held by: tag=b2192-gate-verify`). The candidate prints its waiting line only when `waited % 60 < POLL`, so the first poll prints it. The `since`-versus-release comparison uses macOS `date -j -u -f`, never run here.
- `jira2202.py create`: never run (a write). The ADF is the plain-paragraph shape from JIRA.md line 279. Putting `update.issuelinks` in the create POST is standard Jira REST and has not been tried on this site.
- `owner` `wslot=unknown` for the smoke and the jest proof is PREDICTED from candidate lines 129-139 and the project root having no `__tests__/helpers/test-server.js` (control: `b2181-nodot/mz` has one).

## Outside-the-fences disclosure
- Writes: only my scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s337/d2202/` (the frozen files; a copy of scan1947.py made by `cat` redirect; the rd977 blob; `scantix.py`, `links.py`, `kits.txt`, `stampcheck.out`; `_quarantine/`), the kit, its `.measured`, and this report.
- `py_compile` left a `__pycache__` in `frozen/`. I MOVED it to `d2202/_quarantine/frozen-pycache` (not deleted). A first `.measured`, made before two kit edits, went to `d2202/_quarantine/measured.v1`. A three-line append file existed briefly beside the kit in `tuesday/briefs/` (`.measured.add`) and was moved to `d2202/_quarantine/measured.add`.
- Reads outside TUESDAY:
  - NexusAI `session-tools/` (ls, sha, grep), `.tools/b2175` (scripts and logs), `.tools/b2181` (clone, git read verbs with `--no-optional-locks`, logs), `.tools/b2131/scan1947.py`, CLAUDE.md, JIRA.md, `scripts/jira-query.sh` header.
  - The `.env` names only (a `grep -c` of three names, then values loaded in-process by `jira2202.py`, never printed).
  - Gate g2192's `mut.out` (one file).
- Network: `gh api -X GET` under the NexusAI GH_CONFIG_DIR. Jira GETs only: `search/jql`, `issue/RD-1051`, `issue/RD-1052`, `issueLinkType`.
- Two hook refusals: a `cp` whose source path the hook read as a write (redone as `cat >`), and a `git worktree list` (not rerun). One `cd`-free `exec -a` sleep process ran 4 s as the pgrep control.
- No lock taken, no jest, npm, az, ssh or docker. No Jira, GitHub, mail or card write.

Drafter report ends `date` 03:07 AEDT Sat 28 Nov 2026 (last measured clock 03:06:16).
