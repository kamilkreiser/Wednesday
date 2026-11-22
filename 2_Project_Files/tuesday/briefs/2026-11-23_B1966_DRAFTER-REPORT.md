STARTABLE: YES

# B1966 DRAFTER REPORT (Sonnet, in-session, read-only) -- NexusAI lane NX-SR, kit `2026-11-23_B1966_SEAT-N165_nexusai-signal-read-race.md`

Drafted 2026-11-23 from 09:06 to 09:36 +1100 (clocks printed by `date`: start 09:05:57, kit built 09:35:04, last check 09:35:47). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1966_SEAT-N165_nexusai-signal-read-race.md` (68524 bytes, 382 lines, sha256 `3ad8f2cf8660`), sidecar `.measured` (103 claim lines, sha256 `c67586c347f7`); `stamp_check.py <kit>` exits 0 (103 claims, 103 measured). The unstamped kit holds exactly 5 lines with the four-underscore pattern (4 slots + the last line; `grep -c` printed 5). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s314/d1966/`.

## BLUF
- STARTABLE: YES. Nobody is live on NexusAI code (jest FIFO `queue-jest` empty, no jest or server process, the only tmux pane is `tuesday`, B1958 reads `READY B1958`); main is still `3c3be156e8ea36ad297fdadd3055c6e00252ba38`; `b1966/*` absent at origin; PR 242 is open and shares no path.
- **The lane: test-side only, ONE commit, two files, +8/-2 each, the preload unchanged, the counts file unchanged (6235 / 394 predicted).** Both readers (`rd711...test.js:68-69`, `rd615...test.js:87-88`) wait for "the file parses" (a throwing read is polled again inside the test's existing bound). By program there is no third reader (3 files name the preload or its variable: 2 readers + the writer; control fired).
- **Red-first without a seam in the preload, measured:** a SCRATCH-only planted writer (create empty, hold 700 ms, write) makes rd711 at BASE 4 of 4 red with the hosted failure's own signature (`SyntaxError: Unexpected end of JSON input` at `rd711...:69:42`) and rd615 at BASE 4 of 4 red (`:88:55`); with the lane's readers both are green (8 of 8) under the same writer and 8 of 8 green with the real preload. Mutants M1 (both reverted) 8 red, M2 (rd711 only) 4 red, M3 (rd615 only) 4 red, M4 (a writer that never writes: bounded, no hang) rd615 4 red in 36 s, rd711 2 red in 137 s.
- Precedent found: `__tests__/helpers/rd525-live-store.js:121-123` already does poll + `try { JSON.parse(readFileSync) } catch (_e) { /* retry */ }` for the purge-result file; the lane adopts it (catch binding `_e`).
- **Deploy demo:** `__tests__/**` is NOT in `deploy-demo.yml`'s path-ignore (lines 29-32 ignore `**.md`, `docs/**`, `tests/**`), so a landing starts a Deploy demo run; both jobs are gated on `vars.CI_DEPLOY_ENABLED` and the last four runs on main read `skipped` (ids in the sidecar). It must read `skipped`.

## Facts re-measured with instruments (each has a sidecar line or a scratch file)
| fact | instrument | printed | control |
|---|---|---|---|
| main sha | `gh api -X GET git/ref/heads/main` | `3c3be156...` | compare BASE...main files 0 |
| readers | `readers1966.py` over the BASE tarball | frame 502; 3 files; rd615 read 87,88; rd711 read 68,69; preload write 28 | planted reader in a copy: frame 503, 4 files |
| the race (amplified probe, 2000 files) | `probe1966.js` | old reader: 11 and 14 escaping empty reads; new reader: 0 escaping, 27 empty-or-partial swallowed; atomic writer + old reader: 0 | `swallowedEmptyOrPartial` > 0 shows the window was hit |
| red at BASE under the planted writer | jest 29.7.0, Node v24.22.2, `proto_a` | rd711 4 red (65 s) at `:69:42`; rd615 4 red at `:88:55` | the unplanted BASE rd615: 4 green (14.3 s) |
| green with the lane's readers | `proto_b` | planted: rd711 4 green (69.6 s), rd615 4 green (15.9 s); real preload: 8 of 8 (68 s) | same trees, readers reverted: red |
| mutants | `apply1966.py <tree> revert|revert711|revert615`, writer `slow` or `never` | M1 8 red; M2 rd711 4 red / rd615 4 green; M3 rd615 4 red / rd711 4 green; M4 rd615 4 red, rd711 CTRL and TWO-SIGNAL red, INTERVAL and SOURCE green | the reverted files are byte-equal to BASE (sha256 compared) |
| cell tallies | `tally1966.py` over `raw/*.json` | 13 files, every cell total equals `numTotalTests` | the program's own check |
| blobs | `git hash-object` vs GitHub tree sha | rd711 `023b8f976867`, rd615 `438fcc38f087`, preload `a686b1053313`, counts `32146fe9377e` equal; patched rd711 `931e7fa69b30`, rd615 `180acd015d22` | tarball control equal |
| counts | json of `scripts/verify-expected-counts.json` | tests 6235, suites 394 | not in this lane's paths |
| code scanning | `gh api -X GET code-scanning/alerts?state=open` | 22; 0 under `__tests__/`; `backend/server.js` 13 | the 13 |
| Deploy demo | `gh api -X GET workflows/deploy-demo.yml/runs?branch=main&per_page=4` | 4 runs, all `skipped` | the records merge `3c3be156` created no run |
| static scans on the commit | `.tools/b1958/namescan.py` (run in place, project's own) and `scan1966.py` (drafter's list) over a scratch repo | names 0 (every control fired), B-numbers 0, card ids 0, owner attribution 0, ticket key 0, timers 0, RegExp/eval 0, `existsSync` added 0 (removed 3), non-ASCII 0, bidi 0, plain ASCII; `node --check` rc 0 x2; gitleaks no leaks | gitleaks planted non-EXAMPLE AKIA shape fired (1); the AWS-docs `EXAMPLE` keys did NOT fire (allow-listed): the kit says so |
| kit blocks | `extract_check1966.py` | the five FILE blocks equal their sources (cmp by program); the kit's `apply1966.py` run on fresh BASE copies makes the two patched blobs | an `apply` on a half-reverted tree asserts and writes nothing (blobs unchanged) |

## D-decisions (the drafter's, for Tuesday to overrule)
- D1: the fix is test-side in both readers (the commission's lane); no atomic write in the preload (it would touch the product owner's 2026-11-16 answer quoted in rd711's header); recorded as an option not taken in the new-ticket text.
- D2: both readers swallow every read error (missing file and parse error alike) and poll inside the existing bound (rd711 `waitMs`, rd615 15 s); no new bound, no test retry. M4 proves the bound holds.
- D3: ONE commit A (no K): the counts file does not move, so no `--update-counts`; the plain verify at A must read 6235 / 394 (HOLD 46: any other pair is a STOP).
- D4: builder Sonnet by row C2 (line 92, `model-routing.md`), gate G2 (line 109), Sonnet, model id `claude-sonnet-5-5`.
- D5: the planted writer lives only in the seat's `mut4` tree (saved original, planted, copied back, blob `a686b1053313` proved after); `wt` and `chk11` never carry it; nothing of it is committed.
- D6: no ticket key in the commit message (the ticket is owed to the records pass after the landing; its text is in the kit).
- D7: trees `b1966-nodot/{work4,mut4,chk11}` all slot 17 by the harness rule (computed; controls `b1958-nodot/work4` and `b1931-nodot/new5` read 17); `wt` slot 13 (no jest).
- D8: HOLD 20 lets PR 242's four paths move (the counts file included) without a STOP; a move into the two owned files, the preload or the two helpers is a STOP.

## Q-questions for Tuesday (each with a default; the kit's STAMP slot cites Q-1 to Q-7)
- Q-1: test-side fix, preload untouched? Default YES.
- Q-2: one commit, no counts change? Default YES.
- Q-3: builder Sonnet (C2), gate G2 Sonnet? Default YES.
- Q-4: no ticket key in the commit text? Default YES (ticket after the landing by the records pass).
- Q-5: the planted-writer plants in the seat's scratch tree `mut4` (the preload file temporarily changed there, copied back, blob proved) acceptable? Default YES; the alternative is a scratch copy of the whole tree outside `b1966-nodot`, which loses the slot-17 band.
- Q-6: after this lands, PR 242's merge ref is rebuilt on the new main; a re-run of 242's hosted build is Tuesday's step (the diagnosis calls a re-run alone a weak measurement). Default: re-run after the landing, not before.
- Q-7: HARD STOP clock: predicted need about 40 min reading/census/tools + about 15 min of runs + one verify (about 23 min by B1958's measurement, up to 60 loaded) + CQ + push: about 1h45 to 2h30. Default: a window of 2h30.

## PRIOR WORK CHECK (done)
Jira GET (all `project = RD AND ( ... )`): no ticket names this race (`rd711` 0, `RD615_SIGNAL_FILE` 0, the preload name 0, `"Unexpected end of JSON input"` 1 = RD-203, unrelated; `slow-step` 6 unrelated); controls `key = RD-711`, `RD-615`, `RD-911` 1 each, nonsense word 0. Neighbours, not duplicates: RD-787 (Testing; CodeQL `js/file-system-race` x14 in test code; its fix pattern "read once, treat ENOENT as absent" is this lane's shape; body and 2 comments do not name rd711 or rd615), RD-911, RD-740, RD-867. Git: rd711 test one commit `a63d7f23` (RD-711 RD-806, the second server-security slice, kit B1603; its independent review names neither `existsSync` nor the signal file: 0 hits, control `Counts` 2); rd615 test and preload `5f99fcb1`, `c60a00de` (RD-615). RD-711 Testing, RD-615 Release Ready.

## Seat read load in bytes (PREDICTED sum, each part measured by `wc -c`)
Kit 68524; this report about 9000; the B1965 diagnosis 10436; B1958 STATUS parts (lines 37-47 and 113 to end) 5578; B1958 kit parts (lines 200-213 and 235-272) 18499; B1771 kit parts (lines 568-589 and 630-651) 19966; codeql README + GATE_STEP 5479; the twelve main tools of `.tools/b1958/` 52861 (plus about 15 KB of smaller ones). About 190 KB, about 48K tokens of reading.

## Sources (every row hashed; sha256 first 12 unless a git blob)
| source | bytes | hash |
|---|---|---|
| `2026-11-23_B1966_NEXUSAI-SIGNAL-READ-RACE_DRAFTER_COMMISSION.md` | 5985 | `ded87fe930c7` |
| `2026-11-23_B1965_DIAGNOSIS.md` | 10436 | `7027bb7f1b22` |
| `DRAFTER_RULES.md` | 17216 | `1c51fc0f10a7` |
| `2026-11-23_B1958_SEAT-N164_nexusai-nx-p-permission-table.md` | 75340 | `28e030c2ade4` |
| `2026-11-23_B1958-B1959_NXP-CT_DRAFTER_COMMISSION.md` | - | `8d6b55e770af` |
| `2026-11-23_B1958_STATUS.md` (project Briefs) | 20137 | `3a7c420e1083` |
| `2026-11-20_B1771_SEAT-N161_nexusai-lane-nm-chat-error-text.md` | - | `19f12eab9ec9` |
| `2026-11-16_B1603_verify/VERDICT.md` | - | `1540724c0495` |
| `fleet/specs/model-routing.md` | 27514 | `5ccdffdf183e` |
| `0_Brain/dashboard/data/models_latest.json` | - | `b5f3c04bd8fb` |
| `tuesday/tools/stamp_check.py` | - | `00df367b64f4` |
| BASE tarball `d1966/base.tgz` (gh api tarball of `3c3be156`) | - | `22227332682f` |
| `1_Project_Definition/CLARIFICATIONS.md` (read only `awk NR==2062,2067`) | 891 KB class | `5dcff34112ef` |
| `rd711diag/jira_search.py`, `rd711diag/race_probe.js` (B1965 scratch, read) | - | `b10b5a881094`, `3bee7f813d25` |
| blobs at BASE: rd711 test, rd615 test, preload, counts file, deploy-demo.yml, `rd525-live-store.js` | 7138, 7277, 1926, 496, -, 9933 | `023b8f976867`, `438fcc38f087`, `a686b1053313`, `32146fe9377e`, `597b3487c59e`, `33497a38b2b7` |
| `package-lock.json` at BASE | - | `37e5add354e5` (equals the B1958 kit's value) |
| Jira: RD-711, RD-615, RD-911, RD-787 and the searches (GET) | - | no file; the issue keys and counts are in the kit and sidecar |
| frozen files in the kit | 3719, 1493, 1414, 2467, 897 | `701e5e3e9ffd` (apply1966.py), `5f0a9269aea4` (plantwriter1966.py), `2d96358fdcd4` (readers1966.py), `c25398b7270a` (probe1966.js), `f7673af154ed` (msg-A.txt) |

## Transitions the kit asks (chain table, each step's inputs made earlier or at BASE)
Step 0 inputs: BASE (Step 1). Step 1: BASE + frozen programs (saved preload copy made inside the step). Step 2: step 0's tree + `apply1966.py`. Step 3: step 1's tree (planted writer) + `apply1966.py` modes. Step 4: BASE + frozen programs + step 2's blobs. Step 5: Step 1's clone. Step 6: A (step 4). Step 7: Step 1's clone. No step needs a file a later step makes.

## STOP-severity checks run on my prototype (PASS, control fired) and checks never run
Run on a scratch repo / trees, PASS with controls fired: anchor assertion of `apply1966.py` (including the half-state refusal that writes nothing), the blobs of the patched files, readers census, name scan (the project's `namescan.py`, controls fired), B-number / card-id / `card` word / owner-attribution / ticket-key / timer / RegExp / `existsSync` scans (drafter's `scan1966.py`, "drafter's list, not the project's"), non-ASCII and bidi, `node --check`, gitleaks (control fired after the `EXAMPLE` correction), red-first and green and four mutants in real jest, the bound (M4), the extraction of the kit's FILE blocks and a run of the kit's own `apply1966.py`.
**NEVER RUN on a real output (a failure the seat can trace to the kit's wording is `STOPPED: NEEDS TUESDAY`, not the seat's to amend):** the seat's rewritten tools (`judge.py`/`kept.py` specs for 8 cells, `mkplants.py`, `s2_red.sh`, `s_astep.sh`, `static.py`, `prepush.py`: they are copies of B1958's with this lane's shape, written by the seat); the lock steps and `chain.sh`; the full `npm run verify` at A (PREDICTED 6235 / 394, PASS); CodeQL (PREDICTED rc 0); the git verbs in the seat's own clone (`ls-remote`, `merge-base`, `show`, `fetch`, `worktree add`, `npm ci`: the `gh api -X GET` equivalents were run); the hosted Build and the Deploy demo run a landing starts.

## UNMEASURED
The real hosted rate of the race (one red in 20 builds is not a rate; the probe is an amplified instrument); behaviour on Linux; the verify's wall time under today's load; the `.tools/b1958/*` tool texts the seat must adapt; whether `catch (_e)` with an unused binding passes the project's lint (no lint file was found at the tarball root; the precedent `rd525-live-store.js:123` uses the same form); the INTERVAL cell's 60 s wait under real contention.

## Outside-the-fences disclosure
- jest was run in scratch trees under `d1966/` WITHOUT the jest lock (the commission's tree is read-only toward the project; the lock folder would be a project write): `queue-jest` was empty at every look, no jest or server process, no live NexusAI pane; load not recorded. Runs used `NODE_PATH` to `.tools/b1931/clone/node_modules` (read-only; a symlink would be a project-style write). Scratch bands (`proto_a` slot 14, `proto_b` slot 8) read empty by `lsof` before; the `base` tree (slot 13) was NOT read on its own before its one 14 s rd615 run (the machine-wide listener list taken minutes earlier held nothing in it).
- I ran the project's `.tools/b1958/namescan.py` in place (it reads git in my scratch repo and `gh api -X GET user` under the NexusAI `GH_CONFIG_DIR`; the login is never printed) and read `.tools/b1958/` files and logs (read-only).
- `git init` and two commits in a scratch repo `d1966/proto_repo` (local identity `scratch@invalid.example`, no remote, never pushed). Not a project repo.
- Jira: GET only, credentials by name in-process from the project `.env` (`jira_search1966.py`, `jira_issue1966.py`; nothing but issue rows printed).
- `sed -i.bak1966` on my own scratch `apply1966.py` (a rename-safe edit of my file, backup kept in scratch; never deleted) and `cp` over scratch preload copies inside `proto_b` (restored, blob proved). Skeleton sidecars from earlier builds were MOVED (not deleted) to `d1966/kit.measured.*`.
- A `cd` was typed once by mistake inside a `wc` command (the hook refused it; the intended command was re-issued without the `cd`); I read the `lsof`, `tmux list-panes` and `ps` states only.
- Hook advisories about case-sensitive greps and `cut` after grep were seen; every zero was paired with a control or is a returned line.
- No `decision_queue.sh`, no Wednesday/Friday tree, no `briefs_staged`, no scoreboard, no `_ledger.md` was read. No file was written outside `d1966/` except the kit, its sidecar and this report.
