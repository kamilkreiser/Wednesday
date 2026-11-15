STARTABLE: YES (after Tuesday's stamp; one scope call is wanted first, Q-1, with a default that lets it start)

# B1571 drafter report: HPSM-POC lane H-3, first slice, seat H165

Drafted 2026-11-15 13:05 to 13:14 AEDT (`date` printed 13:05:06, 13:05:34, 13:07:31, 13:08:40, 13:12:14, 13:13:21). Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1571_SEAT-H165_hpsmpoc-lane-h3-a11y-journey-margin.md` (76 lines), sidecar `...a11y-journey-margin.md.measured` (70 claims plus S01-S07, S21, S30), work folder `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s277/d1571/`.

## BLUF
- **Slice: HPSMPOC-470 point 1 only** (the accessibility journey test, `web/e2e/a11y.spec.ts:39`, runs under Playwright's 30 s default and sat at 26 to 28 s alone-in-the-author's-runs, and timed out at 30 s and 34.2 s under load: RELAYED from the ticket). The edit is one comment line and one `test.setTimeout(90_000);` in one test file; 90_000 is an existing bound (11 files in `web/e2e` set 60/90/120 s: MEASURED). The weight of the kit is the proof: a timing table (5 alone runs per viewport with load1 beside each), a red-then-green pair that can fail (CLI `--timeout=N` below the measured duration reds the old spec and leaves the new one green, because the in-file bound wins; a negative-control test at the same `N` is the control), the two e2e shards that hold the file, `--check-shards`, vitest names, the infra job's repo-wide scans, and CodeQL.
- **Why this item and not the others:** it is the only H-3 item that is buildable now with no ruling, one coherent file, one gate tier (G2, test-only), no SQL Server and no docker. See LEFT below.
- Base `b6c282ee50086bc1ac7d773ccabf00fcf8c055cc`. **One open PR: #318** (H-2, branch `b1565/hpsmpoc-forward-proof`, head `349f7a78f25cb1933214b277a80daa12bf9d15d3`): its 9 files share no path with this kit; the kit names it and carries A MOVED MAIN (re-run Step 2 census and Step 5 on a new base).
- Seat H165 (the highest earlier `SEAT-H<n>` by numeric sort is 164), pane `Datasec/HPSM-POC-H165`, branch `b1571/hpsmpoc-a11y-journey-margin`, ports 9890-9899 (WEB 9892, hosted 9893, stub 9894, chooser 9895), model Sonnet (`model-routing.md:92` row C2; gate G2 `:109`; id `claude-sonnet-5-5` at `models_latest.json:23`), launch line with `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.

## Scope: IN and LEFT
IN: HPSMPOC-470 point 1.
LEFT (each with its reason):
- **HPSMPOC-480** (deploy script, Kudu 504): the ticket's remedy is still "to be chosen" (a to d), it has **no comment at all** (jget printed the description only; no ruling id exists); its "default if the product owner does not answer: (a)" is the ticket's own, and Tuesday's s275 stamp on the sweep took all eight defaults, but that is not a ruling on the ticket. Option (a) also needs a real `az` call (a latest-deployment read) whose response shape the seat cannot measure (no az in the fences): the stub test would pin an unmeasured shape. If Tuesday confirms (a) as a ruling, 480 is the natural NEXT H-3 kit (script plus its stub test in `infra/tests/test_deploy_package.py`, python `infra` job).
- **HPSMPOC-470 point 4** (one SQL Server migration timeout seen once on main's squash of #310): a diagnosis ("add a test or record not reproducible"), needs both SQL Server shards run repeatedly in containers and `api/tests/`; a different CI job family and a different gate shape than a one-file e2e edit. Buildable (the ticket allows "not reproducible, recorded"; the seat must prove it by runs), but a mixed kit would need two gate tiers. Candidate NEXT H-3 kit, containers `g1571-*`-style names on a fresh block.
- **Point 3** (emoji cut, `remediation-store.ts:56`): lane H-1's. **Points 2 and 5**: "Not decided" (a 768 px cap edge not measured, a runtime pin vs float; comment 41128 is the point-5 note), layout or policy calls.

## PRIOR WORK (each count with its instrument and control)
- Open PRs: `pulls?state=open` -> 318 only; `pulls/318/files` -> 9 names, none under `web/e2e`; control `pulls/99999` -> 404; `state=all&per_page=3` -> 318 open, 317 and 316 closed.
- Branches: `matching-refs/heads/b1571` length 0; control `heads/b1541` length 1; `branches?per_page=100` paginated 333 names, loose pattern `a11y|1571|h165|journey|timeout|margin|470` 6 hits (`b75/journey-isolation`, `b219/demo-reset-upstream-timeout`, `b234/ci-api-timeout-25`, `b237/reset-timeout-words-w10`, `b905/hpsmpoc-timed-journey-first-spans`, `b1497/hpsmpoc-customer-look-a11y`): names read only, none is a bound on this test.
- `commits?path=web/e2e/a11y.spec.ts` newest six: `db179494` (2026-10-21), `0a85b89e`, `a89359c4`, `30299305`, `5e362ea9`, `c10fab25`; none touches a timeout. `setTimeout` count in the file at main: 0; control `walkthrough-uat.spec.ts` 1.
- Jira (my own GET helpers `jget.py`, `jsearch.py`; every JQL `project = HPSMPOC AND ( ... )`): 470 and 480 read whole (470: description plus comment 41128; 480: description, 0 comments); labels `landing-minor,rec-2026-11-11` and `follow-up,hosted-demo,rec-2026-11-12`; JQL for the three held labels with the two keys -> COUNT 0, control without the keys -> 27; related 110, 273, 282, 308 Done.

## Census by program (tests pinning what changes), frame: tracked files at main `b6c282ee`
| program | what | command and count | verdict |
|---|---|---|---|
| e2e ids | `a11y.spec.ts` | `playwright test --list a11y.spec` on a same-sha tree (the spec file `diff -q` identical to the tarball's) -> 6 tests in 1 file (3 per project, desktop and tablet; :39:5, :47:5, :72:5) | the journey id moves line numbers by the added lines only |
| shard map | which shard runs them | `--list --project=desktop --no-deps --shard=1/2` -> 182 tests, a11y rows 3 (so shard `journey-and-prototype`); `2/2` -> 181, 0; tablet `1/2` -> 182, 3 (so `prototype-tablet-1`); `2/2` -> 181, 0 | the seat runs those two shards whole; six others NOT RUN, with this reading |
| readers of the file | web unit, infra, scripts, workflows | `/usr/bin/grep -rn -F 'a11y.spec' web/src infra scripts .github` -> 0; control `-F 'journey.spec'` -> 2; `axe.ts:1` names it in a comment | nothing reads its text; `--check-shards` compares ids from the same `--list`, so moved lines stay consistent |
| e2e-runner unit test | `web/src/e2e-runner.test.ts` | reads only the `*-live-api.spec.ts` names (`:254-259`) | unaffected |
| infra | repo-wide scans (`test_hidden_characters.py` walks every tracked file) | not run by the drafter (no clone, no bicep) | the seat runs `validate.sh`, the scan alone and `unittest discover` at BASE and head |
| config | `playwright.config.ts` | top-level `timeout:` key lines (`^  timeout:`) -> 0; control `^  retries:` -> 1; four `timeout:` lines (77, 82, 89, 95) are web-server bounds | the 30 s default governs the test today |
| precedent | `test.setTimeout(60|90|120_000)` | 11 files in `web/e2e`, e.g. `walkthrough-uat.spec.ts:17`, `playbook-print.spec.ts:90` | 90_000 is an existing bound, not a new number |
| CodeQL | `javascript-security-extended.qls` over a copy of the BASE spec | ran `database create --build-mode=none` (rc 0) and `analyze` (rc 0): SARIF results 0, rules run 103 | the kit's command works on this box; the seat repeats it over `head` |

## Chain table (rule 4: every step's inputs against the producer)
| step | inputs | produced by |
|---|---|---|
| 0 | the kit, project identity, pinned node 24, Chromium | exist at BASE (Chromium under `~/Library/Caches/ms-playwright`, versions 1208, 1234, 1243: `ls` at 13:07) |
| 1 | `mut` clone, `gh` | step 0 |
| 2 | `mut` with `npm ci`, a `.next` build, ports 9890-9899; writes `base-unit.json` and the a11y timing JSONs | step 0; the build is step 2's own `npm run build`, listed BEFORE the timing runs |
| 3 | `head` clone, the Step-2 timing table (decides any extra test and the comment's numbers), then `npm run build` in `head` | steps 0 and 2; the build is made at the end of step 3 so step 4 can start `next start` and the standalone server |
| 4 | `mut` build (step 2), `head` build (step 3), the table (to choose `N`) | steps 2 and 3 |
| 5 | `head` build (step 3), `base-unit.json` (step 2), the BASE infra baseline taken in `mut` (step 2/5d) | steps 2 and 3 |
| 5e | CodeQL CLI, the suite file, the diff | exist on the box (version printed 2.27.4); step 3 |
| 6 | all green | steps 4, 5, 5e |
| 7 | the pushed sha, the evidence folder | step 6 |
Corrected during drafting: the first draft ran the `head` e2e proof before any `head` build existed; the build now sits at the end of Step 3.

## Facts re-measured with instruments
- main sha `b6c282ee...` (`gh api branches/main`, 13:05 and re-read 13:08), commit time 2026-11-14T20:34:40Z; same sha as the H-2 drafter's base, no movement.
- Ports 9890-9899: `lsof -nP -iTCP:9890-9899 -sTCP:LISTEN` 0 rows; control the unfiltered list 21 rows. Word-boundary scan `(^|[^0-9A-Za-z-])989[0-9]([^0-9A-Za-z-]|$)` over 19 non-`.pre-` SEAT kits of 14 and 15 Nov (the listing is `kits.txt` in the work folder; the 19 is the count of that list's files whose name starts `2026-11-14_` or `2026-11-15_`, after excluding `.measured` sidecars) -> 0 in each; control: the pattern with `981[0-9]` over the B1565 kit -> 2. Pane list `tmux list-panes -a` at 13:07: `%0 wednesday`, `%28 Datasec/Security-Composer-C101`, `%25 Datasec/MPS-M137`, `%22 Datasec/NexusAI-N130`, `%19 Datasec/NexusAI-N129`, `%13 Datasec/NexusAI-N128`, `%1 fleet-monitor` and unnamed panes: no HPSM-POC pane. Load `LC_ALL=C uptime` 13:11: 9.65 8.92 8.70 (five other seats are live, so the kit stays on the load gate).
- Seat id: `ls briefs | grep -o 'SEAT-H[0-9]*' | sort -n` -> highest 164.
- Model rows: `model-routing.md` lines 92 (C2), 93 (C3), 109 (G2) by `grep -n`; ids from `models_latest.json:23`.
- CI predicates (S21) read at `ci.yml` 396, 409, 413, 426, 478, 494, 518, 630 and `e2e.mjs:65-67`, `playwright.config.ts:49`. Pass predicate of the e2e step: exit 0 of `node scripts/e2e.mjs --shard "$SHARD"`; CI retries 1, so a flaky pass is green to the job: the kit makes the seat print flaky rows and set `CI=1`.

## D-decisions (made in the kit, each reversible by Tuesday at the stamp)
- D-1 The bound is `test.setTimeout(90_000);` as the first statement of the journey test (precedent: 11 files). A test of the file gets one only if its measured slowest alone run exceeds 15 000 ms (closed list stated as a property, then "at least the journey test"; any other shape is prove-or-STOP). No config change, no `test.slow()`, no retry, no edit to `journey.ts` (shared with the timed journey whose budgets are the product's timing claim, HPSMPOC-110) or any other spec.
- D-2 Red-first is a pair, not a made-up load: CLI `--timeout=N` (below the journey's smallest alone duration, above the setup cost, with the negative-control test at the same `N` as the control that `N` is not simply too small) must read the old spec red by `Test timeout of <N>ms exceeded` and the new green; plus a scratch `1_000` variant that must go red again. The seat starts no load burner (five other seats share the machine).
- D-3 The comment line carries the seat's own measured numbers and no ticket key, brief number, seat name or person.
- D-4 Two clones only (`mut`, `head`), no `repo` clone; no containers; no dotnet.
- D-5 The e2e proof is the two shards that hold the file, whole, with `CI=1`; the other six are NOT RUN with the reading from the `--list` census.

## QUESTIONS FOR TUESDAY (each with a default)
- **Q-1 Scope call.** HPSMPOC-470 says for point 1 "Not decided: whether to widen the journey test's margin". The sweep lists it as buildable in H-3 and Tuesday read the sweep. A bound on one test changes no product behaviour and adds no word. Default: build it (the kit as written). If Tuesday wants the product owner's word first, the kit is not startable and the next item is 480 or point 4.
- **Q-2 Is HPSMPOC-480 ruled?** Default: no (no ticket comment); LEFT. If Tuesday records option (a) as the ruling, draft 480 as the next H-3 kit.
- **Q-3 Point 4 as the next H-3 kit** (migration-timeout diagnosis with SQL Server containers, "not reproducible, recorded" a valid end). Default: yes, separately, after this one or beside it on a fresh port block (no shared file with this kit).
- **Q-4 Hard stop and window.** READY target 180 minutes after Step 0; launch window and hard stop clocks are Tuesday's slots. With five panes live and load near 9-10, the e2e shards may run slowly; the kit already names a load red with its cause and a re-run alone at BASE and head.

## UNMEASURED
- Everything the seat runs: no build, no browser, no test was run by the drafter. In particular the alone durations of the three tests (the ticket's 26 to 28 s and 15 s are RELAYED), the `--timeout`-versus-`test.setTimeout` pair (a documented Playwright behaviour, not run here; the kit stops the seat if the pair does not read red then green), that the JSON reporter's standard output parses cleanly (the kit has the first run prove it; the drafter could not find the old `PLAYWRIGHT_JSON_OUTPUT_NAME` variable in Playwright 1.63.0's `lib` and so tells the seat to redirect stdout), and the infra job at main in a real clone.
- The hosted CodeQL suite name `extended` and the languages are RELAYED from the H-2 drafter's read; the local run used `javascript-security-extended.qls` as the nearest local suite.
- The landing-rule quote ("The landing form is a head-pinned squash", CLARIFICATIONS.md line 3617) is RELAYED from the H-2 kit.
- Whether #318 lands during the seat's work (A MOVED MAIN covers it).

## Outside-the-fences disclosure
Reads: `DRAFTER_RULES.md`, the sweep (grep plus sections 1 and the questions), the H-2 kit and drafter report, the gate standard (step 7 line), `model-routing.md`, `models_latest.json`, tickets 470 and 480 via my own GET-only Jira helpers (a copy of the H-2 drafter's `jget.py` and `jsearch.py` in my work folder; credentials read in-process from the project `.env`, never printed), `gh api -X GET` under the project's `GH_CONFIG_DIR` (branch, pulls, pulls/318/files, tarball of main, commits for one path, branch list). Local runs in my work folder only: tarball extraction; Playwright `--list` through the node_modules of the H-2 drafter's same-sha tree (read-only use, `--list` writes nothing); one CodeQL database create and analyze over a one-file copy of the BASE spec (database and SARIF under `.../d1571/cq_db`, `cq_out.sarif`); `lsof`, `tmux list-panes`, `uptime`. One accidental `git -C` read of the OUTER repository log (the work folder sits inside the coordinator repo): read verb, no write. No Jira write, no git write, no GitHub write, no file under `/Volumes/Datasec_DEV/!CODING/`, no message, no tmux send-keys, no az, no docker, nothing deployed; no decision card, no `_ledger.md`, no other client's tree, no WEDNESDAY or FRIDAY tree read. Two earlier sidecar skeletons were moved (not deleted) to the work folder (`measured.first-init`, `measured.second-init`) when the kit text changed.

DRAFTED B1571: kit 76 lines, sidecar rc 0, questions 4
