STARTABLE: YES

# B2088 DRAFTER REPORT: Datasec/NexusAI, RD-974 (the automatic-insights check reads a job's start time), seat N175

Drafted by an in-session READ-ONLY drafter for Tuesday (s327). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-25_B2088_SEAT-N175_nexusai-nxt2-rd974-job-start-time.md` (sidecar `.measured` beside it). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s327/d2088/` (frozen files in `frozen/`, runs in `laneT/`, `raw/`, `logs/`, `cq/`). Clocks: first `date` 15:00:45 AEDT, last at the foot.

## BLUF
- **Startable.** BASE is origin main `a3f72428`. The kit builds RD-974 as ONE product file (`backend/server.js`, 29 lines added, 14 removed), ONE existing test file re-pinned (`rd798`, 19 added, 16 removed), ONE new test file (20 cells), the counts file. The whole chain was dry-run end to end: red-first (16 named cells red at BASE), green (4306 of 4306 in 228 suites), red-proof (the same 14 red), the full verify (6449 of 6449 tests across 404 suites, `VERDICT: PASS`), the static checks, gitleaks, local CodeQL (rc 0).
- **The design choice (Q-2): your provisional default stands, and the measurement sharpens it.** No writer anywhere in `backend/` fills the bare field `Job_Start_Time`; every store fills `Job_Start_Time_UTC`. So reading `Job_Start_Time` alone (the ticket's literal code) would leave every real and seeded row undated, and the check would never fire on real data. The default reads `Job_Start_Time`, then `Job_Start_Time_UTC`; a row with neither (or an unparseable one) is left out of the hour check and the day/week buckets and is never stamped with the time of the read; it still counts in the user's totals.
- **What the demo's off-hours paragraph shows (finding 5, run by program with the real function and the 1445 seeded rows):** BASE at 23:00: "1445 jobs during off-hours (10 PM - 6 AM)"; BASE at 12:00: no item at all. Default: the same item at either clock, "60 jobs ..." in a UTC server (676 in `Australia/Sydney`). It is a red item at every hour of the day, with the seed's own count. That is a visible demo change once deployed: it is Q-7, and your landing read.
- **The re-pin is real work, not a one-liner (Q-3).** With the default read and rd798 unchanged, 3 cells go red (`C-BODY-HOURS LIVE`, `IN 190`, `OUT 190`; the B2074 drafter's probe found 2 with a different fix). Route 190 no longer reads the clock, and the count inside its paragraph depends on the child's time zone, which rd798 derives from the real UTC hour: a fixed hash would pin a number that changes with the hour the test runs. The kit runs rd798's child in UTC (`TZ: 'Etc/UTC'`), re-pins the two 190 hashes (the same in both states), retitles three cells and checks the live cell's logger hour against the real UTC hour.

## FACTS RE-MEASURED AT SOURCE (instrument; control)
| fact | instrument | control or note |
|---|---|---|
| BASE `a3f72428241c3e41799f5c11c16b7447fdf521c4`, tree `49e3ed45...`, parents `b1c2f76e` and `8a2d2b88`, 2026-11-25T14:29:32+11:00; open PRs 0; `matching-refs/heads/b2088` 0 | `gh api -X GET` (ref, pulls, matching-refs) and `git rev-parse` in the drafter's clone after `git fetch` of origin main | control `matching-refs/heads/b2077` read 1 |
| counts at BASE `tests` 6429, `suites` 403 | `cat scripts/verify-expected-counts.json` in the BASE clone | the K pair measured below |
| the two readers are server.js lines 20314 and 20419 at BASE (22841 lines, blob `6f811c17...`); the only two now-fallbacks of a job time in `backend/` | `awk NR==n`; Python `re` over the file (`Job_Start_Time ... Date.now()`) and `git grep` over the other `backend/` files | control: the 3 `TimeGenerated \|\| Date.now()` lines of `azureLogAnalytics.js` fire the second pattern and are ids, not times |
| no writer of the bare `Job_Start_Time` in `backend/`; writers of `_UTC` at `azureLogAnalytics.js` 1237, 1378, 1758, 2137, `seedDemoData.js` 34, `simpleDb.js` 67, 212, 372; the seed CSV has 1445 rows, a `_UTC` column, no bare column, 0 empty starts | `git grep -n -E 'Job_Start_Time' <BASE> -- backend`; `csv.DictReader` over `scripts/seed/demo-printer-logs.csv` | control: the `_UTC` writers print; the CSV header read both ways |
| route 190 at BASE (rd798 old pins, one jest run, the product edits only): 3 red of 65 | jest under the lock (`probe1`, 8 s) | the other 62 passed |
| answer at UTC hour 4 with the edits: day state "494 jobs", night state "158 jobs", both "Critical Issues (8)" | a throw-away dump test run under the lock (quarantined) | matches the program count by offset (offset 8: 494; offset 22: 158) |
| the demo text by clock and zone (finding 5) | `demo2088.js` (the real function lifted, `Date` patched, `TZ` set): BASE 1445 / none, edited 60 / 60 (UTC), 676 / 676 (Sydney) | per-zone program count over the seed: UTC 60, Sydney 676, `Etc/GMT-4` 163; least over 24 offsets 57 |
| new test file: 20 cells; at BASE 14 red, 6 green; edited 20 of 20; red-proof the same 14 | `judge2088.py` over the jest JSON of `lane2088.sh` end to end (`laneT/logs/lane.out`) | the judge refused all six wrong-mode pairings and a renamed cell title (it FAILED once on my own rename of cell S2 and I rebuilt it) |
| green set: 227 suites listed, 228 run with the new file, **4306 of 4306 passed** | jest JSON; the two parked paths under `__tests__/helpers/` that `jest.config.js` ignores were dropped from the list | first run listed 229 and read 228 |
| full verify at prototype A `ffcf03c7c00b928f9134916a7ff249011ec51308` | `v2088.sh update` under the lock (`laneT/logs/verify-update.log`) | `Test Suites: 404 passed`, `Tests: 6449 passed`, `VERDICT: PASS`, `EADDRINUSE` 0 (control: 1 VERDICT line), 15:35:08 to 15:57:15; the counts file moved by +20 tests and +1 suite only (BASE 6429 / 403); **K must carry 6449 / 404** |
| static A: `STATIC A PASS`, 19 OK lines; gitleaks A: no leaks found | `static2088.py A`; `gitleaks stdin` | control inside: planted e-acute, U+202E, ids, names fire; the planted AWS-shaped pair read `leaks found: 2`; static first FAILED on its own ordering check (git and difflib pair lines differently: now sorted-list compare, with the byte-for-byte blob check as the order proof) |
| local CodeQL at A (base BASE): `diff pack: 3 files with added lines, 16 ranges`; head 29, base 29; KEPT 0, NEW 0, GONE 0; rc 0; `cq.err` 0 bytes | `pr_codeql_check.sh` 15:23:16 to 15:24:23 | at the prototype K the same: diff pack 4 files, 17 ranges, KEPT 0, NEW 0, rc 0 |
| slots `b2088-nodot/rf` 15, `work` 6, `vupd` 1, `chk` 7; 0 listeners in the four bands | Python port of `worktreeSlot`; `lsof` | control `b2077-nodot/rf` printed 17 (that kit's recorded slot); the awk filter counted 2 in a band around a known listener |
| seat id N175 free | word scan of 40 non-`.pre-` SEAT kits of 24 and 25 Nov | N174 in 2, N173 in 3 |
| model routing rows C2 (line 92), G1 (108), G2 (109); model id `claude-sonnet-5-5` (models_latest.json line 23) | `sed -n` over the table | |
| deploy: `deploy-demo.yml` `on:` 26, `paths-ignore:` 29, build `if` 53, deploy `if` 91, `environment: demo` 95; `backend/**` and `__tests__/**` not ignored | `awk NR==n` | the landing read is yours |

## D-DECISIONS (mine, each overridable)
- **D-1: two fields, not one.** See BLUF. A third option, reusing the file's `_jobDate` (11537), would add `Job_Start_Time_Local`, `TimeGenerated` and `created_at`; `created_at` is the time a row was stored, the very defect RD-975 fixed in the business-hours report, so it is not used.
- **D-2: the buckets are in scope.** The ticket's own recommendation names them ("the check and the buckets") and its text says "the same pattern is at 19984". An undated job is left out of the day and week buckets and out of `firstSeen`/`lastSeen` (null for a user with only such jobs), and stays in jobs, sheets and pixel totals. Measured: at BASE three undated jobs of 100 sheets read as a high day (B1).
- **D-3: a bad time no longer stops the run.** At BASE a non-date `Job_Start_Time` threw in `toISOString()` and the whole insights call returned its error object. Now it is undated. Pinned by U1 (4 shapes, all red at BASE).
- **D-4: the rd798 re-pin runs the child in UTC** (Q-3). The helper `zoneForLocalHour` and its `HOUR-ZONE` cell are kept untouched.
- **D-5: no change to the `hour > 22` test, the threshold 10, the stores or any other reader** (Q-5, Q-6).
- **D-6: the red-first `rf` run carries the re-pinned rd798 as well as the new file**, so the three re-pinned cells are shown to pin the new answer (IN 190 and OUT 190 red at BASE always; LIVE red at UTC hours 6 to 22 and green otherwise; the judge derives LIVE from the run's own start time; I ran at UTC hour 4, LIVE green).
- **D-7: G2 gate, not G1,** because RD-975's gate (G2) measured the same mechanism; widen to G1 if the seat goes past the listed places.

## Q-QUESTIONS FOR TUESDAY (each with a default)
- **Q-1 (model).** Builder C2 Sonnet (`model-routing.md` line 92), gate G2 (line 109); G1 (line 108) only if the seat widens past the listed places. Default: C2 + G2, `BRIEF_SEAT_LEVEL=sonnet`, model id `claude-sonnet-5-5`.
- **Q-2 (does `Job_Start_Time_UTC` count as a job's start time?).** Default **YES**: read `Job_Start_Time`, then `Job_Start_Time_UTC`; a row with neither is left out. Your provisional default is confirmed, not overturned: the bare field has no writer, so the ticket's literal code reads nothing. Alternatives: reuse `_jobDate` (adds `created_at`: rejected), or `Job_Start_Time` only (the check goes dead on real data).
- **Q-3 (the rd798 file in the partition; how to re-pin).** Default **ACCEPT**: ten edits by `apply2088.py` (child `TZ: 'Etc/UTC'`, LIVE cell, two hashes, three titles, comments). Alternative: keep the derived zone and mask the count in the 190 cells (rejected: RD-980 removed that mask because it pinned nothing; the count is now data, not clock).
- **Q-4 (buckets and totals).** Default **ACCEPT** D-2: undated jobs out of the day/week buckets, still in the totals; `firstSeen`/`lastSeen` may now be null for a user with only undated jobs (no consumer in `static/` reads them: `git grep` over `static` and `backend` outside `server.js` found none; the LLM context sees them in `topUsers`).
- **Q-5 (`hour > 22` against the text "10 PM - 6 AM").** The code counts hours 0-5 and 23 only (22:xx jobs are not counted) while the item says 10 PM. Default: **report only, do not change** (it moves the demo count; not in the ticket). A one-line follow-up if you want it.
- **Q-6 (other readers).** Seven other lines read the bare field with no now-fallback (server.js 7349, 9114, 9297, 11318, 16268, 16327, 20851, plus 6079): they miss `_UTC` rows today. Default: **left alone** (RD-695 family, a different function); named for the records pass.
- **Q-7 (deploy and the visible demo change).** A merge starts `Deploy demo` (paths not ignored); both jobs need `CI_DEPLOY_ENABLED == 'true'` and the last runs of the workflow have all skipped. Once the demo is ever deployed with this change, its key-insights answer shows the red off-hours paragraph at every hour. Default: **nothing deploys here; your landing read decides; the C-224 hold stands.** Tell Kam only if you consider the demo text a product matter.

## STEP INPUTS (rule 4 of MEASURED LITERALS)
| step | inputs | made by |
|---|---|---|
| Step 0 | this kit, the report, the frozen folder | Tuesday, drafter |
| Step 1 | origin main, the project checkout, deploy key, lock base | project |
| 1b | clone at BASE, `apply2088.py`, `demo2088.js`, the seed CSV | Step 1, Step 0 |
| 0 `trees` | clone, frozen files | Step 1, Step 0 |
| 3 `lane` | `rf`, `work`, `suites2088.txt`, judge, `apply2088.py` | step 0 |
| 4 A | `work`'s three files, `static2088.py`, `msg-A.txt` | step 3 |
| 5 update | A | step 4 |
| 6 K | `vupd`'s counts file, `msg-K.txt` | step 5 |
| 7 plain | K | step 6 |
| 8, CQ, push | clone, K | step 7 |

## UNMEASURED
The seat's clone and `npm ci`; the plain verify at K (its pair PREDICTED equal to the update run's 6449 / 404); the push; the hosted demo's time zone and its data; a number or a Date object as a start field; a real browser or the HTTP route (`/api/key-insights`); the hosted Build and CodeQL on the merge commit; Linux. The `6449`/`404` fill of `msg-K.txt` was dry-run on the prototype K.

## OUTSIDE-THE-FENCES DISCLOSURE
- **Read:** the commission, `DRAFTER_RULES.md`, kits B2074 and B2077 (whole), the B2074 report's RD-974 lines, `NEXT-PICKUP-TUESDAY.md` lines 60-64 (the commission's own pointer), the model-routing rows, `models_latest.json` line 23, `CLARIFICATIONS.md` line 2067 and `grep -n` for RD-974 (never whole), `grep -n RD-306` over `backend/azureLogAnalytics.js`, RD-974 by the B2077 drafter's GET-only reader (`jwhole.py`, in-process `.env` read, no token printed), `gh api -X GET` only under the project's `GH_CONFIG_DIR`. No card store, ledger, `briefs_staged/`, scoreboard, Wednesday/Friday tree or other client read. No HTTP to any hosted host.
- **Wrote (scratch only):** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s327/d2088/` (a clone of the project checkout with its origin re-pointed to GitHub and a repo-local `core.sshCommand`, `git fetch` of origin main INSIDE that clone only; five worktrees; a scratch identity `d2088 scratch` in that clone's config, never in a project repo; the prototype commits A and K never pushed; `node_modules` symlinks to the B2032 drafter's tree), and the lock base `session-tools/locks-laptop-1017` (the jest lock's own ticket and owner files for my acquisitions: `d2088-probe1` to `-probe5`, `d2088-lane` twice, `d2088-verify-update`). Nothing written to the project checkout, Jira, GitHub or any card store; nothing sent to any human.
- **Jest load:** every jest run inside the lock, `--maxWorkers=2`, `NODE_OPTIONS` unset, dot-free trees; the live records seat R323 (pane `Datasec/NexusAI-R323`) runs no jest. The lane acquisition took 12 min 28 s (15:22:35 to 15:35:03); a first lane run stopped at its judge on a test-title rename of mine (the control fired) and was rerun.
- **Hook refusals met and obeyed:** `git -C "$VAR"` write verbs (refused: literal paths only), `rm` (refused: I moved a probe file to `_quarantine/`), foreground `sleep`, an unquoted `set -- $pair`, `grep -P` (not on macOS).
- **Files left in scratch for you:** `frozen/` (10 files), `kit.draft.md`, `probe*.sh`, `run-*.sh`, `mk_measured88.py`, `census_tz.js`, `_quarantine/`.

## Foot
Kit: 164 lines, sha256 prefix 750babf195c623fe, 142 claims in the sidecar, 142 measured, `stamp_check.py` exit 0 (run alone, rc printed on its own line). Unstamped copy reads 5 lines with the four-underscore pattern (4 slots and the last line); `READ-WHOLE-BY-TUESDAY: ____` is the last line. Prototype commits (scratch, never pushed): A `ffcf03c7c00b928f9134916a7ff249011ec51308`, K `bec9cc53ef6096dc89f5a84560396b477f99189f`. Frozen folder: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s327/d2088/frozen/` (10 files; the sha256 table is in the kit). Last `date`: Wed 25 Nov 2026 15:59:26 AEDT
